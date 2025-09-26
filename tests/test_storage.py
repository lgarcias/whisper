import os
import io
import uuid
import tempfile
import pytest
from backend.app import storage


class DummyUploadFile:
    def __init__(self, filename, content):
        self.filename = filename
        self.file = io.BytesIO(content)


def test_new_job_dir_creates_directory(tmp_path, monkeypatch):
    monkeypatch.setattr(storage.settings, "TRANSCRIPTS_DIR", str(tmp_path))
    job_id = uuid.uuid4().hex
    path = storage.new_job_dir(job_id)
    assert os.path.exists(path)
    assert os.path.isdir(path)
    assert path.endswith(job_id)


def test_save_upload_to_tmp_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr(storage.settings, "TRANSCRIPTS_DIR", str(tmp_path))
    content = b"test audio data"
    upload_file = DummyUploadFile("audio.wav", content)
    file_path = storage.save_upload_to_tmp(upload_file)
    assert os.path.exists(file_path)
    with open(file_path, "rb") as f:
        assert f.read() == content
    assert file_path.endswith(".wav")
