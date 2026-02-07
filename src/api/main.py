"""
FastAPI app — chat endpoint for the IMU assistant.
"""

import os
import uuid
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

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

    engine = sessions[session_id]
    reply = engine.send_message(req.message)

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
