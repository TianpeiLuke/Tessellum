---
tags:
  - resource
  - documentation
  - claude_code
  - subagents
  - forks
keywords:
  - forked subagent
  - fork the current conversation
  - inherit conversation history
  - input vs output isolation
  - claude_code_fork_subagent
  - shared prompt cache
  - fork vs named subagent
topics:
  - Claude Code
  - Subagents
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/sub-agents
access_control_group: ["general"]
---

# Claude Code — Fork the Current Conversation

## Overview

A **fork** is a subagent that inherits the entire conversation so far instead of starting fresh. This drops the **input isolation** that named subagents otherwise provide — a fork sees the same system prompt, tools, model, and message history as the main session, so you can hand it a side task without re-explaining the situation. The fork's own tool calls still stay out of your conversation and only its final result comes back, so your main context window stays clean (**output isolation** is preserved). Use a fork when a named subagent would need too much background to be useful, or when you want to try several approaches in parallel from the same starting point.

Forked subagents require Claude Code v2.1.117 or later. From v2.1.161 the `/fork` command is enabled by default; on earlier versions it requires setting the `CLAUDE_CODE_FORK_SUBAGENT` environment variable to `1`. Making forks the model's *default* spawn behavior is experimental and may change in future releases. This default may also be enabled in interactive sessions as part of a staged rollout.

## Enabling and Starting a Fork

To control fork mode regardless of the staged rollout, set `CLAUDE_CODE_FORK_SUBAGENT` to `1` to enable it explicitly or to `0` to disable it. The variable is honored in interactive mode and via the SDK or `claude -p`.

Enabling fork mode changes Claude Code in two ways:

- Claude spawns a fork whenever it would otherwise use the general-purpose subagent. Named subagents such as Explore still spawn as before.
- Every subagent spawn runs in the background, whether it is a fork or a named subagent. Set `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` to `1` to keep spawns synchronous.

You can start a fork yourself with `/fork` followed by a directive, with or without the variable set. Claude Code names the fork from the first words of the directive. The following example forks the conversation to draft test cases while you continue with the implementation in the main session:

```text
/fork draft unit tests for the parser changes so far
```

The fork appears in a panel below your prompt and runs in the background while you keep working. When it finishes, its result arrives as a message in your main conversation.

## Observe and Steer Running Forks

Running forks appear in a panel below the prompt input, with one row for the main session and one for each fork. Use these keys to interact with the panel:

| Key | Action |
| :-- | :----- |
| `↑` / `↓` | Move between rows |
| `Enter` | Open the selected fork's transcript and send it follow-up messages |
| `x` | Dismiss a finished fork or stop a running one |
| `Esc` | Return focus to the prompt input |

## How Forks Differ From Named Subagents

A fork inherits everything the main session has at the moment it spawns. A named subagent starts from its own definition.

| | Fork | Named subagent |
| :-- | :-- | :-- |
| Context | Full conversation history | Fresh context with the prompt you pass |
| System prompt and tools | Same as main session | From the subagent's definition file |
| Model | Same as main session | From the subagent's `model` field |
| Permissions | Prompts surface in your terminal | Auto-denied when running in the background |
| Prompt cache | Shared with main session | Separate cache |

Because a fork's system prompt and tool definitions are identical to the parent, its first request reuses the parent's prompt cache. This makes forking cheaper than spawning a fresh subagent for tasks that need the same context.

When Claude spawns a fork through the Agent tool, it can pass `isolation: "worktree"` so the fork's file edits are written to a separate git worktree instead of your checkout.

## Limitations

Setting `CLAUDE_CODE_FORK_SUBAGENT=1` enables fork mode in interactive sessions, non-interactive mode, and the Agent SDK; setting it to `0` disables fork mode everywhere, including any server-side rollout. A fork cannot spawn further forks.

**Source**: https://code.claude.com/docs/en/sub-agents
**Last Updated**: 2026-06-13
**Status**: Active
