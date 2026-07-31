---
tags:
  - resource
  - documentation
  - claude_code
  - interactive_mode
  - session_features
keywords:
  - background bash commands
  - shell mode prefix
  - side questions btw
  - task list
  - session recap
  - pr review status
  - prompt suggestions
  - ctrl+b backgrounding
topics:
  - Claude Code
  - Interactive Mode
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/interactive-mode
access_control_group: ["general"]
---

# Claude Code — Interactive Session Features

## Overview

Beyond the keyboard surface and input-editing modes, a Claude Code interactive session offers a set of **in-flight helpers** that run alongside (or independently of) the model turn: backgrounded bash commands, a `!` **shell mode** that bypasses the model, grayed-out **prompt suggestions**, **side questions** with `/btw`, a live **task list**, an automatic **session recap**, and a **PR review status** badge in the footer. Several of these are designed to add value without bloating the conversation context — `/btw` answers stay ephemeral, prompt suggestions reuse the parent conversation's prompt cache, and the task list survives context compactions.

This note covers those features. The full command list lives in the [commands reference](https://code.claude.com/docs/en/commands) (digested as `cc_commands`), keyboard shortcuts proper are in [`cc_interactive_mode_keyboard_shortcuts`](cc_interactive_mode_keyboard_shortcuts.md), and input/editing modes are in [`cc_input_modes_and_editing`](cc_input_modes_and_editing.md).

## Background Bash Commands

Claude Code supports running bash commands in the background, allowing you to continue working while long-running processes execute.

### How Backgrounding Works

When Claude Code runs a command in the background, it runs the command asynchronously and immediately returns a background task ID, and can respond to new prompts while the command continues executing. To run commands in the background you can either prompt Claude Code to run a command in the background, or press **Ctrl+B** to move a regular Bash tool invocation to the background. (Tmux users must press Ctrl+B twice due to tmux's prefix key.)

Key features:

- Output is written to a file and Claude can retrieve it using the Read tool.
- Background tasks have unique IDs for tracking and output retrieval.
- Background tasks are automatically cleaned up when Claude Code exits.
- Background tasks are automatically terminated if output exceeds 5GB, with a note in stderr explaining why.

To disable all background task functionality, set the `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` environment variable to `1` (see [Environment variables](https://code.claude.com/docs/en/env-vars)). Common backgrounded commands include build tools (webpack, vite, make), package managers (npm, yarn, pnpm), test runners (jest, pytest), development servers, and long-running processes (docker, terraform).

### Shell Mode with `!` Prefix

Run shell commands directly without going through Claude by prefixing your input with `!`:

```bash
! npm test
! git status
! ls -la
```

Shell mode adds the command and its output to the conversation context, shows real-time progress and output, supports the same Ctrl+B backgrounding for long-running commands, and does not require Claude to interpret or approve the command. It supports history-based autocomplete (type a partial command and press **Tab** to complete from previous `!` commands in the current project) and exits with `Escape`, `Backspace`, or `Ctrl+U` on an empty prompt. Pasting text that starts with `!` into an empty prompt enters shell mode automatically, matching typed `!` behavior. This is useful for quick shell operations while maintaining conversation context.

## Prompt Suggestions

When you first open a session, a grayed-out example command appears in the prompt input to help you get started. Claude Code picks this from your project's git history, so it reflects files you've been working on recently. After Claude responds, suggestions continue to appear based on conversation history, such as a follow-up step from a multi-part request.

- Press **Tab** or **Right arrow** to place the suggestion in the prompt input, then **Enter** to submit.
- Start typing to dismiss it.

The suggestion runs as a background request that reuses the parent conversation's prompt cache, so the additional cost is minimal. Claude Code skips suggestion generation when the cache is cold to avoid unnecessary cost. Suggestions are automatically skipped after the first turn of a conversation and in plan mode; in print mode they are off by default. To disable prompt suggestions entirely, set `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false` or toggle the setting in `/config`.

## Side Questions with `/btw`

Use `/btw` to ask a quick question about your current work without adding to the conversation history — useful when you want a fast answer but don't want to clutter the main context or derail Claude from a long-running task:

```
/btw what was the name of that config file again?
```

Side questions have full visibility into the current conversation, so you can ask about code Claude has already read or decisions it made earlier. The question and answer are ephemeral: they appear in a dismissible overlay and **never enter the conversation history**. They are available while Claude is working (the side question runs independently and does not interrupt the main turn), have **no tool access** (answering only from what is already in context), allow a **single response** (no follow-up turns — press `f` to fork into its own session), and are **low cost** (reusing the parent conversation's prompt cache).

Once the answer appears, the overlay accepts: `Space`/`Enter`/`Escape` to dismiss; `Up`/`Down` to scroll; `c` to copy the answer as raw Markdown; `f` to fork into a new session (inheriting the parent conversation plus this Q&A as real transcript turns with full tool access; local sessions only); and `x` to clear the list of earlier `/btw` exchanges shown above the current answer.

`/btw` is described as **the inverse of a [subagent](https://code.claude.com/docs/en/sub-agents)**: it sees your full conversation but has no tools, while a subagent has full tools but starts with an empty context. Use `/btw` to ask about what Claude already knows from this session; use a subagent to go find out something new.

## Task List

When working on complex, multi-step work, Claude creates a task list to track progress. Tasks appear in the status area of the terminal with indicators showing what's pending, in progress, or complete.

- Press `Ctrl+T` to toggle the task list view. The display shows up to 5 tasks at a time.
- To see all tasks or clear them, ask Claude directly ("show me all tasks" or "clear all tasks").
- Tasks **persist across context compactions**, helping Claude stay organized on larger projects.
- To share a task list across sessions, set `CLAUDE_CODE_TASK_LIST_ID` to use a named directory in `~/.claude/tasks/`: `CLAUDE_CODE_TASK_LIST_ID=my-project claude`.

## Session Recap

When you return to the terminal after stepping away, Claude Code shows a one-line recap of what happened in the session so far. The recap generates in the background once at least three minutes have passed since the last completed turn and the terminal is unfocused, so it's ready when you switch back. Recaps only appear once the session has at least three turns, and never twice in a row.

Run `/recap` to generate a summary on demand. To turn automatic recaps off, open `/config` and disable **Session recap**. Session recap is on by default for every plan and provider, and is always skipped in non-interactive mode.

## PR Review Status

When working on a branch with an open pull request, Claude Code displays a clickable PR link in the footer (for example, "PR #446"). The link has a colored underline indicating the review state:

- Green: approved
- Yellow: pending review
- Red: changes requested
- Gray: draft

The badge disappears once the pull request merges or closes. `Cmd+click` (Mac) or `Ctrl+click` (Windows/Linux) the link to open the pull request in your browser. The status refreshes every 60 seconds, and immediately after a `gh pr` or `git push` command runs in the session. PR status requires the `gh` CLI to be installed and authenticated (`gh auth login`).

**Source**: https://code.claude.com/docs/en/interactive-mode
**Last Updated**: 2026-06-13
**Status**: Active
