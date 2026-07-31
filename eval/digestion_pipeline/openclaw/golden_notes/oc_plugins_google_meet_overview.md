---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - google_meet
keywords:
  - openclaw google meet plugin
  - googlemeet join create cli
  - google_meet tool agent mode
  - chrome chrome-node twilio transport
  - blackhole 2ch sox audio bridge
  - realtime transcription tts talk-back
  - google meet space create api browser fallback
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

# OpenClaw — Google Meet Plugin Overview, Quick Start, and Transports

## Overview

This note is the procedural overview of the OpenClaw **Google Meet plugin**: what the plugin does, how to install its audio dependencies and enable it, the `googlemeet` CLI / `google_meet` tool quick-start flow (setup, join, create), and the two browser/phone transports (`Chrome`/`chrome-node` and `Twilio`). It mirrors the `plugins/google-meet` source page lead plus its **Quick start**, **Install notes**, and **Transports** sections. OAuth/config, the agent/bidi/transcribe modes, and node-host troubleshooting are split into the sibling notes linked under Related Notes.

## What the plugin does (explicit by design)

Google Meet participant support for OpenClaw is **explicit by design** — it never auto-discovers meetings:

- It only joins an explicit `https://meet.google.com/...` URL.
- It can create a new Meet space through the Google Meet API, then join the returned URL.
- `agent` is the default talk-back mode: realtime transcription listens, the configured OpenClaw agent answers, and regular OpenClaw TTS speaks into Meet.
- `bidi` remains available as the fallback direct realtime voice model mode.
- Agents choose the join behavior with `mode`: use `agent` for live listen/talk-back, `bidi` for direct realtime voice fallback, or `transcribe` to join/control the browser without the talk-back bridge.
- Auth starts as personal Google OAuth or an already signed-in Chrome profile.
- There is **no automatic consent announcement**.
- The default Chrome audio backend is `BlackHole 2ch`.
- Chrome can run locally or on a paired node host.
- Twilio accepts a dial-in number plus optional PIN or DTMF sequence; it cannot dial a Meet URL directly.
- The CLI command is `googlemeet`; `meet` is reserved for broader agent teleconference workflows.

## Quick start

Install the local audio dependencies and configure a realtime transcription provider plus regular OpenClaw TTS. OpenAI is the default transcription provider; Google Gemini Live also works as a separate `bidi` voice fallback with `realtime.voiceProvider: "google"`:

```bash
brew install blackhole-2ch sox
export OPENAI_API_KEY=sk-...
# only needed when realtime.voiceProvider is "google" for bidi mode
export GEMINI_API_KEY=...
```

`blackhole-2ch` installs the `BlackHole 2ch` virtual audio device. Homebrew's installer requires a reboot (`sudo reboot`) before macOS exposes the device; after reboot verify both pieces with `system_profiler SPAudioDataType | grep -i BlackHole` and `command -v sox`. Enable the plugin under `plugins.entries.google-meet`, then check setup:

```json5
{
  plugins: {
    entries: {
      "google-meet": {
        enabled: true,
        config: {},
      },
    },
  },
}
```

Check setup with `openclaw googlemeet setup`. The setup output is meant to be agent-readable and mode-aware. It reports Chrome profile, node pinning, and, for realtime Chrome joins, the BlackHole/SoX audio bridge and delayed realtime intro checks. For observe-only joins, check the same transport with `openclaw googlemeet setup --transport chrome-node --mode transcribe`; that mode skips realtime audio prerequisites because it does not listen through or speak through the bridge. When Twilio delegation is configured, setup also reports whether the `voice-call` plugin, Twilio credentials, and public webhook exposure are ready. Treat any `ok: false` check as a blocker for the checked transport and mode before asking an agent to join. Use `openclaw googlemeet setup --json` for scripts, and `--transport chrome`, `--transport chrome-node`, or `--transport twilio` to preflight a specific transport. For Twilio, always preflight explicitly (`openclaw googlemeet setup --transport twilio`) when the default transport is Chrome — that catches missing `voice-call` wiring, Twilio credentials, or unreachable webhook exposure before the agent tries to dial.

Join a meeting from the CLI, or let an agent join through the `google_meet` tool:

```bash
openclaw googlemeet join https://meet.google.com/abc-defg-hij
```

```json
{
  "action": "join",
  "url": "https://meet.google.com/abc-defg-hij",
  "transport": "chrome-node",
  "mode": "agent"
}
```

The agent-facing `google_meet` tool stays available on non-macOS hosts for artifact, calendar, setup, transcribe, Twilio, and `chrome-node` flows. Local Chrome talk-back actions are blocked there because the bundled Chrome audio path currently depends on macOS `BlackHole 2ch`. On Linux, use `mode: "transcribe"`, Twilio dial-in, or a macOS `chrome-node` host for Chrome talk-back participation.

### Creating a meeting

Create a new meeting and join it with `openclaw googlemeet create --transport chrome-node --mode agent`. For API-created rooms, use Google Meet `SpaceConfig.accessType` to make the room's no-knock policy explicit instead of inherited from Google account defaults (`openclaw googlemeet create --access-type OPEN --transport chrome-node --mode agent`). `OPEN` lets anyone with the Meet URL join without knocking; `TRUSTED` lets the host organization's trusted users, invited external users, and dial-in users join without knocking; `RESTRICTED` limits no-knock entry to invitees. These settings only apply to the official Google Meet API creation path, so OAuth credentials must be configured. If you authenticated before this option existed, rerun `openclaw googlemeet auth login --json` after adding the `meetings.space.settings` scope to your Google OAuth consent screen. Create only the URL without joining with `openclaw googlemeet create --no-join`.

`googlemeet create` has two paths:

- **API create**: used when Google Meet OAuth credentials are configured. This is the most deterministic path and does not depend on browser UI state.
- **Browser fallback**: used when OAuth credentials are absent. OpenClaw uses the pinned Chrome node, opens `https://meet.google.com/new`, waits for Google to redirect to a real meeting-code URL, then returns that URL. This path requires the OpenClaw Chrome profile on the node to already be signed in to Google. Browser automation handles Meet's own first-run microphone prompt; that prompt is not treated as a Google login failure. Join and create flows also try to reuse an existing Meet tab before opening a new one — matching ignores harmless URL query strings such as `authuser`, so an agent retry should focus the already-open meeting instead of creating a second Chrome tab.

The command/tool output includes a `source` field (`api` or `browser`) so agents can explain which path was used. `create` joins the new meeting by default and returns `joined: true` plus the join session; to only mint the URL, use `create --no-join` on the CLI or pass `"join": false` to the tool. An agent should call `google_meet` with `action: "create"` and then share the returned `meetingUri`.

### Observe-only joins and realtime health

For an observe-only/browser-control join, set `"mode": "transcribe"`. That does not start the duplex realtime voice bridge, does not require BlackHole or SoX, and will not talk back into the meeting. Chrome joins in this mode also avoid OpenClaw's microphone/camera permission grant and avoid the Meet **Use microphone** path; if Meet shows an audio-choice interstitial, automation tries the no-microphone path and otherwise reports a manual action. In transcribe mode, managed Chrome transports also install a best-effort Meet caption observer. `googlemeet status --json` and `googlemeet doctor` surface `captioning`, `captionsEnabledAttempted`, `transcriptLines`, `lastCaptionAt`, `lastCaptionSpeaker`, `lastCaptionText`, and a short `recentTranscript` tail so operators can tell whether the browser joined and whether Meet captions are producing text. Use `openclaw googlemeet test-listen <meet-url> --transport chrome-node` for a yes/no probe: it joins in transcribe mode, waits for fresh caption or transcript movement, and returns `listenVerified`, `listenTimedOut`, manual action fields, and the latest caption health.

During realtime sessions, `google_meet` status includes browser and audio bridge health such as `inCall`, `manualActionRequired`, `providerConnected`, `realtimeReady`, `audioInputActive`, `audioOutputActive`, last input/output timestamps, byte counters, and bridge closed state. If a safe Meet page prompt appears, browser automation handles it when it can; login, host admission, and browser/OS permission prompts are reported as manual action with a reason and message for the agent to relay. Managed Chrome sessions only emit the intro or test phrase after browser health reports `inCall: true`; otherwise status reports `speechReady: false` and the speech attempt is blocked instead of pretending the agent spoke into the meeting. Local Chrome joins through the signed-in OpenClaw browser profile; realtime mode requires `BlackHole 2ch` for the microphone/speaker path. For clean duplex audio, use separate virtual devices or a Loopback-style graph — a single BlackHole device is enough for a first smoke test but can echo.

## Install notes

The Chrome talk-back default uses two external tools:

- `sox`: command-line audio utility. The plugin uses explicit CoreAudio device commands for the default 24 kHz PCM16 audio bridge.
- `blackhole-2ch`: macOS virtual audio driver. It creates the `BlackHole 2ch` audio device that Chrome/Meet can route through.

OpenClaw does not bundle or redistribute either package; the docs ask users to install them as host dependencies through Homebrew. SoX is licensed as `LGPL-2.0-only AND GPL-2.0-only`; BlackHole is GPL-3.0. If you build an installer or appliance that bundles BlackHole with OpenClaw, review BlackHole's upstream licensing terms or get a separate license from Existential Audio.

## Transports

### Chrome

Chrome transport opens the Meet URL through OpenClaw browser control and joins as the signed-in OpenClaw browser profile. On macOS, the plugin checks for `BlackHole 2ch` before launch; if configured, it also runs an audio bridge health command and startup command before opening Chrome. Use `chrome` (`openclaw googlemeet join <url> --transport chrome`) when Chrome/audio live on the Gateway host; use `chrome-node` (`openclaw googlemeet join <url> --transport chrome-node`) when Chrome/audio live on a paired node such as a Parallels macOS VM. For local Chrome, choose the profile with `browser.defaultProfile`; `chrome.browserProfile` is passed to `chrome-node` hosts. Route Chrome microphone and speaker audio through the local OpenClaw audio bridge. If `BlackHole 2ch` is not installed, the join fails with a setup error instead of silently joining without an audio path.

### Twilio

Twilio transport is a strict dial plan delegated to the **Voice Call plugin**. It does not parse Meet pages for phone numbers. Use this when Chrome participation is not available or you want a phone dial-in fallback. Google Meet must expose a phone dial-in number and PIN for the meeting; OpenClaw does not discover those from the Meet page. Enable the Voice Call plugin on the **Gateway host**, not on the Chrome node:

```json5
{
  plugins: {
    allow: ["google-meet", "voice-call", "google"],
    entries: {
      "google-meet": {
        enabled: true,
        config: { defaultTransport: "chrome-node" },
      },
      "voice-call": {
        enabled: true,
        config: {
          provider: "twilio",
          inboundPolicy: "allowlist",
          realtime: {
            enabled: true,
            provider: "google",
            instructions: "Join this Google Meet as an OpenClaw agent. Be brief.",
            toolPolicy: "safe-read-only",
          },
        },
      },
      google: { enabled: true },
    },
  },
}
```

Provide Twilio credentials through environment (which keeps secrets out of `openclaw.json`) or config: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`, and `GEMINI_API_KEY` (use `realtime.provider: "openai"` with the OpenAI provider plugin and `OPENAI_API_KEY` instead if that is your realtime voice provider). Restart or reload the Gateway after enabling `voice-call`; plugin config changes do not appear in an already running Gateway process until it reloads. Then verify with `openclaw config validate`, `openclaw plugins list | grep -E 'google-meet|voice-call'`, and `openclaw googlemeet setup`. When Twilio delegation is wired, `googlemeet setup` includes successful `twilio-voice-call-plugin`, `twilio-voice-call-credentials`, and `twilio-voice-call-webhook` checks. Dial in with `--dial-in-number` plus `--pin`, or `--dtmf-sequence` when the meeting needs a custom sequence:

```bash
openclaw googlemeet join https://meet.google.com/abc-defg-hij \
  --transport twilio --dial-in-number +15551234567 --pin 123456

openclaw googlemeet join https://meet.google.com/abc-defg-hij \
  --transport twilio --dial-in-number +15551234567 --dtmf-sequence ww123456#
```

**Source**: OpenClaw documentation — `plugins/google-meet` (mirror `inbox/openclaw_docs/plugins/google-meet.md`)
**Last Updated**: 2026-06-22
**Status**: Active
