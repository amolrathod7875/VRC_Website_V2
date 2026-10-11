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

> Phase 10R.3 removed the PostgreSQL-backed website content APIs. Products,
> applications, blogs, FAQs, clients, partners, industries and media metadata
> are now served exclusively from static frontend data modules
> (`frontend/src/lib/data.ts`, `faqs.ts`, `clients.ts`, `partnersData.ts`,
> `careerData.ts`, `contactData.ts`). Physical media (catalogues, images,
> videos, PDFs, certificates) is still served from the `/media/` static mount.

Active endpoints:

- `GET /health` - Health check
- `POST /api/v1/chat` - RAG chatbot (Qdrant-backed, PostgreSQL-free)
- `GET /api/v1/chat/status` - Chatbot readiness status

Removed endpoints (no longer registered; routes return 404):

- `GET /api/v1/products` (+ `/{slug}`)
- `GET /api/v1/applications` (+ `/{slug}`)
- `GET /api/v1/blogs` (+ `/{slug}`)
- `GET /api/v1/faqs` (+ `/category/{category}`)
- `GET /api/v1/clients`
- `GET /api/v1/partners` (+ `/{slug}`)
- `GET /api/v1/industries` (+ `/{slug}`)
- `GET /api/v1/media/{asset_id}` - database-backed metadata only
- `GET /api/v1/jobs` (+ `/{slug}`) - legacy listing; careers page uses static data
- `POST /api/v1/jobs/{id}/apply` - legacy application storage
- `POST /api/v1/contact` - legacy contact submission storage

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
