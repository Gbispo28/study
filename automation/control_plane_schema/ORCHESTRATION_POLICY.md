# Orchestration Policy: English Learning OS

> **Scope**: Canonical rules governing collaboration between **GitHub (Source of Truth)**, **Google Drive (External Message Bus)**, **Local Runner (Git Delivery Controller)**, **Automated Auditor**, **Make (Cloud Coordinator)**, and **ChatGPT (Strategic Supervisor)**.

---

## 1. Architectural Layers & Separation of Concerns

1. **GitHub (`origin/main`) — Source of Truth**:
   - Canonical repository for all source code, tests, documentation, and history.
   - Zero mutable operational state is versioned in Git.
   - No task is complete until its commit is pushed to `main` and verified by CI.

2. **Google Drive (`English Learning OS Orchestration/`) — External Control Plane**:
   - Resides strictly **outside** the Git repository working tree.
   - Houses volatile state (`STATE.json`), task descriptors (`CURRENT_TASK.md`, `NEXT_TASK.md`), handoffs (`EXECUTOR_HANDOFF.md`), audit reports (`AUDIT_REPORT.md`), human blocks (`HUMAN_ACTION_REQUIRED.md`), and the event journal (`EVENTS.ndjson`).

3. **Local Runner (`automation/runner.py`) — Exclusive Git Delivery Controller**:
   - Outbound polling client (zero incoming network ports on macOS).
   - Enforces protected paths (`PROTECTED_PATHS`).
   - Executes the implementation agent via Antigravity CLI (`agy -p`).
   - The executor is strictly prohibited from running Git commands. The runner alone stages, commits, and pushes after quality gates pass.

4. **Automated Auditor (`automation/auditor.py`) — Independent Background Auditor**:
   - Employs a separate model (`gemini-3.1-pro-high` or `claude-sonnet-4-6`), distinct prompt, and isolated context.
   - **Invariable**: `EXECUTOR != AUDITOR`. The executor cannot audit its own work. The auditor cannot modify code.
   - Audits real GitHub evidence: commit existence, diff boundaries, secret absence, and CI run results.
   - Emits verdicts: `APPROVED`, `FIX_REQUIRED`, `HUMAN_REQUIRED`, `ERROR`.
   - Generates `NEXT_TASK.md` upon approval, or corrective tasks upon rejection.

5. **Make — Cloud Coordinator & Notifier**:
   - Monitors `STATE.json` in the external Drive folder.
   - Promotes `NEXT_TASK.md` -> `CURRENT_TASK.md` and resets `STATE.json` to `READY` upon `APPROVED`.
   - Dispatches alerts upon `HUMAN_REQUIRED` or `ERROR`.
   - Non-SPOF: Runner and Auditor support `--standalone` mode if Make is offline.

6. **ChatGPT — External Strategic Supervisor**:
   - Human-in-the-loop interface for macro reviews, retrospective evaluation, and human escalation.
   - Does NOT block the automated micro-task execution loop.

---

## 2. State Machine Invariants

```
                ┌───────────────┐
                │     READY     │
                └───────┬───────┘
                        │ (Runner picks task; payload-hash validated)
                        ▼
                ┌───────────────┐
                │   EXECUTING   │
                └───────┬───────┘
                        │ (Quality gate pass -> Commit -> Push)
                        ▼
                ┌───────────────┐
                │AWAITING_AUDIT │
                └───────┬───────┘
                        │ (Automated Auditor validates real GitHub commit/CI)
         ┌──────────────┼──────────────┐
         │ (Fix needed) │ (Approved)   │ (Human intervention needed)
         ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌────────────────┐
│ FIX_REQUIRED │ │   APPROVED   │ │ HUMAN_REQUIRED │
└───────┬──────┘ └──────┬───────┘ └────────┬───────┘
        │               │                  │
        │(Auditor emits │(Make/Runner      │(Human resolves issue)
        │ corrective)   │ promotes NEXT)   │
        ▼               ▼                  ▼
     (READY)         (READY)            (READY)
```

1. **Payload-First, State-Last**: Payloads (`CURRENT_TASK.md`, `EXECUTOR_HANDOFF.md`) must be fully written before `STATE.json` is updated. `STATE.json` includes `content_hash` (`sha256(CURRENT_TASK.md)`); execution is refused if hash mismatches.
2. **Optimistic Concurrency**: `STATE.json` contains `state_version`. Every update checks that the disk version matches the read version, preventing race conditions.
3. **Protected Paths Guard**: No regular task may modify:
   - `automation/runner.py`
   - `automation/auditor.py`
   - `automation/control_plane_schema/`
   - `scripts/quality_gate.sh`
   - `scripts/validate_repo.py`
   - `.agents/`
   - `.github/workflows/`
   Modifications to these paths require `maintenance_mode: true` in task metadata.
4. **Finite Retries**: If quality gate or audit fails, `retry_count` increments. If `retry_count >= max_retries`, transition immediately to `ERROR` or `HUMAN_REQUIRED`. Infinite loops are strictly prohibited.
5. **Append-Only Event Journal**: Every transition appends a JSON line to `EVENTS.ndjson`.

---

## 3. Disaster Recovery & Emergency Stop

1. **Stale Lock Cleanup**: If a process crashes, the runner detects dead PID via `os.kill(pid, 0)` and reclaims the lock cleanly.
2. **Emergency Disconnect**: To halt automation immediately, set `"state": "HUMAN_REQUIRED"` in `STATE.json` or terminate runner daemons.
3. **Safe Rollback**: If mid-task execution fails prior to commit, `git reset --hard HEAD` restores the repository cleanly to `expected_git_head`.
