---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw alibaba plugin
  - alibaba-provider
  - video generation provider
  - videoGenerationProviders contract
  - plugin reference descriptor
  - included in openclaw
  - openclaw provider plugin
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/alibaba
access_control_group: ["general"]
---

# OpenClaw — Alibaba Plugin (Reference Catalog Entry)

## Overview

This note is the generated plugin-reference descriptor for the OpenClaw **Alibaba plugin**, mirroring the `plugins/reference/alibaba` source page. It is a catalog stub — one of the per-plugin reference pages emitted from `extensions/*/package.json` + `openclaw.plugin.json` — and records three load-bearing facts: what the plugin adds (video generation provider support), its **Distribution** (npm package id + install route), and its **Surface** (the contract it registers into the runtime). The plugin's one-line summary, verbatim from source, is: "Adds video generation provider support." The fuller provider documentation lives at the `/providers/alibaba` page (linked under References and in Related Notes); this entry is the identity-and-contract descriptor, not a configuration or setup guide.

## Distribution

- Package: `@openclaw/alibaba-provider`
- Install route: included in OpenClaw

The plugin ships as the npm package `@openclaw/alibaba-provider` and is **included in OpenClaw** — i.e., bundled with the distribution rather than installed separately via npm / ClawHub. No additional install or configuration steps are stated on this page.

## Surface

contracts: videoGenerationProviders

The plugin's Surface — what it exposes into the agent runtime — is a single contract registration: `videoGenerationProviders`. By registering this contract, the Alibaba plugin makes a video-generation provider available to OpenClaw's media-generation tooling. The page declares no additional `providers:` or `skills:` Surface entries; the video-generation provider contract is its sole documented registration.

**Source**: OpenClaw documentation — `plugins/reference/alibaba` (mirror `inbox/openclaw_docs/plugins/reference/alibaba.md`)
**Last Updated**: 2026-06-22
**Status**: Active
