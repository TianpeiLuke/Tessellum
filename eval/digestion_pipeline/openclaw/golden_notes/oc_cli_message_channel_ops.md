---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - message
keywords:
  - openclaw message channel operations
  - openclaw message react reactions read edit delete
  - openclaw message pin unpin pins permissions search
  - discord thread create list reply
  - discord emoji sticker role member voice event
  - discord moderation timeout kick ban
  - per-channel action support matrix
topics:
  - OpenClaw
  - CLI message channel actions
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/message
access_control_group: ["general"]
---

# OpenClaw — `openclaw message` Channel-Operations Catalog

## Overview

This note documents the channel-operations half of the single `openclaw message` command — every action beyond the outbound `send` / `poll` / `broadcast` flow (those, plus channel selection, target formats, common flags, SecretRef behavior, and the worked send/presentation examples, live in the sibling note `oc_cli_message_send`). It mirrors the Core action catalog (`react`, `reactions`, `read`, `edit`, `delete`, `pin` / `unpin`, `pins`, `permissions`, `search`) and the Discord-centric `Threads`, `Emojis`, `Stickers`, `Roles / Channels / Members / Voice`, `Events`, and `Moderation` sections of the `cli/message` source page. Each action carries a per-channel support list and a required/optional flag set; this note reproduces those verbatim so an operator knows which action works on which channel and what flags it needs.

These actions inherit the same invocation shape (`openclaw message <subcommand> [flags]`), channel selection (`--channel`), per-channel target formats (`--target`), and SecretRef resolution as `send` — see `oc_cli_message_send` for that shared contract. The action availability is heavily Discord-weighted: reactions and read span many channels, but threads, emojis, stickers, roles/members/voice, events, and moderation are Discord-only on this surface.

## Core Actions (beyond send/poll)

These actions operate on existing messages or channel state. Each lists the channels that support it and its required/optional flags exactly as the source page declares.

- **`react`** — Channels: Discord/Google Chat/Matrix/Nextcloud Talk/Signal/Slack/Telegram/WhatsApp. Required: `--message-id`, `--target`. Optional: `--emoji`, `--remove`, `--participant`, `--from-me`, `--target-author`, `--target-author-uuid`. `--remove` requires `--emoji` (omit `--emoji` to clear own reactions where supported; see `/tools/reactions`). WhatsApp only: `--participant`, `--from-me`. Signal group reactions require `--target-author` or `--target-author-uuid`. Nextcloud Talk supports adding reactions only; `--remove` is rejected with a clear error.
- **`reactions`** — Channels: Discord/Google Chat/Slack/Matrix. Required: `--message-id`, `--target`. Optional: `--limit`.
- **`read`** — Channels: Discord/Slack/Matrix. Required: `--target`. Optional: `--limit`, `--message-id`, `--before`, `--after`. Slack only: `--message-id` reads a specific Slack message timestamp; combine with `--thread-id` to read an exact thread reply. Discord only: `--around`.
- **`edit`** — Channels: Discord/Slack/Matrix. Required: `--message-id`, `--message`, `--target`.
- **`delete`** — Channels: Discord/Slack/Telegram/Matrix. Required: `--message-id`, `--target`.
- **`pin` / `unpin`** — Channels: Discord/Slack/Matrix. Required: `--message-id`, `--target`.
- **`pins`** (list) — Channels: Discord/Slack/Matrix. Required: `--target`.
- **`permissions`** — Channels: Discord/Matrix. Required: `--target`. Matrix only: available when Matrix encryption is enabled and verification actions are allowed.
- **`search`** — Channels: Discord. Required: `--guild-id`, `--query`. Optional: `--channel-id`, `--channel-ids` (repeat), `--author-id`, `--author-ids` (repeat), `--limit`.

A worked reaction example (the only channel-ops example reproduced on the source page) shows `react` against a Slack message and against a Signal group with the required author flag:

```
openclaw message react --channel slack \
  --target C123 --message-id 456 --emoji "✅"

openclaw message react --channel signal \
  --target signal:group:abc123 --message-id 1737630212345 \
  --emoji "✅" --target-author-uuid 123e4567-e89b-12d3-a456-426614174000
```

## Threads (Discord)

Thread management is Discord-only and split across three subcommands:

- **`thread create`** — Channels: Discord. Required: `--thread-name`, `--target` (channel id). Optional: `--message-id`, `--message`, `--auto-archive-min`.
- **`thread list`** — Channels: Discord. Required: `--guild-id`. Optional: `--channel-id`, `--include-archived`, `--before`, `--limit`.
- **`thread reply`** — Channels: Discord. Required: `--target` (thread id), `--message`. Optional: `--media`, `--reply-to`.

## Emojis and Stickers (Discord)

Custom-emoji and sticker management are Discord-centric (`emoji list` additionally works on Slack with no extra flags).

- **`emoji list`** — Discord: `--guild-id`. Slack: no extra flags.
- **`emoji upload`** — Channels: Discord. Required: `--guild-id`, `--emoji-name`, `--media`. Optional: `--role-ids` (repeat).
- **`sticker send`** — Channels: Discord. Required: `--target`, `--sticker-id` (repeat). Optional: `--message`.
- **`sticker upload`** — Channels: Discord. Required: `--guild-id`, `--sticker-name`, `--sticker-desc`, `--sticker-tags`, `--media`.

## Roles / Channels / Members / Voice (Discord)

Guild-administration actions are Discord-only except `member info`, which also works on Slack.

- **`role info`** (Discord): `--guild-id`.
- **`role add`** / **`role remove`** (Discord): `--guild-id`, `--user-id`, `--role-id`.
- **`channel info`** (Discord): `--target`.
- **`channel list`** (Discord): `--guild-id`.
- **`member info`** (Discord/Slack): `--user-id` (+ `--guild-id` for Discord).
- **`voice status`** (Discord): `--guild-id`, `--user-id`.

## Events (Discord)

Scheduled-event management is Discord-only:

- **`event list`** (Discord): `--guild-id`.
- **`event create`** (Discord): `--guild-id`, `--event-name`, `--start-time`. Optional: `--end-time`, `--desc`, `--channel-id`, `--location`, `--event-type`.

## Moderation (Discord)

Member moderation is Discord-only. All three actions take `--guild-id` and `--user-id`:

- **`timeout`**: `--guild-id`, `--user-id` (optional `--duration-min` or `--until`; omit both to clear timeout). `timeout` also supports `--reason`.
- **`kick`**: `--guild-id`, `--user-id` (+ `--reason`).
- **`ban`**: `--guild-id`, `--user-id` (+ `--delete-days`, `--reason`).

**Source**: OpenClaw documentation — `cli/message` (mirror `inbox/openclaw_docs/cli/message.md`), channel-operations sections (Actions › Core beyond send/poll, Threads, Emojis, Stickers, Roles/Channels/Members/Voice, Events, Moderation)
**Last Updated**: 2026-06-22
**Status**: Active
