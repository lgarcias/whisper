# Database Guide

This document describes the database setup, configuration, and best practices for the project.

---

## Service

- **Database:** PostgreSQL (containerized via Docker Compose)
- **Default port:** 5432
- **Data persistence:** Docker volume `whisper-pgdata`

---

## Environment Variables

The following variables control the database connection and SQLAlchemy engine:

```
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=whisperdb
DATABASE_URL=postgresql+psycopg2://user:password@postgres:5432/whisperdb

DB_POOL_SIZE=5
DB_MAX_OVERFLOW=5
DB_POOL_RECYCLE=1800
DB_POOL_TIMEOUT=30
DB_ECHO=false
DB_LOG_LEVEL=INFO
```

- `DATABASE_URL` is required by the backend for SQLAlchemy.
- The other variables are used by the Postgres container or to tune SQLAlchemy's connection pool.

---

## Usage in Backend

- The backend reads `DATABASE_URL` and pool settings from the environment (see `backend/app/db.py`).
- Use the FastAPI dependency `getDb()` to access a session in your routes.

---

## Development

- The default `.env` is suitable for local development.
- For production, use strong credentials and do not commit your `.env` file.

---

## Initialization & Migrations

- You can use tools like [Alembic](https://alembic.sqlalchemy.org/) for schema migrations.
- To manually connect to the database (from the DevContainer):
  - Install `psql` or use a Python client.

---

## Backups

- The database data is stored in the Docker volume `whisper-pgdata`.
- To back up or restore, use `docker volume` commands or `pg_dump`/`pg_restore`.

---

## Security

- Never expose your database to the public internet.
- Use strong, unique passwords in production.
- Restrict access to trusted services/networks only.

---

## See also

- [docs/services.md](services.md) for service orchestration
- [backend/app/db.py](../backend/app/db.py) for SQLAlchemy setup
