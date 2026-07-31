---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - acp
keywords:
  - openclaw acp bridge
  - acp over stdio gateway websocket
  - openclaw acp client debug
  - acp session key mapping
  - acpx openclaw target
  - zed agent_servers openclaw acp
  - gateway auth token-file
  - acp bridge vs harness
topics:
  - OpenClaw
  - CLI
  - Agent Client Protocol
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/acp
access_control_group: ["general"]
---

# OpenClaw — `openclaw acp` ACP Bridge for IDE Integrations

## Overview

This note is the procedure for running `openclaw acp`, the Gateway-backed Agent Client Protocol (ACP) bridge that lets an IDE or ACP client drive an OpenClaw Gateway session. It mirrors the `cli/acp` source page's setup/usage half: what the bridge is (and is not), starting it locally or against a remote Gateway, the built-in debug ACP client, driving a protocol smoke test, targeting a specific agent by session key, wiring up `acpx` and the Zed editor, mapping ACP sessions onto Gateway session keys, and the full `acp` / `acp client` option surface. The ACP↔Gateway capability contract (Compatibility Matrix, Known Limitations, smoke-test ledger shape) is a separate model note — see [oc_cli_acp_compatibility](oc_cli_acp_compatibility.md).

## What `openclaw acp` Is (and Is Not)

`openclaw acp` runs the [Agent Client Protocol (ACP)](https://agentclientprotocol.com/) bridge that talks to an OpenClaw Gateway. The command speaks ACP over stdio for IDEs and forwards prompts to the Gateway over WebSocket, keeping ACP sessions mapped to Gateway session keys. It is a Gateway-backed ACP bridge, **not** a full ACP-native editor runtime: it focuses on session routing, prompt delivery, and basic streaming updates. If you instead want an external MCP client to talk directly to OpenClaw channel conversations (rather than hosting an ACP harness session), use [`openclaw mcp serve`](https://docs.openclaw.ai/cli/mcp).

The page explicitly flags that it is often confused with ACP harness sessions. In `openclaw acp` mode, OpenClaw acts as an ACP **server**, an IDE or ACP client connects to OpenClaw, and OpenClaw forwards that work into a Gateway session. This is different from [ACP Agents](https://docs.openclaw.ai/tools/acp-agents), where OpenClaw runs an external harness such as Codex or Claude Code through `acpx`. The quick rule: when an editor/client wants to talk ACP **to** OpenClaw, use `openclaw acp`; when OpenClaw should launch Codex/Claude/Gemini as an ACP harness, use `/acp spawn` and ACP Agents.

## Usage

Run the bridge with no arguments for a local Gateway, or point it at a remote Gateway and attach to a specific session:

```bash
openclaw acp

# Remote Gateway
openclaw acp --url wss://gateway-host:18789 --token <token>

# Remote Gateway (token from file)
openclaw acp --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token

# Attach to an existing session key
openclaw acp --session agent:main:main

# Attach by label (must already exist)
openclaw acp --session-label "support inbox"

# Reset the session key before the first prompt
openclaw acp --session agent:main:main --reset-session
```

## ACP Client (Debug)

Use the built-in ACP client to sanity-check the bridge without an IDE. It spawns the ACP bridge and lets you type prompts interactively:

```bash
openclaw acp client

# Point the spawned bridge at a remote Gateway
openclaw acp client --server-args --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token

# Override the server command (default: openclaw)
openclaw acp client --server "node" --server-args openclaw.mjs acp --url ws://127.0.0.1:19001
```

The debug client's permission model is allowlist-based auto-approval scoped to trusted core tool IDs only. `read` auto-approval is scoped to the current working directory (`--cwd` when set). ACP only auto-approves narrow readonly classes — scoped `read` calls under the active cwd plus readonly search tools (`search`, `web_search`, `memory_search`); unknown/non-core tools, out-of-scope reads, exec-capable tools, control-plane tools, mutating tools, and interactive flows always require explicit prompt approval. Server-provided `toolCall.kind` is treated as untrusted metadata, not an authorization source. This ACP bridge policy is separate from ACPX harness permissions — if you run OpenClaw through the `acpx` backend, `plugins.entries.acpx.config.permissionMode=approve-all` is the break-glass "yolo" switch for that harness session.

## Protocol Smoke Testing (Driving the Test)

For protocol-level debugging, start a Gateway with isolated state and drive `openclaw acp` over stdio with an ACP JSON-RPC client. The recommended turns to cover are `initialize`, `session/new`, `session/list` with an absolute `cwd`, `session/resume`, `session/close`, duplicate close, and missing resume. The resulting proof should include the advertised lifecycle capabilities, a Gateway-backed session row, update notifications, and the Gateway `sessions.list` log (the shape of that ledger is documented in [oc_cli_acp_compatibility](oc_cli_acp_compatibility.md)). Avoid using `openclaw gateway call sessions.list` as the only ACP proof — that CLI path may request a fresh-token operator scope upgrade, whereas ACP bridge correctness is proven by ACP stdio frames plus the Gateway `sessions.list` log.

## How to Use This

Use ACP when an IDE (or other client) speaks Agent Client Protocol and you want it to drive an OpenClaw Gateway session. The three steps are: (1) ensure the Gateway is running (local or remote); (2) configure the Gateway target (config or flags); (3) point your IDE to run `openclaw acp` over stdio. Persist the Gateway target in config, or pass it directly per run:

```bash
# Example config (persisted)
openclaw config set gateway.remote.url wss://gateway-host:18789
openclaw config set gateway.remote.token <token>

# Example direct run (no config write)
openclaw acp --url wss://gateway-host:18789 --token <token>
# preferred for local process safety
openclaw acp --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token
```

## Selecting Agents

ACP does not pick agents directly — it routes by the Gateway session key. Use agent-scoped session keys to target a specific agent:

```bash
openclaw acp --session agent:main:main
openclaw acp --session agent:design:main
openclaw acp --session agent:qa:bug-123
```

Each ACP session maps to a single Gateway session key. One agent can have many sessions; ACP defaults to an isolated `acp-bridge:<uuid>` session unless you override the key or label. Per-session `mcpServers` are not supported in bridge mode — if an ACP client sends them during `newSession` or `loadSession`, the bridge returns a clear error instead of silently ignoring them. If you want ACPX-backed sessions to see OpenClaw plugin tools or selected built-in tools such as `cron`, enable the gateway-side ACPX MCP bridges instead of trying to pass per-session `mcpServers` (see [ACP Agents — plugin tools MCP bridge](https://docs.openclaw.ai/tools/acp-agents-setup#plugin-tools-mcp-bridge) and [OpenClaw tools MCP bridge](https://docs.openclaw.ai/tools/acp-agents-setup#openclaw-tools-mcp-bridge)).

## Use from `acpx` (Codex, Claude, Other ACP Clients)

If you want a coding agent such as Codex or Claude Code to talk to your OpenClaw bot over ACP, use `acpx` with its built-in `openclaw` target. The typical flow is: (1) run the Gateway and make sure the ACP bridge can reach it; (2) point `acpx openclaw` at `openclaw acp`; (3) target the OpenClaw session key you want the coding agent to use.

```bash
# One-shot request into your default OpenClaw ACP session
acpx openclaw exec "Summarize the active OpenClaw session state."

# Persistent named session for follow-up turns
acpx openclaw sessions ensure --name codex-bridge
acpx openclaw -s codex-bridge --cwd /path/to/repo \
  "Ask my OpenClaw work agent for recent context relevant to this repo."
```

To make `acpx openclaw` target a specific Gateway and session key every time, override the `openclaw` agent command in `~/.acpx/config.json` — set `agents.openclaw.command` to `env OPENCLAW_HIDE_BANNER=1 OPENCLAW_SUPPRESS_NOTES=1 openclaw acp --url ws://127.0.0.1:18789 --token-file ~/.openclaw/gateway.token --session agent:main:main`. For a repo-local OpenClaw checkout, use the direct CLI entrypoint instead of the dev runner so the ACP stream stays clean — for example `env OPENCLAW_HIDE_BANNER=1 OPENCLAW_SUPPRESS_NOTES=1 node openclaw.mjs acp ...`. This is the easiest way to let Codex, Claude Code, or another ACP-aware client pull contextual information from an OpenClaw agent without scraping a terminal.

## Zed Editor Setup

Add a custom ACP agent in `~/.config/zed/settings.json` (or use Zed's Settings UI). The minimal form spawns `openclaw acp` over stdio; the targeted form adds `--url`/`--token`/`--session` args to bind a specific Gateway and agent:

```json
{
  "agent_servers": {
    "OpenClaw ACP": {
      "type": "custom",
      "command": "openclaw",
      "args": [
        "acp",
        "--url",
        "wss://gateway-host:18789",
        "--token",
        "<token>",
        "--session",
        "agent:design:main"
      ],
      "env": {}
    }
  }
}
```

For the simplest setup, set `"args": ["acp"]` with an empty `"env": {}`. In Zed, open the Agent panel and select "OpenClaw ACP" to start a thread.

## Session Mapping

By default, ACP bridge sessions get an isolated Gateway session key with an `acp-bridge:` prefix. These normal-model bridge sessions are synthetic and subject to stale-entry pruning and entry-count caps. To reuse a known session, pass a session key or label: `--session <key>` uses a specific Gateway session key; `--session-label <label>` resolves an existing session by label; `--reset-session` mints a fresh session id for that key (same key, new transcript). If your ACP client supports metadata, you can override per session via a `_meta` object carrying `sessionKey` (e.g. `agent:main:main`), `sessionLabel` (e.g. `support inbox`), and `resetSession: true`. Learn more about session keys at [/concepts/session](https://docs.openclaw.ai/concepts/session).

## Options

The `openclaw acp` bridge options are:

- `--url <url>`: Gateway WebSocket URL (defaults to `gateway.remote.url` when configured).
- `--token <token>`: Gateway auth token.
- `--token-file <path>`: read Gateway auth token from file.
- `--password <password>`: Gateway auth password.
- `--password-file <path>`: read Gateway auth password from file.
- `--session <key>`: default session key.
- `--session-label <label>`: default session label to resolve.
- `--require-existing`: fail if the session key/label does not exist.
- `--reset-session`: reset the session key before first use.
- `--no-prefix-cwd`: do not prefix prompts with the working directory.
- `--provenance <off|meta|meta+receipt>`: include ACP provenance metadata or receipts.
- `--verbose, -v`: verbose logging to stderr.

Security notes: `--token` and `--password` can be visible in local process listings on some systems, so prefer `--token-file`/`--password-file` or the environment variables `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD`. Gateway auth resolution follows the shared contract used by other Gateway clients — in local mode the order is env (`OPENCLAW_GATEWAY_*`) → `gateway.auth.*` → `gateway.remote.*` fallback only when `gateway.auth.*` is unset (configured-but-unresolved local SecretRefs fail closed); in remote mode it is `gateway.remote.*` with env/config fallback per remote precedence rules; `--url` is override-safe and does not reuse implicit config/env credentials, so pass explicit `--token`/`--password` (or file variants). ACP runtime backend child processes receive `OPENCLAW_SHELL=acp` (usable for context-specific shell/profile rules), and `openclaw acp client` sets `OPENCLAW_SHELL=acp-client` on the spawned bridge process.

### `acp client` Options

The `openclaw acp client` debug subcommand adds these options:

- `--cwd <dir>`: working directory for the ACP session.
- `--server <command>`: ACP server command (default: `openclaw`).
- `--server-args <args...>`: extra arguments passed to the ACP server.
- `--server-verbose`: enable verbose logging on the ACP server.
- `--verbose, -v`: verbose client logging.

**Source**: OpenClaw documentation — `cli/acp` (mirror `inbox/openclaw_docs/cli/acp.md`), setup/usage half
**Last Updated**: 2026-06-22
**Status**: Active
