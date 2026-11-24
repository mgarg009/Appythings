---
name: app-idea-brief
description: Turn a rough app idea into a one-page product brief (problem, users, MVP scope, risks, next steps). Use when the user describes an app or product idea and wants it structured.
when_to_use: "I have an app idea", "write a brief for", "is this idea worth building", "scope an MVP"
argument-hint: [idea in a few words]
---

# App idea brief

Write a one-page brief for this idea: $ARGUMENTS

## Steps

1. If the idea is missing the target user or the core problem, ask ONE question to get it. Otherwise continue.
2. Fill in [template.md](template.md) exactly, section by section.
3. Keep the MVP to at most 5 features. Move everything else to "Later".
4. In "Risks", always check: legal or licensing needs, payments, personal data (GDPR), app store rules.
5. Save the result as `briefs/<short-kebab-name>.md` and show the path.

## Rules

- Plain language, short sentences, no dashes as punctuation.
- Do not invent market numbers. If a number would help, write "to verify:" and what to look up.
