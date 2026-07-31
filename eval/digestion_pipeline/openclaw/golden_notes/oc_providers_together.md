---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - together
keywords:
  - together ai openclaw provider
  - together_api_key
  - together-api-key auth choice
  - openai-compatible provider together
  - together built-in model catalog
  - together video_generate wan2.2
  - together daemon env availability
  - models list provider together
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/together
access_control_group: ["general"]
---

# OpenClaw — Connecting the Together AI Provider

## Overview

This note is the procedure for connecting OpenClaw to [Together AI](https://together.ai), an aggregator that provides access to leading open-source models (Llama, DeepSeek, Kimi, and more) through a unified, OpenAI-compatible API. It mirrors the `providers/together` source page: the provider property table, the `Getting started` onboarding path (including the `Non-interactive example` H3), the bundled built-in model catalog, the `Video generation` surface (the `video_generate` Wan2.2 model the same `together` plugin registers), and the environment-note / troubleshooting accordions. Per the sub-plan, the shared video-generation tool itself is owned by `tools/video-generation` and is linked, not redigested here.

## Provider Properties

Together AI is identified by the following properties (verbatim from the source property table):

| Property | Value |
| -------- | ----------------------------- |
| Provider | `together` |
| Auth | `TOGETHER_API_KEY` |
| API | OpenAI-compatible |
| Base URL | `https://api.together.xyz/v1` |

The provider id is `together`, authentication is via the `TOGETHER_API_KEY` environment variable, the API is OpenAI-compatible, and requests go to the base URL `https://api.together.xyz/v1`.

## Getting started

Setup is a three-step onboarding flow:

1. **Get an API key** — create an API key at [api.together.ai/settings/api-keys](https://api.together.ai/settings/api-keys).
2. **Run onboarding** — run the onboarding command with the Together auth choice:

```bash
openclaw onboard --auth-choice together-api-key
```

3. **Set a default model** — pin a default `agents.defaults.model.primary` model ref in config (JSON5):

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "together/meta-llama/Llama-3.3-70B-Instruct-Turbo",
      },
    },
  },
}
```

The onboarding preset sets `together/meta-llama/Llama-3.3-70B-Instruct-Turbo` as the default model.

### Non-interactive example

For scripted / non-interactive setup, pass the mode, auth choice, and key on the command line:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice together-api-key \
  --together-api-key "$TOGETHER_API_KEY"
```

## Built-in catalog

OpenClaw ships this bundled Together catalog (model ref, name, input modalities, context window, and notes are reproduced verbatim from the source):

| Model ref | Name | Input | Context | Notes |
| -------------------------------------------------- | ---------------------------- | ----------- | ------- | -------------------- |
| `together/meta-llama/Llama-3.3-70B-Instruct-Turbo` | Llama 3.3 70B Instruct Turbo | text | 131,072 | Default model |
| `together/moonshotai/Kimi-K2.6` | Kimi K2.6 FP4 | text, image | 262,144 | Kimi reasoning model |
| `together/deepseek-ai/DeepSeek-V4-Pro` | DeepSeek V4 Pro | text | 512,000 | Reasoning text model |
| `together/Qwen/Qwen2.5-7B-Instruct-Turbo` | Qwen2.5 7B Instruct Turbo | text | 32,768 | Fast text model |
| `together/zai-org/GLM-5.1` | GLM 5.1 FP4 | text | 202,752 | Reasoning text model |

The default model is `together/meta-llama/Llama-3.3-70B-Instruct-Turbo`; `together/moonshotai/Kimi-K2.6` accepts `text, image` input; and `together/deepseek-ai/DeepSeek-V4-Pro` has the largest context at 512,000 tokens. Model refs use the form `together/<model-id>`.

## Video generation

The bundled `together` plugin also registers video generation through the shared `video_generate` tool. Its properties (verbatim from the source):

| Property | Value |
| -------------------- | ------------------------------------------------------------------------ |
| Default video model | `together/Wan-AI/Wan2.2-T2V-A14B` |
| Modes | text-to-video; single-image reference only with `Wan-AI/Wan2.2-I2V-A14B` |
| Supported parameters | `aspectRatio`, `resolution` |

The default video model is `together/Wan-AI/Wan2.2-T2V-A14B` (text-to-video); single-image reference is only available with `Wan-AI/Wan2.2-I2V-A14B`; and the supported parameters are `aspectRatio` and `resolution`. To use Together as the default video provider, set `agents.defaults.videoGenerationModel.primary`:

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "together/Wan-AI/Wan2.2-T2V-A14B",
      },
    },
  },
}
```

For the shared tool parameters, provider selection, and failover behavior, see the dedicated Video Generation page (`/tools/video-generation`), which is the primary owner of that tool and is linked rather than redigested here.

## Environment and Troubleshooting

**Environment note.** If the Gateway runs as a daemon (launchd/systemd), make sure `TOGETHER_API_KEY` is available to that process (for example, in `~/.openclaw/.env` or via `env.shellEnv`). Keys set only in your interactive shell are not visible to daemon-managed gateway processes — use `~/.openclaw/.env` or `env.shellEnv` config for persistent availability.

**Troubleshooting.** Verify your key works with `openclaw models list --provider together`. If models are not appearing, confirm the API key is set in the correct environment for your Gateway process. Model refs use the form `together/<model-id>`.

**Source**: OpenClaw documentation — `providers/together` (mirror `inbox/openclaw_docs/providers/together.md`)
**Last Updated**: 2026-06-22
**Status**: Active
