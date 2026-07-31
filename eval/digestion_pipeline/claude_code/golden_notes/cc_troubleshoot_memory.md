---
tags:
  - resource
  - documentation
  - claude_code
  - memory
  - troubleshooting
keywords:
  - troubleshoot claude.md
  - claude not following instructions
  - auto memory inspection
  - claude.md too large
  - instructions lost after compact
  - delivered as user message
  - path-scoped rules
  - instructionsloaded hook
topics:
  - Claude Code
  - Memory
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/memory
access_control_group: ["general"]
---

# Claude Code — Troubleshoot Memory Issues

## Overview

When CLAUDE.md instructions aren't being followed or auto memory behaves unexpectedly, the root cause is usually how memory loads rather than the instructions themselves. This note covers the four most common memory problems and how to debug each: Claude not following CLAUDE.md, not knowing what auto memory saved, a CLAUDE.md that is too large, and instructions that seem lost after `/compact`. These are the troubleshooting procedures from the memory page; for authoring guidance see [`cc_claude_md_files`](cc_claude_md_files.md), and for the auto-memory model see [`cc_auto_memory`](cc_auto_memory.md).

## Claude isn't following my CLAUDE.md

CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself. Claude reads it and tries to follow it, but there's no guarantee of strict compliance, especially for vague or conflicting instructions.

To debug:

- Run `/memory` to verify your CLAUDE.md and CLAUDE.local.md files are being loaded. If a file isn't listed, Claude can't see it.
- Check that the relevant CLAUDE.md is in a location that gets loaded for your session (see [Choose where to put CLAUDE.md files](cc_claude_md_files.md)).
- Make instructions more specific. "Use 2-space indentation" works better than "format code nicely."
- Look for conflicting instructions across CLAUDE.md files. If two files give different guidance for the same behavior, Claude may pick one arbitrarily.

If the instruction is something that must run at a specific point, such as before every commit or after each file edit, write it as a hook (see https://code.claude.com/docs/en/hooks-guide) instead. Hooks execute as shell commands at fixed lifecycle events and apply regardless of what Claude decides to do.

For instructions you want at the system prompt level, use `--append-system-prompt` (see https://code.claude.com/docs/en/cli-reference). This must be passed every invocation, so it's better suited to scripts and automation than interactive use.

> **Tip:** Use the `InstructionsLoaded` hook (see https://code.claude.com/docs/en/hooks) to log exactly which instruction files are loaded, when they load, and why. This is useful for debugging path-specific rules or lazy-loaded files in subdirectories.

## I don't know what auto memory saved

Run `/memory` and select the auto memory folder to browse what Claude has saved. Everything is plain markdown you can read, edit, or delete.

## My CLAUDE.md is too large

Files over 200 lines consume more context and may reduce adherence. Use path-scoped rules (see [`cc_claude_rules_directory`](cc_claude_rules_directory.md)) to load instructions only when Claude works with matching files, or trim content that isn't needed in every session. Splitting into `@path` imports (see [`cc_claude_md_files`](cc_claude_md_files.md)) helps organization but does not reduce context, since imported files load at launch.

## Instructions seem lost after `/compact`

Project-root CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it into the session. Nested CLAUDE.md files in subdirectories are not re-injected automatically; they reload the next time Claude reads a file in that subdirectory.

If an instruction disappeared after compaction, it was either given only in conversation or lives in a nested CLAUDE.md that hasn't reloaded yet. Add conversation-only instructions to CLAUDE.md to make them persist. See https://code.claude.com/docs/en/context-window for the full breakdown of what survives compaction.

See [Write effective instructions](cc_claude_md_files.md) for guidance on size, structure, and specificity.

**Source**: https://code.claude.com/docs/en/memory
**Last Updated**: 2026-06-13
**Status**: Active
