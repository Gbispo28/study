---
name: implement-change
description: Use this skill during active code or configuration implementation to enforce incremental execution, contract preservation, and simultaneous test authoring.
---

# Implement Change Skill

## Purpose
Governs the writing of code, scripts, or configurations to ensure high quality, maintainability, and zero unverified side effects.

## Workflow

### 1. Re-verify the Plan
- Confirm the target file list and expected outcomes from the planning phase before modifying.

### 2. Implement Incrementally
- Make the smallest possible coherent changes.
- Avoid broad refactoring or reformatting of untouched code blocks.
- Preserve existing public API contracts unless breaking changes are explicitly planned.

### 3. Write Tests Alongside Implementation
- Do not postpone testing to a subsequent phase.
- Write unit tests covering both the happy path and critical boundary/error conditions concurrently with feature code.

### 4. Code Hygiene Invariants
- Enforce strict typing where supported.
- Provide descriptive variable and function names.
- Handle every error path with meaningful context; never swallow exceptions.
- Eliminate dead code, debug statements, and untracked TODOs immediately.

### 5. Local Pre-Verification
- Run the localized test suite or linter on modified files to verify correctness before moving to integration gates.
