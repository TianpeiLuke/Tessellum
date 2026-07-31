---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - senseaudio
keywords:
  - openclaw senseaudio provider
  - senseaudio batch speech-to-text
  - SENSEAUDIO_API_KEY
  - tools.media.audio audio provider
  - senseaudio-asr-pro-1.5-260319
  - mediaUnderstandingProviders audio
  - inbound voice note transcription
  - openai-compatible transcription endpoint
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/senseaudio
access_control_group: ["general"]
---

# OpenClaw — Configuring the SenseAudio Speech-to-Text Provider

## Overview

This note is the setup procedure for the **SenseAudio** provider in OpenClaw — a bundled, batch speech-to-text (STT/ASR) provider that transcribes inbound audio and voice-note attachments through OpenClaw's shared `tools.media.audio` pipeline. It mirrors the `providers/senseaudio` source page: the provider header table, the three-step Getting started flow (set the API key, enable the audio provider, send a voice note), and the audio options table. The procedure covers exporting `SENSEAUDIO_API_KEY`, wiring `tools.media.audio` to the `senseaudio` provider with the default `senseaudio-asr-pro-1.5-260319` model, and the per-model/per-request option paths. SenseAudio is **batch STT only**; realtime Voice Call transcription continues to use streaming-STT providers.

## Provider Reference

SenseAudio can transcribe inbound audio and voice-note attachments through OpenClaw's shared `tools.media.audio` pipeline. OpenClaw posts multipart audio to the OpenAI-compatible transcription endpoint and injects the returned text as `{{Transcript}}` plus an `[Audio]` block. The provider's identifying properties (verbatim from the source header table):

| Property | Value |
| --- | --- |
| Provider id | `senseaudio` |
| Plugin | bundled, `enabledByDefault: true` |
| Contract | `mediaUnderstandingProviders` (audio) |
| Auth env var | `SENSEAUDIO_API_KEY` |
| Default model | `senseaudio-asr-pro-1.5-260319` |
| Default URL | `https://api.senseaudio.cn/v1` |
| Website | [senseaudio.cn](https://senseaudio.cn) |
| Docs | [senseaudio.cn/docs](https://senseaudio.cn/docs) |

Because the plugin is bundled and `enabledByDefault: true`, no separate `plugins install` step is required; the provider is registered at gateway start and only needs the API key plus the audio-pipeline wiring below.

## Getting started

The source page documents three steps to start transcribing voice notes.

**Step 1 — Set your API key.** Export the SenseAudio key into the gateway environment:

```bash
export SENSEAUDIO_API_KEY="..."
```

**Step 2 — Enable the audio provider.** Wire the shared `tools.media.audio` pipeline to the `senseaudio` provider with the default model:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "senseaudio", model: "senseaudio-asr-pro-1.5-260319" }],
      },
    },
  },
}
```

**Step 3 — Send a voice note.** Send an audio message through any connected channel. OpenClaw uploads the audio to SenseAudio and uses the transcript in the reply pipeline (injected as `{{Transcript}}` plus an `[Audio]` block, per the Overview).

## Options

The audio provider exposes the following options. Each option's value, config path, and meaning are verbatim from the source page:

| Option | Path | Description |
| --- | --- | --- |
| `model` | `tools.media.audio.models[].model` | SenseAudio ASR model id |
| `language` | `tools.media.audio.models[].language` | Optional language hint |
| `prompt` | `tools.media.audio.prompt` | Optional transcription prompt |
| `baseUrl` | `tools.media.audio.baseUrl` or model | Override the OpenAI-compatible base |
| `headers` | `tools.media.audio.request.headers` | Extra request headers |

SenseAudio is batch STT only in OpenClaw. Voice Call realtime transcription continues to use providers with streaming STT support.

**Source**: OpenClaw documentation — `providers/senseaudio` (mirror `inbox/openclaw_docs/providers/senseaudio.md`)
**Last Updated**: 2026-06-22
**Status**: Active
