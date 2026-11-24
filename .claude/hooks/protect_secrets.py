#!/usr/bin/env python3
"""Guardrail 2 (PreToolUse, Read/Edit/Write): keep Claude away from secret files.

The deny rules in settings.json already cover the common cases. This hook
adds patterns that are awkward to express as rules, and also stops Claude
from WRITING a secret into any file.
"""
import json
import re
import sys
from pathlib import PurePath

SECRET_FILES = re.compile(
    r"(^|/)(\.env(\..*)?|id_rsa|id_ed25519|.*\.pem|.*\.pfx|.*\.key|secrets?\.(json|ya?ml)|local\.settings\.json)$",
    re.IGNORECASE,
)
ALLOWED = re.compile(r"\.env\.example$", re.IGNORECASE)

SECRET_CONTENT = [
    r"-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY",
    r"\bsk-[A-Za-z0-9_-]{20,}",          # OpenAI / Anthropic style keys
    r"\bAKIA[0-9A-Z]{16}\b",             # AWS access key id
    r"AccountKey=[A-Za-z0-9+/=]{40,}",   # Azure storage connection string
    r"\bgh[pousr]_[A-Za-z0-9]{30,}",     # GitHub tokens
]


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"AppyThings guardrail: {reason}",
        }
    }))


def main() -> None:
    data = json.load(sys.stdin)
    tool_input = data.get("tool_input", {})
    path = PurePath(tool_input.get("file_path", "")).as_posix()

    if path and SECRET_FILES.search(path) and not ALLOWED.search(path):
        deny(f"'{path}' looks like a secrets file. Use .env.example or ask the user.")
        return

    new_text = tool_input.get("content", "") or tool_input.get("new_string", "")
    for edit in tool_input.get("edits", []) or []:
        new_text += edit.get("new_string", "")
    for pattern in SECRET_CONTENT:
        if re.search(pattern, new_text):
            deny("This change would write a secret into a file. Use a Key Vault reference or an env variable.")
            return


if __name__ == "__main__":
    main()
