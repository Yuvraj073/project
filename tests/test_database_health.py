from contextlib import contextmanager

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

import database
import main


def test_check_database_connection_executes_select_one(monkeypatch):
    executed_statements = []

    class FakeConnection:
        def execute(self, statement):
            executed_statements.append(str(statement))

    @contextmanager
    def fake_connect():
        yield FakeConnection()

    monkeypatch.setattr(database.engine, "connect", fake_connect)

    database.check_database_connection()

    assert executed_statements == ["SELECT 1"]


def test_check_database_connection_propagates_connection_failure(monkeypatch):
    @contextmanager
    def fake_connect():
        raise OperationalError("connection", {}, Exception("private detail"))
        yield  # Makes this function a context manager without connecting.

    monkeypatch.setattr(database.engine, "connect", fake_connect)

    with pytest.raises(OperationalError):
        database.check_database_connection()


def test_database_health_endpoint_returns_generic_503_on_failure(monkeypatch):
    def fail_connection_check():
        raise OperationalError("connection", {}, Exception("private detail"))

    monkeypatch.setattr(main, "check_database_connection", fail_connection_check)
    client = TestClient(main.app)

    response = client.get("/health/db")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}
    assert "private detail" not in response.text
