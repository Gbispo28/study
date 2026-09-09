#!/usr/bin/env python3
"""
Adversarial Test Suite for English Learning OS Automation Control Plane.
Tests state machine transitions, lock safety, git head divergence, secret sanitization,
and failure handling.
"""

import os
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from automation.runner import (
    sanitize_text,
    SafeLogger,
    RunnerLock,
    OrchestrationRunner,
)


class TestSecretSanitization(unittest.TestCase):
    """Verifies that secrets are stripped from log outputs."""

    def test_sanitize_github_tokens(self):
        # Concatenate string dynamically to avoid static secret scanner false positives
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
    """Verifies concurrency protection and stale lock cleanup."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.lock_path = Path(self.temp_dir.name) / ".lock"
        self.logger = SafeLogger()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_acquire_and_release(self):
        lock = RunnerLock(self.lock_path, self.logger)
        self.assertTrue(lock.acquire())
        self.assertTrue(self.lock_path.exists())
        lock.release()
        self.assertFalse(self.lock_path.exists())

    def test_prevent_concurrent_execution(self):
        lock1 = RunnerLock(self.lock_path, self.logger)
        lock2 = RunnerLock(self.lock_path, self.logger)
        self.assertTrue(lock1.acquire())
        # Second acquire by active PID must fail
        self.assertFalse(lock2.acquire())
        lock1.release()

    def test_stale_lock_cleanup_from_dead_pid(self):
        # Write lock with an impossible/inactive PID
        stale_data = {"pid": 999999, "acquired_at": "2026-01-01T00:00:00Z"}
        self.lock_path.write_text(json.dumps(stale_data), encoding="utf-8")

        lock = RunnerLock(self.lock_path, self.logger)
        # Should detect dead PID and acquire successfully
        self.assertTrue(lock.acquire())
        lock.release()


class TestOrchestrationStateMachine(unittest.TestCase):
    """Adversarial tests for the state machine transitions and invariants."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)
        self.orch_dir = self.repo_root / "orchestration"
        self.orch_dir.mkdir(parents=True)
        self.auto_dir = self.repo_root / "automation"
        self.auto_dir.mkdir(parents=True)

        self.state_file = self.orch_dir / "STATE.json"
        self.task_file = self.orch_dir / "CURRENT_TASK.md"
        self.task_file.write_text("# Test Task\nDo something safe.", encoding="utf-8")

        self.config = {
            "orchestration_dir": "orchestration",
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
            self.state_file.write_text(json.dumps({"state": st, "task_id": "T1"}), encoding="utf-8")
            result = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(result, f"Runner should not act on state {st}")

    def test_head_divergence_fails_to_error_state(self):
        initial_state = {
            "state": "READY",
            "task_id": "T-DIVERGE",
            "expected_git_head": "0000000000000000000000000000000000000000",
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(initial_state), encoding="utf-8")

        with patch.object(self.runner, "get_git_head", return_value="1111111111111111111111111111111111111111"):
            success = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(success)

            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "ERROR")
            self.assertIn("Git HEAD divergence", saved["last_error"])

    def test_successful_task_cycle_advances_to_awaiting_audit(self):
        initial_state = {
            "state": "READY",
            "task_id": "T-SUCCESS",
            "expected_git_head": "HEAD_OK",
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(initial_state), encoding="utf-8")

        with patch.object(self.runner, "get_git_head", return_value="HEAD_OK"), \
             patch.object(self.runner, "execute_agy", return_value=(True, "Executed successfully")), \
             patch.object(self.runner, "run_quality_gate", return_value=(True, "All passed")), \
             patch.object(self.runner, "git_commit_and_push", return_value=(True, "Pushed", "HEAD_NEW")):

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
            "task_id": "T-FAIL-QG",
            "expected_git_head": "HEAD_OK",
            "retry_count": 0,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(initial_state), encoding="utf-8")

        with patch.object(self.runner, "get_git_head", return_value="HEAD_OK"), \
             patch.object(self.runner, "execute_agy", return_value=(True, "Executed successfully")), \
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
            "task_id": "T-MAX-RETRIES",
            "expected_git_head": "HEAD_OK",
            "retry_count": 2,
            "max_retries": 3,
        }
        self.state_file.write_text(json.dumps(initial_state), encoding="utf-8")

        with patch.object(self.runner, "get_git_head", return_value="HEAD_OK"), \
             patch.object(self.runner, "execute_agy", return_value=(True, "Executed")), \
             patch.object(self.runner, "run_quality_gate", return_value=(False, "Failed again")):

            success = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(success)

            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "ERROR")
            self.assertEqual(saved["retry_count"], 3)


if __name__ == "__main__":
    unittest.main()
