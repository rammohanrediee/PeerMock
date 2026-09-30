from collections.abc import AsyncGenerator, Iterator
from datetime import UTC, datetime, timedelta
from typing import cast
from uuid import UUID

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

import peermock.features.availability.router as availability_router_module
from peermock.core.auth import get_current_user
from peermock.db.session import get_db_session
from peermock.features.availability.models import (
    Difficulty,
    InterviewSlot,
    SlotStatus,
)
from peermock.features.availability.schemas import SlotCreate
from peermock.features.users.models import User, UserRole
from peermock.main import create_app

MENTOR_ID = UUID("00000000-0000-0000-0000-000000000001")
SLOT_ID = UUID("00000000-0000-0000-0000-000000000002")
STARTS_AT = datetime(2026, 10, 1, 12, tzinfo=UTC)
SPOOFED_MENTOR_ID = UUID("00000000-0000-0000-0000-000000000004")
CREATE_SLOT_REQUEST = {
    "topic": "Python",
    "difficulty": "beginner",
    "starts_at": "2026-10-01T12:00:00Z",
    "ends_at": "2026-10-01T13:00:00Z",
}


@pytest.fixture
def application() -> Iterator[tuple[FastAPI, AsyncSession]]:
    app = create_app()
    fake_session = cast(AsyncSession, object())

    async def database_dependency() -> AsyncGenerator[AsyncSession]:
        yield fake_session

    app.dependency_overrides[get_db_session] = database_dependency
    yield app, fake_session
    app.dependency_overrides.clear()


def test_create_slot_returns_created_contract(
    application: tuple[FastAPI, AsyncSession],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app, fake_session = application
    mentor = User(
        id=MENTOR_ID,
        email="mentor@example.com",
        display_name="Mentor",
        password_hash="test",
        role=UserRole.MENTOR,
    )

    async def current_mentor() -> User:
        return mentor

    app.dependency_overrides[get_current_user] = current_mentor

    # Arrange
    async def fake_create_slot(
        session: AsyncSession,
        mentor_id: UUID,
        data: SlotCreate,
    ) -> InterviewSlot:
        assert session is fake_session
        assert mentor_id == MENTOR_ID
        assert data.topic == "Python"
        assert data.difficulty is Difficulty.BEGINNER
        assert data.starts_at == STARTS_AT
        assert data.ends_at == STARTS_AT + timedelta(hours=1)

        return InterviewSlot(
            id=SLOT_ID,
            mentor_id=mentor_id,
            topic=data.topic,
            difficulty=data.difficulty,
            starts_at=data.starts_at,
            ends_at=data.ends_at,
            status=SlotStatus.AVAILABLE,
        )

    monkeypatch.setattr(
        availability_router_module,
        "create_slot",
        fake_create_slot,
    )

    # Act
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/slots",
            params={"mentor_id": str(SPOOFED_MENTOR_ID)},
            json=CREATE_SLOT_REQUEST,
        )

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": str(SLOT_ID),
        "mentor_id": str(MENTOR_ID),
        "topic": "Python",
        "difficulty": "beginner",
        "starts_at": "2026-10-01T12:00:00Z",
        "ends_at": "2026-10-01T13:00:00Z",
        "status": "available",
    }


@pytest.mark.parametrize("role", [UserRole.STUDENT, UserRole.COORDINATOR])
def test_create_slot_rejects_non_mentor_roles(
    application: tuple[FastAPI, AsyncSession],
    role: UserRole,
) -> None:
    app, _ = application
    user = User(
        email=f"{role.value}@example.com",
        display_name=role.value,
        password_hash="test",
        role=role,
    )

    async def current_user() -> User:
        return user

    app.dependency_overrides[get_current_user] = current_user

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/slots",
            params={"mentor_id": str(MENTOR_ID)},
            json=CREATE_SLOT_REQUEST,
        )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["code"] == "role_not_permitted"


@pytest.mark.parametrize(
    "headers",
    [{}, {"Authorization": "Bearer invalid-token"}],
)
def test_create_slot_rejects_missing_or_invalid_token(
    application: tuple[FastAPI, AsyncSession],
    headers: dict[str, str],
) -> None:
    app, _ = application

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/slots",
            params={"mentor_id": str(MENTOR_ID)},
            json=CREATE_SLOT_REQUEST,
            headers=headers,
        )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["code"] == "invalid_token"


@pytest.mark.parametrize(
    ("role", "expected_status"),
    [
        (UserRole.MENTOR, status.HTTP_200_OK),
        (UserRole.STUDENT, status.HTTP_403_FORBIDDEN),
        (UserRole.COORDINATOR, status.HTTP_403_FORBIDDEN),
    ],
)
def test_withdraw_slot_requires_mentor_role(
    application: tuple[FastAPI, AsyncSession],
    monkeypatch: pytest.MonkeyPatch,
    role: UserRole,
    expected_status: int,
) -> None:
    app, fake_session = application
    user = User(
        id=MENTOR_ID,
        email=f"{role.value}@example.com",
        display_name=role.value,
        password_hash="test",
        role=role,
    )

    async def current_user() -> User:
        return user

    async def fake_withdraw_slot(
        session: AsyncSession,
        mentor_id: UUID,
        slot_id: UUID,
    ) -> InterviewSlot:
        assert session is fake_session
        assert mentor_id == MENTOR_ID
        return InterviewSlot(
            id=slot_id,
            mentor_id=mentor_id,
            topic="Python",
            difficulty=Difficulty.BEGINNER,
            starts_at=STARTS_AT,
            ends_at=STARTS_AT + timedelta(hours=1),
            status=SlotStatus.CANCELLED,
        )

    app.dependency_overrides[get_current_user] = current_user
    monkeypatch.setattr(
        availability_router_module,
        "withdraw_slot",
        fake_withdraw_slot,
    )

    with TestClient(app) as client:
        response = client.delete(
            f"/api/v1/slots/{SLOT_ID}/withdraw",
            params={"mentor_id": str(SPOOFED_MENTOR_ID)},
        )

    assert response.status_code == expected_status
    if role is not UserRole.MENTOR:
        assert response.json()["code"] == "role_not_permitted"
