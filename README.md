# CAF-AI

Italian IMU (property tax) calculator with a conversational chat interface.

**Stack:** Python / FastAPI / Docker

## Docs

- [TECH-PLAN.md](TECH-PLAN.md) — technical plan and build order
- [docs/imu/imu-calculation.md](docs/imu/imu-calculation.md) — IMU formula, coefficienti, rules, worked examples

## Status

1. ~~IMU calculator (pure Python)~~ — done, 24 tests passing
2. ~~Torino aliquote data~~ — done (2025/2026 rates)
3. Chat engine (LLM conversation layer) — next
4. FastAPI API
5. Docker + deploy to VPS

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
```
