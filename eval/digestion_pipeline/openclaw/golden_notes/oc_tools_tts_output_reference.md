---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - tts
keywords:
  - openclaw tts output formats
  - tts auto behavior decision flow
  - messages.tts field reference
  - tts agent tool audio attachment
  - gateway tts rpc methods
  - opus mp3 pcm transcoding ffmpeg
  - per-channel voice-note output
  - tts.status tts.convert tts.providers
topics:
  - OpenClaw
  - Text-to-Speech Output
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/tools/tts
access_control_group: ["general"]
---

# OpenClaw — TTS Output Contract, Field Reference, and RPC

## Overview

This note models the OpenClaw text-to-speech **output contract**: the channel-capability-driven audio formats each provider emits, the Auto-TTS decision flow that gates whether a reply is synthesized, the full `messages.tts.*` configuration field reference, the built-in `tts` agent tool, and the Gateway TTS RPC methods. It mirrors the back half of the `tools/tts` source page (`Output formats (fixed)`, `Auto-TTS behavior`, `Output formats by channel`, `Field reference`, `Agent tool`, `Gateway RPC`, and `Service links`). Provider auth/config setup and personas/directives are covered by sibling notes (`oc_tools_tts_setup`, `oc_tools_tts_personas_directives`); this note is the format/field/RPC reference half.

## Output formats (fixed)

TTS voice delivery is channel-capability driven. Channel plugins advertise whether voice-style TTS should ask providers for a native `voice-note` target or keep normal `audio-file` synthesis and only mark compatible output for voice delivery. The per-provider output behavior is:

- **Voice-note capable channels**: voice-note replies prefer Opus (`opus_48000_64` from ElevenLabs, `opus` from OpenAI); 48kHz / 64kbps is a good voice message tradeoff.
- **Feishu / WhatsApp**: when a voice-note reply is produced as MP3/WebM/WAV/M4A or another likely audio file, the channel plugin transcodes it to 48kHz Ogg/Opus with `ffmpeg` before sending the native voice message. WhatsApp sends the result through the Baileys `audio` payload with `ptt: true` and `audio/ogg; codecs=opus`. If conversion fails, Feishu receives the original file as an attachment; WhatsApp send fails rather than posting an incompatible PTT payload.
- **Other channels**: MP3 (`mp3_44100_128` from ElevenLabs, `mp3` from OpenAI); 44.1kHz / 128kbps is the default balance for speech clarity.
- **MiniMax**: MP3 (`speech-2.8-hd` model, 32kHz sample rate) for normal audio attachments. For channel-advertised voice-note targets, OpenClaw transcodes the MiniMax MP3 to 48kHz Opus with `ffmpeg` before delivery when the channel advertises transcoding.
- **Xiaomi MiMo**: MP3 by default, or WAV when configured. For channel-advertised voice-note targets, OpenClaw transcodes Xiaomi output to 48kHz Opus with `ffmpeg` before delivery when the channel advertises transcoding.
- **Local CLI**: uses the configured `outputFormat`. Voice-note targets are converted to Ogg/Opus and telephony output is converted to raw 16 kHz mono PCM with `ffmpeg`.
- **Google Gemini**: Gemini API TTS returns raw 24kHz PCM. OpenClaw wraps it as WAV for audio attachments, transcodes it to 48kHz Opus for voice-note targets, and returns PCM directly for Talk/telephony.
- **Gradium**: WAV for audio attachments, Opus for voice-note targets, and `ulaw_8000` at 8 kHz for telephony.
- **Inworld**: MP3 for normal audio attachments, native `OGG_OPUS` for voice-note targets, and raw `PCM` at 22050 Hz for Talk/telephony.
- **xAI**: MP3 by default; `responseFormat` may be `mp3`, `wav`, `pcm`, `mulaw`, or `alaw`. OpenClaw uses xAI's batch REST TTS endpoint and returns a complete audio attachment; xAI's streaming TTS WebSocket is not used by this provider path. Native Opus voice-note format is not supported by this path.
- **Microsoft**: uses `microsoft.outputFormat` (default `audio-24khz-48kbitrate-mono-mp3`). The bundled transport accepts an `outputFormat`, but not all formats are available from the service; output format values follow Microsoft Speech output formats (including Ogg/WebM Opus). Telegram `sendVoice` accepts OGG/MP3/M4A — use OpenAI/ElevenLabs if you need guaranteed Opus voice messages. If the configured Microsoft output format fails, OpenClaw retries with MP3.

OpenAI/ElevenLabs output formats are fixed per channel (see above).

## Auto-TTS behavior

When `messages.tts.auto` is enabled, OpenClaw: skips TTS if the reply already contains structured media; skips very short replies (under 10 chars); summarizes long replies when summaries are enabled, using `summaryModel` (or `agents.defaults.model.primary`); attaches the generated audio to the reply; and in `mode: "final"`, still sends audio-only TTS for streamed final replies after the text stream completes (the generated media goes through the same channel media normalization as normal reply attachments). If the reply exceeds `maxLength` and summary is off (or no API key for the summary model), audio is skipped and the normal text reply is sent. The decision flow is:

```text
Reply -> TTS enabled?
  no  -> send text
  yes -> has media / short?
          yes -> send text
          no  -> length > limit?
                   no  -> TTS -> attach audio
                   yes -> summary enabled?
                            no  -> send text
                            yes -> summarize -> TTS -> attach audio
```

## Output formats by channel

The per-target format summary table:

| Target                                | Format                                                                                                                                |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Feishu / Matrix / Telegram / WhatsApp | Voice-note replies prefer **Opus** (`opus_48000_64` from ElevenLabs, `opus` from OpenAI). 48 kHz / 64 kbps balances clarity and size. |
| Other channels                        | **MP3** (`mp3_44100_128` from ElevenLabs, `mp3` from OpenAI). 44.1 kHz / 128 kbps default for speech.                                 |
| Talk / telephony                      | Provider-native **PCM** (Inworld 22050 Hz, Google 24 kHz), or `ulaw_8000` from Gradium for telephony.                                 |

Per-provider notes:

- **Feishu / WhatsApp transcoding**: when a voice-note reply lands as MP3/WebM/WAV/M4A, the channel plugin transcodes to 48 kHz Ogg/Opus with `ffmpeg`. WhatsApp sends through Baileys with `ptt: true` and `audio/ogg; codecs=opus`. If conversion fails: Feishu falls back to attaching the original file; WhatsApp send fails rather than posting an incompatible PTT payload.
- **MiniMax / Xiaomi MiMo**: default MP3 (32 kHz for MiniMax `speech-2.8-hd`); transcoded to 48 kHz Opus for voice-note targets via `ffmpeg`.
- **Local CLI**: uses configured `outputFormat`. Voice-note targets are converted to Ogg/Opus and telephony output to raw 16 kHz mono PCM.
- **Google Gemini**: returns raw 24 kHz PCM. OpenClaw wraps as WAV for attachments, transcodes to 48 kHz Opus for voice-note targets, returns PCM directly for Talk/telephony.
- **Inworld**: MP3 attachments, native `OGG_OPUS` voice-note, raw `PCM` 22050 Hz for Talk/telephony.
- **xAI**: MP3 by default; `responseFormat` may be `mp3|wav|pcm|mulaw|alaw`. Uses xAI's batch REST endpoint — streaming WebSocket TTS is **not** used. Native Opus voice-note format is **not** supported.
- **Microsoft**: uses `microsoft.outputFormat` (default `audio-24khz-48kbitrate-mono-mp3`). Telegram `sendVoice` accepts OGG/MP3/M4A; use OpenAI/ElevenLabs if you need guaranteed Opus voice messages. If the configured Microsoft format fails, OpenClaw retries with MP3.

OpenAI and ElevenLabs output formats are fixed per channel as listed above.

## Field reference

### Top-level `messages.tts.*`

- `auto` (`"off" | "always" | "inbound" | "tagged"`) — Auto-TTS mode. `inbound` only sends audio after an inbound voice message; `tagged` only sends audio when the reply includes `[[tts:...]]` directives or a `[[tts:text]]` block.
- `enabled` (`boolean`, deprecated) — legacy toggle; `openclaw doctor --fix` migrates this to `auto`.
- `mode` (`"final" | "all"`, default `final`) — `"all"` includes tool/block replies in addition to final replies.
- `provider` (`string`) — speech provider id. When unset, OpenClaw uses the first configured provider in registry auto-select order. Legacy `provider: "edge"` is rewritten to `"microsoft"` by `openclaw doctor --fix`.
- `persona` (`string`) — active persona id from `personas`; normalized to lowercase.
- `personas.<id>` (`object`) — stable spoken identity. Fields: `label`, `description`, `provider`, `fallbackPolicy`, `prompt`, `providers.<provider>`.
- `summaryModel` (`string`) — cheap model for auto-summary; defaults to `agents.defaults.model.primary`. Accepts `provider/model` or a configured model alias.
- `modelOverrides` (`object`) — allow the model to emit TTS directives. `enabled` defaults to `true`; `allowProvider` defaults to `false`.
- `providers.<id>` (`object`) — provider-owned settings keyed by speech provider id. Legacy direct blocks (`messages.tts.openai`, `.elevenlabs`, `.microsoft`, `.edge`) are rewritten by `openclaw doctor --fix`; commit only `messages.tts.providers.<id>`.
- `maxTextLength` (`number`) — hard cap for TTS input characters. `/tts audio` fails if exceeded.
- `timeoutMs` (`number`) — request timeout in milliseconds.
- `prefsPath` (`string`) — override the local prefs JSON path (provider/limit/summary). Default `~/.openclaw/settings/tts.json`.

### Per-provider blocks (`messages.tts.providers.<id>.*`)

- **Azure Speech** — `apiKey` (env `AZURE_SPEECH_KEY`, `AZURE_SPEECH_API_KEY`, or `SPEECH_KEY`); `region` (e.g. `eastus`, env `AZURE_SPEECH_REGION`/`SPEECH_REGION`); `endpoint` (alias `baseUrl`); `speakerVoice` (default `en-US-JennyNeural`, legacy alias `voice`); `lang` (default `en-US`); `outputFormat` (default `audio-24khz-48kbitrate-mono-mp3`); `voiceNoteOutputFormat` (default `ogg-24khz-16bit-mono-opus`).
- **ElevenLabs** — `apiKey` (falls back to `ELEVENLABS_API_KEY`/`XI_API_KEY`); `model` (e.g. `eleven_multilingual_v2`, `eleven_v3`); `speakerVoiceId` (legacy alias `voiceId`); `voiceSettings` (`stability`/`similarityBoost`/`style` each `0..1`, `useSpeakerBoost` `true|false`, `speed` `0.5..2.0` where `1.0` = normal); `applyTextNormalization` (`auto|on|off`); `languageCode` (2-letter ISO 639-1); `seed` (integer `0..4294967295`, best-effort determinism); `baseUrl`.
- **Google Gemini** — `apiKey` (falls back to `GEMINI_API_KEY`/`GOOGLE_API_KEY`, then reuses `models.providers.google.apiKey` before env fallback); `model` (default `gemini-3.1-flash-tts-preview`); `speakerVoice` (default `Kore`, legacy aliases `voiceName`/`voice`); `audioProfile` (natural-language style prompt); `speakerName`; `promptTemplate` (`audio-profile-v1` wraps active persona prompt fields in a deterministic Gemini TTS prompt structure); `personaPrompt` (Google-specific extra persona text appended to the template's Director's Notes); `baseUrl` (only `https://generativelanguage.googleapis.com` accepted).
- **Gradium** — `apiKey` (env `GRADIUM_API_KEY`); `baseUrl` (default `https://api.gradium.ai`); `speakerVoiceId` (default Emma `YTpq7expH9539ERJ`, legacy alias `voiceId`).
- **Inworld** — `apiKey` (env `INWORLD_API_KEY`); `baseUrl` (default `https://api.inworld.ai`); `modelId` (default `inworld-tts-1.5-max`; also `inworld-tts-1.5-mini`, `inworld-tts-1-max`, `inworld-tts-1`); `speakerVoiceId` (default `Sarah`, legacy alias `voiceId`); `temperature` (`0..2`).
- **Local CLI (`tts-local-cli`)** — `command`; `args` (supports `{{Text}}`, `{{OutputPath}}`, `{{OutputDir}}`, `{{OutputBase}}` placeholders); `outputFormat` (`mp3|opus|wav`, default `mp3`); `timeoutMs` (default `120000`); `cwd`; `env` (`Record<string,string>`).
- **Microsoft (no API key)** — `enabled` (`boolean`, default `true`); `speakerVoice` (e.g. `en-US-MichelleNeural`, legacy alias `voice`); `lang` (e.g. `en-US`); `outputFormat` (default `audio-24khz-48kbitrate-mono-mp3`; not all formats supported by the bundled Edge-backed transport); `rate / pitch / volume` (percent strings, e.g. `+10%`); `saveSubtitles` (`boolean`); `proxy`; `timeoutMs`; `edge.*` (deprecated legacy alias — run `openclaw doctor --fix`).
- **MiniMax** — `apiKey` (falls back to `MINIMAX_API_KEY`; Token Plan via `MINIMAX_OAUTH_TOKEN`/`MINIMAX_CODE_PLAN_KEY`/`MINIMAX_CODING_API_KEY`); `baseUrl` (default `https://api.minimax.io`, env `MINIMAX_API_HOST`); `model` (default `speech-2.8-hd`, env `MINIMAX_TTS_MODEL`); `speakerVoiceId` (default `English_expressive_narrator`, env `MINIMAX_TTS_VOICE_ID`, legacy alias `voiceId`); `speed` (`0.5..2.0`, default `1.0`); `vol` (`(0, 10]`, default `1.0`); `pitch` (integer `-12..12`, default `0`, fractional truncated).
- **OpenAI** — `apiKey` (falls back to `OPENAI_API_KEY`); `model` (e.g. `gpt-4o-mini-tts`); `speakerVoice` (e.g. `alloy`, `cedar`, legacy alias `voice`); `instructions` (when set, persona prompt fields are **not** auto-mapped); `extraBody / extra_body` (extra JSON merged into `/audio/speech` bodies after generated fields, for OpenAI-compatible endpoints like Kokoro needing keys such as `lang`; unsafe prototype keys ignored); `baseUrl` (resolution order config → `OPENAI_TTS_BASE_URL` → `https://api.openai.com/v1`; non-default values treated as OpenAI-compatible TTS endpoints, so custom model/voice names are accepted).
- **OpenRouter** — `apiKey` (env `OPENROUTER_API_KEY`, can reuse `models.providers.openrouter.apiKey`); `baseUrl` (default `https://openrouter.ai/api/v1`, legacy `https://openrouter.ai/v1` normalized); `model` (default `hexgrad/kokoro-82m`, alias `modelId`); `speakerVoice` (default `af_alloy`, legacy aliases `voice`/`voiceId`); `responseFormat` (`mp3|pcm`, default `mp3`); `speed`.
- **Volcengine (BytePlus Seed Speech)** — `apiKey` (env `VOLCENGINE_TTS_API_KEY` or `BYTEPLUS_SEED_SPEECH_API_KEY`); `resourceId` (default `seed-tts-1.0`, env `VOLCENGINE_TTS_RESOURCE_ID`; use `seed-tts-2.0` with TTS 2.0 entitlement); `appKey` (default `aGjiRDfUWi`, env `VOLCENGINE_TTS_APP_KEY`); `baseUrl` (env `VOLCENGINE_TTS_BASE_URL`); `speakerVoice` (default `en_female_anna_mars_bigtts`, env `VOLCENGINE_TTS_VOICE`, legacy alias `voice`); `speedRatio`; `emotion`; `appId / token / cluster` (deprecated legacy Speech Console fields; env `VOLCENGINE_TTS_APPID`/`_TOKEN`/`_CLUSTER`, default cluster `volcano_tts`).
- **xAI** — `apiKey` (env `XAI_API_KEY`); `baseUrl` (default `https://api.x.ai/v1`, env `XAI_BASE_URL`); `speakerVoiceId` (default `eve`; live voices `ara`/`eve`/`leo`/`rex`/`sal`/`una`; legacy alias `voiceId`); `language` (BCP-47 or `auto`, default `en`); `responseFormat` (`mp3|wav|pcm|mulaw|alaw`, default `mp3`); `speed`.
- **Xiaomi MiMo** — `apiKey` (env `XIAOMI_API_KEY`); `baseUrl` (default `https://api.xiaomimimo.com/v1`, env `XIAOMI_BASE_URL`); `model` (default `mimo-v2.5-tts`, env `XIAOMI_TTS_MODEL`; also `mimo-v2-tts`, `mimo-v2.5-tts-voicedesign`); `speakerVoice` (default `mimo_default` for preset-voice models, env `XIAOMI_TTS_VOICE`, legacy alias `voice`; not sent for `mimo-v2.5-tts-voicedesign`); `format` (`mp3|wav`, default `mp3`, env `XIAOMI_TTS_FORMAT`); `style` (optional natural-language style instruction sent as user message, not spoken; for `mimo-v2.5-tts-voicedesign` it is the voice-design prompt, with an OpenClaw default when omitted).

## Agent tool

The `tts` tool converts text to speech and returns an audio attachment for reply delivery. On Feishu, Matrix, Telegram, and WhatsApp, the audio is delivered as a voice message rather than a file attachment, and Feishu and WhatsApp can transcode non-Opus TTS output on this path when `ffmpeg` is available. WhatsApp sends audio through Baileys as a PTT voice note (`audio` with `ptt: true`) and sends visible text **separately** from PTT audio because clients do not consistently render captions on voice notes. The tool accepts optional `channel` and `timeoutMs` fields; `timeoutMs` is a per-call provider request timeout in milliseconds. Per-call values override `messages.tts.timeoutMs`; configured TTS timeouts override any plugin-authored provider default.

## Gateway RPC

| Method            | Purpose                                  |
| ----------------- | ---------------------------------------- |
| `tts.status`      | Read current TTS state and last attempt. |
| `tts.enable`      | Set local auto preference to `always`.   |
| `tts.disable`     | Set local auto preference to `off`.      |
| `tts.convert`     | One-off text → audio.                    |
| `tts.setProvider` | Set local provider preference.           |
| `tts.setPersona`  | Set local persona preference.            |
| `tts.providers`   | List configured providers and status.    |

**Source**: OpenClaw documentation — `tools/tts` (mirror `inbox/openclaw_docs/tools/tts.md`)
**Last Updated**: 2026-06-22
**Status**: Active
