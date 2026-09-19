# LLM Question-Generation Boundary

This is a later milestone. Do not implement it before the core Project 2 completion
gate in `GUIDED_BUILD.md`.

## Purpose

Generate a **draft** mock-interview question pack from validated requirements. A mentor
reviews the draft before it is used. The LLM is a content generator, not an authority.

## Allowed user inputs

- target role;
- experience level;
- interview type;
- selected topics;
- difficulty;
- duration;
- bounded question count;
- optional, length-limited job description.

The job description and every free-text field are untrusted content.

## Expected structured output

Each draft question should contain server-validated fields such as:

- question text;
- category;
- difficulty;
- expected concepts;
- optional follow-up;
- evaluation rubric;
- suggested time.

The exact schema is a later design decision. Model output must not be written directly
to trusted state without parsing and validation.

## Non-negotiable boundaries

The server—not the model—decides:

- authenticated identity;
- who can create, read, edit or approve a question pack;
- which interview owns the pack;
- question-count and input-size limits;
- token, retry, timeout and per-user usage budgets;
- booking or interview state;
- what is stored and logged.

The model receives no authentication tokens, database credentials, unrelated feedback
or other users' private data.

## Failure behavior

- Run generation outside the booking transaction.
- Use bounded retries; never retry indefinitely.
- Reject output that does not match the server schema.
- Keep a failed job observable without leaking prompt content.
- Allow the mentor to write questions manually when generation is unavailable.

## Security tests to plan later

- prompt injection inside the optional job description;
- attempts to request another user's question pack;
- oversized inputs or excessive question counts;
- malformed model output;
- timeout and provider failure;
- repeated/replayed generation requests;
- access before mentor approval;
- sensitive content appearing in logs.

Passing one hostile prompt does not prove prompt-injection safety. Authorization must
remain correct even when generated content is malicious or incorrect.

