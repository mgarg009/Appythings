# AppyThings

A small playground for learning Claude Code **skills** and **guardrails**.

- Skills live in `.claude/skills/`. Guardrails live in `.claude/settings.json` and `.claude/hooks/`.
- Never read or print `.env` files. Use `.env.example` for the shape of config.
- If a guardrail blocks you, explain the block to the user. Do not try another command to get around it.
- Run `python3 tests/test_guardrails.py` after changing any hook.
