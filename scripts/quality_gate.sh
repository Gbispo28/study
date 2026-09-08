#!/usr/bin/env bash
# Quality Gate Runner for English Learning OS
# Exits with non-zero code if any check fails.

set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}====================================================${NC}"
echo -e "${CYAN}   English Learning OS — Quality Gate Runner       ${NC}"
echo -e "${CYAN}====================================================${NC}"

# Ensure we are in repo root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Check Python 3
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}[ERROR] python3 is not installed or not in PATH.${NC}"
    exit 1
fi

# 1. Run Repository Integrity Validator
echo -e "\n${CYAN}[1/2] Executing Repository Integrity Validator...${NC}"
python3 scripts/validate_repo.py

# 2. Check Git Working Tree Hygiene
echo -e "\n${CYAN}[2/2] Checking Git Hygiene & Working Tree State...${NC}"
if command -v git &>/dev/null && [ -d ".git" ]; then
    HYGIENE_FAILED=0

    # 2a. Check for unresolved merge conflicts
    CONFLICTS=$(git diff --name-only --diff-filter=U 2>/dev/null || true)
    if [ -n "$CONFLICTS" ]; then
        echo -e "${RED}[ERROR] Unresolved merge conflicts detected in:${NC}"
        echo "$CONFLICTS" | sed 's/^/  ✖ /'
        HYGIENE_FAILED=1
    fi

    # 2b. Check for untracked non-ignored files
    UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null || true)
    if [ -n "$UNTRACKED" ]; then
        echo -e "${RED}[ERROR] Untracked non-ignored files detected in workspace:${NC}"
        echo "$UNTRACKED" | sed 's/^/  ✖ /'
        echo -e "${RED}Remedy: Stage valid files (git add) or add them to .gitignore.${NC}"
        HYGIENE_FAILED=1
    fi

    # 2c. Check for tracked modifications that are NOT staged
    if ! git diff --quiet 2>/dev/null; then
        echo -e "${RED}[ERROR] Tracked files contain unstaged modifications:${NC}"
        git diff --name-only 2>/dev/null | sed 's/^/  ✖ /'
        echo -e "${RED}Remedy: Stage modifications (git add) or revert unneeded changes.${NC}"
        HYGIENE_FAILED=1
    fi

    # 2d. Check staged diff for whitespace errors
    if ! git diff --cached --check 2>/dev/null; then
        echo -e "${RED}[ERROR] Staged diff contains whitespace/formatting errors (see output above).${NC}"
        HYGIENE_FAILED=1
    fi

    if [ "$HYGIENE_FAILED" -ne 0 ]; then
        echo -e "\n${RED}====================================================${NC}"
        echo -e "${RED}   QUALITY GATE STATUS: FAILED (Git Hygiene)        ${NC}"
        echo -e "${RED}====================================================${NC}"
        exit 1
    fi

    echo -e "${GREEN}✔ Working tree hygiene verified (no untracked files, no unstaged edits, clean staged diff).${NC}"
else
    echo -e "${CYAN}[SKIP] Not inside a git repository or git command missing.${NC}"
fi

echo -e "\n${GREEN}====================================================${NC}"
echo -e "${GREEN}   QUALITY GATE STATUS: PASSED                     ${NC}"
echo -e "${GREEN}====================================================${NC}"
exit 0
