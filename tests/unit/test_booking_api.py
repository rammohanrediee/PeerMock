from collections.abc import AsyncGenerator, Iterator
from datetime import UTC, datetime
from typing import cast
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

import peermock.features.bookings.router as booking_router
from peermock.core.auth import get_current_user
from peermock.db.session import get_db_session
from peermock.features.bookings.models import Booking, BookingStatus
from peermock.features.users.models import User, UserRole
from peermock.main import create_app

STUDENT_ID = UUID("00000000-0000-0000-0000-000000000001")
SLOT_ID = UUID("00000000-0000-0000-0000-000000000002")
BOOKING_ID = UUID("00000000-0000-0000-0000-000000000003")

ROUTES = [
    pytest.param("/api/v1/bookings", {"slot_id": str(SLOT_ID)}, 201, id="create"),
    pytest.param(f"/api/v1/bookings/{BOOKING_ID}/cancel", None, 200, id="cancel"),
]


@pytest.fixture
def application() -> Iterator[tuple[FastAPI, AsyncSession]]:
    app = create_app()
    session = cast(AsyncSession, object())

    async def database_dependency() -> AsyncGenerator[AsyncSession]:
        yield session

    app.dependency_overrides[get_db_session] = database_dependency
    yield app, session
    app.dependency_overrides.clear()


@pytest.mark.parametrize("path,body,student_status", ROUTES)
@pytest.mark.parametrize(
    "role",
    [UserRole.STUDENT, UserRole.MENTOR, UserRole.COORDINATOR],
)
def test_booking_routes_are_student_only(
    application: tuple[FastAPI, AsyncSession],
    monkeypatch: pytest.MonkeyPatch,
    path: str,
    body: dict[str, str] | None,
    student_status: int,
    role: UserRole,
) -> None:
    app, session = application
    user = User(
        id=STUDENT_ID,
        email=f"{role.value}@example.com",
        display_name=role.value,
        password_hash="test",
        role=role,
    )

    async def current_user() -> User:
        return user

    async def fake_book_slot(db: AsyncSession, student_id: UUID, slot_id: UUID) -> Booking:
        return Booking(
            id=BOOKING_ID,
            student_id=student_id,
            slot_id=slot_id,
            status=BookingStatus.CONFIRMED,
            created_at=datetime.now(UTC),
        )

    async def fake_cancel_booking(db: AsyncSession, student_id: UUID, booking_id: UUID) -> Booking:
        return Booking(
            id=booking_id,
            student_id=student_id,
            slot_id=SLOT_ID,
            status=BookingStatus.CANCELLED,
            created_at=datetime.now(UTC),
        )

    app.dependency_overrides[get_current_user] = current_user
    monkeypatch.setattr(booking_router, "book_slot", fake_book_slot)
    monkeypatch.setattr(booking_router, "cancel_booking", fake_cancel_booking)

    with TestClient(app) as client:
        response = client.post(
            path,
            params={"student_id": str(STUDENT_ID)},
            json=body,
        )

    if role is UserRole.STUDENT:
        assert response.status_code == student_status
    else:
        assert response.status_code == 403
        assert response.json()["code"] == "role_not_permitted"


SPOOFED_STUDENT_ID = UUID("00000000-0000-0000-0000-000000000004")


@pytest.mark.parametrize("path,body,student_status", ROUTES)
def test_booking_routes_ignore_client_student_id(
    application: tuple[FastAPI, AsyncSession],
    monkeypatch: pytest.MonkeyPatch,
    path: str,
    body: dict[str, str] | None,
    student_status: int,
) -> None:
    app, _ = application
    user = User(
        id=STUDENT_ID,
        email="student@example.com",
        display_name="Student",
        password_hash="test",
        role=UserRole.STUDENT,
    )

    async def current_user() -> User:
        return user

    async def fake_book_slot(
        session: AsyncSession,
        student_id: UUID,
        slot_id: UUID,
    ) -> Booking:
        assert student_id == STUDENT_ID
        return Booking(
            id=BOOKING_ID,
            student_id=student_id,
            slot_id=slot_id,
            status=BookingStatus.CONFIRMED,
            created_at=datetime.now(UTC),
        )

    async def fake_cancel_booking(
        session: AsyncSession,
        student_id: UUID,
        booking_id: UUID,
    ) -> Booking:
        assert student_id == STUDENT_ID
        return Booking(
            id=booking_id,
            student_id=student_id,
            slot_id=SLOT_ID,
            status=BookingStatus.CANCELLED,
            created_at=datetime.now(UTC),
        )

    app.dependency_overrides[get_current_user] = current_user
    monkeypatch.setattr(booking_router, "book_slot", fake_book_slot)
    monkeypatch.setattr(booking_router, "cancel_booking", fake_cancel_booking)

    with TestClient(app) as client:
        response = client.post(
            path,
            params={"student_id": str(SPOOFED_STUDENT_ID)},
            json=body,
        )

    assert response.status_code == student_status
    assert response.json()["student_id"] == str(STUDENT_ID)
