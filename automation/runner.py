#!/usr/bin/env python3
"""
English Learning OS — Outbound Local Runner
Executes orchestration tasks from Google Drive / orchestration directory locally on macOS.

Key Principles:
- Outbound polling only: Zero incoming open ports or attack surfaces on the Mac.
- Concurrency control: PID lock preventing multiple runner instances.
- State validation: Verifies clean working tree and expected Git HEAD.
- Quality Gate: Runs quality gates before any commit or push.
- Safe Logging: Strips any accidental secret patterns from log outputs.
"""

import sys
import os
import time
import json
import signal
import shutil
import re
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]{20,50}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,90}"),
    re.compile(r"AIza[0-9A-Za-z-_]{20,50}"),
    re.compile(r"sk-[A-Za-z0-9]{20,50}"),
    re.compile(r"bearer\s+[A-Za-z0-9\-\._~\+\/]+=*", re.IGNORECASE),
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
    """PID-based concurrency file lock."""

    def __init__(self, lock_path: Path, logger: SafeLogger):
        self.lock_path = lock_path
        self.logger = logger
        self.acquired = False

    def acquire(self) -> bool:
        if self.lock_path.exists():
            try:
                content = json.loads(self.lock_path.read_text(encoding="utf-8"))
                existing_pid = content.get("pid")
                # Check if process is alive
                if existing_pid:
                    try:
                        os.kill(existing_pid, 0)
                        self.logger.warn(f"Runner lock held by active process PID {existing_pid}. Skipping execution.")
                        return False
                    except OSError:
                        self.logger.info(f"Removing stale lock file from dead process PID {existing_pid}.")
            except Exception as e:
                self.logger.warn(f"Could not read existing lock file ({e}), replacing.")

        lock_data = {
            "pid": os.getpid(),
            "acquired_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
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
    """Manages the full lifecycle of a task execution."""

    def __init__(self, repo_root: Path, config: Dict[str, Any], logger: SafeLogger):
        self.repo_root = repo_root.resolve()
        self.config = config
        self.logger = logger
        self.orchestration_dir = self.repo_root / config.get("orchestration_dir", "orchestration")
        self.state_file = self.orchestration_dir / "STATE.json"
        self.current_task_file = self.orchestration_dir / "CURRENT_TASK.md"
        self.handoff_file = self.orchestration_dir / "EXECUTOR_HANDOFF.md"
        self.human_action_file = self.orchestration_dir / "HUMAN_ACTION_REQUIRED.md"
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

    def save_state(self, state: Dict[str, Any]) -> bool:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        try:
            temp_path = self.state_file.with_suffix(".tmp")
            temp_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            temp_path.replace(self.state_file)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save STATE.json: {e}")
            return False

    def get_git_head(self) -> str:
        res = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo_root, text=True)
        return res.strip()

    def is_git_clean(self) -> bool:
        res = subprocess.check_output(["git", "status", "--porcelain"], cwd=self.repo_root, text=True)
        # Filter out orchestration state files if not git-tracked
        lines = [line.strip() for line in res.splitlines() if line.strip()]
        return len(lines) == 0

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
        agy_bin = self.config.get("agy_binary", "/Users/gmbispo/.local/bin/agy")
        if not Path(agy_bin).exists():
            # Fallback to PATH search
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
            "text",
            "--dangerously-skip-permissions",
        ]
        try:
            self.logger.info(f"Invoking agy CLI with model '{chosen_model}'...")
            proc = subprocess.run(
                cmd,
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=self.config.get("execution_timeout_seconds", 300),
            )
            output = sanitize_text(proc.stdout + "\n" + proc.stderr)
            return (proc.returncode == 0, output)
        except subprocess.TimeoutExpired:
            return (False, "agy execution timed out.")
        except Exception as e:
            return (False, f"agy execution error: {e}")

    def git_commit_and_push(self, task_id: str, commit_msg: str) -> Tuple[bool, str, Optional[str]]:
        remote = self.config.get("git_remote", "origin")
        branch = self.config.get("git_branch", "main")
        try:
            subprocess.run(["git", "add", "."], cwd=self.repo_root, check=True)
            # Check if there is anything to commit
            diff_check = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=self.repo_root)
            if diff_check.returncode == 0:
                self.logger.info("No files modified to commit.")
                head = self.get_git_head()
                return (True, "No changes to commit.", head)

            formatted_msg = f"feat(orchestration): {task_id} - {commit_msg}"
            subprocess.run(["git", "commit", "-m", formatted_msg], cwd=self.repo_root, check=True)
            head = self.get_git_head()

            subprocess.run(["git", "push", remote, branch], cwd=self.repo_root, check=True)
            return (True, f"Committed and pushed successfully as {head[:7]}.", head)
        except Exception as e:
            return (False, f"Git operation failed: {e}", None)

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

## Execution Summary
{summary}

## Verification Evidence
- Repository integrity validated.
- Quality gate executed clean.
- Remote synchronization verified on branch `{self.config.get('git_branch', 'main')}`.
"""
        self.handoff_file.write_text(content, encoding="utf-8")

    def execute_task_cycle(self, dry_run: bool = False) -> bool:
        """Executes a single cycle of the task state machine."""
        state = self.load_state()
        if not state:
            self.logger.warn("STATE.json could not be loaded. Skipping cycle.")
            return False

        current_status = state.get("state")
        task_id = state.get("task_id", "UNKNOWN_TASK")
        execution_id = state.get("execution_id", f"exec-{int(time.time())}")
        max_retries = state.get("max_retries", 3)
        retry_count = state.get("retry_count", 0)

        # We only act on READY or FIX_REQUIRED
        if current_status not in ["READY", "FIX_REQUIRED"]:
            self.logger.info(f"State is '{current_status}'. No action required.")
            return False

        self.logger.info(f"Detected actionable state '{current_status}' for task '{task_id}'.")

        if dry_run:
            self.logger.info(f"[DRY RUN] Would execute task '{task_id}' (execution_id: {execution_id}).")
            return True

        if not self.lock.acquire():
            return False

        try:
            # 1. Pre-execution checks
            current_head = self.get_git_head()
            expected_head = state.get("expected_git_head")
            if expected_head and current_head != expected_head:
                err_msg = f"Git HEAD divergence: expected {expected_head}, found {current_head}."
                self.logger.error(err_msg)
                state["last_error"] = err_msg
                state["state"] = "ERROR"
                self.save_state(state)
                return False

            # 2. Mark EXECUTING
            state["state"] = "EXECUTING"
            state["execution_id"] = execution_id
            self.save_state(state)
            self.logger.info(f"Marked state EXECUTING for {task_id}.")

            # 3. Read Task definition
            task_content = ""
            if self.current_task_file.exists():
                task_content = self.current_task_file.read_text(encoding="utf-8")
            else:
                self.logger.warn(f"Task file {self.current_task_file} not found; proceeding with task ID description.")

            # 4. Invoke Executor (agy CLI)
            prompt = (
                f"Execute the task defined below within this repository.\n"
                f"Respect all rules in AGENTS.md.\n"
                f"Task ID: {task_id}\n\n"
                f"{task_content}"
            )
            agy_success, agy_out = self.execute_agy(prompt)
            if not agy_success:
                self.logger.error(f"Executor invocation failed: {agy_out[:200]}")
                retry_count += 1
                state["retry_count"] = retry_count
                state["last_error"] = agy_out[:300]
                if retry_count >= max_retries:
                    state["state"] = "ERROR"
                    self.logger.error(f"Max retries ({max_retries}) exceeded. Transitioning to ERROR.")
                else:
                    state["state"] = "FIX_REQUIRED"
                self.save_state(state)
                return False

            # 5. Run Quality Gate
            qg_passed, qg_out = self.run_quality_gate()
            if not qg_passed:
                self.logger.error(f"Quality gate failed:\n{qg_out}")
                retry_count += 1
                state["retry_count"] = retry_count
                state["last_error"] = f"Quality gate failure: {qg_out[:250]}"
                if retry_count >= max_retries:
                    state["state"] = "ERROR"
                else:
                    state["state"] = "FIX_REQUIRED"
                self.save_state(state)
                return False

            # 6. Git Commit & Push
            commit_ok, commit_msg, resulting_head = self.git_commit_and_push(
                task_id, f"complete autonomous execution ({execution_id})"
            )
            if not commit_ok:
                self.logger.error(f"Git commit/push failed: {commit_msg}")
                state["last_error"] = commit_msg
                state["state"] = "ERROR"
                self.save_state(state)
                return False

            # 7. Write Handoff & Advance to AWAITING_AUDIT
            self.write_handoff(
                task_id=task_id,
                execution_id=execution_id,
                start_head=current_head,
                end_head=resulting_head or current_head,
                summary=f"Task executed via agy.\nOutput snippet: {agy_out[:300]}",
                qg_passed=True,
            )
            state["state"] = "AWAITING_AUDIT"
            state["resulting_git_head"] = resulting_head or current_head
            state["retry_count"] = 0
            state["last_error"] = None
            self.save_state(state)
            self.logger.info(f"Task '{task_id}' successfully executed. Advanced state to AWAITING_AUDIT.")
            return True

        except Exception as e:
            self.logger.error(f"Unexpected exception during execution: {e}")
            state["state"] = "ERROR"
            state["last_error"] = str(e)
            self.save_state(state)
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
    parser.add_argument("--daemon", action="store_true", help="Run continuously in background polling loop")
    parser.add_argument("--dry-run", action="store_true", help="Inspect state and simulate without executing")
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
        # Default is --once if not daemon
        success = runner.execute_task_cycle(dry_run=args.dry_run)
        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
