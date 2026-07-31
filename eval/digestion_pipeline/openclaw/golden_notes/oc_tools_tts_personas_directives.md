---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - tts
keywords:
  - openclaw tts persona
  - tts persona resolution
  - fallbackpolicy preserve-persona
  - model-driven tts directives
  - tts text directive block
  - modeloverrides allowprovider
  - tts slash commands
  - persona provider bindings
  - explicit-first provider selection
topics:
  - OpenClaw
  - Text-to-speech
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/tts
access_control_group: ["general"]
---

# OpenClaw — TTS Personas, Model-Driven Directives, and `/tts` Slash Commands

## Overview

This note covers the OpenClaw text-to-speech (TTS) control surfaces that shape *how* a spoken reply sounds and *who* speaks it: **personas** (stable, provider-neutral spoken identities with deterministic resolution and a fallback policy), **model-driven `[[tts:...]]` directives** (per-reply voice/model/speed overrides the assistant can emit), and the **`/tts` slash-command** family. It mirrors the `Personas`, `Model-driven directives`, and `Slash commands` sections of the `tools/tts` source page. Provider setup and the 14-provider matrix are covered by the split sibling [oc_tools_tts_setup](oc_tools_tts_setup.md); the output-format contract and `messages.tts.*` field reference are in [oc_tools_tts_output_reference](oc_tools_tts_output_reference.md).

## Personas

A **persona** is a stable spoken identity that can be applied deterministically across providers. It can prefer one provider, define provider-neutral prompt intent, and carry provider-specific bindings for voices, models, prompt templates, seeds, and voice settings. The active persona is set globally via `messages.tts.persona` (the id is normalized to lowercase), per-agent via `agents.list[].tts.persona` (which overrides the global value for that agent only), or per-host via the `/tts persona <id>` local preference.

### Minimal persona

A minimal persona pins a label and a single provider binding (voice id + model id) under `personas.<id>`:

```json5
{
  messages: {
    tts: {
      auto: "always",
      persona: "narrator",
      personas: {
        narrator: {
          label: "Narrator",
          provider: "elevenlabs",
          providers: {
            elevenlabs: {
              speakerVoiceId: "EXAVITQu4vr4xnSDxMaL",
              modelId: "eleven_multilingual_v2",
            },
          },
        },
      },
    },
  },
}
```

### Full persona (provider-neutral prompt)

A full persona adds a `description`, a `fallbackPolicy`, a provider-neutral `prompt` (with `profile`, `scene`, `sampleContext`, `style`, `accent`, `pacing`, and `constraints`), and per-provider bindings. The same persona can therefore drive Google Gemini, OpenAI, and ElevenLabs with provider-specific voice/model/seed/`voiceSettings` while sharing one prompt intent:

```json5
{
  messages: {
    tts: {
      auto: "always",
      persona: "alfred",
      personas: {
        alfred: {
          label: "Alfred",
          description: "Dry, warm British butler narrator.",
          provider: "google",
          fallbackPolicy: "preserve-persona",
          prompt: {
            profile: "A brilliant British butler. Dry, witty, warm, charming, emotionally expressive, never generic.",
            scene: "A quiet late-night study. Close-mic narration for a trusted operator.",
            sampleContext: "The speaker is answering a private technical request with concise confidence and dry warmth.",
            style: "Refined, understated, lightly amused.",
            accent: "British English.",
            pacing: "Measured, with short dramatic pauses.",
            constraints: ["Do not read configuration values aloud.", "Do not explain the persona."],
          },
          providers: {
            google: {
              model: "gemini-3.1-flash-tts-preview",
              speakerVoice: "Algieba",
              promptTemplate: "audio-profile-v1",
            },
            openai: { model: "gpt-4o-mini-tts", speakerVoice: "cedar" },
            elevenlabs: {
              speakerVoiceId: "voice_id",
              modelId: "eleven_multilingual_v2",
              seed: 42,
              voiceSettings: {
                stability: 0.65,
                similarityBoost: 0.8,
                style: 0.25,
                useSpeakerBoost: true,
                speed: 0.95,
              },
            },
          },
        },
      },
    },
  },
}
```

### Persona resolution

The active persona is selected deterministically, in order: (1) the `/tts persona <id>` local preference, if set; (2) `messages.tts.persona`, if set; (3) no persona. Provider selection runs **explicit-first**, in order: (1) direct overrides (CLI, gateway, Talk, allowed TTS directives); (2) the `/tts provider <id>` local preference; (3) the active persona's `provider`; (4) `messages.tts.provider`; (5) registry auto-select. For each provider attempt, OpenClaw merges configs in this order: (1) `messages.tts.providers.<id>`; (2) `messages.tts.personas.<persona>.providers.<id>`; (3) trusted request overrides; (4) allowed model-emitted TTS directive overrides.

### How providers use persona prompts

Persona prompt fields (`profile`, `scene`, `sampleContext`, `style`, `accent`, `pacing`, `constraints`) are **provider-neutral**, and each provider decides how to consume them. **Google Gemini** wraps the persona prompt fields in a Gemini TTS prompt structure **only when** the effective Google provider config sets `promptTemplate: "audio-profile-v1"` or `personaPrompt`; the older `audioProfile` and `speakerName` fields are still prepended as Google-specific prompt text, and inline audio tags such as `[whispers]` or `[laughs]` inside a `[[tts:text]]` block are preserved inside the Gemini transcript (OpenClaw does not generate these tags). **OpenAI** maps persona prompt fields to the request `instructions` field **only when** no explicit OpenAI `instructions` is configured — explicit `instructions` always wins. **Other providers** use only the provider-specific persona bindings under `personas.<id>.providers.<provider>`, ignoring the persona prompt fields unless the provider implements its own persona-prompt mapping.

### Fallback policy

`fallbackPolicy` controls behavior when a persona has **no binding** for the attempted provider:

| Policy              | Behavior                                                                                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `preserve-persona`  | **Default.** Provider-neutral prompt fields stay available; the provider may use them or ignore them.                                            |
| `provider-defaults` | Persona is omitted from prompt preparation for that attempt; the provider uses its neutral defaults while fallback to other providers continues. |
| `fail`              | Skip that provider attempt with `reasonCode: "not_configured"` and `personaBinding: "missing"`. Fallback providers are still tried.              |

The whole TTS request only fails when **every** attempted provider is skipped or fails. Talk session provider selection is session-scoped: a Talk client should choose provider ids, model ids, voice ids, and locales from `talk.catalog` and pass them through the Talk session or handoff request, and opening a voice session should not mutate `messages.tts` or global Talk provider defaults.

## Model-driven directives

By default the assistant **can** emit `[[tts:...]]` directives to override voice, model, or speed for a single reply, plus an optional `[[tts:text]]...[[/tts:text]]` block for expressive cues that should appear in audio only. A reply might therefore look like:

```text
Here you go.

[[tts:speakerVoiceId=pMsXgVXv3BLzUgSXRplE model=eleven_v3 speed=1.1]]
[[tts:text]](laughs) Read the song once more.[[/tts:text]]
```

When `messages.tts.auto` is `"tagged"`, **directives are required** to trigger audio. Streaming block delivery strips directives from visible text before the channel sees them, even when split across adjacent blocks. `provider=...` is ignored unless `modelOverrides.allowProvider: true`; when a reply declares `provider=...`, the other keys in that directive are parsed only by that provider, and unsupported keys are stripped and reported as TTS directive warnings.

**Available directive keys:**

- `provider` (registered provider id; requires `allowProvider: true`)
- `speakerVoice` / `speakerVoiceId` (legacy aliases: `voice`, `voiceName`, `voice_name`, `google_voice`, `voiceId`)
- `model` / `google_model`
- `stability`, `similarityBoost`, `style`, `speed`, `useSpeakerBoost`
- `vol` / `volume` (MiniMax volume, 0–10)
- `pitch` (MiniMax integer pitch, −12 to 12; fractional values are truncated)
- `emotion` (Volcengine emotion tag)
- `applyTextNormalization` (`auto|on|off`)
- `languageCode` (ISO 639-1)
- `seed`

Model overrides are toggled under `messages.tts.modelOverrides`. To disable them entirely, set `enabled: false`; to allow provider switching while keeping other knobs configurable, set `enabled: true, allowProvider: true` (and, for example, `allowSeed: false`):

```json5
{ messages: { tts: { modelOverrides: { enabled: true, allowProvider: true, allowSeed: false } } } }
```

## Slash commands

There is a single command, `/tts`. On Discord, OpenClaw also registers `/voice` because `/tts` is a built-in Discord command — text `/tts ...` still works. The command surface is:

```text
/tts off | on | status
/tts chat on | off | default
/tts latest
/tts provider <id>
/tts persona <id> | off
/tts limit <chars>
/tts summary off
/tts audio <text>
```

Commands require an authorized sender (allowlist/owner rules apply) and either `commands.text` or native command registration must be enabled.

**Behavior notes:**

- `/tts on` writes the local TTS preference to `always`; `/tts off` writes it to `off`.
- `/tts chat on|off|default` writes a session-scoped auto-TTS override for the current chat.
- `/tts persona <id>` writes the local persona preference; `/tts persona off` clears it.
- `/tts latest` reads the latest assistant reply from the current session transcript and sends it as audio once. It stores only a hash of that reply on the session entry to suppress duplicate voice sends.
- `/tts audio` generates a one-off audio reply (does **not** toggle TTS on).
- `limit` and `summary` are stored in **local prefs**, not the main config.
- `/tts status` includes fallback diagnostics for the latest attempt — `Fallback: <primary> -> <used>`, `Attempts: ...`, and per-attempt detail (`provider:outcome(reasonCode) latency`).
- `/status` shows the active TTS mode plus configured provider, model, voice, and sanitized custom endpoint metadata when TTS is enabled.

**Source**: OpenClaw documentation — `tools/tts` (mirror `inbox/openclaw_docs/tools/tts.md`), sections Personas / Model-driven directives / Slash commands
**Last Updated**: 2026-06-22
**Status**: Active
