# CAF-AI

Italian IMU (property tax) calculator with a conversational chat interface.

**Stack:** Python / Claude API / FastAPI / React / Docker
**Live:** `https://caf-ai.maisonguida.com` (beta)

## Status

1. ~~IMU calculator (pure Python)~~ — done, 84 tests passing
2. ~~Aliquote data (10 comuni)~~ — done (Torino, Roma, Milano, Napoli, Palermo, Genova, Bologna, Firenze, Bari, Catania)
3. ~~Chat engine (Claude + tool use)~~ — done
4. ~~FastAPI API~~ — done
5. ~~Lovable frontend (React)~~ — done
6. ~~Docker (two containers + nginx)~~ — done
7. Deploy to VPS — next

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your ANTHROPIC_API_KEY
```

## Run Locally

```bash
# Docker (recommended) — http://localhost
docker compose up --build

# Or without Docker:
uvicorn src.api.main:app --port 8000   # API only
python scripts/chat_cli.py             # CLI chat
```

## Run with Docker

```bash
cp .env.example .env   # add ANTHROPIC_API_KEY
docker compose up --build
# http://localhost (or http://localhost:8080 if APP_PORT=8080)
```

Two containers: backend (FastAPI) + frontend (React + nginx). Nginx proxies `/chat`, `/reset`, `/health` to backend.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/chat` | Send message `{"message": "...", "session_id": "..."}` |
| POST | `/reset` | Clear session `?session_id=...` |
| GET | `/health` | Health check |

## Run Tests

```bash
pytest tests/ -v
```

Test cases are YAML-driven — add new scenarios by editing files in `tests/fixtures/`.

## Config

| Setting | File | Notes |
|---------|------|-------|
| LLM model | `src/chat/engine.py` | MODEL variable at top. Default: Claude Sonnet 4.5 |
| Aliquote | `data/aliquote/*.json` | Per-comune rates (10 comuni), add more as JSON files |
| National figures | `data/imu_national.json` | Coefficienti, rivalutazione, sconti nazionali |
| System prompt | `src/chat/prompts.py` | Italian chat tone and rules |
| Port | `.env` → `APP_PORT` | Defaults to 80. Set to 8080 on VPS |

## Project Structure

```
src/calculator/   → Pure Python IMU math (no dependencies)
src/chat/         → Claude conversation layer (tool use)
src/api/          → FastAPI + logging
frontend/         → Lovable React UI (Vite + Tailwind + shadcn/ui)
data/             → JSON: national figures + per-comune aliquote
tests/fixtures/   → YAML test cases
logs/             → Conversation logs (JSONL, one file per day, not in git)
```

## Logging

- Backend logs: `docker compose logs -f backend`
- Conversation logs: `logs/YYYY-MM-DD.jsonl` (persisted via Docker volume)
- Retries: frontend auto-retries on network failures and 500s (2x, backoff)

## Docs

- [TECH-PLAN.md](TECH-PLAN.md) — technical plan and build order
- [docs/imu/imu-calculation.md](docs/imu/imu-calculation.md) — IMU formula, coefficienti, rules, worked examples
- [docs/deployment/vps-deployment.md](docs/deployment/vps-deployment.md) — VPS deployment guide

## Notes

https://www.comune.torino.it/argomenti/tasse-tributi/imu
