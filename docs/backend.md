# Backend: API & Data Contracts

This document expands on the FastAPI surface and the data you can expect to read/write. The code lives in `backend/app/` and is designed to run from the **repository root** so relative imports work.

## Endpoints

> Paths refer to the default Uvicorn port `8000`.

### `POST /transcribe`

Upload an audio file and optional parameters. Returns a JSON body with a `job_id` you can poll later.

**Form fields** (multipart):
- `file` **(required)**: the audio file (`audio/*`, `.mp3`, `.wav`, etc.).
- `engine` *(optional)*: `faster` (default) or `openai`.
- `model` *(optional)*: `tiny|base|small|medium|large` (default from env).
- `device` *(optional)*: `auto|cpu|cuda` (default: `auto`).
- `compute` *(optional, faster-whisper)*: `int8|int8_float16|float16|float32`.
- `task` *(optional)*: `transcribe` (default) or `translate`.
- `language` *(optional)*: BCP‑47 code like `en`, `es`, `fr`. If omitted, language is auto-detected.

**201 Response**

```json
{ "job_id": "rq:job:1a2b3c..." }
```

### `GET /result/{job_id}`

Poll the job. While processing, the API responds with **HTTP 202** and a short status message. When finished, it returns metadata plus the serialized JSON transcript and a filesystem path to the `.txt` file.

**200 Response**
```json
{
  "job_id": "rq:job:1a2b3c...",
  "json": "{ ...stringified JSON with text and segments... }",
  "text_path": "/workspaces/whisper-website/data/<job-id>/transcript.txt"
}
```

> The JSON string contains fields like `text`, and `segments` with `start`, `end`, and `text`. See `transcribe.py` for the exact structure.

### `GET /health`

Returns `{"status":"ok"}` when the API is reachable and Redis is configured.

## Background processing

- Uploads enqueue a task in the `"whisper"` queue (`backend/app/rq_queue.py`).  
- The worker consumes jobs and writes outputs to `TRANSCRIPTS_DIR` under a per‑job folder.  
- A dedicated `worker.py` is included (WIP). In the meantime, you can rely on RQ’s default worker:

```bash
# from repository root
python -m rq worker whisper
```

## Engines

- **faster-whisper** (default): Faster CPU/GPU inference via CTranslate2. Honors `COMPUTE` precision.  
- **openai-whisper**: Reference PyTorch implementation. Slower on CPU, good for parity testing.

Device selection is handled in `pick_device()` and will auto-fallback to CPU if CUDA is not available.

## Files written per job

```
data/<job-id>/
├─ transcript.txt          # concatenated plain text
└─ transcript.json         # metadata + segments (UTF-8, pretty-printed)
```

## Error handling

- 400/422 for malformed requests (missing file, bad params).  
- 202 while the job is still running.  
- 500 if the expected result files are missing.

## CORS

CORS is enabled for all origins during MVP. Lock this down before exposing the API publicly.
