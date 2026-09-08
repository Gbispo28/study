---
name: git-delivery
description: Use this skill prior to any git commit or push to enforce quality gate execution, diff inspection, secret prevention, and push verification.
---

# Git Delivery Skill

## Purpose
Enforces strict gatekeeping before any code or configuration change is committed or pushed to the repository.

## Pre-Commit Checklist & Steps

### 1. Pre-Commit Hygiene
```bash
# 1. Check workspace status for unexpected files
git status

# 2. Run repository quality checks
python3 scripts/validate_repo.py
bash scripts/quality_gate.sh
```

### 2. Selective Staging & Diff Inspection
- Stage only intentional files:
  ```bash
  git add <file1> <file2> ...
  ```
- Review the staged diff line-by-line:
  ```bash
  git diff --cached
  ```
- **Verify zero secrets**: Check that no tokens, credentials, private keys, or `.env` files are included.

### 3. Conventional Commit Formatting
- Write a clear, conventional commit message:
  ```bash
  git commit -m "<type>(<scope>): <clear descriptive summary>"
  ```

### 4. Remote Push & Verification
- Execute push:
  ```bash
  git push origin <branch>
  ```
- Verify push success and capture commit SHA:
  ```bash
  git rev-parse HEAD
  git status
  ```
- Confirm that the working tree is clean and synchronized with origin.
