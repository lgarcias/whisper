from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


def test_engine_connect(test_engine: Engine):
    """
    Tests that the test_engine fixture produces a usable engine.
    """
    with test_engine.connect() as conn:
        conn.execute(text("SELECT 1"))


def test_session_fixture(test_session: Session):
    """
    Tests that the test_session fixture produces a usable session.
    """
    assert test_session.is_active
    test_session.execute(text("SELECT 1"))
