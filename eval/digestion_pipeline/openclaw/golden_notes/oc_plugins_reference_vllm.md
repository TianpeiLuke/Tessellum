---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw vllm plugin
  - vllm provider plugin
  - openclaw vllm-provider package
  - providers vllm surface
  - self-hosted inference server provider
  - bundled openclaw provider plugin
  - openai-compatible inference endpoint
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/vllm
access_control_group: ["general"]
---

# OpenClaw — vLLM Provider Plugin (`@openclaw/vllm-provider`)

## Overview

This note is the plugin-descriptor card for the OpenClaw **vLLM plugin**, mirroring the `plugins/reference/vllm` source page. The card states the plugin's identity (npm package + install route) and the contract surface it registers — nothing more: the source page describes it as "Adds vLLM model provider support to OpenClaw." It is one of the uniform plugin-reference descriptor cards: a packaging-level view that names the plugin and the capability it adds, then defers the deeper serving/config behavior to the dedicated vLLM provider doc. This card covers all three source H2 sections — `## Distribution`, `## Surface`, and `## Related docs` — and links rather than redefines the deeper vLLM provider configuration (`/providers/vllm`).

## Distribution

The plugin's packaging identity, copied verbatim from the source `## Distribution` section:

- **Package:** `@openclaw/vllm-provider`
- **Install route:** included in OpenClaw

The "included in OpenClaw" install route means this is a **bundled** provider plugin — it ships with OpenClaw rather than requiring a separate npm install or ClawHub fetch, unlike npm+ClawHub-distributed plugins. No version, additional install command, or configuration key is given in the source.

## Surface

The contract surface the plugin registers, copied verbatim from the source `## Surface` section:

```
providers: vllm
```

This single line is the load-bearing fact of the card: the plugin contributes a **provider** named `vllm` to OpenClaw's provider contract. In packaging terms, the plugin adds vLLM model-provider support so that a self-hosted vLLM inference server becomes a selectable model provider. The source does not enumerate models, endpoints, environment variables, or any provider configuration — those belong to the deeper vLLM provider doc the card points to.

**Source**: OpenClaw documentation — `plugins/reference/vllm` (mirror `inbox/openclaw_docs/plugins/reference/vllm.md`)
**Last Updated**: 2026-06-22
**Status**: Active
