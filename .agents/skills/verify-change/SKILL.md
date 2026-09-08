---
name: verify-change
description: Use this skill after making changes to execute real, independent verification steps, automated tests, and quality gates without simulating results.
---

# Verify Change Skill

## Purpose
Enforces the iron rule: **No verification = not done.** Governs the execution and reporting of real, reproducible quality checks.

## Workflow

### 1. Independent Execution
- Verification must be run independently of the authoring process.
- Run actual automated test suites and validation scripts. **Never simulate, hypothesize, or assume command results.**

### 2. Full Verification Suite
Execute applicable verification commands:
```bash
# 1. Structural & Foundation Validator
python3 scripts/validate_repo.py

# 2. Quality Gate Runner
bash scripts/quality_gate.sh
```

### 3. Verify Error & Edge Handling
- Confirm that boundary conditions, unexpected inputs, and error states are exercised.
- Ensure that failures yield clear diagnostic messages rather than silent exits or cryptic tracebacks.

### 4. Record Real Evidence
- Capture command exit codes, execution durations, and standard outputs.
- Document any failing tests immediately; do not hide or bypass failures to achieve an artificial green status.
