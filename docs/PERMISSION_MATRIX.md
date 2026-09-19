# Permission Matrix

This document defines the first-release authorization policy. Authentication resolves
the caller; the service then applies role, ownership, assignment and state conditions.
Client-supplied identifiers never establish authority.

## Role decisions

- Each account has exactly one fixed role: student, mentor or coordinator.
- A student acts only for themself. There is no booking on another student's behalf.
- A mentor acts only on their own slots and interviews assigned through those slots.
- A coordinator receives operational schedule visibility, not blanket access to private
  bookings, feedback or mentor-owned mutations.
- Visitors cannot access the scheduling API. Public discovery can be designed later as
  a separate, deliberately limited surface.

## Core permissions

`Allow` always includes valid authentication, valid input and the stated ownership or
state condition. Access to a foreign private object returns the same safe not-found
result as an absent object.

| Operation | Visitor | Owning student | Other student | Assigned mentor | Other mentor | Coordinator |
|---|---|---|---|---|---|---|
| List available slots | Deny | Allow | Allow | Allow | Allow | Allow |
| View one slot | Deny | Allow | Allow | Allow | Allow | Allow |
| Create mentor availability | Deny | Deny | Deny | Allow — create for self | Deny — cannot create for another mentor | Deny — no impersonated mentor action |
| Update an available slot | Deny | Deny | Deny | Allow — own future, unbooked slot | Deny | Deny |
| Withdraw a slot | Deny | Deny | Deny | Allow — own future slot | Deny | Deny |
| Book a slot | Deny | Allow — create own booking | Deny — cannot book for another student | Deny | Deny | Deny |
| View a booking | Deny | Allow — own booking | Deny | Allow — booking for own slot | Deny | Allow — operational projection only |
| Cancel a booking directly | Deny | Allow — own confirmed booking before start | Deny | Deny — use slot withdrawal when necessary | Deny | Deny |
| Mark interview completed | Deny | Deny | Deny | Allow — own confirmed interview after its end | Deny | Deny |
| Mark student no-show | Deny | Deny | Deny | Allow — own confirmed interview after its end | Deny | Deny |
| Submit or edit feedback | Deny | Deny | Deny | Allow — own completed interview, before release | Deny | Deny |
| Release feedback | Deny | Deny | Deny | Allow — own complete draft, once | Deny | Deny |
| Read feedback | Deny | Allow — own released feedback | Deny | Allow — feedback for own assigned interview | Deny | Deny |
| Generate a question-pack draft | Later | Later | Later | Later | Later | Later |
| Approve a question pack | Later | Later | Later | Later | Later | Later |

The coordinator's booking projection contains only fields needed for event operations,
such as identifiers, schedule, topic and status. It excludes feedback content,
credentials and unrelated student profile data. A broader coordinator capability
requires a new explicit policy decision and test.

## Lifecycle decisions

### Slot lifecycle

Persisted states: `AVAILABLE`, `BOOKED`, `COMPLETED`, `CANCELLED`.

- Creating valid future mentor availability creates an `AVAILABLE` slot.
- Confirming its first booking changes `AVAILABLE -> BOOKED` atomically.
- Student cancellation before `starts_at` changes `BOOKED -> AVAILABLE` and the booking
  to `CANCELLED` atomically.
- Mentor withdrawal changes an owned `AVAILABLE -> CANCELLED`.
- Mentor withdrawal of an owned booked slot changes `BOOKED -> CANCELLED` and its
  confirmed booking to `CANCELLED` atomically. It never reopens that slot.
- Marking the interview completed changes `BOOKED -> COMPLETED` and the booking to
  `COMPLETED` atomically.
- Marking a no-show changes the booking to `NO_SHOW` and the slot to `COMPLETED`; the
  elapsed slot is not made available again.
- A booked slot cannot be directly deleted or rescheduled.
- A slot is offered for booking only when its status is `AVAILABLE` and its start time
  is still in the future. An elapsed unbooked slot is excluded by time even if no cleanup
  job has changed its stored status.

### Booking lifecycle

Persisted states: `CONFIRMED`, `CANCELLED`, `COMPLETED`, `NO_SHOW`.

- A successful booking starts as `CONFIRMED`.
- `CONFIRMED -> CANCELLED` occurs through an allowed student cancellation or the assigned
  mentor withdrawing the slot.
- `CONFIRMED -> COMPLETED` occurs only when the assigned mentor completes the interview
  after the scheduled end.
- `CONFIRMED -> NO_SHOW` occurs only when the assigned mentor records the student's
  absence after the scheduled end.
- Terminal bookings are retained as history and cannot transition again.

### Feedback lifecycle

- Only the mentor assigned through the booking's slot may create feedback.
- Feedback is allowed only for a `COMPLETED` booking, not for a `NO_SHOW` booking.
- The mentor may save and edit one private draft per booking while `released_at` is null.
- Release is an explicit, one-way action that sets `released_at`.
- Released feedback is immutable in the first release and visible to its owning student.
- Coordinators never receive feedback content.

## Core invariants

1. Each user has exactly one persisted role for the first release.
2. Each slot belongs to exactly one existing mentor; service logic verifies that the
   referenced user has the mentor role.
3. Each booking belongs to exactly one existing student and one existing slot; service
   logic verifies that the referenced user has the student role.
4. A slot has at most one active `CONFIRMED` booking. PostgreSQL supplies the final
   concurrent guarantee selected in Season 4.
5. A student cannot hold overlapping `CONFIRMED` bookings.
6. A mentor can manage only their own slots and interviews assigned through those slots.
7. Feedback has exactly one booking and its mentor must match the mentor who owns the
   booked slot.
8. A student can read only their own feedback and only after explicit release.
9. A coordinator can inspect limited operational scheduling data but cannot read
   feedback or act as a student or mentor.
10. Cancellation, completion, no-show and release are explicit state transitions;
    retained history is not physically deleted.
11. Caller identity always comes from validated authentication, never a request body,
    query parameter or path identifier.
12. Queries for private records include ownership or assignment predicates so absent
    and foreign objects produce the same safe result.

## Deferred decisions

- Multiple roles for one account
- Public slot discovery
- Coordinator-created events and delegated mentor scheduling
- Administrative overrides or dispute correction after terminal transitions
- Question-pack visibility and approval, which are defined in Season 8
