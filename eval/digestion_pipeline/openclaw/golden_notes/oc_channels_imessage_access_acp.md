---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - imessage
keywords:
  - openclaw imessage access control
  - imessage dmpolicy allowfrom
  - imessage grouppolicy groupallowfrom
  - imessage two-gate group routing
  - imessage groups registry chat_id
  - imessage acp conversation bindings
  - acp spawn bind here imessage
  - imessage deployment patterns dedicated bot mac
  - imessage session dmscope main group isolation
  - imessage multi-account accounts
topics:
  - OpenClaw
  - iMessage Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/imessage
access_control_group: ["general"]
---

# OpenClaw — iMessage Access Control, ACP Bindings, and Deployment Patterns

## Overview

This procedure covers how to gate and route iMessage traffic into an OpenClaw agent and how to deploy the `imsg` iMessage channel. It mirrors three H2 sections of the `channels/imessage` source page — **Access control and routing** (DM policy, group policy + mention gating, sessions and deterministic replies), **ACP conversation bindings** (binding a chat to a persistent ACP agent session), and **Deployment patterns** (dedicated bot Mac, remote Mac over Tailscale, multi-account, DM history). Host setup, private-API enablement, and delivery/recovery operations live in the sibling notes `oc_channels_imessage_setup` and `oc_channels_imessage_delivery_ops`.

## Access control and routing

iMessage admission is gated separately for direct messages and for groups, and the two paths run different code so a misconfigured group gate never blocks DMs.

### DM policy

`channels.imessage.dmPolicy` controls direct messages, with these values:

- `pairing` (default)
- `allowlist`
- `open` (requires `allowFrom` to include `"*"`)
- `disabled`

The DM allowlist field is `channels.imessage.allowFrom`. Allowlist entries must identify senders: handles or static sender access groups (`accessGroup:<name>`). Chat targets are NOT placed in `allowFrom` — use `channels.imessage.groupAllowFrom` for chat targets such as `chat_id:*`, `chat_guid:*`, or `chat_identifier:*`, and use `channels.imessage.groups` for numeric `chat_id` registry keys.

### Group policy and the two-gate model

`channels.imessage.groupPolicy` controls group handling, with these values:

- `allowlist` (default when configured)
- `open`
- `disabled`

The group sender allowlist is `channels.imessage.groupAllowFrom`, whose entries can also reference static sender access groups (`accessGroup:<name>`). Runtime fallback: if `groupAllowFrom` is unset, iMessage group sender checks use `allowFrom`; set `groupAllowFrom` when DM and group admission should differ. If `channels.imessage` is completely missing, runtime falls back to `groupPolicy="allowlist"` and logs a warning (even if `channels.defaults.groupPolicy` is set).

Group routing has **two allowlist gates running back-to-back, and both must pass**: (1) the sender / chat-target allowlist (`channels.imessage.groupAllowFrom`) — handle, `chat_guid`, `chat_identifier`, or `chat_id`; and (2) the group registry (`channels.imessage.groups`) — with `groupPolicy: "allowlist"`, this gate requires either a `groups: { "*": { ... } }` wildcard entry (sets `allowAll = true`) or an explicit per-`chat_id` entry under `groups`. If gate 2 has nothing in it, every group message is dropped while DMs continue to work (different code path). The plugin emits two `warn`-level signals at the default log level: a one-time-per-account startup signal `imessage: groupPolicy="allowlist" but channels.imessage.groups is empty for account "<id>"`, and a one-time-per-`chat_id` runtime signal `imessage: dropping group message from chat_id=<id> ...`. Seeing those `warn` lines means gate 2 is dropping — add the `groups` block. Minimum config to keep groups flowing under `groupPolicy: "allowlist"`:

```json5
{
  channels: {
    imessage: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15555550123"],
      groups: { "*": { "requireMention": true } },
    },
  },
}
```

### Mention gating for groups

iMessage has no native mention metadata, so mention detection uses regex patterns (`agents.list[].groupChat.mentionPatterns`, fallback `messages.groupChat.mentionPatterns`). With no configured patterns, mention gating cannot be enforced. Control commands from authorized senders can bypass mention gating in groups.

### Per-group `systemPrompt`

Each entry under `channels.imessage.groups.*` accepts an optional `systemPrompt` string, injected into the agent's system prompt on every turn that handles a message in that group. Resolution mirrors the per-group prompt resolution used by `channels.whatsapp.groups`: (1) the **group-specific system prompt** (`groups["<chat_id>"].systemPrompt`) is used when the specific group entry exists in the map **and** its `systemPrompt` key is defined — and if `systemPrompt` is an empty string (`""`) the wildcard is suppressed and no system prompt is applied to that group; (2) the **group wildcard system prompt** (`groups["*"].systemPrompt`) is used when the specific group entry is absent from the map entirely, or when it exists but defines no `systemPrompt` key. Per-group prompts only apply to group messages — direct messages in this channel are unaffected.

```json5
{
  channels: {
    imessage: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15555550123"],
      groups: {
        "*": { systemPrompt: "Use British spelling." },
        "8421": {
          requireMention: true,
          systemPrompt: "This is the on-call rotation chat. Keep replies under 3 sentences.",
        },
        "9907": {
          // explicit suppression: the wildcard "Use British spelling." does not apply here
          systemPrompt: "",
        },
      },
    },
  },
}
```

### Sessions and deterministic replies

DMs use direct routing; groups use group routing. With the default `session.dmScope=main`, iMessage DMs collapse into the agent main session, while group sessions are isolated under the key `agent:<agentId>:imessage:group:<chat_id>`. Replies route back to iMessage using the originating channel/target metadata. For group-ish thread behavior, some multi-participant iMessage threads can arrive with `is_group=false`; if that `chat_id` is explicitly configured under `channels.imessage.groups`, OpenClaw treats it as group traffic (group gating + group session isolation).

## ACP conversation bindings

Legacy iMessage chats can also be bound to ACP sessions. The fast operator flow is:

- Run `/acp spawn codex --bind here` inside the DM or allowed group chat.
- Future messages in that same iMessage conversation route to the spawned ACP session.
- `/new` and `/reset` reset the same bound ACP session in place.
- `/acp close` closes the ACP session and removes the binding.

Configured persistent bindings are supported through top-level `bindings[]` entries with `type: "acp"` and `match.channel: "imessage"`. The `match.peer.id` can use a normalized DM handle such as `+15555550123` or `user@example.com`, `chat_id:<id>` (recommended for stable group bindings), `chat_guid:<guid>`, or `chat_identifier:<identifier>`. Example:

```json5
{
  agents: {
    list: [
      {
        id: "codex",
        runtime: {
          type: "acp",
          acp: { agent: "codex", backend: "acpx", mode: "persistent" },
        },
      },
    ],
  },
  bindings: [
    {
      type: "acp",
      agentId: "codex",
      match: {
        channel: "imessage",
        accountId: "default",
        peer: { kind: "group", id: "chat_id:123" },
      },
      acp: { label: "codex-group" },
    },
  ],
}
```

See [ACP Agents](https://docs.openclaw.ai/tools/acp-agents) for shared ACP binding behavior.

## Deployment patterns

OpenClaw supports several iMessage topologies. The **dedicated bot macOS user** pattern uses a dedicated Apple ID and macOS user so bot traffic is isolated from your personal Messages profile; the typical flow is: (1) create/sign in a dedicated macOS user; (2) sign into Messages with the bot Apple ID in that user; (3) install `imsg` in that user; (4) create an SSH wrapper so OpenClaw can run `imsg` in that user context; (5) point `channels.imessage.accounts.<id>.cliPath` and `.dbPath` to that user profile. The first run may require GUI approvals (Automation + Full Disk Access) in that bot user session.

The **remote Mac over Tailscale** topology runs the gateway on Linux/VM, runs iMessage + `imsg` on a Mac in your tailnet, uses a `cliPath` wrapper that SSHes to run `imsg`, and sets `remoteHost` to enable SCP attachment fetches. Use SSH keys so both SSH and SCP are non-interactive, and ensure the host key is trusted first (for example `ssh bot@mac-mini.tailnet-1234.ts.net`) so `known_hosts` is populated. Example config plus wrapper:

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "~/.openclaw/scripts/imsg-ssh",
      remoteHost: "bot@mac-mini.tailnet-1234.ts.net",
      includeAttachments: true,
      dbPath: "/Users/bot/Library/Messages/chat.db",
    },
  },
}
```

The **multi-account pattern** uses per-account config under `channels.imessage.accounts`, where each account can override fields such as `cliPath`, `dbPath`, `allowFrom`, `groupPolicy`, `mediaMaxMb`, history settings, and attachment root allowlists. For **direct-message history**, set `channels.imessage.dmHistoryLimit` to seed new direct-message sessions with recent decoded `imsg` history for that conversation, and use `channels.imessage.dms["<sender>"].historyLimit` for per-sender overrides (including `0` to disable history for a sender). iMessage DM history is fetched on demand from `imsg`; leaving `dmHistoryLimit` unset disables global DM history seeding, but a positive per-sender `channels.imessage.dms["<sender>"].historyLimit` still enables seeding for that sender.

**Source**: OpenClaw documentation — `channels/imessage` (mirror `inbox/openclaw_docs/channels/imessage.md`), sections "Access control and routing", "ACP conversation bindings", "Deployment patterns"
**Last Updated**: 2026-06-22
**Status**: Active
