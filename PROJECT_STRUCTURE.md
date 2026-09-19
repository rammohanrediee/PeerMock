# PeerMock Project Structure

## Architectural style

PeerMock is a modular monolith. Feature folders own cohesive behavior while one FastAPI
process and one PostgreSQL database keep local development and reasoning simple.

## Planned tree

```text
peermock/
├── .codex/
│   ├── notepad.md
│   └── plans/project-tracker.md
├── .github/workflows/            # Added when CI is activated
├── migrations/                   # Alembic environment and revisions
├── src/peermock/
│   ├── api/                      # Application/router composition
│   ├── core/                     # Settings, errors and cross-cutting primitives
│   ├── db/                       # Engine, sessions and shared metadata
│   └── features/
│       ├── users/                # Accounts, authentication and roles
│       ├── availability/         # Mentor slots and availability rules
│       ├── bookings/             # Booking state and consistency
│       ├── feedback/             # Private interview feedback
│       └── question_packs/       # Later AI-assisted drafts and approval
├── tests/
│   ├── unit/                     # Domain/service behavior
│   ├── integration/              # API, migrations and PostgreSQL
│   └── security/                 # Identity and object/role boundaries
├── docs/
│   ├── decisions/                # Dated architecture decisions
│   ├── evidence/                 # Sanitized verification artifacts
│   ├── AI_FEATURE_BOUNDARY.md
│   ├── LAB_JOURNAL.md
│   └── PERMISSION_MATRIX.md
├── AGENTS.md
├── ARCHITECTURE.md
├── GUIDED_BUILD.md
├── PRODUCT.md
├── PRODUCTION.md
├── PROJECT_BLUEPRINT.md
├── PROJECT_STRUCTURE.md
├── README.md
├── compose.yaml                  # Added with PostgreSQL checkpoint
└── pyproject.toml                # Created by the learner in S0E1
```

Planned files are named here to establish ownership; the tracker decides when they are
created.

## Feature module shape

A feature may introduce only the pieces its behavior needs:

```text
feature/
├── models.py       # SQLAlchemy persistence model when owned here
├── schemas.py      # Pydantic input/output contracts
├── service.py      # Business rules and transaction orchestration
├── repository.py   # Queries when separating them improves ownership clarity
├── router.py       # HTTP translation and dependency wiring
└── errors.py       # Stable domain failures
```

This is a menu, not a requirement to create every file. Start with the smallest module
that keeps HTTP, business rules and persistence responsibilities clear.

## Dependency direction

```text
router -> service -> persistence
             |
             -> domain errors/contracts
```

- Routers do not implement booking or authorization rules.
- Services do not depend on FastAPI request objects.
- Persistence receives server-derived identity/ownership predicates.
- Workers later call the same services as HTTP routes.
- AI adapters return untrusted structured candidates; ordinary services validate and
  authorize storage and access.

## Growth rules

- Add infrastructure in the season that exercises it.
- Extract a new abstraction after repeated behavior reveals the boundary.
- Keep one database and deployable service until measured evidence justifies separation.
- Update this file when module ownership changes; update the tracker only for execution
  status.

