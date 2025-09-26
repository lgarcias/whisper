import io
from fastapi.testclient import TestClient
from backend.app import main

client = TestClient(main.app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_transcription(monkeypatch):
    # Stub save_upload_to_tmp to create a real temp file
    def fake_save_upload_to_tmp(upload_file):
        path = "/tmp/fake.wav"
        with open(path, "wb") as f:
            f.write(b"RIFF....DATA")
        return path
    monkeypatch.setattr(main, "save_upload_to_tmp", fake_save_upload_to_tmp)

    class FakeJob:
        def __init__(self):
            self.id = "job123"
            self.meta = {}

        def get_status(self):
            return "queued"

        @property
        def is_finished(self):
            return False

        @property
        def is_failed(self):
            return False

        def save_meta(self):
            self.meta_saved = True

    def fake_enqueue(func, kwargs=None, job_timeout=None, result_ttl=None, ttl=None, **extra_kwargs):
        return FakeJob()

    # Replace the queue object with one exposing enqueue and connection
    monkeypatch.setattr(main, "queue", type(
        "_Q", (), {"enqueue": staticmethod(fake_enqueue), "connection": None})())

    files = {"file": ("audio.wav", b"RIFF....DATA", "audio/wav")}
    data = {"engine": "faster", "model": "base", "device": "cpu",
            "task": "transcribe", "compute_type": "int8"}

    r = client.post("/transcriptions", files=files, data=data)
    assert r.status_code == 200
    body = r.json()
    assert body["job_id"] == "job123"
    assert body["status"] == "queued"


def test_get_transcription_not_found(monkeypatch):
    # Make Job.fetch raise to simulate missing job
    def raise_fetch(job_id, connection=None):
        raise Exception("not found")

    monkeypatch.setattr(main.Job, "fetch", staticmethod(raise_fetch))
    r = client.get("/transcriptions/does-not-exist")
    assert r.status_code == 404


def test_get_transcription_result_not_ready(monkeypatch):
    class FakeJob:
        def __init__(self):
            self.id = "job123"

        def get_status(self):
            return "started"

        @property
        def is_finished(self):
            return False

    monkeypatch.setattr(main.Job, "fetch", staticmethod(
        lambda job_id, connection=None: FakeJob()))
    r = client.get("/transcriptions/job123/result")
    assert r.status_code == 202
