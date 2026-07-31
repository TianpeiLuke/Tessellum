---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - clawbot
keywords:
  - openclaw clawbot
  - clawbot legacy alias namespace
  - clawbot qr alias
  - openclaw clawbot qr
  - backward compatibility cli alias
  - openclaw cli migration
  - legacy command alias
topics:
  - OpenClaw
  - CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/clawbot
access_control_group: ["general"]
---

# OpenClaw — `openclaw clawbot` Legacy Alias Namespace

## Overview

This note documents the `openclaw clawbot` command — a legacy alias namespace kept for backwards compatibility — and its migration guidance to modern top-level commands, mirroring the full `cli/clawbot` source page. The page is relevant to operators who maintain older scripts that still invoke `openclaw clawbot ...` and who need to know which aliases still work and how to move to the current commands.

## `openclaw clawbot`

`openclaw clawbot` is a legacy alias namespace kept for backwards compatibility. The single current supported alias is `openclaw clawbot qr`, which has the same behavior as `openclaw qr`. No other subcommands are documented under this namespace in the source.

## Migration

The source advises preferring modern top-level commands directly. The one documented mapping is:

- `openclaw clawbot qr` → `openclaw qr`

No deprecation timeline, removal date, or additional aliases are specified in source.

**Source**: OpenClaw documentation — `cli/clawbot` (mirror `inbox/openclaw_docs/cli/clawbot.md`)
**Last Updated**: 2026-06-22
**Status**: Active
