---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - timezone
keywords:
  - openclaw timezone
  - three timezone surfaces
  - userTimezone envelopeTimezone
  - envelope timestamp prefix
  - system prompt current date time block
  - prompt cache stability timezone
  - iana timezone override
  - timeFormat 12 24 auto
topics:
  - OpenClaw
  - Timezone
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/timezone
access_control_group: ["general"]
---

# OpenClaw — Timezone Surfaces and Configuration

## Overview

This note covers OpenClaw's **timezone model**: how the runtime standardizes timestamps so the model sees a single reference time instead of a mix of provider-local clocks, where timezones surface (message envelopes, tool payloads, and the system prompt), how the operator sets the user timezone, and when to override the defaults. It mirrors the `concepts/timezone` source page. The page deliberately keeps the system prompt's time block stable for prompt caching and defers the full per-provider reference to the separate Date & Time page.

## Three Timezone Surfaces

OpenClaw standardizes timestamps so the model sees a **single reference time** instead of a mix of provider-local clocks. There are three surfaces where timezones show up, each with its own purpose:

| Surface | What it shows | Default | Configured via |
| --- | --- | --- | --- |
| Message envelopes | Wraps inbound channel messages: `[Signal +1555 Sun 2026-01-18 00:19:42 PST] hello` | Host-local | `agents.defaults.envelopeTimezone` |
| Tool payloads | Channel `readMessages`-style tools return raw provider time + normalized `timestampMs` / `timestampUtc` | UTC fields always present | Not configurable — preserves provider-native timestamps |
| System prompt | A small `Current Date & Time` block with the **time zone only** (no clock value, for cache stability) | Host timezone if `userTimezone` unset | `agents.defaults.userTimezone` |

The system prompt deliberately omits the live clock to keep prompt caching stable across turns. When the agent needs the current time, it calls `session_status`.

## Setting the User Timezone

The user timezone is set through `agents.defaults.userTimezone` (an IANA zone string) in the OpenClaw config:

```json5
{
  agents: {
    defaults: {
      userTimezone: "America/Chicago",
    },
  },
}
```

If `userTimezone` is unset, OpenClaw resolves the host timezone at runtime (no config write). `agents.defaults.timeFormat` (`auto` | `12` | `24`) controls 12h/24h rendering in envelopes and downstream surfaces, not in the system prompt section.

## When to Override

The defaults work for a single-host, single-user setup; the page calls out three override situations:

- **Use UTC envelopes** (`envelopeTimezone: "utc"`) when you want stable timestamps across hosts in different regions, or when you want UTC-aligned logs to match diagnostics output.
- **Use a fixed IANA zone** (e.g. `"Europe/Vienna"`) when the gateway host is in one zone but the user is in another and you want envelopes to read in the user's zone regardless of host migration.
- **Set `envelopeTimestamp: "off"`** when timestamp context is not useful for the conversation. This removes absolute timestamps from envelopes, direct agent prompt prefixes, and embedded model-input prefixes.

For the full behavior reference, examples per provider, and elapsed-time formatting, the page links out to the Date & Time page.

**Source**: OpenClaw documentation — `concepts/timezone` (mirror `inbox/openclaw_docs/concepts/timezone.md`)
**Last Updated**: 2026-06-22
**Status**: Active
