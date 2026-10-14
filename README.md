# LeadFlow — Smart Lead Management CRM

LeadFlow is a high-velocity, single-screen CRM built for the **PravarAI AI-smart Fullstack Intern Coding Assessment**. It provides sales representatives and founders with an intuitive interface to manage inbound/outbound leads, log chronological discussion history, track follow-ups, and organize deals across status pipelines.

---

## Key Features

- **Single-Screen Lead Dashboard**: High-clarity lead view strictly adhering to the assessment reference UI designs.
- **Pinned Today's Follow-ups**: Pinned top container prioritizing actionable follow-ups scheduled for the current date.
- **Overdue Follow-up Highlighting**: Time-sensitive interactions scheduled in the past are visibly highlighted in **red** with alert indicators.
- **Smart Lead De-duplication**: Leads pinned in the follow-ups section are de-duplicated from the main lead list below to prevent clutter.
- **Pipeline Status Filtering**: Instant filtering by lead status (`All`, `New`, `Contacted`, `Qualified`, `Proposal Sent`, `Won`, `Lost`) with pill toggles.
- **Full-Text Lead Search**: Debounced search across lead names, companies, and phone numbers.
- **In-Place Timeline Dialog**: Interactive modal displaying complete discussion history sorted chronologically (newest first) without page navigation.
- **Discussion & Follow-up Scheduling**: Seamless note logging with optional follow-up date and time scheduling.
- **Quick Status Transitions**: Change lead status directly within the timeline dialog with real-time UI badge reflection.
- **Zero-Setup Seeding**: Automatically populates realistic sample leads matching the assessment mockups on first startup.

---

## Tech Stack

| Component | Technology | Version |
|---|---|---|
| **Frontend Framework** | [Next.js](https://nextjs.org/) (App Router, Turbopack) | `16.4.0` |
| **Frontend Core** | [React](https://react.dev/) & [TypeScript](https://www.typescriptlang.org/) | React `19.3.0`, TS `5.x` |
| **Styling** | [Tailwind CSS](https://tailwindcss.com/) & [Lucide Icons](https://lucide.dev/) | Tailwind `v4` |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) (Python) | `0.115.6` |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev/) | `2.10.4` |
| **ORM & Database** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) & [SQLite](https://www.sqlite.org/) | Persistent local storage |
| **Testing** | [Pytest](https://docs.pytest.org/) & [HTTPX](https://www.python-httpx.org/) | In-memory test DB |
| **Containerization** | [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) | Multi-container setup |

---

## Project Structure

```text
leadflow/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI route controllers (/leads, /health)
│   │   ├── core/            # Database engine, session maker, and config
│   │   ├── models/          # SQLAlchemy ORM models (Lead, Discussion)
│   │   ├── schemas/         # Pydantic v2 validation and serialization schemas
│   │   ├── services/        # Query building, metadata derivation, and business logic
│   │   ├── main.py          # FastAPI application, CORS middleware, and lifespan
│   │   └── seed.py          # Initial sample data seeder
│   ├── tests/
│   │   ├── conftest.py      # Pytest fixtures and isolated in-memory DB
│   │   └── test_leads.py    # 15 automated unit and integration tests
│   ├── requirements.txt     # Python backend dependencies
│   └── Dockerfile           # Backend container definition
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js App Router (page.tsx, layout.tsx, globals.css)
│   │   ├── components/      # Modular, reusable React components
│   │   │   ├── header/      # DashboardHeader
│   │   │   ├── filters/     # StatusFilter, SearchInput
│   │   │   ├── leads/       # LeadCard, LeadList, TodayFollowUps
│   │   │   └── dialogs/     # AddLeadDialog, LeadTimelineDialog
│   │   ├── lib/             # Strongly-typed API client (api.ts)
│   │   └── types/           # Shared TypeScript interfaces
│   ├── package.json         # Frontend dependencies and npm scripts
│   └── Dockerfile           # Multi-stage production container build
├── docs/
│   ├── reference/           # Original PravarAI assessment design mockups
│   ├── screenshots/         # Verified browser verification screenshots
│   └── submission-checklist.md # Assessment deliverables checklist
├── docker-compose.yml       # Docker Compose multi-service orchestration
├── .env.example             # Environment variable template
├── .gitignore               # Repository ignore rules
└── README.md                # Project documentation
```

---

## Prerequisites

- **Node.js**: `v18.0.0` or higher (`v22.x` recommended)
- **Python**: `v3.10.0` or higher
- **npm**: `v9.x` or higher
- **Docker Desktop**: (Optional, for containerized run)

---

## Setup & Running Locally

The frontend and backend run independently with hot reload enabled.

### 1. Environment Configuration

Copy `.env.example` to create your local `.env` if desired (defaults work out-of-the-box):

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

Default configuration:
```ini
DATABASE_URL=sqlite:///./leadflow.db
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

---

### 2. Backend Setup

#### Windows (PowerShell):
```powershell
# 1. Create Python virtual environment
python -m venv backend\venv

# 2. Activate virtual environment
.\backend\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r backend\requirements.txt

# 4. Start the development server
$env:PYTHONPATH="."
.\backend\venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

#### macOS / Linux:
```bash
# 1. Create Python virtual environment
python3 -m venv backend/venv

# 2. Activate virtual environment
source backend/venv/bin/activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Start the development server
export PYTHONPATH="."
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

- Backend API: `http://localhost:8000`
- Interactive Swagger API Documentation: `http://localhost:8000/api/docs`
- Health check: `http://localhost:8000/health`

*Note: Database tables and sample seed leads are automatically initialized on startup if the database is empty.*

---

### 3. Frontend Setup

Open a separate terminal window:

```bash
cd frontend

# Install dependencies
npm install

# Start the Next.js development server
npm run dev
```

- Frontend Application: `http://localhost:3000`

---

## Running with Docker Compose

To run both services in isolated Docker containers with persistent SQLite storage:

```bash
# Validate compose configuration
docker compose config

# Build and start both containers in the background
docker compose up --build -d
```

- Frontend: `http://localhost:3000`
- Backend API & Swagger: `http://localhost:8000/api/docs`
- Database data is persisted across container restarts in the `leadflow-data` volume.

To stop the containers:
```bash
docker compose down
```

---

## Running Automated Tests

The backend test suite runs 15 unit and integration tests against an isolated, in-memory SQLite database:

```bash
# Windows (PowerShell)
$env:PYTHONPATH="."
.\backend\venv\Scripts\pytest.exe backend\tests -v

# macOS / Linux
export PYTHONPATH="."
pytest backend/tests -v
```

### Frontend Checks

```bash
cd frontend

# Run ESLint checks
npm run lint

# Build production bundle and verify TypeScript types
npm run build
```

---

## Data Model & Schema Details

### Entity: `Lead`
* `id` (Integer, Primary Key): Unique lead identifier.
* `name` (String, Required): Full name. Strips whitespace and rejects blank names.
* `company` (String, Optional): Company / organization name.
* `phone` (String, Optional): Contact telephone number.
* `status` (Enum, Required): One of `New`, `Contacted`, `Qualified`, `Proposal Sent`, `Won`, `Lost`. Defaults to `New`.
* `created_at` (DateTime): Lead creation timestamp.
* `updated_at` (DateTime): Automatically updated whenever status changes or discussion notes are added.

### Entity: `Discussion`
* `id` (Integer, Primary Key): Unique discussion identifier.
* `lead_id` (Integer, ForeignKey): Cascading foreign key referencing `leads.id`.
* `note` (Text, Required): Discussion note content. Blank notes are rejected.
* `created_at` (DateTime): Timestamp note was logged.
* `follow_up_at` (DateTime, Optional): Scheduled follow-up datetime.

---

## REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service health status check |
| `GET` | `/api/docs` | Interactive Swagger OpenAPI documentation |
| `GET` | `/api/leads` | List leads (supports `?status=` and `?search=` query parameters) |
| `GET` | `/api/leads/today-followups` | Retrieve active leads with follow-ups scheduled for today |
| `GET` | `/api/leads/{id}` | Retrieve lead details with chronological discussion history |
| `POST` | `/api/leads` | Create a new lead (defaults status to `New`) |
| `PATCH` | `/api/leads/{id}/status` | Update lead status |
| `POST` | `/api/leads/{id}/discussions` | Add a discussion note and optional `follow_up_at` date/time |

---

## Troubleshooting

### 1. PowerShell Script Execution Policy
If `.\backend\venv\Scripts\Activate.ps1` gives an execution policy error on Windows:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
Or directly invoke Python via `.\backend\venv\Scripts\python.exe`.

### 2. Port Already in Use
If port `8000` or `3000` is already in use by another service:
```powershell
# Find process on port 8000
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object OwningProcess
# Terminate process if needed
Stop-Process -Id <PID> -Force
```

### 3. Docker Daemon Not Running
If `docker compose up` outputs `failed to connect to the docker API at npipe`:
Ensure Docker Desktop is launched and the Docker engine is running from your Windows system tray / Start Menu.
