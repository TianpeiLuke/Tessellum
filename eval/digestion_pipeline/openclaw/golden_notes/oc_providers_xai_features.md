---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - xai
keywords:
  - openclaw xai feature coverage
  - grok capability matrix
  - xai fast-mode mappings
  - grok legacy aliases
  - xai web_search x_search code_execution
  - xai image_generate video_generate
  - xai tts stt streaming
  - grok-imagine-image grok-imagine-video
  - xai realtime transcription voice call
topics:
  - OpenClaw
  - xAI Feature Coverage
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/providers/xai
access_control_group: ["general"]
---

# OpenClaw — xAI / Grok Capability Surface (Feature Coverage)

## Overview

This note models the **xAI capability surface that OpenClaw actually exposes** — which parts of xAI's public API the bundled `xai` plugin maps onto OpenClaw's shared provider and tool contracts, and which are not exposed. It covers the capability-to-surface coverage matrix, the fast-mode and legacy-alias model-remapping tables, and the per-capability config for web search, video generation, image generation, batch text-to-speech, batch and streaming speech-to-text, `x_search`, `code_execution`, the known limits, advanced runner notes, and live testing — mirroring the `## OpenClaw feature coverage`, `## Features`, and `## Live testing` sections of the `providers/xai` source page. The auth/setup half of this provider (OAuth, device-code, API-key, OAuth troubleshooting, and the chat-model catalog) lives in the sibling `oc_providers_xai_setup` note.

## Capability Coverage Matrix

The bundled plugin maps xAI's current public API surface onto OpenClaw's shared provider and tool contracts. Capabilities that don't fit the shared contract (for example streaming TTS and realtime voice) are not exposed. The matrix below states each xAI capability, the OpenClaw surface it maps onto, and whether it is exposed:

| xAI capability | OpenClaw surface | Status |
| --- | --- | --- |
| Chat / Responses | `xai/<model>` model provider | Yes |
| Server-side web search | `web_search` provider `grok` | Yes |
| Server-side X search | `x_search` tool | Yes |
| Server-side code execution | `code_execution` tool | Yes |
| Images | `image_generate` | Yes |
| Videos | `video_generate` | Yes |
| Batch text-to-speech | `messages.tts.provider: "xai"` / `tts` | Yes |
| Streaming TTS | - | Not exposed; OpenClaw's TTS contract returns complete audio buffers |
| Batch speech-to-text | `tools.media.audio` / media understanding | Yes |
| Streaming speech-to-text | Voice Call `streaming.provider: "xai"` | Yes |
| Realtime voice | - | Not exposed yet; different session/WebSocket contract |
| Files / batches | Generic model API compatibility only | Not a first-class OpenClaw tool |

OpenClaw uses xAI's REST image/video/TTS/STT APIs for media generation, speech, and batch transcription, xAI's streaming STT WebSocket for live voice-call transcription, and the Responses API for model, search, and code-execution tools. Features that need different OpenClaw contracts, such as Realtime voice sessions, are documented as upstream capabilities rather than hidden plugin behavior.

### Fast-mode Mappings

`/fast on` or `agents.defaults.models["xai/<model>"].params.fastMode: true` rewrites native xAI requests by remapping each source model onto its fast-mode target:

| Source model | Fast-mode target |
| --- | --- |
| `grok-3` | `grok-3-fast` |
| `grok-3-mini` | `grok-3-mini-fast` |
| `grok-4` | `grok-4-fast` |
| `grok-4-0709` | `grok-4-fast` |

### Legacy Compatibility Aliases

Legacy aliases still normalize to the canonical bundled ids; these are forward-resolved for existing configs so older slugs keep working:

| Legacy alias | Canonical id |
| --- | --- |
| `grok-code-fast-1` | `grok-build-0.1` |
| `grok-code-fast` | `grok-build-0.1` |
| `grok-code-fast-1-0825` | `grok-build-0.1` |
| `grok-4-fast-reasoning` | `grok-4-fast` |
| `grok-4-1-fast-reasoning` | `grok-4-1-fast` |
| `grok-4.20-reasoning` | `grok-4.20-beta-latest-reasoning` |
| `grok-4.20-non-reasoning` | `grok-4.20-beta-latest-non-reasoning` |

## Web Search

The bundled `grok` web-search provider prefers xAI OAuth, then falls back to `XAI_API_KEY` or a plugin web-search key. It is selected by setting `tools.web.search.provider` to `grok` (`openclaw config set tools.web.search.provider grok`) after `openclaw models auth login --provider xai --method oauth`. Grok `web_search` reads `plugins.entries.xai.config.webSearch.baseUrl` to route through an operator xAI Responses proxy.

## Video Generation

The bundled `xai` plugin registers video generation through the shared `video_generate` tool, with the default video model `xai/grok-imagine-video`. Supported modes are text-to-video, image-to-video, reference-image generation, remote video edit, and remote video extension. Aspect ratios are `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`; resolutions are `480P` and `720P`. Duration is 1-15 seconds for generation/image-to-video, 1-10 seconds when using `reference_image` roles, and 2-10 seconds for extension. For reference-image generation, set `imageRoles` to `reference_image` for every supplied image; xAI accepts up to 7 such images. The default operation timeout is 600 seconds unless `video_generate.timeoutMs` or `agents.defaults.videoGenerationModel.timeoutMs` is set. Local video buffers are not accepted — use remote `http(s)` URLs for video edit/extend inputs; image-to-video accepts local image buffers because OpenClaw can encode those as data URLs for xAI. See the shared Video Generation tool for cross-provider parameters, provider selection, and failover.

## Image Generation

The bundled `xai` plugin registers image generation through the shared `image_generate` tool, with the default image model `xai/grok-imagine-image` and the additional model `xai/grok-imagine-image-quality`. Modes are text-to-image and reference-image edit; reference inputs are one `image` or up to five `images`. Aspect ratios are `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `2:3`, `3:2`; resolutions are `1K` and `2K`; count is up to 4 images. The default operation timeout is 600 seconds unless `image_generate.timeoutMs` or `agents.defaults.imageGenerationModel.timeoutMs` is set. OpenClaw asks xAI for `b64_json` image responses so generated media can be stored and delivered through the normal channel attachment path; local reference images are converted to data URLs, while remote `http(s)` references are passed through. xAI also documents `quality`, `mask`, `user`, and additional native ratios such as `1:2`, `2:1`, `9:20`, and `20:9`, but OpenClaw forwards only the shared cross-provider image controls today — unsupported native-only knobs are intentionally not exposed through `image_generate`.

## Batch Text-to-Speech

The bundled `xai` plugin registers text-to-speech through the shared `tts` provider surface using xAI's batch `/v1/tts` endpoint. Voices are `eve`, `ara`, `rex`, `sal`, `leo`, `una` (default `eve`); formats are `mp3`, `wav`, `pcm`, `mulaw`, `alaw`; language is a BCP-47 code or `auto`; speed is a provider-native speed override. The native Opus voice-note format is not supported. xAI also offers streaming TTS over WebSocket, but the OpenClaw speech provider contract currently expects a complete audio buffer before reply delivery, so streaming TTS is not exposed. To select xAI as the default TTS provider:

```json5
{
  messages: {
    tts: {
      provider: "xai",
      providers: {
        xai: {
          speakerVoiceId: "eve",
        },
      },
    },
  },
}
```

## Batch Speech-to-Text

The bundled `xai` plugin registers batch speech-to-text through OpenClaw's media-understanding transcription surface, with default model `grok-stt` over the xAI REST `/v1/stt` endpoint and a multipart audio-file upload input path. It is supported wherever inbound audio transcription uses `tools.media.audio`, including Discord voice-channel segments and channel audio attachments. Language can be supplied through the shared audio media config or per-call transcription request; prompt hints are accepted by the shared OpenClaw surface, but the xAI REST STT integration only forwards file, model, and language because those map cleanly to the current public xAI endpoint. To force xAI for inbound audio transcription:

```json5
{
  tools: {
    media: {
      audio: {
        models: [
          {
            type: "provider",
            provider: "xai",
            model: "grok-stt",
          },
        ],
      },
    },
  },
}
```

## Streaming Speech-to-Text

The bundled `xai` plugin also registers a realtime transcription provider for live voice-call audio over the xAI WebSocket `wss://api.x.ai/v1/stt` endpoint. Defaults are encoding `mulaw`, sample rate `8000`, endpointing `800ms`, with interim transcripts enabled by default. Voice Call's Twilio media stream sends G.711 µ-law audio frames, so the xAI provider forwards those frames directly without transcoding. Provider-owned config lives under `plugins.entries.voice-call.config.streaming.providers.xai`; supported keys are `apiKey`, `baseUrl`, `sampleRate`, `encoding` (`pcm`, `mulaw`, or `alaw`), `interimResults`, `endpointingMs`, and `language`. This streaming provider is for Voice Call's realtime transcription path; Discord voice currently records short segments and uses the batch `tools.media.audio` transcription path instead. To enable it:

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          streaming: {
            enabled: true,
            provider: "xai",
            providers: {
              xai: {
                apiKey: "${XAI_API_KEY}",
                endpointingMs: 800,
                language: "en",
              },
            },
          },
        },
      },
    },
  },
}
```

## x_search Configuration

The bundled xAI plugin exposes `x_search` as an OpenClaw tool for searching X (formerly Twitter) content via Grok. Its config path is `plugins.entries.xai.config.xSearch`, with keys: `enabled` (boolean), `model` (string, default `grok-4-1-fast`), `baseUrl` (string, xAI Responses base URL override), `inlineCitations` (boolean, include inline citations), `maxTurns` (number, maximum conversation turns), `timeoutSeconds` (number), and `cacheTtlMinutes` (number). `x_search` reads `plugins.entries.xai.config.xSearch.baseUrl`, then falls back to the Grok web-search base URL.

```json5
{
  plugins: {
    entries: {
      xai: {
        config: {
          xSearch: {
            enabled: true,
            model: "grok-4-1-fast",
            baseUrl: "https://api.x.ai/v1",
            inlineCitations: true,
          },
        },
      },
    },
  },
}
```

## code_execution Configuration

The bundled xAI plugin exposes `code_execution` as an OpenClaw tool for remote code execution in xAI's sandbox environment — this is remote xAI sandbox execution, not the local `exec` tool. Its config path is `plugins.entries.xai.config.codeExecution`, with keys: `enabled` (boolean, default `true` if a key is available), `model` (string, default `grok-4-1-fast`), `maxTurns` (number), and `timeoutSeconds` (number).

```json5
{
  plugins: {
    entries: {
      xai: {
        config: {
          codeExecution: {
            enabled: true,
            model: "grok-4-1-fast",
          },
        },
      },
    },
  },
}
```

## Known Limits

- xAI auth can use an API key, environment variable, plugin config fallback, browser OAuth, or device-code OAuth with an eligible xAI account; browser OAuth uses a local callback on `127.0.0.1:56121`, and for remote hosts `xai-device-code` is used unless the port is forwarded before opening the sign-in URL. xAI decides which accounts can receive OAuth API tokens, and the consent page may show Grok Build even though OpenClaw does not require the Grok Build app.
- OpenClaw does not currently expose the xAI multi-agent model family: xAI serves these models through the Responses API, but they do not accept the client-side or custom tools used by OpenClaw's shared agent loop.
- xAI Realtime voice is not registered as an OpenClaw provider yet — it needs a different bidirectional voice session contract than batch STT or streaming transcription.
- xAI image `quality`, image `mask`, and extra native-only aspect ratios are not exposed until the shared `image_generate` tool has corresponding cross-provider controls.

## Advanced Notes

- OpenClaw applies xAI-specific tool-schema and tool-call compatibility fixes automatically on the shared runner path.
- Native xAI requests default `tool_stream: true`; set `agents.defaults.models["xai/<model>"].params.tool_stream` to `false` to disable it.
- The bundled xAI wrapper strips unsupported strict tool-schema flags and reasoning payload keys before sending native xAI requests.
- `web_search`, `x_search`, and `code_execution` are exposed as OpenClaw tools; OpenClaw enables the specific xAI built-in it needs inside each tool request instead of attaching all native tools to every chat turn.
- Grok `web_search` reads `plugins.entries.xai.config.webSearch.baseUrl`; `x_search` reads `plugins.entries.xai.config.xSearch.baseUrl`, then falls back to the Grok web-search base URL.
- `x_search` and `code_execution` are owned by the bundled xAI plugin rather than hardcoded into the core model runtime.

## Live Testing

The xAI media paths are covered by unit tests and opt-in live suites; export `XAI_API_KEY` in the process environment before running live probes. The provider-specific live file synthesizes normal TTS, telephony-friendly PCM TTS, transcribes audio through xAI batch STT, streams the same PCM through xAI realtime STT, generates text-to-image output, and edits a reference image. The shared image live file verifies the same xAI provider through OpenClaw's runtime selection, fallback, normalization, and media attachment path.

```bash
pnpm test extensions/xai
OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_TEST_QUIET=1 pnpm test:live -- extensions/xai/xai.live.test.ts
OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_TEST_QUIET=1 OPENCLAW_LIVE_IMAGE_GENERATION_PROVIDERS=xai pnpm test:live -- test/image-generation.runtime.live.test.ts
```

**Source**: OpenClaw documentation — `providers/xai` (mirror `inbox/openclaw_docs/providers/xai.md`)
**Last Updated**: 2026-06-22
**Status**: Active
