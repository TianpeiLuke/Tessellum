---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - xiaomi
keywords:
  - openclaw xiaomi mimo provider
  - xiaomi pay-as-you-go sk key
  - xiaomi-token-plan tp key regional
  - mimo v2 v2.5 model catalog
  - xiaomi mimo tts speech provider
  - openai-completions provider config
  - openclaw models list provider xiaomi
  - xiaomi auth env vars daemon
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/xiaomi
access_control_group: ["general"]
---

# OpenClaw — Configuring the Xiaomi MiMo Provider

## Overview

This note is the procedure for wiring **Xiaomi MiMo** into OpenClaw, mirroring the `providers/xiaomi` source page. Xiaomi MiMo is the API platform for MiMo models, and OpenClaw ships a bundled Xiaomi plugin (`enabledByDefault: true`) that registers two text-provider presets — `xiaomi` for pay-as-you-go keys (`sk-...`) and `xiaomi-token-plan` for Token Plan keys (`tp-...`) with regional endpoint presets — plus the `xiaomi` speech (TTS) provider. It covers getting the right key, running onboarding, verifying model availability, the pay-as-you-go and Token Plan model catalogs, the chat-completions-based TTS contract, the full `openai-completions` config blocks for both presets, and the auto-injection / model-detail / troubleshooting accordions.

## Provider Summary (header property table)

The two presets and the speech provider all come from the one bundled plugin. The source header table records the load-bearing properties used throughout setup:

- **Provider ids** — `xiaomi` (pay-as-you-go) and `xiaomi-token-plan` (Token Plan).
- **Plugin** — bundled, `enabledByDefault: true`.
- **Auth env vars** — `XIAOMI_API_KEY`, `XIAOMI_TOKEN_PLAN_API_KEY`.
- **Onboarding flags** — `--auth-choice xiaomi-api-key`, `--auth-choice xiaomi-token-plan-cn`, `--auth-choice xiaomi-token-plan-sgp`, `--auth-choice xiaomi-token-plan-ams`.
- **Direct CLI flags** — `--xiaomi-api-key <key>`, `--xiaomi-token-plan-api-key <key>`.
- **Contracts** — chat completions + `speechProviders`.
- **API** — OpenAI-compatible (`openai-completions`).
- **Base URLs** — Pay-as-you-go: `https://api.xiaomimimo.com/v1`; Token Plan presets: `token-plan-{cn,sgp,ams}...`.
- **Default models** — `xiaomi/mimo-v2-flash`, `xiaomi-token-plan/mimo-v2.5-pro`.
- **TTS default** — `mimo-v2.5-tts`, voice `mimo_default`; voicedesign model `mimo-v2.5-tts-voicedesign`.

## Getting started

The setup is a three-step flow (get the key, onboard, verify):

1. **Get the right key** — create a pay-as-you-go key in the Xiaomi MiMo console (`https://platform.xiaomimimo.com/#/console/api-keys`), or open your Token Plan subscription page and copy the regional OpenAI-compatible base URL plus the matching `tp-...` key.
2. **Run onboarding** — pick the auth choice for your key type; you can pass the key directly with `--xiaomi-api-key` / `--xiaomi-token-plan-api-key` instead of relying on the env var.
3. **Verify the model is available** — list each provider's models to confirm the plugin registered them.

```bash
openclaw onboard --auth-choice xiaomi-api-key
openclaw onboard --auth-choice xiaomi-token-plan-sgp

openclaw onboard --auth-choice xiaomi-api-key --xiaomi-api-key "$XIAOMI_API_KEY"
openclaw onboard --auth-choice xiaomi-token-plan-sgp --xiaomi-token-plan-api-key "$XIAOMI_TOKEN_PLAN_API_KEY"

openclaw models list --provider xiaomi
openclaw models list --provider xiaomi-token-plan
```

## Pay-as-you-go catalog

The `xiaomi` (pay-as-you-go) preset registers three MiMo V2 models. The default model ref is `xiaomi/mimo-v2-flash`, and the provider is injected automatically when `XIAOMI_API_KEY` is set or an auth profile exists.

| Model ref | Input | Context | Max output | Reasoning | Notes |
| --- | --- | --- | --- | --- | --- |
| `xiaomi/mimo-v2-flash` | text | 262,144 | 8,192 | No | Default model |
| `xiaomi/mimo-v2-pro` | text | 1,048,576 | 32,000 | Yes | Large context |
| `xiaomi/mimo-v2-omni` | text, image | 262,144 | 32,000 | Yes | Multimodal |

## Token Plan catalog

For Token Plan keys, choose the `xiaomi-token-plan-*` auth choice whose region matches the base URL shown in Xiaomi's subscription UI. The three regional presets map to fixed base URLs:

- `xiaomi-token-plan-cn` -> `https://token-plan-cn.xiaomimimo.com/v1`
- `xiaomi-token-plan-sgp` -> `https://token-plan-sgp.xiaomimimo.com/v1`
- `xiaomi-token-plan-ams` -> `https://token-plan-ams.xiaomimimo.com/v1`

| Model ref | Input | Context | Max output | Reasoning | Notes |
| --- | --- | --- | --- | --- | --- |
| `xiaomi-token-plan/mimo-v2.5-pro` | text | 1,048,576 | 32,000 | Yes | Default model |
| `xiaomi-token-plan/mimo-v2.5` | text, image | 1,048,576 | 32,000 | Yes | Multimodal |

Token Plan onboarding validates the key shape and warns when a `tp-...` key is entered into the pay-as-you-go path, or an `sk-...` key is entered into the Token Plan path.

## Text-to-speech

The bundled `xiaomi` plugin also registers Xiaomi MiMo as a speech provider for `messages.tts`. It calls Xiaomi's chat-completions TTS contract with the text as an `assistant` message and optional style guidance as a `user` message. The TTS id is `xiaomi` (`mimo` alias), auth is `XIAOMI_API_KEY`, the API is `POST /v1/chat/completions` with `audio`, the default is `mimo-v2.5-tts` with voice `mimo_default`, and output is MP3 by default (WAV when configured). Supported built-in voices include `mimo_default`, `default_zh`, `default_en`, `Mia`, `Chloe`, `Milo`, and `Dean`. Preset-voice models use `audio.voice`, so OpenClaw sends `speakerVoice` for `mimo-v2.5-tts` and `mimo-v2-tts`.

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "xiaomi",
      providers: {
        xiaomi: {
          apiKey: "xiaomi_api_key",
          model: "mimo-v2.5-tts",
          speakerVoice: "mimo_default",
          format: "mp3",
          style: "Bright, natural, conversational tone.",
        },
      },
    },
  },
}
```

Xiaomi's voicedesign model, `mimo-v2.5-tts-voicedesign`, generates the voice from a natural-language style prompt instead of a preset voice id. Configure `style` with the desired voice description; OpenClaw sends it as the `user` message, sends the spoken text as the `assistant` message, and omits `audio.voice` for this model. For voice-note targets such as Feishu and Telegram, OpenClaw transcodes Xiaomi output to 48kHz Opus with `ffmpeg` before delivery.

```json5
{
  messages: {
    tts: {
      provider: "xiaomi",
      providers: {
        xiaomi: {
          model: "mimo-v2.5-tts-voicedesign",
          format: "wav",
          style: "Warm, natural female voice with clear pronunciation.",
        },
      },
    },
  },
}
```

## Config example (explicit provider blocks)

For explicit (non-onboarding) configuration, declare the provider with its `baseUrl`, `api: "openai-completions"`, `apiKey` (the env-var name to read), and the `models[]` rows. Pricing and compat flags come from the bundled plugin manifest, so the config examples omit `cost` and `compat` to avoid diverging from runtime behavior. The pay-as-you-go block:

```json5
{
  env: { XIAOMI_API_KEY: "your-key" },
  agents: { defaults: { model: { primary: "xiaomi/mimo-v2-flash" } } },
  models: {
    mode: "merge",
    providers: {
      xiaomi: {
        baseUrl: "https://api.xiaomimimo.com/v1",
        api: "openai-completions",
        apiKey: "XIAOMI_API_KEY",
        models: [
          { id: "mimo-v2-flash", name: "Xiaomi MiMo V2 Flash", reasoning: false, input: ["text"], contextWindow: 262144, maxTokens: 8192 },
          { id: "mimo-v2-pro", name: "Xiaomi MiMo V2 Pro", reasoning: true, input: ["text"], contextWindow: 1048576, maxTokens: 32000 },
          { id: "mimo-v2-omni", name: "Xiaomi MiMo V2 Omni", reasoning: true, input: ["text", "image"], contextWindow: 262144, maxTokens: 32000 },
        ],
      },
    },
  },
}
```

The Token Plan block selects a regional `baseUrl` (here `sgp`) and reads `XIAOMI_TOKEN_PLAN_API_KEY`; its manifest pricing includes tiered cache-read pricing, so the example again omits `cost`:

```json5
{
  env: { XIAOMI_TOKEN_PLAN_API_KEY: "tp-your-key" },
  agents: { defaults: { model: { primary: "xiaomi-token-plan/mimo-v2.5-pro" } } },
  models: {
    mode: "merge",
    providers: {
      "xiaomi-token-plan": {
        baseUrl: "https://token-plan-sgp.xiaomimimo.com/v1",
        api: "openai-completions",
        apiKey: "XIAOMI_TOKEN_PLAN_API_KEY",
        models: [
          { id: "mimo-v2.5-pro", name: "Xiaomi MiMo V2.5 Pro", reasoning: true, input: ["text"], contextWindow: 1048576, maxTokens: 32000 },
          { id: "mimo-v2.5", name: "Xiaomi MiMo V2.5", reasoning: true, input: ["text", "image"], contextWindow: 1048576, maxTokens: 32000 },
        ],
      },
    },
  },
}
```

### Auto-injection behavior

The `xiaomi` provider is injected automatically when `XIAOMI_API_KEY` is set in your environment or an auth profile exists. `xiaomi-token-plan` needs a regional base URL, so the supported path is the bundled Token Plan onboarding choice or an explicit `models.providers.xiaomi-token-plan` config block.

### Model details

- **mimo-v2-flash** — lightweight and fast, ideal for general-purpose text tasks; no reasoning support.
- **mimo-v2-pro** — supports reasoning with a 1M token context window for long-document workloads.
- **mimo-v2-omni** — reasoning-enabled multimodal model that accepts both text and image inputs.
- **mimo-v2.5-pro** — Token Plan default with Xiaomi's current V2.5 reasoning stack.
- **mimo-v2.5** — Token Plan multimodal V2.5 route.

Pay-as-you-go models use the `xiaomi/` prefix; Token Plan models use the `xiaomi-token-plan/` prefix.

### Troubleshooting

- If models do not appear, confirm the relevant key env var or auth profile is present and valid.
- For Token Plan, confirm the chosen onboarding region matches the subscription page base URL and that the key starts with `tp-`.
- When the Gateway runs as a daemon, ensure the key is available to that process (for example in `~/.openclaw/.env` or via `env.shellEnv`). Keys set only in your interactive shell are not visible to daemon-managed gateway processes; use `~/.openclaw/.env` or `env.shellEnv` config for persistent availability.

**Source**: OpenClaw documentation — `providers/xiaomi` (mirror `inbox/openclaw_docs/providers/xiaomi.md`)
**Last Updated**: 2026-06-22
**Status**: Active
