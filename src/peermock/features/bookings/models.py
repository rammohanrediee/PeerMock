"""Student reservations, including retained cancellation history."""

from enum import StrEnum
from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from peermock.db.base import Base
from peermock.db.mixins import RecordMixin


class BookingStatus(StrEnum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"


class Booking(RecordMixin, Base):
    __tablename__ = "bookings"

    student_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    slot_id: Mapped[UUID] = mapped_column(ForeignKey("interview_slots.id"), index=True)
    status: Mapped[BookingStatus] = mapped_column(
        Enum(
            BookingStatus,
            name="booking_status",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        default=BookingStatus.CONFIRMED,
    )
