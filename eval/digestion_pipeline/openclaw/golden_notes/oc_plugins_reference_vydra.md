---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw vydra plugin
  - vydra model provider
  - "@openclaw/vydra-provider"
  - imagegenerationproviders contract
  - speechproviders contract
  - videogenerationproviders contract
  - bundled provider plugin
  - vydra distribution surface
topics:
  - OpenClaw
  - Plugin Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/vydra
access_control_group: ["general"]
---

# OpenClaw — Vydra Provider Plugin (Reference)

## Overview

This note is the reference data sheet for the OpenClaw **Vydra plugin**, mirroring the `plugins/reference/vydra` source page. Per that page's `summary`, the plugin "Adds Vydra model provider support to OpenClaw," and its `read_when` cue scopes it to "installing, configuring, or auditing the vydra plugin." Vydra is a **model-provider plugin**: it registers the `vydra` provider and contributes three generative-media contracts — `imageGenerationProviders`, `speechProviders`, and `videoGenerationProviders` — to OpenClaw's provider layer. The two load-bearing facts are the **Distribution** (npm package id + install route) and the **Surface** (the provider id and the contracts it registers); the page's `## Related docs` pointer links the full `/providers/vydra` provider doc, which carries provider-level configuration that this reference does not duplicate.

## Distribution

- **Package:** `@openclaw/vydra-provider`
- **Install route:** included in OpenClaw

The plugin is a **bundled** plugin — "included in OpenClaw" means it ships with the gateway distribution rather than requiring a separate ClawHub or npm install. Operators do not add it as an external dependency; it is present in the default install and is enabled/configured through OpenClaw's provider configuration rather than a package fetch.

## Surface

The plugin's registered surface is, verbatim from source: `providers: vydra; contracts: imageGenerationProviders, speechProviders, videoGenerationProviders`.

- **providers:** `vydra` — the single provider id this plugin adds to OpenClaw's model/provider catalog.
- **contracts (3):**
  - `imageGenerationProviders` — registers Vydra as an image-generation backend the agent can call to synthesize images.
  - `speechProviders` — registers Vydra as a speech (text-to-speech / voice) provider.
  - `videoGenerationProviders` — registers Vydra as a video-generation backend.

These three contracts make Vydra a multimodal generative-media provider (image + speech + video) plugged in behind OpenClaw's provider abstraction. The contract identifiers are OpenClaw plugin-surface vocabulary, not separate term notes; their consumer-side wiring (image/video/speech dispatch) lives in the linked snippets and the sibling-stack provider docs, not in this reference.

**Source**: OpenClaw documentation — `plugins/reference/vydra` (mirror `inbox/openclaw_docs/plugins/reference/vydra.md`)
**Last Updated**: 2026-06-22
**Status**: Active
