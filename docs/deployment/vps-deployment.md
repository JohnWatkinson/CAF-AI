# VPS Deployment — Assistente IMU

**Server:** Hostinger VPS (shared with fashion-starter)
**SSH:** `ssh john@72.61.20.227`
**Port:** 8080 (fashion-starter uses 80)
**URL:** `http://72.61.20.227:8080`

---

## First-Time Setup

```bash
# 1. SSH into VPS
ssh john@72.61.20.227

# 2. Clone repo
cd ~
git clone https://github.com/JohnWatkinson/CAF-AI.git
cd CAF-AI

# 3. Create .env
cat > .env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-your-key-here
APP_PORT=8080
EOF

# 4. Build and start
docker compose up --build -d

# 5. Verify
curl http://localhost:8080/health
# Open http://72.61.20.227:8080 in browser
```

---

## Deploy Code Changes

```bash
# 1. SSH into VPS
ssh john@72.61.20.227

# 2. Pull and rebuild
cd ~/CAF-AI
git pull origin master
docker compose up --build -d

# 3. Verify
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

## Architecture on VPS

```
Port 80  → fashion-starter (nginx + PM2)
Port 8080 → CAF-AI (Docker Compose)
             ├── frontend (nginx:alpine) → serves React UI + proxies API
             └── backend (python:3.11)   → FastAPI + Claude API
```

---

## Future: Subdomain + SSL

When ready for production:
1. Point a subdomain (e.g., `imu.yourdomain.it`) to VPS IP
2. Add VPS-level nginx config:

```nginx
server {
    server_name imu.yourdomain.it;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 120s;
    }
}
```

3. Add SSL: `sudo certbot --nginx -d imu.yourdomain.it`
4. Keep APP_PORT=8080 in .env (nginx proxies to it)

---

## Checklist

### First Deploy
- [ ] Clone repo on VPS
- [ ] Create .env with API key + APP_PORT=8080
- [ ] `docker compose up --build -d`
- [ ] Test at http://72.61.20.227:8080
- [ ] Verify chat works end-to-end

### Code Updates
- [ ] `git pull origin master`
- [ ] `docker compose up --build -d`
- [ ] Test health + chat
