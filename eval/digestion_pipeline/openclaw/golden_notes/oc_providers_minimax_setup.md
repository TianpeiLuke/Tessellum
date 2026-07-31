---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - minimax
keywords:
  - openclaw minimax provider
  - minimax m3 default model
  - minimax vs minimax-portal
  - minimax oauth coding plan
  - minimax api key onboarding
  - openclaw configure minimax
  - minimax m2.x thinking disabled
  - minimax fast mode highspeed
  - minimax fallback config
  - unknown model minimax fix
topics:
  - OpenClaw
  - Providers
  - MiniMax
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/minimax
access_control_group: ["general"]
---

# OpenClaw — Configure MiniMax Chat Models

## Overview

This note is the **chat-model setup procedure** for OpenClaw's MiniMax provider, mirroring the setup half of the `providers/minimax` source page: the `minimax` (API key) vs `minimax-portal` (OAuth) provider split, the built-in chat/vision/media catalog, OAuth Coding-Plan and API-key onboarding (International vs China), the `openclaw configure` wizard, advanced configuration (config options, M2.x thinking defaults, fast mode, fallback, Coding-Plan usage), the model-ref Notes, and the "Unknown model" Troubleshooting fix. OpenClaw's MiniMax provider **defaults to MiniMax M3**. The multimodal capability surface bundled with the same provider (image generation, text-to-speech, music, video, image understanding, web search) is documented separately in **[oc_providers_minimax_media](oc_providers_minimax_media.md)**.

## Provider Split (`minimax` vs `minimax-portal`)

MiniMax exposes two bundled provider ids that differ only by auth method and a small capability difference. Model refs follow the auth path: API-key setups use `minimax/<model>`, OAuth setups use `minimax-portal/<model>`.

| Provider ID | Auth | Capabilities |
| --- | --- | --- |
| `minimax` | API key | Text, image generation, music generation, video generation, image understanding, speech, web search |
| `minimax-portal` | OAuth | Text, image generation, music generation, video generation, image understanding, speech |

(The capability difference: only the API-key `minimax` id carries `web_search`; the media capabilities themselves are documented in the media sibling note.)

## Built-in Catalog

OpenClaw ships a built-in MiniMax catalog. The chat (reasoning) models materialized by onboarding / API-key setup are `MiniMax-M3` (default), `MiniMax-M2.7`, and `MiniMax-M2.7-highspeed`; the remaining entries are the media/vision models owned elsewhere.

| Model | Type | Description |
| --- | --- | --- |
| `MiniMax-M3` | Chat (reasoning) | Default hosted reasoning model |
| `MiniMax-M2.7` | Chat (reasoning) | Previous hosted reasoning model |
| `MiniMax-M2.7-highspeed` | Chat (reasoning) | Faster M2.7 reasoning tier |
| `MiniMax-VL-01` | Vision | Image understanding model |
| `image-01` | Image generation | Text-to-image and image-to-image editing |
| `music-2.6` | Music generation | Default music model |
| `music-2.5` | Music generation | Previous music generation tier |
| `music-2.0` | Music generation | Legacy music generation tier |
| `MiniMax-Hailuo-2.3` | Video generation | Text-to-video and image reference flows |

## Getting Started

Choose your preferred auth method (OAuth Coding Plan or API key) and follow the onboarding steps. Both methods have International and China endpoint variants selected via the `--auth-choice` flag.

### OAuth (Coding Plan)

Best for quick setup with the MiniMax Coding Plan via OAuth — no API key required. OAuth setups use the `minimax-portal` provider id, and model refs follow the form `minimax-portal/MiniMax-M3`.

- **International** — `openclaw onboard --auth-choice minimax-global-oauth` (authenticates against `api.minimax.io`).
- **China** — `openclaw onboard --auth-choice minimax-cn-oauth` (authenticates against `api.minimaxi.com`).
- After onboarding, verify with `openclaw models list --provider minimax-portal`.

### API key

Best for hosted MiniMax with the Anthropic-compatible API. API-key setups use the `minimax` provider id, and model refs follow the form `minimax/MiniMax-M3`.

- **International** — `openclaw onboard --auth-choice minimax-global-api` (configures `api.minimax.io` as the base URL).
- **China** — `openclaw onboard --auth-choice minimax-cn-api` (configures `api.minimaxi.com` as the base URL).
- After onboarding, verify with `openclaw models list --provider minimax`.

The verbatim API-key config example that onboarding writes (`models.providers.minimax` with the three chat models, `api: "anthropic-messages"`, and per-model `cost`/`contextWindow`/`maxTokens`):

```json5
{
  env: { MINIMAX_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "minimax/MiniMax-M3" } } },
  models: {
    mode: "merge",
    providers: {
      minimax: {
        baseUrl: "https://api.minimax.io/anthropic",
        apiKey: "${MINIMAX_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "MiniMax-M3",
            name: "MiniMax M3",
            reasoning: true,
            input: ["text", "image"],
            cost: { input: 0.6, output: 2.4, cacheRead: 0.12, cacheWrite: 0 },
            contextWindow: 1000000,
            maxTokens: 131072,
          },
          {
            id: "MiniMax-M2.7",
            name: "MiniMax M2.7",
            reasoning: true,
            input: ["text"],
            cost: { input: 0.3, output: 1.2, cacheRead: 0.06, cacheWrite: 0.375 },
            contextWindow: 204800,
            maxTokens: 131072,
          },
          {
            id: "MiniMax-M2.7-highspeed",
            name: "MiniMax M2.7 Highspeed",
            reasoning: true,
            input: ["text"],
            cost: { input: 0.6, output: 2.4, cacheRead: 0.06, cacheWrite: 0.375 },
            contextWindow: 204800,
            maxTokens: 131072,
          },
        ],
      },
    },
  },
}
```

On the Anthropic-compatible streaming path, OpenClaw **disables MiniMax M2.x thinking by default** unless you explicitly set `thinking` yourself: M2.x's streaming endpoint emits `reasoning_content` in OpenAI-style delta chunks instead of native Anthropic thinking blocks, which can leak internal reasoning into visible output if left enabled implicitly. MiniMax-M3 (and forward-compatible M3.x) is exempt from this default — M3 emits proper Anthropic thinking blocks and requires thinking active to produce visible content, so OpenClaw keeps M3 on the provider's omitted/adaptive thinking path. (A referral link for the MiniMax Coding Plan, 10% off, is provided in the source under both Getting started and Notes — see References.)

## Configure via `openclaw configure`

Use the interactive config wizard to set MiniMax without editing JSON: run `openclaw configure`, choose **Model/auth** from the menu, pick one of the available MiniMax auth options, then select your default model when prompted. The four MiniMax auth choices are the same `--auth-choice` values the onboarding commands use:

| Auth choice | Description |
| --- | --- |
| `minimax-global-oauth` | International OAuth (Coding Plan) |
| `minimax-cn-oauth` | China OAuth (Coding Plan) |
| `minimax-global-api` | International API key |
| `minimax-cn-api` | China API key |

## Advanced Configuration

### Configuration options

The configurable `models.providers.minimax` fields (plus the `agents.defaults.models` allowlist and `models.mode`):

| Option | Description |
| --- | --- |
| `models.providers.minimax.baseUrl` | Prefer `https://api.minimax.io/anthropic` (Anthropic-compatible); `https://api.minimax.io/v1` is optional for OpenAI-compatible payloads |
| `models.providers.minimax.api` | Prefer `anthropic-messages`; `openai-completions` is optional for OpenAI-compatible payloads |
| `models.providers.minimax.apiKey` | MiniMax API key (`MINIMAX_API_KEY`) |
| `models.providers.minimax.models` | Define `id`, `name`, `reasoning`, `contextWindow`, `maxTokens`, `cost` |
| `agents.defaults.models` | Alias models you want in the allowlist |
| `models.mode` | Keep `merge` if you want to add MiniMax alongside built-ins |

### Thinking defaults

On `api: "anthropic-messages"`, OpenClaw injects `thinking: { type: "disabled" }` for MiniMax M2.x models unless thinking is already explicitly set in params/config. This prevents M2.x's streaming endpoint from emitting `reasoning_content` in OpenAI-style delta chunks, which would leak internal reasoning into visible output. MiniMax-M3 (and M3.x) is exempt: M3 emits proper Anthropic thinking blocks and returns an empty `content` array with `stop_reason: "end_turn"` when thinking is disabled, so the wrapper keeps M3 on the provider's omitted/adaptive thinking path.

### Fast mode

`/fast on` or `params.fastMode: true` rewrites `MiniMax-M2.7` to `MiniMax-M2.7-highspeed` on the Anthropic-compatible stream path.

### Fallback example

Best for keeping your strongest latest-generation model as primary and failing over to MiniMax M2.7. The source example uses Opus as a concrete primary; swap to your preferred latest-gen primary model.

```json5
{
  env: { MINIMAX_API_KEY: "sk-..." },
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "primary" },
        "minimax/MiniMax-M2.7": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["minimax/MiniMax-M2.7"],
      },
    },
  },
}
```

### Coding Plan usage details

- Coding Plan usage API: `https://api.minimaxi.com/v1/token_plan/remains` or `https://api.minimax.io/v1/token_plan/remains` (requires a coding plan key).
- Usage polling derives the host from `models.providers.minimax-portal.baseUrl` or `models.providers.minimax.baseUrl` when configured, so global setups using `https://api.minimax.io/anthropic` poll `api.minimax.io`. Missing or malformed base URLs keep the CN fallback for compatibility.
- OpenClaw normalizes MiniMax coding-plan usage to the same `% left` display used by other providers. MiniMax's raw `usage_percent` / `usagePercent` fields are remaining quota, not consumed quota, so OpenClaw inverts them. Count-based fields win when present.
- When the API returns `model_remains`, OpenClaw prefers the chat-model entry, derives the window label from `start_time` / `end_time` when needed, and includes the selected model name in the plan label so coding-plan windows are easier to distinguish.
- Usage snapshots treat `minimax`, `minimax-cn`, and `minimax-portal` as the same MiniMax quota surface, and prefer stored MiniMax OAuth before falling back to Coding Plan key env vars.

## Notes

- Model refs follow the auth path: API-key setup `minimax/<model>`; OAuth setup `minimax-portal/<model>`.
- Default chat model: `MiniMax-M3`. Alternate chat models: `MiniMax-M2.7`, `MiniMax-M2.7-highspeed`.
- Onboarding and direct API-key setup write model definitions for M3 and both M2.7 variants.
- Image understanding uses the plugin-owned `MiniMax-VL-01` media provider (documented in the media sibling note).
- Update pricing values in `models.json` if you need exact cost tracking.
- Use `openclaw models list` to confirm the current provider id, then switch with `openclaw models set minimax/MiniMax-M3` or `openclaw models set minimax-portal/MiniMax-M3`.

## Troubleshooting

**"Unknown model: minimax/MiniMax-M3"** — this usually means the **MiniMax provider is not configured** (no matching provider entry and no MiniMax auth profile/env key found). A fix for this detection is in **2026.1.12**. Fix by: upgrading to **2026.1.12** (or run from source `main`), then restarting the gateway; running `openclaw configure` and selecting a **MiniMax** auth option; adding the matching `models.providers.minimax` or `models.providers.minimax-portal` block manually; or setting `MINIMAX_API_KEY`, `MINIMAX_OAUTH_TOKEN`, or a MiniMax auth profile so the matching provider can be injected. Make sure the model id is **case-sensitive** — API-key path: `minimax/MiniMax-M3`, `minimax/MiniMax-M2.7`, or `minimax/MiniMax-M2.7-highspeed`; OAuth path: `minimax-portal/MiniMax-M3`, `minimax-portal/MiniMax-M2.7`, or `minimax-portal/MiniMax-M2.7-highspeed`. Then recheck with `openclaw models list`.

**Source**: OpenClaw documentation — `providers/minimax` (mirror `inbox/openclaw_docs/providers/minimax.md`)
**Last Updated**: 2026-06-22
**Status**: Active
