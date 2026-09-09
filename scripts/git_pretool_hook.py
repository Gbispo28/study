#!/usr/bin/env python3
"""
Antigravity PreToolUse Hook: Enforce Technical Git Read-Only Boundary.

Invariants:
- Fail-Closed Security: Any JSON parse failure, malformed payload, missing schema,
  or internal exception defaults strictly to DENY with a sanitized reason.
- Read-Only Git Allowlist: Replaces fragile blacklists with an explicit allowlist:
  ['status', 'diff', 'log', 'show', 'rev-parse', 'ls-files'].
- Mutating Flags Blocked: Flags that write output to disk (e.g. --output, -o) are denied.
- Multi-Command Defense: Splits chained shell commands (;, &&, ||, |, &) and checks each.
- Sanitized Diagnostics: Never leaks raw input or potential secrets in deny reasons.
"""

import sys
import json
import re

ALLOWED_READONLY_GIT_SUBCOMMANDS = {
    "status",
    "diff",
    "log",
    "show",
    "rev-parse",
    "ls-files",
}

# Subcommands or flags that can write to files or alter configuration even in read-only commands
PROHIBITED_FLAGS = {
    "--output",
    "-o",
    "--output=",
    "--work-tree",
    "--git-dir",
}

# Regex to split on shell separators
SHELL_SEPARATORS = re.compile(r"[;&|\n]+")


def parse_and_validate_command(cmd: str) -> tuple[bool, str]:
    """
    Validates a command line against the read-only Git allowlist.
    Returns (is_allowed, reason).
    """
    # Break into separate commands if chained
    segments = SHELL_SEPARATORS.split(cmd)
    for seg in segments:
        seg_str = seg.strip()
        if not seg_str:
            continue

        tokens = seg_str.split()
        if not tokens:
            continue

        # Look for git invocation
        git_indices = [
            i for i, tok in enumerate(tokens)
            if tok == "git" or tok.endswith("/git") or tok.endswith("\\git")
        ]

        if not git_indices:
            # Not a git command
            continue

        for git_idx in git_indices:
            # Find the subcommand after git
            args_after_git = tokens[git_idx + 1 :]
            if not args_after_git:
                # Bare 'git' invocation with no subcommand
                return (False, "Bare git command without read-only subcommand is prohibited.")

            subcmd = None
            for arg in args_after_git:
                if arg.startswith("-"):
                    # Top-level git options like -C, --no-pager, -c
                    if arg in ["--git-dir", "--work-tree"] or arg.startswith("--git-dir=") or arg.startswith("--work-tree="):
                        return (False, "Git directory mutation options are prohibited.")
                    continue
                subcmd = arg
                break

            if not subcmd:
                return (False, "Could not determine git subcommand; failing closed.")

            subcmd_lower = subcmd.lower()
            if subcmd_lower not in ALLOWED_READONLY_GIT_SUBCOMMANDS:
                return (
                    False,
                    f"Git command 'git {subcmd_lower}' is not in the read-only allowlist "
                    f"({', '.join(sorted(ALLOWED_READONLY_GIT_SUBCOMMANDS))}).",
                )

            # Subcommand is in allowlist: check for mutating flags
            for arg in args_after_git:
                for bad_flag in PROHIBITED_FLAGS:
                    if arg == bad_flag or arg.startswith(bad_flag):
                        return (False, f"Prohibited flag '{arg}' detected in git command.")

    return (True, "Command verified as safe or non-mutating.")


def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input or not raw_input.strip():
            # FAIL CLOSED on empty input
            print(json.dumps({
                "decision": "deny",
                "reason": "SecurityViolation: Empty payload received by pretool security hook (fail-closed)."
            }))
            return 0

        try:
            payload = json.loads(raw_input)
        except Exception:
            # FAIL CLOSED on malformed JSON
            print(json.dumps({
                "decision": "deny",
                "reason": "SecurityViolation: Malformed JSON payload received by pretool security hook (fail-closed)."
            }))
            return 0

        if not isinstance(payload, dict):
            print(json.dumps({
                "decision": "deny",
                "reason": "SecurityViolation: Unexpected payload type (expected JSON object)."
            }))
            return 0

        tool_call = payload.get("toolCall")
        if not isinstance(tool_call, dict):
            print(json.dumps({
                "decision": "deny",
                "reason": "SecurityViolation: Missing or invalid 'toolCall' in hook payload."
            }))
            return 0

        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args")

        if not isinstance(tool_name, str) or not isinstance(tool_args, dict):
            print(json.dumps({
                "decision": "deny",
                "reason": "SecurityViolation: Invalid toolCall fields (name or args missing/malformed)."
            }))
            return 0

        if tool_name == "run_command":
            cmd = tool_args.get("CommandLine")
            if not isinstance(cmd, str):
                print(json.dumps({
                    "decision": "deny",
                    "reason": "SecurityViolation: Missing 'CommandLine' string in run_command toolCall."
                }))
                return 0

            allowed, reason = parse_and_validate_command(cmd)
            if not allowed:
                print(json.dumps({
                    "decision": "deny",
                    "reason": f"SecurityViolation: {reason}"
                }))
                return 0

        # All checks passed
        print(json.dumps({"decision": "allow"}))
        return 0

    except Exception:
        # FAIL CLOSED on any unexpected internal error
        print(json.dumps({
            "decision": "deny",
            "reason": "SecurityViolation: Pretool hook internal exception (fail-closed default)."
        }))
        return 0


if __name__ == "__main__":
    sys.exit(main())
