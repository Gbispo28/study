#!/usr/bin/env python3
"""
Integration Tests for English Learning OS Automation Control Plane.
Validates real filesystem and git interactions in temporary isolated repositories:
- True selective staging (no git add .)
- Technical git containment (detecting unauthorized commits, branch switches)
- Protected path authorization strictly from immutable task metadata (commit message bypass rejected)
- CI parser fail-closed behavior across the full state matrix
- Stage B model review malformed output handling
- Grounded loop termination at Gate 2 (HUMAN_REQUIRED)
"""

import os
import json
import shutil
import tempfile
import subprocess
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from automation.runner import OrchestrationRunner, SafeLogger, PROTECTED_PATHS
from automation.auditor import AutomatedAuditor


def create_sandbox_repo(base_dir: Path) -> Path:
    """Initializes a clean Git repository in a temporary directory."""
    repo = base_dir / "repo"
    repo.mkdir(parents=True)
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Integration Tester"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "integration@test.local"], cwd=repo, check=True, capture_output=True)

    gitignore = repo / ".gitignore"
    gitignore.write_text("automation/state/\nautomation/logs/\nautomation/.lock\n", encoding="utf-8")
    subprocess.run(["git", "add", ".gitignore"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "chore: initialize repository"], cwd=repo, check=True, capture_output=True)

    # Set up canonical project docs for backlog inspection
    docs_dir = repo / "docs" / "project"
    docs_dir.mkdir(parents=True)
    (docs_dir / "STATE.md").write_text("# Project State\nGate 2: BLOCKED ON LEARNER BASELINE\nPhase 03: LOCKED\n", encoding="utf-8")
    (docs_dir / "BACKLOG.md").write_text(
        "# Backlog\n"
        "- [x] **TASK-029**: Audit requirements\n"
        "- [ ] **TASK-030 (GATING BLOCKER)**: Receive learner responses to BASELINE_FORM.md\n"
        "- [ ] **TASK-031**: Daily journey (LOCKED)\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "docs/"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "docs: initialize project state and backlog"], cwd=repo, check=True, capture_output=True)

    return repo


class TestRunnerIntegration(unittest.TestCase):
    """Tests real runner delivery, selective staging, and containment."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)
        self.repo_root = create_sandbox_repo(self.base_dir)

        self.cp_dir = self.base_dir / "external_control_plane"
        self.cp_dir.mkdir(parents=True)

        self.config = {
            "control_plane_dir": str(self.cp_dir),
            "max_retries": 3,
            "disable_git_push": True,
        }
        self.logger = SafeLogger()
        self.runner = OrchestrationRunner(self.repo_root, self.config, self.logger)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_real_selective_staging_and_commit(self):
        """Runner stages only explicit changed files and rejects repository-wide blind staging."""
        # Create an allowed modified file and an untracked file
        file1 = self.repo_root / "learning_note.txt"
        file1.write_text("Vocabulary note content", encoding="utf-8")

        items = self.runner.get_changed_and_untracked_files()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0][1], "learning_note.txt")

        ok, msg, head = self.runner.git_deliver("TASK-TEST-STAGE", "add learning note", maintenance_mode=False)
        self.assertTrue(ok)
        self.assertIsNotNone(head)

        # Verify git commit log has the atomic commit
        log_out = subprocess.check_output(["git", "log", "-1", "--format=%B"], cwd=self.repo_root, text=True)
        self.assertIn("feat(task): TASK-TEST-STAGE - add learning note", log_out)

        # Working tree must now be 100% clean
        self.assertTrue(self.runner.is_git_clean())

    def test_selective_staging_rejects_sensitive_files(self):
        """Runner detects and refuses to stage sensitive credential files like .env."""
        env_file = self.repo_root / ".env"
        env_file.write_text("SECRET_KEY=12345", encoding="utf-8")

        ok, msg, head = self.runner.git_deliver("TASK-ENV", "bad commit", maintenance_mode=False)
        self.assertFalse(ok)
        self.assertIn("Sensitive file detected", msg)

        # Ensure .env was NOT staged
        cached_diff = subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=self.repo_root, text=True)
        self.assertNotIn(".env", cached_diff)

    def test_containment_catches_unauthorized_executor_commit(self):
        """Runner asserts pre_head == post_head; catches and rolls back if executor ran git commit."""
        pre_head = self.runner.get_git_head()

        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": "T-ROGUE-COMMIT",
            "expected_git_head": pre_head,
            "content_hash": "dummy",
            "retry_count": 0,
            "max_retries": 3,
        }
        self.runner.state_file.write_text(json.dumps(initial_state), encoding="utf-8")
        task_file = self.runner.current_task_file
        task_file.write_text("# Task\nmaintenance_mode: false\n", encoding="utf-8")
        initial_state["content_hash"] = self.runner.compute_file_hash(task_file)
        self.runner.state_file.write_text(json.dumps(initial_state), encoding="utf-8")

        # Simulate rogue executor committing directly
        def rogue_executor(prompt):
            (self.repo_root / "rogue.txt").write_text("rogue", encoding="utf-8")
            subprocess.run(["git", "add", "rogue.txt"], cwd=self.repo_root, check=True)
            subprocess.run(["git", "commit", "-m", "rogue executor commit"], cwd=self.repo_root, check=True)
            return (True, "Rogue commit executed")

        with patch.object(self.runner, "execute_agy", side_effect=rogue_executor):
            result = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(result)
            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "ERROR")
            self.assertIn("GitContainmentViolation", saved["last_error"])
            # Working tree and HEAD must be restored to pre_head
            self.assertEqual(self.runner.get_git_head(), pre_head)
            self.assertTrue(self.runner.is_git_clean())

    def test_containment_catches_unauthorized_branch_switch(self):
        """Runner catches and rolls back if executor switches branch."""
        pre_head = self.runner.get_git_head()
        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": "T-ROGUE-BRANCH",
            "expected_git_head": pre_head,
            "content_hash": "dummy",
            "retry_count": 0,
            "max_retries": 3,
        }
        task_file = self.runner.current_task_file
        task_file.write_text("# Task\nmaintenance_mode: false\n", encoding="utf-8")
        initial_state["content_hash"] = self.runner.compute_file_hash(task_file)
        self.runner.state_file.write_text(json.dumps(initial_state), encoding="utf-8")

        def rogue_branch_executor(prompt):
            subprocess.run(["git", "checkout", "-b", "rogue_branch"], cwd=self.repo_root, check=True)
            return (True, "Switched branch")

        with patch.object(self.runner, "execute_agy", side_effect=rogue_branch_executor):
            result = self.runner.execute_task_cycle(dry_run=False)
            self.assertFalse(result)
            saved = self.runner.load_state()
            self.assertEqual(saved["state"], "ERROR")
            self.assertIn("GitContainmentViolation", saved["last_error"])
            # Must be back on main branch
            self.assertIn(self.runner.get_git_branch(), ["main", "master"])


class TestAuditorIntegration(unittest.TestCase):
    """Tests real auditor verification gates, fail-closed CI, and termination."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)
        self.repo_root = create_sandbox_repo(self.base_dir)

        self.cp_dir = self.base_dir / "external_control_plane"
        self.cp_dir.mkdir(parents=True)

        self.config = {
            "control_plane_dir": str(self.cp_dir),
            "max_retries": 3,
            "skip_remote_verification": True,
            "skip_ci_for_tests": False,
            "mock_model_audit": False,
        }
        self.logger = SafeLogger()
        self.auditor = AutomatedAuditor(self.repo_root, self.config, self.logger)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_protected_path_authorization_rejects_commit_message_bypass(self):
        """
        Adversarial test: Commit modifies scripts/validate_repo.py and has
        commit message 'feat: maintenance_mode infra fix', but CURRENT_TASK.md
        has task_type: FEATURE. Auditor MUST reject the change!
        """
        # Commit modifying scripts/validate_repo.py
        val_script = self.repo_root / "scripts" / "validate_repo.py"
        val_script.parent.mkdir(parents=True, exist_ok=True)
        val_script.write_text("# Modified validator\n", encoding="utf-8")
        subprocess.run(["git", "add", "scripts/validate_repo.py"], cwd=self.repo_root, check=True)
        subprocess.run(
            ["git", "commit", "-m", "feat: maintenance_mode infra fix attempts bypass"],
            cwd=self.repo_root,
            check=True,
        )
        commit_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo_root, text=True).strip()

        # Set task with task_type: FEATURE (not authorized for infra)
        task_file = self.auditor.current_task_file
        task_file.write_text("# Regular Task\ntask_type: FEATURE\nmaintenance_mode: false\n", encoding="utf-8")
        task_hash = self.auditor.compute_file_hash(task_file)

        ok, changed_files, diff_out = self.auditor.audit_commit_diff_and_scope(
            commit_sha=commit_sha,
            expected_parent=None,
            task_id="TASK-BYPASS",
            expected_task_hash=task_hash,
        )
        self.assertFalse(ok)
        self.assertIn("ProtectedPathBreach", diff_out)
        self.assertIn("without immutable task authorization", diff_out)

    def test_ci_fail_closed_status_matrix(self):
        """Verifies fail-closed behavior across the entire CI status/conclusion matrix."""
        commit = "1111111111111111111111111111111111111111"

        # Case 1: gh missing
        with patch("shutil.which", return_value=None):
            ok, cat, msg = self.auditor.audit_ci_status(commit)
            self.assertFalse(ok)
            self.assertEqual(cat, "UNVERIFIABLE")

        # Case 2: gh returns non-zero error
        with patch("shutil.which", return_value="/usr/bin/gh"), \
             patch("subprocess.run", return_value=subprocess.CompletedProcess([], 1, stdout="", stderr="network error")):
            ok, cat, msg = self.auditor.audit_ci_status(commit)
            self.assertFalse(ok)
            self.assertEqual(cat, "UNVERIFIABLE")

        # Case 3: no runs recorded yet
        with patch("shutil.which", return_value="/usr/bin/gh"), \
             patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, stdout="[]", stderr="")):
            ok, cat, msg = self.auditor.audit_ci_status(commit)
            self.assertFalse(ok)
            self.assertEqual(cat, "PENDING")

        # Case 4: queued run
        queued_json = json.dumps([{"status": "queued", "conclusion": None, "databaseId": 101}])
        with patch("shutil.which", return_value="/usr/bin/gh"), \
             patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, stdout=queued_json, stderr="")):
            ok, cat, msg = self.auditor.audit_ci_status(commit)
            self.assertFalse(ok)
            self.assertEqual(cat, "PENDING")

        # Case 5: in_progress run
        prog_json = json.dumps([{"status": "in_progress", "conclusion": None, "databaseId": 102}])
        with patch("shutil.which", return_value="/usr/bin/gh"), \
             patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, stdout=prog_json, stderr="")):
            ok, cat, msg = self.auditor.audit_ci_status(commit)
            self.assertFalse(ok)
            self.assertEqual(cat, "PENDING")

        # Case 6: completed with failure
        fail_json = json.dumps([{"status": "completed", "conclusion": "failure", "databaseId": 103}])
        with patch("shutil.which", return_value="/usr/bin/gh"), \
             patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, stdout=fail_json, stderr="")):
            ok, cat, msg = self.auditor.audit_ci_status(commit)
            self.assertFalse(ok)
            self.assertEqual(cat, "FAILED")

        # Case 7: completed with cancelled
        cancel_json = json.dumps([{"status": "completed", "conclusion": "cancelled", "databaseId": 104}])
        with patch("shutil.which", return_value="/usr/bin/gh"), \
             patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, stdout=cancel_json, stderr="")):
            ok, cat, msg = self.auditor.audit_ci_status(commit)
            self.assertFalse(ok)
            self.assertEqual(cat, "FAILED")

        # Case 8: completed with success -> ONLY ONE THAT APPROVES
        succ_json = json.dumps([{"status": "completed", "conclusion": "success", "databaseId": 105}])
        with patch("shutil.which", return_value="/usr/bin/gh"), \
             patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, stdout=succ_json, stderr="")):
            ok, cat, msg = self.auditor.audit_ci_status(commit)
            self.assertTrue(ok)
            self.assertEqual(cat, "SUCCESS")

    def test_stage_b_rejects_malformed_model_output(self):
        """Stage B fails closed when the auditor model returns non-JSON or invalid schema."""
        with patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, stdout="Not a JSON response at all", stderr="")):
            ok, result, model = self.auditor.execute_stage_b_model_audit(
                task_content="task", commit_sha="head", changed_files=[], diff_text="", ci_summary=""
            )
            self.assertFalse(ok)

        # Malformed schema: invalid verdict "LOOKS_PERFECT"
        invalid_schema = json.dumps({"verdict": "LOOKS_PERFECT", "findings": []})
        with patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, stdout=invalid_schema, stderr="")):
            ok, result, model = self.auditor.execute_stage_b_model_audit(
                task_content="task", commit_sha="head", changed_files=[], diff_text="", ci_summary=""
            )
            self.assertFalse(ok)

    def test_grounded_termination_at_gate_2(self):
        """Auditor halts at HUMAN_REQUIRED because Gate 2 is blocked on learner baseline."""
        plan = self.auditor.plan_next_operational_state("TASK-INFRA-01")
        self.assertEqual(plan["action"], "HUMAN_REQUIRED")
        self.assertIn("GATE 2: BLOCKED ON LEARNER BASELINE", plan["blocker"])
        self.assertTrue(self.auditor.human_action_file.exists())
        human_text = self.auditor.human_action_file.read_text(encoding="utf-8")
        self.assertIn("Administer Learner Baseline Diagnostic (TASK-030)", human_text)


if __name__ == "__main__":
    unittest.main()
