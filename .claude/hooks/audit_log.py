#!/usr/bin/env python3
"""Guardrail 4 (PostToolUse): keep an audit trail of every tool Claude used.

Writes one JSON line per tool call to .claude/logs/audit.jsonl. This hook
never blocks; it only records.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def summarize(tool_input: dict) -> str:
    for key in ("command", "file_path", "pattern", "url", "skill"):
        if key in tool_input:
            return str(tool_input[key])[:200]
    return ""


def main() -> None:
    data = json.load(sys.stdin)
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", data.get("cwd", ".")))
    log_dir = project / ".claude" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    entry = {
        "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "session": data.get("session_id"),
        "tool": data.get("tool_name"),
        "target": summarize(data.get("tool_input", {})),
    }
    with open(log_dir / "audit.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    main()
