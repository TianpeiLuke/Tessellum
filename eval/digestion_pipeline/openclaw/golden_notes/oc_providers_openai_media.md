---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - openai
keywords:
  - openai media generation openclaw
  - gpt-image-2 image generation
  - sora-2 video generation
  - gpt-5 prompt contribution overlay
  - openai tts gpt-4o-mini-tts
  - openai speech-to-text gpt-4o-transcribe
  - openai realtime voice gpt-realtime-2
  - openai realtime api websocket
  - platform credits vs codex subscription
topics:
  - OpenClaw
  - OpenAI Provider
  - Media Generation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/openai
access_control_group: ["general"]
---

# OpenClaw — OpenAI Media: Image, Video, GPT-5 Overlay, and Voice/Speech

## Overview

This note is the OpenAI media-and-voice procedure: how OpenClaw routes image generation, video generation, the GPT-5 prompt-contribution overlay, and the full voice/speech surface (TTS, batch STT, realtime transcription, and realtime voice) through the bundled `openai` plugin. It mirrors the **Image generation**, **Video generation**, **GPT-5 prompt contribution**, and **Voice and speech** sections of the `providers/openai` source page. Auth/Codex-runtime onboarding is covered by [oc_providers_openai_auth](oc_providers_openai_auth.md), and Azure endpoints + transport/compaction tuning by [oc_providers_openai_advanced](oc_providers_openai_advanced.md). The single load-bearing distinction throughout: image/video work with either `OPENAI_API_KEY` or Codex OAuth, but **Realtime voice requires OpenAI Platform credits — not Codex/ChatGPT subscription quota**.

## Image generation

The bundled `openai` plugin registers image generation through the `image_generate` tool. It supports both OpenAI API-key image generation and Codex OAuth image generation through the same `openai/gpt-image-2` model ref. The capability differences between the two auth shapes:

| Capability | OpenAI API key | Codex OAuth |
| --- | --- | --- |
| Model ref | `openai/gpt-image-2` | `openai/gpt-image-2` |
| Auth | `OPENAI_API_KEY` | OpenAI Codex OAuth sign-in |
| Transport | OpenAI Images API | Codex Responses backend |
| Max images per request | 4 | 4 |
| Edit mode | Enabled (up to 5 reference images) | Enabled (up to 5 reference images) |
| Size overrides | Supported, including 2K/4K sizes | Supported, including 2K/4K sizes |
| Aspect ratio / resolution | Not forwarded to OpenAI Images API | Mapped to a supported size when safe |

Set the default image-generation model with `agents.defaults.imageGenerationModel.primary: "openai/gpt-image-2"`. `gpt-image-2` is the default for both OpenAI text-to-image generation and image editing. `gpt-image-1.5`, `gpt-image-1`, and `gpt-image-1-mini` remain usable as explicit model overrides. Use `openai/gpt-image-1.5` for transparent-background PNG/WebP output; the current `gpt-image-2` API rejects `background: "transparent"`. For a transparent-background request, agents should call `image_generate` with `model: "openai/gpt-image-1.5"`, `outputFormat: "png"` or `"webp"`, and `background: "transparent"`; the older `openai.background` provider option is still accepted. OpenClaw also protects the public OpenAI and OpenAI Codex OAuth routes by rewriting default `openai/gpt-image-2` transparent requests to `gpt-image-1.5`; Azure and custom OpenAI-compatible endpoints keep their configured deployment/model names.

The same setting is exposed for headless CLI runs:

```bash
openclaw infer image generate \
  --model openai/gpt-image-1.5 \
  --output-format png \
  --background transparent \
  --prompt "A simple red circle sticker on a transparent background" \
  --json
```

Use the same `--output-format` and `--background` flags with `openclaw infer image edit` when starting from an input file. `--openai-background` remains available as an OpenAI-specific alias. Use `--quality low|medium|high|auto` to control OpenAI Images quality and cost, and `--openai-moderation low|auto` to pass OpenAI's provider-specific moderation hint from either `image generate` or `image edit`.

For ChatGPT/Codex OAuth installs, keep the same `openai/gpt-image-2` ref. When an `openai` OAuth profile is configured, OpenClaw resolves that stored OAuth access token and sends image requests through the Codex Responses backend — it does not first try `OPENAI_API_KEY` or silently fall back to an API key for that request. Configure `models.providers.openai` explicitly with an API key, custom base URL, or Azure endpoint when you want the direct OpenAI Images API route instead. If that custom image endpoint is on a trusted LAN/private address, also set `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork: true`; OpenClaw keeps private/internal OpenAI-compatible image endpoints blocked unless this opt-in is present.

In-chat tool invocations (generate, transparent PNG, and edit):

```
/tool image_generate model=openai/gpt-image-2 prompt="A polished launch poster for OpenClaw on macOS" size=3840x2160 count=1
/tool image_generate model=openai/gpt-image-1.5 prompt="A simple red circle sticker on a transparent background" outputFormat=png background=transparent
/tool image_generate model=openai/gpt-image-2 prompt="Preserve the object shape, change the material to translucent glass" image=/path/to/reference.png size=1024x1536
```

## Video generation

The bundled `openai` plugin registers video generation through the `video_generate` tool.

| Capability | Value |
| --- | --- |
| Default model | `openai/sora-2` |
| Modes | Text-to-video, image-to-video, single-video edit |
| Reference inputs | 1 image or 1 video |
| Size overrides | Supported for text-to-video and image-to-video |
| Other overrides | `aspectRatio`, `resolution`, `audio`, `watermark` are ignored with a tool warning |

OpenAI image-to-video requests use `POST /v1/videos` with an image `input_reference`. Single-video edits use `POST /v1/videos/edits` with the uploaded video in the `video` field. Set the default video-generation model in config:

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: { primary: "openai/sora-2" },
    },
  },
}
```

Shared video-tool parameters, provider selection, and failover behavior are documented in the Video Generation tool reference (link-out below — not duplicated here).

## GPT-5 prompt contribution

OpenClaw adds a shared GPT-5 prompt contribution for GPT-5-family runs on OpenClaw-assembled prompt surfaces. It applies by model id, so OpenClaw/provider routes such as legacy pre-repair refs (legacy Codex GPT-5.5 ref), `openrouter/openai/gpt-5.5`, `opencode/gpt-5.5`, and other compatible GPT-5 refs receive the same overlay. Older GPT-4.x models do not.

The bundled native Codex harness does not receive this OpenClaw GPT-5 overlay through Codex app-server developer instructions. Native Codex keeps Codex-owned base, model, and project-doc behavior, while OpenClaw disables Codex's built-in personality for native threads so agent workspace personality files stay authoritative. OpenClaw contributes only runtime context such as channel delivery, OpenClaw dynamic tools, ACP delegation, workspace context, and OpenClaw skills.

The GPT-5 contribution adds a tagged behavior contract for persona persistence, execution safety, tool discipline, output shape, completion checks, and verification on matching OpenClaw-assembled prompts. Channel-specific reply and silent-message behavior stays in the shared OpenClaw system prompt and outbound delivery policy. The friendly interaction-style layer is separate and configurable via `agents.defaults.promptOverlays.gpt5.personality`:

| Value | Effect |
| --- | --- |
| `"friendly"` (default) | Enable the friendly interaction-style layer |
| `"on"` | Alias for `"friendly"` |
| `"off"` | Disable only the friendly style layer |

Configure the personality layer in config or via the CLI command `openclaw config set agents.defaults.promptOverlays.gpt5.personality off`:

```json5
{
  agents: {
    defaults: {
      promptOverlays: {
        gpt5: { personality: "friendly" },
      },
    },
  },
}
```

Values are case-insensitive at runtime, so `"Off"` and `"off"` both disable the friendly style layer. Legacy `plugins.entries.openai.config.personality` is still read as a compatibility fallback when the shared `agents.defaults.promptOverlays.gpt5.personality` setting is not set.

## Voice and speech

OpenClaw's bundled `openai` plugin registers four distinct voice/speech surfaces: speech synthesis (TTS), batch speech-to-text, realtime transcription, and realtime voice. The auth split is critical: TTS and Realtime voice both require an OpenAI Platform API key — OAuth-only installs can still run Codex-backed chat models but not OpenAI live talk-back.

### Speech synthesis (TTS)

The bundled `openai` plugin registers speech synthesis for the `messages.tts` surface.

| Setting | Config path | Default |
| --- | --- | --- |
| Model | `messages.tts.providers.openai.model` | `gpt-4o-mini-tts` |
| Voice | `messages.tts.providers.openai.speakerVoice` | `coral` |
| Speed | `messages.tts.providers.openai.speed` | (unset) |
| Instructions | `messages.tts.providers.openai.instructions` | (unset, `gpt-4o-mini-tts` only) |
| Format | `messages.tts.providers.openai.responseFormat` | `opus` for voice notes, `mp3` for files |
| API key | `messages.tts.providers.openai.apiKey` | Falls back to `OPENAI_API_KEY` |
| Base URL | `messages.tts.providers.openai.baseUrl` | `https://api.openai.com/v1` |
| Extra body | `messages.tts.providers.openai.extraBody` / `extra_body` | (unset) |

Available models: `gpt-4o-mini-tts`, `tts-1`, `tts-1-hd`. Available voices: `alloy`, `ash`, `ballad`, `cedar`, `coral`, `echo`, `fable`, `juniper`, `marin`, `onyx`, `nova`, `sage`, `shimmer`, `verse`. `extraBody` is merged into the `/audio/speech` request JSON after OpenClaw's generated fields, so use it for OpenAI-compatible endpoints that require additional keys such as `lang` (prototype keys are ignored). A minimal TTS config:

```json5
{
  messages: {
    tts: {
      providers: {
        openai: { model: "gpt-4o-mini-tts", speakerVoice: "coral" },
      },
    },
  },
}
```

Set `OPENAI_TTS_BASE_URL` to override the TTS base URL without affecting the chat API endpoint. OpenAI TTS and Realtime voice are both configured through an OpenAI Platform API key; OAuth-only installs can still use Codex-backed chat models, but not OpenAI live talk-back.

### Speech-to-text (batch)

The bundled `openai` plugin registers batch speech-to-text through OpenClaw's media-understanding transcription surface. Default model: `gpt-4o-transcribe`. Endpoint: OpenAI REST `/v1/audio/transcriptions`. Input path: multipart audio file upload. It is supported wherever inbound audio transcription uses `tools.media.audio`, including Discord voice-channel segments and channel audio attachments. To force OpenAI for inbound audio transcription:

```json5
{
  tools: {
    media: {
      audio: {
        models: [
          {
            type: "provider",
            provider: "openai",
            model: "gpt-4o-transcribe",
          },
        ],
      },
    },
  },
}
```

Language and prompt hints are forwarded to OpenAI when supplied by the shared audio media config or per-call transcription request.

### Realtime transcription

The bundled `openai` plugin registers realtime transcription for the Voice Call plugin.

| Setting | Config path | Default |
| --- | --- | --- |
| Model | `plugins.entries.voice-call.config.streaming.providers.openai.model` | `gpt-4o-transcribe` |
| Language | `...openai.language` | (unset) |
| Prompt | `...openai.prompt` | (unset) |
| Silence duration | `...openai.silenceDurationMs` | `800` |
| VAD threshold | `...openai.vadThreshold` | `0.5` |
| Auth | `...openai.apiKey`, `OPENAI_API_KEY`, or `openai` OAuth | API keys connect directly; OAuth mints a Realtime transcription client secret |

Realtime transcription uses a WebSocket connection to `wss://api.openai.com/v1/realtime` with G.711 u-law (`g711_ulaw` / `audio/pcmu`) audio. When only `openai` OAuth is configured, the Gateway mints an ephemeral Realtime transcription client secret before opening the WebSocket. This streaming provider is for Voice Call's realtime transcription path; Discord voice currently records short segments and uses the batch `tools.media.audio` transcription path instead.

### Realtime voice

The bundled `openai` plugin registers realtime voice for the Voice Call plugin.

| Setting | Config path | Default |
| --- | --- | --- |
| Model | `plugins.entries.voice-call.config.realtime.providers.openai.model` | `gpt-realtime-2` |
| Voice | `...openai.voice` | `alloy` |
| Temperature (Azure deployment bridge) | `...openai.temperature` | `0.8` |
| VAD threshold | `...openai.vadThreshold` | `0.5` |
| Silence duration | `...openai.silenceDurationMs` | `500` |
| Prefix padding | `...openai.prefixPaddingMs` | `300` |
| Reasoning effort | `...openai.reasoningEffort` | (unset) |
| Auth | `openai` API-key auth profile, `...openai.apiKey`, or `OPENAI_API_KEY` | OpenAI Platform API key required; OpenAI OAuth does not configure Realtime voice |

Available built-in Realtime voices for `gpt-realtime-2`: `alloy`, `ash`, `ballad`, `coral`, `echo`, `sage`, `shimmer`, `verse`, `marin`, `cedar`. OpenAI recommends `marin` and `cedar` for the best Realtime quality. This is a separate set from the Text-to-speech voices above; do not assume a TTS voice such as `fable`, `nova`, or `onyx` is valid for Realtime sessions. Backend OpenAI realtime bridges use the GA Realtime WebSocket session shape, which does not accept `session.temperature`; Azure OpenAI deployments remain available via `azureEndpoint` and `azureDeployment` and keep the deployment-compatible session shape. Realtime supports bidirectional tool calling and G.711 u-law audio. The voice is selected when the session is created — OpenAI allows most session fields to change later, but the voice cannot be changed after the model has emitted audio in that session, and OpenClaw currently exposes the built-in Realtime voice ids as strings.

Control UI Talk uses OpenAI browser realtime sessions with a Gateway-minted ephemeral client secret and a direct browser WebRTC SDP exchange against the OpenAI Realtime API. The Gateway mints that client secret with the selected `openai` API-key auth profile or configured OpenAI Platform API key (`talk.realtime.providers.openai.apiKey`). Gateway relay and Voice Call backend realtime WebSocket bridges use the same API-key-only auth path for native OpenAI endpoints. Realtime voice is billed against OpenAI Platform credits, not Codex/ChatGPT subscription quota; top up Platform credits for the organization backing your realtime credentials.

**Source**: OpenClaw documentation — `providers/openai` (mirror `inbox/openclaw_docs/providers/openai.md`), Image generation / Video generation / GPT-5 prompt contribution / Voice and speech sections
**Last Updated**: 2026-06-22
**Status**: Active
