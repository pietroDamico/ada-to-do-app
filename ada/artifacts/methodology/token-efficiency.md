# ADA — Token Efficiency (HL/LL)

This document defines how ADA reduces token usage **without** sacrificing traceability or quality.
The goal is to avoid paying the same “context cost” repeatedly.

---

## Canonical Templates (Spec) vs GitHub Forms (UI)

### Canonical formats (spec)
These define the canonical shape of status and task briefs:
- State Block format: `ada/artifacts/templates/state-block.txt`
- Task Brief / Issue format: `ada/artifacts/templates/brief-template.txt`

**Rule**: agents must not reprint these templates in chat. They should reference them by path and output only:
- filled-in instances (for new issues), or
- deltas (ADDED/UPDATED/REMOVED) for state updates.

### GitHub Issue Forms (UI)
These are the GitHub “data entry” layer used to create consistent issues:
- `.github/ISSUE_TEMPLATE/epic.yml`
- `.github/ISSUE_TEMPLATE/task.yml`
- `.github/ISSUE_TEMPLATE/decision.yml`

They should mirror the canonical formats in `ada/artifacts/templates/` and reduce drift by making fields explicit and (where possible) required.

---

## Key Principles

### 1) Reference, Don’t Reprint
Avoid restating long policies, templates, or repeated context.
Prefer:
- file paths
- issue/PR links
- IDs (`REQ-…`, `E-…`, `TSK-…`, `D-…`)

### 2) Delta-First Communication
When updating plans or task lists, output only what changed:
- **ADDED**: new epic/task/decision
- **UPDATED**: changed ACs, scope, deps, status
- **REMOVED**: dropped items or de-scoped work

Default response style:
- `STATE unchanged.`
- then deltas.

### 3) Just-in-Time Decomposition
Do not fully decompose the entire project upfront.
Instead:
- keep **3–7 ready-to-implement tasks** per epic
- generate more tasks only when the “ready queue” is low or after new info appears

### 4) Question Hygiene (Minimize Loops)
If questions are needed:
- ask **only blockers**
- ask them **once**, as a minimal list
- otherwise proceed with explicit assumptions (max 3)

---

## The State Block

### What it is
A State Block is a compact shared “status snapshot” of:
- active epics and tasks
- owners/agents
- dependencies and risks
- next actions
- (optionally) a short list of decisions that prevent repeated debates

Canonical format: `ada/artifacts/templates/state-block.txt`.

### Decisions vs ADRs
- Use a lightweight **Decision** (issue created with `decision.yml`) for fast alignment.
- Promote to an ADR in `ada/artifacts/project/adr/` when the decision is long-lived, high-impact, or needs deeper trade-offs.

### When to print the full State Block (Mandatory)
Print the **full** State Block only:
1) at the start of a new working session, OR
2) after a structural plan change (new/removed epic, major re-decomposition, milestone/priority changes), OR
3) when multiple agents are active and confusion/duplication risk is present.

Otherwise:
- do not print it
- write: **“STATE unchanged.”** and output deltas only.

---

## Task Brief: Keep it Short but Verifiable
For each task issue:
- 1-sentence goal
- scope IN/OUT (small)
- 4–7 verifiable acceptance criteria
- tests to add/adjust
- expected files to touch

Avoid narrative context; link to docs instead.

Canonical format: `ada/artifacts/templates/brief-template.txt`.
GitHub UI for tasks: `.github/ISSUE_TEMPLATE/task.yml`.

---

## Option Limits and Escalation
When presenting alternatives:
- ≤3 options
- ≤2 trade-offs per option
- always recommend a default

If progress loops:
- stop and emit a **Decision Point**:
  - what is blocked
  - minimum missing info
  - options + trade-offs
  - recommended default
  - next actions

---

## Token Budget Labels (Optional but Useful)
Use a simple label per epic/task: **S / M / L**
- S: compact outputs only
- M: allow short explanations
- L: allow deeper reasoning, but still avoid reprinting templates/policies

If a budget is exceeded without convergence:
- escalate with a Decision Point instead of continuing the loop.
