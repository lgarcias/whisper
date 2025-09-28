# Whisper Website

Whisper Website provides a **FastAPI** backend and a **Next.js** frontend to transcribe audio using **OpenAI Whisper** and **Faster-Whisper** models.

The goal is to offer a simple API to upload audio files and get transcriptions, with background job queue processing via **RQ + Redis**. The project is containerized for easy local development and includes a Makefile for packaging.

---

## 🚀 Local Development

### Prerequisites

- Docker and Docker Compose
- VS Code with the **Dev Containers** extension
- Git

### Initial Setup

Clone this repository and open it in VS Code:

```bash
git clone <repo-url>
cd whisper-website
```

Open in VS Code and select `Reopen in Container` to load the development environment. The Dev Container will set up a Python virtual environment and install dependencies automatically.

### Main Services

- **Backend**: FastAPI running at `http://localhost:8000` ([backend/README.md](backend/README.md))
- **Frontend**: React/Next.js running at `http://localhost:3000` ([frontend/README.md](frontend/README.md))
- **Redis**: used for the job queue

---

## 📌 API Endpoints

> Default Base URL: `http://localhost:8000`

- `GET /health` → Check service status
- `POST /transcriptions` → Upload an audio file for transcription (returns `job_id`)
- `GET /transcriptions/{job_id}` → Check job status
- `GET /transcriptions/{job_id}/result` → Get transcription result

> See detailed API documentation in [`docs/backend.md`](docs/backend.md)

---

## 🛠️ Technologies

- [FastAPI](https://fastapi.tiangolo.com/)
- [RQ](https://python-rq.org/) + Redis
- [Whisper](https://github.com/openai/whisper) and [Faster-Whisper](https://github.com/guillaumekln/faster-whisper)
- [Next.js](https://nextjs.org/) (frontend)
- Docker / DevContainers

---

## 🧪 Testing

Tests are written with `pytest` and located in the `tests/` directory. You can run all tests from the project root:

```bash
pytest
```

or using the VS Code Test Explorer (recommended in Dev Container).

> The project includes a `pytest.ini` so you do not need to set `PYTHONPATH` manually.

## 🗂️ Packaging

You can create zip archives of the project using the provided Makefile:

```bash
make zip      # Only tracked files (HEAD)
make zip-all  # Tracked + untracked files (respects .gitignore)
make clean    # Remove build/
```

## 📚 Documentation

- Backend details: [backend/README.md](backend/README.md)
- Frontend details: [frontend/README.md](frontend/README.md)
- API reference: [docs/backend.md](docs/backend.md)
- Database setup & config: [docs/database.md](docs/database.md)
- Developer setup: [docs/developer-setup.md](docs/developer-setup.md)
- App/production setup: [docs/app-setup.md](docs/app-setup.md)
- Services and orchestration: [docs/services.md](docs/services.md)
- Roadmap: [docs/roadmap.md](./docs/roadmap.md)
  - [Prompts esquema inicial](./docs/roadmap/prompts_esquema_inicial.md)

## ⚡ VS Code Tasks

The project includes VS Code tasks for starting/stopping the backend and worker. Use `Ctrl+Shift+P → Run Task` for convenience.

---

## 📄 License

MIT
