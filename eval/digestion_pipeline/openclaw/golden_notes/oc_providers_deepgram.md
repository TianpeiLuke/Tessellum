---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - speech_to_text
keywords:
  - openclaw deepgram provider
  - deepgram speech-to-text
  - tools.media.audio deepgram
  - voice call streaming stt
  - deepgram nova-3 model
  - deepgram listen websocket
  - g.711 u-law mulaw 8khz
  - DEEPGRAM_API_KEY
  - deepgram endpointing interim results
topics:
  - OpenClaw
  - Providers
  - Speech-to-Text
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/deepgram
access_control_group: ["general"]
---

# OpenClaw — Configuring the Deepgram Speech-to-Text Provider

## Overview

This note is the setup procedure for the OpenClaw **Deepgram** provider, mirroring the `providers/deepgram` source page. Deepgram is a speech-to-text API used in OpenClaw two ways: batch transcription of inbound audio/voice notes through `tools.media.audio`, and Voice Call realtime streaming STT through `plugins.entries.voice-call.config.streaming`. For batch transcription OpenClaw uploads the complete audio file to Deepgram and injects the transcript into the reply pipeline (a `{{Transcript}}` substitution plus an `[Audio]` block); for Voice Call streaming OpenClaw forwards live G.711 u-law frames over Deepgram's WebSocket `listen` endpoint and emits partial or final transcripts as Deepgram returns them. Auth is `DEEPGRAM_API_KEY` and the default model is `nova-3` (Website [deepgram.com](https://deepgram.com); Docs [developers.deepgram.com](https://developers.deepgram.com)). This note covers the intro/property table, Getting started, Configuration options, Voice Call streaming STT, and Notes sections.

## Getting started

Three steps wire up batch transcription of inbound voice notes. First, set your Deepgram API key in the environment (the key format shown is `dg_...`):

```
DEEPGRAM_API_KEY=dg_...
```

Second, enable the audio provider by registering `deepgram` with the `nova-3` model under `tools.media.audio`:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "deepgram", model: "nova-3" }],
      },
    },
  },
}
```

Third, send an audio message through any connected channel. OpenClaw transcribes it via Deepgram and injects the transcript into the reply pipeline.

## Configuration options

The batch (`tools.media.audio`) options are listed below. `model` and `language` are set per entry in the `models[]` array, while `detect_language`, `punctuate`, and `smart_format` are set under `tools.media.audio.providerOptions.deepgram`. All except the default model are optional.

| Option | Path | Description |
| --- | --- | --- |
| `model` | `tools.media.audio.models[].model` | Deepgram model id (default: `nova-3`) |
| `language` | `tools.media.audio.models[].language` | Language hint (optional) |
| `detect_language` | `tools.media.audio.providerOptions.deepgram.detect_language` | Enable language detection (optional) |
| `punctuate` | `tools.media.audio.providerOptions.deepgram.punctuate` | Enable punctuation (optional) |
| `smart_format` | `tools.media.audio.providerOptions.deepgram.smart_format` | Enable smart formatting (optional) |

A language hint is added as a `language` key on the model entry — for example pinning English:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "deepgram", model: "nova-3", language: "en" }],
      },
    },
  },
}
```

The optional Deepgram processing flags are set under `providerOptions.deepgram` alongside the same `models[]` entry:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        providerOptions: {
          deepgram: {
            detect_language: true,
            punctuate: true,
            smart_format: true,
          },
        },
        models: [{ provider: "deepgram", model: "nova-3" }],
      },
    },
  },
}
```

## Voice Call streaming STT

The bundled `deepgram` plugin also registers a realtime transcription provider for the Voice Call plugin. Its settings live under `plugins.entries.voice-call.config.streaming.providers.deepgram`; the `apiKey` falls back to `DEEPGRAM_API_KEY` when unset.

| Setting | Config path | Default |
| --- | --- | --- |
| API key | `plugins.entries.voice-call.config.streaming.providers.deepgram.apiKey` | Falls back to `DEEPGRAM_API_KEY` |
| Model | `...deepgram.model` | `nova-3` |
| Language | `...deepgram.language` | (unset) |
| Encoding | `...deepgram.encoding` | `mulaw` |
| Sample rate | `...deepgram.sampleRate` | `8000` |
| Endpointing | `...deepgram.endpointingMs` | `800` |
| Interim results | `...deepgram.interimResults` | `true` |

A minimal streaming config enables Voice Call streaming, selects `deepgram` as the provider, and supplies the per-provider block:

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          streaming: {
            enabled: true,
            provider: "deepgram",
            providers: {
              deepgram: {
                apiKey: "${DEEPGRAM_API_KEY}",
                model: "nova-3",
                endpointingMs: 800,
                language: "en-US",
              },
            },
          },
        },
      },
    },
  },
}
```

Voice Call receives telephony audio as 8 kHz G.711 u-law. The Deepgram streaming provider defaults to `encoding: "mulaw"` and `sampleRate: 8000`, so Twilio media frames can be forwarded directly.

## Notes

Authentication follows the standard provider auth order; `DEEPGRAM_API_KEY` is the simplest path. For proxies, override endpoints or headers with `tools.media.audio.baseUrl` and `tools.media.audio.headers`. Output behavior follows the same audio rules as other providers (size caps, timeouts, transcript injection).

**Source**: OpenClaw documentation — `providers/deepgram` (mirror `inbox/openclaw_docs/providers/deepgram.md`)
**Last Updated**: 2026-06-22
**Status**: Active
