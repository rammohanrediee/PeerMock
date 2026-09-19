# PeerMock Production Baseline

This file defines release requirements, not current implementation status.

## Environments

- **Local:** Docker Compose PostgreSQL and development secrets in an ignored `.env`.
- **Test:** isolated PostgreSQL database with deterministic fixtures.
- **Deployed validation:** one API instance and managed PostgreSQL suitable for a small
  invited cohort.

Provider and hosting choices remain open until the delivery season.

## Configuration and secrets

- Validate required settings at startup.
- Store secrets in environment/hosting secret management, never Git or images.
- Use distinct database, token and model credentials per environment.
- Rotate any credential exposed in logs, screenshots or commits.

## HTTP and identity

- Serve deployed traffic only through HTTPS.
- Use explicit allowed origins if a browser frontend is added.
- Authentication tokens include issuer, audience, issued-at, expiry and unique ID where
  the chosen design requires them.
- Return the same safe result for absent and foreign private objects when existence is
  sensitive.
- Apply request-size and rate limits before public use.

## Database and migrations

- Run reviewed migrations as an explicit release step.
- Back up before destructive schema changes.
- Test restore into a separate database; a backup file alone is not recovery evidence.
- Keep booking constraints and transaction behavior identical between test and deployed
  PostgreSQL.

## Observability

- Correlate requests, background jobs and model calls with generated identifiers.
- Log decisions and failure classes without passwords, tokens, job descriptions,
  feedback text or question content.
- Separate liveness from readiness; readiness checks only critical dependencies with
  strict timeouts.

## Background and AI work

- Jobs carry identifiers, not credentials or unbounded content.
- Every job defines idempotency, maximum attempts, timeout, retryable errors and terminal
  failure behavior.
- Record model/provider, template/schema version, latency and usage for question-pack
  generation without exposing private prompt content.
- Booking remains available when question generation is unavailable.

## Release gate

A validation release requires:

- green tests, linting and type checks;
- migration from a blank database and from the previous schema;
- secret/dependency checks investigated rather than merely run;
- separate student, mentor and coordinator smoke tests;
- repeatable competing-booking test against PostgreSQL;
- backup restore evidence;
- documented rollback and known limitations.

