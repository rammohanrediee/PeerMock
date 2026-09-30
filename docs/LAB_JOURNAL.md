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

## S2E2 — availability create, read and list

**Explain:** The HTTP router owns request/response translation, while the availability
service owns persistence operations. Tests should cross meaningful boundaries rather
than building separate mock islands around every function.

**Prediction:** A valid mentor slot should be created with `AVAILABLE` status, retrieved
by UUID and returned in chronological list order. The HTTP creation contract should
return 201 without exposing the database session as a request parameter.

**Attempt:** The learner implemented typed schemas, async create/read/list services and
FastAPI routes, then composed the availability router under `/api/v1`. One focused HTTP
contract test replaces external boundaries; one PostgreSQL service flow creates slots
out of order and verifies real persistence, retrieval and ordering.

**Observe:** OpenAPI exposes the expected health and slot paths. The database-backed flow
passes against migrated PostgreSQL and rolls back its mentor and slot records. The full
database-enabled suite passes 15 tests with 95% aggregate coverage.

**Repair:** Corrected dependency injection and response conversion during the guided
attempt. Ruff automatically normalized the final availability test and three existing
whitespace-only differences. Rejected additional mocked read tests as unnecessary test
islands.

**Retest:** Ruff lint and format checks pass for 38 files; strict mypy passes 34 source
files. Alembic reports no new upgrade operations and database revision
`7d04311b0d5e (head)`.

**Remaining risk/question:** Identity is still temporarily client supplied and this
slice is not secure until Season 3. Booking conflict behavior begins in S2E3; the final
competing-request consistency strategy remains deliberately deferred to Season 4.

## S2E3–S2E5 — booking, cancellation and temporary vertical slice

**Explain:** Booking and cancellation are state transitions spanning two rows. The
service changes both records in one transaction; routers translate HTTP inputs and
outputs without taking ownership of business rules.

**Prediction:** An available future slot can be booked once; an overlapping confirmed
booking is denied; a student cancellation reopens its future slot; mentor withdrawal
cancels a future booked slot without reopening it. Elapsed withdrawal must be denied
without changing stored state.

**Attempt:** Added booking and cancellation routes/services, a mentor withdrawal route,
and rollback-safe PostgreSQL HTTP tests. The temporary vertical flow creates, lists,
books and cancels synthetic records through the API.

**Observe:** The booking integration module passes three tests against local PostgreSQL.
The full opt-in database suite reports 18 passed. The elapsed-slot withdrawal response
is `409 slot_not_withdrawable`, and the slot remains `AVAILABLE`.

**Repair:** Loaded the complete SQLAlchemy model registry at application startup, fixed
the cancellation ownership check, and added the elapsed-withdrawal guard before any
booking or slot mutation.

**Retest:** Ruff passes for 62 files; strict mypy passes 41 source files; Alembic is at
`7d04311b0d5e (head)` with no detected drift. Test transactions roll back all synthetic
records.

**Remaining risk/question:** Client-supplied student and mentor IDs remain temporary and
unauthenticated. Season 3 must replace them with validated current-user identity.

## S3E1 — registration and Argon2 password hashing

**Explain:** Registration accepts untrusted identity input, narrows self-service roles,
normalizes email and stores a one-way password hash. The response schema excludes both
plaintext passwords and encoded hashes.

**Prediction:** Student or mentor registration returns 201 and a safe user projection.
Reusing a normalized email returns 409. Public coordinator registration fails validation
and creates no row.

**Attempt:** Added registration request/response schemas, an Argon2-backed registration
service, the `/api/v1/auth/register` route and one rollback-safe HTTP-to-PostgreSQL test.

**Observe:** The persisted password differs from plaintext and verifies through pwdlib.
The response contains neither `password` nor `password_hash`; duplicate email returns
`email_already_registered`; coordinator input returns 422.

**Repair:** Corrected an accidental `sqlite3.IntegrityError` import to SQLAlchemy's
`IntegrityError`, preserving PostgreSQL SQLSTATE handling and session rollback after a
failed commit.

**Retest:** The registration integration test passes. The full database-enabled suite
passes 19 tests; Ruff passes for 63 files and strict mypy passes 42 source files.

**Remaining risk/question:** Registration does not verify email ownership or real-world
mentor credentials. Login, JWT validation and database-backed current-user authority are
S3E2 work.

## S3E2 — signed login tokens and current-user resolution

**Explain:** A signed token identifies a request only after its signature and required
claims have been validated. It does not establish authorization: the server must load
the current user, including the role, from PostgreSQL.

**Prediction:** A correctly signed, unexpired token with the configured issuer,
audience and UUID subject resolves its user. Missing, malformed, expired,
invalid-subject and unknown-user credentials all receive the same `401 invalid_token`
failure without revealing which check failed.

**Attempt:** Completed `core.auth` with an HS256 allowlist, configured secret, issuer
and audience validation, UUID-subject parsing and the `get_current_user` dependency.
Added focused unit coverage using an async SQLAlchemy-session double.

**Commands/requests:** `pytest tests/unit/test_auth.py`; `ruff check
tests/unit/test_auth.py src/peermock/core/auth.py`; `mypy src/peermock/core/auth.py
tests/unit/test_auth.py`.

**Observed evidence:** The focused suite reports 7 passed. Ruff and strict mypy pass
for the password-token authentication implementation and tests.

**Cause:** The initial test attempt used `pytest.mark.asyncio`, but PeerMock's installed
test stack exposes AnyIO instead of `pytest-asyncio`, so collection failed.

**Repair:** Replaced the async markers with `pytest.mark.anyio` and applied Ruff's
safe import-order cleanup.

**Retest:** A valid token resolves the database user. Malformed, expired,
invalid-subject, missing-credential and unknown-user cases raise the same safe domain
error.

**Remaining risk/question:** Google sign-in is now a Guided Build extension of S3E2.
The premature implementation snippets were removed before evidence was claimed. Build
the provider identity table, typed verification boundary, subject-first lookup and
atomic link/create flow in Checkpoint 5G. Then S3E3 must apply database-derived roles to
actual role-limited operations, and S3E4 must add object ownership predicates.

## S3E2 / Checkpoint 5G — Google provider boundary

**Explain:** Google token verification is an external-provider boundary. It validates
untrusted provider claims and returns only the typed data required by PeerMock's later
identity-resolution service; it does not query or mutate local accounts.

**Attempt:** The learner added the Google client-ID setting, maintained verification
dependency, `OAuthIdentity` model and initial `google.py` implementation.

**Observe:** The first `google.py` combined token verification with identity lookup,
user creation and a commit. It also called `.strip()` on an unvalidated email claim and
could not create an OAuth-only `User` because password hash and role requirements were
not yet resolved.

**Repair:** Kept provider verification in `google.py`, returning a typed
`VerifiedGoogleIdentity` only after validating non-empty `sub`, email and
`email_verified is True`. Moved database work out of that module. Registered
`OAuthIdentity` metadata and made the model's password hash nullable for future
OAuth-only accounts.

**Retest:** Ruff, strict mypy and `py_compile` pass for `google.py`, user models and the
model registry. Provider behavior tests and a PostgreSQL migration remain required.

**Remaining risk/question:** The persistence changes are not in the live schema yet.
Create and verify the Alembic revision before building subject-first lookup and atomic
link/create behavior.

## S3E2 / Checkpoint 5G — OAuth identity migration

**Explain:** A database migration applies an approved model change to databases that
already exist. Its upgrade and downgrade need to account for the older schema's inability
to represent an OAuth-only account without a password hash.

**Attempt:** The learner created revision `73d63721a2d0` to create `oauth_identities`,
enforce the provider-plus-subject uniqueness invariant, index user lookup and permit a
nullable password hash.

**Observe:** The initial revision metadata still contained the placeholder revision ID
and two module docstrings, preventing a clean Alembic graph/lint result.

**Repair:** Replaced the placeholder with `73d63721a2d0` and removed the duplicate
docstring. The downgrade preserves local user rows by replacing null password hashes
with a disabled marker before restoring the old non-null constraint; it removes OAuth
identity links because the old schema cannot represent them.

**Retest:** Offline PostgreSQL SQL contains the nullable-password alteration, identity
table, uniqueness constraint and user index. Live PostgreSQL upgrade, downgrade to
`7d04311b0d5e`, re-upgrade, Alembic drift check and head check pass. Ruff and strict
mypy pass for the migration, model and provider-boundary modules.

**Remaining risk/question:** A brand-new Google account must explicitly select student
or mentor. Existing/linked accounts retain their stored role regardless of submitted
input. Identity resolution must look up provider subject first and use verified email
only for an initial link decision.

## S3E2 / Checkpoint 5G — identity resolution and completion

**Explain:** Google's verified `sub` is the stable provider identity. Concurrent first
sign-ins can both observe no link, so the database uniqueness constraint must decide
the winner and the losing transaction must roll back, retry and return the same local
user.

**Prediction:** A valid provider identity links or creates one local user. Two
simultaneous first sign-ins for that identity both return the same user, with exactly
one persisted provider link. Missing `sub` and unverified email claims fail before any
link or account is created.

**Attempt:** The saved flow verifies provider claims, resolves identities by subject,
links verified email matches or creates OAuth-only users, and issues a local PeerMock
token. At the learner's request, Codex changed unit-test patches to typed string
targets and added a synchronized two-session PostgreSQL race regression with unique
synthetic records and explicit cleanup.

**Commands/requests:** `PEERMOCK_RUN_DB_TESTS=1 .venv/bin/python -m pytest -q`;
`.venv/bin/ruff check . && .venv/bin/ruff format --check .`; `.venv/bin/mypy`;
`.venv/bin/alembic current && .venv/bin/alembic check`.

**Observed evidence:** All 28 PostgreSQL-enabled tests pass. The concurrency regression
forces both transactions past the initial missing-identity lookup, then verifies both
return the existing user's UUID and exactly one Google identity row remains. Ruff
passes, strict mypy passes for 47 source files, and Alembic reports head
`73d63721a2d0` with no new upgrade operations.

**Cause:** The original unit test accessed imported dependencies through attributes
that the Google module does not explicitly export, which failed strict mypy. The earlier
integration flow did not exercise the uniqueness-conflict retry path.

**Repair:** Patch `settings` and the Google verifier by fully qualified string target.
Use two independent sessions and a barrier after their first scalar lookup to make the
uniqueness conflict deterministic; assert both callers resolve to the same user and
remove the synthetic rows afterward.

**Retest:** Valid and invalid provider-claim unit cases, the existing-account link and
new-account creation flow, and the concurrent retry regression pass. Full PostgreSQL
tests, Ruff, strict mypy and Alembic head/drift checks pass.

**Remaining risk/question:** Provider verification is exercised with mocked Google
claims, not a live Google credential. Account roles are now stored locally; S3E3 must
enforce role capabilities on real operations. Ownership and assignment predicates
remain S3E4 work.

## S3E3 — student-only booking routes

**Explain:** The shared role dependency uses the authenticated user's stored role to
decide whether booking creation and cancellation are available.

**Predict:** A student request reaches the existing booking service and returns its
normal success status. Mentor and coordinator requests receive `403 role_not_permitted`
before either service operation runs.

**Attempt:** The learner added one parameterized API behavior test covering create and
cancel routes for student, mentor and coordinator roles. Both service functions are
stubbed so the test isolates route authorization and response serialization.

**Observed evidence:** All six route/role combinations pass: student create returns 201,
student cancellation returns 200, and mentor/coordinator requests return 403 with the
expected error code. Ruff passes and full mypy passes for 48 source files.

**Retest:** `.venv/bin/pytest -q tests/unit/test_booking_api.py`; Ruff check and format
check for the new test; full `.venv/bin/mypy`.

**Remaining risk/question:** Role review found the existing slot-withdrawal endpoint is
not yet protected by the mentor role. Finish that S3E3 capability check. Client-supplied
mentor/student identity and object ownership remain for S3E4.

## S3E3 — slot-withdrawal role check (in progress)

**Explain:** Slot withdrawal is a mentor-only capability; authentication alone does not
authorize a student or coordinator to perform it.

**Predict:** An authenticated mentor request should reach the withdrawal service and
return 200. Student and coordinator requests should return `403 role_not_permitted`.

**Attempt:** The learner added a parameterized HTTP test for all three roles, with the
withdrawal service stubbed so the role boundary is isolated.

**Observe:** On the first run, mentor, student and coordinator all returned 200, exposing
the missing guard. On recheck, the mentor-role dependency is present and all three cases
pass: mentor returns 200, student/coordinator return 403.

**Retest:** `pytest -q tests/unit/test_availability_api.py` passes all 8 tests. Combined
auth, availability and booking tests pass all 21 cases. The booking-cancellation role
regression was corrected to `STUDENT`. Ruff passes for the changed routers/tests and full
mypy passes for 48 source files.

**Remaining risk/question:** S3E3 covers role capabilities on current operations. S3E4
must stop trusting client-supplied `student_id` and `mentor_id`, and ensure service
queries enforce ownership.

## S3E4 — authenticated student identity for bookings

**Explain:** A role check says the caller is a student; the current user's database ID
must also determine which student's booking is created or cancelled. A query parameter
cannot establish identity.

**Predict:** Supplying another `student_id` in the URL must not change the ID passed to
the booking service or returned in the response. Legitimate create/cancel requests still
return their existing success status.

**Attempt:** At the learner's request, both booking route handlers now inject the
database-backed current user and pass `current_user.id` to their existing services. The
untrusted query parameter is no longer part of either handler signature. The spoofing
test gives the authenticated user and query parameter different UUIDs and covers both
routes.

**Observed evidence:** All 8 booking API cases pass, including both cross-identity query
spoofs and the six existing role cases. Ruff check/format pass for the changed router and
test; full mypy passes for 48 source files.

**Retest:** `.venv/bin/pytest -q tests/unit/test_booking_api.py`; focused Ruff check and
format check; full `.venv/bin/mypy`.

**Remaining risk/question:** Availability create and withdrawal still take
`mentor_id` from the client. Apply the same server-derived identity rule to those two
mentor operations next. No new Python security module was necessary; the rule is to use
the already validated current-user dependency.

## S3E4 — authenticated mentor identity for slots

**Explain:** A mentor role permits slot mutation, while the authenticated user's ID
determines which mentor owns the created slot and which mentor may withdraw it. A query
parameter cannot establish that identity.

**Predict:** Changing `mentor_id` in the request must not change the ID passed to slot
creation or withdrawal. The authenticated mentor retains the normal success paths, and
the existing wrong-role requests remain denied.

**Attempt:** The learner changed both availability handlers to inject the current user
and pass `current_user.id` to the existing services. Codex repaired the two existing
tests so they assign the transient mentor an explicit ID and send a different forged
query ID in the actual HTTP request.

**Observed evidence:** The service doubles receive `MENTOR_ID` despite the forged query
value. Combined auth, availability and booking tests pass all 23 cases. Ruff check and
format pass for the changed availability files; full mypy passes for 48 source files.

**Retest:** `.venv/bin/pytest -q tests/unit/test_auth.py
tests/unit/test_availability_api.py tests/unit/test_booking_api.py`; focused Ruff; full
`.venv/bin/mypy`.

**Test value:** No new cases were added. Extending the existing create and withdrawal
cases protects the cross-mentor identity boundary and catches accidental reuse of a
client query ID without duplicating role or response-contract coverage.

**Remaining risk/question:** Existing PostgreSQL HTTP flows still switch actors through
query IDs from the earlier unauthenticated slice. Update those same tests to override
`get_current_user` for each actor so real ownership predicates are exercised under the
new authentication boundary.

## S3E4 — PostgreSQL ownership verification

**Explain:** Router identity derivation and service ownership predicates must work
together. A legitimate authenticated owner succeeds, while a different authenticated
user receives the same not-found response as an absent private object.

**Attempt:** Codex updated the three existing scheduling integration flows to override
`get_current_user` before each synthetic actor's request and removed query owner IDs. No
new tests were added.

**Observed evidence:** All three PostgreSQL tests pass. The second student cannot cancel
the first student's booking and receives `404 booking_not_found`; the foreign mentor
cannot withdraw the owner's slot and receives `404 slot_not_found`. The legitimate
student and mentor controls succeed. Ruff passes and full mypy passes for 48 source
files.

**Retest:** `PEERMOCK_RUN_DB_TESTS=1 pytest -q
tests/integration/test_booking_service.py`; focused Ruff; full mypy.

**Test value:** These reused tests protect the cross-user and cross-mentor ownership
boundaries through real HTTP, service and PostgreSQL behavior. No additional cases were
needed because the existing flows already contained both attacks and legitimate controls.

**Remaining risk/question:** S3E5 must introduce feedback assignment, privacy and release
rules with similarly bounded cross-identity evidence.
