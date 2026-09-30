# PeerMock Project Tracker

## Tracker contract

Every implementation task belongs to exactly one numbered season and episode. Start by
reporting its purpose, previous verified state, completion condition and narrow
verification. Preserve order unless the user explicitly changes scope. Mark completion
only after inspecting the saved implementation and passing the listed gate.

At the start of each episode, open its season's security learning bridge and report one
of `Study now: <module/section and application>` or `No study prerequisite`. Name at
most one tool-backed question, or say `No tool needed yet`. Installing or running a tool
is never a completion gate; record the observation, implementation decision and retest.

## Project status

- **Season 0 — Reproducible foundation:** Complete
- **Season 1 — Domain and persistence:** Complete
- **Season 2 — Availability and booking API:** Complete
- **Season 3 — Identity and authorization:** Active
- **Season 4 — Concurrency and consistency:** Pending
- **Season 5 — Evidence and validation release:** Pending
- **Season 6 — Reliable background work:** Deferred until core completion
- **Season 7 — Security review and recovery:** Deferred until working application
- **Season 8 — Controlled AI question packs:** Deferred until secure/reliable boundaries

## Season 0 — Reproducible foundation

Purpose: turn the documentation scaffold into an installable, testable Python project.

Learning bridge: [Season 0 — Reproducible foundation](../../docs/SECURITY_LEARNING_MAP.md#season-0--reproducible-foundation).

Study/apply reminder: reinforce Linux and package-environment inspection as needed; no
offensive tool is required.

- [x] **S0E0** Establish product, architecture, structure, production, learning and
  execution documents without claiming application functionality.
- [x] **S0E1** Initialize Git, create `pyproject.toml`, make `peermock`
  importable and add one small test.
- [x] **S0E2** Configure focused test, lint and type-check commands and verify them in a
  fresh virtual environment.

Finale gate: a fresh environment installs PeerMock and runs the documented checks.

## Season 1 — Domain and persistence

Purpose: define PeerMock's rules and make PostgreSQL enforce important relationships.

Learning bridge: [Season 1 — Domain and persistence](../../docs/SECURITY_LEARNING_MAP.md#season-1--domain-and-persistence).

Study/apply reminder: use web/request material only to clarify trust boundaries; prove
important relationships with PostgreSQL and migration evidence.

- [x] **S1E1** Decide roles, states, invariants and complete the permission matrix.
  First-release role, ownership, coordinator, cancellation, completion, no-show and
  feedback-release rules are recorded with twelve invariants and no unresolved core
  permission cells. Documented state names match the persisted enums.
- [x] **S1E2** Draw the data model and record database/authentication decisions.
  Architecture now reflects the actual four-table/five-foreign-key schema. Accepted
  decision records define PostgreSQL/async SQLAlchemy/Alembic persistence and the
  Argon2 plus short-lived HS256 authentication boundary.
- [x] **S1E3** Add local PostgreSQL configuration and SQLAlchemy session wiring.
  Environment-backed local configuration, async Psycopg engine and per-call session
  dependency are verified by a live `SELECT 1` and cleanup check. The engine uses a
  connection timeout, pre-ping and hidden SQL parameters; full database suite: 8 passed.
- [x] **S1E4** Implement User, InterviewSlot, Booking and Feedback persistence models.
  The four registered SQLAlchemy models match the accepted role/state policy and initial
  migration. Portable model tests and live PostgreSQL checks verify linked records,
  foreign keys, positive slot duration and one feedback record per booking. Repository
  verification passes with 13 tests, Ruff, strict mypy and zero Alembic drift.
- [x] **S1E5** Create/apply/reverse the first Alembic migration and test constraints.
  Initial revision `7d04311b0d5e` is generated and its offline PostgreSQL SQL is verified;
  the user reports a live upgrade/downgrade/re-upgrade cycle, and Codex verified the final
  head plus zero autogenerate drift. Three live PostgreSQL constraint tests pass with
  rollback cleanup. Together with the completed policy and model episodes, this satisfies
  the Season 1 finale gate.

Finale gate: a blank PostgreSQL database is reproducible and rejects invalid core
relationships for the expected reason.

## Season 2 — Availability and booking API

Purpose: deliver the smallest complete scheduling workflow before authentication.

Learning bridge: [Season 2 — Availability and booking API](../../docs/SECURITY_LEARNING_MAP.md#season-2--availability-and-booking-api).

Study/apply reminder: study the relevant HTTP/web sections and use `curl` to trace
implemented allowed and rejected requests.

- [x] **S2E1** Add liveness and readiness endpoints with stable response contracts.
  Liveness returns a stable success response. Readiness verifies the database and returns
  a sanitized 503 contract for database failure or an unexpected result. Four focused
  endpoint tests pass, including dependency-controlled success and failure paths.
- [x] **S2E2** Add mentor availability/slot create, read and list behavior.
  The versioned API exposes create, read and chronologically ordered list operations with
  typed request/response contracts and stable creation status. One focused HTTP contract
  test and one rollback-safe PostgreSQL service flow cover the meaningful boundaries
  without duplicative mock tests. Full database-enabled suite: 15 passed; Ruff formatting
  and lint, strict mypy and Alembic drift/head checks pass.
- [x] **S2E3** Add booking state transitions and conflict behavior. Real HTTP-to-
  PostgreSQL tests cover successful booking, sequential slot conflict, overlapping
  student-schedule conflict, permitted adjacent booking, and the future-start rule.
- [x] **S2E4** Add cancellation and prove slot state remains consistent. Student
  cancellation reopens the future slot while retaining cancelled history; mentor
  withdrawal cancels a booked slot and its confirmed booking without reopening it.
  Foreign ownership, repeated cancellation and elapsed-slot withdrawal have stable
  denied responses and leave protected state unchanged.
- [x] **S2E5** Verify the temporary unauthenticated vertical slice without describing it
  as secure or production-ready. A rollback-safe real PostgreSQL flow creates, lists,
  books and cancels a synthetic slot; temporary query-parameter identity remains a
  known non-production limitation.

Finale gate: one slot can be created, listed, booked and cancelled with predictable
errors and meaningful service/API tests.

## Season 3 — Identity and authorization

Purpose: replace temporary identity with authenticated, server-enforced boundaries.

Learning bridge: [Season 3 — Identity and authorization](../../docs/SECURITY_LEARNING_MAP.md#season-3--identity-and-authorization).

Study/apply reminder: study the relevant proxy, authentication and access-control
sections; use Burp only against local PeerMock to alter identifiers or tokens and prove
that the server enforces authority.

- [x] **S3E1** Add registration and Argon2 password hashing. Public registration accepts
  student or mentor accounts but rejects coordinator self-registration, normalizes email,
  stores only an Argon2 hash and returns a password-safe response. A rollback-safe real
  PostgreSQL HTTP test covers success, duplicate email and invalid privileged role.
- [x] **S3E2** Add signed, expiring login tokens, current-user resolution and Google
  identity linking. Password tokens validate HS256 signature, issuer, audience, expiry
  and UUID subject; current users and roles come from PostgreSQL. Google verification
  requires a verified email and stable subject; linking prefers provider subject, while
  first-time email linking preserves the local user's name and role. New OAuth-only
  accounts select student or mentor and receive a normal PeerMock token. A synchronized
  PostgreSQL race regression proves concurrent first sign-ins resolve to one local user.
  Final gate: 28 PostgreSQL-enabled tests, Ruff, strict mypy and Alembic head/drift pass.
- [x] **S3E3** Enforce role capabilities on the implemented role-limited operations using
  the stored current-user role. Mentor-only slot creation/withdrawal and student-only
  booking creation/cancellation are covered by allowed-role controls and denied-role
  tests. Coordinator access is denied on these mutations; no coordinator-only operation
  exists in the current API.
- [x] **S3E4** Enforce owner predicates for implemented slot and booking mutations.
  Routes derive mentor/student IDs from the authenticated database user; service queries
  hide foreign cancellation/withdrawal as not found. Existing PostgreSQL flows prove
  legitimate and foreign-owner behavior without relying on query owner IDs. Feedback
  assignment begins with its implementation in S3E5.
- [ ] **S3E5 — Active** Add feedback submission/release and complete cross-identity
  security tests.

Finale gate: client identifiers cannot grant access; foreign private objects stay hidden
and legitimate role journeys still work.

## Season 4 — Concurrency and consistency

Purpose: prove booking correctness under competing requests.

Learning bridge: [Season 4 — Concurrency and consistency](../../docs/SECURITY_LEARNING_MAP.md#season-4--concurrency-and-consistency).

Study/apply reminder: prioritize PostgreSQL transactions, locking and constraints; use
controlled concurrent tests rather than adding a scanner.

- [ ] **S4E1** Build a deterministic competing-booking test that reproduces the race.
- [ ] **S4E2** Select and document the PostgreSQL locking/constraint strategy.
- [ ] **S4E3** Make exactly one competing booking succeed with a stable conflict result.
- [ ] **S4E4** Verify cancellation and retry behavior preserve consistency.

Finale gate: repeated concurrency tests never produce two active bookings for one slot.

## Season 5 — Evidence and validation release

Purpose: make the core backend reviewable, reproducible and usable by a small cohort.

Learning bridge: [Season 5 — Evidence and validation release](../../docs/SECURITY_LEARNING_MAP.md#season-5--evidence-and-validation-release).

Study/apply reminder: inspect logs, process identity and network exposure; use selective
Nmap only against the owned deployment and manually verify its results.

- [ ] **S5E1** Add sanitized structured logs and request correlation.
- [ ] **S5E2** Add CI for behavior, typing, linting and migration checks.
- [ ] **S5E3** Refresh architecture, permission and lab evidence from implemented behavior.
- [ ] **S5E4** Deploy the minimal API and run separate-role smoke tests.
- [ ] **S5E5** Observe a small user trial and convert one real failure into a regression
  test and repair.

Finale gate: another developer can reproduce the system, deployed core journeys work,
and one real user-discovered problem is repaired with evidence.

## Season 6 — Reliable background work (Project 3)

Purpose: import mentor availability without duplication, silent loss or request blocking.

Learning bridge: [Season 6 — Reliable background work](../../docs/SECURITY_LEARNING_MAP.md#season-6--reliable-background-work).

Study/apply reminder: study relevant upload/API-abuse material while implementing
bounds, idempotency and recovery; interrupt a worker and verify recovery through tests
and correlated logs.

- [ ] **S6E1** Define upload limits, row schema and background-job lifecycle.
- [ ] **S6E2** Add worker/queue infrastructure and job-status API.
- [ ] **S6E3** Import valid rows and report rejected rows.
- [ ] **S6E4** Prove idempotent replay and bounded retry behavior.
- [ ] **S6E5** Interrupt a worker and verify recovery plus ownership boundaries.

Finale gate: replay and interruption produce neither duplicate slots nor silent loss.

## Season 7 — Security review and recovery (Project 4)

Purpose: assess and repair the implemented system using reproducible evidence.

Learning bridge: [Season 7 — Security review and recovery](../../docs/SECURITY_LEARNING_MAP.md#season-7--security-review-and-recovery).

Study/apply reminder: begin with manual behavioral proof, then introduce Semgrep,
Gitleaks, Trivy, `pip-audit`, Nmap or ffuf only for the specific review question each
tool answers.

- [ ] **S7E1** Finalize trust boundaries, permission matrix and selected ASVS controls.
- [ ] **S7E2** Reproduce three relevant weaknesses, including authorization and unsafe
  input handling.
- [ ] **S7E3** Repair each finding with regression and legitimate-use tests.
- [ ] **S7E4** Investigate dependency, secret, deployment exposure and least privilege.
- [ ] **S7E5** Restore a backup into an isolated database and verify core journeys.

Finale gate: all findings contain reproduction, impact, repair, retest and residual risk;
restored data is usable and consistent.

## Season 8 — Controlled AI question packs

Purpose: generate mentor-reviewed draft questions without giving the model authority.

Learning bridge: [Season 8 — Controlled AI question packs](../../docs/SECURITY_LEARNING_MAP.md#season-8--controlled-ai-question-packs).

Study/apply reminder: study the AI-attack material exercised by the implemented
boundary; stabilize manual normal and hostile evaluation cases before automating them
with Promptfoo or Garak.

- [ ] **S8E1** Define strict request, draft, approval and provenance contracts.
- [ ] **S8E2** Implement a provider-independent adapter and deterministic fake.
- [ ] **S8E3** Run bounded generation in the existing worker lifecycle.
- [ ] **S8E4** Validate/store drafts and enforce mentor/interview ownership.
- [ ] **S8E5** Evaluate injection, malformed output, timeout, replay, premature access and
  legitimate requests.
- [ ] **S8E6** Record model/template versions, usage, latency and safe failure behavior.

Finale gate: hostile or incorrect output cannot change authorization or booking state;
authorized mentors can review a validated draft and manual authoring remains available.

## Deferred product ideas

Payments, video calls, public mentor marketplace, calendar synchronization, automated
candidate scoring, résumé ranking and mobile apps remain outside Seasons 0–8.
