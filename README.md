# CAF-AI

Italian IMU (property tax) calculator with a conversational chat interface.

**Stack:** Python / Claude API / FastAPI / Docker

## Status

1. ~~IMU calculator (pure Python)~~ — done, 24 tests passing
2. ~~Torino aliquote data~~ — done (2025/2026 rates)
3. ~~Chat engine (Claude + tool use)~~ — done
4. ~~FastAPI API~~ — done
5. ~~Simple web UI~~ — done
6. ~~Docker~~ — done
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
# Web UI (http://localhost:8000)
uvicorn src.api.main:app --port 8000

# CLI chat (terminal only)
python scripts/chat_cli.py
```

## Run with Docker

```bash
docker compose up --build
# http://localhost:8000
```

Requires `.env` with `ANTHROPIC_API_KEY`. See `.env.example`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Chat web UI |
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
| Aliquote | `data/aliquote/torino_2025.json` | Per-comune rates, add more comuni as JSON files |
| National figures | `data/imu_national.json` | Coefficienti, rivalutazione, sconti nazionali |
| System prompt | `src/chat/prompts.py` | Italian chat tone and rules |

## Project Structure

```
src/calculator/   → Pure Python IMU math (no dependencies)
src/chat/         → Claude conversation layer (tool use)
src/api/          → FastAPI + simple web UI
data/             → JSON: national figures + per-comune aliquote
tests/fixtures/   → YAML test cases
```

## Docs

- [TECH-PLAN.md](TECH-PLAN.md) — technical plan and build order
- [docs/imu/imu-calculation.md](docs/imu/imu-calculation.md) — IMU formula, coefficienti, rules, worked examples

## Notes

https://www.comune.torino.it/argomenti/tasse-tributi/imu
