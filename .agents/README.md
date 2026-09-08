# Antigravity Agentic Foundation

This directory houses the Google Antigravity 2.0 configuration, rules, agents, skills, and integrations for the **English Learning OS**.

## Architecture Overview

```text
.agents/
├── rules/             # System and behavior guidelines (Always On & Triggers)
│   ├── 00-core-engineering.md
│   ├── 10-testing-quality.md
│   ├── 20-git-delivery.md
│   ├── 30-security.md
│   ├── 40-documentation-context.md
│   └── 50-learning-product.md
│
├── agents/            # Custom Agents & Subagents
│   ├── orchestrator/                 # Main Coordinator (mainAgent: true)
│   ├── product-architect/            # Architecture & ADRs (subagent: true)
│   ├── learning-science-researcher/  # SLA & Cognitive Science (subagent: true)
│   ├── anki-srs-specialist/          # FSRS & Card Engineering (subagent: true)
│   ├── test-engineer/                # Adversarial Quality & Tests (subagent: true)
│   ├── code-auditor/                 # Read-Only Code Reviewer (subagent: true)
│   ├── security-reviewer/            # Read-Only Security Inspector (subagent: true)
│   ├── git-guardian/                 # Pre-Commit Gatekeeper (subagent: true)
│   └── context-curator/              # State & Handoff Maintainer (subagent: true)
│
├── skills/            # Procedural runbooks and multi-step skills
│   ├── plan-change/
│   ├── research-with-evidence/
│   ├── implement-change/
│   ├── verify-change/
│   ├── adversarial-review/
│   ├── architecture-decision/
│   ├── update-project-context/
│   └── git-delivery/
│
├── hooks.json         # Lifecycle hooks (safely disabled pending stack selection)
└── mcp_config.json    # MCP server configurations
```

## Agent Hierarchy

- **Main Agent**: `orchestrator` (`mainAgent: true`, `subagent: false`, `model: pro`). This is the primary user-facing coordinator that interacts directly with the developer, plans workflows, delegates tasks, and synthesizes deliverables.
- **Subagents**: All specialist agents (`mainAgent: false`, `subagent: true`, `commandExecutionPolicy: sandbox`).
- **Read-Only Auditors**: `code-auditor` and `security-reviewer` are explicitly restricted to read-only tools (`view_file`, `grep_search`, `list_dir`, `read_url_content`, `search_web`), guaranteeing independent, uncompromised verification.

## MCP Configuration & Security Policy

Antigravity's `mcp_config.json` passes environment variables literally to server processes without shell-style dynamic variable interpolation (`${...}`). Storing secrets or fake interpolation strings in tracked repository configuration violates our core security rules.

- **GitHub MCP**: When enabling GitHub MCP, configure it locally via `~/.gemini/config/mcp_config.json` or through Antigravity's Settings UI using your authenticated credentials.
- **Deferred Integrations**: Database, browser, and third-party MCPs are deferred until Phase 04 architecture decisions require them, preventing tool sprawl.
