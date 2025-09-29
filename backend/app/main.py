# backend/app/main.py
import os
import shutil
import uuid

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from rq.job import Job

from . import transcribe as t
from .config import settings
from .rq_queue import queue
from .storage import new_job_dir, save_upload_to_tmp

app = FastAPI(title="Whisper Website API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/transcriptions")
async def create_transcription(
    file: UploadFile = File(...),
    engine: str = Form(settings.DEFAULT_ENGINE),  # "faster" | "openai"
    # tiny|base|small|medium|large
    model: str = Form(settings.DEFAULT_MODEL),
    device: str = Form(settings.DEFAULT_DEVICE),  # "auto" | "cpu" | "cuda"
    # "transcribe" | "translate"
    task: str = Form("transcribe"),
    language: str | None = Form(None),
    # int8|int8_float16|float16|float32 (faster-whisper)
    compute_type: str = Form(settings.DEFAULT_COMPUTE),
):
    # Basic validation
    if engine not in ("openai", "faster"):
        raise HTTPException(400, "engine must be 'openai' or 'faster'")
    if device not in ("auto", "cpu", "cuda"):
        raise HTTPException(400, "device must be 'auto'|'cpu'|'cuda'")

    # 1) Generate a stable job_id per request
    job_id = uuid.uuid4().hex

    # 2) Save the uploaded file to tmp, then move it under this job's folder
    #    so each job is isolated in /data/<job_id>/uploads/
    local_tmp = save_upload_to_tmp(file)
    outdir = new_job_dir(job_id)
    uploads_dir = os.path.join(outdir, "uploads")
    os.makedirs(uploads_dir, exist_ok=True)

    dst_path = os.path.join(uploads_dir, os.path.basename(local_tmp or "upload.wav"))
    try:
        shutil.move(local_tmp, dst_path)
    except Exception:
        # If move fails, try copy and remove
        shutil.copyfile(local_tmp, dst_path)
        try:
            os.remove(local_tmp)
        except Exception:
            pass

    # 3) Enqueue the job, passing the same job_id both as RQ id and as kwarg
    job = queue.enqueue(
        t.transcribe_job,
        kwargs={
            "audio_path": dst_path,
            "engine": engine,
            "model": model,
            "device": device,
            "task": task,
            "language": language,
            "compute_type": compute_type,
            "job_id": job_id,  # worker writes to /data/<job_id>
        },
        job_timeout=3600,
        result_ttl=86400,
        ttl=86400,
        job_id=job_id,
    )

    # Optional: store metadata for quick inspection
    job.meta = {
        "job_id": job_id,
        "outdir": outdir,
        "uploads_dir": uploads_dir,
        "audio_path": dst_path,
        "engine": engine,
        "model": model,
        "device": device,
        "task": task,
        "language": language,
        "compute_type": compute_type,
    }
    try:
        job.save_meta()
    except Exception:
        pass

    return {"job_id": job.id, "status": job.get_status()}


@app.get("/transcriptions/{job_id}")
def get_transcription(job_id: str):
    try:
        job = Job.fetch(job_id, connection=queue.connection)
    except Exception:
        raise HTTPException(404, "job not found")

    return {"job_id": job.id, "status": job.get_status()}


@app.get("/transcriptions/{job_id}/result")
def get_transcription_result(job_id: str):
    try:
        job = Job.fetch(job_id, connection=queue.connection)
    except Exception:
        raise HTTPException(404, "job not found")

    if not job.is_finished:
        # 202 while still processing; body includes current status
        raise HTTPException(202, f"job status: {job.get_status()}")

    result = job.result or {}
    json_path = result.get("json_path")
    txt_path = result.get("text_path")

    if not (json_path and os.path.exists(json_path)):
        raise HTTPException(500, "result file missing")

    # Return JSON content as a string; client may parse it
    with open(json_path, "r", encoding="utf-8") as f:
        content = f.read()

    return {
        "job_id": job.id,
        "json": content,
        "text_path": txt_path,
        "outdir": result.get("outdir"),
    }
