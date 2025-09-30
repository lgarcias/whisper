from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class JobCreateIn(BaseModel):
    model_name: str
    language: Optional[str] = None
    mode: str
    audio_duration_ms: Optional[int] = None
    # Add other fields as needed


class JobOut(BaseModel):
    id: str
    owner_user_id: str
    status: Literal["queued", "processing", "done", "failed"]
    model_name: str
    mode: str
    language: Optional[str] = None
    audio_duration_ms: Optional[int] = None
    processing_time_ms: Optional[int] = None
    result_json_path: Optional[str] = None
    transcript_txt_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None

    model_config = {"from_attributes": True}
