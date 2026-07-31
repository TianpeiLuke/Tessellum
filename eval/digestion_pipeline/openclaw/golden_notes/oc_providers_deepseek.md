---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - deepseek
keywords:
  - openclaw deepseek provider
  - deepseek-provider plugin
  - deepseek_api_key onboarding
  - deepseek v4 flash pro chat reasoner
  - reasoning_content replay
  - deepseek thinking reasoning_effort
  - openai-compatible deepseek api
  - models list provider deepseek
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/deepseek
access_control_group: ["general"]
---

# OpenClaw — Configure the DeepSeek Provider

## Overview

This note is the procedure for wiring the native **DeepSeek** model provider into OpenClaw, mirroring the `providers/deepseek` source page. DeepSeek serves powerful AI models through an OpenAI-compatible API at base URL `https://api.deepseek.com`, registered under provider id `deepseek` and authenticated with the `DEEPSEEK_API_KEY` environment variable. The procedure covers installing the official `@openclaw/deepseek-provider` plugin, onboarding interactively or non-interactively, verifying the built-in V4 Flash / Pro / Chat / Reasoner catalog, the V4 `thinking` + `reasoning_content` replay contract that lets thinking sessions continue across tool calls, a live-test smoke check, and a minimal config block.

## Install plugin

Install the official plugin, then restart Gateway so it loads:

```bash
openclaw plugins install @openclaw/deepseek-provider
openclaw gateway restart
```

## Getting started

Three steps take you from a fresh DeepSeek account to a working default model:

1. **Get your API key** — create an API key at `platform.deepseek.com` (the `platform.deepseek.com/api_keys` page).
2. **Run onboarding** — `openclaw onboard --auth-choice deepseek-api-key`. This prompts for your API key and sets `deepseek/deepseek-v4-flash` as the default model.
3. **Verify models are available** — `openclaw models list --provider deepseek`. To inspect the plugin's static catalog without requiring a running Gateway, use `openclaw models list --all --provider deepseek`.

For scripted or headless installations, pass all flags directly in a single non-interactive onboarding call:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice deepseek-api-key \
  --deepseek-api-key "$DEEPSEEK_API_KEY" \
  --skip-health \
  --accept-risk
```

If the Gateway runs as a daemon (launchd/systemd), make sure `DEEPSEEK_API_KEY` is available to that process — for example in `~/.openclaw/.env` or via `env.shellEnv`.

## Built-in catalog

The plugin seeds a static catalog of four DeepSeek model refs. All four take `text` input only:

| Model ref | Name | Input | Context | Max output | Notes |
| --------- | ---- | ----- | ------- | ---------- | ----- |
| `deepseek/deepseek-v4-flash` | DeepSeek V4 Flash | text | 1,000,000 | 384,000 | Default model; V4 thinking-capable surface |
| `deepseek/deepseek-v4-pro` | DeepSeek V4 Pro | text | 1,000,000 | 384,000 | V4 thinking-capable surface |
| `deepseek/deepseek-chat` | DeepSeek Chat | text | 131,072 | 8,192 | DeepSeek V3.2 non-thinking surface |
| `deepseek/deepseek-reasoner` | DeepSeek Reasoner | text | 131,072 | 65,536 | Reasoning-enabled V3.2 surface |

V4 models support DeepSeek's `thinking` control, and OpenClaw also replays DeepSeek `reasoning_content` on follow-up turns so thinking sessions with tool calls can continue. Use `/think xhigh` or `/think max` with DeepSeek V4 models to request DeepSeek's maximum `reasoning_effort`.

## Thinking and tools

DeepSeek V4 thinking sessions have a stricter replay contract than most OpenAI-compatible providers: after a thinking-enabled turn uses tools, DeepSeek expects replayed assistant messages from that turn to include `reasoning_content` on follow-up requests. OpenClaw handles this inside the DeepSeek plugin, so normal multi-turn tool use works with `deepseek/deepseek-v4-flash` and `deepseek/deepseek-v4-pro`.

If you switch an existing session from another OpenAI-compatible provider to a DeepSeek V4 model, older assistant tool-call turns may not have native DeepSeek `reasoning_content`. OpenClaw fills that missing field on replayed assistant messages for DeepSeek V4 thinking requests so the provider can accept the history without requiring `/new`.

When thinking is disabled in OpenClaw (including the UI **None** selection), OpenClaw sends DeepSeek `thinking: { type: "disabled" }` and strips replayed `reasoning_content` from the outgoing history. This keeps disabled-thinking sessions on the non-thinking DeepSeek path.

Use `deepseek/deepseek-v4-flash` for the default fast path. Use `deepseek/deepseek-v4-pro` when you want the stronger V4 model and can accept higher cost or latency.

## Live testing

The direct live model suite includes DeepSeek V4 in the modern model set. To run only the DeepSeek V4 direct-model checks:

```bash
OPENCLAW_LIVE_PROVIDERS=deepseek \
OPENCLAW_LIVE_MODELS="deepseek/deepseek-v4-flash,deepseek/deepseek-v4-pro" \
pnpm test:live src/agents/models.profiles.live.test.ts
```

That live check verifies both V4 models can complete and that thinking/tool follow-up turns preserve the replay payload DeepSeek requires.

## Config example

A minimal config sets the API key in `env` and selects a DeepSeek V4 ref as the agents' primary model:

```json5
{
  env: { DEEPSEEK_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "deepseek/deepseek-v4-flash" },
    },
  },
}
```

**Source**: OpenClaw documentation — `providers/deepseek` (mirror `inbox/openclaw_docs/providers/deepseek.md`)
**Last Updated**: 2026-06-22
**Status**: Active
