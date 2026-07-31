---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - whatsapp
keywords:
  - whatsapp runtime model
  - baileys reconnect watchdog
  - web.whatsapp socket timings
  - whatsapp session scoping
  - inbound envelope media normalization
  - text chunking textChunkLimit
  - ptt ogg opus voice note
  - reply quoting replyToMode
  - ack reaction reactionLevel
  - lifecycle status reactions
topics:
  - OpenClaw
  - WhatsApp Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/channels/whatsapp
access_control_group: ["general"]
---

# OpenClaw — WhatsApp Runtime and Delivery Behavior Model

## Overview

This note models the WhatsApp (Baileys / WhatsApp Web) channel's runtime and delivery behavior in OpenClaw: who owns the socket, how the reconnect watchdog and `web.whatsapp.*` timings keep a linked-device session alive, how inbound DM/group/newsletter sessions are scoped, how inbound messages are normalized into the shared envelope (reply context, media placeholders, transcription, pending group-history injection, read receipts), and how outbound replies are chunked, delivered as media/PTT voice notes, quoted, and surfaced through the single per-message reaction slot (ack, reaction level, and lifecycle status reactions). It mirrors the runtime-behavior half of the `channels/whatsapp` source page (the Runtime model, Message normalization and context, Delivery/chunking/media, Reply quoting, Reaction level, Acknowledgment reactions, and Lifecycle status reactions sections); the on-demand install / access-policy onboarding and the operations/troubleshooting playbook are split into the sibling setup and operations notes.

## Runtime Model: Socket Ownership, Reconnect Watchdog, and Session Scoping

The Gateway owns the WhatsApp socket and reconnect loop. The reconnect watchdog uses WhatsApp Web transport activity, not only inbound app-message volume, so a quiet linked-device session is not restarted solely because nobody has sent a message recently; quiet linked-device sessions stay up while transport frames continue, but a transport stall forces reconnect well before the later remote disconnect path. A longer application-silence cap still forces a reconnect if transport frames keep arriving but no application messages are handled for the watchdog window; after a transient reconnect for a recently active session, that application-silence check uses the normal message timeout for the first recovery window.

Baileys socket timings are explicit under `web.whatsapp.*`: `keepAliveIntervalMs` controls WhatsApp Web application pings, `connectTimeoutMs` controls the opening handshake timeout, and `defaultQueryTimeoutMs` controls Baileys query waits plus OpenClaw's local outbound send/presence and inbound read-receipt operation bounds. WhatsApp Web transport honors standard proxy environment variables on the gateway host (`HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY` / lowercase variants), and OpenClaw prefers host-level proxy config over channel-specific WhatsApp proxy settings.

Outbound sends require an active WhatsApp listener for the target account. Group sends attach native mention metadata for `@+<digits>` and `@<digits>` tokens in text and media captions when the token matches current WhatsApp participant metadata, including LID-backed groups. Status and broadcast chats are ignored (`@status`, `@broadcast`). Session scoping is by chat kind: direct chats use DM session rules (`session.dmScope`; default `main` collapses DMs to the agent main session), group sessions are isolated as `agent:<agentId>:whatsapp:group:<jid>`, and WhatsApp Channels/Newsletters can be explicit outbound targets with their native `@newsletter` JID — outbound newsletter sends use channel session metadata (`agent:<agentId>:whatsapp:channel:<jid>`) rather than DM session semantics. When `messages.removeAckAfterReply` is enabled, OpenClaw clears the WhatsApp ack reaction after a visible reply is delivered.

## Message Normalization and Context

Incoming WhatsApp messages are wrapped in the shared inbound envelope. If a quoted reply exists, context is appended in this form, and reply metadata fields are also populated when available (`ReplyToId`, `ReplyToBody`, `ReplyToSender`, sender JID/E.164):

```text
[Replying to <sender> id:<stanzaId>]
<quoted body or media placeholder>
[/Replying]
```

When the quoted reply target is downloadable media, OpenClaw saves it through the normal inbound media store and exposes it as `MediaPath`/`MediaType` so the agent can inspect the referenced image instead of only seeing `<media:image>`. Media-only inbound messages are normalized with placeholders: `<media:image>`, `<media:video>`, `<media:audio>`, `<media:document>`, and `<media:sticker>`. Authorized group voice notes are transcribed before mention gating when the body is only `<media:audio>`, so saying the bot mention in the voice note can trigger the reply; if the transcript still does not mention the bot, the transcript is kept in pending group history instead of the raw placeholder. Location bodies use terse coordinate text, and location labels/comments and contact/vCard details are rendered as fenced untrusted metadata, not inline prompt text.

For groups, unprocessed messages can be buffered and injected as context when the bot is finally triggered: the default limit is `50`, configured via `channels.whatsapp.historyLimit` with fallback `messages.groupChat.historyLimit`, and `0` disables it. The injected context uses the markers `[Chat messages since your last reply - for context]` and `[Current message - respond to this]`. Read receipts are enabled by default for accepted inbound WhatsApp messages, can be disabled globally via `channels.whatsapp.sendReadReceipts: false` (or per-account under `accounts.<id>.sendReadReceipts`), and self-chat turns skip read receipts even when globally enabled.

## Delivery, Chunking, and Media

Outbound text chunking has a default limit of `channels.whatsapp.textChunkLimit = 4000`, with `channels.whatsapp.chunkMode = "length" | "newline"` — `newline` mode prefers paragraph boundaries (blank lines), then falls back to length-safe chunking. Outbound media supports image, video, audio (PTT voice-note), and document payloads. Audio media is sent through the Baileys `audio` payload with `ptt: true`, so WhatsApp clients render it as a push-to-talk voice note; reply payloads preserve `audioAsVoice`, and TTS voice-note output for WhatsApp stays on this PTT path even when the provider returns MP3 or WebM. Native Ogg/Opus audio is sent as `audio/ogg; codecs=opus` for voice-note compatibility, and non-Ogg audio — including Microsoft Edge TTS MP3/WebM output — is transcoded with `ffmpeg` to 48 kHz mono Ogg/Opus before PTT delivery. The `/tts latest` command sends the latest assistant reply as one voice note and suppresses repeat sends for the same reply, while `/tts chat on|off|default` controls auto-TTS for the current WhatsApp chat.

Animated GIF playback is supported via `gifPlayback: true` on video sends. The `forceDocument` / `asDocument` options send outbound images, GIFs, and videos through the Baileys document payload to avoid WhatsApp media compression while preserving the resolved filename and MIME type. Captions are applied to the first media item when sending multi-media reply payloads, except PTT voice notes send the audio first and visible text separately because WhatsApp clients do not render voice-note captions consistently. Media source can be HTTP(S), `file://`, or local paths.

Media size limits are governed by `channels.whatsapp.mediaMaxMb` (default `50`) for both the inbound media save cap and the outbound media send cap, with per-account overrides at `channels.whatsapp.accounts.<accountId>.mediaMaxMb`. Images are auto-optimized (resize/quality sweep) to fit limits unless `forceDocument` / `asDocument` requests document delivery. On media send failure, the first-item fallback sends a text warning instead of dropping the response silently.

## Reply Quoting

WhatsApp supports native reply quoting, where outbound replies visibly quote the inbound message, controlled by `channels.whatsapp.replyToMode`. The default is `"off"`, and per-account overrides use `channels.whatsapp.accounts.<id>.replyToMode`. The four modes are:

| Value       | Behavior                                                              |
| ----------- | --------------------------------------------------------------------- |
| `"off"`     | Never quote; send as a plain message                                  |
| `"first"`   | Quote only the first outbound reply chunk                             |
| `"all"`     | Quote every outbound reply chunk                                      |
| `"batched"` | Quote queued batched replies while leaving immediate replies unquoted |

## Reaction Level

`channels.whatsapp.reactionLevel` controls how broadly the agent uses emoji reactions on WhatsApp; the default is `"minimal"`, and per-account overrides use `channels.whatsapp.accounts.<id>.reactionLevel`. The four levels gate ack reactions (pre-reply receipts) and agent-initiated reactions independently:

| Level         | Ack reactions | Agent-initiated reactions | Description                                      |
| ------------- | ------------- | ------------------------- | ------------------------------------------------ |
| `"off"`       | No            | No                        | No reactions at all                              |
| `"ack"`       | Yes           | No                        | Ack reactions only (pre-reply receipt)           |
| `"minimal"`   | Yes           | Yes (conservative)        | Ack + agent reactions with conservative guidance |
| `"extensive"` | Yes           | Yes (encouraged)          | Ack + agent reactions with encouraged guidance   |

## Acknowledgment Reactions

WhatsApp supports immediate ack reactions on inbound receipt via `channels.whatsapp.ackReaction`. Ack reactions are gated by `reactionLevel` — they are suppressed when `reactionLevel` is `"off"`. A representative config sets the emoji and the direct/group eligibility (`group` accepts `always | mentions | never`):

```json5
{
  channels: {
    whatsapp: {
      ackReaction: {
        emoji: "👀",
        direct: true,
        group: "mentions", // always | mentions | never
      },
    },
  },
}
```

Ack reactions are sent immediately after inbound is accepted (pre-reply). If `ackReaction` is present without `emoji`, WhatsApp uses the routed agent's identity emoji, falling back to `👀`; omitting `ackReaction` or setting `emoji: ""` sends no ack reaction. Failures are logged but do not block normal reply delivery. In group mode `mentions`, the ack reacts on mention-triggered turns, and group activation `always` acts as a bypass for this check. WhatsApp uses `channels.whatsapp.ackReaction` here (legacy `messages.ackReaction` is not used).

## Lifecycle Status Reactions

Setting `messages.statusReactions.enabled: true` lets WhatsApp replace the ack reaction during a turn instead of leaving a static receipt emoji. When enabled, OpenClaw uses the same inbound message reaction slot for lifecycle states such as queued, thinking, tool activity, compaction, done, and error:

```json5
{
  messages: {
    statusReactions: {
      enabled: true,
      emojis: {
        deploy: "🛫",
        build: "🏗️",
        concierge: "💁",
      },
    },
  },
}
```

The behavior is constrained by the single reaction slot: `channels.whatsapp.ackReaction` still controls whether status reactions are eligible for direct messages and groups, and the queued status reaction uses the same effective ack emoji as plain ack reactions. WhatsApp has one bot reaction slot per message, so lifecycle updates replace the current reaction in place. `messages.removeAckAfterReply: true` clears the final status reaction after the configured done/error hold. Tool emoji categories include `tool`, `coding`, `web`, `deploy`, `build`, and `concierge`.

**Source**: OpenClaw documentation — `channels/whatsapp` (mirror `inbox/openclaw_docs/channels/whatsapp.md`)
**Last Updated**: 2026-06-22
**Status**: Active
