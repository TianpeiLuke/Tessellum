---
tags:
  - resource
  - documentation
  - hermes_agent
  - authentication
  - remote_setup
keywords:
  - oauth over ssh
  - loopback redirect callback
  - ssh local forward tunnel
  - manual-paste flag
  - remote host headless oauth
  - proxyjump jump box
topics:
  - Hermes Agent
  - Provider Setup
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/oauth-over-ssh
access_control_group: ["general"]
---

# OAuth over SSH / Remote Hosts

## Overview

This guide is the cross-cutting transport fix for completing browser-based OAuth logins when Hermes runs on a machine other than the one with your browser — a remote server, a container, or a host behind a jump box. A handful of Hermes providers — **xAI Grok OAuth**, **Spotify**, and **remote MCP servers** (Linear, Sentry, Atlassian, Asana, Figma, …) — use a *loopback redirect* OAuth flow: the auth server redirects your browser to `http://127.0.0.1:<port>/callback`, where a tiny HTTP listener that Hermes started grabs the authorization code. That works perfectly when Hermes and your browser share a machine; it breaks the moment they don't, because your laptop's browser tries to reach `127.0.0.1` on your laptop while the listener is bound to `127.0.0.1` on the remote server. The fix is a one-line SSH local-forward — or, when no real SSH client is available (GCP Cloud Shell, GitHub Codespaces, EC2 Instance Connect, Gitpod, browser-based web IDEs), the `--manual-paste` flag. The page is a task script, not the OAuth/credential-pool concept layer (those are owned elsewhere); it documents which providers need the tunnel, the per-provider loopback ports, the single-hop and jump-box recipes, the mosh/tmux/ControlMaster gotchas, and the port-conflict troubleshooting.

## TL;DR

```bash
# On your local machine (laptop), in a separate terminal:
ssh -N -L 56121:127.0.0.1:56121 user@remote-host

# In your existing SSH session on the remote machine:
hermes auth add xai-oauth --no-browser
# → Hermes prints an authorize URL. Open it in a browser on your laptop.
# → Your browser redirects to 127.0.0.1:56121/callback, the tunnel forwards
#   the request to the remote listener, login completes.
```

Port `56121` is what xAI OAuth uses. For Spotify, replace it with `43827`. Hermes prints the exact port it bound to on the `Waiting for callback on ...` line — copy it from there.

## Browser-only remote (Cloud Shell / Codespaces / EC2 Instance Connect)

When you don't have a regular SSH client — because you're running Hermes inside GCP Cloud Shell, GitHub Codespaces, AWS EC2 Instance Connect, Gitpod, or another browser-based console — the SSH tunnel isn't available. Use `--manual-paste` instead:

```bash
hermes auth add xai-oauth --manual-paste
# → Hermes prints an authorize URL. Open it in a browser on your laptop.
# → Approve in the browser. The redirect to 127.0.0.1:56121/callback fails
#   to load — that's expected.
# → Copy the FULL URL from the failed page's address bar.
# → Paste it back into the terminal at the "Callback URL:" prompt.
```

The same flag works on `hermes model --manual-paste` for the integrated model picker. Hermes accepts three callback paste forms interchangeably: the full URL, a bare `?code=...&state=...` query fragment, or — when the upstream consent page renders the authorization code in-page instead of redirecting (xAI's current behavior on browser-based consoles) — just the bare code value on its own.

Hermes uses the **same PKCE verifier, state and nonce** for both paths, so the upstream OAuth flow is byte-identical — `--manual-paste` is purely a transport change for the callback hop and is not a security downgrade.

## Which Providers Need This

| Provider | Loopback port | Tunnel needed? |
|----------|---------------|----------------|
| `xai-oauth` (Grok SuperGrok) | `56121` | Yes, when Hermes is remote |
| Spotify | `43827` | Yes, when Hermes is remote |
| MCP servers (`auth: oauth`) | auto-picked per server | Yes, when Hermes is remote |
| `anthropic` (Claude Pro/Max) | n/a | No — paste-the-code flow |
| `openai-codex` (ChatGPT Plus/Pro) | n/a | No — device code flow |
| `minimax`, `nous-portal` | n/a | No — device code flow |

If your provider isn't in the table, you don't need a tunnel.

## MCP Servers

Remote MCP servers (Linear, Sentry, Atlassian, Asana, Figma, etc.) use the same loopback redirect flow. Hermes auto-picks a free port per server and prints the authorize URL when the OAuth flow kicks off — either at startup (when a new server appears in `mcp_servers:`) or when you run `hermes mcp login <server>`. You have two ways to complete it from a remote host:

**Option 1 — paste the redirect URL back (no setup, works anywhere).** On an interactive terminal, Hermes prints `MCP OAuth: authorization required.` followed by the authorize URL (e.g. `https://mcp.linear.app/authorize?response_type=code&...`) and prompts you to paste the redirect URL back. After approving in your browser, the redirect to `http://127.0.0.1:<port>/callback` will show a connection error — that's expected. Copy the full URL from the browser's address bar (e.g. `https://mcp.linear.app/callback?code=abc123&state=xyz`) and paste it at the `Or paste the redirect URL here ...` prompt; Hermes responds `Got authorization code from paste — completing flow.` A bare `?code=...&state=...` query string is accepted too. This works for any MCP server with `auth: oauth` and requires no SSH config changes.

**Option 2 — SSH port forward (same as xAI / Spotify).** Hermes prints the exact port it bound to in the SSH-session hint. Open a separate terminal on your laptop and run `ssh -N -L <port>:127.0.0.1:<port> user@remote-host`, then open the authorize URL in your browser as normal; the redirect tunnels through and the listener picks it up. Use this when you need the flow to complete unattended (e.g. scripted re-auth where you can't paste interactively).

**Pitfall — the 30s config-reload race.** If you edit `~/.hermes/config.yaml` to add an OAuth MCP server from inside a running Hermes session, the CLI auto-reloads MCP connections with a 30s timeout. That's not enough time to complete an interactive OAuth flow, and the reload will give up. Use `hermes mcp login <server>` from a fresh terminal instead — it has no such cap and waits the full 5 min for you to paste back.

## Why the listener can't just bind 0.0.0.0

xAI and Spotify both validate the `redirect_uri` parameter against an allowlist. Both require the loopback form (`http://127.0.0.1:<exact-port>/callback`). Binding the listener to `0.0.0.0` or a different port would cause the auth server to reject the request as a redirect_uri mismatch. The SSH tunnel keeps the loopback URI intact end-to-end.

## Step-by-step: single SSH hop

```bash
# 1. Start the tunnel from your local machine.
#    xAI Grok OAuth (port 56121)
ssh -N -L 56121:127.0.0.1:56121 user@remote-host
#    Or for Spotify (port 43827)
ssh -N -L 43827:127.0.0.1:43827 user@remote-host

# 2. In a separate SSH session, run the auth command.
ssh user@remote-host
hermes auth add xai-oauth --no-browser
# or for Spotify:  hermes auth add spotify --no-browser
```

`-N` means "don't open a remote shell, just hold the tunnel open." Keep that terminal running for the duration of the login. Hermes detects the SSH session, skips the browser auto-open, and prints an authorize URL plus a `Waiting for callback on http://127.0.0.1:<port>/callback` line. Copy the authorize URL into the browser on your laptop and approve the consent screen; the auth server redirects to `http://127.0.0.1:<port>/callback`, your browser hits the tunnel, the request is forwarded to the remote listener, and Hermes prints `Login successful!`. Tear down the tunnel (Ctrl+C in the first terminal) once you see the success line.

## Step-by-step: through a jump box

If you reach Hermes through a bastion / jump host, use SSH's built-in `-J` (ProxyJump):

```bash
ssh -N -L 56121:127.0.0.1:56121 -J jump-user@jump-host user@final-host
```

This chains an SSH connection through the jump host without putting the loopback port on the jump box itself. The local `127.0.0.1:56121` on your laptop tunnels straight through to `127.0.0.1:56121` on the final remote host. For older OpenSSH that doesn't support `-J`, the long form is:

```bash
ssh -N \
    -o "ProxyCommand=ssh -W %h:%p jump-user@jump-host" \
    -L 56121:127.0.0.1:56121 \
    user@final-host
```

## Mosh, tmux, ssh ControlMaster

The tunnel is a property of the underlying SSH connection. If you're running Hermes inside `tmux` over a mosh session, the mosh roaming doesn't carry the `-L` forwarding. Open a *separate* plain SSH session **only** for the `-L` tunnel — that's the connection that has to stay alive during the auth flow. Your interactive mosh/tmux session can keep running Hermes normally. If you use `ssh -o ControlMaster=auto`, port forwards on a multiplexed connection share the master's lifetime. Restart the master if the tunnel doesn't come up:

```bash
ssh -O exit user@remote-host
ssh -N -L 56121:127.0.0.1:56121 user@remote-host
```

## Troubleshooting

- **`bind [127.0.0.1]:56121: Address already in use`** — something on your laptop is already using that port (a previous tunnel that didn't shut down cleanly, or a local Hermes also listening). Find and kill the offender with `lsof -iTCP:56121 -sTCP:LISTEN` then `kill <PID>`, and retry the `ssh -L` command.
- **"Could not establish connection. We couldn't reach your app." (xAI)** — xAI's authorize page shows this when its redirect to `127.0.0.1:<port>/callback` doesn't reach a listener. Either the tunnel isn't running, the port is wrong, or you're using the port Hermes printed in a previous run (it can be auto-bumped if the preferred one is busy — always read the latest `Waiting for callback on ...` line).
- **`xAI authorization timed out waiting for the local callback`** — same root cause: the redirect never made it back. Check the tunnel is still alive (`ssh -N` shows no output, so look at the terminal you started it from), restart it if needed, and re-run `hermes auth add xai-oauth --no-browser`.
- **Tokens land in the wrong `~/.hermes`** — tokens are written under the Linux user that ran `hermes auth add ...`. If your gateway / systemd service runs as a different user (e.g. `root` or a dedicated `hermes` user), authenticate as *that* user (`sudo -u hermes -i` or equivalent) so the tokens land in their `~/.hermes/auth.json`.

**Source**: https://hermes-agent.nousresearch.com/docs/guides/oauth-over-ssh
**Last Updated**: 2026-06-19
**Status**: Active
