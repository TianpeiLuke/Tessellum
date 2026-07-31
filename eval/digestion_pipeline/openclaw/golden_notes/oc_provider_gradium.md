---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - text_to_speech
keywords:
  - openclaw gradium provider
  - gradium-speech plugin
  - GRADIUM_API_KEY
  - messages.tts.providers.gradium
  - speakerVoiceId voice override
  - per-message voice directive
  - gradium auto-select order 30
  - wav opus ulaw output
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/gradium
access_control_group: ["general"]
---

# OpenClaw — Configuring the Gradium Text-to-Speech Provider

## Overview

This note is the per-provider configuration procedure for **Gradium**, a text-to-speech (TTS) provider for OpenClaw, mirroring the `providers/gradium` source page. It walks through installing the official `@openclaw/gradium-speech` plugin, supplying credentials (`GRADIUM_API_KEY` env var or config `apiKey`), the `messages.tts.providers.gradium` config block, the seven-voice catalog and per-message `/voice:` directive overrides, the surface-driven output formats (WAV / Opus / 8 kHz u-law), and Gradium's auto-select priority of `30`. The provider can render normal audio replies (WAV), voice-note-compatible Opus output, and 8 kHz u-law audio for telephony surfaces.

The provider property summary from the source front matter is: Provider id `gradium`; Auth `GRADIUM_API_KEY` or config `apiKey`; Base URL `https://api.gradium.ai` (default); Default voice `Emma` (`YTpq7expH9539ERJ`). The shared TTS provider-selection and tool behavior are owned by the Text-to-Speech and Media Overview tool pages and are linked, not duplicated, here.

## Install plugin

Install the official plugin, then restart Gateway:

```bash
openclaw plugins install @openclaw/gradium-speech
openclaw gateway restart
```

## Setup

Create a Gradium API key, then expose it to OpenClaw with either an env var or the config key. The env-var form exports `GRADIUM_API_KEY="gsk_..."`. The config-key form sets it under `messages.tts.providers.gradium.apiKey`:

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "gradium",
      providers: {
        gradium: {
          apiKey: "${GRADIUM_API_KEY}",
        },
      },
    },
  },
}
```

The plugin checks the resolved `apiKey` first and falls back to the `GRADIUM_API_KEY` environment variable.

## Config

The full config block pins the default voice via `speakerVoiceId` and optionally overrides `apiKey` / `baseUrl`:

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "gradium",
      providers: {
        gradium: {
          speakerVoiceId: "YTpq7expH9539ERJ",
          // apiKey: "${GRADIUM_API_KEY}",
          // baseUrl: "https://api.gradium.ai",
        },
      },
    },
  },
}
```

The three documented config keys are:

| Key | Type | Description |
| --- | --- | --- |
| `messages.tts.providers.gradium.apiKey` | string | Resolved API key. Supports `${ENV}` and secret refs. |
| `messages.tts.providers.gradium.baseUrl` | string | Override the API origin. Trailing slashes are stripped. Defaults to `https://api.gradium.ai`. |
| `messages.tts.providers.gradium.speakerVoiceId` | string | Default voice id used when no directive override is present. |

The output audio format is selected automatically by the runtime based on the target surface and is not configurable from `openclaw.json` (see "Output" below).

## Voices

Gradium ships seven named voices; the default is **Emma**:

| Name | Voice ID |
| --- | --- |
| Emma | `YTpq7expH9539ERJ` |
| Kent | `LFZvm12tW_z0xfGo` |
| Tiffany | `Eu9iL_CYe8N-Gkx_` |
| Christina | `2H4HY2CBNyJHBCrP` |
| Sydney | `jtEKaLYNn6iif5PR` |
| John | `KWJiFWu2O9nMPYcR` |
| Arthur | `3jUdJyOi9pgbxBTK` |

### Per-message voice override

When the active speech policy allows voice overrides, you can switch voices inline using a directive token. Use `speakerVoiceId` for provider-native voice ids. The accepted directive tokens are:

```text
/voice:LFZvm12tW_z0xfGo
/voice_id:LFZvm12tW_z0xfGo
/voiceid:LFZvm12tW_z0xfGo
/gradium_voice:LFZvm12tW_z0xfGo
/gradiumvoice:LFZvm12tW_z0xfGo
```

If the speech policy disables voice overrides, the directive is consumed but ignored.

## Output

The runtime picks the output format from the target surface; the provider does not synthesize other formats today. The three surface-to-format mappings are:

| Target | Format | File ext | Sample rate | Voice-compatible flag |
| --- | --- | --- | --- | --- |
| Standard audio | `wav` | `.wav` | provider | no |
| Voice note | `opus` | `.opus` | provider | yes |
| Telephony | `ulaw_8000` | n/a | 8 kHz | n/a |

## Auto-select order

Among configured TTS providers, Gradium's auto-select order is `30`. The Text-to-Speech tool page describes how OpenClaw picks the active provider when `messages.tts.provider` is not pinned.

**Source**: OpenClaw documentation — `providers/gradium` (mirror `inbox/openclaw_docs/providers/gradium.md`)
**Last Updated**: 2026-06-22
**Status**: Active
