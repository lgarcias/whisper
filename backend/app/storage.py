import os
import uuid
import shutil
from .config import settings


def new_job_dir(job_id: str) -> str:
    path = os.path.join(settings.TRANSCRIPTS_DIR, job_id)
    os.makedirs(path, exist_ok=True)
    return path


def save_upload_to_tmp(upload_file) -> str:
    ext = os.path.splitext(upload_file.filename or "")[1] or ".wav"
    tmp_path = os.path.join(settings.TRANSCRIPTS_DIR,
                            f"upload-{uuid.uuid4().hex}{ext}")
    with open(tmp_path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)
    return tmp_path
