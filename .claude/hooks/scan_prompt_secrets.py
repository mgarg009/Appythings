#!/usr/bin/env python3
"""Guardrail 3 (UserPromptSubmit): stop secrets before they reach the model.

If you paste a private key or a token into the prompt, the prompt is
rejected and you see why. Nothing is sent to Claude.
"""
import json
import re
import sys

PATTERNS = {
    "a private key": r"-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY",
    "an API key": r"\bsk-[A-Za-z0-9_-]{20,}",
    "an AWS access key": r"\bAKIA[0-9A-Z]{16}\b",
    "an Azure storage key": r"AccountKey=[A-Za-z0-9+/=]{40,}",
    "an APIM subscription key": r"Ocp-Apim-Subscription-Key\s*[:=]\s*[0-9a-f]{32}",
    "a GitHub token": r"\bgh[pousr]_[A-Za-z0-9]{30,}",
    "a client secret": r"client_secret\s*[:=]\s*\S{20,}",
}


def main() -> None:
    data = json.load(sys.stdin)
    prompt = data.get("prompt", "")

    for label, pattern in PATTERNS.items():
        if re.search(pattern, prompt, re.IGNORECASE):
            print(json.dumps({
                "decision": "block",
                "reason": (
                    f"AppyThings guardrail: your prompt seems to contain {label}. "
                    "Remove it (and rotate it if it was real), then try again."
                ),
            }))
            return


if __name__ == "__main__":
    main()
