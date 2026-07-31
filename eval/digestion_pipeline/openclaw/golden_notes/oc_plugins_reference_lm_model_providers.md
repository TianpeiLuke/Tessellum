---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw litellm plugin
  - openclaw llama-cpp plugin
  - openclaw lmstudio plugin
  - model provider plugin install
  - embeddingProviders contract
  - memoryEmbeddingProviders contract
  - imageGenerationProviders contract
  - openclaw provider package
topics:
  - OpenClaw
  - Provider Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/litellm
access_control_group: ["general"]
---

# OpenClaw — `l*` Model and Embedding Provider Plugins (LiteLLM, Llama Cpp, LM Studio)

## Overview

This note is a procedure-oriented inventory card for the three OpenClaw `l*` plugins that register model or embedding **provider** capability surfaces: **LiteLLM** (a model-provider proxy/aggregator), **Llama Cpp** (local GGUF embeddings), and **LM Studio** (a local desktop model plus memory-embedding provider). It consolidates the three micro-stub reference pages `plugins/reference/litellm`, `plugins/reference/llama-cpp`, and `plugins/reference/lmstudio` into one "how to enable this class of provider plugin" card, mirroring each page's `## Distribution`, `## Surface`, and `## Related docs` content. For each plugin it states the npm package name, the install route (included-in-OpenClaw vs `npm`/ClawHub), the `providers:` / `contracts:` capability surface it registers, and the pointer to that integration's deep-dive page. The deep-dive provider pages themselves are owned by other sub-plans and are linked, not duplicated, here.

## LiteLLM Plugin

LiteLLM adds LiteLLM model provider support to OpenClaw — an aggregator/proxy that fronts many upstream models behind one provider entry.

- **Package**: `@openclaw/litellm-provider`
- **Install route**: included in OpenClaw (no separate install step needed)
- **Surface**: `providers: litellm; contracts: imageGenerationProviders`
- **Related docs**: `/providers/litellm` (the provider deep-dive — see References)

Because the install route is "included in OpenClaw", enabling LiteLLM is a configuration step (registering/activating the `litellm` provider) rather than a package fetch. The `providers: litellm` entry registers the provider with the model catalog, and the `imageGenerationProviders` contract advertises that this provider also contributes image-generation capability.

## Llama Cpp Plugin

Llama Cpp provides local GGUF embeddings through `node-llama-cpp` — a local embedding provider that runs quantized GGUF weights on the host.

- **Package**: `@openclaw/llama-cpp-provider`
- **Install route**: `npm`; ClawHub
- **Surface**: `contracts: embeddingProviders`
- **Related docs**: `/plugins/llama-cpp` (the plugin deep-dive — see References)

Unlike LiteLLM and LM Studio, this plugin is not bundled in OpenClaw — it is installed via `npm` or from ClawHub. It registers only the `embeddingProviders` contract (no `providers:` model surface): its role is to generate local text embeddings via `node-llama-cpp` from GGUF model files, feeding the embedding/memory subsystem.

## LM Studio Plugin

LM Studio adds LM Studio model provider support to OpenClaw — a local desktop model server that doubles as a memory-embedding provider.

- **Package**: `@openclaw/lmstudio-provider`
- **Install route**: included in OpenClaw (no separate install step needed)
- **Surface**: `providers: lmstudio; contracts: memoryEmbeddingProviders`
- **Related docs**: `/providers/lmstudio` (the provider deep-dive — see References)

LM Studio is bundled in OpenClaw, so enabling it is a configuration step. The `providers: lmstudio` entry registers the local LM Studio model server as a provider in the model catalog, while the `memoryEmbeddingProviders` contract advertises that this provider also supplies embeddings to the memory subsystem.

## Install-Route and Surface Summary

| Plugin | Package | Install route | `providers:` | `contracts:` |
|---|---|---|---|---|
| LiteLLM | `@openclaw/litellm-provider` | included in OpenClaw | `litellm` | `imageGenerationProviders` |
| Llama Cpp | `@openclaw/llama-cpp-provider` | `npm`; ClawHub | — | `embeddingProviders` |
| LM Studio | `@openclaw/lmstudio-provider` | included in OpenClaw | `lmstudio` | `memoryEmbeddingProviders` |

Two of the three (LiteLLM, LM Studio) are bundled in OpenClaw and only need enabling/configuration; Llama Cpp is the only one of the three requiring a separate `npm`/ClawHub install. LiteLLM and LM Studio register a named model `providers:` surface (`litellm`, `lmstudio`); Llama Cpp registers only an embedding contract. The contract distinction maps to consumer subsystem: `embeddingProviders` and `memoryEmbeddingProviders` feed the embedding/memory path, while `imageGenerationProviders` advertises image-generation capability through the LiteLLM proxy.

**Source**: OpenClaw documentation — `plugins/reference/litellm`, `plugins/reference/llama-cpp`, `plugins/reference/lmstudio` (mirror `inbox/openclaw_docs/plugins/reference/*.md`)
**Last Updated**: 2026-06-22
**Status**: Active
