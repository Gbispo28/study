---
trigger: always_on
description: Security guidelines, secret prevention, least privilege, and defensive input handling.
---

# Security Rules

## 1. Zero Secrets in Version Control
- Never commit credentials, personal access tokens (PATs), API keys, passwords, certificates, or private keys.
- Configuration files containing secrets must be listed in `.gitignore`. Use `.env.example` with sanitized placeholders.
- If a secret is accidentally committed locally, rebase immediately before pushing to remote.

## 2. Principle of Least Privilege
- Restrict file system and network access to only what is strictly required for the specific task.
- Subagents and background tasks should run in sandboxed execution environments whenever possible.

## 3. Defensive Programming & Injection Defense
- **Shell Commands**: Always parameterize arguments; avoid unescaped string interpolation that could lead to command injection.
- **Path Traversal**: Validate and canonicalize file paths; ensure paths do not traverse outside authorized workspace roots.
- **Input Sanitization**: Validate all inputs at the boundary using schema validators or strong type checks before passing them to internal operations.
- **No Sensitive Logging**: Strip credentials, authorization tokens, and personal identifying data from logs and telemetry.
