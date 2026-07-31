---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - imessage
keywords:
  - imessage delivery operations
  - imsg private api actions
  - tapbacks effects attachments
  - coalesce split-send dms
  - inbound recovery dedupe
  - since_rowid replay
  - imessage troubleshooting
  - textchunklimit mediamaxmb
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

# OpenClaw — iMessage Delivery and Operations (`imsg`)

## Overview

This procedure note covers the delivery and operational surface of the native OpenClaw iMessage channel driven by `imsg`, mirroring the lower half of the `channels/imessage` source page: media/chunking/delivery targets, private-API actions, channel-initiated config writes, split-send DM coalescing, automatic inbound recovery after a restart, and troubleshooting. It assumes the host setup, macOS permissions, private-API enablement, and access-control/ACP routing covered in the sibling iMessage notes. Private-API actions require `imsg launch` plus a successful probe (`openclaw channels status --probe` reporting `privateApi.available: true`).

## Media, Chunking, and Delivery Targets

**Attachments and media.** Inbound attachment ingestion is **off by default** — set `channels.imessage.includeAttachments: true` to forward photos, voice memos, video, etc.; with it disabled, attachment-only iMessages are dropped before reaching the agent and may produce no `Inbound message` log line. Remote paths are fetched via SCP when `remoteHost` is set, and must match allowed roots — `channels.imessage.attachmentRoots` (local) / `channels.imessage.remoteAttachmentRoots` (remote SCP) — default pattern `/Users/*/Library/Messages/Attachments`; SCP uses strict host-key checking (`StrictHostKeyChecking=yes`). Outbound media size uses `channels.imessage.mediaMaxMb` (default 16 MB).

**Outbound chunking.** Text chunk limit `channels.imessage.textChunkLimit` (default 4000); `channels.imessage.chunkMode` is `length` (default) or `newline` (paragraph-first splitting).

**Addressing formats.** Preferred explicit targets: `chat_id:123` (recommended for stable routing), `chat_guid:...`, `chat_identifier:...`. Handle targets also work: `imessage:+1555...`, `sms:+1555...`, `user@example.com`. List chats with:

```bash
imsg chats --limit 20
```

## Private API Actions

When `imsg launch` is running and the probe reports `privateApi.available: true`, the message tool can use iMessage-native actions beyond text sends. Toggles live under `channels.imessage.actions`:

```json5
{
  channels: {
    imessage: {
      actions: {
        reactions: true,
        edit: true,
        unsend: true,
        reply: true,
        sendWithEffect: true,
        sendAttachment: true,
        renameGroup: true,
        setGroupIcon: true,
        addParticipant: true,
        removeParticipant: true,
        leaveGroup: true,
      },
    },
  },
}
```

**Available actions.** `react` adds/removes tapbacks (`messageId`, `emoji`, `remove`; maps to love/like/dislike/laugh/emphasize/question). `reply` sends a threaded reply (`messageId`, `text`/`message`, plus `chatGuid`/`chatId`/`chatIdentifier`/`to`). `sendWithEffect` sends text with an effect (`text`/`message`, `effect`/`effectId`). `edit` edits a sent message (`messageId`, `text`/`newText`) and `unsend` retracts one (`messageId`) on supported versions. `upload-file` sends media/files (`buffer` as base64 or hydrated `media`/`path`/`filePath`, `filename`, optional `asVoice`; legacy alias `sendAttachment`). `renameGroup`, `setGroupIcon`, `addParticipant`, `removeParticipant`, `leaveGroup` manage group chats when the target is a group.

**Message IDs.** Inbound context includes both short `MessageSid` values and full message GUIDs. Short IDs are scoped to the recent SQLite-backed reply cache and checked against the current chat; if a short ID has expired or belongs to another chat, retry with the full `MessageSidFull`.

**Capability detection.** OpenClaw hides private-API actions only when the cached probe status says the bridge is unavailable; if unknown, actions stay visible and probe lazily, so the first action can succeed after `imsg launch` without a manual refresh.

**Read receipts and typing.** When the bridge is up, accepted inbound chats are marked read before dispatch and a typing bubble is shown while the agent generates. Disable read-marking with `channels.imessage.sendReadReceipts: false`. Older `imsg` builds gate off typing/read silently; OpenClaw logs a one-time warning per restart so it is attributable.

**Inbound tapbacks.** OpenClaw subscribes to tapbacks and routes accepted reactions as system events instead of message text, so a user tapback does not trigger an ordinary reply loop. `channels.imessage.reactionNotifications` controls mode: `"own"` (default) notifies only on reactions to bot-authored messages, `"all"` notifies for all inbound tapbacks from authorized senders, `"off"` ignores them (per-account override `accounts.<id>.reactionNotifications`).

**Approval reactions (👍 / 👎).** When `approvals.exec.enabled` or `approvals.plugin.enabled` is true and the request routes to iMessage, the gateway delivers an approval prompt natively and accepts a tapback: `👍` (Like) → `allow-once`, `👎` (Dislike) → `deny`; `allow-always` is a manual fallback (`/approve <id> allow-always`). The reacting handle must be an explicit approver — the list is read from `channels.imessage.allowFrom` (or per-account `accounts.<id>.allowFrom`), keyed on E.164 phone or Apple ID email; wildcard `"*"` is honored but allows any sender to approve. The reaction shortcut intentionally bypasses `reactionNotifications`, `dmPolicy`, and `groupAllowFrom` — the explicit-approver allowlist is the only gate that matters. **Behavior change:** when `allowFrom` is non-empty, `/approve <id> <decision>` is authorized against that approver list (not the broader DM allowlist), and DM-allowlisted senders not in `allowFrom` are denied; when empty, the legacy "same-chat fallback" applies. The binding is stored in memory (TTL matched to approval expiry) and in the gateway's persistent keyed store, so a tapback shortly after restart still resolves; cross-device `is_from_me=true` tapbacks (the operator's own reaction on a paired device) are ignored so the bot cannot self-approve; legacy plain-text tapbacks (`Liked "…"` from very old clients) cannot resolve approvals because they carry no message GUID.

## Config Writes

iMessage allows channel-initiated config writes by default (for `/config set|unset` when `commands.config: true`); disable with:

```json5
{
  channels: {
    imessage: {
      configWrites: false,
    },
  },
}
```

## Coalescing Split-Send DMs (command + URL in one composition)

When a user types a command and a URL together — e.g. `Dump https://example.com/article` — Apple's Messages app splits the send into **two separate `chat.db` rows** (text `"Dump"` and a URL-preview balloon with OG-preview attachments) that arrive ~0.8-2.0 s apart. Without coalescing the agent sees the command alone on turn 1, replies (often "send me the URL"), and only sees the URL on turn 2, losing the command context. This is Apple's send pipeline, not OpenClaw or `imsg`.

`channels.imessage.coalesceSameSenderDms` opts a DM into buffering consecutive same-sender rows. When `imsg` exposes the structural URL-preview marker `balloon_bundle_id: "com.apple.messages.URLBalloonProvider"` on a source row, OpenClaw merges only that real split-send and keeps other buffered rows separate. On older builds with no balloon metadata, OpenClaw cannot distinguish a split-send from separate sends, so it falls back to merging the bucket — preserving pre-metadata behavior rather than regressing `Dump <url>` into two turns. Group chats keep per-message dispatch.

**When to use.** Enable when you ship skills expecting `command + payload` in one message (dump, paste, save, queue) and can accept added DM turn latency; leave disabled when you need minimum latency for single-word DM triggers. The flag defaults to `false`; with it on and no explicit `messages.inbound.byChannel.imessage`, the debounce window widens to **2500 ms** (legacy default 0 ms), because Apple's 0.8-2.0 s split-send cadence does not fit a tighter default:

```json5
{
  channels: { imessage: { coalesceSameSenderDms: true } },
  messages: {
    inbound: {
      byChannel: {
        // 2500 ms works for most setups; raise to 4000 ms if your Mac is
        // slow or under memory pressure (observed gap can stretch past 2 s then).
        imessage: 2500,
      },
    },
  },
}
```

**Trade-offs.** Every DM (including standalone control commands and single-text follow-ups) waits up to the debounce window in case a URL-preview row is coming; group messages keep instant dispatch. Merged output is bounded — text caps at 4000 chars with an explicit `…[truncated]` marker, attachments cap at 20, source entries cap at 10 (first-plus-latest retained beyond that), every source GUID tracked in `coalescedMessageGuids`. DM-only and opt-in/per-channel; legacy BlueBubbles `channels.bluebubbles.coalesceSameSenderDms` should migrate to `channels.imessage.coalesceSameSenderDms`.

### Scenarios and what the agent sees

The "Flag on" column shows behavior on an `imsg` build emitting `balloon_bundle_id`; on metadata-less builds, rows marked "Two/N turns" instead fall back to a legacy single-turn merge.

| User composes | `chat.db` produces | Flag off (default) | Flag on + window (balloon metadata) |
| --- | --- | --- | --- |
| `Dump https://example.com` (one send) | 2 rows ~1 s apart | Two turns: "Dump" alone, then URL | One turn: merged `Dump https://example.com` |
| `Save this 📎image.jpg caption` | 2 rows, no URL balloon metadata | Two turns | Two turns (legacy merge on metadata-less builds) |
| `/status` standalone / URL pasted alone | 1 row | Instant dispatch | **Wait up to window, then dispatch** |
| Text + URL as two messages, minutes apart | 2 rows outside window | Two turns | Two turns (window expires between them) |
| Two people typing in a group chat | N rows from M senders | M+ turns (one per sender bucket) | M+ turns — groups are not coalesced |

## Inbound Recovery After a Bridge or Gateway Restart

iMessage recovers messages missed while the gateway was down and suppresses the stale "backlog bomb" Apple can flush after a Push recovery. The behavior is always on, built on the inbound dedupe — no config enables it.

- **Replay dedupe.** Every dispatched inbound message is recorded by its Apple GUID in persistent plugin state (`imessage.inbound-dedupe`), claimed at ingestion and committed after handling (released on transient failure to retry); anything already handled is dropped instead of dispatched twice, letting recovery replay aggressively without per-message bookkeeping.
- **Downtime recovery.** On startup the monitor remembers the last dispatched `chat.db` rowid (a persisted per-account cursor) and passes it to `imsg watch.subscribe` as `since_rowid`, so imsg replays rows that landed while the gateway was down, then tails live. Replay is bounded to recent rows and to messages up to ~2 hours old.
- **Stale-backlog age fence.** Rows above the startup boundary are live; one whose send date is more than ~15 minutes older than its arrival is the Push-flush backlog and is suppressed. Replayed rows (at/below the boundary) use the wider window.

Recovery works over both local and remote `cliPath` setups because `since_rowid` replay runs over the same `imsg` RPC connection; the window differs. Locally the gateway reads `chat.db`, anchors the startup rowid boundary, caps the replay span, and delivers missed messages up to a couple of hours old; over remote SSH it cannot read the database, so replay is uncapped and every row uses the live age fence. Run the gateway on the Messages Mac for the wider window.

**Operator-visible signal.** Suppressed backlog is logged at the default level, never silently dropped (the `recovery` flag shows the window): `imessage: suppressed stale inbound backlog account=<id> sent=<iso> recovery=<bool> (<N> suppressed since start)`.

**Migration.** `channels.imessage.catchup.*` is deprecated — downtime recovery is now automatic and needs no config for new setups. Existing `catchup.enabled: true` configs remain honored as a compatibility profile for the recovery replay window; disabled catchup blocks (`enabled: false` or no `enabled: true`) are retired and `openclaw doctor --fix` removes them.

## Troubleshooting

- **`imsg` not found or RPC unsupported.** Validate with `imsg rpc --help`, `imsg status --json`, `openclaw channels status --probe`. If probe reports RPC unsupported, update `imsg`. If private-API actions are unavailable, run `imsg launch` in the logged-in macOS session and probe again. If the gateway is not on macOS, use the Remote Mac over SSH setup.
- **Messages send but inbound iMessages do not arrive.** First prove whether the message reached the local Mac — if `chat.db` does not change, OpenClaw cannot receive it even when `imsg status --json` reports a healthy bridge:

```bash
imsg chats --limit 10 --json
imsg watch --chat-id <chat-id> --json
sqlite3 ~/Library/Messages/chat.db \
  "select datetime(max(date)/1000000000 + 978307200, 'unixepoch', 'localtime'), max(ROWID) from message;"
```

If phone-sent messages create no new rows, repair the macOS Messages/Apple Push layer before changing OpenClaw config; a one-shot service refresh (`launchctl kickstart -k` of `com.apple.apsd`, `com.apple.CommCenter`, `com.apple.identityservicesd`, `com.apple.imagent`, then `imsg launch` and `openclaw gateway restart`) is often enough. Confirm a new `chat.db` row or `imsg watch` event before debugging sessions. Do not run this as a periodic relaunch loop; repeated `imsg launch` plus gateway restarts during active work can interrupt deliveries and strand in-flight channel runs.

- **Gateway is not running on macOS.** The default `cliPath: "imsg"` must run on the Mac signed into Messages; on Linux/Windows set `channels.imessage.cliPath` to a wrapper that SSHes to that Mac and runs `imsg "$@"`, then run `openclaw channels status --probe --channel imessage`.
- **DMs are ignored.** Check `channels.imessage.dmPolicy`, `allowFrom`, and pairing approvals (`openclaw pairing list imessage`).
- **Group messages are ignored.** Check `channels.imessage.groupPolicy`, `groupAllowFrom`, `groups` allowlist behavior, and mention patterns (`agents.list[].groupChat.mentionPatterns`).
- **Remote attachments fail.** Check `channels.imessage.remoteHost`, `channels.imessage.remoteAttachmentRoots`, SSH/SCP key auth, the host key in `~/.ssh/known_hosts` on the gateway host, and remote path readability on the Messages Mac.
- **macOS permission prompts were missed.** Re-run in an interactive GUI terminal in the same user/session context and approve prompts (`imsg chats --limit 1`, `imsg send <handle> "test"`); confirm Full Disk Access + Automation are granted for the OpenClaw/`imsg` process context.

## Configuration Reference Pointers

The full iMessage field reference is the [Configuration reference - iMessage](https://docs.openclaw.ai/gateway/config-channels#imessage) page (linked, not duplicated), with broader settings under [Gateway configuration](https://docs.openclaw.ai/gateway/configuration) and DM authentication under [Pairing](https://docs.openclaw.ai/channels/pairing).

**Source**: OpenClaw documentation — `channels/imessage` (mirror `inbox/openclaw_docs/channels/imessage.md`), sections: Media/chunking/delivery targets · Private API actions · Config writes · Coalescing split-send DMs · Inbound recovery · Troubleshooting · Configuration reference pointers
**Last Updated**: 2026-06-22
**Status**: Active
