# PeerMock Project Guidance

## Documentation ownership

- Read `.codex/notepad.md` at the start of a new or resumed session for the active
  checkpoint, verified evidence and exact restart point.
- Read `.codex/plans/project-tracker.md` before starting project work. It is the sole
  authority for execution order, active episode and completion gates.
- Read `PRODUCT.md` for product behavior, `PROJECT_BLUEPRINT.md` for capability scope,
  `ARCHITECTURE.md` for technical boundaries, `PROJECT_STRUCTURE.md` for module
  ownership and `PRODUCTION.md` for deployment/release requirements.
- Read `GUIDED_BUILD.md` when the active tracker episode has a learning mission.
- Read `docs/SECURITY_LEARNING_MAP.md` when selecting HTB study, Cyber Vault reading,
  security tools or lab evidence for an episode. The tracker still controls
  implementation order.
- Choose a security tool only after the active feature, failure or threat creates a
  concrete question. Tool installation and scanner output are not episode-completion
  evidence by themselves.
- Read `docs/AI_FEATURE_BOUNDARY.md` only when the tracker reaches the AI question-pack
  season or when reviewing that boundary.
- Keep durable operating rules here and changing progress in `.codex/notepad.md`.

## Session continuity

- At the start of episode work, report the season and episode, previous verified state,
  today's task, completion condition and narrow verification command.
- Preserve tracker order and scope unless the user explicitly changes them.
- Mark an episode complete only after inspecting the saved work and confirming its
  verification and finale gate.
- Inspect Git status and the current branch before edits or Git guidance. Preserve
  user-authored and unrelated changes.
- At a pause or handoff, update `.codex/notepad.md` with evidence and the exact restart.

## Guided Build

- Treat `next`, `nxt`, `continue` and similar requests as requests to present the next
  learning task only. State the filename, goal, requirements, completion condition and
  one small hint without editing files or providing code.
- Edit project files or provide code snippets only when the user's current message
  explicitly asks for that action. Permission from an earlier task does not carry into a
  later episode or task. When permission is absent, let the learner implement first.
- Exception for tests: when assigning a test-case task, provide the complete test snippet
  immediately and explain its Arrange, Act and Assert sections. The learner saves it;
  this exception does not authorize Codex to edit the test file.
- Codex handles read-only inspection and routine test/lint/type commands. Ask before
  applying mechanical file repairs unless the user explicitly requested implementation.
- Assume the learner's interactive shell already has the project `.venv` activated.
  Commands shown to the learner should use `python`, `pytest`, `alembic`, `ruff` and
  `mypy` directly without `.venv/bin/` prefixes or repeated activation instructions.

- For backend feature logic, give the exact filename, goal, requirements and a small hint,
  then let the learner implement the first attempt. Do not show finished production code
  until the learner explicitly asks to see it.
- For test cases, provide the complete test code directly and explain its Arrange, Act
  and Assert sections; the learner does not need to attempt test code first.
- Review the saved attempt, explain exact mistakes and edge cases, then run the narrowest
  meaningful verification.
- Explain each newly introduced library, decorator, type and pattern, including the
  consequence of misuse.
- Every step records explain, predict, attempt, observe, repair and retest evidence in
  `docs/LAB_JOURNAL.md`.
- For security-linked episodes, use the same evidence ID in the Cyber Vault and PeerMock
  lab journals. Reading or module completion counts as study, not applied proof.
- At episode start, name at most one primary HTB module or section and one primary tool
  question. Supporting study blocks a finale only when the security learning map marks
  it **Core before finale**.

## Boundaries

- Keep PeerMock a modular monolith. Routers translate HTTP; feature services own business
  rules; persistence code owns queries and transactions.
- Derive identity from validated authentication. Database queries enforce ownership;
  client-supplied IDs are never proof of access.
- PostgreSQL provides the final booking-consistency guarantee. Demonstrate the race
  before choosing the locking or constraint strategy.
- The LLM produces schema-validated draft content after the core backend is complete. It
  never controls identity, authorization, booking state or question-pack visibility.
- Keep Redis, Celery, frontend and LLM dependencies out of core seasons until the tracker
  activates them.

## Testing and delivery

- Tests protect user-visible behavior, authorization boundaries, data integrity or a
  demonstrated regression. Prefer service and vertical behavior over implementation
  mirroring.
- Every security repair keeps a failing-before/passing-after regression test plus a
  legitimate-use control.
- The user performs commits, pushes, pull requests and merges unless explicitly asking
  Codex to do them.
- Before recommending a commit, run the active episode checks, inspect the diff and check
  for accidental files or secrets.
