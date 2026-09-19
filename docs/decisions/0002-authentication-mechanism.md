# Authentication mechanism and stored identity

Date: 2026-09-16

Status: accepted for the learning MVP

## Problem

PeerMock must authenticate users without storing recoverable passwords or trusting
client-supplied identity, role or ownership claims. The mechanism should be small enough
to reason about before adding refresh-token or session infrastructure.

## Options considered

- Store reversible or plaintext passwords
- Implement password cryptography directly
- Use maintained Argon2 password hashing through `pwdlib`
- Server-side sessions
- Short-lived signed access tokens with or without refresh tokens
- Trust a role embedded in a token versus load current authority from PostgreSQL

## Decision

- Store only the encoded password hash in `User.password_hash`; never store or log a
  plaintext password.
- Normalize an email with `strip().casefold()` at the registration/login service
  boundary before lookup and storage. The database unique constraint then applies to
  the normalized value.
- Use `pwdlib`'s recommended password hasher from the installed Argon2 extra. Verify with
  `verify_and_update` so a valid login can replace an outdated hash when parameters
  change. Do not design password hashing primitives in PeerMock.
- Use a short-lived HS256 access JWT for the learning MVP. A single PeerMock API issues
  and verifies the token, so a symmetric algorithm keeps the boundary small. Use a
  cryptographically random environment secret of at least 32 bytes; verification always
  allowlists `HS256` rather than selecting an algorithm from the token header. Validate
  signature, expiration, issuer and audience.
- The access token carries only the user UUID in `sub` plus `iat`, `exp`, `iss` and
  `aud`. Role, ownership and assignment authority are loaded from PostgreSQL for every
  protected request; token claims never grant those permissions.
- Use a 15-minute access-token lifetime initially. Refresh tokens, persistent sessions,
  revocation lists and remember-me behavior are deferred until a demonstrated product
  need justifies their state and threat model.
- Return the same generic authentication failure for an unknown email or wrong password.
  Invalid, expired or otherwise unverifiable tokens receive an unauthenticated response.
- Keep the signing secret, issuer and audience in runtime configuration outside Git.
  Never include password hashes, tokens or secrets in responses or logs.

## Consequences

- Authorization sees current database role and ownership rather than stale role claims.
- The MVP cannot revoke an individual access token before its short expiry. Secret
  rotation invalidates all tokens signed with the retired secret.
- Password-reset, email verification, account disabling, refresh rotation and session
  inventory remain explicit future work rather than hidden assumptions.
- Authentication establishes identity only; the permission matrix still controls every
  operation.

## Evidence to revisit

- Season 3 must test correct-password login, wrong-password/unknown-user equivalence,
  hash upgrade, token expiry, signature rejection, issuer/audience rejection and current
  database role resolution.
- Deployment work must verify secret strength, injection, rotation procedure and absence
  from source, logs and generated artifacts.
- A requirement for immediate logout, account disabling or multi-device session control
  must reopen the token/session choice.
