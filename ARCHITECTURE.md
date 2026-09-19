# PeerMock System Architecture

## Purpose and status

This document defines PeerMock's technical boundaries. `PROJECT_BLUEPRINT.md` defines
capability scope, `PROJECT_STRUCTURE.md` defines file/module ownership, and the tracker
defines execution status.

Labels:

- **Current:** implemented and verified in the repository.
- **Target:** approved direction, not necessarily implemented.
- **Decision required:** must be resolved before the affected episode completes.

Current state: application/configuration/session shells and four core SQLAlchemy models
exist. The initial Alembic migration has completed a live PostgreSQL
upgrade/downgrade/re-upgrade cycle with no model drift, and live constraint tests pass.
Availability schema/service/router work exists ahead of tracker order but is paused.
Authentication, authorization and booking services are not implemented. Persistence and
authentication decisions are recorded under `docs/decisions/`.

## Architectural style

**Target:** a modular monolith with one FastAPI application and one PostgreSQL database.
Feature services own business rules. HTTP routers and future workers call those same
services.

```text
API client
   |
   v
FastAPI
   |-- users/authentication
   |-- mentor availability
   |-- bookings
   |-- feedback
   `-- later: question packs
   |
   v
PostgreSQL

Later only:
FastAPI -> Redis/queue -> worker -> model adapter
```

Microservices are not a project goal. A boundary is extracted only after demonstrated
scaling, isolation or deployment evidence requires it.

## Module boundaries

| Module | Responsibility | Status |
|---|---|---|
| `api` | Application composition, versioned routers and health endpoints | Target |
| `core` | Settings, stable errors and cross-cutting primitives | Target |
| `db` | Engine, session lifecycle and shared metadata | Target |
| `users` | Accounts, roles, password login and token identity | Target |
| `availability` | Mentor-owned interview slots and visibility | Target |
| `bookings` | Booking/cancellation transitions and consistency | Target |
| `feedback` | Assigned-mentor authoring and student release rules | Target |
| `question_packs` | Later draft generation, review and approval | Deferred |

Routers translate HTTP. Services enforce behavior and authorization. Persistence code
applies ownership predicates and transaction operations. See `PROJECT_STRUCTURE.md` for
the allowed dependency direction.

## Identity and access boundary

**Target request sequence:**

1. Validate authentication and resolve the server-side current user.
2. Pass authenticated context to a typed feature service.
3. Include ownership or assignment predicates in private-record queries.
4. Return the same safe result for absent and foreign private objects when existence is
   sensitive.
5. Validate role and state transition before committing.
6. Record security-sensitive transitions without logging private content.

Client-supplied user, mentor, booking or feedback identifiers never establish authority.
`docs/PERMISSION_MATRIX.md` is completed before implementing this boundary.

## Core data model

**Target vocabulary:**

| Record | Purpose |
|---|---|
| `User` | Authenticated person with an explicit role |
| `InterviewSlot` | Mentor-owned availability with topic, difficulty and time window |
| `Booking` | Student's stateful claim on one slot |
| `Feedback` | Private mentor assessment for one completed booking |

Minimum relationship sketch:

```text
User (mentor) 1 -------- * InterviewSlot
                              |
                              | 1
                              |
User (student) 1 -------- * Booking 1 -------- 0..1 Feedback
                              |                      |
                              | *                    | *
                              |                      |
                              1                      1
                       InterviewSlot          User (mentor)
```

The database enforces existence, unique email, positive slot duration and at most one
feedback row per booking. Services must enforce role correctness, booking-student
ownership and that `Feedback.mentor_id` matches the mentor owning the booked slot.

**Decided in S1E1–S1E2:** records use UUIDs and timezone-aware timestamps; each
first-release account has one fixed role; slot, booking, cancellation, no-show and
feedback-release transitions follow `docs/PERMISSION_MATRIX.md`; terminal history is
retained rather than deleted. PostgreSQL/SQLAlchemy/Alembic decisions are recorded in
`docs/decisions/0001-database-and-persistence.md`; identity storage, Argon2 hashing and
short-lived token decisions are in `docs/decisions/0002-authentication-mechanism.md`.

## Booking lifecycle

The accepted first-release lifecycle is:

```text
Slot:    AVAILABLE -> BOOKED -> COMPLETED
            |           |
            v           +------> AVAILABLE   (student cancellation before start)
         CANCELLED      `------> CANCELLED   (mentor withdrawal)

Booking: CONFIRMED -> COMPLETED
             |  `-----> NO_SHOW
             `--------> CANCELLED
```

Completion enables assigned-mentor feedback. A no-show consumes the elapsed slot and
does not enable feedback. Terminal booking states do not transition again. The permission
matrix owns the full actor, timing, visibility and retention conditions.

## Authentication boundary

**Target for Season 3:** registration normalizes email and stores an Argon2 encoded hash.
Login verifies through `pwdlib` and returns an HS256-signed 15-minute access token. The
token contains a user UUID and standard validation claims, not authorization state.
Each protected request validates the allowlisted algorithm, signature, expiry, issuer
and audience, then loads the current user and role from PostgreSQL before applying the
permission matrix.

Signing secrets remain outside Git. Refresh tokens, persistent sessions and per-token
revocation are deliberately absent from the learning MVP; see the authentication
decision record for consequences and reopening conditions.

## Concurrency boundary

PostgreSQL is the final source of truth for whether a slot may be booked. Season 4 first
reproduces two competing requests, then selects a constraint/locking strategy from the
evidence.

The invariant is independent of implementation choice:

```text
active confirmed bookings per slot <= 1
```

Exactly one competing request succeeds; the other receives a stable conflict response.

## Background-job boundary

**Deferred to Season 6.** Background tasks carry identifiers rather than credentials or
unbounded file content. Each job defines:

- idempotency key and expected state;
- maximum attempts and bounded backoff;
- execution and external-call timeouts;
- retryable versus terminal failures;
- user-safe progress/status;
- correlation and recovery behavior.

Workers call feature services rather than duplicating business or authorization rules.

## AI boundary

**Deferred to Season 8.** Question generation uses a provider-independent adapter with
strict input and output contracts.

```text
Authorized request
  -> validate and admit bounded job
  -> model adapter
  -> parse and schema-validate untrusted output
  -> store draft under ordinary ownership rules
  -> mentor review and approval
```

The model never receives database credentials and never decides identity, access,
booking state or visibility. `docs/AI_FEATURE_BOUNDARY.md` owns the detailed rules.

## API conventions

**Target:**

- versioned routes under `/api/v1`;
- explicit Pydantic request and response contracts;
- stable domain error codes and safe messages;
- server-derived identity;
- pagination for collections that can grow;
- idempotency for retryable creation/background requests;
- separate liveness and readiness endpoints;
- OpenAPI generated from the implemented route contracts.

Readiness checks only critical dependencies with strict timeouts. They do not call an
LLM.

## Decisions still open

- Token/session lifecycle beyond the learning MVP
- Deployment provider and region
- LLM provider/model allowlist and cost ceiling
- Data retention and account deletion policy

Local core development may proceed once the decisions assigned to its active season are
recorded. Deployment or AI decisions do not block Season 0.
