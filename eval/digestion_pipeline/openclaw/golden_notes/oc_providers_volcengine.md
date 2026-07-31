---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - volcengine
keywords:
  - openclaw volcengine provider
  - doubao models openclaw
  - volcengine-plan coding endpoint
  - volcano_engine_api_key
  - byteplus seed speech tts
  - volcengine_tts_api_key
  - openclaw onboard volcengine-api-key
  - seed-tts-1.0 resource id
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/volcengine
access_control_group: ["general"]
---

# OpenClaw — Configuring the Volcengine (Doubao) Provider

## Overview

This note is the procedure for wiring OpenClaw to **Volcengine (Volcano Engine / Doubao)**: a single bundled provider plugin that, from one `VOLCANO_ENGINE_API_KEY`, registers both the general `volcengine` endpoint and the coding `volcengine-plan` endpoint, and that can additionally register BytePlus Seed Speech as a text-to-speech (TTS) provider. It mirrors the `providers/volcengine` source page end to end: the header detail table, `openclaw onboard` getting-started (interactive + non-interactive), the two provider/endpoint base URLs, the built-in Doubao/Kimi/GLM/DeepSeek model catalog (general + coding tabs), the Seed Speech TTS setup (resource id, voice, legacy AppID/token), and the advanced configuration accordions (default model, picker fallback, daemon env vars).

## Header Details

| Detail     | Value                                                      |
| ---------- | ---------------------------------------------------------- |
| Providers  | `volcengine` (general + TTS) + `volcengine-plan` (coding)  |
| Model auth | `VOLCANO_ENGINE_API_KEY`                                   |
| TTS auth   | `VOLCENGINE_TTS_API_KEY` or `BYTEPLUS_SEED_SPEECH_API_KEY` |
| API        | OpenAI-compatible models, BytePlus Seed Speech TTS         |

The Volcengine provider gives access to Doubao models and third-party models hosted on Volcano Engine, with separate endpoints for general and coding workloads; the same bundled plugin can also register Volcengine Speech as a TTS provider.

## Getting started

The setup is three steps. First, run interactive onboarding, which registers BOTH the general (`volcengine`) and coding (`volcengine-plan`) providers from a single API key:

```bash
openclaw onboard --auth-choice volcengine-api-key
```

Second, set a default model in config:

```json5
{
  agents: {
    defaults: {
      model: { primary: "volcengine-plan/ark-code-latest" },
    },
  },
}
```

Third, verify the models are available per provider:

```bash
openclaw models list --provider volcengine
openclaw models list --provider volcengine-plan
```

For non-interactive setup (CI, scripting), pass the key directly:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice volcengine-api-key \
  --volcengine-api-key "$VOLCANO_ENGINE_API_KEY"
```

## Providers and endpoints

| Provider          | Endpoint                                  | Use case       |
| ----------------- | ----------------------------------------- | -------------- |
| `volcengine`      | `ark.cn-beijing.volces.com/api/v3`        | General models |
| `volcengine-plan` | `ark.cn-beijing.volces.com/api/coding/v3` | Coding models  |

Both providers are configured from a single API key, and setup registers both automatically.

## Built-in catalog

The bundled plugin ships two catalog tabs. **General (`volcengine`)** models:

| Model ref                                    | Name                            | Input       | Context |
| -------------------------------------------- | ------------------------------- | ----------- | ------- |
| `volcengine/doubao-seed-1-8-251228`          | Doubao Seed 1.8                 | text, image | 256,000 |
| `volcengine/doubao-seed-code-preview-251028` | doubao-seed-code-preview-251028 | text, image | 256,000 |
| `volcengine/kimi-k2-5-260127`                | Kimi K2.5                       | text, image | 256,000 |
| `volcengine/glm-4-7-251222`                  | GLM 4.7                         | text, image | 200,000 |
| `volcengine/deepseek-v3-2-251201`            | DeepSeek V3.2                   | text, image | 128,000 |

**Coding (`volcengine-plan`)** models:

| Model ref                                         | Name                     | Input | Context |
| ------------------------------------------------- | ------------------------ | ----- | ------- |
| `volcengine-plan/ark-code-latest`                 | Ark Coding Plan          | text  | 256,000 |
| `volcengine-plan/doubao-seed-code`                | Doubao Seed Code         | text  | 256,000 |
| `volcengine-plan/glm-4.7`                         | GLM 4.7 Coding           | text  | 200,000 |
| `volcengine-plan/kimi-k2-thinking`                | Kimi K2 Thinking         | text  | 256,000 |
| `volcengine-plan/kimi-k2.5`                       | Kimi K2.5 Coding         | text  | 256,000 |
| `volcengine-plan/doubao-seed-code-preview-251028` | Doubao Seed Code Preview | text  | 256,000 |

## Text-to-speech

Volcengine TTS uses the BytePlus Seed Speech HTTP API and is configured separately from the OpenAI-compatible Doubao model API key. In the BytePlus console, open Seed Speech > Settings > API Keys, copy the API key, then export the TTS key and resource id:

```bash
export VOLCENGINE_TTS_API_KEY="byteplus_seed_speech_api_key"
export VOLCENGINE_TTS_RESOURCE_ID="seed-tts-1.0"
```

Then enable it in `openclaw.json`:

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "volcengine",
      providers: {
        volcengine: {
          apiKey: "byteplus_seed_speech_api_key",
          voice: "en_female_anna_mars_bigtts",
          speedRatio: 1.0,
        },
      },
    },
  },
}
```

For voice-note targets, OpenClaw asks Volcengine for provider-native `ogg_opus`; for normal audio attachments, it asks for `mp3`. The provider aliases `bytedance` and `doubao` also resolve to the same speech provider. The default resource id is `seed-tts-1.0` because that is what BytePlus grants to newly created Seed Speech API keys in the default project; if your project has TTS 2.0 entitlement, set `VOLCENGINE_TTS_RESOURCE_ID=seed-tts-2.0`. Note that `VOLCANO_ENGINE_API_KEY` is for the ModelArk/Doubao model endpoints and is **not** a Seed Speech API key — TTS needs a Seed Speech API key from the BytePlus Speech Console, or a legacy Speech Console AppID/token pair. Legacy AppID/token auth remains supported for older Speech Console applications by exporting `VOLCENGINE_TTS_APPID="speech_app_id"`, `VOLCENGINE_TTS_TOKEN="speech_access_token"`, and `VOLCENGINE_TTS_CLUSTER="volcano_tts"`.

## Advanced configuration

**Default model after onboarding.** `openclaw onboard --auth-choice volcengine-api-key` currently sets `volcengine-plan/ark-code-latest` as the default model while also registering the general `volcengine` catalog.

**Model picker fallback behavior.** During onboarding/configure model selection, the Volcengine auth choice prefers both `volcengine/*` and `volcengine-plan/*` rows; if those models are not loaded yet, OpenClaw falls back to the unfiltered catalog instead of showing an empty provider-scoped picker.

**Environment variables for daemon processes.** If the Gateway runs as a daemon (launchd/systemd), make sure model and TTS env vars such as `VOLCANO_ENGINE_API_KEY`, `VOLCENGINE_TTS_API_KEY`, `BYTEPLUS_SEED_SPEECH_API_KEY`, `VOLCENGINE_TTS_APPID`, and `VOLCENGINE_TTS_TOKEN` are available to that process (for example, in `~/.openclaw/.env` or via `env.shellEnv`). When running OpenClaw as a background service, environment variables set in your interactive shell are not automatically inherited.

**Source**: OpenClaw documentation — `providers/volcengine` (mirror `inbox/openclaw_docs/providers/volcengine.md`)
**Last Updated**: 2026-06-22
**Status**: Active
