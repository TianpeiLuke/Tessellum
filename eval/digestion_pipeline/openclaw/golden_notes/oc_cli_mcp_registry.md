---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - mcp_registry
keywords:
  - openclaw mcp registry
  - openclaw mcp add set configure
  - mcp.servers config registry
  - mcp doctor probe status
  - mcp tools tool filter
  - mcp login logout oauth
  - mcp reload unset
  - mcp server recipes filesystem memory cua
  - control ui mcp page
topics:
  - OpenClaw
  - MCP Client Registry
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/mcp
access_control_group: ["general"]
---

# OpenClaw — `openclaw mcp` Client Registry (Saved Server Definitions)

## Overview

This note documents the **client-registry** half of `openclaw mcp`: the subcommands that manage OpenClaw-managed outbound MCP server definitions stored under `mcp.servers` in OpenClaw config, plus the browser **Control UI** `/mcp` editor. It mirrors the `cli/mcp` source page's "OpenClaw as an MCP client registry" and "Control UI" sections. These commands make OpenClaw act as an MCP *client-side registry* — a central store of MCP server definitions that OpenClaw's runtimes (embedded OpenClaw and other runtime adapters) launch or configure later, so each runtime does not keep its own duplicate server list. The inbound `openclaw mcp serve` bridge is covered in [oc_cli_mcp_serve](oc_cli_mcp_serve.md); the `--json` output shapes and the stdio/SSE/streamable-http transport field schemas + OAuth workflow are modeled in [oc_cli_mcp_transports](oc_cli_mcp_transports.md).

## What the registry subcommands do

The registry path is the `openclaw mcp list`, `show`, `status`, `doctor`, `probe`, `add`, `set`, `configure`, `tools`, `login`, `logout`, `reload`, and `unset` set of subcommands. These commands do **not** expose OpenClaw over MCP — they manage OpenClaw-managed MCP server definitions under `mcp.servers` in OpenClaw config. They do **not** read mcporter servers from `config/mcporter.json` (use `mcporter list` for that registry). The saved definitions are for runtimes that OpenClaw launches or configures later, such as embedded OpenClaw and other runtime adapters; OpenClaw stores them centrally so those runtimes do not need duplicate MCP server lists.

If unsure which MCP path you need, start with `openclaw mcp status --verbose` — it shows what OpenClaw has saved without starting any MCP servers.

## Important behavior

Key invariants of the registry subcommands (verbatim from source):

- these commands only read or write OpenClaw config
- `status`, `list`, `show`, `doctor` without `--probe`, `set`, `configure`, `tools`, `logout`, `reload`, and `unset` do not connect to the target MCP server
- `login` performs the MCP OAuth network flow for the configured HTTP server and saves the resulting local credentials
- `status --verbose` prints resolved transport, auth, timeout, filter, and parallel-tool-call hints without connecting
- `doctor` checks saved definitions for local setup problems such as missing stdio commands, invalid working directories, missing TLS files, disabled servers, literal sensitive header/env values, and incomplete OAuth authorization
- `doctor --probe` adds the same live connection proof as `probe` after static checks pass
- `probe` connects to the selected server or all configured servers, lists tools, and reports capabilities/diagnostics
- `add` builds a definition from flags and probes before saving unless `--no-probe` is set or OAuth authorization is needed first
- runtime adapters decide which transport shapes they actually support at execution time
- `enabled: false` keeps a server saved but excludes it from embedded runtime discovery
- `timeout` and `connectTimeout` set per-server request and connection timeouts in seconds
- `supportsParallelToolCalls: true` marks servers that adapters can call concurrently
- HTTP servers can use static headers, OAuth login, TLS verification control, and mTLS certificate/key paths
- embedded OpenClaw exposes configured MCP tools in normal `coding` and `messaging` tool profiles; `minimal` still hides them, and `tools.deny: ["bundle-mcp"]` disables them explicitly
- per-server `toolFilter.include` and `toolFilter.exclude` filter discovered MCP tools before they become OpenClaw tools
- servers that advertise resources or prompts also expose utility tools for listing/reading resources and listing/fetching prompts; those generated utility names (`resources_list`, `resources_read`, `prompts_list`, `prompts_get`) use the same include/exclude filter
- dynamic MCP tool-list changes invalidate the cached catalog for that session; the next discovery/use refreshes from the server
- repeated MCP tool request/protocol failures pause that server briefly so one broken server does not consume the whole turn
- session-scoped bundled MCP runtimes are reaped after `mcp.sessionIdleTtlMs` milliseconds of idle time (default 10 minutes; set `0` to disable) and one-shot embedded runs clean them up at run end

### Runtime adapter normalization and the Codex block

Runtime adapters may normalize this shared registry into the shape their downstream client expects. For example, embedded OpenClaw consumes OpenClaw `transport` values directly, while Claude Code and Gemini receive CLI-native `type` values such as `http`, `sse`, or `stdio`.

Codex app-server also honors an optional `codex` block on each server. This is OpenClaw projection metadata for Codex app-server threads only; it does not change ACP sessions, generic Codex harness config, or other runtime adapters. Use non-empty `codex.agents` to project a server only into specific OpenClaw agent ids — empty, blank, or invalid agent lists are rejected by config validation and omitted by the runtime projection path instead of becoming global. Use `codex.defaultToolsApprovalMode` (`auto`, `prompt`, or `approve`) to emit Codex's native `default_tools_approval_mode` for a trusted server. OpenClaw strips the `codex` metadata before handing the native `mcp_servers` config to Codex.

## Saved MCP server definitions

OpenClaw stores a lightweight MCP server registry in config for surfaces that want OpenClaw-managed MCP definitions. The full command set:

```bash
openclaw mcp list
openclaw mcp show [name]
openclaw mcp status [--verbose]
openclaw mcp doctor [name] [--probe]
openclaw mcp probe [name]
openclaw mcp add <name> [flags]
openclaw mcp set <name> <json>
openclaw mcp configure <name> [flags]
openclaw mcp tools <name> [--include csv] [--exclude csv] [--clear]
openclaw mcp login <name> [--code code]
openclaw mcp logout <name>
openclaw mcp reload
openclaw mcp unset <name>
```

Per-command notes (verbatim from source):

- `list` sorts server names.
- `show` without a name prints the full configured MCP server object.
- `status` classifies configured transports without connecting. `--verbose` includes resolved launch, timeout, OAuth, filter, and parallel-call details.
- `doctor` performs static checks without connecting. Add `--probe` when the command should also verify that enabled servers connect.
- `probe` connects and reports tool counts, resources/prompts support, list-change support, and diagnostics.
- `add` accepts stdio flags such as `--command`, `--arg`, `--env`, and `--cwd`, or HTTP flags such as `--url`, `--transport`, `--header`, `--auth oauth`, TLS, timeout, and tool-selection flags.
- `set` expects one JSON object value on the command line.
- `configure` updates enablement, tool filters, timeouts, OAuth, TLS, and parallel-tool-call hints without replacing the whole server definition.
- `tools` updates per-server tool filters. Include/exclude entries are MCP tool names and simple `*` globs.
- `login` runs the OAuth flow for HTTP servers configured with `auth: "oauth"`. The first run prints an authorization URL; rerun with `--code` after approval.
- `logout` clears stored OAuth credentials for the named server without removing the saved server definition.
- `reload` disposes cached in-process MCP runtimes. Gateway or agent processes in another process still need their own reload or restart path.
- Use `transport: "streamable-http"` for Streamable HTTP MCP servers. `openclaw mcp set` also normalizes CLI-native `type: "http"` to the same canonical config shape for compatibility.
- `unset` fails if the named server does not exist.

> **Scope note (from source):** `list`, `show`, `set`, and `unset` only read and write OpenClaw-managed `mcp.servers` entries in OpenClaw config. They do not include mcporter servers from `config/mcporter.json`; use `mcporter list` for that registry.

### Worked command examples

```bash
openclaw mcp list
openclaw mcp show context7 --json
openclaw mcp status --verbose
openclaw mcp doctor --probe
openclaw mcp probe context7 --json
openclaw mcp add memory --command npx --arg -y --arg @modelcontextprotocol/server-memory
openclaw mcp set context7 '{"command":"uvx","args":["context7-mcp"]}'
openclaw mcp tools context7 --include 'resolve-library-id,get-library-docs'
openclaw mcp set docs '{"url":"https://mcp.example.com","transport":"streamable-http"}'
openclaw mcp configure docs --timeout 20 --connect-timeout 5 --include 'search,read_*'
openclaw mcp configure docs --auth oauth --oauth-scope 'docs.read'
openclaw mcp login docs
openclaw mcp logout docs
openclaw mcp unset context7
```

## Common server recipes

These examples save server definitions only. Run `openclaw mcp doctor --probe` afterward to prove that the server starts and exposes tools.

- **Filesystem** — `openclaw mcp add files --command npx --arg -y --arg @modelcontextprotocol/server-filesystem --arg "$HOME/Documents" --include 'read_file,list_directory,search_files'`, then `openclaw mcp doctor files --probe`. Scope filesystem servers to the smallest directory tree that the agent should read or edit.
- **Memory** — `openclaw mcp add memory --command npx --arg -y --arg @modelcontextprotocol/server-memory`, then `openclaw mcp probe memory --json`. Use a tool filter if the server exposes write tools that should not be available to normal agents.
- **Local script** — `openclaw mcp add local-tools --command node --arg ./dist/mcp-server.js --cwd /srv/openclaw-tools --env API_BASE=https://internal.example`, then `openclaw mcp status --verbose`. `doctor` checks that `cwd` exists and that the command resolves from the configured environment.
- **Remote HTTP** — `openclaw mcp add docs --url https://mcp.example.com/mcp --transport streamable-http --auth oauth --oauth-scope docs.read --timeout 20 --connect-timeout 5 --include 'search,read_*'`, then `openclaw mcp doctor docs --probe`. Use OAuth when the remote server supports it; if the server requires static headers, avoid committing literal bearer tokens.
- **Desktop/CUA** — `openclaw mcp set cua-driver '{"command":"cua-driver","args":["mcp"]}'`, then `openclaw mcp tools cua-driver --include 'list_apps,observe,click,type'` and `openclaw mcp doctor cua-driver --probe`. Direct desktop-control servers inherit the permissions of the process they launch; use narrow tool filters and OS-level permission prompts.

The Filesystem recipe in full:

```bash
openclaw mcp add files \
  --command npx \
  --arg -y \
  --arg @modelcontextprotocol/server-filesystem \
  --arg "$HOME/Documents" \
  --include 'read_file,list_directory,search_files'
openclaw mcp doctor files --probe
```

## Control UI

The browser Control UI includes a dedicated MCP settings page at `/mcp`. It shows configured server counts, enabled/OAuth/filter summaries, per-server transport rows, enable/disable controls, common CLI commands, and a scoped editor for the `mcp` config section. Use the page for operator edits and quick inventory; use `openclaw mcp doctor --probe` or `openclaw mcp probe` when you need live server proof.

Operator workflow (from source):

1. Open the Control UI and choose **MCP**.
2. Review the summary cards for total, enabled, OAuth, and filtered servers.
3. Use each server row for transport, auth, filter, timeout, and command hints.
4. Toggle enablement when you want to keep a definition but exclude it from runtime discovery.
5. Edit the scoped `mcp` config section for structural changes such as new servers, headers, TLS, OAuth metadata, or tool filters.
6. Choose **Save** to persist config only, or **Save & Publish** to apply through the Gateway config path.
7. Run `openclaw mcp doctor --probe` when you need live proof that the edited server starts and lists tools.

Control UI notes (verbatim):

- command snippets quote server names so unusual names remain copyable in a shell
- displayed URL-like values are redacted before rendering when they contain embedded credentials
- the page does not start MCP transports by itself
- active runtimes may need `openclaw mcp reload`, Gateway config publish, or process restart depending on which process owns the MCP clients

**Source**: OpenClaw documentation — `cli/mcp` (mirror `inbox/openclaw_docs/cli/mcp.md`), "OpenClaw as an MCP client registry" + "Control UI" sections
**Last Updated**: 2026-06-22
**Status**: Active
