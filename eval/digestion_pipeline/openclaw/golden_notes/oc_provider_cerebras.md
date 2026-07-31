---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - cerebras
keywords:
  - openclaw cerebras provider
  - cerebras-provider plugin
  - cerebras_api_key
  - auth-choice cerebras-api-key
  - openai-compatible inference
  - cerebras static catalog
  - models mode merge
  - high-speed inference hardware
topics:
  - OpenClaw
  - Model Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/cerebras
access_control_group: ["general"]
---

# OpenClaw — Cerebras Provider Setup

## Overview

This note is the setup procedure for the OpenClaw **Cerebras** model provider — high-speed OpenAI-compatible inference served on Cerebras' custom inference hardware. It mirrors the `providers/cerebras` source page: installing the official provider plugin, resolving the `CEREBRAS_API_KEY` credential through onboarding or environment variables, verifying the bundled static four-model catalog, the preview/deprecation caveats on those models, and the optional `models.providers.cerebras` manual config with `mode: "merge"`. Cerebras is an externally-packaged provider plugin (`@openclaw/cerebras-provider`); once the key resolves, OpenClaw exposes a static catalog whose model refs are usable as `model.primary`.

## Provider Properties

The header table fixes the provider's identity and auth surface (copied verbatim from the source page):

| Property | Value |
| --- | --- |
| Provider id | `cerebras` |
| Plugin | official external package |
| Auth env var | `CEREBRAS_API_KEY` |
| Onboarding flag | `--auth-choice cerebras-api-key` |
| Direct CLI flag | `--cerebras-api-key <key>` |
| API | OpenAI-compatible (`openai-completions`) |
| Base URL | `https://api.cerebras.ai/v1` |
| Default model | `cerebras/zai-glm-4.7` |

## Install plugin

Cerebras is NOT bundled — it ships as an official external package. Install the plugin and then restart the Gateway so the provider registers:

```bash
openclaw plugins install @openclaw/cerebras-provider
openclaw gateway restart
```

## Getting started

First create an API key in the [Cerebras Cloud Console](https://cloud.cerebras.ai). Then resolve the `CEREBRAS_API_KEY` credential by one of three routes: interactive onboarding, the non-interactive direct flag, or an environment variable only. The interactive onboarding flow is the standard path:

```bash
openclaw onboard --auth-choice cerebras-api-key
```

The direct-flag and env-only routes (from the source `<CodeGroup>`) are: pass `--cerebras-api-key "$CEREBRAS_API_KEY"` alongside `--non-interactive --auth-choice cerebras-api-key`, or simply `export CEREBRAS_API_KEY=csk-...` before starting the Gateway. After the key is set, verify the models are visible:

```bash
openclaw models list --provider cerebras
```

The list should include all four static models. If `CEREBRAS_API_KEY` is unresolved, `openclaw models status --json` reports the missing credential under `auth.unusableProfiles`.

## Non-interactive setup

For scripted/headless onboarding, combine the non-interactive flags with an explicit `--mode local`:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice cerebras-api-key \
  --cerebras-api-key "$CEREBRAS_API_KEY"
```

## Built-in catalog

OpenClaw ships a static Cerebras catalog that mirrors the public OpenAI-compatible endpoint. **All four models share a 128k context and 8,192 max-output tokens.** The catalog (verbatim from source):

| Model ref | Name | Reasoning | Notes |
| --- | --- | --- | --- |
| `cerebras/zai-glm-4.7` | Z.ai GLM 4.7 | yes | Default model; preview reasoning model |
| `cerebras/gpt-oss-120b` | GPT OSS 120B | yes | Production reasoning model |
| `cerebras/qwen-3-235b-a22b-instruct-2507` | Qwen 3 235B Instruct | no | Preview non-reasoning model |
| `cerebras/llama3.1-8b` | Llama 3.1 8B | no | Production speed-focused model |

**Preview / deprecation caveat (source `<Warning>`):** Cerebras marks `zai-glm-4.7` and `qwen-3-235b-a22b-instruct-2507` as preview models, and `llama3.1-8b` plus `qwen-3-235b-a22b-instruct-2507` are documented for deprecation on May 27, 2026. Check Cerebras' supported-models page before relying on them for production workloads.

## Manual config

The plugin usually means you only need the API key. Use explicit `models.providers.cerebras` config when you want to override model metadata or run in `mode: "merge"` against the static catalog (verbatim JSON5 from source):

```json5
{
  env: { CEREBRAS_API_KEY: "csk-..." },
  agents: {
    defaults: {
      model: { primary: "cerebras/zai-glm-4.7" },
    },
  },
  models: {
    mode: "merge",
    providers: {
      cerebras: {
        baseUrl: "https://api.cerebras.ai/v1",
        apiKey: "${CEREBRAS_API_KEY}",
        api: "openai-completions",
        models: [
          { id: "zai-glm-4.7", name: "Z.ai GLM 4.7" },
          { id: "gpt-oss-120b", name: "GPT OSS 120B" },
        ],
      },
    },
  },
}
```

**Daemon env note (source `<Note>`):** If the Gateway runs as a daemon (launchd, systemd, Docker), make sure `CEREBRAS_API_KEY` is available to that process — for example in `~/.openclaw/.env` or through `env.shellEnv`. A key exported only in an interactive shell will not help a managed service unless the env is imported separately.

**Source**: OpenClaw documentation — `providers/cerebras` (mirror `inbox/openclaw_docs/providers/cerebras.md`)
**Last Updated**: 2026-06-22
**Status**: Active
