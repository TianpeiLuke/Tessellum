---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - feishu
keywords:
  - feishu advanced configuration
  - feishu streaming interactive cards
  - feishu quota optimization
  - feishu acp sessions binding
  - feishu multi-agent routing bindings
  - dynamic agent creation per-user isolation
  - dmscope per-channel-peer
  - feishu configuration reference
topics:
  - OpenClaw
  - Feishu Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/feishu
access_control_group: ["general"]
---

# OpenClaw — Feishu Advanced Configuration, ACP Sessions, and Per-User Agent Isolation

## Overview

This note covers the advanced half of the OpenClaw Feishu/Lark channel: multi-account setup, message limits, streaming interactive cards, quota optimization, ACP session bindings, multi-agent routing, per-user dynamic agent isolation, and the full configuration reference table. It mirrors the `channels/feishu` source page's "Advanced configuration", "Per-user agent isolation (Dynamic Agent Creation)", and "Configuration reference" sections. The basic connect/access-control/troubleshooting half lives in the sibling setup note. Every config key, default, and CLI command below is reproduced verbatim from the source; all keys are nested under `channels.feishu.*` unless noted otherwise.

## Multiple Accounts

A single Feishu channel can run several bot accounts. Configure `defaultAccount` plus an `accounts` map keyed by account id; each account carries its own `appId` / `appSecret` / `name`, an optional `enabled: false` to keep a backup account dormant, and an optional per-account `tts` block.

```json5
{
  channels: {
    feishu: {
      defaultAccount: "main",
      accounts: {
        main: {
          appId: "cli_xxx",
          appSecret: "xxx",
          name: "Primary bot",
          tts: {
            providers: {
              openai: { voice: "shimmer" },
            },
          },
        },
        backup: {
          appId: "cli_yyy",
          appSecret: "yyy",
          name: "Backup bot",
          enabled: false,
        },
      },
    },
  },
}
```

`defaultAccount` controls which account is used when outbound APIs do not specify an `accountId`. `accounts.<id>.tts` uses the same shape as `messages.tts` and deep-merges over global TTS config, so multi-bot Feishu setups can keep shared provider credentials globally while overriding only voice, model, persona, or auto mode per account.

## Message Limits, Streaming, and Quota Optimization

Two limits cap message size: `textChunkLimit` is the outbound text chunk size (default `2000` chars) and `mediaMaxMb` is the media upload/download limit (default `30` MB).

Feishu/Lark supports streaming replies via interactive cards: when enabled, the bot updates the card in real time as it generates text. Set `streaming: false` to send the complete reply in one message. `blockStreaming` is off by default; enable it only when you want completed assistant blocks flushed before the final reply.

```json5
{
  channels: {
    feishu: {
      streaming: true, // enable streaming card output (default: true)
      blockStreaming: true, // opt into completed-block streaming
    },
  },
}
```

To reduce Feishu/Lark API calls, two optional quota-optimization flags exist: `typingIndicator` (default `true`) — set `false` to skip typing reaction calls — and `resolveSenderNames` (default `true`) — set `false` to skip sender profile lookups.

## ACP Sessions

Feishu/Lark supports ACP (Agent Client Protocol) for DMs and group thread messages. Feishu/Lark ACP is text-command driven — there are no native slash-command menus, so use `/acp ...` messages directly in the conversation. A persistent binding declares an ACP-runtime agent (`runtime.type: "acp"` with `acp.backend: "acpx"`, `acp.mode: "persistent"`) and `bindings[]` entries that match `channel: "feishu"` plus a `peer` of `kind: "direct"` (with an `ou_` open_id) or `kind: "group"`.

```json5
{
  agents: {
    list: [
      {
        id: "codex",
        runtime: {
          type: "acp",
          acp: {
            agent: "codex",
            backend: "acpx",
            mode: "persistent",
            cwd: "/workspace/openclaw",
          },
        },
      },
    ],
  },
  bindings: [
    {
      type: "acp",
      agentId: "codex",
      match: {
        channel: "feishu",
        accountId: "default",
        peer: { kind: "direct", id: "ou_1234567890" },
      },
    },
    {
      type: "acp",
      agentId: "codex",
      match: {
        channel: "feishu",
        accountId: "default",
        peer: { kind: "group", id: "oc_group_chat:topic:om_topic_root" },
      },
      acp: { label: "codex-feishu-topic" },
    },
  ],
}
```

To spawn an ACP session interactively, send `/acp spawn codex --thread here` in a Feishu/Lark DM or thread. `--thread here` works for DMs and Feishu/Lark thread messages; follow-up messages in the bound conversation route directly to that ACP session.

## Multi-Agent Routing

Use `bindings` to route Feishu/Lark DMs or groups to different agents — each binding names an `agentId` from `agents.list` and a `match` describing which peer routes there. The routing fields are: `match.channel` is `"feishu"`; `match.peer.kind` is `"direct"` (DM) or `"group"` (group chat); and `match.peer.id` is the user Open ID (`ou_xxx`) or group ID (`oc_xxx`).

```json5
{
  agents: {
    list: [
      { id: "main" },
      { id: "agent-a", workspace: "/home/user/agent-a" },
      { id: "agent-b", workspace: "/home/user/agent-b" },
    ],
  },
  bindings: [
    {
      agentId: "agent-a",
      match: {
        channel: "feishu",
        peer: { kind: "direct", id: "ou_xxx" },
      },
    },
    {
      agentId: "agent-b",
      match: {
        channel: "feishu",
        peer: { kind: "group", id: "oc_zzz" },
      },
    },
  ],
}
```

## Per-User Agent Isolation (Dynamic Agent Creation)

Enable `dynamicAgentCreation` to automatically create **isolated agent instances** for each DM user. Each user gets their own independent workspace directory, separate `USER.md` / `SOUL.md` / `MEMORY.md`, private conversation history, and isolated skills and state — essential for public bots where each user should have their own private AI assistant experience. Dynamic bindings include the normalized Feishu `accountId`, so default and named accounts route each sender to the correct dynamic agent. If a named account created an unscoped dynamic agent on an older release, that legacy agent still counts toward `maxAgents`; confirm it is not used by the default account before removing it, or temporarily increase `maxAgents`, because OpenClaw cannot safely infer which account owns ambiguous legacy state.

### Quick Setup

Enable per-user isolation by setting an open DM policy plus the `dynamicAgentCreation` block with `enabled: true` and path templates, and set the global `session.dmScope`.

```json5
{
  channels: {
    feishu: {
      dmPolicy: "open",
      allowFrom: ["*"],
      dynamicAgentCreation: {
        enabled: true,
        workspaceTemplate: "~/.openclaw/workspace-{agentId}",
        agentDirTemplate: "~/.openclaw/agents/{agentId}/agent",
      },
    },
  },
  session: {
    // Critical: makes each user's DM their "main session"
    // Automatically loads USER.md / SOUL.md / MEMORY.md
    // For stronger isolation, use "per-channel-peer" instead
    dmScope: "main",
  },
}
```

### How It Works

When a new user sends their first DM, the channel performs five steps in order: (1) generates a unique `agentId` — `feishu-{user_open_id}` for the default account, or a bounded account-prefixed identity digest for a named account; (2) creates a new workspace at the `workspaceTemplate` path; (3) registers the agent and creates a binding for this user; (4) the workspace helper ensures bootstrap files (`AGENTS.md`, `SOUL.md`, `USER.md`, etc.) on first access; and (5) routes all future messages from this user to their dedicated agent.

### Configuration Options

The `dynamicAgentCreation` block has four settings (all under `channels.feishu.dynamicAgentCreation`):

| Setting             | Description                                | Default                              |
| ------------------- | ------------------------------------------ | ------------------------------------ |
| `enabled`           | Enable automatic per-user agent creation   | `false`                              |
| `workspaceTemplate` | Path template for dynamic agent workspaces | `~/.openclaw/workspace-{agentId}`    |
| `agentDirTemplate`  | Agent directory name template              | `~/.openclaw/agents/{agentId}/agent` |
| `maxAgents`         | Maximum number of dynamic agents to create | unlimited                            |

Two template variables are available: `{agentId}` is the generated agent ID (e.g., `feishu-ou_xxxxxx` or `feishu-support-<identity_digest>`) and `{userId}` is the sender's Feishu open_id (e.g., `ou_xxxxxx`).

### Session Scope

`session.dmScope` controls how direct messages are mapped to agent sessions; this is a **global setting** that affects all channels, not just Feishu.

| Value                        | Behavior                                                            | Best for                                                           |
| ---------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `"main"`                     | Each user's DM maps to their agent's main session                   | Single-user bots where you want `USER.md` / `SOUL.md` to auto-load |
| `"per-channel-peer"`         | Each (channel + user) combination gets a separate session           | Public multi-user bots needing stronger isolation                  |
| `"per-account-channel-peer"` | Each (account + channel + user) combination gets a separate session | Multi-account bots needing account-level session isolation         |

**Tradeoff**: Using `"main"` enables automatic bootstrap file loading (`USER.md`, `SOUL.md`, `MEMORY.md`), but means all DMs across all channels share the same session key pattern. For public multi-user bots where isolation matters more than bootstrap auto-loading, consider `"per-channel-peer"` and manage bootstrap files manually. Use `"per-account-channel-peer"` when named Feishu accounts should keep separate sessions for the same sender; dynamic bindings preserve the account scope.

### Typical Multi-User Deployment and Verification

A typical public multi-user deployment combines `dmPolicy: "open"`, `allowFrom: ["*"]`, `groupPolicy: "open"`, `requireMention: true`, the `dynamicAgentCreation` block, a chosen `session.dmScope`, and an empty `bindings: []` (dynamic agents auto-bind). To verify dynamic creation is working, check the gateway logs for lines such as `feishu: creating dynamic agent "feishu-ou_xxxxxx" for user ou_xxxxxx`, `workspace: /Users/you/.openclaw/workspace-feishu-ou_xxxxxx`, and `feishu: dynamic agent created, new route: agent:feishu-ou_xxxxxx:main`. List all created workspaces with `ls -la ~/.openclaw/workspace-*`.

Five notes apply to dynamic agents: **Workspace isolation** — each user gets their own workspace directory and agent instance; users cannot see each other's conversation history or files within the normal messaging flow. **Security boundary** — this is a messaging-context isolation mechanism, NOT a hostile co-tenant security boundary; the agent process and host environment are shared. **`bindings` should be empty** — dynamic agents auto-register their own bindings. **Upgrade path** — existing manual bindings continue to work alongside dynamic agents. **`session.dmScope` is global** — it affects all channels, not just Feishu.

## Configuration Reference

Full configuration lives at Gateway configuration (`/gateway/configuration`). The complete `channels.feishu.*` settings table:

| Setting                                                  | Description                                                                      | Default                              |
| -------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------ |
| `channels.feishu.enabled`                                | Enable/disable the channel                                                       | `true`                               |
| `channels.feishu.domain`                                 | API domain (`feishu` or `lark`)                                                  | `feishu`                             |
| `channels.feishu.connectionMode`                         | Event transport (`websocket` or `webhook`)                                       | `websocket`                          |
| `channels.feishu.defaultAccount`                         | Default account for outbound routing                                             | `default`                            |
| `channels.feishu.verificationToken`                      | Required for webhook mode                                                        | -                                    |
| `channels.feishu.encryptKey`                             | Required for webhook mode                                                        | -                                    |
| `channels.feishu.webhookPath`                            | Webhook route path                                                               | `/feishu/events`                     |
| `channels.feishu.webhookHost`                            | Webhook bind host                                                                | `127.0.0.1`                          |
| `channels.feishu.webhookPort`                            | Webhook bind port                                                                | `3000`                               |
| `channels.feishu.accounts.<id>.appId`                    | App ID                                                                           | -                                    |
| `channels.feishu.accounts.<id>.appSecret`                | App Secret                                                                       | -                                    |
| `channels.feishu.accounts.<id>.domain`                   | Per-account domain override                                                      | `feishu`                             |
| `channels.feishu.accounts.<id>.tts`                      | Per-account TTS override                                                         | `messages.tts`                       |
| `channels.feishu.dmPolicy`                               | DM policy                                                                        | `pairing`                            |
| `channels.feishu.allowFrom`                              | DM allowlist (open_id list)                                                      | -                                    |
| `channels.feishu.groupPolicy`                            | Group policy                                                                     | `allowlist`                          |
| `channels.feishu.groupAllowFrom`                         | Group allowlist                                                                  | -                                    |
| `channels.feishu.requireMention`                         | Require @mention in groups                                                       | `true`                               |
| `channels.feishu.groups.<chat_id>.requireMention`        | Per-group @mention override; explicit IDs also admit the group in allowlist mode | inherited                            |
| `channels.feishu.groups.<chat_id>.enabled`               | Enable/disable a specific group                                                  | `true`                               |
| `channels.feishu.dynamicAgentCreation.enabled`           | Enable automatic per-user agent creation                                         | `false`                              |
| `channels.feishu.dynamicAgentCreation.workspaceTemplate` | Path template for dynamic agent workspaces                                       | `~/.openclaw/workspace-{agentId}`    |
| `channels.feishu.dynamicAgentCreation.agentDirTemplate`  | Agent directory name template                                                    | `~/.openclaw/agents/{agentId}/agent` |
| `channels.feishu.dynamicAgentCreation.maxAgents`         | Maximum number of dynamic agents to create                                       | unlimited                            |
| `channels.feishu.textChunkLimit`                         | Message chunk size                                                               | `2000`                               |
| `channels.feishu.mediaMaxMb`                             | Media size limit                                                                 | `30`                                 |
| `channels.feishu.streaming`                              | Streaming card output                                                            | `true`                               |
| `channels.feishu.blockStreaming`                         | Completed-block reply streaming                                                  | `false`                              |
| `channels.feishu.typingIndicator`                        | Send typing reactions                                                            | `true`                               |
| `channels.feishu.resolveSenderNames`                     | Resolve sender display names                                                     | `true`                               |
| `channels.feishu.tools.bitable`                          | Enable Bitable/Base tools                                                        | `true`                               |
| `channels.feishu.tools.base`                             | Alias for `channels.feishu.tools.bitable`; explicit `bitable` wins when both set | `true`                               |
| `channels.feishu.accounts.<id>.tools.bitable`            | Per-account Bitable/Base tool gate                                               | inherited                            |
| `channels.feishu.accounts.<id>.tools.base`               | Per-account alias for `tools.bitable`                                            | inherited                            |

**Source**: OpenClaw documentation — `channels/feishu` (mirror `inbox/openclaw_docs/channels/feishu.md`)
**Last Updated**: 2026-06-22
**Status**: Active
