---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - ollama
keywords:
  - ollama vision models
  - image understanding ollama
  - infer image describe
  - agents.defaults.imagemodel
  - input text image
  - qwen2.5vl ollama
  - num_ctx vision timeout
  - image-capable model
topics:
  - OpenClaw
  - Ollama Vision
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/ollama
access_control_group: ["general"]
---

# OpenClaw — Ollama Vision and Image Description

## Overview

This note is the procedure for routing image understanding through local or hosted Ollama vision models in OpenClaw, mirroring the **Vision and image description** section of the `providers/ollama` source page. It covers marking a model image-capable (`input: ["text", "image"]`), the `openclaw infer image describe` smoke test, choosing it over `infer model run --file`, setting `agents.defaults.imageModel` as the inbound-media default, and capping `num_ctx` plus the image timeout so slow or constrained local vision models do not crash. Provider setup, auth, and auto-discovery (which is how implicit vision capability is detected) are prerequisites covered in the sibling Ollama setup note; advanced context/timeout tuning continues in the Ollama advanced note.

## Image-capable provider and detection

The bundled Ollama plugin registers Ollama as an **image-capable media-understanding provider**. This lets OpenClaw route explicit image-description requests and configured image-model defaults through local or hosted Ollama vision models. OpenClaw **rejects image-description requests for models that are not marked image-capable**. With implicit discovery, OpenClaw reads this from Ollama when `/api/show` reports a `vision` capability; such models are marked image-capable (`input: ["text", "image"]`) so OpenClaw auto-injects images into the prompt. When you define `models.providers.ollama.models` manually instead of relying on discovery, mark vision models with image input support explicitly:

```json5
{
  id: "qwen2.5vl:7b",
  name: "qwen2.5vl:7b",
  input: ["text", "image"],
  contextWindow: 128000,
  maxTokens: 8192,
}
```

## Pull and smoke-test a local vision model

For local vision, pull a model that supports images and set the local auth marker:

```bash
ollama pull qwen2.5vl:7b
export OLLAMA_API_KEY="ollama-local"
```

Then verify with the infer CLI. `--model` must be a full `<provider/model>` ref; when it is set, `openclaw infer image describe` runs that model directly instead of skipping description because the model supports native vision:

```bash
openclaw infer image describe \
  --file ./photo.jpg \
  --model ollama/qwen2.5vl:7b \
  --json
```

Use `infer image describe` when you want OpenClaw's image-understanding provider flow, the configured `agents.defaults.imageModel`, and the image-description output shape. Use `infer model run --file` (covered in the setup note) when you want a raw multimodal model probe with a custom prompt and one or more images. To live-verify the explicit image tool against local Ollama, run `OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_OLLAMA_IMAGE=1 pnpm test:live -- src/agents/tools/image-tool.ollama.live.test.ts`.

## Default image-understanding model for inbound media

To make Ollama the default image-understanding model for inbound media, configure `agents.defaults.imageModel`:

```json5
{
  agents: {
    defaults: {
      imageModel: {
        primary: "ollama/qwen2.5vl:7b",
      },
    },
  },
}
```

Prefer the full `ollama/<model>` ref. If the same model is listed under `models.providers.ollama.models` with `input: ["text", "image"]` and no other configured image provider exposes that bare model ID, OpenClaw also normalizes a bare `imageModel` ref such as `qwen2.5vl:7b` to `ollama/qwen2.5vl:7b`. If more than one configured image provider has the same bare ID, use the provider prefix explicitly.

## Timeouts and num_ctx for constrained hardware

Slow local vision models can need a longer image-understanding timeout than cloud models. They can also crash or stop when Ollama tries to allocate the full advertised vision context on constrained hardware. Set a capability timeout, and cap `num_ctx` on the model entry when you only need a normal image-description turn:

```json5
{
  models: {
    providers: {
      ollama: {
        models: [
          {
            id: "qwen2.5vl:7b",
            name: "qwen2.5vl:7b",
            input: ["text", "image"],
            params: { num_ctx: 2048, keep_alive: "1m" },
          },
        ],
      },
    },
  },
  tools: {
    media: {
      image: {
        timeoutSeconds: 180,
        models: [{ provider: "ollama", model: "qwen2.5vl:7b", timeoutSeconds: 300 }],
      },
    },
  },
}
```

This timeout applies to inbound image understanding and to the explicit `image` tool the agent can call during a turn. Provider-level `models.providers.ollama.timeoutSeconds` still controls the underlying Ollama HTTP request guard for normal model calls.

**Source**: OpenClaw documentation — `providers/ollama` (Vision and image description section; mirror `inbox/openclaw_docs/providers/ollama.md`)
**Last Updated**: 2026-06-22
**Status**: Active
