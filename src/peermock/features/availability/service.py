from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from peermock.features.availability.models import InterviewSlot
from peermock.features.availability.schemas import SlotCreate


async def create_slot(
    session: AsyncSession,
    mentor_id: UUID,
    data: SlotCreate,
) -> InterviewSlot:
    slot = InterviewSlot(
        mentor_id=mentor_id,
        topic=data.topic,
        difficulty=data.difficulty,
        starts_at=data.starts_at,
        ends_at=data.ends_at,
    )
    session.add(slot)
    await session.commit()
    await session.refresh(slot)
    return slot


async def get_slot(
    session: AsyncSession,
    slot_id: UUID,
) -> InterviewSlot | None:
    slot = select(InterviewSlot).where(InterviewSlot.id == slot_id)
    result = await session.execute(slot)
    return result.scalar_one_or_none()


async def list_slots(
    session: AsyncSession,
) -> list[InterviewSlot]:
    slot = select(InterviewSlot).order_by(InterviewSlot.starts_at)
    result = await session.execute(slot)
    return list(result.scalars().all())
