# CAF-AI

Italian IMU (property tax) calculator with a conversational chat interface.

**Stack:** Python / FastAPI / Docker

**Current focus:** IMU calculator proof of concept — chat in Italian, get accurate IMU calculations with explanations.

## Docs

- [TECH-PLAN.md](TECH-PLAN.md) — technical plan and build order
- [docs/imu/imu-calculation.md](docs/imu/imu-calculation.md) — IMU formula, coefficienti, rules, worked examples

## Status

Setting up. Build order:
1. IMU calculator (pure Python)
2. Torino aliquote data
3. Chat engine (LLM conversation layer)
4. FastAPI API
5. Docker + deploy to VPS
