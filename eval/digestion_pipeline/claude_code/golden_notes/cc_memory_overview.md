---
tags:
  - resource
  - documentation
  - claude_code
  - memory
keywords:
  - claude code memory
  - claude.md vs auto memory
  - cross-session memory
  - persistent instructions
  - fresh context window
  - memory as context not enforcement
  - pretooluse hook enforcement
topics:
  - Claude Code
  - Memory
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/memory
access_control_group: ["general"]
---

# Claude Code — How Claude Remembers Your Project

## Overview

Each Claude Code session begins with a **fresh context window**. Two complementary mechanisms carry knowledge across sessions so Claude doesn't start from zero every time: **CLAUDE.md files**, the persistent instructions *you* write, and **auto memory**, the notes *Claude* writes for itself based on your corrections and preferences. Both are loaded at the start of every conversation.

Critically, Claude treats both memory systems as **context, not enforced configuration** — the more specific and concise your instructions, the more consistently Claude follows them, but there is no guarantee of strict compliance. To block an action regardless of what Claude decides, you use a PreToolUse hook instead, which is a hard enforcement layer rather than guidance.

## Two mechanisms for cross-session knowledge

The two memory systems serve different roles and are written by different authors:

- **CLAUDE.md files** — instructions you write to give Claude persistent context. Use them when you want to *guide* Claude's behavior.
- **Auto memory** — notes Claude writes itself based on your corrections and preferences. It lets Claude *learn* from your corrections without manual effort.

Both load at session start. Author-written CLAUDE.md is documented in [CLAUDE.md files](cc_claude_md_files.md); Claude-written auto memory is documented in [auto memory](cc_auto_memory.md).

## CLAUDE.md vs auto memory

Claude Code has two complementary memory systems, both loaded at the start of every conversation. The table contrasts them across who authors the content, what it contains, its scope, when it loads, and what each is best used for:

|                      | CLAUDE.md files                                   | Auto memory                                                      |
| :------------------- | :------------------------------------------------ | :--------------------------------------------------------------- |
| **Who writes it**    | You                                               | Claude                                                           |
| **What it contains** | Instructions and rules                            | Learnings and patterns                                           |
| **Scope**            | Project, user, or org                             | Per repository, shared across worktrees                          |
| **Loaded into**      | Every session                                     | Every session (first 200 lines or 25KB)                          |
| **Use for**          | Coding standards, workflows, project architecture | Build commands, debugging insights, preferences Claude discovers |

Use **CLAUDE.md files** when you want to guide Claude's behavior. **Auto memory** lets Claude learn from your corrections without manual effort.

## Memory is context, not enforcement

Because both systems load as context rather than enforced configuration, instruction-following is best-effort. Two implications follow:

- **To enforce behavior, use a hook.** To block an action regardless of what Claude decides, use a [PreToolUse hook](https://code.claude.com/docs/en/hooks-guide). Hooks execute deterministically at lifecycle events, independent of the model's discretion.
- **Subagents have their own auto memory.** Subagents can also maintain their own auto memory; see [subagent configuration](https://code.claude.com/docs/en/sub-agents#enable-persistent-memory) for details.

**Source**: https://code.claude.com/docs/en/memory
**Last Updated**: 2026-06-13
**Status**: Active
