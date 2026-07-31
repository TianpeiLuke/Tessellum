---
tags:
  - resource
  - documentation
  - hermes_agent
  - tools
  - context_management
keywords:
  - tool search
  - progressive disclosure
  - tool_search tool_describe tool_call
  - BM25 retrieval
  - deferred tool schemas
  - context window savings
topics:
  - Hermes Agent
  - Tool Surface
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-search
access_control_group: ["general"]
---

# Hermes Agent — Tool Search

## Overview

Tool Search is Hermes Agent's opt-in **progressive-disclosure layer** for sessions with many tools. When many MCP servers or non-core plugin tools are attached, their JSON schemas can consume a substantial fraction of the context window on *every* turn — even when only a few are relevant to what the user asked. Tool Search solves this by *deferring* those schemas: when activated, the deferrable MCP and plugin tools are removed from the model-visible tools array and replaced by **three bridge tools**, and the model loads each specific tool's schema on demand instead of carrying all of them statically.

The mechanism is built on a hard invariant — **built-in Hermes core tools never defer**. The tools that make up Hermes' core capability set (`terminal`, `read_file`, `write_file`, `patch`, `search_files`, `todo`, `memory`, `browser_*`, `web_search`, `web_extract`, `clarify`, `execute_code`, `delegate_task`, `session_search`, `send_message`, and the rest of `_HERMES_CORE_TOOLS`) are *always* loaded directly. Only MCP tools and non-core plugin tools are eligible for deferral. This is a model-BB note: it documents what the tool-search layer *is* and how the deferral/retrieval mechanics behave, not a per-step setup procedure.

## How It Works

When Tool Search activates for a turn, the model sees three new tools in place of the deferred ones:

```
tool_search(query, limit?)     — search the deferred-tool catalog
tool_describe(name)            — load the full schema for one tool
tool_call(name, arguments)     — invoke a deferred tool
```

A typical interaction walks search → describe → call:

```
Model: tool_search("create a github issue")
  → { matches: [{ name: "mcp_github_create_issue", ... }, ...] }
Model: tool_describe("mcp_github_create_issue")
  → { parameters: { type: "object", properties: { ... } } }
Model: tool_call("mcp_github_create_issue", { title: "...", body: "..." })
  → { ok: true, issue_number: 42 }
```

When the model invokes `tool_call`, Hermes **unwraps the bridge** and dispatches the underlying tool exactly as if the model had called it directly. Pre-tool-call hooks, guardrails, approval prompts, and post-tool-call hooks all run against the **real tool name** — not against `tool_call`. The activity feed in the CLI and gateway also unwraps, so you see the underlying tool, not the bridge.

## When Does It Activate?

By default Tool Search runs in `auto` mode: it activates only when the deferrable tool schemas would consume at least **10% of the active model's context window**. Below that threshold, the tools-array assembly is a pure pass-through and you pay no overhead. This decision is **re-evaluated every time the tools array is built**, so:

- A session with just a few MCP tools and a long-context model never activates Tool Search.
- A session with many MCP servers attached (15+ tools, typically) starts activating it.
- Removing MCP servers mid-session correctly returns to direct exposure on the next assembly.

## Configuration

```yaml
tools:
  tool_search:
    enabled: auto       # auto (default), on, or off
    threshold_pct: 10   # percentage of context — only used in auto mode
    search_default_limit: 5
    max_search_limit: 20
```

| Key | Default | Meaning |
| --- | --- | --- |
| `enabled` | `auto` | `auto` activates above threshold; `on` always activates if there is at least one deferrable tool; `off` disables entirely. |
| `threshold_pct` | `10` | Percentage of context length at which `auto` mode kicks in. Range 0–100. |
| `search_default_limit` | `5` | Hits returned when the model calls `tool_search` without a `limit`. |
| `max_search_limit` | `20` | Hard upper bound the model can request via `limit`. Range 1–50. |

The legacy boolean shape `tool_search: true` is equivalent to `{enabled: auto}`.

## When NOT to Use It

Tool Search trades a fixed per-turn token cost (the three bridge tool schemas, ~300 tokens) and at least one extra round trip (search → describe → call) for the savings on the deferred schemas. It is a clear win when you have many tools and use few per turn; it is pure overhead when you have few tools total. The `auto` default handles this automatically — but if you set `enabled: on` unconditionally, expect a slight per-turn cost on small toolsets.

## Trade-offs That Don't Go Away

These come from the **prompt-cache integrity invariant** and are inherent to any progressive-disclosure design, not specific to this implementation:

- **One extra round trip on cold tools.** The first time the model needs a deferred tool, it spends one or two extra model calls to find and load the schema; a portion of the static-side savings is paid back at runtime.
- **No cache benefit on deferred schemas.** A loaded `tool_describe` result enters the conversation history (so it *does* get cached on subsequent turns) but never benefits from the system-prompt cache prefix.
- **Model-quality dependence.** Tool Search assumes the model can write a reasonable search query for the tool it wants. Smaller models do this less well; the published Anthropic numbers (49% → 74% on Opus 4 with vs. without tool search) show the upside but also that ~26 points of accuracy is still retrieval failure.
- **Toolset edits invalidate cache.** Adding or removing a tool mid-session changes the bridge tools' descriptions (which include the count of deferred tools) and the catalog, so the prompt cache is invalidated — the same trade-off as any toolset edit.

## Implementation Details

- **Retrieval:** BM25 over tokenized tool name + description + parameter names. Falls back to a literal substring match on the tool name when BM25 returns no positive-score hits, which protects against zero-IDF degenerate cases (e.g. searching `"github"` against a catalog where every tool name contains "github").
- **Catalog is stateless across turns.** It rebuilds from the current tool-defs list on every assembly — no session-keyed `Map`. This avoids the class of bug where a stored catalog drifts out of sync with the live tool registry.
- **The catalog is scoped to the session's toolsets.** `tool_search`, `tool_describe`, and `tool_call` only ever see and invoke tools the session was actually granted. A subagent, kanban worker, or gateway session restricted to a subset of toolsets cannot use the bridge to discover or call a tool outside that subset — the deferred catalog is the deferrable slice of the session's own enabled/disabled toolsets, not the whole process registry.
- **No JS sandbox.** Hermes uses the simpler "structured tools" mode (search / describe / call as plain functions). The JS-sandbox "code mode" some other implementations offer is a large surface area; Hermes skips it.

The source's *See also* points at `tools/tool_search.py` (the implementation), `tests/tools/test_tool_search.py` (the regression suite), and the `openclaw-tool-search-report` PDF in the original implementation PR for the research that shaped the design.

**Source**: `inbox/hermes_agent_docs/user-guide/features/tool-search.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-search
**Last Updated**: 2026-06-19
**Status**: Active
