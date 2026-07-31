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

## Related Notes

### Related Notes (Claude Code Series)

- [Claude Code — Context Window Anatomy](cc_context_window_anatomy.md) — relevance: the CLI counterpart to this note's "What Consumes Context" table — it anatomizes what fills the window across a realistic session (startup loads, working reads, rules, hooks), the same accumulation this SDK note describes.
- [Claude Code — What Survives Compaction](cc_what_survives_compaction.md) — relevance: the CLI analog of this note's Automatic Compaction section; it spells out the per-mechanism survival rules (re-injected vs summarized away) behind the claim here that early-prompt instructions may not be preserved and belong in CLAUDE.md.
- [Claude Code — Context Cost by Feature](cc_context_cost_by_feature.md) — relevance: expands the per-source impact this note tabulates (CLAUDE.md every request, skill descriptions at session start, MCP schemas deferred, subagent isolated window, hook zero cost) into a full when-it-loads breakdown.
- [Claude Code — How Prompt Caching Works](cc_prompt_caching_mechanism.md) — relevance: this note says stable prefixes (system prompt, tool definitions, CLAUDE.md) are automatically prompt-cached; this sibling is the mechanism — exact prefix match, the three request layers, and the model+effort cache key.
- [Agent SDK — Control How the Loop Runs](cc_agent_sdk_loop_controls.md) — relevance: this note's "use lower effort for routine tasks" efficiency tip points here; the sibling documents the `effort` option (and turns/budget/permission) on `ClaudeAgentOptions` that this note references.
- [Agent SDK — settingSources and Claude Code Features](cc_agent_sdk_settingsources_and_features.md) — relevance: this note says CLAUDE.md and skills load via `settingSources` and persistent rules belong there; the sibling is the procedure for loading those filesystem features the context table depends on.

### Related Notes (Out-of-Series)

- [Context Window](../../term_dictionary/term_context_window.md) — this note IS the SDK's context-window page (what accumulates, the per-source cost table, and limits); the term is its definitional anchor.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — stable prefixes (system prompt, tool definitions, CLAUDE.md) are automatically prompt-cached to cut cost/latency for repeated prefixes — the mechanism this term defines.
- [Compaction](../../term_dictionary/term_compaction.md) — the Automatic Compaction section (summarize older history, `compact_boundary` message, `PreCompact` hook, `/compact`) is exactly the compaction mechanism this term names.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — the "Keep context efficient" strategies (subagents, scoped tools, watch MCP costs, lower effort) are textbook context-engineering practices this term defines.
- [Subagent](../../term_dictionary/term_subagent.md) — the top efficiency strategy is offloading subtasks to subagents that start with fresh context and return only a summary, so the main window grows by the summary not the transcript — the isolation property this term defines.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — MCP tool schemas can consume significant context unless deferred by tool search; MCP is a major context-cost source this note tracks.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — persistent rules belong in CLAUDE.md (re-injected every request, survives compaction) rather than the prompt — the agentic-memory persistence mechanism this term describes.
- [How To: Manage the Context Window Effectively](../../how_to/howto_manage_context_window.md) — relevance: a tool-agnostic procedure whose "what's in your context window" list (system prompt, conversation history, file contents, tool outputs) and pruning/isolation strategies mirror this note's "What Consumes Context" and "Keep Context Efficient" sections.
- [Org Context Engineering](../org_docs/org_context_engineering.md) — relevance: organizational best-practices summary for managing the LLM context window and token budget, the org-context complement to this note's SDK-specific efficiency strategies.
- [Context Engineering Guide (Org Docs)](../org_docs/context_engineering_guide.md) — relevance: the org's guide to context-window management and token optimization across AI coding agents, generalizing the keep-context-small discipline this note applies to Agent SDK sessions.
- [Project: SuperAgent](../../../projects/project_superagent.md) — relevance: a production agent that delegates tasks to one or more subagents — the same fresh-context subagent offloading this note names as its top context-efficiency strategy.

*(No tool note is closely relevant: this note is about the SDK's context mechanics, not a specific tool; MCP servers appear only as a generic context-cost source, covered by the MCP term link above.)*

**Source**: https://code.claude.com/docs/en/agent-sdk/agent-loop
**Last Updated**: 2026-06-13
**Status**: Active
