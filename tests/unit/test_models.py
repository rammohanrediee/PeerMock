"""Portable integrity smoke tests; PostgreSQL migration tests follow in S1E5."""

from collections.abc import Iterator
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from peermock.db.base import Base
from peermock.db.models import Booking, Feedback, InterviewSlot, User
from peermock.features.availability.models import Difficulty
from peermock.features.users.models import UserRole


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite://")

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection: object, record: object) -> None:
        from sqlite3 import Connection

        assert isinstance(connection, Connection)
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    with Session(engine) as value:
        yield value
    engine.dispose()


def create_slot(session: Session) -> InterviewSlot:
    mentor = User(
        email="mentor@example.test",
        display_name="Mentor",
        password_hash="test-only-hash",
        role=UserRole.MENTOR,
    )
    session.add(mentor)
    session.flush()
    start = datetime(2026, 10, 1, 12, tzinfo=UTC)
    slot = InterviewSlot(
        mentor_id=mentor.id,
        topic="Python",
        difficulty=Difficulty.BEGINNER,
        starts_at=start,
        ends_at=start + timedelta(hours=1),
    )
    session.add(slot)
    session.flush()
    return slot


def test_booking_and_private_feedback_round_trip(session: Session) -> None:
    slot = create_slot(session)
    student = User(
        email="student@example.test",
        display_name="Student",
        password_hash="test-only-hash",
        role=UserRole.STUDENT,
    )
    session.add(student)
    session.flush()
    booking = Booking(student_id=student.id, slot_id=slot.id)
    session.add(booking)
    session.flush()
    feedback = Feedback(
        booking_id=booking.id,
        mentor_id=slot.mentor_id,
        strengths="Clear explanation",
        improvements="Add edge cases",
    )
    session.add(feedback)
    session.commit()
    session.expire_all()
    saved = session.get(Feedback, feedback.id)
    assert saved is not None
    assert saved.booking_id == booking.id
    assert saved.released_at is None

    session.add(
        Feedback(
            booking_id=booking.id,
            mentor_id=slot.mentor_id,
            strengths="Duplicate",
            improvements="Duplicate",
        )
    )
    with pytest.raises(IntegrityError):
        session.flush()


def test_slot_rejects_nonpositive_duration(session: Session) -> None:
    slot = create_slot(session)
    slot.ends_at = slot.starts_at
    with pytest.raises(IntegrityError):
        session.flush()


def test_booking_rejects_missing_student(session: Session) -> None:
    from uuid import uuid4

    slot = create_slot(session)
    session.add(Booking(student_id=uuid4(), slot_id=slot.id))
    with pytest.raises(IntegrityError):
        session.flush()
