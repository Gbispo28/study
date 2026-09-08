---
trigger: always_on
description: Mandatory testing philosophy, deterministic verification requirements, and quality standards.
---

# Testing & Quality Rules

> Principle: **No verification = not done.**

## 1. Test Pyramid & Boundaries (When Application Code Exists)
- **Unit Tests**: Test core domain logic, algorithms, state mutations, and edge conditions in total isolation.
- **Integration Tests**: Verify interactions across module boundaries, persistence adapters, and external APIs.
- **End-to-End (E2E) Tests**: Reserve for critical user flows and journeys.
- **Regression Tests**: Every resolved bug must have a reproducible test case added to prevent recurrence.

## 2. Determinism & Reliability
- Tests must be completely deterministic. Flaky tests are defects and must be eliminated immediately.
- Never use arbitrary `sleep()` or real-time timeouts to await asynchronous operations; use explicit event or state polling.
- Control fixtures and seed random generators where determinism is required.
- Do not depend on ambient timezone or locale settings unless explicitly testing internationalization.

## 3. Useful Assertions & Coverage
- Assert expected behaviors and contracts, not implementation trivia or private variables.
- Provide descriptive failure messages when assertion intent is non-obvious.
- Code coverage is a diagnostic indicator, not an ultimate metric. Never write vacuous assertions merely to artificially inflate coverage percentages.
