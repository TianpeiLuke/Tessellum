---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - heartbeat
keywords:
  - openclaw heartbeat delivery
  - heartbeat target routing
  - heartbeat visibility controls
  - showok showalerts useindicator
  - alerts-disabled skip reason
  - heartbeat session lifecycle audit
  - directpolicy block dm
  - per-channel per-account heartbeat
topics:
  - OpenClaw
  - Heartbeat Delivery
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/heartbeat
access_control_group: ["general"]
---

# OpenClaw — Heartbeat Delivery and Visibility Routing

## Overview

This note documents the **delivery and visibility** half of the OpenClaw heartbeat feature: once a periodic heartbeat agent turn produces a reply, this procedure governs where that reply is routed (`target` / `to` / `session`), whether it is shown at all (the `showOk` / `showAlerts` / `useIndicator` flags and their precedence), when the run is skipped up front, and how heartbeat turns affect session lifecycle and audit history. It mirrors the `Delivery behavior`, `Visibility controls`, `What each flag does`, `Per-channel vs per-account examples`, and `Common patterns` sections of the `gateway/heartbeat` source page. The companion note `oc_gateway_heartbeat` covers cadence, defaults, the response contract, the full config schema, and `HEARTBEAT.md`.

## Session and Target Routing

The session a heartbeat *runs in* and the destination a heartbeat is *delivered to* are independent controls. By default heartbeats run in the agent's main session (`agent:<id>:<mainKey>`), or `global` when `session.scope = "global"`; set the `session` field to override to a specific channel session (Discord/WhatsApp/etc.). The `session` field only affects the run context — delivery is controlled by `target` and `to`. To deliver to a specific channel/recipient, set `target` plus `to`; with `target: "last"`, delivery uses the last external channel for that session.

Heartbeat deliveries allow direct/DM targets by default. Set `directPolicy: "block"` to suppress direct-target sends while still running the heartbeat turn (the source contract reports the suppression as `reason=dm-blocked`). If `target` resolves to no external destination, the run still happens but no outbound message is sent.

Routing also defers to lane busyness: if the main queue, target session lane, cron lane, or an active cron job is busy, the heartbeat is skipped and retried later. If `skipWhenBusy: true`, this agent's session-keyed subagent and nested lanes also defer heartbeat runs; other agents' busy lanes do not defer this agent.

## Visibility and Skip Behavior

Three channel-level visibility flags decide whether a heartbeat run is even worth performing. If `showOk`, `showAlerts`, and `useIndicator` are **all disabled**, the run is skipped up front as `reason=alerts-disabled` (no model call). If only alert delivery is disabled, OpenClaw can still run the heartbeat, update due-task timestamps, restore the session idle timestamp, and suppress the outward alert payload — i.e. the internal state work still happens even though nothing is sent.

If the resolved heartbeat target supports typing, OpenClaw shows a typing indicator while the heartbeat run is active. This uses the same target the heartbeat would send chat output to, and it is disabled by `typingMode: "never"`.

## Session Lifecycle and Audit

Heartbeat-only replies do **not** keep the session alive. Heartbeat metadata may update the session row, but idle expiry uses `lastInteractionAt` from the last real user/channel message, and daily expiry uses `sessionStartedAt` — so a stream of heartbeat ticks will not artificially extend a session's lifetime.

Control UI and WebChat history hide heartbeat prompts and OK-only acknowledgments, but the underlying session transcript can still contain those turns for audit/replay. Detached background tasks can enqueue a system event and wake heartbeat when the main session should notice something quickly; that wake does not make the heartbeat run a background task.

## Visibility Controls

By default, `HEARTBEAT_OK` acknowledgments are suppressed while alert content is delivered. You can adjust this per channel or per account. The built-in defaults are `showOk: false`, `showAlerts: true`, `useIndicator: true`:

```yaml
channels:
  defaults:
    heartbeat:
      showOk: false # Hide HEARTBEAT_OK (default)
      showAlerts: true # Show alert messages (default)
      useIndicator: true # Emit indicator events (default)
  telegram:
    heartbeat:
      showOk: true # Show OK acknowledgments on Telegram
  whatsapp:
    accounts:
      work:
        heartbeat:
          showAlerts: false # Suppress alert delivery for this account
```

Precedence is **per-account → per-channel → channel defaults → built-in defaults** — the most specific configuration block wins.

### What each flag does

- `showOk`: sends a `HEARTBEAT_OK` acknowledgment when the model returns an OK-only reply.
- `showAlerts`: sends the alert content when the model returns a non-OK reply.
- `useIndicator`: emits indicator events for UI status surfaces.

If **all three** are false, OpenClaw skips the heartbeat run entirely (no model call) — the same `alerts-disabled` short-circuit described under Visibility and Skip Behavior.

### Per-channel vs per-account examples

A per-channel `heartbeat` block applies to all accounts on that channel; an `accounts.<id>.heartbeat` block narrows the override to a single account (here, suppressing alerts for the Slack `ops` account only while the rest of Slack still shows OKs):

```yaml
channels:
  defaults:
    heartbeat:
      showOk: false
      showAlerts: true
      useIndicator: true
  slack:
    heartbeat:
      showOk: true # all Slack accounts
    accounts:
      ops:
        heartbeat:
          showAlerts: false # suppress alerts for the ops account only
  telegram:
    heartbeat:
      showOk: true
```

### Common patterns

| Goal | Config |
| --- | --- |
| Default behavior (silent OKs, alerts on) | *(no config needed)* |
| Fully silent (no messages, no indicator) | `channels.defaults.heartbeat: { showOk: false, showAlerts: false, useIndicator: false }` |
| Indicator-only (no messages) | `channels.defaults.heartbeat: { showOk: false, showAlerts: false, useIndicator: true }` |
| OKs in one channel only | `channels.telegram.heartbeat: { showOk: true }` |

The "fully silent" pattern is the case that trips the `alerts-disabled` up-front skip — with all three flags false there is no reason to run the model. The "indicator-only" pattern keeps `useIndicator: true` so the run still happens and emits UI status events without sending any chat message.

**Source**: OpenClaw documentation — `gateway/heartbeat` (mirror `inbox/openclaw_docs/gateway/heartbeat.md`), Delivery behavior + Visibility controls sections
**Last Updated**: 2026-06-22
**Status**: Active
