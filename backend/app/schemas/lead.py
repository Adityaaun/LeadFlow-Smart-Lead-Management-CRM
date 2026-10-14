from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, field_validator
from backend.app.models.lead import LeadStatus
from backend.app.schemas.discussion import DiscussionResponse


class LeadBase(BaseModel):
    name: str = Field(..., max_length=255, description="Full name of lead")
    company: Optional[str] = Field(None, max_length=255, description="Company name")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")

    @field_validator("name")
    def validate_name_not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Lead name cannot be blank or whitespace-only")
        return v.strip()

    @field_validator("company", "phone", mode="before")
    def clean_optional_strings(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            v = v.strip()
            return v if v else None
        return v


class LeadCreate(LeadBase):
    status: Optional[LeadStatus] = Field(default=LeadStatus.NEW, description="Initial status defaulting to New")
    initial_note: Optional[str] = Field(None, description="Optional initial note when creating a lead")
    initial_follow_up_at: Optional[datetime] = Field(None, description="Optional initial follow-up datetime")

    @field_validator("initial_note", mode="before")
    def clean_initial_note(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            v = v.strip()
            return v if v else None
        return v


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
    is_overdue: bool = False

    model_config = ConfigDict(from_attributes=True)


class LeadDetail(LeadBase):
    id: int
    status: LeadStatus
    created_at: datetime
    updated_at: datetime
    discussions: List[DiscussionResponse] = []
    next_follow_up: Optional[datetime] = None
    is_today_follow_up: bool = False
    is_overdue: bool = False

    model_config = ConfigDict(from_attributes=True)
