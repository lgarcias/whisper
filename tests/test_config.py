import os
from backend.app import config


def test_settings_defaults(monkeypatch):
    monkeypatch.delenv("REDIS_URL", raising=False)
    monkeypatch.delenv("ENGINE", raising=False)
    monkeypatch.delenv("MODEL", raising=False)
    monkeypatch.delenv("DEVICE", raising=False)
    monkeypatch.delenv("COMPUTE", raising=False)
    monkeypatch.delenv("TRANSCRIPTS_DIR", raising=False)
    settings = config.Settings()
    assert settings.REDIS_URL == "redis://redis:6379/0"
    assert settings.DEFAULT_ENGINE == "faster"
    assert settings.DEFAULT_MODEL == "base"
    assert settings.DEFAULT_DEVICE == "auto"
    assert settings.DEFAULT_COMPUTE == "int8"
    assert settings.TRANSCRIPTS_DIR == "/workspaces/whisper-website/data"


def test_settings_env(monkeypatch):
    monkeypatch.setenv("REDIS_URL", "redis://localhost:1234/1")
    monkeypatch.setenv("ENGINE", "openai")
    monkeypatch.setenv("MODEL", "large")
    monkeypatch.setenv("DEVICE", "cpu")
    monkeypatch.setenv("COMPUTE", "float32")
    monkeypatch.setenv("TRANSCRIPTS_DIR", "/tmp/testdata")
    import importlib
    importlib.reload(config)
    settings = config.Settings()
    assert settings.REDIS_URL == "redis://localhost:1234/1"
    assert settings.DEFAULT_ENGINE == "openai"
    assert settings.DEFAULT_MODEL == "large"
    assert settings.DEFAULT_DEVICE == "cpu"
    assert settings.DEFAULT_COMPUTE == "float32"
    assert settings.TRANSCRIPTS_DIR == "/tmp/testdata"
