---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - feishu
keywords:
  - openclaw feishu setup
  - feishu lark bot channel
  - channels login feishu
  - dmpolicy grouppolicy allowlist
  - requiremention mention gating
  - chat_id open_id lookup
  - feishu websocket webhook mode
  - supported message types feishu
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/feishu
access_control_group: ["general"]
---

# OpenClaw — Connecting a Feishu/Lark Bot (Setup & Access Control)

## Overview

This note is the **setup-and-access-control procedure** for docking a Feishu/Lark bot to OpenClaw, mirroring the first half of the `channels/feishu` source page: the quick-start setup wizard, DM and group access control (`dmPolicy` / `groupPolicy` / `requireMention`), group configuration examples, resolving `chat_id` / `open_id`, the common in-chat commands, the troubleshooting paths, and the supported inbound/outbound message types. Feishu/Lark is a collaboration platform (chat, docs, calendars); the channel is **production-ready for bot DMs and group chats**, with **WebSocket as the default mode** and webhook mode optional. The advanced operational cluster (streaming, quota optimization, ACP sessions, multi-agent routing, per-user dynamic agent isolation, full config reference) lives in the sibling note `oc_channels_feishu_advanced`.

## Quick start

Setup requires **OpenClaw 2026.5.29 or above** — check with `openclaw --version` and upgrade with `openclaw update`. Two steps connect the bot:

1. **Run the channel setup wizard.** Choose **manual setup** to paste an **App ID** and **App Secret** from the Feishu Open Platform, or choose **QR setup** to create a bot automatically. If the domestic Feishu mobile app does not react to the QR code, rerun setup and choose manual setup.
2. **Restart the gateway to apply the changes** after setup completes.

```bash
openclaw channels login --channel feishu
openclaw gateway restart
```

## Access control

### Direct messages

Configure `dmPolicy` to control who can DM the bot:

- `"pairing"` — unknown users receive a pairing code; approve via CLI.
- `"allowlist"` — only users listed in `allowFrom` can chat.
- `"open"` — allow public DMs only when `allowFrom` includes `"*"`; with restrictive entries, only matching users can chat.
- `"disabled"` — disable all DMs.

The default `dmPolicy` is `pairing` (per the configuration reference). To approve a pending pairing request, list then approve by code:

```bash
openclaw pairing list feishu
openclaw pairing approve feishu <CODE>
```

### Group chats

The group policy (`channels.feishu.groupPolicy`, **default `allowlist`**) decides which groups the bot answers in:

| Value | Behavior |
| --- | --- |
| `"open"` | Respond to all messages in groups |
| `"allowlist"` | Only respond to groups in `groupAllowFrom` or explicitly configured under `groups.<chat_id>` |
| `"disabled"` | Disable all group messages; explicit `groups.<chat_id>` entries do not override this |

The mention requirement (`channels.feishu.requireMention`) gates whether an @mention is needed: `true` requires an @mention (**default**), `false` responds without one, and a per-group override is `channels.feishu.groups.<chat_id>.requireMention`. Broadcast-only `@all` and `@_all` are **not** treated as bot mentions; a message that mentions both `@all` and the bot directly still counts as a bot mention.

## Group configuration examples

The four canonical group setups (JSON5 config) are: **allow all groups, no @mention required** (`groupPolicy: "open"`); **allow all groups but still require @mention** (`groupPolicy: "open"` + `requireMention: true`); **allow specific groups only** (`groupPolicy: "allowlist"` + `groupAllowFrom: ["oc_xxx", "oc_yyy"]`, where group IDs look like `oc_xxx`); and **restrict senders within a group** (a `groups.<chat_id>.allowFrom` list of `open_id`s). In `allowlist` mode you can also admit a group by adding an explicit `groups.<chat_id>` entry; explicit entries do **not** override `groupPolicy: "disabled"`, and wildcard defaults under `groups.*` configure matching groups but do not admit groups by themselves. The sender-restriction example:

```json5
{
  channels: {
    feishu: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["oc_xxx"],
      groups: {
        oc_xxx: {
          // User open_ids look like: ou_xxx
          allowFrom: ["ou_user1", "ou_user2"],
        },
      },
    },
  },
}
```

## Get group/user IDs

**Group IDs (`chat_id`, format `oc_xxx`):** open the group in Feishu/Lark, click the menu icon in the top-right corner, and go to **Settings** — the group ID (`chat_id`) is listed on the settings page.

**User IDs (`open_id`, format `ou_xxx`):** start the gateway, send a DM to the bot, then check the logs and look for `open_id` in the output. You can also inspect pending pairing requests:

```bash
openclaw logs --follow
openclaw pairing list feishu
```

## Common commands

Feishu/Lark does **not** support native slash-command menus, so send these as **plain text messages**:

| Command | Description |
| --- | --- |
| `/status` | Show bot status |
| `/reset` | Reset the current session |
| `/model` | Show or switch the AI model |

## Troubleshooting

**Bot does not respond in group chats:** (1) ensure the bot is added to the group; (2) ensure you @mention the bot (required by default); (3) verify `groupPolicy` is not `"disabled"`; (4) check logs with `openclaw logs --follow`.

**Bot does not receive messages:** (1) ensure the bot is published and approved in Feishu Open Platform / Lark Developer; (2) ensure event subscription includes `im.message.receive_v1`; (3) ensure **persistent connection (WebSocket)** is selected; (4) ensure all required permission scopes are granted; (5) ensure the gateway is running with `openclaw gateway status`; (6) check logs with `openclaw logs --follow`.

**QR setup does not react in the Feishu mobile app:** rerun setup (`openclaw channels login --channel feishu`), choose manual setup, create a self-built app in Feishu Open Platform and copy its App ID and App Secret, then paste those credentials into the setup wizard.

**App Secret leaked:** reset the App Secret in Feishu Open Platform / Lark Developer, update the value in your config, and restart the gateway with `openclaw gateway restart`.

## Supported message types

**Receive:** ✅ Text, ✅ Rich text (post), ✅ Images, ✅ Files, ✅ Audio, ✅ Video/media, ✅ Stickers. Inbound Feishu/Lark audio messages are normalized as media placeholders instead of raw `file_key` JSON; when `tools.media.audio` is configured, OpenClaw downloads the voice-note resource and runs shared audio transcription before the agent turn so the agent receives the spoken transcript (if Feishu includes transcript text directly in the audio payload, that text is used without another ASR call). Without an audio transcription provider, the agent still receives a `<media:audio>` placeholder plus the saved attachment, not the raw Feishu resource payload.

**Send:** ✅ Text, ✅ Images, ✅ Files, ✅ Audio, ✅ Video/media, ✅ Interactive cards (including streaming updates), ⚠️ Rich text (post-style formatting; doesn't support full Feishu/Lark authoring capabilities). Native Feishu/Lark audio bubbles use the Feishu `audio` message type and require Ogg/Opus upload media (`file_type: "opus"`); existing `.opus` and `.ogg` media is sent directly as native audio, while MP3/WAV/M4A and other likely audio formats are transcoded to 48kHz Ogg/Opus with `ffmpeg` only when the reply requests voice delivery (`audioAsVoice` / message-tool `asVoice`, including TTS voice-note replies). Ordinary MP3 attachments stay regular files, and if `ffmpeg` is missing or conversion fails, OpenClaw falls back to a file attachment and logs the reason.

**Threads and replies:** ✅ Inline replies, ✅ Thread replies, ✅ Media replies stay thread-aware when replying to a thread message. For `groupSessionScope: "group_topic"` and `"group_topic_sender"`, native Feishu/Lark topic groups use the event `thread_id` (`omt_*`) as the canonical topic session key; if a native topic starter event omits `thread_id`, OpenClaw hydrates it from Feishu before routing the turn. Normal group replies that OpenClaw turns into threads keep using the reply root message ID (`om_*`) so the first turn and follow-up turn stay in the same session.

**Source**: OpenClaw documentation — `channels/feishu` (mirror `inbox/openclaw_docs/channels/feishu.md`)
**Last Updated**: 2026-06-22
**Status**: Active
