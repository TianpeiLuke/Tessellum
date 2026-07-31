---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - config
keywords:
  - openclaw config basics
  - openclaw.json json5 config
  - OPENCLAW_CONFIG_PATH
  - env vars .env loading
  - config env block shellEnv
  - config.apply config.patch recover
  - gateway hot reload
  - workspace .env provider credentials
topics:
  - OpenClaw
  - Config and Environment
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/faq
access_control_group: ["general"]
---

# OpenClaw — FAQ: Config Basics & `.env` Loading

## Overview

This note is the FAQ-level procedure for **where OpenClaw config lives, how to edit it safely, and how environment variables / `.env` files are loaded** — mirroring the **Config basics** and **Env vars and .env loading** accordions of the `help/faq` source page. It answers the day-to-day "where is my config", "do I have to restart", "how do I recover from `config.apply`", and "why did my env vars disappear" questions at the support-FAQ depth. For the full highest→lowest precedence rule and the complete env-var catalog it defers to **[oc_help_environment](oc_help_environment.md)** (the source explicitly links `/help/environment` "for full precedence and sources").

## Config Basics

### Format and Location (`openclaw.json`)

OpenClaw reads an **optional JSON5** config from `$OPENCLAW_CONFIG_PATH` (default: `~/.openclaw/openclaw.json`). If the file is missing, OpenClaw uses "safe-ish defaults", including a default workspace of `~/.openclaw/workspace`. Because the format is JSON5 (not strict JSON), trailing commas and unquoted keys are accepted, as seen throughout the config snippets on this page.

### Do I Have to Restart After Changing Config?

No — the Gateway watches the config file and supports **hot-reload**. The behavior is controlled by `gateway.reload.mode`, whose default is `"hybrid"` (hot-apply safe changes, restart for critical ones). The other supported values are `hot`, `restart`, and `off`.

### Non-Loopback Binds Require Gateway Auth

If you set `gateway.bind: "lan"` (or `"tailnet"`) and nothing listens or the UI says unauthorized, the cause is that **non-loopback binds require a valid gateway auth path**. In practice that means either shared-secret auth (a token or password) or `gateway.auth.mode: "trusted-proxy"` behind a correctly configured identity-aware reverse proxy. A minimal token example:

```json5
{
  gateway: {
    bind: "lan",
    auth: {
      mode: "token",
      token: "replace-me",
    },
  },
}
```

Key behaviors to know: `gateway.remote.token` / `.password` do **not** enable local gateway auth by themselves, and local call paths only fall back to `gateway.remote.*` when `gateway.auth.*` is unset. For password auth, set `gateway.auth.mode: "password"` plus `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`). If `gateway.auth.token`/`gateway.auth.password` is set via SecretRef and unresolved, resolution **fails closed** (no remote fallback masking). Shared-secret Control UI setups authenticate via `connect.params.auth.token` / `connect.params.auth.password`, while identity-bearing modes (Tailscale Serve, `trusted-proxy`) use request headers — avoid putting shared secrets in URLs. With `trusted-proxy`, same-host loopback reverse proxies additionally require `gateway.auth.trustedProxy.allowLoopback = true` and a loopback entry in `gateway.trustedProxies`.

### Why a Token on Localhost

OpenClaw enforces gateway auth **by default, including loopback**. On the normal default path that means token auth: if no explicit auth path is configured, gateway startup resolves to token mode and generates a **runtime-only token for that startup**, so local WebSocket clients must authenticate — this blocks other local processes from calling the Gateway. Configure `gateway.auth.token`, `gateway.auth.password`, `OPENCLAW_GATEWAY_TOKEN`, or `OPENCLAW_GATEWAY_PASSWORD` explicitly when clients need a stable secret across restarts. To open loopback fully, set `gateway.auth.mode: "none"` explicitly. Doctor can mint a token any time: `openclaw doctor --generate-gateway-token`.

### Recovering From `config.apply` (and Avoiding the Clobber)

`config.apply` replaces the **entire config** — sending a partial object removes everything else. OpenClaw guards many accidental clobbers: OpenClaw-owned writes validate the full post-change config before writing; invalid/destructive owned writes are rejected and saved as `openclaw.json.rejected.*`; a bad direct edit makes the Gateway fail closed or skip the reload rather than rewrite `openclaw.json`; and `openclaw doctor --fix` owns repair and can restore last-known-good while saving the clobbered payload as `openclaw.json.clobbered.*`.

To recover, the source prescribes this sequence: check `openclaw logs --follow` for `Invalid config at`, `Config write rejected:`, or `config reload skipped (invalid config)`; inspect the newest `openclaw.json.clobbered.*` or `openclaw.json.rejected.*` beside the active config; run `openclaw config validate` and `openclaw doctor --fix`; copy only the intended keys back with `openclaw config set` or `config.patch`; and if there is no last-known-good or rejected payload, restore from backup or re-run `openclaw doctor` and reconfigure channels/models.

To **avoid** the clobber: use `openclaw config set` for small changes, `openclaw configure` for interactive edits, `config.schema.lookup` first when unsure of an exact path or field shape (it returns a shallow schema node plus immediate child summaries), and `config.patch` for partial RPC edits — reserve `config.apply` for full-config replacement only. Note the agent-facing `gateway` tool still **rejects** writes to `tools.exec.ask` / `tools.exec.security` (including legacy `tools.bash.*` aliases that normalize to the same protected exec paths).

### Other Config Edits (Taglines, Headless Browser)

Disable the CLI taglines via `cli.banner.taglineMode` (`random | default | off`): `off` hides the tagline text but keeps the banner title/version line, `default` always uses `All your chats, one OpenClaw.`, and `random` rotates funny/seasonal taglines (the default). To remove the banner entirely, set the env var `OPENCLAW_HIDE_BANNER=1`. The OpenClaw browser can run headless (default is `false`/headful) via a config option:

```json5
{
  browser: { headless: true },
  agents: {
    defaults: {
      sandbox: { browser: { headless: true } },
    },
  },
}
```

Headless uses the same Chromium engine and works for most automation, but is more likely to trigger anti-bot/CAPTCHA checks on some sites (e.g. X/Twitter). To drive Brave or another Chromium-based browser, set `browser.executablePath` to that binary and restart the Gateway.

## Env Vars and `.env` Loading

### How OpenClaw Loads Environment Variables

OpenClaw reads env vars from the **parent process** (shell, launchd/systemd, CI, etc.) and additionally loads two `.env` files: `.env` from the current working directory, and a global fallback `.env` from `~/.openclaw/.env` (aka `$OPENCLAW_STATE_DIR/.env`). **Neither `.env` file overrides existing env vars.** Provider credential variables are an exception for the workspace `.env`: keys such as `GEMINI_API_KEY`, `XAI_API_KEY`, or `MISTRAL_API_KEY` are **ignored from workspace `.env`** and should live in the process environment, `~/.openclaw/.env`, or the config `env` block. You can also define inline env vars in config (applied only if **missing** from the process env):

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: { GROQ_API_KEY: "gsk-..." },
  },
}
```

The source defers the full precedence and source list to `/help/environment` (see **[oc_help_environment](oc_help_environment.md)**).

### Service Started but Env Vars "Disappeared"

When the Gateway runs as a **service (launchd/systemd)** it won't inherit your shell environment, so keys set only in your interactive shell go missing. Two common fixes: (1) put the missing keys in `~/.openclaw/.env` so they're picked up even when the service doesn't inherit your shell env; or (2) enable shell import (opt-in convenience), which runs your login shell and imports **only missing expected keys** (never overrides):

```json5
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

The env-var equivalents of that block are `OPENCLAW_LOAD_SHELL_ENV=1` and `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`.

### "Shell env: off" Is Not an Error

`openclaw models status` reports whether **shell-env import** is enabled. Seeing "Shell env: off" does **not** mean your env vars are missing — it only means OpenClaw won't load your login shell automatically. If the Gateway runs as a service and won't inherit your shell environment, fix it by one of: (1) putting the token in `~/.openclaw/.env` (e.g. `COPILOT_GITHUB_TOKEN=...`); (2) enabling shell import (`env.shellEnv.enabled: true`); or (3) adding it to the config `env` block (applies only if missing). Then restart the gateway and recheck with `openclaw models status`. Copilot tokens are read from `COPILOT_GITHUB_TOKEN` (also `GH_TOKEN` / `GITHUB_TOKEN`).

**Source**: OpenClaw documentation — `help/faq` (Config basics + Env vars and .env loading; mirror `inbox/openclaw_docs/help/faq.md`)
**Last Updated**: 2026-06-22
**Status**: Active
