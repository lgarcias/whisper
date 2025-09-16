import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rq.job import Job
from .config import settings
from .rq_queue import queue
from .storage import save_upload_to_tmp
from . import transcribe as t

app = FastAPI(title="Whisper Website API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/transcriptions")
async def create_transcription(
    file: UploadFile = File(...),
    engine: str = Form(settings.DEFAULT_ENGINE),
    model: str = Form(settings.DEFAULT_MODEL),
    device: str = Form(settings.DEFAULT_DEVICE),
    task: str = Form("transcribe"),   # "transcribe" | "translate"
    language: str | None = Form(None),
    compute_type: str = Form(settings.DEFAULT_COMPUTE),
):
    if engine not in ("openai", "faster"):
        raise HTTPException(400, "engine must be 'openai' or 'faster'")
    if device not in ("auto", "cpu", "cuda"):
        raise HTTPException(400, "device must be 'auto'|'cpu'|'cuda'")

    # Save uploaded audio to disk (repo bind-mount → persistent)
    local_path = save_upload_to_tmp(file)

    # Enqueue job; pass job_id to the worker so it can write results into its own folder
    job = queue.enqueue(
        t.transcribe_job,
        kwargs={
            "audio_path": local_path,
            "engine": engine,
            "model": model,
            "device": device,
            "task": task,
            "language": language,
            "compute_type": compute_type,
            "job_id": None  # RQ asigna ID; lo recuperamos luego
        },
        job_timeout=3600, result_ttl=86400, ttl=86400
    )

    # Small tweak: add the job_id to job.meta so transcribe_job can access it if desired
    job.meta["job_id"] = job.id
    job.save_meta()

    return {"job_id": job.id, "status": job.get_status()}


@app.get("/transcriptions/{job_id}")
def get_transcription(job_id: str):
    try:
        job = Job.fetch(job_id, connection=queue.connection)
    except Exception:
        raise HTTPException(404, "job not found")

    resp = {"job_id": job.id, "status": job.get_status()}
    if job.is_finished:
        resp["result"] = job.result
    if job.is_failed:
        resp["error"] = str(job.exc_info or "")
    return resp


@app.get("/transcriptions/{job_id}/result")
def get_transcription_result(job_id: str):
    try:
        job = Job.fetch(job_id, connection=queue.connection)
    except Exception:
        raise HTTPException(404, "job not found")

    if not job.is_finished:
        raise HTTPException(202, f"job status: {job.get_status()}")

    result = job.result or {}
    json_path = result.get("json_path")
    txt_path = result.get("text_path")

    if not (json_path and os.path.exists(json_path)):
        raise HTTPException(500, "result file missing")

    with open(json_path, "r", encoding="utf-8") as f:
        content = f.read()
    return {"job_id": job.id, "json": content, "text_path": txt_path}
