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

# 2. Check Git Working Tree & Submodules
echo -e "\n${CYAN}[2/2] Checking Git Hygiene & Untracked Files...${NC}"
if command -v git &>/dev/null && [ -d ".git" ]; then
    UNTRACKED=$(git status --porcelain | grep '^??' || true)
    if [ -n "$UNTRACKED" ]; then
        echo -e "${CYAN}[NOTE] Untracked files present in workspace:${NC}"
        echo "$UNTRACKED"
    else
        echo -e "${GREEN}✔ Working tree is clean or fully staged.${NC}"
    fi
else
    echo -e "${CYAN}[SKIP] Not inside a git repository or git command missing.${NC}"
fi

echo -e "\n${GREEN}====================================================${NC}"
echo -e "${GREEN}   QUALITY GATE STATUS: PASSED                     ${NC}"
echo -e "${GREEN}====================================================${NC}"
exit 0
