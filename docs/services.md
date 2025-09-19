# Services Guide (FastAPI, Redis, RQ Worker)

This document explains what each service does and how to **start / stop / restart** them from the **host** and from the **DevContainer terminal in VS Code**.

> Compose file used below: `.devcontainer/docker-compose.yml`

---

## Services Overview

- **FastAPI (app)**

  - Python API served by `uvicorn`.
  - Default ports exposed in compose: `8000:8000` (API), optionally `3000:3000` if your frontend uses it.
  - Health endpoint: `GET /health` → `{ "status": "ok" }`.

- **Redis (redis)**

  - In‑memory queue broker for RQ.
  - Internal port: `6379` (usually not published to host).

- **RQ Worker (worker)**

  - Background worker that consumes jobs from the Redis queue `whisper`.
  - Runs `python -m backend.app.worker`.

---

## From the Host (outside the container)

> Run these in the project root on your host (Windows PowerShell / Git Bash), adjusting the path if needed.

### Start

```bash
# Start everything
docker compose -f .devcontainer/docker-compose.yml up -d

# Start a specific service
docker compose -f .devcontainer/docker-compose.yml up -d app
docker compose -f .devcontainer/docker-compose.yml up -d redis
docker compose -f .devcontainer/docker-compose.yml up -d worker
```

### Stop

```bash
# Stop everything (keeps containers)
docker compose -f .devcontainer/docker-compose.yml stop

# Stop specific service
docker compose -f .devcontainer/docker-compose.yml stop app
```

### Restart

```bash
# Restart everything
docker compose -f .devcontainer/docker-compose.yml restart

# Restart specific services
docker compose -f .devcontainer/docker-compose.yml restart app
Docker compose -f .devcontainer/docker-compose.yml restart worker
```

### Status & Logs

```bash
# Status of all services
docker compose -f .devcontainer/docker-compose.yml ps

# Follow logs
docker compose -f .devcontainer/docker-compose.yml logs -f app
docker compose -f .devcontainer/docker-compose.yml logs -f redis
docker compose -f .devcontainer/docker-compose.yml logs -f worker
```

### One‑liners (common flows)

```bash
# Start worker and tail logs
docker compose -f .devcontainer/docker-compose.yml up -d worker && docker compose -f .devcontainer/docker-compose.yml logs -f worker

# Recreate app after compose edits
docker compose -f .devcontainer/docker-compose.yml up -d --force-recreate app
```

---

## From the DevContainer Terminal (inside VS Code)

Open a terminal **inside** the DevContainer (it shows a path like `/workspaces/whisper-website`).

### FastAPI (app)

**Start (manual)**

```bash
source .venv/bin/activate
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Stop**: `Ctrl+C` in that terminal.

**Restart**: stop then start again, or use VS Code Tasks (below).

### RQ Worker (worker)

**Start (manual)**

```bash
source .venv/bin/activate
python -m backend.app.worker
```

**Stop**: `Ctrl+C` in that terminal.

> If you added the worker as a Compose service (recommended), prefer using the host commands: `up -d worker`, `logs -f worker`, etc.

### Redis (redis)

Managed by Docker Compose. From inside the DevContainer you can ping it:

```bash
redis-cli -h redis ping   # → PONG
```

---

## VS Code Tasks (optional convenience)

Create `.vscode/tasks.json` with entries like:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start FastAPI (uvicorn)",
      "type": "shell",
      "command": "source .venv/bin/activate && uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload",
      "problemMatcher": []
    },
    {
      "label": "Stop FastAPI (uvicorn)",
      "type": "shell",
      "command": "pkill -f 'uvicorn' || true",
      "problemMatcher": []
    },
    {
      "label": "Restart FastAPI (uvicorn)",
      "type": "shell",
      "command": "pkill -f 'uvicorn' || true && source .venv/bin/activate && uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload",
      "problemMatcher": []
    },

    {
      "label": "Start RQ Worker",
      "type": "shell",
      "command": "source .venv/bin/activate && python -m backend.app.worker",
      "problemMatcher": [],
      "isBackground": false,
      "presentation": { "reveal": "always", "panel": "dedicated" }
    },
    {
      "label": "Stop RQ Worker",
      "type": "shell",
      "command": "pkill -f 'backend.app.worker' || true",
      "problemMatcher": []
    },
    {
      "label": "Restart RQ Worker",
      "type": "shell",
      "command": "pkill -f 'backend.app.worker' || true && source .venv/bin/activate && python -m backend.app.worker",
      "problemMatcher": [],
      "isBackground": false,
      "presentation": { "reveal": "always", "panel": "dedicated" }
    }
  ]
}
```

Run with **Ctrl+Shift+P → Run Task**.

---

## Health Checks & Quick Tests

- **FastAPI**

  - From host: `curl http://localhost:8000/health` → `{ "status": "ok" }`
  - Upload transcription test:
    ```bash
    curl -X POST "http://localhost:8000/transcriptions" -F "file=@/path/to/audio.wav"
    ```

- **Redis**

  - Inside DevContainer: `redis-cli -h redis ping` → `PONG`

- **RQ Worker**

  - Logs: `docker compose -f .devcontainer/docker-compose.yml logs -f worker`
  - Should show: `Listening on whisper...`, `Started job ...`, `Finished ...`.

---

## Common Issues

- **Port 3000/8000 already in use**: free the port on host or change port mapping in compose (`ports:` section).
- **Worker stops when closing VS Code terminal**: run worker as a Compose service with `restart: unless-stopped`.
- **Results location**: by default `TRANSCRIPTS_DIR` → `/workspaces/whisper-website/data`. If using a volume, set `TRANSCRIPTS_DIR=/data` and mount `whisper-data:/data` in `app` and `worker`.
- **Redis connectivity**: inside Compose network, host is `redis` (not `localhost`).
