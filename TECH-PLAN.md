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

### 3. Chat Layer (`chat/engine.py`)
- Sends conversation to LLM (Claude or OpenAI) with a system prompt
- System prompt defines: you're an IMU assistant, you speak Italian, you collect the required inputs, you call the calculator, you explain the result
- LLM does NOT calculate — it extracts user inputs and formats them for the calculator
- Function calling / tool use pattern: LLM decides when it has enough info → calls `calculate_imu()`

### 4. API (`api/main.py`)
FastAPI app with:
- `POST /chat` — takes message + session_id, returns assistant reply
- Session state stored in memory (dict) for PoC, Redis later
- CORS enabled for future frontend

### 5. Docker (`docker-compose.yml`)
- Single container for PoC (FastAPI app)
- Nginx reverse proxy (same pattern as fashion-starter)
- `.env` for API keys
- Ready to add Redis, Postgres containers later

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
│   ├── chat/                    # Next
│   │   ├── engine.py            # LLM conversation handler
│   │   └── prompts.py           # System prompts (Italian)
│   └── api/
│       └── main.py              # FastAPI app
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
3. **Chat engine** — LLM conversation with tool-calling to the calculator ← **next**
4. **FastAPI API** — wrap it in an endpoint
5. **Docker + deploy** — containerize, nginx, push to VPS
6. **Scraper** (later) — populate aliquote for more comuni

---

## Future Growth Path

- WhatsApp / Telegram bot (connect to same API)
- Document upload (parse visura catastale / previous F24)
- Full aliquote DB (Postgres) with yearly scraper from MEF
- Additional tax types beyond IMU
- Multi-property support in single session
- F24 code generation
- Commercialista dashboard / lead funnel
