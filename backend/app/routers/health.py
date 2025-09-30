"""
health.py - FastAPI router for health and readiness endpoints.
"""

import os
from datetime import datetime, timezone
from typing import Any, Optional

import redis
from app.db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

try:
    import redis
except ImportError:
    redis = None  # type: ignore

router = APIRouter()


class HealthOut(BaseModel):
    db_ok: Optional[bool] = None
    redis_ok: Optional[bool] = None
    version: str
    time: int


def get_version() -> str:
    """Get app version from environment variables or default to 'dev'."""
    return os.getenv("GIT_SHA") or os.getenv("APP_VERSION") or "dev"


def get_redis_client() -> Optional[Any]:
    """Return a Redis client if configured, else None."""
    if redis is None:
        return None
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        return None
    try:
        client = redis.Redis.from_url(redis_url, socket_connect_timeout=0.2, socket_timeout=0.2)
        return client
    except Exception:
        return None


@router.get("/api/health", response_model=HealthOut, tags=["health"])
def liveness_handler() -> HealthOut:
    """Liveness probe: always returns 200, does not check DB or Redis."""
    return HealthOut(
        db_ok=None,
        redis_ok=None,
        version=get_version(),
        time=int(datetime.now(timezone.utc).timestamp()),
    )


@router.get("/api/ready", response_model=HealthOut, tags=["health"])
def readiness_handler(
    db: Session = Depends(get_db),
    redis_client: Optional[Any] = Depends(get_redis_client),
) -> HealthOut:
    """Readiness probe: checks DB and optionally Redis, returns 503 if not ready."""
    db_ok = False
    redis_ok: Optional[bool] = None
    # Check DB
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    # Check Redis if configured
    if redis_client is not None:
        try:
            pong = redis_client.ping()
            redis_ok = bool(pong)
        except Exception:
            redis_ok = False
    # If DB or Redis (if configured) is not OK, return 503
    if not db_ok or (redis_ok is False):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not ready",
        )
    return HealthOut(
        db_ok=db_ok,
        redis_ok=redis_ok,
        version=get_version(),
        time=int(datetime.utcnow().timestamp()),
    )
