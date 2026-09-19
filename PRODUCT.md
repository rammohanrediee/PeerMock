# PeerMock Product

## Product statement

PeerMock helps students book practice interviews with peer mentors and receive private,
structured feedback. Coordinators organize interview events without weakening the
privacy of bookings, feedback or question packs.

## People

- **Student:** finds a suitable slot, books it, manages the booking and reads released
  feedback.
- **Mentor:** publishes availability, conducts assigned interviews and writes feedback.
- **Coordinator:** organizes events and schedules using explicitly authorized actions.

A later product decision may allow one account to hold multiple roles. Until that
decision is recorded, each test identity has one role.

## Core journeys

### Student books an interview

1. The student signs in.
2. They filter available slots by topic, difficulty and time.
3. They book one slot.
4. The server confirms exactly one booking or returns a clear conflict.
5. The student can view or cancel only their own booking.

### Mentor completes an interview

1. The mentor signs in and sees their own schedule.
2. They view the assigned student's minimum necessary booking details.
3. They mark the interview complete and submit private feedback.
4. The student sees feedback only after the defined release transition.

### Coordinator organizes an event

1. The coordinator creates or updates an event.
2. They associate mentors and time boundaries using explicit permissions.
3. They monitor operational status without gaining unrestricted access to private
   feedback.

## Core promises

- A slot cannot have two active confirmed bookings.
- Private records are accessible only to authorized people.
- State changes are explicit, validated and auditable.
- Errors are safe, predictable and useful without revealing foreign records.
- The deployed system exposes only behavior proved by tests and smoke checks.

## Later AI-assisted journey

A mentor requests a draft question pack using a target role, experience level, topics,
difficulty, duration, question count and optional job description. Generation runs as a
bounded background job. The mentor reviews the draft before it becomes usable.

The model supplies content, not authority. Product behavior for this capability is
constrained by `docs/AI_FEATURE_BOUNDARY.md`.

## Validation MVP

The first deployable version includes authentication, availability, booking,
cancellation, role/object authorization, feedback and concurrency protection. A small
group can complete the core student and mentor journeys without developer intervention.

## Deferred

- Payments, subscriptions and marketplace behavior
- Video calling and recording
- Calendar synchronization
- Real email/SMS delivery
- Public mentor marketplace and ratings
- Automated interview scoring
- Resume parsing or candidate ranking
- Native mobile application

