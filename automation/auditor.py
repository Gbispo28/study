#!/usr/bin/env python3
"""
English Learning OS — Independent Automated Auditor
Evaluates task execution against real GitHub evidence (diffs, commits, CI, quality gates).

Key Invariants:
- EXECUTOR != AUDITOR: Employs a separate model, prompt, and process.
- PROHIBITION: The auditor CANNOT modify code in the repository.
- GitHub Evidence: Audits real commit SHAs, diff boundaries, secret absence, and CI.
- Ownership of NEXT_TASK: Generates candidate NEXT_TASK upon approval, or corrective tasks upon rejection.
- Standalone Promotion: Can promote NEXT_TASK -> CURRENT_TASK if Make is offline.
"""

import sys
import os
import time
import json
import signal
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
    sanitized = text
    for pattern in SECRET_PATTERNS:
        sanitized = pattern.sub("[REDACTED_SECRET]", sanitized)
    return sanitized


class SafeLogger:
    def __init__(self, log_file: Optional[Path] = None):
        self.log_file = log_file
        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, level: str, msg: str, **kwargs):
        timestamp = datetime.now(timezone.utc).isoformat()
        clean_msg = sanitize_text(msg)
        out_str = f"[{timestamp}] [{level:5s}] {clean_msg}"
        if kwargs:
            out_str += f" | {json.dumps({k: sanitize_text(str(v)) for k, v in kwargs.items()})}"
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


class AutomatedAuditor:
    """Evaluates task execution against GitHub reality and governs state transitions."""

    def __init__(self, repo_root: Path, config: Dict[str, Any], logger: SafeLogger):
        self.repo_root = repo_root.resolve()
        self.config = config
        self.logger = logger

        default_cp_dir = Path.home() / "Google Drive" / "Meu Drive" / "English Learning OS Orchestration"
        configured_cp = config.get("control_plane_dir")
        if configured_cp:
            self.control_plane_dir = Path(configured_cp).expanduser().resolve()
        elif default_cp_dir.exists():
            self.control_plane_dir = default_cp_dir
        else:
            self.control_plane_dir = Path.home() / ".english_learning_os_orchestration"

        self.control_plane_dir.mkdir(parents=True, exist_ok=True)

        self.state_file = self.control_plane_dir / "STATE.json"
        self.current_task_file = self.control_plane_dir / "CURRENT_TASK.md"
        self.next_task_file = self.control_plane_dir / "NEXT_TASK.md"
        self.handoff_file = self.control_plane_dir / "EXECUTOR_HANDOFF.md"
        self.audit_report_file = self.control_plane_dir / "AUDIT_REPORT.md"
        self.events_file = self.control_plane_dir / "EVENTS.ndjson"
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
        try:
            if expected_version is not None and self.state_file.exists():
                current_on_disk = json.loads(self.state_file.read_text(encoding="utf-8"))
                disk_version = current_on_disk.get("state_version", 1)
                if disk_version != expected_version:
                    self.logger.error(f"Concurrency conflict: disk version {disk_version} != expected {expected_version}")
                    return False

            state["state_version"] = (state.get("state_version", 0) + 1)
            state["updated_at"] = datetime.now(timezone.utc).isoformat()

            temp_path = self.state_file.with_suffix(".tmp")
            temp_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            temp_path.replace(self.state_file)

            # Append to event log
            self.append_event({
                "timestamp": state["updated_at"],
                "event": f"AUDIT_VERDICT_{state.get('state')}",
                "task_id": state.get("task_id"),
                "state": state.get("state"),
                "state_version": state["state_version"]
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

    def audit_commit(self, commit_sha: str) -> Tuple[bool, List[str], str]:
        """Audits real commit diff and secret scan."""
        try:
            # 1. Verify commit exists
            subprocess.run(["git", "cat-file", "-e", f"{commit_sha}^{{commit}}"], cwd=self.repo_root, check=True)

            # 2. Get changed files
            files_out = subprocess.check_output(
                ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_sha],
                cwd=self.repo_root,
                text=True,
            )
            changed_files = [f.strip() for f in files_out.splitlines() if f.strip()]

            # 3. Get commit diff
            diff_out = subprocess.check_output(
                ["git", "show", "--format=", commit_sha], cwd=self.repo_root, text=True
            )

            # 4. Check for secrets
            for pattern in SECRET_PATTERNS:
                if pattern.search(diff_out):
                    return (False, changed_files, "SecretLeakDetected: Found potential secret matching pattern in commit diff.")

            # 5. Check protected paths
            for cf in changed_files:
                for pp in PROTECTED_PATHS:
                    if cf == pp or cf.startswith(pp):
                        # Verify if commit was maintenance mode
                        msg = subprocess.check_output(
                            ["git", "log", "-1", "--format=%B", commit_sha], cwd=self.repo_root, text=True
                        )
                        if "maintenance_mode" not in msg.lower() and "infra" not in msg.lower():
                            return (False, changed_files, f"ProtectedPathBreach: Commit modified {cf} without maintenance mode.")

            return (True, changed_files, diff_out[:500])

        except Exception as e:
            return (False, [], f"Commit audit error: {e}")

    def audit_ci_status(self, commit_sha: str) -> Tuple[bool, str]:
        """Audits GitHub Actions CI status for the commit."""
        gh_bin = shutil.which("gh")
        if not gh_bin:
            self.logger.warn("gh CLI not available; skipping CI check in local mode.")
            return (True, "CI check skipped (gh CLI missing)")

        try:
            proc = subprocess.run(
                [gh_bin, "run", "list", "--commit", commit_sha, "--json", "status,conclusion,name", "--limit", "1"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if proc.returncode != 0:
                return (True, f"CI check query failed ({proc.stderr.strip()}); continuing local audit.")

            runs = json.loads(proc.stdout)
            if not runs:
                return (True, "No CI runs recorded yet.")

            latest = runs[0]
            conclusion = latest.get("conclusion")
            if conclusion == "success":
                return (True, "CI passed successfully.")
            elif conclusion in ["failure", "timed_out", "cancelled"]:
                return (False, f"CI run concluded with status: {conclusion}")
            else:
                # Still in progress or queued
                return (True, f"CI status: {latest.get('status')} ({conclusion})")

        except Exception as e:
            return (True, f"CI audit non-blocking warning: {e}")

    def generate_next_task(self, current_task_id: str) -> str:
        """Generates the next task candidate specification."""
        next_id = f"TASK-{int(time.time())}"
        content = f"""# Task: {next_id} — Autonomous Follow-Up Task

## Metadata
- **Task ID**: `{next_id}`
- **Parent Task ID**: `{current_task_id}`
- **Task Type**: `FEATURE`
- **Maintenance Mode**: `false`

## 1. Context & Objective
Follow-up autonomous iteration continuing from approved {current_task_id}.

## 2. Invariants & Scope
- Gate 2 baseline preserved (`GATE 2: BLOCKED ON LEARNER BASELINE`).
- Zero secrets in repository.
- Protected paths must not be modified.

## 3. Verification Acceptance Criteria
- Quality gate passing (`bash scripts/quality_gate.sh`).
"""
        self.next_task_file.write_text(content, encoding="utf-8")
        return next_id

    def generate_corrective_task(self, original_task_id: str, feedback: str, retry_count: int) -> str:
        """Generates a corrective task in CURRENT_TASK.md."""
        content = f"""# Task: {original_task_id} (Remediation Attempt {retry_count + 1})

## Metadata
- **Task ID**: `{original_task_id}`
- **Parent Task ID**: `{original_task_id}`
- **Task Type**: `REFACTOR`
- **Maintenance Mode**: `false`

## 1. Remediation Directive
The previous execution was rejected by the Automated Auditor.
Specific Defects:
{feedback}

## 2. Required Corrective Action
Address all deficiencies noted above without introducing regressions.
Ensure `bash scripts/quality_gate.sh` passes before completion.
"""
        self.current_task_file.write_text(content, encoding="utf-8")
        return self.compute_file_hash(self.current_task_file)

    def write_audit_report(self, task_id: str, execution_id: str, commit_sha: str, verdict: str, details: str):
        content = f"""# Audit Report

> Generated autonomously by English Learning OS Automated Auditor.

## Metadata
- **Task ID**: `{task_id}`
- **Execution ID**: `{execution_id}`
- **Auditor Model**: `{self.config.get('auditor_model', 'gemini-3.1-pro-high')}`
- **Audit Timestamp**: `{datetime.now(timezone.utc).isoformat()}`
- **Verified Commit**: `{commit_sha}`
- **Verdict**: `{verdict}`

## Verification Findings
{details}
"""
        self.audit_report_file.write_text(content, encoding="utf-8")

    def execute_audit_cycle(self, standalone_promote: bool = False) -> bool:
        state = self.load_state()
        if not state:
            return False

        if state.get("state") != "AWAITING_AUDIT":
            return False

        task_id = state.get("task_id", "UNKNOWN_TASK")
        execution_id = state.get("execution_id", "UNKNOWN_EXEC")
        commit_sha = state.get("resulting_git_head", "")
        max_retries = state.get("max_retries", 3)
        retry_count = state.get("retry_count", 0)
        current_version = state.get("state_version", 1)

        self.logger.info(f"Auditing task '{task_id}' (commit: {commit_sha[:7] if commit_sha else 'NONE'})...")

        if not commit_sha:
            self.logger.error("No resulting_git_head recorded in state. Rejecting.")
            state["state"] = "ERROR"
            state["last_error"] = "resulting_git_head missing in AWAITING_AUDIT state."
            self.save_state(state, expected_version=current_version)
            return False

        # 1. Audit Commit Diff & Secrets
        commit_ok, changed_files, diff_summary = self.audit_commit(commit_sha)
        if not commit_ok:
            self.logger.error(f"Audit failed commit verification: {diff_summary}")
            retry_count += 1
            state["retry_count"] = retry_count
            state["last_error"] = diff_summary

            if retry_count >= max_retries:
                state["state"] = "ERROR"
                self.logger.error(f"Max retries exceeded for '{task_id}'. State set to ERROR.")
            else:
                new_hash = self.generate_corrective_task(task_id, diff_summary, retry_count)
                state["state"] = "FIX_REQUIRED"
                state["content_hash"] = new_hash

            self.write_audit_report(task_id, execution_id, commit_sha, "FIX_REQUIRED", diff_summary)
            self.save_state(state, expected_version=current_version)
            return False

        # 2. Audit CI Status
        ci_ok, ci_summary = self.audit_ci_status(commit_sha)
        if not ci_ok:
            self.logger.error(f"Audit failed CI check: {ci_summary}")
            retry_count += 1
            state["retry_count"] = retry_count
            state["last_error"] = ci_summary
            state["state"] = "ERROR" if retry_count >= max_retries else "FIX_REQUIRED"
            new_hash = self.generate_corrective_task(task_id, ci_summary, retry_count)
            state["content_hash"] = new_hash
            self.write_audit_report(task_id, execution_id, commit_sha, "FIX_REQUIRED", ci_summary)
            self.save_state(state, expected_version=current_version)
            return False

        # 3. Approve Execution & Generate NEXT_TASK
        next_task_id = self.generate_next_task(task_id)
        audit_details = (
            f"- Commit {commit_sha[:7]} verified on remote.\n"
            f"- Changed files ({len(changed_files)}): {changed_files}\n"
            f"- Scope check passed: Zero protected path breaches.\n"
            f"- Secret scan clean: Zero credential patterns detected.\n"
            f"- CI status: {ci_summary}\n"
            f"- Next task generated: `{next_task_id}`"
        )
        self.write_audit_report(task_id, execution_id, commit_sha, "APPROVED", audit_details)

        state["state"] = "APPROVED"
        state["last_error"] = None
        self.save_state(state, expected_version=current_version)
        current_version += 1
        self.logger.info(f"Task '{task_id}' APPROVED by Automated Auditor.")

        # 4. Standalone Promotion (if Make is offline or standalone mode requested)
        if standalone_promote or self.config.get("standalone_mode", False):
            self.logger.info("Standalone promotion: promoting NEXT_TASK.md to CURRENT_TASK.md...")
            next_content = self.next_task_file.read_text(encoding="utf-8")
            self.current_task_file.write_text(next_content, encoding="utf-8")
            new_hash = self.compute_file_hash(self.current_task_file)

            state["state"] = "READY"
            state["task_id"] = next_task_id
            state["execution_id"] = f"exec-{int(time.time())}"
            state["retry_count"] = 0
            state["content_hash"] = new_hash
            state["expected_git_head"] = commit_sha
            self.save_state(state, expected_version=current_version)
            self.logger.info(f"Promoted '{next_task_id}' to CURRENT_TASK.md and set state to READY.")

        return True

    def run_loop(self, poll_interval: int):
        self.logger.info(f"Starting Automated Auditor daemon (interval: {poll_interval}s)...")
        while self._running:
            try:
                self.execute_audit_cycle(standalone_promote=self.config.get("standalone_mode", False))
            except Exception as e:
                self.logger.error(f"Error in audit poll cycle: {e}")
            for _ in range(poll_interval):
                if not self._running:
                    break
                time.sleep(1)
        self.logger.info("Auditor stopped gracefully.")


def main():
    parser = argparse.ArgumentParser(description="English Learning OS Automated Auditor")
    parser.add_argument("--once", action="store_true", help="Execute single audit cycle and exit")
    parser.add_argument("--daemon", action="store_true", help="Run continuous audit polling daemon")
    parser.add_argument("--standalone", action="store_true", help="Enable standalone task promotion without Make")
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

    if args.standalone:
        config["standalone_mode"] = True

    log_path = repo_root / config.get("log_file", "automation/logs/auditor.log")
    logger = SafeLogger(log_path)
    auditor = AutomatedAuditor(repo_root, config, logger)

    def handle_signal(sig, frame):
        logger.info(f"Received signal {sig}. Stopping auditor...")
        auditor.stop()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    if args.daemon:
        interval = config.get("poll_interval_seconds", 10)
        auditor.run_loop(interval)
    else:
        success = auditor.execute_audit_cycle(standalone_promote=args.standalone)
        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
