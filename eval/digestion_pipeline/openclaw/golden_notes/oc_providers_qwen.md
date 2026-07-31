---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - qwen
keywords:
  - openclaw qwen provider
  - qwen-provider plugin install
  - qwen coding plan standard endpoint
  - dashscope modelstudio compatibility alias
  - qwen built-in catalog model refs
  - enable_thinking dashscope flag
  - qwen-vl video understanding wan video generation
  - QWEN_API_KEY DASHSCOPE_API_KEY auth choice
topics:
  - OpenClaw
  - Providers
  - Qwen
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/qwen
access_control_group: ["general"]
---

# OpenClaw — Configuring the Qwen Provider

## Overview

This note is the setup procedure for the first-class OpenClaw `qwen` provider plugin, mirroring the `providers/qwen` source page. It covers installing `@openclaw/qwen-provider`, onboarding across the three plan types (Coding Plan subscription, Standard pay-as-you-go, and Qwen OAuth / Portal) and the China/Global endpoints, setting a default model, the endpoint table, the built-in static catalog, the `enable_thinking` mapping, the multimodal add-ons (Qwen-VL understanding and Wan video generation), and the advanced-configuration accordions. The provider targets Qwen Cloud / Alibaba DashScope and Coding Plan endpoints, keeps legacy `modelstudio` ids working as a compatibility alias, and also exposes the Qwen Portal token flow as provider `qwen-oauth` (documented in its own note).

## Provider Summary

OpenClaw treats Qwen as a first-class provider plugin with canonical id `qwen`. The header facts from the source page:

- Provider: `qwen`
- Portal provider: `qwen-oauth` (separate page)
- Preferred env var: `QWEN_API_KEY`
- Also accepted for compatibility: `MODELSTUDIO_API_KEY`, `DASHSCOPE_API_KEY`
- API style: OpenAI-compatible

A source `<Tip>` advises that if you want `qwen3.6-plus`, prefer the **Standard (pay-as-you-go)** endpoint, because Coding Plan support can lag behind the public catalog.

## Install plugin

Install the official plugin, then restart Gateway:

```bash
openclaw plugins install @openclaw/qwen-provider
openclaw gateway restart
```

## Getting started

Choose your plan type and follow the setup steps. The source page presents three tabs.

**Coding Plan (subscription)** — best for subscription-based access through the Qwen Coding Plan. Get or copy an API key from `home.qwencloud.com/api-keys`, then run onboarding for your region. For the **Global** endpoint run `openclaw onboard --auth-choice qwen-api-key`; for the **China** endpoint run `openclaw onboard --auth-choice qwen-api-key-cn`. Then set a default model and verify it is available:

```json5
{
  agents: {
    defaults: {
      model: { primary: "qwen/qwen3.5-plus" },
    },
  },
}
```

Verify with `openclaw models list --provider qwen`.

**Standard (pay-as-you-go)** — best for pay-as-you-go access through the Standard Model Studio endpoint, including models like `qwen3.6-plus` that may not be available on the Coding Plan. The flow is identical (get API key → onboard → set default model `qwen/qwen3.5-plus` → verify with `openclaw models list --provider qwen`), but the onboarding auth-choice differs: **Global** is `openclaw onboard --auth-choice qwen-standard-api-key` and **China** is `openclaw onboard --auth-choice qwen-standard-api-key-cn`.

Both the Coding Plan and Standard tabs carry the same `<Note>`: legacy `modelstudio-*` auth-choice ids and `modelstudio/...` model refs still work as compatibility aliases, but new setup flows should prefer the canonical `qwen-*` auth-choice ids and `qwen/...` model refs. If you define an exact custom `models.providers.modelstudio` entry with another `api` value, that custom provider owns `modelstudio/...` refs instead of the Qwen compatibility alias.

**Qwen OAuth / Portal** — best for a Qwen Portal token against `https://portal.qwen.ai/v1`; see the dedicated `qwen-oauth` provider page for migration notes. Provide your portal token with `openclaw onboard --auth-choice qwen-oauth`, set the default model to `qwen-oauth/qwen3.5-plus`, and verify with `openclaw models list --provider qwen-oauth`. A `<Note>` clarifies that `qwen-oauth` uses the same `QWEN_API_KEY` env var name as the DashScope provider, but stores auth under the `qwen-oauth` provider id when configured through OpenClaw onboarding.

## Plan types and endpoints

The provider auto-selects the endpoint based on your auth choice. Canonical choices use the `qwen-*` family; `modelstudio-*` remains compatibility-only. You can override with a custom `baseUrl` in config.

| Plan | Region | Auth choice | Endpoint |
| --- | --- | --- | --- |
| Standard (pay-as-you-go) | China | `qwen-standard-api-key-cn` | `dashscope.aliyuncs.com/compatible-mode/v1` |
| Standard (pay-as-you-go) | Global | `qwen-standard-api-key` | `dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| Coding Plan (subscription) | China | `qwen-api-key-cn` | `coding.dashscope.aliyuncs.com/v1` |
| Coding Plan (subscription) | Global | `qwen-api-key` | `coding-intl.dashscope.aliyuncs.com/v1` |
| Qwen Portal | Global | `qwen-oauth` | `portal.qwen.ai/v1` |

A source `<Tip>` points to key management at `home.qwencloud.com/api-keys` and docs at `docs.qwencloud.com`.

## Built-in catalog

OpenClaw currently ships a Qwen static catalog. The configured catalog is endpoint-aware: Coding Plan configs omit models that are only known to work on the Standard endpoint. Availability can still vary by endpoint and billing plan even when a model is present in the static catalog.

| Model ref | Input | Context | Notes |
| --- | --- | --- | --- |
| `qwen/qwen3.5-plus` | text, image | 1,000,000 | Default model |
| `qwen/qwen3.6-plus` | text, image | 1,000,000 | Prefer Standard endpoints when you need this model |
| `qwen/qwen3-max-2026-01-23` | text | 262,144 | Qwen Max line |
| `qwen/qwen3-coder-next` | text | 262,144 | Coding |
| `qwen/qwen3-coder-plus` | text | 1,000,000 | Coding |
| `qwen/MiniMax-M2.5` | text | 1,000,000 | Reasoning enabled |
| `qwen/glm-5` | text | 202,752 | GLM |
| `qwen/glm-4.7` | text | 202,752 | GLM |
| `qwen/kimi-k2.5` | text, image | 262,144 | Moonshot AI via Alibaba |
| `qwen-oauth/qwen3.5-plus` | text, image | 1,000,000 | Qwen Portal default |

## Thinking Controls

For reasoning-enabled Qwen Cloud models, the provider maps OpenClaw thinking levels to DashScope's top-level `enable_thinking` request flag. Disabled thinking sends `enable_thinking: false`; other thinking levels send `enable_thinking: true`.

## Multimodal add-ons

The `qwen` plugin also exposes multimodal capabilities on the **Standard** DashScope endpoints (not the Coding Plan endpoints): **Video understanding** via `qwen-vl-max-latest`, and **Wan video generation** via `wan2.6-t2v` (default), `wan2.6-i2v`, `wan2.6-r2v`, `wan2.6-r2v-flash`, and `wan2.7-r2v`. To use Qwen as the default video provider, set the default video generation model:

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: { primary: "qwen/wan2.6-t2v" },
    },
  },
}
```

A `<Note>` points to the Video Generation tool page for shared tool parameters, provider selection, and failover behavior.

## Advanced configuration

The source `<AccordionGroup>` contains six accordions, distilled below.

**Image and video understanding** — the Qwen plugin registers media understanding for images and video on the **Standard** DashScope endpoints (not the Coding Plan endpoints), using model `qwen-vl-max-latest` with supported input "Images, video". Media understanding is auto-resolved from the configured Qwen auth — no additional config is needed; ensure you are using a Standard (pay-as-you-go) endpoint for media understanding support.

**Qwen 3.6 Plus availability** — `qwen3.6-plus` is available on the Standard (pay-as-you-go) Model Studio endpoints (China: `dashscope.aliyuncs.com/compatible-mode/v1`; Global: `dashscope-intl.aliyuncs.com/compatible-mode/v1`). If the Coding Plan endpoints return an "unsupported model" error for `qwen3.6-plus`, switch to Standard (pay-as-you-go) instead of the Coding Plan endpoint/key pair. OpenClaw's Qwen static catalog does not advertise `qwen3.6-plus` on Coding Plan endpoints, but explicitly configured `qwen/qwen3.6-plus` entries under `models.providers.qwen.models` are honored on Coding Plan baseUrls so you can opt that model in if Aliyun enables it on your subscription — the upstream API still decides whether the call succeeds.

**Capability plan** — the `qwen` plugin is being positioned as the vendor home for the full Qwen Cloud surface, not just coding/text models: text/chat models are available through the plugin; tool calling, structured output, and thinking are inherited from the OpenAI-compatible transport; image generation is planned at the provider-plugin layer; image/video understanding is available through the plugin on the Standard endpoint; speech/audio is planned at the provider-plugin layer; memory embeddings/reranking is planned through the embedding adapter surface; and video generation is available through the plugin through the shared video-generation capability.

**Video generation details** — for video generation, OpenClaw maps the configured Qwen region to the matching DashScope AIGC host before submitting the job (Global/Intl: `https://dashscope-intl.aliyuncs.com`; China: `https://dashscope.aliyuncs.com`), so a normal `models.providers.qwen.baseUrl` pointing at either the Coding Plan or Standard Qwen hosts still keeps video generation on the correct regional DashScope video endpoint. Current Qwen video-generation limits: up to **1** output video per request, up to **1** input image, up to **4** input videos, up to **10 seconds** duration; it supports `size`, `aspectRatio`, `resolution`, `audio`, and `watermark`. Reference image/video mode currently requires **remote http(s) URLs** — local file paths are rejected up front because the DashScope video endpoint does not accept uploaded local buffers for those references.

**Streaming usage compatibility** — native Model Studio endpoints advertise streaming usage compatibility on the shared `openai-completions` transport. OpenClaw keys that off endpoint capabilities now, so DashScope-compatible custom provider ids targeting the same native hosts inherit the same streaming-usage behavior instead of requiring the built-in `qwen` provider id specifically. Native-streaming usage compatibility applies to both the Coding Plan hosts (`https://coding.dashscope.aliyuncs.com/v1`, `https://coding-intl.dashscope.aliyuncs.com/v1`) and the Standard DashScope-compatible hosts (`https://dashscope.aliyuncs.com/compatible-mode/v1`, `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`).

**Multimodal endpoint regions** — multimodal surfaces (video understanding and Wan video generation) use the **Standard** DashScope endpoints, not the Coding Plan endpoints (Global/Intl Standard base URL: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`; China Standard base URL: `https://dashscope.aliyuncs.com/compatible-mode/v1`).

**Environment and daemon setup** — if the Gateway runs as a daemon (launchd/systemd), make sure `QWEN_API_KEY` is available to that process (for example, in `~/.openclaw/.env` or via `env.shellEnv`).

**Source**: OpenClaw documentation — `providers/qwen` (mirror `inbox/openclaw_docs/providers/qwen.md`)
**Last Updated**: 2026-06-22
**Status**: Active
