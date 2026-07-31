---
tags:
  - resource
  - terminology
  - llm
  - multimodal
keywords:
  - Voice Mode
  - real-time voice
  - push-to-talk
  - voice conversation
  - voice channel
  - chained speech pipeline
topics:
  - multimodal agents
  - speech interfaces
  - voice agents
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Voice Mode

## Definition

**Voice mode** is the real-time, spoken-conversation modality of an AI agent: the user speaks (microphone or messaging-app voice message), the agent transcribes the audio to text, runs its normal reasoning/tool loop on that text, and speaks the reply back as synthesized audio. It turns a text-first agent into a hands-free, conversational one without changing the underlying model or tool layer — voice is an I/O surface wrapped around the existing text pipeline.

In the Hermes Agent it spans three delivery surfaces sharing one underlying pipeline: (1) **CLI / TUI push-to-talk** — press a key (`Ctrl+B`), the agent auto-detects when you stop speaking, transcribes via Whisper, and streams the spoken reply sentence-by-sentence; (2) **gateway auto voice-reply** on Telegram and Discord — the bot answers in a native voice bubble (Opus/OGG) alongside or instead of text; and (3) **Discord voice channels** — the bot joins a VC, listens to each speaker's audio stream, transcribes, runs the full agent pipeline, and speaks the reply back into the channel. Voice mode is deliberately distinct from wake-word voice *activation* (see [Voice Wake](term_voice_wake.md)) and from telephony voice *calls* (see [Voice Call](term_voice_call.md)): it is conversation-mode, not trigger-detection or PSTN signaling.

## Context

Voice mode sits at the intersection of an [autonomous coding agent](term_autonomous_coding_agents.md)'s [harness](term_agent_harness.md) and the [multimodal](term_multimodal.md) I/O layer. The transcript is injected as a normal turn into the model's [context window](term_context_window.md), so the agent's session, tools, and memory behave identically whether the turn arrived as typed text or spoken audio.

It is delivered through several systems:

- **CLI / TUI** — push-to-talk recording, slash commands (`/voice on|off|tts|status`), a live audio-level bar, and streaming TTS playback.
- **Messaging gateways** — Telegram/Discord auto voice-reply, with platform delivery as native voice bubbles; the gateway also auto-transcribes inbound voice messages (see [Speech-to-Text](term_speech_to_text.md)).
- **Discord voice channels** — per-user SSRC→user mapping over the voice [WebSocket](term_websocket.md), echo prevention (the listener pauses while TTS plays), and access control via an allowed-users list ([authentication](term_authentication.md)).

Architecturally, agent voice mode follows one of two designs: a **chained pipeline** (separate STT → LLM → TTS components, which Hermes uses) versus an **end-to-end speech-to-speech** model (e.g. realtime audio models). The chained design is provider-pluggable — both the [STT](term_speech_to_text.md) and [TTS](term_text_to_speech.md) stages are pluggable provider subsystems with automatic [fallback](term_failover.md) — at the cost of higher per-turn latency from the staged round-trips.

## Key Characteristics

- **Chained STT→LLM→TTS pipeline**: record → transcribe ([Speech-to-Text](term_speech_to_text.md)) → agent reasoning → synthesize ([Text-to-Speech](term_text_to_speech.md)) → play. Each stage is a swappable [provider plugin](term_provider_plugin.md) rather than a single fused model.
- **Two-stage silence detection (VAD)**: speech is confirmed when audio exceeds the RMS threshold ($\text{RMS} > 200$ on a 0–32767 scale) for at least $0.3\,\text{s}$; end-of-turn fires after $3.0\,\text{s}$ of continuous silence. A hard cap stops recording if no speech is detected for $15\,\text{s}$. In a Discord voice channel the per-speaker thresholds are tighter ($0.5\,\text{s}$ confirm, $1.5\,\text{s}$ silence) to keep multi-user turns responsive.
- **Streaming TTS**: the reply is spoken sentence-by-sentence as the model generates text — deltas are buffered into complete sentences (min ~20 chars), markdown and `<think>` blocks are stripped, and audio plays per sentence so the user does not wait for the full response.
- **Hallucination filtering**: Whisper can emit phantom text from silence/noise ("thank you for watching", "subscribe"); a filter of ~26 known phrases plus a repetition regex removes these before they reach the agent.
- **Push-to-talk + continuous loop**: a configurable record key (default `Ctrl+B`) starts recording; after each reply the loop auto-restarts so the conversation continues without re-pressing the key.
- **Provider fallback + zero-key default**: local faster-whisper STT and Edge TTS need no API key, so voice works offline-ish; cloud providers (Groq/OpenAI/ElevenLabs/etc.) are opt-in via env-var keys with an automatic fallback chain.
- **Persisted per-platform setting**: the gateway voice-reply mode (`off` / `voice_only` / `all`) survives restarts; per-user [session](term_session_persistence.md) state is keyed independently in voice channels.

## Related Terms


## References

- [Hermes Agent — Voice Mode (user guide)](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode)
- [OpenAI Realtime API — speech-to-speech models](https://platform.openai.com/docs/guides/realtime)
- [OpenAI Whisper (robust speech recognition)](https://github.com/openai/whisper)
- [Wikipedia — Voice user interface](https://en.wikipedia.org/wiki/Voice_user_interface)
- [Wikipedia — Speech recognition](https://en.wikipedia.org/wiki/Speech_recognition)
