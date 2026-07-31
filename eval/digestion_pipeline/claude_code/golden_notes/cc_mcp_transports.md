---
tags:
  - resource
  - documentation
  - claude_code
  - mcp
  - transports
keywords:
  - mcp transports
  - claude mcp add
  - http server
  - sse deprecated
  - stdio local server
  - websocket server
  - claude mcp add-json
  - double dash separator
  - import from claude desktop
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

# Claude Code — Install MCP Servers by Transport

## Overview

An MCP server connects to Claude Code over one of **four transports**, and which one you pick determines the `claude mcp add` command (or JSON config) you use to install it. **HTTP** is the recommended option for remote cloud services; **SSE** is a deprecated remote transport kept for compatibility; **stdio** runs a server as a local subprocess on your machine; and **WebSocket** holds a persistent bidirectional connection for servers that push events to Claude unprompted. This note is the install-by-transport procedure: the four `claude mcp add` / `add-json` forms, the `--` separator that stdio servers require, adding a server from a JSON blob, and importing servers you already configured in Claude Desktop. (Lifecycle commands — `claude mcp list/get/remove`, reconnection, dynamic updates — are in [Manage MCP Servers](cc_mcp_server_management.md); where each server is stored and its scope precedence are in [MCP Installation Scopes](cc_mcp_installation_scopes.md); the OAuth and dynamic-header authentication these transports support is in [Authenticate with MCP Servers](cc_mcp_authentication.md).)

## Option 1: Add a remote HTTP server

HTTP servers are the recommended option for connecting to remote MCP servers — the most widely supported transport for cloud-based services. The basic syntax is `claude mcp add --transport http <name> <url>` (e.g. `claude mcp add --transport http notion https://mcp.notion.com/mcp`). To pass a static bearer token, append a `--header` flag:

```bash
# Example with Bearer token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

When configuring HTTP servers via JSON (in `.mcp.json`, `~/.claude.json`, or `claude mcp add-json`), the `type` field accepts **`streamable-http`** as an alias for `http`. The MCP specification uses the name `streamable-http` for this transport, so configurations copied from server documentation work without modification.

## Option 2: Add a remote SSE server

The SSE (Server-Sent Events) transport is **deprecated** — use HTTP servers instead, where available. The form parallels HTTP: `claude mcp add --transport sse <name> <url>` (e.g. `claude mcp add --transport sse asana https://mcp.asana.com/sse`), and it accepts the same `--header` flag for authentication headers such as `X-API-Key`.

## Option 3: Add a local stdio server

Stdio servers run as local processes on your machine. They are ideal for tools that need direct system access or custom scripts. Claude Code sets `CLAUDE_PROJECT_DIR` in the spawned server's environment to the project root, so your server can resolve project-relative paths without depending on the working directory — the same directory hooks receive. Read it from inside your server process (for example `process.env.CLAUDE_PROJECT_DIR` in Node or `os.environ["CLAUDE_PROJECT_DIR"]` in Python). Your server can also call the MCP `roots/list` request, which returns the directory Claude Code was launched from. Because this variable is set in the *server's* environment (not Claude Code's own), referencing it via `${VAR}` expansion in a project- or user-scoped `.mcp.json` `command` or `args` requires a default such as `${CLAUDE_PROJECT_DIR:-.}`; plugin-provided configurations substitute `${CLAUDE_PROJECT_DIR}` directly and don't need the default.

```bash
# Basic syntax
claude mcp add [options] <name> -- <command> [args...]

# Real example: Add Airtable server
claude mcp add --env AIRTABLE_API_KEY=YOUR_KEY --transport stdio airtable \
  -- npx -y airtable-mcp-server
```

### Important: separate server arguments with `--`

For stdio servers, the `--` (double dash) separates Claude's own options — such as `--transport`, `--env`, and `--scope` — from the command and arguments that run the server. Everything after `--` is passed to the server untouched:

- `claude mcp add --transport stdio myserver -- npx server` runs `npx server`.
- `claude mcp add --env KEY=value --transport stdio myserver -- python server.py --port 8080` runs `python server.py --port 8080` with `KEY=value` in the environment.

Without `--`, Claude Code would try to parse the server's flags (like `--port` above) as its own options. `--env` accepts multiple `KEY=value` pairs; if the server name comes directly after `--env`, the CLI reads the name as another pair and rejects it, so place at least one other option between `--env` and the server name (as in the examples above).

## Option 4: Add a remote WebSocket server

WebSocket servers hold a persistent bidirectional connection, which suits remote MCP servers that **push events to Claude unprompted**. Use HTTP instead when your server only responds to requests, since HTTP supports OAuth and the `claude mcp add --transport` flag, while WebSocket supports neither. Configure WebSocket servers in `.mcp.json` or with `claude mcp add-json`:

```bash
claude mcp add-json events-server \
  '{"type":"ws","url":"wss://mcp.example.com/socket","headers":{"Authorization":"Bearer YOUR_TOKEN"}}'
```

The `type: "ws"` entry accepts the same `url`, `headers`, `headersHelper`, `timeout`, and `alwaysLoad` fields as `http`. Authentication is header-only, so pass a static token in `headers` or generate one at connect time with `headersHelper` (see [Authenticate with MCP Servers](cc_mcp_authentication.md)). The `claude mcp add --transport` flag does not accept `ws`.

## Add MCP servers from JSON configuration

If you have a JSON configuration for an MCP server, add it directly with `claude mcp add-json <name> '<json>'`. The JSON blob carries the `type` field, so this single command works for any transport — HTTP, stdio, WebSocket, or HTTP with pre-configured OAuth credentials:

```bash
# Example: Adding a stdio server with JSON configuration
claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'
```

Verify the result with `claude mcp get <name>`. Make sure the JSON is properly escaped in your shell and conforms to the MCP server configuration schema; use `--scope user` to add the server to your user configuration instead of the project-specific one (see [MCP Installation Scopes](cc_mcp_installation_scopes.md)).

## Import MCP servers from Claude Desktop

If you've already configured MCP servers in Claude Desktop, import them with `claude mcp add-from-claude-desktop`. After running the command, an interactive dialog lets you select which servers to import; verify them afterward with `claude mcp list`. This feature only works on macOS and Windows Subsystem for Linux (WSL), where it reads the Claude Desktop configuration file from its standard location. Use the `--scope user` flag to add servers to your user configuration. Imported servers keep the same names as in Claude Desktop; if servers with the same names already exist, they get a numerical suffix (for example, `server_1`).

**Source**: https://code.claude.com/docs/en/mcp
**Last Updated**: 2026-06-13
**Status**: Active
