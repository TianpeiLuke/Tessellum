---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - channel_docking
keywords:
  - openclaw channel docking
  - dock command reply route
  - session identitylinks
  - dock-discord dock-slack
  - lastchannel lastto lastaccountid
  - cross-channel session forwarding
  - channel-prefixed peer id
topics:
  - OpenClaw
  - Channel Docking
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/channel-docking
access_control_group: ["general"]
---

# OpenClaw — Channel Docking (Move a Session's Reply Route)

## Overview

This note is the operator procedure for **channel docking** in OpenClaw: keeping one session's conversation context while moving where its future replies are delivered between linked chat channels (Telegram, Discord, Slack, Mattermost). It mirrors the `concepts/channel-docking` source page — the call-forwarding analogy, the required `session.identityLinks` identity group, the bundled `/dock-<channel>` commands and their underscore aliases, the session delivery fields that change (`lastChannel`, `lastTo`, `lastAccountId`), what docking deliberately does **not** change, and the troubleshooting cases.

## What docking does

Channel docking is **call forwarding for one OpenClaw session**: it keeps the same conversation context but changes where future replies for that session are delivered. The session is **not recreated** and the transcript history stays attached to the same session — only the delivery route changes.

In the source example, Alice can message OpenClaw on both Telegram and Discord. If she sends `/dock_discord` from her Telegram session, OpenClaw keeps the current session context and changes the reply route: before docking, replies go to Telegram `123`; after `/dock_discord`, replies go to Discord `456`.

## Why use it

Use docking when a task starts in one chat app but the next replies should land somewhere else. The common flow from the source is:

1. Start an agent task from Telegram.
2. Move to Discord where you are coordinating work.
3. Send `/dock_discord` from the Telegram session.
4. Keep the same OpenClaw session, but receive future replies in Discord.

## Required config — `session.identityLinks`

Docking requires `session.identityLinks`. The **source sender and target peer must be in the same identity group**. Example config:

```json5
{
  session: {
    identityLinks: {
      alice: ["telegram:123", "discord:456", "slack:U123"],
    },
  },
}
```

The values are **channel-prefixed peer ids**:

| Value          | Meaning                      |
| -------------- | ---------------------------- |
| `telegram:123` | Telegram sender id `123`     |
| `discord:456`  | Discord direct peer id `456` |
| `slack:U123`   | Slack user id `U123`         |

The canonical key (`alice` above) is **only the shared identity group name**. Dock commands use the channel-prefixed values to prove that the source sender and target peer are the same person.

## Commands — `/dock-<channel>`

Dock commands are **generated from loaded channel plugins that support native commands**. The current bundled commands are:

| Target channel | Command            | Alias              |
| -------------- | ------------------ | ------------------ |
| Discord        | `/dock-discord`    | `/dock_discord`    |
| Mattermost     | `/dock-mattermost` | `/dock_mattermost` |
| Slack          | `/dock-slack`      | `/dock_slack`      |
| Telegram       | `/dock-telegram`   | `/dock_telegram`   |

The underscore aliases (`/dock_discord`, etc.) are useful on native command surfaces such as Telegram.

## What changes — session delivery fields

Docking updates the active session **delivery fields**:

| Session field   | Example after `/dock_discord`            |
| --------------- | ---------------------------------------- |
| `lastChannel`   | `discord`                                |
| `lastTo`        | `456`                                    |
| `lastAccountId` | the target channel account, or `default` |

Those fields are persisted in the session store and used by later reply delivery for that session.

## What does not change

Docking only changes the delivery route for the current session. It does **not**:

- create channel accounts
- connect a new Discord, Telegram, Slack, or Mattermost bot
- grant access to a user
- bypass channel allowlists or DM policies
- move transcript history to another session
- make unrelated users share a session

## Troubleshooting

**The command says the sender is not linked.** Add both the current sender and the target peer to the same `session.identityLinks` group. For example, if Telegram sender `123` should dock to Discord peer `456`, include both `telegram:123` and `discord:456`.

**The command says no active session exists.** Dock from an existing direct-chat session. The command needs an active session entry so it can persist the new route.

**Replies still go to the old channel.** Check that the command replied with a success message, and confirm the target peer id matches the id used by that channel. Docking only changes the active session route; another session may still route elsewhere.

**I need to switch back.** Send the matching command for the original channel, such as `/dock_telegram` or `/dock-telegram`, from a linked sender.

## Related Notes

**Terms**

- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — gateway product; relevance: docking moves an OpenClaw session's reply route.
- **[DM Pairing](../../term_dictionary/term_dm_pairing.md)** — identity linking; relevance: `session.identityLinks` proves sender/peer are the same person.
- **[Session Persistence](../../term_dictionary/term_session_persistence.md)** — durable session; relevance: docking persists new delivery fields to the session store.
- **[Session ID](../../term_dictionary/term_sessionid.md)** — session identifier; relevance: the same session keeps its transcript while the route changes.
- **[Messaging Gateway](../../term_dictionary/term_messaging_gateway.md)** — chat gateway; relevance: the Gateway re-routes replies across linked channels.
- **[Slack](../../term_dictionary/term_slack.md)** — chat platform; relevance: `/dock-slack` is one bundled dock target.
- **[Message Queue](../../term_dictionary/term_message_queue.md)** — delivery queue; relevance: future replies for the session are delivered to the new channel.
- **[Channel Adapter](../../term_dictionary/term_channel_adapter.md)** — per-platform channel plugin; relevance: dock commands are generated from loaded channel adapters that support native commands.

**Docs**

- **[oc_concepts_architecture](oc_concepts_architecture.md)** — gateway architecture (this series); relevance: the Gateway that delivers docked replies.
- **[oc_concepts_agent](oc_concepts_agent.md)** — agent/session contract (this series); relevance: the session whose route docks.
- **[oc_concepts_session](oc_concepts_session.md)** — session model (co06); relevance: the `lastChannel`/`lastTo`/`lastAccountId` delivery fields.
- **[oc_concepts_multi_agent](oc_concepts_multi_agent_routing.md)** — multi-agent routing (co05); relevance: channel routing / identity groups.
- **[oc_concepts_messages](oc_concepts_messages.md)** — message lifecycle (co04); relevance: reply delivery the route change affects.
- **[cc_channels_overview](../claude_code/cc_channels_overview.md)** — Claude Code channels; relevance: cross-tool multi-channel delivery model.
- **[cc_channel_reply_tool](../claude_code/cc_channel_reply_tool.md)** — channel reply routing; relevance: how a reply is routed to a channel (analog).
- **[cc_claude_code_in_slack](../claude_code/cc_claude_code_in_slack.md)** — Claude Code in Slack; relevance: Slack as a dock target/channel analog.
- **[hermes_messaging_slack](../hermes_agent/hermes_messaging_slack.md)** — Hermes Slack; relevance: Slack channel adapter (`/dock-slack`).
- **[hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md)** — Hermes messaging gateway; relevance: cross-channel routing architecture.
- **[band_chat_rooms_and_routing](../band/band_chat_rooms_and_routing.md)** — Band chat routing; relevance: cross-platform session/route forwarding analog.

**Repos**

- **[repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md)** — channels; relevance: dock-command generation from channel plugins.
- **[repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md)** — messaging channels; relevance: per-channel native dock commands.
- **[repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md)** — sessions; relevance: persists the updated delivery route.

**Snippets**

- **[snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md)** — binding/routing; relevance: how a session binds to a channel route.
- **[snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md)** — conversation resolution; relevance: resolving the target peer id for docking.
- **[snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md)** — adapter contract; relevance: native-command-capable channel plugins generate dock commands.
- **[snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md)** — session-id resolution; relevance: finding the active session to re-route.
- **[snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md)** — DM pairing allowlist; relevance: identityLinks group membership check.
- **[snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md)** — match resolver; relevance: matching the channel-prefixed peer id.
- **[snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md)** — thread bindings; relevance: session-to-channel binding the dock updates.
- **[snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md)** — send policy; relevance: docking does not bypass channel allowlists/DM policy.
- **[snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md)** — channel registry normalize; relevance: channel-prefixed peer-id normalization.
- **[snippet_openclaw_sessions_session_label](../../code_snippets/snippet_openclaw_sessions_session_label.md)** — session label; relevance: the session whose lastChannel/lastTo fields change.
- **[snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md)** — channel kernel dispatch; relevance: delivering replies to the docked channel.

## References

- [OpenClaw Docs — Channel docking](https://docs.openclaw.ai/concepts/channel-docking)
- [OpenClaw Docs — Sessions](https://docs.openclaw.ai/concepts/session)
- [OpenClaw Docs — Architecture](https://docs.openclaw.ai/concepts/architecture)

**Source**: OpenClaw documentation — `concepts/channel-docking` (mirror `inbox/openclaw_docs/concepts/channel-docking.md`)
**Last Updated**: 2026-06-22
**Status**: Active
