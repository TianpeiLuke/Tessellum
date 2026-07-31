---
tags:
  - resource
  - documentation
  - claude_code
  - mcp
  - authentication
keywords:
  - mcp oauth authentication
  - remote mcp server sign-in
  - callback port
  - pre-configured oauth credentials
  - oauth scopes restriction
  - dynamic headers headersHelper
  - claude mcp serve
  - claude.ai connectors
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

# Claude Code — Authenticate with Remote MCP Servers

## Overview

Many cloud-based MCP servers require authentication, and Claude Code supports OAuth 2.0 for secure connections. Claude Code marks a remote server as needing authentication when the server responds with `401 Unauthorized` or `403 Forbidden`; either status flags the server in `/mcp` so you can complete the OAuth flow, and a custom server returning a `WWW-Authenticate` header pointing to its authorization server gets the same automatic discovery as any other remote server. If you configured `headers.Authorization` for the server and it rejects that header, Claude Code reports the connection as failed instead of falling back to OAuth.

This note covers the remote-server authentication procedures (the interactive OAuth flow, fixed callback ports, pre-configured credentials, metadata-discovery overrides, scope pinning, and dynamic headers for non-OAuth schemes), plus using MCP servers from a Claude.ai account and running Claude Code itself as an MCP server. For where these servers are configured, see [cc_mcp_transports](cc_mcp_transports.md) and [cc_mcp_installation_scopes](cc_mcp_installation_scopes.md).

## Authenticate with the interactive OAuth flow

The basic flow has two steps. First add the server that requires authentication, then complete sign-in from inside Claude Code:

```bash theme={null}
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

Then run the `/mcp` command within Claude Code and follow the steps in your browser to log in. Authentication tokens are stored securely and refreshed automatically; use "Clear authentication" in the `/mcp` menu to revoke access. If your browser doesn't open automatically, copy the provided URL and open it manually. If the browser redirect fails with a connection error after authenticating, paste the full callback URL from your browser's address bar into the URL prompt that appears in Claude Code. OAuth authentication works with HTTP servers.

## Use a fixed OAuth callback port

Some MCP servers require a specific redirect URI registered in advance. By default Claude Code picks a random available port for the OAuth callback; use `--callback-port` to fix the port so it matches a pre-registered redirect URI of the form `http://localhost:PORT/callback`. You can use `--callback-port` on its own (with dynamic client registration) or together with `--client-id` (with pre-configured credentials):

```bash theme={null}
# Fixed callback port with dynamic client registration
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

## Use pre-configured OAuth credentials

Some MCP servers don't support automatic OAuth setup via Dynamic Client Registration. If you see an error like "Incompatible auth server: does not support dynamic client registration," the server requires pre-configured credentials. Claude Code also supports servers that use a Client ID Metadata Document (CIMD) instead of Dynamic Client Registration and discovers these automatically; if automatic discovery fails, register an OAuth app through the server's developer portal first, then provide the credentials when adding the server. Note your client ID and client secret, and if the server requires a redirect URI, choose a port, register a redirect URI in the format `http://localhost:PORT/callback`, and use that same port with `--callback-port`.

You can supply credentials with `claude mcp add` (`--client-id` passes the app's client ID; `--client-secret` prompts for the secret with masked input), with `claude mcp add-json` (include an `oauth` object and pass `--client-secret` as a separate flag), or in CI by setting `MCP_CLIENT_SECRET` to skip the interactive prompt. The `claude mcp add` form is:

```bash theme={null}
claude mcp add --transport http \
  --client-id your-client-id --client-secret --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

After adding, run `/mcp` and follow the browser login flow. The client secret is stored securely in your system keychain (macOS) or a credentials file, not in your config. If the server uses a public OAuth client with no secret, use only `--client-id` without `--client-secret`. These flags only apply to HTTP and SSE transports and have no effect on stdio servers; use `claude mcp get <name>` to verify that OAuth credentials are configured for a server.

## Override OAuth metadata discovery

Point Claude Code at a specific OAuth authorization-server metadata URL to bypass the default discovery chain. By default, Claude Code first checks RFC 9728 Protected Resource Metadata at `/.well-known/oauth-protected-resource`, then falls back to RFC 8414 authorization-server metadata at `/.well-known/oauth-authorization-server`. Set `authServerMetadataUrl` in the `oauth` object when the MCP server's standard endpoints error, or when you want to route discovery through an internal proxy:

```json theme={null}
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

The URL must use `https://`, and `authServerMetadataUrl` requires Claude Code v2.1.64 or later. The metadata URL's `scopes_supported` overrides the scopes the upstream server advertises.

## Restrict OAuth scopes

Set `oauth.scopes` to pin the scopes Claude Code requests during the authorization flow. This is the supported way to restrict an MCP server to a security-team-approved subset when the upstream authorization server advertises more scopes than you want to grant. The value is a single space-separated string, matching the `scope` parameter format in RFC 6749 §3.3 (for example, `"channels:read chat:write search:read"` for a Slack server). `oauth.scopes` takes precedence over both `authServerMetadataUrl` and the scopes the server discovers at `/.well-known`; leave it unset to let the MCP server determine the requested scope set.

If the authorization server advertises `offline_access` in `scopes_supported`, Claude Code appends it to the pinned scopes so the access token can be refreshed without a new browser sign-in. If the server later returns a 403 `insufficient_scope` for a tool call, Claude Code re-authenticates with the same pinned scopes; widen `oauth.scopes` when a tool you need requires a scope outside the pin.

## Use dynamic headers for custom authentication

If your MCP server uses an authentication scheme other than OAuth (such as Kerberos, short-lived tokens, or an internal SSO), use `headersHelper` to generate request headers at connection time. Claude Code runs the command and merges its output into the connection headers; the command can be a script path or inline:

```json theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "/opt/bin/get-mcp-auth-headers.sh"
    }
  }
}
```

The command must write a JSON object of string key-value pairs to stdout, runs in a shell with a 10-second timeout, and its dynamic headers override any static `headers` with the same name. The helper runs fresh on each connection (at session start and on reconnect) with no caching, so your script is responsible for any token reuse. Claude Code sets `CLAUDE_CODE_MCP_SERVER_NAME` and `CLAUDE_CODE_MCP_SERVER_URL` in the helper's environment so one script can serve multiple servers. Because `headersHelper` executes arbitrary shell commands, when defined at project or local scope it only runs after you accept the workspace trust dialog.

## Use MCP servers from Claude.ai

If you've logged into Claude Code with a Claude.ai account, MCP servers you've added in Claude.ai (at `claude.ai/customize/connectors`; on Team and Enterprise plans only admins can add servers) are automatically available in Claude Code. Complete any required authentication in Claude.ai, then run `/mcp` — Claude.ai servers appear in the list with indicators showing they come from Claude.ai. From v2.1.161, connectors you have never signed in to are collapsed behind a `Show unused connectors` row at the end of the claude.ai section.

Claude.ai connectors are fetched only when your active authentication method is your Claude.ai subscription; they are not loaded when `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `apiKeyHelper`, or a third-party provider such as Bedrock or Vertex is active, even if you previously ran `/login`. A server you've added in Claude Code takes precedence over a claude.ai connector pointing at the same URL. Some Anthropic-hosted connectors (Microsoft 365, Gmail, Google Calendar) do not support local OAuth from Claude Code and must be connected at Settings → Connectors on claude.ai. To disable claude.ai MCP servers in Claude Code, set `ENABLE_CLAUDEAI_MCP_SERVERS=false`.

## Use Claude Code as an MCP server

You can use Claude Code itself as an MCP server that other applications can connect to by starting it as a stdio server:

```bash theme={null}
# Start Claude as a stdio MCP server
claude mcp serve
```

To use this in Claude Desktop, add a `claude-code` entry to `claude_desktop_config.json` with `"command": "claude"` and `"args": ["mcp", "serve"]`. The `command` field must reference the Claude Code executable: if `claude` is not in your PATH, find it with `which claude` and use the full path, otherwise you'll encounter errors like `spawn claude ENOENT`. The server provides access to Claude's tools like View, Edit, and LS; because it only exposes Claude Code's tools to your MCP client, your own client is responsible for implementing user confirmation for individual tool calls.

**Source**: https://code.claude.com/docs/en/mcp
**Last Updated**: 2026-06-13
**Status**: Active
