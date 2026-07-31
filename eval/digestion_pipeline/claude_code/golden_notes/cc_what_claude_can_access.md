---
tags:
  - resource
  - documentation
  - claude_code
  - context
  - access
keywords:
  - what claude can access
  - project files access
  - terminal access
  - git state
  - claude.md
  - auto memory
  - memory.md
  - configured extensions
topics:
  - Claude Code
  - Access and Context
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/how-claude-code-works
access_control_group: ["general"]
---

# Claude Code — What Claude Can Access

## Overview

When you run `claude` in a directory, Claude Code gains access to a defined set of resources drawn from that working directory and its surrounding environment. This guide section focuses on the terminal (Claude Code also runs in VS Code, JetBrains IDEs, and other environments). Because Claude sees your whole project, it can work across it rather than file-by-file. The access set spans your project files, your terminal, your git state, your `CLAUDE.md`, auto memory, and the extensions you configure.

## What Running `claude` Grants

Running `claude` in a directory gives Claude Code access to:

- **Your project.** Files in your directory and subdirectories, plus files elsewhere with your permission.
- **Your terminal.** Any command you could run: build tools, git, package managers, system utilities, scripts. If you can do it from the command line, Claude can too.
- **Your git state.** Current branch, uncommitted changes, and recent commit history.
- **Your CLAUDE.md.** A markdown file where you store project-specific instructions, conventions, and context that Claude should know every session.
- **Auto memory.** Learnings Claude saves automatically as you work, like project patterns and your preferences. The first 200 lines or 25KB of MEMORY.md, whichever comes first, load at the start of each session.
- **Extensions you configure.** MCP servers for external services, skills for workflows, subagents for delegated work, and Claude in Chrome for browser interaction.

## Why Whole-Project Access Matters

Because Claude sees your whole project, it can work across it. When you ask Claude to "fix the authentication bug," it searches for relevant files, reads multiple files to understand context, makes coordinated edits across them, runs tests to verify the fix, and commits the changes if you ask. This is different from inline code assistants that only see the current file.

**Source**: https://code.claude.com/docs/en/how-claude-code-works
**Last Updated**: 2026-06-13
**Status**: Active
