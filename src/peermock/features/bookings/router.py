from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from peermock.core.auth import get_current_user, require_roles
from peermock.db.session import get_db_session
from peermock.features.bookings.schemas import BookingCreate, BookingRead
from peermock.features.bookings.service import book_slot, cancel_booking
from peermock.features.users.models import User, UserRole

router = APIRouter(tags=["bookings"])


@router.post(
    "/bookings",
    status_code=201,
    response_model=BookingRead,
    dependencies=[Depends(require_roles(UserRole.STUDENT))],
)
async def create_booking(
    booking: BookingCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> BookingRead:
    new_booking = await book_slot(session, current_user.id, booking.slot_id)
    return BookingRead.model_validate(new_booking)


@router.post(
    "/bookings/{booking_id}/cancel",
    status_code=200,
    response_model=BookingRead,
    dependencies=[Depends(require_roles(UserRole.STUDENT))],
)
async def cancel_booking_point(
    booking_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> BookingRead:

    canceled_booking = await cancel_booking(session, current_user.id, booking_id)
    return BookingRead.model_validate(canceled_booking)
