---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - whatsapp
keywords:
  - whatsapp operations openclaw
  - whatsapp acp bindings
  - whatsapp approval reactions
  - whatsapp multi-account credentials
  - whatsapp reconnect loop troubleshooting
  - whatsapp system prompts groups direct
  - whatsapp configwrites action gates
  - openclaw doctor ensure-whatsapp
topics:
  - OpenClaw
  - WhatsApp Channel Operations
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/whatsapp
access_control_group: ["general"]
---

# OpenClaw — Operating the WhatsApp Channel (Approvals, ACP Bindings, Multi-Account, Troubleshooting)

## Overview

This note is the operations procedure for OpenClaw's WhatsApp (Baileys / WhatsApp Web) channel: how to wire exec/plugin approval reactions, route specific peers to ACP agents with persistent `bindings[]`, manage multi-account credential paths and logout, gate channel actions and config writes, work through the reconnect/proxy/group-message troubleshooting playbook, resolve per-scope system prompts, and find the config-reference field map. It mirrors the back half of the `channels/whatsapp` source page (Approval prompts → Configuration reference pointers). The onboarding/access procedure lives in `oc_channels_whatsapp_setup` and the socket/delivery behavior model in `oc_channels_whatsapp_runtime_delivery`; this note assumes the channel is already linked and gated.

## Approval prompts

WhatsApp can render exec and plugin approval prompts with `👍` / `👎` reactions. Delivery is controlled by the top-level approval forwarding config, and `approvals.exec` and `approvals.plugin` are independent families:

```json5
{
  approvals: {
    exec: {
      enabled: true,
      mode: "session",
    },
    plugin: {
      enabled: true,
      mode: "targets",
      targets: [{ channel: "whatsapp", to: "+15551234567" }],
    },
  },
}
```

Enabling WhatsApp as a channel only links the transport; it does not send approval prompts unless the matching approval family is enabled and routes to WhatsApp. Session mode (`mode: "session"`) delivers native emoji approvals only for approvals that originate from WhatsApp. Target mode (`mode: "targets"`) uses the shared forwarding pipeline for explicit WhatsApp targets and does not create separate approver-DM fanout. WhatsApp approval reactions require explicit WhatsApp approvers from `allowFrom` or `"*"`; `defaultTo` controls ordinary default message targets and is **not** an approval approver. Manual `/approve` commands still pass through the normal WhatsApp sender authorization path before approval resolution.

## Configured ACP bindings

WhatsApp supports persistent ACP bindings via top-level `bindings[]` entries. Each binding pins a `channel`/`accountId`/`peer` match to an `agentId` (here `codex`):

```json5
{
  bindings: [
    {
      type: "acp",
      agentId: "codex",
      match: {
        channel: "whatsapp",
        accountId: "work",
        peer: { kind: "direct", id: "+15555550123" },
      },
    },
    {
      type: "acp",
      agentId: "codex",
      match: {
        channel: "whatsapp",
        accountId: "work",
        peer: { kind: "group", id: "120363424282127706@g.us" },
      },
    },
  ],
}
```

Direct chats match E.164 numbers such as `+15555550123`, and groups match WhatsApp group JIDs such as `120363424282127706@g.us`. Group allowlists, sender policy, and mention or activation gating all run **before** OpenClaw ensures the configured ACP session exists. A matched configured ACP binding owns the route, and WhatsApp broadcast groups do not fan out that turn to ordinary WhatsApp sessions.

## Multi-account and credentials

Account ids come from `channels.whatsapp.accounts`. The default account is `default` if present, otherwise the first configured account id (sorted); account ids are normalized internally for lookup. Credential paths and logout behave as follows:

- Current auth path: `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`, with a backup file `creds.json.bak`.
- Legacy default auth in `~/.openclaw/credentials/` is still recognized/migrated for default-account flows.
- `openclaw channels logout --channel whatsapp [--account <id>]` clears WhatsApp auth state for that account.
- When a Gateway is reachable, logout first stops the live WhatsApp listener for the selected account so the linked session does not keep receiving messages until the next restart; `openclaw channels remove --channel whatsapp` also stops the live listener before disabling or deleting account config.
- In legacy auth directories, `oauth.json` is preserved while Baileys auth files are removed.

## Tools, actions, and config writes

Agent tool support includes a WhatsApp reaction action (`react`). Channel actions are gated by two flags, and channel-initiated config writes are on by default:

- `channels.whatsapp.actions.reactions` — gate for reaction actions.
- `channels.whatsapp.actions.polls` — gate for poll actions.
- `channels.whatsapp.configWrites` — channel-initiated config writes are enabled by default; disable with `channels.whatsapp.configWrites=false`.

## Troubleshooting

The page documents a per-symptom playbook. Work the checks in order for each symptom.

**Not linked (QR required).** Channel status reports not linked — relink and re-check status:

```bash
openclaw channels login --channel whatsapp
openclaw channels status
```

**Linked but disconnected / reconnect loop.** A linked account shows repeated disconnects or reconnect attempts. Quiet accounts can stay connected past the normal message timeout; the watchdog restarts when WhatsApp Web transport activity stops, the socket closes, or application-level activity stays silent beyond the longer safety window. If logs show repeated `status=408 Request Time-out Connection was lost`, tune Baileys socket timings under `web.whatsapp` — start by shortening `keepAliveIntervalMs` below your network's idle timeout and increasing `connectTimeoutMs` on slow or lossy links:

```json5
{
  web: {
    whatsapp: {
      keepAliveIntervalMs: 15000,
      connectTimeoutMs: 60000,
      defaultQueryTimeoutMs: 60000,
    },
  },
}
```

Then probe and inspect: `openclaw channels status --probe`, `openclaw doctor`, `openclaw logs --follow`, `openclaw gateway status`. If the loop persists after host connectivity and timing are fixed, back up the account auth directory (`cp -a ~/.openclaw/credentials/whatsapp/<accountId> ~/.openclaw/credentials/whatsapp/<accountId>.bak`) and re-link with `openclaw channels logout`/`login --account <accountId>`. If `~/.openclaw/logs/whatsapp-health.log` says `Gateway inactive` but `openclaw gateway status` and `openclaw channels status --probe` show the gateway and WhatsApp healthy, run `openclaw doctor`. On Linux, doctor warns about legacy crontab entries that still invoke `~/.openclaw/bin/ensure-whatsapp.sh`; remove those stale entries with `crontab -e` because cron can lack the systemd user-bus environment and make that old script misreport gateway health.

**QR login times out behind a proxy.** `openclaw channels login --channel whatsapp` fails before showing a usable QR code with `status=408 Request Time-out` or a TLS socket disconnect. WhatsApp Web login uses the gateway host's standard proxy environment (`HTTPS_PROXY`, `HTTP_PROXY`, lowercase variants, and `NO_PROXY`); verify the gateway process inherits the proxy env and that `NO_PROXY` does not match `mmg.whatsapp.net`.

**No active listener when sending.** Outbound sends fail fast when no active gateway listener exists for the target account — make sure the gateway is running and the account is linked.

**Reply appears in transcript but not in WhatsApp.** Transcript rows record what the agent generated; WhatsApp delivery is checked separately, and OpenClaw only treats an auto-reply as sent after Baileys returns an outbound message id for at least one visible text or media send. Ack reactions are independent pre-reply receipts, so a successful reaction does not prove the later text or media reply was accepted. Check gateway logs for `auto-reply delivery failed` or `auto-reply was not accepted by WhatsApp provider`.

**Group messages unexpectedly ignored.** Check in this order: `groupPolicy`; `groupAllowFrom` / `allowFrom`; `groups` allowlist entries; mention gating (`requireMention` + mention patterns); and duplicate keys in `openclaw.json` (JSON5 takes later entries over earlier ones, so keep a single `groupPolicy` per scope). If `channels.whatsapp.groups` is present, WhatsApp can still observe messages from other groups, but OpenClaw drops them before session routing — add the group JID to `channels.whatsapp.groups`, or add `groups["*"]` to admit all groups while keeping sender authorization under `groupPolicy` and `groupAllowFrom`.

**Bun runtime warning.** The WhatsApp gateway runtime should use Node; Bun is flagged as incompatible for stable WhatsApp/Telegram gateway operation.

## System prompts

WhatsApp supports Telegram-style system prompts for groups and direct chats via the `groups` and `direct` maps. The **effective `groups` map is resolved first**: if the account defines its own `groups`, it fully replaces the root `groups` map (no deep merge), and prompt lookup then runs on the resulting single map. For group messages, a group-specific prompt (`groups["<groupId>"].systemPrompt`) is used when the specific group entry exists **and** its `systemPrompt` key is defined; an empty string (`""`) suppresses the wildcard so no prompt is applied; otherwise the group wildcard (`groups["*"].systemPrompt`) applies when the specific entry is absent or defines no `systemPrompt` key. Direct messages resolve identically with the `direct` map (`direct["<peerId>"].systemPrompt` → `direct["*"].systemPrompt`, empty string suppresses the wildcard). The `dms` bucket remains the lightweight per-DM history override (`dms.<id>.historyLimit`); prompt overrides live under `direct`.

Multi-account differs from Telegram: Telegram intentionally suppresses root `groups` for all accounts in a multi-account setup (even accounts with no `groups` of their own) to stop a bot from receiving group messages for groups it does not belong to. WhatsApp does **not** apply this guard — root `groups` and root `direct` are always inherited by accounts that define no account-level override, regardless of account count. For per-account group or direct prompts in a multi-account WhatsApp setup, define the full map under each account explicitly rather than relying on root-level defaults.

Two admission side effects matter: `channels.whatsapp.groups` is both a per-group config map **and** the chat-level group allowlist, so at either root or account scope `groups["*"]` means "all groups are admitted" for that scope — only add a wildcard group `systemPrompt` when you already want that scope to admit all groups (otherwise repeat the prompt on each explicitly allowlisted group entry). Group admission and sender authorization stay separate: `groups["*"]` widens which groups reach group handling but does not authorize every sender — sender access is still controlled by `channels.whatsapp.groupPolicy` and `channels.whatsapp.groupAllowFrom`. By contrast, `channels.whatsapp.direct` has no such side effect: `direct["*"]` only provides a default direct-chat config after a DM is already admitted by `dmPolicy` plus `allowFrom` or pairing-store rules.

```json5
{
  channels: {
    whatsapp: {
      groups: {
        // Use only if all groups should be admitted at the root scope.
        // Applies to all accounts that do not define their own groups map.
        "*": { systemPrompt: "Default prompt for all groups." },
      },
      direct: {
        // Applies to all accounts that do not define their own direct map.
        "*": { systemPrompt: "Default prompt for all direct chats." },
      },
      accounts: {
        work: {
          groups: {
            // This account defines its own groups, so root groups are fully
            // replaced. To keep a wildcard, define "*" explicitly here too.
            "120363406415684625@g.us": {
              requireMention: false,
              systemPrompt: "Focus on project management.",
            },
            // Use only if all groups should be admitted in this account.
            "*": { systemPrompt: "Default prompt for work groups." },
          },
          direct: {
            // This account defines its own direct map, so root direct entries are
            // fully replaced. To keep a wildcard, define "*" explicitly here too.
            "+15551234567": { systemPrompt: "Prompt for a specific work direct chat." },
            "*": { systemPrompt: "Default prompt for work direct chats." },
          },
        },
      },
    },
  },
}
```

## Configuration reference pointers

The primary reference is [Configuration reference - WhatsApp](https://docs.openclaw.ai/gateway/config-channels#whatsapp). High-signal WhatsApp fields, grouped by concern:

- access: `dmPolicy`, `allowFrom`, `groupPolicy`, `groupAllowFrom`, `groups`
- delivery: `textChunkLimit`, `chunkMode`, `mediaMaxMb`, `sendReadReceipts`, `ackReaction`, `reactionLevel`
- multi-account: `accounts.<id>.enabled`, `accounts.<id>.authDir`, account-level overrides
- operations: `configWrites`, `debounceMs`, `web.enabled`, `web.heartbeatSeconds`, `web.reconnect.*`, `web.whatsapp.*`
- session behavior: `session.dmScope`, `historyLimit`, `dmHistoryLimit`, `dms.<id>.historyLimit`
- prompts: `groups.<id>.systemPrompt`, `groups["*"].systemPrompt`, `direct.<id>.systemPrompt`, `direct["*"].systemPrompt`

**Source**: OpenClaw documentation — `channels/whatsapp` (mirror `inbox/openclaw_docs/channels/whatsapp.md`)
**Last Updated**: 2026-06-22
**Status**: Active
