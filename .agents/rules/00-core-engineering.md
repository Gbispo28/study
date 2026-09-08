---
trigger: always_on
description: Mandatory core engineering standards, clean code invariants, and root-cause problem-solving principles.
---

# Core Engineering Rules

> Reference: See [AGENTS.md](../../AGENTS.md) for full context.

## 1. Inspect Before Modifying
- Always examine the target file, its tests, and its callers before applying any change.
- Understand the contracts, data structures, and invariants already established.

## 2. Fix Root Cause, Never Mask Symptoms
- Never wrap a failing operation in an empty or swallow-all `try/catch`.
- Never silence linter errors with disable comments without documented justification.
- Do not apply quick hacks or monkey-patches. Find and resolve the source of the defect.

## 3. Simplicity & YAGNI
- Build only what is needed for the current verified requirement.
- Do not introduce speculative abstractions, generic wrappers, or unused parameters.
- Keep functions small, single-purpose, and clearly named.

## 4. Anti-Patterns Strictly Prohibited
- **Dead Code**: Never leave commented-out code or unreferenced modules.
- **Untracked TODOs**: Never insert `TODO` or `FIXME` comments without an associated issue or roadmap entry.
- **Unverified Claims**: Never claim a test or check passed without executing the command and reviewing output.
- **Silent Failures**: Log or bubble errors with actionable diagnostics.
- **Unjustified Dependencies**: Never introduce a package when standard libraries or straightforward logic suffice.
