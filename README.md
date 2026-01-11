# ADA — Agent-Driven Development (GitHub Template)

This repository is a **template** for running projects with **ADA (Agent‑Driven Development)**: a practical workflow where a **High-Level (HL) agent** plans and coordinates work, and **Low-Level (LL) agents** implement bounded tasks, with a human acting as final decision-maker and reviewer.

This repo is designed to be used as a **GitHub template** to bootstrap a new project repo with the full ADA workflow preinstalled.

---

## What you get

- **Agent prompts** (HL + LL) you can copy into your agents
- **Canonical templates** (State Block + Task Brief) to standardize artifacts and reduce token waste
- **Methodology docs** (overview, workflow, token efficiency)
- **Project docs** scaffolding (requirements + ADRs)
- **GitHub-native workflow UI** (Issue Forms + PR template)

---

## Repository layout

### Workflow / methodology (inside `ada/`)
- `ada/agents/`
  - `hl/prompt.md`
  - `ll/prompt.md`
- `ada/artifacts/methodology/`
  - `overview.md`
  - `workflow.md`
  - `token-efficiency.md`
- `ada/artifacts/templates/`
  - `state-block.txt`
  - `brief-template.txt`
- `ada/artifacts/project/`
  - `capsule.md`
  - `requirements/README.md`
  - `adr/README.md`

### GitHub UI layer (must stay at repo root)
- `.github/ISSUE_TEMPLATE/`
  - `epic.yml`
  - `task.yml`
  - `decision.yml`
- `.github/pull_request_template.md`

---

## Quick Start (new project)

### 1) Create a new repo from this template
**Option A (GitHub UI):**
- Open this template repository on GitHub
- Click **Use this template** → **Create a new repository**

**Option B (GitHub CLI):**
```bash
gh repo create <new-repo> --template <owner>/<ada-template-repo> --private --clone
```

---

### 2) Initialize agents
- Start the **HL agent** with: `ada/agents/hl/prompt.md`
- Start the **LL agent(s)** with: `ada/agents/ll/prompt.md`

---

### 3) Establish the project baseline (once)
- Fill `ada/artifacts/project/capsule.md` (stack, commands, repo conventions)
- Write/import requirements under:
  - `ada/artifacts/project/requirements/` (follow its `README.md`)
- If needed, create ADRs under:
  - `ada/artifacts/project/adr/` (follow its `README.md`)

---

### 4) Run the ADA loop
1. **HL** creates **Epics** and **Tasks** as GitHub issues using the Issue Forms in `.github/ISSUE_TEMPLATE/`.
2. **LL** implements a Task on a feature branch and opens a PR using `.github/pull_request_template.md`.
3. **Human + HL** review, merge, and repeat.

---

## Where to read the real rules
- Practical workflow: `ada/artifacts/methodology/workflow.md`
- Token discipline + State Block usage: `ada/artifacts/methodology/token-efficiency.md`
- Big picture: `ada/artifacts/methodology/overview.md`
