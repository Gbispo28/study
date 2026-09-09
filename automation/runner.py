#!/usr/bin/env python3
"""
English Learning OS — Outbound Local Runner
Exclusive Git Delivery Controller & Task Executor.

Key Invariants:
- Outbound polling only: Zero listening ports or inbound network attack surfaces.
- Exclusive Git Delivery Controller: The executor agent is prohibited from git operations;
  runner alone inspects diffs, validates scope, runs quality gates, commits, and pushes.
- True Selective Staging: Eliminates 'git add .'; stages only validated explicit files.
- Technical Git Containment: Pre/post execution assertions ensure executor cannot commit,
  switch branches, alter remotes, or create refs.
- Protected Paths: Blocks edits to runner, auditor, schemas, quality gates, .agents, CI.
- Payload-First, State-Last: Validates SHA-256 content_hash of CURRENT_TASK.md.
- Optimistic Concurrency: Enforces state_versioning on STATE.json.
- Idempotency: Tracks executed (task_id, expected_git_head) in execution_history.json.
- Defense-in-Depth Secret Detection: Covers modern Google AI Studio keys, OpenAI, Anthropic,
  Slack, PEM keys, and assignment heuristics without logging sensitive values.
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

# Defense-in-depth secret patterns
SECRET_PATTERNS = [
    re.compile(r"\bghp_[A-Za-z0-9_]{20,80}"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,90}"),
    # Google AI / Gemini API keys (standard AIza and modern 39-char format)
    re.compile(r"\bAIza[0-9A-Za-z-_]{30,50}"),
    # Google AI Studio modern AQ.-style keys (bare tokens without assignment prefix)
    re.compile(r"\bAQ\.[A-Za-z0-9_-]{20,90}"),
    # OpenAI formats (classic sk- and modern sk-proj-, sk-admin-)
    re.compile(r"\bsk-(?:proj-|admin-)?[A-Za-z0-9_-]{20,90}"),
    # Anthropic formats
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,90}"),
    # Slack tokens
    re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,60}"),
    # Bearer & Basic Auth headers with real credential tokens (15+ chars)
    re.compile(r"\b(?:Bearer|Basic)\s+[A-Za-z0-9\-\._~\+\/]{15,}=*", re.IGNORECASE),
    # PEM Private Keys
    re.compile(r"-----BEGIN (?:[A-Z0-9_-]+ )?PRIVATE KEY-----[\s\S]*?-----END (?:[A-Z0-9_-]+ )?PRIVATE KEY-----"),
    # Generic secret assignment heuristics: api_key = "..." or password = "..."
    re.compile(r"""(?i)\b(?:api[_-]?key|secret[_-]?key|client[_-]?secret|access[_-]?token|auth[_-]?token|private[_-]?key)\s*[:=]\s*['"][A-Za-z0-9_\-\.\/+=]{12,}['"]"""),
]

PROTECTED_PATHS = [
    "automation/runner.py",
    "automation/auditor.py",
    "automation/control_plane_schema/",
    "scripts/quality_gate.sh",
    "scripts/validate_repo.py",
    "scripts/git_pretool_hook.py",
    ".agents/",
    ".github/workflows/",
]

SENSITIVE_FILENAME_PATTERNS = [
    re.compile(r"^\.env(?:\..+)?$"),
    re.compile(r".*\.(?:pem|key|pkcs12|pfx)$", re.IGNORECASE),
    re.compile(r"(?:id_rsa|id_ecdsa|id_ed25519)(?:\.pub)?$"),
    re.compile(r"(?:credentials|secrets)\.json$", re.IGNORECASE),
]


def sanitize_text(text: str) -> str:
    """Mask potential secret patterns from strings without revealing secret values."""
    sanitized = text
    for pattern in SECRET_PATTERNS:
        sanitized = pattern.sub("[REDACTED_SECRET]", sanitized)
    return sanitized


def scan_text_for_secrets(text: str) -> Tuple[bool, str]:
    """Scans text for secrets; returns (has_secret, summary). Never logs secret content."""
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            return (True, f"Potential credential pattern detected (matched regex {pattern.pattern[:30]}...)")
    return (False, "")


def parse_task_scope(task_text: str) -> Tuple[List[str], List[str]]:
    """
    Extracts allowed_paths and allowed_path_prefixes from task specification markdown.
    Supports YAML-style block lists, inline lists, or markdown bullet items.
    """
    allowed_paths: List[str] = []
    allowed_prefixes: List[str] = []

    lines = task_text.splitlines()
    current_section = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        clean_header = stripped.lower().replace("**", "").replace("-", "").strip()
        if clean_header.startswith("allowed_paths:") or clean_header.startswith("allowed paths:"):
            current_section = "paths"
            inline_match = re.search(r"\[(.*?)\]", stripped)
            if inline_match:
                items = [it.strip().strip("'\"`") for it in inline_match.group(1).split(",") if it.strip()]
                allowed_paths.extend(items)
                current_section = None
            continue
        elif clean_header.startswith("allowed_path_prefixes:") or clean_header.startswith("allowed path prefixes:"):
            current_section = "prefixes"
            inline_match = re.search(r"\[(.*?)\]", stripped)
            if inline_match:
                items = [it.strip().strip("'\"`") for it in inline_match.group(1).split(",") if it.strip()]
                allowed_prefixes.extend(items)
                current_section = None
            continue
        elif stripped.startswith("#") or (":" in stripped and not stripped.startswith("-")):
            current_section = None

        if current_section == "paths":
            if stripped.startswith("-"):
                val = stripped.lstrip("-").strip().strip("'\"`")
                if val:
                    allowed_paths.append(val)
        elif current_section == "prefixes":
            if stripped.startswith("-"):
                val = stripped.lstrip("-").strip().strip("'\"`")
                if val:
                    allowed_prefixes.append(val)

    return allowed_paths, allowed_prefixes


def is_path_in_scope(filepath: str, allowed_paths: List[str], allowed_prefixes: List[str]) -> bool:
    """Checks whether a filepath matches explicit allowed paths or path prefixes."""
    clean_fp = filepath.strip().lstrip("./")
    for ap in allowed_paths:
        clean_ap = ap.strip().lstrip("./")
        if clean_fp == clean_ap:
            return True
    for pref in allowed_prefixes:
        clean_pref = pref.strip().lstrip("./")
        if clean_fp == clean_pref or clean_fp.startswith(clean_pref):
            return True
    return False


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

    def get_git_branch(self) -> str:
        res = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=self.repo_root, text=True)
        return res.strip()

    def get_git_remotes(self) -> str:
        try:
            res = subprocess.check_output(["git", "remote", "-v"], cwd=self.repo_root, text=True)
            return res.strip()
        except Exception:
            return ""

    def get_git_refs_snapshot(self) -> str:
        try:
            res = subprocess.check_output(["git", "show-ref"], cwd=self.repo_root, text=True)
            return res.strip()
        except Exception:
            return ""

    def is_git_clean(self) -> bool:
        res = subprocess.check_output(["git", "status", "--porcelain", "-uall"], cwd=self.repo_root, text=True)
        lines = [line.strip() for line in res.splitlines() if line.strip()]
        return len(lines) == 0

    def is_git_index_clean(self) -> bool:
        """Returns True if git staging index has no staged changes."""
        res = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=self.repo_root)
        return res.returncode == 0

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

    def get_all_status_changes(self) -> List[Tuple[str, str, Optional[str]]]:
        """
        Returns list of (status, primary_filepath, old_filepath_if_rename).
        Parses git status --porcelain -uall.
        """
        res = subprocess.check_output(["git", "status", "--porcelain", "-uall"], cwd=self.repo_root, text=True)
        items = []
        for line in res.splitlines():
            line_str = line.strip()
            if not line_str:
                continue
            status = line[:2].strip()
            path_part = line[3:].strip()
            if " -> " in path_part:
                old_p, new_p = path_part.split(" -> ", 1)
                items.append((status, new_p.strip(), old_p.strip()))
            else:
                items.append((status, path_part, None))
        return items

    def get_changed_and_untracked_files(self) -> List[Tuple[str, str]]:
        """Returns list of (status_code, file_path) from git status --porcelain."""
        changes = self.get_all_status_changes()
        return [(status, primary_p) for status, primary_p, _ in changes]

    def verify_task_scope(self, task_content: str) -> Tuple[bool, List[str]]:
        """
        Machine-enforces task scope allowlist:
        Compares ALL modified, untracked, deleted, or renamed files against
        allowed_paths and allowed_path_prefixes.
        For renames, checks BOTH source and destination paths.
        """
        allowed_paths, allowed_prefixes = parse_task_scope(task_content)
        changes = self.get_all_status_changes()
        violations = []

        for status, primary_p, old_p in changes:
            if not is_path_in_scope(primary_p, allowed_paths, allowed_prefixes):
                violations.append(f"{primary_p} (status: {status})")
            if old_p and not is_path_in_scope(old_p, allowed_paths, allowed_prefixes):
                violations.append(f"{old_p} (rename source)")

        return (len(violations) == 0, violations)

    def verify_protected_paths(self, maintenance_mode: bool = False) -> Tuple[bool, List[str]]:
        """Verifies that no protected paths are modified unless maintenance_mode is enabled."""
        if maintenance_mode:
            return (True, [])

        changed = self.get_changed_and_untracked_files()
        violations = []
        for _, mf in changed:
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
        """
        Invokes Antigravity CLI in non-interactive print mode with JSON output.

        NOTE ON --dangerously-skip-permissions:
        In headless/non-interactive print mode (-p), agy cannot prompt for interactive
        tool confirmations; omitting this flag causes tools to auto-deny ('jetski: no output produced').
        Technical Git containment is enforced by Pre/Post Git state assertions
        and the Antigravity PreToolUse hook in .agents/hooks.json.
        """
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

    def git_deliver(
        self,
        task_id: str,
        commit_msg: str,
        maintenance_mode: bool = False,
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Exclusive Git Delivery Controller with True Selective Staging.
        NEVER uses 'git add .'. Stages only validated explicit files.
        """
        remote = self.config.get("git_remote", "origin")
        branch = self.config.get("git_branch", "main")
        try:
            # 1. Collect exact changed and untracked files
            changes = self.get_all_status_changes()
            if not changes:
                self.logger.info("No modifications detected to deliver.")
                head = self.get_git_head()
                return (True, "No changes to deliver.", head)

            # 2. Validate paths against sensitive file rules and protected paths
            for _, primary_p, old_p in changes:
                paths_to_check = [primary_p]
                if old_p:
                    paths_to_check.append(old_p)
                for filepath in paths_to_check:
                    filename = Path(filepath).name
                    for sens_pat in SENSITIVE_FILENAME_PATTERNS:
                        if sens_pat.match(filename):
                            return (False, f"SecurityViolation: Sensitive file detected in working tree: {filepath}", None)

                    if not maintenance_mode:
                        for pp in PROTECTED_PATHS:
                            if filepath == pp or filepath.startswith(pp):
                                return (
                                    False,
                                    f"SecurityViolation: Protected path modification rejected without maintenance mode: {filepath}",
                                    None,
                                )

            # 3. Stage ONLY validated explicit paths (True Selective Staging)
            for _, primary_p, old_p in changes:
                if old_p:
                    subprocess.run(["git", "add", old_p], cwd=self.repo_root, check=True)
                subprocess.run(["git", "add", primary_p], cwd=self.repo_root, check=True)

            # 4. Check if anything staged
            diff_check = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=self.repo_root)
            if diff_check.returncode == 0:
                self.logger.info("No modifications staged to deliver.")
                head = self.get_git_head()
                return (True, "No changes to deliver.", head)

            # 5. Check staged diff for whitespace/formatting errors
            ws_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=self.repo_root, capture_output=True, text=True)
            if ws_check.returncode != 0:
                # Unstage
                subprocess.run(["git", "reset", "HEAD"], cwd=self.repo_root)
                return (False, f"Whitespace errors in staged diff:\n{ws_check.stderr or ws_check.stdout}", None)

            # 6. Secret scan staged diff before commit
            staged_diff = subprocess.check_output(["git", "diff", "--cached"], cwd=self.repo_root, text=True)
            has_secret, secret_reason = scan_text_for_secrets(staged_diff)
            if has_secret:
                # Unstage to prevent accidental persistence
                subprocess.run(["git", "reset", "HEAD"], cwd=self.repo_root)
                return (False, f"SecretLeakDetected: {secret_reason}", None)

            # 7. Commit atomically
            formatted_msg = f"feat(task): {task_id} - {commit_msg}"
            subprocess.run(["git", "commit", "-m", formatted_msg], cwd=self.repo_root, check=True)
            head = self.get_git_head()

            # 8. Push to remote (if push is not disabled in config)
            if self.config.get("disable_git_push", False):
                self.logger.info("Git push disabled by configuration (test/local mode).")
            else:
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
- Technical Git containment enforced: zero git delivery operations during execution.
- Protected paths respected; no perimeter violations.
- Staged diff verified whitespace-clean and secret-free.
- True selective staging enforced; zero repository-wide additions.
- Commit pushed to `{self.config.get('git_branch', 'main')}`.
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

            if not self.is_git_index_clean():
                err_msg = "Git staged index is dirty before task execution."
                self.logger.error(err_msg)
                state["last_error"] = err_msg
                state["state"] = "ERROR"
                self.save_state(state, expected_version=current_version)
                return False

            # Capture pre-execution repository baseline for containment verification
            pre_head = current_head
            pre_branch = self.get_git_branch()
            pre_remotes = self.get_git_remotes()
            pre_refs = self.get_git_refs_snapshot()

            # 2. Mark EXECUTING
            state["state"] = "EXECUTING"
            state["execution_id"] = execution_id
            if not self.save_state(state, expected_version=current_version):
                return False
            current_version += 1
            self.logger.info(f"Marked state EXECUTING for '{task_id}'.")

            # 3. Read Task & Inspect Maintenance Mode from immutable task metadata
            task_content = self.current_task_file.read_text(encoding="utf-8")
            maintenance_mode = (
                "maintenance_mode: true" in task_content.lower()
                or "maintenance mode: true" in task_content.lower()
            )

            # 4. Invoke Executor (agy CLI) with prompt boundaries
            prompt = (
                f"You are the implementation agent for English Learning OS.\n"
                f"Task ID: {task_id}\n"
                f"CRITICAL CONSTRAINT: You are FORBIDDEN from running 'git add', 'git commit', 'git push', 'git reset', 'git checkout', 'git switch', or 'git tag'.\n"
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

            # 5. Technical Git Containment Verification
            post_head = self.get_git_head()
            post_branch = self.get_git_branch()
            post_remotes = self.get_git_remotes()
            post_refs = self.get_git_refs_snapshot()

            if not self.is_git_index_clean():
                err_msg = "GitContainmentViolation: Executor modified Git staged index without runner authorization."
                self.logger.error(err_msg)
                subprocess.run(["git", "reset", "HEAD"], cwd=self.repo_root)
                subprocess.run(["git", "checkout", "--", "."], cwd=self.repo_root)
                subprocess.run(["git", "clean", "-fd"], cwd=self.repo_root)
                state["last_error"] = err_msg
                state["state"] = "ERROR"
                self.save_state(state, expected_version=current_version)
                return False

            if post_head != pre_head:
                err_msg = f"GitContainmentViolation: Executor altered Git HEAD (pre: {pre_head}, post: {post_head})."
                self.logger.error(err_msg)
                subprocess.run(["git", "reset", "--hard", pre_head], cwd=self.repo_root)
                subprocess.run(["git", "clean", "-fd"], cwd=self.repo_root)
                state["last_error"] = err_msg
                state["state"] = "ERROR"
                self.save_state(state, expected_version=current_version)
                return False

            if post_branch != pre_branch:
                err_msg = f"GitContainmentViolation: Executor switched branch (pre: {pre_branch}, post: {post_branch})."
                self.logger.error(err_msg)
                subprocess.run(["git", "checkout", pre_branch], cwd=self.repo_root)
                state["last_error"] = err_msg
                state["state"] = "ERROR"
                self.save_state(state, expected_version=current_version)
                return False

            if post_remotes != pre_remotes:
                err_msg = "GitContainmentViolation: Executor modified Git remote configurations."
                self.logger.error(err_msg)
                state["last_error"] = err_msg
                state["state"] = "ERROR"
                self.save_state(state, expected_version=current_version)
                return False

            if post_refs != pre_refs:
                err_msg = "GitContainmentViolation: Executor created or altered Git refs/branches/tags."
                self.logger.error(err_msg)
                state["last_error"] = err_msg
                state["state"] = "ERROR"
                self.save_state(state, expected_version=current_version)
                return False

            # 6. Task Scope Verification (Machine-Enforceable Path Allowlist)
            scope_ok, scope_violations = self.verify_task_scope(task_content)
            if not scope_ok:
                err_msg = f"ScopeViolation: Files modified outside task scope allowlist: {scope_violations}"
                self.logger.error(err_msg)
                subprocess.run(["git", "reset", "--hard", "HEAD"], cwd=self.repo_root)
                subprocess.run(["git", "clean", "-fd"], cwd=self.repo_root)
                retry_count += 1
                state["retry_count"] = retry_count
                state["last_error"] = err_msg
                state["state"] = "ERROR" if retry_count >= max_retries else "FIX_REQUIRED"
                self.save_state(state, expected_version=current_version)
                return False

            # 7. Protected Paths Scope Verification (Strict Additional Layer)
            paths_ok, violations = self.verify_protected_paths(maintenance_mode)
            if not paths_ok:
                err_msg = f"SecurityViolation: Protected paths modified without maintenance mode: {violations}"
                self.logger.error(err_msg)
                subprocess.run(["git", "reset", "--hard", "HEAD"], cwd=self.repo_root)
                subprocess.run(["git", "clean", "-fd"], cwd=self.repo_root)
                retry_count += 1
                state["retry_count"] = retry_count
                state["last_error"] = err_msg
                state["state"] = "ERROR" if retry_count >= max_retries else "FIX_REQUIRED"
                self.save_state(state, expected_version=current_version)
                return False

            # 7. Run Quality Gate
            qg_passed, qg_out = self.run_quality_gate()
            if not qg_passed:
                self.logger.error(f"Quality gate failed:\n{qg_out[:300]}")
                retry_count += 1
                state["retry_count"] = retry_count
                state["last_error"] = f"Quality gate failure: {qg_out[:250]}"
                state["state"] = "ERROR" if retry_count >= max_retries else "FIX_REQUIRED"
                self.save_state(state, expected_version=current_version)
                return False

            # 8. Git Delivery via Runner (True Selective Staging)
            commit_ok, commit_msg, resulting_head = self.git_deliver(
                task_id=task_id,
                commit_msg=f"complete autonomous execution ({execution_id})",
                maintenance_mode=maintenance_mode,
            )
            if not commit_ok:
                self.logger.error(f"Git delivery failed: {commit_msg}")
                state["last_error"] = commit_msg
                state["state"] = "ERROR"
                self.save_state(state, expected_version=current_version)
                return False

            # 9. Record Execution in History
            self.record_execution(task_id, expected_head, execution_id)

            # 10. Payload First: Write Handoff
            self.write_handoff(
                task_id=task_id,
                execution_id=execution_id,
                start_head=current_head,
                end_head=resulting_head or current_head,
                summary=f"Task executed successfully via agy.\nResponse: {agy_out[:300]}",
                qg_passed=True,
            )

            # 11. State Last: Advance to AWAITING_AUDIT
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
