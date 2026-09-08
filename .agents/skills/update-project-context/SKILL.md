---
name: update-project-context
description: Use this skill at the end of every significant task or session to update the living project state, roadmap, and backlog without accumulating conversational bloat.
---

# Update Project Context Skill

## Purpose
Prevents "context rot" by maintaining a concise, accurate snapshot of project state, ensuring that subsequent agents or human contributors can orient themselves in seconds.

## Workflow

### 1. Review Verified Deliverables
- Check what was actually completed, tested, and pushed during the current turn or session.

### 2. Update `docs/project/STATE.md`
Update all relevant fields in [docs/project/STATE.md](../../../docs/project/STATE.md):
- **Current Phase**: Increment or refine phase description.
- **Current Objective**: State the active priority clearly.
- **Implemented Capabilities**: List only verified, functioning capabilities.
- **Important Decisions**: Reference new ADRs or confirmed design choices.
- **Active Constraints**: Note hardware, environment, or policy limits.
- **Blockers**: Document any technical or clarification impediments.
- **Next Milestone**: Declare the immediate next goal.
- **Last Verified Commit**: Record the commit SHA and message.

### 3. Synchronize Roadmap & Backlog
- In `docs/project/ROADMAP.md`: Mark completed phases or sub-phases.
- In `docs/project/BACKLOG.md`: Move completed items from `To Do` to `Done`.

### 4. Condensation Rules
- Never copy chat logs or full terminal transcripts into documentation.
- Focus strictly on state, decisions, constraints, and actionable next steps.
