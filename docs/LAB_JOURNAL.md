# Lab Journal

Create one entry for each meaningful checkpoint, failure or repair.

## Entry template

**Date:**

**Checkpoint:**

**Question:** What am I trying to understand or prove?

**Explain:** Describe the concept in your own words.

**Prediction:** State the expected allowed result and failure result before running
anything.

**Attempt:** Describe what you implemented or changed. Link to the relevant commit when
available.

**Commands/requests:** Record only useful, reproducible commands and sanitized HTTP
requests. Never record credentials or tokens.

**Observed evidence:** Include status codes, relevant test output, constraint errors or
sanitized logs.

**Cause:** Explain why the observed behavior happened.

**Repair:** Explain the smallest change that addressed the cause.

**Retest:** Record both the previously failing case and a legitimate case that must
continue to work.

**Remaining risk/question:** What has not been proved yet?

---

**Date:** 2026-09-14

**Checkpoint:** S0E1 — early application/configuration shell

**Question:** Can PeerMock expose an importable FastAPI application whose basic metadata
comes from environment-backed settings without introducing later database or feature work?

**Explain:** `Settings` owns process configuration and reads `PEERMOCK_`-prefixed
environment variables. The app factory owns FastAPI composition, keeping construction
separate from module-level ASGI discovery.

**Prediction:** Importing `peermock.main` should expose a FastAPI instance named `app`.
An invalid value for a typed environment setting should fail validation rather than be
silently accepted.

**Attempt:** Added `src/peermock/core/config.py` and `src/peermock/main.py`. No routes,
database connections or feature behavior were added.

**Commands/requests:** `python3 -m py_compile src/peermock/core/config.py
src/peermock/main.py`; a `PYTHONPATH=src python3 -c ...` runtime import probe.

**Observed evidence:** Both files compiled successfully. The runtime import stopped at
`ModuleNotFoundError: No module named 'pydantic_settings'` because the project dependencies
have not been installed in a virtual environment. No Ruff or mypy executable is currently
available.

**Cause:** The repository declares `pydantic-settings` and FastAPI, but S0E1's fresh
environment install has not yet been performed.

**Repair:** No source repair was indicated by the syntax check. Install the declared `dev`
extra in a Python 3.12+ virtual environment before runtime verification.

**Retest:** Re-run the default and environment-override import probes after dependencies
are installed, followed by Ruff and strict mypy.

**Remaining risk/question:** S0E1 still requires the package initializer, its small import
test and fresh-environment installation evidence before it can be marked complete.

## S0E1 — package import verification

**Explain:** The package initializer exposes a version; pytest imports the installed
package and checks that public value.

**Prediction:** Version `0.1.0` passes; a different version fails the assertion.

**Attempt:** Codex filled the two empty files at the user's explicit request.

**Observe:** `.venv/bin/pytest tests/unit/test_package.py` reported 1 passed.

**Repair:** Replaced empty files that previously collected zero tests with a package
initializer and one typed test function.

**Retest:** The narrow test and Ruff checks on both changed Python files passed.

**Remaining:** Full application behavior is not covered by this import test. Fresh
environment installation and full quality checks remain the S0E2/Season 0 finale gate.

## S0E2 — reproducible quality checks

**Explain:** Quality tools must check the local source, and an isolated environment
must install the declared dependencies without relying on the developer environment.

**Predict:** Fresh installation should run the import test, lint and strict type checks.

**Attempt:** Codex ran routine verification as requested by the learner.

**Observe:** Pytest and Ruff passed; mypy initially treated PeerMock as an installed
untyped package and refused package discovery.

**Repair:** Configured mypy to check `src` and `tests` directly and added package
initializers for api/core/db. Documented setup and quality commands in README.

**Retest:** Installed `.[dev]` in a fresh temporary Python 3.12 environment. Pytest:
1 passed; Ruff: passed; mypy: 10 files passed; pip check: no broken requirements.
The initial sandbox DNS restriction was resolved by an approved network-enabled retry.

**Remaining:** The single test checks package import/version only. Database connectivity
and product behavior are unverified. Temporary verification environment remains at
`/private/tmp/peermock-verify.J2qhLR/venv`.

## Early S1E4 — core entities requested by the learner

**Explain:** Typed SQLAlchemy models describe stored records. Foreign keys enforce
existence; services must still enforce role, ownership and lifecycle rules.

**Predict:** Linked records persist; duplicate feedback, invalid slot duration and a
missing student reference fail integrity checks.

**Attempt:** Codex implemented four feature-owned models, explicit enums, a shared
identity/time mixin and a model import registry at the user's request.

**Observe:** Four tests passed, including SQLite integrity smoke tests with foreign keys
enabled. All four tables compile using the PostgreSQL dialect; mappers configure.

**Repair:** No behavior repair was needed; Ruff formatted the new files.

**Retest:** Full pytest, Ruff and strict mypy pass (22 source files checked).

**Remaining:** No database was modified. PostgreSQL migrations, race protection and
service permissions remain unverified; earlier Season 1 policy gates stay open.

## Early S1E5 — initial migration generation

**Explain:** Alembic compares registered SQLAlchemy metadata with the current database
schema and records the difference in a versioned upgrade/downgrade revision.

**Predict:** A blank PeerMock database should produce four tables in foreign-key order;
offline SQL should reverse them safely in dependency order through `downgrade()`.

**Attempt:** Added Alembic configuration for the async Psycopg engine and generated
revision `7d04311b0d5e` against the blank local database.

**Observe:** The first connection exposed a missing SQLAlchemy async dependency. After
declaring `sqlalchemy[asyncio]`, Alembic connected and detected all four tables plus their
indexes and constraints. PostgreSQL offline SQL generation completed.

**Repair:** Installed the declared asyncio extra, formatted the generated revision and
fixed its import ordering.

**Retest:** Four pytest tests, Ruff, strict mypy and offline `upgrade head --sql` pass.

**Remaining:** The local `peermock` database exists but the migration has not been
applied. Live upgrade, constraint inspection, downgrade and re-upgrade remain required.

## S1E5 — PostgreSQL constraint verification

**Explain:** Live database tests verify migration-created constraints rather than only
ORM declarations. SQLSTATE identifies the reason for each rejection.

**Predict:** Valid linked records succeed; duplicate feedback, absent students and
zero-duration slots fail with 23505, 23503 and 23514 respectively.

**Attempt:** User reports upgrade/downgrade/re-upgrade completed. Codex added opt-in
PostgreSQL tests using unique test emails and outer rollback transactions/savepoints.

**Observe:** All three PostgreSQL cases pass, including legitimate record controls and
timezone-aware creation timestamps. Test writes are rolled back; no schema changes.

**Repair:** Sandbox denied localhost access; approved local access enabled verification.

**Retest:** Full suite 7 passed; Ruff passed; mypy passed for 23 files. Alembic head is
7d04311b0d5e and its drift check reports no new upgrade operations.

**Remaining:** Earlier domain/permission gates are open. These constraints do not enforce
authorization or concurrent booking exclusivity.

## Availability schema attempt

**Explain:** API schema field names must match the model/service vocabulary so validated
data maps without manual renaming.

**Predict:** A payload with `starts_at` and `ends_at` should validate; reversed or naive
times should fail.

**Attempt:** Learner added `SlotCreate` and `SlotRead`.

**Observe:** `SlotRead` is correctly shaped. `SlotCreate` still expects `start_time` and
`ends_time`, so the real payload reports both expected fields missing. Mypy passes; Ruff
also reports import formatting.

**Repair/Retest:** Rename the two fields and validator references, then rerun the three
schema cases before continuing.

**Lifecycle retest:** The learner reports completing upgrade, downgrade to base and
re-upgrade. Codex independently observed revision `7d04311b0d5e (head)` afterward, and
`alembic check` reported no new upgrade operations. PostgreSQL constraint failure cases
remain to be exercised.

## S1E1 — permission and lifecycle policy

**Explain:** Authentication identifies the caller; authorization combines that identity
with role, ownership, assignment and current object state. A foreign identifier is not
proof of access.

**Prediction:** The completed matrix should allow each documented student and mentor
journey while denying cross-user actions and coordinator access to feedback. Its state
names should match the SQLAlchemy enums.

**Attempt:** At the learner's explicit request, Codex completed the first-release role
policy, permission matrix, slot/booking/feedback lifecycles and twelve invariants.

**Commands/requests:** Searched the matrix for unresolved `TBD` values and imported the
persisted slot and booking enums to compare their names with the documented states.

**Observed evidence:** No core `TBD` remains. All persisted states are documented:
`AVAILABLE`, `BOOKED`, `CANCELLED`, `COMPLETED`, `CONFIRMED` and `NO_SHOW`. The saved
matrix includes legitimate-use conditions and explicit denial boundaries.

**Cause:** Model and migration work had been completed early, while the policy document
still contained only placeholders.

**Repair:** Replaced the placeholders with default-deny, ownership-aware rules; resolved
coordinator scope, withdrawal, cancellation, completion, no-show and feedback release;
and linked the decisions from the architecture document.

**Retest:** Repeated the unresolved-marker and enum-name checks after saving the policy;
both passed. No application behavior is claimed because service authorization is a later
season.

**Remaining risk/question:** S1E2 must reconcile the architecture with the implemented
schema and record the authentication storage decision. Server-side enforcement remains
for Seasons 2 and 3.

## S1E2 — data model and persistence/authentication decisions

**Explain:** A model diagram describes relationships, while a decision record explains
why storage and authentication boundaries were chosen and which guarantees belong to
the database, service or later season.

**Prediction:** The architecture should contain the same four tables and five foreign
keys registered in SQLAlchemy metadata. The installed authentication dependencies should
support the chosen Argon2 hashing and HS256 token mechanisms.

**Attempt:** Codex reconciled the architecture and initial-model note with the live
migration evidence. Two accepted decision records now define PostgreSQL persistence,
async session/transaction ownership, retention, Argon2 password storage and the
short-lived HS256 access-token boundary.

**Commands/requests:** Imported `Base.metadata` and compared its table/foreign-key sets
with the documented model. Inspected the installed `pwdlib` recommended hasher and
`verify_and_update` support, then checked PyJWT's available algorithms.

**Observed evidence:** Metadata contains exactly `users`, `interview_slots`, `bookings`
and `feedback`, connected by the five documented foreign keys. `pwdlib` 0.3.1 selects
`Argon2Hasher` and exposes hash upgrade support. PyJWT 2.14.0 provides HS256.

**Cause:** Earlier implementation notes still described live migration work as pending
and left the authentication mechanism underspecified.

**Repair:** Updated the current-state architecture and lifecycle diagram, refreshed the
initial-model verification, and recorded explicit database and authentication decisions
with consequences and reopening conditions.

**Retest:** Metadata, dependency-capability, stale-marker and trailing-whitespace checks
all passed after the documentation changes.

**Remaining risk/question:** These decisions are not authentication implementation.
Season 3 must prove hashing, generic login failures, claim validation, expiry and current
database role resolution. S1E3 must first inspect the existing database/session wiring.

## S1E3 — async PostgreSQL session lifecycle

**Explain:** `create_async_engine` owns the connection pool, `async_sessionmaker` creates
one unit-of-work object per call, and the async-generator dependency guarantees session
cleanup when its consumer finishes or fails.

**Prediction:** A local `postgresql+psycopg` session should return `1` from `SELECT 1`,
start a transaction, and have no active transaction after the dependency generator is
closed. A non-local database URL must fail before connecting.

**Attempt:** Added an opt-in integration test for the application session dependency and
strengthened the engine with pre-ping, a five-second connection timeout and hidden SQL
parameters. Corrected the dependency return type from `AsyncIterator` to the accurate
`AsyncGenerator` so cleanup is visible to static analysis.

**Commands/requests:** Ran focused Ruff and mypy checks, the live session test and the
full suite with `PEERMOCK_RUN_DB_TESTS=1`.

**Observed evidence:** The initial live test was denied by the filesystem/network
sandbox, not PostgreSQL. With approved localhost access, `SELECT 1` and cleanup passed.
The full database-enabled suite reports 8 passed; Ruff and focused mypy pass.

**Cause:** Existing wiring had never been exercised through the async application
dependency. Its broad iterator annotation also concealed `aclose()` from mypy.

**Repair:** Added the focused integration check, corrected the annotation, bounded
connection attempts and configured pytest for short tracebacks after a deep driver trace
revealed sensitive connection parameters.

**Retest:** The hardened focused integration test and all eight tests pass. No records or
schema objects are changed by the session test.

**Remaining risk/question:** The database credential shown by the first failed traceback
must be rotated outside the repository. Full-project mypy still reports the already-known
paused Season 2 router return-type mismatch; S1E3's two affected files pass mypy.
