"""
Alembic env.py for FastAPI project.

- Loads DATABASE_URL from .env (repo root) or env vars.
- Ensures `from app...` works by adding <repo>/backend to sys.path.
- Imports only Base.metadata (no engine creation, no side-effects).
- Safe autogenerate with compare_type and server defaults.
"""
from __future__ import annotations
from sqlalchemy import engine_from_config, pool
from alembic import context
from logging.config import fileConfig

# --- Path setup: add <repo>/backend so `from app...` works -------------------
import os
import sys

currentDir = os.path.dirname(os.path.abspath(
    __file__))      # .../backend/alembic
backendDir = os.path.dirname(currentDir)                      # .../backend
repoRoot = os.path.dirname(backendDir)                        # .../<repo>

if backendDir not in sys.path:
    sys.path.insert(0, backendDir)

# --- Load .env from repo root so DATABASE_URL is available -------------------
try:
    from dotenv import load_dotenv, find_dotenv  # type: ignore
except Exception:
    load_dotenv = None  # type: ignore[assignment]
    find_dotenv = None  # type: ignore[assignment]

if load_dotenv:
    envPath = os.path.join(repoRoot, ".env")
    if os.path.exists(envPath):
        load_dotenv(envPath)
    else:
        # Fallback: search for .env in current working directory or parent directories.
        # This helps when running Alembic from a different location or in CI environments.
        if find_dotenv:
            found = find_dotenv(usecwd=True)
            if found:
                load_dotenv(found)

# --- Alembic / SQLAlchemy setup ----------------------------------------------

config = context.config
# Set sqlalchemy.url from DATABASE_URL env var if present
database_url = os.environ.get("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import metadata WITHOUT creating engines or requiring DATABASE_URL on import
from app.models import Base  # noqa: E402

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section) or {}
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
