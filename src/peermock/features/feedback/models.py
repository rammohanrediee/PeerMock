"""One private assessment per booking, explicitly released later."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from peermock.db.base import Base
from peermock.db.mixins import RecordMixin


class Feedback(RecordMixin, Base):
    __tablename__ = "feedback"

    booking_id: Mapped[UUID] = mapped_column(ForeignKey("bookings.id"), unique=True)
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    strengths: Mapped[str] = mapped_column(Text)
    improvements: Mapped[str] = mapped_column(Text)
    released_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
