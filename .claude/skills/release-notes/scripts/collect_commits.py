#!/usr/bin/env python3
"""Collect commits since a ref (default: last tag, else full history) as grouped JSON."""
import json
import re
import subprocess
import sys

GROUPS = {"feat": "new", "fix": "fixed", "perf": "improved", "docs": "improved"}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()


def main() -> None:
    since = sys.argv[1] if len(sys.argv) > 1 else git("describe", "--tags", "--abbrev=0")
    rev_range = f"{since}..HEAD" if since else "HEAD"
    log = git("log", rev_range, "--no-merges", "--pretty=format:%s")

    result = {"since": since or "beginning", "new": [], "improved": [], "fixed": [], "other": []}
    for subject in filter(None, log.splitlines()):
        m = re.match(r"^(\w+)(\([^)]*\))?!?:\s*(.+)$", subject)
        if m:
            result[GROUPS.get(m.group(1), "other")].append(m.group(3))
        else:
            result["other"].append(subject)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
