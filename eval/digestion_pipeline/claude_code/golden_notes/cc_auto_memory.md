---
tags:
  - resource
  - documentation
  - claude_code
  - memory
  - auto_memory
keywords:
  - auto memory
  - claude writes notes
  - memory.md index
  - topic files
  - autoMemoryEnabled
  - autoMemoryDirectory
  - per-repository memory
  - 200 lines 25kb
  - /memory command
  - cross-session learnings
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

# Claude Code — Auto Memory

## Overview

**Auto memory** lets Claude accumulate knowledge across sessions without you writing anything: Claude saves notes for itself as it works — build commands, debugging insights, architecture notes, code style preferences, and workflow habits. Claude does not save something every session; it decides what is worth remembering based on whether the information would be useful in a future conversation. This is the Claude-written counterpart to author-written [CLAUDE.md files](https://code.claude.com/docs/en/memory) (see the [memory overview](cc_memory_overview.md) for the comparison).

Auto memory requires Claude Code **v2.1.59 or later** (check with `claude --version`). It is on by default. Memory is stored per repository as a `MEMORY.md` index plus optional topic files, and only the start of `MEMORY.md` is loaded into each session so the feature stays cheap on context.

## Enable or disable auto memory

Auto memory is on by default. To toggle it, open `/memory` in a session and use the auto memory toggle, or set `autoMemoryEnabled` in your project settings:

```json
{
  "autoMemoryEnabled": false
}
```

To disable auto memory via environment variable, set `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

## Storage location

Each project gets its own memory directory at `~/.claude/projects/<project>/memory/`. The `<project>` path is derived from the git repository, so all worktrees and subdirectories within the same repo share one auto memory directory. Outside a git repo, the project root is used instead.

To store auto memory in a different location, set `autoMemoryDirectory` in your `settings.json`. It is read from any settings scope: user, project, local, policy, or `--settings`.

```json
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

The value must be an absolute path or start with `~/`. When set in a project's `.claude/settings.json` or `.claude/settings.local.json`, the value is honored only after you accept the workspace trust dialog for that folder — the same gate that governs hooks.

The directory contains a `MEMORY.md` entrypoint and optional topic files:

```text
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Concise index, loaded into every session
├── debugging.md       # Detailed notes on debugging patterns
├── api-conventions.md # API design decisions
└── ...                # Any other topic files Claude creates
```

`MEMORY.md` acts as an index of the memory directory. Claude reads and writes files in this directory throughout your session, using `MEMORY.md` to keep track of what is stored where.

Auto memory is **machine-local**. All worktrees and subdirectories within the same git repository share one auto memory directory. Files are not shared across machines or cloud environments.

## How it works

The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start. Claude keeps `MEMORY.md` concise by moving detailed notes into separate topic files.

This limit applies only to `MEMORY.md`. CLAUDE.md files are loaded in full regardless of length, though shorter files produce better adherence.

Topic files like `debugging.md` or `patterns.md` are not loaded at startup. Claude reads them on demand using its standard file tools when it needs the information.

Claude reads and writes memory files during your session. When you see "Writing memory" or "Recalled memory" in the Claude Code interface, Claude is actively updating or reading from `~/.claude/projects/<project>/memory/`.

Subagents can also maintain their own auto memory; see [subagent configuration](https://code.claude.com/docs/en/sub-agents#enable-persistent-memory) for details.

## Audit and edit your memory

Auto memory files are plain markdown you can edit or delete at any time. Run `/memory` to browse and open memory files from within a session.

## View and edit with `/memory`

The `/memory` command lists all CLAUDE.md, CLAUDE.local.md, and rules files loaded in your current session, lets you toggle auto memory on or off, and provides a link to open the auto memory folder. Select any file to open it in your editor.

When you ask Claude to remember something — like "always use pnpm, not npm" or "remember that the API tests require a local Redis instance" — Claude saves it to auto memory. To add instructions to CLAUDE.md instead, ask Claude directly (for example, "add this to CLAUDE.md"), or edit the file yourself via `/memory`.

**Source**: https://code.claude.com/docs/en/memory
**Last Updated**: 2026-06-13
**Status**: Active
