---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - tts
keywords:
  - openclaw tts setup
  - messages.tts provider config
  - text-to-speech providers
  - elevenlabs openai azure speech tts
  - per-agent voice override
  - tts prefsPath local preferences
  - tts auto always provider
  - speech provider api key
topics:
  - OpenClaw
  - Text-to-Speech
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/tts
access_control_group: ["general"]
---

# OpenClaw — Enabling and Configuring Text-to-Speech (Providers, Config, Overrides)

## Overview

This note is the setup-and-configuration procedure for OpenClaw text-to-speech (TTS): how to enable audio replies, the 14-provider support matrix with auth, the `messages.tts` provider config blocks, per-agent/channel/account override precedence, and per-user local preferences. It mirrors the setup half of the `tools/tts` source page (intro, Quick start, Supported providers, Configuration, Per-agent voice overrides, Per-user preferences). Personas, model-driven `[[tts:...]]` directives, and the `/tts` slash commands are covered in the split sibling `oc_tools_tts_personas_directives`; output formats, Auto-TTS decision flow, the `messages.tts.*` field reference, the `tts` agent tool, and gateway TTS RPC live in `oc_tools_tts_output_reference`.

OpenClaw can convert outbound replies into audio across **14 speech providers** and deliver native voice messages on Feishu, Matrix, Telegram, and WhatsApp, audio attachments everywhere else, and PCM/Ulaw streams for telephony and Talk. TTS is the speech-output half of Talk's `stt-tts` mode; provider-native `realtime` Talk sessions synthesize speech inside the realtime provider instead of calling this TTS path, while `transcription` sessions do not synthesize an assistant voice response.

## Quick start

Four steps enable TTS for replies:

1. **Pick a provider** — OpenAI and ElevenLabs are the most reliable hosted options; Microsoft and Local CLI work without an API key. See the provider matrix below for the full list.
2. **Set the API key** — export the env var for your provider (for example `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`). Microsoft and Local CLI need no key.
3. **Enable in config** — set `messages.tts.auto: "always"` and `messages.tts.provider`:

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "elevenlabs",
    },
  },
}
```

4. **Try it in chat** — `/tts status` shows the current state; `/tts audio Hello from OpenClaw` sends a one-off audio reply.

Auto-TTS is **off** by default. When `messages.tts.provider` is unset, OpenClaw picks the first configured provider in registry auto-select order. The built-in `tts` agent tool is explicit-intent only: ordinary chat stays text unless the user asks for audio, uses `/tts`, or enables Auto-TTS/directive speech.

## Supported providers

OpenClaw supports 14 speech providers. The table reproduces each provider's auth requirements and notes verbatim from source:

| Provider | Auth | Notes |
|---|---|---|
| **Azure Speech** | `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION` (also `AZURE_SPEECH_API_KEY`, `SPEECH_KEY`, `SPEECH_REGION`) | Native Ogg/Opus voice-note output and telephony. |
| **DeepInfra** | `DEEPINFRA_API_KEY` | OpenAI-compatible TTS. Defaults to `hexgrad/Kokoro-82M`. |
| **ElevenLabs** | `ELEVENLABS_API_KEY` or `XI_API_KEY` | Voice cloning, multilingual, deterministic via `seed`; streamed for Discord voice playback. |
| **Google Gemini** | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | Gemini API batch TTS; persona-aware via `promptTemplate: "audio-profile-v1"`. |
| **Gradium** | `GRADIUM_API_KEY` | Voice-note and telephony output. |
| **Inworld** | `INWORLD_API_KEY` | Streaming TTS API. Native Opus voice-note and PCM telephony. |
| **Local CLI** | none | Runs a configured local TTS command. |
| **Microsoft** | none | Public Edge neural TTS via `node-edge-tts`. Best-effort, no SLA. |
| **MiniMax** | `MINIMAX_API_KEY` (or Token Plan: `MINIMAX_OAUTH_TOKEN`, `MINIMAX_CODE_PLAN_KEY`, `MINIMAX_CODING_API_KEY`) | T2A v2 API. Defaults to `speech-2.8-hd`. |
| **OpenAI** | `OPENAI_API_KEY` | Also used for auto-summary; supports persona `instructions`. |
| **OpenRouter** | `OPENROUTER_API_KEY` (can reuse `models.providers.openrouter.apiKey`) | Default model `hexgrad/kokoro-82m`. |
| **Volcengine** | `VOLCENGINE_TTS_API_KEY` or `BYTEPLUS_SEED_SPEECH_API_KEY` (legacy AppID/token: `VOLCENGINE_TTS_APPID`/`_TOKEN`) | BytePlus Seed Speech HTTP API. |
| **Vydra** | `VYDRA_API_KEY` | Shared image, video, and speech provider. |
| **xAI** | `XAI_API_KEY` | xAI batch TTS. Native Opus voice-note is **not** supported. |
| **Xiaomi MiMo** | `XIAOMI_API_KEY` | MiMo TTS through Xiaomi chat completions. |

If multiple providers are configured, the selected one is used first and the others are fallback options. Auto-summary uses `summaryModel` (or `agents.defaults.model.primary`), so that provider must also be authenticated if you keep summaries enabled.

The bundled **Microsoft** provider uses Microsoft Edge's online neural TTS service via `node-edge-tts` — a public web service without a published SLA or quota, so treat it as best-effort. The legacy provider id `edge` is normalized to `microsoft`, and `openclaw doctor --fix` rewrites persisted config; new configs should always use `microsoft`.

## Configuration

TTS config lives under `messages.tts` in `~/.openclaw/openclaw.json`. Pick a preset and adapt the provider block; OpenClaw documents one config block per provider. Two representative provider blocks (ElevenLabs and the OpenAI + ElevenLabs fallback pair) are reproduced verbatim below; the remaining provider blocks (Azure Speech, DeepInfra, Google Gemini, Gradium, Inworld, Local CLI, Microsoft, MiniMax, OpenRouter, Volcengine, xAI, Xiaomi MiMo) follow the same `messages.tts.providers.<id>` shape with the provider-specific keys listed in the matrix above and detailed in the field reference (`oc_tools_tts_output_reference`).

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "elevenlabs",
      providers: {
        elevenlabs: {
          apiKey: "${ELEVENLABS_API_KEY}",
          model: "eleven_multilingual_v2",
          speakerVoiceId: "EXAVITQu4vr4xnSDxMaL",
        },
      },
    },
  },
}
```

The OpenAI + ElevenLabs preset configures a primary provider plus a fallback, enables the auto-summary model, and turns on model overrides:

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "openai",
      summaryModel: "openai/gpt-4.1-mini",
      modelOverrides: { enabled: true },
      providers: {
        openai: {
          apiKey: "${OPENAI_API_KEY}",
          model: "gpt-4o-mini-tts",
          speakerVoice: "alloy",
        },
        elevenlabs: {
          apiKey: "${ELEVENLABS_API_KEY}",
          model: "eleven_multilingual_v2",
          speakerVoiceId: "EXAVITQu4vr4xnSDxMaL",
          voiceSettings: { stability: 0.5, similarityBoost: 0.75, style: 0.0, useSpeakerBoost: true, speed: 1.0 },
          applyTextNormalization: "auto",
          languageCode: "en",
        },
      },
    },
  },
}
```

Provider-specific notes from the source's config tabs: Microsoft (no key) sets `enabled: true` plus `speakerVoice`, `lang`, `outputFormat`, `rate`, and `pitch`; Local CLI (`tts-local-cli`) sets `command`, `args` (supporting `{{OutputPath}}` and `{{Text}}` placeholders), `outputFormat`, and `timeoutMs`; OpenRouter sets `model: "hexgrad/kokoro-82m"`, `speakerVoice: "af_alloy"`, and `responseFormat: "mp3"`. For Xiaomi `mimo-v2.5-tts-voicedesign`, omit `speakerVoice` and set `style` to the voice-design prompt — OpenClaw sends that prompt as the TTS `user` message and does not send `audio.voice` for the voicedesign model.

### Per-agent voice overrides

Use `agents.list[].tts` when one agent should speak with a different provider, voice, model, persona, or auto-TTS mode. The agent block deep-merges over `messages.tts`, so provider credentials can stay in the global provider config:

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "elevenlabs",
      providers: {
        elevenlabs: { apiKey: "${ELEVENLABS_API_KEY}", model: "eleven_multilingual_v2" },
      },
    },
  },
  agents: {
    list: [
      {
        id: "reader",
        tts: {
          providers: {
            elevenlabs: { speakerVoiceId: "EXAVITQu4vr4xnSDxMaL" },
          },
        },
      },
    ],
  },
}
```

To pin a per-agent persona, set `agents.list[].tts.persona` alongside provider config — it overrides the global `messages.tts.persona` for that agent only.

Precedence order for automatic replies, `/tts audio`, `/tts status`, and the `tts` agent tool is, from lowest to highest:

1. `messages.tts`
2. active `agents.list[].tts`
3. channel override, when the channel supports `channels.<channel>.tts`
4. account override, when the channel passes `channels.<channel>.accounts.<id>.tts`
5. local `/tts` preferences for this host
6. inline `[[tts:...]]` directives when model overrides are enabled (see `oc_tools_tts_personas_directives`)

Channel and account overrides use the same shape as `messages.tts` and deep-merge over the earlier layers, so shared provider credentials can stay in `messages.tts` while a channel or bot account changes only speaker voice, model, persona, or auto mode (e.g. a `channels.feishu.accounts.english.tts` block overriding only `openai.speakerVoice`).

## Per-user preferences

Slash commands write local overrides to `prefsPath`. The default is `~/.openclaw/settings/tts.json`; override it with the `OPENCLAW_TTS_PREFS` env var or `messages.tts.prefsPath`. The stored fields and their effects:

| Stored field | Effect |
|---|---|
| `auto` | Local auto-TTS override (`always`, `off`, …) |
| `provider` | Local primary provider override |
| `persona` | Local persona override |
| `maxLength` | Summary threshold (default `1500` chars) |
| `summarize` | Summary toggle (default `true`) |

These override the effective config from `messages.tts` plus the active `agents.list[].tts` block for that host.

**Source**: OpenClaw documentation — `tools/tts` (mirror `inbox/openclaw_docs/tools/tts.md`)
**Last Updated**: 2026-06-22
**Status**: Active
