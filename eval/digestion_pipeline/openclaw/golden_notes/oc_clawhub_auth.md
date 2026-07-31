---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - auth
keywords:
  - clawhub auth
  - clawhub login
  - clawhub api token
  - clawhub cli login
  - headless token login
  - clawhub device login
  - clawhub config.json token storage
  - clawhub 401 unauthorized revocation
topics:
  - OpenClaw
  - ClawHub Authentication
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/clawhub/auth
access_control_group: ["general"]
---

# OpenClaw — ClawHub Authentication (Web Sign-In, CLI Login, Token Storage, Revocation)

## Overview

This note is the step-by-step procedure for authenticating to **ClawHub**, the OpenClaw registry, mirroring the `clawhub/auth` source page. ClawHub uses **GitHub for web sign-in**, and the CLI authenticates with **ClawHub API tokens** created through that signed-in account. It covers the GitHub web sign-in, the three CLI login flows (default browser callback, headless `--token`, and `--device`), where the API token is stored per operating system (and how to override that path), how to print the stored token for CI, and how to revoke tokens and recover from `401 Unauthorized`.

## Web sign-in

Sign in at [clawhub.ai](https://clawhub.ai) using **GitHub** — ClawHub uses GitHub as its identity provider for web sign-in. The CLI subsequently uses ClawHub API tokens created through that signed-in account, so web sign-in is the prerequisite for obtaining any token.

**Deleted, banned, or disabled accounts cannot complete normal ClawHub sign-in.** If sign-in returns you to a logged-out state, your account may not be in good standing. If your account was banned or disabled, use the [ClawHub appeal form](https://appeals.openclaw.ai/) if you believe this is a mistake.

## CLI login

The default CLI login flow opens your browser:

```bash
clawhub login
clawhub whoami
```

What happens (the source page enumerates these five steps in order):

1. The CLI starts a temporary callback server on `127.0.0.1`.
2. Your browser opens the ClawHub sign-in page.
3. After GitHub sign-in, ClawHub creates an API token.
4. The browser redirects back to the local callback.
5. The CLI stores the token in your ClawHub config file.

`clawhub whoami` confirms the signed-in account after login. If your browser cannot reach the local callback because of **firewall, VPN, or proxy rules**, use the headless token flow described below.

## Headless login

For servers, CI jobs, or terminal-only environments, create a token in the ClawHub web UI and pass it to the CLI:

```bash
clawhub login --token clh_...
```

(ClawHub API tokens carry the `clh_` prefix.) Use this `--token` flow for servers, CI jobs, or terminal-only environments where the browser-callback flow is unavailable.

For remote shells where you can open a browser elsewhere, run:

```bash
clawhub login --device
```

The CLI prints a **one-time code** and waits while you authorize it at `https://clawhub.ai/cli/device`.

## Token storage

After login, the CLI stores the API token in your ClawHub config file. Default config paths by operating system:

- **macOS**: `~/Library/Application Support/clawhub/config.json`
- **Linux/XDG**: `$XDG_CONFIG_HOME/clawhub/config.json` or `~/.config/clawhub/config.json`
- **Windows**: `%APPDATA%\clawhub\config.json`

Override the config-file path with the `CLAWHUB_CONFIG_PATH` environment variable:

```bash
export CLAWHUB_CONFIG_PATH=/path/to/config.json
```

Print the stored token (for CI setup — e.g., to copy it into a CI secret) with:

```bash
clawhub token
```

## Revocation

You can revoke API tokens in the ClawHub web UI. **Revoked, invalid, or missing tokens return `401 Unauthorized`.** To recover from a `401`, sign in again with `clawhub login` or provide a fresh token with `clawhub login --token`.

**Deleted, banned, or disabled accounts cannot continue using existing API tokens** — account standing gates token use as well as sign-in. If your account was banned or disabled, use the [ClawHub appeal form](https://appeals.openclaw.ai/) if you believe this is a mistake.

**Source**: OpenClaw documentation — `clawhub/auth` (mirror `inbox/openclaw_docs/clawhub/auth.md`)
**Last Updated**: 2026-06-22
**Status**: Active
