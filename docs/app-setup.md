# Application Setup (Production)

This guide targets a small VPS (e.g., Hetzner CX or similar) to run the API privately.

For local development, see [../README.md](../README.md) and [docs/developer-setup.md](developer-setup.md).

## 1) System packages

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg python3-pip python3-venv git redis-server
```

If you plan to use GPU, provision a CUDA-capable host and install NVIDIA drivers + CUDA toolkit as appropriate.

## 2) Clone & Python env

```bash
git clone <your-fork-url> whisper-website
cd whisper-website
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -r backend/requirements.txt
```

## 3) Environment

Create a `.env` (or systemd EnvironmentFile) with sensible defaults:

```
ENGINE=faster
MODEL=base
DEVICE=auto
COMPUTE=int8
REDIS_URL=redis://localhost:6379/0
TRANSCRIPTS_DIR=/opt/whisper-website/data
```

Create the directory and permissions:

```bash
sudo mkdir -p /opt/whisper-website/data
sudo chown -R $USER:$USER /opt/whisper-website
```

## 4) Run services

In one shell (API):

```bash
source .venv/bin/activate
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

In another shell (worker):

```bash
source .venv/bin/activate
python -m rq worker whisper
```

## 5) Reverse proxy + TLS

Use Nginx or Caddy to expose `https://your-domain` to `http://127.0.0.1:8000` and obtain TLS via Let’s Encrypt. Example Nginx location:

```
location / {
    proxy_pass         http://127.0.0.1:8000;
    proxy_set_header   Host $host;
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Proto $scheme;
}
```

## 6) Systemd units (optional)

Create services for API and worker for automatic restarts. Ensure `WorkingDirectory`, `Environment`, and `User` are set correctly.

## 7) Backups

Back up `TRANSCRIPTS_DIR` (and any logs) on a schedule.

---

## Packaging & Testing

To create zip archives, see the [Makefile usage in the main README](../README.md#-packaging).

For running tests, see [Developer Setup](developer-setup.md#testing).

---

## Frontend

This document covers backend setup. For frontend setup and deployment, see [frontend/README.md](../frontend/README.md).
