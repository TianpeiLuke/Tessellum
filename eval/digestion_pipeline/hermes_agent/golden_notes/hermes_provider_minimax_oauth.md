---
tags:
  - resource
  - documentation
  - hermes_agent
  - provider_setup
  - oauth
keywords:
  - MiniMax OAuth
  - minimax-oauth provider
  - anthropic_messages transport
  - PKCE browser login
  - MiniMax-M2.7
  - region endpoints
topics:
  - Hermes Agent
  - Providers & Setup
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/minimax-oauth
access_control_group: ["general"]
---

# Hermes Agent — MiniMax via Browser OAuth

## Overview

This guide is the **task script** for connecting Hermes Agent to **MiniMax** without an API key, using a browser-based OAuth login. The `minimax-oauth` provider reuses the **same credentials as the [MiniMax portal](https://www.minimax.io)** — you log in once and Hermes refreshes the session automatically before each run, so there is no `MINIMAX_API_KEY` and no credit card. Under the hood the transport reuses the existing `anthropic_messages` adapter (MiniMax exposes an Anthropic Messages-compatible endpoint at `/anthropic`), which means all of Hermes' tool-calling, streaming, and long-context features work with **no adapter changes**.

At a glance, the provider serves the `MiniMax-M2.7` and `MiniMax-M2.7-highspeed` models (each up to 200,000 tokens of context), supports a **global** (`minimax.io`) and a **China** region split, and stores its tokens under the `minimax-oauth` key in `~/.hermes/auth.json`. This note covers the picker and manual login paths, the PKCE OAuth flow, region/alias configuration, the (non-)use of env vars, the model list, and the standard re-auth/CSRF/timeout troubleshooting set. Remote-host login completion is the cross-cutting concern owned by [OAuth over SSH](hermes_oauth_over_ssh.md); the `config.yaml` provider/model reference lives in [aux & provider config](hermes_model_aux_provider_config.md).

| Item | Value |
|------|-------|
| Provider ID | `minimax-oauth` |
| Display name | MiniMax (OAuth) |
| Auth type | Browser OAuth (PKCE redirect flow) |
| Transport | Anthropic Messages-compatible (`anthropic_messages`) |
| Models | `MiniMax-M2.7`, `MiniMax-M2.7-highspeed` |
| Global endpoint | `https://api.minimax.io/anthropic` |
| China endpoint | `https://api.minimaxi.com/anthropic` |
| Requires env var | No (`MINIMAX_API_KEY` is **not** used) |

## Prerequisites

- Python 3.9+ and Hermes Agent installed.
- A MiniMax account at [minimax.io](https://www.minimax.io) (global) or [minimaxi.com](https://www.minimaxi.com) (China).
- A browser available on the local machine — or use `--no-browser` for remote/headless sessions (see [OAuth over SSH](hermes_oauth_over_ssh.md)).

## Quick Start

The fastest path is the model picker, which combines login and model selection:

```bash
# Launch the provider and model picker
hermes model
# → Select "MiniMax (OAuth)" from the provider list
# → Hermes opens your browser to the MiniMax authorization page
# → Approve access in the browser
# → Select a model (MiniMax-M2.7 or MiniMax-M2.7-highspeed)
# → Start chatting

hermes
```

After the first login, credentials are stored under `~/.hermes/auth.json` and are refreshed automatically before each session.

## Logging In Manually

You can trigger a login without going through the model picker:

```bash
hermes auth add minimax-oauth
```

**China region.** If your account is on the China platform (`minimaxi.com`), use the API-key-based `minimax-cn` provider instead — `minimax-cn` is registered with `auth_type="api_key"` only (no OAuth flow). Configure `MINIMAX_CN_API_KEY` (and optionally `MINIMAX_CN_BASE_URL`) directly, e.g. `echo 'MINIMAX_CN_API_KEY=your-key' >> ~/.hermes/.env`.

**Remote / headless sessions.** On servers or containers where no browser is available, add `--no-browser`: Hermes prints the verification URL and user code, which you open on any device and enter when prompted.

```bash
hermes auth add minimax-oauth --no-browser
```

## The OAuth Flow

Hermes implements a **PKCE** browser OAuth flow against the MiniMax OAuth endpoints:

1. Hermes generates a PKCE verifier / challenge pair and a random `state` value.
2. It POSTs to `{base_url}/oauth/code` with the challenge and receives a `user_code` and `verification_uri`.
3. Your browser opens `verification_uri`. If prompted, enter the `user_code`.
4. Hermes polls `{base_url}/oauth/token` until the token arrives (or the deadline passes).
5. Tokens (`access_token`, `refresh_token`, expiry) are saved to `~/.hermes/auth.json` under the `minimax-oauth` key.

Token refresh (the standard OAuth `refresh_token` grant) runs automatically at each session start whenever the access token is within **60 seconds** of expiry. The verifier/challenge/state machinery is shared with the other PKCE OAuth providers (see the parallel [xAI Grok OAuth](hermes_provider_xai_grok_oauth.md) flow and the SSH-tunnel completion in [OAuth over SSH](hermes_oauth_over_ssh.md)).

## Checking Login Status

```bash
hermes doctor
```

The `◆ Auth Providers` section reports the MiniMax login state and region — `✓ MiniMax OAuth  (logged in, region=global)` when authenticated, or `⚠ MiniMax OAuth  (not logged in)` otherwise.

## Switching Models, Configuration & Aliases

Re-run `hermes model`, select **MiniMax (OAuth)**, and pick from the model list — or set the model directly:

```bash
hermes config set model.default MiniMax-M2.7
hermes config set model.provider minimax-oauth
```

After login, `~/.hermes/config.yaml` contains entries similar to:

```yaml
model:
  default: MiniMax-M2.7
  provider: minimax-oauth
  base_url: https://api.minimax.io/anthropic
```

**Region endpoints** map a provider ID to its portal + inference endpoint: `minimax-oauth` (global) uses `https://api.minimax.io` → `https://api.minimax.io/anthropic`, while `minimax-cn` (China) uses `https://api.minimaxi.com` → `https://api.minimaxi.com/anthropic`. **Provider aliases** — `minimax-portal`, `minimax-global`, and the underscore form `minimax_oauth` — all resolve to the canonical `minimax-oauth` (e.g. `hermes --provider minimax-portal`). The full config-key reference lives in [aux & provider config](hermes_model_aux_provider_config.md).

## Environment Variables & Models

The `minimax-oauth` provider does **not** use `MINIMAX_API_KEY` or `MINIMAX_BASE_URL` — those belong to the API-key-based `minimax` and `minimax-cn` providers only. To make `minimax-oauth` the active provider, set `model.provider: minimax-oauth` in `config.yaml` (use `hermes setup` for the guided flow) or pass `--provider minimax-oauth` for a single invocation.

| Variable | Effect |
|----------|--------|
| `MINIMAX_API_KEY` | Used by `minimax` provider only — ignored for `minimax-oauth` |
| `MINIMAX_CN_API_KEY` | Used by `minimax-cn` provider only — ignored for `minimax-oauth` |

Two models are available, each supporting up to **200,000 tokens** of context. `MiniMax-M2.7` is best for long-context reasoning and complex tool-calling; `MiniMax-M2.7-highspeed` is lower-latency for lighter tasks and auxiliary calls — and is also used automatically as the **auxiliary model** for vision and delegation when `minimax-oauth` is the primary provider (see [aux & provider config](hermes_model_aux_provider_config.md)).

## Troubleshooting & Logging Out

- **Token expired — not re-logging in automatically.** Hermes refreshes the token at each session start if it is within 60s of expiry; an already-expired token refreshes on the next request. If refresh fails with `refresh_token_reused` or `invalid_grant` (HTTP 4xx, revoked grant, etc.), Hermes marks the refresh token **dead**, quarantines it locally so it does not keep replaying the doomed exchange, and surfaces a single "re-authentication required" message. **Fix:** run `hermes auth add minimax-oauth` again — the quarantine clears on the next successful exchange.
- **Authorization timed out.** The device-code flow has a finite expiry window. **Fix:** re-run `hermes auth add minimax-oauth` (or `hermes model`); the flow starts fresh.
- **State mismatch (possible CSRF).** Hermes detected that the returned `state` does not match what it sent. **Fix:** re-run the login; if it persists, check for a proxy or redirect modifying the OAuth response.
- **Logging in from a remote server.** Use `--no-browser` and open the printed URL on any device — see [OAuth over SSH](hermes_oauth_over_ssh.md).
- **"Not logged into MiniMax OAuth" at runtime.** The auth store has no `minimax-oauth` credentials. **Fix:** run `hermes model` and select MiniMax (OAuth), or `hermes auth add minimax-oauth`.

To remove stored credentials, run `hermes auth remove minimax-oauth`.

**Source**: `inbox/hermes_agent_docs/guides/minimax-oauth.md` · https://hermes-agent.nousresearch.com/docs/guides/minimax-oauth
**Last Updated**: 2026-06-19
**Status**: Active
