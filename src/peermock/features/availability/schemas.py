from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

from peermock.features.availability.models import Difficulty, SlotStatus


class SlotCreate(BaseModel):
    topic: str = Field(min_length=1, max_length=200)
    difficulty: Difficulty
    starts_at: AwareDatetime
    ends_at: AwareDatetime

    @model_validator(mode="after")
    def validate_time_window(self) -> "SlotCreate":
        if self.ends_at <= self.starts_at:
            raise ValueError("End time must be after start time")
        return self


class SlotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    mentor_id: UUID
    topic: str
    difficulty: Difficulty
    starts_at: AwareDatetime
    ends_at: AwareDatetime
    status: SlotStatus
