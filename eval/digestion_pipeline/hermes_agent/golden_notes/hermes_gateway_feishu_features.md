---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - feishu
keywords:
  - feishu interactive cards
  - document comment intelligent reply
  - meeting invitation auto-join
  - feishu media and batching
  - webhook rate limiting
  - feishu deduplication
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/feishu
access_control_group: ["general"]
---

# Hermes Gateway — Feishu / Lark Advanced Features

## Overview

This note documents the **advanced feature surface** of the Hermes Feishu / Lark adapter — everything beyond getting the bot running (covered in the [base setup note](hermes_gateway_feishu_setup.md)). Once connected, the adapter layers on **interactive card actions** (including command approval), **document-comment intelligent reply** (answering `@`-mentions on documents via the `feishu_doc`/`feishu_drive` toolsets), **meeting-invitation auto-join**, inbound/outbound **media support**, markdown-to-post rendering with plain-text fallback, status reactions, **burst protection and batching**, per-IP **webhook rate limiting** with anomaly tracking, WebSocket tuning, and inbound **deduplication** — closing with the full environment-variable reference and the `hermes-feishu` toolset preset. These features turn the bot from a chat relay into a full agent surface: cards drive approvals, doc comments spawn scoped agent sessions, and meeting invites can pull Hermes into a video call.

## Bot Identity

Hermes auto-detects the bot's `open_id` and display name on startup. You only need to set these manually when auto-detection cannot reach the Feishu API, or when your app uses tenant-scoped user IDs:

```bash
FEISHU_BOT_OPEN_ID=ou_xxx     # only when auto-detection fails
FEISHU_BOT_USER_ID=xxx        # required if your app uses sender_id_type=user_id
FEISHU_BOT_NAME=MyBot         # only when auto-detection fails
```

## Bot-to-Bot Messaging

By default Hermes ignores messages from other bots. Enable bot-to-bot messaging to participate in A2A orchestration or receive notifications from other bots in the same group, via `FEISHU_ALLOW_BOTS` (default `none`):

| Value | Behavior |
|-------|----------|
| `none` | Ignore all messages from other bots (default). |
| `mentions` | Accept only when the peer bot @mentions Hermes. |
| `all` | Accept every peer bot message. |

Also configurable as `feishu.allow_bots` in `config.yaml` (env wins). Peer bots do **not** need to be in `FEISHU_ALLOWED_USERS` — that allowlist applies to human senders only. Grant `application:bot.basic_info:read` to display peer bot names; without it, peer bots route correctly but appear as their `open_id`.

## Interactive Card Actions

When users click buttons or interact with interactive cards sent by the bot, the adapter routes these as synthetic `/card` command events:

- Button clicks become: `/card button {"key": "value", ...}`
- The action's `value` payload from the card definition is included as JSON.
- Card actions are deduplicated with a 15-minute window to prevent double processing.

Gateway-driven update prompts use a native Feishu `Yes` / `No` card instead of plain-text replies; when `hermes update --gateway` needs confirmation, the adapter records the answer in Hermes's `.update_response` file and replaces the card inline with a resolved state. Card action events are dispatched with `MessageType.COMMAND`, so they flow through the normal command pipeline.

This is also how **command approval** works — for a dangerous command, the agent sends an interactive card with Allow Once / Session / Always / Deny buttons; the user clicks, and the card-action callback delivers the approval decision back to the agent.

### Required Feishu App Configuration

Interactive cards require **three** configuration steps in the Feishu Developer Console. Missing any of them causes error **200340** when users click card buttons:

1. **Subscribe to the card action event:** In **Event Subscriptions**, add `card.action.trigger`.
2. **Enable the Interactive Card capability:** In **App Features > Bot**, enable the **Interactive Card** toggle.
3. **Configure the Card Request URL (webhook mode only):** In **App Features > Bot > Message Card Request URL**, set the URL to the same endpoint as your event webhook (e.g. `https://your-server:8765/feishu/webhook`). In WebSocket mode this is handled automatically by the SDK.

Without all three steps, Feishu still *sends* cards (sending only needs `im:message:send`), but clicking any button returns error 200340 — the error surfaces only on interaction.

## Document Comment Intelligent Reply

Beyond chat, the adapter can answer `@`-mentions left on **Feishu/Lark documents**. When a user comments on a document (local text selection or whole-doc) and @-mentions the bot, Hermes reads the document plus the surrounding comment thread and posts an LLM reply inline. Powered by the `drive.notice.comment_add_v1` event, the handler:

- Fetches document content and comment timeline in parallel (20 messages for whole-doc threads, 12 for local-selection).
- Runs the agent with the `feishu_doc` + `feishu_drive` toolsets scoped to that single comment session.
- Chunks replies at 4000 chars, posted back as threaded replies.
- Caches per-document sessions for 1 hour (50-message cap) so follow-up comments keep context.

### 3-Tier Access Control

Document-comment replies are **explicit-grant only** — no implicit allow-all mode. Permissions resolve in this order (first match wins, per field):

1. **Exact doc** — rule scoped to a specific document token.
2. **Wildcard** — rule that matches a pattern of docs.
3. **Top-level** — default rule for the workspace.

Two policies are available per rule:

- **`allowlist`** — a static list of users / tenants.
- **`pairing`** — static list ∪ runtime-approved store. Useful for rollouts where moderators can grant access live.

Rules live in `~/.hermes/feishu_comment_rules.json` (pairing grants in `~/.hermes/feishu_comment_pairing.json`) with mtime-cached hot-reload — edits take effect on the next comment event without a gateway restart.

```bash
# Inspect current rules and pairing state
python -m gateway.platforms.feishu_comment_rules status

# Simulate an access check for a specific doc + user
python -m gateway.platforms.feishu_comment_rules check <fileType:fileToken> <user_open_id>

# Manage pairing grants at runtime
python -m gateway.platforms.feishu_comment_rules pairing list
python -m gateway.platforms.feishu_comment_rules pairing add <user_open_id>
python -m gateway.platforms.feishu_comment_rules pairing remove <user_open_id>
```

### Required Feishu App Configuration

On top of the chat/card permissions already granted, add the drive comment event:

- Subscribe to `drive.notice.comment_add_v1` in **Event Subscriptions**.
- Grant the `docs:doc:readonly` and `drive:drive:readonly` scopes so the handler can read document content.

## Meeting Invitation Events

You can invite the Hermes bot into a video meeting the same way you invite a human participant; on the invitation event, Hermes can start an agent turn that attempts to join. Powered by the `vc.bot.meeting_invited_v1` event, the flow is:

- A user invites the bot to a video meeting; Feishu/Lark sends the invitation event.
- Hermes extracts the inviter, meeting topic, and meeting number.
- If the inviter is authorized by the normal gateway allowlist or pairing policy, the agent receives the meeting number and tries to join automatically.
- If the invite is malformed or the agent cannot join, Hermes drops the event or replies to the inviter with a concise explanation.

Invitations lacking both an inviter and a `meeting_no` are ignored.

### Required Feishu App Configuration

On top of the chat/card permissions already granted, add the video-meeting invitation event:

- Subscribe to `vc.bot.meeting_invited_v1` in **Event Subscriptions**.
- Enable the Video Conferencing permission scope prompted by the developer console for that event.
- Keep `im:message` and `im:message:send_as_bot` enabled so Hermes can reply to the inviter.
- Ensure the gateway user allowlist or pairing policy authorizes the inviter. Meeting invitations do not bypass normal gateway access checks.

## Media Support

**Inbound (receiving).** The adapter downloads and caches images (.jpg, .jpeg, .png, .gif, .webp, .bmp), audio (.ogg, .mp3, .wav, .m4a, .aac, .flac, .opus, .webm — small text files auto-extracted), video (.mp4, .mov, .avi, .mkv, .webm, .m4v, .3gp — cached as documents), and files (.pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx, and more — cached as documents). Media from rich-text (post) messages, including inline images and attachments, is also extracted. For small text documents (.txt, .md), content is injected into the message text so the agent can read it without tools.

**Outbound (sending).** Methods: `send` (text/rich post, auto-detected from markdown); `send_image` / `send_image_file` (native image bubble, optional caption); `send_document` (file attachment); `send_voice` (audio as file attachment); `send_video` (native media message); `send_animation` (GIFs downgraded to file attachments — Feishu has no native GIF bubble). Upload routing is automatic by extension: `.ogg`/`.opus` → `opus` audio; `.mp4`/`.mov`/`.avi`/`.m4v` → `mp4` media; `.pdf`/`.doc(x)`/`.xls(x)`/`.ppt(x)` → their document type; everything else → generic stream file.

## Markdown Rendering and Post Fallback

When outbound text contains markdown (headings, bold, lists, code blocks, links, etc.), the adapter sends it as a Feishu **post** message with an embedded `md` tag for rich rendering. If the API rejects the post payload (e.g. unsupported markdown), it falls back to plain text with markdown stripped — this two-stage fallback ensures delivery. Text with no markdown is sent as the simple `text` message type.

## Processing Status Reactions

While the agent works, the bot shows a `Typing` reaction on your message, cleared when the reply arrives or replaced with `CrossMark` on failure. Set `FEISHU_REACTIONS=false` to disable.

## Burst Protection and Batching

The adapter debounces rapid message bursts to avoid overwhelming the agent.

**Text batching** — multiple text messages in quick succession are merged into one event: quiet period `HERMES_FEISHU_TEXT_BATCH_DELAY_SECONDS` (0.6s), max messages `HERMES_FEISHU_TEXT_BATCH_MAX_MESSAGES` (8), max characters `HERMES_FEISHU_TEXT_BATCH_MAX_CHARS` (4000).

**Media batching** — multiple attachments in quick succession (e.g. dragging several images) are merged into one event: quiet period `HERMES_FEISHU_MEDIA_BATCH_DELAY_SECONDS` (0.8s).

**Per-chat serialization** — messages in the same chat are processed serially (each chat has its own lock); different chats run concurrently.

## Rate Limiting (Webhook Mode)

In webhook mode, the adapter enforces per-IP rate limiting to protect against abuse:

- **Window:** 60-second sliding window
- **Limit:** 120 requests per window per (app_id, path, IP) triple
- **Tracking cap:** up to 4096 unique keys tracked (prevents unbounded memory growth)

Requests that exceed the limit receive HTTP 429 (Too Many Requests).

**Webhook anomaly tracking** — the adapter tracks consecutive error responses per IP; after 25 consecutive errors from the same IP within a 6-hour window, a warning is logged, helping detect misconfigured clients or probing. Additional protections: body size limit 1 MB, body read timeout 30s, and Content-Type enforcement (only `application/json`).

## WebSocket Tuning

When using `websocket` mode, you can customize reconnect and ping behavior under `platforms.feishu.extra` in `config.yaml`:

```yaml
platforms:
  feishu:
    extra:
      ws_reconnect_interval: 120   # Seconds between reconnect attempts (default: 120)
      ws_ping_interval: 30         # Seconds between WebSocket pings (optional; SDK default if unset)
```

`ws_reconnect_interval` (default 120s) sets the wait between reconnection attempts; `ws_ping_interval` (SDK default if unset) sets the keepalive ping frequency.

## Deduplication

Inbound messages are deduplicated using message IDs with a 24-hour TTL. The dedup state is persisted across restarts to `~/.hermes/feishu_seen_message_ids.json`. The cache size is controlled by `HERMES_FEISHU_DEDUP_CACHE_SIZE` (default 2048 entries).

## All Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FEISHU_APP_ID` | ✅ | — | Feishu/Lark App ID |
| `FEISHU_APP_SECRET` | ✅ | — | Feishu/Lark App Secret |
| `FEISHU_DOMAIN` | — | `feishu` | `feishu` (China) or `lark` (international) |
| `FEISHU_CONNECTION_MODE` | — | `websocket` | `websocket` or `webhook` |
| `FEISHU_ALLOWED_USERS` | — | _(empty)_ | Comma-separated open_id list for user allowlist |
| `FEISHU_ALLOW_BOTS` | — | `none` | Accept messages from other bots: `none`, `mentions`, or `all` |
| `FEISHU_REQUIRE_MENTION` | — | `true` | Whether group messages must @mention the bot |
| `FEISHU_HOME_CHANNEL` | — | — | Chat ID for cron/notification output |
| `FEISHU_ENCRYPT_KEY` | — | _(empty)_ | Encrypt key for webhook signature verification |
| `FEISHU_VERIFICATION_TOKEN` | — | _(empty)_ | Verification token for webhook payload auth |
| `FEISHU_GROUP_POLICY` | — | `allowlist` | Group message policy: `open`, `allowlist`, `disabled` |
| `FEISHU_BOT_OPEN_ID` | — | _(empty)_ | Bot's open_id (for @mention detection) |
| `FEISHU_BOT_USER_ID` | — | _(empty)_ | Bot's user_id (for @mention detection) |
| `FEISHU_BOT_NAME` | — | _(empty)_ | Bot's display name (for @mention detection) |
| `FEISHU_WEBHOOK_HOST` | — | `127.0.0.1` | Webhook server bind address |
| `FEISHU_WEBHOOK_PORT` | — | `8765` | Webhook server port |
| `FEISHU_WEBHOOK_PATH` | — | `/feishu/webhook` | Webhook endpoint path |
| `HERMES_FEISHU_DEDUP_CACHE_SIZE` | — | `2048` | Max deduplicated message IDs to track |
| `HERMES_FEISHU_TEXT_BATCH_DELAY_SECONDS` | — | `0.6` | Text burst debounce quiet period |
| `HERMES_FEISHU_TEXT_BATCH_MAX_MESSAGES` | — | `8` | Max messages merged per text batch |
| `HERMES_FEISHU_TEXT_BATCH_MAX_CHARS` | — | `4000` | Max characters merged per text batch |
| `HERMES_FEISHU_MEDIA_BATCH_DELAY_SECONDS` | — | `0.8` | Media burst debounce quiet period |

WebSocket and per-group ACL settings are configured via `config.yaml` under `platforms.feishu.extra` (see [WebSocket Tuning](#websocket-tuning) above and Per-Group Access Control in the [base setup note](hermes_gateway_feishu_setup.md)).

## Toolset

Feishu / Lark uses the `hermes-feishu` platform preset, which includes the same core tools as Telegram and other gateway-based messaging platforms. The document-comment handler additionally scopes the `feishu_doc` and `feishu_drive` toolsets to each comment session.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/feishu.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/feishu
**Last Updated**: 2026-06-19
**Status**: Active
