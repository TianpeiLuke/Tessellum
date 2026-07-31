---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - qa_channel
keywords:
  - openclaw qa-channel
  - synthetic qa transport
  - qa-channel config
  - slack-class target grammar
  - pnpm qa:e2e
  - pnpm openclaw qa suite
  - qa:lab debugger
  - end-to-end qa automation
topics:
  - OpenClaw
  - Channels
  - QA Automation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/qa-channel
access_control_group: ["general"]
---

# OpenClaw — QA Channel (Synthetic QA Transport)

## Overview

This note documents the OpenClaw **`qa-channel`** — a bundled synthetic message transport used for automated OpenClaw QA, mirroring the `channels/qa-channel` source page. It is NOT a production channel; it exists to exercise the same channel-plugin boundary used by real transports while keeping state deterministic and fully inspectable. The note covers what the channel does (its Slack-class target grammar, room-turn surfacing, the HTTP-backed synthetic bus, and the host-side self-check runner), its full configuration surface (per-account keys plus multi-account keys), and the three runner entry points (`pnpm qa:e2e` self-check, `pnpm openclaw qa suite` scenario suite, and the `pnpm qa:lab:up` Docker-backed QA Lab debugger).

## What it does

`qa-channel` is a bundled synthetic message transport for automated OpenClaw QA. It is not a production channel — it exists to exercise the same channel plugin boundary used by real transports while keeping state deterministic and fully inspectable. Concretely, the channel provides:

- A **Slack-class target grammar** with four target forms: `dm:<user>`, `channel:<room>`, `group:<room>`, and `thread:<room>/<thread>`.
- Shared `channel:` and `group:` conversations are surfaced to agents as group/channel **room turns**, so they exercise the same visible-reply and message-tool routing policy used by Discord, Slack, Telegram, and similar transports.
- An **HTTP-backed synthetic bus** for inbound message injection, outbound transcript capture, thread creation, reactions, edits, deletes, and search/read actions.
- A **host-side self-check runner** that writes a Markdown report to `.artifacts/qa-e2e/`.

## Config

The channel is configured under `channels.qa-channel`. A minimal config:

```json
{
  "channels": {
    "qa-channel": {
      "baseUrl": "http://127.0.0.1:43123",
      "botUserId": "openclaw",
      "botDisplayName": "OpenClaw QA",
      "allowFrom": ["*"],
      "pollTimeoutMs": 1000
    }
  }
}
```

**Account keys** (per the source's verbatim descriptions):

- `enabled` — master toggle for this account.
- `name` — optional display label.
- `baseUrl` — synthetic bus URL.
- `botUserId` — Matrix-style bot user id used in target grammar.
- `botDisplayName` — display name for outbound messages.
- `pollTimeoutMs` — long-poll wait window. Integer between 100 and 30000.
- `allowFrom` — sender allowlist (user ids or `"*"`). Direct messages and allowlisted group policy both use these synthetic sender ids.
- `groupPolicy` — shared-room policy: `"open"` (default), `"allowlist"`, or `"disabled"`.
- `groupAllowFrom` — optional shared-room sender allowlist. When omitted under `"allowlist"`, QA Channel falls back to `allowFrom`.
- `groups.<room>.requireMention` — require a bot mention before replying in a specific group/channel room. `groups."*"` sets the default.
- `defaultTo` — fallback target when none is supplied.
- `actions.messages` / `actions.reactions` / `actions.search` / `actions.threads` — per-action tool gating.

**Multi-account keys at the top level:**

- `accounts` — record of named per-account overrides keyed by account id.
- `defaultAccount` — preferred account id when multiple are configured.

## Runners

The channel ships with three runner entry points spanning a fast host-side self-check, a full scenario suite, and a Docker-backed debugger UI.

The **host-side self-check** writes a Markdown report under `.artifacts/qa-e2e/`:

```bash
pnpm qa:e2e
```

This routes through `qa-lab`, starts the in-repo QA bus, boots the bundled `qa-channel` runtime slice, and runs a deterministic self-check.

The **full repo-backed scenario suite** runs scenarios in parallel against the QA gateway lane:

```bash
pnpm openclaw qa suite
```

See the QA overview page for scenarios, profiles, and provider modes (linked under References).

The **Docker-backed QA site** (gateway + QA Lab debugger UI in one stack):

```bash
pnpm qa:lab:up
```

This builds the QA site, starts the Docker-backed gateway + QA Lab stack, and prints the QA Lab URL. From there you can pick scenarios, choose the model lane, launch individual runs, and watch results live. The QA Lab debugger is separate from the shipped Control UI bundle.

**Source**: OpenClaw documentation — `channels/qa-channel` (mirror `inbox/openclaw_docs/channels/qa-channel.md`)
**Last Updated**: 2026-06-22
**Status**: Active
