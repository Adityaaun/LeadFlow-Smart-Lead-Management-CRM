from datetime import datetime, timedelta
import pytest


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "leadflow-api"


def test_create_lead_default_status(client):
    payload = {
        "name": "Bruce Wayne",
        "company": "Wayne Enterprises",
        "phone": "555-0100",
    }
    response = client.post("/api/leads", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Bruce Wayne"
    assert data["company"] == "Wayne Enterprises"
    assert data["phone"] == "555-0100"
    assert data["status"] == "New"
    assert len(data["discussions"]) == 1
    assert "web form" in data["discussions"][0]["note"].lower()


def test_create_lead_with_custom_note(client):
    payload = {
        "name": "Clark Kent",
        "company": "Daily Planet",
        "phone": "555-0199",
        "initial_note": "Referred by Perry White.",
    }
    response = client.post("/api/leads", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert len(data["discussions"]) == 1
    assert data["discussions"][0]["note"] == "Referred by Perry White."


def test_validation_missing_or_whitespace_name(client):
    # Missing name
    res1 = client.post("/api/leads", json={"company": "No Name Corp"})
    assert res1.status_code == 422

    # Whitespace-only name
    res2 = client.post("/api/leads", json={"name": "   ", "company": "Spaces Inc"})
    assert res2.status_code == 422
    assert "blank" in res2.text.lower() or "whitespace" in res2.text.lower()


def test_validation_blank_discussion_note(client):
    lead = client.post("/api/leads", json={"name": "Diana Prince"}).json()
    lead_id = lead["id"]

    # Blank note
    res = client.post(f"/api/leads/{lead_id}/discussions", json={"note": "   "})
    assert res.status_code == 422
    assert "blank" in res.text.lower() or "whitespace" in res.text.lower()


def test_validation_invalid_status(client):
    lead = client.post("/api/leads", json={"name": "Hal Jordan"}).json()
    lead_id = lead["id"]

    res = client.patch(f"/api/leads/{lead_id}/status", json={"status": "NonExistentStatus"})
    assert res.status_code == 422


def test_list_and_filter_leads(client):
    client.post("/api/leads", json={"name": "Alice Smith", "company": "Alpha Inc"}).json()
    lead2 = client.post("/api/leads", json={"name": "Bob Jones", "company": "Beta LLC"}).json()

    # Update lead2 status to Qualified
    client.patch(f"/api/leads/{lead2['id']}/status", json={"status": "Qualified"})

    # List all
    all_resp = client.get("/api/leads")
    assert all_resp.status_code == 200
    all_data = all_resp.json()
    assert len(all_data) == 2

    # Filter by New
    new_resp = client.get("/api/leads?status=New")
    assert new_resp.status_code == 200
    new_data = new_resp.json()
    assert len(new_data) == 1
    assert new_data[0]["name"] == "Alice Smith"

    # Filter by Qualified
    qual_resp = client.get("/api/leads?status=Qualified")
    assert qual_resp.status_code == 200
    qual_data = qual_resp.json()
    assert len(qual_data) == 1
    assert qual_data[0]["name"] == "Bob Jones"


def test_search_leads(client):
    client.post("/api/leads", json={"name": "Tony Stark", "company": "Stark Industries"}).json()
    client.post("/api/leads", json={"name": "Peter Parker", "company": "Daily Bugle"}).json()

    # Search by full name
    res = client.get("/api/leads?search=Tony Stark")
    assert res.status_code == 200
    assert len(res.json()) == 1

    # Search by partial name
    res2 = client.get("/api/leads?search=stark")
    assert res2.status_code == 200
    assert len(res2.json()) == 1
    assert res2.json()[0]["name"] == "Tony Stark"

    # Search by company
    res3 = client.get("/api/leads?search=bugle")
    assert res3.status_code == 200
    assert len(res3.json()) == 1
    assert res3.json()[0]["name"] == "Peter Parker"

    # Search clear / empty
    res4 = client.get("/api/leads?search=")
    assert res4.status_code == 200
    assert len(res4.json()) >= 2


def test_get_lead_details(client):
    lead = client.post("/api/leads", json={"name": "Diana Prince", "company": "Themyscira"}).json()
    lead_id = lead["id"]

    res = client.get(f"/api/leads/{lead_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Diana Prince"
    assert len(data["discussions"]) >= 1


def test_get_nonexistent_lead(client):
    res = client.get("/api/leads/99999")
    assert res.status_code == 404


def test_add_discussion_and_today_followup(client):
    lead = client.post("/api/leads", json={"name": "Sarah Connor", "company": "Cyberdyne"}).json()
    lead_id = lead["id"]

    today_str = datetime.now().date().isoformat()
    follow_up_time = f"{today_str}T14:00:00"

    disc_payload = {
        "note": "Sent proposal document. Follow up scheduled.",
        "follow_up_at": follow_up_time,
    }
    disc_res = client.post(f"/api/leads/{lead_id}/discussions", json=disc_payload)
    assert disc_res.status_code == 201
    disc_data = disc_res.json()
    assert disc_data["note"] == disc_payload["note"]
    assert disc_data["follow_up_at"] is not None

    # Check today's followups endpoint
    followup_res = client.get("/api/leads/today-followups")
    assert followup_res.status_code == 200
    followup_data = followup_res.json()
    assert len(followup_data) == 1
    assert followup_data[0]["name"] == "Sarah Connor"
    assert followup_data[0]["is_today_follow_up"] is True


def test_future_followup_not_in_today(client):
    lead = client.post("/api/leads", json={"name": "Future Lead"}).json()
    tomorrow_str = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT14:00:00")

    client.post(f"/api/leads/{lead['id']}/discussions", json={
        "note": "Call scheduled for next week",
        "follow_up_at": tomorrow_str,
    })

    followups = client.get("/api/leads/today-followups").json()
    lead_ids = [l["id"] for l in followups]
    assert lead["id"] not in lead_ids


def test_won_or_lost_leads_excluded_from_actionable_followups(client):
    lead = client.post("/api/leads", json={"name": "Closed Lead"}).json()
    today_str = datetime.now().strftime("%Y-%m-%dT14:00:00")

    client.post(f"/api/leads/{lead['id']}/discussions", json={
        "note": "Signed deal follow-up",
        "follow_up_at": today_str,
    })

    # Initially in today's followups
    res1 = client.get("/api/leads/today-followups").json()
    assert any(l["id"] == lead["id"] for l in res1)

    # Now mark as Won
    client.patch(f"/api/leads/{lead['id']}/status", json={"status": "Won"})

    # Should no longer be presented as an actionable follow-up
    res2 = client.get("/api/leads/today-followups").json()
    assert not any(l["id"] == lead["id"] for l in res2)


def test_overdue_followup_detection(client):
    lead = client.post("/api/leads", json={"name": "Overdue Lead"}).json()
    past_time = (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S")

    client.post(f"/api/leads/{lead['id']}/discussions", json={
        "note": "Call was missed",
        "follow_up_at": past_time,
    })

    lead_detail = client.get(f"/api/leads/{lead['id']}").json()
    assert lead_detail["is_overdue"] is True
    assert lead_detail["discussions"][0]["is_overdue"] is True


def test_update_status_transitions(client):
    lead = client.post("/api/leads", json={"name": "Hank Scorpio", "company": "Globex"}).json()
    lead_id = lead["id"]

    # Transition New -> Contacted
    res1 = client.patch(f"/api/leads/{lead_id}/status", json={"status": "Contacted"})
    assert res1.status_code == 200
    assert res1.json()["status"] == "Contacted"

    # Transition Contacted -> Qualified
    res2 = client.patch(f"/api/leads/{lead_id}/status", json={"status": "Qualified"})
    assert res2.status_code == 200
    assert res2.json()["status"] == "Qualified"
