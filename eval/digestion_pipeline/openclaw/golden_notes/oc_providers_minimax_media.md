---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - minimax
keywords:
  - minimax media capabilities
  - minimax image generation image-01
  - minimax t2a v2 text-to-speech
  - minimax music_generate music-2.6
  - minimax video_generate hailuo-2.3
  - minimax-vl-01 image understanding
  - minimax token plan web_search
  - minimax multimodal provider
topics:
  - OpenClaw
  - MiniMax Media Capabilities
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/providers/minimax
access_control_group: ["general"]
---

# OpenClaw — MiniMax Multimodal Media & Search Capabilities

## Overview

This note models the multimodal **capability surface** bundled with OpenClaw's MiniMax provider plugin — the six non-chat capabilities the `minimax` (API-key) and `minimax-portal` (OAuth) providers register: image generation (`image-01`), text-to-speech (T2A v2), music generation (`music-2.6`), video generation (`MiniMax-Hailuo-2.3`), image understanding (`MiniMax-VL-01`), and `web_search` via the MiniMax Token Plan search API. It covers each capability's default model, config path, defaults, and auth resolution, mirroring the `## Capabilities` section (Image generation, Text-to-speech, Music generation, Video generation, Image understanding, Web search) of the `providers/minimax` source page. The chat-LLM setup half (provider split, catalog, onboarding, the `configure` wizard, thinking defaults, fallback, troubleshooting) is the split sibling [oc_providers_minimax_setup](oc_providers_minimax_setup.md); shared media-tool parameters/failover live in the linked `/tools/*` pages, not here.

## Image Generation

The MiniMax plugin registers the `image-01` model for the shared `image_generate` tool. It supports **text-to-image generation** with aspect ratio control, **image-to-image editing** (subject reference) with aspect ratio control, up to **9 output images** per request, up to **1 reference image** per edit request, and supported aspect ratios `1:1`, `16:9`, `4:3`, `3:2`, `2:3`, `3:4`, `9:16`, `21:9`. Both `minimax` and `minimax-portal` register `image_generate` with the same `image-01` model; API-key setups use `MINIMAX_API_KEY` while OAuth setups can use the bundled `minimax-portal` auth path instead. The plugin uses the same `MINIMAX_API_KEY` or OAuth auth as the text models, so no additional configuration is needed if MiniMax is already set up. To set MiniMax as the image generation provider:

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: { primary: "minimax/image-01" },
    },
  },
}
```

Image generation always uses MiniMax's dedicated image endpoint (`/v1/image_generation`) and **ignores** `models.providers.minimax.baseUrl`, since that field configures the chat/Anthropic-compatible base URL. Set `MINIMAX_API_HOST=https://api.minimaxi.com` to route image generation through the CN endpoint; the default global endpoint is `https://api.minimax.io`. When onboarding or API-key setup writes explicit `models.providers.minimax` entries, OpenClaw materializes `MiniMax-M3`, `MiniMax-M2.7`, and `MiniMax-M2.7-highspeed` as chat models; M3 advertises text and image input, but image understanding remains exposed separately through the plugin-owned `MiniMax-VL-01` media provider. Shared tool parameters, provider selection, and failover behavior are documented in the OpenClaw `/tools/image-generation` page (see References).

## Text-to-Speech

The bundled `minimax` plugin registers MiniMax **T2A v2** as a speech provider for `messages.tts`. The default TTS model is `speech-2.8-hd` and the default voice is `English_expressive_narrator`. Supported bundled model ids include `speech-2.8-hd`, `speech-2.8-turbo`, `speech-2.6-hd`, `speech-2.6-turbo`, `speech-02-hd`, `speech-02-turbo`, `speech-01-hd`, and `speech-01-turbo`. Auth resolution proceeds in order: `messages.tts.providers.minimax.apiKey`, then `minimax-portal` OAuth/token auth profiles, then Token Plan environment keys (`MINIMAX_OAUTH_TOKEN`, `MINIMAX_CODE_PLAN_KEY`, `MINIMAX_CODING_API_KEY`), then `MINIMAX_API_KEY`. If no TTS host is configured, OpenClaw reuses the configured `minimax-portal` OAuth host and strips Anthropic-compatible path suffixes such as `/anthropic`.

For audio delivery, normal audio attachments stay MP3; voice-note targets such as Feishu and Telegram are transcoded from MiniMax MP3 to 48kHz Opus with `ffmpeg`, because the Feishu/Lark file API only accepts `file_type: "opus"` for native audio messages. MiniMax T2A accepts fractional `speed` and `vol`, but `pitch` is sent as an integer; OpenClaw truncates fractional `pitch` values before the API request. The TTS settings, their env-var overrides, defaults, and ranges:

| Setting | Env var | Default | Description |
| --- | --- | --- | --- |
| `messages.tts.providers.minimax.baseUrl` | `MINIMAX_API_HOST` | `https://api.minimax.io` | MiniMax T2A API host. |
| `messages.tts.providers.minimax.model` | `MINIMAX_TTS_MODEL` | `speech-2.8-hd` | TTS model id. |
| `messages.tts.providers.minimax.speakerVoiceId` | `MINIMAX_TTS_VOICE_ID` | `English_expressive_narrator` | Voice id used for speech output. |
| `messages.tts.providers.minimax.speed` | | `1.0` | Playback speed, `0.5..2.0`. |
| `messages.tts.providers.minimax.vol` | | `1.0` | Volume, `(0, 10]`. |
| `messages.tts.providers.minimax.pitch` | | `0` | Integer pitch shift, `-12..12`. |

## Music Generation

The bundled MiniMax plugin registers music generation through the shared `music_generate` tool for both `minimax` and `minimax-portal`. The default music model is `minimax/music-2.6` (OAuth music model `minimax-portal/music-2.6`); it also supports `minimax/music-2.5` and `minimax/music-2.0`. Prompt controls are `lyrics` and `instrumental`, the output format is `mp3`, and session-backed runs detach through the shared task/status flow, including `action: "status"`. To set MiniMax as the default music provider:

```json5
{
  agents: {
    defaults: {
      musicGenerationModel: {
        primary: "minimax/music-2.6",
      },
    },
  },
}
```

Shared tool parameters, provider selection, and failover behavior are documented in the OpenClaw `/tools/music-generation` page (see References).

## Video Generation

The bundled MiniMax plugin registers video generation through the shared `video_generate` tool for both `minimax` and `minimax-portal`. The default video model is `minimax/MiniMax-Hailuo-2.3` (OAuth video model `minimax-portal/MiniMax-Hailuo-2.3`). Modes are text-to-video and single-image reference flows, and it supports `aspectRatio` and `resolution`. To set MiniMax as the default video provider:

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "minimax/MiniMax-Hailuo-2.3",
      },
    },
  },
}
```

Shared tool parameters, provider selection, and failover behavior are documented in the OpenClaw `/tools/video-generation` page (see References).

## Image Understanding

The MiniMax plugin registers image understanding **separately** from the text catalog, via the plugin-owned `MiniMax-VL-01` media provider. Both provider ids resolve to the same default image model:

| Provider ID | Default image model |
| --- | --- |
| `minimax` | `MiniMax-VL-01` |
| `minimax-portal` | `MiniMax-VL-01` |

Because image understanding is a separate media provider, automatic media routing can use MiniMax image understanding even when the bundled text-provider catalog also includes M3 image-capable chat refs.

## Web Search

The MiniMax plugin also registers `web_search` through the MiniMax **Token Plan** search API. The provider id is `minimax`, and it returns structured results: titles, URLs, snippets, and related queries. The preferred env var is `MINIMAX_CODE_PLAN_KEY`, with accepted aliases `MINIMAX_CODING_API_KEY` and `MINIMAX_OAUTH_TOKEN`; the compatibility fallback is `MINIMAX_API_KEY` when it already points at a token-plan credential. Region reuse resolves through `plugins.entries.minimax.config.webSearch.region`, then `MINIMAX_API_HOST`, then the MiniMax provider base URLs. Search stays on provider id `minimax`; an OAuth CN/global setup can steer region indirectly through `models.providers.minimax-portal.baseUrl` and can provide bearer auth through `MINIMAX_OAUTH_TOKEN`. Config lives under `plugins.entries.minimax.config.webSearch.*`. See the OpenClaw `/tools/minimax-search` page (in References) for full web search configuration and usage.

**Source**: OpenClaw documentation — `providers/minimax` (mirror `inbox/openclaw_docs/providers/minimax.md`), `## Capabilities` section
**Last Updated**: 2026-06-22
**Status**: Active
