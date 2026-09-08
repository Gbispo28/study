# CLAUDE.md — Claude Code Pair Programming Guide

> This repository is managed under an agent-first engineering governance model.

## Core Operational Workflow

When initiating or continuing work in this repository with Claude Code Pro:

1. **Read Canonical Contract**: Always review [AGENTS.md](./AGENTS.md) first. It contains mandatory engineering, testing, security, and Git rules.
2. **Inspect Current Project State**: Read [docs/project/STATE.md](./docs/project/STATE.md) before taking any action to understand current phase, blockers, active constraints, and next milestones.
3. **Check Architecture & ADRs**: Consult [docs/architecture/README.md](./docs/architecture/README.md) and [docs/decisions/README.md](./docs/decisions/README.md). Do not assume frameworks or database stacks until formal ADRs exist.
4. **Execute Quality Gates**: Before proposing commits or completing tasks, run the quality gate:
   ```bash
   bash scripts/quality_gate.sh
   ```
5. **Update State & Handoff**: After completing verified work, update `docs/project/STATE.md` and generate a concise handoff.
6. **No Verification = Not Done**: Never declare a task done without automated test execution and diff verification.
