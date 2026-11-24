---
name: release-notes
description: Write user-facing release notes from the git history since the last tag (or a given ref). Use when the user asks for release notes, a changelog, or "what changed".
argument-hint: [since-ref]
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/collect_commits.py *)
---

# Release notes

## 1. Collect the commits

Run the bundled script. It groups commits by Conventional Commit type and prints JSON:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/collect_commits.py $ARGUMENTS
```

## 2. Write the notes

Use this structure, and skip empty sections:

```
## <version or date>

### New
- ...

### Improved
- ...

### Fixed
- ...
```

Rules:
- Write for users, not developers: say what they can now do, not which file changed.
- Merge commits that describe the same change into one line.
- Leave out `chore`, `ci`, `test` and `refactor` commits unless they change behaviour.
- No commit hashes, no author names.
