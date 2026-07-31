---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - protocol
keywords:
  - openclaw gateway runtime model
  - always-on multiplexed gateway process
  - openai-compatible endpoints v1
  - port and bind precedence
  - hot reload modes hybrid
  - connect hello-ok req res protocol
  - two-stage agent runs
  - gateway safety guarantees
topics:
  - OpenClaw
  - Gateway Runtime and Protocol
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/gateway
access_control_group: ["general"]
---

# OpenClaw — Gateway Runtime Model and Operator Protocol

## Overview

This note describes the OpenClaw **Gateway runtime model and operator-view protocol** — the conceptual surface of the always-on Gateway process — mirroring the runtime/protocol half of the `gateway` source page (the operational runbook half lives in [oc_gateway_runbook](oc_gateway_runbook.md)). It covers the single multiplexed process that hosts WebSocket control/RPC plus HTTP APIs, the OpenAI-compatible HTTP endpoint set (`/v1/models`, `/v1/embeddings`, `/v1/chat/completions`, `/v1/responses`, `/tools/invoke`), port and bind precedence, the four hot-reload modes, the `connect` → `hello-ok` → `req/res` + events protocol handshake (including the two-stage agent run), and the Gateway's safety guarantees.

## Runtime model

The Gateway is **one always-on process** for routing, the control plane, and channel connections. It exposes a **single multiplexed port** that simultaneously serves:

- WebSocket control/RPC
- HTTP APIs (`/v1/models`, `/v1/embeddings`, `/v1/chat/completions`, `/v1/responses`, `/tools/invoke`)
- Plugin HTTP routes, such as the optional `/api/v1/admin/rpc`
- Control UI and hooks

The default bind mode is `loopback`. **Auth is required by default.** Shared-secret setups use `gateway.auth.token` / `gateway.auth.password` (or the environment variables `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD`), and non-loopback reverse-proxy setups can use `gateway.auth.mode: "trusted-proxy"`.

## OpenAI-compatible endpoints

OpenClaw's highest-leverage compatibility surface is the OpenAI-compatible HTTP API:

- `GET /v1/models`
- `GET /v1/models/{id}`
- `POST /v1/embeddings`
- `POST /v1/chat/completions`
- `POST /v1/responses`

This set matters because most Open WebUI, LobeChat, and LibreChat integrations probe `/v1/models` first; many RAG and memory pipelines expect `/v1/embeddings`; and agent-native clients increasingly prefer `/v1/responses`. The `/v1/models` endpoint is **agent-first**: it returns `openclaw`, `openclaw/default`, and `openclaw/<agentId>`. `openclaw/default` is the stable alias that always maps to the configured default agent. Use the `x-openclaw-model` header when you want a backend provider/model override; otherwise the selected agent's normal model and embedding setup stays in control. All of these run on the **main Gateway port** and use the **same trusted operator auth boundary** as the rest of the Gateway HTTP API. Admin HTTP RPC (`POST /api/v1/admin/rpc`) is a separate, default-off plugin route for host tooling that cannot use WebSocket RPC (see the Admin HTTP RPC plugin docs in References).

## Port and bind precedence

Port and bind mode each resolve through an ordered precedence chain:

| Setting | Resolution order |
| --- | --- |
| Gateway port | `--port` → `OPENCLAW_GATEWAY_PORT` → `gateway.port` → `18789` |
| Bind mode | CLI/override → `gateway.bind` → `loopback` |

Installed gateway services record the resolved `--port` in supervisor metadata. After changing `gateway.port`, run `openclaw doctor --fix` or `openclaw gateway install --force` so launchd/systemd/schtasks starts the process on the new port. Gateway startup uses the same effective port and bind when it seeds local Control UI origins for non-loopback binds — for example, `--bind lan --port 3000` seeds `http://localhost:3000` and `http://127.0.0.1:3000` before runtime validation runs. Add any remote browser origins, such as HTTPS proxy URLs, to `gateway.controlUi.allowedOrigins` explicitly.

## Hot reload modes

Gateway config reload watches the active config file path (resolved from profile/state defaults, or `OPENCLAW_CONFIG_PATH` when set). After the first successful load, the running process serves the active in-memory config snapshot; a successful reload swaps that snapshot atomically. The behavior is governed by `gateway.reload.mode`, which defaults to `hybrid`:

| `gateway.reload.mode` | Behavior |
| --- | --- |
| `off` | No config reload |
| `hot` | Apply only hot-safe changes |
| `restart` | Restart on reload-required changes |
| `hybrid` (default) | Hot-apply when safe, restart when required |

## Protocol quick reference (operator view)

The operator-facing WebSocket protocol is a connection handshake followed by request/response calls and a server-pushed event stream:

- The **first client frame must be `connect`.**
- The Gateway returns a **`hello-ok` snapshot** carrying `presence`, `health`, `stateVersion`, `uptimeMs`, and limits/policy.
- `hello-ok.features.methods` / `events` are a **conservative discovery list**, not a generated dump of every callable helper route.
- Requests follow `req(method, params)` → `res(ok/payload | error)`.
- Common events include `connect.challenge`, `agent`, `chat`, `session.message`, `session.operation`, `session.tool`, `sessions.changed`, `presence`, `tick`, `health`, `heartbeat`, pairing/approval lifecycle events, and `shutdown`.

Agent runs are **two-stage**:

1. An immediate **accepted ack** (`status:"accepted"`).
2. A **final completion response** (`status:"ok" | "error"`), with streamed `agent` events in between.

The full protocol documentation lives at the Gateway Protocol page (see References).

## Safety guarantees

The Gateway runtime makes three explicit safety guarantees:

- Gateway protocol clients **fail fast** when the Gateway is unavailable — there is no implicit direct-channel fallback.
- Invalid / non-`connect` first frames are **rejected and closed**.
- Graceful shutdown **emits a `shutdown` event before socket close**.

**Source**: OpenClaw documentation — `gateway` (mirror `inbox/openclaw_docs/gateway.md`), runtime/protocol sections
**Last Updated**: 2026-06-22
**Status**: Active
