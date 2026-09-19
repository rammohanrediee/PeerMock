# PeerMock Guided Build Roadmap

Execution order and completion status live only in
`.codex/plans/project-tracker.md`. This file supplies the learning missions for the
active episode.

This is a learning sequence, not a code-generation checklist. Complete one checkpoint
at a time. Do not request a finished implementation before writing your own attempt
unless you explicitly decide to change the learning method.

## Learning loop

For every checkpoint, record the following in `docs/LAB_JOURNAL.md`:

- **Explain:** What concept are you applying?
- **Predict:** What should happen for one allowed and one failure case?
- **Attempt:** What did you implement yourself?
- **Observe:** What did the test, response, database or log show?
- **Repair:** What caused the problem, and why does the change address it?
- **Retest:** Which allowed and denied cases now pass?

Ask Codex for help in this order:

1. “Give me the requirements and one hint for checkpoint X. Do not give me code.”
2. Implement your attempt.
3. “Review my checkpoint X implementation and identify exact mistakes and edge cases.”
4. Repair it yourself and request another review when useful.

## Entry gate

Project 1 is complete. Before the first API endpoint, confirm that you can:

- create and activate a Python virtual environment;
- explain functions, exceptions and imports;
- write basic `SELECT`, `INSERT`, `UPDATE` and `DELETE` statements;
- explain tables, primary keys and foreign keys;
- identify an HTTP method, path, request body, status code and response body.

Recommended HTB preparation:

- Start Introduction to Networking alongside foundation work when it helps the API
  mental model; it does not block unrelated packaging or domain work.
- Complete relevant Web Requests and Introduction to Web Applications sections by the
  Season 2 finale, using `curl` to inspect real local requests and responses.
- Complete relevant Using Web Proxies sections before permission testing, then use Burp
  only against local PeerMock to alter identifiers or tokens.
- Broken Authentication and Web Attacks while building authentication and object-level
  authorization; they are not blockers for starting the data model.
- SQL Injection Fundamentals before the later security-review milestone.

Use `docs/SECURITY_LEARNING_MAP.md` for the exact season-to-module mapping, Cyber Vault
references, tool triggers, PeerMock application task and evidence gate. The project
tracker still owns implementation order. Keep one active HTB module, and do not delay
unrelated backend episodes for supporting security material.

Choose tools from a concrete review question rather than working through a catalogue.
At episode start, state one tool-backed question or `No tool needed yet`. After using a
tool, explain what its output proves, what it cannot prove and how the result changed a
test, control or design decision.

## Checkpoint 0 — development foundation

**Purpose:** Make the repository reproducible before adding product behavior.

Learn virtual environments, dependency groups, Python package layout, environment
variables, linting, type checking and tests.

Your task:

- initialize Git;
- create `pyproject.toml` with runtime and development dependencies;
- make the `peermock` package importable;
- add one intentionally small test;
- document commands for linting, type checking and tests;
- make the first focused commit.

Predict what happens when the package is imported outside the repository and which
files must never be committed.

Done when a fresh virtual environment can install the project and run the test.

## Checkpoint 1 — domain and permission model

**Purpose:** Define the real workflow before designing endpoints.

Learn entities, identifiers, relationships, authentication versus authorization,
roles, ownership and application invariants.

Model only the core concepts:

- User with a student, mentor or coordinator role
- InterviewSlot published by a mentor
- Booking owned by a student and linked to one slot
- Feedback written by the assigned mentor for the booked student

Your task:

- decide slot and booking states;
- complete `docs/PERMISSION_MATRIX.md`;
- draw the initial data model in `ARCHITECTURE.md`;
- write at least six invariants in plain language;
- resolve cancellation, no-show and feedback-visibility rules.

Required invariants include:

- one slot belongs to exactly one mentor;
- one confirmed booking belongs to one student and one slot;
- a slot cannot have two active confirmed bookings;
- a student sees only their own bookings and feedback;
- a mentor manages only their own slots and assigned interviews;
- a mentor cannot submit feedback for an unassigned interview.

Done when you can settle permission questions without framework code.

## Checkpoint 2 — PostgreSQL schema and migrations

**Purpose:** Make the database enforce important truths.

Learn foreign keys, unique constraints, indexes, transactions, rollback, SQLAlchemy
models versus Pydantic schemas, and forward/reverse migrations.

Your task:

- run PostgreSQL locally with Docker Compose;
- configure SQLAlchemy and Alembic;
- create the User, InterviewSlot, Booking and Feedback tables;
- create and apply the initial migration;
- prove invalid relationships are rejected;
- upgrade a blank database and downgrade it safely.

Done when migrations recreate the schema and constraints reject invalid data for the
expected reason.

## Checkpoint 3 — minimal availability API

**Purpose:** Learn the complete HTTP-to-database path without pretending temporary
identity is real authentication.

Learn HTTP methods and status codes, request/response validation, database sessions and
stable error responses.

Your task:

- add a health endpoint;
- add the smallest useful create, retrieve and list operations for interview slots;
- return explicit response schemas;
- define predictable not-found and invalid-input errors;
- test allowed requests and failure cases.

Done when you can trace one request through validation, application behavior,
persistence and response creation.

## Checkpoint 4 — booking and cancellation behavior

**Purpose:** Express booking rules outside route handlers.

Learn service-level transactions, state transitions, conflict responses and the
difference between input validation and business rules.

Your task:

- reserve an available slot;
- cancel a booking;
- reject invalid state transitions;
- prevent overlapping active bookings for one student;
- test success, conflict, cancellation and no-show-related rules.

Done when the rules can be tested without depending on HTTP details.

## Checkpoint 5 — authentication

**Purpose:** Establish caller identity using maintained cryptographic libraries.

Learn password hashing, token expiry and verification, authentication versus
authorization failures, and secret storage.

Your task:

- register users without storing plaintext passwords;
- authenticate valid credentials;
- reject invalid and expired credentials;
- derive the current user only from validated authentication;
- keep secrets outside Git.

Do not invent password hashing or token cryptography.

Done when protected endpoints never trust a user ID in a request as proof of identity.

## Checkpoint 6 — role and object authorization

**Purpose:** Enforce privacy and role boundaries on every relevant operation.

Learn object-level authorization, IDOR, default-deny decisions, ownership-aware queries
and information leakage through errors.

Your task:

- enforce the permission matrix server-side;
- let students access only their bookings and feedback;
- let mentors manage only their slots and assigned interviews;
- restrict coordinator operations explicitly;
- test every role across create, read, update, list, book, cancel and feedback actions;
- capture and modify requests using a web proxy in your local lab.

Done when changing a booking, slot, mentor or feedback ID cannot expose or modify an
unauthorized record, while legitimate requests still work.

## Checkpoint 7 — concurrency and consistency

**Purpose:** Prevent two students from booking the same final slot.

Learn race conditions, transaction isolation, row locking, database constraints and
why a read-then-write check can fail.

Your task:

- send two competing booking attempts for one slot;
- observe the failure before selecting a control;
- implement a transaction/constraint strategy you can explain;
- prove exactly one booking succeeds and the other receives a conflict;
- prove cancellation returns the slot to an available, consistent state.

Done when the test is repeatable and the guarantee does not depend on lucky timing.

## Checkpoint 8 — evidence and delivery

**Purpose:** Make the backend understandable and reproducible to a reviewer.

Learn structured logging without sensitive values, CI feedback, trust boundaries,
residual risk and fresh-checkout verification.

Your task:

- add request correlation identifiers;
- trace one allowed and one denied request in sanitized logs;
- run tests, linting and type checks in CI;
- update architecture and permission documents;
- reproduce setup and migrations from a fresh checkout;
- document remaining limitations honestly;
- deploy a minimal working version when the local evidence is stable.

Done when another developer can run the API and its tests using only the repository
documentation.

## Core Project 2 completion gate

Before adding background or AI features, demonstrate:

- two simultaneous requests cannot book the same interview slot;
- identifier changes do not reveal or modify another user's records;
- students cannot perform mentor or coordinator actions;
- mentors cannot modify another mentor's slots or interviews;
- cancellation preserves consistency;
- migrations and meaningful tests run from a fresh checkout.

## Later milestone — reliable background work (Project 3)

Only after the core gate:

- import mentor availability from CSV;
- validate rows and expose job status;
- make retries idempotent;
- survive worker interruption without silent loss or duplication;
- enforce ownership, upload size and resource limits.

This milestone introduces the worker and queue. Do not add them earlier.

## Later milestone — LLM question-pack generation

Only after the core scheduling, authorization and background-job boundaries are
repeatable:

- accept role, experience level, topics, interview type, difficulty, duration, question
  count and an optional job description;
- generate a draft structured question pack in a bounded background job;
- validate the model output against a server-controlled schema;
- let the assigned mentor review and edit the draft before use;
- keep question-pack access subject to ordinary server-side authorization;
- apply input-length, question-count, token, retry, timeout and per-user usage limits;
- provide a safe failure or deterministic fallback when generation fails.

Read `docs/AI_FEATURE_BOUNDARY.md` before implementing this milestone. An LLM never
decides identity, permissions, booking state or who may access a question pack.
