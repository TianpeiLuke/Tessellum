---
tags:
  - resource
  - documentation
  - hermes_agent
  - mcp
  - tool_integration
keywords:
  - hermes mcp configuration
  - mcp_servers config block
  - stdio vs http mcp servers
  - oauth 2.1 mcp authentication
  - mtls client certificates
  - mcp catalog one-click install
  - env var substitution
topics:
  - Hermes Agent
  - Model Context Protocol
  - Tool Integration
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
access_control_group: ["general"]
---

# Hermes MCP — Concept & Server Configuration

## Overview

MCP (Model Context Protocol) is how Hermes Agent connects to external tool servers so the agent can use tools that live outside Hermes itself — GitHub, databases, file systems, browser stacks, internal APIs, and more. This note covers the **declaration/configuration half** of Hermes MCP: what MCP gives you, the curated one-click catalog, the two kinds of MCP servers (local stdio vs remote HTTP vs OAuth 2.1), mutual-TLS client certs, the `mcp_servers` config-key reference, and the `--preset` shortcut. The complementary runtime half — the tool-prefix scheme, per-server filtering, dynamic discovery, sampling, and running Hermes as an MCP server — is documented in [hermes_mcp_filtering_serving](hermes_mcp_filtering_serving.md). MCP support ships with the standard install — no extra step needed.

## What MCP gives you

- Access to external tool ecosystems without writing a native Hermes tool first
- Local stdio servers and remote HTTP MCP servers in the same config
- Automatic tool discovery and registration at startup
- Utility wrappers for MCP resources and prompts when supported by the server
- Per-server filtering so you can expose only the MCP tools you actually want Hermes to see

## Quick start

Add an MCP server to `~/.hermes/config.yaml`, start Hermes (`hermes chat`), and ask it to use the MCP-backed capability. Hermes discovers the server's tools and uses them like any other tool.

```yaml
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
```

## Catalog: one-click install for Nous-approved MCPs

Hermes ships a curated catalog of MCP servers that Nous staff has reviewed and merged. They are disabled by default — install only what you actually want. The interactive picker (`hermes mcp`) shows each entry's status (`available` / `enabled` / `installed (disabled)`); `hermes mcp catalog` is the scriptable plain-text list; `hermes mcp install <name>` installs an entry by name. Hitting `Enter` on a row installs (walking through any required credentials), enables, disables, or uninstalls. Catalog entries are stored under `optional-mcps/` in the hermes-agent repo — presence in that directory means Nous approval; there is no community submission tier (entries are added by merging a PR).

Catalog entries can require an **API key** (Hermes prompts at install time and writes the value to `~/.hermes/.env`; non-secret values like base URLs go to the same file), **OAuth** for a remote MCP (written as `auth: oauth` in config; the MCP client opens a browser on first connection), or **OAuth** for a third-party provider like Google/GitHub (Hermes points you at `hermes auth <provider>` if not yet authenticated).

### Tool selection at install time

After credentials are configured, Hermes probes the MCP server to list every tool it exposes and presents a checklist. The pre-checked rows come from (1) your prior selection if you have installed this entry before (reinstalls preserve what you had — the manifest's defaults don't override it), (2) the manifest's `tools.default_enabled` if the entry declares one (some catalog entries pre-prune mutating or rarely-useful tools), or (3) **everything** if neither applies. Submit with `ENTER`; only the checked tools end up in `mcp_servers.<name>.tools.include`. If you select everything, no filter is written (cleanest config shape, identical behavior). **If the probe fails** (server unreachable, OAuth not yet completed, backing service not running) the install still succeeds — the manifest's `tools.default_enabled` is applied directly (if declared) or no filter is written; re-run `hermes mcp configure <name>` once the server is reachable to refine.

### Trust model

Installing a catalog entry runs whatever the manifest specifies — `git clone`, the entry's `bootstrap` commands (`pip install`, `npm install`, etc.), and ultimately the MCP server's own code. Manifests are gated by PR review into the hermes-agent repo, so Nous has reviewed each entry before it shipped — **but you should still read the manifest before installing**, especially the `source:` field's repository, the `install.bootstrap:` commands, and any `transport.command:` invocation. Manifests live at `optional-mcps/<name>/manifest.yaml` on GitHub; the picker prints the manifest's `source:` URL at install time, and the web dashboard's MCP page surfaces the same detail (transport, auth type, endpoint URL or command+args, git install source/ref, bootstrap commands, setup notes) so you can inspect exactly what an entry connects to or runs before installing.

### Manifest version compatibility

Manifests pin a `manifest_version`. The catalog is forward-compatible: if a PR adds an entry with a newer `manifest_version` than your installed Hermes understands, the picker surfaces a warning (`⚠ '<name>' requires a newer Hermes`) for that entry instead of silently hiding it. Run `hermes update` to install the latest Hermes when you see that.

### Runtime `${ENV_VAR}` substitution

Inside an entry's `transport.command`, `transport.args`, `transport.url`, and `headers`, `${VAR}` placeholders are resolved at server-connect time from environment variables (which include everything in `~/.hermes/.env`) — useful when a catalog entry references a value the user configured elsewhere (e.g. `${HOME}/foo` or `${MY_PROVIDER_TOKEN}`). This is distinct from `${INSTALL_DIR}` in catalog manifests, which is substituted at install-time with the path the catalog cloned the entry's repo into.

### Updating tool selection / manifest

`hermes mcp configure <name>` reopens the same checklist with your current selection pre-checked (use it to enable more tools or opt into newly added server tools). MCPs are never auto-updated — re-run `hermes mcp install <name>` to refresh after a Hermes update if a manifest version changed. To add an MCP to the catalog, open a PR against `optional-mcps/`.

## Two kinds of MCP servers

**Stdio servers** run as local subprocesses and talk over stdin/stdout — use them when the server is installed locally, you want low-latency access to local resources, or you are following MCP server docs that show `command`, `args`, and `env`:

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
```

**HTTP servers** are remote endpoints Hermes connects to directly — use them when the MCP server is hosted elsewhere, your organization exposes internal MCP endpoints, or you do not want Hermes spawning a local subprocess:

```yaml
mcp_servers:
  remote_api:
    url: "https://mcp.example.com/mcp"
    headers:
      Authorization: "Bearer ***"
```

### OAuth-authenticated HTTP servers

Most hosted MCP servers (Linear, Sentry, Atlassian, Asana, Figma, Stripe, …) require OAuth 2.1 instead of a static bearer token. Set `auth: oauth` and Hermes handles discovery, dynamic client registration, [PKCE](../../term_dictionary/term_pkce.md), token exchange, refresh, and step-up auth via the MCP Python SDK. On first connect Hermes prints an authorize URL, opens your browser when possible, and waits for the OAuth callback on a local loopback port; tokens are cached at `~/.hermes/mcp-tokens/<server>.json` with `0o600` perms and reused silently until refresh fails.

```yaml
mcp_servers:
  linear:
    url: "https://mcp.linear.app/mcp"
    auth: oauth
```

**Remote / headless hosts.** When Hermes runs on a different machine than your browser, the loopback callback can't reach your laptop. Two ways to complete the flow: **paste-back** (Hermes prints "Or paste the redirect URL here…" alongside the authorize URL — open it, approve, copy the full URL the browser ends up on even though it shows a connection error, paste it at the prompt; bare `?code=…&state=…` query strings work too), or an **SSH port forward** (`ssh -N -L <port>:127.0.0.1:<port> user@host` in a separate terminal, then let the redirect flow normally). See the OAuth-over-SSH guide (SP15) for the full walkthrough, including DCR-less servers (e.g. Slack), pre-registered `client_id`/`client_secret`, scope customization, and re-auth via `hermes mcp login <server>`.

**Pitfall — providers that don't support automatic registration (Google Drive, Atlassian).** Some servers reject the dynamic client registration step (RFC 7591) that bare `auth: oauth` relies on — Google's official Drive server returns a `400 Bad Request`, so no OAuth client is created and no token is acquired. The symptom is subtle: these servers also serve `tools/list` *without* auth, so `hermes mcp login` can list the tools and look like it worked, but every real tool call later times out. `hermes mcp login` now detects this (it checks that a token actually landed on disk) and tells you to supply your own OAuth client — create one in the provider's console and add it under an `oauth:` block (`client_id`/`client_secret`), then run `hermes mcp login googledrive` to skip registration and run the normal browser authorization flow.

**Pitfall — config auto-reload race.** When you edit `~/.hermes/config.yaml` from inside a running Hermes session, the CLI auto-reloads MCP connections with a 30s timeout — not enough for an interactive OAuth flow. Add the entry, then run `hermes mcp login <server>` from a fresh terminal; it waits the full 5 minutes for you to complete auth.

## mTLS / client certificates

Remote HTTP MCP servers that require mutual TLS (client-certificate authentication) are supported via `client_cert` / `client_key`; Hermes passes the resolved certificate to the underlying HTTP client for the TLS handshake. `client_cert` accepts three shapes — a single combined PEM path, a `[cert, key]` 2-tuple, or a `[cert, key, password]` 3-tuple (the third element is the passphrase when the private key is encrypted):

```yaml
mcp_servers:
  internal_api:
    url: "https://mcp.internal.example.com/mcp"
    client_cert: ["~/.certs/mcp-client.crt", "~/.certs/mcp-client.key", "${MCP_KEY_PASSWORD}"]
```

You can also keep the cert and key fully separate via `client_cert` (combined PEM) plus an explicit `client_key`. Paths support `~` expansion; a missing file raises a clear, server-scoped error rather than an opaque TLS handshake failure.

## Basic configuration reference

Hermes reads MCP config from `~/.hermes/config.yaml` under `mcp_servers`. (SP02's config-file reference owns the full `mcp_servers` key catalog — see [hermes_config_files_precedence](hermes_config_files_precedence.md); the common keys are mirrored here for context.)

| Key | Type | Meaning |
|---|---|---|
| `command` | string | Executable for a stdio MCP server |
| `args` | list | Arguments for the stdio server |
| `env` | mapping | Environment variables passed to the stdio server |
| `url` | string | HTTP MCP endpoint |
| `headers` | mapping | HTTP headers for remote servers |
| `client_cert` | string \| list | Client certificate for mTLS — a combined PEM path, or `[cert, key]` / `[cert, key, password]` |
| `client_key` | string | Client private-key PEM path (when separate from `client_cert`) |
| `timeout` | number | Tool call timeout |
| `connect_timeout` | number | Initial connection timeout |
| `enabled` | bool | If `false`, Hermes skips the server entirely |
| `supports_parallel_tool_calls` | bool | If `true`, tools from this server may run concurrently |
| `tools` | mapping | Per-server tool filtering and utility policy |

A minimal stdio entry needs only `command` + `args`; a minimal HTTP entry needs only `url` (+ `headers` for a static bearer):

```yaml
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
  company_api:
    url: "https://mcp.internal.example.com"
    headers:
      Authorization: "Bearer ***"
```

## Built-in presets

For well-known MCP servers, `hermes mcp add` accepts a `--preset` flag that fills in the transport details so you don't have to look up the command and args. The preset only supplies defaults — anything else (env vars, headers, filtering) you pass on the same command line still wins. The only current preset is `codex` (the Codex CLI's MCP server, `codex mcp-server` over stdio; requires the `codex` CLI on PATH): `hermes mcp add codex --preset codex` adds it in one line. You can pick any local name (`hermes mcp add my-codex --preset codex` is fine); the preset only provides the `command`/`args` defaults.

**Source**: `inbox/hermes_agent_docs/user-guide/features/mcp.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
**Last Updated**: 2026-06-19
**Status**: Active
