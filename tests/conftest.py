import os
from urllib.parse import urlparse

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


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
