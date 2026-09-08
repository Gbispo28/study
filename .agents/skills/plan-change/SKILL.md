---
name: plan-change
description: Use this skill before undertaking any non-trivial change or architectural task to structure analysis, assess impact, and define validation strategies.
---

# Plan Change Skill

## Purpose
Enforces a structured, disciplined analysis workflow before modifying code or configurations, ensuring changes are intentional, minimal, and fully testable.

## Workflow

### 1. Understand the Requirement
- Clarify the user intent and problem statement.
- Identify what is confirmed vs what is an assumption. If uncertain, flag open questions.

### 2. Inspect Existing System
- Locate relevant files, tests, and configurations.
- Map existing contracts, data structures, and invariants that must be preserved.

### 3. Impact Analysis
- Identify callers, dependents, and indirect downstream effects.
- Determine if public interfaces, configuration schemas, or user workflows are affected.

### 4. Step-by-Step Implementation Plan
- Break down the task into discrete, logical increments.
- Demarcate new files `[NEW]`, modified files `[MODIFY]`, or deleted files `[DELETE]`.

### 5. Risk Assessment & Mitigation
- Identify failure modes (e.g., race conditions, edge cases, breaking changes).
- Formulate concrete fallback or prevention steps.

### 6. Validation Strategy
- Define exact automated tests or commands needed to verify correctness.
- Establish measurable acceptance criteria following the Definition of Done.
