# Architecture Decision Records (ADR)

This folder contains **Architecture Decision Records**: short documents that capture
**important decisions** about architecture, technology, constraints, or process that
would otherwise be forgotten and re-debated.

ADRs are part of ADA’s traceability chain:
`Code → PR → Issue/Task → Epic → Requirement → ADR (when needed)`

---

## Why ADRs exist

ADRs prevent:
- repeated discussions (“why did we choose X?”)
- inconsistent implementations across tasks/agents
- hidden assumptions that cause rework

They make decisions **auditable** and **stable**, while still allowing change over time
(via superseding ADRs).

---

## What should become an ADR

Create an ADR when a decision is:
- **high-impact** (affects many modules/teams/tasks)
- **hard to reverse** (data model, persistence, protocol, public API)
- **risky** (security, compliance, reliability)
- **non-obvious** (multiple plausible options, trade-offs)
- likely to be questioned later (onboarding, reviewers, future you)

Do **not** create an ADR for:
- trivial refactors
- purely local implementation details
- decisions that are already fully specified by requirements and have no meaningful alternatives

---

## Relationship to State Block "Decisions"

The project may track lightweight decisions in the **State Block** (e.g., `D-001`).
Use that for fast alignment.

Promote a Decision to an ADR when it becomes:
- long-lived,
- high-impact, or
- needs deeper rationale/trade-offs.

When promoted:
- reference the ADR from the State Block decision entry.

---

## File naming and location

ADRs live in `ada/artifacts/adr/` and use this naming scheme:

- `NNNN-short-title.md`
  - `NNNN` is a zero-padded integer: `0001`, `0002`, ...
  - `short-title` is lowercase, hyphen-separated

Example:
- `0003-api-auth-strategy.md`

---

## ADR status lifecycle

Use one of these statuses:
- **Proposed**: drafted, not yet accepted
- **Accepted**: approved and active
- **Deprecated**: no longer recommended (but not replaced by a specific ADR)
- **Superseded**: replaced by another ADR (link to it)

A new ADR can supersede an old one; do not rewrite history—link it.

---

## How ADRs are created and maintained

1. Draft ADR as **Proposed**
2. Review via PR (or explicit approval in the related issue)
3. Mark as **Accepted**
4. Link it from:
   - the relevant Epic/Task issues, and/or
   - the PR description
5. If a decision changes later, create a new ADR and mark the old one **Superseded**

---

## ADR Template (copy/paste)

Create a new file `ada/artifacts/adr/NNNN-short-title.md` with:

```md
# ADR NNNN: <Title>

- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Date**: YYYY-MM-DD
- **Decision ID**: D-### (optional, if tracked in State Block)
- **Context**: links to Epic/Task/REQ (optional but recommended)
  - Epic: E-###
  - Task(s): #123, #124
  - Requirements: REQ-###, REQ-###

## Context
What problem are we solving? What constraints matter (time, security, platform, scale, team)?

## Decision
What we decided, stated clearly and concisely.

## Alternatives considered
List up to 2–4 alternatives with brief trade-offs.

## Consequences
- Positive: what we gain
- Negative: what we accept / risk
- Follow-ups: migrations, deprecations, documentation, etc.

## Notes
Anything that helps future readers (links, references, benchmarks).

