---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - telegram
keywords:
  - openclaw telegram features
  - telegram live stream preview streaming
  - telegram rich messages richMessages
  - telegram native commands setMyCommands
  - telegram inline buttons reactions stickers
  - channels.telegram configuration reference
  - telegram errorPolicy errorCooldownMs
  - telegram polling network troubleshooting
topics:
  - OpenClaw
  - Telegram Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/telegram
access_control_group: ["general"]
---

# OpenClaw — Telegram Feature, Config, and Troubleshooting Reference

## Overview

This note is the Telegram runtime-feature, configuration, and troubleshooting reference for the OpenClaw `channels/telegram` page (its second half: **Feature reference**, **Error reply controls**, **Troubleshooting**, **Configuration reference**). It covers live-preview streaming, rich-message formatting, native/custom commands, inline buttons / reactions / stickers, forum-topic threading, error-reply controls, and the full `channels.telegram.*` field surface. The setup, access-control, and runtime-routing procedure lives in the sibling note [oc_channels_telegram_setup](oc_channels_telegram_setup.md).

## Live stream preview (message edits)

OpenClaw streams partial replies by posting a preview message and updating it with `editMessageText` in direct chats, groups, and topics. `channels.telegram.streaming` is `off | partial | block | progress` (default `partial`); `progress` keeps one editable status draft for tool progress, clears it at completion, and sends the final answer as a normal message. `streaming.preview.toolProgress` controls whether tool/progress updates reuse the same edited preview message (default `true` when preview streaming is active). `streaming.preview.commandText`: `raw` (default) or `status` (tool label only) for command/exec detail in tool-progress lines. `streaming.progress.commentary` (default `false`) opts assistant commentary/preamble into the progress draft. Legacy `streamMode`, boolean `streaming` values, and retired native-draft preview keys are detected — run `openclaw doctor --fix` to migrate. Tool-progress preview updates are on by default (released behavior `v2026.4.22`+); to hide tool-progress lines set `streaming.preview.toolProgress: false`, or hide command/exec text via `streaming.preview.commandText: "status"`. `streaming.mode: "off"` gives final-only delivery: preview edits disabled and tool/progress chatter suppressed (approval prompts, media, errors still use normal delivery). For text-only replies, short previews edit in place; long finals reuse the preview as the first chunk then send the rest; progress-mode finals clear the draft; a failed final edit or a complex reply (e.g. media) falls back to normal delivery and cleans up the stale preview. Preview streaming is separate from block streaming — when block streaming is explicitly enabled, the preview stream is skipped. **Selected quote-reply exception**: when `replyToMode` is `"first"`, `"all"`, or `"batched"` and the inbound message includes selected quote text, OpenClaw uses Telegram's native quote-reply path instead of editing the preview, so `streaming.preview.toolProgress` cannot show status lines that turn. `/reasoning stream` streams reasoning into the preview then deletes it after delivery; `/reasoning on` keeps reasoning visible.

## Rich message formatting

Outbound text uses standard Telegram **HTML** by default (bold, italic, links, code, spoilers, quotes) but not Bot API 10.1 rich-only blocks (native tables, details, rich media, formulas). `channels.telegram.richMessages: true` opts into Bot API 10.1 rich messages: Markdown renders through OpenClaw's Markdown IR as rich HTML, explicit rich-HTML payloads preserve supported 10.1 tags (headings, tables, details, rich media, formulas), and media captions still use HTML. This keeps model text away from Rich Markdown sigils (e.g. `$400-600K` is not parsed as math); long rich text splits across rich-text/rich-block limits; tables over the column limit become code blocks. Default off for client compatibility (some clients show accepted rich messages as unsupported); keep disabled unless every client can render them. `/status` shows session rich-message state. Link previews are on by default; `channels.telegram.linkPreview: false` skips automatic entity detection.

## Native commands and custom commands

Command-menu registration happens at startup via `setMyCommands`; `commands.native: "auto"` enables native commands. Custom menu entries go under `channels.telegram.customCommands` (`command` + `description`); names are normalized (strip leading `/`, lowercase), valid pattern `a-z`, `0-9`, `_`, length `1..32`, cannot override native commands, conflicts/duplicates skipped+logged. Custom commands are menu entries only (no behavior); plugin/skill commands still work when typed even if not shown. Disabling native commands removes built-ins but custom/plugin commands may still register. Common failures: `BOT_COMMANDS_TOO_MUCH` = menu overflowed after trimming (reduce commands or disable `commands.native`); `404: Not Found` on `deleteWebhook`/`deleteMyCommands`/`setMyCommands` while direct curl works = `apiRoot` set to the full `/bot<TOKEN>` endpoint (must be Bot API root only; `openclaw doctor --fix` removes a trailing `/bot<TOKEN>`); `getMe returned 401` = token rejected. **Device pairing** (`device-pair` plugin): `/pair` generates a setup code, `/pair pending` lists pending requests (role/scopes), `/pair approve <requestId>` (or `/pair approve [latest]`) approves. The bootstrap token is node-only — first connect creates a pending node request; after approval the Gateway returns a durable node token with `scopes: []`, not an operator token.

## Inline buttons, reactions, stickers, and message actions

**Inline buttons**: `channels.telegram.capabilities.inlineButtons` scopes inline keyboards to `off | dm | group | all | allowlist` (default `allowlist`); legacy `capabilities: ["inlineButtons"]` maps to `"all"`. A send action supplies `buttons` (rows of `{ text, callback_data }`); Mini App buttons use `web_app: { url }` (private chats only); callback clicks reach the agent as text `callback_data: <value>`.

**Tool actions**: `sendMessage` (`to`, `content`, optional `mediaUrl`, `replyToMessageId`, `messageThreadId`), `react` (`chatId`, `messageId`, `emoji`), `deleteMessage` (`chatId`, `messageId`), `editMessage` (`chatId`, `messageId`, `content`/`caption`, optional `presentation` buttons — button-only edits update reply markup), `createForumTopic` (`chatId`, `name`, optional `iconColor`, `iconCustomEmojiId`). Aliases: `send`, `react`, `delete`, `edit`, `sticker`, `sticker-search`, `topic-create`. Gating: `actions.sendMessage`, `.deleteMessage`, `.reactions`, `.sticker` (default disabled); `edit` and `topic-create` are on by default (no separate toggle). Runtime sends use the active config/secrets snapshot — no per-send SecretRef re-resolution.

**Audio/video/stickers**: voice notes vs audio files (default audio-file; `[[audio_as_voice]]` forces voice-note; inbound voice-note transcripts are framed as machine-generated untrusted text, mention detection on the raw transcript); video files vs video notes (`asVideoNote: true`; video notes have no captions, text sent separately). Inbound stickers: static WEBP downloaded/processed (placeholder `<media:sticker>`), animated TGS and video WEBM skipped; context fields `Sticker.emoji`, `.setName`, `.fileId`, `.fileUniqueId`, `.cachedDescription` (cached in SQLite plugin state). Enable with `actions.sticker: true`; send via `action: "sticker"` (`fileId`) or `"sticker-search"` (`query`, `limit`).

**Reaction notifications**: reactions arrive as separate `message_reaction` updates. `channels.telegram.reactionNotifications`: `off | own | all` (default `own`); `reactionLevel`: `off | ack | minimal | extensive` (default `minimal`). `own` = user reactions to bot-sent messages only; events still respect access controls (`dmPolicy`, `allowFrom`, `groupPolicy`, `groupAllowFrom`). No thread IDs are given, so forum groups route to the general-topic session (`:topic:1`), not the originating topic. `allowed_updates` include `message_reaction` automatically.

**Ack reactions**: `ackReaction` sends an acknowledgement emoji while processing; `ackReactionScope` decides when. Emoji resolution: `accounts.<accountId>.ackReaction` → `channels.telegram.ackReaction` → `messages.ackReaction` → agent identity emoji (`agents.list[].identity.emoji`, else `"👀"`); `""` disables. Scope reads from `messages.ackReactionScope` (default `"group-mentions"`; no per-account/channel override): `"all"`, `"direct"`, `"group-all"`, `"group-mentions"` (default; **no DMs**), `"off"`/`"none"`. For an ack on inbound DMs set scope `"direct"`/`"all"`; read at provider startup, so a restart is needed.

## Reply threading, forum topics, and config writes

**Reply threading tags**: `[[reply_to_current]]` replies to the triggering message; `[[reply_to:<id>]]` to a specific message ID. `channels.telegram.replyToMode`: `off` (default) | `first` | `all`. When threading is enabled and the original text/caption is available, OpenClaw adds a native Telegram quote excerpt (capped at 1024 UTF-16 code units; longer messages quote from the start, falling back to a plain reply if rejected). `off` disables implicit threading but explicit `[[reply_to_*]]` tags are still honored.

**Forum topics**: topic session keys append `:topic:<threadId>`; replies and typing target the topic thread; config path `channels.telegram.groups.<chatId>.topics.<threadId>`. General topic (`threadId=1`) special-case: sends omit `message_thread_id` (Telegram rejects `sendMessage(...thread_id=1)`) while typing still includes it. Topic entries inherit group settings unless overridden (`requireMention`, `allowFrom`, `skills`, `systemPrompt`, `enabled`, `groupPolicy`); `agentId` is topic-only; `topics."*"` sets per-topic defaults while exact IDs win. Each topic can route to a different agent via `agentId` with its own session key (e.g. `agent:zu:telegram:group:-1001234567890:topic:3`). Persistent ACP topic binding pins ACP sessions via top-level typed `bindings[]` (`type: "acp"`, `match.channel: "telegram"`, `peer.kind: "group"`, topic-qualified id); `/acp spawn <agent> --thread here|auto` binds the current topic to a new ACP session (needs `channels.telegram.threadBindings.spawnSessions`, default `true`). Template context exposes `MessageThreadId` and `IsForum`; the former `dm.threadReplies` / `direct.*.threadReplies` overrides are retired (use BotFather threaded mode).

**Config writes**: on by default (`configWrites !== false`); Telegram-triggered writes include group migration events (`migrate_to_chat_id`) and `/config set` / `/config unset` (needs command enablement). Disable with `channels.telegram.configWrites: false`.

## Limits, retry, CLI targets, and exec approvals

Defaults: `textChunkLimit` `4000`; `chunkMode="newline"` prefers paragraph boundaries before length splitting; `mediaMaxMb` `100` caps inbound/outbound media; `mediaGroupFlushMs` `500` buffers albums/media groups into one inbound message; `timeoutSeconds` overrides the API client timeout (clamped below the 60s outbound text/typing guard; long polling uses a 45s `getUpdates` guard); `pollingStallThresholdMs` `120000` (tune `30000`–`600000` only for false-positive stall restarts); group history `historyLimit` or `messages.groupChat.historyLimit` (`50`, `0` disables); DM history `dmHistoryLimit`, `dms["<user_id>"].historyLimit`. `channels.telegram.retry` covers send helpers for recoverable outbound errors; inbound final-reply uses a bounded safe-send retry for pre-connect failures but does not retry ambiguous post-send envelopes (avoiding duplicate messages). **Exec approvals**: `execApprovals.enabled` (auto-enables when an approver is resolvable), `.approvers` (falls back to numeric owner IDs from `commands.ownerAllowFrom`), `.target`: `dm` (default) | `channel` | `both`, plus `agentFilter`/`sessionFilter`; approvers must be numeric IDs; channel delivery shows the command text (use `channel`/`both` only in trusted groups/topics); inline approval buttons require `capabilities.inlineButtons`; approvals expire after 30 minutes by default; IDs prefixed `plugin:` resolve through plugin approvals, others exec approvals first. **Long-polling vs webhook**: default long polling; webhook mode sets `webhookUrl` + `webhookSecret` (optional `webhookPath`, `webhookHost`, `webhookPort`, defaults `/telegram-webhook`, `127.0.0.1`, `8787`). CLI/message-tool targets: numeric chat ID, `@name`, or a `:topic:` target:

```bash
openclaw message poll --channel telegram --target -1001234567890:topic:42 \
  --poll-question "Pick a time" --poll-option "10am" --poll-option "2pm" --poll-public
```

Telegram-only poll flags: `--poll-duration-seconds` (5-600), `--poll-anonymous`, `--poll-public`, `--thread-id`. Send also supports `--presentation` (`buttons` blocks, gated by `capabilities.inlineButtons`), `--pin` / `--delivery '{"pin":true}'`, `--force-document`. Gating: `actions.sendMessage=false` disables outbound messages (incl. polls); `actions.poll=false` disables poll creation while leaving sends enabled.

## Error reply controls

When the agent hits a delivery or provider error, Telegram either replies with the error text or suppresses it, via two keys. `channels.telegram.errorPolicy` (`reply` | `silent`, default `reply`): `reply` sends a friendly error message; `silent` suppresses error replies. `channels.telegram.errorCooldownMs` (ms, default `60000`): minimum time between error replies to the same chat, preventing spam during outages. Per-account, per-group, and per-topic overrides are supported.

## Troubleshooting

- **No response to non-mention group messages**: with `requireMention=false`, privacy mode must allow full visibility — BotFather `/setprivacy` → Disable, then remove + re-add the bot; `openclaw channels status` warns when config expects unmentioned messages; `--probe` checks explicit numeric group IDs (wildcard `"*"` cannot be probed); session test `/activation always`.
- **Bot not seeing group messages at all**: when `channels.telegram.groups` exists the group must be listed (or `"*"`); verify membership; check `openclaw logs --follow` for skip reasons.
- **Commands work partially or not at all**: authorize the sender (pairing and/or numeric `allowFrom`); command authorization applies even when group policy is `open`; `BOT_COMMANDS_TOO_MUCH` = too many native menu entries (reduce commands or disable native menus); `deleteMyCommands`/`setMyCommands`/`sendChatAction` retry once via transport fallback on timeout, and persistent network/fetch errors usually mean DNS/HTTPS reachability issues to `api.telegram.org`.
- **Startup reports unauthorized token**: `getMe returned 401` is an auth failure — re-copy/regenerate the BotFather token and update `botToken`, `tokenFile`, `accounts.<id>.botToken`, or `TELEGRAM_BOT_TOKEN`; `deleteWebhook 401 Unauthorized` at startup is also an auth failure.
- **Polling/network instability**: Node 22+ with custom fetch/proxy can abort on AbortSignal type mismatch; broken IPv6 egress (hosts resolving `api.telegram.org` to IPv6 first) causes intermittent failures; `TypeError: fetch failed` / `Network request for 'getUpdates' failed!` are retried; `Polling stall detected` rebuilds the transport after 120s without long-poll liveness. Proxy env: `HTTP_PROXY`/`HTTPS_PROXY`/`ALL_PROXY` (+ lowercase), `OPENCLAW_PROXY_URL`, or `channels.telegram.proxy: socks5://...`. DNS order honors `OPENCLAW_TELEGRAM_DNS_RESULT_ORDER` → `network.dnsResultOrder` → process default (Node 22+ falls back to `ipv4first`); force IPv4 with `network.autoSelectFamily: false`. `network.dangerouslyAllowPrivateNetwork: true` weakens media SSRF protection (only for trusted fake-IP proxies outside the already-allowed RFC 2544 `198.18.0.0/15` range).

## Configuration reference

Primary reference: [Configuration reference - Telegram](https://docs.openclaw.ai/gateway/config-channels#telegram). High-signal `channels.telegram.*` fields by group:

- startup/auth — `enabled`, `botToken`, `tokenFile` (regular file only; symlinks rejected), `accounts.*`, `apiRoot` (Bot API root only; no `/bot<TOKEN>`)
- access control — `dmPolicy`, `allowFrom`, `groupPolicy`, `groupAllowFrom`, `groups`, `groups.*.topics.*`, `groups.<chatId>.topics."*"`, top-level `bindings[]` (`type: "acp"`)
- exec approvals — `execApprovals`, `accounts.*.execApprovals`; command/menu — `commands.native`, `commands.nativeSkills`, `customCommands`; threading — `replyToMode`
- streaming — `streaming`, `streaming.preview.toolProgress`, `blockStreaming`; formatting — `textChunkLimit`, `chunkMode`, `richMessages`, `linkPreview`, `responsePrefix`
- media/network — `mediaMaxMb`, `mediaGroupFlushMs`, `timeoutSeconds`, `pollingStallThresholdMs`, `retry`, `network.autoSelectFamily`, `network.dangerouslyAllowPrivateNetwork`, `proxy`
- webhook — `webhookUrl`, `webhookSecret`, `webhookPath`, `webhookHost`; actions — `capabilities.inlineButtons`, `actions.sendMessage|editMessage|deleteMessage|reactions|sticker`
- reactions — `reactionNotifications`, `reactionLevel`; errors — `errorPolicy`, `errorCooldownMs`; writes/history — `configWrites`, `historyLimit`, `dmHistoryLimit`, `dms.*.historyLimit`

Multi-account precedence: with two or more account IDs, set `channels.telegram.defaultAccount` (or `channels.telegram.accounts.default`) for explicit default routing — otherwise OpenClaw falls back to the first normalized account ID and `openclaw doctor` warns; named accounts inherit `allowFrom` / `groupAllowFrom` but not `accounts.default.*`.

**Source**: OpenClaw documentation — `channels/telegram` (mirror `inbox/openclaw_docs/channels/telegram.md`)
**Last Updated**: 2026-06-22
**Status**: Active
