"""
db.py - SQLAlchemy setup for FastAPI with Postgres.
- CamelCase for internal names (project convention).
- PEP8-compliant line lengths and imports.
"""
from typing import Generator
import logging
import os

from sqlalchemy import create_engine, text
from sqlalchemy.exc import DBAPIError, OperationalError
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# -------------------------
# Logging
# -------------------------
logger = logging.getLogger("db")
logLevelName = os.getenv("DB_LOG_LEVEL", "INFO").upper()
logger.setLevel(getattr(logging, logLevelName, logging.INFO))

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# -------------------------
# Env configuration
# -------------------------
databaseUrl = os.getenv("DATABASE_URL")
if not databaseUrl:
    raise RuntimeError(
        "DATABASE_URL environment variable is required for database connection."
    )

poolSize = int(os.getenv("DB_POOL_SIZE", "5"))
maxOverflow = int(os.getenv("DB_MAX_OVERFLOW", "5"))
poolRecycle = int(os.getenv("DB_POOL_RECYCLE", "1800"))  # seconds
poolTimeout = int(os.getenv("DB_POOL_TIMEOUT", "30"))     # seconds
echoSql = os.getenv("DB_ECHO", "false").lower() == "true"

# -------------------------
# Engine
# -------------------------
engine = create_engine(
    databaseUrl,
    pool_pre_ping=True,
    pool_size=poolSize,
    max_overflow=maxOverflow,
    pool_recycle=poolRecycle,
    pool_timeout=poolTimeout,
    echo=echoSql,
    future=True,
)

# Optional: fail fast if DB is not reachable at startup
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info("Database connection test succeeded.")
except (OperationalError, DBAPIError) as exc:
    logger.error("Database connection test failed: %s", exc)
    raise

# -------------------------
# Session / Base
# -------------------------
SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True,
)

Base = declarative_base()

# -------------------------
# FastAPI dependency
# -------------------------


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a SQLAlchemy Session and ensures it is closed.
    Usage in routes:
        def handler(db: Session = Depends(get_db)): ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
