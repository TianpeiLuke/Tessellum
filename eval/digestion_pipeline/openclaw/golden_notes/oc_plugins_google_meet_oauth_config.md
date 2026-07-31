---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - google_meet
keywords:
  - google meet oauth
  - googlemeet auth login
  - meetings.space.created scope
  - refresh token mint
  - googlemeet doctor oauth
  - openclaw_google_meet env vars
  - google-meet plugin config
  - realtime transcription provider
  - chrome audio bridge config
topics:
  - OpenClaw
  - Google Meet Plugin
  - OAuth
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/google-meet
access_control_group: ["general"]
---

# OpenClaw — Google Meet Plugin: OAuth Setup and Plugin Config

## Overview

This note is the procedure for authenticating the OpenClaw Google Meet plugin to the official Google Meet REST API and for configuring the plugin's behavior. It covers the OAuth-and-preflight workflow — when OAuth is needed, creating Google Cloud OAuth credentials and scopes, minting and storing the refresh token with `googlemeet auth login`, the non-secret `googlemeet doctor --oauth` preflight, and the accepted `OPENCLAW_GOOGLE_MEET_*` environment-variable fallbacks — plus the `plugins.entries.google-meet.config` block (defaults, transports, `chrome`/`chromeNode`, and the `realtime` transcription/voice surface). It mirrors the `OAuth and preflight` (+ its three H3 sub-sections) and `Config` sections of the `plugins/google-meet` source page. The browser-only join path, transports overview, and the agent/bidi/transcribe modes live in the sibling overview and agent-modes notes.

## When OAuth is needed

OAuth is optional for creating a Meet link because `googlemeet create` can fall back to browser automation. Configure OAuth when you want official API create, space resolution, or Meet Media API preflight checks. Google Meet API access uses user OAuth: create a Google Cloud OAuth client, request the required scopes, authorize a Google account, then store the resulting refresh token in the Google Meet plugin config or provide the `OPENCLAW_GOOGLE_MEET_*` environment variables.

OAuth does not replace the Chrome join path. Chrome and Chrome-node transports still join through a signed-in Chrome profile, BlackHole/SoX, and a connected node when you use browser participation. OAuth is only for the official Google Meet API path: create meeting spaces, resolve spaces, and run Meet Media API preflight checks. No OAuth credentials are needed for the browser fallback; in that mode, Google auth comes from the signed-in Chrome profile on the selected node, not from OpenClaw config.

## Create Google credentials

In Google Cloud Console: (1) create or select a Google Cloud project; (2) enable the **Google Meet REST API** for that project; (3) configure the OAuth consent screen — **Internal** is simplest for a Google Workspace organization, **External** works for personal/test setups (while the app is in Testing, add each Google account that will authorize the app as a test user); (4) add the scopes OpenClaw requests; (5) create an OAuth client ID with application type **Web application** and authorized redirect URI; (6) copy the client ID and client secret.

The four requested scopes and the authorized redirect URI are copied verbatim below.

```text
https://www.googleapis.com/auth/meetings.space.created
https://www.googleapis.com/auth/meetings.space.readonly
https://www.googleapis.com/auth/meetings.space.settings
https://www.googleapis.com/auth/meetings.conference.media.readonly

http://localhost:8085/oauth2callback
```

Each scope has a distinct purpose: `meetings.space.created` is required by Google Meet `spaces.create`; `meetings.space.readonly` lets OpenClaw resolve Meet URLs/codes to spaces; `meetings.space.settings` lets OpenClaw pass `SpaceConfig` settings such as `accessType` during API room creation; `meetings.conference.media.readonly` is for Meet Media API preflight and media work (Google may require Developer Preview enrollment for actual Media API use). If you only need browser-based Chrome joins, skip OAuth entirely.

## Mint the refresh token

Configure `oauth.clientId` and optionally `oauth.clientSecret`, or pass them as environment variables, then run `openclaw googlemeet auth login --json`. The command prints an `oauth` config block with a refresh token. It uses PKCE, localhost callback on `http://localhost:8085/oauth2callback`, and a manual copy/paste flow with `--manual` (use manual mode when the browser cannot reach the local callback).

```bash
OPENCLAW_GOOGLE_MEET_CLIENT_ID="your-client-id" \
OPENCLAW_GOOGLE_MEET_CLIENT_SECRET="your-client-secret" \
openclaw googlemeet auth login --json

# when the browser cannot reach the local callback:
OPENCLAW_GOOGLE_MEET_CLIENT_ID="your-client-id" \
OPENCLAW_GOOGLE_MEET_CLIENT_SECRET="your-client-secret" \
openclaw googlemeet auth login --json --manual
```

The JSON output includes an `oauth` object (`clientId`, `clientSecret`, `refreshToken`, `accessToken`, numeric `expiresAt`) plus a `scope` field. Store the `oauth` object under the Google Meet plugin config — the source stores only `clientId`, `clientSecret`, and `refreshToken` in config:

```json5
{
  plugins: {
    entries: {
      "google-meet": {
        enabled: true,
        config: {
          oauth: {
            clientId: "your-client-id",
            clientSecret: "your-client-secret",
            refreshToken: "refresh-token",
          },
        },
      },
    },
  },
}
```

Prefer environment variables when you do not want the refresh token in config. If both config and environment values are present, the plugin resolves config first and then environment fallback. The OAuth consent includes Meet space creation, Meet space read access, and Meet conference media read access. If you authenticated before meeting creation support existed, rerun `openclaw googlemeet auth login --json` so the refresh token has the `meetings.space.created` scope.

## Verify OAuth with doctor

Run the OAuth doctor when you want a fast, non-secret health check: `openclaw googlemeet doctor --oauth --json`. This does not load the Chrome runtime or require a connected Chrome node. It checks that OAuth config exists and that the refresh token can mint an access token. The JSON report includes only status fields such as `ok`, `configured`, `tokenSource`, `expiresAt`, and check messages; it does not print the access token, refresh token, or client secret.

| Check | Meaning |
| --- | --- |
| `oauth-config` | `oauth.clientId` plus `oauth.refreshToken`, or a cached access token, is present. |
| `oauth-token` | The cached access token is still valid, or the refresh token minted a new access token. |
| `meet-spaces-get` | Optional `--meeting` check resolved an existing Meet space. |
| `meet-spaces-create` | Optional `--create-space` check created a new Meet space. |

To also prove Google Meet API enablement and the `spaces.create` scope, run the side-effecting create check `openclaw googlemeet doctor --oauth --create-space --json`; `--create-space` creates a throwaway Meet URL. To prove read access for an existing space, run `openclaw googlemeet doctor --oauth --meeting <url> --json`. A `403` from these checks usually means the Google Meet REST API is disabled, the consented refresh token is missing the required scope, or the Google account cannot access that Meet space; a refresh-token error means rerun `openclaw googlemeet auth login --json` and store the new `oauth` block.

These environment variables are accepted as fallbacks (each `OPENCLAW_GOOGLE_MEET_*` name also accepts the same name without the `OPENCLAW_` prefix):

- `OPENCLAW_GOOGLE_MEET_CLIENT_ID` or `GOOGLE_MEET_CLIENT_ID`
- `OPENCLAW_GOOGLE_MEET_CLIENT_SECRET` or `GOOGLE_MEET_CLIENT_SECRET`
- `OPENCLAW_GOOGLE_MEET_REFRESH_TOKEN` or `GOOGLE_MEET_REFRESH_TOKEN`
- `OPENCLAW_GOOGLE_MEET_ACCESS_TOKEN` or `GOOGLE_MEET_ACCESS_TOKEN`
- `OPENCLAW_GOOGLE_MEET_ACCESS_TOKEN_EXPIRES_AT` or `GOOGLE_MEET_ACCESS_TOKEN_EXPIRES_AT`
- `OPENCLAW_GOOGLE_MEET_DEFAULT_MEETING` or `GOOGLE_MEET_DEFAULT_MEETING`
- `OPENCLAW_GOOGLE_MEET_PREVIEW_ACK` or `GOOGLE_MEET_PREVIEW_ACK`

## Config block

The common Chrome agent path only needs the plugin enabled, BlackHole, SoX, a realtime transcription provider key, and a configured OpenClaw TTS provider. OpenAI is the default transcription provider; set `realtime.voiceProvider` to `"google"` and `realtime.model` to use Google Gemini Live for `bidi` mode without changing the default agent-mode transcription provider. The plugin config goes under `plugins.entries.google-meet.config` (an empty `config: {}` accepts all defaults).

Source-documented config defaults (verbatim values): `defaultTransport: "chrome"`; `defaultMode: "agent"` (`"realtime"` is accepted only as a legacy compatibility alias for `"agent"`); `chromeNode.node` is an optional node id/name/IP for `chrome-node`; `chrome.audioBackend: "blackhole-2ch"`; `chrome.guestName: "OpenClaw Agent"`; `chrome.autoJoin: true`; `chrome.reuseExistingTab: true`; `chrome.waitForInCallMs: 20000`; `chrome.audioFormat: "pcm16-24khz"` (use `"g711-ulaw-8khz"` only for legacy/custom command pairs); `chrome.audioBufferBytes: 4096` (half SoX's default 8192-byte buffer; values below SoX's minimum are clamped to 17 bytes). `chrome.audioInputCommand` is a SoX command reading from CoreAudio `BlackHole 2ch` and writing audio in `chrome.audioFormat`; `chrome.audioOutputCommand` is the reverse. `chrome.bargeInInputCommand` is an optional local microphone command writing signed 16-bit little-endian mono PCM for human barge-in detection (currently the Gateway-hosted `chrome` command-pair bridge); `chrome.bargeInRmsThreshold: 650`; `chrome.bargeInPeakThreshold: 2500`; `chrome.bargeInCooldownMs: 900`.

The three `mode` values: `mode: "agent"` (default) transcribes participant speech via the configured realtime transcription provider, sends it to the configured OpenClaw agent in a per-meeting sub-agent session, and speaks the answer back through the normal OpenClaw TTS runtime; `mode: "bidi"` is the fallback direct bidirectional realtime model mode where the realtime voice provider answers directly and may call `openclaw_agent_consult`; `mode: "transcribe"` is observe-only without the talk-back bridge. The `realtime.*` surface: `realtime.provider: "openai"` (compatibility fallback when the scoped fields are unset); `realtime.transcriptionProvider: "openai"` (used by `agent` mode); `realtime.voiceProvider` (used by `bidi` mode — set `"google"` for Gemini Live while keeping agent-mode transcription on OpenAI); `realtime.toolPolicy: "safe-read-only"`; `realtime.instructions`; `realtime.introMessage` (short spoken readiness check; set to `""` to join silently); `realtime.agentId` (optional OpenClaw agent id for `openclaw_agent_consult`; defaults to `main`).

An optional-overrides example showing the Gemini Live `bidi` voice path alongside agent-mode transcription on OpenAI:

```json5
{
  defaults: {
    meeting: "https://meet.google.com/abc-defg-hij",
  },
  browser: {
    defaultProfile: "openclaw",
  },
  chrome: {
    guestName: "OpenClaw Agent",
    waitForInCallMs: 30000,
  },
  chromeNode: {
    node: "parallels-macos",
  },
  defaultMode: "agent",
  realtime: {
    provider: "openai",
    transcriptionProvider: "openai",
    voiceProvider: "google",
    model: "gemini-2.5-flash-native-audio-preview-12-2025",
    agentId: "jay",
    toolPolicy: "owner",
    introMessage: "Say exactly: I'm here.",
    providers: {
      google: {
        speakerVoice: "Kore",
      },
    },
  },
}
```

For ElevenLabs as both the agent-mode listening (transcription) and speaking (TTS) provider, the persistent Meet voice comes from `messages.tts.providers.elevenlabs.speakerVoiceId`, with `realtime.transcriptionProvider: "elevenlabs"` (e.g. `modelId: "scribe_v2_realtime"`, `audioFormat: "ulaw_8000"`, `sampleRate: 8000`, `commitStrategy: "vad"`) under the plugin config. Per-reply `[[tts:speakerVoiceId=... model=eleven_v3]]` directives are possible when TTS model overrides are enabled, but config is the deterministic default for meetings. A Twilio-only config sets `defaultTransport: "twilio"`, `twilio.defaultDialInNumber`/`twilio.defaultPin`, and `voiceCall.gatewayUrl`; `voiceCall.enabled` defaults to `true` and, with Twilio transport, delegates the PSTN call, DTMF, and intro greeting to the Voice Call plugin (if `voice-call` is not enabled, Google Meet can validate and record the dial plan but cannot place the call).

**Source**: OpenClaw documentation — `plugins/google-meet` (mirror `inbox/openclaw_docs/plugins/google-meet.md`), `OAuth and preflight` + `Config` sections
**Last Updated**: 2026-06-22
**Status**: Active
