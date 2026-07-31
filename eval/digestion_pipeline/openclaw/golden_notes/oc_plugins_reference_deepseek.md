---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw deepseek plugin
  - deepseek provider
  - "@openclaw/deepseek-provider"
  - clawhub deepseek provider
  - deepseek model provider
  - openclaw provider plugin
  - deepseek npm install
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/deepseek
access_control_group: ["general"]
---

# OpenClaw — DeepSeek Plugin Reference Card

## Overview

This note is the reference card for the OpenClaw **DeepSeek plugin** — the packaged extension that "Adds DeepSeek model provider support to OpenClaw." It mirrors the `plugins/reference/deepseek` source page, capturing the two load-bearing facts that the machine-generated catalog stub declares: the plugin's **Distribution** (package id `@openclaw/deepseek-provider` plus its install routes) and its **Surface** (the runtime contribution — it registers the `deepseek` model provider). The card is a registry descriptor for one distributable plugin unit; the runtime configuration of the provider itself (env vars, model list, auth) lives on the separate `/providers/deepseek` config page, which is owned by another sub-plan and linked, not duplicated here.

## Distribution

The plugin's distribution facts, reproduced verbatim from the source page:

- Package: `@openclaw/deepseek-provider`
- Install route: npm; ClawHub: `clawhub:@openclaw/deepseek-provider`

The plugin is published to the npm registry and is also available through ClawHub under the identifier `clawhub:@openclaw/deepseek-provider`. Unlike bundled plugins that ship "included in OpenClaw," this is an externally installed plugin pulled in via npm or the ClawHub distribution route.

## Surface

The Surface line declares what the plugin contributes to the OpenClaw runtime when loaded:

```
providers: deepseek
```

The plugin registers a single model **provider** with the id `deepseek`. It contributes no capability contracts (such as `imageGenerationProviders`, `mediaUnderstandingProviders`, `memoryEmbeddingProviders`, `speechProviders`, or `realtimeTranscriptionProviders`) — its sole surface is the `deepseek` model provider, which exposes DeepSeek's chat/reasoning language models to OpenClaw agents. The provider configuration details (model catalog entries, API key, endpoint) are documented on the upstream `/providers/deepseek` page, not in this catalog stub.

**Source**: OpenClaw documentation — `plugins/reference/deepseek` (mirror `inbox/openclaw_docs/plugins/reference/deepseek.md`)
**Last Updated**: 2026-06-22
**Status**: Active
