---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - microsoft
keywords:
  - openclaw microsoft speech plugin
  - microsoft-speech text-to-speech
  - speechProviders contract
  - azure tts provider plugin
  - bundled openclaw plugin
  - openclaw plugin reference card
  - microsoft-speech distribution surface
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/microsoft
access_control_group: ["general"]
---

# OpenClaw — Microsoft (Azure) Text-to-Speech Plugin Reference Card

## Overview

This note is the plugin-reference card for OpenClaw's **Microsoft plugin** — the first-party package that "Adds text-to-speech provider support." It mirrors the `plugins/reference/microsoft` source page, which is a thin reference-card stub carrying two sections: `## Distribution` (the package name and install route) and `## Surface` (the declared contract). The card documents the package identifier `@openclaw/microsoft-speech`, its bundled install route ("included in OpenClaw"), and its single contract surface `speechProviders`. It is the Microsoft-vendor TTS counterpart to — and is kept deliberately distinct from — the Microsoft Foundry model/image provider card ([oc_plugins_reference_microsoft_foundry](oc_plugins_reference_microsoft_foundry.md)): same vendor (Microsoft / Azure), different capability family (speech vs model/image). Per the pl14 reference-card schema, every plugin is an `@openclaw/<name>` package with a distribution + install route and a declared contract surface; the cross-cutting abstraction of that schema lives in [oc_plugins_reference_overview](oc_plugins_reference_overview.md).

## Distribution

The package and install route, copied verbatim from the source card:

- **Package**: `@openclaw/microsoft-speech`
- **Install route**: included in OpenClaw

The plugin is therefore **bundled** — it ships with OpenClaw and requires no separate npm or ClawHub install step to be available. (The package identifier `@openclaw/microsoft-speech` is the scoped npm name; the human-facing page title is "Microsoft plugin." No version, dependency, or configuration detail beyond these two fields is specified in source.)

## Surface

The card declares exactly one contract surface, verbatim:

```
contracts: speechProviders
```

This means the plugin contributes to OpenClaw's `speechProviders` contract — it registers a text-to-speech (TTS) provider. The `speechProviders` surface is one of the plugin contract-surface types enumerated across the pl14 cards (alongside `tools`, `skills`, `providers`, `imageGenerationProviders`, and `migrationProviders`); see [oc_plugins_reference_overview](oc_plugins_reference_overview.md) for that vocabulary. The plugin's sole documented capability — "Adds text-to-speech provider support." — maps directly to this single declared surface: a registered TTS provider that OpenClaw's voice/speech layer can select to synthesize audio from text. The source card does not enumerate concrete voices, languages, Azure region/endpoint settings, an STT (speech-to-text) surface, credentials, or configuration keys; those are *(not specified in source)* on this reference page.

## Position in the Plugin Family

Within pl14, this card sits beside two other Microsoft-vendor and family cards. It is distinct from the Foundry card because the contract surface differs: Foundry declares `providers` + `imageGenerationProviders` (model and image generation), whereas this plugin declares only `speechProviders` (audio output). As a `speechProviders` contributor it is a peer of OpenClaw's other bundled/registered TTS providers in the voice/speech extension layer, and its output is downstream-consumed by OpenClaw's voice channels. The remaining family cards — [oc_plugins_reference_memory](oc_plugins_reference_memory.md) (memory plugins) and [oc_plugins_reference_migration](oc_plugins_reference_migration.md) (migration plugins) — share the identical `## Distribution` / `## Surface` card schema this page follows.

**Source**: OpenClaw documentation — `plugins/reference/microsoft` (mirror `inbox/openclaw_docs/plugins/reference/microsoft.md`)
**Last Updated**: 2026-06-22
**Status**: Active
