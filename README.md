# CAF-AI

Italian IMU (property tax) calculator with a conversational chat interface.

**Stack:** Python / Claude API / FastAPI / Docker

## Status

1. ~~IMU calculator (pure Python)~~ — done, 24 tests passing
2. ~~Torino aliquote data~~ — done (2025/2026 rates)
3. ~~Chat engine (Claude + tool use)~~ — done
4. FastAPI API — next
5. Docker + deploy to VPS

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Tests

```bash
pytest tests/ -v
```

## Run Chat (CLI)

```bash
# Add your Anthropic API key to .env (see .env.example)
python scripts/chat_cli.py
```

Uses Claude Sonnet 4.5. Model can be changed in `src/chat/engine.py` (MODEL variable at top).

## Docs

- [TECH-PLAN.md](TECH-PLAN.md) — technical plan and build order
- [docs/imu/imu-calculation.md](docs/imu/imu-calculation.md) — IMU formula, coefficienti, rules, worked examples

## Notes

https://www.comune.torino.it/argomenti/tasse-tributi/imu
