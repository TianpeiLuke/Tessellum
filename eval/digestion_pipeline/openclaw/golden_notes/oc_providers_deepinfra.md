---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - deepinfra
keywords:
  - deepinfra provider openclaw
  - deepinfra unified api
  - openclaw deepinfra-provider plugin
  - deepinfra_api_key
  - deepinfra model ref prefix
  - live model catalog discovery
  - deepinfra supported surfaces
  - deepseek-v4-flash default model
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/deepinfra
access_control_group: ["general"]
---

# OpenClaw — Configuring the DeepInfra Unified Provider

## Overview

This note is the setup procedure for the **DeepInfra** provider in OpenClaw, mirroring the `providers/deepinfra` source page. DeepInfra provides a **unified API** that routes requests to the most popular open source and frontier models behind a single endpoint and API key; it is OpenAI-compatible, so most OpenAI SDKs work by switching the base URL. The procedure covers installing the official plugin and restarting the Gateway, obtaining and configuring the `DEEPINFRA_API_KEY` (via the CLI onboard flag or an environment variable), the `agents.defaults.model` config snippet, the full set of OpenClaw surfaces the plugin registers (chat / image / video / media-understanding / STT / TTS / memory embeddings) with their default models, live catalog discovery, the `deepinfra/<provider>/<model>` ref format, and the base/inference URLs.

## Install plugin

Install the official plugin, then restart Gateway:

```bash
openclaw plugins install @openclaw/deepinfra-provider
openclaw gateway restart
```

## Getting an API key

1. Go to [https://deepinfra.com/](https://deepinfra.com/)
2. Sign in or create an account
3. Navigate to Dashboard / Keys and generate a new API key or use the auto created one

## CLI setup

Onboard with the API key directly:

```bash
openclaw onboard --deepinfra-api-key <key>
```

Or set the environment variable:

```bash
export DEEPINFRA_API_KEY="<your-deepinfra-api-key>"
```

## Config snippet

The config sets the env var and points `agents.defaults.model.primary` at a DeepInfra model ref:

```json5
{
  env: { DEEPINFRA_API_KEY: "<your-deepinfra-api-key>" },
  agents: {
    defaults: {
      model: { primary: "deepinfra/deepseek-ai/DeepSeek-V4-Flash" },
    },
  },
}
```

## Supported OpenClaw surfaces

The plugin registers all DeepInfra surfaces that match current OpenClaw provider contracts. Chat, image generation, and video generation refresh their model catalogues live from `/v1/openai/models?sort_by=openclaw&filter=with_meta` when `DEEPINFRA_API_KEY` is configured; the other surfaces use the curated static defaults below.

| Surface | Default model | OpenClaw config/tool |
| --- | --- | --- |
| Chat / model provider | first chat-tagged entry from live catalog (manifest fallback `deepseek-ai/DeepSeek-V4-Flash`) | `agents.defaults.model` |
| Image generation/editing | first `image-gen`-tagged entry from live catalog (static fallback `black-forest-labs/FLUX-1-schnell`) | `image_generate`, `agents.defaults.imageGenerationModel` |
| Media understanding | `moonshotai/Kimi-K2.5` for images | inbound image understanding |
| Speech-to-text | `openai/whisper-large-v3-turbo` | inbound audio transcription |
| Text-to-speech | `hexgrad/Kokoro-82M` | `messages.tts.provider: "deepinfra"` |
| Video generation | first `video-gen`-tagged entry from live catalog (static fallback `Pixverse/Pixverse-T2V`) | `video_generate`, `agents.defaults.videoGenerationModel` |
| Memory embeddings | `BAAI/bge-m3` | `agents.defaults.memorySearch.provider: "deepinfra"` |

DeepInfra also exposes reranking, classification, object-detection, and other native model types. OpenClaw does not currently have first-class provider contracts for those categories, so this plugin does not register them yet.

## Available models

OpenClaw dynamically discovers available DeepInfra models at startup. Use `/models deepinfra` to see the full list of models available. Any model available on [DeepInfra.com](https://deepinfra.com/) can be used with the `deepinfra/` prefix:

```
deepinfra/deepseek-ai/DeepSeek-V4-Flash
deepinfra/deepseek-ai/DeepSeek-V3.2
deepinfra/MiniMaxAI/MiniMax-M2.5
deepinfra/moonshotai/Kimi-K2.5
deepinfra/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B
deepinfra/zai-org/GLM-5.1
...and many more
```

## Notes

- Model refs are `deepinfra/<provider>/<model>` (e.g., `deepinfra/Qwen/Qwen3-Max`).
- Default model: `deepinfra/deepseek-ai/DeepSeek-V4-Flash`
- Base URL: `https://api.deepinfra.com/v1/openai`
- Native video generation uses `https://api.deepinfra.com/v1/inference/<model>`.

**Source**: OpenClaw documentation — `providers/deepinfra` (mirror `inbox/openclaw_docs/providers/deepinfra.md`)
**Last Updated**: 2026-06-22
**Status**: Active
