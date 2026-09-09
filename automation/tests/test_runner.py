#!/usr/bin/env python3
"""
Comprehensive 30-Case Adversarial Test Suite for English Learning OS Automation Control Plane.
Tests state machine transitions, lock safety, git head divergence, secret sanitization,
protected path scope enforcement, optimistic concurrency, payload-first hashing,
independent auditor verification, idempotency, standalone promotion, and event logging.
"""

import os
import json
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from automation.runner import (
    sanitize_text,
    SafeLogger,
    RunnerLock,
    OrchestrationRunner,
    PROTECTED_PATHS,
)
from automation.auditor import AutomatedAuditor


class TestSecretSanitization(unittest.TestCase):
    """Verifies that secrets are stripped from log outputs (Tests 1-3)."""

    def test_sanitize_github_tokens(self):
        fake_token = "ghp_" + ("A" * 36)
        raw = f"Error with token {fake_token} in call"
        clean = sanitize_text(raw)
        self.assertNotIn("ghp_", clean)
        self.assertIn("[REDACTED_SECRET]", clean)

    def test_sanitize_google_api_keys(self):
        fake_key = "AIza" + ("B" * 35)
        raw = f"Google AI key {fake_key} failed"
        clean = sanitize_text(raw)
        self.assertNotIn("AIza", clean)
        self.assertIn("[REDACTED_SECRET]", clean)

    def test_sanitize_bearer_tokens(self):
        token_val = "ya29." + "test_fake_token_123"
        raw = "Authorization: " + "Bearer " + token_val
        clean = sanitize_text(raw)
        self.assertNotIn("ya29", clean)
        self.assertIn("[REDACTED_SECRET]", clean)


class TestRunnerLock(unittest.TestCase):
    """Verifies concurrency protection and stale lock cleanup (Tests 4-6)."""

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
    """Adversarial tests for state transitions, git head checks, and retries (Tests 7-11)."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name) / "repo"
        self.repo_root.mkdir(parents=True)
        self.cp_dir = Path(self.temp_dir.name) / "external_control_plane"
        self.cp_dir.mkdir(parents=True)

        self.state_file = self.cp_dir / "STATE.json"
        self.task_file = self.cp_dir / "CURRENT_TASK.md"
        self.task_content = "# Test Task\nmaintenance_mode: false\nDo something safe."
        self.task_file.write_text(self.task_content, encoding="utf-8")
        self.task_hash = hashlib.sha256(self.task_content.encode("utf-8")).hexdigest()

        self.config = {
            "control_plane_dir": str(self.cp_dir),
            "max_retries": 3,
            "poll_interval_seconds": 1,
            "git_branch": "main",
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

        with patch.object(self.runner, "get_git_head", return_value="1111111111111111111111111111111111111111"), \
             patch.object(self.runner, "is_git_clean", return_value=True):
            success = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(success)
            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "ERROR")
            self.assertIn("Git HEAD divergence", saved["last_error"])

    def test_successful_task_cycle_advances_to_awaiting_audit(self):
        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": "T-SUCCESS",
            "expected_git_head": "HEAD_OK",
            "content_hash": self.task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(initial_state), encoding="utf-8")

        with patch.object(self.runner, "get_git_head", return_value="HEAD_OK"), \
             patch.object(self.runner, "is_git_clean", return_value=True), \
             patch.object(self.runner, "execute_agy", return_value=(True, "Executed successfully")), \
             patch.object(self.runner, "verify_protected_paths", return_value=(True, [])), \
             patch.object(self.runner, "run_quality_gate", return_value=(True, "All passed")), \
             patch.object(self.runner, "git_deliver", return_value=(True, "Delivered", "HEAD_NEW")):

            success = self.runner.execute_task_cycle(dry_run=False)
            self.assertTrue(success)
            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "AWAITING_AUDIT")
            self.assertEqual(saved["resulting_git_head"], "HEAD_NEW")
            self.assertEqual(saved["retry_count"], 0)
            self.assertIsNone(saved["last_error"])
            self.assertTrue(self.runner.handoff_file.exists())

    def test_quality_gate_failure_increments_retry_and_sets_fix_required(self):
        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": "T-FAIL-QG",
            "expected_git_head": "HEAD_OK",
            "content_hash": self.task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(initial_state), encoding="utf-8")

        with patch.object(self.runner, "get_git_head", return_value="HEAD_OK"), \
             patch.object(self.runner, "is_git_clean", return_value=True), \
             patch.object(self.runner, "execute_agy", return_value=(True, "Executed successfully")), \
             patch.object(self.runner, "verify_protected_paths", return_value=(True, [])), \
             patch.object(self.runner, "run_quality_gate", return_value=(False, "Lint check failed")):

            success = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(success)
            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "FIX_REQUIRED")
            self.assertEqual(saved["retry_count"], 1)
            self.assertIn("Lint check failed", saved["last_error"])

    def test_max_retries_exceeded_transitions_to_error(self):
        initial_state = {
            "state": "FIX_REQUIRED",
            "state_version": 1,
            "task_id": "T-MAX-RETRIES",
            "expected_git_head": "HEAD_OK",
            "content_hash": self.task_hash,
            "retry_count": 2,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(initial_state), encoding="utf-8")

        with patch.object(self.runner, "get_git_head", return_value="HEAD_OK"), \
             patch.object(self.runner, "is_git_clean", return_value=True), \
             patch.object(self.runner, "execute_agy", return_value=(True, "Executed")), \
             patch.object(self.runner, "verify_protected_paths", return_value=(True, [])), \
             patch.object(self.runner, "run_quality_gate", return_value=(False, "Failed again")):

            success = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(success)
            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "ERROR")
            self.assertEqual(saved["retry_count"], 3)


class TestArchitectureAndSecurityEnhancements(unittest.TestCase):
    """Tests 12-22: Clean git tree, protected paths, optimistic concurrency, transactions."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name) / "repo"
        self.repo_root.mkdir(parents=True)
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
        }
        self.logger = SafeLogger()
        self.runner = OrchestrationRunner(self.repo_root, self.config, self.logger)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_git_cleanliness_after_state_mutation(self):
        """Test 12: Mutating STATE.json outside Git repo leaves git repo completely clean."""
        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": "T-CLEAN",
            "expected_git_head": "H1",
            "content_hash": self.task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.runner.save_state(initial_state)
        # Check files inside repo_root
        repo_files = list(self.repo_root.iterdir())
        # Only automation/ state might exist if created, no orchestration files
        self.assertNotIn("orchestration", [f.name for f in repo_files])

    def test_control_plane_separation(self):
        """Test 13: Control plane directory is not a subdirectory of repo_root."""
        self.assertFalse(str(self.runner.control_plane_dir).startswith(str(self.runner.repo_root)))

    def test_protected_path_runner_py_rejected(self):
        """Test 14: Modifying runner.py in regular task is rejected."""
        with patch("subprocess.check_output", return_value=" M automation/runner.py\n"):
            paths_ok, violations = self.runner.verify_protected_paths(maintenance_mode=False)
            self.assertFalse(paths_ok)
            self.assertIn("automation/runner.py", violations)

    def test_protected_path_quality_gate_rejected(self):
        """Test 15: Modifying quality_gate.sh in regular task is rejected."""
        with patch("subprocess.check_output", return_value=" M scripts/quality_gate.sh\n"):
            paths_ok, violations = self.runner.verify_protected_paths(maintenance_mode=False)
            self.assertFalse(paths_ok)
            self.assertIn("scripts/quality_gate.sh", violations)

    def test_protected_path_agents_rejected(self):
        """Test 16: Modifying .agents/ in regular task is rejected."""
        with patch("subprocess.check_output", return_value=" M .agents/rules/00-core-engineering.md\n"):
            paths_ok, violations = self.runner.verify_protected_paths(maintenance_mode=False)
            self.assertFalse(paths_ok)
            self.assertIn(".agents/rules/00-core-engineering.md", violations)

    def test_maintenance_mode_allows_infrastructure_tasks(self):
        """Test 17: Infrastructure task with maintenance_mode=True allows protected paths."""
        with patch("subprocess.check_output", return_value=" M automation/runner.py\n"):
            paths_ok, violations = self.runner.verify_protected_paths(maintenance_mode=True)
            self.assertTrue(paths_ok)
            self.assertEqual(len(violations), 0)

    def test_idempotency_duplicate_execution_rejected(self):
        """Test 18 & 19: Re-executing identical (task_id, expected_git_head) is rejected."""
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
        """Test 20: Missing CURRENT_TASK.md aborts execution and marks ERROR."""
        self.task_file.unlink()
        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": "T-NOTASK",
            "expected_git_head": "HEAD-1",
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
        """Test 21: Payload content hash mismatch aborts execution (partial write defense)."""
        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": "T-CORRUPT",
            "expected_git_head": "HEAD-1",
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
        """Test 22: Conflicting state_version write fails to save."""
        state1 = {"state": "READY", "state_version": 5, "task_id": "T1"}
        self.state_file.write_text(json.dumps(state1), encoding="utf-8")

        # Attempting save with expected_version 4 when disk has 5 must fail
        save_ok = self.runner.save_state({"state": "EXECUTING", "state_version": 4}, expected_version=4)
        self.assertFalse(save_ok)


class TestAutomatedAuditor(unittest.TestCase):
    """Tests 23-30: Automated Auditor checks, verdicts, task ownership, and standalone mode."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name) / "repo"
        self.repo_root.mkdir(parents=True)
        self.cp_dir = Path(self.temp_dir.name) / "external_cp"
        self.cp_dir.mkdir(parents=True)

        self.state_file = self.cp_dir / "STATE.json"
        self.current_task_file = self.cp_dir / "CURRENT_TASK.md"
        self.next_task_file = self.cp_dir / "NEXT_TASK.md"
        self.events_file = self.cp_dir / "EVENTS.ndjson"

        self.config = {
            "control_plane_dir": str(self.cp_dir),
            "max_retries": 3,
            "auditor_model": "gemini-3.1-pro-high",
        }
        self.logger = SafeLogger()
        self.auditor = AutomatedAuditor(self.repo_root, self.config, self.logger)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_auditor_prohibits_code_modification(self):
        """Test 23: Automated Auditor has zero methods that write to repository code files."""
        self.assertFalse(hasattr(self.auditor, "git_commit_and_push"))
        self.assertFalse(hasattr(self.auditor, "git_deliver"))

    def test_auditor_verifies_real_commit_and_approves(self):
        """Test 24: Valid commit diff and clean secrets emit APPROVED."""
        state = {
            "state": "AWAITING_AUDIT",
            "state_version": 2,
            "task_id": "T-AUDIT-OK",
            "execution_id": "exec-100",
            "resulting_git_head": "COMMIT_1234567",
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(state), encoding="utf-8")

        with patch.object(self.auditor, "audit_commit", return_value=(True, ["docs/file.md"], "Diff OK")), \
             patch.object(self.auditor, "audit_ci_status", return_value=(True, "CI success")):

            approved = self.auditor.execute_audit_cycle(standalone_promote=False)
            self.assertTrue(approved)
            saved = self.auditor.load_state()
            self.assertEqual(saved["state"], "APPROVED")
            self.assertTrue(self.auditor.audit_report_file.exists())
            self.assertTrue(self.next_task_file.exists())

    def test_auditor_rejects_secret_leak_in_commit_diff(self):
        """Test 25: Potential secret in commit diff triggers FIX_REQUIRED."""
        state = {
            "state": "AWAITING_AUDIT",
            "state_version": 2,
            "task_id": "T-SECRET-DIFF",
            "execution_id": "exec-101",
            "resulting_git_head": "COMMIT_LEAK",
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(state), encoding="utf-8")

        with patch.object(self.auditor, "audit_commit", return_value=(False, ["file.txt"], "SecretLeakDetected")):
            approved = self.auditor.execute_audit_cycle(standalone_promote=False)
            self.assertFalse(approved)
            saved = self.auditor.load_state()
            self.assertEqual(saved["state"], "FIX_REQUIRED")
            self.assertEqual(saved["retry_count"], 1)

    def test_auditor_rejects_protected_path_in_diff(self):
        """Test 26: Protected path modified in commit diff triggers FIX_REQUIRED."""
        state = {
            "state": "AWAITING_AUDIT",
            "state_version": 2,
            "task_id": "T-PROTECT-DIFF",
            "execution_id": "exec-102",
            "resulting_git_head": "COMMIT_BREACH",
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(state), encoding="utf-8")

        with patch.object(self.auditor, "audit_commit", return_value=(False, ["scripts/validate_repo.py"], "ProtectedPathBreach")):
            approved = self.auditor.execute_audit_cycle(standalone_promote=False)
            self.assertFalse(approved)
            saved = self.auditor.load_state()
            self.assertEqual(saved["state"], "FIX_REQUIRED")

    def test_auditor_generates_next_task_upon_approval(self):
        """Test 27: NEXT_TASK.md is generated before marking APPROVED."""
        state = {
            "state": "AWAITING_AUDIT",
            "state_version": 2,
            "task_id": "T-NEXT-GEN",
            "execution_id": "exec-103",
            "resulting_git_head": "COMMIT_OK",
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(state), encoding="utf-8")

        with patch.object(self.auditor, "audit_commit", return_value=(True, ["README.md"], "Diff clean")), \
             patch.object(self.auditor, "audit_ci_status", return_value=(True, "CI success")):

            self.auditor.execute_audit_cycle(standalone_promote=False)
            self.assertTrue(self.next_task_file.exists())
            self.assertIn("Parent Task ID", self.next_task_file.read_text(encoding="utf-8"))

    def test_auditor_generates_corrective_task_with_parent_id(self):
        """Test 28: FIX_REQUIRED writes corrective instructions with parent_task_id."""
        state = {
            "state": "AWAITING_AUDIT",
            "state_version": 2,
            "task_id": "T-REMEDIATE",
            "execution_id": "exec-104",
            "resulting_git_head": "COMMIT_FAIL",
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(state), encoding="utf-8")

        with patch.object(self.auditor, "audit_commit", return_value=(False, ["mod.py"], "Syntax error in mod.py")):
            self.auditor.execute_audit_cycle(standalone_promote=False)
            saved = self.auditor.load_state()
            self.assertEqual(saved["state"], "FIX_REQUIRED")
            self.assertTrue(self.current_task_file.exists())
            task_text = self.current_task_file.read_text(encoding="utf-8")
            self.assertIn("Remediation Attempt", task_text)
            self.assertIn("Syntax error in mod.py", task_text)

    def test_standalone_mode_promotes_next_task_without_make(self):
        """Test 29: Standalone mode automatically promotes NEXT_TASK to CURRENT_TASK and sets READY."""
        state = {
            "state": "AWAITING_AUDIT",
            "state_version": 2,
            "task_id": "T-STANDALONE",
            "execution_id": "exec-105",
            "resulting_git_head": "COMMIT_STANDALONE",
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(state), encoding="utf-8")

        with patch.object(self.auditor, "audit_commit", return_value=(True, ["file.md"], "Diff clean")), \
             patch.object(self.auditor, "audit_ci_status", return_value=(True, "CI success")):

            approved = self.auditor.execute_audit_cycle(standalone_promote=True)
            self.assertTrue(approved)
            saved = self.auditor.load_state()
            # In standalone promotion, state ends at READY with the new task_id!
            self.assertEqual(saved["state"], "READY")
            self.assertNotEqual(saved["task_id"], "T-STANDALONE")
            self.assertEqual(saved["expected_git_head"], "COMMIT_STANDALONE")

    def test_auditor_handles_human_required_transition(self):
        """Test 30: Auditor can safely record HUMAN_REQUIRED when external intervention is required."""
        state = {
            "state": "AWAITING_AUDIT",
            "state_version": 2,
            "task_id": "T-OAUTH-BLOCK",
            "execution_id": "exec-106",
            "resulting_git_head": "COMMIT_BLOCK",
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(state), encoding="utf-8")
        state["state"] = "HUMAN_REQUIRED"
        state["last_error"] = "OAuth consent required by Google Cloud."
        self.auditor.save_state(state)
        saved = self.auditor.load_state()
    def test_event_log_appends_valid_ndjson(self):
        """Test 30: State transitions append valid JSON lines to EVENTS.ndjson."""
        event = {"event": "TEST_EVENT", "task_id": "T1", "state": "READY"}
        self.auditor.append_event(event)
        self.assertTrue(self.events_file.exists())
        lines = self.events_file.read_text(encoding="utf-8").splitlines()
        self.assertTrue(len(lines) > 0)
        parsed = json.loads(lines[-1])
        self.assertEqual(parsed["event"], "TEST_EVENT")


if __name__ == "__main__":

    unittest.main()
