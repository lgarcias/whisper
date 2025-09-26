# Developer Setup

## Prerequisites

- VS Code + Dev Containers extension
- Docker Desktop (Windows/macOS) or Docker Engine (Linux)

## Start the Dev Container

1. Open the repo in VS Code.
2. `Dev Containers: Reopen in Container`.
3. Post-create script sets up a Python virtualenv and installs `backend/requirements.txt`.

## Common commands (from repo root)

```bash
# API (hot reload)
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# RQ worker
python -m rq worker whisper

# Frontend (from frontend/)
npm run dev
```

## Testing

Tests are located in the `tests/` directory and use `pytest`. Run all tests from the project root:

```bash
pytest
```

or use the VS Code Test Explorer.

> The project includes a `pytest.ini` so you do not need to set `PYTHONPATH` manually.

## VS Code Tasks

The project includes VS Code tasks for starting/stopping the backend and worker. Use `Ctrl+Shift+P → Run Task` for convenience.

---

### Curl examples

```bash
# Health
curl -s http://localhost:8000/health

# Transcribe
curl -F "file=@sample.wav"      -F "engine=faster"      -F "model=base"      http://localhost:8000/transcribe

# Poll result
curl -s http://localhost:8000/result/<job_id>
```

## Troubleshooting

- **Import errors**: run from the repo root (`uvicorn backend.app.main:app`).
- **Models re-downloading**: check that `/models` volume is mounted and `WHISPER_CACHE_DIR`, `HF_HOME`, `XDG_CACHE_HOME` are set.
- **CUDA**: set `DEVICE=cuda`. The code will fallback to CPU if CUDA is unavailable.

---

For production setup, see [app-setup.md](app-setup.md).
