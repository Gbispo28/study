# English Learning OS — Automation Control Plane & Local Runner

> **Architecture Overview**: Autonomous, closed-loop collaboration between **ChatGPT (Auditor)**, **Gemini / Antigravity (Executor)**, **GitHub (Source of Truth)**, **Google Drive (Control Plane / Message Bus)**, and **Make (Orchestrator)**.

---

## 1. System Architecture

```
[ChatGPT: Supervisor/Auditor] ──> Reviews Diff, CI & Approves ──> [Google Drive: Message Bus]
                                                                        │
                                                                        ▼
                                                             [Make: Cloud Orchestrator]
                                                                        │ (Watches STATE.json)
                                                                        ▼
[MacBook: Local Runner (runner.py)] <── Polls STATE.json ───────────────┘
  │
  ├── 1. Validates Git Cleanliness & expected_git_head
  ├── 2. Executes Task via Antigravity CLI (`agy -p`)
  ├── 3. Executes Quality Gate (`bash scripts/quality_gate.sh`)
  ├── 4. Commits and Pushes to GitHub `main`
  └── 5. Generates Handoff & transitions state to `AWAITING_AUDIT`
```

---

## 2. Security & Zero-Secret Architecture

1. **Outbound-Only Polling**: The local runner (`runner.py`) runs as a pure client. It opens zero network listening ports on the MacBook Air, presenting no ingress attack surface.
2. **Subscription Authentication**: The local runner leverages the locally authenticated `/Users/gmbispo/.local/bin/agy` CLI, which authenticates via your Google AI Pro subscription without exposing raw API keys.
3. **Secret Sanitization**: `runner.py` uses `SafeLogger` with regex filters to strip tokens (`ghp_`, `AIza`, `Bearer`, etc.) from console output and `automation/logs/runner.log`.
4. **Git Hygiene**: Runtime states (`automation/logs/`, `automation/state/`, `automation/.lock`) are isolated in `.gitignore`.

---

## 3. State Machine Protocol

All state transitions are persisted in `orchestration/STATE.json`:

| State | Role Responsible | Trigger / Description | Next Permitted State |
| :--- | :--- | :--- | :--- |
| **`READY`** | Orchestrator / Human | Task in `CURRENT_TASK.md` is ready for execution. | `EXECUTING` |
| **`EXECUTING`** | Local Runner | Local runner acquired lock and is executing the task. | `AWAITING_AUDIT`, `FIX_REQUIRED`, `ERROR` |
| **`AWAITING_AUDIT`** | Local Runner | Execution, quality gates, and git push succeeded. | `APPROVED`, `FIX_REQUIRED`, `HUMAN_REQUIRED` |
| **`FIX_REQUIRED`** | Auditor (ChatGPT) | Auditor found deficiencies; returns with feedback. | `EXECUTING` |
| **`APPROVED`** | Auditor (ChatGPT) | Auditor verified git diff and CI. Prompts task advancement. | `READY` (via Make promotion) |
| **`HUMAN_REQUIRED`** | Any | Unavoidable human action needed (OAuth, 2FA, GUI click). | `READY` (after human completes) |
| **`COMPLETE`** | Orchestrator | All planned tasks in current milestone are finished. | Terminal |
| **`ERROR`** | Local Runner | Unrecoverable failure or `retry_count >= max_retries`. | Terminal (manual intervention) |

---

## 4. How to Run the Local Runner

### Option A: Manual / Single Run (Verification Mode)
```bash
# Dry run: Inspect current task without modifying repository
python3 automation/runner.py --dry-run

# Single run: Execute the current task once and exit
python3 automation/runner.py --once
```

### Option B: Continuous Background Poller (Daemon Mode)
```bash
# Run in background polling every 10 seconds
python3 automation/runner.py --daemon
```

### Option C: macOS `launchd` Service (Persistent Background Runner)
To keep the runner active automatically in macOS without an open terminal window:

1. Copy the provided launchd plist (see template below) to `~/Library/LaunchAgents/com.englishlearningos.runner.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.englishlearningos.runner</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/python3</string>
        <string>/Users/gmbispo/Documents/Programação/study/automation/runner.py</string>
        <string遮--daemon</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/gmbispo/Documents/Programação/study</string>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/gmbispo/Documents/Programação/study/automation/logs/launchd.stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/gmbispo/Documents/Programação/study/automation/logs/launchd.stderr.log</string>
</dict>
</plist>
```
2. Load the service:
```bash
launchctl load ~/Library/LaunchAgents/com.englishlearningos.runner.plist
```
3. Stop the service:
```bash
launchctl unload ~/Library/LaunchAgents/com.englishlearningos.runner.plist
```

---

## 5. Failure Recovery & Troubleshooting

1. **Concurrency Lock Error (`Runner lock held`)**:
   - If a previous runner crashed or was killed abruptly, run:
   ```bash
   python3 automation/runner.py --force-unlock
   ```
2. **Git Divergence Error (`Git HEAD divergence`)**:
   - Occurs when the remote has new commits that the local repo does not have.
   - Run `git pull --rebase origin main` and update `"expected_git_head"` in `orchestration/STATE.json`.
3. **Quality Gate Failure**:
   - Inspect `automation/logs/runner.log`.
   - Run `bash scripts/quality_gate.sh` manually to pinpoint the failing test or git hygiene issue.
4. **Emergency Stop**:
   - Immediately change `"state": "HUMAN_REQUIRED"` in `orchestration/STATE.json`.
   - All runners will pause execution on their next poll.
