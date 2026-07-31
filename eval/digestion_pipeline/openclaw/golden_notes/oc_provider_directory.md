---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - model_providers
keywords:
  - openclaw provider directory
  - provider/model default model
  - llm provider catalog
  - openclaw onboard authenticate
  - transcription providers
  - amazon bedrock anthropic openrouter
  - local models ollama vllm lm studio
  - claude max api proxy caveat
topics:
  - OpenClaw
  - Model Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/providers
access_control_group: ["general"]
---

# OpenClaw — Model Provider Directory

## Overview

This note is the conceptual index of the OpenClaw **provider directory**: the catalog of LLM, transcription, and media-generation model backends OpenClaw can use, fronted by a single configuration pattern. It mirrors the `providers` source page, which states that "OpenClaw can use many LLM providers" and that the usage model is uniform: "Pick a provider, authenticate, then set the default model as `provider/model`." The page is a routing/landing hub — it links down into per-provider detail pages (the `oc_providers_*` series owned by another sub-plan) rather than configuring each provider here. This note covers the `provider/model` quick-start pattern, the catalog of 50+ providers, the shared media-generation overview pages, the transcription providers, and the community Claude-Max proxy caveat.

## The `provider/model` Default-Model Pattern

The page reduces provider usage to three steps: "Pick a provider, authenticate, then set the default model as `provider/model`." Authentication is "usually via `openclaw onboard`" — the onboarding wizard handles per-provider credential capture. After authentication, the default model is set in config as a `provider/model` string. The page's quick-start gives the canonical JSON5 config example:

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

Here `anthropic/claude-opus-4-6` is a `provider/model` value: `anthropic` is the provider segment and `claude-opus-4-6` is the model segment, set under `agents.defaults.model.primary`. Each provider's own detail page documents which model identifiers are valid for that provider; the directory page itself only establishes the pattern and links out.

## Provider Docs (LLM Provider Catalog)

The "Provider docs" section lists the LLM (and some media/speech) provider detail pages OpenClaw supports — 50+ entries, each linking to a `/providers/<name>` page (or, for a few, a `/concepts/model-providers#...` anchor). These are config values, not vault terms; the per-provider pages are owned by the `oc_providers_*` (pr*) series and are linked, not inlined here. The catalog (verbatim from source) spans cloud, aggregator/gateway, and local-model providers:

- **Cloud LLM providers**: Alibaba Model Studio, Amazon Bedrock, Amazon Bedrock Mantle, Anthropic (API + Claude CLI), Arcee AI (Trinity models), BytePlus (International), Cerebras, Chutes, Cohere, DeepSeek, Fireworks, GitHub Copilot, GMI Cloud, Google (Gemini), Gradium, Groq (LPU inference), Hugging Face (Inference), Kilocode, MiniMax, Mistral, Moonshot AI (Kimi + Kimi Coding), NVIDIA, NovitaAI, OpenAI (API + Codex), OpenCode, OpenCode Go, Perplexity (web search), Qianfan, Qwen Cloud, Qwen OAuth / Portal, StepFun, Synthetic, Tencent Cloud (TokenHub), Together AI, Venice (Venice AI, privacy-focused), Volcengine (Doubao), Vydra, xAI, Xiaomi, Z.AI (GLM).
- **Unified gateways / aggregators**: Cloudflare AI Gateway, LiteLLM (unified gateway), OpenRouter, Vercel AI Gateway — these route across multiple underlying providers.
- **Local / self-hosted models**: ds4 (local DeepSeek V4), inferrs (local models), LM Studio (local models), Ollama (cloud + local models), Ollama Cloud, SGLang (local models), vLLM (local models).
- **Media-capable entries listed here**: Azure Speech, ComfyUI, ElevenLabs, fal, Runway, SenseAudio — these appear in the provider list and also feed the media/transcription surfaces below.

The list is reproduced from the source page's link set; each name is the link text and each target is a `/providers/<slug>` page (e.g. `/providers/bedrock`, `/providers/anthropic`, `/providers/openrouter`) except BytePlus, which links to `/concepts/model-providers#byteplus-international`.

## Shared Overview Pages

Beyond per-provider pages, the directory links four "Shared overview pages" that document cross-provider, shared-tool behavior rather than a single provider:

- **Additional bundled variants** (`/providers/models#additional-bundled-provider-variants`) — described as "Anthropic Vertex, Copilot Proxy, and Gemini CLI OAuth" — bundled provider variants beyond the primary provider pages.
- **Image Generation** (`/tools/image-generation`) — the shared `image_generate` tool, provider selection, and failover.
- **Music Generation** (`/tools/music-generation`) — the shared `music_generate` tool, provider selection, and failover.
- **Video Generation** (`/tools/video-generation`) — the shared `video_generate` tool, provider selection, and failover.

The three media-generation pages live under `/tools/` (not `/providers/`) because the generation capability is exposed as a shared tool (`image_generate` / `music_generate` / `video_generate`) with its own provider-selection and failover logic, indexed by the Tools surface.

## Transcription Providers

A separate "Transcription providers" section lists the speech-to-text (audio transcription) backends, several of which are sub-sections of an LLM provider's page rather than standalone provider pages:

- Deepgram (audio transcription) — `/providers/deepgram`
- ElevenLabs — `/providers/elevenlabs#speech-to-text`
- Mistral — `/providers/mistral#audio-transcription-voxtral`
- OpenAI — `/providers/openai#speech-to-text`
- SenseAudio — `/providers/senseaudio`
- xAI — `/providers/xai#speech-to-text`

The anchored links (`#speech-to-text`, `#audio-transcription-voxtral`) indicate that ElevenLabs, Mistral, OpenAI, and xAI document their transcription capability as a section of their main provider page, while Deepgram and SenseAudio have dedicated provider pages.

## Community Tools

The page closes with a "Community tools" section listing one entry: the **Claude Max API Proxy** (`/providers/claude-max-api-proxy`), described as a "Community proxy for Claude subscription credentials." The source attaches an explicit caveat: "verify Anthropic policy/terms before use." This is a community-maintained proxy (not a first-party OpenClaw provider) for using Claude subscription credentials, and the directory flags the terms-of-service verification responsibility on the user. The page also directs readers to the full catalog: "For the full provider catalog (xAI, Groq, Mistral, etc.) and advanced configuration, see [Model providers](https://docs.openclaw.ai/concepts/model-providers)." A note at the top of the page also points chat-channel readers elsewhere: "Looking for chat channel docs (WhatsApp/Telegram/Discord/Slack/Mattermost (plugin)/etc.)? See [Channels](https://docs.openclaw.ai/channels)."

**Source**: OpenClaw documentation — `providers` (mirror `inbox/openclaw_docs/providers.md`)
**Last Updated**: 2026-06-22
**Status**: Active
