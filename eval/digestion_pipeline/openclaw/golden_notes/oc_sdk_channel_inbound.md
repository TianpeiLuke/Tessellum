---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw channel inbound api
  - plugin-sdk channel-inbound
  - buildChannelInboundEventContext
  - runChannelInboundEvent
  - dispatchChannelInboundReply
  - runtime.channel.inbound
  - channel receive path
  - channel turn helpers migration
topics:
  - OpenClaw
  - Channel Plugin SDK
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/sdk-channel-inbound
access_control_group: ["general"]
---

# OpenClaw — Channel Inbound SDK API (Receive-Path Helpers)

## Overview

This note is the procedure for a channel plugin's **receive path** built on the `openclaw/plugin-sdk/channel-inbound` SDK module, mirroring the `plugins/sdk-channel-inbound` source page. It covers the inbound noun-model a channel plugin should model (platform event → inbound facts/context → agent reply → message delivery), the three Core Helpers (`buildChannelInboundEventContext`, `runChannelInboundEvent`, `dispatchChannelInboundReply`) and their bundled-channel `runtime.channel.inbound.*` aliases, and the migration off the removed `runtime.channel.turn.*` aliases. The complementary native send / receipt / durable-delivery surface is `openclaw/plugin-sdk/channel-outbound`, documented separately.

## Receive-Path Noun Model

Channel plugins should model receive paths with **inbound** and **message** nouns. The source defines the receive path as a four-stage flow:

```text
platform event -> inbound facts/context -> agent reply -> message delivery
```

The page splits the contract across two SDK import modules by responsibility: use `openclaw/plugin-sdk/channel-inbound` for inbound event normalization, formatting, roots, and orchestration; and use `openclaw/plugin-sdk/channel-outbound` for native send, receipt, durable delivery, and live preview behavior. A plugin's receive path is therefore the inbound module's job (normalize the incoming platform event, build context, run the turn, dispatch the reply), while the actual platform-facing send is owned by the outbound module / a delivery adapter.

## Core Helpers

The inbound module exports three helpers, imported together:

```ts
import {
  buildChannelInboundEventContext,
  runChannelInboundEvent,
  dispatchChannelInboundReply,
} from "openclaw/plugin-sdk/channel-inbound";
```

Each helper owns one step of the receive path:

- **`buildChannelInboundEventContext(...)`** — project normalized channel facts into the prompt/session context.
- **`runChannelInboundEvent(...)`** — run ingest, classify, preflight, resolve, record, dispatch, and finalize for one inbound platform event (the full single-event orchestrator).
- **`dispatchChannelInboundReply(...)`** — record and dispatch an already assembled inbound reply with a delivery adapter.

For bundled/native channels that already receive the injected plugin **runtime** object, the same high-level helpers are exposed under the `runtime.channel.inbound.*` namespace. The minimal orchestration call passes the channel name, account id, the raw platform event, and an `adapter` supplying `ingest` (normalize the platform event) and `resolveTurn` (resolve the inbound reply):

```ts
await runtime.channel.inbound.run({
  channel: "demo",
  accountId,
  raw: platformEvent,
  adapter: {
    ingest: normalizePlatformEvent,
    resolveTurn: resolveInboundReply,
  },
});
```

Compatibility dispatchers should assemble `dispatchChannelInboundReply(...)` inputs and keep platform delivery in the delivery adapter. New send paths should prefer message adapters and durable message helpers (i.e. the outbound module) rather than hand-rolling delivery in the inbound path.

## Migration

The old `runtime.channel.turn.*` runtime aliases were **removed**. Replace each old `turn.*` call with the corresponding `inbound.*` alias:

- `runtime.channel.inbound.run(...)` — for raw inbound events.
- `runtime.channel.inbound.dispatchReply(...)` — for assembled reply contexts.
- `runtime.channel.inbound.buildContext(...)` — for inbound context payloads.
- `runtime.channel.inbound.runPreparedReply(...)` — only for channel-owned prepared dispatch paths that already assemble their own dispatch closure.

New plugin code should **not** introduce `turn`-named channel APIs. The source draws a vocabulary boundary: keep model or agent turn vocabulary inside agent/provider code, and have channel plugins use **inbound**, **message**, **delivery**, and **reply** terms.

**Source**: OpenClaw documentation — `plugins/sdk-channel-inbound` (mirror `inbox/openclaw_docs/plugins/sdk-channel-inbound.md`)
**Last Updated**: 2026-06-22
**Status**: Active
