from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from backend.app.models.lead import LeadStatus
from backend.app.schemas.discussion import DiscussionResponse


class LeadBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Full name of lead")
    company: Optional[str] = Field(None, max_length=255, description="Company name")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")


class LeadCreate(LeadBase):
    status: Optional[LeadStatus] = Field(default=LeadStatus.NEW, description="Initial status defaulting to New")
    initial_note: Optional[str] = Field(None, description="Optional initial note when creating a lead")
    initial_follow_up_at: Optional[datetime] = Field(None, description="Optional initial follow-up datetime")


class LeadStatusUpdate(BaseModel):
    status: LeadStatus = Field(..., description="Target lead status")


class LeadListItem(LeadBase):
    id: int
    status: LeadStatus
    created_at: datetime
    updated_at: datetime
    last_note: Optional[str] = None
    last_note_created_at: Optional[datetime] = None
    next_follow_up: Optional[datetime] = None
    is_today_follow_up: bool = False

    model_config = ConfigDict(from_attributes=True)


class LeadDetail(LeadBase):
    id: int
    status: LeadStatus
    created_at: datetime
    updated_at: datetime
    discussions: List[DiscussionResponse] = []
    next_follow_up: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
