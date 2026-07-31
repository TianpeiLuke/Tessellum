---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - google
keywords:
  - google gemini media providers
  - gemini image generation flash image
  - veo video generation
  - lyria music generation
  - gemini batch tts voices audio tags
  - gemini live api realtime voice
  - voice call meet realtime config
  - imageGenerationModel videoGenerationModel musicGenerationModel
topics:
  - OpenClaw
  - Google Provider
  - Media and Voice
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/google
access_control_group: ["general"]
---

# OpenClaw — Configuring the Google Media and Realtime-Voice Providers

## Overview

This note is the configuration procedure for the bundled Google media and voice providers that ship with the same `google` plugin documented in the chat half — image generation, video generation, music generation, batch Gemini text-to-speech, and realtime voice over the Gemini Live API. It mirrors the Image generation, Video generation, Music generation, Text-to-speech, and Realtime voice sections of the `providers/google` source page. Auth, default-chat-model selection, the Capabilities matrix, and Grounding web search live in the chat half ([oc_provider_google_chat](oc_provider_google_chat.md)); the credential fallbacks repeated below resolve through the same `models.providers.google.apiKey` / `GEMINI_API_KEY` / `GOOGLE_API_KEY` chain.

## Image generation

The bundled `google` image-generation provider defaults to `google/gemini-3.1-flash-image-preview`. It also supports `google/gemini-3-pro-image-preview`, generates up to 4 images per request, enables edit mode with up to 5 input images, and exposes the geometry controls `size`, `aspectRatio`, and `resolution`. To make Google the default image provider, set `agents.defaults.imageGenerationModel.primary`:

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "google/gemini-3.1-flash-image-preview",
      },
    },
  },
}
```

Shared image-tool parameters, provider selection, and failover behavior are documented at the shared Image Generation tool page (`/tools/image-generation`), not here — see the `oc_tools_image_generation` cross-link below.

## Video generation

The bundled `google` plugin registers video generation through the shared `video_generate` tool. The default video model is `google/veo-3.1-fast-generate-preview`, with text-to-video, image-to-video, and single-video reference flows. It supports `aspectRatio` (`16:9`, `9:16`) and `resolution` (`720P`, `1080P`); audio output is not supported by Veo today. Supported durations are **4, 6, or 8 seconds** — other values snap to the nearest allowed value. To make Google the default video provider, set `agents.defaults.videoGenerationModel.primary` to `google/veo-3.1-fast-generate-preview`. Shared video-tool parameters, provider selection, and failover behavior are documented at the shared Video Generation tool page (`/tools/video-generation`).

## Music generation

The bundled `google` plugin registers music generation through the shared `music_generate` tool. The default music model is `google/lyria-3-clip-preview`, and it also supports `google/lyria-3-pro-preview`. Prompt controls are `lyrics` and `instrumental`; output format is `mp3` by default, plus `wav` on `google/lyria-3-pro-preview`; reference inputs accept up to 10 images. Session-backed runs detach through the shared task/status flow, including `action: "status"`. To make Google the default music provider, set `agents.defaults.musicGenerationModel.primary` to `google/lyria-3-clip-preview`. Shared music-tool parameters, provider selection, and failover behavior are documented at the shared Music Generation tool page (`/tools/music-generation`).

## Text-to-speech

The bundled `google` speech provider uses the Gemini API TTS path with `gemini-3.1-flash-tts-preview`. The default voice is `Kore`. Auth resolves through `messages.tts.providers.google.apiKey`, then `models.providers.google.apiKey`, then `GEMINI_API_KEY`, then `GOOGLE_API_KEY`. Output is WAV for regular TTS attachments, Opus for voice-note targets, and PCM for Talk/telephony; for voice-note output, Google PCM is wrapped as WAV and transcoded to 48 kHz Opus with `ffmpeg`. Google's batch Gemini TTS path returns generated audio in the completed `generateContent` response — for lowest-latency spoken conversations, use the Google realtime voice provider (Gemini Live API) instead of batch TTS. To make Google the default TTS provider:

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "google",
      providers: {
        google: {
          model: "gemini-3.1-flash-tts-preview",
          speakerVoice: "Kore",
          audioProfile: "Speak professionally with a calm tone.",
        },
      },
    },
  },
}
```

Gemini API TTS uses natural-language prompting for style control: set `audioProfile` to prepend a reusable style prompt before the spoken text, and set `speakerName` when your prompt text refers to a named speaker. It also accepts expressive square-bracket audio tags in the text, such as `[whispers]` or `[laughs]`. To keep tags out of the visible chat reply while still sending them to TTS, wrap them in a `[[tts:text]]...[[/tts:text]]` block:

```text
Here is the clean reply text.

[[tts:text]][whispers] Here is the spoken version.[[/tts:text]]
```

A Google Cloud Console API key restricted to the Gemini API is valid for this provider; this is not the separate Cloud Text-to-Speech API path.

## Realtime voice

The bundled `google` plugin registers a realtime voice provider backed by the Gemini Live API for backend audio bridges such as Voice Call and Google Meet. Settings are configured under `plugins.entries.voice-call.config.realtime.providers.google.*`:

| Setting | Config path | Default |
| --- | --- | --- |
| Model | `...google.model` | `gemini-2.5-flash-native-audio-preview-12-2025` |
| Voice | `...google.voice` | `Kore` |
| Temperature | `...google.temperature` | (unset) |
| VAD start sensitivity | `...google.startSensitivity` | (unset) |
| VAD end sensitivity | `...google.endSensitivity` | (unset) |
| Silence duration | `...google.silenceDurationMs` | (unset) |
| Activity handling | `...google.activityHandling` | Google default, `start-of-activity-interrupts` |
| Turn coverage | `...google.turnCoverage` | Google default, `only-activity` |
| Disable auto VAD | `...google.automaticActivityDetectionDisabled` | `false` |
| Session resumption | `...google.sessionResumption` | `true` |
| Context compression | `...google.contextWindowCompression` | `true` |
| API key | `...google.apiKey` | Falls back to `models.providers.google.apiKey`, `GEMINI_API_KEY`, or `GOOGLE_API_KEY` |

Example Voice Call realtime config:

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        enabled: true,
        config: {
          realtime: {
            enabled: true,
            provider: "google",
            providers: {
              google: {
                model: "gemini-2.5-flash-native-audio-preview-12-2025",
                speakerVoice: "Kore",
                activityHandling: "start-of-activity-interrupts",
                turnCoverage: "only-activity",
              },
            },
          },
        },
      },
    },
  },
}
```

The Google Live API uses bidirectional audio and function calling over a WebSocket; OpenClaw adapts telephony/Meet bridge audio to Gemini's PCM Live API stream and keeps tool calls on the shared realtime voice contract. Leave `temperature` unset unless you need sampling changes — OpenClaw omits non-positive values because Google Live can return transcripts without audio for `temperature: 0`. Gemini API transcription is enabled without `languageCodes`; the current Google SDK rejects language-code hints on this API path. Control UI Talk supports Google Live browser sessions with constrained one-use tokens, and backend-only realtime voice providers can also run through the generic Gateway relay transport, which keeps provider credentials on the Gateway. For maintainer live verification, run `OPENAI_API_KEY=... GEMINI_API_KEY=... node --import tsx scripts/dev/realtime-talk-live-smoke.ts`: the smoke also covers OpenAI backend/WebRTC paths, while the Google leg mints the same constrained Live API token shape used by Control UI Talk, opens the browser WebSocket endpoint, sends the initial setup payload, and waits for `setupComplete`.

**Source**: OpenClaw documentation — `providers/google` (Image/Video/Music generation, Text-to-speech, Realtime voice sections; mirror `inbox/openclaw_docs/providers/google.md`)
**Last Updated**: 2026-06-22
**Status**: Active
