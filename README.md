# LeadFlow — Smart Lead Management CRM

LeadFlow is a modern, lightweight single-screen CRM built for the **PravarAI AI-smart Fullstack Intern coding assessment**. It enables sales teams to manage inbound and outbound leads, track follow-ups, maintain chronological discussion notes, and filter leads seamlessly.

---

## Features

- **Single-Screen Dashboard**: Clean, responsive, high-velocity lead tracking interface matching assessment specs.
- **Pinned Today's Follow-ups**: Prioritized top section highlighting critical customer interactions scheduled for today.
- **Multi-Status Filtering & Search**: Instant filtering by lead status (`New`, `Contacted`, `Qualified`, `Proposal Sent`, `Won`, `Lost`) and full-text keyword search across names, companies, and phone numbers.
- **Lead Timeline Dialog**: Interactive chronological audit trail of all previous discussions and upcoming follow-ups.
- **Quick Status Updates**: Real-time status transitions directly from the timeline view.
- **Discussion Logging**: Fast note creation with optional follow-up date and time scheduling.
- **Seed Script**: Realistic sample data mirroring the reference UI out of the box.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | [Next.js](https://nextjs.org/) (App Router, React 19, TypeScript), [Tailwind CSS v4](https://tailwindcss.com/), [Lucide React](https://lucide.dev/) |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+), [Pydantic v2](https://docs.pydantic.dev/) |
| **Database** | [SQLite](https://www.sqlite.org/) via [SQLAlchemy 2.0 ORM](https://www.sqlalchemy.org/) |
| **Testing** | [Pytest](https://docs.pytest.org/), [HTTPX](https://www.python-httpx.org/) |
| **Containerization** | [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/) |

---

## Project Structure

```text
leadflow/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI route controllers (/leads, /health)
│   │   ├── core/            # Configuration and database engine setup
│   │   ├── models/          # SQLAlchemy ORM models (Lead, Discussion)
│   │   ├── schemas/         # Pydantic v2 request/response schemas
│   │   ├── services/        # Business logic and query layer
│   │   ├── main.py          # Application entrypoint & CORS config
│   │   └── seed.py          # Database sample data seeder
│   ├── tests/               # Automated Pytest suite
│   ├── requirements.txt     # Python backend dependencies
│   └── Dockerfile           # Backend container definition
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js App Router (page.tsx, layout.tsx)
│   │   ├── components/      # Reusable modular UI components
│   │   │   ├── header/      # DashboardHeader
│   │   │   ├── filters/     # StatusFilter, SearchInput
│   │   │   ├── leads/       # LeadCard, LeadList, TodayFollowUps
│   │   │   └── dialogs/     # AddLeadDialog, LeadTimelineDialog
│   │   ├── lib/             # Typed API client
│   │   └── types/           # Shared TypeScript interfaces
│   ├── package.json         # Frontend dependencies and scripts
│   └── Dockerfile           # Frontend production multi-stage build
├── docs/
│   └── reference/           # Reference UI screenshots
├── docker-compose.yml       # Multi-container orchestration
├── .env.example             # Environment variable template
├── .gitignore               # Secrets and build ignore rules
└── README.md                # Project documentation
```

---

## Getting Started

### Prerequisites

- **Node.js**: v18.0.0 or higher (v22.x recommended)
- **Python**: v3.10 or higher
- **npm**: v9.x or higher
- **Docker & Docker Compose**: (Optional, for containerized run)

---

### Option 1: Local Development (Recommended)

The frontend and backend run independently with hot reload.

#### 1. Backend Setup

```bash
# From workspace root
python -m venv backend/venv

# Activate virtual environment
# Windows (PowerShell):
.\backend\venv\Scripts\Activate.ps1
# macOS/Linux:
source backend/venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# (Optional) Seed sample data matching the reference design
python -m backend.app.seed

# Start the FastAPI development server
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be live at `http://localhost:8000`.  
Interactive Swagger API documentation: `http://localhost:8000/api/docs`.

#### 2. Frontend Setup

In a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start the Next.js development server
npm run dev
```

The frontend application will be live at `http://localhost:3000`.

---

### Option 2: Docker Compose

To build and run the entire application stack in containers:

```bash
# Build and launch both services
docker compose up --build
```

- Frontend: `http://localhost:3000`
- Backend API & Docs: `http://localhost:8000/api/docs`
- Database data is persisted in the Docker volume `leadflow-data`.

---

## Data Model & Schema

### `Lead`

| Column | Type | Constraints / Description |
|---|---|---|
| `id` | Integer | Primary key, autoincrement, indexed |
| `name` | String(255) | Required, indexed |
| `company` | String(255) | Optional |
| `phone` | String(50) | Optional |
| `status` | Enum | Values: `New`, `Contacted`, `Qualified`, `Proposal Sent`, `Won`, `Lost`. Default: `New`. Indexed. |
| `created_at` | DateTime(UTC) | Creation timestamp |
| `updated_at` | DateTime(UTC) | Auto-updated on status change or note addition |

### `Discussion`

| Column | Type | Constraints / Description |
|---|---|---|
| `id` | Integer | Primary key, autoincrement, indexed |
| `lead_id` | Integer | Foreign key referencing `leads.id` (`ondelete="CASCADE"`), indexed |
| `note` | Text | Required discussion content |
| `created_at` | DateTime(UTC) | Timestamp note was logged, indexed |
| `follow_up_at` | DateTime(UTC) | Optional scheduled follow-up datetime, indexed |

---

## API Contract

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service health status check |
| `GET` | `/api/leads` | List leads with optional `?status=` and `?search=` query parameters |
| `GET` | `/api/leads/today-followups` | Retrieve leads with follow-ups scheduled for today |
| `GET` | `/api/leads/{id}` | Retrieve individual lead with complete chronological discussion history |
| `POST` | `/api/leads` | Create a new lead (defaults status to `New`) |
| `PATCH` | `/api/leads/{id}/status` | Update lead status (`New`, `Contacted`, `Qualified`, `Proposal Sent`, `Won`, `Lost`) |
| `POST` | `/api/leads/{id}/discussions` | Add discussion note and optional `follow_up_at` date/time |

---

## Running Automated Tests

Backend unit and integration tests run against an isolated in-memory SQLite database via Pytest:

```bash
# From workspace root with backend virtual environment active
pytest backend/tests -v
```

All 10 test suites verify:
- Health check endpoint
- Lead creation defaulting to `New` status
- Custom initial notes and auto-creation notes
- Pydantic validation (e.g. missing required fields)
- Status-based filtering
- Full-text search across name, company, and phone
- Timeline and discussion chronological retrieval
- 404 handling for invalid IDs
- Scheduling follow-ups and today's pinned follow-ups detection
- Status updates
