# Project State: English Learning OS

> **Last Updated**: 2026-09-08<br>
> **Active Milestone**: Milestone 1 — Complete (Gate 1 Passed) | Milestone 2 — Ready (Next)<br>
> **Status**: Gate 1 Passed — Foundation Complete

---

## 1. Quick Orientation

- **Current Phase**: `Phase 01: Foundation & Governance (COMPLETE)` | `Phase 02: Product Discovery & SLA Specification (READY / NEXT)`
- **Current Objective**: Foundation hardening and Gate 1 formal closure completed; ready to initiate Phase 02 discovery.
- **Architecture Status**: Application framework, backend, and persistence are **deliberately deferred to Phase 04** via ADR-0000. Agentic infrastructure and quality gates are operational and verified.

---

## 2. Implemented Capabilities

| Component | Status | Description |
| :--- | :--- | :--- |
| **Governance Contracts** | Verified | [AGENTS.md](../../AGENTS.md), [CLAUDE.md](../../CLAUDE.md), [README.md](../../README.md) |
| **Workspace Rules** | Verified | 6 rules in `.agents/rules/` (`00-core-engineering`, `10-testing-quality`, `20-git-delivery`, `30-security`, `40-documentation-context`, `50-learning-product`) |
| **Custom Agent Fleet** | Verified | 9 specialized agents in `.agents/agents/` (1 Orchestrator + 8 Specialists/Auditors) |
| **Agent Skills** | Verified | 8 standardized skills in `.agents/skills/` |
| **Tooling & Config** | Verified | `.editorconfig`, `.gitattributes`, `.gitignore`, `.agents/hooks.json`, `.agents/mcp_config.json` |
| **Quality Infrastructure** | Verified | `scripts/validate_repo.py`, `scripts/quality_gate.sh` |
| **CI / CD Pipeline** | Verified | `.github/workflows/repository-quality.yml` |
| **Living Documentation** | Verified | Complete suite in `docs/` (`product/`, `project/`, `architecture/`, `decisions/`, `research/`, `quality/`, `handoffs/`) |

---

## 3. Important Decisions Log

- **DEC-001**: Stack and technology selection is strictly deferred to Phase 04 through formal ADRs.
- **DEC-002**: Custom agent hierarchy is explicit: `orchestrator` is `mainAgent: true, subagent: false`; all specialists are `mainAgent: false, subagent: true` with `sandbox` policy.
- **DEC-003**: `code-auditor` and `security-reviewer` are restricted to read-only tools to preserve adversarial independence.
- **DEC-004**: Storing literal `${...}` in `mcp_config.json` is rejected due to runtime lack of interpolation; GitHub MCP is deferred to local/official authentication.

---

## 4. Active Constraints & Environment

- **Development Hardware**: MacBook Air M4 (macOS).
- **Target Mobile Companion**: Galaxy S24 Ultra (Android / AnkiDroid).
- **Installed Runtimes**: Python 3.14.6, Git 2.50.1, Node v24.14.1.
- **Primary AI Platforms**: Google Antigravity 2.0 / Gemini, Claude Code Pro.

---

## 5. Blockers & Risks

- **Blockers**: None. Foundation Gate 1 is closed.
- **Risks**: Potential temptation in Phase 02 to begin building UI before learner baseline and SLA routine are mathematically defined. Mitigated by strict gatekeeper rules.

---

## 6. Next Milestone

- **Milestone 2**: Product Discovery & Learning Science Specification (Ready / Next)
  - Task 1: Baseline diagnostic questionnaire & CEFR placement model.
  - Task 2: Mathematical breakdown of the 60-minute daily routine.
  - Task 3: Card design & FSRS configuration specification.

---

## 7. Stable Verification & Baseline State

- **Branch**: `main`
- **Remote**: `origin` (`https://github.com/Gbispo28/study.git`)
- **Foundation Baseline Commit**: `9737f2d` (*chore: bootstrap agent-first project foundation*)
- **Gate 1 Status**: `PASSED`
- **Verification Suite**: `scripts/quality_gate.sh` (Integrity validator + Git hygiene gate)
- **CI Workflow**: GitHub Actions (`.github/workflows/repository-quality.yml`)
- **Current HEAD**: Resolve dynamically at runtime with `git rev-parse HEAD` (not stored statically to avoid self-referential commit loops)
