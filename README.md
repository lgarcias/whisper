# Whisper Website

Whisper Website is a project that provides a **FastAPI** backend and a frontend to transcribe audio using **OpenAI Whisper** and **Faster-Whisper** models.

The goal is to offer a simple API to upload audio files and get transcriptions, with background job queue processing via **RQ + Redis**.

---

## 🚀 Local development

### Prerequisites

- Docker and Docker Compose
- VS Code with the **Dev Containers** extension
- Git

### Initial setup

Clone this repository and open it in VS Code:

```bash
git clone <repo-url>
cd whisper-website
```

Open in VS Code and select `Reopen in Container` to load the development environment.

### Main services

- **Backend**: FastAPI running at `http://localhost:8000`
- **Frontend**: React/Next.js running at `http://localhost:3000`
- **Redis**: used for the job queue

---

## 📌 API Endpoints

> Default Base URL: `http://localhost:8000`

- `GET /health` → Check service status
- `POST /transcriptions` → Upload an audio file for transcription (returns `job_id`)
- `GET /transcriptions/{job_id}` → Check job status
- `GET /transcriptions/{job_id}/result` → Get transcription result

> Detailed documentation in [`docs/backend.md`](docs/backend.md)

---

## 🛠️ Technologies

- [FastAPI](https://fastapi.tiangolo.com/)
- [RQ](https://python-rq.org/) + Redis
- [Whisper](https://github.com/openai/whisper) and [Faster-Whisper](https://github.com/guillaumekln/faster-whisper)
- Docker / DevContainers

---

## 📄 License

MIT
