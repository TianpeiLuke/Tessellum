---
tags:
  - resource
  - documentation
  - claude_code
  - context_window
  - anatomy
keywords:
  - context window anatomy
  - what loads into context
  - auto-loaded startup content
  - file reads dominate context
  - invisible vs visible in terminal
  - check your session
  - context command
  - memory command
topics:
  - Claude Code
  - Context Window
language: markdown
date of note: 2026-06-13
status: active
building_block: model
source_url: https://code.claude.com/docs/en/context-window
access_control_group: ["general"]
---

# Claude Code — Context Window Anatomy

## Overview

Claude Code's **context window** holds everything Claude knows about your session: your instructions, the files it reads, its own responses, and content that never appears in your terminal. A large share of that window is consumed *before you type anything* — project knowledge, not your words — and most of it is invisible in the terminal even though it costs tokens. This note anatomizes what fills the window across a realistic session (startup loads, Claude's working reads, rules, hooks, your prompts) and how to inspect your own usage.

The official page presents this through an interactive timeline simulation; the token counts below are **representative / illustrative** (actual values vary with your CLAUDE.md size, MCP servers, and file lengths) and are paraphrased from the page's written breakdown rather than measured.

## What loads before you type anything

Before your first prompt, a set of startup content auto-loads into context. Each item is invisible in your terminal:

- **System prompt** — core instructions for behavior, tool use, and response formatting. Always loaded first; you never see it.
- **Auto memory (MEMORY.md)** — Claude's notes to itself from previous sessions (build commands it learned, patterns, mistakes to avoid). The first 200 lines or 25KB, whichever comes first, are loaded into the conversation context.
- **Environment info** — working directory, platform, shell, OS version, and whether this is a git repo. Git branch, status, and recent commits load as a separate block at the very end of the system prompt.
- **MCP tool names (deferred)** — MCP tool names are listed so Claude knows what is available; by default full schemas stay deferred and Claude loads specific ones on demand via tool search.
- **Skill descriptions** — one-line descriptions of available skills. Full skill content loads only when Claude actually uses one. Skills with `disable-model-invocation: true` are not in this list and cost zero context until invoked with `/name`.
- **`~/.claude/CLAUDE.md`** — your global preferences, applied to every project, loaded at the start of every conversation.
- **Project CLAUDE.md** — project conventions, build commands, and architecture notes; loaded alongside the global instructions.

Your own setup may add more here, like an [output style](https://code.claude.com/docs/en/output-styles) or text from [`--append-system-prompt`](https://code.claude.com/docs/en/cli-reference), which both go into the system prompt the same way. Your first prompt is tiny compared to what is already loaded — most of Claude's context is project knowledge.

## What loads as Claude works

As Claude works through the task, each step adds to the window:

- **File reads** — each file Claude reads grows the context, and file reads dominate context usage. You see a one-line "Read auth.ts" in your terminal, but the file's full content (only Claude sees it) is what enters context.
- **Path-scoped rules** — [path-specific rules](https://code.claude.com/docs/en/memory#path-specific-rules) in `.claude/rules/` with a `paths:` pattern load automatically alongside matching files. You see a one-line "Loaded ..." notice, not the rule content.
- **Tool output** — search results and command output (e.g. test runs) enter context; you see a brief mention, not the full output.
- **Claude's own work** — analysis, edits, and summaries appear in your terminal *and* count against context.
- **Hooks** — a [PostToolUse hook](https://code.claude.com/docs/en/hooks-guide) can fire after each edit. Output reaches Claude's context only via the hook's `hookSpecificOutput.additionalContext` field; plain stdout on exit 0 goes to the debug log, not the context.

A follow-up prompt builds on the same context — everything from earlier is still there. The biggest context-saving move is to **delegate large reads to a [subagent](https://code.claude.com/docs/en/sub-agents)**: the subagent works in its own separate context window, so its file reads stay out of yours and only its final summary (plus a small metadata trailer with token counts and duration) comes back.

## Invisible vs visible in your terminal

A key property of the window is that what you see in your terminal is a small subset of what is in context. Startup content (system prompt, memory, CLAUDE.md, MCP names, skill descriptions), file contents, rule bodies, and hook context are **invisible** — they cost tokens without appearing in the terminal. Your prompts, Claude's analysis, and diffs are **shown**; rule loads, file reads, and tool output appear as **one-line** notices. This is why context usage is easy to underestimate from the terminal alone.

## What survives when the window fills

As the window fills toward the limit, Claude Code compacts automatically (and you can run `/compact` yourself) to summarize the conversation back into a smaller space. Which loaded content survives versus is dropped is governed by per-mechanism rules — covered in the sibling note [What Survives Compaction](cc_what_survives_compaction.md).

If you need a larger window rather than a shorter conversation, certain models support a 1 million token context window; see [Extended context](https://code.claude.com/docs/en/model-config#extended-context) for availability and how to select a `[1m]` model variant. Compaction works the same way at the larger limit.

## Check your own session

The visualization uses representative numbers. To see your actual context usage at any point:

- Run `/context` for a live breakdown by category with optimization suggestions.
- Run `/memory` to check which CLAUDE.md and auto memory files loaded at startup.

**Source**: https://code.claude.com/docs/en/context-window
**Last Updated**: 2026-06-13
**Status**: Active
