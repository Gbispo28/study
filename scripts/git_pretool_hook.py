#!/usr/bin/env python3
"""
Antigravity PreToolUse Hook: Prohibit Git Delivery Commands for Executor Sessions.

Enforces technical Git containment:
Blocks git mutating/delivery operations (add, commit, push, checkout, reset, etc.)
while allowing read-only inspection commands (status, diff, log, rev-parse).
"""

import sys
import json
import re

BLOCKED_GIT_SUBCOMMANDS = [
    "add",
    "commit",
    "push",
    "checkout",
    "switch",
    "reset",
    "restore",
    "rebase",
    "merge",
    "tag",
    "branch",
    "cherry-pick",
    "revert",
    "pull",
    "clean",
]

# Regex detecting blocked git subcommands e.g. "git commit", "git push", "/usr/bin/git add", etc.
BLOCKED_PATTERN = re.compile(
    r"(?:^|[;&|]\s*|\b)git\s+(" + "|".join(BLOCKED_GIT_SUBCOMMANDS) + r")\b",
    re.IGNORECASE,
)


def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"decision": "allow"}))
            return 0

        payload = json.loads(raw_input)
        tool_call = payload.get("toolCall", {})
        tool_name = tool_call.get("name", "")
        tool_args = tool_call.get("args", {})

        if tool_name == "run_command":
            cmd = tool_args.get("CommandLine", "")
            match = BLOCKED_PATTERN.search(cmd)
            if match:
                subcmd = match.group(1)
                response = {
                    "decision": "deny",
                    "reason": f"Git delivery command 'git {subcmd}' is strictly prohibited for executor sessions. Git operations are managed exclusively by the outer runner.",
                }
                print(json.dumps(response))
                return 0

        print(json.dumps({"decision": "allow"}))
        return 0
    except Exception as e:
        # In case of parsing issues, default to allow unless it's clearly a blocked command
        print(json.dumps({"decision": "allow"}))
        return 0


if __name__ == "__main__":
    sys.exit(main())
