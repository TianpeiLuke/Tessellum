---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - channels
keywords:
  - openclaw group chat mention gating
  - messages.groupChat.visibleReplies
  - message_tool automatic visible replies
  - mention patterns mentionPatterns
  - chat command handling commands
  - commands.native commands.text
  - ownerAllowFrom useAccessGroups
  - dm history limit self-chat mode
topics:
  - OpenClaw
  - Channel Routing and Commands
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/config-channels
access_control_group: ["general"]
---

# OpenClaw — Channel Group-Chat Mention Gating and Chat Commands

## Overview

This note covers the two cross-channel routing concerns of the OpenClaw `config-channels` reference: **group-chat mention gating** (deciding when the bot replies in a group/channel, and whether its final text is delivered visibly) and **chat command handling** (the top-level `commands.*` config block that gates `/commands` such as `/config`, `/mcp`, `/restart`, and owner-only actions). It mirrors the `### Group chat mention gating` (with its `DM history limits` and `Self-chat mode` subsections) and `### Commands (chat command handling)` sections of `gateway/config-channels`. Per-channel transport config (Slack, Discord, Telegram, etc.) and `DM and group access` policies live in the sibling note `oc_gateway_config_channels`; this note is the routing/commands half of that split.

## Group Chat Mention Gating

Group messages default to **require mention** — either a metadata (native platform) mention or a safe regex pattern match. This applies to WhatsApp, Telegram, Discord, Google Chat, and iMessage group chats. Mention gating decides whether an inbound group message is *processed* at all.

**Mention types:**

- **Metadata mentions**: Native platform @-mentions. Ignored in WhatsApp self-chat mode.
- **Text patterns**: Safe regex patterns in `agents.list[].groupChat.mentionPatterns`. Invalid patterns and unsafe nested repetition are ignored.
- Mention gating is enforced only when detection is possible (native mentions or at least one pattern).

```json5
{
  messages: {
    visibleReplies: "automatic", // force old automatic final replies for direct/source chats
    groupChat: {
      historyLimit: 50,
      unmentionedInbound: "room_event", // always-on unmentioned room chatter becomes quiet context
      visibleReplies: "message_tool", // opt-in; require message(action=send) for visible room replies
    },
  },
  agents: {
    list: [{ id: "main", groupChat: { mentionPatterns: ["@openclaw", "openclaw"] } }],
  },
}
```

### Visible Reply Modes (automatic vs message_tool)

Whether a processed message produces a *visible* reply is controlled separately from gating. Normal group, channel, and internal WebChat direct requests default to **automatic** final delivery: the final assistant text posts through the legacy visible-reply path. Opt into `messages.visibleReplies: "message_tool"` (or `messages.groupChat.visibleReplies: "message_tool"`) when visible output should only post after the agent calls `message(action=send)`. If the model returns final text without calling the message tool in an opted-in tool-only mode, that text stays private and the gateway verbose log records suppressed-payload metadata.

`messages.visibleReplies` is the global source-event default; `messages.groupChat.visibleReplies` overrides it for group/channel source events. When `messages.visibleReplies` is unset, direct/source chats use the selected runtime or harness default, but internal WebChat direct turns use automatic final delivery for Pi/Codex prompt parity. Channel allowlists and mention gating still decide whether an event is processed before reply-mode resolution applies.

Tool-only visible replies require a model/runtime that reliably calls tools, and are recommended for shared ambient rooms on latest-generation models such as GPT 5.5. Weaker models can answer final text but fail to understand that source-visible output must be sent with `message(action=send)`; for those, use `"automatic"` so the final assistant turn is the visible reply path. If the session log shows assistant text with `didSendViaMessagingTool: false`, the model produced private final text instead of calling the message tool. If the message tool is unavailable under the active tool policy, OpenClaw falls back to automatic visible replies instead of silently suppressing the response, and `openclaw doctor` warns about this mismatch. Plugin-owned conversation bindings are exempt — they use the owning plugin's returned reply as the visible response for claimed bound-thread turns and do not need to call `message(action=send)`.

### History and Quiet Context

`messages.groupChat.historyLimit` sets the global group-chat history default (`50` in the example); channels can override with `channels.<channel>.historyLimit` (or per-account), and `0` disables it. `messages.groupChat.unmentionedInbound: "room_event"` submits unmentioned, always-on group/channel messages as quiet room context on supported channels, while mentioned messages, commands, and direct messages remain user requests.

### Troubleshooting: Group @mention triggers typing then silence (no error)

**Symptom**: a group/channel @mention shows the typing indicator and the gateway log reports `dispatch complete (queuedFinal=false, replies=0)`, but no message lands in the room; DMs to the same agent reply normally.

**Cause**: the group/channel visible-reply mode resolves to `"message_tool"`, so OpenClaw runs the turn but suppresses the final assistant text unless the agent calls `message(action=send)`. There is no `NO_REPLY` contract in this mode — no message-tool call means no source reply, and there is no error because suppression is the configured behavior. Normal group/channel turns default to `"automatic"`, so this only appears when `messages.groupChat.visibleReplies` (or global `messages.visibleReplies`) is explicitly set to `"message_tool"`. Harness `defaultVisibleReplies` does not apply here — the group/channel resolver ignores it; it only affects direct/source chats (the Codex harness suppresses direct-chat finals that way).

**Fix**: pick a stronger tool-calling model, remove the explicit `"message_tool"` override to fall back to the `"automatic"` default, or set `messages.groupChat.visibleReplies: "automatic"` to force visible replies for every group/channel request. The gateway hot-reloads `messages` config after the file is saved; only restart the gateway when file watching or config reload is disabled in the deployment.

### DM History Limits

DM history is bounded per channel and optionally per DM peer:

```json5
{
  channels: {
    telegram: {
      dmHistoryLimit: 30,
      dms: {
        "123456789": { historyLimit: 50 },
      },
    },
  },
}
```

Resolution order: per-DM override → provider default → no limit (all retained). Supported channels: `telegram`, `whatsapp`, `discord`, `slack`, `signal`, `imessage`, `msteams`.

### Self-Chat Mode

Include your own number in `allowFrom` to enable self-chat mode, which ignores native @-mentions and only responds to text patterns:

```json5
{
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: { mentionPatterns: ["reisponde", "@openclaw"] },
      },
    ],
  },
}
```

## Commands (Chat Command Handling)

The top-level `commands.*` block configures which chat-command surfaces are active. This page is a **config-key reference**, not the full command catalog (see [Slash Commands](https://docs.openclaw.ai/tools/slash-commands) for the built-in + bundled catalog). Text commands must be **standalone** messages with a leading `/`.

```json5
{
  commands: {
    native: "auto", // register native commands when supported
    nativeSkills: "auto", // register native skill commands when supported
    text: true, // parse /commands in chat messages
    bash: false, // allow ! (alias: /bash)
    bashForegroundMs: 2000,
    config: false, // allow /config
    mcp: false, // allow /mcp
    plugins: false, // allow /plugins
    debug: false, // allow /debug
    restart: true, // allow /restart + gateway restart tool
    ownerAllowFrom: ["discord:123456789012345678"],
    ownerDisplay: "raw", // raw | hash
    ownerDisplaySecret: "${OWNER_ID_HASH_SECRET}",
    allowFrom: {
      "*": ["user1"],
      discord: ["user:123"],
    },
    useAccessGroups: true,
  },
}
```

### Command Surface Keys

- `native: "auto"` turns on native commands for Discord/Telegram and leaves Slack off; `nativeSkills: "auto"` does the same for native skill commands. Override per channel with `channels.discord.commands.native` (bool or `"auto"`; for Discord, `false` skips native command registration and cleanup during startup) and `channels.<provider>.commands.nativeSkills`. `channels.telegram.customCommands` adds extra Telegram bot menu entries.
- `bash: true` enables `! <cmd>` for the host shell. It requires `tools.elevated.enabled` and the sender in `tools.elevated.allowFrom.<channel>`.
- `config: true` enables `/config` (reads/writes `openclaw.json`). For gateway `chat.send` clients, persistent `/config set|unset` writes also require `operator.admin`; read-only `/config show` stays available to normal write-scoped operator clients.
- `mcp: true` enables `/mcp` for OpenClaw-managed MCP server config under `mcp.servers`; `plugins: true` enables `/plugins` for plugin discovery, install, and enable/disable controls.
- `restart: false` disables `/restart` and the gateway restart tool actions (default: `true`).
- `channels.<provider>.configWrites` gates config mutations per channel (default: true). For multi-account channels, `channels.<provider>.accounts.<id>.configWrites` also gates writes targeting that account (for example `/allowlist --config --account <id>` or `/config set channels.<provider>.accounts.<id>...`).

### Owner and Authorization Keys

- `ownerAllowFrom` is the explicit owner allowlist for owner-only commands and owner-gated channel actions; it is separate from `allowFrom`.
- `ownerDisplay: "hash"` hashes owner ids in the system prompt — set `ownerDisplaySecret` to control hashing.
- `allowFrom` is per-provider. When set, it is the **only** authorization source (channel allowlists/pairing and `useAccessGroups` are ignored).
- `useAccessGroups: false` allows commands to bypass access-group policies when `allowFrom` is not set.

Channel/plugin-owned commands (for example QQ Bot `/bot-ping`, LINE `/card`, device-pair `/pair`, memory `/dreaming`, phone-control `/phone`, Talk `/voice`) are documented in their channel/plugin pages plus [Slash Commands](https://docs.openclaw.ai/tools/slash-commands), not in this config-key reference.

**Source**: OpenClaw documentation — `gateway/config-channels` (mirror `inbox/openclaw_docs/gateway/config-channels.md`), sections "Group chat mention gating" + "Commands (chat command handling)"
**Last Updated**: 2026-06-22
**Status**: Active
