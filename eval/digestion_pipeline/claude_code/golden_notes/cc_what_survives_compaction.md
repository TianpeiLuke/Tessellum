---
tags:
  - resource
  - documentation
  - claude_code
  - context_window
  - compaction
keywords:
  - what survives compaction
  - re-injected from disk
  - path-scoped rules lost
  - invoked skill bodies cap
  - automatic compaction
  - compact with focus
  - clear between tasks
  - delegate large reads
topics:
  - Claude Code
  - Context Window
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/context-window
access_control_group: ["general"]
---

# Claude Code — What Survives Compaction

## Overview

When a long Claude Code session compacts, the harness summarizes the conversation history so the session can keep going inside the context window. **What happens to each piece of your context depends on how it was loaded.** Startup content that lives outside the message history (the system prompt, output style, project-root `CLAUDE.md`, auto memory) is re-injected unchanged, while content that entered the message history (path-scoped rules, nested `CLAUDE.md`, the verbatim conversation) is summarized away and only reloads on demand. Skill bodies are a special case: they are re-injected but capped.

This note documents Claude Code's per-mechanism survival rules and the actions you can take when your context fills up. Compaction runs **automatically** as you approach the limit, so a full window never ends your session; you can also trigger it deliberately or steer it.

## What survives compaction

When a long session compacts, Claude Code summarizes the conversation history to fit the context window. What happens to your instructions depends on how they were loaded:

| Mechanism | After compaction |
| :--- | :--- |
| System prompt and output style | Unchanged; not part of message history |
| Project-root CLAUDE.md and unscoped rules | Re-injected from disk |
| Auto memory | Re-injected from disk |
| Rules with `paths:` frontmatter | Lost until a matching file is read again |
| Nested CLAUDE.md in subdirectories | Lost until a file in that subdirectory is read again |
| Invoked skill bodies | Re-injected, capped at 5,000 tokens per skill and 25,000 tokens total; oldest dropped first |
| Hooks | Not applicable; hooks run as code, not context |

### Path-scoped rules and nested CLAUDE.md

Path-scoped rules and nested `CLAUDE.md` files load into message history when their trigger file is read, so compaction summarizes them away with everything else. They reload the next time Claude reads a matching file. If a rule must persist across compaction, **drop the `paths:` frontmatter or move it to the project-root `CLAUDE.md`.**

### Invoked skill bodies

Skill bodies are re-injected after compaction, but large skills are truncated to fit the per-skill cap, and the oldest invoked skills are dropped once the total budget is exceeded. Truncation keeps the start of the file, so **put the most important instructions near the top of `SKILL.md`.**

## When your context fills up

Claude Code compacts automatically as you approach the limit, so a full context window doesn't end your session. The automatic pass works the same way as a deliberate `/compact`. (See the source page's link to [When context fills up](https://code.claude.com/docs/en/how-claude-code-works#when-context-fills-up) for what the automatic pass preserves.)

You can also act before the automatic pass runs:

* **Compact with a focus**: run `/compact` with instructions, like `/compact focus on the auth bug fix`, before starting a long new task. The summary keeps what you choose instead of what the automatic pass guesses is important.
* **Clear between tasks**: run `/clear` when switching to unrelated work. Old conversation crowds out the files you need next and costs tokens on every message.
* **Delegate large reads**: send research to a subagent so the file contents stay in its context window, not yours.

If you need a larger window rather than a smaller conversation, Fable 5, Opus 4.6 and later, and Sonnet 4.6 support a 1 million token context window (see [Extended context](https://code.claude.com/docs/en/model-config#extended-context) for availability by plan and how to select a `[1m]` model variant). Compaction works the same way at the larger limit.

**Source**: https://code.claude.com/docs/en/context-window
**Last Updated**: 2026-06-13
**Status**: Active
