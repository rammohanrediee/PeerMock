# PeerMock Working Memory

## Current checkpoint

- **Git:** `main` at `a5b2b76`, synchronized with `origin/main`; current episode work is
  uncommitted.
- **Active episode:** S3E5 — feedback submission/release and cross-identity security.
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
- **Exact restart:** Password login issues a 15-minute HS256 token, and `core.auth`
  accepts only HS256 tokens with a valid signature, issuer, audience, expiry and UUID
  subject. The current-user dependency loads the user from PostgreSQL, so role and
  ownership remain server-derived rather than token claims. `tests/unit/test_auth.py`
  passes 7 focused cases; focused Ruff and strict mypy pass. S3E2 remains active for a
  Guided Build Google identity-linking extension. Checkpoint 5G stages 1–2 now define
  the `OAuthIdentity` model, nullable password hash for OAuth-only accounts, and a
  provider-only `google.py` verification boundary. The `73d63721a2d0` OAuth migration
  creates `oauth_identities`, makes password hashes nullable and passed upgrade,
  downgrade-to-`7d04311b0d5e`, re-upgrade, drift and head checks against PostgreSQL.
  Ruff, strict mypy and compilation passed for the migration/model/provider modules.
  A brand-new Google account must select student or mentor; existing/linked accounts
  retain their stored role. The implementation includes provider verification,
  subject-first lookup, account link/create, nullable OAuth-only passwords and the
  `/auth/google` route. S3E2 completed on 2026-09-29: all 28 PostgreSQL-enabled tests
  pass, including synchronized concurrent Google sign-ins; Ruff and strict mypy pass;
  Alembic reports head `73d63721a2d0` with no drift. The race test confirms both
  sign-ins resolve to the same local user after the unique provider-subject conflict.
  S3E3 is complete. `require_roles` derives the stored database role through
  `get_current_user`; slot creation/withdrawal require `MENTOR`, and booking
  create/cancel require `STUDENT`. Student, mentor and coordinator request tests prove
  allowed operations work and disallowed roles receive 403. The booking-cancellation
  role regression was corrected. Combined focused auth, availability and booking tests
  pass (21); Ruff passes for the changed routers/tests and full mypy passes (48 source
  files). S3E4 booking identity slice is complete: booking create/cancel now pass
  `current_user.id` to their services and ignore a forged `student_id` query value. The
  focused booking API tests pass (8), including both spoofing cases; Ruff and full mypy
  pass. The S3E4 mentor routes now pass `current_user.id` to slot create/withdraw and no
  longer accept `mentor_id`, but the existing availability tests have two expected
  fixture failures because their transient mentor users have `id=None`. Ruff formatted
  the router and full mypy passes. The existing create and withdrawal tests now use an
  authenticated `MENTOR_ID` while sending a distinct forged query ID; their service
  assertions prove both routes use the authenticated identity. No new test cases were
  added. Combined focused auth/availability/booking tests pass (23); Ruff and full mypy
  pass. S3E4 is complete: the three existing PostgreSQL scheduling flows now override
  `get_current_user` for each synthetic actor and no longer rely on query owner IDs. All
  three pass against PostgreSQL, including foreign student cancellation and foreign
  mentor withdrawal returning hidden 404 responses. No integration tests were added.
  The S3E4 delivery gate passes: all 43 database-enabled tests pass; Ruff lint and format
  checks pass; strict mypy passes for 48 source files; Alembic is at head
  `73d63721a2d0` with no schema drift; and `git diff --check` passes. The untracked
  51-byte ASCII file `:memory:.ses` appears accidental and must not be staged unless the
  learner confirms it belongs in the repository. Exact restart: begin S3E5 by defining
  the smallest feedback create/read/release contracts and service rules from
  `docs/PERMISSION_MATRIX.md`.
  Before implementation, inspect the current `Feedback` model and decide the endpoint
  shapes without adding tests yet. Season 4 owns simultaneous-booking race protection.
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

- Guided Build checkpoint cadence reaffirmed 2026-09-28: after the learner says a task
  is done, Codex must inspect the saved work, run the narrow relevant verification,
  update this checkpoint with evidence and exact restart, then present the next task.
  Do not advance merely because a snippet was supplied or a task was described.
- Headroom preference confirmed 2026-09-20: launch future long PeerMock Codex CLI
  sessions from the repository with `headroom-codex`. The installed privacy wrapper keeps
  telemetry off and does not enable Serena. Headroom optimization does not replace the
  repository tracker or checkpoint, and it cannot be retrofitted into an already-running
  Codex Desktop conversation.
- Ruff cleanup authorization confirmed 2026-09-20: Codex automatically applies Ruff
  formatting and safe Ruff import/lint fixes. Do not assign those mechanical cleanups to
  the learner or pause episode progress for permission.
- Git-island guard confirmed 2026-09-20: do not create a branch, pull request or commit
  for each small learning step. Group related work into one cohesive episode/delivery
  branch and pull request; add commits only when they form useful review, rollback or
  independently complete boundaries. The user still performs Git/GitHub mutations unless
  explicitly delegating them to Codex.
- Test-island guard confirmed 2026-09-20: add a test only when it protects a meaningful
  user-visible contract, authorization boundary, data-integrity guarantee or demonstrated
  regression. Avoid accumulating mocked router/service tests that merely mirror calls or
  repeat serialization coverage. Prefer the smallest vertical test that crosses real
  application boundaries. For S2E2, the existing create-route contract test is enough
  mocked HTTP coverage; remaining evidence should be consolidated rather than adding
  separate mocked read-success and read-not-found tests.
- High-value test policy requested 2026-09-30; follow
  [`tests` skill](/Users/raghusmac/.codex/skills/tests/SKILL.md) whenever creating,
  changing or fixing tests. Before adding one, name the realistic bug it catches and
  search the existing suite to confirm the behavior is not already covered. Prefer
  extending a relevant test over adding a near-duplicate; parameterize only genuinely
  different behavior. Prioritize important happy paths, security/authorization edges,
  business failures and regressions; skip trivial wrappers, constructors, framework
  guarantees, exhaustive input combinations and implementation details. Aim for 1–4
  meaningful new tests for a normal change, adding more only when branching, security
  impact or demonstrated regressions justify them. Still run relevant existing checks.
  At handoff, state what tests were added, what each protects and why it is needed; if
  none are warranted, say so explicitly. This policy governs added tests, not verification
  commands.
- Production roadmap decision 2026-09-20: Jev may later act as an advisory typed judge.
  Phase 1 evaluates generated question drafts after the controlled Season 8 capability is
  stable. Candidate-answer scoring, adaptive interviews and performance analytics remain
  a separate post-MVP phase requiring consent, retention rules, labelled calibration,
  bias/error review, mentor override and a non-AI fallback. Jev supplies bounded signals;
  Python policy and mentors retain authority. See `PRODUCTION.md`.
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
