---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - messaging
keywords:
  - openclaw message send
  - openclaw message poll
  - openclaw message broadcast
  - message channel selection
  - message target formats
  - presentation semantic blocks
  - secretref scoping
  - outbound message cli
topics:
  - OpenClaw
  - CLI Messaging
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/message
access_control_group: ["general"]
---

# OpenClaw — `openclaw message` Send, Poll, and Broadcast

## Overview

This note is the procedure for the outbound half of the single `openclaw message` CLI command — the `send`, `poll`, and `broadcast` Core actions plus the cross-channel plumbing they share: channel selection, per-channel `--target` formats, name lookup, common flags, SecretRef resolution, and the worked send/poll/presentation examples. It mirrors the `cli/message` source page (sections Usage, Channel selection, Target formats, Name lookup, Common flags, SecretRef behavior, the `send`/`poll`/`broadcast` Core actions, and the Examples block). The remaining `openclaw message` channel-operations actions (react/read/edit/delete/pin/threads/emoji/stickers/roles/events/moderation) are documented in the sibling note **oc_cli_message_channel_ops**.

## Command Surface and Usage

`openclaw message` is a single outbound command for sending messages and channel actions across Discord, Google Chat, iMessage, Matrix, Mattermost (plugin), Microsoft Teams, Signal, Slack, Telegram, and WhatsApp. The usage form is:

```
openclaw message <subcommand> [flags]
```

The send-side `<subcommand>` values covered here are `send`, `poll`, and `broadcast`.

## Channel Selection

The active channel is chosen as follows: `--channel` is required if more than one channel is configured; if exactly one channel is configured it becomes the default. Valid values are `discord|googlechat|imessage|matrix|mattermost|msteams|signal|slack|telegram|whatsapp` (Mattermost requires the plugin). `openclaw message` resolves the selected channel to its owning plugin when `--channel` or a channel-prefixed target is present; otherwise it loads configured channel plugins for default-channel inference.

## Target Formats (`--target`)

Each channel accepts its own `--target` destination syntax:

- WhatsApp: E.164, group JID, or WhatsApp Channel/Newsletter JID (`...@newsletter`)
- Telegram: chat id, `@username`, or forum topic target (`-1001234567890:topic:42`, or `--thread-id 42`)
- Discord: `channel:<id>` or `user:<id>` (or `<@id>` mention; raw numeric ids are treated as channels)
- Google Chat: `spaces/<spaceId>` or `users/<userId>`
- Slack: `channel:<id>` or `user:<id>` (raw channel id is accepted)
- Mattermost (plugin): `channel:<id>`, `user:<id>`, or `@username` (bare ids are treated as channels)
- Signal: `+E.164`, `group:<id>`, `signal:+E.164`, `signal:group:<id>`, or `username:<name>`/`u:<name>`
- iMessage: handle, `chat_id:<id>`, `chat_guid:<guid>`, or `chat_identifier:<id>`
- Matrix: `@user:server`, `!room:server`, or `#alias:server`
- Microsoft Teams: conversation id (`19:...@thread.tacv2`) or `conversation:<id>` or `user:<aad-object-id>`

## Name Lookup

For supported providers (Discord/Slack/etc), channel names like `Help` or `#help` are resolved via the directory cache. On cache miss, OpenClaw will attempt a live directory lookup when the provider supports it.

## Common Flags

These flags are shared across the send-side actions: `--channel <name>`, `--account <id>`, `--target <dest>` (target channel or user for send/poll/read/etc), `--targets <name>` (repeat; broadcast only), `--json`, `--dry-run`, and `--verbose`.

## SecretRef Behavior

`openclaw message` resolves supported channel SecretRefs before running the selected action. Resolution is scoped to the active action target when possible: channel-scoped when `--channel` is set (or inferred from prefixed targets like `discord:...`); account-scoped when `--account` is set (channel globals + selected account surfaces); and when `--account` is omitted, OpenClaw does not force a `default` account SecretRef scope. Unresolved SecretRefs on unrelated channels do not block a targeted message action. If the selected channel/account SecretRef is unresolved, the command fails closed for that action.

## `send`

The `send` action delivers a message to a single target on WhatsApp/Telegram/Discord/Google Chat/Slack/Mattermost (plugin)/Signal/iMessage/Matrix/Microsoft Teams. It requires `--target`, plus one of `--message`, `--media`, or `--presentation`. Optional flags are `--media`, `--presentation`, `--delivery`, `--pin`, `--reply-to`, `--thread-id`, `--gif-playback`, `--force-document`, and `--silent`. The flag semantics are:

- **Shared presentation payloads:** `--presentation` sends semantic blocks (`text`, `context`, `divider`, `buttons`, `select`) that core renders through the selected channel's declared capabilities. See [Message Presentation](https://docs.openclaw.ai/plugins/message-presentation).
- **Generic delivery preferences:** `--delivery` accepts delivery hints such as `{ "pin": true }`; `--pin` is shorthand for pinned delivery when the channel supports it.
- **Telegram + WhatsApp:** `--force-document` (send images, GIFs, and videos as documents to avoid channel compression).
- **Telegram only:** `--thread-id` (forum topic id).
- **Slack only:** `--thread-id` (thread timestamp; `--reply-to` uses the same field).
- **Telegram + Discord:** `--silent`.
- **WhatsApp only:** `--gif-playback`; WhatsApp Channels/Newsletters are addressed with their native `@newsletter` JID.

## `poll`

The `poll` action creates a poll on WhatsApp/Telegram/Discord/Matrix/Microsoft Teams. It requires `--target`, `--poll-question`, and `--poll-option` (repeat for each choice), with optional `--poll-multi`. Per-channel extras: Discord only — `--poll-duration-hours`, `--silent`, `--message`; Telegram only — `--poll-duration-seconds` (5-600), `--silent`, `--poll-anonymous` / `--poll-public`, `--thread-id`.

## `broadcast`

The `broadcast` action sends to many targets at once on any configured channel; use `--channel all` to target all providers. It requires `--targets <target...>` (repeated) and accepts optional `--message`, `--media`, and `--dry-run`.

## Semantic Presentation Rendering

The `--presentation` payload is the cross-channel contract: core renders the same `presentation` payload into Discord components, Slack blocks, Telegram inline buttons, Mattermost props, or Teams/Feishu cards depending on channel capability. See [Message Presentation](https://docs.openclaw.ai/plugins/message-presentation) for the full contract and fallback rules. Telegram web app buttons are supported only in private chats between a user and the bot; older JSON payloads using `web_app` still parse, but `webApp` is the canonical presentation field.

## Examples

Send a Discord reply, then a message with semantic buttons (presentation blocks core renders per channel):

```
openclaw message send --channel discord \
  --target channel:123 --message "hi" --reply-to 456

openclaw message send --channel discord \
  --target channel:123 --message "Choose:" \
  --presentation '{"blocks":[{"type":"buttons","buttons":[{"label":"Approve","value":"approve","style":"success"},{"label":"Decline","value":"decline","style":"danger"}]}]}'
```

A richer presentation payload (Google Chat) with title/tone and a Teams card / Telegram Mini App button:

```bash
openclaw message send --channel googlechat --target spaces/AAA... \
  --message "Choose:" \
  --presentation '{"title":"Deploy approval","tone":"warning","blocks":[{"type":"text","text":"Choose a path"},{"type":"buttons","buttons":[{"label":"Approve","value":"approve"},{"label":"Decline","value":"decline"}]}]}'

openclaw message send --channel telegram --target 123456789 --message "Open app:" \
  --presentation '{"blocks":[{"type":"buttons","buttons":[{"label":"Launch","webApp":{"url":"https://example.com/app"}}]}]}'
```

Create a Discord poll (multi-select, 48h) and a Telegram poll (auto-close in 2 minutes):

```
openclaw message poll --channel discord \
  --target channel:123 \
  --poll-question "Snack?" \
  --poll-option Pizza --poll-option Sushi \
  --poll-multi --poll-duration-hours 48

openclaw message poll --channel telegram \
  --target @mychat \
  --poll-question "Lunch?" \
  --poll-option Pizza --poll-option Sushi \
  --poll-duration-seconds 120 --silent
```

Send a Microsoft Teams proactive message and a Teams card through generic presentation:

```bash
openclaw message send --channel msteams \
  --target conversation:19:abc@thread.tacv2 --message "hi"

openclaw message send --channel msteams \
  --target conversation:19:abc@thread.tacv2 \
  --presentation '{"title":"Status update","blocks":[{"type":"text","text":"Build completed"}]}'
```

Send a Telegram or WhatsApp image as a document to avoid compression:

```bash
openclaw message send --channel telegram --target @mychat \
  --media ./diagram.png --force-document
```

**Source**: OpenClaw documentation — `cli/message` (mirror `inbox/openclaw_docs/cli/message.md`)
**Last Updated**: 2026-06-22
**Status**: Active
