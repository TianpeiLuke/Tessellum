---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - speech
keywords:
  - openclaw elevenlabs provider
  - elevenlabs text to speech
  - scribe v2 speech to text
  - scribe v2 realtime streaming stt
  - elevenlabs_api_key xi_api_key
  - messages.tts elevenlabs
  - voice call ulaw_8000 transcription
  - google meet transcriptionprovider
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/elevenlabs
access_control_group: ["general"]
---

# OpenClaw — Configure the ElevenLabs Voice/Media Provider

## Overview

This note is the setup procedure for wiring **ElevenLabs** into OpenClaw as a voice/media provider, mirroring the `providers/elevenlabs` source page. ElevenLabs is not an LLM provider — it supplies three speech surfaces: text-to-speech (TTS), batch speech-to-text (STT) with **Scribe v2**, and streaming STT with **Scribe v2 Realtime**. The procedure covers authentication via `ELEVENLABS_API_KEY` (or the compatibility alias `XI_API_KEY`), the `messages.tts` TTS provider block (including Discord streaming TTS and the `latencyTier` → `optimize_streaming_latency` mapping), the `tools.media.audio` Scribe v2 batch STT block for inbound audio attachments, and the `voice-call` / `google-meet` plugin `streaming` blocks for realtime transcription (defaulting to `ulaw_8000` to match Twilio telephony frames). The capability/surface/default summary the page leads with is reproduced below.

| Capability | OpenClaw surface | Default |
| --- | --- | --- |
| Text-to-speech | `messages.tts` / `talk` | `eleven_multilingual_v2` |
| Batch speech-to-text | `tools.media.audio` | `scribe_v2` |
| Streaming speech-to-text | Voice Call streaming or Google Meet `realtime.transcriptionProvider` | `scribe_v2_realtime` |

## Authentication

Set `ELEVENLABS_API_KEY` in the environment to authenticate every ElevenLabs surface (TTS, batch STT, streaming STT). `XI_API_KEY` is also accepted for compatibility with existing ElevenLabs tooling, so an environment that already exports `XI_API_KEY` works without renaming.

```bash
export ELEVENLABS_API_KEY="..."
```

## Text-to-speech

Configure ElevenLabs TTS under `messages.tts.providers.elevenlabs`. The `apiKey` is typically interpolated from the environment, `speakerVoiceId` selects the ElevenLabs voice, and `modelId` selects the TTS model. The default model for existing installs is `eleven_multilingual_v2`.

```json5
{
  messages: {
    tts: {
      providers: {
        elevenlabs: {
          apiKey: "${ELEVENLABS_API_KEY}",
          speakerVoiceId: "pMsXgVXv3BLzUgSXRplE",
          modelId: "eleven_multilingual_v2",
        },
      },
    },
  },
}
```

Set `modelId` to `eleven_v3` to use ElevenLabs v3 TTS; OpenClaw keeps `eleven_multilingual_v2` as the default for existing installs rather than auto-upgrading them. Discord voice channels use ElevenLabs' streaming TTS endpoint when ElevenLabs is the selected `voice.tts` / `messages.tts` provider: playback starts from the returned audio stream instead of waiting for OpenClaw to download and write the whole audio file first. The `latencyTier` setting maps to ElevenLabs' `optimize_streaming_latency` query parameter for models that accept it; OpenClaw omits that parameter for `eleven_v3`, which rejects it.

## Speech-to-text

Use **Scribe v2** for inbound audio attachments and short recorded voice segments by enabling the `tools.media.audio` block and listing ElevenLabs `scribe_v2` as a model. Setting `enabled: true` turns on audio handling; the `models` array selects the provider/model pair.

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "elevenlabs", model: "scribe_v2" }],
      },
    },
  },
}
```

OpenClaw sends multipart audio to the ElevenLabs `/v1/speech-to-text` endpoint with `model_id: "scribe_v2"`. Language hints map to `language_code` when present.

## Streaming STT

The bundled `elevenlabs` plugin registers **Scribe v2 Realtime** for Voice Call and Google Meet agent-mode streaming transcription. The settings, their config paths, and defaults are reproduced verbatim from the page below.

| Setting | Config path | Default |
| --- | --- | --- |
| API key | `plugins.entries.voice-call.config.streaming.providers.elevenlabs.apiKey` | Falls back to `ELEVENLABS_API_KEY` / `XI_API_KEY` |
| Model | `...elevenlabs.modelId` | `scribe_v2_realtime` |
| Audio format | `...elevenlabs.audioFormat` | `ulaw_8000` |
| Sample rate | `...elevenlabs.sampleRate` | `8000` |
| Commit strategy | `...elevenlabs.commitStrategy` | `vad` |
| Language | `...elevenlabs.languageCode` | (unset) |

Enable streaming STT for the Voice Call channel by configuring the `streaming` block under the `voice-call` plugin entry — set `enabled: true`, select `provider: "elevenlabs"`, and supply the provider-specific block.

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          streaming: {
            enabled: true,
            provider: "elevenlabs",
            providers: {
              elevenlabs: {
                apiKey: "${ELEVENLABS_API_KEY}",
                audioFormat: "ulaw_8000",
                commitStrategy: "vad",
                languageCode: "en",
              },
            },
          },
        },
      },
    },
  },
}
```

Voice Call receives Twilio media as 8 kHz G.711 u-law. The ElevenLabs realtime provider defaults to `ulaw_8000`, so telephony frames can be forwarded without transcoding. For Google Meet agent mode, set `plugins.entries.google-meet.config.realtime.transcriptionProvider` to `"elevenlabs"` and configure the same provider block under `plugins.entries.google-meet.config.realtime.providers.elevenlabs`.

**Source**: OpenClaw documentation — `providers/elevenlabs` (mirror `inbox/openclaw_docs/providers/elevenlabs.md`)
**Last Updated**: 2026-06-22
**Status**: Active
