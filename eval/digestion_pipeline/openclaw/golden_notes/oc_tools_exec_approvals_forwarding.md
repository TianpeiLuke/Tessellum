---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - exec_approvals
keywords:
  - openclaw approval forwarding
  - approvals.exec approvals.plugin
  - /approve allow-once allow-always deny
  - same-chat approvals
  - native approval delivery
  - channels execApprovals
  - macos ipc approval flow
  - telegram accountId threadId
topics:
  - OpenClaw
  - Exec Approvals
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/exec-approvals-advanced
access_control_group: ["general"]
---

# OpenClaw — Forwarding Exec & Plugin Approvals to Chat Channels

## Overview

This note is the procedure for forwarding OpenClaw's host exec (and plugin) approval prompts to chat channels — Slack, Telegram, Discord, Matrix, Microsoft Teams, Google Chat, WhatsApp, and Signal — so an operator can approve commands with `/approve` or native approval cards instead of being tied to the Web/terminal UI. It mirrors the second half of `tools/exec-approvals-advanced`: the `approvals.exec` / `approvals.plugin` forwarding config, the `/approve` decision verbs, same-chat approvals on any deliverable channel, native approval clients gated by `channels.<channel>.execApprovals`, the macOS IPC flow, and the FAQ on `accountId`/`threadId` targeting and session-approval authorization. The safe-bins / interpreter-binding first half is its split sibling `oc_tools_exec_approvals_safe_bins`; the underlying request→resolve flow lives in `oc_tools_exec_approvals_operations`.

## Approval Forwarding to Chat Channels (`approvals.exec`)

You can forward exec approval prompts to any chat channel (including plugin channels) and approve them with `/approve`; forwarding uses OpenClaw's normal outbound delivery pipeline. Configure it under `approvals.exec`: `enabled` turns forwarding on, `mode` chooses where prompts go (`"session"`, `"targets"`, or `"both"`), `agentFilter` restricts which agents forward, `sessionFilter` matches session identifiers by substring or regex, and `targets` is an explicit list of `{ channel, to }` destinations.

```json5
{
  approvals: {
    exec: {
      enabled: true,
      mode: "session", // "session" | "targets" | "both"
      agentFilter: ["main"],
      sessionFilter: ["discord"], // substring or regex
      targets: [
        { channel: "slack", to: "U12345678" },
        { channel: "telegram", to: "123456789" },
      ],
    },
  },
}
```

An operator replies in chat to resolve the prompt by id with one of three decision verbs:

```
/approve <id> allow-once
/approve <id> allow-always
/approve <id> deny
```

The `/approve` command handles both exec approvals and plugin approvals: if the id does not match a pending exec approval, it automatically checks plugin approvals instead. This exec-to-plugin fallback is intentionally bounded to "approval not found" failures — a real exec approval denial or error is NOT silently retried as a plugin approval.

## Plugin Approval Forwarding (`approvals.plugin`)

Plugin approval forwarding uses the same delivery pipeline as exec approvals but has its own independent config under `approvals.plugin`; enabling or disabling one does not affect the other. The config shape is identical to `approvals.exec` — `enabled`, `mode`, `agentFilter`, `sessionFilter`, and `targets` work the same way. For plugin-authoring behavior, request fields, and decision semantics see the Plugin permission requests page (link-out, not duplicated here).

```json5
{
  approvals: {
    plugin: {
      enabled: true,
      mode: "targets",
      agentFilter: ["main"],
      targets: [
        { channel: "slack", to: "U12345678" },
        { channel: "telegram", to: "123456789" },
      ],
    },
  },
}
```

Channels that support shared interactive replies render the same approval buttons for both exec and plugin approvals; channels without shared interactive UI fall back to plain text with `/approve` instructions. Plugin approval requests may restrict the available decisions — approval surfaces use the request's declared decision set, and the Gateway rejects attempts to submit a decision that was not offered.

## Same-Chat Approvals on Any Channel

When an exec or plugin approval request originates from a deliverable chat surface, that same chat can approve it with `/approve` by default — applying to channels such as Slack, Matrix, and Microsoft Teams in addition to the existing Web UI and terminal UI flows. This shared text-command path uses the normal channel auth model for that conversation: if the originating chat can already send commands and receive replies, approval requests no longer need a separate native delivery adapter just to stay pending. Discord and Telegram also support same-chat `/approve`, but those channels still use their resolved approver list for authorization even when native approval delivery is disabled.

## Native Approval Delivery

Some channels can also act as native approval clients, adding approver DMs, origin-chat fanout, and channel-specific interactive approval UX on top of the shared same-chat `/approve` flow. When native approval cards/buttons are available, that native UI is the primary agent-facing path — the agent should not also echo a duplicate plain chat `/approve` command unless the tool result says chat approvals are unavailable or manual approval is the only remaining path. If a native approval client is configured but no native runtime is active for the originating channel, OpenClaw keeps the local deterministic `/approve` prompt visible; if the native runtime is active and attempts delivery but no target receives the card, OpenClaw sends a same-chat fallback notice with the exact `/approve <id> <decision>` command so the request can still be resolved.

The generic model layers three independent controls: host exec policy still decides whether exec approval is required; `approvals.exec` controls forwarding prompts to other chat destinations; and `channels.<channel>.execApprovals` controls whether Discord, Slack, Telegram, and similar channel-specific native clients are enabled. Slack plugin approvals can use Slack's native approval client when the request comes from Slack and Slack plugin approvers resolve, and `approvals.plugin` can also route plugin approvals to Slack sessions or targets even when Slack exec approvals are disabled. Google Chat native cards handle exec and plugin approvals originating from Google Chat spaces or threads when stable `users/<id>` approvers resolve from `dm.allowFrom` or `defaultTo` (they do not use reaction events for decisions). WhatsApp and Signal reaction approval delivery are gated by `approvals.exec` and `approvals.plugin`; they do not have `channels.<channel>.execApprovals` blocks.

Native approval clients auto-enable DM-first delivery when ALL of these are true: the channel supports native approval delivery; approvers can be resolved from explicit `execApprovals.approvers` or owner identity such as `commands.ownerAllowFrom`; and `channels.<channel>.execApprovals.enabled` is unset or `"auto"`. Set `enabled: false` to disable a native approval client explicitly, or `enabled: true` to force it on when approvers resolve. Public origin-chat delivery stays explicit through `channels.<channel>.execApprovals.target`.

### Per-Channel Native Client Configuration

Each native client has its own config surface, listed explicitly in the source: Discord uses `channels.discord.execApprovals.*`; Slack uses `channels.slack.execApprovals.*`; Telegram uses `channels.telegram.execApprovals.*`. Google Chat configures stable approvers with `channels.googlechat.dm.allowFrom` or `channels.googlechat.defaultTo` and requires no `execApprovals` block. WhatsApp and Signal each use `approvals.exec` and `approvals.plugin` to route prompts. These clients add DM routing and optional channel fanout on top of the shared same-chat `/approve` flow and shared approval buttons.

### Shared Native-Delivery Behavior

Slack, Matrix, Microsoft Teams, and similar deliverable chats use the normal channel auth model for same-chat `/approve`. When a native approval client auto-enables, the default native delivery target is approver DMs. For Discord and Telegram, only resolved approvers can approve or deny: Discord, Telegram, and Slack approvers can each be explicit (`execApprovals.approvers`) or inferred from `commands.ownerAllowFrom`. Slack plugin approval DMs use Slack plugin approvers from `allowFrom` and account default routing (not Slack exec approvers), and Slack native buttons preserve approval id kind so `plugin:` ids can resolve plugin approvals without a second Slack-local fallback layer. Google Chat native cards preserve the manual `/approve` fallback in message text, but card button callbacks carry only opaque action tokens — approval id and decision are recovered from server-side pending state.

WhatsApp emoji approvals handle both exec and plugin prompts only when the matching top-level forwarding family is enabled and routes to WhatsApp; target-only WhatsApp forwarding stays on the shared forwarding path unless it matches the same native origin target. Signal reaction approvals handle both exec and plugin prompts only when the matching top-level forwarding family is enabled and routes to Signal — direct same-chat Signal exec approvals can suppress the local `/approve` fallback without explicit approvers, but Signal reaction resolution still requires explicit Signal approvers from `channels.signal.allowFrom` or `defaultTo`. Matrix native DM/channel routing and reaction shortcuts handle both exec and plugin approvals (plugin authorization still comes from `channels.matrix.dm.allowFrom`), and Matrix native prompts include `com.openclaw.approval` custom event content on the first prompt event so OpenClaw-aware Matrix clients can read structured approval state while stock clients keep the plain-text `/approve` fallback. The requester does not need to be an approver, and the originating chat can approve directly with `/approve` when that chat already supports commands and replies. Native Discord approval buttons route by approval id kind (`plugin:` ids go straight to plugin approvals, everything else to exec approvals), and native Telegram approval buttons follow the same bounded exec-to-plugin fallback as `/approve`. When native `target` enables origin-chat delivery, approval prompts include the command text; pending exec approvals expire after 30 minutes by default; and if no operator UI or configured approval client can accept the request, the prompt falls back to `askFallback`.

Sensitive owner-only group commands such as `/diagnostics` and `/export-trajectory` use private owner routing for approval prompts and final results: OpenClaw first tries a private route on the same surface where the owner ran the command, and if that surface has no private owner route it falls back to the first available owner route from `commands.ownerAllowFrom` — so a Discord group command can still send the approval and result to the owner's Telegram DM when Telegram is the configured primary private interface, while the group chat only gets a short acknowledgement. Telegram defaults to approver DMs (`target: "dm"`); you can switch to `channel` or `both` when you want approval prompts to appear in the originating Telegram chat/topic as well, and for Telegram forum topics OpenClaw preserves the topic for the approval prompt and the post-approval follow-up.

### macOS IPC Flow

On macOS the gateway delivers `system.run` approvals to the Mac app over an inter-process channel: the Gateway talks to the Node Service over WebSocket, which in turn reaches the Mac App (UI + approvals + `system.run`) over IPC carrying a Unix-domain-socket connection plus token, HMAC, and TTL.

```
Gateway -> Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + approvals + system.run)
```

The source records three security properties for this flow: the Unix socket runs in mode `0600` with the token stored in `exec-approvals.json`; a same-UID peer check verifies the caller; and a challenge/response (nonce + HMAC token + request hash) bounded by a short TTL authenticates each exchange.

## FAQ

**When would `accountId` and `threadId` be used on an approval target?** Use `accountId` when the channel has multiple configured identities and the approval prompt must leave through one specific account; use `threadId` when the destination supports topics or threads and the prompt should stay inside that thread instead of the top-level chat. A concrete Telegram case is an operations supergroup with forum topics and two Telegram bot accounts: the `to` value names the supergroup, `accountId` selects the bot account, and `threadId` selects the forum topic. With the setup below, forwarded exec approvals are posted by the `ops-bot` account into topic `77` of chat `-1001234567890`; a target without `accountId` uses the channel's default account and a target without `threadId` posts to the top-level destination.

```json5
{
  approvals: {
    exec: {
      enabled: true,
      mode: "targets",
      targets: [
        {
          channel: "telegram",
          to: "-1001234567890",
          accountId: "ops-bot",
          threadId: "77",
        },
      ],
    },
  },
  channels: {
    telegram: {
      accounts: {
        default: {
          name: "Primary bot",
          botToken: "env:TELEGRAM_PRIMARY_BOT_TOKEN",
        },
        "ops-bot": {
          name: "Operations bot",
          botToken: "env:TELEGRAM_OPS_BOT_TOKEN",
        },
      },
    },
  },
}
```

**When approvals are sent to a session, can anyone in that session approve them?** No — session delivery only controls where the prompt appears, and does not by itself authorize every participant in that chat to approve. For generic same-chat `/approve`, the sender must already be authorized for commands in that channel session; if the channel exposes explicit approval approvers, those approvers can authorize the `/approve` action even when they are not otherwise command-authorized in that session. Some channels are stricter — Discord, Telegram, Matrix, Slack native approval DMs, and similar native approval clients use their resolved approver lists for approval authorization. For example, a Telegram forum-topic approval prompt can be visible to everyone in the topic, but only numeric Telegram user IDs resolved from `channels.telegram.execApprovals.approvers` or `commands.ownerAllowFrom` can approve or deny it.

**Source**: OpenClaw documentation — `tools/exec-approvals-advanced` (mirror `inbox/openclaw_docs/tools/exec-approvals-advanced.md`), Approval-forwarding sections
**Last Updated**: 2026-06-22
**Status**: Active
