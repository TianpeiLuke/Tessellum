---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - mcp
keywords:
  - connect mcp server
  - mcpservers option
  - mcp.json config file
  - mcp__server__tool naming
  - allowedtools wildcard
  - transport types stdio http sse
  - sdk mcp server
  - discover mcp tools init message
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/mcp
access_control_group: ["general"]
---

# Connecting the Agent SDK to External MCP Servers

## Overview

The Model Context Protocol (MCP) is an open standard for connecting AI agents to external tools and data sources — querying databases, integrating with APIs like Slack and GitHub, and connecting to other services without writing custom tool implementations. This note is the SDK how-to for **connecting** to MCP servers: how to configure them (in code or in a `.mcp.json` file), how to grant the tools permission so Claude can call them, and the three transport types a server can use (stdio, HTTP/SSE, and in-process SDK servers).

MCP servers can run as local processes, connect over HTTP, or execute directly within your SDK application. (This page covers MCP configuration for the Agent SDK; to add MCP servers to the Claude Code CLI so they load in every project, see [MCP installation scopes](https://code.claude.com/docs/en/mcp#mcp-installation-scopes).)

## Quickstart

The minimal connection sets the `mcp_servers` (Python) / `mcpServers` (TypeScript) option plus an `allowedTools` (Python `allowed_tools`) entry. For example, connecting to the Claude Code documentation MCP server using HTTP transport with an `allowedTools` wildcard to permit all tools — `mcp_servers={"claude-code-docs": {"type": "http", "url": "https://code.claude.com/docs/mcp"}}` and `allowed_tools=["mcp__claude-code-docs__*"]` — lets the agent connect to the documentation server, search for information about hooks, and return the results. The same `mcpServers` / `allowedTools` shape is what every later example below builds on.

## Add an MCP server

You can configure MCP servers in code when calling `query()`, or in a `.mcp.json` file loaded via `settingSources`.

### In code

Pass MCP servers directly in the `mcpServers` option (TypeScript) / `mcp_servers` (Python). A local stdio server is given a `command` plus `args`:

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "List files in my project",
  options: {
    mcpServers: {
      filesystem: {
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"]
      }
    },
    allowedTools: ["mcp__filesystem__*"]
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

### From a config file

Create a `.mcp.json` file at your project root. The file is picked up when the `project` setting source is enabled, which it is for default `query()` options. If you set `settingSources` explicitly, include `"project"` for this file to load:

```json theme={null}
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"]
    }
  }
}
```

## Allow MCP tools

MCP tools require explicit permission before Claude can use them. Without permission, Claude will see that tools are available but won't be able to call them.

### Tool naming convention

MCP tools follow the naming pattern `mcp__<server-name>__<tool-name>`. For example, a GitHub server named `"github"` with a `list_issues` tool becomes `mcp__github__list_issues`.

### Auto-approve with allowedTools

Use `allowedTools` to auto-approve specific MCP tools so Claude can use them without a permission prompt. Wildcards (`*`) let you allow all tools from a server without listing each one individually:

```typescript hidelines={1,-1} theme={null}
const _ = {
  options: {
    mcpServers: {
      // your servers
    },
    allowedTools: [
      "mcp__github__*", // All tools from the github server
      "mcp__db__query", // Only the query tool from db server
      "mcp__slack__send_message" // Only send_message from slack server
    ]
  }
};
```

Prefer `allowedTools` over permission modes for MCP access. `permissionMode: "acceptEdits"` does not auto-approve MCP tools (only file edits and filesystem Bash commands); `permissionMode: "bypassPermissions"` does auto-approve MCP tools but also disables other safety prompts, which is broader than necessary. A wildcard in `allowedTools` grants exactly the MCP server you want and nothing more. See [Permission modes](https://code.claude.com/docs/en/agent-sdk/permissions#permission-modes) for the full comparison and evaluation order.

### Discover available tools

To see what tools an MCP server provides, check the server's documentation or connect to the server and inspect the `system` init message:

```typescript theme={null}
for await (const message of query({ prompt: "...", options })) {
  if (message.type === "system" && message.subtype === "init") {
    console.log("Available MCP tools:", message.mcp_servers);
  }
}
```

## Transport types

MCP servers communicate with your agent using different transport protocols. Check the server's documentation to see which transport it supports:

- If the docs give you a **command to run** (like `npx @modelcontextprotocol/server-github`), use **stdio**.
- If the docs give you a **URL**, use **HTTP** or **SSE**.
- If you're building your own tools in code, use an **SDK MCP server**.

### stdio servers

Local processes that communicate via stdin/stdout. Use this for MCP servers you run on the same machine. In code, the server has a `command`, `args`, and an optional `env` for credentials:

```python Python theme={null}
options = ClaudeAgentOptions(
    mcp_servers={
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": os.environ["GITHUB_TOKEN"]},
        }
    },
    allowed_tools=["mcp__github__list_issues", "mcp__github__search_issues"],
)
```

The same server can be declared in `.mcp.json`, where `"${GITHUB_TOKEN}"` expands the environment variable at runtime.

### HTTP/SSE servers

Use HTTP or SSE for cloud-hosted MCP servers and remote APIs. Pass the `url` and (optionally) auth `headers`:

```typescript TypeScript hidelines={1,-1} theme={null}
const _ = {
  options: {
    mcpServers: {
      "remote-api": {
        type: "sse",
        url: "https://api.example.com/mcp/sse",
        headers: {
          Authorization: `Bearer ${process.env.API_TOKEN}`
        }
      }
    },
    allowedTools: ["mcp__remote-api__*"]
  }
};
```

For the streamable HTTP transport, use `"type": "http"` instead. In `.mcp.json` and other JSON config files, `"streamable-http"` is accepted as an alias for `"http"`. The programmatic `mcpServers` option accepts only `"http"`.

### SDK MCP servers

Define custom tools directly in your application code instead of running a separate server process. See [Defining SDK Custom Tools](cc_sdk_custom_tool_definition.md) (the in-process `create_sdk_mcp_server` server) for implementation details.

## MCP tool search

When you have many MCP tools configured, tool definitions can consume a significant portion of your context window. Tool search solves this by withholding tool definitions from context and loading only the ones Claude needs for each turn. Tool search is enabled by default; see [SDK Tool Search](cc_sdk_tool_search.md) for configuration options, best practices, and using tool search with custom SDK tools.

## Beyond connecting

Authenticating servers (env vars, HTTP headers, OAuth2), worked GitHub/Postgres examples, detecting connection failures via the `init` message `status`, and troubleshooting (failed status, tools not being called, 60-second timeouts) are covered in [SDK MCP Authentication & Error Handling](cc_sdk_mcp_auth_and_errors.md).

**Source**: https://code.claude.com/docs/en/agent-sdk/mcp
**Last Updated**: 2026-06-13
**Status**: Active
