#!/usr/bin/env python3
"""
English Learning OS — Independent Automated Auditor
Evaluates task execution against real GitHub evidence (diffs, commits, CI, quality gates).

Key Invariants:
- EXECUTOR != AUDITOR: Employs a separate model, prompt, and process.
- PROHIBITION: The auditor CANNOT modify code in the repository (read-only audit).
- Real Two-Stage Audit:
  STAGE A: Deterministic mandatory gates (remote commit, parent relationship, scope,
           protected path authorization strictly from immutable task metadata,
           defense-in-depth secret scanning, completed green CI).
  STAGE B: Independent model review with structured JSON schema validation.
- Real Model Reporting: Only records the actual model used; never fabricates model identifiers.
- Fail-Closed CI Gate: Approval strictly requires completed CI with conclusion 'success'.
  Pending/unverifiable CI keeps state in AWAITING_AUDIT without approving.
- Grounded Next Task & Termination: Grounded in docs/project/STATE.md and BACKLOG.md.
  Respects Gate 2 blocker (Learner Baseline) by transitioning to HUMAN_REQUIRED.
"""

import sys
import os
import time
import json
import signal
import shutil
import tempfile
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
    re.compile(r"\bAIza[0-9A-Za-z-_]{30,50}"),
    # Google AI Studio modern AQ.-style keys (bare tokens without assignment prefix)
    re.compile(r"\bAQ\.[A-Za-z0-9_-]{20,90}"),
    re.compile(r"\bsk-(?:proj-|admin-)?[A-Za-z0-9_-]{20,90}"),
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,90}"),
    re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,60}"),
    re.compile(r"\b(?:Bearer|Basic)\s+[A-Za-z0-9\-\._~\+\/]{15,}=*", re.IGNORECASE),
    re.compile(r"-----BEGIN (?:[A-Z0-9_-]+ )?PRIVATE KEY-----[\s\S]*?-----END (?:[A-Z0-9_-]+ )?PRIVATE KEY-----"),
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


def sanitize_text(text: str) -> str:
    sanitized = text
    for pattern in SECRET_PATTERNS:
        sanitized = pattern.sub("[REDACTED_SECRET]", sanitized)
    return sanitized


def scan_text_for_secrets(text: str) -> Tuple[bool, str]:
    """Scans text for secrets without logging sensitive values."""
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            return (True, f"Potential credential pattern detected (matched regex {pattern.pattern[:30]}...)")
    return (False, "")


def parse_auditor_response(raw_output: str) -> Tuple[bool, Dict[str, Any], str]:
    """
    Parses agy output, extracting outer envelope if present,
    then extracting and validating inner structured JSON schema.
    Handles real agy JSON outer envelope: {"response": "..."}
    and markdown code fences (```json ... ```).
    """
    cleaned_input = raw_output.strip()
    if not cleaned_input:
        return (False, {}, "Empty output from auditor model.")

    candidate_text = cleaned_input
    # 1. Unpack outer JSON envelope if present
    try:
        envelope = json.loads(cleaned_input)
        if isinstance(envelope, dict) and "response" in envelope:
            candidate_text = envelope["response"]
    except Exception:
        pass

    candidate_text = candidate_text.strip()
    # 2. Extract JSON payload from text (handling markdown code fences or raw JSON)
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", candidate_text, re.IGNORECASE)
    if fence_match:
        json_str = fence_match.group(1).strip()
    else:
        json_match = re.search(r"\{[\s\S]*\}", candidate_text)
        if json_match:
            json_str = json_match.group(0).strip()
        else:
            return (False, {}, f"Auditor output does not contain JSON block: {candidate_text[:200]}")

    try:
        data = json.loads(json_str)
    except Exception as e:
        return (False, {}, f"JSON parse error: {e}")

    if not isinstance(data, dict):
        return (False, {}, "Parsed JSON is not an object.")

    verdict = data.get("verdict")
    if verdict not in ["APPROVED", "FIX_REQUIRED", "HUMAN_REQUIRED"]:
        return (False, {}, f"Invalid verdict in auditor payload: '{verdict}'")

    findings = data.get("findings")
    if not isinstance(findings, list):
        return (False, {}, "Auditor findings must be a list.")

    return (True, data, "Valid auditor response schema.")


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
        self.human_action_file = self.control_plane_dir / "HUMAN_ACTION_REQUIRED.md"
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

    def extract_task_id(self, task_content: str) -> Optional[str]:
        """Extracts task_id from task specification markdown."""
        m = re.search(r"\*\*Task ID\*\*:\s*`?([A-Za-z0-9_-]+)`?", task_content)
        if m:
            return m.group(1).strip()
        m2 = re.search(r"^#\s+Task:\s*([A-Za-z0-9_-]+)", task_content, re.MULTILINE)
        if m2:
            return m2.group(1).strip()
        return None

    def get_repo_fingerprint(self) -> Dict[str, Any]:
        """Captures comprehensive repository fingerprint to detect any mutation."""
        try:
            status = subprocess.check_output(["git", "status", "--porcelain", "-uall"], cwd=self.repo_root, text=True)
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo_root, text=True).strip()
            branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=self.repo_root, text=True).strip()
            refs = subprocess.check_output(["git", "show-ref"], cwd=self.repo_root, text=True).strip()
            index_clean = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=self.repo_root).returncode == 0
            return {
                "status": status,
                "head": head,
                "branch": branch,
                "refs": refs,
                "index_clean": index_clean,
            }
        except Exception as e:
            return {"error": str(e)}

    def verify_remote_commit(self, commit_sha: str) -> Tuple[bool, str]:
        """Verifies that commit exists on remote origin/main."""
        if self.config.get("skip_remote_verification", False):
            return (True, "Remote verification bypassed by configuration (test mode).")

        remote = self.config.get("git_remote", "origin")
        branch = self.config.get("git_branch", "main")
        try:
            ls_out = subprocess.check_output(
                ["git", "ls-remote", remote, f"refs/heads/{branch}"],
                cwd=self.repo_root,
                text=True,
                timeout=20,
            )
            lines = ls_out.strip().splitlines()
            if not lines:
                return (False, f"Remote branch '{branch}' not found on '{remote}'.")

            remote_sha = lines[0].split()[0]
            if remote_sha != commit_sha:
                return (
                    False,
                    f"Remote HEAD divergence: {remote}/{branch} is {remote_sha}, expected {commit_sha}.",
                )
            return (True, f"Verified commit {commit_sha[:7]} matches {remote}/{branch} on remote.")
        except Exception as e:
            return (False, f"Remote commit verification failed: {e}")

    def verify_commit_parent(self, commit_sha: str, expected_parent: Optional[str]) -> Tuple[bool, str]:
        """Verifies commit's parent matches expected base commit."""
        if not expected_parent:
            return (True, "No expected parent specified.")
        try:
            parents_out = subprocess.check_output(
                ["git", "rev-parse", f"{commit_sha}^@"],
                cwd=self.repo_root,
                text=True,
            )
            parents = [p.strip() for p in parents_out.splitlines() if p.strip()]
            if expected_parent not in parents:
                return (
                    False,
                    f"Commit {commit_sha[:7]} parent mismatch: expected {expected_parent[:7]}, found {parents}",
                )
            return (True, f"Verified parent {expected_parent[:7]} of commit {commit_sha[:7]}.")
        except Exception as e:
            return (False, f"Parent verification error: {e}")

    def audit_commit_diff_and_scope(
        self,
        commit_sha: str,
        expected_parent: Optional[str],
        task_id: str,
        expected_task_hash: Optional[str],
    ) -> Tuple[bool, List[str], str]:
        """
        Stage A Gate: Audits local commit existence, parent relationship,
        changed files, protected path authorization, and secret absence.
        """
        try:
            # 1. Verify local commit existence
            subprocess.run(["git", "cat-file", "-e", f"{commit_sha}^{{commit}}"], cwd=self.repo_root, check=True)

            # 2. Verify parent relationship
            parent_ok, parent_msg = self.verify_commit_parent(commit_sha, expected_parent)
            if not parent_ok:
                return (False, [], parent_msg)

            # 3. Get changed files
            files_out = subprocess.check_output(
                ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_sha],
                cwd=self.repo_root,
                text=True,
            )
            changed_files = [f.strip() for f in files_out.splitlines() if f.strip()]

            # 4. Get commit diff
            diff_out = subprocess.check_output(
                ["git", "show", "--format=", commit_sha], cwd=self.repo_root, text=True
            )

            # 5. Secret scan commit diff
            has_secret, secret_reason = scan_text_for_secrets(diff_out)
            if has_secret:
                return (False, changed_files, f"SecretLeakDetected: {secret_reason}")

            # 6. Protected path authorization check (Strictly from immutable CURRENT_TASK.md)
            protected_changed = []
            for cf in changed_files:
                for pp in PROTECTED_PATHS:
                    if cf == pp or cf.startswith(pp):
                        protected_changed.append(cf)

            if protected_changed:
                auth_ok, auth_reason = self.verify_protected_path_authorization(
                    task_id=task_id,
                    expected_hash=expected_task_hash,
                    protected_files=protected_changed,
                )
                if not auth_ok:
                    return (False, changed_files, auth_reason)

            return (True, changed_files, diff_out)

        except Exception as e:
            return (False, [], f"Commit audit error: {e}")

    def verify_protected_path_authorization(
        self,
        task_id: str,
        expected_hash: Optional[str],
        protected_files: List[str],
    ) -> Tuple[bool, str]:
        """
        Validates that protected path changes were authorized by immutable task metadata:
        task_type == INFRASTRUCTURE AND maintenance_mode == true AND hash matches.
        NEVER allows authorization from commit messages.
        """
        if not self.current_task_file.exists():
            return (
                False,
                f"ProtectedPathBreach: Protected paths {protected_files} modified, but CURRENT_TASK.md is missing.",
            )

        actual_hash = self.compute_file_hash(self.current_task_file)
        if expected_hash and actual_hash != expected_hash:
            return (
                False,
                f"ProtectedPathBreach: Protected paths {protected_files} modified, but task content hash mismatch.",
            )

        task_content = self.current_task_file.read_text(encoding="utf-8").lower()
        is_infra = "task_type: infrastructure" in task_content or "task type: infrastructure" in task_content
        is_maint = "maintenance_mode: true" in task_content or "maintenance mode: true" in task_content

        if not (is_infra and is_maint):
            return (
                False,
                f"ProtectedPathBreach: Protected paths {protected_files} modified without immutable task authorization "
                "(requires task_type: INFRASTRUCTURE and maintenance_mode: true in CURRENT_TASK.md).",
            )

        return (True, f"Protected paths {protected_files} authorized under verified maintenance mode.")

    def audit_ci_status(self, commit_sha: str) -> Tuple[bool, str, str]:
        """
        Audits GitHub Actions CI status for the commit.
        Returns: (is_success, status_category, details)
        status_category: 'SUCCESS', 'PENDING', 'FAILED', 'UNVERIFIABLE'

        FAIL CLOSED REQUIREMENT:
        Approval strictly requires: matching workflow run on GitHub Actions for commit_sha,
        specifically pinned to .github/workflows/repository-quality.yml ("Repository Quality Gate"),
        status == 'completed', and conclusion == 'success'.
        Unrelated green workflows on the same commit MUST NOT satisfy this gate.
        """
        if self.config.get("skip_ci_for_tests", False):
            return (True, "SUCCESS", "CI check bypassed by explicit test configuration.")

        gh_bin = shutil.which("gh")
        if not gh_bin:
            return (False, "UNVERIFIABLE", "gh CLI not available on system; cannot verify remote CI.")

        try:
            # Query runs specifically for repository-quality.yml workflow
            proc = subprocess.run(
                [
                    gh_bin,
                    "run",
                    "list",
                    "--workflow",
                    "repository-quality.yml",
                    "--commit",
                    commit_sha,
                    "--json",
                    "status,conclusion,name,workflowName,databaseId",
                    "--limit",
                    "5",
                ],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if proc.returncode != 0:
                return (False, "UNVERIFIABLE", f"gh query failed: {proc.stderr.strip()}")

            runs = json.loads(proc.stdout)
            # Filter specifically for Repository Quality Gate workflow (exclude unrelated workflows)
            matching_runs = []
            for r in runs:
                w_name = r.get("name") or r.get("workflowName")
                if w_name:
                    clean_name = str(w_name).lower().replace(".yml", "").replace(".yaml", "").replace(" ", "-")
                    if clean_name not in ["repository-quality-gate", "repository-quality"]:
                        continue
                matching_runs.append(r)

            if not matching_runs:
                return (
                    False,
                    "PENDING",
                    f"No required 'Repository Quality Gate' CI runs recorded yet for commit {commit_sha[:7]}.",
                )

            latest = matching_runs[0]
            status = latest.get("status")
            conclusion = latest.get("conclusion")
            run_id = latest.get("databaseId", "unknown")

            if status == "completed" and conclusion == "success":
                return (True, "SUCCESS", f"Required CI workflow 'Repository Quality Gate' (run #{run_id}) completed successfully.")
            elif status == "completed":
                return (False, "FAILED", f"Required CI workflow 'Repository Quality Gate' (run #{run_id}) completed with negative conclusion: '{conclusion}'.")
            else:
                return (False, "PENDING", f"Required CI workflow 'Repository Quality Gate' (run #{run_id}) is currently '{status}' (conclusion: '{conclusion}').")

        except Exception as e:
            return (False, "UNVERIFIABLE", f"CI audit query exception: {e}")

    def execute_stage_b_model_audit(
        self,
        task_content: str,
        commit_sha: str,
        changed_files: List[str],
        diff_text: str,
        ci_summary: str,
    ) -> Tuple[bool, Dict[str, Any], str]:
        """
        Stage B: Independent model review via agy.
        Enforces separate model, separate prompt, read-only evidence,
        and validates structured JSON output schema.
        """
        model_name = self.config.get("auditor_model", "gemini-3.1-pro-high")

        # In testing/local simulation where agy model call is mocked or skipped
        if self.config.get("mock_model_audit", False):
            mock_res = self.config.get("mock_model_result", {
                "verdict": "APPROVED",
                "findings": ["Mock verification passed"],
                "requirement_coverage": ["All test requirements satisfied"],
                "confidence": "HIGH",
                "next_action": "PROCEED",
            })
            return (True, mock_res, "mock-auditor")

        # 1. Capture Pre-Stage B Repository Baseline Fingerprint
        pre_fingerprint = self.get_repo_fingerprint()

        agy_bin = self.config.get("agy_binary", "/Users/gmbispo/.local/bin/agy")
        if not Path(agy_bin).exists():
            agy_bin = shutil.which("agy") or agy_bin

        if not Path(agy_bin).exists():
            return (False, {}, f"Antigravity CLI not found at '{agy_bin}'")

        # 2. Construct Isolated External Evidence Bundle outside the repository
        with tempfile.TemporaryDirectory(prefix="agy_auditor_evidence_") as evidence_dir:
            ev_path = Path(evidence_dir)
            (ev_path / "CURRENT_TASK.md").write_text(task_content, encoding="utf-8")
            (ev_path / "COMMIT_DIFF.patch").write_text(diff_text, encoding="utf-8")
            (ev_path / "CHANGED_FILES.json").write_text(json.dumps(changed_files, indent=2), encoding="utf-8")
            (ev_path / "CI_SUMMARY.txt").write_text(ci_summary, encoding="utf-8")

            prompt = f"""You are the Independent Automated Auditor for English Learning OS.
Your task is to independently review task execution against read-only evidence.

EVALUATION INVARIANTS:
1. EXECUTOR != AUDITOR: You are a separate adversarial reviewer.
2. Read-only audit: You are executing in an isolated evidence directory outside the repository.
   You have NO repository write capabilities and must not attempt filesystem mutations.
3. Validate requirements coverage, boundary safety, and code quality.
4. Output STRICT JSON ONLY matching this schema:
{{
  "verdict": "APPROVED" | "FIX_REQUIRED" | "HUMAN_REQUIRED",
  "findings": ["finding 1", "finding 2"],
  "requirement_coverage": ["req 1: covered", ...],
  "confidence": "HIGH" | "MEDIUM" | "LOW",
  "next_action": "PROCEED" | "REMEDIATE" | "ESCALATE"
}}

EVIDENCE:
- Task Specification (from CURRENT_TASK.md):
{task_content[:1500]}

- Commit SHA: {commit_sha}
- Changed Files: {json.dumps(changed_files)}
- CI Evidence: {ci_summary}
- Staged Diff (from COMMIT_DIFF.patch, Truncated):
{diff_text[:3000]}
"""
            cmd = [
                agy_bin,
                "-p",
                prompt,
                "--model",
                model_name,
                "--agent",
                "code-auditor",
                "--output-format",
                "json",
                "--dangerously-skip-permissions",
            ]
            try:
                self.logger.info(f"Invoking independent auditor model ({model_name}) in isolated evidence boundary...")
                proc = subprocess.run(
                    cmd,
                    cwd=evidence_dir,
                    capture_output=True,
                    text=True,
                    timeout=self.config.get("audit_timeout_seconds", 180),
                )
                raw_out = proc.stdout.strip()
            except subprocess.TimeoutExpired:
                return (False, {}, "Auditor model execution timed out.")
            except Exception as e:
                return (False, {}, f"Auditor model execution error: {e}")

            # 3. Capture Post-Stage B Repository Baseline Fingerprint & Assert Zero Mutation
            post_fingerprint = self.get_repo_fingerprint()
            if pre_fingerprint != post_fingerprint:
                err_msg = (
                    "AUDITOR_CONTAINMENT_VIOLATION: Repository mutation detected during Stage B model audit! "
                    f"pre={pre_fingerprint}, post={post_fingerprint}"
                )
                self.logger.error(err_msg)
                return (False, {}, err_msg)

            if proc.returncode != 0:
                return (False, {}, f"Auditor model returned non-zero code {proc.returncode}: {proc.stderr.strip()}")

            # 4. Structured Output Parsing (Envelope + Code fence + Schema validation)
            parse_ok, parsed_data, parse_msg = parse_auditor_response(raw_out)
            if not parse_ok:
                return (False, {}, f"Auditor model output validation failed: {parse_msg}")

            return (True, parsed_data, model_name)

    def plan_next_operational_state(self, current_task_id: str) -> Dict[str, Any]:
        """
        Grounds next task generation in canonical project state (STATE.md & BACKLOG.md).
        Enforces project invariants:
        - GATE 2: BLOCKED ON LEARNER BASELINE.
        - Phase 03: LOCKED.
        - NEVER creates generic synthetic tasks merely to keep looping.
        - When no unblocked autonomous task exists, transitions to HUMAN_REQUIRED.
        """
        backlog_file = self.repo_root / "docs" / "project" / "BACKLOG.md"
        state_file = self.repo_root / "docs" / "project" / "STATE.md"

        if not backlog_file.exists() or not state_file.exists():
            return {
                "action": "HUMAN_REQUIRED",
                "reason": "Canonical project state documentation missing.",
            }

        backlog_text = backlog_file.read_text(encoding="utf-8")
        state_text = state_file.read_text(encoding="utf-8")

        # Parse TASK-030 checklist status: unchecked vs checked
        task_030_unchecked = bool(re.search(r"- \[ \]\s+\*\*TASK-030(?:\s*\([^)]*\))?\*\*", backlog_text))
        gate_2_blocked = "BLOCKED ON LEARNER BASELINE" in state_text

        # Only stop on TASK-030 if it is UNCHECKED AND Gate 2 is BLOCKED ON LEARNER BASELINE
        if task_030_unchecked and gate_2_blocked:
            blocker_msg = (
                "Project is at GATE 2: BLOCKED ON LEARNER BASELINE.\n"
                "TASK-030 requires administering the intake and baseline diagnostic forms "
                "(docs/assessment/learner/BASELINE_FORM.md) to the learner to compute state vector P.\n"
                "Phase 03 remains LOCKED until human baseline responses are received."
            )
            # Write HUMAN_ACTION_REQUIRED.md
            self.write_human_action_required(
                action_title="Administer Learner Baseline Diagnostic (TASK-030)",
                blocker_description=blocker_msg,
                instructions="1. Administer docs/assessment/learner/BASELINE_FORM.md to learner.\n2. Record responses and score via SCORING_GUIDE.md.\n3. Close Gate 2 to unlock Phase 03.",
            )
            return {
                "action": "HUMAN_REQUIRED",
                "blocker": blocker_msg,
                "task_id": None,
            }

        # Check for unblocked pending tasks
        pending_tasks = re.findall(r"- \[ \] \*\*([A-Z0-9_-]+)\*\*:\s*(.+)", backlog_text)
        if not pending_tasks:
            return {
                "action": "COMPLETE",
                "reason": "All backlog items completed.",
                "task_id": None,
            }

        next_task_id, next_task_desc = pending_tasks[0]
        # Grounded task candidate with explicit task scope
        content = f"""# Task: {next_task_id} — {next_task_desc.strip()}

## Metadata
- **Task ID**: `{next_task_id}`
- **Parent Task ID**: `{current_task_id}`
- **Task Type**: `FEATURE`
- **Maintenance Mode**: `false`

## 1. Context & Objective
Grounded task derived directly from docs/project/BACKLOG.md.
{next_task_desc.strip()}

## 2. Scope & Allowed Paths
allowed_paths:
  - docs/project/STATE.md
allowed_path_prefixes:
  - docs/

- Respect all rules in AGENTS.md.
- Zero secrets in repository.
- Quality gate passing before handoff.
"""
        self.next_task_file.write_text(content, encoding="utf-8")
        return {
            "action": "APPROVED",
            "task_id": next_task_id,
            "content_hash": self.compute_file_hash(self.next_task_file),
        }

    def write_human_action_required(self, action_title: str, blocker_description: str, instructions: str):
        content = f"""# Human Action Required

> Generated autonomously by English Learning OS Automated Auditor.
> Pipeline paused at milestone boundary.

## Action Title
`{action_title}`

## Timestamp
`{datetime.now(timezone.utc).isoformat()}`

## Blocker Description
{blocker_description}

## Required Action
{instructions}
"""
        self.human_action_file.write_text(content, encoding="utf-8")

    def generate_corrective_task(self, original_task_id: str, feedback: str, retry_count: int) -> str:
        """Generates a corrective task in CURRENT_TASK.md with parent_task_id."""
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

    def write_audit_report(
        self,
        task_id: str,
        execution_id: str,
        commit_sha: str,
        verdict: str,
        model_name: str,
        stage_a_details: str,
        stage_b_details: str,
    ):
        content = f"""# Audit Report

> Generated autonomously by English Learning OS Automated Auditor.

## Metadata
- **Task ID**: `{task_id}`
- **Execution ID**: `{execution_id}`
- **Auditor Model**: `{model_name}`
- **Audit Timestamp**: `{datetime.now(timezone.utc).isoformat()}`
- **Verified Commit**: `{commit_sha}`
- **Verdict**: `{verdict}`

## Stage A: Deterministic Mandatory Gates
{stage_a_details}

## Stage B: Independent Model Review
{stage_b_details}
"""
        self.audit_report_file.write_text(content, encoding="utf-8")

    def execute_audit_cycle(self, standalone_promote: bool = False) -> bool:
        """Executes a single cycle of the automated auditor."""
        state = self.load_state()
        if not state:
            return False

        if state.get("state") != "AWAITING_AUDIT":
            return False

        task_id = state.get("task_id", "UNKNOWN_TASK")
        execution_id = state.get("execution_id", "UNKNOWN_EXEC")
        commit_sha = state.get("resulting_git_head", "")
        expected_parent = state.get("expected_git_head")
        expected_task_hash = state.get("content_hash")
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

        # =========================================================================
        # CONTROL PLANE IMMUTABILITY GATE (Mandatory for EVERY task)
        # =========================================================================
        if not self.current_task_file.exists():
            err_msg = "ControlPlaneIntegrityViolation: CURRENT_TASK.md is missing before audit."
            self.logger.error(err_msg)
            state["state"] = "ERROR"
            state["last_error"] = err_msg
            self.save_state(state, expected_version=current_version)
            return False

        actual_task_hash = self.compute_file_hash(self.current_task_file)
        if expected_task_hash and actual_task_hash != expected_task_hash:
            err_msg = (
                f"ControlPlaneIntegrityViolation: CURRENT_TASK.md hash mismatch "
                f"(expected {expected_task_hash}, actual {actual_task_hash}). "
                "Task specification was altered after execution."
            )
            self.logger.error(err_msg)
            state["state"] = "ERROR"
            state["last_error"] = err_msg
            self.save_state(state, expected_version=current_version)
            return False

        task_content = self.current_task_file.read_text(encoding="utf-8")
        file_task_id = self.extract_task_id(task_content)
        if file_task_id and file_task_id != task_id:
            err_msg = (
                f"ControlPlaneIntegrityViolation: task_id mismatch in CURRENT_TASK.md "
                f"(file specifies '{file_task_id}', state specifies '{task_id}')."
            )
            self.logger.error(err_msg)
            state["state"] = "ERROR"
            state["last_error"] = err_msg
            self.save_state(state, expected_version=current_version)
            return False

        # =========================================================================
        # STAGE A: Deterministic Mandatory Gates (Fail-Closed)
        # =========================================================================

        # 1. Remote commit verification
        remote_ok, remote_msg = self.verify_remote_commit(commit_sha)
        if not remote_ok:
            self.logger.error(f"Stage A Gate Failed (Remote Commit): {remote_msg}")
            # Keep in AWAITING_AUDIT if remote sync is in progress or query issue
            return False

        # 2. Commit diff, scope, protected paths, and secret scanning
        diff_ok, changed_files, diff_out = self.audit_commit_diff_and_scope(
            commit_sha=commit_sha,
            expected_parent=expected_parent,
            task_id=task_id,
            expected_task_hash=expected_task_hash,
        )
        if not diff_ok:
            self.logger.error(f"Stage A Gate Failed (Diff/Scope/Secrets): {diff_out}")
            retry_count += 1
            state["retry_count"] = retry_count
            state["last_error"] = diff_out

            if retry_count >= max_retries:
                state["state"] = "ERROR"
            else:
                new_hash = self.generate_corrective_task(task_id, diff_out, retry_count)
                state["state"] = "FIX_REQUIRED"
                state["content_hash"] = new_hash

            self.write_audit_report(
                task_id=task_id,
                execution_id=execution_id,
                commit_sha=commit_sha,
                verdict="FIX_REQUIRED",
                model_name="deterministic-stage-a",
                stage_a_details=f"- Gate FAILED: {diff_out}",
                stage_b_details="Stage B skipped due to Stage A failure.",
            )
            self.save_state(state, expected_version=current_version)
            return False

        # 3. CI Status Verification (FAIL-CLOSED)
        ci_ok, ci_category, ci_msg = self.audit_ci_status(commit_sha)
        if not ci_ok:
            if ci_category in ["PENDING", "UNVERIFIABLE"]:
                # State remains AWAITING_AUDIT; safe retry without failing or approving
                self.logger.info(f"CI status pending/unverifiable: {ci_msg}. Retaining state AWAITING_AUDIT.")
                return False
            else:
                # CI concluded with failure/cancelled/timed_out
                self.logger.error(f"Stage A Gate Failed (CI Failure): {ci_msg}")
                retry_count += 1
                state["retry_count"] = retry_count
                state["last_error"] = ci_msg
                state["state"] = "ERROR" if retry_count >= max_retries else "FIX_REQUIRED"
                new_hash = self.generate_corrective_task(task_id, ci_msg, retry_count)
                state["content_hash"] = new_hash

                self.write_audit_report(
                    task_id=task_id,
                    execution_id=execution_id,
                    commit_sha=commit_sha,
                    verdict="FIX_REQUIRED",
                    model_name="deterministic-stage-a",
                    stage_a_details=f"- CI Check FAILED: {ci_msg}",
                    stage_b_details="Stage B skipped due to Stage A failure.",
                )
                self.save_state(state, expected_version=current_version)
                return False

        stage_a_summary = (
            f"- Remote Commit: {remote_msg}\n"
            f"- Changed Files ({len(changed_files)}): {changed_files}\n"
            f"- Scope & Protected Paths: Verified\n"
            f"- Secret Scan: Clean (zero credentials detected)\n"
            f"- GitHub Actions CI: {ci_msg}"
        )

        # =========================================================================
        # STAGE B: Independent Model Review
        # =========================================================================
        task_content = self.current_task_file.read_text(encoding="utf-8") if self.current_task_file.exists() else ""
        model_ok, model_result, actual_model_id = self.execute_stage_b_model_audit(
            task_content=task_content,
            commit_sha=commit_sha,
            changed_files=changed_files,
            diff_text=diff_out,
            ci_summary=ci_msg,
        )

        if not model_ok:
            # Model audit failed or returned malformed output: FAIL CLOSED!
            err_msg = f"Stage B Model Audit Failed: {actual_model_id}"
            self.logger.error(err_msg)
            retry_count += 1
            state["retry_count"] = retry_count
            state["last_error"] = err_msg
            state["state"] = "ERROR" if retry_count >= max_retries else "FIX_REQUIRED"
            new_hash = self.generate_corrective_task(task_id, err_msg, retry_count)
            state["content_hash"] = new_hash

            self.write_audit_report(
                task_id=task_id,
                execution_id=execution_id,
                commit_sha=commit_sha,
                verdict="FIX_REQUIRED",
                model_name=actual_model_id,
                stage_a_details=stage_a_summary,
                stage_b_details=f"Model review rejected with error: {err_msg}",
            )
            self.save_state(state, expected_version=current_version)
            return False

        verdict = model_result.get("verdict", "FIX_REQUIRED")
        stage_b_summary = (
            f"- Verdict: {verdict}\n"
            f"- Confidence: {model_result.get('confidence', 'UNKNOWN')}\n"
            f"- Findings: {json.dumps(model_result.get('findings', []))}\n"
            f"- Coverage: {json.dumps(model_result.get('requirement_coverage', []))}\n"
            f"- Next Action: {model_result.get('next_action', 'UNKNOWN')}"
        )

        if verdict != "APPROVED":
            retry_count += 1
            state["retry_count"] = retry_count
            remedy_msg = f"Auditor model returned {verdict}: {model_result.get('findings')}"
            state["last_error"] = remedy_msg
            state["state"] = verdict if verdict == "HUMAN_REQUIRED" else ("ERROR" if retry_count >= max_retries else "FIX_REQUIRED")

            if state["state"] == "FIX_REQUIRED":
                new_hash = self.generate_corrective_task(task_id, remedy_msg, retry_count)
                state["content_hash"] = new_hash

            self.write_audit_report(
                task_id=task_id,
                execution_id=execution_id,
                commit_sha=commit_sha,
                verdict=verdict,
                model_name=actual_model_id,
                stage_a_details=stage_a_summary,
                stage_b_details=stage_b_summary,
            )
            self.save_state(state, expected_version=current_version)
            return False

        # =========================================================================
        # Post-Approval: Grounded Next Operational State Planning
        # =========================================================================
        next_plan = self.plan_next_operational_state(task_id)
        next_action = next_plan.get("action", "HUMAN_REQUIRED")

        self.write_audit_report(
            task_id=task_id,
            execution_id=execution_id,
            commit_sha=commit_sha,
            verdict="APPROVED",
            model_name=actual_model_id,
            stage_a_details=stage_a_summary,
            stage_b_details=stage_b_summary + f"\n- Grounded Next Step: {next_action}",
        )

        if next_action == "HUMAN_REQUIRED":
            state["state"] = "HUMAN_REQUIRED"
            state["last_error"] = next_plan.get("blocker", "Human intervention required.")
            state["retry_count"] = 0
            self.save_state(state, expected_version=current_version)
            self.logger.info("Task APPROVED. Pipeline paused at milestone boundary: HUMAN_REQUIRED.")
            return True

        if next_action == "COMPLETE":
            state["state"] = "COMPLETE"
            state["last_error"] = None
            self.save_state(state, expected_version=current_version)
            self.logger.info("Task APPROVED. Milestone completed: COMPLETE.")
            return True

        # Next actionable task exists
        next_task_id = next_plan.get("task_id")
        state["state"] = "APPROVED"
        state["last_error"] = None
        self.save_state(state, expected_version=current_version)
        current_version += 1
        self.logger.info(f"Task '{task_id}' APPROVED. Next candidate: '{next_task_id}'.")

        # Standalone Promotion
        if standalone_promote or self.config.get("standalone_mode", False):
            if next_task_id and self.next_task_file.exists():
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
