---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - messages
keywords:
  - openclaw message flow
  - inbound dedupe debouncing
  - messages.queue steer followup collect interrupt
  - sessions and devices
  - tool result content vs details
  - bodyforagent commandbody history context
  - block streaming chunking
  - reasoning visibility tokens
  - silent reply no_reply
topics:
  - OpenClaw
  - Messages
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/messages
access_control_group: ["general"]
---

# OpenClaw — Runtime Message Flow Model

## Overview

This note captures OpenClaw's **runtime message-flow model**: the conceptual path from an inbound channel message to an outbound reply, plus the behaviors layered along that path. It mirrors the `concepts/messages` source page in full — the high-level pipeline, inbound dedupe and debouncing, session/device ownership, the tool-result `content`/`details` boundary, inbound body provenance and history context, queueing/followup modes, channel run ownership, streaming/chunking, reasoning visibility and its token cost, prefixes/threading/replies, and silent replies. It describes how the *current* runtime behaves; the planned durable redesign of this flow lives in the message-lifecycle-refactor notes.

## Message Flow (High Level)

OpenClaw handles inbound messages through a pipeline of session resolution, queueing, streaming, tool execution, and reasoning visibility. The high-level path from inbound message to reply is:

```
Inbound message
  -> routing/bindings -> session key
  -> queue (if a run is active)
  -> agent run (streaming + tools)
  -> outbound replies (channel limits + chunking)
```

The key knobs live in configuration: `messages.*` controls prefixes, queueing, and group behavior; `agents.defaults.*` controls block streaming and chunking defaults; and channel overrides (`channels.whatsapp.*`, `channels.telegram.*`, etc.) set caps and streaming toggles. The full schema is documented on the Configuration page.

## Inbound Dedupe

Channels can redeliver the same message after reconnects. OpenClaw keeps a short-lived cache keyed by **channel/account/peer/session/message id** so duplicate deliveries do not trigger another agent run.

## Inbound Debouncing

Rapid consecutive messages from the **same sender** can be batched into a single agent turn via `messages.inbound`. Debouncing is scoped per channel + conversation and uses the most recent message for reply threading/IDs. It is configured with a global default plus per-channel overrides:

```json5
{
  messages: {
    inbound: {
      debounceMs: 2000,
      byChannel: {
        whatsapp: 5000,
        slack: 1500,
        discord: 1500,
      },
    },
  },
}
```

Two behavioral notes apply. Debounce applies to **text-only** messages; media/attachments flush immediately. Control commands bypass debouncing so they remain standalone — but channels that explicitly opt in to same-sender DM coalescing can keep DM commands inside the debounce window so a split-send payload can join the same agent turn.

## Sessions and Devices

Sessions are owned by the gateway, not by clients. Direct chats collapse into the agent main session key; groups/channels get their own session keys; and the session store and transcripts live on the gateway host. Multiple devices/channels can map to the same session, but history is not fully synced back to every client — the recommendation is to use one primary device for long conversations to avoid divergent context. The Control UI and TUI always show the gateway-backed session transcript, so they are the source of truth.

## Tool Result Metadata

Tool result `content` is the model-visible result, while tool result `details` is runtime metadata for UI rendering, diagnostics, media delivery, and plugins. OpenClaw keeps that boundary explicit: `toolResult.details` is stripped before provider replay and compaction input; persisted session transcripts keep only bounded `details`, and oversized metadata is replaced with a compact summary marked `persistedDetailsTruncated: true`. Plugins and tools should therefore put text the model must read in `content`, not only in `details`.

## Inbound Bodies and History Context

OpenClaw separates the **prompt body** from the **command body** across four fields. `BodyForAgent` is the primary model-facing text for the current message, and channel plugins should keep it focused on the sender's current prompt-bearing text. `Body` is the legacy prompt fallback that may include channel envelopes and optional history wrappers, but current channels should not rely on it as the primary model input when `BodyForAgent` is available. `CommandBody` is the raw user text for directive/command parsing, and `RawBody` is a legacy alias for `CommandBody` kept for compatibility.

When a channel supplies history, it uses a shared wrapper with two markers: `[Chat messages since your last reply - for context]` and `[Current message - respond to this]`. For **non-direct chats** (groups/channels/rooms), the current message body is prefixed with the sender label (the same style used for history entries), which keeps real-time and queued/history messages consistent in the agent prompt.

History buffers are **pending-only**: they include group messages that did *not* trigger a run (for example, mention-gated messages) and **exclude** messages already in the session transcript. Directive stripping only applies to the **current message** section so history remains intact. Channels that wrap history should set `CommandBody` (or `RawBody`) to the original message text and keep `Body` as the combined prompt. Structured history, reply, forwarded, and channel metadata are rendered as user-role untrusted context blocks during prompt assembly. History buffers are configurable via `messages.groupChat.historyLimit` (global default) and per-channel overrides like `channels.slack.historyLimit` or `channels.telegram.accounts.<id>.historyLimit` (set `0` to disable).

## Queueing and Followups

If a run is already active, inbound messages are steered into the current run by default. `messages.queue` selects whether active-run messages steer, queue for later, collect into one later turn, or interrupt the active run. It is configured via `messages.queue` (and `messages.queue.byChannel`). The default mode is `steer`, with a 500ms debounce for Codex steering batches and followup/collect queues. The four modes are `steer`, `followup`, `collect`, and `interrupt`.

## Channel Run Ownership

Channel plugins may preserve ordering, debounce input, and apply transport backpressure before a message enters the session queue. They should **not** impose a separate timeout around the agent turn itself. Once a message is routed to a session, long-running work is governed by the session, tool, and runtime lifecycle, so all channels report and recover from slow turns consistently.

## Streaming, Chunking, and Batching

Block streaming sends partial replies as the model produces text blocks. Chunking respects channel text limits and avoids splitting fenced code. The key settings are: `agents.defaults.blockStreamingDefault` (`on|off`, default off); `agents.defaults.blockStreamingBreak` (`text_end|message_end`); `agents.defaults.blockStreamingChunk` (`minChars|maxChars|breakPreference`); `agents.defaults.blockStreamingCoalesce` (idle-based batching); and `agents.defaults.humanDelay` (human-like pause between block replies). Channel overrides are `*.blockStreaming` and `*.blockStreamingCoalesce` — non-Telegram channels require an explicit `*.blockStreaming: true`.

## Reasoning Visibility and Tokens

OpenClaw can expose or hide model reasoning. `/reasoning on|off|stream` controls visibility. Reasoning content still counts toward token usage when produced by the model. Telegram supports reasoning stream into a transient draft bubble that is deleted after final delivery; use `/reasoning on` for persistent reasoning output.

## Prefixes, Threading, and Replies

Outbound message formatting is centralized in `messages`. The outbound prefix cascade is `messages.responsePrefix`, `channels.<channel>.responsePrefix`, and `channels.<channel>.accounts.<id>.responsePrefix`, plus `channels.whatsapp.messagePrefix` for the WhatsApp inbound prefix. Reply threading is controlled via `replyToMode` and per-channel defaults.

## Silent Replies

The exact silent token `NO_REPLY` / `no_reply` means "do not deliver a user-visible reply". When a turn also has pending tool media, such as generated TTS audio, OpenClaw strips the silent text but still delivers the media attachment. OpenClaw resolves that behavior by conversation type. Direct conversations never receive `NO_REPLY` prompt guidance; if a direct run accidentally returns a bare silent token, OpenClaw suppresses it instead of rewriting or delivering it. Groups/channels allow silence by default only for automatic group replies, and in `message_tool` visible-reply mode silence means the model does not call `message(action=send)`. Internal orchestration allows silence by default.

OpenClaw also uses silent replies for generic internal runner failures in non-direct chats, so groups/channels do not see gateway error boilerplate. Classified failures with user-facing recovery copy — such as missing auth, rate-limit, or overload notices — can still be delivered. Direct chats show compact failure copy by default; raw runner details are shown only when `/verbose full` is enabled. Defaults live under `agents.defaults.silentReply`, and `surfaces.<id>.silentReply` can override group/internal policy per surface. Bare silent replies are dropped on all surfaces, so parent sessions stay quiet instead of rewriting sentinel text into fallback chatter.

**Source**: OpenClaw documentation — `concepts/messages` (mirror `inbox/openclaw_docs/concepts/messages.md`)
**Last Updated**: 2026-06-22
**Status**: Active
