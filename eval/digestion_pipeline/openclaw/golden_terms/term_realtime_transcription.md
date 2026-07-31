---
tags:
  - resource
  - terminology
  - realtime-transcription
  - streaming-stt
  - speech-recognition
  - voice-call
  - openclaw
keywords:
  - Realtime transcription
  - streaming STT
  - speech to text
  - partial transcript
  - Deepgram realtime
  - endpointing
  - audio encoding mulaw linear16
topics:
  - Voice processing
  - Speech recognition
  - OpenClaw voice-call substrate
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://en.wikipedia.org/wiki/Speech_recognition
access_control_group: ["general"]
---

# Realtime Transcription

## Definition

**Realtime transcription** (also called **streaming speech-to-text** or **streaming STT**) is the speech-recognition pattern in which audio is sent to an ASR backend **as it is being captured** — typically a few tens of milliseconds at a time — and the backend pushes hypotheses back **before the utterance ends**. It contrasts with **batch STT**, where a complete recorded audio file is uploaded and a single final transcript is returned after the full duration is processed. The streaming mode trades a small amount of word-error-rate quality (the model sees less right-context) for **first-word latency under ~300 ms and turn-end latency under ~500 ms**, which is the threshold below which voice agents and live captioning feel conversational rather than walkie-talkie.

The industry has converged on a remarkably uniform wire-level shape: a **persistent WebSocket session** opened with authentication plus encoding/sample-rate/model parameters carried in the URL or an opening JSON frame; **binary audio frames** flowing client-to-server in ~100 ms chunks; and a **bidirectional stream of typed events** flowing server-to-client carrying two transcript states distinguished by an `is_final` (or equivalent) boolean — **partial hypotheses** that may be revised as more audio arrives, and **final transcripts** sealed after **endpointing** (silence-based or model-based detection that the speaker has stopped). Most providers also expose a **`Finalize`-style close frame** the client sends to flush any buffered audio before tearing down the socket, so the server has a chance to emit the last `final` before the connection closes.

## Context

Every major commercial ASR vendor offers this pattern with near-identical primitives: **Deepgram** at `wss://api.deepgram.com/v1/listen` (auth header, `encoding`/`sample_rate`/`model`/`endpointing`/`interim_results` query params, `Results` events with `is_final` and `speech_final`, JSON `{type: "Finalize"}` close frame); **OpenAI Realtime API** (`input_audio_buffer.append` + `input_audio_buffer.commit`, `conversation.item.input_audio_transcription.delta` and `.completed` events); **Azure AI Speech** streaming recognition over WebSocket; **Google Cloud Speech-to-Text** StreamingRecognize over gRPC; and **AssemblyAI**, **ElevenLabs**, **Amazon Transcribe**, **xAI**, and **Rev.ai** all expose WebSocket streaming endpoints with the same partial-vs-final dispatch.

Inside the **OpenClaw** agent runtime, realtime transcription is the **ASR leg of the voice-call substrate**: telephony providers (Twilio Media Streams) push mu-law/PCM audio frames into a per-call WebSocket; OpenClaw routes those frames through a `RealtimeTranscriptionProvider` plugin (Deepgram is the reference implementation in `extensions/deepgram/`), and the resulting partials drive **live captioning + barge-in detection** while finals drive a **two-step commit** (`input.audio.committed` then `transcript.done`) that seals each turn for the LLM. The provider-plugin contract abstracts the vendor-specific WebSocket shape so a future Azure or AssemblyAI adapter can drop in without touching the turn-management code.

## Key Characteristics

- **Persistent WebSocket session** — one socket per call/session, full-duplex, kept open for the entire utterance stream rather than re-handshaking per chunk; eliminates handshake overhead that REST cannot amortize at conversational latency.
- **Subscribe-by-URL-params** — model, encoding, sample rate, channels, language, endpointing duration, and interim-results flag are pushed onto the WebSocket URL's query string (Deepgram, AssemblyAI) or sent in an opening JSON frame (OpenAI Realtime). The URL **is** the session contract.
- **Audio-encoding negotiation** — vendors accept a narrow canonical set (`linear16`/`mulaw`/`alaw` on Deepgram; 24 kHz PCM on OpenAI Realtime) and adapters **alias-map** the many telephony spellings (`pcm`, `pcm_s16le`, `ulaw`, `g711_ulaw`, `g711-mulaw`) onto canonical names, with **reject-on-unknown** so a misconfigured encoding fails before the socket opens rather than silently dropping frames.
- **Partial-vs-final dispatch** — every transcript event carries an `is_final` (or `speech_final` / `transcript.done`) boolean. Partials stream incrementally and may be revised; finals are sealed text that downstream consumers can commit. Adapters route partials to a `transcript.delta` event (for live UI) and finals to a `transcript.done` event (for the agent turn pipeline).
- **Two-step final commit** — when ASR returns a final, the consumer emits an **audio-side seal** (`input.audio.committed`) followed by a **text-side seal** (`transcript.done`) under the same `turnId`, so downstream consumers can correlate the two sides of one committed turn.
- **`Finalize` close frame** — graceful shutdown sends a JSON `{type: "Finalize"}` (Deepgram) or `input_audio_buffer.commit` (OpenAI) before closing the socket so the server flushes any held audio and emits the last final.
- **Endpointing** — silence-duration threshold (Deepgram default 800 ms) or model-based speech-end detection that decides when a partial becomes a final. Tunable, and dominates **turn-end latency** more than network or model time.
- **Async connect lifecycle** — the ASR socket's own handshake takes 100s of ms; consumers must **not block** the telephony WebSocket on it. The shared pattern is `void connectTranscriptionAndNotify(session)` with a try/catch and an identity re-check after every `await`, so a fast hang-up between connect-start and connect-finish produces a clean no-op exit rather than a phantom `session.ready`.
- **Interim results trade quality for latency** — `interim_results=true` gives first-word latency under 300 ms; turning it off lets the model see more right-context and improves word error rate, at the cost of users perceiving a frozen UI until endpointing fires.

## Related Terms


## Related Code Snippets

- **[Deepgram Streaming-STT Speech Provider](../code_snippets/snippet_openclaw_speech_deepgram_stt.md)**: The OpenClaw `RealtimeTranscriptionProviderPlugin` implementation — WebSocket session factory, encoding alias normalization with reject-on-unknown, `/listen` URL builder, `Results` event dispatch (partial vs final), `{type: "Finalize"}` close frame.
- **[OpenClaw Voice-Call — Media Stream Realtime Transcription](../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md)**: The consumer side — how `MediaStreamHandler` wires `onPartial`/`onTranscript`/`onSpeechStart`/`onError` callbacks into `transcript.delta` and the two-step `input.audio.committed` + `transcript.done` final commit, with async connect lifecycle and identity re-check.

## References

- [Speech recognition (Wikipedia)](https://en.wikipedia.org/wiki/Speech_recognition) — foundational survey of ASR; covers streaming vs batch, acoustic models, and word error rate.
- [Deepgram Live Audio API Reference](https://developers.deepgram.com/reference/speech-to-text/listen-streaming) — canonical streaming-STT vendor doc; `/listen` WebSocket endpoint, encoding/sample_rate/model query params, `is_final` partial-vs-final dispatch, `Finalize` close frame.
- [Deepgram Getting Started: Live Streaming Audio](https://developers.deepgram.com/docs/live-streaming-audio) — implementation walkthrough for the streaming pattern; chunking, interim results, endpointing.
- [OpenAI Realtime Transcription Guide](https://developers.openai.com/api/docs/guides/realtime-transcription) — `input_audio_buffer.append`/`.commit`, `conversation.item.input_audio_transcription.delta`/`.completed`, `item_id` correlation.
- [Streaming Speech Recognition API for Real-Time Transcription (Deepgram)](https://deepgram.com/learn/streaming-speech-recognition-api) — comparative overview of streaming vs batch, latency budgets, WebSocket vs REST tradeoffs.
- [Transcribe Speech-to-Text in Real Time using Amazon Transcribe with WebSocket (AWS)](https://aws.amazon.com/blogs/machine-learning/transcribe-speech-to-text-in-real-time-using-amazon-transcribe-with-websocket/) — sister vendor implementation of the same WebSocket-streaming pattern.
