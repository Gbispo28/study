# Task: {{TASK_ID}} — {{TASK_TITLE}}

## Metadata
- **Task ID**: `{{TASK_ID}}`
- **Parent Task ID**: `{{PARENT_TASK_ID}}`
- **Task Type**: `{{TASK_TYPE}}` <!-- FEATURE | REFACTOR | TEST | INFRASTRUCTURE -->
- **Maintenance Mode**: `false` <!-- Set true only for infrastructure tasks altering protected paths -->
- **Expected Starting HEAD**: `{{EXPECTED_GIT_HEAD}}`

## 1. Context & Objective
{{TASK_OBJECTIVE}}

## 2. Scope & Invariants
- Pedagogical Invariant: `GATE 2: BLOCKED ON LEARNER BASELINE` remains strictly preserved.
- Zero secrets permitted.
- Protected paths must NOT be modified unless `Maintenance Mode` is explicitly enabled.

## 3. Detailed Requirements
{{TASK_REQUIREMENTS}}

## 4. Verification Acceptance Criteria
- Quality gate passing: `bash scripts/quality_gate.sh` exits 0.
- Unit/deterministic tests passing.
- Clean diff adhering strictly to scope.
