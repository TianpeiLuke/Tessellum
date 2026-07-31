---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - slack
keywords:
  - openclaw slack slash command
  - slack interactive replies block kit
  - slack plugin modal view_submission
  - slack native approvals
  - slack interaction system events
  - channels.slack configuration reference
  - slack channel troubleshooting
  - slack socket mode http troubleshooting
topics:
  - OpenClaw
  - Slack Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/slack
access_control_group: ["general"]
---

# OpenClaw — Slack Interactivity, Operational Events, Config Reference & Troubleshooting

## Overview

This note is the interactivity-and-operations procedure for the OpenClaw Slack channel, covering the back half of the `channels/slack` source page: slash-command behavior, agent-authored interactive replies (buttons/selects compiled to Block Kit, including plugin-owned modal submissions), Slack as a native approval client, the operational/system-event surface, the high-signal `channels.slack.*` configuration reference, and the per-symptom troubleshooting ladder. It assumes the channel is already installed and authenticated (see the setup and security/access siblings) and documents what to configure and check once Slack is dispatching interactions and commands to the agent.

## Commands and Slash Behavior

Slash commands appear in Slack as either a single configured command or multiple native commands. Configure `channels.slack.slashCommand` to change command defaults; the documented defaults are `enabled: false`, `name: "openclaw"`, `sessionPrefix: "slack:slash"`, and `ephemeral: true`. In single-command mode the user invokes the configured command (for example `/openclaw /help`). Native commands require [additional manifest settings](https://docs.openclaw.ai/channels/slack#additional-manifest-settings) in the Slack app and are enabled with `channels.slack.commands.native: true` (or `commands.native: true` in global configuration). Native command auto-mode is **off** for Slack, so `commands.native: "auto"` does not enable Slack native commands; with native mode on, the user invokes the registered command directly (for example `/help`).

Native argument menus use an adaptive rendering strategy that shows a confirmation modal before dispatching a selected option value: up to 5 options render as button blocks; 6-100 options render as a static select menu; more than 100 options render as an external select with async option filtering when interactivity options handlers are available; and if Slack limits are exceeded, encoded option values fall back to buttons (for example `/think`). Slash sessions use isolated keys like `agent:<agentId>:slack:slash:<userId>` and still route command executions to the target conversation session using `CommandTargetSessionKey`.

## Interactive Replies

Slack can render agent-authored interactive reply controls, but this feature is disabled by default. For new agent, CLI, and plugin output, prefer the shared `presentation` buttons or select blocks — they use the same Slack interaction path while also degrading gracefully on other channels. Enable interactive replies globally:

```json5
{
  channels: {
    slack: {
      capabilities: {
        interactiveReplies: true,
      },
    },
  },
}
```

Or enable it for one Slack account only by nesting the capability under `accounts.<name>`:

```json5
{
  channels: {
    slack: {
      accounts: {
        ops: {
          capabilities: {
            interactiveReplies: true,
          },
        },
      },
    },
  },
}
```

When enabled, agents can still emit deprecated Slack-only reply directives such as `[[slack_buttons: Approve:approve, Reject:reject]]` and `[[slack_select: Choose a target | Canary:canary, Production:production]]`. These directives compile into Slack Block Kit and route clicks or selections back through the existing Slack interaction event path; keep them for old prompts and Slack-specific escape hatches, but use shared presentation for new portable controls. The directive compiler APIs are also deprecated for new producer code: `compileSlackInteractiveReplies(...)`, `parseSlackOptionsLine(...)`, `isSlackInteractiveRepliesEnabled(...)`, and `buildSlackInteractiveBlocks(...)`; use `presentation` payloads and `buildSlackPresentationBlocks(...)` for new Slack-rendered controls. Notes: this is Slack-specific legacy UI and other channels do not translate Slack Block Kit directives into their own button systems; the interactive callback values are OpenClaw-generated opaque tokens, not raw agent-authored values; and if generated interactive blocks would exceed Slack Block Kit limits, OpenClaw falls back to the original text reply instead of sending an invalid blocks payload.

### Plugin-Owned Modal Submissions

Slack plugins that register an interactive handler can also receive modal `view_submission` and `view_closed` lifecycle events before OpenClaw compacts the payload for the agent-visible system event. Use one of these routing patterns when opening a Slack modal: set `callback_id` to `openclaw:<namespace>:<payload>`; or keep an existing `callback_id` and put `pluginInteractiveData: "<namespace>:<payload>"` in the modal `private_metadata`. The handler receives `ctx.interaction.kind` as `view_submission` or `view_closed`, normalized `inputs`, and the full raw `stateValues` object from Slack. Callback-id-only routing is enough to invoke the plugin handler; include the existing modal `private_metadata` user/session routing fields when the modal should also produce an agent-visible system event. The agent receives a compact, redacted `Slack interaction: ...` system event, and if the handler returns `systemEvent.summary`, `systemEvent.reference`, or `systemEvent.data`, those fields are included in that compact event so the agent can reference plugin-owned storage without seeing the complete form payload.

## Native Approvals in Slack (cross-link)

Slack can act as a native approval client with interactive buttons and interactions instead of falling back to the Web UI or terminal — exec and plugin approvals can render as Slack-native Block Kit prompts. This surface is documented in full in the [Slack security/access sibling](oc_channels_slack_security_access.md); the interactivity-relevant points are that approvals reuse the same shared approval button surface as other channels, and when `interactivity` is enabled in the Slack app settings, approval prompts render as Block Kit buttons directly in the conversation. When those buttons are present they are the primary approval UX; OpenClaw should only include a manual `/approve` command when the tool result says chat approvals are unavailable or manual approval is the only path. Same-chat `/approve` also works in Slack channels and DMs that already support commands. The enabling/routing config (`channels.slack.execApprovals.*`, approver resolution via `commands.ownerAllowFrom`, and the `approvals.plugin` path) lives with the security/access note; see [Exec approvals](https://docs.openclaw.ai/tools/exec-approvals) for the full approval-forwarding model.

## Events and Operational Behavior

The Slack channel maps a range of platform events into agent-visible system events. Message edits/deletes are mapped into system events; thread broadcasts ("Also send to channel" thread replies) are processed as normal user messages; reaction add/remove events are mapped into system events; and member join/leave, channel created/renamed, and pin add/remove events are mapped into system events. `channel_id_changed` can migrate channel config keys when `configWrites` is enabled. Channel topic/purpose metadata is treated as untrusted context and can be injected into routing context, and thread starter plus initial thread-history context seeding are filtered by configured sender allowlists when applicable.

Block actions, shortcuts, and modal interactions emit structured `Slack interaction: ...` system events with rich payload fields: block actions carry selected values, labels, picker values, and `workflow_*` metadata; global shortcuts carry callback and actor metadata, routed to the actor's direct session; message shortcuts carry callback, actor, channel, thread, and selected-message context; and modal `view_submission` and `view_closed` events carry routed channel metadata and form inputs. Define global or message shortcuts in the Slack app configuration and use any non-empty callback ID — OpenClaw acknowledges matching shortcut payloads, applies the same DM/channel sender policy as other Slack interactions, and queues the sanitized event for the routed agent session. Trigger IDs and response URLs are redacted from agent context.

## Configuration Reference

The primary reference is [Configuration reference - Slack](https://docs.openclaw.ai/gateway/config-channels#slack). The high-signal `channels.slack.*` fields documented on this page, grouped by purpose:

- mode/auth: `mode`, `botToken`, `appToken`, `signingSecret`, `webhookPath`, `accounts.*`
- DM access: `dm.enabled`, `dmPolicy`, `allowFrom` (legacy: `dm.policy`, `dm.allowFrom`), `dm.groupEnabled`, `dm.groupChannels`
- compatibility toggle: `dangerouslyAllowNameMatching` (break-glass; keep off unless needed)
- channel access: `groupPolicy`, `channels.*`, `channels.*.users`, `channels.*.requireMention`
- threading/history: `replyToMode`, `replyToModeByChatType`, `thread.*`, `historyLimit`, `dmHistoryLimit`, `dms.*.historyLimit`
- delivery: `textChunkLimit`, `chunkMode`, `mediaMaxMb`, `streaming`, `streaming.nativeTransport`, `streaming.preview.toolProgress`
- unfurls: `unfurlLinks` (default: `false`), `unfurlMedia` for `chat.postMessage` link/media preview control; set `unfurlLinks: true` to opt back into link previews
- ops/features: `configWrites`, `commands.native`, `slashCommand.*`, `actions.*`, `userToken`, `userTokenReadOnly`

## Troubleshooting

The source page documents four symptom-keyed accordions. **No replies in channels** — check, in order: `groupPolicy`; the channel allowlist (`channels.slack.channels`), whose keys must be channel IDs (`C12345678`), not names (`#channel-name`), because name-based keys silently fail under `groupPolicy: "allowlist"` since channel routing is ID-first by default (find the ID by right-clicking the channel in Slack → **Copy link** and reading the `C...` value at the end of the URL); `requireMention`; the per-channel `users` allowlist; `messages.groupChat.visibleReplies`, which defaults to `"automatic"` for normal group/channel requests, so if you opted into `"message_tool"` and logs show assistant text with no `message(action=send)` call the model missed the visible message-tool path (final text stays private in this mode — inspect the gateway verbose log for suppressed payload metadata, or set it back to `"automatic"`); and `messages.groupChat.unmentionedInbound`, where `"room_event"` keeps unmentioned allowed channel chatter as ambient context that stays silent unless the agent calls the `message` tool.

```json5
{
  messages: {
    groupChat: {
      visibleReplies: "automatic",
    },
  },
}
```

Useful diagnostic commands for the channel are `openclaw channels status --probe`, `openclaw logs --follow`, and `openclaw doctor`.

```bash
openclaw channels status --probe
openclaw logs --follow
openclaw doctor
```

**DM messages ignored** — check `channels.slack.dm.enabled`; `channels.slack.dmPolicy` (or legacy `channels.slack.dm.policy`); pairing approvals / allowlist entries (`dmPolicy: "open"` still requires `channels.slack.allowFrom: ["*"]`); group DMs, which use MPIM handling so enable `channels.slack.dm.groupEnabled` and, if configured, include the MPIM in `channels.slack.dm.groupChannels`; and Slack Assistant DM events, where verbose logs mentioning `drop message_changed` usually mean Slack sent an edited Assistant-thread event without a recoverable human sender in message metadata. Use `openclaw pairing list slack` to inspect pairings. **Socket mode not connecting** — validate bot + app tokens and Socket Mode enablement in Slack app settings; the App-Level Token needs `connections:write`, and the Bot User OAuth Token must belong to the same Slack app/workspace as the app token. If `openclaw channels status --probe --json` shows `botTokenStatus` or `appTokenStatus: "configured_unavailable"`, the account is configured but the runtime could not resolve the SecretRef-backed value; logs such as `slack socket mode failed to start; retry ...` are recoverable start failures, while missing scopes, revoked tokens, and invalid auth fail fast, and a `slack token mismatch ...` log means the bot and app tokens appear to belong to different Slack apps.

**HTTP mode not receiving events** — validate the signing secret, the webhook path, the Slack Request URLs (Events + Interactivity + Slash Commands), a unique `webhookPath` per HTTP account, that the public URL terminates TLS and forwards requests to the Gateway path, and that the Slack app `request_url` path exactly matches `channels.slack.webhookPath` (default `/slack/events`). If `signingSecretStatus: "configured_unavailable"` appears in account snapshots, the account is configured but the runtime could not resolve the SecretRef-backed signing secret, and a repeated `slack: webhook path ... already registered` log means two HTTP accounts share a `webhookPath`. **Native/slash commands not firing** — verify whether you intended native command mode (`channels.slack.commands.native: true`) with matching slash commands registered in Slack, or single slash command mode (`channels.slack.slashCommand.enabled: true`); Slack does not create or remove slash commands automatically, `commands.native: "auto"` does not enable Slack native commands (use `true` and create the matching commands), in HTTP mode every Slack slash command must include the Gateway URL, and in Socket Mode command payloads arrive over the websocket so Slack ignores `slash_commands[].url`. Also check `commands.useAccessGroups`, DM authorization, channel allowlists, and per-channel `users` allowlists; Slack returns ephemeral errors for blocked slash-command senders, including `This channel is not allowed.` and `You are not authorized to use this command here.`

**Source**: OpenClaw documentation — `channels/slack` (mirror `inbox/openclaw_docs/channels/slack.md`, sections "Commands and slash behavior" → "Troubleshooting")
**Last Updated**: 2026-06-22
**Status**: Active
