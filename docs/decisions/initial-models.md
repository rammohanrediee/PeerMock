# Initial entity model

The user requested model implementation ahead of the remaining Season 1 planning and
database gates. S1E2 later reviewed these schema choices against the saved models,
migration and permission policy. The accepted persistence boundary now lives in
`0001-database-and-persistence.md`; one role per account remains the first-release rule.

## Persisted shape

- User: UUID, creation time, unique email, display name, password hash and required role.
- InterviewSlot: mentor foreign key, topic, difficulty, start/end time and status.
- Booking: student and slot foreign keys, status and creation time. Keep cancellation
  history; `slot_id` is intentionally not unique.
- Feedback: unique booking foreign key, mentor foreign key, strengths, improvements and
  nullable release time. Null means private draft; student visibility is enforced later.

Identifiers are UUIDs generated at insert; creation timestamps use database defaults.
Timestamp columns request timezone support for PostgreSQL. Services must require aware
input and normalize to UTC. SQLite smoke tests do not prove timezone behavior.
Enums use named CHECK constraints and persist Python enum member names (uppercase);
their string values are lowercase. No ORM relationship loaders are added yet: explicit
foreign keys establish relationships without introducing implicit async database I/O.

Slot states are AVAILABLE, BOOKED, COMPLETED and CANCELLED. Booking states are CONFIRMED,
CANCELLED, COMPLETED and NO_SHOW. `docs/PERMISSION_MATRIX.md` owns the accepted transition,
actor and visibility rules. Models restrict stored values; services must enforce legal
transitions. Feedback may only be submitted by the assigned mentor after completion.

## Constraints and limits

The schema requires references to exist, positive slot duration, unique email and one
feedback record per booking. Referenced rows have no cascading deletion configured.
Email normalization, student/mentor role checks, assigned-mentor matching, release
permissions, cancellation rules and overlapping student bookings remain service work.
A foreign key proves existence, not authorization. Duplicate active bookings remain
possible until Season 4 demonstrates the race and selects the PostgreSQL guarantee.

## Verification

The initial model tests include a linked-record round trip and SQLite smoke rejection of
duplicate feedback, zero-duration slots and nonexistent student references. PostgreSQL
DDL compilation and ORM mapper configuration pass for all four tables. The live Alembic
upgrade/downgrade/re-upgrade cycle finishes at revision `7d04311b0d5e` with zero drift.
PostgreSQL tests verify valid controls plus unique, foreign-key and CHECK constraint
rejections. Booking concurrency remains deliberately unproved until Season 4.
