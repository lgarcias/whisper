import os
from urllib.parse import urlparse

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from backend.app import db, main


@pytest.fixture(scope="session")
def test_db_session():
    """
    Main test fixture for whisperdb. It creates a clean, migrated database
    for a test session, and destroys it after the session is over.
    """
    # Get the database url from the environment
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")

    # The database name is the last part of the path in the URL
    db_name = db_url.split("/")[-1]

    # Create an engine to the postgres database to create the test database
    postgres_db_url = db_url.replace(db_name, "postgres")
    engine = create_engine(postgres_db_url)
    conn = engine.connect()
    conn.execute("commit")

    # Drop the database if it exists and create a new one
    conn.execute(f"DROP DATABASE IF EXISTS {db_name}")
    conn.execute(f"CREATE DATABASE {db_name}")
    conn.close()

    # Run the migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    command.upgrade(alembic_cfg, "head")

    yield db_url

    # Drop the database
    conn = engine.connect()
    conn.execute("commit")
    conn.execute(f"DROP DATABASE {db_name}")
    conn.close()


@pytest.fixture(scope="session")
def test_engine(test_db_session: str) -> Engine:
    """
    Creates a SQLAlchemy engine for the test database.
    """
    engine = create_engine(test_db_session, future=True)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def test_session(test_engine: Engine):
    """
    Creates a SQLAlchemy session for a test function.
    """
    SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine, future=True
    )
    session = SessionLocal()
    session.begin()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def client_override(test_session: sessionmaker) -> TestClient:
    """
    Creates a TestClient with the get_db dependency overridden.
    """

    def override_get_db():
        yield test_session

    main.app.dependency_overrides[db.get_db] = override_get_db
    yield TestClient(main.app)
    del main.app.dependency_overrides[db.get_db]
