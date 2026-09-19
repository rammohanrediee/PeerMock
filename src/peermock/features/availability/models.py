"""Mentor-owned interview windows."""

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from peermock.db.base import Base
from peermock.db.mixins import RecordMixin


class SlotStatus(StrEnum):
    AVAILABLE = "available"
    BOOKED = "booked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Difficulty(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class InterviewSlot(RecordMixin, Base):
    __tablename__ = "interview_slots"
    __table_args__ = (CheckConstraint("ends_at > starts_at", name="slot_positive_duration"),)

    mentor_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    topic: Mapped[str] = mapped_column(String(200))
    difficulty: Mapped[Difficulty] = mapped_column(
        Enum(
            Difficulty,
            name="slot_difficulty",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        )
    )
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[SlotStatus] = mapped_column(
        Enum(
            SlotStatus,
            name="slot_status",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        default=SlotStatus.AVAILABLE,
    )
