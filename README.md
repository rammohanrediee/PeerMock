# PeerMock

**A secure mock-interview scheduling API built through guided learning.**

Students book practice interviews with peer mentors. Mentors publish availability and
record private feedback. Coordinators organize interview events. The backend must keep
bookings consistent, protect private records and enforce every permission on the
server.

## Current status

**Season 0 complete; Season 1 active.** Fresh-environment installation and quality checks
pass. The initial PostgreSQL migration and constraints are verified, and the application
async session dependency connects and cleans up successfully. Business behavior and
authorization remain incomplete.

Start with [GUIDED_BUILD.md](GUIDED_BUILD.md) and complete one checkpoint at a time:

1. Learn the minimum theory.
2. Explain it in your own words.
3. Predict one allowed and one failure result.
4. Implement the task yourself.
5. Ask Codex to review your exact implementation and tests.
6. Repair mistakes and record evidence before moving on.

## Local setup and quality checks

From the repository root, create an isolated Python 3.12+ environment and install the
project with its development tools:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/pytest
.venv/bin/ruff check src tests
.venv/bin/mypy
```

Mypy checks local source and tests directly. The import test does not need a database
or `.env`. Application/session imports require `PEERMOCK_DATABASE_URL` supplied through
the environment or the repository-root `.env` file. The opt-in database tests guard
against non-local hosts before connecting.

## Project documents

PostgreSQL constraint checks are opt-in after applying migrations to local `peermock`:

```bash
PEERMOCK_RUN_DB_TESTS=1 pytest tests/integration/test_postgres_constraints.py
```

These tests insert temporary records and roll them back; they do not migrate the schema.
Without the flag, ordinary pytest skips the database checks.

- [`PRODUCT.md`](PRODUCT.md) — users, product behavior, promises and deferred scope
- [`PROJECT_BLUEPRINT.md`](PROJECT_BLUEPRINT.md) — capabilities and exit gates
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — current/target technical boundaries
- [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) — directory and module ownership
- [`PRODUCTION.md`](PRODUCTION.md) — deployment, operations and release gates
- [`.codex/plans/project-tracker.md`](.codex/plans/project-tracker.md) — execution order
  and status
- [`GUIDED_BUILD.md`](GUIDED_BUILD.md) — learning missions for each checkpoint

## Product story

- Mentors publish interview slots for topics such as Python, backend, SQL and ML.
- Students reserve and cancel slots.
- Exactly one student may hold a particular slot.
- Mentors see only their own schedule and assigned students.
- Students see only their own bookings and feedback.
- Coordinators manage events and schedules without bypassing privacy boundaries.
- After the secure scheduling system is complete, an optional LLM feature can create
  draft question packs from validated user requirements.

## Intended stack

- Python 3.12
- FastAPI and Pydantic v2
- PostgreSQL 16
- SQLAlchemy 2 and Alembic
- `pwdlib` with Argon2 and PyJWT
- pytest and HTTPX/FastAPI TestClient
- Docker Compose
- Ruff and mypy
- GitHub Actions

Redis, Celery, a frontend and LLM integration are intentionally excluded from the core
Project 2 checkpoints. Background work belongs to Project 3. LLM generation is a later,
separately gated feature.

## Project structure

```text
peermock/
├── src/peermock/
│   ├── api/                    # HTTP routes and dependency wiring
│   ├── core/                   # Configuration and shared application concerns
│   ├── db/                     # Database session and persistence wiring
│   └── features/
│       ├── users/              # Accounts, authentication and roles
│       ├── availability/       # Mentor availability and interview slots
│       ├── bookings/           # Booking, cancellation and concurrency rules
│       ├── feedback/           # Private post-interview feedback
│       └── question_packs/     # Reserved for the later LLM milestone
├── migrations/                 # Alembic migrations
├── tests/
│   ├── unit/                   # Domain and service tests
│   ├── integration/            # API and PostgreSQL behavior
│   └── security/               # Authentication and authorization boundaries
├── docs/
│   ├── decisions/              # Architecture decision records
│   ├── evidence/               # Sanitized proof and diagrams
│   ├── AI_FEATURE_BOUNDARY.md
│   ├── LAB_JOURNAL.md
│   └── PERMISSION_MATRIX.md
├── ARCHITECTURE.md
├── PRODUCT.md
├── PRODUCTION.md
├── PROJECT_BLUEPRINT.md
├── PROJECT_STRUCTURE.md
└── GUIDED_BUILD.md
```

Directories describe ownership, not mandatory complexity. Add files only when a
completed checkpoint needs them.

## Core definition of done

- Two simultaneous requests cannot book the same interview slot.
- Changing an identifier cannot reveal or modify another user's booking or feedback.
- Students cannot perform mentor or coordinator actions.
- Mentors cannot alter another mentor's slots or interviews.
- Cancellation leaves slot and booking state consistent.
- Migrations and meaningful tests run from a fresh checkout.
- The architecture, permission rules and important failures are documented.

The LLM feature is not required to call the core backend complete.
