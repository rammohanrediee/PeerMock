# PeerMock Security Learning Bridge

## Purpose

This map connects each PeerMock season to relevant HTB study, Cyber Vault reading,
authorized lab practice, security tools and project evidence. HTB supplies attacker
perspective; PeerMock supplies the engineering application. Finishing a module or
running a scanner is not evidence that PeerMock is secure.

The project tracker remains the authority for implementation order and completion. The
Cyber Vault roadmap remains the authority for the overall HTB path order. This file owns
only the bridge between them.

## Cyber Vault

Vault name: `Obsidian Vault`

Primary references:

- [Project-driven skills and security tools](obsidian://open?vault=Obsidian%20Vault&file=Cyber%2F01%20Roadmap%2FProject-Driven%20Skills%20and%20Security%20Tools)
- [HTB path selection](obsidian://open?vault=Obsidian%20Vault&file=Cyber%2F01%20Roadmap%2FHTB%20Path%20Selection%20-%20Secure%20AI%20and%20Backend%20Engineering)
- [Cybersecurity and AI Security knowledge map](obsidian://open?vault=Obsidian%20Vault&file=Cyber%2F01%20Roadmap%2FCybersecurity%20and%20AI%20Security%20-%20Knowledge%20Map)
- [Cyber Vault lab journal](obsidian://open?vault=Obsidian%20Vault&file=Cyber%2F04%20Labs%2FLab%20Journal)
- [Five-project learning path](obsidian://open?vault=Obsidian%20Vault&file=Cyber%2F05%20Projects%2F00%20Projects%20-%20Learning%20Path)

If an Obsidian link does not open, search the vault using the displayed note title. Do
not copy the Cyber Vault into this repository or commit personal vault content.

## Learning-to-engineering loop

For a security-linked episode:

1. Study only the HTB sections needed for the active behavior.
2. Read the linked Cyber Vault note and explain the concept without copying it.
3. Practise only on an assigned platform target or an isolated system you own, using
   synthetic identities, data and credentials.
4. Apply one concrete test, control or design decision to PeerMock.
5. Use one evidence ID such as `PM-S3E4-2026-09-16` in both journals:
   - the Cyber Vault lab journal records the learning source, lab reasoning, assistance
     used and raw sanitized observations;
   - `docs/LAB_JOURNAL.md` records the PeerMock prediction, implementation,
     verification, repair and remaining risk.
6. Retest both the attack or failure case and a legitimate-use control before claiming
   the property is proved.

Use honest status words: `planned`, `read`, `attempted`, `applied` and `proved`. An HTB
completion badge does not automatically become `applied` or `proved`.

## Time, scope and tool rules

- Keep roughly 80% of project-learning time on building, debugging and verification and
  20% on HTB/security study, unless an active security gap needs focused practice.
- Keep one active HTB module at a time.
- Supporting study does not block unrelated backend work.
- A module becomes a season gate only where this map says **Core before finale**. The
  gate is explain-and-apply evidence, not the badge.
- Do not add Redis, Celery, LLMs or offensive tooling before the tracker activates the
  behavior that needs them.
- Choose a tool by question: state what it should reveal, its authorized scope, what
  output counts as evidence and what it cannot prove. Prefer the smallest tool that
  answers the question.
- At episode start, select at most one primary module or section and one primary tool.
  Add another only when the first result creates a specific follow-up question.
- Run active testing only against HTB targets, isolated local labs or systems the user
  owns and has authorized for the stated scope.

## Season summary

| Season | HTB focus | Tool trigger | PeerMock evidence |
|---|---|---|---|
| 0 — Foundation | Linux reinforcement; Bash as needed | Shell/environment inspection and pytest | Reproducible commands and safe configuration |
| 1 — Domain/persistence | Web/request concepts only when useful | PostgreSQL, Alembic and schema inspection | Permission model and database invariants |
| 2 — Booking API | Web Requests; Introduction to Web Applications | `curl` for exact allowed/rejected requests | Requests traced through validation, service and persistence |
| 3 — Identity/authorization | Web Proxies; Broken Authentication; Web Attacks; API authorization | Burp Community against local PeerMock | Modified-token/identifier tests plus legitimate controls |
| 4 — Concurrency | API business-logic lessons as needed | Controlled pytest concurrency and PostgreSQL inspection | Repeatable race and database-backed repair |
| 5 — Delivery | Information Gathering; selective Nmap and Linux privilege review | Logs, process inspection and scoped Nmap | Exposure, service identity and deployment evidence |
| 6 — Background work | File Upload Attacks; API Attacks; conditional command/path study | Worker interruption and correlated logs | Malformed, oversized, replayed, interrupted and foreign-job tests |
| 7 — Security review | SQL Injection; Web Fuzzing; assessment/reporting | Burp, Nmap, ffuf, Semgrep, `pip-audit`, Gitleaks and Trivy, each scoped to one question | Findings with repair, regression and legitimate-use controls |
| 8 — AI question packs | Selected AI Red Teamer modules | Versioned manual evals; Promptfoo or Garak only after cases stabilize | Repeated hostile/normal evaluations with authority outside the model |

## Season 0 — Reproducible foundation

**HTB:** Reuse `Linux Fundamentals`; use `Introduction to Bash Scripting` only for a
specific automation gap. There is no offensive-module gate.

**Apply:** Explain the virtual environment, package import path, environment variables,
ignored secret files and command exit status. Record the exact fresh-install and
narrow-test result. Networking study must not delay foundation work.

**Evidence gate:** A fresh environment installs PeerMock and runs its documented checks.

## Season 1 — Domain and persistence

**HTB:** Begin or reuse `Introduction to Web Applications` and `Web Requests` when they
help explain trust boundaries. No offensive module is required before modelling.

**Apply:** Identify assets, identities, ownership boundaries, attacker-controlled
identifiers and database invariants before writing routes. For every important
relationship, predict an invalid row the database should reject.

**Evidence gate:** The permission matrix and invariants are recorded, and invalid
relationships are rejected by PostgreSQL for the expected reason.

## Season 2 — Availability and booking API

**HTB — Core before finale:** Relevant parts of `Web Requests` and `Introduction to Web
Applications`: methods, paths, headers, bodies, status codes, cookies or tokens, and the
browser/API/database boundary.

**Tool question:** Use `curl` to inspect the exact request and response for one valid
create/list/book/cancel journey and validation, not-found and conflict failures. Mark
every user-controlled field and trace where validation, business rules and persistence
act on it.

**Evidence gate:** Sanitized request/response evidence plus tests whose expected status
and error contracts the learner can explain.

## Season 3 — Identity and authorization

**HTB — Core before finale:** Relevant parts of `Using Web Proxies`, `Broken
Authentication`, `Web Attacks` and the object/function authorization material in `API
Attacks`. Study `Session Security` after the token or session lifecycle exists.

**Tool question:** Through Burp Community against local PeerMock, replay a legitimate
request and change one identity, role, slot, booking or feedback identifier at a time.
Test missing, invalid and expired credentials. Retain the equivalent legitimate request
as a control for every denied request.

**Evidence gate:** Cross-identity tests prove that client-supplied identifiers never
establish authority and sensitive foreign objects do not leak through responses.

## Season 4 — Concurrency and consistency

**HTB:** Reuse business-logic and resource-control lessons from `API Attacks` as needed.
HTB does not replace learning PostgreSQL transactions, isolation, locking and
constraints.

**Tool question:** Use controlled concurrent tests and PostgreSQL inspection to predict
and reproduce the unsafe read-then-write interleaving before implementing its repair.

**Evidence gate:** The test demonstrates the race before repair and repeatedly proves at
most one active booking afterward, with cancellation/retry as a valid control.

## Season 5 — Evidence and validation release

**HTB:** Relevant parts of `Information Gathering - Web Edition`, `Network Enumeration
with Nmap` for an owned deployment, and Linux privilege material covering service
identity, writable paths, secrets and unnecessary privilege.

**Tool question:** Inventory intended routes and listening services, inspect the runtime
account and dependencies, then use narrowly scoped Nmap only when it answers a stated
exposure question. Verify results manually.

**Evidence gate:** The deployment has an evidence-backed exposure and least-privilege
review, sanitized decision logs and separate-role smoke tests.

## Season 6 — Reliable background work

**HTB — Core before finale:** Relevant parts of `File Upload Attacks` and `API Attacks`.
Use `Command Injections` only if processing invokes an external command, and `File
Inclusion` only if user-controlled names or paths affect storage or reading.

**Tool question:** Trace a job through correlated logs, then interrupt a worker and
verify recovery. Test malformed encoding or rows, oversized inputs, duplicate/replayed
submission, retry exhaustion and access to another user's job, source or result. Add a
load tool only when a concrete capacity question requires it.

**Evidence gate:** Replay and interruption cause neither duplicates nor silent loss;
foreign users cannot access artifacts; malformed or oversized inputs fail predictably;
normal work still succeeds.

## Season 7 — Security review and recovery

**HTB — Core before finale:** `SQL Injection Fundamentals`, selected `Web Fuzzing`,
`Penetration Testing Process` and `Documentation & Reporting`. Use `Vulnerability
Assessment` to learn that scanner output is a lead, not proof. Reapply relevant earlier
modules instead of collecting unrelated ones.

**Tool questions:** Start with manual requests or Burp for behavioral proof. Introduce
tools only for a named review question:

- Semgrep: which source patterns deserve manual review?
- Gitleaks: does Git history or the worktree contain likely secrets?
- Trivy: which dependency, image or configuration findings apply to the deployed stack?
- `pip-audit`: do installed Python packages have relevant published advisories?
- Nmap: which services are reachable on the explicitly authorized target?
- ffuf: which routes or parameters are exposed on the explicitly authorized target?

Every result needs manual validation, scope, impact and a limitation statement.

**Evidence gate:** Each accepted finding records scope, reproduction, attacker-controlled
input, missing control, impact, repair, same-attack retest, legitimate-use control and
residual risk. A restored isolated database supports core journeys.

## Season 8 — Controlled AI question packs

**HTB — Core in dependency order:** Use prerequisite AI fundamentals only for a
demonstrated gap, then relevant sections from `Introduction to Red Teaming AI`, `Prompt
Injection Attacks`, `LLM Output Attacks`, `Attacking AI - Application and System`, `AI
Data Attacks`, `AI Privacy` and `AI Defense` as the implemented boundary requires.

**Tool question:** Build manual, versioned normal and hostile evaluation cases while the
adapter, optional retrieval inputs and authorization boundary are implemented. Stabilize
their inputs, expected outcomes and repetition policy before introducing Promptfoo or
Garak. Automation scales known cases; it does not define the security boundary.

**Apply:** Test direct and indirect prompt injection separately, malformed output,
unauthorized source material, replay, timeout, resource exhaustion, premature draft
visibility and any future tool argument. Authorization, booking state, visibility and
approval remain enforced outside the model.

**Evidence gate:** Hostile content cannot change identity, authorization, booking state
or question-pack visibility; malformed output is rejected; authorized normal use and a
manual fallback remain available.

## Episode prompts

At the start of a relevant episode, report:

- active season and episode;
- backend behavior being built;
- one supporting HTB module or section, or `No study prerequisite`;
- one tool-backed question, or `No tool needed yet`;
- authorized lab or PeerMock test;
- shared evidence ID and exact proof required.

At completion, answer:

- What did the attacker or failure control?
- Which boundary was verified or missing?
- What did the real output show?
- Which application control enforces the property?
- Does the same attack now fail?
- Does legitimate use still work?
- What remains unproved?
