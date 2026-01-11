# ADA — Workflow (GitHub-Native)

This document describes the end-to-end operational workflow for ADA: **how requirements become merged code** using GitHub as the single coordination surface.

This workflow references the canonical formats in:
- `ada/artifacts/templates/brief-template.txt`
- `ada/artifacts/templates/state-block.txt`

…and the GitHub UI layer in:
- `.github/ISSUE_TEMPLATE/` (issue forms)
- `.github/pull_request_template.md` (PR body)

---

## 1) GitHub Artifacts and How They Are Used

### Requirements (docs)
- Location: `ada/artifacts/project/requirements/`
- Format/rules: `ada/artifacts/project/requirements/README.md`
- HL extracts/normalizes atomic requirements into stable IDs: `REQ-001`, `REQ-002`, …

### ADRs (docs)
- Location: `ada/artifacts/project/adr/`
- ADR rules + template: `ada/artifacts/project/adr/README.md`
- Used for **long-lived/high-impact decisions** (vs lightweight decision issues)

### Issues (Epics / Tasks / Decisions)
Issue creation should use GitHub Issue Forms:
- Epic: `.github/ISSUE_TEMPLATE/epic.yml`
- Task: `.github/ISSUE_TEMPLATE/task.yml`
- Decision: `.github/ISSUE_TEMPLATE/decision.yml`

How they relate:
- **Epic** groups requirements and child tasks.
- **Task** is the LL unit of work (bounded, verifiable, ideally 1 PR).
- **Decision** records a choice; can be promoted to an ADR if long-lived/high-impact.

### Pull Requests
PR body should follow:
- `.github/pull_request_template.md`

Each PR should:
- reference the task issue (e.g., `Closes #123`)
- mention REQ-IDs covered (`REQ-…`)
- include how to test (commands/steps)
- include risk/rollback when relevant

### Project Board (Recommended)
Minimum columns:
`Intake → Decomposed → In Progress → Review → Done`

Suggested fields:
Priority, Area, Risk, Owner/Agent, Milestone/Release

---

## 2) Suggested Branch Strategy

```
main  (production-ready)
dev   (integration)
feature/*  (agent branches)
```

Flow:
1. LL creates `feature/<task-id>-<short-name>` from `dev`
2. Implement + tests
3. PR: `feature/* → dev`
4. Review and merge
5. Periodic release PR: `dev → main`

---

## 3) Operational Phases

### Phase 1 — Requirements Gathering
Actors: Human + HL

Steps:
1. Collect requirements into `ada/artifacts/project/requirements/`.
2. Normalize to atomic `REQ-###` IDs (stable).
3. Identify dependencies and priorities.

Output: versioned requirements documents.

### Phase 2 — Epic Decomposition
Actors: HL + Human

Steps:
1. Group requirements into epics.
2. Create epic issues using `epic.yml` and include:
   - covered REQ-IDs
   - scope in/out
   - Definition of Done
   - key risks/assumptions (link decisions/ADRs if needed)

Output: epic issues ready for task breakdown.

### Phase 3 — Task Breakdown
Actors: HL (human input only for blockers)

Steps:
1. Split epics into tasks that are small and reviewable (ideally 1 PR).
2. Create task issues using `task.yml` (mirrors `ada/artifacts/templates/brief-template.txt`).
3. Sequence dependencies and assign to LL agents.

Output: task issues ready to implement.

### Phase 4 — Implementation (per task)
Actors: LL

Steps:
1. Treat the task issue as the contract.
2. Implement minimal change that satisfies acceptance criteria.
3. Add/adjust tests required by the task.
4. Open PR and follow `.github/pull_request_template.md`.

Output: PR ready for review.

### Phase 5 — Review & Integration
Actors: Human + HL

Review checklist:
- acceptance criteria met
- tests included and passing (or commands provided)
- traceability intact (REQ/issue links)
- security basics addressed (no secrets; validate untrusted input where applicable)
- no scope creep / unnecessary refactors
- rollback/rollout notes included if risky

Output: merged PR, closed task issue.

### Phase 6 — Release
Actors: Human + HL

Steps:
1. Validate epic Definition of Done.
2. Run integration/e2e checks as appropriate.
3. Merge `dev → main` (or equivalent).
4. Close epic, document release notes if needed.

Output: release delivered.

---

## 4) Quality Gates (Applied at Task Definition and PR Review)

### Testing
- Each task specifies required test types (unit/integration/e2e).
- PRs include tests for new/changed behavior and edge cases.

### Security
- No secrets in code/logs.
- Validate/escape untrusted input where applicable.
- Be explicit about authn/authz changes.

### Observability (when applicable)
For I/O or service-like changes:
- clear error handling
- sensible logging
- add metrics/tracing only when required or clearly beneficial

### Documentation
Update docs when setup, APIs, or behavior changes in a user-facing way.
