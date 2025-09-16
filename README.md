# Whisper Website

A minimal, container-friendly backend for speech-to-text using OpenAI Whisper. It exposes a FastAPI service that accepts audio uploads, queues the transcription job in Redis/RQ, and writes results (plain text + JSON with segments) to a persistent folder. The repo is structured to work smoothly in a VS Code Dev Container with model caches persisted across rebuilds.

> **Status:** early MVP. The HTTP surface and worker loop are intentionally small so you can iterate quickly.

## Why this project?

- **Private & portable:** run on your own VPS / desktop without sending audio to third parties (when using `faster-whisper`).  
- **Queue-first design:** uploads return a `job_id` immediately; processing happens in a background RQ worker.  
- **DevContainer ready:** reproducible local dev with cached Whisper models to speed up rebuilds.  

## Project layout

```
.
├─ .devcontainer/           # Dev Container (Dockerfile, docker-compose, post-create)
├─ backend/
│  ├─ app/                  # FastAPI app + transcription utils
│  │  ├─ main.py            # API endpoints (upload, job status/result, health)
│  │  ├─ transcribe.py      # engine selection (openai|faster), run + serialize
│  │  ├─ storage.py         # file helpers (tmp upload, job output directory)
│  │  ├─ rq_queue.py        # shared Redis/RQ connection
│  │  ├─ config.py          # settings & defaults (env-driven)
│  │  └─ worker.py          # (WIP) long-lived RQ worker
│  ├─ requirements.txt
│  └─ README.md             # quick notes for running the backend
└─ docs/                    # extended documentation (this README links here)
```

## Quick start (Dev Container)

1. Open this folder in VS Code and choose **“Reopen in Container”**.  
2. The post-create hook sets up a Python venv and installs backend deps.  
3. Start services from the repo root:

```bash
# API (hot reload)
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Redis is already running as a sidecar in the Dev Container
# Start an RQ worker in another terminal:
python -m rq worker whisper
```

> The Dev Container maps a persistent volume at `/models` to store Whisper/HuggingFace caches so you don’t re-download models after rebuilds.

## API at a glance

- `POST /transcribe` — upload audio, returns `{ job_id }`.  
- `GET  /result/{job_id}` — returns 202 while processing; otherwise returns JSON string (with segments) and a path to the `.txt`.  
- `GET  /health` — liveness/readiness check.

> The exact payloads and field names are documented in **[docs/backend.md](docs/backend.md)**.

## Configuration (env vars)

- `ENGINE` (`faster`|`openai`) – default `faster`  
- `MODEL`  (`tiny`|`base`|`small`|`medium`|`large`) – default `base`  
- `DEVICE` (`auto`|`cpu`|`cuda`) – default `auto` (auto-detects CUDA when available)  
- `COMPUTE` (`int8`|`int8_float16`|`float16`|`float32`) – faster-whisper compute type; default `int8`  
- `REDIS_URL` – default `redis://redis:6379/0`  
- `TRANSCRIPTS_DIR` – default `/workspaces/whisper-website/data`

All of these are wired in `backend/app/config.py` and can be overridden per environment.

## Next steps

- Finish the dedicated `worker.py` loop to preload the model once and reuse it across jobs.  
- Add a simple web UI (dropzone + job viewer).  
- Add auth and rate limiting when exposing the API publicly.

## Documentation index

- **[docs/backend.md](docs/backend.md)** — API details, error shapes, and data formats.  
- **[docs/services.md](docs/services.md)** — Redis/RQ, queues, and model cache volumes.  
- **[docs/app-setup.md](docs/app-setup.md)** — Deploying on a VPS (reverse proxy, SSL, systemd).  
- **[docs/developer-setup.md](docs/developer-setup.md)** — Local development flows and common commands.

---

If you prefer ultra-short READMEs, keep this file as the “front door” and move the rest of the details into the files under `docs/`.
