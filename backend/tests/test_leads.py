from datetime import datetime, time
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
    # Should automatically have initial discussion entry
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


def test_validation_missing_name(client):
    payload = {
        "company": "No Name Corp",
    }
    response = client.post("/api/leads", json=payload)
    assert response.status_code == 422


def test_list_and_filter_leads(client):
    # Create two leads with different status
    lead1 = client.post("/api/leads", json={"name": "Alice Smith", "company": "Alpha Inc"}).json()
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

    # Search by name
    res = client.get("/api/leads?search=stark")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["name"] == "Tony Stark"

    # Search by company
    res2 = client.get("/api/leads?search=bugle")
    assert res2.status_code == 200
    data2 = res2.json()
    assert len(data2) == 1
    assert data2[0]["name"] == "Peter Parker"


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


def test_update_status(client):
    lead = client.post("/api/leads", json={"name": "Hank Scorpio", "company": "Globex"}).json()
    lead_id = lead["id"]

    update_res = client.patch(f"/api/leads/{lead_id}/status", json={"status": "Won"})
    assert update_res.status_code == 200
    data = update_res.json()
    assert data["status"] == "Won"
