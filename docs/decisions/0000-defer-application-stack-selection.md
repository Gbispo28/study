# ADR-0000: Defer Application Stack Selection

- **Status**: Accepted
- **Date**: 2026-09-08
- **Author(s)**: Orchestrator & Product Architect

## 1. Context & Problem Statement
During the initial repository bootstrap phase, there is a risk of prematurely selecting application frameworks (React, Vue, FastAPI, NestJS, etc.), database systems (PostgreSQL, SQLite, Mongo), or cloud deployment patterns before the domain model, pedagogical requirements, and daily user journey are formally specified.

## 2. Options Considered
- **Option 1**: Arbitrarily select a popular stack (e.g., Next.js + SQLite or Python FastAPI) during bootstrap.
  - *Pros*: Quick visual prototype.
  - *Cons*: High risk of premature optimization, framework lock-in, unneeded dependencies, and misalignment with actual learning science workflows.
- **Option 2 (Chosen)**: Deliberately defer all application framework and database decisions until Phase 02 (SLA Specification) and Phase 03 (Daily Routine Architecture) are completed.
  - *Pros*: Keeps the foundation pure, minimal, and agile. Allows decisions to be driven by empirical learning workflows rather than speculative tooling.
  - *Cons*: No runnable application UI during the bootstrap phase (acceptable per project charter).

## 3. Decision Outcome
Chosen Option: **Option 2**. Only engineering governance, multi-agent structure, workspace rules, skills, and quality gate infrastructure will be created in this phase.

## 4. Consequences
- **Positive**: Zero bloat, zero technical debt from unused dependencies, and complete clarity for AI agents on project boundaries.
- **Negative / Trade-offs**: Development of functional application features is paused until formal discovery and requirements are recorded.

## 5. Risks & Mitigation
- **Risk**: Momentum loss or ambiguity on what comes next.
- **Mitigation**: A comprehensive roadmap (`docs/project/ROADMAP.md`) and backlog (`docs/project/BACKLOG.md`) clearly outline the subsequent discovery milestones.

## 6. Revisit Criteria
This decision will be revisited at the start of Phase 04, after the pedagogical routines and card architecture are finalized.
