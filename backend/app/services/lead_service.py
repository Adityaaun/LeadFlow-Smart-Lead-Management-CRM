from datetime import datetime, date, time
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc
from backend.app.models.lead import Lead, LeadStatus
from backend.app.models.discussion import Discussion
from backend.app.schemas.lead import (
    LeadCreate,
    LeadStatusUpdate,
    LeadListItem,
    LeadDetail,
)
from backend.app.schemas.discussion import DiscussionCreate, DiscussionResponse


def _safe_dt_compare_past(dt: datetime, ref_now: datetime) -> bool:
    """Compare datetime against reference now safely handling naive and aware datetimes."""
    if dt.tzinfo is not None and ref_now.tzinfo is None:
        dt = dt.astimezone().replace(tzinfo=None)
    elif dt.tzinfo is None and ref_now.tzinfo is not None:
        ref_now = ref_now.astimezone().replace(tzinfo=None)
    return dt < ref_now


def _safe_dt_is_today(dt: datetime, today_date: date) -> bool:
    """Check if datetime falls on today_date in local time."""
    if dt.tzinfo is not None:
        dt = dt.astimezone()
    return dt.date() == today_date


def _derive_lead_metadata(lead: Lead) -> dict:
    """Derive last note, note timestamp, next follow-up, is_today_follow_up, and is_overdue."""
    last_note = None
    last_note_created_at = None
    next_follow_up = None
    is_today = False
    is_overdue = False

    now = datetime.now()
    today_date = now.date()
    is_actionable = lead.status not in (LeadStatus.WON, LeadStatus.LOST)

    if lead.discussions:
        # Sort discussions by created_at descending, tie-breaking by id descending
        sorted_discussions = sorted(
            lead.discussions,
            key=lambda d: (d.created_at or datetime.min, d.id or 0),
            reverse=True,
        )
        latest_disc = sorted_discussions[0]
        last_note = latest_disc.note
        last_note_created_at = latest_disc.created_at

        # Find the most relevant scheduled follow-up
        for d in sorted_discussions:
            if d.follow_up_at:
                next_follow_up = d.follow_up_at
                if is_actionable:
                    if _safe_dt_is_today(d.follow_up_at, today_date):
                        is_today = True
                    if _safe_dt_compare_past(d.follow_up_at, now):
                        is_overdue = True
                break

    return {
        "last_note": last_note,
        "last_note_created_at": last_note_created_at,
        "next_follow_up": next_follow_up,
        "is_today_follow_up": is_today,
        "is_overdue": is_overdue,
    }


def get_leads(
    db: Session,
    status: Optional[str] = None,
    search: Optional[str] = None,
) -> List[LeadListItem]:
    """Retrieve list of leads with optional status filter and name/company search."""
    query = db.query(Lead).options(joinedload(Lead.discussions))

    if status and status.lower() != "all":
        # Match enum value case-insensitively
        matched_status = None
        for s in LeadStatus:
            if s.value.lower() == status.lower():
                matched_status = s
                break
        if matched_status:
            query = query.filter(Lead.status == matched_status)

    if search:
        search_filter = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Lead.name.ilike(search_filter),
                Lead.company.ilike(search_filter),
                Lead.phone.ilike(search_filter),
            )
        )

    # Order by updated_at descending
    leads = query.order_by(desc(Lead.updated_at)).all()

    result: List[LeadListItem] = []
    for lead in leads:
        meta = _derive_lead_metadata(lead)
        result.append(
            LeadListItem(
                id=lead.id,
                name=lead.name,
                company=lead.company,
                phone=lead.phone,
                status=lead.status,
                created_at=lead.created_at,
                updated_at=lead.updated_at,
                last_note=meta["last_note"],
                last_note_created_at=meta["last_note_created_at"],
                next_follow_up=meta["next_follow_up"],
                is_today_follow_up=meta["is_today_follow_up"],
                is_overdue=meta["is_overdue"],
            )
        )
    return result


def get_today_followups(db: Session) -> List[LeadListItem]:
    """Retrieve active leads that have follow-ups scheduled for today (excluding Won and Lost)."""
    today = datetime.now().date()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)

    # Find leads with discussions having follow_up_at today, excluding completed/lost leads
    leads = (
        db.query(Lead)
        .join(Discussion)
        .filter(
            Discussion.follow_up_at >= start_of_day,
            Discussion.follow_up_at <= end_of_day,
            Lead.status.notin_([LeadStatus.WON, LeadStatus.LOST]),
        )
        .options(joinedload(Lead.discussions))
        .distinct()
        .all()
    )

    result: List[LeadListItem] = []
    for lead in leads:
        meta = _derive_lead_metadata(lead)
        result.append(
            LeadListItem(
                id=lead.id,
                name=lead.name,
                company=lead.company,
                phone=lead.phone,
                status=lead.status,
                created_at=lead.created_at,
                updated_at=lead.updated_at,
                last_note=meta["last_note"],
                last_note_created_at=meta["last_note_created_at"],
                next_follow_up=meta["next_follow_up"],
                is_today_follow_up=True,
                is_overdue=meta["is_overdue"],
            )
        )
    return result


def get_lead_by_id(db: Session, lead_id: int) -> Optional[LeadDetail]:
    """Retrieve a single lead with full discussion timeline and overdue markers."""
    lead = (
        db.query(Lead)
        .options(joinedload(Lead.discussions))
        .filter(Lead.id == lead_id)
        .first()
    )
    if not lead:
        return None

    meta = _derive_lead_metadata(lead)
    now = datetime.now()
    is_actionable = lead.status not in (LeadStatus.WON, LeadStatus.LOST)

    # Discussions ordered chronologically descending (latest first)
    discussions_sorted = sorted(
        lead.discussions,
        key=lambda d: (d.created_at or datetime.min, d.id or 0),
        reverse=True,
    )
    disc_responses: List[DiscussionResponse] = []
    for d in discussions_sorted:
        d_overdue = False
        if d.follow_up_at and is_actionable:
            d_overdue = _safe_dt_compare_past(d.follow_up_at, now)
        disc_responses.append(
            DiscussionResponse(
                id=d.id,
                lead_id=d.lead_id,
                note=d.note,
                created_at=d.created_at,
                follow_up_at=d.follow_up_at,
                is_overdue=d_overdue,
            )
        )

    return LeadDetail(
        id=lead.id,
        name=lead.name,
        company=lead.company,
        phone=lead.phone,
        status=lead.status,
        created_at=lead.created_at,
        updated_at=lead.updated_at,
        discussions=disc_responses,
        next_follow_up=meta["next_follow_up"],
        is_today_follow_up=meta["is_today_follow_up"],
        is_overdue=meta["is_overdue"],
    )


def create_lead(db: Session, lead_in: LeadCreate) -> LeadDetail:
    """Create a new lead with optional initial note and follow-up."""
    new_lead = Lead(
        name=lead_in.name,
        company=lead_in.company,
        phone=lead_in.phone,
        status=lead_in.status or LeadStatus.NEW,
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    # Create initial note if provided, or default creation entry
    note_content = (
        lead_in.initial_note if lead_in.initial_note else "Lead created via web form."
    )
    initial_discussion = Discussion(
        lead_id=new_lead.id,
        note=note_content,
        follow_up_at=lead_in.initial_follow_up_at,
    )
    db.add(initial_discussion)
    db.commit()
    db.refresh(new_lead)

    return get_lead_by_id(db, new_lead.id)


def update_lead_status(
    db: Session, lead_id: int, status_update: LeadStatusUpdate
) -> Optional[LeadDetail]:
    """Update lead status."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return None

    lead.status = status_update.status
    lead.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(lead)

    return get_lead_by_id(db, lead.id)


def add_discussion(
    db: Session, lead_id: int, discussion_in: DiscussionCreate
) -> Optional[DiscussionResponse]:
    """Add a discussion note to an existing lead."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return None

    discussion = Discussion(
        lead_id=lead.id,
        note=discussion_in.note,
        follow_up_at=discussion_in.follow_up_at,
    )
    db.add(discussion)
    lead.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(discussion)

    now = datetime.now()
    is_actionable = lead.status not in (LeadStatus.WON, LeadStatus.LOST)
    d_overdue = False
    if discussion.follow_up_at and is_actionable:
        d_overdue = _safe_dt_compare_past(discussion.follow_up_at, now)

    return DiscussionResponse(
        id=discussion.id,
        lead_id=discussion.lead_id,
        note=discussion.note,
        created_at=discussion.created_at,
        follow_up_at=discussion.follow_up_at,
        is_overdue=d_overdue,
    )
