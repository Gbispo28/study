---
trigger: always_on
description: Git hygiene, conventional commits, secret prevention, and safe delivery procedures.
---

# Git Delivery Rules

## 1. Pre-Commit Hygiene
- Always run `git status` prior to staging files to detect unexpected or extraneous files.
- Never use `git add .` or `git add -A` blindly. Explicitly add only files relevant to the current task.
- Review the staged diff line-by-line using `git diff --cached` before writing the commit message.
- Verify that no credentials, tokens, local paths, or scratch files are being committed.

## 2. Commit Standards
- Use Conventional Commits formatting: `<type>(<scope>): <short description>`
  - Permitted types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `perf`, `build`.
- Commit messages must clearly explain the intent and rationale of the change.
- Keep commits atomic and focused. Do not mix unrelated refactorings or file reformatting into feature commits.

## 3. Remote Operations & Safety
- Never run `git push --force` on shared or main branches.
- Never delete remote branches without explicit user authorization.
- Always confirm push completion by validating remote ref synchronization and noting the commit SHA.
