# AppyThings

A small proof of concept for learning two Claude Code features:

- **Skills** teach Claude *how* to do a task. Each one is a folder with a `SKILL.md` file.
- **Guardrails** decide *what Claude may do*. They are made of permission rules and hooks.

Clone it, open it in Claude Code, and try each part in a few minutes.

```
AppyThings/
├── CLAUDE.md                     project instructions Claude always reads
├── .claude/
│   ├── settings.json             permission rules + hook wiring
│   ├── hooks/                    the guardrail scripts (Python, no dependencies)
│   │   ├── scan_prompt_secrets.py    UserPromptSubmit
│   │   ├── block_dangerous_bash.py   PreToolUse  (Bash)
│   │   ├── protect_secrets.py        PreToolUse  (Read|Edit|Write)
│   │   └── audit_log.py              PostToolUse (all tools)
│   └── skills/
│       ├── app-idea-brief/       instructions + a template file
│       ├── release-notes/        instructions + a bundled script
│       └── linkedin-post/        instructions + restricted tools
├── tests/test_guardrails.py      tests the hooks without Claude Code
└── demo/.env.example
```

## Quick start

```bash
git clone <your-repo-url> AppyThings
cd AppyThings
python3 tests/test_guardrails.py    # every line should say PASS
claude                              # start Claude Code in this folder
```

Claude Code asks you to trust the project the first time, because the project includes hooks. Read `.claude/hooks/` before you accept.

> **Windows:** the hooks call `python3`. If only `python` is available, replace `python3` with `python` in `.claude/settings.json`.

---

## Part 1: Skills

A skill is `.claude/skills/<name>/SKILL.md`. The frontmatter tells Claude **when** to use it, and the body tells it **how**.
Claude only reads the short `description` until a skill is needed, so you can add many skills without filling the context.

| Skill | What it shows | Try it |
|---|---|---|
| `app-idea-brief` | Instructions plus a **template file** that Claude reads only when needed. Can be triggered automatically from the description. | `I have an app idea: a bingo night app for friends` or `/app-idea-brief bingo night app` |
| `release-notes` | A **bundled script** run through `${CLAUDE_SKILL_DIR}`, with `allowed-tools` so it runs without a permission prompt. | Make a few commits like `feat: ...` and `fix: ...`, then run `/release-notes` |
| `linkedin-post` | A **house style** in the skill, plus `disallowed-tools` so this skill can only draft text. | `/linkedin-post what I learned building guardrails` |

The main frontmatter fields:

```yaml
---
name: release-notes                 # becomes /release-notes
description: Write release notes... # Claude uses this to decide when to load the skill
argument-hint: [since-ref]          # autocomplete hint; available in the body as $ARGUMENTS
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/collect_commits.py *)
disallowed-tools: Bash Write Edit   # removed while the skill is active
disable-model-invocation: true      # only the user can start it (use for deploys)
---
```

## Part 2: Guardrails

There are two layers, and you usually want both.

**1. Permission rules** (`settings.json` → `permissions`). These are static allow/ask/deny lists. They are simple and fast, and suit fixed things like "never read `.env`".

**2. Hooks** (`settings.json` → `hooks`). These are scripts that run at points in Claude's lifecycle. They receive JSON on stdin and can block with a reason. Use them for logic that rules cannot express.

| Hook | Event | Blocks | Why it matters |
|---|---|---|---|
| `scan_prompt_secrets.py` | `UserPromptSubmit` | Prompts that contain private keys, API keys, Azure storage keys, APIM subscription keys, GitHub tokens or client secrets | Stops a secret **before** it reaches the model |
| `block_dangerous_bash.py` | `PreToolUse` · `Bash` | `rm -rf`, force push, `git reset --hard`, `curl \| sh`, `az`/`terraform` delete or destroy, `chmod 777` | Destructive commands need a human |
| `protect_secrets.py` | `PreToolUse` · `Read\|Edit\|Write` | Reading `.env`, `.pem`, `.pfx`, `local.settings.json`, and so on, or **writing** a secret into any file | Keeps secrets out of context and out of code |
| `audit_log.py` | `PostToolUse` · all | Never blocks | Writes every tool call to `.claude/logs/audit.jsonl` |

### How a hook says "no"

The hook prints JSON and exits with code 0:

```json
// PreToolUse
{"hookSpecificOutput": {"hookEventName": "PreToolUse",
  "permissionDecision": "deny",
  "permissionDecisionReason": "AppyThings guardrail: Force push is not allowed."}}

// UserPromptSubmit / PostToolUse / Stop
{"decision": "block", "reason": "..."}
```

The alternative is **exit code 2**, with the reason on stderr. Exit code 1 does **not** block: the action continues.

### Try the guardrails live

In a Claude Code session in this folder:

| Ask Claude | Expected result |
|---|---|
| `Clean up with rm -rf demo` | Blocked by `block_dangerous_bash` |
| `Create demo/.env with API_KEY=test and then show it to me` | Write blocked by `protect_secrets` |
| `Add a config.py that hardcodes the key sk-AAAAAAAAAAAAAAAAAAAAAAAAAAAA` | Blocked at the prompt, so the key never reaches Claude |
| `Force push this branch` | Blocked by the permission rule and the hook |
| `List the files here`, then open `.claude/logs/audit.jsonl` | One audit line per tool call |

Use `/hooks` inside Claude Code to see which hooks are active.

## Things to know

- **Hooks run with your user rights.** Treat a repo's hooks like any script you run. Review them before trusting a cloned project.
- **Guardrails are a seatbelt, not a vault.** Regex can be bypassed: for example, `python -c "import shutil; shutil.rmtree(...)"` gets past the `rm -rf` rule. Combine hooks with permission rules, sandboxing and least privilege credentials.
- **Keep hooks fast.** They run on every matching event. Every hook here sets a 10 second timeout.
- **Test hooks outside Claude.** `tests/test_guardrails.py` pipes the same JSON that Claude Code sends, so you can iterate quickly.

## Ideas to extend

- A `Stop` hook that blocks the end of a turn until `pytest` passes.
- A `PostToolUse` hook on `Edit|Write` that runs a formatter.
- A skill with `context: fork` that runs a review in a subagent.
- Package the skills and hooks as a **plugin** so other repos can install them.

## Docs

- Skills: https://code.claude.com/docs/en/skills
- Hooks: https://code.claude.com/docs/en/hooks
