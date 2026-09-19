"""Persisted user identity; authentication belongs in services."""

from enum import StrEnum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from peermock.db.base import Base
from peermock.db.mixins import RecordMixin


class UserRole(StrEnum):
    STUDENT = "student"
    MENTOR = "mentor"
    COORDINATOR = "coordinator"


class User(RecordMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True)
    display_name: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="user_role",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        )
    )
