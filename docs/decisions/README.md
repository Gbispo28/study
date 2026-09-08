# Architecture Decision Records (ADRs)

This directory maintains the historical log of all architecturally significant decisions made for the **English Learning OS**.

## ADR Index

| ID | Title | Status | Date | Decision Summary |
| :--- | :--- | :--- | :--- | :--- |
| **ADR-0000** | [Defer Application Stack Selection](./0000-defer-application-stack-selection.md) | **Accepted** | 2026-09-08 | Keep application frameworks and persistence deferred during foundation bootstrap. |

---

## How to Propose a New ADR

1. Use the **[architecture-decision](../../.agents/skills/architecture-decision/SKILL.md)** skill.
2. Create a new file named `XXXX-short-title.md` with sequential numbering.
3. Use the standardized ADR template:
   - **Status**: `Proposed`, `Accepted`, `Deprecated`, or `Superseded by ADR-YYYY`.
   - **Context & Problem Statement**: What technical or product challenge demands a decision?
   - **Options Considered**: List alternatives evaluated with pros/cons.
   - **Decision Outcome**: What was chosen and why?
   - **Consequences**: Positive benefits and negative trade-offs accepted.
   - **Risks & Mitigation**: Anticipated failure modes and safeguards.
   - **Revisit Criteria**: Under what conditions this decision must be re-evaluated.
4. Update this index table in `docs/decisions/README.md`.
