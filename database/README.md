# VR Coatings Database

This folder contains database-related files for the VR Coatings application.

## Structure

- `migrations/` - Database migration files (managed by Alembic)
- `seeds/` - Seed data scripts
- `init/` - Database initialization scripts
- `README.md` - This file

## Notes

- PostgreSQL data is stored in a Docker volume managed by Docker Compose.
- Do not store physical database files in this directory.
- Use Alembic for schema migrations: `cd backend && alembic upgrade head`
