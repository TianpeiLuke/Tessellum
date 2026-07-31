---
tags:
  - resource
  - documentation
  - claude_code
  - mcp
  - server_management
keywords:
  - claude mcp list
  - claude mcp get
  - claude mcp remove
  - mcp panel
  - pending approval
  - dynamic tool updates
  - list_changed
  - automatic reconnection
  - exponential backoff
  - push messages channels
  - plugin-provided mcp servers
  - mcp output limits
topics:
  - Claude Code
  - MCP
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/mcp
access_control_group: ["general"]
---

# Claude Code — Managing MCP Servers

## Overview

Once an MCP server is configured, Claude Code provides commands and runtime behaviors for managing its lifecycle: `claude mcp list/get/remove` from the shell and the `/mcp` panel inside a session inspect and remove servers, surface pending-approval and rejected states, and show per-server tool counts. At runtime Claude Code refreshes capabilities when a server sends a `list_changed` notification, automatically reconnects dropped HTTP/SSE servers with exponential backoff, lets a server push messages into the session via the `claude/channel` capability, runs MCP servers bundled inside plugins, and warns when MCP tool output grows large.

This note covers the management and output-handling operations. For *adding* servers across the four transports see [Transports](cc_mcp_transports.md); for scopes and approval-prompt origins see [Installation Scopes](cc_mcp_installation_scopes.md).

## Managing your servers

Once configured, manage your MCP servers with these commands:

```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get github

# Remove a server
claude mcp remove github

# (within Claude Code) Check server status
/mcp
```

Project-scoped servers from `.mcp.json` that are awaiting your approval appear in `claude mcp list` as `⏸ Pending approval`. Run `claude` interactively to review and approve them. `claude mcp get <name>` shows pending servers as `⏸ Pending approval` and rejected servers as `✗ Rejected`.

The `/mcp` panel shows the tool count next to each connected server and flags servers that advertise the tools capability but expose no tools.

If your request needs tools from a server that is still connecting in the background, Claude waits for that server before continuing. With [tool search](cc_mcp_tool_search.md) enabled, which is the default, the wait happens inside the `ToolSearch` call. In configurations without tool search — such as Vertex AI, a custom `ANTHROPIC_BASE_URL`, or `ENABLE_TOOL_SEARCH=false` — Claude uses the `WaitForMcpServers` tool instead.

The server name `workspace` is reserved for internal use. If your configuration defines a server with that name, Claude Code skips it at load time and shows a warning asking you to rename it.

## Dynamic tool updates

Claude Code supports MCP `list_changed` notifications, allowing MCP servers to dynamically update their available tools, prompts, and resources without requiring you to disconnect and reconnect. When an MCP server sends a `list_changed` notification, Claude Code automatically refreshes the available capabilities from that server.

## Automatic reconnection

If an HTTP or SSE server disconnects mid-session, Claude Code automatically reconnects with exponential backoff: up to five attempts, starting at a one-second delay and doubling each time. The server appears as pending in `/mcp` while reconnection is in progress. After five failed attempts the server is marked as failed and you can retry manually from `/mcp`. Stdio servers are local processes and are not reconnected automatically.

The same backoff applies when an HTTP or SSE server fails its initial connection at startup. As of v2.1.121, Claude Code retries the initial connection up to three times on transient errors such as a 5xx response, a connection refused, or a timeout, then marks the server as failed if it still cannot connect. Authentication and not-found errors are not retried because they require a configuration change to resolve.

## Push messages with channels

An MCP server can also push messages directly into your session so Claude can react to external events like CI results, monitoring alerts, or chat messages. To enable this, your server declares the `claude/channel` capability and you opt it in with the `--channels` flag at startup. See [Channels](https://code.claude.com/docs/en/channels) for an officially supported channel, or [Channels reference](https://code.claude.com/docs/en/channels-reference) to build your own.

## Server timeouts and tips

Configuration tips that apply when managing running servers:

- Use the `--scope` flag to specify where the configuration is stored (`local` default, `project`, or `user` — see [Installation Scopes](cc_mcp_installation_scopes.md)).
- Set environment variables with `--env` flags (for example, `--env KEY=value`).
- Configure MCP server startup timeout with the `MCP_TIMEOUT` environment variable (for example, `MCP_TIMEOUT=10000 claude` sets a 10-second timeout).
- Set a per-server tool execution timeout by adding a `timeout` field in milliseconds to that server's `.mcp.json` entry, for example `"timeout": 600000` for ten minutes. This overrides the `MCP_TOOL_TIMEOUT` environment variable for that server only.
- Use `/mcp` to authenticate with remote servers that require OAuth 2.0 authentication (see [Authentication](cc_mcp_authentication.md)).

The per-server `timeout` is a hard wall-clock limit per tool call, and progress notifications from the server do not extend it. Values below 1000 are ignored and fall through to `MCP_TOOL_TIMEOUT`, or to its default of about 28 hours when that variable is unset. (Before v2.1.162, values below 1000 were floored to one second instead.) For HTTP and SSE servers, the per-request fetch first-byte budget has a 60-second minimum.

## Plugin-provided MCP servers

[Plugins](https://code.claude.com/docs/en/plugins) can bundle MCP servers, automatically providing tools and integrations when the plugin is enabled. Plugin MCP servers work identically to user-configured servers: plugins define them in `.mcp.json` at the plugin root or inline in `plugin.json`; when a plugin is enabled its servers start automatically and appear alongside manually configured tools; and plugin servers are managed through plugin installation rather than `/mcp` commands. At session startup, servers for enabled plugins connect automatically — if you enable or disable a plugin during a session, run `/reload-plugins` to connect or disconnect its MCP servers. Plugin configs use `${CLAUDE_PLUGIN_ROOT}` for bundled files, `${CLAUDE_PLUGIN_DATA}` for persistent state, and `${CLAUDE_PROJECT_DIR}` for the project root, and support stdio, SSE, HTTP, and WebSocket transports.

Plugin servers appear in the `/mcp` list with indicators showing they come from plugins. Their tools include both the plugin name and the server key in the callable name. The full form is `mcp__plugin_<plugin-name>_<server-name>__<tool-name>`, where any character outside `A-Z`, `a-z`, `0-9`, `_`, and `-` is replaced with `_`. For the `database-tools` server bundled in a plugin named `my-plugin`, a `query` tool is callable as:

```
mcp__plugin_my-plugin_database-tools__query
```

Use this full name when referencing the tool in [permission rules](https://code.claude.com/docs/en/permissions), a skill's `allowed-tools` list, or a [subagent's `tools` field](https://code.claude.com/docs/en/sub-agents#available-tools). See the [plugin components reference](https://code.claude.com/docs/en/plugins-reference#mcp-servers) for details on bundling MCP servers with plugins.

## MCP output limits and warnings

When MCP tools produce large outputs, Claude Code helps manage the token usage to prevent overwhelming your conversation context:

- **Output warning threshold**: Claude Code displays a warning when any MCP tool output exceeds 10,000 tokens.
- **Configurable limit**: adjust the maximum allowed MCP output tokens with the `MAX_MCP_OUTPUT_TOKENS` environment variable.
- **Default limit**: the default maximum is 25,000 tokens.
- **Scope**: the environment variable applies to tools that don't declare their own limit. Tools that set `anthropic/maxResultSizeChars` use that value instead for text content, regardless of `MAX_MCP_OUTPUT_TOKENS`. Tools that return image data are still subject to `MAX_MCP_OUTPUT_TOKENS`.

To raise the limit for tools that produce large outputs, export the variable before launching Claude:

```bash
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

This is particularly useful with MCP servers that query large datasets, generate detailed reports, or process extensive log files.

### Raise the limit for a specific tool

If you're building an MCP server, you can allow individual tools to return results larger than the default persist-to-disk threshold by setting `_meta["anthropic/maxResultSizeChars"]` in the tool's `tools/list` response entry. Claude Code raises that tool's threshold to the annotated value, up to a hard ceiling of 500,000 characters. This is useful for tools that return inherently large but necessary outputs, such as database schemas or full file trees. Without the annotation, results that exceed the default threshold are persisted to disk and replaced with a file reference in the conversation.

```json
{
  "name": "get_schema",
  "description": "Returns the full database schema",
  "_meta": {
    "anthropic/maxResultSizeChars": 200000
  }
}
```

The annotation applies independently of `MAX_MCP_OUTPUT_TOKENS` for text content, so users don't need to raise the environment variable for tools that declare it. Tools that return image data are still subject to the token limit. If you frequently hit output warnings with a server you don't control, consider raising `MAX_MCP_OUTPUT_TOKENS`, or ask the server author to add the `anthropic/maxResultSizeChars` annotation or paginate responses.

**Source**: https://code.claude.com/docs/en/mcp
**Last Updated**: 2026-06-13
**Status**: Active
