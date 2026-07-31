---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - openrouter
keywords:
  - openclaw openrouter provider
  - openrouter unified api
  - openrouter pkce oauth onboarding
  - openrouter/<provider>/<model> ref
  - openrouter fusion router
  - openrouter image video music generation
  - openrouter tts stt
  - openrouter response caching
  - openrouter provider routing metadata
  - openrouter app-attribution headers
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/openrouter
access_control_group: ["general"]
---

# OpenClaw — Configuring the OpenRouter Aggregator Provider

## Overview

This note is the procedure for connecting OpenClaw to **OpenRouter**, a unified, OpenAI-compatible API that routes requests to many upstream models behind a single endpoint and API key. It mirrors the `providers/openrouter` source page end to end: PKCE-OAuth vs manual API-key onboarding, the config example, the `openrouter/<provider>/<model>` ref pattern, OpenRouter as a backend for the `image_generate` / `video_generate` / `music_generate` / TTS / STT media tools, the Fusion parallel-panel-and-judge router, app-attribution headers, and the advanced-configuration knobs (response caching, Anthropic cache markers and reasoning prefill, thinking/reasoning injection, DeepSeek V4 reasoning replay, OpenAI-only shaping that is NOT forwarded, Gemini-backed routes, and provider-routing metadata).

## Getting started (OAuth or API key)

OpenRouter can be onboarded two ways. **OAuth** runs `openclaw onboard --auth-choice openrouter-oauth`: OpenClaw opens OpenRouter's browser sign-in flow, exchanges the PKCE code for an OpenRouter API key, and stores that key in the default OpenRouter auth profile. On remote/headless hosts, OpenClaw prints the sign-in URL and asks you to paste the redirect URL after signing in. **API key** runs `openclaw onboard --auth-choice openrouter-api-key` after you create a key at `openrouter.ai/keys`. Either path defaults to `openrouter/auto`; pick a concrete model later with `openclaw models set openrouter/<provider>/<model>`.

## Config example

The minimal configuration sets the env key and the default model ref:

```json5
{
  env: { OPENROUTER_API_KEY: "sk-or-..." },
  agents: {
    defaults: {
      model: { primary: "openrouter/auto" },
    },
  },
}
```

## Model references

Model refs follow the pattern `openrouter/<provider>/<model>`; the full provider/model list lives at `/concepts/model-providers`. Bundled fallback examples include `openrouter/auto` (OpenRouter automatic routing), `openrouter/openrouter/fusion` (the Fusion router), and `openrouter/moonshotai/kimi-k2.6` / `openrouter/moonshotai/kimi-k2.5` (Kimi K2.6 / K2.5 via MoonshotAI).

## Media generation (image / video / music)

OpenRouter can back OpenClaw's media-generation tools. For **image**, set `agents.defaults.imageGenerationModel.primary` to an OpenRouter image model; OpenClaw sends image requests to OpenRouter's chat completions image API with `modalities: ["image", "text"]`, and Gemini image models receive supported `aspectRatio` and `resolution` hints through OpenRouter's `image_config`. Use `agents.defaults.imageGenerationModel.timeoutMs` for slower models, though the `image_generate` tool's per-call `timeoutMs` parameter still wins.

```json5
{
  env: { OPENROUTER_API_KEY: "sk-or-..." },
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "openrouter/google/gemini-3.1-flash-image-preview",
        timeoutMs: 180_000,
      },
    },
  },
}
```

For **video**, set `agents.defaults.videoGenerationModel.primary` (e.g. `openrouter/google/veo-3.1-fast`). OpenClaw submits text-to-video and image-to-video jobs through OpenRouter's asynchronous `/videos` API, polls the returned `polling_url`, and downloads the completed video from OpenRouter's `unsigned_urls` or the documented job content endpoint. Reference images are sent as first/last frame images by default; images tagged with `reference_image` are sent as OpenRouter input references. The bundled `google/veo-3.1-fast` default advertises the supported 4/6/8 second durations, `720P`/`1080P` resolutions, and `16:9`/`9:16` aspect ratios. Video-to-video is not registered for OpenRouter because the upstream API currently accepts only text and image references. For **music**, set `agents.defaults.musicGenerationModel.primary`; the bundled OpenRouter music provider defaults to `google/lyria-3-pro-preview` and also exposes `google/lyria-3-clip-preview`. OpenClaw sends `modalities: ["text", "audio"]`, enables streaming, collects the streamed audio chunks, and saves the result as generated media for channel delivery; reference images are accepted for Lyria models through the shared `music_generate image=...` parameter.

## Text-to-speech and speech-to-text

OpenRouter is usable as a **TTS** provider through its OpenAI-compatible `/audio/speech` endpoint, configured under `messages.tts`. If `messages.tts.providers.openrouter.apiKey` is omitted, TTS reuses `models.providers.openrouter.apiKey`, then `OPENROUTER_API_KEY`.

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "openrouter",
      providers: {
        openrouter: {
          model: "hexgrad/kokoro-82m",
          speakerVoice: "af_alloy",
          responseFormat: "mp3",
        },
      },
    },
  },
}
```

For **STT (inbound audio)**, OpenRouter transcribes inbound voice/audio attachments through the shared `tools.media.audio` path using its STT endpoint (`/audio/transcriptions`) — applying to any channel plugin that forwards inbound voice/audio into media-understanding preflight. Configure it with `tools.media.audio.models` entries such as `{ provider: "openrouter", model: "openai/whisper-large-v3-turbo" }`. OpenClaw sends OpenRouter STT requests as JSON with base64 audio under `input_audio` (the OpenRouter STT contract), not as multipart OpenAI form uploads.

## Fusion router

Use OpenRouter **Fusion** when you want one OpenClaw model ref to ask several OpenRouter models in parallel, have OpenRouter judge their answers, and return a single final response through the normal OpenRouter provider endpoint. Because the upstream model slug is `openrouter/fusion`, the OpenClaw ref includes both the OpenClaw provider prefix and the upstream namespace: `openclaw models set openrouter/openrouter/fusion`. Configure Fusion's panel and judge through the model's `params.extraBody`, which is forwarded into the OpenRouter chat-completions request body. The `analysis_models` list is the parallel panel, and `model` inside the Fusion plugin config is the judge model. Fusion works with either OAuth or API-key onboarding; with OAuth, omit the `env.OPENROUTER_API_KEY` line.

```json5
{
  agents: {
    defaults: {
      model: { primary: "openrouter/openrouter/fusion" },
      models: {
        "openrouter/openrouter/fusion": {
          params: {
            extraBody: {
              plugins: [
                {
                  id: "fusion",
                  analysis_models: [
                    "google/gemini-3.5-flash",
                    "moonshotai/kimi-k2.6",
                    "deepseek/deepseek-v4-pro",
                  ],
                  model: "google/gemini-3.5-flash",
                },
              ],
            },
          },
        },
      },
    },
  },
}
```

Do not set top-level `tool_choice` to `"required"` in normal OpenClaw agent/chat turns to try to force Fusion; OpenClaw turns may include OpenClaw tool definitions, and a top-level required tool choice can require one of those tools instead of the Fusion router. When the Fusion plugin config is present, OpenClaw also adds a sanitized system-prompt note with the configured analysis models and judge model so the agent can answer questions about its current Fusion panel; other `extraBody` fields are not copied into the prompt. Fusion is slower by design (parallel panel plus a judge/synthesis step), so use it for deliberate, high-quality answers or escalation paths, not latency-sensitive chat; for faster responses, keep the panel small and choose faster analysis/judge models. Verify the configured ref with a one-shot local call: `openclaw infer model run --local --model openrouter/openrouter/fusion --prompt "Reply with exactly: FUSION_OK" --json`.

## Authentication and headers

OpenRouter uses a Bearer token with your API key under the hood. OpenRouter OAuth is a PKCE login flow that issues an OpenRouter API key, so OpenClaw stores the result as the same `openrouter:default` API-key auth profile used by the manual API-key setup path. For an existing install, sign in or rotate the stored key without rerunning full onboarding via `openclaw models auth login --provider openrouter --method oauth`; use `--method api-key` to paste a manually created key. On real OpenRouter requests (`https://openrouter.ai/api/v1`), OpenClaw adds OpenRouter's documented app-attribution headers: `HTTP-Referer: https://openclaw.ai`, `X-OpenRouter-Title: OpenClaw`, and `X-OpenRouter-Categories: cli-agent,cloud-agent,programming-app,creative-writing,writing-assistant,general-chat,personal-agent`. If you repoint the OpenRouter provider at some other proxy or base URL, OpenClaw does NOT inject those OpenRouter-specific headers or Anthropic cache markers.

## Advanced configuration

**Response caching** is opt-in per model via `params.responseCache: true` and `responseCacheTtlSeconds`; OpenClaw sends `X-OpenRouter-Cache: true` and, when configured, `X-OpenRouter-Cache-TTL`. `responseCacheClear: true` forces a refresh and stores the replacement; snake_case aliases (`response_cache`, `response_cache_ttl_seconds`, `response_cache_clear`) are accepted. This is separate from provider prompt caching and from OpenRouter's Anthropic `cache_control` markers, and only applies on verified `openrouter.ai` routes, not custom proxy base URLs.

```json5
{
  agents: {
    defaults: {
      models: {
        "openrouter/auto": {
          params: {
            responseCache: true,
            responseCacheTtlSeconds: 300,
          },
        },
      },
    },
  },
}
```

**Anthropic cache markers**: on verified routes, Anthropic model refs keep the OpenRouter-specific Anthropic `cache_control` markers OpenClaw uses for better prompt-cache reuse on system/developer prompt blocks. **Anthropic reasoning prefill**: on verified routes, Anthropic refs with reasoning enabled drop trailing assistant prefill turns before the request reaches OpenRouter, matching Anthropic's requirement that reasoning conversations end with a user turn. **Thinking / reasoning injection**: on supported non-`auto` routes, OpenClaw maps the selected thinking level to OpenRouter proxy reasoning payloads; unsupported model hints and `openrouter/auto` skip injection, and Hunter Alpha also skips proxy reasoning for stale configured refs because OpenRouter could return final answer text in reasoning fields for that retired route. **DeepSeek V4 reasoning replay**: on verified routes, `openrouter/deepseek/deepseek-v4-flash` and `openrouter/deepseek/deepseek-v4-pro` fill missing `reasoning_content` on replayed assistant turns to keep DeepSeek V4's required follow-up shape; OpenClaw sends OpenRouter-supported `reasoning_effort` values, where `xhigh` is the highest advertised level and stale `max` overrides map to `xhigh`. **OpenAI-only request shaping**: OpenRouter runs through the proxy-style OpenAI-compatible path, so native OpenAI-only shaping (`serviceTier`, Responses `store`, OpenAI reasoning-compat payloads, prompt-cache hints) is NOT forwarded. **Gemini-backed routes**: Gemini-backed refs stay on the proxy-Gemini path — OpenClaw keeps Gemini thought-signature sanitation but does not enable native Gemini replay validation or bootstrap rewrites.

**Provider routing metadata**: OpenRouter supports a `provider` request object for underlying provider routing. Configure a default policy for all OpenRouter text-model requests with `models.providers.openrouter.params.provider`; OpenClaw forwards that object to OpenRouter as the request `provider` payload. Use OpenRouter's documented snake_case fields, including `sort`, `only`, `ignore`, `order`, `allow_fallbacks`, `require_parameters`, `data_collection`, `quantizations`, `max_price`, `preferred_max_latency`, `preferred_min_throughput`, `zdr`, and `enforce_distillable_text`.

```json5
{
  models: {
    providers: {
      openrouter: {
        params: {
          provider: {
            sort: "latency",
            require_parameters: true,
            data_collection: "deny",
          },
        },
      },
    },
  },
}
```

Per-model `params` still override the provider-wide routing object (e.g. a per-model `provider: { order: ["anthropic"], allow_fallbacks: false }`). This only applies on OpenRouter chat-completions routes; direct Anthropic, Google, OpenAI, or custom provider routes ignore OpenRouter routing params.

**Source**: OpenClaw documentation — `providers/openrouter` (mirror `inbox/openclaw_docs/providers/openrouter.md`)
**Last Updated**: 2026-06-22
**Status**: Active
