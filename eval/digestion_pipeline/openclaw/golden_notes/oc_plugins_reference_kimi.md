---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw kimi plugin
  - kimi provider
  - kimi-coding provider
  - openclaw kimi-provider npm
  - clawhub kimi-provider
  - moonshot provider docs
  - openclaw model provider plugin
  - dual provider surface
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/kimi
access_control_group: ["general"]
---

# OpenClaw — Kimi Plugin Reference Card

## Overview

This note is the procedure for identifying, installing, and auditing the OpenClaw **Kimi plugin** — the catalog reference card at the `plugins/reference/kimi` source page. The card declares that the plugin "Adds Kimi, Kimi Coding model provider support to OpenClaw." It ships as the npm package `@openclaw/kimi-provider`, installs via npm or ClawHub, and contributes a **dual model-provider surface** — `providers: kimi, kimi-coding` — so a single plugin registers two selectable provider entries. It is the thin catalog layer above the deeper provider config page, which (uniquely among these cards) routes to `/providers/moonshot` rather than a `/providers/kimi` slug, reflecting that Kimi is Moonshot AI's model family. This note reproduces the three card sections (Distribution, Surface, Related docs) verbatim and links the deeper provider/channel pages and code-side implementations rather than re-documenting them.

## Distribution

The card's **Distribution** section lists how the plugin is packaged and obtained, verbatim from source:

- Package: `@openclaw/kimi-provider`
- Install route: npm; ClawHub: `clawhub:@openclaw/kimi-provider`

Unlike the bundled provider cards (e.g. Hugging Face), this plugin is NOT "included in OpenClaw" — it is acquired through an explicit install route. It can be installed from the public npm registry as `@openclaw/kimi-provider`, or through ClawHub using the identifier `clawhub:@openclaw/kimi-provider`. To audit whether the plugin is present, check for the `@openclaw/kimi-provider` package among OpenClaw's installed/loaded plugins; its presence is what makes the `kimi` and `kimi-coding` provider surfaces available. No version pin, configuration key, or environment variable is stated on the card itself — those deeper provider-config details live on the Related-docs target, not in this catalog entry.

## Surface

The **Surface** section names the OpenClaw extension surface this plugin contributes, verbatim from source:

```
providers: kimi, kimi-coding
```

This is a **model-provider surface**, and it is a dual surface: the single `@openclaw/kimi-provider` plugin registers two provider entries — `kimi` and `kimi-coding`. The `kimi` entry exposes the general Kimi model family for inference into OpenClaw's agent loop, while the `kimi-coding` entry exposes a coding-focused provider variant. Once the plugin is installed and loaded, both `kimi` and `kimi-coding` become valid provider identifiers that the model/provider routing layer can select. This dual-surface registration is the distinguishing feature of the Kimi card versus the single-surface provider cards (huggingface declares `providers: huggingface`; kilocode declares `providers: kilocode`).

**Source**: OpenClaw documentation — `plugins/reference/kimi` (mirror `inbox/openclaw_docs/plugins/reference/kimi.md`)
**Last Updated**: 2026-06-22
**Status**: Active
