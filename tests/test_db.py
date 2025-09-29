import pytest
from sqlalchemy.exc import OperationalError

from backend.app import db


def test_engine_connect():
    """Test that the SQLAlchemy engine can connect and execute a simple query."""
    try:
        with db.get_engine().connect() as conn:
            from sqlalchemy import text

            conn.execute(text("SELECT 1"))
    except OperationalError as exc:
        pytest.fail(f"Database connection failed: {exc}")


def test_session_local():
    """Test that a session can be created and closed without error."""
    session = db.get_session_local()()
    try:
        assert session.is_active
    finally:
        session.close()


# def test_get_db_dependency():


def test_get_db_dependency():
    """Test that the get_db FastAPI dependency yields a session and closes it."""
    gen = db.get_db()
    session = next(gen)
    assert session.is_active
    try:
        next(gen)
    except StopIteration:
        pass
    else:
        pytest.fail("getDb generator did not stop after yielding session.")
