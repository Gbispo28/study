---
name: architecture-decision
description: Use this skill when evaluating, formulating, and documenting architectural choices, technology selections, or system boundaries via Architecture Decision Records (ADRs).
---

# Architecture Decision Skill

## Purpose
Standardizes the process of evaluating technical alternatives and documenting decisions through Architecture Decision Records (ADRs), preserving institutional memory and architectural rationale.

## When to Create an ADR
- Selecting or changing programming languages, frameworks, or libraries.
- Choosing database or persistence strategies.
- Defining integration patterns (e.g., AnkiDroid sync, mobile bridge, AI model connectors).
- Significant changes to system boundaries, security models, or directory structure.

## ADR Lifecycle
1. **Proposed**: Draft under review; options and consequences are actively being evaluated.
2. **Accepted**: Approved by team/user; implementation may proceed.
3. **Deprecated**: Decision is no longer relevant due to scope or system evolution.
4. **Superseded**: Replaced by a newer ADR (must link to the superseding ADR).

## Standard ADR Format
Every ADR in `docs/decisions/` must follow this structure:
```markdown
# ADR-XXXX: [Short Title of Decision]

- **Status**: [Proposed | Accepted | Deprecated | Superseded by ADR-YYYY]
- **Date**: YYYY-MM-DD
- **Author(s)**: [Agent or Engineer Name]

## 1. Context & Problem Statement
What context led to this decision? What specific problem are we solving?

## 2. Options Considered
- Option 1: [Description, Pros, Cons]
- Option 2: [Description, Pros, Cons]

## 3. Decision Outcome
Chosen Option: [Option X] because [rationale].

## 4. Consequences
- **Positive**: What benefits or capabilities are unlocked?
- **Negative / Trade-offs**: What complexity or limitations do we accept?

## 5. Risks & Mitigation
What could go wrong with this choice, and how will we mitigate it?

## 6. Revisit Criteria
Under what specific conditions should this decision be re-evaluated?
```
