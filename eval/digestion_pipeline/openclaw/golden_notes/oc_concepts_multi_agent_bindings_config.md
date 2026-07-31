---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - multi_agent
keywords:
  - openclaw agents add
  - openclaw multi-agent bindings config
  - per-channel account binding
  - whatsapp dm split routing
  - discord telegram per-agent bot
  - per-agent sandbox tools allow deny
  - accountId binding match
  - openclaw channels login account
topics:
  - OpenClaw
  - Multi-Agent Bindings
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/multi-agent
access_control_group: ["general"]
---

# OpenClaw — Configuring Multiple Agents and Channel Bindings

## Overview

This note is the configuration procedure for running multiple isolated agents in one OpenClaw Gateway and wiring inbound channel accounts to them. It covers the `openclaw agents add` wizard, the four-step quick start (workspaces, channel accounts, agents/accounts/bindings, restart + verify), the one-WhatsApp-number DM-split pattern, multi-account routing by `accountId`, per-platform binding examples (Discord, Telegram, WhatsApp), common split patterns, and per-agent sandbox + tool allow/deny configuration. It mirrors the configuration ("how-to") half of the `concepts/multi-agent` source page; the conceptual routing model (what an agent is, most-specific-wins precedence) lives in the sibling routing note. All config keys, CLI commands, and JSON5 examples are reproduced verbatim from the source.

## Agent helper (`openclaw agents add`)

Use the agent wizard to add a new isolated agent (`openclaw agents add work`), then add `bindings` (or let the wizard do it) to route inbound messages. Verify the agents and their bindings with `openclaw agents list --bindings`.

## Quick start

Bringing up a multi-agent gateway is a four-step flow. (1) **Create each agent workspace** — use the wizard (or create workspaces manually); each agent gets its own workspace with `SOUL.md`, `AGENTS.md`, and optional `USER.md`, plus a dedicated `agentDir` and session store under `~/.openclaw/agents/<agentId>`. (2) **Create channel accounts** — create one account per agent on your preferred channels: for Discord, one bot per agent, enable Message Content Intent, copy each token; for Telegram, one bot per agent via BotFather, copy each token; for WhatsApp, link each phone number per account (see the channel guides for Discord, Telegram, WhatsApp). (3) **Add agents, accounts, and bindings** — add agents under `agents.list`, channel accounts under `channels.<channel>.accounts`, and connect them with `bindings`. (4) **Restart and verify** — restart the gateway, then list bindings and probe channel status. The CLI commands across these steps:

```bash
openclaw agents add coding
openclaw agents add social
openclaw channels login --channel whatsapp --account work
openclaw gateway restart
openclaw agents list --bindings
openclaw channels status --probe
```

## One WhatsApp number, multiple people (DM split)

You can route **different WhatsApp DMs** to different agents while staying on **one WhatsApp account**. Match on sender E.164 (like `+15551234567`) with `peer.kind: "direct"`. Replies still come from the same WhatsApp number (no per-agent sender identity). The source warns that direct chats collapse to the agent's **main session key**, so true isolation requires **one agent per person**. The binding/channel config for this pattern:

```json5
{
  agents: {
    list: [
      { id: "alex", workspace: "~/.openclaw/workspace-alex" },
      { id: "mia", workspace: "~/.openclaw/workspace-mia" },
    ],
  },
  bindings: [
    {
      agentId: "alex",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230001" } },
    },
    {
      agentId: "mia",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230002" } },
    },
  ],
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551230001", "+15551230002"],
    },
  },
}
```

Two caveats the source calls out: DM access control is **global per WhatsApp account** (pairing/allowlist), not per agent; and for shared groups, bind the group to one agent or use Broadcast groups.

## Multiple accounts / phone numbers

Channels that support **multiple accounts** (e.g. WhatsApp) use `accountId` to identify each login. Each `accountId` can be routed to a different agent, so one server can host multiple phone numbers without mixing sessions. If you want a channel-wide default account when `accountId` is omitted, set `channels.<channel>.defaultAccount` (optional); when unset, OpenClaw falls back to `default` if present, otherwise the first configured account id (sorted). Common channels supporting this pattern include `whatsapp`, `telegram`, `discord`, `slack`, `signal`, `imessage`, `irc`, `line`, `googlechat`, `mattermost`, `matrix`, `nextcloud-talk`, `zalo`, `zalouser`, `nostr`, and `feishu`.

## Platform examples

### Discord bots per agent

Each Discord bot account maps to a unique `accountId`. Bind each account to an agent and keep allowlists per bot. Invite each bot to the guild and enable Message Content Intent. Tokens live in `channels.discord.accounts.<id>.token` (the default account can use `DISCORD_BOT_TOKEN`):

```json5
{
  agents: {
    list: [
      { id: "main", workspace: "~/.openclaw/workspace-main" },
      { id: "coding", workspace: "~/.openclaw/workspace-coding" },
    ],
  },
  bindings: [
    { agentId: "main", match: { channel: "discord", accountId: "default" } },
    { agentId: "coding", match: { channel: "discord", accountId: "coding" } },
  ],
  channels: {
    discord: {
      groupPolicy: "allowlist",
      accounts: {
        default: {
          token: "DISCORD_BOT_TOKEN_MAIN",
          guilds: {
            "123456789012345678": {
              channels: {
                "222222222222222222": { allow: true, requireMention: false },
              },
            },
          },
        },
        coding: {
          token: "DISCORD_BOT_TOKEN_CODING",
          guilds: {
            "123456789012345678": {
              channels: {
                "333333333333333333": { allow: true, requireMention: false },
              },
            },
          },
        },
      },
    },
  },
}
```

### Telegram bots per agent

Create one bot per agent with BotFather and copy each token; tokens live in `channels.telegram.accounts.<id>.botToken` (the default account can use `TELEGRAM_BOT_TOKEN`). For multiple bots in the same Telegram group, invite each bot and mention the bot that should answer. Disable BotFather Privacy Mode for each group bot, then re-add the bot so Telegram applies the setting. Allow groups with `channels.telegram.groups`, or use `groupPolicy: "open"` only for trusted group deployments. Put sender user IDs in `groupAllowFrom`; group and supergroup IDs belong in `channels.telegram.groups`, not `groupAllowFrom`. Bind by `accountId` so each bot routes to its own agent:

```json5
{
  agents: {
    list: [
      { id: "main", workspace: "~/.openclaw/workspace-main" },
      { id: "alerts", workspace: "~/.openclaw/workspace-alerts" },
    ],
  },
  bindings: [
    { agentId: "main", match: { channel: "telegram", accountId: "default" } },
    { agentId: "alerts", match: { channel: "telegram", accountId: "alerts" } },
  ],
  channels: {
    telegram: {
      accounts: {
        default: {
          botToken: "123456:ABC...",
          dmPolicy: "pairing",
        },
        alerts: {
          botToken: "987654:XYZ...",
          dmPolicy: "allowlist",
          allowFrom: ["tg:123456789"],
        },
      },
    },
  },
}
```

### WhatsApp numbers per agent

Link each account before starting the gateway (`openclaw channels login --channel whatsapp --account personal` and `... --account biz`), then configure `agents.list` with explicit `agentDir`, the `bindings` for `accountId` and an optional per-peer override, optional agent-to-agent messaging (off by default; must be explicitly enabled + allowlisted), and per-account WhatsApp `authDir` overrides:

```js
{
  agents: {
    list: [
      {
        id: "home",
        default: true,
        name: "Home",
        workspace: "~/.openclaw/workspace-home",
        agentDir: "~/.openclaw/agents/home/agent",
      },
      {
        id: "work",
        name: "Work",
        workspace: "~/.openclaw/workspace-work",
        agentDir: "~/.openclaw/agents/work/agent",
      },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
    {
      agentId: "work",
      match: {
        channel: "whatsapp",
        accountId: "personal",
        peer: { kind: "group", id: "1203630...@g.us" },
      },
    },
  ],
  tools: {
    agentToAgent: { enabled: false, allow: ["home", "work"] },
  },
  channels: {
    whatsapp: {
      accounts: { personal: {}, biz: {} },
    },
  },
}
```

The source notes that the WhatsApp `accounts.<id>.authDir` defaults to `~/.openclaw/credentials/whatsapp/<account>` and is an optional override.

## Common patterns

The source documents three reusable split patterns, each with a worked config example. **WhatsApp daily + Telegram deep work** splits by channel — route WhatsApp to a fast everyday agent (e.g. `model: "anthropic/claude-sonnet-4-6"`) and Telegram to an Opus agent (`model: "anthropic/claude-opus-4-6"`) using `accountId: "*"` bindings so they keep working if you add accounts later; to route a single DM/group to Opus while keeping the rest on chat, add a `match.peer` binding (peer matches always win over channel-wide rules). **Same channel, one peer to Opus** keeps WhatsApp on the fast agent but routes one DM to Opus via a `peer: { kind: "direct", id: "+15551234567" }` binding placed above the channel-wide rule (peer bindings always win). **Family agent bound to a WhatsApp group** binds a dedicated agent to a single WhatsApp group (`peer: { kind: "group", id: "120363999999999999@g.us" }`) with mention gating (`identity: { name: "Family Bot" }`, `groupChat.mentionPatterns: ["@family", "@familybot", "@Family Bot"]`) and a tighter tool policy — its `sandbox: { mode: "all", scope: "agent" }` and `tools.allow`/`tools.deny` are shown verbatim in the next section. The source notes that tool allow/deny lists are **tools**, not skills (if a skill needs to run a binary, ensure `exec` is allowed and the binary exists in the sandbox), and for stricter gating you set `agents.list[].groupChat.mentionPatterns` and keep group allowlists enabled for the channel.

## Per-agent sandbox and tool configuration

Each agent can have its own sandbox and tool restrictions, set on its `agents.list[]` entry. Sandbox `mode` can be `"off"` (no sandbox) or `"all"` (always sandboxed); `scope: "agent"` gives one container per agent; and `sandbox.docker.setupCommand` runs once on container creation:

```js
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: { mode: "off" },
      },
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",
          scope: "agent",
          docker: { setupCommand: "apt-get update && apt-get install -y git curl" },
        },
        tools: {
          allow: ["read"],
          deny: ["exec", "write", "edit", "apply_patch"],
        },
      },
    ],
  },
}
```

The source adds three constraints. `setupCommand` lives under `sandbox.docker` and runs once on container creation; per-agent `sandbox.docker.*` overrides are ignored when the resolved scope is `"shared"`. The benefits are security isolation (restrict tools for untrusted agents), resource control (sandbox specific agents while keeping others on host), and flexible per-agent policies. Finally, `tools.elevated` is **global** and sender-based — it is not configurable per agent; for per-agent boundaries use `agents.list[].tools` to deny `exec`, and for group targeting use `agents.list[].groupChat.mentionPatterns` so @mentions map cleanly to the intended agent. The source links a dedicated "Multi-agent sandbox and tools" page for detailed examples.

**Source**: OpenClaw documentation — `concepts/multi-agent` (mirror `inbox/openclaw_docs/concepts/multi-agent.md`)
**Last Updated**: 2026-06-22
**Status**: Active
