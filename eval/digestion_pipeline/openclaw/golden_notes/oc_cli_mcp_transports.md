---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - mcp
keywords:
  - openclaw mcp transport schema
  - mcp stdio sse streamable-http transport
  - mcp status doctor probe json
  - stdio env safety filter
  - mcp oauth login workflow
  - clientcert clientkey mtls ssverify
  - authstatus hastokens hascodeverifier
  - mcp.servers config shape
topics:
  - OpenClaw
  - MCP Transports
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/cli/mcp
access_control_group: ["general"]
---

# OpenClaw — MCP Registry Transport & JSON-Output Data Contract

## Overview

This note models the **data contract** for OpenClaw-managed MCP server definitions: the `--json` output shapes of `openclaw mcp status` / `doctor` / `probe`, the field schemas of the three saved-server transports (**stdio**, **SSE / HTTP**, **streamable-http**), the **stdio env safety filter** that rejects interpreter-startup variables, and the `auth: "oauth"` login workflow that the registry validates and persists. It is a contract reference, not a how-to: the operator-facing registry commands (`add`/`set`/`configure`/`login`/`logout`/…) live in the sibling `oc_cli_mcp_registry` note, and `serve` (the inbound bridge) in `oc_cli_mcp_serve`. Source: the `cli/mcp` page sections "JSON output shapes", "Stdio transport", "SSE / HTTP transport", "OAuth workflow", and "Streamable HTTP transport".

## JSON Output Shapes (`status` / `doctor` / `probe --json`)

Use `--json` for scripts and dashboards. Field sets can grow over time, so consumers should **ignore unknown keys**. Each of the three read commands emits a distinct shape.

### `status --json`

`status` classifies configured transports without connecting. Per-server fields include `name`, `configured`, `enabled`, `ok`, `transport`, a human `launch` summary, `auth`, an `authStatus` block, `requestTimeoutMs`, `connectionTimeoutMs`, a `toolFilter` (`include`/`exclude`), and `supportsParallelToolCalls`. The top level carries the config `path` and a `servers` array:

```json
{
  "path": "/home/user/.openclaw/openclaw.json",
  "servers": [
    {
      "name": "docs",
      "configured": true,
      "enabled": true,
      "ok": true,
      "transport": "streamable-http",
      "launch": "streamable-http https://mcp.example.com/mcp",
      "auth": "oauth",
      "authStatus": {
        "hasTokens": true,
        "hasClientInformation": true,
        "hasCodeVerifier": false,
        "hasDiscoveryState": true,
        "hasLastAuthorizationUrl": false
      },
      "requestTimeoutMs": 20000,
      "connectionTimeoutMs": 5000,
      "toolFilter": {
        "include": ["search", "read_*"],
        "exclude": []
      },
      "supportsParallelToolCalls": true
    }
  ]
}
```

The `authStatus` block reports OAuth credential state without connecting: `hasTokens`, `hasClientInformation`, `hasCodeVerifier`, `hasDiscoveryState`, and `hasLastAuthorizationUrl`.

### `doctor --json`

`doctor` performs static checks without connecting (add `--probe` for a live connection proof). The shape is a top-level `ok` plus `path` and a `servers` array; each server carries `name`, `ok`, and an `issues` array of `{ level, message }`. `doctor --json` exits nonzero when any enabled checked server has an `error`; warnings are reported but do not make the command fail by themselves:

```json
{
  "ok": false,
  "path": "/home/user/.openclaw/openclaw.json",
  "servers": [
    {
      "name": "docs",
      "ok": false,
      "issues": [
        {
          "level": "error",
          "message": "OAuth credentials are not authorized; run openclaw mcp login docs"
        }
      ]
    }
  ]
}
```

### `probe --json`

`probe` opens a live MCP client session — use it for reachability and capability proof, not for static config audits. The shape carries `path`, `generatedAt`, a `servers` map (each with `launch`, `tools` count, `resources`/`prompts` booleans, and a `listChanged` block for `tools`/`resources`/`prompts`), a flat `tools` name array, and a `diagnostics` array:

```json
{
  "path": "/home/user/.openclaw/openclaw.json",
  "generatedAt": "2026-05-31T09:00:00.000Z",
  "servers": {
    "docs": {
      "launch": "streamable-http https://mcp.example.com/mcp",
      "tools": 2,
      "resources": true,
      "prompts": false,
      "listChanged": {
        "tools": true,
        "resources": false,
        "prompts": false
      }
    }
  },
  "tools": ["docs__read_page", "docs__search"],
  "diagnostics": []
}
```

The saved registry itself lives under `mcp.servers.<name>` in OpenClaw config; a representative config object spanning a stdio server (`context7`) and an OAuth streamable-http server (`docs` with `timeout`/`connectTimeout`/`supportsParallelToolCalls`/`sslVerify`/`clientCert`/`clientKey`/`toolFilter`) is the canonical shape validated against these transport schemas.

## Stdio Transport (+ Env Safety Filter)

Stdio launches a local child process and communicates over stdin/stdout. Its fields:

| Field | Description |
| --- | --- |
| `command` | Executable to spawn (required) |
| `args` | Array of command-line arguments |
| `env` | Extra environment variables |
| `cwd` / `workingDirectory` | Working directory for the process |

**Stdio env safety filter.** OpenClaw rejects interpreter-startup env keys that can alter how a stdio MCP server starts up before the first RPC, even if they appear in a server's `env` block. Blocked keys include `BASHOPTS`, `FPATH`, `KSH_ENV`, `NODE_OPTIONS`, `NODE_REDIRECT_WARNINGS`, `NODE_REPL_EXTERNAL_MODULE`, `NODE_REPL_HISTORY`, `NODE_V8_COVERAGE`, `PYTHONSTARTUP`, `PYTHONPATH`, `PERL5OPT`, `RUBYOPT`, `SHELLOPTS`, `PS4`, `TCLLIBPATH`, and similar runtime-control variables. Startup rejects these with a configuration error so they cannot inject an implicit prelude, swap the interpreter, enable a debugger, or redirect runtime output against the stdio process. Ordinary credential, proxy, and server-specific env vars (`GITHUB_TOKEN`, `HTTP_PROXY`, custom `*_API_KEY`, etc.) are unaffected. If a server genuinely needs one of the blocked variables, set it on the gateway host process instead of under the stdio server's `env`.

## SSE / HTTP Transport

SSE / HTTP connects to a remote MCP server over HTTP Server-Sent Events. Its fields:

| Field | Description |
| --- | --- |
| `url` | HTTP or HTTPS URL of the remote server (required) |
| `headers` | Optional key-value map of HTTP headers (for example auth tokens) |
| `connectionTimeoutMs` | Per-server connection timeout in ms (optional) |
| `connectTimeout` | Per-server connection timeout in seconds (optional) |
| `timeout` / `requestTimeoutMs` | Per-server MCP request timeout in seconds or ms |
| `auth: "oauth"` | Use MCP OAuth token storage and `openclaw mcp login` |
| `sslVerify` | Set false only for explicitly trusted private HTTPS endpoints |
| `clientCert` / `clientKey` | mTLS client certificate and key paths |
| `supportsParallelToolCalls` | Hint that concurrent calls are safe for this server |

Sensitive values in `url` (userinfo) and `headers` are redacted in logs and status output. `openclaw mcp doctor` warns when sensitive-looking `headers` or `env` entries contain literal values, so operators can move those values out of committed config. A minimal SSE/HTTP server with an OAuth + static `Authorization` header takes this shape:

```json
{
  "mcp": {
    "servers": {
      "remote-tools": {
        "url": "https://mcp.example.com",
        "auth": "oauth",
        "timeout": 20,
        "headers": {
          "Authorization": "Bearer <token>"
        }
      }
    }
  }
}
```

## OAuth Workflow

OAuth is for HTTP MCP servers that advertise the MCP OAuth flow. Static `Authorization` headers are **ignored** for a server while `auth: "oauth"` is enabled. The flow is five steps. (1) Save the server with `auth: "oauth"` and any optional OAuth metadata (e.g. `openclaw mcp set docs '{"url":"https://mcp.example.com/mcp","transport":"streamable-http","auth":"oauth","oauth":{"scope":"docs.read"}}'`). (2) Run `openclaw mcp login docs`, which prints the authorization URL and stores temporary OAuth verifier state under the OpenClaw state directory. (3) After approving in the browser, finish with the returned code: `openclaw mcp login docs --code abc123`. (4) Confirm tokens are present with `openclaw mcp status --verbose` or `openclaw mcp doctor docs --probe`. (5) `openclaw mcp logout docs` removes stored OAuth credentials but keeps the saved server definition. If the provider rotates tokens or authorization state gets stuck, run `openclaw mcp logout <name>` then repeat `login`. `logout` can clear credentials for a saved HTTP server even after `auth: "oauth"` has been removed from config, as long as the server name and URL still identify the credential store entry. The persisted result surfaces in the `status --json` `authStatus` block (`hasTokens`, `hasCodeVerifier`, `hasDiscoveryState`, etc.).

## Streamable HTTP Transport

`streamable-http` is an additional transport option alongside `sse` and `stdio`; it uses HTTP streaming for bidirectional communication with remote MCP servers. Its fields:

| Field | Description |
| --- | --- |
| `url` | HTTP or HTTPS URL of the remote server (required) |
| `transport` | Set to `"streamable-http"` to select this transport; when omitted, OpenClaw uses `sse` |
| `headers` | Optional key-value map of HTTP headers (for example auth tokens) |
| `connectionTimeoutMs` | Per-server connection timeout in ms (optional) |
| `connectTimeout` | Per-server connection timeout in seconds (optional) |
| `timeout` / `requestTimeoutMs` | Per-server MCP request timeout in seconds or ms |
| `auth: "oauth"` | Use MCP OAuth token storage and `openclaw mcp login` |
| `sslVerify` | Set false only for explicitly trusted private HTTPS endpoints |
| `clientCert` / `clientKey` | mTLS client certificate and key paths |
| `supportsParallelToolCalls` | Hint that concurrent calls are safe for this server |

OpenClaw config uses `transport: "streamable-http"` as the canonical spelling. CLI-native MCP `type: "http"` values are accepted when saved through `openclaw mcp set` and repaired by `openclaw doctor --fix` in existing config, but `transport` is what embedded OpenClaw consumes directly. A streamable-http server with `connectTimeout`/`timeout` and a static header takes this shape:

```json
{
  "mcp": {
    "servers": {
      "streaming-tools": {
        "url": "https://mcp.example.com/stream",
        "transport": "streamable-http",
        "connectTimeout": 10,
        "timeout": 30,
        "headers": {
          "Authorization": "Bearer <token>"
        }
      }
    }
  }
}
```

Registry commands do not start the channel bridge. Only `probe` and `doctor --probe` open a live MCP client session to prove the target server is reachable.

**Source**: OpenClaw documentation — `cli/mcp` (mirror `inbox/openclaw_docs/cli/mcp.md`, sections: JSON output shapes / Stdio transport / SSE / HTTP transport / OAuth workflow / Streamable HTTP transport)
**Last Updated**: 2026-06-22
**Status**: Active
