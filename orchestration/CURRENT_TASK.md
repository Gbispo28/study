# Task: TASK-INFRA-001 — Automation Control Plane Infrastructure

## 1. Context & Objective
Establish the end-to-end automation infrastructure connecting ChatGPT, Gemini/Antigravity, GitHub, Google Drive, and Make, enabling autonomous execution and rigorous external auditing without manual copy-pasting.

## 2. Invariants & Scope
- Scope: Automation control plane only.
- Strict Invariant: Do NOT modify pedagogical architecture. Gate 2 remains `GATE 2: BLOCKED ON LEARNER BASELINE`.
- Security: Zero secrets in repository or message bus.

## 3. Deliverables
1. Control Plane message bus structure (`orchestration/`).
2. Robust local runner (`automation/runner.py`) with PID lock, outbound polling, quality gates, and git delivery.
3. Make scenario blueprints (`automation/make/`).
4. Adversarial test suite (`automation/tests/test_runner.py`).
5. Updated living project state and handoff.

## 4. Verification Criteria
- All adversarial tests passing.
- Quality gates passing with code 0 (`bash scripts/quality_gate.sh`).
- Zero unstaged edits or uncommitted secrets.
