---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - matrix
keywords:
  - openclaw matrix message behavior
  - matrix streaming blockStreaming preview
  - matrix voice note transcription
  - com.openclaw.approval metadata
  - matrix threads sessionScope threadReplies
  - matrix acp conversation bindings
  - matrix reactions ackReaction
  - matrix dm room policy direct repair
  - matrix exec approvals slash commands
  - matrix multi-account target resolution
topics:
  - OpenClaw
  - Matrix channel
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/channels/matrix
access_control_group: ["general"]
---

# OpenClaw — Matrix Channel Runtime Message Behavior

## Overview

This note models the **runtime message behavior** of the OpenClaw Matrix channel — how an already-configured bot streams replies, ingests voice notes, renders approval prompts, threads conversations, binds ACP workspaces, reacts, scopes context/history, enforces DM/room policy, and resolves targets across accounts. It mirrors the behavior sections of the `channels/matrix` source page (Configuration example, Streaming, Voice messages, Approval metadata, Bot-to-bot rooms, Threads, ACP bindings, Reactions, History/Context visibility, DM/room policy, Direct room repair, Exec approvals, Slash commands, Multi-account routing, Target resolution). Install/auth setup, E2EE/verification, and the flat config-key reference live in sibling notes.

## Baseline Configuration

A practical baseline combines DM pairing, a room allowlist, E2EE, and partial streaming under `channels.matrix`:

```json5
{
  channels: {
    matrix: {
      enabled: true,
      homeserver: "https://matrix.example.org",
      accessToken: "syt_xxx",
      encryption: true,
      dm: { policy: "pairing", sessionScope: "per-room", threadReplies: "off" },
      groupPolicy: "allowlist",
      groupAllowFrom: ["@admin:example.org"],
      groups: { "!roomid:example.org": { requireMention: true } },
      autoJoin: "allowlist",
      autoJoinAllowlist: ["!roomid:example.org"],
      threadReplies: "inbound",
      replyToMode: "off",
      streaming: "partial",
    },
  },
}
```

## Streaming Previews

Matrix reply streaming is opt-in. `streaming` controls how the in-flight reply is delivered; `blockStreaming` (independent) controls whether each completed block is kept as its own message. Modes:

- `"off"` (default): wait for the full reply, send once. `true` ↔ `"partial"`, `false` ↔ `"off"`.
- `"partial"`: edit one normal text message in place as the model writes the current block. Stock clients may notify on the first preview, not the final edit.
- `"quiet"`: like `"partial"` but a non-notifying notice; recipients are notified only once a per-user push rule matches the finalized edit (see push-rules sibling).

Under `"partial"`/`"quiet"`, `blockStreaming: true` keeps a live draft plus completed blocks as messages while `false` (default) finalizes the draft in place; under `streaming: "off"`, `true` sends one notifying message per finished block and `false` one for the full reply. The object form `streaming: { mode: "partial", preview: { toolProgress: false } }` keeps answer previews but hides interim tool/progress lines (otherwise on by default). A preview that grows past Matrix's per-event size limit falls back to final-only delivery. Media replies always send attachments normally, redacting an unreusable stale preview first. Preview edits cost extra API calls, so `streaming: "off"` is the most conservative rate-limit profile.

## Voice Messages

Inbound voice notes are transcribed **before the room mention gate** — so a voice note saying the bot name can trigger the agent in a `requireMention: true` room, and the agent gets the transcript rather than an audio placeholder. Matrix uses the shared audio media provider under `tools.media.audio` (such as OpenAI `gpt-4o-mini-transcribe`). Details: `m.audio` and `m.file` events with an `audio/*` MIME type are eligible; encrypted rooms decrypt the attachment through the existing media path first; the transcript is marked machine-generated and untrusted; the attachment is marked already-transcribed so media tools do not re-transcribe it; set `tools.media.audio.enabled: false` to disable transcription globally.

## Approval Metadata

Matrix native approval prompts are normal `m.room.message` events with OpenClaw-specific custom event content under `com.openclaw.approval`. Matrix permits custom event-content keys, so stock clients still render the text body while OpenClaw-aware clients read the structured approval id, kind, state, available decisions, and exec/plugin details. When a prompt is too long for one event, OpenClaw chunks the visible text and attaches `com.openclaw.approval` to the first chunk only; allow/deny reactions bind to that first event, so long prompts keep the same approval target as single-event prompts. `streaming: "quiet"` notifies recipients only once a block/turn is finalized and a per-user push rule matches the finalized preview marker — full recipe in the push-rules sibling note.

## Bot-to-Bot Rooms

By default, Matrix messages from other configured OpenClaw Matrix accounts are ignored. Use `allowBots` to enable inter-agent traffic: `true` accepts messages from other configured Matrix bot accounts in allowed rooms and DMs; `"mentions"` accepts them only when they visibly mention this bot in rooms (DMs still allowed); `groups.<room>.allowBots` overrides per room. Accepted configured-bot messages use shared bot loop protection — set `channels.defaults.botLoopProtection`, then override with `channels.matrix.botLoopProtection` or `...groups.<room>.botLoopProtection` per room. OpenClaw still ignores messages from the same Matrix user ID to avoid self-reply loops; Matrix exposes no native bot flag, so "bot-authored" means "sent by another configured Matrix account on this gateway". Use strict allowlists and mention requirements for bot-to-bot traffic in shared rooms.

## Threads

Matrix supports native threads for automatic replies and message-tool sends, via two independent knobs. `dm.sessionScope` maps DM rooms to sessions: `"per-user"` (default) shares one session across all DM rooms with the same routed peer, `"per-room"` gives each DM room its own session key even for the same peer — explicit conversation bindings always win over `sessionScope`. `threadReplies` decides where the bot replies: `"off"` keeps replies top-level (inbound threaded messages stay on the parent session), `"inbound"` replies in a thread only when the inbound message was already threaded, and `"always"` replies in a thread rooted at the triggering message, routing that conversation through a matching thread-scoped session from the first trigger. `dm.threadReplies` overrides this for DMs only. Inbound threaded messages include the thread root as context; message-tool sends auto-inherit the current thread when targeting the same room (or same DM user target) unless an explicit `threadId` is given, with DM user-target reuse only when session metadata proves the same DM peer on the same account. `/focus`, `/unfocus`, `/agents`, `/session idle`, `/session max-age`, and thread-bound `/acp spawn` all work in rooms and DMs; top-level `/focus` creates and binds a new thread when `threadBindings.spawnSessions` is enabled, and `/focus` or `/acp spawn --thread here` inside an existing thread binds it in place. When two DM rooms collide on the same shared session, OpenClaw posts a one-time `m.notice` pointing to the `/focus` escape hatch and suggesting a `dm.sessionScope` change (only when thread bindings are on).

## ACP Conversation Bindings

Matrix rooms, DMs, and existing threads can become durable ACP workspaces without changing the chat surface. `/acp spawn codex --bind here` inside a DM, room, or thread keeps that surface as the chat and routes future messages to the spawned ACP session (inside a thread it binds that thread in place). `/new`/`/reset` reset the same bound session in place; `/acp close` closes it and removes the binding. `--bind here` does not create a child thread, whereas `threadBindings.spawnSessions` gates `/acp spawn --thread auto|here`, where OpenClaw must create or bind a child thread. Matrix inherits global defaults from `session.threadBindings` and supports per-channel overrides `threadBindings.{enabled,idleHours,maxAgeHours,spawnSessions,defaultSpawnContext}` (set `defaultSpawnContext: "isolated"` so native subagent thread spawns do not fork the parent transcript).

## Reactions

Matrix supports outbound reactions, inbound reaction notifications, and ack reactions; outbound tooling is gated by `channels.matrix.actions.reactions`. Tool actions: `react` adds a reaction, `reactions` lists the summary, `emoji=""` removes the bot's own reactions on that event, `remove: true` removes only the named emoji. Each ack setting resolves per-account → channel → `messages.*` default (first defined wins): `ackReaction` falls back to an agent identity emoji; `ackReactionScope` defaults to `"group-mentions"`; `reactionNotifications` defaults to `"own"`. `reactionNotifications: "own"` forwards added `m.reaction` events targeting bot-authored messages; `"off"` disables them. Reaction removals are not synthesized into system events — Matrix surfaces them as redactions, not standalone `m.reaction` removals.

## History Context

`channels.matrix.historyLimit` controls how many recent room messages are included as `InboundHistory` when a room message triggers the agent (falls back to `messages.groupChat.historyLimit`; if both unset the effective default is `0`/disabled). Room history is room-only — DMs keep normal session history — and pending-only: OpenClaw buffers room messages that have not triggered a reply yet, then snapshots that window when a trigger arrives. The current trigger message is excluded (it stays in the main inbound body), and retries of the same event reuse the original snapshot rather than drifting to newer messages.

## Context Visibility

Matrix supports the shared `contextVisibility` control for supplemental room context (fetched reply text, thread roots, pending history). `"all"` (default) keeps it as received; `"allowlist"` filters it to senders allowed by the active room/user allowlist checks; `"allowlist_quote"` is like `allowlist` but keeps one explicit quoted reply. This affects supplemental context visibility, not whether the inbound message can trigger a reply — trigger authorization still comes from `groupPolicy`/`groups`/`groupAllowFrom` and DM policy.

## DM and Room Policy

DM and room policy combine a DM policy block (`dm.policy: "allowlist"` + `dm.allowFrom` + `dm.threadReplies`) with `groupPolicy: "allowlist"`/`groupAllowFrom`/`groups.<room>.requireMention` room gating (see baseline above). To silence DMs entirely while keeping rooms working, set `dm.enabled: false`. Pairing uses `openclaw pairing list matrix` and `openclaw pairing approve matrix <CODE>`; if an unapproved user keeps messaging before approval, OpenClaw reuses the same pending pairing code and may send a reminder after a short cooldown rather than minting a new code.

## Direct Room Repair

If direct-message state drifts, OpenClaw can end up with stale `m.direct` mappings pointing at old solo rooms instead of the live DM. Inspect with `openclaw matrix direct inspect --user-id @alice:example.org` and repair with `openclaw matrix direct repair --user-id @alice:example.org` (both accept `--account <id>`). The repair flow prefers a strict 1:1 DM already mapped in `m.direct`, falls back to any currently joined strict 1:1 DM with that user, and creates a fresh direct room (rewriting `m.direct`) if none is healthy. It does not delete old rooms automatically — it picks the healthy DM and updates the mapping so future sends, verification notices, and other direct-message flows target the right room.

## Exec Approvals

Matrix can act as a native approval client under `channels.matrix.execApprovals` (or `...accounts.<account>.execApprovals`). `enabled` delivers Matrix-native prompts (when unset or `"auto"`, auto-enables once an approver resolves; `false` disables); `approvers` lists Matrix user IDs allowed to approve exec requests (falls back to `dm.allowFrom`); `target` is `"dm"` (default), `"channel"`, or `"both"`; `agentFilter`/`sessionFilter` are optional agent/session allowlists. Authorization differs by kind: exec approvals use `execApprovals.approvers` (falling back to `dm.allowFrom`), plugin approvals use `dm.allowFrom` only. Both share reaction shortcuts on the primary approval message — `✅` allow once, `❌` deny, `♾️` allow always (when the effective exec policy allows it) — plus fallback slash commands `/approve <id> allow-once|allow-always|deny`. Only resolved approvers can approve or deny; channel delivery includes the command text, so enable `channel`/`both` in trusted rooms only.

## Slash Commands

Slash commands (`/new`, `/reset`, `/model`, `/focus`, `/unfocus`, `/agents`, `/session`, `/acp`, `/approve`, and others) work directly in DMs. In rooms, OpenClaw also recognizes commands prefixed with the bot's own Matrix mention, so `@bot:server /new` triggers the command path without a custom mention regex — keeping the bot responsive to the `@mention /command` posts that Element and similar clients emit on tab-completion. Authorization rules still apply: command senders must satisfy the same DM/room allowlist/owner policies as plain messages.

## Multi-Account Routing

Behavior is per-account through `channels.matrix.accounts`. Top-level `channels.matrix` values are defaults for named accounts unless overridden; a room entry is scoped with `groups.<room>.account`, while entries without `account` are shared (`account: "default"` works when a default is configured at top level). Set `defaultAccount` to pick the account that implicit routing, probing, and CLI commands prefer; an account literally named `default` is used implicitly even when `defaultAccount` is unset; with multiple named accounts and no default, CLI commands refuse to guess and require `defaultAccount` or `--account <id>`. The top-level block is the implicit `default` account only when its auth is complete. Promotion to multi-account moves only Matrix auth/bootstrap keys into the promoted account — shared delivery-policy keys stay at the top level.

## Target Resolution

Matrix accepts these target forms anywhere OpenClaw asks for a room or user target: users as `@user:server`, `user:@user:server`, or `matrix:user:@user:server`; rooms as `!room:server`, `room:!room:server`, or `matrix:room:!room:server`; aliases as `#alias:server`, `channel:#alias:server`, or `matrix:channel:#alias:server`. Matrix room IDs are case-sensitive — use exact casing for explicit delivery targets, cron jobs, bindings, or allowlists, because OpenClaw keeps internal session keys canonical (lowercase) and those are not a reliable source for delivery IDs. Live directory lookup uses the logged-in account: user lookups query the homeserver's user directory; room lookups accept explicit IDs and aliases directly, while joined-room name lookup is best-effort and applies to runtime allowlists only when `dangerouslyAllowNameMatching: true`; an unresolvable room name is ignored by runtime allowlist resolution.

**Source**: OpenClaw documentation — `channels/matrix` (mirror `inbox/openclaw_docs/channels/matrix.md`)
**Last Updated**: 2026-06-22
**Status**: Active
