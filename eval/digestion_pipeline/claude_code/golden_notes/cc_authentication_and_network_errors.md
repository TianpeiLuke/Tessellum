---
tags:
  - resource
  - documentation
  - claude_code
  - errors
  - authentication
keywords:
  - authentication errors
  - not logged in
  - invalid api key
  - oauth token revoked
  - could not resolve authentication method
  - network connection errors
  - ssl certificate errors
  - host not allowed cloud session
  - anthropic api key precedence
  - node extra ca certs
topics:
  - Claude Code
  - Errors
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/errors
access_control_group: ["general"]
---

# Claude Code — Authentication and Network Errors

## Overview

This note is the recovery procedure for two families of Claude Code runtime errors: **authentication errors** (Claude Code cannot prove who you are to the API) and **network and connection errors** (a request failed to reach its destination). Both surface the same way across the CLI, the Desktop app, and Claude Code on the web, since all three wrap the same Claude Code CLI. For installation-time auth and login failures (OAuth browser issues, 403 Forbidden, clock/Keychain), see the install-troubleshooting login section linked below rather than this runtime reference.

The single most useful first step for any authentication error is `/status`, which shows **which credential is currently active**. Most authentication errors are caused by a credential-precedence surprise — a stray `ANTHROPIC_API_KEY` or `apiKeyHelper` overriding your subscription `/login`. Network errors usually originate in your local network, proxy, or firewall, or in a cloud environment's outbound network policy.

## Authentication Errors

These errors mean Claude Code cannot prove who you are to the API. Run `/status` at any time to see which credential is currently active.

### Not logged in

No valid credential is available for this session.

```text theme={null}
Not logged in · Please run /login
```

**What to do:**

- Run `/login` to authenticate with your Claude subscription or Console account.
- If you expected an environment variable to authenticate you, confirm `ANTHROPIC_API_KEY` is set and exported in the shell where you launched `claude`.
- For CI or automation where interactive login is not possible, configure an `apiKeyHelper` script that fetches a key at startup.
- See [Authentication precedence](https://code.claude.com/docs/en/authentication) to understand which credential wins when several are present.

If you are prompted to log in repeatedly, the system clock and macOS Keychain fixes live in the install-troubleshooting login section (see [Login and authentication troubleshooting](cc_login_authentication_troubleshooting.md)).

### Could not resolve authentication method

The session reached the API client without any credential. This appears in background sessions, cloud sessions, and Agent SDK contexts where the interactive login check does not run before the first request.

```text theme={null}
Could not resolve authentication method. Expected one of apiKey, authToken, credentials, config, or profile to be set. Or for one of the "X-Api-Key" or "Authorization" headers to be explicitly omitted
```

Before v2.1.174, a background or cloud session assigned to an idle pre-initialized worker could fail this way even when valid credentials were configured; upgrade to recover. On current versions the error means no credential was available to the worker process.

**What to do:**

- Upgrade to v2.1.174 or later if this appears in a background or cloud session and your credentials are already configured.
- Confirm `ANTHROPIC_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN`, or your cloud provider credentials are set in the environment that launches the worker, not only in your interactive shell.
- For the Agent SDK, see [authentication setup](https://code.claude.com/docs/en/agent-sdk/overview).
- Run `/status` in an interactive session in the same environment to confirm which credential source resolves.

### Invalid API key

The `ANTHROPIC_API_KEY` environment variable or `apiKeyHelper` script returned a key the API rejected (`Invalid API key · Fix external API key`).

**What to do:**

- Check for typos and confirm the key has not been revoked in the Console.
- Run `env | grep ANTHROPIC` in the same shell. Tools like direnv, dotenv shell plugins, and IDE terminals can load a stale key from a `.env` file in your project without you setting it explicitly.
- Unset `ANTHROPIC_API_KEY` and run `/login` to use subscription auth instead.
- If the key comes from an `apiKeyHelper` script, run the script directly to confirm it prints a valid key on stdout.
- Run `/status` to confirm which credential source Claude Code is actually using.

### Organization-disabled and policy errors

Several authentication errors share a root cause: a server-side organization setting, or a stale API key overriding your subscription. Environment variables and `apiKeyHelper` take precedence over `/login`, so a key exported in your shell profile or loaded from a `.env` file is used even when you have a working Pro or Max subscription; in non-interactive mode (`-p`), a present key is always used.

- **This organization has been disabled** — a stale `ANTHROPIC_API_KEY` from a disabled Console organization is overriding your subscription login (`Your ANTHROPIC_API_KEY belongs to a disabled organization · Unset the environment variable to use your other credentials` / `API Error: 400 ... This organization has been disabled.`). Unset `ANTHROPIC_API_KEY` in the current shell and remove it from your shell profile, then relaunch `claude` and run `/status`. If no variable is set and the error persists, the disabled org is the one tied to your `/login` — contact support or sign in with a different account.
- **Your organization has disabled API key authentication** — the admin turned off API-key auth, so the API rejects the key. The recovery hint after the `·` names where the key came from (`ANTHROPIC_API_KEY`, an `apiKeyHelper` setting, or both). Unset the named source (remove `ANTHROPIC_API_KEY` from shell/`.env`, or remove `apiKeyHelper` from `settings.json`), run `/login` to sign in with your claude.ai account, then confirm with `/status`. Ask your admin to re-enable API-key auth if automation needs it.
- **Your organization has disabled Claude subscription access** — a server-side setting prevents subscription login; running `/login` again returns the same error. The Agent SDK and `-p` surface this as the `oauth_org_not_allowed` error code. Ask your admin to enable Claude Code access, or authenticate with a Console API key instead.
- **Routines are disabled by your organization's policy** — a Team/Enterprise admin turned off routines org-wide; appears when creating or running a routine, including from `/schedule` and the Routines UI. Ask your admin to enable the **Routines** toggle, or use [scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks) for one-off work.

All four cannot be overridden from local settings, environment variables, or CLI flags when the cause is the server-side org setting.

### OAuth token revoked or expired

Your saved login is no longer valid. A revoked token means you signed out everywhere or an admin removed access; an expired token means the automatic refresh failed mid-session.

```text theme={null}
OAuth token revoked · Please run /login
OAuth token has expired · Please run /login
API Error: 401 ... authentication_error
```

**What to do:**

- Run `/login` to sign in again.
- If the error returns within the same session after re-authenticating, run `/logout` first to fully clear the stored token, then `/login`.
- For repeated prompts to log in across launches, see the system clock and macOS Keychain checks in [Login and authentication troubleshooting](cc_login_authentication_troubleshooting.md).
- For other failures including `403 Forbidden` and OAuth browser issues, see [Login and authentication troubleshooting](cc_login_authentication_troubleshooting.md).

### OAuth scope requirement

The stored token predates a permission scope that a newer feature needs (`OAuth token does not meet scope requirement: user:profile`). You see this most often from `/usage` and the status line usage indicator. Run `/login` to mint a new token with the current scopes — you do not need to log out first.

## Network and Connection Errors

These errors mean a network request from Claude Code failed to reach its destination. They usually originate in your local network, proxy, or firewall, or in the cloud environment's network policy.

### Unable to connect to API

The TCP connection to the API failed or never completed. Variants include `Unable to connect to API. Check your internet connection`, `(ECONNREFUSED)`, `(ECONNRESET)`, `(ETIMEDOUT)`, `fetch failed`, and `Request timed out. Check your internet connection and proxy settings`. Common causes are no internet access, a VPN that blocks `api.anthropic.com`, or a required corporate proxy that is not configured.

**What to do:**

- Confirm you can reach the API host from the same shell:

```bash theme={null}
curl -I https://api.anthropic.com
```

  On Windows PowerShell use `curl.exe -I https://api.anthropic.com` so the built-in `Invoke-WebRequest` alias is not used.

- If you are behind a corporate proxy, set `HTTPS_PROXY` before launching Claude Code and see [Network configuration](https://code.claude.com/docs/en/network-config).
- If you route through an LLM gateway or relay, set `ANTHROPIC_BASE_URL` to its address.
- Ensure your firewall allows the hosts listed in Network access requirements.
- Intermittent failures are retried automatically; persistent failures point to a local network issue.

If `curl` succeeds but Claude Code still fails, the cause is usually something between the runtime and the network: on Linux/WSL check `/etc/resolv.conf` for an unreachable nameserver (WSL can inherit a broken resolver); on macOS check `ifconfig` for stale `utun` interfaces left by a disconnected/uninstalled VPN and remove the VPN's network extension; quit Docker Desktop and similar container runtimes that can intercept outbound traffic, and retry.

### SSL certificate errors

A proxy or security appliance on your network is intercepting TLS traffic with its own certificate, and Claude Code does not trust it.

```text theme={null}
Unable to connect to API: SSL certificate verification failed. Check your proxy or corporate SSL certificates
Unable to connect to API: Self-signed certificate detected
```

**What to do:**

- Export your organization's CA bundle and point Claude Code at it with `NODE_EXTRA_CA_CERTS=/path/to/ca-bundle.pem`.
- See [Network configuration](https://code.claude.com/docs/en/network-config) for full setup instructions.
- **Do not** set `NODE_TLS_REJECT_UNAUTHORIZED=0`, which disables certificate validation entirely.

### Host not allowed in a cloud session

An outbound HTTP request from a cloud session or routine was blocked by the environment's network policy.

```text theme={null}
HTTP 403
x-deny-reason: host_not_allowed
```

You may also see a TLS certificate that doesn't match the destination's real certificate. The cloud environment routes outbound traffic through a proxy that enforces the network policy, so a mismatched certificate means the proxy terminated the connection, not the destination. This is not a client-side network problem — cloud sessions and routines run inside a sandboxed environment whose outbound traffic is filtered to the environment's allowlist. The **Default** environment uses **Trusted** access, which permits a default allowlist of package registries, cloud provider APIs, container registries, and common development domains but blocks everything else.

**What to do:**

- Open the routine for editing, or start a cloud session. Select the cloud icon showing your environment's name (such as **Default**) to open the selector. Hover over your environment and click the settings icon.
- In the **Update cloud environment** dialog, change **Network access** from **Trusted** to **Custom**, then add the blocked domain to **Allowed domains** (one per line). Check **Also include default list of common package managers** to keep the default allowlist alongside your custom domains. Select **Full** instead for unrestricted access.
- Click **Save changes**. The next run uses the updated allowlist.

Local CLI sessions are not affected by this policy.

**Source**: https://code.claude.com/docs/en/errors
**Last Updated**: 2026-06-13
**Status**: Active
