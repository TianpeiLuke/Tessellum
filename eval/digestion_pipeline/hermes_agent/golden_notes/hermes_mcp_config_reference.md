---
tags:
  - resource
  - documentation
  - hermes_agent
  - mcp
  - configuration
keywords:
  - mcp_servers config schema
  - mcp tool include exclude filtering
  - mcp utility-tool policy resources prompts
  - mcp tool name sanitization
  - mcp mtls client certificate
  - mcp oauth 2.1 pkce
topics:
  - Hermes Agent
  - MCP
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference
access_control_group: ["general"]
---

# Hermes Agent — MCP Config Reference

## Overview

The MCP Config Reference is the compact schema companion for the `mcp_servers` block of Hermes Agent's `config.yaml` — it enumerates every key you can set on a Model Context Protocol (MCP) server entry, the tool include/exclude filtering rules, the utility-tool (resources/prompts) policy, the worked example configs, and the OAuth 2.1 / mTLS authentication knobs. It is a look-up reference, not conceptual prose: the *what is MCP* and *how to use MCP with Hermes* guidance lives in the feature pages (see [term_mcp](../../term_dictionary/term_mcp.md) and SP09's MCP docs). Each Hermes MCP server is either a **stdio** server (launched via `command`/`args`/`env`) or an **HTTP** server (reached via `url`/`headers`), and each exposes server-native tools plus optional utility wrappers. This note documents the declarative config that decides which of those tools get registered, under what transport security, and how their names are sanitized into LLM-callable identifiers.

## Root config shape

Every server lives under the top-level `mcp_servers` mapping, keyed by a server name. A server is configured as either stdio (`command`) or HTTP (`url`), with shared lifecycle and `tools` policy keys:

```yaml
mcp_servers:
  <server_name>:
    command: "..."      # stdio servers
    args: []
    env: {}

    # OR
    url: "..."          # HTTP servers
    headers: {}

    # Optional HTTP/SSE TLS settings:
    ssl_verify: true                # bool or path to a CA bundle (PEM)
    client_cert: "/path/to/cert.pem"  # mTLS client certificate (see below)
    # client_key: "/path/to/key.pem"  # optional, when key lives in a separate file

    enabled: true
    timeout: 120
    connect_timeout: 60
    supports_parallel_tool_calls: false
    tools:
      include: []
      exclude: []
      resources: true
      prompts: true
```

## Server keys

| Key | Type | Applies to | Meaning |
|---|---|---|---|
| `command` | string | stdio | Executable to launch |
| `args` | list | stdio | Arguments for the subprocess |
| `env` | mapping | stdio | Environment passed to the subprocess |
| `url` | string | HTTP | Remote MCP endpoint |
| `headers` | mapping | HTTP | Headers for remote server requests |
| `ssl_verify` | bool or string | HTTP | TLS verification. `true` (default) uses system CAs, `false` disables verification (insecure), or a string path to a custom CA bundle (PEM) |
| `client_cert` | string or list | HTTP | mTLS client certificate. String = path to a PEM file containing cert + key. List `[cert, key]` = separate files. List `[cert, key, password]` = encrypted key |
| `client_key` | string | HTTP | Path to the client private key, when `client_cert` is a string and the key is in a separate file |
| `enabled` | bool | both | Skip the server entirely when false |
| `timeout` | number | both | Tool call timeout in seconds (default: `300`) |
| `connect_timeout` | number | both | Initial connection timeout in seconds (default: `60`) |
| `supports_parallel_tool_calls` | bool | both | Allow tools from this server to run concurrently |
| `tools` | mapping | both | Filtering and utility-tool policy |
| `auth` | string | HTTP | Authentication method. Set to `oauth` to enable OAuth 2.1 with PKCE |
| `sampling` | mapping | both | Server-initiated LLM request policy (see MCP guide) |

## `tools` policy keys and filtering semantics

The `tools` mapping decides which server-native MCP tools are registered. `include` (string or list) whitelists tools; `exclude` (string or list) blacklists them; `resources` and `prompts` (bool-like) toggle the utility wrappers (below).

- **`include`** — if set, *only* the named server-native MCP tools are registered.
- **`exclude`** — if set and `include` is not, *every* server-native tool *except* those names is registered.
- **Precedence** — if both are set, **`include` wins**; names in `exclude` that are not in `include` are simply absent, and names in both stay allowed (the `exclude` entry is ignored).

This worked precedence example is the canonical case to internalize:

```yaml
tools:
  include: [create_issue]
  exclude: [create_issue, delete_issue]
```

Result: `create_issue` is still allowed (it is on the include list), and `delete_issue` is ignored because `include` takes precedence — only `create_issue` is registered.

## Utility-tool policy

Beyond server-native tools, Hermes may register four utility wrappers per MCP server — Resources (`list_resources`, `read_resource`) and Prompts (`list_prompts`, `get_prompt`). Set `tools.resources: false` to disable the resource pair, `tools.prompts: false` to disable the prompt pair.

**Capability-aware registration:** even when `resources: true` or `prompts: true`, Hermes only registers the utility tools if the MCP session actually exposes the corresponding capability. So it is normal to enable prompts and still see no prompt utilities appear — because that server does not support prompts.

**`enabled: false`** skips the server entirely: no connection attempt, no discovery, no tool registration; the config remains in place for later reuse. **Empty result behavior:** if filtering removes all server-native tools and no utility tools are registered, Hermes does not create an empty MCP runtime toolset for that server.

## Example configs

Four worked patterns ship in the reference. The `github` allowlist is the safe default — pin an explicit `include` and turn the utility wrappers off:

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
    tools:
      include: [list_issues, create_issue, update_issue, search_code]
      resources: false
      prompts: false
```

The other three patterns: a **Stripe blacklist** (HTTP `url` + `headers.Authorization`, `exclude: [delete_customer, refund_payment]`); a **resource-only docs server** (`include: []` so no native tools register, with `resources: true` / `prompts: false`); and a **TLS client certificate (mTLS)** set, where HTTP/SSE servers requiring a client cert set `client_cert` as a PEM path, a `[cert, key]` list of separate files, or a 3-element `[cert, key, password]` list for an encrypted key, optionally with `ssl_verify` pointed at a private CA bundle. Paths support `~` expansion and missing files fail fast at connect time with a server-scoped error; `ssl_verify: false` disables server-cert verification entirely (do not use with real services); mTLS works on both Streamable HTTP and SSE transports.

## Reloading, tool naming, and sanitization

After changing MCP config, reload servers in-session with the `/reload-mcp` slash command — no restart required. Server-native MCP tools are registered under the `mcp_<server>_<tool>` naming pattern (e.g. `mcp_github_create_issue`, `mcp_filesystem_read_file`); utility tools follow the same prefix (`mcp_<server>_list_resources`, `..._read_resource`, `..._list_prompts`, `..._get_prompt`).

**Name sanitization:** hyphens (`-`) and dots (`.`) in both server and tool names are replaced with underscores before registration, so the names are valid identifiers for LLM function-calling APIs. A server `my-api` exposing a tool `list-items.v2` becomes:

```text
mcp_my_api_list_items_v2
```

Critically, when writing `include`/`exclude` filters you must use the **original** MCP tool name (with hyphens/dots), *not* the sanitized version.

## OAuth 2.1 authentication

For HTTP servers that require OAuth, set `auth: oauth` on the server entry. Hermes then uses the MCP SDK's OAuth 2.1 **PKCE** flow — metadata discovery, dynamic client registration, token exchange, and refresh:

- On first connect, a browser window opens for authorization.
- Tokens are persisted to `~/.hermes/mcp-tokens/<server>.json` and reused across sessions.
- Token refresh is automatic; re-authorization only happens when refresh fails.
- Applies only to HTTP/StreamableHTTP transport (`url`-based servers).

**Source**: `inbox/hermes_agent_docs/reference/mcp-config-reference.md` · https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference
**Last Updated**: 2026-06-19
**Status**: Active
