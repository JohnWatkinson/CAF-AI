"""
FastAPI app — chat endpoint for the IMU assistant.
"""

import os
import uuid
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

from src.chat.engine import ChatEngine

app = FastAPI(title="CAF-AI IMU", version="0.1.0")

# CORS — allow Lovable frontend or any frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store (Redis later)
sessions: dict[str, ChatEngine] = {}

API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Conversation log — one JSONL file per day
LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
LOG_DIR.mkdir(exist_ok=True)


def log_exchange(session_id: str, user_msg: str, assistant_reply: str):
    """Append a conversation exchange to the daily JSONL log."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "session": session_id[:8],
        "user": user_msg,
        "assistant": assistant_reply[:500],
    }
    try:
        with open(LOG_DIR / f"{today}.jsonl", "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        log.warning("Failed to write conversation log: %s", e)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not configured")

    # Get or create session
    session_id = req.session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = ChatEngine(api_key=API_KEY)
        log.info("New session: %s", session_id[:8])

    engine = sessions[session_id]

    try:
        reply = engine.send_message(req.message)
    except Exception as e:
        log.error("Chat error [%s]: %s", session_id[:8], e, exc_info=True)
        raise HTTPException(status_code=500, detail="Errore durante l'elaborazione. Riprova.")

    log_exchange(session_id, req.message, reply)
    return ChatResponse(reply=reply, session_id=session_id)


@app.post("/reset")
def reset(session_id: str):
    if session_id in sessions:
        sessions[session_id].reset()
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}


# Serve static UI
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")
