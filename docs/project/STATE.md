# Project State: English Learning OS

> **Last Updated**: 2026-09-08<br>
> **Active Milestone**: Milestone 2 — Phase 02: Product Discovery & SLA Specification (Specification Drafted — Baseline Pending)<br>
> **Gate 2 Decision**: `GATE 2: BLOCKED ON LEARNER BASELINE`<br>
> **Current Phase Status**: **OPEN / IN PROGRESS** (Pedagogical specification delivered; blocked on user diagnostic administration)

---

## 1. Quick Orientation

- **Current Phase**: `Phase 02: Product Discovery & Learning Science Specification (OPEN — BASELINE PENDING)`
- **Next Phase**: `Phase 03: Daily Journey & Card Architecture (LOCKED PENDING BASELINE)`
- **Current Objective**: The scientific specification, evidence matrix, 10 research notes, and 7-part diagnostic pack are fully authored and verified. The phase remains formally open until the user executes the diagnostic protocol and submits intake responses.
- **Architecture Status**: Application framework, backend, and persistence are **deliberately deferred to Phase 04** via ADR-0000. Zero production code written; zero unverified language learning myths accepted.

---

## 2. Implemented Capabilities (Specification Suite)

| Component | Status | Description |
| :--- | :--- | :--- |
| **Governance Contracts** | Verified | [AGENTS.md](../../AGENTS.md), [CLAUDE.md](../../CLAUDE.md), [README.md](../../README.md) |
| **Workspace Rules** | Verified | 6 rules in `.agents/rules/` (`00` to `50-learning-product`) |
| **Custom Agent Fleet** | Verified | 9 specialized agents in `.agents/agents/` (Orchestrator + 8 Specialists) |
| **Agent Skills** | Verified | 8 standardized skills in `.agents/skills/` |
| **Quality Infrastructure** | Verified | `scripts/validate_repo.py`, `scripts/quality_gate.sh`, `.github/workflows/repository-quality.yml` |
| **Evidence Matrix** | Verified | [EVIDENCE_MATRIX.md](../research/EVIDENCE_MATRIX.md) (16 graded claims, 4 hypothesis audits) |
| **Research Repository** | Verified | 10 comprehensive research notes (`0001` through `0010`) in [docs/research/](../research/README.md) |
| **Diagnostic Pack** | Verified | Standardized 7-part test battery, rubrics, intake questionnaire, scoring model, and retest schedule in [docs/assessment/](../assessment/README.md) |
| **Pedagogical Invariants** | Verified | [LEARNING_PRINCIPLES.md](../product/LEARNING_PRINCIPLES.md) (Canonical pedagogical contract) |
| **System Specification** | Verified | [LEARNING_SYSTEM_SPEC.md](../product/LEARNING_SYSTEM_SPEC.md) (Master 18-section specification) |
| **Automation Control Plane** | Verified | [ORCHESTRATION_POLICY.md](../../automation/control_plane_schema/ORCHESTRATION_POLICY.md), [runner.py](../../automation/runner.py), [auditor.py](../../automation/auditor.py), Make blueprints (`automation/make/`), 64-case test suite (62 deterministic CI + 2 local real agy smoke) |

---

## 3. Important Decisions Log

- **DEC-001**: Stack and technology selection is strictly deferred to Phase 04 through formal ADRs.
- **DEC-002**: Custom agent hierarchy is explicit: `orchestrator` is `mainAgent: true, subagent: false`; all specialists are `mainAgent: false, subagent: true` with `sandbox` policy.
- **DEC-003**: `code-auditor` and `security-reviewer` are restricted to read-only tools to preserve adversarial independence.
- **DEC-004**: Storing literal `${...}` in `mcp_config.json` is rejected due to runtime lack of interpolation; GitHub MCP is deferred to local/official authentication.
- **DEC-005**: FSRS Desired Retention is set to **90%** ($R = 0.90$) as the initial default for core foundational vocabulary, revising the previous 85% hypothesis. Legacy CMRR was removed in Anki 25.07; workload trade-offs are guided by native Anki Simulator and Help Me Decide.
- **DEC-006**: Contrastive phonetics prioritizes **epenthesis suppression on word-final stops** and **word stress** over native-accent eradication, accounting for BP regional dialect variation.
- **DEC-007**: The 60-minute daily budget is governed by a **modular 3-block architecture** (15m Retrieval / 30m Input / 15m Production) with automatic workload throttling.
- **DEC-008**: Hypotheses audited: HYP-01 revised (abandoned exact 2x retention claim); HYP-02 revised (unvalidated 85% parameter replaced with 90% default); HYP-03 revised (absolute fossilization prevention replaced with continuous contrastive training); HYP-04 supported (structured AI dialogue reduces anxiety).
- **DEC-009**: Phase 02 remains formally **OPEN** under `GATE 2: BLOCKED ON LEARNER BASELINE`. Phase 03 is locked until learner diagnostic data is submitted.
- **DEC-010**: Assessment architecture strictly segregates learner surfaces (`docs/assessment/learner/`) from administrative surfaces (`docs/assessment/admin/`) to prevent test answer and audio script contamination.
- **DEC-011**: The custom diagnostic battery operates under an explicit measurement ceiling at **B2**, reporting `ABOVE CURRENT INSTRUMENT CEILING` for advanced performances rather than making pseudo-psychometric C1/C2 claims.
- **DEC-012**: Automation control plane separates Layer A (Git source code, schemas, tools) from Layer B (mutable runtime control plane on external Google Drive). Local runner (`automation/runner.py`) is exclusive Git Delivery Controller with protected path enforcement; Automated Auditor (`automation/auditor.py`) runs independently (`EXECUTOR != AUDITOR`) verifying real GitHub evidence; Make provides cloud coordination; ChatGPT acts as external strategic supervisor.
- **DEC-013**: Automation Hardening & Containment: Fail-closed CI gate (requires completed + success); real two-stage audit (Stage A deterministic + Stage B independent model review with structured JSON validation); true selective staging (no `git add .`); technical Git containment (pre/post execution assertions + `.agents/hooks.json` PreToolUse hook); remote commit verification against `origin/main`; immutable task metadata authorization for protected paths; and grounded task generation terminating at `HUMAN_REQUIRED` (Gate 2 Learner Baseline blocker). Zero background daemons active.



---

## 4. Active Constraints & Environment

- **Development Hardware**: MacBook Air M4 (macOS desktop workstation).
- **Target Mobile Companion**: Galaxy S24 Ultra (Android mobile companion for AnkiDroid & Gemini Live).
- **Installed Runtimes**: Python 3.14.6, Git 2.50.1, Node v24.14.1.
- **Primary AI Platforms (Current 2026)**: Google AI Pro (Gemini 3.1 Pro, Gemini Live, NotebookLM Audio Overview with 300 sources/notebook), Claude Code Pro (using supported frontier models).
- **Daily Timebox**: Strictly 60 focused minutes/day. Ambient exposure is tracked separately as optional bonus.

---

## 5. Blockers & Dependencies

- **ACTIVE BLOCKER**: Individualized calibration of state vector $\vec{P}$ and dynamic routine weights is **BLOCKED ON LEARNER BASELINE**.
  - *Required User Input 1*: Submission of answers to [LEARNER_INTAKE.md](../assessment/LEARNER_INTAKE.md).
  - *Required User Input 2*: Completion and audio recording of [learner/BASELINE_FORM.md](../assessment/learner/BASELINE_FORM.md).

---

## 6. Next Milestone Status

- **Milestone 2**: Phase 02 — Product Discovery & Learning Science Specification (**IN PROGRESS / BASELINE PENDING**)
  - Task 1: Learner completes intake questionnaire ([LEARNER_INTAKE.md](../assessment/LEARNER_INTAKE.md)).
  - Task 2: Learner executes diagnostic battery ([learner/BASELINE_FORM.md](../assessment/learner/BASELINE_FORM.md)).
  - Task 3: Ingest responses, score vector $\vec{P}$ via [admin/SCORING_GUIDE.md](../assessment/admin/SCORING_GUIDE.md), detect bottleneck, and close Gate 2.
- **Milestone 3**: Phase 03 — Daily Journey & Card Architecture (**LOCKED** until Gate 2 closes).

---

## 7. Stable Verification & Baseline State

- **Branch**: `main`
- **Remote**: `origin` (`https://github.com/Gbispo28/study.git`)
- **Foundation Baseline Commit**: `9737f2d` (*chore: bootstrap agent-first project foundation*)
- **Phase 01 Hardening Commit**: `4b0e109` (*chore(quality): enforce git hygiene and align foundation rules*)
- **Gate 1 Status**: `PASSED`
- **Gate 2 Status**: `BLOCKED ON LEARNER BASELINE` (Phase 02 Open)
- **Verification Suite**: `scripts/quality_gate.sh` (Integrity validator + Git hygiene gate)
- **CI Workflow**: GitHub Actions (`.github/workflows/repository-quality.yml`)
- **Current HEAD**: Resolve dynamically at runtime with `git rev-parse HEAD`
