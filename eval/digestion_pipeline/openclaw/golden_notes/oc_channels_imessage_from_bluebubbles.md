---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - imessage
keywords:
  - bluebubbles to imessage migration
  - channels.bluebubbles channels.imessage config translation
  - imsg rpc json-rpc stdio
  - group registry footgun groupPolicy allowlist
  - openclaw channels status probe
  - inbound recovery since_rowid dedupe
  - acp bindings match.channel imessage
  - no rollback bluebubbles
topics:
  - OpenClaw
  - iMessage Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/imessage-from-bluebubbles
access_control_group: ["general"]
---

# OpenClaw — Migrating from BlueBubbles to the Bundled iMessage Plugin

## Overview

This note is the step-by-step procedure for migrating an existing OpenClaw `channels.bluebubbles` configuration to the bundled `channels.imessage` plugin, mirroring the `channels/imessage-from-bluebubbles` source page. BlueBubbles support was removed and OpenClaw now reaches iMessage only through [`steipete/imsg`](https://github.com/steipete/imsg) over JSON-RPC, so this is the single supported migration path. It covers the migration checklist, what `imsg` does, pre-flight verification, the config-key translation table, the load-bearing "group registry footgun", the disabled-block-then-cut-over step-by-step, action parity, how pairing/sessions/ACP bindings carry over, and the no-rollback warning.

## Migration checklist

Shortest safe path when you already know your old BlueBubbles config (each step is detailed in the sections below):

1. Verify `imsg` directly on the Messages Mac (`imsg chats`, `imsg history`, `imsg send`, `imsg rpc --help`).
2. Copy behavior keys `channels.bluebubbles`→`channels.imessage`: `dmPolicy`, `allowFrom`, `groupPolicy`, `groupAllowFrom`, `groups`, `includeAttachments`, `attachmentRoots`, `mediaMaxMb`, `textChunkLimit`, `coalesceSameSenderDms`, `actions`.
3. Drop the removed transport keys: `serverUrl`, `password`, webhook URLs, BlueBubbles server setup. If the Gateway is off-Mac, set `cliPath` to an SSH wrapper + `remoteHost` for attachments.
4. With the Gateway stopped, enable `channels.imessage`, run `openclaw channels status --probe --channel imessage`, then test one DM, one allowed group, attachments, and each private API action before deleting the BlueBubbles server and config.

## When this migration makes sense

- You already run `imsg` on the same Mac (or one reachable over SSH) where Messages.app is signed in.
- You want one fewer moving part — no BlueBubbles server, REST endpoint, or webhook plumbing; a single CLI binary instead of server + client app + helper.
- You are on a supported macOS / `imsg` build where the private API probe reports `available: true`.

## What imsg does

`imsg` is a local macOS CLI for Messages. OpenClaw starts `imsg rpc` as a child process and talks JSON-RPC over stdin/stdout — no HTTP server, webhook URL, background daemon, launch agent, or port to expose.

- Reads come from `~/Library/Messages/chat.db` via a read-only SQLite handle.
- Live inbound comes from `imsg watch` / `watch.subscribe`, following `chat.db` filesystem events with a polling fallback.
- Sends use Messages.app automation for normal text and file sends.
- Advanced actions use `imsg launch` to inject the `imsg` helper into Messages.app, unlocking read receipts, typing indicators, rich sends, edit, unsend, threaded reply, tapbacks, and group management.
- Linux builds can inspect a copied `chat.db` but cannot send, watch the live Mac database, or drive Messages.app — run `imsg` on the signed-in Mac or via an SSH wrapper to it.

## Before you start

1. Install `imsg` on the Mac that runs Messages.app and sanity-check it. If `imsg chats` fails with `unable to open database file`, empty output, or `authorization denied`, grant Full Disk Access to the parent process that launches `imsg` (terminal/editor/Node/Gateway/SSH), then reopen it.

   ```bash
   brew install steipete/tap/imsg
   imsg --version
   imsg chats --limit 3
   ```

2. Verify read, watch, send, and RPC surfaces before changing config. Replace `42` with a real chat id; sending needs Automation permission for Messages.app. If OpenClaw runs through SSH, run these through the same SSH wrapper/user context. If reads/probes work but sends fail with AppleEvents `-1743`, check whether Automation landed on `/usr/libexec/sshd-keygen-wrapper`.

   ```bash
   imsg chats --limit 10 --json | jq -s
   imsg history --chat-id 42 --limit 10 --attachments --json | jq -s
   imsg watch --chat-id 42 --reactions --json
   imsg send --chat-id 42 --text "OpenClaw imsg test"
   imsg rpc --help
   ```

3. Enable the private API bridge for advanced actions. `imsg launch` requires SIP disabled; basic send/history/watch work without it, advanced actions do not.

   ```bash
   imsg launch
   imsg status --json
   ```

4. After adding an enabled `channels.imessage` config, verify through OpenClaw with `openclaw channels status --probe`. You want `imessage.privateApi.available: true`; if `false`, fix that first. The probe only checks configured, enabled accounts.
5. Snapshot your config: `cp ~/.openclaw/openclaw.json5 ~/.openclaw/openclaw.json5.bak`.

## Config translation

iMessage and BlueBubbles share most channel-level config; the keys that change are mostly transport (REST server vs local CLI), while behavior keys (`dmPolicy`, `groupPolicy`, `allowFrom`, etc.) keep the same meaning.

| BlueBubbles | bundled iMessage | Notes |
| --- | --- | --- |
| `channels.bluebubbles.enabled` | `channels.imessage.enabled` | Same semantics. |
| `channels.bluebubbles.serverUrl` | _(removed)_ | No REST server — the plugin spawns `imsg rpc` over stdio. |
| `channels.bluebubbles.password` | _(removed)_ | No webhook authentication needed. |
| _(implicit)_ | `channels.imessage.cliPath` | Path to `imsg` (default `imsg`); use a wrapper script for SSH. |
| _(implicit)_ | `channels.imessage.dbPath` | Optional Messages.app `chat.db` override; auto-detected when omitted. |
| _(implicit)_ | `channels.imessage.remoteHost` | `host` or `user@host` — only needed when `cliPath` is an SSH wrapper and you want SCP attachment fetches. |
| `channels.bluebubbles.dmPolicy` | `channels.imessage.dmPolicy` | Same values (`pairing` / `allowlist` / `open` / `disabled`). |
| `channels.bluebubbles.allowFrom` | `channels.imessage.allowFrom` | Pairing approvals carry over by handle, not by token. |
| `channels.bluebubbles.groupPolicy` | `channels.imessage.groupPolicy` | Same values (`allowlist` / `open` / `disabled`). |
| `channels.bluebubbles.groupAllowFrom` | `channels.imessage.groupAllowFrom` | Same. |
| `channels.bluebubbles.groups` | `channels.imessage.groups` | **Copy verbatim, including any `groups: { "*": { ... } }` wildcard.** Per-group `requireMention`, `tools`, `toolsBySender` carry over. With `groupPolicy: "allowlist"`, an empty/missing `groups` block silently drops every group message — see "Group registry footgun". |
| `channels.bluebubbles.sendReadReceipts` | `channels.imessage.sendReadReceipts` | Default `true`. With the bundled plugin this only fires when the private API probe is up. |
| `channels.bluebubbles.includeAttachments` | `channels.imessage.includeAttachments` | Same shape, **same off-by-default**. Re-set explicitly on the iMessage block — it does not carry over implicitly; inbound photos/media are silently dropped (no `Inbound message` log line) until you do. |
| `channels.bluebubbles.attachmentRoots` | `channels.imessage.attachmentRoots` | Local roots; same wildcard rules. |
| _(N/A)_ | `channels.imessage.remoteAttachmentRoots` | Only used when `remoteHost` is set for SCP fetches. |
| `channels.bluebubbles.mediaMaxMb` | `channels.imessage.mediaMaxMb` | Default 16 MB on iMessage (BlueBubbles default was 8 MB). Set explicitly to keep the lower cap. |
| `channels.bluebubbles.textChunkLimit` | `channels.imessage.textChunkLimit` | Default 4000 on both. |
| `channels.bluebubbles.coalesceSameSenderDms` | `channels.imessage.coalesceSameSenderDms` | Same opt-in. DM-only — groups keep instant per-message dispatch. Widens default inbound debounce to 2500 ms when enabled without an explicit `messages.inbound.byChannel.imessage`. |
| `channels.bluebubbles.enrichGroupParticipantsFromContacts` | _(N/A)_ | iMessage already reads sender display names from `chat.db`. |
| `channels.bluebubbles.actions.*` | `channels.imessage.actions.*` | Per-action toggles: `reactions`, `edit`, `unsend`, `reply`, `sendWithEffect`, `renameGroup`, `setGroupIcon`, `addParticipant`, `removeParticipant`, `leaveGroup`, `sendAttachment`. |

Multi-account configs (`channels.bluebubbles.accounts.*`) translate one-to-one to `channels.imessage.accounts.*`.

## Group registry footgun

The bundled iMessage plugin runs **two** separate group allowlist gates back-to-back; both must pass for a group message to reach the agent:

1. **Sender / chat-target allowlist** (`channels.imessage.groupAllowFrom`) — checked by `isAllowedIMessageSender`, matching by sender handle, `chat_guid`, `chat_identifier`, or `chat_id`. Same shape as BlueBubbles.
2. **Group registry** (`channels.imessage.groups`) — checked by `resolveChannelGroupPolicy` (`inbound-processing.ts:199`). With `groupPolicy: "allowlist"` it requires a `groups: { "*": { ... } }` wildcard (sets `allowAll = true`) or an explicit per-`chat_id` entry.

If gate 1 passes but gate 2 fails, the message is dropped. Two `warn`-level signals make this non-silent at default log level: a one-time startup `warn` per account when `groupPolicy: "allowlist"` is set but `channels.imessage.groups` is empty (no `"*"`, no per-`chat_id` entries); and a one-time per-`chat_id` `warn` the first time a group is dropped, naming the chat_id and the exact key to add. DMs keep working via a different code path. This is the most common migration failure: operators copy `groupAllowFrom`/`groupPolicy` but skip `groups`, because BlueBubbles' `groups: { "*": { "requireMention": true } }` looks like an unrelated mention setting — it is load-bearing for the registry gate. Minimum config to keep group messages flowing after `groupPolicy: "allowlist"`:

```json5
{
  channels: {
    imessage: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15555550123", "chat_guid:any;-;..."],
      groups: {
        "*": { requireMention: true },
      },
    },
  },
}
```

`requireMention: true` under `*` is harmless with no mention patterns configured: the runtime sets `canDetectMention = false` and short-circuits the mention drop at `inbound-processing.ts:512`; with `agents.list[].groupChat.mentionPatterns` it works as expected.

## Step-by-step

1. Add an iMessage block alongside the BlueBubbles block, disabled while the Gateway still routes BlueBubbles traffic:

   ```json5
   {
     channels: {
       bluebubbles: {
         enabled: true,
         // ... existing config ...
       },
       imessage: {
         enabled: false,
         cliPath: "/opt/homebrew/bin/imsg",
         dmPolicy: "pairing",
         allowFrom: ["+15555550123"], // from bluebubbles.allowFrom
         groupPolicy: "allowlist",
         groupAllowFrom: [], // from bluebubbles.groupAllowFrom
         groups: { "*": { requireMention: true } }, // from bluebubbles.groups — silently drops groups if missing
         actions: {
           reactions: true,
           edit: true,
           unsend: true,
           reply: true,
           sendWithEffect: true,
           sendAttachment: true,
         },
       },
     },
   }
   ```

2. **Probe before traffic matters** — stop the Gateway, temporarily enable the iMessage block, and confirm it reports healthy from the CLI. The probe only checks configured, enabled accounts. Do not restart the Gateway with both BlueBubbles and iMessage enabled unless you want both channel monitors running; if not cutting over immediately, set `channels.imessage.enabled` back to `false` first.

   ```bash
   openclaw gateway stop
   # edit config: channels.imessage.enabled = true
   openclaw channels status --probe --channel imessage   # expect imessage.privateApi.available: true
   ```

3. **Cut over.** Once the enabled iMessage account reports healthy, remove the BlueBubbles config, keep iMessage enabled (`channels: { imessage: { enabled: true /* ... */ } }`), and restart the gateway. Inbound iMessage traffic now flows through the bundled plugin.
4. **Verify DMs.** Send the agent a direct message; confirm the reply lands.
5. **Verify groups separately** — DMs and groups take different code paths, so DM success does not prove groups route. Send a message in a paired group chat; if it goes silent (no reply, no error), the `imessage: dropping group message from chat_id=<id>` or `imessage: groupPolicy="allowlist" but channels.imessage.groups is empty` log line means the `groups` block is missing/empty (see "Group registry footgun").
6. **Verify the action surface** — from a paired DM, ask the agent to react, edit, unsend, reply, send a photo, and (in a group) rename / add or remove a participant; each should land natively in Messages.app. If any throws "iMessage `<action>` requires the imsg private API bridge", run `imsg launch` again and refresh `channels status --probe`.
7. **Remove the BlueBubbles server and config** once iMessage DMs, groups, and actions are verified — OpenClaw will not use `channels.bluebubbles`.

## Action parity at a glance

| Action | legacy BlueBubbles | bundled iMessage |
| --- | --- | --- |
| Send text / SMS fallback | ✅ | ✅ |
| Send media (photo, video, file, voice) | ✅ | ✅ |
| Threaded reply (`reply_to_guid`) | ✅ | ✅ ([#51892](https://github.com/openclaw/openclaw/issues/51892)) |
| Tapback (`react`) | ✅ | ✅ |
| Edit / unsend (macOS 13+ recipients) | ✅ | ✅ |
| Send with screen effect | ✅ | ✅ (part of [#9394](https://github.com/openclaw/openclaw/issues/9394)) |
| Rich text bold / italic / underline / strikethrough | ✅ | ✅ (via attributedBody) |
| Rename group / set group icon | ✅ | ✅ |
| Add / remove participant, leave group | ✅ | ✅ |
| Read receipts and typing indicator | ✅ | ✅ (gated on private API probe) |
| Same-sender DM coalescing | ✅ | ✅ (DM-only; opt-in `coalesceSameSenderDms`) |
| Inbound recovery after a restart | ✅ (webhook replay + history fetch) | ✅ (replay via since_rowid + dedupe; wider window on local) |

iMessage recovers messages missed while the gateway was down: on startup it replays from the last dispatched rowid via `imsg watch.subscribe` `since_rowid` and dedupes by GUID, with a stale-backlog age fence suppressing the Push-flush "backlog bomb". This runs over the `imsg` RPC connection (so remote SSH `cliPath` works too); local setups get a wider window via direct `chat.db` reads.

## Pairing, sessions, and ACP bindings

- **Pairing approvals** carry over by handle — no need to re-approve known senders; `channels.imessage.allowFrom` recognizes the same `+15555550123` / `user@example.com` strings as BlueBubbles.
- **Sessions** stay scoped per agent + chat. DMs collapse into the agent main session under default `session.dmScope=main`; group sessions stay isolated per `chat_id`. The session keys differ (`agent:<id>:imessage:group:<chat_id>` vs the BlueBubbles equivalent), so old BlueBubbles conversation history does not carry into iMessage sessions.
- **ACP bindings** referencing `match.channel: "bluebubbles"` must be updated to `"imessage"`. The `match.peer.id` shapes (`chat_id:`, `chat_guid:`, `chat_identifier:`, bare handle) are identical.

## No rollback channel

There is no supported BlueBubbles runtime to switch back to. If iMessage verification fails, set `channels.imessage.enabled: false`, restart the Gateway, fix the `imsg` blocker, and retry. The reply cache lives in SQLite plugin state; `openclaw doctor --fix` imports and archives the old `imessage/reply-cache.jsonl` sidecar if present.

**Source**: OpenClaw documentation — `channels/imessage-from-bluebubbles` (mirror `inbox/openclaw_docs/channels/imessage-from-bluebubbles.md`)
**Last Updated**: 2026-06-22
**Status**: Active
