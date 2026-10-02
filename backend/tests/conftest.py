import pytest
from fastapi.testclient import TestClient

from app.db import connect
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "expenses.db"))
    with TestClient(app) as test_client:
        with connect() as conn:
            conn.execute("DELETE FROM expenses")
        yield test_client
