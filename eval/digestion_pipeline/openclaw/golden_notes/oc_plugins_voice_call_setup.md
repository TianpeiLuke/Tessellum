---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - voice_call
keywords:
  - openclaw voice call plugin
  - voicecall setup smoke cli
  - voice-call plugin config
  - inbound calls allowlist policy
  - per-number routing voice call
  - twilio telnyx plivo provider
  - voice_call agent tool rpc
  - stale call reaper
topics:
  - OpenClaw
  - Voice Call Plugin
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/voice-call
access_control_group: ["general"]
---

# OpenClaw — Operating the Voice Call Plugin (Setup, Inbound, CLI, RPC)

## Overview

This note is the operator procedure for the bundled **Voice Call plugin**: install, carrier-provider + public-webhook config, verify with `voicecall setup`/`smoke`, session scope, inbound-call enablement and routing, stale-call reaping, and driving calls via the `voicecall` CLI, the `voice_call` agent tool, and the `voicecall.*` Gateway RPC — mirroring the `plugins/voice-call` source page from install through troubleshooting. The audio-mode contract (realtime voice, streaming transcription, TTS deep-merge) and the webhook signature/replay security model are split into [oc_plugins_voice_call_audio_modes](oc_plugins_voice_call_audio_modes.md).

The plugin places outbound and accepts inbound voice calls — outbound notifications, multi-turn conversations, full-duplex realtime voice, streaming transcription, and allowlist-gated inbound calls. Current providers: `twilio` (Programmable Voice + Media Streams), `telnyx` (Call Control v2), `plivo` (Voice API + XML transfer + GetInput speech), and `mock` (dev/no network). It runs **inside the Gateway process**; for a remote Gateway, install and configure it on the Gateway host, then restart to load it.

## Quick start

1. **Install.** From npm: `openclaw plugins install @openclaw/voice-call`. From a local folder (dev): `PLUGIN_SRC=./path/to/local/voice-call-plugin`, `openclaw plugins install "$PLUGIN_SRC"`, then `cd "$PLUGIN_SRC" && pnpm install`. The bare package follows the current official release tag; pin a version only for reproducibility. Restart the Gateway so the plugin loads.
2. **Configure provider and webhook.** Set config under `plugins.entries.voice-call.config` (full shape below); at minimum `provider`, provider credentials, `fromNumber`, and a publicly reachable webhook URL.
3. **Verify setup.** `openclaw voicecall setup` checks plugin enablement, provider credentials, webhook exposure, and that only one audio mode (`streaming` or `realtime`) is active; output is readable in chat logs/terminals, with `--json` for scripts.
4. **Smoke test.** `openclaw voicecall smoke` (or `--to "+15555550123"`) — both dry runs by default. Add `--yes` to place a short outbound notify call: `openclaw voicecall smoke --to "+15555550123" --yes`.

For Twilio, Telnyx, and Plivo, setup must resolve to a **public webhook URL**: if `publicUrl`, the tunnel/Tailscale URL, or the serve fallback resolves to loopback or private network space, setup fails rather than start a provider that cannot receive carrier webhooks.

## Configuration

If `enabled: true` but the selected provider lacks credentials, Gateway startup logs a setup-incomplete warning with the missing keys and skips starting the runtime; commands, RPC, and agent tools still return the exact missing configuration when used. Voice-call credentials accept SecretRefs — `twilio.authToken`, `realtime.providers.*.apiKey`, `streaming.providers.*.apiKey`, and `tts.providers.*.apiKey` resolve through the standard SecretRef surface (see [oc_reference_secretref_credential_surface](oc_reference_secretref_credential_surface.md)).

The core config shape (abbreviated; `realtime`/`streaming`/`tts` audio-mode detail in the sibling note):

```json5
{
  plugins: { entries: { "voice-call": {
    enabled: true,
    config: {
      provider: "twilio", // or "telnyx" | "plivo" | "mock"
      fromNumber: "+15550001234", // or TWILIO_FROM_NUMBER
      toNumber: "+15550005678",
      sessionScope: "per-phone", // per-phone | per-call
      numbers: { /* per-number route overrides */ },
      twilio: { accountSid: "ACxxxxxxxx", authToken: "..." },
      telnyx: { apiKey: "...", connectionId: "...", publicKey: "..." },
      plivo: { authId: "MAxxxxxxxxxxxxxxxxxxxx", authToken: "..." },
      serve: { port: 3334, path: "/voice/webhook" },
      webhookSecurity: { allowedHosts: ["voice.example.com"], trustedProxyIPs: ["100.64.0.1"] },
      // Public exposure (pick one): publicUrl | tunnel | tailscale
      outbound: { defaultMode: "notify" }, // notify | conversation
      streaming: { enabled: true },
      realtime: { enabled: false },
    },
  } } },
}
```

The Telnyx webhook public key comes from the Mission Control Portal (Base64; also settable via `TELNYX_PUBLIC_KEY`). The source documents three configuration accordions. **Provider exposure and security notes:** Twilio/Telnyx/Plivo all require a publicly reachable webhook URL, `mock` is a local dev provider, and Telnyx requires `telnyx.publicKey` (or `TELNYX_PUBLIC_KEY`) unless `skipSignatureVerification` is true (local testing only); on ngrok free tier set `publicUrl` to the exact ngrok URL (signature verification is always enforced), `tunnel.allowNgrokFreeTierLoopbackBypass: true` allows invalid-signature Twilio webhooks **only** when `tunnel.provider="ngrok"` and `serve.bind` is loopback (local dev), and since ngrok URLs can drift, production should prefer a stable domain or Tailscale funnel. **Streaming connection caps:** `streaming.preStartTimeoutMs` closes sockets that never send a valid `start` frame; `maxPendingConnections`/`maxPendingConnectionsPerIp` cap unauthenticated pre-start sockets (total / per source IP); `maxConnections` caps total open media stream sockets. **Legacy config migrations:** `provider: "log"`, `twilio.from`, and legacy `streaming.*` OpenAI keys are rewritten by `openclaw doctor --fix` (the old-key compat shim is temporary), auto-migrating `streaming.sttProvider`→`streaming.provider`, `streaming.openaiApiKey`→`streaming.providers.openai.apiKey`, `streaming.sttModel`→`…openai.model`, `streaming.silenceDurationMs`→`…openai.silenceDurationMs`, `streaming.vadThreshold`→`…openai.vadThreshold`.

## Session scope

`sessionScope: "per-phone"` (default) keeps conversation memory across repeat calls from the same caller. Set `sessionScope: "per-call"` when each call should start fresh — e.g. reception, booking, IVR, or Google Meet bridge flows where the same number may represent different meetings.

## Inbound calls

Inbound policy defaults to `disabled`. To enable inbound calls, set:

```json5
{
  inboundPolicy: "allowlist",
  allowFrom: ["+15550001234"],
  inboundGreeting: "Hello! How can I help?",
}
```

`inboundPolicy: "allowlist"` is a **low-assurance caller-ID screen**: the plugin normalizes the provider-supplied `From` and compares it to `allowFrom`. Webhook verification authenticates provider delivery and payload integrity but does **not** prove PSTN/VoIP caller-number ownership — treat `allowFrom` as caller-ID filtering, not strong identity. Auto-responses use the agent system; tune with `responseModel`, `responseSystemPrompt`, and `responseTimeoutMs`.

### Per-number Routing

Use `numbers` when one plugin serves multiple phone numbers and each should behave like a different line (e.g. a casual assistant on one, a business persona with its own response agent and TTS voice on another). Routes are keyed by E.164 number and selected from the dialed `To`; on call arrival Voice Call resolves the matching route once, stores it on the call record, and reuses that config for the greeting, classic auto-response, realtime consult, and TTS playback (global config if none matches). Outbound calls do not use `numbers` — pass the target, message, and session explicitly.

Route overrides currently support `inboundGreeting`, `tts`, `agentId`, `responseModel`, `responseSystemPrompt`, and `responseTimeoutMs`. The `tts` route value deep-merges over the global `tts`, so you can usually override only the provider voice:

```json5
{
  inboundGreeting: "Hello from the main line.",
  responseSystemPrompt: "You are the default voice assistant.",
  tts: { provider: "openai", providers: { openai: { speakerVoice: "coral" } } },
  numbers: {
    "+15550001111": {
      inboundGreeting: "Silver Fox Cards, how can I help?",
      responseSystemPrompt: "You are a concise baseball card specialist.",
      tts: { providers: { openai: { speakerVoice: "alloy" } } },
    },
  },
}
```

### Spoken output contract

For auto-responses, Voice Call appends a strict spoken-output contract to the system prompt, instructing the model to emit `{"spoken":"..."}`. It extracts speech text defensively — ignoring reasoning/error payloads, parsing direct JSON, fenced JSON, or inline `"spoken"` keys, and falling back to plain text while stripping likely planning/meta lead-in — so playback stays focused on caller-facing text without leaking planning text into audio.

### Conversation startup behavior

For outbound `conversation` calls, first-message handling is tied to live playback state. Barge-in queue clear and auto-response are suppressed only while the initial greeting is actively speaking; if initial playback fails, the call returns to `listening` with the message re-queued. Twilio streaming initial playback starts on stream connect without delay. Barge-in aborts active playback and clears queued-but-not-yet-playing Twilio TTS entries (resolved as skipped, so follow-up logic does not wait on audio that will never play). Realtime voice conversations use the realtime stream's own opening turn: Voice Call does **not** post a legacy `<Say>` TwiML update for that message, so outbound `<Connect><Stream>` sessions stay attached.

### Twilio stream disconnect grace

When a Twilio media stream disconnects, Voice Call waits **2000 ms** before auto-ending the call: a reconnect within that window cancels the auto-end; if no stream re-registers after the grace period, the call ends to prevent stuck active calls.

## Stale call reaper

Use `staleCallReaperSeconds` to end calls that never receive a terminal webhook (e.g. notify-mode calls that never complete); default `0` (disabled). Recommended: `120`–`300` for production notify flows, kept **higher than `maxDurationSeconds`** so normal calls finish (start at `maxDurationSeconds + 30–60`).

```json5
{
  plugins: { entries: { "voice-call": { config: {
    maxDurationSeconds: 300,
    staleCallReaperSeconds: 360,
  } } } },
}
```

## CLI

```bash
openclaw voicecall call --to "+15555550123" --message "Hello from OpenClaw"
openclaw voicecall start --to "+15555550123"   # alias for call
openclaw voicecall continue --call-id <id> --message "Any questions?"
openclaw voicecall speak --call-id <id> --message "One moment"
openclaw voicecall dtmf --call-id <id> --digits "ww123456#"
openclaw voicecall end --call-id <id>
openclaw voicecall status --call-id <id>
openclaw voicecall tail
openclaw voicecall latency                      # summarize turn latency from logs
openclaw voicecall expose --mode funnel
```

When the Gateway is already running, operational `voicecall` commands delegate to the Gateway-owned runtime so the CLI does not bind a second webhook server; with no Gateway reachable they fall back to a standalone CLI runtime. `latency` reads `calls.jsonl` from the default voice-call storage path (`--file <path>` for another log, `--last <n>` to limit to the last N records, default 200) and reports p50/p90/p99 turn latency and listen-wait times.

## Agent tool

Tool name: `voice_call`.

| Action          | Args                                       |
| --------------- | ------------------------------------------ |
| `initiate_call` | `message`, `to?`, `mode?`, `dtmfSequence?` |
| `continue_call` | `callId`, `message`                        |
| `speak_to_user` | `callId`, `message`                        |
| `send_dtmf`     | `callId`, `digits`                         |
| `end_call`      | `callId`                                   |
| `get_status`    | `callId`                                   |

The repo ships a matching skill doc at `skills/voice-call/SKILL.md`.

## Gateway RPC

| Method               | Args                                       |
| -------------------- | ------------------------------------------ |
| `voicecall.initiate` | `to?`, `message`, `mode?`, `dtmfSequence?` |
| `voicecall.continue` | `callId`, `message`                        |
| `voicecall.speak`    | `callId`, `message`                        |
| `voicecall.dtmf`     | `callId`, `digits`                         |
| `voicecall.end`      | `callId`                                   |
| `voicecall.status`   | `callId`                                   |

`dtmfSequence` is only valid with `mode: "conversation"`; notify-mode calls needing post-connect digits should use `voicecall.dtmf` after the call exists.

## Troubleshooting

The source documents six cases. **Setup fails webhook exposure:** run setup from the Gateway's environment; for `twilio`/`telnyx`/`plivo`, `webhook-exposure` must be green, and a `publicUrl` in local/private space (`localhost`, `127.0.0.1`, `0.0.0.0`, `10.x`, `172.16.x`-`172.31.x`, `192.168.x`, `169.254.x`, `fc00::/7`, `fd00::/8`) still fails because the carrier cannot call back. Twilio notify-mode outbound calls send the initial `<Say>` TwiML in the create-call request, but a public webhook is still required for status callbacks, conversation calls, pre-connect DTMF, realtime streams, and post-connect control; use one exposure path (`publicUrl`, `tunnel: { provider: "ngrok" }`, or `tailscale: { mode: "funnel", path: "/voice/webhook" }`), then restart/reload the Gateway and re-run `setup` + `smoke`. **Provider credentials fail:** verify the provider's fields — Twilio `twilio.accountSid`/`authToken`/`fromNumber` (or `TWILIO_ACCOUNT_SID`/`TWILIO_AUTH_TOKEN`/`TWILIO_FROM_NUMBER`); Telnyx `telnyx.apiKey`/`connectionId`/`publicKey`/`fromNumber`; Plivo `plivo.authId`/`authToken`/`fromNumber` — and they must exist on the Gateway host (a running Gateway picks up shell-profile edits only after restart/reload). **Calls start but webhooks do not arrive:** confirm the provider console points at the exact webhook URL, then inspect `voicecall status --call-id <id>`, `voicecall tail`, `openclaw logs --follow`; common causes are a `publicUrl`/`serve.path` mismatch, a changed tunnel URL, a proxy stripping host/proto headers, firewall/DNS misrouting, or a Gateway restarted without the plugin — for a proxy/tunnel set `webhookSecurity.allowedHosts`/`trustedProxyIPs`, and `trustForwardingHeaders` only when the proxy boundary is under your control. **Signature verification fails:** signatures are checked against the URL OpenClaw reconstructs from the request, so match `publicUrl` exactly (scheme/host/path), update it on ngrok hostname changes, preserve host/proto headers, and never enable `skipSignatureVerification` outside local testing. **Google Meet Twilio joins fail:** Meet uses this plugin for Twilio dial-in (`openclaw googlemeet setup --transport twilio`); if Voice Call is green but the participant never joins, check the dial-in number, PIN, and `--dtmf-sequence` — Meet starts the Twilio leg via `voicecall.start` with a pre-connect DTMF sequence whose PIN-derived digits prepend the Google Meet plugin's `voiceCall.dtmfDelayMs` as leading Twilio wait digits (default 12 seconds). **Realtime call has no speech:** confirm only one audio mode is enabled (`realtime.enabled` and `streaming.enabled` cannot both be true), a realtime provider plugin is loaded/registered, `realtime.provider` is unset or names a registered provider, and its API key is on the Gateway process (audio-mode detail in [oc_plugins_voice_call_audio_modes](oc_plugins_voice_call_audio_modes.md)).

**Source**: OpenClaw documentation — `plugins/voice-call` (mirror `inbox/openclaw_docs/plugins/voice-call.md`)
**Last Updated**: 2026-06-22
**Status**: Active
