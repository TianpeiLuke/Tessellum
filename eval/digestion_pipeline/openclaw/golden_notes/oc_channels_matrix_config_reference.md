---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - matrix
keywords:
  - matrix channel config reference
  - channels.matrix config keys
  - matrix account connection keys
  - matrix encryption startupverification keys
  - matrix grouppolicy dm.policy allowlist
  - matrix replyto streaming chunkmode keys
  - matrix ackreaction reactionnotifications
  - matrix groups per-room overrides
  - matrix execapprovals config
  - dangerouslyallownamematching
topics:
  - OpenClaw
  - Matrix Channel Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/channels/matrix
access_control_group: ["general"]
---

# OpenClaw — Matrix Channel Configuration Reference

## Overview

This note models the flat **configuration-key reference** for the OpenClaw Matrix channel — the `## Configuration reference` section of the `channels/matrix` source page. It catalogs every documented option under `channels.matrix` (and the per-account `channels.matrix.accounts.<id>` overrides) across the seven option groups the source defines: account-and-connection, encryption, access-and-policy, reply-behavior, reaction-settings, tooling/per-room-overrides, and exec-approval-settings — plus the allowlist-resolution semantics (`dangerouslyAllowNameMatching`) that gate how user/room keys are matched. It documents the keys, their accepted values, and their defaults verbatim from source; the operational *procedures* that set these keys live in the sibling setup/encryption/behavior notes (linked under Related Notes).

## Allowlist field semantics (`dangerouslyAllowNameMatching`)

Allowlist-style user fields (`groupAllowFrom`, `dm.allowFrom`, `groups.<room>.users`) accept full Matrix user IDs (safest). Non-ID user entries are ignored by default. If you set `dangerouslyAllowNameMatching: true`, exact Matrix directory display-name matches are resolved at startup and whenever the allowlist changes while the monitor is running; entries that cannot be resolved are ignored at runtime.

Room allowlist keys (`groups`, legacy `rooms`) should be room IDs or aliases. Plain room-name keys are ignored by default; `dangerouslyAllowNameMatching: true` restores best-effort lookup against joined room names.

## Account and connection

These keys identify the Matrix account and its homeserver connection. Top-level `channels.matrix` values are inherited as defaults by named accounts.

- `enabled`: enable or disable the channel.
- `name`: optional display label for the account.
- `defaultAccount`: preferred account ID when multiple Matrix accounts are configured.
- `accounts`: named per-account overrides. Top-level `channels.matrix` values are inherited as defaults.
- `homeserver`: homeserver URL, for example `https://matrix.example.org`.
- `network.dangerouslyAllowPrivateNetwork`: allow this account to connect to `localhost`, LAN/Tailscale IPs, or internal hostnames.
- `proxy`: optional HTTP(S) proxy URL for Matrix traffic. Per-account override supported.
- `userId`: full Matrix user ID (`@bot:example.org`).
- `accessToken`: access token for token-based auth. Plaintext and SecretRef values supported across env/file/exec providers ([Secrets Management](https://docs.openclaw.ai/gateway/secrets)).
- `password`: password for password-based login. Plaintext and SecretRef values supported.
- `deviceId`: explicit Matrix device ID.
- `deviceName`: device display name used at password-login time.
- `avatarUrl`: stored self-avatar URL for profile sync and `profile set` updates.
- `initialSyncLimit`: maximum number of events fetched during startup sync.

## Encryption

These keys control E2EE enablement and the startup self-verification cadence.

- `encryption`: enable E2EE. Default: `false`.
- `startupVerification`: `"if-unverified"` (default when E2EE is on) or `"off"`. Auto-requests self-verification on startup when this device is unverified.
- `startupVerificationCooldownHours`: cooldown before the next automatic startup request. Default: `24`.

## Access and policy

These keys gate which senders may interact and how invites are handled.

- `groupPolicy`: `"open"`, `"allowlist"`, or `"disabled"`. Default: `"allowlist"`.
- `groupAllowFrom`: allowlist of user IDs for room traffic.
- `dm.enabled`: when `false`, ignore all DMs. Default: `true`.
- `dm.policy`: `"pairing"` (default), `"allowlist"`, `"open"`, or `"disabled"`. Applies after the bot has joined and classified the room as a DM; it does not affect invite handling.
- `dm.allowFrom`: allowlist of user IDs for DM traffic.
- `dm.sessionScope`: `"per-user"` (default) or `"per-room"`.
- `dm.threadReplies`: DM-only override for reply threading (`"off"`, `"inbound"`, `"always"`).
- `allowBots`: accept messages from other configured Matrix bot accounts (`true` or `"mentions"`).
- `allowlistOnly`: when `true`, forces all active DM policies (except `"disabled"`) and `"open"` group policies to `"allowlist"`. Does not change `"disabled"` policies.
- `dangerouslyAllowNameMatching`: when `true`, allows Matrix display-name directory lookup for user allowlist entries and joined-room name lookup for room allowlist keys. Prefer full `@user:server` IDs and room IDs or aliases.
- `autoJoin`: `"always"`, `"allowlist"`, or `"off"`. Default: `"off"`. Applies to every Matrix invite, including DM-style invites.
- `autoJoinAllowlist`: rooms/aliases allowed when `autoJoin` is `"allowlist"`. Alias entries are resolved against the homeserver, not against state claimed by the invited room.
- `contextVisibility`: supplemental context visibility (`"all"` default, `"allowlist"`, `"allowlist_quote"`).

## Reply behavior

These keys shape how, where, and in what chunks the bot posts its replies.

- `replyToMode`: `"off"`, `"first"`, `"all"`, or `"batched"`.
- `threadReplies`: `"off"`, `"inbound"`, or `"always"`.
- `threadBindings`: per-channel overrides for thread-bound session routing and lifecycle.
- `streaming`: `"off"` (default), `"partial"`, `"quiet"`, or object form `{ mode, preview: { toolProgress } }`. `true` ↔ `"partial"`, `false` ↔ `"off"`.
- `blockStreaming`: when `true`, completed assistant blocks are kept as separate progress messages.
- `markdown`: optional Markdown rendering config for outbound text.
- `responsePrefix`: optional string prepended to outbound replies.
- `textChunkLimit`: outbound chunk size in characters when `chunkMode: "length"`. Default: `4000`.
- `chunkMode`: `"length"` (default, splits by character count) or `"newline"` (splits at line boundaries).
- `historyLimit`: number of recent room messages included as `InboundHistory` when a room message triggers the agent. Falls back to `messages.groupChat.historyLimit`; effective default `0` (disabled).
- `mediaMaxMb`: media size cap in MB for outbound sends and inbound processing.

## Reaction settings

These keys override the channel/account reaction defaults.

- `ackReaction`: ack reaction override for this channel/account.
- `ackReactionScope`: scope override (`"group-mentions"` default, `"group-all"`, `"direct"`, `"all"`, `"none"`, `"off"`).
- `reactionNotifications`: inbound reaction notification mode (`"own"` default, `"off"`).

## Tooling and per-room overrides

These keys gate per-action tools and provide a per-room policy map. The `groups` map keys are stable room IDs after resolution (`rooms` is a legacy alias), and each room may carry its own overrides.

- `actions`: per-action tool gating (`messages`, `reactions`, `pins`, `profile`, `memberInfo`, `channelInfo`, `verification`).
- `groups`: per-room policy map. Session identity uses the stable room ID after resolution. (`rooms` is a legacy alias.)
  - `groups.<room>.account`: restrict one inherited room entry to a specific account.
  - `groups.<room>.allowBots`: per-room override of the channel-level setting (`true` or `"mentions"`).
  - `groups.<room>.users`: per-room sender allowlist.
  - `groups.<room>.tools`: per-room tool allow/deny overrides.
  - `groups.<room>.autoReply`: per-room mention-gating override. `true` disables mention requirements for that room; `false` forces them back on.
  - `groups.<room>.skills`: per-room skill filter.
  - `groups.<room>.systemPrompt`: per-room system prompt snippet.

## Exec approval settings

These keys configure Matrix as a native exec/plugin approval client. They live under `channels.matrix.execApprovals` (or `channels.matrix.accounts.<account>.execApprovals` for a per-account override).

- `execApprovals.enabled`: deliver exec approvals through Matrix-native prompts.
- `execApprovals.approvers`: Matrix user IDs allowed to approve. Falls back to `dm.allowFrom`.
- `execApprovals.target`: `"dm"` (default), `"channel"`, or `"both"`.
- `execApprovals.agentFilter` / `execApprovals.sessionFilter`: optional agent/session allowlists for delivery.

**Source**: OpenClaw documentation — `channels/matrix` § Configuration reference (mirror `inbox/openclaw_docs/channels/matrix.md`)
**Last Updated**: 2026-06-22
**Status**: Active
