# Database and persistence boundary

Date: 2026-09-16

Status: accepted

## Problem

PeerMock needs one authoritative persistence model for relationships, lifecycle history
and later booking concurrency. Local tests must not create confidence from behavior that
differs from production PostgreSQL.

## Options considered

- SQLite for local development and PostgreSQL later
- PostgreSQL from the first persistence season
- Synchronous SQLAlchemy sessions
- SQLAlchemy asyncio sessions using Psycopg
- Eager ORM relationships versus explicit foreign-key queries

## Decision

- PostgreSQL is the authoritative database for application and integration behavior.
  SQLite is limited to fast model smoke tests and never proves PostgreSQL constraints,
  timestamp behavior, migrations or concurrency.
- Use SQLAlchemy 2.x asyncio APIs with `psycopg`, one `AsyncSession` per request or job,
  and Alembic for every schema change.
- Services own transaction completion. Routers translate HTTP and inject sessions;
  repositories or explicit statements own queries when they improve clarity.
- Use application-generated UUID primary keys and database-generated creation times.
  Services accept timezone-aware datetimes and normalize them to UTC.
- Persist enum member names through named CHECK constraints. Stored lifecycle values are
  therefore uppercase even though Python enum string values are lowercase.
- Keep relationships explicit through foreign keys and queries. Do not add implicit ORM
  relationship loading that can trigger unexpected async I/O.
- Keep terminal booking and feedback history. Foreign keys have no cascading deletion;
  account deletion and anonymization require a later explicit retention decision.
- Database constraints enforce referential existence, unique email, positive slot
  duration and one feedback row per booking. Services enforce user roles, ownership,
  mentor/slot matching, legal transitions, normalized email and overlapping student
  schedules.
- The final one-active-booking-per-slot concurrency guarantee remains a Season 4
  decision made after reproducing the race. `Booking.slot_id` remains non-unique until
  then so cancelled history can coexist with a later valid booking.

## Consequences

- PostgreSQL-backed tests are required for claims about constraints or migrations.
- A foreign key proves that a row exists, not that its role or caller is authorized.
- Transaction boundaries remain visible and testable in feature services.
- Raw SQL writers must provide required enum values because current defaults are
  application-side, not server defaults.
- Deletion is intentionally conservative until retention and anonymization are designed.

## Evidence to revisit

- Migration `7d04311b0d5e` upgrades, downgrades and returns to head without drift.
- Live PostgreSQL tests distinguish valid records from unique, foreign-key and CHECK
  constraint failures by SQLSTATE.
- Season 4 must revisit the booking constraint after recording the unsafe interleaving.
- A future account-deletion requirement must revisit non-cascading foreign keys and
  retained personal data.
