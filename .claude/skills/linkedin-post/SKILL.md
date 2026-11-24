---
name: linkedin-post
description: Draft a short LinkedIn post in a fixed house style from a topic, a launch, or a lesson learned. Use when the user asks for a LinkedIn post or a social update.
argument-hint: [topic]
disallowed-tools: Bash Write Edit
---

# LinkedIn post

Draft a post about: $ARGUMENTS

## House style

- Hook in the first line, under 12 words. No "I'm excited to announce".
- 80 to 150 words total. Short paragraphs of 1 to 2 lines.
- No em dashes or en dashes anywhere. Use a full stop or a comma instead.
- At most 3 hashtags, at the end.
- End with one question to invite comments.

## Output

Give two versions labelled **Short** and **Story**, then stop.
This skill only drafts text: it cannot run commands or write files (see `disallowed-tools`).
