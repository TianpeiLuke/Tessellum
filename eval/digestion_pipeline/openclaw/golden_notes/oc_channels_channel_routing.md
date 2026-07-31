---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - routing
keywords:
  - openclaw channel routing
  - outbound target prefixes
  - session key shapes
  - main dm route pinning
  - routing rules binding ladder
  - guarded inbound recording
  - session storage sessions.json
  - webchat cross-channel context
topics:
  - OpenClaw
  - Channel Routing
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/channels/channel-routing
access_control_group: ["general"]
---

# OpenClaw — Channels & Routing Model

## Overview

This note captures the OpenClaw **channel-routing model** — the shared target-prefix, session-key, and routing-rule grammar that every channel reuses — mirroring the `channels/channel-routing` source page. OpenClaw routes replies **back to the channel where a message came from**; the model does not choose a channel, and routing is deterministic and controlled by the host configuration. It covers the key terms (Channel / AccountId / AgentId / SessionKey), outbound target prefixes, session-key shapes for DMs / groups / channels / threads, main-DM route pinning, guarded inbound recording, the eight-step routing ladder that picks one agent, the pointer to broadcast groups, the `agents.list` + `bindings` config overview, session storage on disk, WebChat behavior, and reply context.

## Key Terms

The routing model is built from four entities. A **Channel** is one of `telegram`, `whatsapp`, `discord`, `irc`, `googlechat`, `slack`, `signal`, `imessage`, `line`, plus plugin channels; `webchat` is the internal WebChat UI channel and is **not** a configurable outbound channel. An **AccountId** is a per-channel account instance (when supported), and an optional channel default account `channels.<channel>.defaultAccount` chooses which account is used when an outbound path does not specify `accountId`. In multi-account setups you should set an explicit default (`defaultAccount` or `accounts.default`) when two or more accounts are configured; without it, fallback routing may pick the first normalized account ID. An **AgentId** is an isolated workspace + session store ("brain"). A **SessionKey** is the bucket key used to store context and control concurrency.

## Outbound Target Prefixes

Explicit outbound targets may include a **provider prefix**, such as `telegram:123` or `tg:123`. Core treats that prefix as a channel-selection hint **only** when the selected channel is `last` or otherwise unresolved, and **only** when the loaded plugin advertises that prefix. If the caller already selected an explicit channel, the provider prefix must match that channel; cross-channel combinations such as WhatsApp delivery to `telegram:123` fail before plugin-specific target normalization.

Separately, **target-kind and service prefixes** such as `channel:<id>`, `user:<id>`, `room:<id>`, `thread:<id>`, `imessage:<handle>`, and `sms:<number>` stay inside the selected channel's grammar. They do not select the provider by themselves.

## Session Key Shapes

Direct messages collapse to the agent's **main** session by default, of the form `agent:<agentId>:<mainKey>` (default: `agent:main:main`). Even when direct-message conversation history is shared with main, sandbox and tool policy use a derived per-account direct-chat runtime key for external DMs, so channel-originated messages are not treated like local main-session runs. Groups and channels remain isolated per channel — groups use `agent:<agentId>:<channel>:group:<id>` and channels/rooms use `agent:<agentId>:<channel>:channel:<id>`. For threads, Slack/Discord threads append `:thread:<threadId>` to the base key, while Telegram forum topics embed `:topic:<topicId>` in the group key. Two concrete examples from the source:

```
agent:main:telegram:group:-1001234567890:topic:42
agent:main:discord:channel:123456:thread:987654
```

## Main DM Route Pinning

When `session.dmScope` is `main`, direct messages may share one main session. To prevent the session's `lastRoute` from being overwritten by non-owner DMs, OpenClaw infers a **pinned owner** from `allowFrom` when all of these are true: `allowFrom` has exactly one non-wildcard entry; the entry can be normalized to a concrete sender ID for that channel; and the inbound DM sender does not match that pinned owner. In that mismatch case, OpenClaw still records inbound session metadata, but it skips updating the main session `lastRoute`.

## Guarded Inbound Recording

Channel plugins can mark an inbound session record as `createIfMissing: false` when a guarded path must not create a new OpenClaw session. In that mode, OpenClaw may update metadata and `lastRoute` for an existing session, but it does not create a route-only session entry just because a message was observed.

## Routing Rules (How an Agent Is Chosen)

Routing picks **one agent** for each inbound message via an ordered eight-step ladder:

1. **Exact peer match** (`bindings` with `peer.kind` + `peer.id`).
2. **Parent peer match** (thread inheritance).
3. **Guild + roles match** (Discord) via `guildId` + `roles`.
4. **Guild match** (Discord) via `guildId`.
5. **Team match** (Slack) via `teamId`.
6. **Account match** (`accountId` on the channel).
7. **Channel match** (any account on that channel, `accountId: "*"`).
8. **Default agent** (`agents.list[].default`, else first list entry, fallback to `main`).

When a binding includes multiple match fields (`peer`, `guildId`, `teamId`, `roles`), **all provided fields must match** for that binding to apply. The matched agent determines which workspace and session store are used.

## Broadcast Groups (Pointer)

Broadcast groups let you run **multiple agents** for the same peer **when OpenClaw would normally reply** (for example: in WhatsApp groups, after mention/activation gating). The configured set is keyed by peer with a `strategy` field:

```json5
{
  broadcast: {
    strategy: "parallel",
    "120363403215116621@g.us": ["alfred", "baerbel"],
    "+15555550123": ["support", "logger"],
  },
}
```

The full fan-out contract is documented separately — see the Broadcast Groups note in Related Notes.

## Config Overview

Routing config has two main blocks: `agents.list` holds named agent definitions (workspace, model, etc.), and `bindings` maps inbound channels/accounts/peers to agents. Example:

```json5
{
  agents: {
    list: [{ id: "support", name: "Support", workspace: "~/.openclaw/workspace-support" }],
  },
  bindings: [
    { match: { channel: "slack", teamId: "T123" }, agentId: "support" },
    { match: { channel: "telegram", peer: { kind: "group", id: "-100123" } }, agentId: "support" },
  ],
}
```

## Session Storage

Session stores live under the state directory (default `~/.openclaw`): the store is at `~/.openclaw/agents/<agentId>/sessions/sessions.json`, and JSONL transcripts live alongside the store. You can override the store path via `session.store` and `{agentId}` templating. Gateway and ACP session discovery also scans disk-backed agent stores under the default `agents/` root and under templated `session.store` roots. Discovered stores must stay inside that resolved agent root and use a regular `sessions.json` file; symlinks and out-of-root paths are ignored.

## WebChat Behavior and Reply Context

WebChat attaches to the **selected agent** and defaults to the agent's main session, so WebChat lets you see cross-channel context for that agent in one place. For reply context, inbound replies include `ReplyToId`, `ReplyToBody`, and `ReplyToSender` when available, and quoted context is appended to `Body` as a `[Replying to ...]` block. This is consistent across channels.

**Source**: OpenClaw documentation — `channels/channel-routing` (mirror `inbox/openclaw_docs/channels/channel-routing.md`)
**Last Updated**: 2026-06-22
**Status**: Active
