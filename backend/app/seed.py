"""
Seed script to populate initial sample leads matching the assessment reference design.
Run with: python -m backend.app.seed
"""
from datetime import datetime, timedelta, time
from backend.app.core.database import SessionLocal, Base, engine
from backend.app.models.lead import Lead, LeadStatus
from backend.app.models.discussion import Discussion


def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if database is already seeded
        if db.query(Lead).count() > 0:
            print("Database already contains data. Skipping seed.")
            return

        now = datetime.now()
        today = now.date()

        # Follow-up for today at 2:00 PM (14:00)
        today_follow_up = datetime.combine(today, time(14, 0))

        # 1. Sarah Connor (Acme Corp) - With today's pinned follow-up
        sarah = Lead(
            name="Sarah Connor",
            company="Acme Corp",
            phone="555-0199",
            status=LeadStatus.PROPOSAL_SENT,
            created_at=now - timedelta(days=6),
            updated_at=now - timedelta(days=2),
        )
        db.add(sarah)
        db.flush()

        # Sarah's discussions
        d1 = Discussion(
            lead_id=sarah.id,
            note="Lead created via web form.",
            created_at=now - timedelta(days=6),
        )
        d2 = Discussion(
            lead_id=sarah.id,
            note="Initial discovery call. They need a CRM for 50 reps. Pain points include dropping leads and no follow-up tracking.",
            created_at=now - timedelta(days=5),
        )
        d3 = Discussion(
            lead_id=sarah.id,
            note="Sent pricing tier PDF. Said she would review with her boss.",
            created_at=now - timedelta(days=2),
            follow_up_at=today_follow_up,
        )
        db.add_all([d1, d2, d3])

        # 2. Hank Scorpio (Globex) - New Lead
        hank = Lead(
            name="Hank Scorpio",
            company="Globex",
            phone="555-0142",
            status=LeadStatus.NEW,
            created_at=now - timedelta(hours=2),
            updated_at=now - timedelta(hours=2),
        )
        db.add(hank)
        db.flush()

        d4 = Discussion(
            lead_id=hank.id,
            note="Inbound lead from website contact form.",
            created_at=now - timedelta(hours=2),
        )
        db.add(d4)

        # 3. Bill Lumbergh (Initech) - Contacted
        bill = Lead(
            name="Bill Lumbergh",
            company="Initech",
            phone="555-0188",
            status=LeadStatus.CONTACTED,
            created_at=now - timedelta(days=7),
            updated_at=now - timedelta(days=7),
        )
        db.add(bill)
        db.flush()

        d5 = Discussion(
            lead_id=bill.id,
            note="Left a voicemail with his assistant.",
            created_at=now - timedelta(days=7),
        )
        db.add(d5)

        # 4. Bruce Wayne (Wayne Ent) - Won
        bruce = Lead(
            name="Bruce Wayne",
            company="Wayne Ent",
            phone="555-0100",
            status=LeadStatus.WON,
            created_at=now - timedelta(days=21),
            updated_at=now - timedelta(days=21),
        )
        db.add(bruce)
        db.flush()

        d6 = Discussion(
            lead_id=bruce.id,
            note="Contract signed! Sending welcome package.",
            created_at=now - timedelta(days=21),
        )
        db.add(d6)

        db.commit()
        print("Database successfully seeded with realistic sample leads!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
