---
tags:
  - resource
  - documentation
  - hermes_agent
  - programmatic_integration
  - developer
keywords:
  - programmatic integration
  - ACP agent client protocol
  - TUI gateway JSON-RPC
  - OpenAI-compatible API server
  - model hot-swapping
  - in-process AIAgent embed
topics:
  - Hermes Agent
  - Developer Guide
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration
access_control_group: ["general"]
---

# Hermes Programmatic Integration

## Overview

Programmatic Integration is the developer procedure for **driving the Hermes agent from external programs** — IDE plugins, custom UIs, CI pipelines, and embedded sub-agents — by picking one of three protocols Hermes ships. It is fundamentally a "pick + drive" decision: all three protocols drive the *same* `AIAgent` core and differ only in wire format and which feature set they expose, so the work is choosing the protocol that matches your transport and consumer rather than wiring new agent behavior.

The three protocols are **ACP** (JSON-RPC over stdio, for IDE clients that already speak the Agent Client Protocol), the **TUI gateway JSON-RPC** (stdio or WebSocket, for custom hosts that want fine-grained control of sessions, slash commands, approvals, and streaming events), and the **OpenAI-compatible API server** (HTTP + Server-Sent Events, for OpenAI-format frontends and language-agnostic web clients). A fourth, lower-ceremony option is a direct in-process embed: import `run_agent.AIAgent` and drive it without a subprocess. This note mirrors the source page's protocol table, per-protocol method/endpoint catalogs, the "which one should I use?" decision, cross-surface model hot-swapping, and the deliberate absence of a `--mode rpc` flag.

## The Three Protocols

Hermes ships three protocols for external integration. Pick the one that matches your transport and consumer:

| Protocol | Transport | Best for | Defined by |
|----------|-----------|----------|------------|
| **ACP** | JSON-RPC over stdio | IDE clients (VS Code, Zed, JetBrains) that already speak the Agent Client Protocol | `acp_adapter/` |
| **TUI gateway** | JSON-RPC over stdio (or WebSocket) | Custom hosts that want fine-grained control of sessions, slash commands, approvals, and streaming events | `tui_gateway/server.py` |
| **API server** | HTTP + Server-Sent Events | OpenAI-compatible frontends (Open WebUI, LobeChat, LibreChat…) and language-agnostic web clients | `gateway/platforms/api_server.py` |

All three drive the same `AIAgent` core. They differ only in wire format and which set of features they expose — choosing a protocol is therefore a transport/consumer decision, not a capability re-build.

## ACP (Agent Client Protocol)

`hermes acp` starts a stdio JSON-RPC server speaking ACP. It is used in production by VS Code (Zed Industries' ACP extension), Zed, and any JetBrains IDE with an ACP plugin.

Capabilities exposed: session creation, prompt submission, streaming agent message chunks, tool-call events, permission requests, session fork, cancel, and authentication. Tool output is rendered into ACP `Diff`/`ToolCall` content blocks the IDE understands. The full lifecycle, event bridge, and approval flow live in the ACP Internals page (link-out — owned by the internals sub-plan).

```bash
hermes acp                  # serve ACP on stdio
hermes acp --bootstrap      # print install snippet for an ACP-capable IDE
```

## TUI Gateway JSON-RPC

`tui_gateway/server.py` is the protocol the Ink TUI (`hermes --tui`) and the embedded dashboard PTY bridge talk to. Any external host can speak the same protocol over stdio (or WebSocket via `tui_gateway/ws.py`). This is the richest-feature surface: a custom desktop/web/TUI host gets slash commands, approvals, clarify, multi-agent, and session branching.

**Method catalog (selected):**

```
prompt.submit           prompt.background       session.steer
session.create          session.list            session.active_list
session.activate        session.close           session.interrupt
session.history         session.compress        session.branch
session.title           session.usage           session.status
clarify.respond         sudo.respond            secret.respond
approval.respond        config.set / config.get commands.catalog
command.resolve         command.dispatch        cli.exec
reload.mcp              reload.env              process.stop
delegation.status       subagent.interrupt      spawn_tree.save / list / load
terminal.resize         clipboard.paste         image.attach
```

`session.active_list`, `session.activate`, and `session.close` are the process-local live-session controls used by the TUI session switcher. Use `session.list` / `/resume` for saved transcript discovery; use the active-session methods only for sessions currently open in the TUI gateway process.

**Events streamed back:** `message.delta`, `message.complete`, `tool.start`, `tool.progress`, `tool.complete`, `approval.request`, `clarify.request`, `sudo.request`, `secret.request`, `gateway.ready`, plus session lifecycle and error events.

**Pi-style RPC mapping** — every command in the Pi-mono RPC spec has a TUI-gateway equivalent:

| Pi command | Hermes equivalent |
|------------|-------------------|
| `prompt` | `prompt.submit` (or ACP `session/prompt`) |
| `steer` | `session.steer` |
| `follow_up` | `prompt.submit` queued after current turn |
| `abort` | `session.interrupt` |
| `set_model` | `command.dispatch` for `/model <provider:model>` (mid-session, persistent) |
| `compact` | `session.compress` |
| `get_state` | `session.status` |
| `get_messages` | `session.history` |
| `switch_session` | `session.resume` |
| `fork` | `session.branch` |
| `ui_request` / `ui_response` | `clarify.respond` / `sudo.respond` / `secret.respond` / `approval.respond` |

## OpenAI-Compatible API Server

`gateway/platforms/api_server.py` exposes Hermes over HTTP for any client that already speaks the OpenAI format. It is useful when you want a web frontend, a curl-driven CI runner, or a non-Python consumer. Setup, headers (`X-Hermes-Session-Id`, `X-Hermes-Session-Key`), and frontend wiring are documented on the API Server feature page (link-out).

```
POST /v1/chat/completions        OpenAI Chat Completions (streaming via SSE)
POST /v1/responses               OpenAI Responses API (stateful)
POST /v1/runs                    Start a run, returns run_id (202)
GET  /v1/runs/{id}               Run status
GET  /v1/runs/{id}/events        SSE stream of lifecycle events
POST /v1/runs/{id}/approval      Resolve a pending approval
POST /v1/runs/{id}/stop          Interrupt the run
GET  /v1/capabilities            Machine-readable feature flags
GET  /v1/models                  Lists hermes-agent
GET  /health, /health/detailed
```

## Which One Should I Use?

- **You're writing an IDE plugin and the IDE already speaks ACP** → ACP. Zero protocol work on the IDE side.
- **You're writing a custom desktop / web / TUI host and want every Hermes feature** (slash commands, approvals, clarify, multi-agent, session branching) → TUI gateway JSON-RPC.
- **You want any OpenAI-compatible frontend, a language-agnostic HTTP client, or curl-driven automation** → API server.
- **You want a Python in-process embed without a subprocess** → import `run_agent.AIAgent` directly (see the Agent Loop internals page).

## Model Hot-Swapping

Mid-session model switching works on every surface — it's the `/model` slash command under the hood. Provider-aware resolution (the same model name picks the right format for whatever provider you're on) is built in; the implementation is `hermes_cli/model_switch.py`.

- **CLI / TUI:** `/model claude-sonnet-4` or `/model openrouter:anthropic/claude-sonnet-4.6`
- **TUI gateway RPC:** `command.dispatch` with `{"command": "/model claude-sonnet-4"}`
- **ACP:** the IDE sends the slash command as a prompt; the agent dispatches it
- **API server:** include a `model` field in the request body or set `X-Hermes-Model`

## A Note on `--mode rpc`

Hermes does **not** have a `--mode rpc` flag. The three protocols above already cover the use cases — ACP for IDE-protocol clients, the TUI gateway for stdio JSON-RPC hosts, and the API server for HTTP. If you find a real gap that none of them fill, open an issue with the concrete consumer you're building.

**Source**: `inbox/hermes_agent_docs/developer-guide/programmatic-integration.md`
**Last Updated**: 2026-06-19
**Status**: Active
