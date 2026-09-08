#!/usr/bin/env python3
"""
Repository Quality & Integrity Validator for English Learning OS.
Uses only the Python standard library.
"""

import sys
import os
import json
import re
from pathlib import Path

# ANSI colors for clear terminal reporting
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

REPO_ROOT = Path(__file__).resolve().parent.parent

MANDATORY_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
    ".agents/README.md",
    ".agents/hooks.json",
    ".agents/mcp_config.json",
    "docs/product/VISION.md",
    "docs/product/REQUIREMENTS.md",
    "docs/project/STATE.md",
    "docs/project/ROADMAP.md",
    "docs/project/BACKLOG.md",
    "docs/architecture/README.md",
    "docs/decisions/README.md",
    "docs/decisions/0000-defer-application-stack-selection.md",
    "docs/research/README.md",
    "docs/quality/QUALITY_GATES.md",
    "docs/handoffs/LATEST.md",
    "scripts/validate_repo.py",
    "scripts/quality_gate.sh",
    ".github/workflows/repository-quality.yml",
    ".github/pull_request_template.md",
]

MANDATORY_RULES = [
    "00-core-engineering.md",
    "10-testing-quality.md",
    "20-git-delivery.md",
    "30-security.md",
    "40-documentation-context.md",
    "50-learning-product.md",
]

MANDATORY_AGENTS = [
    "orchestrator",
    "product-architect",
    "learning-science-researcher",
    "anki-srs-specialist",
    "test-engineer",
    "code-auditor",
    "security-reviewer",
    "git-guardian",
    "context-curator",
]

MANDATORY_SKILLS = [
    "plan-change",
    "research-with-evidence",
    "implement-change",
    "verify-change",
    "adversarial-review",
    "architecture-decision",
    "update-project-context",
    "git-delivery",
]

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]{36}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{22,82}"),
    re.compile(r"-----BEGIN (RSA|EC|OPENSSH|DSA|PGP) PRIVATE KEY-----"),
    re.compile(r"AIza[0-9A-Za-z-_]{35}"),
    re.compile(r"sk-[A-Za-z0-9]{20,48}"),
    re.compile(r"bearer\s+[A-Za-z0-9\-\._~\+\/]+=*", re.IGNORECASE),
]


def extract_frontmatter(content: str) -> dict:
    """Extract key-value pairs from simple YAML frontmatter."""
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    frontmatter_text = parts[1]
    data = {}
    current_key = None
    for line in frontmatter_text.splitlines():
        line_str = line.strip()
        if not line_str or line_str.startswith("#"):
            continue
        if ":" in line_str and not line_str.startswith("-"):
            k, v = line_str.split(":", 1)
            current_key = k.strip()
            val = v.strip().strip("\"'")
            if val.lower() == "true":
                data[current_key] = True
            elif val.lower() == "false":
                data[current_key] = False
            elif val == "":
                data[current_key] = []
            else:
                data[current_key] = val
        elif line_str.startswith("-") and current_key:
            item = line_str.lstrip("-").strip().strip("\"'")
            if isinstance(data.get(current_key), list):
                data[current_key].append(item)
            else:
                data[current_key] = [item]
    return data


def run_checks():
    errors = []
    warnings = []
    checks_passed = 0

    print(f"{CYAN}==> Starting English Learning OS Repository Validation{RESET}")

    # 1. Check Mandatory Files
    for rel_path in MANDATORY_FILES:
        target = REPO_ROOT / rel_path
        if not target.exists():
            errors.append(f"Missing mandatory file: {rel_path}")
        elif target.is_file() and target.stat().st_size == 0:
            errors.append(f"Mandatory file is empty (0 bytes): {rel_path}")
        else:
            checks_passed += 1

    # 2. Check JSON Files
    for json_file in [".agents/hooks.json", ".agents/mcp_config.json"]:
        p = REPO_ROOT / json_file
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    json.load(f)
                checks_passed += 1
            except Exception as e:
                errors.append(f"Invalid JSON syntax in {json_file}: {e}")

    # 3. Check Workspace Rules & Frontmatter
    rules_dir = REPO_ROOT / ".agents" / "rules"
    for rule_name in MANDATORY_RULES:
        rule_file = rules_dir / rule_name
        if not rule_file.exists():
            errors.append(f"Missing mandatory workspace rule: .agents/rules/{rule_name}")
            continue
        content = rule_file.read_text(encoding="utf-8")
        fm = extract_frontmatter(content)
        if not fm.get("trigger"):
            errors.append(f"Rule .agents/rules/{rule_name} missing 'trigger' frontmatter")
        if not fm.get("description"):
            errors.append(f"Rule .agents/rules/{rule_name} missing 'description' frontmatter")
        checks_passed += 1

    # 4. Check Custom Agents
    agents_dir = REPO_ROOT / ".agents" / "agents"
    for agent_name in MANDATORY_AGENTS:
        agent_file = agents_dir / agent_name / "agent.md"
        if not agent_file.exists():
            errors.append(f"Missing mandatory custom agent: .agents/agents/{agent_name}/agent.md")
            continue
        content = agent_file.read_text(encoding="utf-8")
        fm = extract_frontmatter(content)
        if not fm.get("name"):
            errors.append(f"Agent {agent_name} missing 'name' in frontmatter")
        if not fm.get("description"):
            errors.append(f"Agent {agent_name} missing 'description' in frontmatter")
        if not fm.get("model"):
            errors.append(f"Agent {agent_name} missing 'model' in frontmatter")
        if "mainAgent" not in fm:
            errors.append(f"Agent {agent_name} missing explicit 'mainAgent' in frontmatter")
        if "subagent" not in fm:
            errors.append(f"Agent {agent_name} missing explicit 'subagent' in frontmatter")

        # Specific hierarchy validations
        if agent_name == "orchestrator":
            if fm.get("mainAgent") is not True or fm.get("subagent") is not False:
                errors.append("Orchestrator must have mainAgent: true and subagent: false")
        else:
            if fm.get("mainAgent") is not False or fm.get("subagent") is not True:
                errors.append(f"Specialist agent {agent_name} must have mainAgent: false and subagent: true")
            if fm.get("commandExecutionPolicy") != "sandbox":
                warnings.append(f"Agent {agent_name} does not have commandExecutionPolicy: sandbox")

        # Read-only tool restriction check for auditors
        if agent_name in ["code-auditor", "security-reviewer"]:
            tools = fm.get("tools", [])
            if not tools:
                errors.append(f"Auditor {agent_name} must explicitly restrict tools")
            forbidden = {"replace_file_content", "multi_replace_file_content", "write_to_file", "run_command"}
            active_forbidden = set(tools).intersection(forbidden)
            if active_forbidden:
                errors.append(f"Auditor {agent_name} contains mutating tools: {active_forbidden}")

        checks_passed += 1

    # 5. Check Skills
    skills_dir = REPO_ROOT / ".agents" / "skills"
    for skill_name in MANDATORY_SKILLS:
        skill_file = skills_dir / skill_name / "SKILL.md"
        if not skill_file.exists():
            errors.append(f"Missing mandatory skill: .agents/skills/{skill_name}/SKILL.md")
            continue
        content = skill_file.read_text(encoding="utf-8")
        fm = extract_frontmatter(content)
        if not fm.get("name"):
            errors.append(f"Skill {skill_name} missing 'name' in frontmatter")
        if not fm.get("description"):
            errors.append(f"Skill {skill_name} missing 'description' in frontmatter")
        checks_passed += 1

    # 6. Secret Detection & Tracked File Scrutiny
    for root, dirs, files in os.walk(REPO_ROOT):
        # Ignore .git directory
        if ".git" in dirs:
            dirs.remove(".git")
        for file in files:
            file_path = Path(root) / file
            # Check for forbidden filenames
            if file == ".env" or (file.startswith(".env.") and file != ".env.example"):
                errors.append(f"Forbidden environment file detected: {file_path}")
            # Scan text files for secret patterns
            if file.endswith((".md", ".json", ".yml", ".yaml", ".py", ".sh", ".txt")):
                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    for pattern in SECRET_PATTERNS:
                        if pattern.search(content):
                            errors.append(f"Potential exposed secret matching pattern in {file_path}")
                except Exception:
                    pass

    # 7. Check Internal Markdown Links
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    for md_file in REPO_ROOT.glob("**/*.md"):
        if ".git" in md_file.parts:
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
            for label, target in link_pattern.findall(text):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                file_target = target.split("#")[0]
                if not file_target:
                    continue
                resolved = (md_file.parent / file_target).resolve()
                if not resolved.exists():
                    errors.append(f"Broken markdown link in {md_file.relative_to(REPO_ROOT)}: '{target}' does not exist")
                else:
                    checks_passed += 1
        except Exception as e:
            warnings.append(f"Could not check links in {md_file}: {e}")

    # 8. Print Results
    print(f"{CYAN}==> Ran {checks_passed} validation assertions.{RESET}")

    if warnings:
        for w in warnings:
            print(f"{YELLOW}[WARNING]{RESET} {w}")

    if errors:
        print(f"\n{RED}Validation FAILED with {len(errors)} error(s):{RESET}")
        for err in errors:
            print(f"  {RED}✖{RESET} {err}")
        return 1

    print(f"\n{GREEN}✔ ALL QUALITY GATES PASSED! Repository foundation is intact and healthy.{RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(run_checks())
