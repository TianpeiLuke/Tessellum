---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - tts
keywords:
  - openclaw azure speech provider
  - azure ai speech text-to-speech
  - AZURE_SPEECH_KEY AZURE_SPEECH_REGION
  - messages.tts provider azure-speech
  - en-US-JennyNeural speakerVoice
  - ogg opus voice note output
  - mulaw telephony voice call audio
  - azure-speech vs azure alias
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/azure-speech
access_control_group: ["general"]
---

# OpenClaw — Configuring the Azure AI Speech Text-to-Speech Provider

## Overview

This note is the setup procedure for **Azure Speech**, OpenClaw's bundled Azure AI Speech text-to-speech (TTS) provider that synthesizes outbound reply audio. It mirrors the `providers/azure-speech` source page: authenticating with `AZURE_SPEECH_KEY` plus `AZURE_SPEECH_REGION`, selecting the provider under `messages.tts`, the per-option configuration table (`apiKey`/`region`/`endpoint`/`baseUrl`/`speakerVoice`/`lang`/`outputFormat`/`voiceNoteOutputFormat`), and the four operator notes (authentication header, voice ShortNames, audio output formats, and the `azure-speech` vs `azure` alias). Azure Speech is a TTS-only provider — it synthesizes outbound speech and does not transcribe inbound audio.

OpenClaw calls the Azure Speech REST API directly with SSML and sends the provider-owned output format through the `X-Microsoft-OutputFormat` header. By default it emits MP3 (`audio-24khz-48kbitrate-mono-mp3`) for standard audio, native Ogg/Opus (`ogg-24khz-16bit-mono-opus`) for voice notes, and 8 kHz mulaw audio for telephony channels such as Voice Call. The default voice is `en-US-JennyNeural`.

## Getting started

The source page walks three `<Steps>`:

1. **Create an Azure Speech resource.** In the Azure portal, create a Speech resource. Copy **KEY 1** from *Resource Management > Keys and Endpoint*, and copy the resource location such as `eastus`. Set the credentials as environment variables:

```
AZURE_SPEECH_KEY=<speech-resource-key>
AZURE_SPEECH_REGION=eastus
```

2. **Select Azure Speech in `messages.tts`.** Point the TTS provider at `azure-speech` and configure the per-provider block. The source uses `json5` config:

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "azure-speech",
      providers: {
        "azure-speech": {
          speakerVoice: "en-US-JennyNeural",
          lang: "en-US",
        },
      },
    },
  },
}
```

3. **Send a message.** Send a reply through any connected channel. OpenClaw synthesizes the audio with Azure Speech and delivers MP3 for standard audio, or Ogg/Opus when the channel expects a voice note.

## Configuration options

All options live under `messages.tts.providers.azure-speech.*`. The source page documents these keys (paths and defaults verbatim):

| Option | Path | Description |
| --- | --- | --- |
| `apiKey` | `messages.tts.providers.azure-speech.apiKey` | Azure Speech resource key. Falls back to `AZURE_SPEECH_KEY`, `AZURE_SPEECH_API_KEY`, or `SPEECH_KEY`. |
| `region` | `messages.tts.providers.azure-speech.region` | Azure Speech resource region. Falls back to `AZURE_SPEECH_REGION` or `SPEECH_REGION`. |
| `endpoint` | `messages.tts.providers.azure-speech.endpoint` | Optional Azure Speech endpoint/base URL override. |
| `baseUrl` | `messages.tts.providers.azure-speech.baseUrl` | Optional Azure Speech base URL override. |
| `speakerVoice` | `messages.tts.providers.azure-speech.speakerVoice` | Azure voice ShortName (default `en-US-JennyNeural`). Legacy alias: `voice`. |
| `lang` | `messages.tts.providers.azure-speech.lang` | SSML language code (default `en-US`). |
| `outputFormat` | `messages.tts.providers.azure-speech.outputFormat` | Audio-file output format (default `audio-24khz-48kbitrate-mono-mp3`). |
| `voiceNoteOutputFormat` | `messages.tts.providers.azure-speech.voiceNoteOutputFormat` | Voice-note output format (default `ogg-24khz-16bit-mono-opus`). |

## Notes

The source page's `<AccordionGroup>` covers four operator notes:

- **Authentication.** Azure Speech uses a Speech resource key, **not** an Azure OpenAI key. The key is sent as the `Ocp-Apim-Subscription-Key` header; OpenClaw derives `https://<region>.tts.speech.microsoft.com` from `region` unless you provide `endpoint` or `baseUrl`.
- **Voice names.** Use the Azure Speech voice `ShortName` value, for example `en-US-JennyNeural`. The bundled provider can list voices through the same Speech resource and filters voices marked deprecated or retired.
- **Audio outputs.** Azure accepts output formats such as `audio-24khz-48kbitrate-mono-mp3`, `ogg-24khz-16bit-mono-opus`, and `riff-24khz-16bit-mono-pcm`. OpenClaw requests Ogg/Opus for `voice-note` targets so channels can send native voice bubbles without an extra MP3 conversion.
- **Alias.** `azure` is accepted as a provider alias for existing PRs and user config, but new config should use `azure-speech` to avoid confusion with Azure OpenAI model providers.

**Source**: OpenClaw documentation — `providers/azure-speech` (mirror `inbox/openclaw_docs/providers/azure-speech.md`)
**Last Updated**: 2026-06-22
**Status**: Active
