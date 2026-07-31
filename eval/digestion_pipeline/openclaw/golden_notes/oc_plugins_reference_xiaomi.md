---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw xiaomi plugin
  - xiaomi-provider package
  - xiaomi token plan provider
  - speechProviders contract
  - bundled provider plugin
  - xiaomi model provider
  - openclaw provider reference
topics:
  - OpenClaw
  - Plugin Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/xiaomi
access_control_group: ["general"]
---

# OpenClaw — Xiaomi Provider Plugin Reference

## Overview

This note is the reference data sheet for the OpenClaw **Xiaomi** plugin, mirroring the `plugins/reference/xiaomi` source page. Per the source `summary`, the plugin "Adds Xiaomi, Xiaomi Token Plan model provider support to OpenClaw." It is a bundled model-provider plugin you would read about when installing, configuring, or auditing the `xiaomi` plugin (the page's `read_when` cue). The page is a one-screen plugin data sheet with three blocks — Distribution (the npm package and how it ships), Surface (the provider ids and contracts the plugin registers), and Related docs (the link-out to the full provider page) — each captured verbatim below. The full provider configuration (auth env vars, base URLs, default models, onboarding flags) lives in the `/providers/xiaomi` doc this reference points at, not here.

## Distribution

- Package: `@openclaw/xiaomi-provider`
- Install route: included in OpenClaw

The package ships as part of OpenClaw (a bundled plugin), so there is no separate ClawHub or npm install step for this provider plugin.

## Surface

The plugin's registered surface, verbatim from the source page, is: `providers: xiaomi, xiaomi-token-plan; contracts: speechProviders`.

The plugin therefore exposes **two provider ids** — `xiaomi` and `xiaomi-token-plan` — and registers into the **`speechProviders`** contract (OpenClaw's text-to-speech / speech provider surface). The `xiaomi-token-plan` id is the Token Plan variant of the same provider. Both provider ids and the `speechProviders` contract are OpenClaw configuration identifiers, not separate term notes.

**Source**: OpenClaw documentation — `plugins/reference/xiaomi` (mirror `inbox/openclaw_docs/plugins/reference/xiaomi.md`)
**Last Updated**: 2026-06-22
**Status**: Active
