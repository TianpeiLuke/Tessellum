---
tags:
  - resource
  - documentation
  - claude_code
  - mcp
  - tool_search
keywords:
  - mcp tool search
  - deferred tool loading
  - enable_tool_search
  - alwaysload exemption
  - tool_reference blocks
  - mcp resources
  - mcp prompts as commands
  - mcp elicitation
  - context window budget
topics:
  - Claude Code
  - MCP
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/mcp
access_control_group: ["general"]
---

# Claude Code — Scaling MCP with Tool Search, Resources, Prompts, and Elicitation

## Overview

As you connect more MCP servers, every tool definition they expose competes for room in the model's context window. **MCP Tool Search** is the concept that keeps that cost low: it defers tool definitions until Claude needs them, so only tool names and server instructions load at session start and adding more servers has minimal impact on the context window. Claude Code imposes no fixed per-server tool cap — the practical limit is your context budget. This note covers Tool Search (how deferral works, how to configure it with `ENABLE_TOOL_SEARCH`, and how to exempt a server with `alwaysLoad`) plus three other ways an MCP server surfaces capabilities into a session: **resources** referenced with `@` mentions, **prompts** that become `/mcp__server__prompt` slash commands, and **elicitation** requests where a server asks you for structured input mid-task.

## Scale with MCP Tool Search

Tool Search keeps MCP context usage low by deferring tool definitions until Claude needs them. Only tool names and server instructions load at session start, so adding more MCP servers has minimal impact on your context window. Claude Code does not impose a fixed per-server tool cap; the practical limit is your context window budget.

### How it works

Tool search is enabled by default. MCP tools are deferred rather than loaded into context upfront, and Claude uses a search tool to discover relevant ones when a task needs them. Only the tools Claude actually uses enter context. From your perspective, MCP tools work exactly as before.

If you prefer threshold-based loading, set `ENABLE_TOOL_SEARCH=auto` to load schemas upfront when they fit within 10% of the context window and defer only the overflow.

### For MCP server authors

With Tool Search enabled, the server instructions field becomes more useful: it helps Claude understand when to search for your tools, similar to how skills work. Add clear, descriptive server instructions that explain what category of tasks your tools handle, when Claude should search for them, and the key capabilities your server provides. Claude Code **truncates tool descriptions and server instructions at 2KB each**, so keep them concise and put critical details near the start to avoid truncation.

### Configure tool search

Tool search is enabled by default (MCP tools deferred and discovered on demand). Claude Code disables it by default on Vertex AI, and also when `ANTHROPIC_BASE_URL` points to a non-first-party host, since most proxies do not forward `tool_reference` blocks. Set `ENABLE_TOOL_SEARCH` explicitly to override either fallback.

Tool search **requires a model that supports `tool_reference` blocks**. Haiku models do not support it. On Vertex AI, tool search is supported for Claude Sonnet 4.5 and later and Claude Opus 4.5 and later.

Control behavior with the `ENABLE_TOOL_SEARCH` environment variable:

| Value    | Behavior                                                                                                                                                                                                                          |
| :------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| (unset)  | All MCP tools deferred and loaded on demand. Falls back to loading upfront on Vertex AI or when `ANTHROPIC_BASE_URL` is a non-first-party host                                                                                    |
| `true`   | All MCP tools deferred. Claude Code sends the beta header even on Vertex AI and through proxies. Requests fail on Vertex AI models earlier than Sonnet 4.5 or Opus 4.5, or on proxies that do not support `tool_reference` blocks |
| `auto`   | Threshold mode: tools load upfront if they fit within 10% of the context window, deferred otherwise                                                                                                                               |
| `auto:N` | Threshold mode with a custom percentage, where `N` is 0-100. For example, `auto:5` for 5%                                                                                                                                         |
| `false`  | All MCP tools loaded upfront, no deferral                                                                                                                                                                                         |

```bash theme={null}
# Use a custom 5% threshold
ENABLE_TOOL_SEARCH=auto:5 claude

# Disable tool search entirely
ENABLE_TOOL_SEARCH=false claude
```

You can also set the value in your settings.json `env` field, or disable the `ToolSearch` tool specifically via `permissions.deny: ["ToolSearch"]`. (When a request needs tools from a server still connecting in the background, the wait happens inside the `ToolSearch` call when tool search is enabled; configurations without it use the `WaitForMcpServers` tool instead.)

### Exempt a server from deferral

If a server's tools should always be visible to Claude without a search step, set `alwaysLoad` to `true` in that server's configuration. Every tool from that server then loads into context at session start regardless of the `ENABLE_TOOL_SEARCH` setting. Use this only for a small number of tools that Claude needs on every turn, since each upfront tool consumes context that would otherwise be available for your conversation.

```json theme={null}
{
  "mcpServers": {
    "core-tools": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "alwaysLoad": true
    }
  }
}
```

The `alwaysLoad` field is available on all server types and requires Claude Code v2.1.121 or later. An MCP server can also mark individual tools as always-loaded by including `"anthropic/alwaysLoad": true` in the tool's `_meta` object, which has the same effect for that tool only. Setting `alwaysLoad: true` also blocks startup until the server connects, capped at the standard 5-second connect timeout (this applies even though MCP startup is otherwise non-blocking by default, since the tools must be present when the first prompt is built). Other servers continue to connect in the background.

## Use MCP resources

MCP servers can expose resources that you can reference using `@` mentions, similar to how you reference files. Type `@` in your prompt to see available resources from all connected MCP servers; resources appear alongside files in the autocomplete menu. Reference a specific resource with the format `@server:protocol://resource/path`:

```text theme={null}
Can you analyze @github:issue://123 and suggest a fix?
```

You can reference multiple resources in a single prompt (for example, `Compare @postgres:schema://users with @docs:file://database/user-model`). Resources are automatically fetched and included as attachments when referenced, resource paths are fuzzy-searchable in the `@` mention autocomplete, and Claude Code automatically provides tools to list and read MCP resources when servers support them. Resources can contain any type of content the MCP server provides (text, JSON, structured data, etc.).

## Use MCP prompts as commands

MCP servers can expose prompts that become available as commands in Claude Code. Type `/` to see all available commands, including those from MCP servers — MCP prompts appear with the format `/mcp__servername__promptname`. Execute a prompt without arguments (for example, `/mcp__github__list_prs`), or pass arguments space-separated after the command:

```text theme={null}
/mcp__github__pr_review 456
```

MCP prompts are dynamically discovered from connected servers, arguments are parsed based on the prompt's defined parameters, prompt results are injected directly into the conversation, and server and prompt names are normalized (spaces become underscores).

## Respond to MCP elicitation requests

MCP servers can request structured input from you mid-task using **elicitation**. When a server needs information it can't get on its own, Claude Code displays an interactive dialog and passes your response back to the server. No configuration is required on your side — elicitation dialogs appear automatically when a server requests them. Servers can request input in two ways:

- **Form mode**: Claude Code shows a dialog with form fields defined by the server (for example, a username and password prompt). Fill in the fields and submit.
- **URL mode**: Claude Code opens a browser URL for authentication or approval. Complete the flow in the browser, then confirm in the CLI.

To auto-respond to elicitation requests without showing a dialog, use the [`Elicitation` hook](https://code.claude.com/docs/en/hooks). If you're building an MCP server that uses elicitation, see the [MCP elicitation specification](https://modelcontextprotocol.io/docs/learn/client-concepts#elicitation) for protocol details and schema examples.

## Related Notes

- [Context Window](../../term_dictionary/term_context_window.md) — finite token memory an LLM processes per interaction; relevance: Tool Search exists to keep MCP context usage low by deferring tool definitions until needed, so the context-window budget is the constraint this whole note optimizes against.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — open AI-tool integration protocol; relevance: the note covers MCP-specific features (deferred tools, @-mention resources, `/mcp__*` prompts, elicitation), all surfaced through connected MCP servers.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — LLM tool-invocation via structured calls; relevance: Tool Search changes when tool definitions load into context (deferred vs upfront), directly shaping the tool-use mechanism this term defines.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — supplying the right info/tools at the right time; relevance: deferring tool schemas and loading only what Claude needs is a textbook context-engineering optimization, the discipline this term names.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — the typed declarative record (name/description/schema) every callable tool registers under; relevance: Tool Search defers exactly these tool descriptors and truncates descriptions/server-instructions at 2KB, so the descriptor is the unit being searched and loaded.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic CLI tool; relevance: the note documents Claude Code's `ENABLE_TOOL_SEARCH` settings, `ToolSearch`/`WaitForMcpServers` tools, and `alwaysLoad` exemption.
- [Structured Output](../../term_dictionary/term_structured_output.md) — constraining LLM generation to a predefined schema; relevance: MCP elicitation requests (covered here) show server-defined form fields whose schema constrains the user's structured response, mirroring the schema-constrained I/O this term covers.
- [MCP Quickstart](cc_mcp_quickstart.md) — end-to-end connect/verify/use walkthrough for one MCP server; the hands-on counterpart to this scaling/usage concept note.
- [MCP Server Management](cc_mcp_server_management.md) — list/get/remove, dynamic updates, output limits, and the `/mcp` panel that complements the resource/prompt/tool-search surfaces here.

**Source**: https://code.claude.com/docs/en/mcp
**Last Updated**: 2026-06-13
**Status**: Active
