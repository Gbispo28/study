---
name: adversarial-review
description: Use this skill to perform rigorous, adversarial code and architectural audits, assuming latent defects exist and actively searching for failure modes.
---

# Adversarial Review Skill

## Purpose
Establishes a rigorous review mindset: *"Assume a subtle bug, security vulnerability, or requirement discrepancy exists, and actively search for evidence."*

## Workflow

### 1. Requirements vs Implementation Audit
- Compare the code changes against the user request and [AGENTS.md](../../../AGENTS.md).
- Identify any gaps, unhandled cases, or features implemented that were never requested (scope creep).

### 2. Failure Mode Investigation
Scrutinize the implementation for:
- **Boundary Conditions**: Zero, null, empty collections, very large inputs, special characters.
- **Race Conditions & Concurrency**: Unsynchronized state updates or resource contention.
- **Error Recovery**: How does the system behave when a file is missing, network drops, or JSON is malformed?
- **Flaky Tests**: Tests with timing sensitivities, ambient environment dependencies, or order dependencies.

### 3. Maintainability & Code Smells
- Check for magic numbers, dead code, copy-pasted blocks, or overly complex nested logic.
- Verify that comments explain *why*, not merely restate *what* the code does.

### 4. Produce Structured Audit Report
- Categorize findings by severity: `Blocker`, `Major`, `Minor`, or `Nit`.
- Provide exact file paths, line ranges, and recommended resolutions.
