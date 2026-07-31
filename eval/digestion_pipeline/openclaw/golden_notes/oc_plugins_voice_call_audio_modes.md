---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - voice_call
keywords:
  - openclaw voice call audio modes
  - realtime voice conversations
  - streaming transcription
  - tts for calls deep-merge
  - realtime toolPolicy consultPolicy
  - openclaw_agent_consult
  - agentContext capsule
  - webhook security replay protection
topics:
  - OpenClaw
  - Voice Call Plugin
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/voice-call
access_control_group: ["general"]
---

# OpenClaw — Voice Call Audio-Mode Contract (Realtime / Streaming / TTS / Webhook Security)

## Overview

This note models the **audio-mode contract** of the OpenClaw Voice Call plugin — the mutually-exclusive choice between full-duplex **realtime voice** and **streaming transcription** for live call audio, the **TTS-for-calls** deep-merge, and the **webhook security** model — mirroring the `plugins/voice-call` source page's "Realtime voice conversations", "Streaming transcription", "TTS for calls", and "Webhook security" sections. The operator setup, CLI, inbound-call policy, per-number routing, stale-call reaper, agent tool, RPC, and troubleshooting are documented in the sibling note [oc_plugins_voice_call_setup](oc_plugins_voice_call_setup.md). The central invariant: `realtime.enabled` and `streaming.enabled` cannot both be true — each call picks exactly one audio mode, with TTS-for-calls layered on top for spoken output.

## Mode selection: realtime vs streaming (mutually exclusive)

`realtime` selects a full-duplex realtime voice provider for live call audio; `streaming` selects a realtime transcription provider for live call audio. They are distinct: `realtime` runs a full-duplex voice conversation, while `streaming` only forwards audio to realtime transcription providers. The source states the hard constraint explicitly: `realtime.enabled` cannot be combined with `streaming.enabled` — pick one audio mode per call. The `openclaw voicecall setup` verifier checks that only one audio mode (`streaming` or `realtime`) is active, and the realtime troubleshooting path begins with "Confirm only one audio mode is enabled." Both modes fail soft: if the configured provider is unregistered (or none is registered), Voice Call logs a warning and skips realtime media / media streaming rather than failing the whole plugin.

## Realtime voice conversations

`realtime.enabled` is supported for **Twilio Media Streams**. `realtime.provider` is optional — if unset, Voice Call uses the first registered realtime voice provider. The bundled realtime voice providers are **Google Gemini Live (`google`)** and **OpenAI (`openai`)**, registered by their provider plugins. Provider-owned raw config lives under `realtime.providers.<providerId>`. By default Voice Call exposes the shared `openclaw_agent_consult` realtime tool; the realtime model can call it when the caller asks for deeper reasoning, current information, or normal OpenClaw tools. If `realtime.provider` points at an unregistered provider, or no realtime voice provider is registered at all, Voice Call logs a warning and skips realtime media instead of failing the whole plugin. Consult session keys reuse the stored call session when available, then fall back to the configured `sessionScope` (`per-phone` by default, or `per-call` for isolated calls).

Two context-acceleration options are default-off. `realtime.agentContext.enabled` (default-off): when enabled, Voice Call injects a bounded agent identity and selected workspace-file capsule into the realtime provider instructions at session setup. `realtime.fastContext.enabled` (default-off): when enabled, Voice Call first searches indexed memory/session context for the consult question and returns those snippets to the realtime model within `realtime.fastContext.timeoutMs` before falling back to the full consult agent only if `realtime.fastContext.fallbackToConsult` is true. `realtime.consultPolicy` optionally adds guidance for when the realtime model should call `openclaw_agent_consult`.

### Tool policy

`realtime.toolPolicy` controls the consult run:

| Policy           | Behavior                                                                                                                                 |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `safe-read-only` | Expose the consult tool and limit the regular agent to `read`, `web_search`, `web_fetch`, `x_search`, `memory_search`, and `memory_get`. |
| `owner`          | Expose the consult tool and let the regular agent use the normal agent tool policy.                                                      |
| `none`           | Do not expose the consult tool. Custom `realtime.tools` are still passed through to the realtime provider.                               |

`realtime.consultPolicy` controls only the realtime model instructions (not tool exposure):

| Policy        | Guidance                                                                                        |
| ------------- | ----------------------------------------------------------------------------------------------- |
| `auto`        | Keep the default prompt and let the provider decide when to call the consult tool.              |
| `substantive` | Answer simple conversational glue directly and consult before facts, memory, tools, or context. |
| `always`      | Consult before every substantive answer.                                                        |

### Agent voice context

Enable `realtime.agentContext` when the voice bridge should sound like the configured OpenClaw agent without paying a full agent-consult round trip on ordinary turns. The context capsule is added once when the realtime session is created, so it does not add per-turn latency. Calls to `openclaw_agent_consult` still run the full OpenClaw agent and should be used for tool work, current information, memory lookups, or workspace state.

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          agentId: "main",
          realtime: {
            enabled: true,
            provider: "google",
            toolPolicy: "safe-read-only",
            consultPolicy: "substantive",
            agentContext: {
              enabled: true,
              maxChars: 6000,
              includeIdentity: true,
              includeWorkspaceFiles: true,
              files: ["SOUL.md", "IDENTITY.md", "USER.md"],
            },
          },
        },
      },
    },
  },
}
```

### Realtime provider examples

**Google Gemini Live** defaults: API key from `realtime.providers.google.apiKey`, `GEMINI_API_KEY`, or `GOOGLE_GENERATIVE_AI_API_KEY`; model `gemini-2.5-flash-native-audio-preview-12-2025`; voice `Kore`. `sessionResumption` and `contextWindowCompression` default on for longer, reconnectable calls. Use `silenceDurationMs`, `startSensitivity`, and `endSensitivity` to tune faster turn-taking on telephony audio. The OpenAI realtime tab sets `provider: "openai"` with API key from `providers.openai.apiKey` (`${OPENAI_API_KEY}`). See the [Google provider](https://docs.openclaw.ai/providers/google) and [OpenAI provider](https://docs.openclaw.ai/providers/openai) docs for provider-specific realtime voice options.

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          provider: "twilio",
          inboundPolicy: "allowlist",
          allowFrom: ["+15550005678"],
          realtime: {
            enabled: true,
            provider: "google",
            instructions: "Speak briefly. Call openclaw_agent_consult before using deeper tools.",
            toolPolicy: "safe-read-only",
            consultPolicy: "substantive",
            consultThinkingLevel: "low",
            consultFastMode: true,
            agentContext: { enabled: true },
            providers: {
              google: {
                apiKey: "${GEMINI_API_KEY}",
                model: "gemini-2.5-flash-native-audio-preview-12-2025",
                speakerVoice: "Kore",
                silenceDurationMs: 500,
                startSensitivity: "high",
              },
            },
          },
        },
      },
    },
  },
}
```

## Streaming transcription

`streaming` selects a realtime transcription provider for live call audio. `streaming.provider` is optional — if unset, Voice Call uses the first registered realtime transcription provider. The bundled realtime transcription providers are **Deepgram (`deepgram`)**, **ElevenLabs (`elevenlabs`)**, **Mistral (`mistral`)**, **OpenAI (`openai`)**, and **xAI (`xai`)**, registered by their provider plugins. Provider-owned raw config lives under `streaming.providers.<providerId>`. After Twilio sends an accepted stream `start` message, Voice Call registers the stream immediately, queues inbound media through the transcription provider while the provider connects, and starts the initial greeting only after realtime transcription is ready. If `streaming.provider` points at an unregistered provider, or none is registered, Voice Call logs a warning and skips media streaming instead of failing the whole plugin.

Provider defaults from the streaming examples: **OpenAI** — API key `streaming.providers.openai.apiKey` or `OPENAI_API_KEY`; model `gpt-4o-transcribe`; `silenceDurationMs: 800`; `vadThreshold: 0.5`. **xAI** — API key `streaming.providers.xai.apiKey` or `XAI_API_KEY`; endpoint `wss://api.x.ai/v1/stt`; encoding `mulaw`; sample rate `8000`; `endpointingMs: 800`; `interimResults: true`.

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          streaming: {
            enabled: true,
            provider: "openai",
            streamPath: "/voice/stream",
            providers: {
              openai: {
                apiKey: "sk-...", // optional if OPENAI_API_KEY is set
                model: "gpt-4o-transcribe",
                silenceDurationMs: 800,
                vadThreshold: 0.5,
              },
            },
          },
        },
      },
    },
  },
}
```

## TTS for calls

Voice Call uses the core `messages.tts` configuration for streaming speech on calls. You can override it under the plugin config with the **same shape** — it deep-merges with `messages.tts`. **Microsoft speech is ignored for voice calls:** telephony audio needs PCM, and the current Microsoft transport does not expose telephony PCM output. Behavior notes from the source: legacy `tts.<provider>` keys inside plugin config (`openai`, `elevenlabs`, `microsoft`, `edge`) are repaired by `openclaw doctor --fix`, while committed config should use `tts.providers.<provider>`. Core TTS is used when Twilio media streaming is enabled; otherwise calls fall back to provider-native voices. If a Twilio media stream is already active, Voice Call does not fall back to TwiML `<Say>` — if telephony TTS is unavailable in that state, the playback request fails instead of mixing two playback paths. When telephony TTS falls back to a secondary provider, Voice Call logs a warning with the provider chain (`from`, `to`, `attempts`) for debugging. When Twilio barge-in or stream teardown clears the pending TTS queue, queued playback requests settle instead of hanging callers awaiting playback completion.

### TTS examples

The "Core TTS only" tab configures `messages.tts` with `provider: "openai"` and `providers.openai.speakerVoice: "alloy"`. The "Override to ElevenLabs (calls only)" tab sets the plugin-config `tts` to `provider: "elevenlabs"` with `providers.elevenlabs` `apiKey`, `speakerVoiceId: "pMsXgVXv3BLzUgSXRplE"`, and `modelId: "eleven_multilingual_v2"`. The "OpenAI model override (deep-merge)" tab shows that you can supply only the changed keys — the override deep-merges with the core config.

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          tts: {
            providers: {
              openai: {
                model: "gpt-4o-mini-tts",
                speakerVoice: "marin",
              },
            },
          },
        },
      },
    },
  },
}
```

## Webhook security

When a proxy or tunnel sits in front of the Gateway, the plugin reconstructs the public URL for signature verification. Three options control which forwarded headers are trusted: `webhookSecurity.allowedHosts` (`string[]`) allowlists hosts from forwarding headers; `webhookSecurity.trustForwardingHeaders` (`boolean`) trusts forwarded headers without an allowlist; and `webhookSecurity.trustedProxyIPs` (`string[]`) only trusts forwarded headers when the request remote IP matches the list.

Additional protections from the source: webhook **replay protection** is enabled for Twilio and Plivo — replayed valid webhook requests are acknowledged but skipped for side effects. Twilio conversation turns include a per-turn token in `<Gather>` callbacks, so stale/replayed speech callbacks cannot satisfy a newer pending transcript turn. Unauthenticated webhook requests are rejected before body reads when the provider's required signature headers are missing. The voice-call webhook uses the shared pre-auth body profile (**64 KB / 5 seconds**) plus a per-IP in-flight cap before signature verification.

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          publicUrl: "https://voice.example.com/voice/webhook",
          webhookSecurity: {
            allowedHosts: ["voice.example.com"],
          },
        },
      },
    },
  },
}
```

**Source**: OpenClaw documentation — `plugins/voice-call` (mirror `inbox/openclaw_docs/plugins/voice-call.md`)
**Last Updated**: 2026-06-22
**Status**: Active
