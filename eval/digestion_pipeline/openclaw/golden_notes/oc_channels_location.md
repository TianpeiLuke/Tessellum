---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - location
keywords:
  - openclaw channel location parsing
  - inbound shared location normalization
  - location ctx fields
  - geo_uri matrix location
  - telegram whatsapp matrix location
  - untrusted metadata json block
  - locationsource pin place live
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/channels/location
access_control_group: ["general"]
---

# OpenClaw — Inbound Channel Location Parsing

## Overview

This note models how OpenClaw normalizes shared locations received from chat channels into agent-readable context, mirroring the `channels/location` source page. A shared location is rendered two ways: as terse coordinate text appended to the inbound message body, and as structured `Location*` fields in the auto-reply context (`ctx`) payload. Channel-provided free text — labels, addresses, and captions/comments — is NOT inlined in the user body; instead it is rendered into the prompt through the shared **untrusted metadata** JSON block, the same bounded path used for other untrusted channel context. Three channels are supported today: **Telegram** (location pins, venues, and live locations), **WhatsApp** (`locationMessage` + `liveLocationMessage`), and **Matrix** (`m.location` with `geo_uri`).

## Text Formatting

Locations are rendered as friendly single lines without brackets and appended to the inbound body. The source documents three rendered forms (a plain pin and a named place both render the same coordinate line, while a live share is prefixed differently):

- Pin: `📍 48.858844, 2.294351 ±12m`
- Named place: `📍 48.858844, 2.294351 ±12m`
- Live share: `🛰 Live location: 48.858844, 2.294351 ±12m`

If the channel includes a label, address, or caption/comment, that text is preserved in the context payload (not the body) and appears in the prompt as a fenced **untrusted metadata** JSON block, prefixed by the literal line `Location (untrusted metadata):`. The JSON object carries the coordinates plus the channel-supplied free text:

```json
{
  "latitude": 48.858844,
  "longitude": 2.294351,
  "name": "Eiffel Tower",
  "address": "Champ de Mars, Paris",
  "caption": "Meet here"
}
```

## Context Fields

When a location is present, OpenClaw adds the following fields to `ctx`. Coordinate and source fields are always set when a location exists; the name/address/accuracy/caption fields are optional and present only when the channel supplied them:

- `LocationLat` (number)
- `LocationLon` (number)
- `LocationAccuracy` (number, meters; optional)
- `LocationName` (string; optional)
- `LocationAddress` (string; optional)
- `LocationSource` (`pin | place | live`)
- `LocationIsLive` (boolean)
- `LocationCaption` (string; optional)

The prompt renderer treats `LocationName`, `LocationAddress`, and `LocationCaption` as untrusted metadata and serializes them through the same bounded JSON path used for other channel context, keeping channel-controlled free text out of the trusted user-body text.

## Channel Notes

Per-channel mapping of the upstream message shape onto the normalized fields:

- **Telegram**: venues map to `LocationName` / `LocationAddress`; live locations use `live_period`.
- **WhatsApp**: `locationMessage.comment` and `liveLocationMessage.caption` populate `LocationCaption`.
- **Matrix**: `geo_uri` is parsed as a pin location; altitude is ignored and `LocationIsLive` is always `false`.

**Source**: OpenClaw documentation — `channels/location` (mirror `inbox/openclaw_docs/channels/location.md`)
**Last Updated**: 2026-06-22
**Status**: Active
