# PeerMock Working Memory

## Current checkpoint

- **Git:** initialized on `main`; no commits exist yet.
- **Active episode:** S2E2 — mentor availability/slot create, read and list behavior.
- **Verified:** planning scaffold exists and Git is initialized. `pyproject.toml` now
  declares bounded core backend/authentication dependencies, a `dev` extra, Hatchling
  src-layout packaging, pytest/coverage, Ruff and strict mypy configuration. TOML syntax
  was checked. A project `.venv` now uses Python 3.12.14 and contains the editable
  PeerMock package plus pytest 9.1.1, Ruff 0.16.7 and mypy 2.3.1. At the user's explicit
  request, `src/peermock/core/config.py` now defines
  typed, `PEERMOCK_`-prefixed settings and `src/peermock/main.py` defines the FastAPI app
  factory/ASGI app. Both pass `py_compile`; the earlier missing-dependency blocker is
  resolved. At the user's implementation request, added `__version__ = "0.1.0"`
  and one typed package import/version test. `.venv/bin/pytest tests/unit/test_package.py`
  passed (1 test); Ruff passed for both changed Python files. S0E1 is complete.
- **S0E2 evidence:** Fresh Python 3.12 environment at
  `/private/tmp/peermock-verify.J2qhLR/venv` installed `.[dev]` successfully. Its pytest
  passed (1 test), Ruff passed, mypy passed (10 files), and pip check found no broken
  requirements. Mypy now checks local `src` and `tests`; initialized api/core/db packages
  so discovery includes their modules. README documents reproduction commands.
- **Latest implementation:** At the user's explicit request, created User, InterviewSlot,
  Booking and Feedback SQLAlchemy models ahead of the open Season 1 gates. Shared UUID
  and creation-time mixin; model registration through `peermock.db.models`. See
  `docs/decisions/initial-models.md` for schema choices and service-boundary limitations.
  Four tests pass, Ruff passes, strict mypy passes (22 files); PostgreSQL DDL compilation
  and mapper configuration pass. SQLite checks are not PostgreSQL migration evidence.
- **Exact restart:** S1E4 and the Season 1 finale are complete. S2E1 is also complete.
  Live verification on 2026-09-19 passed all 13 tests, Ruff, strict mypy and
  `alembic check`; the database is at revision `7d04311b0d5e` (head). Continue S2E2 by composing
  the availability router into `src/peermock/api/router.py`, then verify the application
  OpenAPI paths before adding behavior tests. The learner's availability router, service
  and schema files still need `ruff format`.
- **Historical Alembic checkpoint (completed):** User then authorized migration setup. Created the configured
  local `peermock` database because it did not exist, but left it schema-empty. Added
  `alembic.ini`, async `migrations/env.py`, the revision template, and generated initial
  revision `7d04311b0d5e_create_core_tables.py`. Offline PostgreSQL SQL generation passed;
  repository pytest (4), Ruff, and strict mypy (22 files) passed. The later lifecycle and
  constraint evidence below supersedes the then-pending application step.
- **Migration lifecycle:** Upgrade, downgrade-to-base and re-upgrade are complete. Codex
  independently verified database head `7d04311b0d5e`, zero autogenerate drift and the
  PostgreSQL constraint cases recorded below. The learner works in an activated `.venv`;
  show bare commands without `.venv/bin/` prefixes.

## Active decisions

- Guided Build authorization clarified by the learner: `next`, `nxt` and `continue` mean
  present the next task only. Codex must not edit files or show code snippets unless the
  current user message explicitly asks. Earlier implementation permission does not carry
  forward. Read-only inspection and routine checks remain Codex-owned; ask before any
  repair that changes files.
- Test-case exception confirmed by the learner: whenever a task requires tests, Codex
  provides the complete test snippet immediately with Arrange/Act/Assert explanation.
  The learner saves it unless explicitly asking Codex to edit the file.
- Security learning context is now authoritative in
  `docs/SECURITY_LEARNING_MAP.md`. Each tracker season links to its HTB focus, concrete
  tool trigger and PeerMock evidence gate. Use one module/section and one tool-backed
  question at a time; module completion or scanner output alone is not proof. Season 2
  uses `curl`, Season 3 uses local Burp request modification, Season 6 proves worker
  interruption/recovery, Season 7 introduces scoped review tools, and Season 8 keeps
  Promptfoo/Garak behind stable manual evaluation cases.
- Availability service/router follow-up 2026-09-19: the learner repaired session
  injection with `Annotated[AsyncSession, Depends(get_db_session)]`, uses HTTP 201 and
  explicitly converts the created entity with `SlotRead.model_validate`. Standalone
  OpenAPI verification shows `mentor_id` as a query parameter, `SlotCreate` as the body
  and no exposed session parameter. Read/list work now also exists. The availability
  router is not yet composed into the application, behavior tests remain open and Ruff
  reports the router, service and schema files need formatting.

- Durable Guided Build preference confirmed 2026-09-15 and stored in `AGENTS.md`:
  learner writes backend feature logic first from requirements/hints; Codex shows finished
  production code only after an explicit request. Codex may provide complete test code
  immediately and must explain Arrange, Act and Assert. Routine checks remain Codex-owned.

- Availability schemas verified 2026-09-15: learner corrected `SlotCreate` to use
  `starts_at`/`ends_at` and `SlotRead` to mirror persisted fields with
  `from_attributes=True`. Real valid create/read serialization passes; equal timestamps
  fail with the intended validation error. Ruff import/format repair applied and strict
  mypy passes (24 files). Next learner step: smallest availability create service.

- Historical availability schema issue (resolved): `SlotCreate` originally used
  `start_time`/`ends_time`; the learner renamed them to model-aligned
  `starts_at`/`ends_at`, and the later schema verification above supersedes this issue.

- Season 1 closure: user reaffirmed upgrade/downgrade/re-upgrade completion. Codex
  verified head `7d04311b0d5e`, zero drift, and three real PostgreSQL tests for duplicate
  feedback (23505), missing student (23503), and invalid duration (23514), plus valid
  record controls. Tests use transactions/savepoints and roll back all inserted records.
  Full database-enabled suite most recently passes 13 tests; Ruff and strict mypy pass,
  Alembic reports no drift and the database is at head. S1E1–S1E5 and the Season 1
  finale are complete; Season 2 is active at S2E2.
- Accepted cancellation policy: student cancels own confirmed booking before start,
  reopening the slot; mentor withdraws own slot, cancelling its confirmed booking while
  keeping the slot unavailable. Preserve completed booking/feedback history. No direct
  deletion or rescheduling of booked slots. These rules still need service enforcement.

- Latest user-directed task: populated the user's empty, Git-ignored `.env` with the
  three existing application settings and a placeholder `PEERMOCK_DATABASE_URL` using
  `postgresql+psycopg`. Dotenv parsing verified four populated entries without printing
  values. User subsequently supplied values and the URL structure/import checks passed.
- User added `db/base.py` and async `db/session.py` and repaired configuration to load
  `.env`, declare `database_url` and restore the `PEERMOCK_` prefix. Verified settings and
  session imports pass; engine driver is `postgresql+psycopg` and dialect is async.
  No database connection was attempted and no later tracker episode is marked complete.
  Package initializer and package import test now pass; database connectivity is unverified.

- Project name: PeerMock.
- Core product: secure mock-interview scheduling and private feedback.
- Core stack direction: Python, FastAPI, PostgreSQL, SQLAlchemy and Alembic.
- LLM question generation is deferred until core scheduling, authorization, concurrency
  and background-job boundaries are verified.
- The first deployable release has no payments, video calling, calendar integration or
  automated candidate scoring.

## Handoff discipline

At each pause, replace the current checkpoint and exact restart with fresh evidence.
Keep durable product, architecture, structure, production, learning and Git rules in
their authoritative documents rather than duplicating them here.
