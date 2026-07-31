---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - skills
keywords:
  - openclaw macos skills settings
  - skills.status gateway eligibility
  - skills.install installer selection
  - metadata.openclaw.requires
  - metadata.openclaw.install
  - security.installPolicy gating
  - skills.entries openclaw.json
  - skills.update apikey env
  - remote mode skill install
topics:
  - OpenClaw
  - macOS Skills Settings
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/platforms/mac/skills
access_control_group: ["general"]
---

# OpenClaw — macOS App Skills Settings (Gateway-Backed)

## Overview

This note explains how the macOS OpenClaw app surfaces OpenClaw **skills** through the gateway rather than evaluating them locally — mirroring the `platforms/mac/skills` source page. The page's central design fact is that the macOS app **does not parse skills locally**: it asks the gateway for skill status, eligibility, and missing requirements, and delegates installer execution to the gateway host. It covers the four source sections — the `skills.status` data source and where requirements come from, the `skills.install` install-action flow and its preferred-installer selection, env/API-key storage in `openclaw.json`, and how install/config behaves in remote mode.

## Data Source — `skills.status`

The macOS app's Skills settings UI is populated from the gateway, not from any local skill parsing. The gateway RPC `skills.status` returns all skills plus their **eligibility** and **missing requirements**, including allowlist blocks for bundled skills. Each skill's requirements are derived from the `metadata.openclaw.requires` field in that skill's `SKILL.md`. Because eligibility and requirement resolution live on the gateway, the app simply displays what `skills.status` reports rather than independently inspecting the skill manifests.

## Install Actions — `skills.install` and Installer Selection

Install options for a skill come from the `metadata.openclaw.install` field in its `SKILL.md`, which can declare installers from the set **brew / node / go / uv**. To install, the app calls the gateway RPC `skills.install`, which runs the installers on the gateway host (not on the local Mac). Two gating and selection rules govern this flow:

- **Install-policy gating:** the operator-owned `security.installPolicy` can block gateway-backed skill installs *before* installer metadata runs. The source page notes that install-time built-in dangerous-code blocking is **not** part of the skill install flow — that protection is a separate layer.
- **Installer selection:** if *every* install option is `download`, the gateway surfaces all download choices to the user. Otherwise, the gateway picks **one** preferred installer using the current install preferences and the host's available binaries, in this order: **Homebrew first** when `skills.install.preferBrew` is enabled and `brew` exists, then `uv`, then the configured node manager from `skills.install.nodeManager`, then later fallbacks like `go` or `download`. Node install labels reflect the configured node manager, including `yarn`.

## Env / API Keys — `skills.entries` in `openclaw.json`

The app persists per-skill configuration into the OpenClaw config file at `~/.openclaw/openclaw.json`, under `skills.entries.<skillKey>`. The gateway RPC `skills.update` patches three fields for a skill entry: `enabled`, `apiKey`, and `env`. This is how an operator turns a skill on or off and supplies the credentials/environment a skill needs without editing the manifest itself.

## Remote Mode

When the macOS app is driving a gateway on another host (remote mode), both **install and config updates happen on the gateway host, not on the local Mac**. The `skills.install` installer run and the `skills.update` config patch are executed where the gateway lives, consistent with the gateway-backed model used everywhere on this page.

**Source**: OpenClaw documentation — `platforms/mac/skills` (mirror `inbox/openclaw_docs/platforms/mac/skills.md`)
**Last Updated**: 2026-06-22
**Status**: Active
