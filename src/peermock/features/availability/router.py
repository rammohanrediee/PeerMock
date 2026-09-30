from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from peermock.core.auth import get_current_user, require_roles
from peermock.core.errors import DomainError
from peermock.db.session import get_db_session
from peermock.features.availability.schemas import SlotCreate, SlotRead
from peermock.features.availability.service import create_slot, get_slot, list_slots, withdraw_slot
from peermock.features.users.models import User, UserRole

router = APIRouter()


@router.post(
    "/slots",
    response_model=SlotRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(UserRole.MENTOR))],
)
async def create_slot_endpoint(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
    data: SlotCreate,
) -> SlotRead:
    slot = await create_slot(session, current_user.id, data)
    return SlotRead.model_validate(slot)


@router.get(
    "/slots/{slot_id}",
    response_model=SlotRead,
)
async def read_slot(
    slot_id: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SlotRead:
    slot = await get_slot(session, slot_id)
    if not slot:
        raise DomainError(
            status_code=status.HTTP_404_NOT_FOUND,
            code="slot_not_found",
            message=f"Slot with ID {slot_id} not found",
        )
    return SlotRead.model_validate(slot)


@router.get(
    "/slots",
    response_model=list[SlotRead],
)
async def read_slots(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[SlotRead]:
    slots = await list_slots(session)
    return [SlotRead.model_validate(slot) for slot in slots]


@router.delete(
    "/slots/{slot_id}/withdraw",
    status_code=200,
    response_model=SlotRead,
    dependencies=[Depends(require_roles(UserRole.MENTOR))],
)
async def withdraw_slot_endpoint(
    slot_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SlotRead:
    withdrawn_slot = await withdraw_slot(
        session=session, mentor_id=current_user.id, slot_id=slot_id
    )
    return SlotRead.model_validate(withdrawn_slot)
