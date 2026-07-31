---
tags:
  - resource
  - terminology
  - llm
  - multimodal
keywords:
  - TTS
  - Text-to-Speech
  - speech synthesis
  - voice synthesis
  - neural TTS
  - text_to_speech
  - tts provider
topics:
  - Speech synthesis
  - Multimodal AI
  - Voice agents
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: https://en.wikipedia.org/wiki/Speech_synthesis
---

# TTS - Text-to-Speech

## Definition

**Text-to-Speech (TTS)**, also called **speech synthesis** or **voice synthesis**, is the
artificial production of human-sounding speech from written text. It is the audio-output half of a multimodal interface — the inverse of [speech-to-text](term_speech_to_text.md) (STT, which turns inbound audio into text) — and it lets an agent "speak" a reply that a user can hear instead of read. Modern TTS is dominated by **neural** approaches that train deep networks on large recorded-speech corpora; the canonical pipeline is two-stage: an **acoustic model** maps text (or phonemes) to a mel-spectrogram, and a separate **neural vocoder** converts that spectrogram into a raw waveform (e.g., Tacotron 2 → WaveNet/HiFi-GAN). Earlier paradigms — **concatenative** (splicing recorded units, most natural but glitchy), **formant** (rule-based additive synthesis, robotic but tiny), and **statistical-parametric** (HMM-based) — are still used in memory-constrained or fully offline settings.

In an agent runtime such as **Hermes Agent**, "text-to-speech" names a whole **provider subsystem** rather than a single model: a registry of interchangeable backends that the agent's `text_to_speech` tool routes to. Hermes ships **ten built-in providers** (Edge TTS as the free no-key default, plus ElevenLabs, OpenAI, MiniMax, Mistral/Voxtral, Google Gemini, xAI, NeuTTS, KittenTTS, and Piper) and two **user-extension surfaces** — a no-Python **command-type provider** registry and a Python **plugin** ABC (`register_tts_provider()`) — so any CLI- or SDK-based engine can be wired in without forking the agent. This subsystem framing (selectable provider + per-provider config + key resolution + delivery formatting) is the reusable abstraction the term documents.

## Context

- **Hermes Agent** — the `text_to_speech` tool and the CLI/gateway "voice reply" features consume the TTS subsystem. The provider is chosen via `tts.provider` in `~/.hermes/config.yaml` or the `hermes tools` Voice & TTS picker; output is delivered as a Telegram/Discord **voice bubble** (Opus/OGG) or, on WhatsApp/CLI, as an audio-file attachment. Paid OpenAI TTS is reachable through the [Tool Gateway](term_tool_gateway.md) for [Nous Portal](term_nous_portal.md) subscribers without a separate key.
- **Voice agents generally** — TTS is component (5) of the canonical voice-agent stack (alongside a [realtime-transcription](term_realtime_transcription.md) STT leg), streaming the agent's text reply back as audio frames in tools like the [voice-call](term_voice_call.md) substrate, voice assistants, and [conversational AI](term_conversational_ai.md) front ends.
- **Cloud TTS platforms** — Azure AI Speech, Google, OpenAI, and ElevenLabs expose neural voices, an XML markup language (**SSML**) for controlling pitch / pauses / pronunciation / speaking style, and **custom / cloned voices** built from a handful of recorded samples (Hermes surfaces xAI voice cloning the same way). Cloud providers bill per **character** of input, which is why TTS subsystems enforce per-provider input-length caps.

## Key Characteristics

- **Provider subsystem, not one model** — the defining trait of agent TTS: a pluggable registry where a [model catalog](term_model_catalog.md) of backends (free-local → premium-cloud) is selected at runtime, mirroring the [provider-plugin](term_provider_plugin.md) abstraction.
- **Quality / cost / key tradeoff** — backends span a matrix of quality, cost, and credential needs: free no-key local engines (Edge, NeuTTS, KittenTTS, Piper) vs. paid cloud engines (ElevenLabs/OpenAI/MiniMax/xAI) gated by an API key (see [authentication](term_authentication.md)).
- **Free no-key default + fallback** — a free default (Edge TTS) means TTS works out of the box; a premium provider that is unavailable or unkeyed falls back to the default (a [failover](term_failover.md) pattern).
- **Per-provider input-length caps** — each backend has a documented character cap (Edge 5000, OpenAI 4096, Gemini 32000, ElevenLabs model-aware, …); the subsystem truncates text before the call so a request never fails on length. If $n$ characters exceed a provider cap $C_p$, the input is clipped to $\min(n, C_p)$.
- **Performance direction & expressive control** — analogous to SSML on cloud platforms, Hermes Gemini supports **persona prompts** (natural-language voice direction via a local file) and **audio tags** (`[whispers]`, `[laughs]`) inserted by a hidden rewrite pass; the visible chat reply is unchanged.
- **Voice cloning** — custom voices built from recorded samples (xAI Custom Voices; Azure personal voice) let the synthesized voice match a specific speaker.
- **Delivery-format negotiation** — Telegram voice bubbles require Opus/OGG; MP3/WAV/PCM outputs are transcoded with **ffmpeg**, otherwise audio is sent as a plain file. Built-in provider names always win over a same-name user-declared provider, so user config can never silently shadow a built-in.
- **Two extension surfaces** — a no-code **command-type provider** (shell template with `{input_path}`/`{output_path}` placeholders, shell-quoted, timeout-killed) for any CLI engine, and a Python **plugin** (`TTSProvider` ABC + `register_tts_provider()`) for SDK-only / streaming / OAuth-refresh backends — the [plugin SDK](term_plugin_sdk.md) path.

## Related Terms

- **[OpenClaw — Elevenlabs Plugin Reference Card](../documentation/openclaw/oc_plugins_reference_elevenlabs.md)** — This note is the plugin-manifest reference card for the OpenClaw **`@openclaw/elevenlabs-speech`** plugin, mirroring the `plugins/reference/elevenlabs` source…

## References

- [Speech synthesis (Wikipedia)](https://en.wikipedia.org/wiki/Speech_synthesis) — survey of TTS: concatenative / formant / statistical-parametric / neural approaches, the two-stage acoustic-model + vocoder pipeline, WaveNet and Tacotron 2.
- [Text to speech overview — Azure AI Speech](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech) — neural voices, SSML for prosody/pronunciation control, custom/personal voice cloning, real-time vs batch synthesis, per-character billing.
- [Hermes Agent — Voice & TTS](https://hermes-agent.nousresearch.com/docs/user-guide/features/tts) — the ten-provider TTS subsystem, command-type providers, the `register_tts_provider()` plugin ABC, per-provider input-length caps, Telegram Opus/ffmpeg delivery, Gemini persona prompts and audio tags, xAI voice cloning.
- [ElevenLabs Text to Speech docs](https://elevenlabs.io/docs/capabilities/text-to-speech) — commercial neural-TTS reference: models, voices, and model-aware input limits.
- [WaveNet: A Generative Model for Raw Audio (DeepMind)](https://arxiv.org/abs/1609.03499) — the deep-learning vocoder that established raw-waveform neural TTS.
