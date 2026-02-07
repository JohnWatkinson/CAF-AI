# VPS Deployment — Assistente IMU

**Server:** Hostinger VPS (shared with fashion-starter)
**SSH:** `ssh john@72.61.20.227`
**Domain:** `https://caf-ai.maisonguida.com`
**Internal port:** 8080 (Docker Compose) → proxied by VPS nginx

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

### 1. DNS (Hostinger panel)

Add A record for `maisonguida.com`:
- **Type:** A
- **Name:** `caf-ai`
- **Value:** `72.61.20.227`
- **TTL:** default

### 2. Deploy app

```bash
ssh john@72.61.20.227

# Clone
cd ~
git clone https://github.com/JohnWatkinson/CAF-AI.git
cd CAF-AI

# Create .env
cat > .env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-your-key-here
APP_PORT=8080
EOF

# Build and start
docker compose up --build -d

# Verify
curl http://localhost:8080/health
```

### 3. VPS nginx config

```bash
sudo nano /etc/nginx/sites-available/caf-ai_maisonguida_com
```

```nginx
server {
    listen 80;
    server_name caf-ai.maisonguida.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 120s;
    }
}
```

Enable and reload:

```bash
sudo ln -s /etc/nginx/sites-available/caf-ai_maisonguida_com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. SSL

```bash
sudo certbot --nginx -d caf-ai.maisonguida.com
```

Certbot auto-updates the nginx config with SSL directives and sets up auto-renewal.

---

## Deploy Code Changes

```bash
ssh john@72.61.20.227
cd ~/CAF-AI
git pull origin master
docker compose up --build -d

# Verify
docker compose ps
curl http://localhost:8080/health
```

---

## Useful Commands

```bash
# Status
docker compose ps

# Logs
docker compose logs -f
docker compose logs -f backend
docker compose logs -f frontend

# Restart
docker compose restart

# Full rebuild
docker compose down
docker compose up --build -d

# Stop
docker compose down
```

---

## Environment

### .env (on VPS)
```
ANTHROPIC_API_KEY=sk-ant-...
APP_PORT=8080
```

`APP_PORT` defaults to 80 for local dev. Set to 8080 on VPS to avoid conflict with fashion-starter on port 80.

---

## Checklist

### First Deploy
- [ ] Add DNS A record: `caf-ai` → `72.61.20.227`
- [ ] Clone repo on VPS
- [ ] Create .env with API key + APP_PORT=8080
- [ ] `docker compose up --build -d`
- [ ] Create nginx site config
- [ ] `sudo certbot --nginx -d caf-ai.maisonguida.com`
- [ ] Test at https://caf-ai.maisonguida.com
- [ ] Verify chat works end-to-end

### Code Updates
- [ ] `git pull origin master`
- [ ] `docker compose up --build -d`
- [ ] Test health + chat
