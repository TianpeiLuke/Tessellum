---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - google_meet
keywords:
  - google meet plugin troubleshooting
  - parallels chrome node host
  - openclaw_allow_insecure_private_ws
  - gateway nodes allowcommands
  - googlemeet.chrome browser.proxy
  - no connected google meet-capable node
  - gateway token mismatch
  - twilio dtmf dial-in failures
  - manualactionrequired speechready
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

# OpenClaw — Operating the Google Meet Plugin Across a Node Host and Troubleshooting

## Overview

This note is the operational procedure for running the OpenClaw Google Meet plugin across a node host and diagnosing the symptom→fix matrix, mirroring the `### Local gateway + Parallels Chrome` subsection (under Quick start), the `## Troubleshooting` section (all 8 H3 symptoms), and the closing `## Notes` of the `plugins/google-meet` source page. It covers the Gateway-vs-Parallels-VM split, the `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS` plaintext-WebSocket opt-in for LAN nodes, node pairing and `gateway.nodes.allowCommands`, the `googlemeet.chrome` + `browser.proxy` capability requirement, and each documented failure. Plugin enablement, OAuth/config, and the agent/bidi/transcribe modes are covered in the sibling notes.

## Operating across a node host (Local Gateway + Parallels Chrome)

You do **not** need a full OpenClaw Gateway or model API key inside a macOS VM just to make the VM own Chrome. Run the Gateway and agent locally, then run a node host in the VM and enable the bundled plugin there so the node advertises the Chrome command. The **Gateway host** owns the Gateway, agent workspace, model/API keys, realtime provider, and Google Meet plugin config; the **Parallels macOS VM** owns the OpenClaw CLI/node host, Google Chrome, SoX, `BlackHole 2ch`, and a signed-in Chrome profile (the Gateway service, agent config, model keys, and provider setup are not needed in the VM). Install the VM audio dependencies (`brew install blackhole-2ch sox`), `sudo reboot` so macOS exposes `BlackHole 2ch`, verify with `system_profiler SPAudioDataType | grep -i BlackHole` and `command -v sox`, then install OpenClaw in the VM and run `openclaw plugins enable google-meet`.

### Start and pair the node (plaintext-WS opt-in)

Start the node host in the VM, then approve it from the Gateway host. If `<gateway-host>` is a LAN IP without TLS, the node refuses the plaintext WebSocket unless you opt in for that trusted private network with `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` (also used when installing the node as a LaunchAgent):

```bash
openclaw node run --host <gateway-host> --port 18789 --display-name parallels-macos
# LAN, no TLS:
OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1 \
  openclaw node run --host <gateway-lan-ip> --port 18789 --display-name parallels-macos
# install as LaunchAgent (stores the env var in the LaunchAgent environment):
OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1 \
  openclaw node install --host <gateway-lan-ip> --port 18789 --display-name parallels-macos --force
openclaw node restart
```

`OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` is process environment, not an `openclaw.json` setting (stored in the LaunchAgent environment when present on `node install`). Approve the node from the Gateway host (`openclaw devices list`, `openclaw devices approve <requestId>`), and confirm with `openclaw nodes status` that the Gateway sees the node advertising both `googlemeet.chrome` and `browser.proxy`.

### Route Meet through the node

The Gateway must allow both node commands via `gateway.nodes.allowCommands`, and the plugin config pins the transport and node:

```json5
{
  gateway: {
    nodes: {
      allowCommands: ["googlemeet.chrome", "browser.proxy"],
    },
  },
  plugins: {
    entries: {
      "google-meet": {
        enabled: true,
        config: {
          defaultTransport: "chrome-node",
          chrome: {
            guestName: "OpenClaw Agent",
            autoJoin: true,
            reuseExistingTab: true,
          },
          chromeNode: {
            node: "parallels-macos",
          },
        },
      },
    },
  },
}
```

Then join from the Gateway host (`openclaw googlemeet join https://meet.google.com/abc-defg-hij`) or via the `google_meet` tool with `transport: "chrome-node"`; for a smoke test, run `openclaw googlemeet test-speech https://meet.google.com/abc-defg-hij`. During realtime join, browser automation fills the guest name, clicks Join/Ask to join, and accepts Meet's first-run "Use microphone" choice; when the profile is signed out, Meet awaits host admission, Chrome needs mic/camera permission, or a prompt is unresolvable, the result reports `manualActionRequired: true` with `manualActionReason`/`manualActionMessage` (see "Browser opens but agent cannot join"). If `chromeNode.node` is omitted, OpenClaw auto-selects only when exactly one connected node advertises both `googlemeet.chrome` and browser control; with several capable nodes, set `chromeNode.node` to the node id, display name, or remote IP.

### Common failure checks (node host)

Most node-host failure messages are expanded in the Troubleshooting matrix below (`No connected Google Meet-capable node`, `BlackHole 2ch audio device not found` / `... not found on the node`, Chrome opens but cannot join). Two node-only states are documented only here: `Configured Google Meet node ... is not usable: offline` means the pinned node is known but unavailable — treat it as diagnostic state, not a usable Chrome host, and report the blocker rather than silently falling back to another transport; duplicate Meet tabs are prevented by `chrome.reuseExistingTab: true`, which activates an existing tab for the same Meet URL (and reuses an in-progress `https://meet.google.com/new` or Google account prompt tab during creation). For no audio, route Meet mic/speaker through OpenClaw's virtual audio path with separate virtual devices or Loopback-style routing.

## Troubleshooting symptom → fix matrix

### Agent cannot see the Google Meet tool

Confirm the plugin is enabled and reload the Gateway (`openclaw plugins list | grep google-meet`, then `openclaw googlemeet setup`). After editing `plugins.entries.google-meet`, restart or reload the Gateway — the running agent only sees plugin tools registered by the current Gateway process. On non-macOS Gateway hosts the `google_meet` tool stays visible, but local Chrome talk-back actions are blocked before the audio bridge (they depend on macOS `BlackHole 2ch`), so Linux agents should use `mode: "transcribe"`, Twilio dial-in, or a macOS `chrome-node` host.

### No connected Google Meet-capable node

On the node host run `openclaw plugins enable google-meet`, `openclaw plugins enable browser`, and `openclaw node run` (with `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` for a LAN/no-TLS Gateway, as above). On the Gateway host approve the node (`openclaw devices list`, `openclaw devices approve <requestId>`, `openclaw nodes status`). The node must be connected and list `googlemeet.chrome` plus `browser.proxy`, and the Gateway must allow those commands via `gateway.nodes.allowCommands: ["browser.proxy", "googlemeet.chrome"]`. If `googlemeet setup` fails `chrome-node-connected` or the Gateway log reports `gateway token mismatch`, reinstall the node with the current token (`openclaw node install ... --force`), then reload the node service and re-run `openclaw googlemeet setup` and `openclaw nodes status --connected`.

### Browser opens but agent cannot join

Run `googlemeet test-listen` for observe-only joins or `googlemeet test-speech` for realtime joins, then inspect the returned Chrome health. If either reports `manualActionRequired: true`, show `manualActionMessage` and stop retrying until the action completes. Common manual actions: sign in to the Chrome profile; admit the guest from the Meet host account; grant Chrome mic/camera permissions; close or repair a stuck Meet permission dialog. Do not report "not signed in" just because Meet shows "Do you want people to hear you in the meeting?" — that is the audio-choice interstitial; OpenClaw clicks **Use microphone** when available and keeps waiting for the real meeting state.

### Meeting creation fails

`googlemeet create` first uses the Google Meet API `spaces.create` endpoint when OAuth credentials are configured; without them it falls back to the pinned Chrome node browser. Confirm:

- API creation: `oauth.clientId` and `oauth.refreshToken` (or matching `OPENCLAW_GOOGLE_MEET_*` env vars) are present, and the refresh token was minted after create support was added — older tokens may lack the `meetings.space.created` scope, so rerun `openclaw googlemeet auth login --json` and update config.
- Browser fallback: `defaultTransport: "chrome-node"` and `chromeNode.node` point at a connected node with `browser.proxy` and `googlemeet.chrome`, and the OpenClaw Chrome profile on that node is signed in to Google and can open `https://meet.google.com/new`. Retries reuse an existing `https://meet.google.com/new` or Google account prompt tab — on timeout, retry the tool call.
- Browser fallback: on `manualActionRequired: true`, use the returned `browser.nodeId`, `browser.targetId`, `browserUrl`, and `manualActionMessage` to guide the operator and do not retry until it completes; for the audio-choice interstitial OpenClaw clicks **Use microphone** (or **Continue without microphone** for create-only) and the error should mention `meet-audio-choice-required`, not `google-login-required`.

### Agent joins but does not talk

Check the realtime path with `openclaw googlemeet setup` and `openclaw googlemeet doctor`. Use `mode: "agent"` for the STT → OpenClaw agent → TTS talk-back path, `mode: "bidi"` for the direct realtime voice fallback; `mode: "transcribe"` intentionally does not start the talk-back bridge. For observe-only debugging, run `openclaw googlemeet status --json <session-id>` after participants speak and check `captioning`, `transcriptLines`, and `lastCaptionText` — if `inCall` is true but `transcriptLines` stays at `0`, captions may be disabled, no one has spoken, the Meet UI changed, or captions are unavailable for the meeting language/account. `googlemeet test-speech` reports whether bridge output bytes were observed; if `speechOutputVerified` is false and `speechOutputTimedOut` is true, the provider may have accepted the utterance but OpenClaw saw no new output bytes reach the Chrome audio bridge. Also verify a realtime provider key on the Gateway host (`OPENAI_API_KEY` or `GEMINI_API_KEY`), `BlackHole 2ch` and `sox` present on the Chrome host, and Meet mic/speaker routed through OpenClaw's virtual audio path (`doctor` should show `meet output routed: yes` for local Chrome realtime joins). `googlemeet doctor [session-id]` prints session/node/in-call state, manual action reason, provider connection, `realtimeReady`, audio activity, timestamps, byte counters, and browser URL; use `googlemeet status [session-id] --json` for raw JSON, and `googlemeet doctor --oauth` (optionally `--meeting`/`--create-space`) to verify OAuth without exposing tokens. If a Meet tab is open after a timeout, inspect it without opening another via `openclaw googlemeet recover-tab` (tool action `recover_current_tab`): it focuses an existing tab, opens no new tab/session, and reports the current blocker. The CLI needs the Gateway running; `chrome-node` also needs the Chrome node connected.

### Twilio setup checks fail

`twilio-voice-call-plugin` fails when `voice-call` is not allowed or not enabled — add it to `plugins.allow`, enable `plugins.entries.voice-call`, and reload the Gateway. `twilio-voice-call-credentials` fails when the backend is missing account SID, auth token, or caller number; set `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_FROM_NUMBER` on the Gateway host. `twilio-voice-call-webhook` fails when `voice-call` has no public webhook exposure or `publicUrl` points at loopback/private space; set `plugins.entries.voice-call.config.publicUrl` to the public provider URL or configure a `voice-call` tunnel/Tailscale exposure. Loopback/private URLs are not valid for carrier callbacks: do not use `localhost`, `127.0.0.1`, `0.0.0.0`, `10.x`, `172.16.x`-`172.31.x`, `192.168.x`, `169.254.x`, `fc00::/7`, or `fd00::/8` as `publicUrl` (for local dev use a `tunnel: { provider: "ngrok" }` or `tailscale: { mode: "funnel", path: "/voice/webhook" }` exposure). Then reload the Gateway and run `openclaw googlemeet setup --transport twilio`, `openclaw voicecall setup`, and `openclaw voicecall smoke` (readiness-only; dry-run with `--to "+15555550123"`, add `--yes` only for a live outbound call).

### Twilio call starts but never enters the meeting

Confirm the Meet event exposes phone dial-in details and pass the exact dial-in number and PIN or a custom DTMF sequence; use leading `w` or commas in `--dtmf-sequence` for a pause before the PIN:

```bash
openclaw googlemeet join https://meet.google.com/abc-defg-hij \
  --transport twilio \
  --dial-in-number +15551234567 \
  --dtmf-sequence ww123456#
```

If the call is created but the Meet roster never shows the dial-in participant: run `openclaw googlemeet doctor <session-id>` to confirm the delegated Twilio call ID, DTMF queueing, and intro-greeting request; `openclaw voicecall status --call-id <id>` to confirm the call is active; `openclaw voicecall tail` to check Twilio webhooks reach the Gateway; and `openclaw logs --follow` for the Twilio Meet sequence (Google Meet delegates the join, Voice Call serves pre-connect DTMF TwiML then realtime TwiML, then Google Meet requests intro speech with `voicecall.speak`). Re-run `openclaw googlemeet setup --transport twilio` (a green check does not prove the PIN sequence is correct), confirm the dial-in number matches the Meet invitation's region/PIN, and increase `voiceCall.dtmfDelayMs` from the 12-second default if Meet answers slowly or the transcript still prompts for a PIN after pre-connect DTMF. If the transcript still contains "enter the meeting PIN", the phone leg has not joined the Meet room. If webhooks do not arrive, debug the Voice Call plugin first — the provider must reach `publicUrl` or the configured tunnel.

## Notes (boundaries and audio routing)

Google Meet's official media API is receive-oriented, so speaking into a call still needs a participant path, and the plugin keeps that boundary visible: Chrome handles browser participation and local audio; Twilio handles phone dial-in. Chrome talk-back modes need `BlackHole 2ch` plus either `chrome.audioInputCommand` + `chrome.audioOutputCommand` (OpenClaw owns the bridge, default 24 kHz PCM16) or `chrome.audioBridgeCommand` (an external bridge owning the whole local audio path that must exit after starting/validating its daemon — only valid for `bidi`, since `agent` mode needs direct command-pair access for TTS). In agent mode the meeting consultant session forks the caller's transcript before answering, and the Meet session stays separate (`agent:<agentId>:subagent:google-meet:<sessionId>`) so follow-ups do not mutate the caller transcript. For clean duplex audio, route Meet output and microphone through separate virtual devices or a Loopback-style graph — a single shared BlackHole device can echo participants back into the call; the command-pair bridge's `chrome.bargeInInputCommand` (an operator-configured local command — use a trusted path) can clear assistant playback when a human starts talking. `googlemeet speak` triggers the active talk-back bridge and `googlemeet leave` stops it (for Twilio sessions, `leave` also hangs up the underlying voice call); use `googlemeet end-active-conference` to close the active Google Meet conference for an API-managed space.

**Source**: OpenClaw documentation — `plugins/google-meet` (mirror `inbox/openclaw_docs/plugins/google-meet.md`)
**Last Updated**: 2026-06-22
**Status**: Active
