# VR Coatings Website

Full-stack architecture with Next.js frontend, FastAPI backend, and PostgreSQL database.

## Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL 17 (or Docker)
- Docker & Docker Compose (optional)

## Architecture

```
Browser
  │
  ▼
Next.js Frontend (frontend/)
  │ HTTPS / REST API
  ▼
FastAPI Backend (backend/)
  │
  ├─────────────┴──────────────┐
  ▼                            ▼
PostgreSQL                 Media Storage
structured data         images/videos/PDFs/files
  │                            │
  └──────── metadata / URLs ───┘
```

## Environment Variables

Copy `.env.example` to `.env` and update values.

```bash
cp .env.example .env
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Database Setup

```bash
docker compose up postgres -d
cd backend
alembic upgrade head
```

## Full Stack (Docker)

```bash
docker compose up --build
```

## API Endpoints

- `GET /api/v1/health` - Health check
- `GET /api/v1/products` - List products
- `GET /api/v1/products/{slug}` - Get product by slug
- `GET /api/v1/applications` - List applications
- `GET /api/v1/applications/{slug}` - Get application by slug
- `GET /api/v1/blogs` - List published blogs
- `GET /api/v1/blogs/{slug}` - Get blog by slug
- `GET /api/v1/faqs` - List FAQs
- `GET /api/v1/jobs` - List jobs
- `GET /api/v1/jobs/{slug}` - Get job by slug
- `POST /api/v1/jobs/{id}/apply` - Apply for a job
- `POST /api/v1/contact` - Submit contact form
- `GET /api/v1/clients` - List clients
- `GET /api/v1/partners` - List partners
- `GET /api/v1/partners/{slug}` - Get partner by slug
- `GET /api/v1/industries` - List industries
- `GET /api/v1/industries/{slug}` - Get industry by slug
- `GET /api/v1/media/{id}` - Get media asset metadata

## Migrations

```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Notes

- All public URLs remain unchanged during migration.
- Product catalogue PDFs are preserved under `backend/storage/catalogues/` after migration phase.
- Frontend routes remain Next.js pages; backend serves data APIs only.
