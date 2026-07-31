---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - context_window
keywords:
  - agent sdk context window
  - what consumes context
  - automatic compaction
  - compact_boundary
  - precompact hook
  - prompt caching
  - keep context efficient
  - subagents fresh context
  - mcp tool search
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/agent-loop
access_control_group: ["general"]
---

# Agent SDK — The Context Window

## Overview

The **context window** is the total amount of information available to Claude during a session. It does **not** reset between turns within a session — everything accumulates: the system prompt, tool definitions, conversation history, tool inputs, and tool outputs. Content that stays the same across turns (system prompt, tool definitions, CLAUDE.md) is automatically **prompt cached**, which reduces cost and latency for repeated prefixes.

This note covers what consumes context in an Agent SDK session, how the SDK automatically compacts the conversation when the window approaches its limit, and the strategies for keeping context efficient in long-running agents. It is one slice of the agent-loop page; the broader loop mechanics, loop controls (including the `effort` option referenced here), and result/hooks are documented in sibling notes.

## What Consumes Context

Each component affects context differently in the SDK:

| Source | When it loads | Impact |
| :--- | :--- | :--- |
| **System prompt** | Every request | Small fixed cost, always present |
| **CLAUDE.md files** | Session start, via `settingSources` | Full content in every request (but prompt-cached, so only the first request pays full cost) |
| **Tool definitions** | Every request; MCP schemas deferred by default | Built-in tool schemas load every request. Tool search defers MCP tool schemas by default, falling back to upfront loading on Vertex AI or a non-first-party `ANTHROPIC_BASE_URL` |
| **Conversation history** | Accumulates over turns | Grows with each turn: prompts, responses, tool inputs, tool outputs |
| **Skill descriptions** | Session start, via setting sources | Short summaries; full content loads only when invoked |

Large tool outputs consume significant context: reading a big file or running a command with verbose output can use thousands of tokens in a single turn. Because context accumulates across turns, longer sessions with many tool calls build up significantly more context than short ones.

CLAUDE.md and skills are loaded via `settingSources` — see [Agent SDK — settingSources and Claude Code Features](cc_agent_sdk_settingsources_and_features.md). For the full tool-search loading matrix and per-feature context-cost breakdown, see the [MCP](https://code.claude.com/docs/en/agent-sdk/mcp) and [features overview](https://code.claude.com/docs/en/features-overview) pages.

## Automatic Compaction

When the context window approaches its limit, the SDK automatically **compacts** the conversation: it summarizes older history to free space, keeping your most recent exchanges and key decisions intact. The SDK emits a message with `type: "system"` and `subtype: "compact_boundary"` in the stream when this happens (in Python this is a `SystemMessage`; in TypeScript it is a separate `SDKCompactBoundaryMessage` type).

Compaction replaces older messages with a summary, so specific instructions from early in the conversation may not be preserved. Persistent rules belong in CLAUDE.md (loaded via `settingSources`) rather than in the initial prompt, because CLAUDE.md content is re-injected on every request.

You can customize compaction behavior in several ways:

- **Summarization instructions in CLAUDE.md** — the compactor reads your CLAUDE.md like any other context, so you can include a section telling it what to preserve when summarizing. The section header is free-form (not a magic string); the compactor matches on intent.
- **`PreCompact` hook** — run custom logic before compaction occurs, for example to archive the full transcript. The hook receives a `trigger` field (`manual` or `auto`).
- **Manual compaction** — send `/compact` as a prompt string to trigger compaction on demand. Commands sent this way are SDK inputs, not CLI-only shortcuts.

A CLAUDE.md summarization-instructions section (the header name isn't special; use any clear label) looks like:

```markdown CLAUDE.md
# Summary instructions

When summarizing this conversation, always preserve:
- The current task objective and acceptance criteria
- File paths that have been read or modified
- Test results and error messages
- Decisions made and the reasoning behind them
```

The `PreCompact` hook and the full loop hooks table are documented in [Agent SDK — Result and Hooks](https://code.claude.com/docs/en/agent-sdk/agent-loop).

## Keep Context Efficient

A few strategies for long-running agents:

- **Use subagents for subtasks.** Each subagent starts with a fresh conversation (no prior message history, though it does load its own system prompt and project-level context like CLAUDE.md). It does not see the parent's turns, and only its final response returns to the parent as a tool result. The main agent's context grows by that summary, not by the full subtask transcript.
- **Be selective with tools.** Every tool definition takes context space. Use the `tools` field on `AgentDefinition` to scope subagents to the minimum set they need.
- **Watch MCP server costs.** MCP tool search defers MCP tool schemas by default and loads them on demand. When tool search is off, on Vertex AI, or behind a non-first-party `ANTHROPIC_BASE_URL`, each MCP server adds all its tool schemas to every request, so a few servers with many tools can consume significant context before the agent does any work.
- **Use lower effort for routine tasks.** Set `effort` to `"low"` for agents that only need to read files or list directories. This reduces token usage and cost. (The `effort` levels and other loop controls are detailed in [Agent SDK — Control How the Loop Runs](cc_agent_sdk_loop_controls.md).)

**Source**: https://code.claude.com/docs/en/agent-sdk/agent-loop
**Last Updated**: 2026-06-13
**Status**: Active
