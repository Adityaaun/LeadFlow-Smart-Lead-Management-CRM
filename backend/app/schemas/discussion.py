from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class DiscussionBase(BaseModel):
    note: str = Field(..., description="Content of the discussion note")
    follow_up_at: Optional[datetime] = Field(None, description="Optional scheduled follow-up datetime")

    @field_validator("note")
    def validate_note_not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Discussion note cannot be blank or whitespace-only")
        return v.strip()


class DiscussionCreate(DiscussionBase):
    pass


class DiscussionResponse(DiscussionBase):
    id: int
    lead_id: int
    created_at: datetime
    is_overdue: bool = False

    model_config = ConfigDict(from_attributes=True)
