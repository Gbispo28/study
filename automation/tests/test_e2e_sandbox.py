#!/usr/bin/env python3
"""
SANDBOX INTEGRATION LIFECYCLE TEST for English Learning OS Automation Control Plane.
Demonstrates a complete task lifecycle in a temporary sandbox environment:
real temporary task -> runner -> working tree modification -> selective staging ->
local commit -> deterministic audit (Stage A) -> model audit (Stage B) ->
APPROVED -> terminal HUMAN_REQUIRED behavior (Gate 2 Learner Baseline blocker).
Zero mutation to production repository.
Mocks external boundaries (agy executor, model audit, remote CI).
"""

import os
import json
import shutil
import tempfile
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from automation.runner import OrchestrationRunner, SafeLogger
from automation.auditor import AutomatedAuditor


class TestEndToEndSandboxCycle(unittest.TestCase):
    """SANDBOX INTEGRATION LIFECYCLE TEST: Demonstrates complete lifecycle with sandboxed external boundaries."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)

        # 1. Initialize isolated sandbox git repo
        self.repo_root = self.base_dir / "sandbox_repo"
        self.repo_root.mkdir(parents=True)
        subprocess.run(["git", "init", "-b", "main"], cwd=self.repo_root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Sandbox Auditor"], cwd=self.repo_root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "sandbox@auditor.local"], cwd=self.repo_root, check=True, capture_output=True)

        gitignore = self.repo_root / ".gitignore"
        gitignore.write_text("automation/state/\nautomation/logs/\nautomation/.lock\n", encoding="utf-8")
        subprocess.run(["git", "add", ".gitignore"], cwd=self.repo_root, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "chore: initialize sandbox repository"], cwd=self.repo_root, check=True, capture_output=True)

        # Set up canonical project documentation reflecting Gate 2 status
        docs_dir = self.repo_root / "docs" / "project"
        docs_dir.mkdir(parents=True)
        (docs_dir / "STATE.md").write_text("# Project State\nGate 2: BLOCKED ON LEARNER BASELINE\nPhase 03: LOCKED\n", encoding="utf-8")
        (docs_dir / "BACKLOG.md").write_text(
            "# Backlog\n"
            "- [x] **TASK-029**: Audit requirements\n"
            "- [ ] **TASK-030 (GATING BLOCKER)**: Receive learner responses to BASELINE_FORM.md\n"
            "- [ ] **TASK-031**: Daily journey (LOCKED)\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "docs/"], cwd=self.repo_root, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "docs: initialize project governance and backlog"], cwd=self.repo_root, check=True, capture_output=True)

        self.initial_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo_root, text=True).strip()

        # 2. Set up isolated external control plane
        self.cp_dir = self.base_dir / "external_control_plane"
        self.cp_dir.mkdir(parents=True)

        # 3. Instantiate Runner & Auditor configurations
        self.logger = SafeLogger()
        self.runner_config = {
            "control_plane_dir": str(self.cp_dir),
            "max_retries": 3,
            "disable_git_push": True,  # Sandbox mode (no remote push)
        }
        self.auditor_config = {
            "control_plane_dir": str(self.cp_dir),
            "max_retries": 3,
            "skip_remote_verification": True,
            "skip_ci_for_tests": False,
            "mock_model_audit": True,  # Uses strict model schema validator with approved mock result
            "mock_model_result": {
                "verdict": "APPROVED",
                "findings": ["Code changes strictly within requested scope", "Quality gate verified passing"],
                "requirement_coverage": ["Sandbox feature requirements fully satisfied"],
                "confidence": "HIGH",
                "next_action": "PROCEED",
            },
        }

        self.runner = OrchestrationRunner(self.repo_root, self.runner_config, self.logger)
        self.auditor = AutomatedAuditor(self.repo_root, self.auditor_config, self.logger)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_complete_sandbox_cycle_to_gate2_stop_condition(self):
        """
        Executes a complete end-to-end sandbox cycle:
        Task Setup -> Runner Execution -> Selective Delivery -> Commit ->
        Auditor Stage A (Deterministic) -> Auditor Stage B (AI Review) ->
        Post-Approval Stop Condition (HUMAN_REQUIRED at Gate 2).
        """
        # STEP 1: Publish a legitimate sandbox task
        task_id = "TASK-SANDBOX-FEATURE-01"
        task_content = f"""# Task: {task_id} — Add Sandbox Documentation

## Metadata
- **Task ID**: `{task_id}`
- **Task Type**: `FEATURE`
- **Maintenance Mode**: `false`

## 1. Context & Objective
Add a documentation note in docs/notes/sandbox.md for verification.

## 2. Scope & Allowed Paths
allowed_paths:
  - docs/notes/sandbox.md
allowed_path_prefixes:
  - docs/notes/
"""
        task_file = self.runner.current_task_file
        task_file.write_text(task_content, encoding="utf-8")
        task_hash = self.runner.compute_file_hash(task_file)

        initial_state = {
            "state": "READY",
            "state_version": 1,
            "task_id": task_id,
            "execution_id": "exec-sandbox-001",
            "expected_git_head": self.initial_head,
            "content_hash": task_hash,
            "retry_count": 0,
            "max_retries": 3,
        }
        self.runner.state_file.write_text(json.dumps(initial_state, indent=2), encoding="utf-8")

        # STEP 2: Runner Execution
        def sandbox_executor(prompt):
            # Executor creates the target file in working tree
            notes_dir = self.repo_root / "docs" / "notes"
            notes_dir.mkdir(parents=True, exist_ok=True)
            (notes_dir / "sandbox.md").write_text("# Sandbox Documentation\nAutonomous verified test.\n", encoding="utf-8")
            return (True, "Created docs/notes/sandbox.md successfully")

        with patch.object(self.runner, "execute_agy", side_effect=sandbox_executor), \
             patch.object(self.runner, "run_quality_gate", return_value=(True, "Quality gates all passed")):

            runner_ok = self.runner.execute_task_cycle(dry_run=False)
            self.assertTrue(runner_ok, "Runner execution cycle should succeed")

        # Verify post-runner state
        runner_state = self.runner.load_state()
        self.assertEqual(runner_state["state"], "AWAITING_AUDIT")
        resulting_commit = runner_state["resulting_git_head"]
        self.assertNotEqual(resulting_commit, self.initial_head)
        self.assertTrue(self.runner.handoff_file.exists())
        self.assertTrue(self.runner.is_git_clean(), "Working tree must be clean after selective delivery")

        # Verify commit message format
        commit_log = subprocess.check_output(["git", "log", "-1", "--format=%B"], cwd=self.repo_root, text=True)
        self.assertIn(f"feat(task): {task_id}", commit_log)

        # STEP 3: Auditor Execution (Stage A + Stage B)
        # Mock GitHub Actions CI returning completed + success for resulting_commit
        ci_run_response = json.dumps([{
            "databaseId": 9991234,
            "status": "completed",
            "conclusion": "success",
            "name": "repository-quality",
        }])

        orig_run = subprocess.run

        def mock_run(cmd, *args, **kwargs):
            if cmd and (cmd[0] == "/usr/local/bin/gh" or "gh" in str(cmd[0])):
                return subprocess.CompletedProcess(cmd, 0, stdout=ci_run_response, stderr="")
            return orig_run(cmd, *args, **kwargs)

        with patch("shutil.which", return_value="/usr/local/bin/gh"), \
             patch("subprocess.run", side_effect=mock_run):

            audit_ok = self.auditor.execute_audit_cycle(standalone_promote=False)
            self.assertTrue(audit_ok, "Auditor cycle should complete successfully")

        # STEP 4: Verify Terminal State & Gate 2 Stop Condition
        final_state = self.auditor.load_state()
        # MUST halt at HUMAN_REQUIRED because Gate 2 is blocked on the learner baseline!
        self.assertEqual(final_state["state"], "HUMAN_REQUIRED")
        self.assertIn("GATE 2: BLOCKED ON LEARNER BASELINE", final_state["last_error"])

        # Verify AUDIT_REPORT.md contents
        self.assertTrue(self.auditor.audit_report_file.exists())
        audit_report = self.auditor.audit_report_file.read_text(encoding="utf-8")
        self.assertIn("Verdict**: `APPROVED`", audit_report)
        self.assertIn("Auditor Model**: `mock-auditor`", audit_report)
        self.assertIn("Stage A: Deterministic Mandatory Gates", audit_report)
        self.assertIn("Stage B: Independent Model Review", audit_report)
        self.assertIn("Grounded Next Step: HUMAN_REQUIRED", audit_report)

        # Verify HUMAN_ACTION_REQUIRED.md
        self.assertTrue(self.auditor.human_action_file.exists())
        action_text = self.auditor.human_action_file.read_text(encoding="utf-8")
        self.assertIn("Administer Learner Baseline Diagnostic (TASK-030)", action_text)
        self.assertIn("BASELINE_FORM.md", action_text)


if __name__ == "__main__":
    unittest.main()
