---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - groq
keywords:
  - openclaw groq provider
  - groq api key
  - openai-compatible chat provider
  - groq lpu inference
  - reasoning_effort think mapping
  - whisper audio transcription
  - groq built-in model catalog
  - tools media audio
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/groq
access_control_group: ["general"]
---

# OpenClaw — Configuring the Groq Provider

## Overview

This note is the procedure for configuring the OpenClaw **Groq** provider, mirroring the `providers/groq` source page. Groq provides ultra-fast inference on open-weight models (Llama, Gemma, Kimi, Qwen, GPT OSS, and more) using custom LPU hardware, and the Groq plugin registers BOTH an OpenAI-compatible chat provider and an audio media-understanding provider. The steps below cover installing the official plugin, supplying the `GROQ_API_KEY` credential, choosing a default `groq/*` chat model, the built-in manifest-backed catalog, the `/think` → `reasoning_effort` mapping per reasoning model, and wiring Groq's Whisper transcription onto the shared `tools.media.audio` surface (plus the daemon-environment and custom-model-id advanced notes).

## Provider Identity

The Groq integration is defined by the following fixed properties (front-matter property table). These are the values you reference when authenticating and selecting models:

| Property               | Value                                    |
| ---------------------- | ---------------------------------------- |
| Provider id            | `groq`                                   |
| Plugin                 | official external package                |
| Auth env var           | `GROQ_API_KEY`                           |
| API                    | OpenAI-compatible (`openai-completions`) |
| Base URL               | `https://api.groq.com/openai/v1`         |
| Audio transcription    | `whisper-large-v3-turbo` (default)       |
| Suggested chat default | `groq/llama-3.3-70b-versatile`           |

## Install plugin

Install the official plugin, then restart Gateway:

```bash
openclaw plugins install @openclaw/groq-provider
openclaw gateway restart
```

## Getting started

After installing the plugin, the four onboarding steps are:

1. **Get an API key** — create an API key at `console.groq.com/keys`.
2. **Set the API key** — export it as the `GROQ_API_KEY` environment variable: `export GROQ_API_KEY=gsk_...`.
3. **Set a default model** — point the agent default at a `groq/*` model ref (shown below).
4. **Verify the catalog is reachable** — run `openclaw models list --provider groq`.

The default-model step uses `agents.defaults.model.primary`:

```json5
{
  agents: {
    defaults: {
      model: { primary: "groq/llama-3.3-70b-versatile" },
    },
  },
}
```

### Config file example

The same setup can be written entirely in the config file, supplying the key via `env` instead of a shell export:

```json5
{
  env: { GROQ_API_KEY: "gsk_..." },
  agents: {
    defaults: {
      model: { primary: "groq/llama-3.3-70b-versatile" },
    },
  },
}
```

## Built-in catalog

OpenClaw ships a manifest-backed Groq catalog with both reasoning and non-reasoning entries. Run `openclaw models list --provider groq` to see the static rows for your installed version, or check `console.groq.com/docs/models` for Groq's authoritative list. The catalog evolves with each OpenClaw release: `openclaw models list --provider groq` shows the rows known to your installed version, so cross-check against Groq's docs for newly-added or deprecated models.

| Model ref                                        | Name                    | Reasoning | Input        | Context |
| ------------------------------------------------ | ----------------------- | --------- | ------------ | ------- |
| `groq/llama-3.3-70b-versatile`                   | Llama 3.3 70B Versatile | no        | text         | 131,072 |
| `groq/llama-3.1-8b-instant`                      | Llama 3.1 8B Instant    | no        | text         | 131,072 |
| `groq/meta-llama/llama-4-scout-17b-16e-instruct` | Llama 4 Scout 17B       | no        | text + image | 131,072 |
| `groq/openai/gpt-oss-120b`                       | GPT OSS 120B            | yes       | text         | 131,072 |
| `groq/openai/gpt-oss-20b`                        | GPT OSS 20B             | yes       | text         | 131,072 |
| `groq/openai/gpt-oss-safeguard-20b`              | Safety GPT OSS 20B      | yes       | text         | 131,072 |
| `groq/qwen/qwen3-32b`                            | Qwen3 32B               | yes       | text         | 131,072 |
| `groq/groq/compound`                             | Compound                | yes       | text         | 131,072 |
| `groq/groq/compound-mini`                        | Compound Mini           | yes       | text         | 131,072 |

## Reasoning models

OpenClaw maps its shared `/think` levels to Groq's model-specific `reasoning_effort` values:

- For `qwen/qwen3-32b`, disabled thinking sends `none` and enabled thinking sends `default`.
- For Groq GPT OSS reasoning models (`openai/gpt-oss-*`), OpenClaw sends `low`, `medium`, or `high` based on `/think` level. Disabled thinking omits `reasoning_effort` because those models do not support a disabled value.
- DeepSeek R1 Distill, Qwen QwQ, and Compound use Groq's native reasoning surface; `/think` controls visibility but the model always reasons.

See the shared Thinking modes tool (`/tools/thinking`) for the `/think` levels and how OpenClaw translates them per provider.

## Audio transcription

Groq's plugin also registers an **audio media-understanding provider** so voice messages can be transcribed through the shared `tools.media.audio` surface. Its properties:

| Property           | Value                                     |
| ------------------ | ----------------------------------------- |
| Shared config path | `tools.media.audio`                       |
| Default base URL   | `https://api.groq.com/openai/v1`          |
| Default model      | `whisper-large-v3-turbo`                  |
| Auto priority      | 20                                        |
| API endpoint       | OpenAI-compatible `/audio/transcriptions` |

To make Groq the default audio backend, pin the provider under `tools.media.audio.models`:

```json5
{
  tools: {
    media: {
      audio: {
        models: [{ provider: "groq" }],
      },
    },
  },
}
```

## Advanced configuration

**Environment availability for the daemon** — if the Gateway runs as a managed service (launchd, systemd, Docker), `GROQ_API_KEY` must be visible to that process — not just to your interactive shell. A key exported only in an interactive shell will not help a launchd or systemd daemon unless that environment is imported there too; set the key in `~/.openclaw/.env` or via `env.shellEnv` to make it readable from the gateway process.

**Custom Groq model ids** — OpenClaw accepts any Groq model id at runtime. Use the exact id shown by Groq and prefix it with `groq/`. The static catalog covers the common cases; uncatalogued ids fall through to the default OpenAI-compatible template. Point the default at a custom id with `agents.defaults.model.primary: "groq/<your-model-id>"`.

**Source**: OpenClaw documentation — `providers/groq` (mirror `inbox/openclaw_docs/providers/groq.md`)
**Last Updated**: 2026-06-22
**Status**: Active
