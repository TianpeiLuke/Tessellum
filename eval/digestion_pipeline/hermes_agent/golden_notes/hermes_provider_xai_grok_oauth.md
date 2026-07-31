---
tags:
  - resource
  - documentation
  - hermes_agent
  - providers
  - oauth
keywords:
  - xAI Grok OAuth
  - SuperGrok
  - X Premium+
  - browser OAuth PKCE
  - codex_responses transport
  - no XAI_API_KEY
  - direct-to-xAI tools
topics:
  - Hermes Agent
  - Providers & Setup
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/xai-grok-oauth
access_control_group: ["general"]
---

# Hermes Agent — xAI Grok OAuth (SuperGrok / X Premium+)

## Overview

This is the setup procedure for using **xAI Grok models in Hermes Agent through a browser-based OAuth login** — no `XAI_API_KEY` required. Instead of pasting an API key, you authenticate once against [accounts.x.ai](https://accounts.x.ai) using either a **SuperGrok subscription** or an **X Premium+ subscription** (xAI automatically links a Premium+ X account's subscription status to your xAI session, so both paths behave identically). After the first login, Hermes refreshes the access token in the background and you stay signed in until you log out or revoke access.

Two implementation facts shape everything else on the page. First, the transport **reuses the `codex_responses` adapter** because xAI exposes a Responses-style endpoint (`https://api.x.ai/v1`) — so reasoning, tool-calling, streaming, and prompt caching work with no adapter changes. Second, the **same OAuth bearer token is reused by every direct-to-xAI surface** — TTS, image generation, video generation, transcription, and X (Twitter) search — so a single login covers all of them. The provider ID is `xai-oauth` and the default model is `grok-build-0.1`. Where this page touches remote-host login, it links DOWN to [OAuth over SSH / Remote Hosts](hermes_oauth_over_ssh.md); the media tools and the env-var master table are owned by other guides and are referenced rather than duplicated here.

## Overview Table

| Item | Value |
|------|-------|
| Provider ID | `xai-oauth` |
| Display name | xAI Grok OAuth (SuperGrok / X Premium+) |
| Auth type | Browser OAuth 2.0 PKCE (loopback callback) |
| Transport | xAI Responses API (`codex_responses`) |
| Default model | `grok-build-0.1` |
| Endpoint | `https://api.x.ai/v1` |
| Auth server | `https://accounts.x.ai` |
| Requires env var | No (`XAI_API_KEY` is **not** used for this provider) |
| Subscription | [SuperGrok](https://x.ai/grok) or [X Premium+](https://x.com/i/premium_sign_up) |

## Prerequisites

- Python 3.9+
- Hermes Agent installed
- An active **SuperGrok** subscription on your xAI account, **or** an **X Premium+** subscription on the X account you sign in with (xAI links the subscription automatically)
- A browser on the local machine (or use `--no-browser` for remote sessions)

**Tier caution.** xAI's backend enforces its own allowlist on the OAuth API surface and has been seen to reject standard SuperGrok subscribers with `HTTP 403` even when the in-app subscription is active. If OAuth login succeeds in the browser but inference returns 403, set `XAI_API_KEY` and switch to the API-key path (`provider: xai`) — that surface is not subject to the same gating today.

## Quick Start

```bash
# Launch the provider and model picker
hermes model
# → Select "xAI Grok OAuth (SuperGrok / X Premium+)" from the provider list
# → Hermes opens your browser to accounts.x.ai
# → Approve access in the browser
# → Pick a model (grok-build-0.1 is at the top)
# → Start chatting

hermes
```

After the first login, credentials are stored under `~/.hermes/auth.json` and refreshed automatically before they expire.

## Logging In Manually

Trigger a login directly, without going through the model picker, with `hermes auth add xai-oauth`.

**Remote / headless sessions.** On servers, containers, or SSH sessions with no local browser, Hermes detects the remote environment and prints the authorization URL instead of opening a browser. The catch: the loopback listener still runs on the *remote* machine at `127.0.0.1:56121`, so the xAI redirect must reach that listener. Opening the URL on your laptop fails (`Could not establish connection`) unless you forward the port:

```bash
# In a separate terminal on your local machine:
ssh -N -L 56121:127.0.0.1:56121 user@remote-host

# Then in your SSH session on the remote machine:
hermes auth add xai-oauth --no-browser
# Open the printed authorize URL in your local browser.
```

Through a jump box / bastion, add `-J jump-user@jump-host`. See [OAuth over SSH / Remote Hosts](hermes_oauth_over_ssh.md) for the full step-by-step (ProxyJump chains, mosh/tmux, ControlMaster gotchas).

**Browser-only remotes (Cloud Shell, Codespaces, EC2 Instance Connect).** When you have no regular SSH client — GCP Cloud Shell, GitHub Codespaces, AWS EC2 Instance Connect, Gitpod — the `ssh -L` recipe is unavailable. Use `--manual-paste`: Hermes skips the loopback listener and lets you paste the failed callback URL straight from the browser:

```bash
hermes auth add xai-oauth --manual-paste
# Or via the model picker:
hermes model --manual-paste
```

If the consent page renders the authorization code directly (xAI's current behavior on browser-based consoles) instead of redirecting to `127.0.0.1:56121/callback`, paste **just the bare code value** at the `Callback URL:` prompt — Hermes accepts the full URL, a bare `?code=...&state=...` query fragment, or a bare code interchangeably.

## How the Login Works

1. Hermes opens your browser to `accounts.x.ai`.
2. You sign in (or confirm an existing session) and approve access.
3. xAI redirects back to Hermes and the tokens are saved to `~/.hermes/auth.json`.
4. From then on, Hermes refreshes the access token in the background — you stay signed in until you `hermes auth remove xai-oauth` or revoke access in your xAI account settings.

## Checking Login Status

Run `hermes doctor`; its `◆ Auth Providers` section shows the current state of every provider, including `xai-oauth`.

## Switching Models

Run `hermes model`, select "xAI Grok OAuth (SuperGrok / X Premium+)", and pick from the model list (`grok-build-0.1` is pinned to the top). Or set the model directly:

```bash
hermes config set model.default grok-build-0.1
hermes config set model.provider xai-oauth
```

## Configuration Reference

After login, `~/.hermes/config.yaml` will contain:

```yaml
model:
  default: grok-build-0.1
  provider: xai-oauth
  base_url: https://api.x.ai/v1
```

**Provider aliases.** All of the following resolve to `xai-oauth`: `xai-oauth` (canonical), `grok-oauth`, `x-ai-oauth`, and `xai-grok-oauth` — usable as `hermes --provider <alias>`. (The full per-provider config surface lives in the model/provider config docs.)

## Direct-to-xAI Tools (TTS / Image / Video / Transcription / X Search)

Once you're logged in via OAuth, every direct-to-xAI tool **reuses the same bearer token automatically** — no separate setup unless you prefer an API key. Pick a backend per tool with `hermes tools` → choose "xAI TTS", "xAI Grok Imagine (image)", "xAI Grok Imagine" (video), or "xAI Grok OAuth" for X search. If OAuth tokens are already stored, the picker confirms it and skips the credential prompt; if neither OAuth nor `XAI_API_KEY` is set, it offers a 3-choice menu (OAuth login / paste API key / skip).

Two defaults to know: **video generation is off by default** (enable `🎬 Video Generation` in `hermes tools` before the agent can call `video_generate`), and **X search auto-enables whenever xAI credentials are present** — the `x_search` toolset routes through xAI's built-in `x_search` Responses API, works with either the OAuth token or `XAI_API_KEY`, and **prefers OAuth when both are configured** (using subscription quota instead of API spend). The voice/TTS and X-search feature surfaces are documented in their own notes.

**Models.** The chat catalog is derived live from the on-disk `models.dev` cache (new xAI releases appear automatically once it refreshes), with `grok-build-0.1` always pinned to the top of the list:

| Tool | Model | Notes |
|------|-------|-------|
| Chat | `grok-build-0.1` | Default; auto-selected when you log in via OAuth |
| Chat | `grok-4.3` | Previous default |
| Chat | `grok-4.20-0309-reasoning` | Reasoning variant |
| Chat | `grok-4.20-0309-non-reasoning` | Non-reasoning variant |
| Chat | `grok-4.20-multi-agent-0309` | Multi-agent variant |
| Image | `grok-imagine-image` | Default; ~5–10 s |
| Image | `grok-imagine-image-quality` | Higher fidelity; ~10–20 s |
| Video | `grok-imagine-video` | Text-to-video |
| Video | `grok-imagine-video-1.5-preview` | Image-to-video (dated alias `…-2026-05-30`) |
| TTS | (default voice) | xAI `/v1/tts` endpoint |

## Environment Variables

| Variable | Effect |
|----------|--------|
| `XAI_BASE_URL` | Override the default `https://api.x.ai/v1` endpoint (rarely needed). |

To select xAI as the active provider, set `model.provider: xai-oauth` in `config.yaml` (use `hermes setup` for the guided flow) or pass `--provider xai-oauth` for a single invocation. The complete env-var catalog lives in the environment-variables reference.

## Troubleshooting

- **Token expired — not re-logging in automatically.** Hermes refreshes before each session and reactively on a 401. If refresh fails with `invalid_grant` (revoked refresh token or rotated account), Hermes marks the refresh token dead, quarantines it locally so subsequent calls skip the doomed refresh, and surfaces a single "re-authentication required" message. **Fix:** run `hermes auth add xai-oauth` again — the quarantine clears on the next successful exchange.
- **Authorization timed out.** The loopback listener has a finite expiry (default 180 s). **Fix:** re-run `hermes auth add xai-oauth` (or `hermes model`).
- **State mismatch (possible CSRF).** The `state` returned by the authorization server doesn't match what Hermes sent. **Fix:** re-run the login; if it persists, check for a proxy or redirect modifying the OAuth response.
- **Logging in from a remote server.** The loopback callback still binds `127.0.0.1:56121` on the remote host; forward it with `ssh -N -L 56121:127.0.0.1:56121 user@remote-host`, then `hermes auth add xai-oauth --no-browser`. Full walkthrough: [OAuth over SSH / Remote Hosts](hermes_oauth_over_ssh.md).
- **HTTP 403 after a successful login (tier / entitlement).** OAuth completed and tokens are saved, but inference/refresh returns `HTTP 403`. This is **not** a stale-token problem; xAI restricts OAuth API access to specific SuperGrok tiers. **Fix:** set `XAI_API_KEY` and switch to the API-key path (`export XAI_API_KEY=xai-…` then `hermes config set model.provider xai`), or upgrade your subscription.
- **"No xAI credentials found" at runtime.** No `xai-oauth` entry and no `XAI_API_KEY`. **Fix:** run `hermes model` and pick the xAI Grok OAuth provider, or `hermes auth add xai-oauth`.

## Logging Out

Run `hermes auth logout xai-oauth` to remove all stored xAI Grok OAuth credentials. This clears both the singleton OAuth entry in `auth.json` and any credential-pool rows for `xai-oauth`. Use `hermes auth remove xai-oauth <index|id|label>` to drop a single pool entry (run `hermes auth list xai-oauth` to see them).

**Source**: https://hermes-agent.nousresearch.com/docs/guides/xai-grok-oauth
**Last Updated**: 2026-06-19
**Status**: Active
