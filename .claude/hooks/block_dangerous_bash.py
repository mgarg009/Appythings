#!/usr/bin/env python3
"""Guardrail 1 (PreToolUse, Bash): stop destructive or risky shell commands.

Claude Code sends the tool call as JSON on stdin. We answer with a JSON
"deny" decision, which blocks the call and tells Claude why.
"""
import json
import re
import sys

RULES = [
    (r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)\b", "Recursive force delete (rm -rf) is not allowed."),
    (r"\bgit\s+push\b.*(--force\b|\s-f\b)", "Force push is not allowed. Open a PR instead."),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard throws away work. Ask the user first."),
    (r"(curl|wget)[^|]*\|\s*(ba|z)?sh\b", "Piping a download into a shell is not allowed."),
    (r"\b(az|terraform)\b.*\b(delete|destroy)\b", "Deleting cloud resources needs a human."),
    (r"\bchmod\s+(-R\s+)?777\b", "chmod 777 opens files to everyone."),
]


def main() -> None:
    data = json.load(sys.stdin)
    command = data.get("tool_input", {}).get("command", "")

    for pattern, reason in RULES:
        if re.search(pattern, command):
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"AppyThings guardrail: {reason}",
                }
            }))
            return
    # No output and exit 0 means: carry on as normal.


if __name__ == "__main__":
    main()
