from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from peermock.core.errors import DomainError
from peermock.db.session import get_db_session
from peermock.features.availability.schemas import SlotCreate, SlotRead
from peermock.features.availability.service import create_slot, get_slot, list_slots

router = APIRouter()


@router.post(
    "/slots",
    response_model=SlotRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_slot_endpoint(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    mentor_id: UUID,
    data: SlotCreate,
) -> SlotRead:
    slot = await create_slot(session, mentor_id, data)
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
