---
tags:
  - resource
  - documentation
  - hermes_agent
  - deployment
  - desktop_app
keywords:
  - hermes desktop remote backend
  - hermes dashboard auth gate
  - basic auth username password
  - nous portal oauth
  - electron mirror
  - desktop.log boot logs
topics:
  - Hermes Agent
  - Deployment & Platforms
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/desktop
access_control_group: ["general"]
---

# Hermes Desktop — Connecting to a Remote Backend

## Overview

This is the procedure for pointing the Hermes Desktop app at a Hermes backend running on **another machine** — a VPS, a home server, or a Mini behind Tailscale — instead of the bundled local backend it starts and manages by default. The "remote backend" is a running `hermes dashboard` process on the remote host; the desktop app attaches to it but never starts it for you. The connection has two halves: on the backend you protect the dashboard with an **auth provider**, and in the app you enter the backend's URL and sign in. Binding the dashboard to a non-loopback address automatically engages its auth gate, and the provider you configure is what lets the desktop app through.

## Picking a Provider

Choose the auth provider based on where the backend lives:

- **OAuth (Nous Portal) — preferred for anything reachable beyond your own machine.** Logins are verified against your Nous account, so this is the option suitable for a VPS, a public host, or any remote backend. Register the dashboard with `hermes dashboard register` (or the Portal `/local-dashboards` page) to provision its OAuth client, then sign in from the app with **Sign in with Nous Research**. A self-hosted OIDC provider works the same way if you run your own identity provider.
- **Username/password — local / trusted-network use only.** The simplest option when the backend is on the same trusted LAN or reachable only over a VPN (e.g. Tailscale). It protects a single shared credential with no external identity provider, so **do not use it for a dashboard exposed to the public internet** — reach for OAuth there instead.

The source documents the username/password path in full because it is the quickest to stand up on a trusted network; the OAuth path is covered by the Web Dashboard's "Default provider: Nous Research" section (owned by SP10 — link-out, not duplicated here).

## On the Backend (the Remote Machine)

Set a username and password, then start the dashboard bound to a reachable address. The credentials live in `~/.hermes/.env` (the secrets file, mode 0600):

```bash
# 1. Set the dashboard login credentials.
cat >> ~/.hermes/.env <<'EOF'
HERMES_DASHBOARD_BASIC_AUTH_USERNAME=admin
HERMES_DASHBOARD_BASIC_AUTH_PASSWORD=choose-a-strong-password
# Recommended: a stable signing secret so sessions survive restarts.
# Without it a random key is generated per boot and you'll be logged out
# on every restart.
HERMES_DASHBOARD_BASIC_AUTH_SECRET=$(openssl rand -base64 32)
EOF
chmod 600 ~/.hermes/.env

# 2. Run the dashboard bound to a reachable address. The non-loopback bind
#    engages the auth gate; the username/password provider handles login.
hermes dashboard --no-open --host 0.0.0.0 --port 9119
```

Keep that `hermes dashboard` process running for as long as you want the desktop app to be able to connect — if it stops, the app can no longer reach the backend. Run it under `systemd`, `tmux`, or your process manager of choice so it survives logout and reboots. Running the dashboard as a systemd service? Give the unit `EnvironmentFile=%h/.hermes/.env` so the credentials are in the environment at boot.

Separately, make sure the **gateway is running** on the remote host if you rely on messaging channels — the dashboard backend is what the desktop app talks to, but your Telegram/Discord/Slack gateway sessions are a *different* process that you start and keep running on their own.

Prefer not to keep a plaintext password at rest? Set `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH` to a scrypt hash instead — compute it with:

```bash
python -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('PW'))"
```

The full configuration surface (config.yaml keys, every env var, the rate limiter) is documented by the Web Dashboard's "Username/password provider" section (SP10 — link-out).

> **Security warning (verbatim from source):** The dashboard reads and writes your `.env` (API keys, secrets) and can run agent commands. The **username/password** setup shown above is for a trusted network — never expose a password-protected dashboard directly to the open internet; put it behind a VPN. [Tailscale](https://tailscale.com/) is the clean option: bind to the machine's tailscale IP (`--host <tailscale-ip>`) and use `http://<tailscale-ip>:9119` as the Remote URL so only your tailnet can reach it. To reach a backend over the public internet, use the **OAuth (Nous Portal)** provider instead.

## In the App

**Settings → Gateway → Remote gateway:**

1. **Remote URL** — `http://<backend-host>:9119` (path prefixes like `/hermes` work if you front it with a reverse proxy).
2. **Sign in** — the app detects which provider the backend advertises and adapts the button. For a username/password backend it shows a **Sign in** button that opens a credential form (enter the credentials from step 1). For an OAuth backend it shows **Sign in with `<provider>`** (e.g. *Sign in with Nous Research*), which runs the provider's browser sign-in. Either way the app ends up with an authenticated session against the backend.
3. **Save and reconnect** — switches the desktop shell onto the remote backend. The session refreshes automatically; you stay signed in across restarts when `HERMES_DASHBOARD_BASIC_AUTH_SECRET` is set.

You can also set the backend URL without the UI via the `HERMES_DESKTOP_REMOTE_URL` environment variable before launching the app (it overrides the in-app setting); you still sign in from the Gateway settings panel.

**Per-profile remote hosts:** the remote gateway host is configured per [profile](hermes_desktop_app.md), so each profile can point at its own remote backend (or stay on its local one). Switching profiles switches which remote host the app connects to.

## Remote-Backend Troubleshooting

- **Sign-in fails with 401 / "Invalid credentials"** — the username or password doesn't match the backend's `HERMES_DASHBOARD_BASIC_AUTH_USERNAME` / `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD`. The backend returns the same generic error for an unknown user and a wrong password (no enumeration oracle), so double-check both. Confirm the gate is on:

```bash
curl -s http://<host>:9119/api/status | jq '.auth_required, .auth_providers'
```

It should report `true` and include `"basic"`.

- **No "Sign in" button — it asks for a session token instead** — the backend's username/password provider isn't active. `/api/status` won't list `"basic"` in `auth_providers`. Make sure both the username and a password (or password hash) are set in `~/.hermes/.env` and that the dashboard process actually loaded them.
- **Signed out on every restart** — set `HERMES_DASHBOARD_BASIC_AUTH_SECRET` to a stable value. Without it the token-signing key is regenerated per boot, invalidating all sessions.
- **Connection refused / times out** — the backend bound to `127.0.0.1` (the default) or a firewall/VPN is blocking the port. Bind to `0.0.0.0` or the tailscale IP and open the port to your trusted network.

The same setup from the web-dashboard angle (the auth gate, the `/api/ws` chat socket, and WebSocket close-code triage) is owned by the Web Dashboard page (SP10); the env vars are catalogued under Environment Variables → Web Dashboard & Hermes Desktop (SP21) — link-outs, not duplicated.

## App Troubleshooting (Boot Logs, Electron Download, Resets)

Boot logs land in `HERMES_HOME/logs/desktop.log` (it includes backend output and recent Python tracebacks) — check it first if the app reports a boot failure. You can also tail it from the CLI:

```bash
hermes logs gui -f
```

Common resets (remove the bootstrap marker for a clean first-launch setup, rebuild a broken Python venv, or reset a stuck macOS microphone prompt):

```bash
rm "$HOME/.hermes/hermes-agent/.hermes-bootstrap-complete"   # clean first-launch (macOS/Linux)
rm -rf "$HOME/.hermes/hermes-agent/venv"                     # rebuild broken Python venv
tccutil reset Microphone com.nousresearch.hermes             # reset stuck macOS mic prompt
```

### "Build desktop app" stuck on Electron download

The build downloads the Electron runtime (~114 MB) from `github.com/electron/electron/releases`. If the installer hangs on the **Build desktop app** step with the live output repeating `retrying attempt=…`, GitHub is being blocked or throttled on your network (firewall, proxy, or region).

The installer self-heals this automatically: on a failed build it (1) clears a corrupt cached Electron zip and retries, then (2) if it still fails and you haven't set `ELECTRON_MIRROR`, retries once more through `npmmirror.com`, the de-facto Electron community mirror. `@electron/get` SHASUM-checks the download, but the checksums come from the same mirror — that catches a corrupt or partial download, not a compromised mirror. If you'd rather not trust a third-party host, pin your own `ELECTRON_MIRROR`; the build never overrides one you've set.

To choose your own mirror (e.g. a corporate/trusted one), set `ELECTRON_MIRROR` before installing or rebuild manually — the build honors it and won't override it:

```bash
ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/ \
  bash -c 'cd "$HOME/.hermes/hermes-agent/apps/desktop" && CSC_IDENTITY_AUTO_DISCOVERY=false npm run pack'
```

To clear a corrupt cached zip by hand: `rm -f "$HOME/Library/Caches/electron"/electron-*.zip` on macOS, or `rm -f "$HOME/.cache/electron"/electron-*.zip` on Linux.

**Source**: `inbox/hermes_agent_docs/user-guide/desktop.md` · https://hermes-agent.nousresearch.com/docs/user-guide/desktop
**Last Updated**: 2026-06-19
**Status**: Active
