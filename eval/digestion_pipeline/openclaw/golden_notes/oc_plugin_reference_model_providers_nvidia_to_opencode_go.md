---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw model provider plugins
  - nvidia-provider ollama-provider openai-provider
  - opencode-provider opencode-go-provider
  - included in openclaw install route
  - providers nvidia ollama ollama-cloud openai opencode
  - memoryEmbeddingProviders webSearchProviders contracts
  - imageGenerationProviders videoGenerationProviders speechProviders
  - mediaUnderstandingProviders realtimeTranscriptionProviders realtimeVoiceProviders
  - built-in model provider plugin reference
topics:
  - OpenClaw
  - Model Provider Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/nvidia
access_control_group: ["general"]
---

# OpenClaw — Built-in Model-Provider Plugins (NVIDIA → OpenCode-Go)

## Overview

This note is a consolidated reference for five of OpenClaw's built-in **model-provider plugins** — NVIDIA, Ollama (which also serves Ollama Cloud), OpenAI, OpenCode, and OpenCode-Go — mirroring their `plugins/reference/<name>` stub pages. Each plugin is a self-contained npm package that, when loaded, registers one or more model **provider IDs** with the OpenClaw runtime and (for some) backs additional capability **contracts** (embedding, web search, image/video generation, speech, transcription, realtime voice, media understanding). All five share the same shape: a one-line summary, a `## Distribution` block (npm `Package` + `Install route`), a `## Surface` block (the `providers:` IDs and optional `contracts:` it contributes), and `## Related docs` pointers to the per-provider configuration pages. Every one of these five carries the identical install route — **included in OpenClaw** — so no separate install step registers them; the per-provider authentication, base URL, and model-selection configuration is documented in the `providers/*` pages, not here. This note records what each plugin registers; it does not redefine the providers themselves.

## Plugin → Package → Provider IDs → Contracts (reference table)

The following table reproduces each plugin's `## Distribution` and `## Surface` blocks verbatim from the source stubs. Every plugin's install route is "included in OpenClaw"; the `Related docs` column lists the per-provider config page each stub points to.

| Plugin | npm `Package` | Install route | `providers:` | `contracts:` | Related docs |
|---|---|---|---|---|---|
| NVIDIA | `@openclaw/nvidia-provider` | included in OpenClaw | `nvidia` | *(none)* | `/providers/nvidia` |
| Ollama | `@openclaw/ollama-provider` | included in OpenClaw | `ollama`, `ollama-cloud` | `memoryEmbeddingProviders`, `webSearchProviders` | `/providers/ollama`, `/providers/ollama-cloud` |
| OpenAI | `@openclaw/openai-provider` | included in OpenClaw | `openai` | `imageGenerationProviders`, `mediaUnderstandingProviders`, `memoryEmbeddingProviders`, `realtimeTranscriptionProviders`, `realtimeVoiceProviders`, `speechProviders`, `videoGenerationProviders` | `/providers/openai` |
| OpenCode | `@openclaw/opencode-provider` | included in OpenClaw | `opencode` | `mediaUnderstandingProviders` | `/providers/opencode` |
| OpenCode-Go | `@openclaw/opencode-go-provider` | included in OpenClaw | `opencode-go` | `mediaUnderstandingProviders` | `/providers/opencode-go` |

## Per-Plugin Detail

### NVIDIA plugin (`@openclaw/nvidia-provider`)

"Adds NVIDIA model provider support to OpenClaw." Its `## Surface` registers a single provider — `providers: nvidia` — and declares no additional capability contracts. Install route is included in OpenClaw; per-provider configuration lives at the `nvidia` provider doc (`/providers/nvidia`). Read this plugin's page when installing, configuring, or auditing the nvidia plugin.

### Ollama plugin (`@openclaw/ollama-provider`)

"Adds Ollama, Ollama Cloud model provider support to OpenClaw." This is the only plugin in this set that registers **two** provider IDs from one package: `providers: ollama, ollama-cloud`. It additionally backs two capability contracts — `contracts: memoryEmbeddingProviders, webSearchProviders` — meaning Ollama can supply both memory-embedding generation and web-search provision in addition to chat/completion models. Install route is included in OpenClaw. Related docs point to both provider config pages: `/providers/ollama` and `/providers/ollama-cloud`. (Ollama is a local / self-hosted inference engine; OpenClaw has no dedicated `term_ollama` note, so the local-inference concept links via `term_vllm` and `term_quantization`.)

### OpenAI plugin (`@openclaw/openai-provider`)

"Adds OpenAI model provider support to OpenClaw." It registers `providers: openai` and is the **broadest** contract surface in this set, backing seven contracts: `contracts: imageGenerationProviders, mediaUnderstandingProviders, memoryEmbeddingProviders, realtimeTranscriptionProviders, realtimeVoiceProviders, speechProviders, videoGenerationProviders`. In other words, the single OpenAI plugin can supply chat models plus image generation, video generation, media (image/audio) understanding, embedding generation for memory, audio transcription, realtime voice, and text-to-speech. Install route is included in OpenClaw; configuration lives at `/providers/openai`.

### OpenCode plugin (`@openclaw/opencode-provider`)

"Adds OpenCode model provider support to OpenClaw." It registers `providers: opencode` and backs a single contract — `contracts: mediaUnderstandingProviders`. Install route is included in OpenClaw; configuration lives at `/providers/opencode`.

### OpenCode-Go plugin (`@openclaw/opencode-go-provider`)

"Adds OpenCode Go model provider support to OpenClaw." It registers `providers: opencode-go` and backs the same single contract as OpenCode — `contracts: mediaUnderstandingProviders`. It is a distinct package (`@openclaw/opencode-go-provider`) registering a distinct provider ID (`opencode-go`), separate from the `opencode` provider above. Install route is included in OpenClaw; configuration lives at `/providers/opencode-go`.

## Capability Contracts Referenced by These Plugins

A model-provider plugin's `## Surface` lists, beyond the `providers:` IDs, any capability **contracts:** it satisfies. The contract names appearing across these five stubs are reproduced verbatim below with the capability each names (the contract semantics are OpenClaw-internal; the configuration of each lives in the relevant `providers/*` doc):

- `memoryEmbeddingProviders` — supplies embedding generation used for memory search (backed here by ollama and openai).
- `webSearchProviders` — supplies web-search provision (backed here by ollama).
- `imageGenerationProviders` — supplies image generation (backed here by openai).
- `videoGenerationProviders` — supplies video generation (backed here by openai).
- `mediaUnderstandingProviders` — supplies media (image/audio) understanding (backed here by openai, opencode, opencode-go).
- `realtimeTranscriptionProviders` — supplies realtime audio transcription (backed here by openai).
- `realtimeVoiceProviders` — supplies realtime voice (backed here by openai).
- `speechProviders` — supplies speech / text-to-speech (backed here by openai).

A plugin that lists only `providers:` and no `contracts:` (NVIDIA) contributes only chat/completion model access through its provider ID. The `providers:` IDs are what populate the runtime's model catalog and what configuration references; the `contracts:` are the optional extra capability surfaces a provider plugin can fill.

**Source**: OpenClaw documentation — `plugins/reference/{nvidia,ollama,openai,opencode,opencode-go}` (mirror `inbox/openclaw_docs/plugins/reference/*.md`)
**Last Updated**: 2026-06-22
**Status**: Active
