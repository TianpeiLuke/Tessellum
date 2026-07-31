---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw channel outbound api
  - defineChannelMessageAdapter
  - createMessageReceiptFromOutboundResults
  - createChannelMessageAdapterFromOutbound
  - sendDurableMessageBatch outcomes
  - durable message send context
  - dispatchChannelInboundReply compatibility
  - channel send receipt durability ownership
topics:
  - OpenClaw
  - Plugin SDK
  - Channel Outbound API
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/sdk-channel-outbound
access_control_group: ["general"]
---

# OpenClaw — Channel Outbound SDK API

## Overview

This note is the procedure for the OpenClaw **channel outbound SDK** that a messaging channel plugin uses to define its send path, imported from `openclaw/plugin-sdk/channel-outbound`. It mirrors the `plugins/sdk-channel-outbound` source page: defining a `message` adapter with `defineChannelMessageAdapter` (plus the `createMessageReceiptFromOutboundResults` receipt helper), deriving an adapter from an existing `outbound` adapter via `createChannelMessageAdapterFromOutbound`, the runtime durable-send helpers (notably `sendDurableMessageBatch(...)` and its four explicit outcomes), and the compatibility-dispatch rule for assembling inbound reply delivery. It also states the core-vs-plugin ownership split for send, receipts, and durability. Use the companion `openclaw/plugin-sdk/channel-inbound` subpath for receive/context/dispatch orchestration.

## Core vs Plugin Ownership

The page splits responsibility between the OpenClaw core kernel and the channel plugin. **Core owns** queueing, durability, generic retry policy, hooks, receipts, and the shared `message` tool. **The plugin owns** native send/edit/delete calls, target normalization, platform threading, selected quotes, notification flags, account state, and platform-specific side effects. The outbound subpath is where channel plugins expose this outbound message behavior; receive-path orchestration belongs to `openclaw/plugin-sdk/channel-inbound`.

## Adapter

Most plugins define one `message` adapter via `defineChannelMessageAdapter`. The adapter declares an `id`, a `durableFinal.capabilities` set (e.g. `text`, `replyTo`, `thread`, `messageSendingHooks`), and a `send.text` async handler that performs the native platform send and returns a `receipt`. The receipt is built with `createMessageReceiptFromOutboundResults`, passing the `results` array (`{ channel, messageId, conversationId }` entries), a `kind` (e.g. `"text"`), and optional `threadId` / `replyToId`:

```ts
import {
  defineChannelMessageAdapter,
  createMessageReceiptFromOutboundResults,
} from "openclaw/plugin-sdk/channel-outbound";

export const demoMessageAdapter = defineChannelMessageAdapter({
  id: "demo",
  durableFinal: {
    capabilities: {
      text: true,
      replyTo: true,
      thread: true,
      messageSendingHooks: true,
    },
  },
  send: {
    text: async ({ cfg, to, text, accountId, replyToId, threadId, signal }) => {
      const sent = await sendDemoMessage({
        cfg,
        to,
        text,
        accountId: accountId ?? undefined,
        replyToId: replyToId ?? undefined,
        threadId: threadId == null ? undefined : String(threadId),
        signal,
      });

      return {
        receipt: createMessageReceiptFromOutboundResults({
          results: [{ channel: "demo", messageId: sent.id, conversationId: to }],
          kind: "text",
          threadId: threadId == null ? undefined : String(threadId),
          replyToId: replyToId ?? undefined,
        }),
      };
    },
  },
});
```

The page is explicit about capability hygiene: **only declare capabilities the native transport actually preserves**. Cover each declared send, receipt, live-preview, and receive-ack capability with the contract helpers exported from this subpath.

## Existing Outbound Adapters

If the channel already has a compatible `outbound` adapter, derive the message adapter with `createChannelMessageAdapterFromOutbound` instead of duplicating send code. The derivation takes the existing `outbound` adapter plus its own `id` and `durableFinal.capabilities` (e.g. `text`, `media`):

```ts
import { createChannelMessageAdapterFromOutbound } from "openclaw/plugin-sdk/channel-outbound";

export const messageAdapter = createChannelMessageAdapterFromOutbound({
  id: "demo",
  outbound,
  durableFinal: {
    capabilities: {
      text: true,
      media: true,
    },
  },
});
```

## Durable Sends

Runtime send helpers also live on `channel-outbound`: `sendDurableMessageBatch(...)`, `withDurableMessageSendContext(...)`, `deliverInboundReplyWithMessageSendContext(...)`, and draft streaming/progress helpers such as `resolveChannelDraftStreamingChunking(...)`. The primary helper, `sendDurableMessageBatch(...)`, returns exactly one explicit outcome describing what the platform did with the batch:

- **`sent`** — at least one visible platform message was delivered.
- **`suppressed`** — no platform message should be treated as missing (i.e. a deliberate no-send, not a failure).
- **`partial_failed`** — at least one platform message was delivered before a later payload or side effect failed.
- **`failed`** — no platform receipt was produced.

When a batch mixes sent, suppressed, and failed payloads, use `payloadOutcomes` to read per-payload results rather than relying on the single batch outcome. The page also gives an anti-pattern: **do not infer hook cancellation from an empty legacy direct-delivery result** — an empty result is not a reliable signal that a hook cancelled the send.

## Compatibility Dispatch

Inbound reply dispatch should be assembled through `dispatchChannelInboundReply(...)` from `channel-inbound` (not reconstructed here). Keep platform delivery in the delivery adapter; use `channel-outbound` only for message adapters, durable sends, receipts, live preview, and reply pipeline options. This keeps the outbound subpath focused on the send/receipt/durability surface while the inbound subpath owns reply orchestration.

**Source**: OpenClaw documentation — `plugins/sdk-channel-outbound` (mirror `inbox/openclaw_docs/plugins/sdk-channel-outbound.md`)
**Last Updated**: 2026-06-22
**Status**: Active
