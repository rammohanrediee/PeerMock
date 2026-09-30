# PeerMock

PeerMock is a backend API for scheduling peer-led mock interviews. Students can find
and book interview slots, mentors can publish availability, and participants receive
role-appropriate access to bookings and private feedback.

The project focuses on server-enforced authorization, reliable booking state, and a
clear modular architecture. PeerMock is currently under active development.

## Features

- Student and mentor account registration
- Password login with short-lived bearer tokens
- Google identity sign-in and account linking
- Role-based access control for students, mentors, and coordinators
- Mentor availability creation, listing, and withdrawal
- Student booking and cancellation workflows
- PostgreSQL-backed persistence with Alembic migrations
- Liveness and database-readiness endpoints
- Structured API errors and generated OpenAPI documentation

Feedback workflows, concurrency hardening, background jobs, and AI-assisted question
packs are planned but are not part of the current release.

## Tech stack

- Python 3.12+
- FastAPI and Pydantic
- PostgreSQL
- SQLAlchemy 2 and Alembic
- Argon2 password hashing and JWT authentication
- pytest, Ruff, and mypy

## Project structure

```text
peermock/
├── migrations/                   # Alembic environment and database revisions
├── src/peermock/
│   ├── api/                      # API composition, health checks, and error responses
│   ├── core/                     # Configuration, authentication, and shared errors
│   ├── db/                       # Database engine, sessions, metadata, and model registry
│   └── features/
│       ├── users/                # Registration, login, identities, and roles
│       ├── availability/         # Mentor interview slots
│       ├── bookings/             # Student bookings and cancellations
│       └── feedback/             # Private post-interview feedback
├── tests/                        # Unit and PostgreSQL integration tests
├── ARCHITECTURE.md               # System boundaries and design
├── PRODUCT.md                    # Product behavior and scope
├── PRODUCTION.md                 # Deployment and release requirements
└── pyproject.toml                # Package metadata, dependencies, and tool configuration
```

## Local setup

### Prerequisites

- Python 3.12 or newer
- PostgreSQL
- Git

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/rammohanrediee/PeerMock.git
cd PeerMock
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

Create a `.env` file in the repository root:

```dotenv
PEERMOCK_DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/peermock
PEERMOCK_JWT_SECRET=replace-this-with-a-random-secret-at-least-32-characters-long
PEERMOCK_JWT_ISSUER=peermock
PEERMOCK_JWT_AUDIENCE=peermock-api
PEERMOCK_ACCESS_TOKEN_MINUTES=15
PEERMOCK_DEBUG=false
PEERMOCK_GOOGLE_CLIENT_ID=
```

Keep `.env` local. It is ignored by Git and must never contain production credentials.

Create the PostgreSQL database, apply migrations, and start the API:

```bash
createdb peermock
alembic upgrade head
uvicorn peermock.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation is at
`http://127.0.0.1:8000/docs`.

## API overview

All application routes use the `/api/v1` prefix.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/v1/health/live` | Check whether the API process is running |
| `GET` | `/api/v1/health/ready` | Check whether PostgreSQL is reachable |
| `POST` | `/api/v1/auth/register` | Register a student or mentor |
| `POST` | `/api/v1/auth/login` | Authenticate with email and password |
| `POST` | `/api/v1/auth/google` | Authenticate with a Google ID token |
| `GET` | `/api/v1/slots` | List interview slots |
| `GET` | `/api/v1/slots/{slot_id}` | Read an interview slot |
| `POST` | `/api/v1/slots` | Create a mentor-owned slot |
| `DELETE` | `/api/v1/slots/{slot_id}/withdraw` | Withdraw a mentor-owned slot |
| `POST` | `/api/v1/bookings` | Book a slot as a student |
| `POST` | `/api/v1/bookings/{booking_id}/cancel` | Cancel a student-owned booking |

Protected endpoints expect an access token in the `Authorization` header:

```text
Authorization: Bearer <access-token>
```

## Development checks

Run the standard checks from the activated virtual environment:

```bash
pytest
ruff check src tests
ruff format --check src tests
mypy
```

PostgreSQL integration tests are opt-in and require a local migrated test database:

```bash
PEERMOCK_RUN_DB_TESTS=1 pytest tests/integration
```

## Design principles

- Authentication establishes identity; request parameters never establish ownership.
- Feature services own business rules, while routers translate HTTP requests and
  responses.
- PostgreSQL is the final authority for booking consistency and relational integrity.
- Private records are filtered by the authenticated user's role and ownership.
- AI-generated content, when introduced, remains advisory and cannot control identity,
  authorization, booking state, or visibility.

For more detail, see [PRODUCT.md](PRODUCT.md), [ARCHITECTURE.md](ARCHITECTURE.md),
[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md), and
[docs/PERMISSION_MATRIX.md](docs/PERMISSION_MATRIX.md).

## License

No license has been added yet. All rights are reserved unless a license is introduced.
