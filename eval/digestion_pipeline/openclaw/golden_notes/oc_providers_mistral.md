---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - mistral
keywords:
  - openclaw mistral provider
  - mistral api key onboarding
  - voxtral batch transcription
  - voxtral realtime stt voice call
  - mistral-embed memory embeddings
  - mistral reasoning_effort thinking
  - mistral built-in llm catalog
  - openai-completions api.mistral.ai
topics:
  - OpenClaw
  - Mistral provider
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/mistral
access_control_group: ["general"]
---

# OpenClaw — Configure the Mistral Provider (chat, Voxtral STT, embeddings)

## Overview

This note is the setup procedure for OpenClaw's bundled **Mistral** plugin, mirroring the `providers/mistral` source page. OpenClaw ships a bundled Mistral plugin (`enabledByDefault: true`) that registers **four contracts**: chat completions, media understanding (Voxtral batch transcription), realtime STT for Voice Call (Voxtral Realtime), and memory embeddings (`mistral-embed`). It walks the property reference, API-key onboarding, the bundled LLM catalog, Voxtral batch audio transcription, Voxtral Realtime streaming STT for Voice Call, and advanced configuration (adjustable reasoning → `reasoning_effort`, memory embeddings, auth and base URL).

## Provider Reference

The bundled Mistral plugin exposes one provider id and these configuration anchors:

| Property | Value |
| --- | --- |
| Provider id | `mistral` |
| Plugin | bundled, `enabledByDefault: true` |
| Auth env var | `MISTRAL_API_KEY` |
| Onboarding flag | `--auth-choice mistral-api-key` |
| Direct CLI flag | `--mistral-api-key <key>` |
| API | OpenAI-compatible (`openai-completions`) |
| Base URL | `https://api.mistral.ai/v1` |
| Default model | `mistral/mistral-large-latest` |
| Embedding model | `mistral-embed` |
| Voxtral batch | `voxtral-mini-latest` (audio transcription) |
| Voxtral realtime | `voxtral-mini-transcribe-realtime-2602` |

## Getting Started

The page documents a four-step onboarding flow:

1. **Get your API key** — create an API key in the [Mistral Console](https://console.mistral.ai/).
2. **Run onboarding** — either `openclaw onboard --auth-choice mistral-api-key`, or pass the key directly with `openclaw onboard --mistral-api-key "$MISTRAL_API_KEY"`.
3. **Set a default model** — write the key into `env` and set the primary model to `mistral/mistral-large-latest`.
4. **Verify the model is available** — run `openclaw models list --provider mistral`.

The default-model config block (step 3):

```json5
{
  env: { MISTRAL_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "mistral/mistral-large-latest" } } },
}
```

## Built-in LLM Catalog

[Mistral Medium 3.5](https://docs.mistral.ai/models/model-cards/mistral-medium-3-5-26-04) is the current blended Medium model in the bundled catalog: 128B dense weights, text and image input, 256K context, function calling, structured output, coding, and adjustable reasoning through the Chat Completions API. Use `mistral/mistral-medium-3-5` when you want Mistral's newer unified agentic/coding model instead of the default `mistral/mistral-large-latest`. OpenClaw currently ships this bundled Mistral catalog:

| Model ref | Input | Context | Max output | Notes |
| --- | --- | --- | --- | --- |
| `mistral/mistral-large-latest` | text, image | 262,144 | 16,384 | Default model |
| `mistral/mistral-medium-2508` | text, image | 262,144 | 8,192 | Mistral Medium 3.1 |
| `mistral/mistral-medium-3-5` | text, image | 262,144 | 8,192 | Mistral Medium 3.5; adjustable reasoning |
| `mistral/mistral-small-latest` | text, image | 128,000 | 16,384 | Mistral Small 4; adjustable reasoning via API `reasoning_effort` |
| `mistral/pixtral-large-latest` | text, image | 128,000 | 32,768 | Pixtral |
| `mistral/codestral-latest` | text | 256,000 | 4,096 | Coding |
| `mistral/devstral-medium-latest` | text | 262,144 | 32,768 | Devstral 2 |
| `mistral/magistral-small` | text | 128,000 | 40,000 | Reasoning-enabled |

After onboarding, smoke-test Medium 3.5 without starting the Gateway with `openclaw infer model run --local --model mistral/mistral-medium-3-5 --prompt "Reply with exactly: mistral-ok" --json`, and browse the bundled catalog row before changing config with `openclaw models list --all --provider mistral --plain`.

## Audio Transcription (Voxtral)

Use Voxtral for batch audio transcription through the media understanding pipeline. The media transcription path uses `/v1/audio/transcriptions`, and the default audio model for Mistral is `voxtral-mini-latest`. Enable it under `tools.media.audio`:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "mistral", model: "voxtral-mini-latest" }],
      },
    },
  },
}
```

## Voice Call Streaming STT

The bundled `mistral` plugin registers Voxtral Realtime as a Voice Call streaming STT provider. The settings live under `plugins.entries.voice-call.config.streaming.providers.mistral`:

| Setting | Config path | Default |
| --- | --- | --- |
| API key | `plugins.entries.voice-call.config.streaming.providers.mistral.apiKey` | Falls back to `MISTRAL_API_KEY` |
| Model | `...mistral.model` | `voxtral-mini-transcribe-realtime-2602` |
| Encoding | `...mistral.encoding` | `pcm_mulaw` |
| Sample rate | `...mistral.sampleRate` | `8000` |
| Target delay | `...mistral.targetStreamingDelayMs` | `800` |

OpenClaw defaults Mistral realtime STT to `pcm_mulaw` at 8 kHz so Voice Call can forward Twilio media frames directly; use `encoding: "pcm_s16le"` and a matching `sampleRate` only if your upstream stream is already raw PCM. The Voice Call streaming config block:

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          streaming: {
            enabled: true,
            provider: "mistral",
            providers: {
              mistral: {
                apiKey: "${MISTRAL_API_KEY}",
                targetStreamingDelayMs: 800,
              },
            },
          },
        },
      },
    },
  },
}
```

## Advanced Configuration

### Adjustable reasoning

`mistral/mistral-small-latest` (Mistral Small 4) and `mistral/mistral-medium-3-5` support [adjustable reasoning](https://docs.mistral.ai/studio-api/conversations/reasoning/adjustable) on the Chat Completions API via `reasoning_effort` (`none` minimizes extra thinking in the output; `high` surfaces full thinking traces before the final answer). Mistral recommends `reasoning_effort="high"` for Medium 3.5 agentic and code use cases. OpenClaw maps the session **thinking** level to Mistral's API: **off** / **minimal** → `none`; **low** / **medium** / **high** / **xhigh** / **adaptive** / **max** → `high`.

Do not combine Medium 3.5 reasoning mode with `temperature: 0` — the Mistral HTTP API rejects `reasoning_effort="high"` plus `temperature: 0` with a 400 response; leave temperature unset so Mistral uses its default, or follow the [Medium 3.5 recommended settings](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B) and use `temperature: 0.7` for high reasoning. For deterministic direct answers, turn thinking off/minimal so OpenClaw sends `reasoning_effort: "none"` before you lower temperature. Other bundled Mistral catalog models do not use this parameter — keep using `magistral-*` models when you want Mistral's native reasoning-first behavior. Example model-scoped config for Medium 3.5 reasoning:

```json5
{
  agents: {
    defaults: {
      model: { primary: "mistral/mistral-medium-3-5" },
      models: {
        "mistral/mistral-medium-3-5": {
          params: { thinking: "high" },
        },
      },
    },
  },
}
```

### Memory embeddings

Mistral can serve memory embeddings via `/v1/embeddings` (default model: `mistral-embed`). Point memory search at the provider:

```json5
{
  memorySearch: { provider: "mistral" },
}
```

### Auth and base URL

Mistral auth uses `MISTRAL_API_KEY` (Bearer header). The provider base URL defaults to `https://api.mistral.ai/v1` and accepts the standard OpenAI-compatible chat-completions request shape. The onboarding default model is `mistral/mistral-large-latest`. Override the base URL under `models.providers.mistral.baseUrl` only when Mistral explicitly publishes a regional endpoint you need.

**Source**: OpenClaw documentation — `providers/mistral` (mirror `inbox/openclaw_docs/providers/mistral.md`)
**Last Updated**: 2026-06-22
**Status**: Active
