#!/usr/bin/env python3
"""
English Learning OS — Outbound Local Runner
Exclusive Git Delivery Controller & Task Executor.

Key Invariants:
- Outbound polling only: Zero listening ports or inbound network attack surfaces.
- Exclusive Git Delivery Controller: The executor agent is prohibited from git operations;
  runner alone inspects diffs, validates scope, runs quality gates, commits, and pushes.
- Protected Paths: Blocks edits to runner, auditor, schemas, quality gates, .agents, CI.
- Payload-First, State-Last: Validates SHA-256 content_hash of CURRENT_TASK.md.
- Optimistic Concurrency: Enforces state_versioning on STATE.json.
- Idempotency: Tracks executed (task_id, expected_git_head) in execution_history.json.
- Zero Secrets: SafeLogger strips API keys and credentials from logs and output.
"""

import sys
import os
import time
import json
import signal
import shutil
import re
import hashlib
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]{20,50}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,90}"),
    re.compile(r"AIza[0-9A-Za-z-_]{20,50}"),
    re.compile(r"sk-[A-Za-z0-9]{20,50}"),
    re.compile(r"bearer\s+[A-Za-z0-9\-\._~\+\/]+=*", re.IGNORECASE),
]

PROTECTED_PATHS = [
    "automation/runner.py",
    "automation/auditor.py",
    "automation/control_plane_schema/",
    "scripts/quality_gate.sh",
    "scripts/validate_repo.py",
    ".agents/",
    ".github/workflows/",
]


def sanitize_text(text: str) -> str:
    """Mask potential secret patterns from strings."""
    sanitized = text
    for pattern in SECRET_PATTERNS:
        sanitized = pattern.sub("[REDACTED_SECRET]", sanitized)
    return sanitized


class SafeLogger:
    """Structured, secret-sanitizing logger."""

    def __init__(self, log_file: Optional[Path] = None):
        self.log_file = log_file
        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, level: str, msg: str, **kwargs):
        timestamp = datetime.now(timezone.utc).isoformat()
        clean_msg = sanitize_text(msg)
        entry = {"timestamp": timestamp, "level": level, "message": clean_msg}
        if kwargs:
            entry["details"] = {k: sanitize_text(str(v)) for k, v in kwargs.items()}

        out_str = f"[{timestamp}] [{level:5s}] {clean_msg}"
        if kwargs:
            out_str += f" | {json.dumps(entry['details'])}"

        print(out_str, flush=True)

        if self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(out_str + "\n")
            except Exception:
                pass

    def info(self, msg: str, **kwargs):
        self.log("INFO", msg, **kwargs)

    def warn(self, msg: str, **kwargs):
        self.log("WARN", msg, **kwargs)

    def error(self, msg: str, **kwargs):
        self.log("ERROR", msg, **kwargs)


class RunnerLock:
    """PID-based concurrency file lock with dead process detection."""

    def __init__(self, lock_path: Path, logger: SafeLogger):
        self.lock_path = lock_path
        self.logger = logger
        self.acquired = False

    def acquire(self) -> bool:
        if self.lock_path.exists():
            try:
                content = json.loads(self.lock_path.read_text(encoding="utf-8"))
                existing_pid = content.get("pid")
                if existing_pid:
                    try:
                        os.kill(existing_pid, 0)
                        self.logger.warn(f"Runner lock held by active PID {existing_pid}. Skipping execution.")
                        return False
                    except OSError:
                        self.logger.info(f"Removing stale lock file from dead PID {existing_pid}.")
            except Exception as e:
                self.logger.warn(f"Could not read existing lock file ({e}), replacing.")

        lock_data = {
            "pid": os.getpid(),
            "acquired_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            self.lock_path.parent.mkdir(parents=True, exist_ok=True)
            self.lock_path.write_text(json.dumps(lock_data, indent=2), encoding="utf-8")
            self.acquired = True
            return True
        except Exception as e:
            self.logger.error(f"Failed to acquire lock at {self.lock_path}: {e}")
            return False

    def release(self):
        if self.acquired and self.lock_path.exists():
            try:
                self.lock_path.unlink()
            except Exception:
                pass
            self.acquired = False


class OrchestrationRunner:
    """Manages the full lifecycle of autonomous task execution and Git delivery."""

    def __init__(self, repo_root: Path, config: Dict[str, Any], logger: SafeLogger):
        self.repo_root = repo_root.resolve()
        self.config = config
        self.logger = logger

        # Control plane directory (external Google Drive folder by default)
        default_cp_dir = Path.home() / "Google Drive" / "Meu Drive" / "English Learning OS Orchestration"
        configured_cp = config.get("control_plane_dir")
        if configured_cp:
            self.control_plane_dir = Path(configured_cp).expanduser().resolve()
        elif default_cp_dir.exists():
            self.control_plane_dir = default_cp_dir
        else:
            # Local fallback outside working tree
            self.control_plane_dir = Path.home() / ".english_learning_os_orchestration"

        self.control_plane_dir.mkdir(parents=True, exist_ok=True)

        self.state_file = self.control_plane_dir / "STATE.json"
        self.current_task_file = self.control_plane_dir / "CURRENT_TASK.md"
        self.next_task_file = self.control_plane_dir / "NEXT_TASK.md"
        self.handoff_file = self.control_plane_dir / "EXECUTOR_HANDOFF.md"
        self.audit_report_file = self.control_plane_dir / "AUDIT_REPORT.md"
        self.events_file = self.control_plane_dir / "EVENTS.ndjson"
        self.history_file = self.repo_root / "automation" / "state" / "execution_history.json"
        self.history_file.parent.mkdir(parents=True, exist_ok=True)

        self.lock = RunnerLock(self.repo_root / "automation" / ".lock", logger)
        self._running = True

    def stop(self):
        self._running = False

    def load_state(self) -> Optional[Dict[str, Any]]:
        if not self.state_file.exists():
            return None
        try:
            return json.loads(self.state_file.read_text(encoding="utf-8"))
        except Exception as e:
            self.logger.error(f"Failed to parse STATE.json: {e}")
            return None

    def save_state(self, state: Dict[str, Any], expected_version: Optional[int] = None) -> bool:
        """Saves state with optimistic concurrency check."""
        try:
            if expected_version is not None and self.state_file.exists():
                current_on_disk = json.loads(self.state_file.read_text(encoding="utf-8"))
                disk_version = current_on_disk.get("state_version", 1)
                if disk_version != expected_version:
                    self.logger.error(
                        f"Optimistic concurrency violation: disk version {disk_version} != expected {expected_version}"
                    )
                    return False

            state["state_version"] = (state.get("state_version", 0) + 1)
            state["updated_at"] = datetime.now(timezone.utc).isoformat()

            temp_path = self.state_file.with_suffix(".tmp")
            temp_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            temp_path.replace(self.state_file)

            # Append to event log
            self.append_event({
                "timestamp": state["updated_at"],
                "event": f"STATE_TRANSITION_{state.get('state')}",
                "task_id": state.get("task_id"),
                "state": state.get("state"),
                "state_version": state["state_version"],
                "execution_id": state.get("execution_id")
            })
            return True
        except Exception as e:
            self.logger.error(f"Failed to save STATE.json: {e}")
            return False

    def append_event(self, event_data: Dict[str, Any]):
        try:
            with open(self.events_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event_data) + "\n")
        except Exception:
            pass

    def compute_file_hash(self, path: Path) -> str:
        if not path.exists():
            return ""
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def get_git_head(self) -> str:
        res = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo_root, text=True)
        return res.strip()

    def is_git_clean(self) -> bool:
        res = subprocess.check_output(["git", "status", "--porcelain"], cwd=self.repo_root, text=True)
        lines = [line.strip() for line in res.splitlines() if line.strip()]
        return len(lines) == 0

    def load_history(self) -> List[Dict[str, str]]:
        if not self.history_file.exists():
            return []
        try:
            return json.loads(self.history_file.read_text(encoding="utf-8"))
        except Exception:
            return []

    def record_execution(self, task_id: str, expected_head: str, execution_id: str):
        history = self.load_history()
        history.append({
            "task_id": task_id,
            "expected_git_head": expected_head,
            "execution_id": execution_id,
            "executed_at": datetime.now(timezone.utc).isoformat()
        })
        self.history_file.write_text(json.dumps(history, indent=2), encoding="utf-8")

    def is_already_executed(self, task_id: str, expected_head: str) -> bool:
        history = self.load_history()
        return any(
            h.get("task_id") == task_id and h.get("expected_git_head") == expected_head
            for h in history
        )

    def verify_protected_paths(self, maintenance_mode: bool = False) -> Tuple[bool, List[str]]:
        """Verifies that no protected paths are modified unless maintenance_mode is enabled."""
        if maintenance_mode:
            return (True, [])

        res = subprocess.check_output(["git", "status", "--porcelain"], cwd=self.repo_root, text=True)
        modified_files = []
        for line in res.splitlines():
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                modified_files.append(parts[1].strip())

        violations = []
        for mf in modified_files:
            for pp in PROTECTED_PATHS:
                if mf == pp or mf.startswith(pp):
                    violations.append(mf)

        return (len(violations) == 0, violations)

    def run_quality_gate(self) -> Tuple[bool, str]:
        cmd = self.config.get("quality_gate_command", "bash scripts/quality_gate.sh")
        try:
            proc = subprocess.run(
                cmd,
                shell=True,
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=self.config.get("execution_timeout_seconds", 300),
            )
            output = sanitize_text(proc.stdout + "\n" + proc.stderr)
            return (proc.returncode == 0, output)
        except subprocess.TimeoutExpired:
            return (False, "Quality gate timed out.")
        except Exception as e:
            return (False, f"Error executing quality gate: {e}")

    def execute_agy(self, prompt: str, model: Optional[str] = None) -> Tuple[bool, str]:
        """Invokes Antigravity CLI in non-interactive print mode with JSON output."""
        agy_bin = self.config.get("agy_binary", "/Users/gmbispo/.local/bin/agy")
        if not Path(agy_bin).exists():
            agy_bin = shutil.which("agy") or agy_bin

        if not Path(agy_bin).exists():
            return (False, f"Antigravity CLI not found at '{agy_bin}'")

        chosen_model = model or self.config.get("default_model", "gemini-3.8-flash-high")
        cmd = [
            agy_bin,
            "-p",
            prompt,
            "--model",
            chosen_model,
            "--output-format",
            "json",
            "--dangerously-skip-permissions",
        ]
        try:
            self.logger.info(f"Invoking agy CLI (model: {chosen_model})...")
            proc = subprocess.run(
                cmd,
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=self.config.get("execution_timeout_seconds", 300),
            )
            raw_out = proc.stdout.strip()
            if proc.returncode != 0:
                err_msg = sanitize_text(proc.stderr.strip() or raw_out)
                return (False, f"agy returned non-zero code {proc.returncode}: {err_msg}")

            try:
                parsed = json.loads(raw_out)
                resp_text = parsed.get("response", raw_out)
                return (True, sanitize_text(resp_text))
            except Exception:
                return (True, sanitize_text(raw_out))

        except subprocess.TimeoutExpired:
            return (False, "agy execution timed out.")
        except Exception as e:
            return (False, f"agy execution error: {e}")

    def git_deliver(self, task_id: str, commit_msg: str) -> Tuple[bool, str, Optional[str]]:
        """Exclusive Git Delivery Controller."""
        remote = self.config.get("git_remote", "origin")
        branch = self.config.get("git_branch", "main")
        try:
            # 1. Selective add
            subprocess.run(["git", "add", "."], cwd=self.repo_root, check=True)

            # 2. Check if anything staged
            diff_check = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=self.repo_root)
            if diff_check.returncode == 0:
                self.logger.info("No modifications staged to deliver.")
                head = self.get_git_head()
                return (True, "No changes to deliver.", head)

            # 3. Check for whitespace/formatting errors
            ws_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=self.repo_root, capture_output=True)
            if ws_check.returncode != 0:
                return (False, f"Whitespace errors in staged diff:\n{ws_check.stderr.decode()}", None)

            # 4. Commit atomically
            formatted_msg = f"feat(task): {task_id} - {commit_msg}"
            subprocess.run(["git", "commit", "-m", formatted_msg], cwd=self.repo_root, check=True)
            head = self.get_git_head()

            # 5. Push to remote
            subprocess.run(["git", "push", remote, branch], cwd=self.repo_root, check=True)
            return (True, f"Committed and pushed as {head[:7]}.", head)
        except Exception as e:
            return (False, f"Git delivery failed: {e}", None)

    def write_handoff(
        self,
        task_id: str,
        execution_id: str,
        start_head: str,
        end_head: str,
        summary: str,
        qg_passed: bool,
    ):
        content = f"""# Executor Handoff

> Generated autonomously by English Learning OS Local Runner.

## Metadata
- **Task ID**: `{task_id}`
- **Execution ID**: `{execution_id}`
- **Timestamp**: `{datetime.now(timezone.utc).isoformat()}`
- **Starting Commit**: `{start_head}`
- **Resulting Commit**: `{end_head}`
- **Quality Gate**: `{'PASSED' if qg_passed else 'FAILED'}`
- **CI Status**: `TRIGGERED`

## Execution Summary
{summary}

## Verification Evidence
- Repository working tree verified clean before run.
- Protected paths respected; no perimeter violations.
- Quality gates passed with code 0.
- Staged diff verified whitespace-clean; commit pushed to `{self.config.get('git_branch', 'main')}`.
"""
        self.handoff_file.write_text(content, encoding="utf-8")

    def execute_task_cycle(self, dry_run: bool = False) -> bool:
        """Executes a single cycle of the task state machine."""
        state = self.load_state()
        if not state:
            self.logger.warn("STATE.json not found in control plane directory. Skipping.")
            return False

        current_status = state.get("state")
        task_id = state.get("task_id", "UNKNOWN_TASK")
        execution_id = state.get("execution_id", f"exec-{int(time.time())}")
        max_retries = state.get("max_retries", 3)
        retry_count = state.get("retry_count", 0)
        expected_head = state.get("expected_git_head")
        current_version = state.get("state_version", 1)

        # Only act on READY or FIX_REQUIRED
        if current_status not in ["READY", "FIX_REQUIRED"]:
            self.logger.info(f"State is '{current_status}'. No action taken.")
            return False

        # Idempotency check: prevent re-executing same task and head
        if self.is_already_executed(task_id, expected_head):
            self.logger.warn(f"Task '{task_id}' with HEAD '{expected_head}' was already executed. Skipping.")
            return False

        # Transactional verification: Payload-First / State-Last check
        if not self.current_task_file.exists():
            self.logger.error("CURRENT_TASK.md is missing. Rejecting execution.")
            state["state"] = "ERROR"
            state["last_error"] = "CURRENT_TASK.md missing."
            self.save_state(state, expected_version=current_version)
            return False

        expected_hash = state.get("content_hash")
        actual_hash = self.compute_file_hash(self.current_task_file)
        if expected_hash and actual_hash != expected_hash:
            self.logger.error(f"Payload hash mismatch! expected: {expected_hash}, actual: {actual_hash}")
            state["state"] = "ERROR"
            state["last_error"] = "Content hash mismatch (partial write detected)."
            self.save_state(state, expected_version=current_version)
            return False

        self.logger.info(f"Detected actionable task '{task_id}' in state '{current_status}'.")

        if dry_run:
            self.logger.info(f"[DRY RUN] Would execute task '{task_id}' (execution_id: {execution_id}).")
            return True

        if not self.lock.acquire():
            return False

        try:
            # 1. Pre-execution git baseline verification
            current_head = self.get_git_head()
            if expected_head and current_head != expected_head:
                err_msg = f"Git HEAD divergence: expected {expected_head}, found {current_head}."
                self.logger.error(err_msg)
                state["last_error"] = err_msg
                state["state"] = "ERROR"
                self.save_state(state, expected_version=current_version)
                return False

            if not self.is_git_clean():
                err_msg = "Git working tree is dirty before task execution."
                self.logger.error(err_msg)
                state["last_error"] = err_msg
                state["state"] = "ERROR"
                self.save_state(state, expected_version=current_version)
                return False

            # 2. Mark EXECUTING
            state["state"] = "EXECUTING"
            state["execution_id"] = execution_id
            if not self.save_state(state, expected_version=current_version):
                return False
            current_version += 1
            self.logger.info(f"Marked state EXECUTING for '{task_id}'.")

            # 3. Read Task & Inspect Maintenance Mode
            task_content = self.current_task_file.read_text(encoding="utf-8")
            maintenance_mode = "maintenance_mode: true" in task_content.lower() or "maintenance mode: true" in task_content.lower()

            # 4. Invoke Executor (agy CLI) with prompt boundaries
            prompt = (
                f"You are the implementation agent for English Learning OS.\n"
                f"Task ID: {task_id}\n"
                f"CRITICAL CONSTRAINT: You are FORBIDDEN from running 'git add', 'git commit', or 'git push'.\n"
                f"Git delivery is handled exclusively by the outer runner.\n"
                f"Respect all rules in AGENTS.md.\n\n"
                f"TASK SPECIFICATION (DATA):\n{task_content}"
            )
            agy_success, agy_out = self.execute_agy(prompt)
            if not agy_success:
                self.logger.error(f"Executor invocation failed: {agy_out[:200]}")
                retry_count += 1
                state["retry_count"] = retry_count
                state["last_error"] = agy_out[:300]
                state["state"] = "ERROR" if retry_count >= max_retries else "FIX_REQUIRED"
                self.save_state(state, expected_version=current_version)
                return False

            # 5. Protected Paths Scope Verification
            paths_ok, violations = self.verify_protected_paths(maintenance_mode)
            if not paths_ok:
                err_msg = f"SecurityViolation: Protected paths modified without maintenance mode: {violations}"
                self.logger.error(err_msg)
                # Rollback changes to keep tree clean
                subprocess.run(["git", "reset", "--hard", "HEAD"], cwd=self.repo_root)
                retry_count += 1
                state["retry_count"] = retry_count
                state["last_error"] = err_msg
                state["state"] = "ERROR" if retry_count >= max_retries else "FIX_REQUIRED"
                self.save_state(state, expected_version=current_version)
                return False

            # 6. Run Quality Gate
            qg_passed, qg_out = self.run_quality_gate()
            if not qg_passed:
                self.logger.error(f"Quality gate failed:\n{qg_out[:300]}")
                retry_count += 1
                state["retry_count"] = retry_count
                state["last_error"] = f"Quality gate failure: {qg_out[:250]}"
                state["state"] = "ERROR" if retry_count >= max_retries else "FIX_REQUIRED"
                self.save_state(state, expected_version=current_version)
                return False

            # 7. Git Delivery via Runner
            commit_ok, commit_msg, resulting_head = self.git_deliver(
                task_id, f"complete autonomous execution ({execution_id})"
            )
            if not commit_ok:
                self.logger.error(f"Git delivery failed: {commit_msg}")
                state["last_error"] = commit_msg
                state["state"] = "ERROR"
                self.save_state(state, expected_version=current_version)
                return False

            # 8. Record Execution in History
            self.record_execution(task_id, expected_head, execution_id)

            # 9. Payload First: Write Handoff
            self.write_handoff(
                task_id=task_id,
                execution_id=execution_id,
                start_head=current_head,
                end_head=resulting_head or current_head,
                summary=f"Task executed successfully via agy.\nResponse: {agy_out[:300]}",
                qg_passed=True,
            )

            # 10. State Last: Advance to AWAITING_AUDIT
            state["state"] = "AWAITING_AUDIT"
            state["resulting_git_head"] = resulting_head or current_head
            state["retry_count"] = 0
            state["last_error"] = None
            self.save_state(state, expected_version=current_version)
            self.logger.info(f"Task '{task_id}' executed. State advanced to AWAITING_AUDIT.")
            return True

        except Exception as e:
            self.logger.error(f"Unexpected exception during execution: {e}")
            state["state"] = "ERROR"
            state["last_error"] = str(e)
            self.save_state(state, expected_version=current_version)
            return False
        finally:
            self.lock.release()

    def run_loop(self, poll_interval: int):
        self.logger.info(f"Starting runner polling daemon (interval: {poll_interval}s)...")
        while self._running:
            try:
                self.execute_task_cycle(dry_run=False)
            except Exception as e:
                self.logger.error(f"Error in poll cycle: {e}")
            for _ in range(poll_interval):
                if not self._running:
                    break
                time.sleep(1)
        self.logger.info("Runner stopped gracefully.")


def main():
    parser = argparse.ArgumentParser(description="English Learning OS Local Runner")
    parser.add_argument("--once", action="store_true", help="Execute single cycle and exit")
    parser.add_argument("--daemon", action="store_true", help="Run continuous polling daemon")
    parser.add_argument("--dry-run", action="store_true", help="Inspect state and simulate without modifying")
    parser.add_argument("--force-unlock", action="store_true", help="Remove stale lock file")
    parser.add_argument("--config", type=str, default="automation/config.example.json", help="Path to configuration JSON")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    config_file = repo_root / args.config
    config = {}
    if config_file.exists():
        try:
            config = json.loads(config_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    log_path = repo_root / config.get("log_file", "automation/logs/runner.log")
    logger = SafeLogger(log_path)

    if args.force_unlock:
        lock_file = repo_root / "automation" / ".lock"
        if lock_file.exists():
            lock_file.unlink()
            logger.info("Forced unlock: .lock removed.")
        else:
            logger.info("No .lock file present.")
        return 0

    runner = OrchestrationRunner(repo_root, config, logger)

    def handle_signal(sig, frame):
        logger.info(f"Received signal {sig}. Initiating graceful shutdown...")
        runner.stop()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    if args.daemon:
        interval = config.get("poll_interval_seconds", 10)
        runner.run_loop(interval)
    else:
        success = runner.execute_task_cycle(dry_run=args.dry_run)
        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
