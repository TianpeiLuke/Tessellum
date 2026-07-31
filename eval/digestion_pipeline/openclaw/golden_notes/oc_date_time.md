---
tags:
  - resource
  - documentation
  - openclaw
  - top_level
  - date_time
keywords:
  - openclaw date and time handling
  - host-local envelope timestamp
  - envelopetimezone envelopetimestamp envelopeelapsed
  - usertimezone timeformat config
  - current date and time system prompt
  - session_status current time
  - timestampms timestamputc normalized fields
  - time format auto detection
topics:
  - OpenClaw
  - Date and Time
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/date-time
access_control_group: ["general"]
---

# OpenClaw — Date and Time Handling

## Overview

This note documents how OpenClaw handles dates and times across message envelopes, the system prompt, system event lines, tool payloads, and channel connectors, mirroring the `date-time` source page. The governing default is **host-local time for transport timestamps** and **user timezone only in the system prompt**; provider timestamps are preserved so tools keep their native semantics, and the current time is available to the agent via the `session_status` tool. This is a procedure note: it enumerates the configuration keys (`envelopeTimezone`, `envelopeTimestamp`, `envelopeElapsed`, `userTimezone`, `timeFormat`), their accepted values and effects, auto time-format detection, and the raw-plus-normalized time fields (`timestampMs` / `timestampUtc`) that channel tools return.

## Message Envelopes (Local by Default)

Inbound messages are wrapped with a timestamp at second precision. The envelope renders as a bracketed prefix carrying the provider, address, and timestamp ahead of the message text:

```
[Provider ... Mon 2026-01-05 16:26:34 PST] message text
```

This envelope timestamp is **host-local by default, regardless of the provider timezone**. The behavior is overridden through `agents.defaults`:

```json5
{
  agents: {
    defaults: {
      envelopeTimezone: "local", // "utc" | "local" | "user" | IANA timezone
      envelopeTimestamp: "on", // "on" | "off"
      envelopeElapsed: "on", // "on" | "off"
    },
  },
}
```

The `envelopeTimezone` accepted values behave as follows: `"utc"` uses UTC; `"local"` uses the host timezone; `"user"` uses `agents.defaults.userTimezone` (falling back to the host timezone); and an explicit IANA timezone (e.g., `"America/Chicago"`) pins a fixed zone. Setting `envelopeTimestamp: "off"` removes absolute timestamps from envelope headers, direct agent prompt prefixes, and embedded model-input prefixes. Setting `envelopeElapsed: "off"` removes elapsed-time suffixes (the `+2m` style).

### Examples

The source shows three rendered envelope forms. The **local (default)** form, the **user timezone** form (note the `CST` zone in place of `PST`), and the **elapsed time enabled** form (note the `+30s` elapsed suffix and the `Z` UTC marker):

```
[WhatsApp +1555 Sun 2026-01-18 00:19:42 PST] hello
[WhatsApp +1555 Sun 2026-01-18 00:19:42 CST] hello
[WhatsApp +1555 +30s Sun 2026-01-18T05:19:00Z] follow-up
```

## System Prompt: Current Date and Time

If the user timezone is known, the system prompt includes a dedicated **Current Date & Time** section that carries the **time zone only** — no clock or time format — specifically to keep prompt caching stable. The injected line is just the zone:

```
Time zone: America/Chicago
```

When the agent needs the actual current time, it uses the `session_status` tool; the status card includes a timestamp line. Omitting the clock from the cached system-prompt prefix is the deliberate design choice that prevents a constantly-changing time value from invalidating the prompt cache on every turn.

## System Event Lines (Local by Default)

Queued system events that are inserted into the agent context are prefixed with a timestamp using the **same timezone selection as message envelopes** (default: host-local). A model-switch event, for example, renders as:

```
System: [2026-01-12 12:19:17 PST] Model switched.
```

### Configure User Timezone and Format

The user-facing prompt timezone and the displayed time format are set together under `agents.defaults`:

```json5
{
  agents: {
    defaults: {
      userTimezone: "America/Chicago",
      timeFormat: "auto", // auto | 12 | 24
    },
  },
}
```

Here `userTimezone` sets the **user-local timezone** for prompt context, and `timeFormat` controls **12h/24h display** in the prompt, where `auto` follows OS preferences. The accepted `timeFormat` values are `auto`, `12`, and `24`.

## Time Format Detection (Auto)

When `timeFormat: "auto"`, OpenClaw inspects the OS preference (macOS/Windows) and falls back to locale formatting when no OS preference resolves. The detected value is **cached per process** to avoid repeated system calls within a running gateway.

## Tool Payloads and Connectors (Raw Provider Time + Normalized Fields)

Channel tools return **provider-native timestamps** and additionally attach normalized fields for consistency across providers. The two normalized fields are `timestampMs` (epoch milliseconds, UTC) and `timestampUtc` (ISO 8601 UTC string). Raw provider fields are preserved so that nothing is lost in normalization. The provider-native time formats vary by connector: Slack returns epoch-like strings from the API, Discord returns UTC ISO timestamps, and Telegram/WhatsApp return provider-specific numeric or ISO timestamps. If local time is needed, the source instructs callers to convert it downstream using the known timezone, rather than expecting OpenClaw to localize the tool payload itself.

**Source**: OpenClaw documentation — `date-time` (mirror `inbox/openclaw_docs/date-time.md`)
**Last Updated**: 2026-06-22
**Status**: Active
