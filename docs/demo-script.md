# LeadFlow — Video Demonstration Script (Max 3 Minutes)

This script provides a concise, professional presenter walkthrough for recording the 3-minute assessment demo video. It aligns directly with the actual LeadFlow user interface and live workflows.

---

## Preparation Before Recording

1. Ensure the backend and frontend servers are running:
   * Backend: `http://localhost:8000`
   * Frontend: `http://localhost:3000`
2. Open your browser in full screen (or 1080p window) at `http://localhost:3000`.
3. Open Developer Tools Console tab (optional, to showcase zero console errors during interaction).
4. Recommended recording tool: OBS Studio or Windows Game Bar (`Win + Alt + R`).

---

## Walkthrough Sequence & Timing Guide

### Scene 1: Introduction & Dashboard Overview (0:00 – 0:30)
* **What to Show**: The main LeadFlow dashboard.
* **Spoken Narrative**:
  > *"Hi everyone, this is LeadFlow, a lightweight, single-screen CRM built for the PravarAI Fullstack assessment. It is engineered with a Next.js 16 App Router frontend, Tailwind CSS, a Python FastAPI backend, and SQLite via SQLAlchemy 2.0 ORM.*
  >
  > *Here on the main screen, we have a clean, high-velocity view of all leads with their current status, latest discussion note, and relative timestamps."*
* **Action**:
  * Point cursor to the LeadFlow branding and the top status filter pills: `All`, `New`, `Contacted`, `Qualified`, `Proposal Sent`, `Won`, and `Lost`.
  * Click `New`, `Contacted`, and `Proposal Sent` to demonstrate instant pipeline filtering. Click `All` to restore the complete list.

---

### Scene 2: Today's Follow-ups & Overdue Highlighting (0:30 – 1:00)
* **What to Show**: Pinned "TODAY'S FOLLOW-UPS" section at the top.
* **Spoken Narrative**:
  > *"At the top of the dashboard, time-critical interactions are pinned under 'Today's Follow-ups'. Notice Sarah Connor's card: her follow-up was scheduled for earlier today at 2:00 PM, so LeadFlow automatically flags it in red as overdue with an alert indicator.*
  >
  > *Upcoming follow-ups scheduled for later today appear in clear blue. Notice also that pinned leads are automatically de-duplicated from the main list below to keep the interface uncluttered, while completed or lost leads are excluded from actionable alerts."*

---

### Scene 3: Search & Timeline Dialog (1:00 – 1:30)
* **What to Show**: Full-text search bar and in-place timeline modal.
* **Spoken Narrative**:
  > *"Next, let's search for a lead. In the search bar, typing 'Hank' instantly filters the list to Hank Scorpio. Clearing the input brings back all leads immediately.*
  >
  > *Clicking on any lead card opens the in-place Lead Timeline dialog without any disruptive page navigation or URL reload."*
* **Action**:
  * Type `Hank` in search.
  * Clear search.
  * Click on `Hank Scorpio` (or `Sarah Connor`) to open the timeline dialog.

---

### Scene 4: Logging Discussions & Scheduling Follow-ups (1:30 – 2:05)
* **What to Show**: Discussion history and note logger.
* **Spoken Narrative**:
  > *"Inside the timeline dialog, discussions are strictly ordered newest-first, showing exactly when each interaction occurred.*
  >
  > *Let's log a new note: 'Initial discovery call completed; client requested custom enterprise quote.'*
  > *We can check 'Set Follow-up', select today's date, and set the time. Clicking 'Save Note' instantly appends the discussion to the top of the timeline and updates the lead card in the background."*
* **Action**:
  * Type note in textarea.
  * Check `Set Follow-up`, pick date and time.
  * Click `Save Note`. Show note appearing at top of timeline.

---

### Scene 5: Live Status Transition (2:05 – 2:25)
* **What to Show**: Status dropdown switcher in timeline header.
* **Spoken Narrative**:
  > *"In the dialog header, sales reps can transition the lead's stage seamlessly. Let's move Hank from 'New' to 'Contacted', and then 'Qualified'.*
  >
  > *The backend persists the update immediately in SQLite, and when we close the modal, the card's badge reflects 'QUALIFIED' in real time."*
* **Action**:
  * Click status dropdown, select `Contacted`, then `Qualified`.
  * Click `X` to close dialog and point to updated card badge on dashboard.

---

### Scene 6: Adding a New Lead (2:25 – 2:45)
* **What to Show**: Add New Lead modal.
* **Spoken Narrative**:
  > *"Now let's add a new lead using the '+ Add New Lead' button. If we try submitting blank input or spaces, LeadFlow rejects it with a clear validation error.*
  >
  > *Let's enter: 'Elena Fisher', Company 'Uncharted Tech', and Phone '555-0182'. Clicking 'Save Lead' immediately registers the lead with default 'NEW' status, logs an initial creation event, and updates the list."*
* **Action**:
  * Click `+ Add New Lead`.
  * Enter name, company, phone.
  * Click `Save Lead`. Point out new card in `ALL LEADS`.

---

### Scene 7: Architecture & Conclusion (2:45 – 3:00)
* **What to Show**: Brief display of Swagger docs (`/api/docs`) or terminal test output.
* **Spoken Narrative**:
  > *"Under the hood, the backend is covered by 15 automated Pytest tests, the Next.js frontend has zero ESLint or build errors, and the entire stack is dockerized with persistent storage.*
  >
  > *Thank you for watching the LeadFlow demonstration!"*

---

## Recording Checklist

- [ ] Clean browser window at `http://localhost:3000`.
- [ ] No extraneous tabs or notifications.
- [ ] Clear microphone audio.
- [ ] Total length between 2:30 and 3:00 minutes.
