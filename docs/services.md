# Services, Queues & Caching

This repo ships with a Dev Container that starts two services via Docker Compose:

- **app** — your development environment (Python, Node.js) where you run the FastAPI app and RQ worker.
- **redis** — Redis 7 used by RQ.

```yaml
# .devcontainer/docker-compose.yml (excerpt)
services:
  app:
    build: .devcontainer/Dockerfile
    volumes:
      - ..:/workspaces/whisper-website:cached
      - whisper-models:/models
    ports: ["3000:3000", "8000:8000"]
    environment:
      WHISPER_CACHE_DIR=/models/whisper
      HF_HOME=/models/hf
      XDG_CACHE_HOME=/models/cache
  redis:
    image: redis:7-alpine

volumes:
  whisper-models: {}
```

## Model caches

Model downloads are persisted to the named volume `whisper-models`, mounted at `/models` inside the dev container. This avoids re-downloading models after rebuilds:

- `WHISPER_CACHE_DIR=/models/whisper`
- `HF_HOME=/models/hf`
- `XDG_CACHE_HOME=/models/cache`

## Ports

- `8000` — FastAPI (Uvicorn)  
- `3000` — reserved for a future web frontend  
- `6379` — Redis (forwarded internally by the devcontainer)

## Queue

- Queue name: **`whisper`**  
- Connection: created in `backend/app/rq_queue.py` using `REDIS_URL` from env (default `redis://redis:6379/0`).

Start a worker with:

```bash
python -m rq worker whisper
```

## Storage

Transcripts are written under `TRANSCRIPTS_DIR` (default `/workspaces/whisper-website/data`). Mount or bind this path in production so results persist across restarts.
