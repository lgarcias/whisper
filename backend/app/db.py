"""
db.py - SQLAlchemy setup for FastAPI with SQLAlchemy.
- Safe to import without DATABASE_URL set (lazy engine init).
"""
from __future__ import annotations

from typing import Generator, Optional
import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# -------------------------
# Logging
# -------------------------
logger = logging.getLogger(__name__)

# -------------------------
# ORM Base
# -------------------------
Base = declarative_base()

# -------------------------
# Lazy Engine / Session maker
# -------------------------
_engine: Optional[Engine] = None
_SessionLocal: Optional[sessionmaker] = None


def getDatabaseUrl() -> str:
    """
    Returns DATABASE_URL or raises at call time (not import time).
    """
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL environment variable is required for database connection."
        )
    return url


def getEngine() -> Engine:
    """
    Lazily create and cache the SQLAlchemy engine.
    """
    global _engine
    if _engine is None:
        url = getDatabaseUrl()
        _engine = create_engine(url, future=True)
        logger.info("SQLAlchemy engine initialized")
    return _engine


def getSessionLocal() -> sessionmaker:
    """
    Lazily create and cache the sessionmaker bound to the engine.
    """
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=getEngine(), future=True
        )
    return _SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a SQLAlchemy Session and ensures it is closed.

    Usage in routes:
        def handler(db: Session = Depends(get_db)): ...
    """
    db = getSessionLocal()()
    try:
        yield db
    finally:
        db.close()
