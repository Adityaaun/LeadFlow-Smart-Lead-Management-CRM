from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class DiscussionBase(BaseModel):
    note: str = Field(..., min_length=1, description="Content of the discussion note")
    follow_up_at: Optional[datetime] = Field(None, description="Optional scheduled follow-up datetime")


class DiscussionCreate(DiscussionBase):
    pass


class DiscussionResponse(DiscussionBase):
    id: int
    lead_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
