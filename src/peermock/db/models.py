"""Import all models to register their tables for migrations and metadata tools."""

from peermock.features.availability.models import InterviewSlot
from peermock.features.bookings.models import Booking
from peermock.features.feedback.models import Feedback
from peermock.features.users.models import User

__all__ = ["Booking", "Feedback", "InterviewSlot", "User"]
