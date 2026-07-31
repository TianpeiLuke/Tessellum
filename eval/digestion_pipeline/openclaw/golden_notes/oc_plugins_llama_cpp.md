---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - llama_cpp
keywords:
  - openclaw llama-cpp provider
  - local gguf memory embeddings
  - node-llama-cpp runtime
  - memorysearch provider local
  - embeddinggemma-300m gguf
  - openclaw plugins install llama-cpp-provider
  - pnpm rebuild node-llama-cpp
  - local embeddings ollama lm studio
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/llama-cpp
access_control_group: ["general"]
---

# OpenClaw — Install the llama.cpp Local-Embeddings Provider Plugin

## Overview

This note is the procedure for installing and configuring `@openclaw/llama-cpp-provider`, the official external provider plugin that supplies local GGUF embeddings for OpenClaw memory search. It owns the `node-llama-cpp` runtime dependency used by `memorySearch.provider: "local"`, points that provider at a GGUF model, and walks the native-runtime build steps (Node 24, pnpm approve/rebuild). It mirrors the `plugins/llama-cpp` source page (lead + Configuration + Native Runtime sections).

## Install the Plugin

`llama-cpp` is the official external provider plugin for local GGUF embeddings, and it owns the `node-llama-cpp` runtime dependency used by `memorySearch.provider: "local"`. Install it before using local memory embeddings:

```bash
openclaw plugins install @openclaw/llama-cpp-provider
```

The main `openclaw` npm package does not include `node-llama-cpp`. Keeping the native dependency in this plugin prevents normal OpenClaw npm updates from deleting a manually installed runtime inside the OpenClaw package directory — that is, the native dep is deliberately isolated in the plugin so it survives core `openclaw` package updates.

## Configuration

Set the memory search provider to `local` under `agents.defaults.memorySearch`, with `local.modelPath` pointing at a GGUF model:

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "local",
        local: {
          modelPath: "hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/embeddinggemma-300m-qat-Q8_0.gguf",
        },
      },
    },
  },
}
```

The default model is `embeddinggemma-300m-qat-Q8_0.gguf`. You can also point `local.modelPath` at a local `.gguf` file.

## Native Runtime

Use Node 24 for the smoothest native install path. Source checkouts using pnpm may need to approve and rebuild the native dependency:

```bash
pnpm approve-builds
pnpm rebuild node-llama-cpp
```

For lower-friction local embeddings, use a local service provider such as Ollama or LM Studio instead.

**Source**: OpenClaw documentation — `plugins/llama-cpp` (mirror `inbox/openclaw_docs/plugins/llama-cpp.md`)
**Last Updated**: 2026-06-22
**Status**: Active
