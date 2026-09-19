"""Opt-in checks against migrated local PostgreSQL; all records are rolled back."""

import os
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from psycopg import Error
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from peermock.db.models import Booking, Feedback, InterviewSlot, User
from peermock.features.availability.models import Difficulty
from peermock.features.users.models import UserRole

pytestmark = pytest.mark.skipif(
    os.environ.get("PEERMOCK_RUN_DB_TESTS") != "1",
    reason="Set PEERMOCK_RUN_DB_TESTS=1 to check the migrated local database",
)


@pytest.fixture
def records() -> Iterator[tuple[Session, InterviewSlot, Booking]]:
    from peermock.core.config import settings

    engine = create_engine(settings.database_url, connect_args={"connect_timeout": 5})
    assert engine.url.host in {"localhost", "127.0.0.1", "::1"}
    assert engine.url.database == "peermock"
    try:
        with engine.connect() as connection:
            transaction = connection.begin()
            try:
                with Session(bind=connection, join_transaction_mode="create_savepoint") as session:
                    mentor = User(
                        email=f"{uuid4()}@example.test",
                        display_name="Mentor",
                        password_hash="test-only",
                        role=UserRole.MENTOR,
                    )
                    student = User(
                        email=f"{uuid4()}@example.test",
                        display_name="Student",
                        password_hash="test-only",
                        role=UserRole.STUDENT,
                    )
                    session.add_all([mentor, student])
                    session.flush()
                    start = datetime(2026, 10, 1, 12, tzinfo=UTC)
                    slot = InterviewSlot(
                        mentor_id=mentor.id,
                        topic="Constraint test",
                        difficulty=Difficulty.BEGINNER,
                        starts_at=start,
                        ends_at=start + timedelta(hours=1),
                    )
                    session.add(slot)
                    session.flush()
                    booking = Booking(student_id=student.id, slot_id=slot.id)
                    session.add(booking)
                    session.flush()
                    yield session, slot, booking
            finally:
                transaction.rollback()
    finally:
        engine.dispose()


def test_valid_records_and_duplicate_feedback(
    records: tuple[Session, InterviewSlot, Booking],
) -> None:
    session, slot, booking = records
    feedback = Feedback(
        booking_id=booking.id,
        mentor_id=slot.mentor_id,
        strengths="Clear",
        improvements="More examples",
    )
    session.add(feedback)
    session.flush()
    session.refresh(feedback)
    assert feedback.released_at is None
    assert feedback.created_at.tzinfo is not None
    with pytest.raises(IntegrityError) as failure, session.begin_nested():
        session.add(
            Feedback(
                booking_id=booking.id,
                mentor_id=slot.mentor_id,
                strengths="Duplicate",
                improvements="Duplicate",
            )
        )
        session.flush()
    assert isinstance(failure.value.orig, Error)
    assert failure.value.orig.sqlstate == "23505"
    assert session.get(Booking, booking.id) is booking


def test_missing_student_rejected(records: tuple[Session, InterviewSlot, Booking]) -> None:
    session, slot, _ = records
    with pytest.raises(IntegrityError) as failure, session.begin_nested():
        session.add(Booking(student_id=uuid4(), slot_id=slot.id))
        session.flush()
    assert isinstance(failure.value.orig, Error)
    assert failure.value.orig.sqlstate == "23503"
    assert session.get(InterviewSlot, slot.id) is slot


def test_invalid_duration_rejected(records: tuple[Session, InterviewSlot, Booking]) -> None:
    session, slot, _ = records
    with pytest.raises(IntegrityError) as failure, session.begin_nested():
        session.execute(
            text("UPDATE interview_slots SET ends_at = starts_at WHERE id = :id"), {"id": slot.id}
        )
    assert isinstance(failure.value.orig, Error)
    assert failure.value.orig.sqlstate == "23514"
    assert failure.value.orig.diag.constraint_name == "slot_positive_duration"
    session.refresh(slot)
    assert slot.ends_at > slot.starts_at
