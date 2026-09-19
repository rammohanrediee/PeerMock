"""Tests for API liveness and readiness."""

from collections.abc import AsyncGenerator, Iterator
from typing import cast

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from peermock.db.session import get_db_session
from peermock.main import create_app


class FakeSession:
    def __init__(
        self,
        result: int | None = 1,
        failure: SQLAlchemyError | None = None,
    ) -> None:
        self.result = result
        self.failure = failure

    async def scalar(self, statement: object) -> int | None:
        del statement

        if self.failure is not None:
            raise self.failure

        return self.result


@pytest.fixture
def application() -> Iterator[FastAPI]:
    value = create_app()
    yield value
    value.dependency_overrides.clear()


def override_database(
    application: FastAPI,
    fake_session: FakeSession,
) -> None:
    async def database_dependency() -> AsyncGenerator[AsyncSession]:
        yield cast(AsyncSession, fake_session)

    application.dependency_overrides[get_db_session] = database_dependency


def test_liveness_returns_ok(application: FastAPI) -> None:
    with TestClient(application) as client:
        response = client.get("/api/v1/health/live")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


def test_readiness_returns_ok_when_database_responds(
    application: FastAPI,
) -> None:
    override_database(application, FakeSession(result=1))

    with TestClient(application) as client:
        response = client.get("/api/v1/health/ready")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


def test_readiness_returns_503_when_database_fails(
    application: FastAPI,
) -> None:
    failure = SQLAlchemyError("private database failure")
    override_database(application, FakeSession(failure=failure))

    with TestClient(application) as client:
        response = client.get("/api/v1/health/ready")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == {
        "code": "database_unavailable",
        "message": "Database is unavailable",
    }
    assert "private database failure" not in response.text


def test_readiness_returns_503_for_unexpected_answer(
    application: FastAPI,
) -> None:
    override_database(application, FakeSession(result=None))

    with TestClient(application) as client:
        response = client.get("/api/v1/health/ready")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == {
        "code": "database_unavailable",
        "message": "Database is unavailable",
    }