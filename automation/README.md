# English Learning OS — Automation Architecture & Control Plane

> **Architecture Overview**: Autonomous, closed-loop collaboration between **GitHub (Source of Truth)**, **Google Drive (External Control Plane)**, **Local Runner (Git Delivery Controller)**, **Automated Auditor**, and **Make (Cloud Coordinator)**, with **ChatGPT** serving as external strategic supervisor.

---

## 1. Two-Layer Architecture

### Layer A: Versioned Source Code (GitHub `main`)
- Canonical source of truth for code, tests, rules, and governance.
- **Zero mutable runtime files**: Schemas and templates live in `automation/control_plane_schema/`. The repository working tree remains 100% clean during all state mutations.

### Layer B: Mutable Runtime Control Plane (Google Drive)
- Resides outside the Git repository at `Google Drive/Meu Drive/English Learning OS Orchestration/` (or configured via `control_plane_dir`).
- Contains:
  - `STATE.json` (State machine status, optimistic version, content hash)
  - `CURRENT_TASK.md` (Active task descriptor)
  - `EXECUTOR_HANDOFF.md` (Executor report)
  - `AUDIT_REPORT.md` (Automated auditor verdict)
  - `NEXT_TASK.md` (Next task candidate)
  - `HUMAN_ACTION_REQUIRED.md` (Human blocker queue)
  - `EVENTS.ndjson` (Append-only event journal)

---

## 2. Invariants & Security Perimeter

1. **Exclusive Git Delivery Controller**: The Antigravity executor (`agy`) is strictly prohibited from running Git commands. `runner.py` alone performs diff inspection, protected path checks, quality gates, atomic commits, and pushes.
2. **Protected Paths**: The following paths cannot be modified by regular tasks:
   - `automation/runner.py`
   - `automation/auditor.py`
   - `automation/control_plane_schema/`
   - `scripts/quality_gate.sh`
   - `scripts/validate_repo.py`
   - `.agents/`
   - `.github/workflows/`
   Any regular task touching these paths is rejected (`SecurityViolation`). Edits require `maintenance_mode: true` in task metadata.
3. **Payload-First / State-Last Protocol**: Payloads (`CURRENT_TASK.md`, `EXECUTOR_HANDOFF.md`) are written first, and their SHA-256 hash is verified against `STATE.json` before execution.
4. **Optimistic Concurrency**: `STATE.json` uses `state_version` to prevent concurrent write collisions.
5. **Auditor Independence (`EXECUTOR != AUDITOR`)**: The Automated Auditor uses a separate process and model (`gemini-3.1-pro-high` vs `gemini-3.8-flash-high`) and verifies real GitHub commits, diffs, and CI runs. The auditor cannot modify code.
6. **Zero Inbound Ports**: Local runner and auditor run outbound-only with zero open network ports on macOS.

---

## 3. Operational Usage

### Local Runner (`runner.py`)
```bash
# Dry run: Inspect current task without modifying repository
python3 automation/runner.py --dry-run

# Single run: Execute the current task once and exit
python3 automation/runner.py --once

# Continuous polling daemon:
python3 automation/runner.py --daemon

# Standalone mode (runs without Make):
python3 automation/runner.py --standalone
```

### Automated Auditor (`auditor.py`)
```bash
# Single audit check:
python3 automation/auditor.py --once

# Continuous audit daemon:
python3 automation/auditor.py --daemon

# Standalone promotion mode (promotes NEXT_TASK without Make):
python3 automation/auditor.py --standalone
```

---

## 4. Disaster Recovery & Troubleshooting

1. **Stale Lock (`Runner lock held`)**:
   - Detects inactive PID automatically. To manually clear:
   ```bash
   python3 automation/runner.py --force-unlock
   ```
2. **Git HEAD Divergence (`Git HEAD divergence`)**:
   - Occurs if remote has new commits. Run `git pull --rebase origin main` and align `expected_git_head` in `STATE.json`.
3. **Emergency Stop**:
   - Set `"state": "HUMAN_REQUIRED"` in `STATE.json`. All runners and auditors will pause on next poll.
