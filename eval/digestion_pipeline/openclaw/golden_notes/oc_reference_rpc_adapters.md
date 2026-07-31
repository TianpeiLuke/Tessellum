---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - rpc
keywords:
  - openclaw rpc adapters
  - json-rpc external cli
  - signal-cli http daemon
  - imsg stdio child process
  - watch.subscribe send chats.list
  - sse event stream api/v1/events
  - adapter guidelines gateway lifecycle
topics:
  - OpenClaw
  - RPC Adapters
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/reference/rpc
access_control_group: ["general"]
---

# OpenClaw — RPC Adapter Patterns for External CLIs

## Overview

This note models the two RPC adapter patterns OpenClaw uses to integrate external command-line tools over **JSON-RPC**, mirroring the `reference/rpc` source page. OpenClaw integrates external CLIs via JSON-RPC, and two patterns are used today: **Pattern A** — a long-running HTTP daemon (e.g. `signal-cli`) — and **Pattern B** — a stdio child process spawned per integration (e.g. `imsg`). The note covers each pattern's transport, event stream, health probe, lifecycle ownership, and core methods, plus the cross-pattern **adapter guidelines** for adding or changing a CLI integration. It is the operational reference the channel docs (Signal, iMessage) and the Gateway protocol reference point to for the exact RPC integration shape.

## Pattern A: HTTP daemon (signal-cli)

The first pattern runs the external CLI as a long-lived HTTP daemon that OpenClaw talks to over JSON-RPC. Per the source page, the contract is:

- `signal-cli` runs as a daemon with **JSON-RPC over HTTP**.
- The event stream is **SSE** at `/api/v1/events`.
- The health probe is `/api/v1/check`.
- OpenClaw owns the daemon lifecycle when `channels.signal.autoStart=true`.

In this shape the external tool is a persistent server: it exposes an HTTP endpoint for JSON-RPC calls, pushes events back over a Server-Sent-Events stream, and answers a liveness/health check. When `channels.signal.autoStart=true`, OpenClaw is responsible for starting and stopping the `signal-cli` daemon itself (lifecycle ownership), rather than expecting an operator-managed external process. The source page directs operators to the **Signal** channel documentation (`/channels/signal`) for the concrete setup and endpoints.

## Pattern B: stdio child process (imsg)

The second pattern spawns the external CLI as a child process and exchanges JSON-RPC over its standard input/output rather than over a network socket. Per the source page:

- OpenClaw spawns `imsg rpc` as a **child process** for iMessage.
- JSON-RPC is **line-delimited over stdin/stdout** — one JSON object per line.
- There is **no TCP port and no daemon required**.

This is a lighter-weight integration: instead of a network daemon, OpenClaw launches the CLI directly (`imsg rpc`) and frames each JSON-RPC message as a single line of JSON written to / read from the child's stdio streams. Because there is no listening socket, the integration needs no port allocation and no separately-managed daemon process — the child's lifetime is bound to OpenClaw's.

The core JSON-RPC methods used in this pattern, copied verbatim from the source page, are:

- `watch.subscribe` → notifications (`method: "message"`)
- `watch.unsubscribe`
- `send`
- `chats.list` (probe/diagnostics)

Here `watch.subscribe` opens a subscription whose inbound events arrive as JSON-RPC notifications with `method: "message"`; `watch.unsubscribe` tears that subscription down; `send` delivers an outbound message; and `chats.list` is used as a probe / diagnostics call. The source page directs operators to the **iMessage** channel documentation (`/channels/imessage`) for legacy setup and addressing, noting that the stable `chat_id` is the preferred addressing identifier.

## Adapter guidelines

The source page closes with three cross-pattern guidelines that apply when adding or changing any external-CLI RPC integration, copied verbatim:

- Gateway owns the process (start/stop tied to provider lifecycle).
- Keep RPC clients resilient: timeouts, restart on exit.
- Prefer stable IDs (e.g., `chat_id`) over display strings.

The first guideline makes the OpenClaw **gateway** the owner of the adapter process lifecycle — process start and stop are tied to the provider's lifecycle, matching Pattern A's `autoStart` ownership and Pattern B's spawned child. The second requires adapter RPC clients to be resilient: enforce timeouts and restart the underlying process when it exits. The third prescribes addressing by stable identifiers such as `chat_id` instead of human-facing display strings, so integrations stay robust against renamed or ambiguous display names.

**Source**: OpenClaw documentation — `reference/rpc` (mirror `inbox/openclaw_docs/reference/rpc.md`)
**Last Updated**: 2026-06-22
**Status**: Active
