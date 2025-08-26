"""
Pytest configuration and fixtures for Capper chatbot tests.
Sets up test database, client, and handles teardown.
"""
import os
import shutil
import pytest
import sqlalchemy
from fastapi.testclient import TestClient

@pytest.fixture(scope="session", autouse=True)
def test_db(monkeypatch, tmp_path_factory):
    """
    1) Copy the prod DB to a tmp file
    2) Monkey‑patch db.DB_PATH before importing anything else
    3) Re‑create db.engine & SessionLocal
    4) Truncate Conversation_History via SQLAlchemy
    """
    # 1) Copy SQLite
    src_db = os.path.join("data", "Carton_Caps_Data.sqlite")
    dst_dir = tmp_path_factory.mktemp("db")
    dst_db  = dst_dir / "test.db"
    shutil.copy(src_db, dst_db)

    # 2) Force db.py to pick up our test copy
    import importlib
    import db as real_db
    monkeypatch.setattr(real_db, "DB_PATH", str(dst_db))

    # 3) Dispose old engine, recreate with new path
    real_db.engine.dispose()
    real_db.engine = sqlalchemy.create_engine(
        f"sqlite:///{real_db.DB_PATH}", connect_args={"check_same_thread": False}
    )
    real_db.SessionLocal = sqlalchemy.orm.sessionmaker(bind=real_db.engine)
    real_db.init_db()

    # 4) Truncate via SQLAlchemy
    session = real_db.SessionLocal()
    session.execute(sqlalchemy.text("DELETE FROM Conversation_History;"))
    session.commit()
    session.close()

    yield

    # teardown
    real_db.engine.dispose()

@pytest.fixture
def client():
    """
    Returns a FastAPI test client for API testing.
    """
    from app import app
    return TestClient(app)

@pytest.fixture
def sample_user():
    return 1
