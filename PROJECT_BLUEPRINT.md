# PeerMock Project Blueprint

This blueprint defines the longer-term capability scope. `PRODUCT.md` owns product
behavior, `ARCHITECTURE.md` owns technical boundaries, `PRODUCTION.md` owns release
operations, and `.codex/plans/project-tracker.md` alone owns execution order and status.

## Outcome

Build a small, secure backend that turns mentor availability into consistent interview
bookings and private feedback, then extend it with reliable bulk work and controlled AI
question generation.

## Capability 1 — Reproducible foundation

- Installable Python package and isolated environment
- Runtime/development dependency groups
- One meaningful test and documented quality commands
- Configuration that keeps secrets outside Git

Exit gate: a fresh environment installs the project and runs its first test.

## Capability 2 — Domain and persistence

- Users with explicit student, mentor and coordinator roles
- Mentor-owned interview slots
- Student-owned bookings
- Assigned-mentor feedback with controlled release
- PostgreSQL schema, constraints and reversible Alembic migrations

Exit gate: a blank database can be migrated and invalid relationships are rejected for
the expected reason.

## Capability 3 — HTTP availability and booking

- Health endpoint
- Versioned slot list/read/create/update surface
- Booking and cancellation operations
- Stable response contracts and domain error codes
- Explicit state transitions

Exit gate: allowed and failure journeys work through the API with meaningful tests.

## Capability 4 — Identity and authorization

- Argon2 password hashing through a maintained library
- Signed, expiring authentication tokens
- Server-derived current user
- Role and object predicates inside services/queries
- Hidden-not-found behavior where revealing a foreign record would leak information
- Cross-user and cross-mentor isolation tests

Exit gate: changing identifiers cannot reveal or mutate foreign bookings, slots,
feedback or question packs.

## Capability 5 — Booking consistency

- Explicit transaction boundary for booking/cancellation
- Repeatable competing-request test
- PostgreSQL locking/constraint strategy selected from observed evidence
- Clear conflict behavior
- Consistent cancellation and slot availability

Exit gate: exactly one of two simultaneous attempts can book the same slot.

## Capability 6 — Reviewable delivery

- Structured logs and request correlation without private content
- CI for tests, linting, typing, migrations and secret/dependency checks
- Current architecture and permission documentation
- Fresh-checkout verification
- Minimal deployment and multi-role smoke test

Exit gate: another developer can run and verify the documented system, and the deployed
core journeys work for separate test identities.

## Capability 7 — Reliable background work

- Coordinator CSV import of mentor availability
- Validated rows, job states and rejected-row reporting
- Idempotency, bounded retries and interruption recovery
- Ownership, upload-size and resource limits

Exit gate: replay and worker interruption do not silently duplicate or lose slots.

## Capability 8 — Security review and recovery

- Architecture/trust-boundary diagram and completed permission matrix
- Three reproduced findings, repairs and regression tests
- Legitimate-use controls after each repair
- Dependency, secret and deployment-permission review
- PostgreSQL backup restoration into an isolated test database

Exit gate: findings are reproducible, repaired and retested, and restored data supports
the core journeys.

## Capability 9 — Controlled AI question packs

- Strict input/output schemas and provider-independent adapter
- Bounded asynchronous generation
- Server-side ownership and approval rules
- Prompt-injection, malformed-output, timeout and replay evaluations
- Manual question-authoring fallback
- Versioned model/template metadata, latency and usage evidence

Exit gate: hostile or malformed model behavior cannot change permissions or booking
state, and mentors can safely review a stored draft.

