---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw channel plugins
  - msteams plugin
  - nextcloud-talk plugin
  - nostr plugin
  - channels surface
  - clawhub install route
  - nip-04 encrypted dms
  - chat-channel plugin manifest
topics:
  - OpenClaw
  - Channel Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/msteams
access_control_group: ["general"]
---

# OpenClaw — Built-in Chat-Channel Plugins Reference Catalog

## Overview

This note is the catalog/index entry for OpenClaw's three built-in chat-channel plugins — **Microsoft Teams** (`msteams`), **Nextcloud Talk** (`nextcloud-talk`), and **Nostr** (`nostr`) — consolidating the per-plugin reference manifest stubs at `plugins/reference/msteams`, `plugins/reference/nextcloud-talk`, and `plugins/reference/nostr`. Each source page is a thin, machine-generated manifest with the identical three-H2 skeleton — `## Distribution` (npm package + install route), `## Surface` (the `channels:` identifier the plugin registers), and `## Related docs` (one pointer to the per-channel setup how-to) — preceded by a one-sentence H1 summary. This catalog records the unique-per-plugin facts (package name, install route, registered channel identifier, and what each channel covers) and links out to the substantive `/channels/<name>` setup pages rather than duplicating their content.

## Catalog Summary

The table below reproduces the three manifest stubs verbatim — npm package, install route, the `channels:` identifier each plugin registers, and the one-sentence summary of what the channel covers.

| Plugin | npm package | Install route | `channels:` identifier | Channel covers | Related docs pointer |
|--------|-------------|---------------|------------------------|----------------|----------------------|
| Microsoft Teams | `@openclaw/msteams` | npm; ClawHub | `msteams` | Bot conversations | `/channels/msteams` |
| Nextcloud Talk | `@openclaw/nextcloud-talk` | npm; ClawHub | `nextcloud-talk` | Conversations | `/channels/nextcloud-talk` |
| Nostr | `@openclaw/nostr` | npm; ClawHub | `nostr` | NIP-04 encrypted direct messages | `/channels/nostr` |

All three plugins share the same install route, stated verbatim in their `## Distribution` H2 as `npm; ClawHub` — meaning each is distributed as a published npm package under the `@openclaw/` scope and is also available through ClawHub (OpenClaw's plugin registry), rather than being bundled "included in OpenClaw" the way the model/media provider plugins are. Each plugin registers exactly one platform identifier under its `## Surface` H2 `channels:` list, which is the value an operator references to enable that channel in the gateway configuration.

## Microsoft Teams (`msteams`)

The `@openclaw/msteams` plugin is the "OpenClaw Microsoft Teams channel plugin for bot conversations." Its `## Surface` registers `channels: msteams`, exposing OpenClaw as a Teams bot that participates in bot conversations. The manifest's `## Related docs` H2 points to `/channels/msteams` for the substantive setup/configuration how-to (owned by the channels series), which is linked-not-duplicated here.

## Nextcloud Talk (`nextcloud-talk`)

The `@openclaw/nextcloud-talk` plugin is the "OpenClaw Nextcloud Talk channel plugin for conversations." Its `## Surface` registers `channels: nextcloud-talk`, exposing OpenClaw inside Nextcloud Talk conversations. The manifest's `## Related docs` H2 points to `/channels/nextcloud-talk` for the per-channel setup how-to.

## Nostr (`nostr`)

The `@openclaw/nostr` plugin is the "OpenClaw Nostr channel plugin for NIP-04 encrypted direct messages." Its `## Surface` registers `channels: nostr`. NIP-04 is the Nostr protocol specification for encrypted direct messages, so this channel carries OpenClaw conversations as encrypted DMs over Nostr. The manifest's `## Related docs` H2 points to `/channels/nostr` for the per-channel setup how-to.

**Source**: OpenClaw documentation — `plugins/reference/{msteams,nextcloud-talk,nostr}` (mirror `inbox/openclaw_docs/plugins/reference/`)
**Last Updated**: 2026-06-22
**Status**: Active
