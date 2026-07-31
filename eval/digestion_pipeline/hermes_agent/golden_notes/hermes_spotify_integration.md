---
tags:
  - resource
  - documentation
  - hermes_agent
  - spotify
  - oauth
keywords:
  - spotify integration
  - hermes auth spotify
  - PKCE OAuth
  - spotify connect device
  - spotify tools
  - spotify cron
topics:
  - Hermes Agent
  - Spotify
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/spotify
access_control_group: ["general"]
---

# Hermes Agent — Spotify Integration

## Overview

Spotify integration is the **opt-in toolset that lets the Hermes agent control a user's Spotify account directly** — playback, queue, search, playlists, saved tracks/albums, and listening history — through Spotify's official Web API using PKCE OAuth. It is a procedure: register a personal Spotify developer app, run `hermes auth spotify` once per machine to log in, and the agent gains 7 Spotify tools it picks between conversationally. Tokens are stored locally in `~/.hermes/auth.json` and refreshed automatically on a 401, so you only log in once unless you revoke the app or sign out.

Unlike Hermes' built-in OAuth integrations (Google, GitHub Copilot, Codex), Spotify requires **every user to register their own lightweight developer app** — Spotify does not let third parties ship a public OAuth app that anyone can use. It takes about two minutes, and `hermes auth spotify` walks you through the app registration inline. PKCE does not use a client secret, so only the Client ID is needed. Spotify auth is independent of the LLM provider — approving it does not change the active inference provider.

## Prerequisites

- A **Spotify account.** Free works for search, playlist, library, and activity tools. **Premium is required for playback control** (play, pause, skip, seek, volume, queue add, transfer).
- Hermes Agent installed and running.
- For playback tools, an **active Spotify Connect device** — the Spotify app must be open on at least one device (phone, desktop, web player, speaker) so the Web API has something to control. If nothing is active you get a `403 Forbidden` with a "no active device" message; open Spotify on any device and retry.

## Setup

Two paths register and authenticate the toolset; both gate the 7 tools behind enabling Spotify so users who don't want them don't ship extra tool schemas on every API call.

**One-shot (`hermes tools` or first-run setup):** run `hermes tools`, scroll to `🎵 Spotify`, press space to toggle it on, then `s` to save (the same toggle appears in the first-run `hermes setup` / `hermes setup tools` flow). Hermes drops straight into the OAuth flow — if you don't have a Spotify app yet, it walks you through creating one inline, and on finish the toolset is enabled AND authenticated in one pass.

**Two-step (separate or re-auth):** first toggle `🎵 Spotify` on in `hermes tools` and dismiss the inline wizard with Ctrl+C (the toolset stays on; only auth is deferred), then run the login wizard separately:

```bash
hermes auth spotify
```

If no `HERMES_SPOTIFY_CLIENT_ID` is set, Hermes walks you through app registration inline: it opens `https://developer.spotify.com/dashboard`, prints the exact values to paste into Spotify's "Create app" form, prompts for the Client ID you get back, saves it to `~/.hermes/.env` so future runs skip this step, and continues straight into the OAuth consent flow. After you approve, tokens are written under `providers.spotify` in `~/.hermes/auth.json`.

### Creating the Spotify app (what the wizard asks for)

When the dashboard opens, click **Create app** and fill in:

| Field | Value |
|-------|-------|
| App name | anything (e.g. `hermes-agent`) |
| App description | anything (e.g. `personal Hermes integration`) |
| Website | leave blank |
| Redirect URI | `http://127.0.0.1:43827/spotify/callback` |
| Which API/SDKs? | check **Web API** |

Agree to the terms and click **Save**, then on the next page click **Settings** → copy the **Client ID** and paste it into the Hermes prompt. That Client ID is the only value Hermes needs — PKCE doesn't use a client secret.

### Running over SSH / headless

If `SSH_CLIENT` or `SSH_TTY` is set, Hermes skips the automatic browser open during both the wizard and the OAuth step. Copy the dashboard URL and the authorization URL Hermes prints, open them in a browser on your local machine, and proceed normally — the local HTTP listener still runs on the remote host on port `43827`. A laptop browser can't reach the remote loopback without an SSH local-forward:

```bash
ssh -N -L 43827:127.0.0.1:43827 user@remote-host
```

For jump-box / bastion setups and other gotchas (mosh, tmux, port conflicts), the source link-outs to a dedicated OAuth-over-SSH guide.

## Verify

```bash
hermes auth status spotify
```

Shows whether tokens are present and when the access token expires. Refresh is automatic: when any Spotify API call returns 401, the client exchanges the refresh token and retries once. Refresh tokens persist across Hermes restarts, so you only re-auth if you revoke the app in your Spotify account settings or run `hermes auth logout spotify`.

## Using it — the 7 tools

Once logged in, the agent has access to 7 Spotify tools. You talk to the agent naturally ("play some miles davis", "what am I listening to", "transfer playback to my kitchen speaker") and it picks the right tool and action. For best behavior the agent loads a companion skill teaching canonical usage patterns (single-search-then-play, when not to preflight `get_state`). All playback-mutating actions accept an optional `device_id` to target a specific device; if omitted, Spotify uses the currently active device.

- **`spotify_playback`** — control and inspect playback plus fetch history: `get_state` (full state), `get_currently_playing` (current track; returns empty on 204), `play` / `pause` / `next` / `previous` / `seek` / `set_repeat` / `set_shuffle` / `set_volume`, and `recently_played`.
- **`spotify_devices`** — `list` (every Spotify Connect device) and `transfer` (move playback to `device_id`, optional `play: true`).
- **`spotify_queue`** — `get` (queued tracks) and `add` (append a `uri`).
- **`spotify_search`** — search the catalog; `query` required, optional `types` (`track`/`album`/`artist`/`playlist`/`show`/`episode`), `limit`, `offset`, `market`.
- **`spotify_playlists`** — `list` / `get` / `create` / `add_items` / `remove_items` / `update_details`.
- **`spotify_albums`** — `get` (metadata) and `tracks` (track list).
- **`spotify_library`** — unified saved tracks/albums via `kind` = `tracks` or `albums`, with `list` / `save` / `remove`.

**Home Assistant-managed speakers:** if Home Assistant manages Spotify-Connect-capable speakers (Sonos, Echo, Nest, etc.), they appear in `spotify_devices list` automatically whenever Spotify can see them — no Home Assistant ↔ Spotify bridge is needed because Spotify handles device routing natively. Ask Hermes to transfer by the speaker's display name, or pass the exact `device_id` to `spotify_devices transfer` when scripting.

### Feature matrix: Free vs Premium

Read-only tools work on Free accounts; anything that mutates playback or the queue requires Premium.

| Works on Free | Premium required |
|---------------|------------------|
| `spotify_search` (all) | `spotify_playback` — play, pause, next, previous, seek, set_repeat, set_shuffle, set_volume |
| `spotify_playback` — get_state, get_currently_playing, recently_played | `spotify_queue` — add |
| `spotify_devices` — list | `spotify_devices` — transfer |
| `spotify_queue` — get | |
| `spotify_playlists` (all) | |
| `spotify_albums` (all) | |
| `spotify_library` (all) | |

## Scheduling: Spotify + cron

Because Spotify tools are regular Hermes tools, a cron job running in a Hermes session can trigger playback on any schedule — no new code needed. A natural-language prompt is scheduled with `hermes cron add`:

```bash
hermes cron add \
  --name "morning-commute" \
  "0 7 * * 1-5" \
  "Transfer playback to my kitchen speaker and start my 'Morning Commute' playlist. Volume to 40. Shuffle on."
```

At 7am every weekday, cron spins up a headless Hermes session; the agent reads the prompt, calls `spotify_devices list` to find "kitchen speaker" by name, then `spotify_devices transfer` → `spotify_playback set_volume` → `spotify_playback set_shuffle` → `spotify_search` + `spotify_playback play`. A wind-down job (`"30 22 * * *"`) can pause and lower the volume. Gotchas: an active device must exist when the cron fires (target an always-on speaker, not your phone); Premium is required for any playback-mutating action; the cron agent inherits your active toolsets (Spotify must be enabled in `hermes tools`); and cron jobs run with `skip_memory=True` so they don't write to your memory store.

## Sign out

`hermes auth logout spotify` removes tokens from `~/.hermes/auth.json`. To also clear the app config, delete `HERMES_SPOTIFY_CLIENT_ID` (and `HERMES_SPOTIFY_REDIRECT_URI` if set) from `~/.hermes/.env`, or run the wizard again. To revoke the app on Spotify's side, visit "Apps connected to your account" in Spotify settings and click REMOVE ACCESS.

## Advanced: custom scopes / client ID / redirect URI

By default Hermes requests the scopes needed for every shipped tool. Restrict them with `hermes auth spotify --scope "user-read-playback-state user-modify-playback-state playlist-read-private"` — but requesting fewer scopes than a tool needs makes that tool's calls fail with 403. Override the app identity with `hermes auth spotify --client-id <id> --redirect-uri http://localhost:3000/callback`, or set `HERMES_SPOTIFY_CLIENT_ID` / `HERMES_SPOTIFY_REDIRECT_URI` permanently in `~/.hermes/.env`. The redirect URI must be allow-listed in your Spotify app's settings; the default `http://127.0.0.1:43827/spotify/callback` works for almost everyone — only change it if port 43827 is taken.

## Troubleshooting

- **`403 Forbidden — No active device found`** — open Spotify on a device, start any track briefly to register it, and retry; `spotify_devices list` shows what's visible.
- **`403 Forbidden — Premium required`** — a Free account tried a playback-mutating action (see the feature matrix).
- **`204 No Content` on `get_currently_playing`** — nothing is playing on any device; Spotify's normal response, surfaced as an empty result (`is_playing: false`), not an error.
- **`INVALID_CLIENT: Invalid redirect URI`** — the app-settings redirect URI doesn't match Hermes' (default `http://127.0.0.1:43827/spotify/callback`); add it to the app's allowed URIs or set `HERMES_SPOTIFY_REDIRECT_URI`.
- **`429 Too Many Requests`** — Spotify's rate limit; wait a minute and retry. A tight script loop trips this; the quota resets roughly every 30 seconds.
- **`401 Unauthorized` keeps coming back** — the refresh token was revoked (app removed or deleted); run `hermes auth spotify` again.

## Where things live

| File | Contents |
|------|----------|
| `~/.hermes/auth.json` → `providers.spotify` | access token, refresh token, expiry, scope, redirect URI |
| `~/.hermes/.env` | `HERMES_SPOTIFY_CLIENT_ID`, optional `HERMES_SPOTIFY_REDIRECT_URI` |
| Spotify app | owned by you at developer.spotify.com/dashboard; contains the Client ID and the redirect URI allow-list |

**Source**: `inbox/hermes_agent_docs/user-guide/features/spotify.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/spotify
**Last Updated**: 2026-06-19
**Status**: Active
