---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - slack
keywords:
  - openclaw slack token model
  - slack bot app signing user token
  - slack dmpolicy allowfrom
  - slack grouppolicy channel allowlist
  - slack actions and gates
  - slack native approvals
  - dangerouslyallownamematching
  - execapprovals approvers
topics:
  - OpenClaw
  - Slack Channel Security
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/slack
access_control_group: ["general"]
---

# OpenClaw — Slack Channel Security and Access Model

## Overview

This note covers the **security and access model** of the OpenClaw Slack channel: the four-credential token model and its per-credential status snapshot, the `channels.slack.actions.*` action groups and gates, DM-policy plus channel access control and routing (allowlists, mention gating, ID-first matching), and Slack as a native in-conversation approval client. It mirrors the `Token model`, `Actions and gates`, `Access control and routing`, and `Native approvals in Slack` sections of the `channels/slack` source page. The transport/setup procedure (Socket Mode vs HTTP, manifest, scopes) lives in the sibling setup note; the messaging-runtime UX and interactivity/ops live in the messaging and interactivity siblings — this note is the safety boundary that gates who may reach the agent and which tool actions are exposed.

## Token model

OpenClaw resolves four Slack credentials, each required depending on transport mode:

- `botToken` + `appToken` are required for **Socket Mode**.
- HTTP mode requires `botToken` + `signingSecret`.
- `botToken`, `appToken`, `signingSecret`, and `userToken` accept plaintext strings or **SecretRef** objects.
- **Config tokens override env fallback.**
- `SLACK_BOT_TOKEN` / `SLACK_APP_TOKEN` env fallback applies only to the **default account**.
- `userToken` is **config-only** (no env fallback) and defaults to read-only behavior (`userTokenReadOnly: true`).

For actions/directory reads the user token can be preferred when configured; for writes the bot token remains preferred, and user-token writes are only allowed when `userTokenReadOnly: false` **and** the bot token is unavailable.

### Status snapshot behavior

Slack account inspection tracks a per-credential `*Source` and `*Status` field for each of `botToken`, `appToken`, `signingSecret`, and `userToken`. Each status is one of three values:

- `available`
- `configured_unavailable`
- `missing`

`configured_unavailable` means the account is configured through SecretRef or another non-inline secret source, but the current command/runtime path could not resolve the actual value. The status fields surfaced depend on transport: in HTTP mode `signingSecretStatus` is included; in Socket Mode the required pair is `botTokenStatus` + `appTokenStatus`.

## Actions and gates

Slack tool actions are controlled by `channels.slack.actions.*`. The available action groups in current Slack tooling, all enabled by default, are:

| Group      | Default |
| ---------- | ------- |
| messages   | enabled |
| reactions  | enabled |
| pins       | enabled |
| memberInfo | enabled |
| emojiList  | enabled |

Current Slack **message actions** include `send`, `upload-file`, `download-file`, `read`, `edit`, `delete`, `pin`, `unpin`, `list-pins`, `member-info`, and `emoji-list`. The `download-file` action accepts Slack file IDs shown in inbound file placeholders and returns image previews for images, or local file metadata for other file types.

## Access control and routing

Access control spans three surfaces: the DM policy (who may direct-message the bot), the channel/group policy (which channels the bot acts in), and mention gating plus per-channel controls.

### DM policy

`channels.slack.dmPolicy` controls DM access, and `channels.slack.allowFrom` is the **canonical DM allowlist**. The four policy values are:

- `pairing` (default)
- `allowlist`
- `open` (requires `channels.slack.allowFrom` to include `"*"`)
- `disabled`

DM flags: `dm.enabled` (default `true`), `channels.slack.allowFrom`, `dm.allowFrom` (legacy), `dm.groupEnabled` (group DMs default `false`), and `dm.groupChannels` (optional MPIM allowlist). Multi-account precedence rules: `channels.slack.accounts.default.allowFrom` applies only to the `default` account; named accounts inherit `channels.slack.allowFrom` when their own `allowFrom` is unset; named accounts do **not** inherit `channels.slack.accounts.default.allowFrom`. Legacy `channels.slack.dm.policy` and `channels.slack.dm.allowFrom` still read for compatibility, and `openclaw doctor --fix` migrates them to `dmPolicy` and `allowFrom` when it can do so without changing access. Pairing in DMs uses `openclaw pairing approve slack <code>`.

### Channel policy

`channels.slack.groupPolicy` controls channel handling with three values: `open`, `allowlist`, and `disabled`. The channel allowlist lives under `channels.slack.channels` and **must use stable Slack channel IDs** (for example `C12345678`) as config keys. Runtime note: if `channels.slack` is completely missing (env-only setup), runtime falls back to `groupPolicy="allowlist"` and logs a warning — even if `channels.defaults.groupPolicy` is set.

Name/ID resolution rules: channel-allowlist and DM-allowlist entries are resolved at startup when token access allows; unresolved channel-name entries are kept as configured but ignored for routing by default; inbound authorization and channel routing are **ID-first by default**, and direct username/slug matching requires `channels.slack.dangerouslyAllowNameMatching: true`.

Name-based keys (`#channel-name` or `channel-name`) do **not** match under `groupPolicy: "allowlist"`. Because channel lookup is ID-first by default, a name-based key will never route successfully and **all messages in that channel are silently blocked**. This differs from `groupPolicy: "open"`, where the channel key is not required for routing and a name-based key appears to work. Always use the Slack channel ID as the key (right-click the channel → **Copy link**; the `C...` value at the end of the URL is the ID):

```json5
{
  channels: {
    slack: {
      groupPolicy: "allowlist",
      channels: {
        C12345678: { allow: true, requireMention: true },
      },
    },
  },
}
```

### Mentions and channel users

Channel messages are **mention-gated by default**. Mention sources: explicit app mention (`<@botId>`); Slack user-group mention (`<!subteam^S...>`) when the bot user is a member of that user group, which requires `usergroups:read`; mention regex patterns (`agents.list[].groupChat.mentionPatterns`, fallback `messages.groupChat.mentionPatterns`); and implicit reply-to-bot thread behavior (disabled when `thread.requireExplicitMention` is `true`).

Per-channel controls live under `channels.slack.channels.<id>` (names only via startup resolution or `dangerouslyAllowNameMatching`): `requireMention`, `users` (allowlist), `allowBots`, `skills`, `systemPrompt`, `tools`, and `toolsBySender`. The `toolsBySender` key format is `channel:`, `id:`, `e164:`, `username:`, `name:`, or `"*"` wildcard (legacy unprefixed keys still map to `id:` only).

`allowBots` is conservative for channels and private channels: bot-authored room messages are accepted only when the sending bot is explicitly listed in that room's `users` allowlist, or when at least one explicit Slack owner ID from `channels.slack.allowFrom` is currently a room member. Wildcards and display-name owner entries do **not** satisfy owner presence. Owner presence uses Slack `conversations.members`, so the app needs the matching read scope for the room type (`channels:read` for public channels, `groups:read` for private channels); if the member lookup fails, OpenClaw drops the bot-authored room message. Accepted bot-authored Slack messages use shared bot loop protection: configure `channels.defaults.botLoopProtection` for the default budget, then override with `channels.slack.botLoopProtection` or `channels.slack.channels.<id>.botLoopProtection` when a workspace or channel needs a different limit.

## Native approvals in Slack

Slack can act as a **native approval client** with interactive buttons and interactions, instead of falling back to the Web UI or terminal. Behavior:

- Exec and plugin approvals can render as Slack-native Block Kit prompts.
- `channels.slack.execApprovals.*` remains the native exec-approval client enablement and DM/channel routing config.
- Exec approval DMs use `channels.slack.execApprovals.approvers` or `commands.ownerAllowFrom`.
- Plugin approvals use Slack-native buttons when Slack is enabled as a native approval client for the originating session, or when `approvals.plugin` routes to the originating Slack session or a Slack target.
- Plugin approval DMs use Slack plugin approvers from `channels.slack.allowFrom`, named-account `allowFrom`, or the account default route.
- Approver authorization is still enforced: exec-only approvers cannot approve plugin requests unless they are also plugin approvers.

This uses the same shared approval button surface as other channels. When `interactivity` is enabled in the Slack app settings, approval prompts render as Block Kit buttons directly in the conversation, and those buttons are the primary approval UX; OpenClaw should only include a manual `/approve` command when the tool result says chat approvals are unavailable or manual approval is the only path. The config path is `channels.slack.execApprovals.enabled`, `channels.slack.execApprovals.approvers` (optional; falls back to `commands.ownerAllowFrom` when possible), `channels.slack.execApprovals.target` (`dm` | `channel` | `both`, default `dm`), plus `agentFilter` and `sessionFilter`.

Slack auto-enables native exec approvals when `enabled` is unset or `"auto"` and at least one exec approver resolves; it can also handle native plugin approvals through this native-client path when Slack plugin approvers resolve and the request matches the native-client filters. Set `enabled: false` to disable Slack as a native approval client explicitly, or `enabled: true` to force native approvals on when approvers resolve. Disabling Slack exec approvals does **not** disable native Slack plugin approval delivery enabled through `approvals.plugin`. The minimal default with no explicit Slack exec approval config:

```json5
{
  commands: {
    ownerAllowFrom: ["slack:U12345678"],
  },
}
```

Explicit Slack-native config is only needed to override approvers, add filters, or opt into origin-chat delivery:

```json5
{
  channels: {
    slack: {
      execApprovals: {
        enabled: true,
        approvers: ["U12345678"],
        target: "both",
      },
    },
  },
}
```

Shared `approvals.exec` forwarding is separate (use it only when exec approval prompts must also route to other chats or out-of-band targets), and shared `approvals.plugin` forwarding is also separate (Slack native delivery suppresses that fallback only when Slack can handle the plugin approval natively). Same-chat `/approve` also works in Slack channels and DMs that already support commands.

**Source**: OpenClaw documentation — `channels/slack` (mirror `inbox/openclaw_docs/channels/slack.md`), sections Token model · Actions and gates · Access control and routing · Native approvals in Slack
**Last Updated**: 2026-06-22
**Status**: Active
