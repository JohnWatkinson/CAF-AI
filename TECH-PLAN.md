# Tech Plan — IMU Calculator PoC

**Date:** February 7, 2026
**Status:** Active
**Stack:** Python / FastAPI / Docker

---

## Goal

Chat-based IMU calculator. User talks in Italian, system guides them through the calculation, returns accurate IMU with explanation. Simple, correct, deployable.

---

## Architecture

```
User (chat) → FastAPI API → LLM (conversation) → IMU Calculator (pure Python)
                                ↓
                         Aliquote Data (JSON → eventually DB)
```

### Principles
- **No agent frameworks** — plain Python, no CrewAI/LangChain
- **Calculation is deterministic** — never let the LLM do math
- **LLM handles conversation only** — parse user input, explain results, guide the flow
- **Designed to grow** — clean separation so we can add WhatsApp/Telegram, more tax types, DB, scraper later

---

## Components

### 1. IMU Calculator (`calculator/imu.py`)
Pure Python. Takes structured input, returns structured output.

**Input:**
- rendita_catastale (float)
- categoria_catastale (str)
- aliquota (float)
- percentuale_possesso (float, default 100)
- mesi_possesso (int, default 12)
- sconto (float, default 0)

**Output:**
- base_imponibile
- imu_annuale
- acconto (50%)
- saldo (50%)
- breakdown of each step

**Also includes:**
- Coefficienti lookup table
- 15-day rule helper (given a date + month length → who pays that month)

### 2. Aliquote Data (`data/aliquote/`)
- `torino.json` — start here, manually compiled
- Structure: `{ "comune": "Torino", "anno": 2025, "aliquote": { "abitazione_principale_lusso": 0.6, "altri_fabbricati": 1.06, ... } }`
- Later: scraper fills this for all comuni, or migrates to DB

### 3. Chat Layer (`src/chat/`)
- `engine.py` — ChatEngine class, manages conversation with Claude API
- `prompts.py` — Italian system prompt (tu, one question at a time, never calculate)
- `tools.py` — tool definitions for Claude + execution mapping to calculator
- Claude Sonnet 4.5 with tool use — LLM collects inputs, calls `calculate_imu()`
- Also exposes `calculate_mesi_possesso` and `get_aliquote_comune` as tools

### 4. API (`src/api/main.py`)
FastAPI app with:
- `POST /chat` — takes message + session_id, returns assistant reply
- `POST /reset` — clear a session
- `GET /health` — health check
- `GET /` — serves simple chat UI
- Session state stored in memory (dict) for PoC, Redis later
- CORS enabled for Lovable frontend

### 5. Simple UI (`src/api/static/index.html`)
- Single HTML file, no framework, no build step
- Chat interface that calls `POST /chat`
- Temporary — Lovable replaces this later

### 6. Docker
- `Dockerfile` — Python 3.11 slim, uvicorn on port 8000
- `docker-compose.yml` — single service, .env for API key
- Ready to add nginx, Redis, Postgres containers later (same pattern as fashion-starter)

---

## Project Structure

```
CAF-AI/
├── docs/imu/                  # Specs (this file, calculation doc)
├── data/
│   ├── imu_national.json        # Coefficienti, rivalutazione, sconti nazionali
│   └── aliquote/
│       └── torino_2025.json     # Torino rates (confirmed 2026)
├── src/
│   ├── calculator/              # ✅ Done
│   │   ├── imu.py               # Pure calculation logic
│   │   └── coefficienti.py      # Category → coefficient lookup, data loader
│   ├── chat/                    # ✅ Done
│   │   ├── engine.py            # ChatEngine — Claude API conversation
│   │   ├── prompts.py           # Italian system prompt
│   │   └── tools.py             # Tool definitions + execution
│   └── api/                     # ✅ Done
│       ├── main.py              # FastAPI app
│       └── static/
│           └── index.html       # Simple chat UI (Lovable replaces later)
├── tests/
│   ├── fixtures/                # ✅ YAML-driven test cases
│   │   ├── calc_basic.yaml
│   │   ├── calc_partial_ownership.yaml
│   │   ├── calc_partial_year.yaml
│   │   ├── calc_sconti.yaml
│   │   ├── calc_15day_rule.yaml
│   │   └── calc_edge_cases.yaml
│   └── test_imu.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## Build Order

1. ~~**IMU calculator**~~ — done. 24 tests passing. Pure Python, YAML-driven test fixtures.
2. ~~**Torino aliquote JSON**~~ — done. 2025 rates (confirmed same for 2026).
3. ~~**Chat engine**~~ — done. Claude Sonnet 4.5 + tool use. CLI + web UI working.
4. ~~**FastAPI API**~~ — done. POST /chat, session management, CORS.
5. ~~**Simple UI**~~ — done. Single HTML chat interface served by FastAPI.
6. ~~**Docker**~~ — done. Single container, docker-compose.
7. **Deploy to VPS** — nginx, same pattern as fashion-starter ← **next**
8. **Scraper** (later) — populate aliquote for more comuni

---

## Future Growth Path

- WhatsApp / Telegram bot (connect to same API)
- Document upload (parse visura catastale / previous F24)
- Full aliquote DB (Postgres) with yearly scraper from MEF
- Additional tax types beyond IMU
- Multi-property support in single session
- F24 code generation
- Commercialista dashboard / lead funnel
