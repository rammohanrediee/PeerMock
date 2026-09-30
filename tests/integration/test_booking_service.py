"""Booking and scheduling HTTP flows against migrated PostgreSQL."""

import asyncio
import os
from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from peermock.core.auth import get_current_user
from peermock.core.config import settings
from peermock.db.session import get_db_session
from peermock.features.availability.models import Difficulty, InterviewSlot, SlotStatus
from peermock.features.bookings.models import Booking, BookingStatus
from peermock.features.users.models import User, UserRole
from peermock.main import create_app

pytestmark = pytest.mark.skipif(
    os.environ.get("PEERMOCK_RUN_DB_TESTS") != "1",
    reason="Set PEERMOCK_RUN_DB_TESTS=1 to check booking against PostgreSQL",
)


@asynccontextmanager
async def postgres_app_context() -> AsyncIterator[tuple[AsyncSession, FastAPI]]:
    engine = create_async_engine(
        settings.database_url,
        connect_args={"connect_timeout": 5},
    )
    assert engine.url.host in {"localhost", "127.0.0.1", "::1"}
    assert engine.url.database == "peermock"

    try:
        async with engine.connect() as connection:
            transaction = await connection.begin()
            try:
                async with AsyncSession(
                    bind=connection,
                    join_transaction_mode="create_savepoint",
                    expire_on_commit=False,
                ) as session:
                    application = create_app()

                    async def override_db_session() -> AsyncGenerator[AsyncSession]:
                        yield session

                    application.dependency_overrides[get_db_session] = override_db_session
                    try:
                        yield session, application
                    finally:
                        application.dependency_overrides.clear()
            finally:
                await transaction.rollback()
    finally:
        await engine.dispose()


def future_window() -> tuple[datetime, datetime]:
    starts_at = datetime.now(UTC) + timedelta(days=7)
    return starts_at, starts_at + timedelta(hours=1)


def make_user(display_name: str, role: UserRole) -> User:
    return User(
        email=f"{uuid4()}@example.test",
        display_name=display_name,
        password_hash="test-only",
        role=role,
    )


def make_slot(mentor_id: UUID, topic: str, starts_at: datetime) -> InterviewSlot:
    return InterviewSlot(
        mentor_id=mentor_id,
        topic=topic,
        difficulty=Difficulty.INTERMEDIATE,
        starts_at=starts_at,
        ends_at=starts_at + timedelta(hours=1),
    )


def authenticate_as(application: FastAPI, user: User) -> None:
    async def current_user() -> User:
        return user

    application.dependency_overrides[get_current_user] = current_user


def test_booking_http_flow_against_postgres() -> None:
    async def verify_flow() -> None:
        async with postgres_app_context() as (session, application):
            mentor = make_user("Synthetic Mentor", UserRole.MENTOR)
            first_student = make_user("First Synthetic Student", UserRole.STUDENT)
            second_student = make_user("Second Synthetic Student", UserRole.STUDENT)
            session.add_all([mentor, first_student, second_student])
            await session.flush()

            starts_at, _ = future_window()
            slot = make_slot(mentor.id, "Python", starts_at)
            overlapping_slot = make_slot(
                mentor.id,
                "Overlapping Python interview",
                starts_at + timedelta(minutes=30),
            )
            adjacent_slot = make_slot(
                mentor.id,
                "Adjacent Python interview",
                starts_at + timedelta(hours=1),
            )
            session.add_all([slot, overlapping_slot, adjacent_slot])
            await session.flush()

            async with AsyncClient(
                transport=ASGITransport(app=application),
                base_url="http://test",
            ) as client:
                authenticate_as(application, first_student)
                success_response = await client.post(
                    "/api/v1/bookings",
                    json={"slot_id": str(slot.id)},
                )

                authenticate_as(application, second_student)
                unavailable_response = await client.post(
                    "/api/v1/bookings",
                    json={"slot_id": str(slot.id)},
                )

                authenticate_as(application, first_student)
                overlap_response = await client.post(
                    "/api/v1/bookings",
                    json={"slot_id": str(overlapping_slot.id)},
                )
                adjacent_response = await client.post(
                    "/api/v1/bookings",
                    json={"slot_id": str(adjacent_slot.id)},
                )
                adjacent_booking_id = adjacent_response.json()["id"]

                authenticate_as(application, second_student)
                foreign_cancel_response = await client.post(
                    f"/api/v1/bookings/{adjacent_booking_id}/cancel",
                )

                authenticate_as(application, first_student)
                cancel_response = await client.post(
                    f"/api/v1/bookings/{adjacent_booking_id}/cancel",
                )
                repeat_cancel_response = await client.post(
                    f"/api/v1/bookings/{adjacent_booking_id}/cancel",
                )

            await session.refresh(slot)
            await session.refresh(overlapping_slot)
            await session.refresh(adjacent_slot)
            slot_booking_count = await session.scalar(
                select(func.count()).select_from(Booking).where(Booking.slot_id == slot.id)
            )
            overlap_booking_count = await session.scalar(
                select(func.count())
                .select_from(Booking)
                .where(Booking.slot_id == overlapping_slot.id)
            )
            adjacent_booking = await session.scalar(
                select(Booking).where(Booking.slot_id == adjacent_slot.id)
            )

            assert success_response.status_code == 201
            assert success_response.json()["status"] == "confirmed"
            assert unavailable_response.status_code == 409
            assert unavailable_response.json()["code"] == "slot_unavailable"
            assert overlap_response.status_code == 409
            assert overlap_response.json()["code"] == "student_schedule_conflict"
            assert adjacent_response.status_code == 201
            assert slot.status is SlotStatus.BOOKED
            assert overlapping_slot.status is SlotStatus.AVAILABLE
            assert adjacent_slot.status is SlotStatus.AVAILABLE
            assert slot_booking_count == 1
            assert overlap_booking_count == 0
            assert foreign_cancel_response.status_code == 404
            assert foreign_cancel_response.json()["code"] == "booking_not_found"
            assert cancel_response.status_code == 200
            assert cancel_response.json()["status"] == "cancelled"
            assert repeat_cancel_response.status_code == 409
            assert repeat_cancel_response.json()["code"] == "booking_not_cancelable"
            assert adjacent_booking is not None
            assert adjacent_booking.status is BookingStatus.CANCELLED

    asyncio.run(verify_flow())


def test_mentor_can_withdraw_booked_slot_against_postgres() -> None:
    async def verify_flow() -> None:
        async with postgres_app_context() as (session, application):
            mentor = make_user("Slot Owner", UserRole.MENTOR)
            foreign_mentor = make_user("Other Mentor", UserRole.MENTOR)
            student = make_user("Booking Student", UserRole.STUDENT)
            session.add_all([mentor, foreign_mentor, student])
            await session.flush()

            starts_at, _ = future_window()
            slot = make_slot(mentor.id, "Python", starts_at)
            session.add(slot)
            await session.flush()

            async with AsyncClient(
                transport=ASGITransport(app=application),
                base_url="http://test",
            ) as client:
                authenticate_as(application, student)
                booking_response = await client.post(
                    "/api/v1/bookings",
                    json={"slot_id": str(slot.id)},
                )

                authenticate_as(application, foreign_mentor)
                foreign_response = await client.delete(
                    f"/api/v1/slots/{slot.id}/withdraw",
                )

                authenticate_as(application, mentor)
                withdraw_response = await client.delete(
                    f"/api/v1/slots/{slot.id}/withdraw",
                )

            await session.refresh(slot)
            booking = await session.scalar(select(Booking).where(Booking.slot_id == slot.id))

            assert booking_response.status_code == 201
            assert foreign_response.status_code == 404
            assert foreign_response.json()["code"] == "slot_not_found"
            assert withdraw_response.status_code == 200
            assert withdraw_response.json()["status"] == "cancelled"
            assert slot.status is SlotStatus.CANCELLED
            assert booking is not None
            assert booking.status is BookingStatus.CANCELLED

    asyncio.run(verify_flow())


def test_temporary_scheduling_vertical_slice_against_postgres() -> None:
    async def verify_flow() -> None:
        async with postgres_app_context() as (session, application):
            mentor = make_user("Vertical Slice Mentor", UserRole.MENTOR)
            student = make_user("Vertical Slice Student", UserRole.STUDENT)
            session.add_all([mentor, student])
            await session.flush()
            starts_at, ends_at = future_window()

            async with AsyncClient(
                transport=ASGITransport(app=application),
                base_url="http://test",
            ) as client:
                authenticate_as(application, mentor)
                create_response = await client.post(
                    "/api/v1/slots",
                    json={
                        "topic": "Temporary vertical slice",
                        "difficulty": "beginner",
                        "starts_at": starts_at.isoformat(),
                        "ends_at": ends_at.isoformat(),
                    },
                )
                slot_id = create_response.json()["id"]
                list_response = await client.get("/api/v1/slots")

                authenticate_as(application, student)
                booking_response = await client.post(
                    "/api/v1/bookings",
                    json={"slot_id": slot_id},
                )
                cancel_response = await client.post(
                    f"/api/v1/bookings/{booking_response.json()['id']}/cancel",
                )

            slot = await session.get(InterviewSlot, UUID(slot_id))
            assert create_response.status_code == 201
            assert create_response.json()["status"] == "available"
            assert list_response.status_code == 200
            assert any(item["id"] == slot_id for item in list_response.json())
            assert booking_response.status_code == 201
            assert booking_response.json()["status"] == "confirmed"
            assert cancel_response.status_code == 200
            assert cancel_response.json()["status"] == "cancelled"
            assert slot is not None
            assert slot.status is SlotStatus.AVAILABLE

    asyncio.run(verify_flow())
