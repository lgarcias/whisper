import os

from pydantic import BaseModel


class Settings(BaseModel):
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    DEFAULT_ENGINE: str = os.getenv("ENGINE", "faster")  # faster | openai
    # tiny|base|small|medium|large
    DEFAULT_MODEL: str = os.getenv("MODEL", "base")
    DEFAULT_DEVICE: str = os.getenv("DEVICE", "auto")  # auto|cpu|cuda
    # faster-whisper: int8|int8_float16|float16|float32
    DEFAULT_COMPUTE: str = os.getenv("COMPUTE", "int8")
    TRANSCRIPTS_DIR: str = os.getenv("TRANSCRIPTS_DIR", "/workspaces/whisper-website/data")


settings = Settings()

# Ensure transcripts directory exists
os.makedirs(settings.TRANSCRIPTS_DIR, exist_ok=True)
