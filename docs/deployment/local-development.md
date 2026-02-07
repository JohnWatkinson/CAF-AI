# Local Development

## Setup (once)

```bash
git clone https://github.com/JohnWatkinson/CAF-AI.git
cd CAF-AI
cp .env.example .env   # add ANTHROPIC_API_KEY
```

## Daily workflow

```bash
# Start
docker compose up --build -d
# → http://localhost

# Check it's running
docker compose ps
curl http://localhost/health

# View logs
docker compose logs -f backend

# Stop
docker compose down
```

## Make changes → test → push

```bash
# 1. Edit code in VSCode

# 2. Rebuild and test
docker compose up --build -d

# 3. Check conversation logs
cat logs/$(date +%Y-%m-%d).jsonl

# 4. Push
git add -A
git commit -m "description"
git push origin master
```

## Deploy to VPS

```bash
ssh john@72.61.20.227
cd ~/CAF-AI
git pull origin master
docker compose up --build -d
```

## Run tests (no Docker needed)

```bash
source .venv/bin/activate
pytest tests/ -v
```

## Without Docker

```bash
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.api.main:app --port 8000 --reload
# → http://localhost:8000 (API only, no frontend)
```
