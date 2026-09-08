---
trigger: always_on
description: Living documentation protocols, state maintenance, and ADR governance.
---

# Documentation & Context Rules

## 1. Documentation as Source of Truth
- Documentation must reflect the actual, verified state of the system, not hypothetical future features.
- Avoid duplicate documentation that can fall out of sync; centralize architectural decisions in ADRs.

## 2. Living Project State (`docs/project/STATE.md`)
- After any verified architectural change, dependency update, or milestone completion, update `docs/project/STATE.md`.
- Keep `STATE.md` concise, scannable, and up-to-date. Do not allow historical transcripts or raw logs to accumulate there.

## 3. Architecture Decision Records (ADRs)
- Significant decisions regarding system boundaries, technology stacks, persistence, or major libraries require an ADR in `docs/decisions/`.
- Every ADR must record: Context, Problem, Options Considered, Decision, Rationale, Consequences, Risks, and Revisit Criteria.
