---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - message_lifecycle
keywords:
  - openclaw message lifecycle refactor
  - receive send domain model
  - durable send intent
  - channelmessage target relation origin receipt
  - receive send live state context
  - channelmessageadapter plugin sdk
  - at-least-once exactly-once delivery
  - shoulddropopenclawecho gateway failure origin
topics:
  - OpenClaw
  - Message Lifecycle
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/concepts/message-lifecycle-refactor
access_control_group: ["general"]
---

# OpenClaw — Message Lifecycle Refactor: The Durable Receive/Send Domain Model

## Overview

This note captures the *target design argument* of OpenClaw's `concepts/message-lifecycle-refactor` page — the half defining the durable message domain model (the migration/rollout half is its sibling note). The page proposes replacing scattered channel inbound, reply dispatch, preview streaming, and outbound delivery helpers with one durable lifecycle. The central thesis: the core primitives should be **receive** and **send**, not **reply** — a reply is only a *relation* on an outbound message, a turn is an inbound-processing convenience (not the owner of delivery), and both sending and receiving must be *context based*. It covers the problems, goals, reference model, core model, message terms, the receive/send/live contexts, the adapter surface, and the SDK reduction (migration plan, failure classes, channel mapping, and acceptance criteria are the sibling note).

## Problems the Refactor Argues Against

The current channel stack grew from several valid local needs that together leave too many public concepts and places where delivery semantics drift: simple inbound adapters use `runtime.channel.inbound.run`; rich adapters use `runtime.channel.inbound.runPreparedReply`; legacy helpers use `dispatchInboundReplyWithBase`, `recordInboundSessionAndDispatchReply`, reply payload/chunking/reference and outbound runtime helpers; preview streaming lives in channel-specific dispatchers; final-delivery durability is bolted around existing reply payload paths. The reliability bug: a Telegram polling update is acked, assistant final text exists, the process restarts before `sendMessage` succeeds, the final response is lost. The argued **target invariant**: once core decides a visible outbound message should exist, the intent must be durable *before* the platform send is attempted, and the receipt committed *after* success — giving at-least-once recovery. Exactly-once exists only for adapters that prove native idempotency or reconcile an unknown-after-send attempt against platform state before replay. This is the end state, not every current path.

## Goals and Non Goals

Explicit goals: one core lifecycle for all channel receive/send paths; durable final sends by default after an adapter declares replay-safe behavior; shared preview/edit/stream/finalization/retry/recovery/receipt semantics; a small plugin SDK surface with clear extension points; migration compatibility for existing inbound-reply callers; no platform-specific branches in core; no token-delta channel messages (channel streaming remains preview/edit/append/completed-block delivery); and structured OpenClaw-origin metadata so visible gateway failures do not re-enter shared bot-enabled rooms as fresh prompts. Non goals: do not force every channel onto durable delivery in phase one or into the same native transport; do not teach core platform specifics (Telegram topics, Slack native streams, Matrix redactions, Feishu cards, QQ voice, Teams activities); do not publish all internal migration helpers as stable SDK API; do not make retries replay completed non-idempotent platform operations.

## Reference Model

The argument borrows Vercel Chat's public mental model (`Chat`, `Thread`, `Channel`, `Message`, adapter methods such as `postMessage`/`editMessage`/`deleteMessage`/`stream`/`startTyping`, and a state adapter for dedupe/locks/queues/persistence) — the *vocabulary*, not the surface. Beyond that OpenClaw needs durable send intents before direct transport calls, explicit send contexts (begin/commit/fail), receive contexts that know platform ack policy, restart-surviving receipts that drive edits/deletes/recovery/duplicate-suppression, a smaller public SDK, and agent-specific behavior (sessions, transcripts, block streaming, tool progress, approvals, media directives, silent replies). `thread.post()`-style promises are not enough — they hide the transaction boundary that decides whether a send is recoverable.

## Core Model

The new domain should live under an internal core namespace such as `src/channels/message/*` with four concepts: `core.messages.receive(...)` owns the inbound lifecycle; `core.messages.send(...)` owns the outbound lifecycle; `core.messages.live(...)` owns preview/edit/progress/stream state; `core.messages.state(...)` owns durable intent storage, receipts, idempotency, recovery, locks, and dedupe.

## Message Terms

A normalized **Message** is platform-neutral, and **Target**, **Relation**, **Origin**, and **Receipt** are its key sub-types:

```typescript
type ChannelMessage = {
  id: string;
  channel: string;
  accountId?: string;
  direction: "inbound" | "outbound";
  target: MessageTarget;
  sender?: MessageActor;
  body?: MessageBody;
  attachments?: MessageAttachment[];
  relation?: MessageRelation;
  origin?: MessageOrigin;
  timestamp?: number;
  raw?: unknown;
};
```

**Target** (`MessageTarget`) describes where the message lives — a `kind` of `direct | group | channel | thread` plus `id` and optional `label?`/`spaceId?`/`parentId?`/`threadId?`/`nativeChannelId?`. **Relation** makes reply a relation, not an API root — its variants are `reply` (`inboundMessageId?`/`replyToId?`/`threadId?`/`quote?`), `followup` (`sessionKey?`/`previousMessageId?`), `broadcast` (`reason?`), and `system` with a `reason` enum of `approval | task | hook | cron | subagent | message_tool | cli | control_ui | automation | error`. This lets one send path handle normal replies, cron notifications, approval prompts, task completions, message-tool/CLI/Control-UI sends, subagent results, and automation sends.

**Origin** describes who produced a message and how to treat echoes of it; it is separate from relation (a message can be a reply to a user *and* OpenClaw-originated operational output). `MessageOrigin` is a union: an `{ source: "openclaw"; schemaVersion: 1; kind: "gateway_failure"; code: "agent_failed_before_reply" | "missing_api_key" | "model_login_expired"; echoPolicy: "drop_bot_room_echo" }` variant, and a `{ source: "user" | "external_bot" | "platform" | "unknown" }` variant. Core owns the meaning of OpenClaw-originated output; channels own how it is encoded into transport. The first required use is gateway-failure output: humans should still see messages such as "Agent failed before reply" or "Missing API key", but tagged operational output must not be accepted as bot-authored input in shared rooms when `allowBots` is enabled.

**Receipts** are first-class — a `MessageReceipt` carries `primaryPlatformMessageId?`, a `platformMessageIds[]` array, `parts: MessageReceiptPart[]`, `threadId?`/`replyToId?`/`editToken?`/`deleteToken?`/`url?`, `sentAt`, and `raw?`; each `MessageReceiptPart` carries `platformMessageId`, a `kind` of `text | media | voice | card | preview | unknown`, an `index`, and the same threading/edit/delete/url fields. Receipts bridge durable intent to future edit/delete/preview-finalization/duplicate-suppression/recovery, and can describe one platform message or a multi-part delivery (chunked text, media-plus-text, voice-plus-text, card fallbacks) — preserving all platform ids while exposing a primary id for threading and later edits.

## Receive Context

Receiving should not be a bare helper call; the core needs a `MessageReceiveContext` that knows dedupe, routing, session recording, and platform ack policy, exposing `dedupe()`/`resolve()`/`record(resolved)`/`dispatch(recorded)`/`commit(result)`/`fail(error)` alongside `ack`/`route`/`session`/`log` controllers. The receive flow: platform event → begin context → normalize → classify → dedupe/self-echo gate → route/authorize → record inbound session metadata → dispatch agent run → durable outbound sends through send context → commit receive → ack platform when policy allows. Critically, **ack is not one thing** — the contract keeps four signals separate: **transport ack** (the webhook/socket accepts the event envelope; some require it before dispatch); **polling offset ack** (advances a cursor so the event is not refetched — must not advance past unrecoverable work); **inbound record ack** (enough metadata persisted to dedupe/route a redelivery); and **user-visible receipt** (optional read/status/typing, never a durability boundary). `ReceiveAckPolicy` controls transport or polling acknowledgement only and must not be reused for read receipts or status reactions. Before bot authorization, receive applies the shared `shouldDropOpenClawEcho(params)` predicate when the channel can decode message origin metadata: it returns true (drop the echo) only when `isBotAuthor && isRoomish && origin?.source === "openclaw" && origin.kind === "gateway_failure" && origin.echoPolicy === "drop_bot_room_echo"`. This drop is tag-based, not text-based: a bot-authored room message with the same visible gateway-failure text but *without* OpenClaw origin metadata follows normal `allowBots` authorization. Ack policy itself is an explicit discriminated union of `{ kind: "immediate"; reason: "webhook-timeout" | "platform-contract" }`, `{ kind: "after-record" }`, `{ kind: "after-durable-send" }`, and `{ kind: "manual" }`. Telegram polling uses this ack policy for its persisted restart watermark — OpenClaw persists only the safe completed update id after successful dispatch, leaving failed or lower pending updates replayable after restart. Webhook platforms may need immediate HTTP ack yet still need inbound dedupe and durable outbound send intents because webhooks can redeliver.

## Send Context

Sending is also context based. A `MessageSendContext` carries the `message`, a `DurableSendIntent`, an `attempt` counter, an `AbortSignal`, an optional `previousReceipt`/`preview`, and exposes `render()`/`previewUpdate()`/`send()`/`edit()`/`delete()`/`commit()`/`fail()`. The preferred `core.messages.withSendContext(message, async (ctx) => …)` orchestration renders, edits in place when `ctx.preview?.canFinalizeInPlace`, otherwise calls `ctx.send(rendered)`; it expands to begin durable intent → render → optional preview/edit/stream → mark sending → final send/edit → mark committing with raw receipt → commit receipt → ack intent → fail intent on classified failure. The intent must exist before transport I/O, so a restart after begin but before commit is recoverable.

The dangerous boundary is after platform success and before receipt commit: if a process dies there, OpenClaw cannot know whether the platform message exists unless the adapter provides native idempotency or a reconciliation path. Such attempts resume in `unknown_after_send`, not blind replay; the SDK bridge requires the adapter to declare `reconcileUnknownSend`, which classifies an unknown entry as `sent`/`not_sent`/`unresolved` — only `not_sent` permits replay. Durability policy is explicit as `type MessageDurabilityPolicy = "required" | "best_effort" | "disabled"`: `required` fails closed when the intent cannot be written, `best_effort` falls through when persistence is unavailable, `disabled` keeps old direct-send behavior (legacy/compatibility helpers default to `disabled`).

Send contexts also own channel-local post-send effects — durable delivery must not bypass behavior attached to the direct send path (self-echo caches, thread markers, native edit anchors, model-signature rendering, duplicate guards), so those effects move into the send/render adapter or a named send-context hook first. Send helpers must return receipts to their caller (durable wrappers cannot swallow message ids; buffered dispatchers need them for thread anchors, edits, preview-finalization, and duplicate-suppression). Fallback sends operate on **batches**, not single payloads — a `RenderedMessageBatch` carries `units: RenderedMessageUnit[]`, an `atomicity` of `all_or_retry_remaining | best_effort_parts`, and an `idempotencyKey`; each `RenderedMessageUnit` carries `index`/`kind`/`payload`/`required`. When durable, the whole projected batch must be one durable intent or atomic batch plan, since recording payloads one-by-one risks a crash leaving a partial visible fallback with no durable record.

## Live Context

Preview/edit/progress/stream behavior should be one opt-in lifecycle. A `MessageLiveAdapter` exposes optional `begin?`/`update?`/`finalize?`/`cancel?` hooks over a `MessageSendContext` and a `LiveMessageState`; that state is durable enough to recover or suppress duplicates — `LiveMessageState` carries a `mode` of `partial | block | progress | native`, an optional `receipt?`, `visibleSince?`, `canFinalizeInPlace`, `lastRenderedHash?`, and `staleAfterMs?`. One lifecycle should cover current per-channel behavior (Telegram send-plus-edit preview with fresh final after stale age; Discord preview cancelled on media/error/explicit-reply; Slack native stream or draft by thread shape; Matrix draft finalization or redaction on mismatch; Mattermost/Teams/QQ-Bot progress streams or accumulated fallback).

## Adapter Surface and Public SDK Reduction

The public SDK target is one subpath, `defineChannelMessageAdapter` from `openclaw/plugin-sdk/channel-outbound`. The `ChannelMessageAdapter` shape composes optional `receive?: MessageReceiveAdapter`, required `send: MessageSendAdapter`, optional `live?: MessageLiveAdapter`/`origin?: MessageOriginAdapter`/`render?: MessageRenderAdapter`, and required `capabilities: MessageCapabilities`. The `MessageSendAdapter` requires `send(ctx, rendered)` plus optional `edit?`/`delete?`/`classifyError?` (→ `DeliveryFailureKind`)/`reconcileUnknownSend?`/`afterSendSuccess?`/`afterCommit?`. The `MessageReceiveAdapter` requires `normalize(raw, ctx)` plus optional `classify?`/`preflight?`/`ackPolicy?`; before preflight authorization core runs the shared echo predicate whenever `origin.decode` returns OpenClaw-origin metadata — the adapter supplies platform facts (bot author, room shape), core owns the drop decision so channels do not reimplement text filters. The `MessageOriginAdapter` offers `encode?(origin)`/`decode?(raw)`: core sets `MessageOrigin`, channels translate it to/from native metadata (Slack → `chat.postMessage({ metadata })`; Matrix → event content; others → a receipt/outbound registry). `MessageCapabilities` declares per-channel `text`/`attachments?`/`threads?`/`live?`/`delivery?` flags.

The argued **public SDK reduction** has the new surface absorb or deprecate `reply-runtime`, `reply-dispatch-runtime`, `reply-reference`, `reply-chunking`, `reply-payload`, `inbound-reply-dispatch`, `channel-reply-pipeline`, most public uses of `outbound-runtime`, and ad hoc draft-stream helpers. Compatibility subpaths can remain as wrappers, but new third-party plugins should not need them; bundled plugins may keep internal helper imports through reserved runtime subpaths while migrating.

## Relationship to Channel Inbound

`runtime.channel.inbound.*` is the runtime bridge during migration and becomes a compatibility adapter: `channel.inbound.run` → messages.receive context → session dispatch → messages.send context. `channel.inbound.runPreparedReply` remains initially: channel-owned dispatcher → messages.receive record/finalize bridge → messages.live for preview/progress → messages.send for final delivery. The old `channel.turn` runtime surface was removed; callers use `channel.inbound.*`, and docs/SDK subpaths use inbound/message nouns. (Migration steps, failure classes, durable storage schema, channel mapping, and acceptance criteria are the migration-half sibling note.)

**Source**: OpenClaw documentation — `concepts/message-lifecycle-refactor` (mirror `inbox/openclaw_docs/concepts/message-lifecycle-refactor.md`), domain-model half
**Last Updated**: 2026-06-22
**Status**: Active
