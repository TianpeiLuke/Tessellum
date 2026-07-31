---
tags:
  - resource
  - terminology
  - voice-call
  - telephony
  - call-manager
  - voice-agent-substrate
  - openclaw
keywords:
  - Voice Call
  - CallManager
  - VoiceCallProvider
  - Telnyx Twilio Plivo
  - JSONL persistence
  - call lifecycle state store context
topics:
  - Voice agents
  - Telephony substrate
  - OpenClaw voice-call architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: null
access_control_group: ["general"]
---

# Voice Call (Substrate)

## Definition

**Voice Call (Substrate)** is the layer of an agent runtime that converts a phone call — a duplex, real-time, telephony-grade audio session — into a programmable surface an LLM agent can act on (place, answer, speak, listen, hang up). The substrate hides three telephony concerns from the agent: which carrier carries the bits (Twilio, Telnyx, Plivo, or a SIP trunk), how the carrier signals state (webhook verbs, TwiML, Call Control JSON, Plivo XML), and how live audio frames travel between the carrier and the agent (typically 8 kHz μ-law over a WebSocket "media stream"). All four 2026 industry voice-agent frameworks (Vapi, LiveKit Agents, Pipecat, Bland.ai/Retell) build some version of this substrate; OpenClaw's `extensions/voice-call/` is the local-first variant in the agent-runtime model.

In OpenClaw specifically, Voice Call refers to the unified `CallManager` facade (`extensions/voice-call/src/manager.ts`) plus the `VoiceCallProvider` interface (`providers/base.ts`) that Telnyx, Twilio, and Plivo each implement. One agent runtime, one `CallManager`, three swappable providers — chosen by config, not by code branches in the agent. Per-call state (active calls, provider-call-ID reverse map, dedup sets, transcript waiters, max-duration timers) lives on `CallManager`'s private fields and is projected to free-function helpers via a `CallManagerContext`; durable state lives on disk as an append-only `calls.jsonl` log that the manager replays on restart.

## Context

The 2026 voice-agent landscape splits into two architectures. **Managed platforms** (Vapi, Bland.ai, Retell) provision phone numbers, run STT/LLM/TTS in their cloud, and expose a turnkey HTTP/WebSocket API; the substrate is invisible. **Open frameworks** (LiveKit Agents, Pipecat, OpenClaw) make the substrate explicit: the developer's process owns the WebSocket that carries audio frames, the LLM call, the turn-taking logic, and the carrier integration. LiveKit centers a WebRTC room with SIP bridging; Pipecat exposes a frame-processor pipeline (VAD → STT → LLM → TTS); OpenClaw routes calls through `CallManager` and a `VoiceCallWebhookServer` that handles `/webhook/{provider}` HTTP endpoints plus `/media-stream` and `/transcription-stream` WebSockets.

All three open frameworks converge on the same primitive set, regardless of vocabulary: a provider interface that abstracts the carrier; a state machine per call (initiated → ringing → answered → active → speaking ↔ listening → terminal); a media-stream WebSocket that admits bidirectional μ-law audio; a realtime-transcription provider that ingests the inbound audio and emits text deltas; and webhook signature verification + replay-cache idempotency on the inbound HTTP side. OpenClaw's distinctive choice is **local-first**: webhooks are received by a Node HTTP server inside the agent process (port 3334 by default), exposed via ngrok or Tailscale for development, with per-user JSONL persistence under `~/.openclaw/voice-calls/{userId}/calls.jsonl`. No SaaS dependency, no central queue — the agent process is the call manager.

## Key Characteristics

- **`VoiceCallProvider` interface** — single TypeScript interface keyed on a `name` discriminator (`telnyx | twilio | plivo`), with required methods for verify/parse webhook, `initiateCall`, `hangupCall`, `playTts`, `startListening`, `stopListening`, `getCallStatus`, and optional capability hooks (`answerCall`, `sendDtmf`, `consumeInitialTwiML`).
- **`CallManager` facade with context projection** — owns thirteen private state fields (active calls Map, provider-call-ID Map, processed-event-IDs Set, rejected-provider-IDs Set, transcript-waiters Map, max-duration-timers Map, in-flight initial-message Set, etc.); helpers under `manager/{outbound,events,lifecycle,state,store,timers,lookup}.ts` receive a flat `CallManagerContext` projection and never touch `this`.
- **Forward-only FSM with conversation cycle** — `transitionState` enforces ordered progression through `StateOrder` (`initiated → ringing → answered → active → speaking ↔ listening`), allows free cycling between `speaking` and `listening` for multi-turn dialogs, and treats `completed | failed | timeout` as a one-way terminal trapdoor.
- **JSONL append-only persistence** — every state change is fire-and-forget-appended to `calls.jsonl` via `persistCallRecord`; `loadActiveCallsFromStore` replays on restart, drops terminal rows, and verifies remaining calls against `provider.getCallStatus` before re-arming `maxDurationTimers`.
- **Webhook signature verification across three providers** — Telnyx Ed25519, Twilio HMAC-SHA1 (Authy), Plivo HMAC-SHA256, each implemented behind `provider.verifyWebhook(ctx)` so the manager only sees verified events.
- **Replay-cache idempotency** — a TTL-bounded set of processed event IDs deduplicates carrier retries; rejected provider-call-IDs are tracked separately to avoid double-hangup on rejected inbound calls.
- **Bidirectional media-stream WebSocket** — `/media-stream` accepts the carrier's μ-law 8 kHz audio (Twilio Media Streams envelope, Telnyx/Plivo equivalents); the same socket carries TTS audio frames back to the carrier.
- **Realtime transcription provider integration** — inbound audio is forked to a streaming-STT provider (OpenAI Realtime, Deepgram, AssemblyAI); transcripts arrive as text deltas the agent loop can react to mid-utterance.
- **Admission control** — the media-stream WebSocket admits only calls whose provider-call-ID is in `providerCallIdMap` (verified webhook side), rejecting stream connects for unknown or already-terminal calls.

## Related Terms


## Related Code Snippets

- [Voice-Call — Manager + Providers](../code_snippets/snippet_openclaw_voice_call_manager.md): the unified `CallManager` facade and `VoiceCallProvider` interface across Telnyx/Twilio/Plivo with seven extraction patterns.
- [Voice-Call — Runtime + Tunnel](../code_snippets/snippet_openclaw_voice_call_runtime.md): `createVoiceCallRuntime` startup spine — config resolution, webhook server, public-URL chain (ngrok/Tailscale), lifecycle teardown, voice-name normalizer.
- [Voice-Call — Webhook Replay Cache](../code_snippets/snippet_openclaw_voice_call_webhook_replay_cache.md): TTL-bounded processed-event-ID set that deduplicates carrier retries.
- [Voice-Call — Webhook Signature Verify](../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md): Telnyx Ed25519 / Twilio HMAC-SHA1 / Plivo HMAC-SHA256 verification behind a single `verifyWebhook(ctx)` method.
- [Voice-Call — Media-Stream Audio](../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md): bidirectional μ-law 8 kHz audio framing on the `/media-stream` WebSocket.
- [Voice-Call — Media-Stream Transcription](../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md): realtime-STT provider integration on the inbound audio fork.
- [Voice-Call — Media-Stream Admission](../code_snippets/snippet_openclaw_voice_call_media_stream_admission.md): admission control that rejects stream connects for unknown or terminal calls.

## Related Analysis (FZ 15)


## References

- [OpenClaw `extensions/voice-call/`](https://github.com/openclaw/openclaw/tree/main/extensions/voice-call): canonical source for `CallManager`, `VoiceCallProvider`, and the three provider implementations.
- [Voice over IP — Wikipedia](https://en.wikipedia.org/wiki/Voice_over_IP): foundational protocol family (SIP, RTP, codecs) underlying every modern voice-call substrate.
- [LiveKit Agents — Documentation](https://docs.livekit.io/agents/): the comparable open-source voice-agent framework, WebRTC-rooms-with-SIP-bridge architecture.
- [Pipecat — Documentation](https://docs.pipecat.ai/): the comparable open-source frame-processor-pipeline voice-agent framework.
- [Twilio Media Streams — Documentation](https://www.twilio.com/docs/voice/media-streams): canonical reference for the μ-law-over-WebSocket audio envelope OpenClaw consumes on the Twilio path.
- [Vapi — Quickstart](https://docs.vapi.ai/quickstart): managed voice-agent platform contrast point; turnkey alternative to the open-substrate approach.
