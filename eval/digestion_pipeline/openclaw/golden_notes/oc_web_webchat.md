---
tags:
  - resource
  - documentation
  - openclaw
  - web
  - webchat
keywords:
  - openclaw webchat
  - native macos ios chat ui
  - chat.history chat.send chat.inject
  - chat.message.get display projection
  - transcript vs delivery model
  - replypayload live projection
  - tools.effective tools.catalog
  - webchat gateway websocket auth
topics:
  - OpenClaw
  - WebChat
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/web/webchat
access_control_group: ["general"]
---

# OpenClaw — WebChat (Native macOS/iOS Chat Over the Gateway WS)

## Overview

This note models **WebChat**, OpenClaw's native macOS/iOS SwiftUI chat UI that talks directly to the Gateway WebSocket (no embedded browser and no local static server), mirroring the `web/webchat` source page. WebChat reuses the same sessions and routing rules as other channels with deterministic routing (replies always go back to WebChat), and its observable behavior is the `chat.*` RPC contract plus a **display-projection** layer over the stored transcript. The note covers what WebChat is and the quick start, the `chat.history` / `chat.send` / `chat.inject` / `chat.message.get` behavior and display normalization, the **two-path transcript-vs-delivery model** (the durable JSONL session log vs the live `ReplyPayload` projection), the Control UI `/agents` Tools panel (`tools.effective` vs `tools.catalog`), remote tunneling, and the (config-less) global gateway options that govern it.

## What It Is and Quick Start

WebChat is a native chat UI for the Gateway with **no embedded browser and no local static server**. It uses the same sessions and routing rules as other channels, with **deterministic routing**: replies always go back to WebChat. To start: (1) start the gateway; (2) open the WebChat UI (macOS/iOS app) or the Control UI chat tab; (3) ensure a valid gateway auth path is configured — **shared-secret by default, even on loopback**.

## How It Works — The `chat.*` Contract and Display Projection

The UI connects to the Gateway WebSocket and uses `chat.history`, `chat.send`, and `chat.inject`. The behavioral model is:

- **Bounded history.** `chat.history` is bounded for stability: the Gateway may truncate long text fields, omit heavy metadata, and replace oversized entries with the literal marker `[chat.history omitted: message too large]`.
- **On-demand full entry.** When a visible assistant message was truncated in `chat.history`, the Control UI can open a side reader and fetch the full **display-normalized** entry on demand through `chat.message.get` without increasing the default history payload.
- **Active-branch only.** `chat.history` follows the **active transcript branch** for modern append-only session files, so abandoned rewrite branches and superseded prompt copies are not rendered in WebChat.
- **Compaction divider.** Compaction entries render as an explicit **compacted-history divider**. The divider explains that the compacted transcript is preserved as a checkpoint and links to the Sessions checkpoint controls, where operators can branch or restore from that compacted view when their permissions allow it.
- **Session continuity.** The Control UI remembers the backing Gateway `sessionId` returned by `chat.history` and includes it on follow-up `chat.send` calls, so reconnects and page refreshes continue the same stored conversation unless the user starts or resets a session.
- **In-flight dedup / idempotency.** The Control UI coalesces duplicate in-flight submits for the same session, message, and attachments before generating a new `chat.send` run id; the Gateway still dedupes repeated requests that reuse the same **idempotency key**.
- **Bootstrap via system prompt.** Workspace startup files and pending `BOOTSTRAP.md` instructions are supplied through the agent system prompt's Project Context, **not** copied into the WebChat user message. Bootstrap truncation only adds a concise system-prompt recovery notice; detailed counts and config knobs stay on diagnostic surfaces.

`chat.history` is also **display-normalized**: runtime-only OpenClaw context, inbound envelope wrappers, inline delivery directive tags such as `[[reply_to_*]]` and `[[audio_as_voice]]`, plain-text tool-call XML payloads (including `<tool_call>...</tool_call>`, `<function_call>...</function_call>`, `<tool_calls>...</tool_calls>`, `<function_calls>...</function_calls>`, and truncated tool-call blocks), and leaked ASCII/full-width model control tokens are stripped from visible text; assistant entries whose whole visible text is only the exact silent token `NO_REPLY` / `no_reply` are omitted. Reasoning-flagged reply payloads (`isReasoning: true`) are excluded from WebChat assistant content, transcript replay text, and audio content blocks, so thinking-only payloads do not surface as visible assistant messages or playable audio.

Two more behaviors round out the contract: `chat.inject` appends an assistant note directly to the transcript and broadcasts it to the UI (**no agent run**), and aborted runs can keep partial assistant output visible in the UI — the Gateway persists aborted partial assistant text into transcript history when buffered output exists and marks those entries with **abort metadata**. History is always fetched from the gateway (no local file watching), and if the gateway is unreachable WebChat is **read-only**.

### Transcript and Delivery Model

WebChat has two separate data paths:

- **The session JSONL file is the durable model/runtime transcript.** For normal agent runs, the embedded OpenClaw runtime persists model-visible `user`, `assistant`, and `toolResult` messages through its session manager. WebChat does not write arbitrary delivery, status, or helper text into that transcript.
- **Gateway `ReplyPayload` events are the live delivery projection.** They can be normalized for WebChat/channel display, block streaming, directive tags, media embedding, TTS/audio flags, and UI fallback behavior. They are **not** themselves the canonical session log.

Harnesses that require visible replies through `tools.message` still use WebChat as a current-run **internal source reply sink**. A targetless `message.send` from that active WebChat run is projected into the same chat and mirrored to the session transcript; WebChat does **not** become a reusable outbound channel and never inherits `lastChannel`. WebChat injects assistant transcript entries only when the Gateway owns a displayed message **outside** a normal embedded agent turn: `chat.inject`, non-agent command replies, aborted partial output, and WebChat-managed media transcript supplements.

`chat.history` reads the stored session transcript and applies WebChat display projection. If live assistant text appears during a run but disappears after history reload, the documented debug order is: first check whether the raw JSONL contains the assistant text, then whether `chat.history` projection stripped it, then whether the Control UI optimistic-tail merge replaced local delivery state with the persisted snapshot. `chat.message.get` uses the same transcript branch and display projection rules as `chat.history` — including **active-agent scoping** — but targets one transcript entry by `messageId` and returns an honest unavailable reason when the full content can no longer be returned. Normal agent-run final answers should be durable because the embedded runtime writes the assistant `message_end`; any fallback that mirrors a delivered final payload into the transcript must first avoid duplicating an assistant turn that the embedded runtime already wrote.

## Control UI Agents Tools Panel

The Control UI `/agents` Tools panel has two separate views:

- **Available Right Now** uses `tools.effective(sessionKey=...)` and shows a server-derived **read-only** projection of the current session inventory, including core, plugin, channel-owned, and already-discovered MCP server tools.
- **Tool Configuration** uses `tools.catalog` and stays focused on profiles, overrides, and catalog semantics.

Runtime availability is **session-scoped**: switching sessions on the same agent can change the **Available Right Now** list. If configured MCP servers have not been connected or were changed since the last discovery, the panel shows a notice instead of silently starting MCP transports from the read path. The config editor does not imply runtime availability — effective access still follows policy precedence (`allow` / `deny`, per-agent and provider/channel overrides).

## Remote Use

Remote mode tunnels the gateway WebSocket over SSH/Tailscale, and you do not need to run a separate WebChat server.

## Configuration Reference (WebChat)

WebChat has **no persisted config section**. The Gateway uses the built-in `chat.history` display limit; API clients can send a per-request `maxChars` to override it for a single `chat.history` call. Legacy `channels.webchat` and `gateway.webchat` config is retired — run `openclaw doctor --fix` to remove it. The full configuration reference is the gateway Configuration page (linked under References). Related global options that govern WebChat are:

- `gateway.port`, `gateway.bind`: WebSocket host/port.
- `gateway.auth.mode`, `gateway.auth.token`, `gateway.auth.password`: shared-secret WebSocket auth.
- `gateway.auth.allowTailscale`: the browser Control UI chat tab can use Tailscale Serve identity headers when enabled.
- `gateway.auth.mode: "trusted-proxy"`: reverse-proxy auth for browser clients behind an identity-aware **non-loopback** proxy source.
- `gateway.remote.url`, `gateway.remote.token`, `gateway.remote.password`: remote gateway target.
- `session.*`: session storage and main key defaults.

**Source**: OpenClaw documentation — `web/webchat` (mirror `inbox/openclaw_docs/web/webchat.md`)
**Last Updated**: 2026-06-22
**Status**: Active
