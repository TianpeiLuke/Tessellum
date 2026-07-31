---
tags:
  - resource
  - documentation
  - claude_code
  - commands
  - workflow
keywords:
  - commands across a typical workflow
  - first session in a repo
  - during a task
  - running work in parallel
  - before you ship
  - between sessions
  - when something is wrong
  - task-oriented command index
topics:
  - Claude Code
  - Commands
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/commands
access_control_group: ["general"]
---

# Claude Code — Commands Across a Typical Workflow

## Overview

Most Claude Code commands are useful at a specific point in a session, from setting up a project to shipping a change. This note is the **task-oriented index** into the full command catalogue (the alphabetical reference lives in [Commands Reference](cc_commands_reference.md)): rather than listing every command, it walks the **six phases of a typical session** and names the commands that matter in each — **first session in a repo**, **during a task**, **running work in parallel**, **before you ship**, **between sessions**, and **when something is wrong**.

A command is recognized only at the start of your message, and any text after the command name is passed to it as arguments. Use this note to find the right command for *what you are doing*; use the [reference](cc_commands_reference.md) for the full purpose, arguments, and availability of any individual command.

## First session in a repo

When you open Claude Code in a repository for the first time, set up the project's memory, servers, and rules:

- Run `/init` to generate a starter `CLAUDE.md`, then `/memory` to refine it.
- Use `/mcp` and `/agents` to set up any servers or subagents the project needs.
- Use `/permissions` to set the approval rules you want.

## During a task

Once you are working, these commands shape *how* Claude approaches the task and keep the context window healthy:

- `/plan` switches into plan mode before a large change.
- `/model` and `/effort` adjust how much reasoning you're spending.
- When the conversation gets long, `/context` shows where the window is going and `/compact` summarizes it down.
- Use `/btw` for a quick aside that shouldn't bloat history.

## Running work in parallel

When you want Claude working on more than one thing at once:

- `/agents` opens the manager for the subagents Claude can delegate side tasks to.
- `/tasks` lists what's running in the background of the current session.
- `/background` detaches the whole session to keep running as a background agent and frees your terminal.
- For a large change that spans the codebase, `/batch` decomposes it into independent units and runs each in its own worktree.

(See [Run agents in parallel](https://code.claude.com/docs/en/agents) for how these approaches relate.)

## Before you ship

When the work is done and you want a review of the diff:

- `/diff` shows what changed.
- `/code-review` checks the diff for correctness bugs and cleanups, and can apply the findings with `--fix`.
- `/review` or `/security-review` give a deeper read-only pass.
- `/code-review ultra` runs a multi-agent review in the cloud.

## Between sessions

To start, return to, fork, or move conversations:

- `/clear` starts fresh on a new task while keeping project memory.
- `/resume` and `/branch` let you return to or fork an earlier conversation.
- `/teleport` pulls a web session into this terminal.
- `/remote-control` lets you continue this local session from another device.

## When something is wrong

To recover from a bad state or diagnose problems:

- `/rewind` rolls code and conversation back to a checkpoint, or summarizes part of the conversation.
- `/doctor` and `/debug` diagnose install and runtime issues.
- `/feedback` reports a bug with session context attached.

**Source**: https://code.claude.com/docs/en/commands
**Last Updated**: 2026-06-13
**Status**: Active
