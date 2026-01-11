# Requirements

This folder contains the **project requirements** used by ADA to drive planning and implementation.

In ADA, requirements are the top-level source of truth for *what the system must do*.
Everything else should trace back to them:

`Code → PR → Task → Epic → Requirement`

---

## What belongs here

Put requirements here when they describe:
- product behavior (features, workflows, APIs)
- non-functional constraints (security, performance, reliability, compliance)
- operational constraints (deployment, observability, data retention)
- acceptance/verification expectations (how we prove it works)

Do **not** put here:
- architecture choices and trade-offs → use ADRs in `ada/artifacts/project/adr/`
- task plans or implementation notes → use GitHub Issues/PRs

---

## How requirements are written

Requirements must be:
- **atomic** (one requirement = one testable claim)
- **stable** (do not rewrite history; evolve via versioned changes)
- **verifiable** (each requirement must have a clear verification approach)

### Requirement IDs (mandatory)
Use stable IDs:

- `REQ-001`, `REQ-002`, ...

Rules:
- IDs are never reused.
- Do not renumber existing requirements.
- If a requirement is removed, mark it as **Deprecated** (do not delete silently).

---

## Recommended format (per requirement)

Use this template (in any requirements document in this folder):

```text
REQ-###: <short title>
Status: Proposed | Accepted | Deprecated | Superseded
Priority: P0 | P1 | P2
Type: Functional | Non-Functional
Description: <one sentence, clear and specific>
Rationale: <why it matters, optional but useful>
Dependencies: REQ-###, ADR-#### (optional)
Verification: <how we prove it; test type, scenario, measurable condition>
Notes: <optional>

