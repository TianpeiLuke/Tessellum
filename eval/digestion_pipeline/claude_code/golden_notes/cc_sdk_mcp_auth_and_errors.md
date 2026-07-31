---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - mcp
keywords:
  - mcp authentication
  - env credentials
  - http headers bearer token
  - oauth2 mcp
  - init message status
  - mcp connection failed
  - tools not being called
  - connection timeout
  - github mcp example
  - postgres mcp example
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

# SDK MCP Server Authentication and Error Handling

## Overview

Most MCP servers require authentication to reach the external service they front, and any server can fail to connect (process not installed, bad credentials, unreachable host). This note covers the operational layer of connecting an Agent SDK application to MCP servers: how to **pass credentials** (environment variables, HTTP headers, OAuth2 bearer tokens), how to **detect connection failures** by inspecting the `system`/`init` message's per-server `status`, and how to **troubleshoot** the three common failure modes — a server stuck in `failed` status, tools that Claude sees but never calls, and connection timeouts. Defining and selecting the servers themselves (the `mcpServers` option, transports, `allowedTools` naming) is covered separately; see [cc_sdk_connect_mcp_servers](cc_sdk_connect_mcp_servers.md).

## Authentication

Most MCP servers require authentication to access external services. Pass credentials through the server configuration — `env` for stdio (subprocess) servers and `headers` for HTTP/SSE (remote) servers.

### Pass credentials via environment variables

Use the `env` field to pass API keys, tokens, and other credentials to a stdio MCP server. The SDK injects them into the spawned server process's environment:

```python Python theme={null}
options = ClaudeAgentOptions(
    mcp_servers={
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": os.environ["GITHUB_TOKEN"]},
        }
    },
    allowed_tools=["mcp__github__list_issues"],
)
```

In a `.mcp.json` config file the same credential is written under the server's `env` block with the `${GITHUB_TOKEN}` syntax (e.g. `"GITHUB_TOKEN": "${GITHUB_TOKEN}"`), which expands environment variables at runtime.

### HTTP headers for remote servers

For HTTP and SSE servers, pass authentication headers directly in the server configuration (typically a bearer token):

```python Python theme={null}
options = ClaudeAgentOptions(
    mcp_servers={
        "secure-api": {
            "type": "http",
            "url": "https://api.example.com/mcp",
            "headers": {"Authorization": f"Bearer {os.environ['API_TOKEN']}"},
        }
    },
    allowed_tools=["mcp__secure-api__*"],
)
```

In `.mcp.json`, the header value uses the same `${API_TOKEN}` runtime expansion: `"Authorization": "Bearer ${API_TOKEN}"`.

### OAuth2 authentication

The [MCP specification supports OAuth 2.1](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization) for authorization. **The SDK does not handle OAuth flows automatically** — you complete the OAuth flow yourself in your application, then pass the resulting access token via headers exactly like any other bearer token:

```python Python theme={null}
# After completing OAuth flow in your app
access_token = await get_access_token_from_oauth_flow()

options = ClaudeAgentOptions(
    mcp_servers={
        "oauth-api": {
            "type": "http",
            "url": "https://api.example.com/mcp",
            "headers": {"Authorization": f"Bearer {access_token}"},
        }
    },
    allowed_tools=["mcp__oauth-api__*"],
)
```

## Examples

### List issues from a repository

This example connects to the GitHub MCP server (a stdio server) to list recent issues, with debug logging that verifies the MCP connection and logs each MCP tool call. Before running, create a GitHub personal access token with `repo` scope and export it: `export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx`.

```python Python theme={null}
async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_TOKEN": os.environ["GITHUB_TOKEN"]},
            }
        },
        allowed_tools=["mcp__github__list_issues"],
    )

    async for message in query(
        prompt="List the 3 most recent issues in anthropics/claude-code",
        options=options,
    ):
        # Verify MCP server connected successfully
        if isinstance(message, SystemMessage) and message.subtype == "init":
            print("MCP servers:", message.data.get("mcp_servers"))

        # Log when Claude calls an MCP tool
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "name") and block.name.startswith("mcp__"):
                    print("MCP tool called:", block.name)

        # Print the final result
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)
```

### Query a database

This example uses the Postgres MCP server to query a database. The connection string is passed as an argument to the server (not as an env var). The agent automatically discovers the schema, writes the SQL, and returns the results. Note that `allowedTools` is scoped to only `mcp__postgres__query` — allowing read queries but not writes:

```python Python theme={null}
connection_string = os.environ["DATABASE_URL"]

options = ClaudeAgentOptions(
    mcp_servers={
        "postgres": {
            "command": "npx",
            # Pass connection string as argument to the server
            "args": ["-y", "@modelcontextprotocol/server-postgres", connection_string],
        }
    },
    # Allow only read queries, not writes
    allowed_tools=["mcp__postgres__query"],
)

# Natural language query - Claude writes the SQL
async for message in query(
    prompt="How many users signed up last week? Break it down by day.",
    options=options,
):
    if isinstance(message, ResultMessage) and message.subtype == "success":
        print(message.result)
```

## Error handling

MCP servers can fail to connect for various reasons: the server process might not be installed, credentials might be invalid, or a remote server might be unreachable.

The SDK emits a `system` message with subtype `init` at the start of each query. This message includes the connection status for each MCP server. Check the `status` field to detect connection failures **before the agent starts working** — and watch for a `result` message with subtype `error_during_execution`:

```python Python theme={null}
async for message in query(prompt="Process data", options=options):
    if isinstance(message, SystemMessage) and message.subtype == "init":
        failed_servers = [
            s
            for s in message.data.get("mcp_servers", [])
            if s.get("status") != "connected"
        ]
        if failed_servers:
            print(f"Failed to connect: {failed_servers}")

    if (
        isinstance(message, ResultMessage)
        and message.subtype == "error_during_execution"
    ):
        print("Execution failed")
```

## Troubleshooting

### Server shows "failed" status

Inspect the `init` message and look for any server whose `status` is `"failed"`. Common causes:

- **Missing environment variables** — ensure required tokens and credentials are set. For stdio servers, check the `env` field matches what the server expects.
- **Server not installed** — for `npx` commands, verify the package exists and Node.js is in your PATH.
- **Invalid connection string** — for database servers, verify the connection string format and that the database is accessible.
- **Network issues** — for remote HTTP/SSE servers, check the URL is reachable and any firewalls allow the connection.

### Tools not being called

If Claude **sees** tools but doesn't use them, the cause is almost always missing permission: MCP tools require explicit approval before Claude can call them. Grant it by listing the tools (or a `mcp__servername__*` wildcard) in `allowedTools`.

### Connection timeouts

The MCP SDK has a **default timeout of 60 seconds** for server connections. If your server takes longer to start, the connection will fail. For servers that need more startup time, consider:

- Using a lighter-weight server if available.
- Pre-warming the server before starting your agent.
- Checking server logs for slow initialization causes.

**Source**: https://code.claude.com/docs/en/agent-sdk/mcp
**Last Updated**: 2026-06-13
**Status**: Active
