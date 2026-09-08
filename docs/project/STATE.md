# Project State: English Learning OS

> **Last Updated**: 2026-09-08<br>
> **Active Milestone**: Milestone 2 — Phase 02 Complete (Pedagogical Specification Delivered)<br>
> **Gate 2 Decision**: `GATE 2: BLOCKED ON LEARNER BASELINE` (Specification 100% complete; dependent individual calibration awaiting diagnostic test execution)

---

## 1. Quick Orientation

- **Current Phase**: `Phase 02: Product Discovery & Learning Science Specification (SPECIFICATION COMPLETE)`
- **Next Phase**: `Phase 03: Daily Journey & Card Architecture (READY PENDING BASELINE)`
- **Current Objective**: Pedagogical specification, evidence matrix, 10 research notes, and standardized 7-part diagnostic pack delivered. Ready for learner diagnostic execution.
- **Architecture Status**: Application framework, backend, and persistence are **deliberately deferred to Phase 04** via ADR-0000. Zero production code written; zero unverified language learning myths accepted.

---

## 2. Implemented Capabilities

| Component | Status | Description |
| :--- | :--- | :--- |
| **Governance Contracts** | Verified | [AGENTS.md](../../AGENTS.md), [CLAUDE.md](../../CLAUDE.md), [README.md](../../README.md) |
| **Workspace Rules** | Verified | 6 rules in `.agents/rules/` (`00` to `50-learning-product`) |
| **Custom Agent Fleet** | Verified | 9 specialized agents in `.agents/agents/` (Orchestrator + 8 Specialists) |
| **Agent Skills** | Verified | 8 standardized skills in `.agents/skills/` |
| **Tooling & Config** | Verified | `.editorconfig`, `.gitattributes`, `.gitignore`, `.agents/hooks.json`, `.agents/mcp_config.json` |
| **Quality Infrastructure** | Verified | `scripts/validate_repo.py`, `scripts/quality_gate.sh`, `.github/workflows/repository-quality.yml` |
| **Evidence Matrix** | Verified | [EVIDENCE_MATRIX.md](../research/EVIDENCE_MATRIX.md) (16 graded claims, 4 hypothesis audits) |
| **Research Repository** | Verified | 10 comprehensive research notes (`0001` through `0010`) in [docs/research/](../research/README.md) |
| **Diagnostic Pack** | Verified | Standardized 7-part test battery, rubrics, intake questionnaire, scoring model, and retest schedule in [docs/assessment/](../assessment/README.md) |
| **Pedagogical Invariants** | Verified | [LEARNING_PRINCIPLES.md](../product/LEARNING_PRINCIPLES.md) (Canonical pedagogical contract) |
| **System Specification** | Verified | [LEARNING_SYSTEM_SPEC.md](../product/LEARNING_SYSTEM_SPEC.md) (Master 18-section specification) |
| **Product Requirements** | Verified | Updated [REQUIREMENTS.md](../product/REQUIREMENTS.md) reflecting audits and new confirmed requirements |

---

## 3. Important Decisions Log

- **DEC-001**: Stack and technology selection is strictly deferred to Phase 04 through formal ADRs.
- **DEC-002**: Custom agent hierarchy is explicit: `orchestrator` is `mainAgent: true, subagent: false`; all specialists are `mainAgent: false, subagent: true` with `sandbox` policy.
- **DEC-003**: `code-auditor` and `security-reviewer` are restricted to read-only tools to preserve adversarial independence.
- **DEC-004**: Storing literal `${...}` in `mcp_config.json` is rejected due to runtime lack of interpolation; GitHub MCP is deferred to local/official authentication.
- **DEC-005**: FSRS Desired Retention is set to **90%** ($R = 0.90$) as the initial default for core foundational vocabulary, revising the previous 85% hypothesis to prevent high lapse churn.
- **DEC-006**: Contrastive phonetics prioritizes **epenthesis suppression on word-final stops** and **word stress** over native-accent eradication, adhering to the Intelligibility Principle.
- **DEC-007**: The 60-minute daily budget is governed by a **modular 3-block architecture** (15m Retrieval / 30m Input / 15m Production) with automatic workload throttling when review time exceeds 15 minutes.
- **DEC-008**: Hypotheses audited: HYP-01 revised (abandoned exact 2x retention claim); HYP-02 revised (unvalidated 85% parameter replaced with 90% default); HYP-03 revised (absolute fossilization prevention replaced with continuous contrastive training); HYP-04 supported (structured AI dialogue reduces anxiety).

---

## 4. Active Constraints & Environment

- **Development Hardware**: MacBook Air M4 (macOS desktop workstation).
- **Target Mobile Companion**: Galaxy S24 Ultra (Android mobile companion for AnkiDroid & Gemini Live).
- **Installed Runtimes**: Python 3.14.6, Git 2.50.1, Node v24.14.1.
- **Primary AI Platforms**: Google AI Pro (Gemini Advanced / Live), Claude Code Pro.
- **Daily Timebox**: Strictly 60 focused minutes/day. Ambient exposure is tracked separately and not counted toward the 60-minute core.

---

## 5. Blockers & Dependencies

- **Blocker**: Dependent personalization decisions (initialization of vector $\vec{P}$ and dynamic routine weights) are **BLOCKED ON LEARNER BASELINE**.
  - *Required User Input 1*: Submission of answers to [LEARNER_INTAKE.md](../assessment/LEARNER_INTAKE.md).
  - *Required User Input 2*: Completion and audio recording of [BASELINE_PROTOCOL.md](../assessment/BASELINE_PROTOCOL.md).

---

## 6. Next Milestone

- **Milestone 3**: Daily Journey & Card Architecture (Phase 03)
  - Task 1: Initialize learner baseline vector $\vec{P}$ upon test execution.
  - Task 2: Formulate Anki note type templates (4 card schemas: Lean Receptive, Sentence Cloze, Minimal Pair, Productive Prompt).
  - Task 3: Establish Galaxy S24 Ultra + MacBook Air M4 daily execution workflows.

---

## 7. Stable Verification & Baseline State

- **Branch**: `main`
- **Remote**: `origin` (`https://github.com/Gbispo28/study.git`)
- **Foundation Baseline Commit**: `9737f2d` (*chore: bootstrap agent-first project foundation*)
- **Phase 01 Hardening Commit**: `4b0e109` (*chore(quality): enforce git hygiene and align foundation rules*)
- **Gate 1 Status**: `PASSED`
- **Gate 2 Status**: `BLOCKED ON LEARNER BASELINE` (Specification Complete)
- **Verification Suite**: `scripts/quality_gate.sh` (Integrity validator + Git hygiene gate)
- **CI Workflow**: GitHub Actions (`.github/workflows/repository-quality.yml`)
- **Current HEAD**: Resolve dynamically at runtime with `git rev-parse HEAD`
