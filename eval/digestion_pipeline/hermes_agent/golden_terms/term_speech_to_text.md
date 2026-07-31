---
tags:
  - resource
  - terminology
  - llm
  - multimodal
keywords:
  - STT
  - Speech-to-Text
  - speech recognition
  - ASR
  - automatic speech recognition
  - voice message transcription
  - Whisper
  - faster-whisper
  - transcription provider
topics:
  - Speech recognition
  - Multimodal agents
  - Provider fallback
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
related_wiki: https://en.wikipedia.org/wiki/Speech_recognition
access_control_group: ["general"]
---

# STT - Speech-to-Text

## Definition

**Speech-to-Text (STT)**, also called **automatic speech recognition (ASR)** or simply **speech recognition**, is the technology that converts spoken-audio input into machine-readable text. It is the audio-input half of a multimodal interface (the mirror of [text-to-speech](term_text_to_speech.md), which is the audio-output half), and it lets a user speak instead of type — the recognizer transcribes the utterance, and the resulting text is injected into the conversation as if the user had typed it. Classic STT systems pair an **acoustic model** (historically Hidden Markov Models over short ~10 ms frames; now end-to-end neural encoders) with a **language model** that scores likely word sequences; modern systems such as **OpenAI Whisper** collapse both into a single transformer encoder-decoder trained by weak supervision on large multilingual audio corpora, predicting transcription, translation, and language-identification as a unified sequence-of-tokens task. The canonical quality metric is **word error rate (WER)**, $\text{WER} = (s + d + i) / n$, where $s$, $d$, $i$ are substitution, deletion, and insertion counts against a reference of $n$ words.

In the **Hermes Agent** context, "Speech-to-Text" specifically names Hermes' **voice-message transcription subsystem**: voice messages sent on Telegram, Discord, WhatsApp, Slack, or Signal are automatically transcribed and injected as text into the conversation, and the same path transcribes each push-to-talk recording in CLI [voice mode](term_voice_mode.md). The subsystem is built around a **pluggable provider registry** with an automatic **fallback chain**, a **local-faster-whisper default** (zero-config, no API key), command-type providers, and Python-plugin providers — a scope distinct from generic streaming [realtime transcription](term_realtime_transcription.md), which it links to but does not duplicate.

## Context

STT is a building block of any agent or assistant that accepts voice input. In **Hermes Agent** it appears in two surfaces:

- **Gateway voice-message intake** — the messaging gateway receives an inbound voice message on a chat platform, hands the audio file to the STT subsystem, and injects the returned transcript into the conversation so the agent sees normal text. This is the inbound counterpart of the gateway's outbound TTS voice-bubble delivery.
- **CLI / voice mode** — the local push-to-talk loop records each utterance, transcribes it via the STT provider chain, and forwards the transcript to the agent harness before streaming a spoken reply.

The subsystem is configured under the `stt:` block in `~/.hermes/config.yaml` (owned and documented in full by the Hermes media-settings configuration note) and is consumed by the messaging gateway and the agent harness. More broadly, STT is foundational across the agent ecosystem — every voice-bot, voice-call substrate, and dictation feature depends on an ASR backend, and the provider-abstraction pattern Hermes uses mirrors how its sibling [text-to-speech](term_text_to_speech.md) and [provider-routing](term_provider_routing.md) subsystems are organized.

## Key Characteristics

- **Pluggable provider registry** — built-in providers (`local`, `local_command`, `groq`, `openai`, `mistral`, `xai`) coexist with `stt.providers.<name>: type: command` command providers and Python plugins registered via `register_transcription_provider()`. This is the speech-recognition specialization of a general [provider-plugin](term_provider_plugin.md) abstraction.
- **Local-faster-whisper default (zero-config)** — local transcription works out of the box when `faster-whisper` is installed (CPU by default, GPU if available), with model sizes `tiny → base (default) → small → medium → large-v3` trading speed for quality. No API key is required for the default path.
- **Automatic fallback chain** — if the configured provider is unavailable, Hermes falls back in a documented order: local faster-whisper → local `whisper` CLI / `HERMES_LOCAL_STT_COMMAND` → cloud providers (Groq, then OpenAI); a missing Groq key falls to local then OpenAI; a missing OpenAI key falls to local then Groq; Mistral is skipped in auto-detect when its key/SDK is absent. With nothing available, voice messages pass through with a note to the user. This makes STT a concrete instance of provider [failover](term_failover.md).
- **Resolution order with built-in precedence** — `stt.provider` resolves as: built-in name (always wins) → matching `stt.providers.<name>` command provider (wins over a same-name plugin) → plugin-registered `TranscriptionProvider` → "No STT provider available" error. Built-in names are short-circuited before the command-provider resolver runs, so user config can never silently shadow a native handler.
- **Command-type providers (no Python)** — wire in any CLI ASR engine (NVIDIA Parakeet, whisper.cpp, SenseVoice, Doubao/Volcengine ASR) by declaring a shell command with `{input_path}`, `{output_path}`, `{output_dir}`, `{format}`, `{language}`, `{model}` placeholders (shell-quoted automatically). The transcript is read back from the output file, falling through to stdout if no file is written.
- **Python-plugin providers** — for SDK-only backends, OAuth-refreshing auth, or streaming chunks, a plugin subclasses `TranscriptionProvider` and returns a standard `{success, transcript, provider, error}` envelope (converting exceptions rather than raising), reading per-provider config from `stt.<provider>` and exposing optional `list_models()` / `default_model()` / `get_setup_schema()` hooks.
- **Security model** — command providers run under the same user as Hermes with full filesystem access; the command template is trusted local input, the same trust model as `HERMES_LOCAL_STT_COMMAND`. Process trees are killed on timeout (default 300 s).
- **Multilingual and cloud options** — Mistral Voxtral Transcribe supports 13 languages with speaker diarization and word-level timestamps; xAI Grok STT posts multipart form-data to `/v1/stt`; OpenAI supports `whisper-1`, `gpt-4o-mini-transcribe`, and `gpt-4o-transcribe`.

## Related Terms

- **[OpenClaw — Deepgram Plugin Reference Card](../documentation/openclaw/oc_plugins_reference_deepgram.md)** — This note is the reference-card descriptor for the OpenClaw **Deepgram plugin**, mirroring the `plugins/reference/deepgram` source page

## References

- [Speech recognition (Wikipedia)](https://en.wikipedia.org/wiki/Speech_recognition) — foundational survey of ASR/STT: acoustic vs language models, HMM and end-to-end neural approaches, and the word-error-rate metric.
- [OpenAI Whisper (GitHub)](https://github.com/openai/whisper) — open-source transformer encoder-decoder ASR model (weakly supervised, multilingual; tiny/base/small/medium/large/turbo sizes) underlying Hermes' local-whisper default and the OpenAI Whisper API provider.
- [faster-whisper (GitHub)](https://github.com/SYSTRAN/faster-whisper) — the CTranslate2 reimplementation of Whisper that powers Hermes' zero-config local STT default.
- [Mistral Voxtral Transcribe — Speech-to-Text](https://docs.mistral.ai/capabilities/audio/speech_to_text/) — the multilingual Voxtral transcription models (diarization, word-level timestamps) used by Hermes' Mistral STT provider.
- [Hermes Agent — Voice & TTS (Voice Message Transcription / STT)](https://hermes-agent.nousresearch.com/docs/user-guide/features/tts/) — the source documentation page for Hermes' STT subsystem: provider table, configuration, fallback behavior, and command/plugin provider registries.

---

**Last Updated**: 2026-06-19
**Status**: Active
