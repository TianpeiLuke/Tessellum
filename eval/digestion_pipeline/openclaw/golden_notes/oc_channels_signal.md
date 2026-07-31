---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - signal
keywords:
  - openclaw signal channel
  - signal-cli integration
  - signal-cli-rest-api container
  - signal bot number setup
  - signal dmpolicy pairing
  - signal apimode auto native container
  - signal qr link vs sms register
  - signal access control allowlist
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/signal
access_control_group: ["general"]
---

# OpenClaw — Connecting Signal via signal-cli

## Overview

This note is the operator procedure for connecting Signal to the OpenClaw gateway through `signal-cli`, mirroring the `channels/signal` source page. OpenClaw does not embed libsignal; the gateway talks to `signal-cli` over HTTP in one of two transports — a **native daemon** (JSON-RPC + SSE) or the **`bbernhard/signal-cli-rest-api`** Docker container (REST + WebSocket). It covers prerequisites, the dedicated-number model, the two setup paths (Path A QR-link an existing account vs Path B register a bot number by SMS on Linux), external-daemon (`httpUrl`) and container (`apiMode`) modes, DM/group access control, media limits, typing/read receipts, reactions and approval reactions, delivery targets, troubleshooting, security notes, and the full configuration reference.

## Prerequisites

- OpenClaw installed on your server (the Linux flow is tested on Ubuntu 24).
- One of: `signal-cli` available on the host (native mode), **or** the `bbernhard/signal-cli-rest-api` Docker container (container mode).
- A phone number that can receive one verification SMS (for the SMS registration path).
- Browser access for the Signal captcha (`signalcaptchas.org`) during registration.

## Quick setup (beginner) and the number model

The recommended flow: use a **separate Signal number** for the bot, install `signal-cli` (Java/JRE required for the JVM build), pick one setup path (Path A QR link or Path B SMS register), configure OpenClaw, restart the gateway, then send a first DM and approve pairing with `openclaw pairing approve signal <CODE>`. The **number model is load-bearing**: the gateway connects to a Signal *device* (the `signal-cli` account); running the bot on your personal Signal account makes it ignore your own messages (loop protection), so "I text the bot and it replies" requires a separate bot number. Minimal config:

```json5
{
  channels: {
    signal: {
      enabled: true,
      account: "+15551234567",
      cliPath: "signal-cli",
      dmPolicy: "pairing",
      allowFrom: ["+15557654321"],
    },
  },
}
```

Field reference: `account` is the bot phone number in E.164 format; `cliPath` is the path to `signal-cli` (just `signal-cli` if on `PATH`); `configPath` is the signal-cli config dir passed as `--config`; `dmPolicy` is the DM access policy (`pairing` recommended); `allowFrom` lists phone numbers or `uuid:<id>` values allowed to DM. **What it is**: a Signal channel via `signal-cli` (not embedded libsignal) with deterministic routing — replies always go back to Signal; DMs share the agent's main session while groups are isolated under `agent:<agentId>:signal:group:<groupId>`. **Config writes**: by default Signal may write config updates triggered by `/config set|unset` (requires `commands.config: true`); disable with `channels: { signal: { configWrites: false } }`.

## Setup path A: link existing Signal account (QR)

Install `signal-cli` (JVM or native build), link a bot account with `signal-cli link -n "OpenClaw"` then scan the QR in Signal, configure Signal and start the gateway. The config is the same minimal `channels.signal` block shown above. Multi-account support uses `channels.signal.accounts` with per-account config and an optional `name` (the shared multi-account pattern is documented in the gateway config-channels reference).

## Setup path B: register a dedicated bot number (SMS, Linux)

Use this for a dedicated bot number instead of linking an existing Signal app account. Get a number that can receive SMS (or voice verification for landlines) to avoid account/session conflicts. Install `signal-cli` on the gateway host (native build shown; the JVM build `signal-cli-${VERSION}.tar.gz` needs JRE 25+ first), and keep `signal-cli` updated since upstream notes old releases can break as Signal server APIs change:

```bash
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/AsamK/signal-cli/releases/latest | sed -e 's/^.*\/v//')
curl -L -O "https://github.com/AsamK/signal-cli/releases/download/v${VERSION}/signal-cli-${VERSION}-Linux-native.tar.gz"
sudo tar xf "signal-cli-${VERSION}-Linux-native.tar.gz" -C /opt
sudo ln -sf /opt/signal-cli /usr/local/bin/
signal-cli --version
```

Register and verify the number with `signal-cli -a +<BOT_PHONE_NUMBER> register`. If captcha is required, open `https://signalcaptchas.org/registration/generate.html`, complete it, copy the `signalcaptcha://...` link target from "Open Signal", run from the same external IP as the browser session when possible, then re-run registration immediately (captcha tokens expire quickly):

```bash
signal-cli -a +<BOT_PHONE_NUMBER> register --captcha '<SIGNALCAPTCHA_URL>'
signal-cli -a +<BOT_PHONE_NUMBER> verify <VERIFICATION_CODE>
```

Then configure OpenClaw and restart the gateway — if run as a user systemd service, `systemctl --user restart openclaw-gateway.service` — then verify with `openclaw doctor` and `openclaw channels status --probe`. Finally pair your DM sender: send any message to the bot number, approve the code with `openclaw pairing approve signal <PAIRING_CODE>`, and save the bot number as a contact to avoid "Unknown contact". **Warning**: registering a phone-number account with `signal-cli` can de-authenticate the main Signal app session for that number — prefer a dedicated bot number, or use QR link mode to keep your existing phone app setup. Upstream references: the `signal-cli` README, captcha flow wiki, and linking/provisioning wiki.

## External daemon mode (httpUrl)

If you want to manage `signal-cli` yourself (slow JVM cold starts, container init, or shared CPUs), run the daemon separately and point OpenClaw at it via `httpUrl`; this skips auto-spawn and the in-OpenClaw startup wait. For slow starts when auto-spawning instead, set `channels.signal.startupTimeoutMs`.

```json5
{
  channels: {
    signal: {
      httpUrl: "http://127.0.0.1:8080",
      autoStart: false,
    },
  },
}
```

## Container mode (bbernhard/signal-cli-rest-api)

Instead of running `signal-cli` natively, use the `bbernhard/signal-cli-rest-api` Docker container, which wraps `signal-cli` behind a REST API and WebSocket interface. The container **must** run with `MODE=json-rpc` for real-time receiving, and register or link your Signal account inside the container before connecting OpenClaw. Example `docker-compose.yml` service plus matching OpenClaw config:

```yaml
signal-cli:
  image: bbernhard/signal-cli-rest-api:latest
  environment:
    MODE: json-rpc
  ports:
    - "8080:8080"
  volumes:
    - signal-cli-data:/home/.local/share/signal-cli
```

```json5
{
  channels: {
    signal: {
      enabled: true,
      account: "+15551234567",
      httpUrl: "http://signal-cli:8080",
      autoStart: false,
      apiMode: "container", // or "auto" to detect automatically
    },
  },
}
```

The `apiMode` field selects the protocol: `"auto"` (default) probes both transports and streaming validates the container WebSocket receive; `"native"` forces native signal-cli (JSON-RPC at `/api/v1/rpc`, SSE at `/api/v1/events`); `"container"` forces the bbernhard container (REST at `/v2/send`, WebSocket at `/v1/receive/{account}`). In `"auto"` mode OpenClaw caches the detected mode for 30 seconds to avoid repeated probes, and container receive is only selected for streaming after `/v1/receive/{account}` upgrades to WebSocket (which requires `MODE=json-rpc`). Container mode supports the same Signal operations as native mode where the container exposes matching APIs — sends, receives, attachments, typing indicators, read/viewed receipts, reactions, groups, and styled text — and OpenClaw translates its native Signal RPC calls into the container's REST payloads, including `group.{base64(internal_id)}` group IDs and `text_mode: "styled"`. Operational notes: use `autoStart: false` with container mode (OpenClaw should not spawn a native daemon when `apiMode: "container"`); use `MODE=json-rpc` for receiving because `MODE=normal` can make `/v1/about` look healthy while `/v1/receive/{account}` does not WebSocket-upgrade, so OpenClaw will not select container receive streaming in `auto` mode; set `apiMode: "container"` when the `httpUrl` points at bbernhard's REST API and `"native"` when it points at native `signal-cli` JSON-RPC/SSE; and container attachment downloads honor the same media byte limits as native mode.

## Access control (DMs + groups)

**DMs** default to `channels.signal.dmPolicy = "pairing"`: unknown senders receive a pairing code, their messages are ignored until approved, and codes expire after 1 hour. Approve via `openclaw pairing list signal` and `openclaw pairing approve signal <CODE>`; pairing is the default token exchange for Signal DMs. UUID-only senders (from `sourceUuid`) are stored as `uuid:<id>` in `channels.signal.allowFrom`. **Groups** use `channels.signal.groupPolicy = open | allowlist | disabled`, with `channels.signal.groupAllowFrom` controlling which groups or senders may trigger replies when `allowlist` is set — entries can be Signal group IDs (raw, `group:<id>`, or `signal:group:<id>`), sender phone numbers, `uuid:<id>` values, or `*`. `channels.signal.groups["<group-id>" | "*"]` overrides group behavior with `requireMention`, `tools`, and `toolsBySender`, and `channels.signal.accounts.<id>.groups` supplies per-account overrides. Two gotchas: allowlisting a group through `groupAllowFrom` does not by itself disable mention gating — a configured `channels.signal.groups["<group-id>"]` entry processes every group message unless `requireMention=true`; and if `channels.signal` is completely missing, runtime falls back to `groupPolicy="allowlist"` for group checks even if `channels.defaults.groupPolicy` is set.

## How it works (behavior)

In native mode `signal-cli` runs as a daemon and the gateway reads events via SSE; in container mode the gateway sends via REST and receives via WebSocket. Inbound messages are normalized into the shared channel envelope, and replies always route back to the same number or group.

## Media + limits

Outbound text is chunked to `channels.signal.textChunkLimit` (default 4000); `channels.signal.chunkMode="newline"` splits on blank lines (paragraph boundaries) before length chunking. Attachments are supported (base64 fetched from `signal-cli`); voice-note attachments use the `signal-cli` filename as a MIME fallback when `contentType` is missing so transcription can still classify AAC voice memos. The default media cap is `channels.signal.mediaMaxMb` (default 8), and `channels.signal.ignoreAttachments` skips downloading media. Group history context uses `channels.signal.historyLimit` (or `channels.signal.accounts.*.historyLimit`), falling back to `messages.groupChat.historyLimit`; set `0` to disable (default 50).

## Typing + read receipts

OpenClaw sends typing signals via `signal-cli sendTyping` and refreshes them while a reply is running. When `channels.signal.sendReadReceipts` is true, OpenClaw forwards read receipts for allowed DMs. `signal-cli` does not expose read receipts for groups.

## Reactions and approval reactions

Use `message action=react` with `channel=signal`; targets are sender E.164 or UUID (`uuid:<id>` from pairing output, or a bare UUID), `messageId` is the Signal timestamp of the message you react to, and group reactions require `targetAuthor` or `targetAuthorUuid`. Verbatim invocations: `message action=react channel=signal target=uuid:<id> messageId=<ts> emoji=🔥`, `... target=+15551234567 messageId=<ts> emoji=🔥 remove=true`, and `... target=signal:group:<groupId> targetAuthor=uuid:<sender-uuid> messageId=<ts> emoji=✅`. Reactions are governed by `channels.signal.actions.reactions` (default true) and `channels.signal.reactionLevel` (`off | ack | minimal | extensive` — `off`/`ack` disable agent reactions so `react` errors, `minimal`/`extensive` enable them and set the guidance level), with per-account overrides at `channels.signal.accounts.<id>.actions.reactions` and `channels.signal.accounts.<id>.reactionLevel`.

**Approval reactions**: Signal exec and plugin approval prompts use the top-level `approvals.exec` and `approvals.plugin` routing blocks — there is no `channels.signal.execApprovals` block. `👍` approves once, `👎` denies, and `/approve <id> allow-always` grants persistent approval when offered. Approval-reaction resolution requires explicit Signal approvers from `channels.signal.allowFrom`, `channels.signal.defaultTo`, or the matching account-level fields; direct same-chat exec prompts can suppress the duplicate local `/approve` fallback without explicit approvers, while no-approver group approvals keep the local fallback visible.

## Delivery targets (CLI/cron)

DMs: `signal:+15551234567` (or plain E.164). UUID DMs: `uuid:<id>` (or bare UUID). Groups: `signal:group:<groupId>`. Usernames: `username:<name>` (if supported by your Signal account).

## Troubleshooting

Run this ladder first: `openclaw status`, `openclaw gateway status`, `openclaw logs --follow`, `openclaw doctor`, `openclaw channels status --probe`. Then confirm DM pairing state with `openclaw pairing list signal`. Common failures: reachable daemon but no replies → verify account/daemon settings (`httpUrl`, `account`) and receive mode; DMs ignored → the sender is pending pairing approval; group messages ignored → group sender/mention gating blocks delivery; config validation errors after edits → run `openclaw doctor --fix`; Signal missing from diagnostics → confirm `channels.signal.enabled: true`. Extra checks: `pgrep -af signal-cli` and grepping the daily log `/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log` for `signal`.

## Security notes

`signal-cli` stores account keys locally (typically `~/.local/share/signal-cli/data/`). Back up Signal account state before a server migration or rebuild. Keep `channels.signal.dmPolicy: "pairing"` unless you explicitly want broader DM access. SMS verification is only needed for registration or recovery, but losing control of the number/account can complicate re-registration.

## Configuration reference (Signal)

Provider options under `channels.signal`: `enabled`; `apiMode` (`auto | native | container`, default auto); `account` (E.164 bot account); `cliPath`; `configPath` (optional `--config` dir); `httpUrl` (full daemon URL, overrides host/port); `httpHost`/`httpPort` (daemon bind, default 127.0.0.1:8080); `autoStart` (default true if `httpUrl` unset); `startupTimeoutMs` (ms, cap 120000); `receiveMode` (`on-start | manual`); `ignoreAttachments`; `ignoreStories`; `sendReadReceipts`; `dmPolicy` (`pairing | allowlist | open | disabled`, default pairing); `allowFrom` (DM allowlist of E.164 or `uuid:<id>`; `open` requires `"*"`; Signal has no usernames, so use phone/UUID ids); `groupPolicy` (`open | allowlist | disabled`, default allowlist); `groupAllowFrom` (Signal group IDs raw/`group:<id>`/`signal:group:<id>`, sender E.164, or `uuid:<id>`); `groups` (per-group overrides keyed by group id or `"*"`, supporting `requireMention`/`tools`/`toolsBySender`); `accounts.<id>.groups` (per-account version); `historyLimit` (max group context messages, 0 disables); `dmHistoryLimit` (DM history in turns, per-user override `channels.signal.dms["<phone_or_uuid>"].historyLimit`); `textChunkLimit`; `chunkMode` (`length` default or `newline`); and `mediaMaxMb`. Related global options: `agents.list[].groupChat.mentionPatterns` (Signal has no native mentions), `messages.groupChat.mentionPatterns` (fallback), and `messages.responsePrefix`.

**Source**: OpenClaw documentation — `channels/signal` (mirror `inbox/openclaw_docs/channels/signal.md`)
**Last Updated**: 2026-06-22
**Status**: Active
