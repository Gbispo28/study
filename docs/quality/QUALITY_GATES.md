# Quality Gates & Verification Philosophy

> **Core Tenet**: *No verification = not done.*

---

## 1. Robust & Deterministic Verification Philosophy

We reject fragile, flaky, or ornamental tests. In this project, high-quality automated testing means:

1. **Deterministic Execution**:
   - Tests produce identical results regardless of execution order, machine performance, or ambient timezone.
   - **Zero Flaky Sleep Calls**: Never use `time.sleep()` to await asynchronous events; use deterministic event signals or deterministic polling.
2. **Behavior-Oriented Assertions**:
   - Test contracts and observable system behavior, not private internal state or transient variable names.
   - Avoid tests that break merely because an internal method was renamed or reorganized.
3. **Controlled & Seeded Fixtures**:
   - Randomness must be seeded. Clocks and timers must be injectable or mocked with explicit timestamps.
4. **Meaningful Error Diagnostics**:
   - Assertions must output informative diffs explaining what was expected vs what was received.
5. **Mandatory Regression Tests**:
   - Every bug fix must include a test that reproduces the failure prior to the patch and confirms resolution after the patch.
6. **Coverage as Diagnostic, Not Goal**:
   - We do not chase arbitrary 100% coverage numbers with trivial, assertion-free tests.

---

## 2. Verification Gate Levels

```
Level 1: Structural & Secret Integrity (Local script + CI)
   ↓
Level 2: Unit & Domain Determinism (Fast in-memory tests)
   ↓
Level 3: Boundary & Integration Verifications (Adapters & file IO)
   ↓
Level 4: Adversarial Audit & Git Delivery (Pre-commit gatekeeper)
```

### Level 1: Repository & Structural Integrity
- Executed by `scripts/validate_repo.py`.
- Verifies directory layout, presence of core documents, valid JSON configs, valid agent/skill/rule frontmatters, and absence of leaked secrets.

### Level 2: Domain Unit Tests (Phase 04 onwards)
- Fast, in-memory tests verifying business logic, FSRS calculation math, CEFR transitions, and daily routine state machines.

### Level 3: Integration Tests (Phase 04 onwards)
- Tests verifying Anki export formats, file system persistence, and audio adapter contracts with mocked external endpoints.

### Level 4: Adversarial Audit & Pre-Commit Gate
- Executed via `scripts/quality_gate.sh` and `git-guardian`.
- Full diff inspection, status validation, conventional commit check, and push confirmation.

---

## 3. Definition of Done (DoD) Checklist

Before any pull request or task branch is merged into `main`:

- [ ] 1. Requirement understood and referenced to an approved task or roadmap item.
- [ ] 2. Code written adhering to clean code invariants (SOLID, DRY, YAGNI).
- [ ] 3. Deterministic automated tests added/updated.
- [ ] 4. Test suite executed locally with real output verified (PASS).
- [ ] 5. Code formatting and linting pass with zero errors.
- [ ] 6. Static typing checks pass with zero errors (where applicable).
- [ ] 7. No secrets, credentials, or `.env` files tracked in git.
- [ ] 8. Independent adversarial review performed (no hidden regression or edge case failure).
- [ ] 9. Documentation and `docs/project/STATE.md` updated.
- [ ] 10. Atomic commit created with conventional commit message.
- [ ] 11. Push verified against remote tracking branch.
