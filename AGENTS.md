# AGENTS.md — Canonical Engineering & Collaboration Contract

> **Scope**: This document is the single source of truth (SSOT) and canonical vendor-agnostic contract for all AI agents, models (Gemini, Claude, GPT, etc.), and human engineers contributing to this repository.

---

## 1. Project Mission

We are building the **English Learning OS**: a highly personalized, scientifically grounded, agentic operating system for mastering English as a second language. 

The primary user is a Brazilian software/data professional starting from near-zero English proficiency, dedicating 60 minutes of focused study per day, with access to Google AI Pro, Claude Code Pro, a MacBook Air M4, Galaxy S24 Ultra, and Anki/AnkiDroid.

---

## 2. Fundamental Engineering Principles

### 2.1 Read Before Write
- **Never modify without inspecting**: Before modifying or creating code, agents must inspect the current workspace, active rules, existing tests, and relevant documentation.
- **Root Cause First**: Never apply superficial workarounds or mask errors with empty `try/catch` or suppressive flags. Understand and solve the underlying problem.

### 2.2 Plan Before Execution
- Substantial or architectural changes require an explicit plan before writing code: Understand → Inspect → Impact Analysis → Plan → Risks → Verification Strategy.
- Do not create premature abstractions or speculatively build features ahead of verified user requirements (strictly follow YAGNI).

### 2.3 Architecture & Stack Status
- **Stack is Not Arbitrarily Decided**: The frontend framework, backend language, database, and hosting architecture are currently deferred and will be determined through formal Architecture Decision Records (ADRs).
- **Zero Hallucinated Requirements**: Never invent features, endpoints, frameworks, or database schemas that have not been explicitly confirmed or formally approved in ADRs.

### 2.4 Code Quality & Design
- **Clean Code & Simplicity**: Favor readable, explicit, and intention-revealing code over clever or terse solutions.
- **SOLID & Separation of Concerns**: Maintain clear boundaries between domain logic, data persistence, and interface layers when application code is introduced.
- **DRY without Premature Abstraction**: Do not extract shared abstractions until duplication is proven and semantic alignment is certain.
- **Type Safety**: Use strict static typing whenever supported by the chosen language and tooling. Avoid untyped bypasses (e.g., blanket `any`).

### 2.5 Anti-Patterns Strictly Prohibited
- Catching exceptions without logging or handling them.
- Magic numbers and hardcoded configuration strings.
- Monolithic functions or oversized, multi-responsibility modules.
- Duplicate business logic scattered across presentation layers.
- Untracked `TODO` comments without clear issue/context linkages.
- False claims of verification (claiming a check passed without actually running it).

---

## 3. Dependency Policy

Before proposing or introducing any new dependency, answer:
1. Is this dependency strictly necessary, or can standard platform capabilities resolve it?
2. Is the library actively maintained and backed by a trustworthy community?
3. Does it introduce security vulnerabilities or restrictive licenses?
4. Does it create excessive bloat or vendor lock-in?
5. Is there a lighter, simpler, or native alternative?

---

## 4. Testing & Verification Philosophy: "No Verification = Not Done"

- Every functional implementation must be accompanied by automated, deterministic verification.
- **Deterministic**: Tests must not rely on arbitrary sleeps, real-time clock drifts, or unmanaged global state.
- **Behavior-Oriented**: Test expected behaviors and boundary contracts, not ephemeral internal implementation details.
- **Regressions**: Every bug fix must include a regression test reproducing the issue before the fix and verifying it after.
- Code coverage is a diagnostic signal, not a substitute for meaningful assertion quality.

---

## 5. Security & Privacy

- **Zero Secrets in Repository**: Never commit API keys, personal access tokens, private keys, or passwords. `.env` and sensitive files must remain ignored by git.
- **Principle of Least Privilege**: Run processes and agents with minimal necessary permissions. Default to sandbox execution.
- **Defensive Input Handling**: Always sanitize and validate inputs against injection attacks (shell injection, path traversal, SSRF, XSS).
- **No Sensitive Logging**: Never print PII, tokens, or authorization headers into execution logs or console outputs.

---

## 6. Git Hygiene & Delivery

- **Pre-Commit Verification**: Run `git status` and inspect the complete staged diff (`git diff --cached`) before committing.
- **Atomic, Focused Commits**: Commits must contain related changes only. Do not mix refactorings with new features or unrelated fixes.
- **Never `git add .` Blindly**: Add explicitly intended files.
- **Conventional Commits**: Use semantic prefixes (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:`, `ci:`).
- **History Preservation**: Never force-push (`git push --force`) to shared branches or rewrite history without explicit human instruction.
- **Verified Push**: After pushing, verify remote synchronization using `git status` and commit SHA confirmation.

---

## 7. Documentation & State Management

- Documentation must mirror real architectural decisions, not aspirational musings.
- Whenever architectural milestones, constraints, or new capabilities are verified, immediately update:
  `docs/project/STATE.md`
- Substantial architectural decisions must be recorded in `docs/decisions/` following the ADR format.

---

## 8. Definition of Done (DoD)

A task or feature is officially **DONE** if and only if all applicable steps below are completed:

1. [ ] Requirement understood and verified against current product specifications.
2. [ ] Implementation complete, minimal, and adhering to clean code standards.
3. [ ] Deterministic tests implemented or updated.
4. [ ] All test suites executed and passing (real execution evidence required).
5. [ ] Linting and formatting checks passing with zero warnings/errors.
6. [ ] Typecheck passing with zero errors (where applicable).
7. [ ] Build succeeds cleanly (where applicable).
8. [ ] Independent adversarial review performed (no hidden bugs or regressions).
9. [ ] Security check completed (zero exposed secrets, safe input handling).
10. [ ] Living documentation and `docs/project/STATE.md` updated.
11. [ ] Staged Git diff reviewed line-by-line.
12. [ ] Atomic commit created with conventional commit message.
13. [ ] Remote push executed and verified.
14. [ ] Comprehensive session handoff documented.

*If any step is not applicable, state explicitly: `N/A — <technical rationale>`.*

---

## 9. Session Handoff Obligation

Every agent execution session must end with a structured handoff artifact or message enabling another agent or human engineer to resume work immediately with zero context loss.
