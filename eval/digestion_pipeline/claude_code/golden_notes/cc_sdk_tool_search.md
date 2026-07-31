---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - tool_search
keywords:
  - tool search
  - enable_tool_search
  - scale to many tools
  - context efficiency
  - tool selection accuracy
  - discover tools on demand
  - tool catalog
  - tool discovery optimization
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/tool-search
access_control_group: ["general"]
---

# Agent SDK — Tool Search

## Overview

**Tool search** lets an Agent SDK application scale to hundreds or thousands of tools by **discovering and loading only what is needed, on demand**, instead of loading every tool definition into the context window upfront. The agent receives a summary of available tools, searches the catalog when a task needs a capability it has not already loaded, and the 3-5 most relevant tools are loaded into context. It is **enabled by default** and applies to all registered tools — whether they come from remote MCP servers or custom SDK MCP servers.

Tool search solves two challenges that appear as tool libraries scale: **context efficiency** (tool definitions can consume large portions of the context window — 50 tools can use 10-20K tokens — leaving less room for actual work) and **tool selection accuracy** (which degrades with more than 30-50 tools loaded at once).

## How tool search works

When tool search is active, tool definitions are **withheld from the context window**. The agent receives a summary of available tools and searches for relevant ones when the task requires a capability not already loaded. The 3-5 most relevant tools are loaded into context, where they **stay available for subsequent turns**. If the conversation is long enough that the SDK **compacts** earlier messages to free space, previously discovered tools may be removed, and the agent searches again as needed.

Tool search adds **one extra round-trip** the first time Claude discovers a tool (the search step), but for large tool sets this is offset by smaller context on every turn. With fewer than ~10 tools, loading everything upfront is typically faster.

For details on the underlying API mechanism, see [Tool search in the API](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool).

> **Note:** Tool search is supported on every Claude model except Haiku.

## Configure tool search

Tool search is on by default. It is **disabled by default on Vertex AI** (where it is supported for Claude Sonnet 4.5 and later and Claude Opus 4.5 and later) and **disabled when `ANTHROPIC_BASE_URL` points to a non-first-party host**, since most proxies do not forward `tool_reference` blocks. Override either default with the `ENABLE_TOOL_SEARCH` environment variable:

| Value | Behavior |
|:------|:---------|
| (unset) | Tool search is on. Tool definitions are deferred and discovered on demand. Falls back to loading upfront on Vertex AI or a non-first-party `ANTHROPIC_BASE_URL`. |
| `true` | Tool search is always on. The SDK sends the beta header even on Vertex AI and through proxies. Requests fail on Vertex AI models earlier than Sonnet 4.5 or Opus 4.5, or on proxies that do not support `tool_reference` blocks. |
| `auto` | Checks the combined token count of all tool definitions against the model's context window. If they exceed 10%, tool search activates. If they're under 10%, all tools are loaded into context normally. |
| `auto:N` | Same as `auto` with a custom percentage. `auto:5` activates when tool definitions exceed 5% of the context window. Lower values activate sooner. |
| `false` | Tool search is off. All tool definitions are loaded into context on every turn. |

When using `auto`, the threshold is based on the **combined size of all tool definitions across all servers**. Set the value in the `env` option on `query()`. This example connects to a remote MCP server that exposes many tools, pre-approves all of them with a wildcard, and uses `auto:5` so tool search activates when their definitions exceed 5% of the context window:

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "enterprise-tools": {
                "type": "http",
                "url": "https://tools.example.com/mcp",
            }
        },
        allowed_tools=[
            "mcp__enterprise-tools__*"
        ],  # Wildcard pre-approves all tools from this server
        env={
            "ENABLE_TOOL_SEARCH": "auto:5"  # Activate tool search when tools exceed 5% of context
        },
    )

    async for message in query(
        prompt="Find and run the appropriate database query",
        options=options,
    ):
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
```

Setting `ENABLE_TOOL_SEARCH` to `"false"` disables tool search and loads all tool definitions into context on every turn. This removes the search round-trip, which can be faster when the tool set is small (fewer than ~10 tools) and the definitions fit comfortably in the context window.

## Optimize tool discovery

The search mechanism matches queries against **tool names and descriptions**. Names like `search_slack_messages` surface for a wider range of requests than `query_slack`. Descriptions with specific keywords ("Search Slack messages by keyword, channel, or date range") match more queries than generic ones ("Query Slack").

You can also add a **system prompt section** listing available tool categories, which gives the agent context about what kinds of tools are available to search for:

```text theme={null}
You can search for tools to interact with Slack, GitHub, and Jira.
```

## Limits

- **Maximum tools:** 10,000 tools in your catalog
- **Search results:** Returns 3-5 most relevant tools per search
- **Model support:** every Claude model except Haiku

## MCP tool search (folded from mcp.md)

The `mcp.md` page surfaces tool search as a short pointer in the MCP-server context: when you have many MCP tools configured, tool definitions can consume a significant portion of your context window, and tool search solves this by withholding tool definitions from context and loading only the ones Claude needs for each turn. It is enabled by default; this note (mirroring `/en/agent-sdk/tool-search`) is the single place those configuration options and details live, and it covers using tool search with custom SDK tools as well as remote MCP servers.

**Source**: https://code.claude.com/docs/en/agent-sdk/tool-search
**Last Updated**: 2026-06-13
**Status**: Active
