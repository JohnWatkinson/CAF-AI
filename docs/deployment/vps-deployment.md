# VPS Deployment — Assistente IMU

**Server:** Hostinger VPS (shared with fashion-starter)
**SSH:** `ssh john@72.61.20.227`
**Domain:** `https://caf-ai.maisonguida.com`
**Internal port:** 8080 (Docker Compose) → proxied by VPS nginx
**Repo:** `~/CAF-AI` on VPS
**Nginx config:** `/etc/nginx/sites-available/caf-ai_maisonguida_com`

---

## Architecture on VPS

```
Internet
  │
  ├── caf-ai.maisonguida.com (443/SSL)
  │     └── VPS nginx → proxy_pass localhost:8080
  │           └── Docker Compose
  │                 ├── frontend (nginx:alpine) → React UI + proxies /chat, /reset, /health
  │                 └── backend (python:3.11)   → FastAPI + Claude API
  │
  ├── shop.maisonguida.com (443/SSL)
  │     └── VPS nginx → PM2 (fashion-starter)
  │
  └── tracker.maisonguida.com (443/SSL)
        └── VPS nginx → ...
```

---

## First-Time Setup

```bash
ssh john@72.61.20.227

cd ~
git clone https://github.com/JohnWatkinson/CAF-AI.git
cd CAF-AI

cat > .env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-your-key-here
APP_PORT=8080
EOF

docker compose up --build -d
curl http://localhost:8080/health
```

Then set up DNS A record, nginx site config, and certbot (one-time, not repeated here).

---

## Deploy Code Changes

```bash
ssh john@72.61.20.227
cd ~/CAF-AI
git pull origin master
docker compose up --build -d

docker compose ps
curl http://localhost:8080/health
```

---

## Useful Commands

```bash
docker compose ps              # status
docker compose logs -f         # all logs
docker compose logs -f backend # backend only
docker compose restart         # restart
docker compose down            # stop
docker compose up --build -d   # full rebuild
```

---

## .env (on VPS)

```
ANTHROPIC_API_KEY=sk-ant-...
APP_PORT=8080
```

`APP_PORT` defaults to 80 for local dev. Set to 8080 on VPS to avoid conflict with fashion-starter.
