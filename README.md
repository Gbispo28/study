# English Learning OS

> **Current Status**: `Foundation Complete (Gate 1 Passed) | Next: Phase 02 (Product Discovery)`<br>
> An agent-first, scientifically grounded personal operating system for English mastery.

---

## 1. Overview

**English Learning OS** is a platform engineered to help a Portuguese-speaking professional (software and data engineering background) acquire English proficiency starting from near-zero.

Rather than being a static course or a random collection of flashcards, the system is designed as an **adaptive learning operating system** built around:
- **60 minutes per day** of focused, deliberate practice.
- **Second Language Acquisition (SLA) & Cognitive Science**: Active recall, spaced repetition (FSRS), comprehensible input ($i+1$), retrieval practice, and error feedback.
- **Agentic Multi-Model Engineering**: Leveraging Google Antigravity 2.0, Gemini, Claude Code Pro, and local tooling to design, execute, and refine the learning workflow.
- **Multi-Device Synergy**: MacBook Air M4 (deep study, writing, coding) + Galaxy S24 Ultra (mobile retrieval, AnkiDroid, quick listening).

---

## 2. Current Status: Foundation Complete (Gate 1 Passed)

This repository has completed its **Foundational Engineering Phase (Gate 1 Closed)**.
- **No application framework has been chosen** (frontend, backend, and database decisions are deliberately deferred to formal Architecture Decision Records in Phase 04).
- **No speculative code exists**: All files in this initial phase establish governance, quality gates, custom agents, skills, workspace rules, and living documentation.

---

## 3. Repository Architecture

```text
.
├── AGENTS.md                  # Canonical engineering and collaboration contract
├── CLAUDE.md                  # Workflow instructions for Claude Code Pro
├── README.md                  # Project overview and orientation
├── .editorconfig              # Consistent file formatting rules
├── .gitattributes             # Git line-ending and diff configurations
├── .gitignore                 # Strict ignore rules for artifacts, caches, secrets
│
├── .agents/                   # Antigravity 2.0 Agentic Foundation
│   ├── README.md              # Overview of agentic architecture
│   ├── rules/                 # Always-on and triggerable workspace rules
│   ├── agents/                # Custom agents (Orchestrator + Specialists)
│   ├── skills/                # Standardized runbooks and multi-step skills
│   ├── hooks.json             # Lifecycle hook configurations
│   └── mcp_config.json        # MCP server integration registry
│
├── docs/                      # Living Project Documentation
│   ├── product/               # Vision, user persona, confirmed requirements
│   ├── project/               # Living state (STATE.md), roadmap, backlog
│   ├── architecture/          # System design guidelines and boundary rules
│   ├── decisions/             # Architecture Decision Records (ADR index)
│   ├── research/              # Learning science & cognitive research repository
│   ├── quality/               # Quality gates and Definition of Done
│   └── handoffs/              # Inter-session handoff logs (LATEST.md)
│
├── scripts/                   # Quality & Validation Scripts
│   ├── validate_repo.py       # Zero-dependency repo integrity validator
│   └── quality_gate.sh        # Executable gatekeeper script
│
└── .github/                   # CI/CD and GitHub Governance
    ├── workflows/
    │   └── repository-quality.yml # Automated CI quality check
    └── pull_request_template.md   # Standardized PR verification checklist
```

---

## 4. How Agents Begin a Session

When an AI agent or developer begins a new session in this workspace:

1. Read **[AGENTS.md](./AGENTS.md)** to assimilate engineering invariants.
2. Read **[docs/project/STATE.md](./docs/project/STATE.md)** to understand the current phase, active blockers, and immediate milestone.
3. Check **[docs/decisions/README.md](./docs/decisions/README.md)** for existing ADRs before proposing architectural changes.
4. Execute the verification suite before proposing commits:
   ```bash
   bash scripts/quality_gate.sh
   ```
5. Update `docs/project/STATE.md` upon completing verified work and produce a handoff.

---

## 5. Running the Quality Gate

The repository includes a zero-dependency validation suite checking structural integrity, frontmatter schema, JSON validity, and secret isolation:

```bash
# Run via python directly
python3 scripts/validate_repo.py

# Or run via the quality gate shell runner
bash scripts/quality_gate.sh
```

---

## 6. Next Steps

- **Milestone 1 (Complete — Gate 1 Passed)**: Bootstrap foundational engineering, agentic architecture, rules, skills, and living documentation.
- **Milestone 2 (Phase 02 — Ready / Next)**: Product Discovery & Learning Science Specification (analyzing 60-minute daily routine, CEFR baseline assessment, and memory optimization).
- **Milestone 3 (Phase 03 — Planned)**: Daily Journey & Card Architecture.
- **Milestone 4 (Phase 04 — Planned)**: Architecture Decision Records (evaluating technology stack and integration boundaries).
- **Milestone 5 (Phase 05 — Planned)**: Core MVP Implementation.
