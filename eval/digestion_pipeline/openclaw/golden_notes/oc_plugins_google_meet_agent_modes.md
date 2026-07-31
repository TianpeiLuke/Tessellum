---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - google_meet
keywords:
  - openclaw google_meet tool
  - google meet agent mode
  - google meet bidi mode
  - openclaw_agent_consult
  - realtime toolpolicy safe-read-only
  - googlemeet test-speech
  - googlemeet live test checklist
  - per-meeting subagent session
topics:
  - OpenClaw
  - Google Meet Plugin
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/google-meet
access_control_group: ["general"]
---

# OpenClaw — Google Meet Tool, Agent/Bidi Modes, and Live Test Checklist

## Overview

This note documents the agent-facing `google_meet` tool, the `agent`/`bidi` talk-back modes, and the live-test checklist of the OpenClaw Google Meet plugin — the `Tool`, `Agent and bidi modes`, and `Live test checklist` sections of the `plugins/google-meet` source page. It is the operational procedure for an agent (or operator) to join, speak into, inspect, and verify a Meet session: the tool `action`/`mode` surface and its status fields, how `agent` mode routes participant transcripts through the configured OpenClaw agent versus how `bidi` answers directly with the realtime voice model (and falls back to `openclaw_agent_consult`), and the ordered command sequence that confirms a Chrome-node or Twilio path before handing a meeting to an unattended agent. Plugin install, audio prerequisites, transports, Google OAuth, the full `config` block, and the troubleshooting matrix are covered by sibling notes.

## The `google_meet` Tool

Agents drive the plugin through the `google_meet` tool by passing an `action`. A `join` call takes `url`, `transport`, and `mode`:

```json
{
  "action": "join",
  "url": "https://meet.google.com/abc-defg-hij",
  "transport": "chrome-node",
  "mode": "agent"
}
```

Use `transport: "chrome"` when Chrome runs on the Gateway host and `transport: "chrome-node"` when Chrome runs on a paired node such as a Parallels VM. In both cases the model providers and `openclaw_agent_consult` run on the Gateway host, so model credentials stay there. With the default `mode: "agent"` the realtime transcription provider handles listening, the configured OpenClaw agent produces the answer, and regular OpenClaw TTS speaks it into Meet; use `mode: "bidi"` when you want the realtime voice model to answer directly. Raw `mode: "realtime"` remains accepted as a legacy compatibility alias for `mode: "agent"`, but it is no longer advertised in the agent tool schema. Agent-mode logs include the resolved transcription provider/model at bridge startup and the TTS provider, model, voice, output format, and sample rate after each synthesized reply.

### Session-control actions

The tool exposes additional `action` values for managing an active session:

- `action: "status"` — list active sessions or inspect a session ID.
- `action: "speak"` — with `sessionId` and `message`, make the realtime agent speak immediately.
- `action: "test_speech"` — create or reuse the session, trigger a known phrase, and return `inCall` health when the Chrome host can report it. `test_speech` always forces `mode: "agent"` and fails if asked to run in `mode: "transcribe"` because observe-only sessions intentionally cannot emit speech. Its `speechOutputVerified` result is based on realtime audio output bytes increasing during this test call, so a reused session with older audio does not count as a fresh successful speech check.
- `action: "leave"` — mark a session ended.

A `speak` call supplies `sessionId` and `message`:

```json
{
  "action": "speak",
  "sessionId": "meet_...",
  "message": "Say exactly: I'm here and listening."
}
```

### `status` Chrome health fields

`status` includes Chrome health when available:

- `inCall`: Chrome appears to be inside the Meet call.
- `micMuted`: best-effort Meet microphone state.
- `manualActionRequired` / `manualActionReason` / `manualActionMessage`: the browser profile needs manual login, Meet host admission, permissions, or browser-control repair before speech can work.
- `speechReady` / `speechBlockedReason` / `speechBlockedMessage`: whether managed Chrome speech is allowed now. `speechReady: false` means OpenClaw did not send the intro/test phrase into the audio bridge.
- `providerConnected` / `realtimeReady`: realtime voice bridge state.
- `lastInputAt` / `lastOutputAt`: last audio seen from or sent to the bridge.
- `audioOutputRouted` / `audioOutputDeviceLabel`: whether the Meet tab's media output was actively routed to the BlackHole device used by the bridge.
- `lastSuppressedInputAt` / `suppressedInputBytes`: loopback input ignored while assistant playback is active.

## Agent and Bidi Modes

Chrome `agent` mode is optimized for "my agent is in the meeting" behavior. The realtime transcription provider hears the meeting audio, final participant transcripts are routed through the configured OpenClaw agent, and the answer is spoken through the normal OpenClaw TTS runtime. Set `mode: "bidi"` when you want the realtime voice model to answer directly. Nearby final transcript fragments are coalesced before the consult so one spoken turn does not produce several stale partial answers. Realtime input is also suppressed while queued assistant audio is still playing, and recent assistant-like transcript echoes are ignored before the agent consult so BlackHole loopback does not make the agent answer its own speech.

| Mode    | Who decides the answer        | Speech output path                     | Use when                                              |
| ------- | ----------------------------- | -------------------------------------- | ----------------------------------------------------- |
| `agent` | The configured OpenClaw agent | Normal OpenClaw TTS runtime            | You want "my agent is in the meeting" behavior        |
| `bidi`  | The realtime voice model      | Realtime voice provider audio response | You want the lowest-latency conversational voice loop |

### `openclaw_agent_consult` and the per-meeting subagent

In `bidi` mode, when the realtime model needs deeper reasoning, current information, or normal OpenClaw tools, it can call `openclaw_agent_consult`. The consult tool runs the regular OpenClaw agent behind the scenes with recent meeting transcript context and returns a concise spoken answer. In `agent` mode, OpenClaw sends that answer directly to the TTS runtime; in `bidi` mode, the realtime voice model can speak the consult result back into the meeting. It uses the same shared consult machinery as Voice Call. By default, consults run against the `main` agent. Set `realtime.agentId` when a Meet lane should consult a dedicated OpenClaw agent workspace, model defaults, tool policy, memory, and session history. Agent-mode consults use a per-meeting `agent:<id>:subagent:google-meet:<session>` session key so follow-up questions keep meeting context while inheriting normal agent policy from the configured agent. The consult session key is scoped per Meet session, so follow-up consult calls can reuse prior consult context during the same meeting.

### `realtime.toolPolicy`

`realtime.toolPolicy` controls the consult run:

- `safe-read-only`: expose the consult tool and limit the regular agent to `read`, `web_search`, `web_fetch`, `x_search`, `memory_search`, and `memory_get`.
- `owner`: expose the consult tool and let the regular agent use the normal agent tool policy.
- `none`: do not expose the consult tool to the realtime voice model.

### Forcing a spoken readiness check

To force a spoken readiness check after Chrome has fully joined the call:

```bash
openclaw googlemeet speak meet_... "Say exactly: I'm here and listening."
```

For the full join-and-speak smoke:

```bash
openclaw googlemeet test-speech https://meet.google.com/abc-defg-hij \
  --transport chrome-node \
  --message "Say exactly: I'm here and listening."
```

## Live Test Checklist

Use this sequence before handing a meeting to an unattended agent:

```bash
openclaw googlemeet setup
openclaw nodes status
openclaw googlemeet test-speech https://meet.google.com/abc-defg-hij \
  --transport chrome-node \
  --message "Say exactly: Google Meet speech test complete."
```

Expected Chrome-node state:

- `googlemeet setup` is all green.
- `googlemeet setup` includes `chrome-node-connected` when Chrome-node is the default transport or a node is pinned.
- `nodes status` shows the selected node connected.
- The selected node advertises both `googlemeet.chrome` and `browser.proxy`.
- The Meet tab joins the call and `test-speech` returns Chrome health with `inCall: true`.

For a remote Chrome host such as a Parallels macOS VM, this is the shortest safe check after updating the Gateway or the VM:

```bash
openclaw googlemeet setup
openclaw nodes status --connected
openclaw nodes invoke \
  --node parallels-macos \
  --command googlemeet.chrome \
  --params '{"action":"setup"}'
```

That proves the Gateway plugin is loaded, the VM node is connected with the current token, and the Meet audio bridge is available before an agent opens a real meeting tab.

For a Twilio smoke, use a meeting that exposes phone dial-in details. The expected Twilio state is: `googlemeet setup` includes green `twilio-voice-call-plugin`, `twilio-voice-call-credentials`, and `twilio-voice-call-webhook` checks; `voicecall` is available in the CLI after Gateway reload; the returned session has `transport: "twilio"` and a `twilio.voiceCallId`; `openclaw logs --follow` shows DTMF TwiML served before realtime TwiML, then a realtime bridge with the initial greeting queued; and `googlemeet leave <sessionId>` hangs up the delegated voice call.

**Source**: OpenClaw documentation — `plugins/google-meet` (mirror `inbox/openclaw_docs/plugins/google-meet.md`), sections Tool / Agent and bidi modes / Live test checklist
**Last Updated**: 2026-06-22
**Status**: Active
