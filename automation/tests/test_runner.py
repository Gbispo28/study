#!/usr/bin/env python3
"""
Comprehensive Adversarial Unit Test Suite for English Learning OS Automation Control Plane.
Tests state machine transitions, lock safety, git head divergence, modern secret detection,
protected path scope enforcement, optimistic concurrency, payload-first hashing,
independent two-stage auditor verification, idempotency, standalone promotion, and event logging.
"""

import os
import json
import hashlib
import tempfile
import subprocess
from typing import Any, Dict, List, Optional, Tuple
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from automation.runner import (
    sanitize_text,
    scan_text_for_secrets,
    SafeLogger,
    RunnerLock,
    OrchestrationRunner,
    PROTECTED_PATHS,
    normalize_scope_path,
    is_path_in_scope,
    parse_task_scope,
)
from automation.auditor import AutomatedAuditor


def init_git_repo(repo_dir: Path):
    """Helper to initialize a real git repository in a temp directory."""
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test Runner"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "runner@test.local"], cwd=repo_dir, check=True, capture_output=True)
    gitignore = repo_dir / ".gitignore"
    gitignore.write_text("automation/state/\nautomation/logs/\nautomation/.lock\n", encoding="utf-8")
    subprocess.run(["git", "add", ".gitignore"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial commit"], cwd=repo_dir, check=True, capture_output=True)


class TestSecretSanitization(unittest.TestCase):
    """Verifies that secrets across modern formats are stripped from log outputs (Tests 1-5)."""

    def test_sanitize_github_tokens(self):
        fake_token = "ghp_" + ("A" * 36)
        raw = f"Error with token {fake_token} in call"
        clean = sanitize_text(raw)
        self.assertNotIn("ghp_", clean)
        self.assertIn("[REDACTED_SECRET]", clean)

    def test_sanitize_modern_gemini_api_keys(self):
        # Fake key shaped like current Google AI Studio key (AIzaSy + 33 chars = 39 chars total)
        fake_key = "AIzaSy" + ("X" * 33)
        raw = f"Google AI key {fake_key} failed"
        clean = sanitize_text(raw)
        self.assertNotIn("AIzaSy", clean)
        self.assertIn("[REDACTED_SECRET]", clean)
        has_secret, msg = scan_text_for_secrets(raw)
        self.assertTrue(has_secret)
        self.assertNotIn("AIzaSy", msg)

    def test_sanitize_fake_aq_style_google_ai_key(self):
        """Verifies detection and sanitization of modern AQ.-style Google AI keys without assignment prefix."""
        fake_aq_key = "AQ." + ("Z" * 36) + "AbCdEf1234567890"
        raw = f"Processing request with credential {fake_aq_key} in environment"
        clean = sanitize_text(raw)
        self.assertNotIn("AQ.", clean)
        self.assertIn("[REDACTED_SECRET]", clean)

        has_secret, msg = scan_text_for_secrets(raw)
        self.assertTrue(has_secret)
        self.assertNotIn(fake_aq_key, msg)
        self.assertNotIn("AbCdEf", msg)

    def test_sanitize_openai_and_anthropic_keys(self):
        fake_oai = "sk-proj-" + ("K" * 45)
        fake_ant = "sk-ant-" + ("M" * 45)
        clean = sanitize_text(f"{fake_oai} and {fake_ant}")
        self.assertNotIn("sk-proj-", clean)
        self.assertNotIn("sk-ant-", clean)

    def test_sanitize_pem_private_keys(self):
        fake_pem = "-----" + "BEGIN RSA PRIVATE KEY-----\nMIIEfakekeycontent...\n-----" + "END RSA PRIVATE KEY-----"
        clean = sanitize_text(fake_pem)
        self.assertNotIn("MIIEfakekeycontent", clean)
        self.assertIn("[REDACTED_SECRET]", clean)

    def test_sanitize_assignment_heuristics(self):
        raw = "api_" + 'key = "sensitive_secret_value_1234567890"'
        clean = sanitize_text(raw)
        self.assertNotIn("sensitive_secret_value_1234567890", clean)
        self.assertIn("[REDACTED_SECRET]", clean)


class TestRunnerLock(unittest.TestCase):
    """Verifies concurrency protection and stale lock cleanup (Tests 6-8)."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.lock_path = Path(self.temp_dir.name) / ".lock"
        self.logger = SafeLogger()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_acquire_and_release_lock(self):
        lock = RunnerLock(self.lock_path, self.logger)
        self.assertTrue(lock.acquire())
        self.assertTrue(self.lock_path.exists())
        lock.release()
        self.assertFalse(self.lock_path.exists())

    def test_prevent_concurrent_execution(self):
        lock1 = RunnerLock(self.lock_path, self.logger)
        lock2 = RunnerLock(self.lock_path, self.logger)
        self.assertTrue(lock1.acquire())
        self.assertFalse(lock2.acquire())
        lock1.release()

    def test_stale_lock_cleanup_from_dead_pid(self):
        stale_data = {"pid": 999999, "acquired_at": "2026-01-01T00:00:00Z"}
        self.lock_path.write_text(json.dumps(stale_data), encoding="utf-8")
        lock = RunnerLock(self.lock_path, self.logger)
        self.assertTrue(lock.acquire())
        lock.release()


class TestOrchestrationRunnerCore(unittest.TestCase):
    """Adversarial tests for state transitions, git head checks, and retries (Tests 9-13)."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name) / "repo"
        self.repo_root.mkdir(parents=True)
        init_git_repo(self.repo_root)

        self.cp_dir = Path(self.temp_dir.name) / "external_control_plane"
        self.cp_dir.mkdir(parents=True)

        self.state_file = self.cp_dir / "STATE.json"
        self.task_file = self.cp_dir / "CURRENT_TASK.md"
        self.task_content = "# Test Task\nmaintenance_mode: false\nallowed_paths:\n  - test_file.txt\nDo something safe."
        self.task_file.write_text(self.task_content, encoding="utf-8")
        self.task_hash = hashlib.sha256(self.task_content.encode("utf-8")).hexdigest()

        self.config = {
            "control_plane_dir": str(self.cp_dir),
            "max_retries": 3,
            "poll_interval_seconds": 1,
            "git_branch": "main",
            "disable_git_push": True,
        }
        self.logger = SafeLogger()
        self.runner = OrchestrationRunner(self.repo_root, self.config, self.logger)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_ignore_non_actionable_states(self):
        non_actionable = ["EXECUTING", "AWAITING_AUDIT", "APPROVED", "HUMAN_REQUIRED", "COMPLETE", "ERROR"]
        for st in non_actionable:
            self.state_file.write_text(json.dumps({
                "state": st,
                "task_id": "T1",
                "state_version": 1,
                "content_hash": self.task_hash
            }), encoding="utf-8")
            result = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(result, f"Runner should not act on state {st}")

    def test_head_divergence_fails_to_error_state(self):
        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": "T-DIVERGE",
            "expected_git_head": "0000000000000000000000000000000000000000",
            "content_hash": self.task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(initial_state), encoding="utf-8")

        success = self.runner.execute_task_cycle(dry_run=False)
        self.assertFalse(success)
        saved = self.runner.load_state()
        self.assertEqual(saved["state"], "ERROR")
        self.assertIn("Git HEAD divergence", saved["last_error"])

    def test_successful_task_cycle_advances_to_awaiting_audit(self):
        head = self.runner.get_git_head()
        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": "T-SUCCESS",
            "expected_git_head": head,
            "content_hash": self.task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(initial_state), encoding="utf-8")

        # Mock agy executor to modify a file
        def fake_execute_agy(prompt):
            (self.repo_root / "test_file.txt").write_text("safe content", encoding="utf-8")
            return (True, "Executed successfully")

        with patch.object(self.runner, "execute_agy", side_effect=fake_execute_agy), \
             patch.object(self.runner, "run_quality_gate", return_value=(True, "All passed")):

            success = self.runner.execute_task_cycle(dry_run=False)
            self.assertTrue(success)
            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "AWAITING_AUDIT")
            self.assertEqual(saved["retry_count"], 0)
            self.assertIsNone(saved["last_error"])
            self.assertTrue(self.runner.handoff_file.exists())

    def test_quality_gate_failure_increments_retry_and_sets_fix_required(self):
        head = self.runner.get_git_head()
        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": "T-FAIL-QG",
            "expected_git_head": head,
            "content_hash": self.task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(initial_state), encoding="utf-8")

        with patch.object(self.runner, "execute_agy", return_value=(True, "Executed successfully")), \
             patch.object(self.runner, "run_quality_gate", return_value=(False, "Lint check failed")):

            success = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(success)
            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "FIX_REQUIRED")
            self.assertEqual(saved["retry_count"], 1)
            self.assertIn("Lint check failed", saved["last_error"])

    def test_max_retries_exceeded_transitions_to_error(self):
        head = self.runner.get_git_head()
        initial_state = {
            "state": "FIX_REQUIRED",
            "state_version": 1,
            "task_id": "T-MAX-RETRIES",
            "expected_git_head": head,
            "content_hash": self.task_hash,
            "retry_count": 2,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(initial_state), encoding="utf-8")

        with patch.object(self.runner, "execute_agy", return_value=(True, "Executed")), \
             patch.object(self.runner, "run_quality_gate", return_value=(False, "Failed again")):

            success = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(success)
            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "ERROR")
            self.assertEqual(saved["retry_count"], 3)


class TestArchitectureAndSecurityEnhancements(unittest.TestCase):
    """Tests 14-23: Clean git tree, protected paths, optimistic concurrency, transactions."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name) / "repo"
        self.repo_root.mkdir(parents=True)
        init_git_repo(self.repo_root)

        self.cp_dir = Path(self.temp_dir.name) / "external_cp"
        self.cp_dir.mkdir(parents=True)

        self.state_file = self.cp_dir / "STATE.json"
        self.task_file = self.cp_dir / "CURRENT_TASK.md"
        self.task_content = "# Task\nmaintenance_mode: false\nBody"
        self.task_file.write_text(self.task_content, encoding="utf-8")
        self.task_hash = hashlib.sha256(self.task_content.encode("utf-8")).hexdigest()

        self.config = {
            "control_plane_dir": str(self.cp_dir),
            "max_retries": 3,
            "poll_interval_seconds": 1,
            "disable_git_push": True,
        }
        self.logger = SafeLogger()
        self.runner = OrchestrationRunner(self.repo_root, self.config, self.logger)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_git_cleanliness_after_state_mutation(self):
        """Test 14: Mutating STATE.json outside Git repo leaves git repo completely clean."""
        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": "T-CLEAN",
            "expected_git_head": self.runner.get_git_head(),
            "content_hash": self.task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.runner.save_state(initial_state)
        self.assertTrue(self.runner.is_git_clean())

    def test_control_plane_separation(self):
        """Test 15: Control plane directory is not a subdirectory of repo_root."""
        self.assertFalse(str(self.runner.control_plane_dir).startswith(str(self.runner.repo_root)))

    def test_protected_path_runner_py_rejected(self):
        """Test 16: Modifying runner.py in regular task is rejected."""
        with patch.object(self.runner, "get_changed_and_untracked_files", return_value=[("M", "automation/runner.py")]):
            paths_ok, violations = self.runner.verify_protected_paths(maintenance_mode=False)
            self.assertFalse(paths_ok)
            self.assertIn("automation/runner.py", violations)

    def test_protected_path_quality_gate_rejected(self):
        """Test 17: Modifying quality_gate.sh in regular task is rejected."""
        with patch.object(self.runner, "get_changed_and_untracked_files", return_value=[("M", "scripts/quality_gate.sh")]):
            paths_ok, violations = self.runner.verify_protected_paths(maintenance_mode=False)
            self.assertFalse(paths_ok)
            self.assertIn("scripts/quality_gate.sh", violations)

    def test_protected_path_agents_rejected(self):
        """Test 18: Modifying .agents/ in regular task is rejected."""
        with patch.object(self.runner, "get_changed_and_untracked_files", return_value=[("M", ".agents/rules/00-core-engineering.md")]):
            paths_ok, violations = self.runner.verify_protected_paths(maintenance_mode=False)
            self.assertFalse(paths_ok)
            self.assertIn(".agents/rules/00-core-engineering.md", violations)

    def test_maintenance_mode_allows_infrastructure_tasks(self):
        """Test 19: Infrastructure task with maintenance_mode=True allows protected paths."""
        with patch.object(self.runner, "get_changed_and_untracked_files", return_value=[("M", "automation/runner.py")]):
            paths_ok, violations = self.runner.verify_protected_paths(maintenance_mode=True)
            self.assertTrue(paths_ok)
            self.assertEqual(len(violations), 0)

    def test_idempotency_duplicate_execution_rejected(self):
        """Test 20: Re-executing identical (task_id, expected_git_head) is rejected."""
        self.runner.record_execution("T-IDEM", "HEAD-1", "exec-1")
        self.assertTrue(self.runner.is_already_executed("T-IDEM", "HEAD-1"))
        self.assertFalse(self.runner.is_already_executed("T-IDEM", "HEAD-2"))

        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": "T-IDEM",
            "expected_git_head": "HEAD-1",
            "content_hash": self.task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(initial_state), encoding="utf-8")
        result = self.runner.execute_task_cycle(dry_run=False)
        self.assertFalse(result)

    def test_transactions_missing_current_task_aborts(self):
        """Test 21: Missing CURRENT_TASK.md aborts execution and marks ERROR."""
        self.task_file.unlink()
        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": "T-NOTASK",
            "expected_git_head": self.runner.get_git_head(),
            "content_hash": self.task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(initial_state), encoding="utf-8")
        result = self.runner.execute_task_cycle(dry_run=False)
        self.assertFalse(result)
        saved = self.runner.load_state()
        self.assertEqual(saved["state"], "ERROR")
        self.assertIn("CURRENT_TASK.md missing", saved["last_error"])

    def test_transactions_content_hash_mismatch_aborts(self):
        """Test 22: Payload content hash mismatch aborts execution (partial write defense)."""
        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": "T-CORRUPT",
            "expected_git_head": self.runner.get_git_head(),
            "content_hash": "bad_hash_1234567890",
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(initial_state), encoding="utf-8")
        result = self.runner.execute_task_cycle(dry_run=False)
        self.assertFalse(result)
        saved = self.runner.load_state()
        self.assertEqual(saved["state"], "ERROR")
        self.assertIn("Content hash mismatch", saved["last_error"])

    def test_optimistic_concurrency_stale_version_rejected(self):
        """Test 23: Conflicting state_version write fails to save."""
        state1 = {"state": "READY", "state_version": 5, "task_id": "T1"}
        self.state_file.write_text(json.dumps(state1), encoding="utf-8")

        save_ok = self.runner.save_state({"state": "EXECUTING", "state_version": 4}, expected_version=4)
        self.assertFalse(save_ok)


class TestAutomatedAuditor(unittest.TestCase):
    """Tests 24-30: Automated Auditor two-stage checks, fail-closed CI, and grounded termination."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name) / "repo"
        self.repo_root.mkdir(parents=True)
        init_git_repo(self.repo_root)

        # Create docs structure for backlog checking
        docs_dir = self.repo_root / "docs" / "project"
        docs_dir.mkdir(parents=True)
        (docs_dir / "STATE.md").write_text("# State\nGate 2: BLOCKED ON LEARNER BASELINE\n", encoding="utf-8")
        (docs_dir / "BACKLOG.md").write_text("# Backlog\n- [ ] **TASK-030 (GATING BLOCKER)**: Learner baseline\n", encoding="utf-8")

        self.cp_dir = Path(self.temp_dir.name) / "external_cp"
        self.cp_dir.mkdir(parents=True)

        self.state_file = self.cp_dir / "STATE.json"
        self.current_task_file = self.cp_dir / "CURRENT_TASK.md"
        self.current_task_file.write_text("# Task\ntask_type: FEATURE\nmaintenance_mode: false\n", encoding="utf-8")
        self.next_task_file = self.cp_dir / "NEXT_TASK.md"
        self.events_file = self.cp_dir / "EVENTS.ndjson"

        self.config = {
            "control_plane_dir": str(self.cp_dir),
            "max_retries": 3,
            "skip_remote_verification": True,
            "skip_ci_for_tests": True,
            "mock_model_audit": True,
        }
        self.logger = SafeLogger()
        self.auditor = AutomatedAuditor(self.repo_root, self.config, self.logger)

    def tearDown(self):
        self.temp_dir.cleanup()

    def _set_task(self, task_id: str, content: Optional[str] = None) -> str:
        if content is None:
            content = f"""# Task: {task_id}
## Metadata
- **Task ID**: `{task_id}`
- **Task Type**: `FEATURE`
- **Maintenance Mode**: `false`

### Allowed Paths (Machine-Enforceable Scope)
allowed_paths:
  - docs/file.md
  - file.md
  - file.txt
  - scripts/validate_repo.py
allowed_path_prefixes: []
"""
        self.current_task_file.write_text(content, encoding="utf-8")
        return self.auditor.compute_file_hash(self.current_task_file)

    def test_auditor_prohibits_code_modification(self):
        """Test 24: Automated Auditor has zero methods that modify repository source code."""
        self.assertFalse(hasattr(self.auditor, "git_commit_and_push"))
        self.assertFalse(hasattr(self.auditor, "git_deliver"))

    def test_auditor_two_stage_approves_and_halts_at_human_required_gate(self):
        """Test 25: Auditor validates Stage A and Stage B, and grounds termination at Gate 2 (HUMAN_REQUIRED)."""
        commit_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo_root, text=True).strip()
        task_hash = self._set_task("T-AUDIT-OK")
        state = {
            "state": "AWAITING_AUDIT",
            "state_version": 2,
            "task_id": "T-AUDIT-OK",
            "execution_id": "exec-100",
            "resulting_git_head": commit_sha,
            "content_hash": task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(state), encoding="utf-8")

        with patch.object(self.auditor, "audit_commit_diff_and_scope", return_value=(True, ["docs/file.md"], "Diff OK")), \
             patch.object(self.auditor, "audit_ci_status", return_value=(True, "SUCCESS", "CI passed")):

            result = self.auditor.execute_audit_cycle(standalone_promote=False)
            self.assertTrue(result)
            saved = self.auditor.load_state()
            # Must halt at HUMAN_REQUIRED due to Gate 2 invariant!
            self.assertEqual(saved["state"], "HUMAN_REQUIRED")
            self.assertTrue(self.auditor.human_action_file.exists())
            self.assertTrue(self.auditor.audit_report_file.exists())

    def test_auditor_rejects_secret_leak_in_commit_diff(self):
        """Test 26: Potential secret in commit diff triggers FIX_REQUIRED in Stage A."""
        commit_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo_root, text=True).strip()
        task_hash = self._set_task("T-SECRET-DIFF")
        state = {
            "state": "AWAITING_AUDIT",
            "state_version": 2,
            "task_id": "T-SECRET-DIFF",
            "execution_id": "exec-101",
            "resulting_git_head": commit_sha,
            "content_hash": task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(state), encoding="utf-8")

        with patch.object(self.auditor, "audit_commit_diff_and_scope", return_value=(False, ["file.txt"], "SecretLeakDetected")):
            approved = self.auditor.execute_audit_cycle(standalone_promote=False)
            self.assertFalse(approved)
            saved = self.auditor.load_state()
            self.assertEqual(saved["state"], "FIX_REQUIRED")
            self.assertEqual(saved["retry_count"], 1)

    def test_auditor_rejects_protected_path_in_diff_without_metadata_authorization(self):
        """Test 27: Protected path modified in diff without immutable task authorization triggers FIX_REQUIRED."""
        commit_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo_root, text=True).strip()
        task_hash = self._set_task("T-PROTECT-DIFF")
        state = {
            "state": "AWAITING_AUDIT",
            "state_version": 2,
            "task_id": "T-PROTECT-DIFF",
            "execution_id": "exec-102",
            "resulting_git_head": commit_sha,
            "content_hash": task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(state), encoding="utf-8")

        with patch.object(self.auditor, "audit_commit_diff_and_scope", return_value=(False, ["scripts/validate_repo.py"], "ProtectedPathBreach")):
            approved = self.auditor.execute_audit_cycle(standalone_promote=False)
            self.assertFalse(approved)
            saved = self.auditor.load_state()
            self.assertEqual(saved["state"], "FIX_REQUIRED")

    def test_ci_fail_closed_pending_state_retains_awaiting_audit(self):
        """Test 28: CI still pending or queued MUST NOT approve; retains state AWAITING_AUDIT."""
        commit_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo_root, text=True).strip()
        task_hash = self._set_task("T-CI-PENDING")
        state = {
            "state": "AWAITING_AUDIT",
            "state_version": 2,
            "task_id": "T-CI-PENDING",
            "execution_id": "exec-103",
            "resulting_git_head": commit_sha,
            "content_hash": task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(state), encoding="utf-8")

        with patch.object(self.auditor, "audit_commit_diff_and_scope", return_value=(True, ["file.md"], "Diff OK")), \
             patch.object(self.auditor, "audit_ci_status", return_value=(False, "PENDING", "CI is queued")):

            result = self.auditor.execute_audit_cycle(standalone_promote=False)
            self.assertFalse(result)
            saved = self.auditor.load_state()
            self.assertEqual(saved["state"], "AWAITING_AUDIT")

    def test_ci_failure_transitions_to_fix_required(self):
        """Test 29: CI failure transitions state to FIX_REQUIRED with corrective task."""
        commit_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo_root, text=True).strip()
        task_hash = self._set_task("T-CI-FAIL")
        state = {
            "state": "AWAITING_AUDIT",
            "state_version": 2,
            "task_id": "T-CI-FAIL",
            "execution_id": "exec-104",
            "resulting_git_head": commit_sha,
            "content_hash": task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(state), encoding="utf-8")

        with patch.object(self.auditor, "audit_commit_diff_and_scope", return_value=(True, ["file.md"], "Diff OK")), \
             patch.object(self.auditor, "audit_ci_status", return_value=(False, "FAILED", "CI run failed tests")):

            result = self.auditor.execute_audit_cycle(standalone_promote=False)
            self.assertFalse(result)
            saved = self.auditor.load_state()
            self.assertEqual(saved["state"], "FIX_REQUIRED")
            self.assertEqual(saved["retry_count"], 1)

    def test_event_log_appends_valid_ndjson(self):
        """Test 30: State transitions append valid JSON lines to EVENTS.ndjson."""
        event = {"event": "TEST_EVENT", "task_id": "T1", "state": "READY"}
        self.auditor.append_event(event)
        self.assertTrue(self.events_file.exists())
        lines = self.events_file.read_text(encoding="utf-8").splitlines()
        self.assertTrue(len(lines) > 0)
        parsed = json.loads(lines[-1])
        self.assertEqual(parsed["event"], "TEST_EVENT")


class TestTaskScopeAndIndexContainment(unittest.TestCase):
    """Tests machine-enforceable task scope allowlists and technical index containment."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name) / "repo"
        self.repo_root.mkdir(parents=True)
        init_git_repo(self.repo_root)

        self.cp_dir = Path(self.temp_dir.name) / "external_control_plane"
        self.cp_dir.mkdir(parents=True)

        self.state_file = self.cp_dir / "STATE.json"
        self.current_task_file = self.cp_dir / "CURRENT_TASK.md"

        self.config = {
            "control_plane_dir": str(self.cp_dir),
            "max_retries": 3,
            "poll_interval_seconds": 1,
            "git_branch": "main",
            "disable_git_push": True,
        }
        self.logger = SafeLogger()
        self.runner = OrchestrationRunner(self.repo_root, self.config, self.logger)

    def tearDown(self):
        self.temp_dir.cleanup()

    def _setup_task(self, task_id: str, content: str):
        self.current_task_file.write_text(content, encoding="utf-8")
        task_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        head = self.runner.get_git_head()
        state = {
            "state": "READY",
            "state_version": 1,
            "task_id": task_id,
            "expected_git_head": head,
            "content_hash": task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(state), encoding="utf-8")
        return head

    def test_executor_staged_index_mutation_rejected(self):
        """Executor mutates Git staged index (git add without commit) -> GitContainmentViolation -> ERROR."""
        task_content = """# Task: T-INDEX-MUTATION
task_type: FEATURE
maintenance_mode: false
allowed_paths:
  - test.txt
"""
        self._setup_task("T-INDEX-MUTATION", task_content)

        def index_mutating_executor(prompt):
            (self.repo_root / "test.txt").write_text("modified", encoding="utf-8")
            subprocess.run(["git", "add", "test.txt"], cwd=self.repo_root, check=True)
            return (True, "Staged file directly")

        with patch.object(self.runner, "execute_agy", side_effect=index_mutating_executor):
            res = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(res)
            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "ERROR")
            self.assertIn("GitContainmentViolation", saved["last_error"])
            self.assertIn("staged index", saved["last_error"])
            self.assertTrue(self.runner.is_git_index_clean())

    def test_out_of_scope_normal_file_rejected(self):
        """Executor creates file outside task scope allowlist -> ScopeViolation -> FIX_REQUIRED."""
        task_content = """# Task: T-OUT-OF-SCOPE
task_type: FEATURE
maintenance_mode: false
allowed_paths:
  - docs/authorized.md
"""
        self._setup_task("T-OUT-OF-SCOPE", task_content)

        def out_of_scope_executor(prompt):
            docs_dir = self.repo_root / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)
            (docs_dir / "unauthorized.md").write_text("evil", encoding="utf-8")
            return (True, "Wrote unauthorized file")

        with patch.object(self.runner, "execute_agy", side_effect=out_of_scope_executor):
            res = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(res)
            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "FIX_REQUIRED")
            self.assertIn("ScopeViolation", saved["last_error"])
            self.assertIn("docs/unauthorized.md", saved["last_error"])
            self.assertTrue(self.runner.is_git_clean())

    def test_out_of_scope_deletion_rejected(self):
        """Executor deletes an out-of-scope tracked file -> ScopeViolation -> FIX_REQUIRED."""
        # Commit a file first
        tracked = self.repo_root / "existing.txt"
        tracked.write_text("existing content\n", encoding="utf-8")
        subprocess.run(["git", "add", "existing.txt"], cwd=self.repo_root, check=True)
        subprocess.run(["git", "commit", "-m", "chore: add existing.txt"], cwd=self.repo_root, check=True)

        task_content = """# Task: T-DELETE-OUT-OF-SCOPE
task_type: FEATURE
maintenance_mode: false
allowed_paths:
  - other.txt
"""
        self._setup_task("T-DELETE-OUT-OF-SCOPE", task_content)

        def deleting_executor(prompt):
            tracked.unlink()
            return (True, "Deleted tracked file")

        with patch.object(self.runner, "execute_agy", side_effect=deleting_executor):
            res = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(res)
            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "FIX_REQUIRED")
            self.assertIn("ScopeViolation", saved["last_error"])
            self.assertIn("existing.txt", saved["last_error"])

    def test_rename_checks_source_and_destination_scope(self):
        """Rename with out-of-scope source file -> ScopeViolation -> FIX_REQUIRED."""
        # Commit source file
        src_file = self.repo_root / "unauthorized_source.txt"
        src_file.write_text("source content\n", encoding="utf-8")
        subprocess.run(["git", "add", "unauthorized_source.txt"], cwd=self.repo_root, check=True)
        subprocess.run(["git", "commit", "-m", "chore: add source file"], cwd=self.repo_root, check=True)

        task_content = """# Task: T-RENAME-SCOPE
task_type: FEATURE
maintenance_mode: false
allowed_paths:
  - authorized_destination.txt
"""
        self._setup_task("T-RENAME-SCOPE", task_content)

        def rename_executor(prompt):
            src_file.rename(self.repo_root / "authorized_destination.txt")
            return (True, "Renamed file")

        with patch.object(self.runner, "execute_agy", side_effect=rename_executor):
            res = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(res)
            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "FIX_REQUIRED")
            self.assertIn("ScopeViolation", saved["last_error"])
            self.assertIn("unauthorized_source.txt", saved["last_error"])

    def test_maintenance_mode_does_not_bypass_task_scope(self):
        """maintenance_mode: true does NOT grant unlimited repo access without allowed_paths."""
        task_content = """# Task: T-MAINT-SCOPE
task_type: INFRASTRUCTURE
maintenance_mode: true
allowed_paths:
  - automation/runner.py
"""
        self._setup_task("T-MAINT-SCOPE", task_content)

        def rogue_maint_executor(prompt):
            # Tries to edit an out-of-scope file under the guise of maintenance mode
            (self.repo_root / "arbitrary.txt").write_text("exploit", encoding="utf-8")
            return (True, "Attempted out of scope write")

        with patch.object(self.runner, "execute_agy", side_effect=rogue_maint_executor):
            res = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(res)
            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "FIX_REQUIRED")
            self.assertIn("ScopeViolation", saved["last_error"])
            self.assertIn("arbitrary.txt", saved["last_error"])


class TestPathScopeNormalization(unittest.TestCase):
    """Unit tests for path scope normalization and directory boundary matching (Requirement 5)."""

    def test_normalize_scope_path_valid(self):
        self.assertEqual(normalize_scope_path("docs/foo.md"), "docs/foo.md")
        self.assertEqual(normalize_scope_path("./docs/foo.md"), "docs/foo.md")
        self.assertEqual(normalize_scope_path("docs/foo/"), "docs/foo")
        self.assertEqual(normalize_scope_path("automation/runner.py"), "automation/runner.py")

    def test_normalize_scope_path_rejects_traversal(self):
        self.assertIsNone(normalize_scope_path(".."))
        self.assertIsNone(normalize_scope_path("../docs/foo.md"))
        self.assertIsNone(normalize_scope_path("docs/../../etc/passwd"))
        self.assertIsNone(normalize_scope_path("docs/../bar.md"))

    def test_normalize_scope_path_rejects_absolute_and_wildcards(self):
        self.assertIsNone(normalize_scope_path("/etc/passwd"))
        self.assertIsNone(normalize_scope_path("C:/windows/win.ini"))
        self.assertIsNone(normalize_scope_path("."))
        self.assertIsNone(normalize_scope_path("/"))
        self.assertIsNone(normalize_scope_path(""))
        self.assertIsNone(normalize_scope_path("   \n\t  "))

    def test_prefix_boundary_matching_rejects_similar_sibling_names(self):
        """Prefix 'docs/foo' must NOT authorize 'docs/foobar/file.md'."""
        allowed_prefixes = ["docs/foo"]
        self.assertTrue(is_path_in_scope("docs/foo/file.md", [], allowed_prefixes))
        self.assertTrue(is_path_in_scope("docs/foo/sub/nested.md", [], allowed_prefixes))
        self.assertTrue(is_path_in_scope("docs/foo", [], allowed_prefixes))
        # Boundary violation: sibling directory starting with same prefix string
        self.assertFalse(is_path_in_scope("docs/foobar/file.md", [], allowed_prefixes))
        self.assertFalse(is_path_in_scope("docs/foobar.md", [], allowed_prefixes))
        self.assertFalse(is_path_in_scope("docs/foo_bar/file.md", [], allowed_prefixes))

    def test_exact_path_scope_matches_only_exact_file(self):
        allowed_paths = ["docs/assessment/baseline.md"]
        self.assertTrue(is_path_in_scope("docs/assessment/baseline.md", allowed_paths, []))
        self.assertFalse(is_path_in_scope("docs/assessment/other.md", allowed_paths, []))
        self.assertFalse(is_path_in_scope("docs/assessment/baseline.md/sub", allowed_paths, []))


if __name__ == "__main__":
    unittest.main()
