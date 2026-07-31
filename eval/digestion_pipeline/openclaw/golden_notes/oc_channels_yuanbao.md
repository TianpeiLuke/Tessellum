---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - yuanbao
keywords:
  - openclaw yuanbao channel
  - tencent yuanbao bot
  - yuanbao websocket connection
  - appkey appsecret token
  - yuanbao dmpolicy requiremention
  - outboundqueuestrategy merge-text
  - yuanbao bindings multi-agent
  - yuanbao configuration reference
topics:
  - OpenClaw
  - Channels
  - Yuanbao
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/yuanbao
access_control_group: ["general"]
---

# OpenClaw — Connecting the Tencent Yuanbao Channel

## Overview

This note is the procedure for connecting a Tencent Yuanbao bot to OpenClaw, mirroring the `channels/yuanbao` source page. Tencent Yuanbao is Tencent's AI assistant platform; the OpenClaw channel plugin connects Yuanbao bots to OpenClaw over **WebSocket** (the only supported connection mode) so they interact with users through direct messages and group chats. The channel is **production-ready for bot DMs + group chats**. The note walks the quick-start and interactive setup, DM/group access control, the configuration examples, native slash commands, the troubleshooting playbook, the advanced configuration (multi-account, message limits, streaming, history, reply-to, markdown-hint, debug, multi-agent routing), the full configuration reference table, and supported message types.

## Quick start

> **Requires OpenClaw 2026.4.10 or above.** Run `openclaw --version` to check. Upgrade with `openclaw update`.

Add the Yuanbao channel with your credentials, then restart the gateway. The `--token` value uses colon-separated `appKey:appSecret` format. You obtain these from the Yuanbao app by creating a robot in your application settings.

```bash
openclaw channels add --channel yuanbao --token "appKey:appSecret"
openclaw gateway restart
```

### Interactive setup (alternative)

You can also use the interactive wizard with `openclaw channels login --channel yuanbao`; follow the prompts to enter your App ID and App Secret.

## Access control

### Direct messages

Configure `dmPolicy` to control who can DM the bot. The four values are: `"pairing"` (unknown users receive a pairing code; approve via CLI), `"allowlist"` (only users listed in `allowFrom` can chat), `"open"` (allow all users — **default**), and `"disabled"` (disable all DMs). Approve a pairing request with the CLI:

```bash
openclaw pairing list yuanbao
openclaw pairing approve yuanbao <CODE>
```

### Group chats

The mention requirement (`channels.yuanbao.requireMention`) is `true` (require @mention, default) or `false` (respond without @mention). Replying to the bot's message in a group chat is treated as an implicit mention.

## Configuration examples

Configuration uses JSON5. The basic open-DM setup nests credentials and DM policy under `channels.yuanbao`; an allowlist restricts DMs to a `dm.allowFrom` user-ID list; `requireMention: false` disables the group @mention requirement. For outbound delivery, `outboundQueueStrategy: "immediate"` sends each chunk immediately without buffering, while `"merge-text"` buffers and is tuned with `minChars` (buffer until this many chars), `maxChars` (force split above this limit), and `idleMs` (auto-flush after idle timeout in ms).

```json5
{
  channels: {
    yuanbao: {
      appKey: "your_app_key",
      appSecret: "your_app_secret",
      dm: { policy: "allowlist", allowFrom: ["user_id_1", "user_id_2"] },
      requireMention: false,
      outboundQueueStrategy: "merge-text",
      minChars: 2800, // buffer until this many chars
      maxChars: 3000, // force split above this limit
      idleMs: 5000, // auto-flush after idle timeout (ms)
    },
  },
}
```

## Common commands

Yuanbao supports native slash-command menus. Commands are synced to the platform automatically when the gateway starts. The available commands are `/help` (show available commands), `/status` (show bot status), `/new` (start a new session), `/stop` (stop the current run), `/restart` (restart OpenClaw), and `/compact` (compact the session context).

## Troubleshooting

- **Bot does not respond in group chats:** ensure the bot is added to the group, ensure you @mention the bot (required by default), and check logs with `openclaw logs --follow`.
- **Bot does not receive messages:** ensure the bot is created and approved in the Yuanbao app, ensure `appKey` and `appSecret` are correctly configured, ensure the gateway is running (`openclaw gateway status`), and check logs (`openclaw logs --follow`).
- **Bot sends empty or fallback replies:** check if the AI model is returning valid content; the default fallback reply is `暂时无法解答，你可以换个问题问问我哦`, customizable via `channels.yuanbao.fallbackReply`.
- **App Secret leaked:** reset the App Secret in the YuanBao APP, update the value in your config, and restart the gateway (`openclaw gateway restart`).

## Advanced configuration

**Multiple accounts** are declared under `channels.yuanbao.accounts.<id>` (each with `appKey`, `appSecret`, `name`, and optional `enabled: false`); `defaultAccount` controls which account is used when outbound APIs do not specify an `accountId`.

```json5
{
  channels: {
    yuanbao: {
      defaultAccount: "main",
      accounts: {
        main: { appKey: "key_xxx", appSecret: "secret_xxx", name: "Primary bot" },
        backup: { appKey: "key_yyy", appSecret: "secret_yyy", name: "Backup bot", enabled: false },
      },
    },
  },
}
```

**Message limits:** `maxChars` is the single-message max character count (default `3000` chars), `mediaMaxMb` is the media upload/download limit (default `20` MB), and `overflowPolicy` controls behavior when a message exceeds the limit — `"split"` (default) or `"stop"`.

**Streaming:** Yuanbao supports block-level streaming output — when enabled, the bot sends text in chunks as it generates. `disableBlockStreaming: false` keeps block streaming enabled (default); set `disableBlockStreaming: true` to send the complete reply in one message.

**Group chat history context:** `historyLimit` controls how many historical messages are included in the AI context for group chats (default `100`, set `0` to disable).

**Reply-to mode:** `replyToMode` controls how the bot quotes messages when replying in group chats — `"off"` (no quote reply), `"first"` (quote only the first reply per inbound message — default), or `"all"` (quote every reply).

**Markdown hint injection:** by default the bot injects instructions in the system prompt to prevent the AI model from wrapping the entire reply in markdown code blocks; `markdownHintEnabled: true` is the default.

**Debug mode:** `debugBotIds` enables unsanitized log output for specific bot IDs (e.g. `["bot_user_id_1", "bot_user_id_2"]`).

**Multi-agent routing** uses `bindings` to route Yuanbao DMs or groups to different agents. Routing fields are `match.channel` (`"yuanbao"`), `match.peer.kind` (`"direct"` for DM or `"group"` for group chat), and `match.peer.id` (user ID or group code).

```json5
{
  agents: { list: [ { id: "main" }, { id: "agent-a", workspace: "/home/user/agent-a" }, { id: "agent-b", workspace: "/home/user/agent-b" } ] },
  bindings: [
    { agentId: "agent-a", match: { channel: "yuanbao", peer: { kind: "direct", id: "user_xxx" } } },
    { agentId: "agent-b", match: { channel: "yuanbao", peer: { kind: "group", id: "group_zzz" } } },
  ],
}
```

## Configuration reference

Full configuration lives in the Gateway configuration reference. The Yuanbao settings and defaults:

| Setting | Description | Default |
| --- | --- | --- |
| `channels.yuanbao.enabled` | Enable/disable the channel | `true` |
| `channels.yuanbao.defaultAccount` | Default account for outbound routing | `default` |
| `channels.yuanbao.accounts.<id>.appKey` | App Key (used for signing and ticket generation) | - |
| `channels.yuanbao.accounts.<id>.appSecret` | App Secret (used for signing) | - |
| `channels.yuanbao.accounts.<id>.token` | Pre-signed token (skips automatic ticket signing) | - |
| `channels.yuanbao.accounts.<id>.name` | Account display name | - |
| `channels.yuanbao.accounts.<id>.enabled` | Enable/disable a specific account | `true` |
| `channels.yuanbao.dm.policy` | DM policy | `open` |
| `channels.yuanbao.dm.allowFrom` | DM allowlist (user ID list) | - |
| `channels.yuanbao.requireMention` | Require @mention in groups | `true` |
| `channels.yuanbao.overflowPolicy` | Long message handling (`split` or `stop`) | `split` |
| `channels.yuanbao.replyToMode` | Group reply-to strategy (`off`, `first`, `all`) | `first` |
| `channels.yuanbao.outboundQueueStrategy` | Outbound strategy (`merge-text` or `immediate`) | `merge-text` |
| `channels.yuanbao.minChars` | Merge-text: min chars to trigger send | `2800` |
| `channels.yuanbao.maxChars` | Merge-text: max chars per message | `3000` |
| `channels.yuanbao.idleMs` | Merge-text: idle timeout before auto-flush (ms) | `5000` |
| `channels.yuanbao.mediaMaxMb` | Media size limit (MB) | `20` |
| `channels.yuanbao.historyLimit` | Group chat history context entries | `100` |
| `channels.yuanbao.disableBlockStreaming` | Disable block-level streaming output | `false` |
| `channels.yuanbao.fallbackReply` | Fallback reply when AI returns no content | `暂时无法解答，你可以换个问题问问我哦` |
| `channels.yuanbao.markdownHintEnabled` | Inject markdown anti-wrapping instructions | `true` |
| `channels.yuanbao.debugBotIds` | Debug whitelist bot IDs (unsanitized logs) | `[]` |

## Supported message types

**Receive:** Text, Images, Files, Audio / Voice, Video, Stickers / Custom emoji, and Custom elements (link cards, etc.) are all supported. **Send:** Text (with markdown support), Images, Files, Audio, Video, and Stickers are all supported. **Threads and replies:** Quote replies are supported (configurable via `replyToMode`); thread replies are not supported by the platform.

**Source**: OpenClaw documentation — `channels/yuanbao` (mirror `inbox/openclaw_docs/channels/yuanbao.md`)
**Last Updated**: 2026-06-22
**Status**: Active
