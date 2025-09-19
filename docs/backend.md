# Backend API Documentation

The backend is built with **FastAPI** and exposes REST endpoints to manage audio transcriptions.

---

## Endpoints

> Default Base URL during development: `http://localhost:8000`

---

### GET /health

Checks that the API is alive.

**Response 200 OK**

```json
{ "status": "ok" }
```

---

### POST /transcriptions

Uploads an audio file for transcription. The transcription runs in the background (RQ) and returns a `job_id` to query the status.

**Content-Type:** `multipart/form-data`  
**Form fields:**

- `file` **(required)**: audio file (`audio/*`, `.mp3`, `.wav`, …)
- `engine` _(optional)_: `faster` (default) or `openai`
- `model` _(optional)_: `tiny|base|small|medium|large`
- `device` _(optional)_: `auto|cpu|cuda` (`auto` tries CUDA if available)
- `compute_type` _(optional, only faster-whisper)_: `int8|int8_float16|float16|float32`
- `task` _(optional)_: `transcribe` (default) or `translate`
- `language` _(optional)_: ISO-639-1 code (auto-detected if omitted)

**Response 201 Created**

```json
{ "job_id": "rq:job:XXXXXXXX..." }
```

**Example cURL**

```bash
curl -F "file=@sample.wav"      -F "engine=faster"      -F "model=base"      http://localhost:8000/transcriptions
```

---

### GET /transcriptions/{job_id}

Returns the **status** of the transcription job.

**Response 200 OK**

```json
{
  "job_id": "rq:job:XXXXXXXX",
  "status": "queued|started|finished|failed",
  "meta": {
    /* optional info */
  }
}
```

**Response 404 Not Found**

```json
{ "detail": "Job not found" }
```

---

### GET /transcriptions/{job_id}/result

Returns the **result** of the transcription once it has finished.

- **202 Accepted** if still in progress:

```json
{ "job_id": "rq:job:XXXXXXXX", "status": "queued|started" }
```

- **200 OK** if finished:

```json
{
  "job_id": "rq:job:XXXXXXXX",
  "json": "{ ...serialized JSON content... }",
  "text_path": "/path/to/transcript.txt"
}
```

- **500 Internal Server Error** if the expected result file is missing.
- **404 Not Found** if the `job_id` does not exist.

**Example cURL**

```bash
JOB_ID="rq:job:XXXXXXXX"
curl -s "http://localhost:8000/transcriptions/$JOB_ID/result"
```

---

## Implementation notes

- Jobs are managed with **RQ in Redis**.
- Results are stored under `TRANSCRIPTS_DIR/<job_id>/`:
  - `transcript.txt` (plain text)
  - `result.json` (with `engine`, `model`, `task`, `language`, `text`, `segments`).
- **CORS** is open for development (all origins). Restrict before production.
