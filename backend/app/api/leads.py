from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.lead import (
    LeadCreate,
    LeadStatusUpdate,
    LeadListItem,
    LeadDetail,
)
from backend.app.schemas.discussion import DiscussionCreate, DiscussionResponse
from backend.app.services import lead_service

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get("", response_model=List[LeadListItem], summary="List all leads")
def list_leads(
    status: Optional[str] = Query(None, description="Filter by status (e.g. New, Contacted, Qualified, Proposal Sent, Won, Lost)"),
    search: Optional[str] = Query(None, description="Search term matching lead name, company, or phone"),
    db: Session = Depends(get_db),
):
    """List leads with optional status filtering and full-text keyword search."""
    return lead_service.get_leads(db, status=status, search=search)


@router.get("/today-followups", response_model=List[LeadListItem], summary="Get today's pinned follow-ups")
def get_today_followups(
    db: Session = Depends(get_db),
):
    """Retrieve leads that have follow-ups scheduled for today's date."""
    return lead_service.get_today_followups(db)


@router.get("/{lead_id}", response_model=LeadDetail, summary="Get lead details with timeline")
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db),
):
    """Get lead details including complete discussion history and notes."""
    lead = lead_service.get_lead_by_id(db, lead_id=lead_id)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lead with id {lead_id} not found",
        )
    return lead


@router.post("", response_model=LeadDetail, status_code=status.HTTP_201_CREATED, summary="Create a new lead")
def create_lead(
    lead_in: LeadCreate,
    db: Session = Depends(get_db),
):
    """Create a new lead defaulting to New status with optional initial note and follow-up."""
    return lead_service.create_lead(db, lead_in=lead_in)


@router.patch("/{lead_id}/status", response_model=LeadDetail, summary="Update lead status")
def update_lead_status(
    lead_id: int,
    status_update: LeadStatusUpdate,
    db: Session = Depends(get_db),
):
    """Update lead status to one of New, Contacted, Qualified, Proposal Sent, Won, or Lost."""
    lead = lead_service.update_lead_status(db, lead_id=lead_id, status_update=status_update)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lead with id {lead_id} not found",
        )
    return lead


@router.post(
    "/{lead_id}/discussions",
    response_model=DiscussionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a discussion note to a lead",
)
def add_discussion(
    lead_id: int,
    discussion_in: DiscussionCreate,
    db: Session = Depends(get_db),
):
    """Log a discussion note and optionally set/update follow-up date and time."""
    discussion = lead_service.add_discussion(db, lead_id=lead_id, discussion_in=discussion_in)
    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lead with id {lead_id} not found",
        )
    return discussion
