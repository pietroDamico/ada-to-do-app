# ADA — Agent-Driven Development
## Methodology Overview

ADA (Agent-Driven Development) is a structured workflow where AI agents collaborate under **human oversight** to deliver software that is **traceable**, **reviewable**, and **verifiably correct**.

ADA uses a **hierarchical coordination model**:
- A **High-Level (HL) Agent** partners with a human to turn requirements into a plan (epics, tasks, dependencies, acceptance criteria).
- One or more **Low-Level (LL) Agents** implement individual tasks autonomously, producing small PRs that are easy to review.
- **GitHub** is the single source of truth for planning, execution, review, and history.

---

## Core Principles

### 1) Traceability First
Every change must trace back to a requirement or an explicitly documented rationale.

**Chain**: `Code → PR → Task → Epic → Requirement → (ADR, when needed)`

No “orphan work” without justification.

### 2) Explicit Over Implicit
Write down what matters:
- acceptance criteria (observable outcomes)
- risks and mitigations
- dependencies
- test requirements

### 3) Verifiable Completion
“Done” must be objectively verifiable (tests, checklists, reproducible steps), not subjective (“looks good”).

### 4) Atomic Work Units
Prefer: **one task → one PR** with a clear outcome. Split work if a task risks becoming multi-PR or ambiguous.

### 5) Quality Gates Are Mandatory
Testing, security, and (where relevant) observability are part of the work definition, not afterthoughts.

### 6) GitHub as Source of Truth
Planning and coordination happen through GitHub artifacts (issues, PRs, project board) plus versioned docs under `ada/artifacts/`.

---

## Roles and Responsibilities

### HL Agent — Orchestrator
Owns:
- requirement parsing and stable IDs (`REQ-###`)
- epic/task decomposition
- acceptance criteria and test expectations
- dependency mapping and sequencing
- integration-level review (consistency, risks, traceability)

HL prompt (canonical):
- `prompts/hl/prompt.md`

### LL Agent — Implementer
Owns:
- implementing a single task within scope
- adding/adjusting tests required by the task
- producing a PR with clean diffs and clear verification steps
- asking questions **only** when blocked

LL prompt (canonical):
- `prompts/ll/prompt.md`

### Human — Decision & Quality Authority
Owns:
- product priorities and final decisions
- resolving ambiguities when flagged
- approving PRs (or rejecting and requesting changes)
- intervening when quality gates or scope boundaries are violated

---

## Repository Map (What lives where)

### Methodology (reusable)
- `ada/artifacts/methodology/overview.md` — what ADA is and how it works
- `ada/artifacts/methodology/workflow.md` — operational flow (GitHub-native)
- `ada/artifacts/methodology/token-efficiency.md` — how to reduce token usage safely

### Canonical formats (“spec”)
These define the *canonical* shape of status and task briefs. Agents must reference them and avoid reprinting them.
- `ada/artifacts/templates/state-block.txt`
- `ada/artifacts/templates/brief-template.txt`

### Project knowledge (project-specific)
- Requirements:
  - `ada/artifacts/project/requirements/README.md` (format + rules)
  - additional requirement files in the same folder
- ADRs:
  - `ada/artifacts/project/adr/README.md` (how to write ADRs)
  - ADR files: `ada/artifacts/project/adr/NNNN-*.md`

### GitHub UI layer (enforcement)
These are the “data-entry UI” forms/templates used on GitHub.
- Issue forms: `.github/ISSUE_TEMPLATE/`
  - `epic.yml` — create epics
  - `task.yml` — create tasks (LL work units)
  - `decision.yml` — record decisions (may be promoted to ADRs)
- PR template:
  - `.github/pull_request_template.md`

---

## Quick Start (New Project)
1. Initialize agents using:
   - HL: `prompts/hl/prompt.md`
   - LL: `prompts/ll/prompt.md`
2. Write/import requirements under `ada/artifacts/project/requirements/` following `README.md`.
3. HL creates epics and tasks as GitHub issues using `.github/ISSUE_TEMPLATE/`.
4. LL implements tasks and opens PRs following `.github/pull_request_template.md`.
5. Human + HL review and merge; iterate with updated requirements and decisions/ADRs.

---

## When to Use ADA (and when not to)
ADA works best when:
- you want parallel execution with predictable quality
- you need auditability (“why does this code exist?”)
- requirements are evolving and you want controlled iteration

ADA may be overkill when:
- the change is extremely small (single-file trivial tweak)
- you cannot afford human review cycles (quality will drift)

In those cases, use a lighter version: tasks only (skip epics), or manual dev.
