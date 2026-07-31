---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - text_to_speech
keywords:
  - inworld speech provider
  - inworld streaming tts
  - INWORLD_API_KEY http basic
  - openclaw/inworld-speech plugin
  - messages.tts.providers.inworld
  - inworld-tts-1.5-max
  - speakerVoiceId modelId temperature
  - ogg_opus pcm 22050 telephony
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/inworld
access_control_group: ["general"]
---

# OpenClaw — Configuring the Inworld Streaming TTS Provider

## Overview

This note is the configuration procedure for the **Inworld** streaming text-to-speech (TTS) provider in OpenClaw, mirroring the `providers/inworld` source page. Inworld synthesizes outbound reply audio (MP3 by default, OGG_OPUS for voice notes) and PCM audio for telephony channels such as Voice Call; OpenClaw posts to Inworld's streaming TTS endpoint, concatenates the returned base64 audio chunks into a single buffer, and hands the result to the standard reply-audio pipeline. The procedure covers installing the `@openclaw/inworld-speech` plugin, supplying the `INWORLD_API_KEY` HTTP-Basic (Base64 dashboard) credential, selecting Inworld under `messages.tts`, the five `messages.tts.providers.inworld.*` configuration options, the supported model ids, surface-driven audio output formats, and custom-endpoint overrides.

## Provider Properties

The provider's front-matter property table fixes the integration's contract and defaults:

| Property      | Value |
| ------------- | ----- |
| Provider id   | `inworld` |
| Plugin        | official external package |
| Contract      | `speechProviders` (TTS only) |
| Auth env var  | `INWORLD_API_KEY` (HTTP Basic, Base64 dashboard credential) |
| Base URL      | `https://api.inworld.ai` |
| Default voice | `Sarah` |
| Default model | `inworld-tts-1.5-max` |
| Output        | MP3 (default), OGG_OPUS (voice notes), PCM 22050 Hz (telephony) |

Website: [inworld.ai](https://inworld.ai). Provider docs: [docs.inworld.ai/tts/tts](https://docs.inworld.ai/tts/tts). Inworld implements the `speechProviders` (TTS-only) contract, so it serves outbound reply audio but is not an LLM chat or transcription provider.

## Install plugin

Install the official external plugin, then restart Gateway so the provider registers:

```bash
openclaw plugins install @openclaw/inworld-speech
openclaw gateway restart
```

## Getting started

The source page documents a three-step setup:

1. **Set your API key.** Copy the credential from your Inworld dashboard (Workspace > API Keys) and set it as an env var. The value is sent verbatim as the HTTP Basic credential, so do not Base64-encode it again or convert it to a bearer token. Set it as `INWORLD_API_KEY=<base64-credential-from-dashboard>`.
2. **Select Inworld in `messages.tts`.** Point the TTS layer at the `inworld` provider and configure its voice and model:

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "inworld",
      providers: {
        inworld: {
          speakerVoiceId: "Sarah",
          modelId: "inworld-tts-1.5-max",
        },
      },
    },
  },
}
```

3. **Send a message.** Send a reply through any connected channel. OpenClaw synthesizes the audio with Inworld and delivers it as MP3 (or OGG_OPUS when the channel expects a voice note).

## Configuration options

All Inworld settings live under `messages.tts.providers.inworld`:

| Option           | Path                                            | Description |
| ---------------- | ----------------------------------------------- | ----------- |
| `apiKey`         | `messages.tts.providers.inworld.apiKey`         | Base64 dashboard credential. Falls back to `INWORLD_API_KEY`. |
| `baseUrl`        | `messages.tts.providers.inworld.baseUrl`        | Override Inworld API base URL (default `https://api.inworld.ai`). |
| `speakerVoiceId` | `messages.tts.providers.inworld.speakerVoiceId` | Voice identifier (default `Sarah`). |
| `modelId`        | `messages.tts.providers.inworld.modelId`        | TTS model id (default `inworld-tts-1.5-max`). |
| `temperature`    | `messages.tts.providers.inworld.temperature`    | Sampling temperature `0..2` (optional). |

## Notes

The source page's accordion notes cover four operational details:

**Authentication.** Inworld uses HTTP Basic auth with a single Base64-encoded credential string. Copy it verbatim from the Inworld dashboard. The provider sends it as `Authorization: Basic <apiKey>` without any further encoding, so do not Base64-encode it yourself and do not pass a bearer-style token. See [TTS auth notes](https://docs.openclaw.ai/tools/tts#inworld-primary) for the same callout.

**Models.** Supported model ids: `inworld-tts-1.5-max` (default), `inworld-tts-1.5-mini`, `inworld-tts-1-max`, `inworld-tts-1`.

**Audio outputs.** Replies use MP3 by default. When the channel target is `voice-note` OpenClaw asks Inworld for `OGG_OPUS` so the audio plays as a native voice bubble. Telephony synthesis uses raw `PCM` at 22050 Hz to feed the telephony bridge.

**Custom endpoints.** Override the API host with `messages.tts.providers.inworld.baseUrl`. Trailing slashes are stripped before requests are sent.

**Source**: OpenClaw documentation — `providers/inworld` (mirror `inbox/openclaw_docs/providers/inworld.md`)
**Last Updated**: 2026-06-22
**Status**: Active
