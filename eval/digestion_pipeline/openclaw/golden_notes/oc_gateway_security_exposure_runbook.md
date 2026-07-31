---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - exposure
keywords:
  - openclaw gateway exposure runbook
  - expose gateway beyond loopback
  - pre-flight inventory rollback
  - minimum safe baseline gateway
  - reverse proxy trustedproxies checks
  - dm group exposure pairing allowlist
  - openclaw security audit deep
  - gateway exposure pattern choice
topics:
  - OpenClaw
  - Gateway Security
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/security/exposure-runbook
access_control_group: ["general"]
---

# OpenClaw — Gateway Exposure Runbook

## Overview

This note is the operator **procedure** for safely exposing an OpenClaw Gateway beyond loopback — over LAN, tailnet, Tailscale Serve, Funnel, or a reverse proxy. It mirrors the `gateway/security/exposure-runbook` page, which turns the broader Security guidance into an operator checklist for remote access and messaging exposure. The page's governing rule (a `<Warning>` at the top) is that you should expose the Gateway only after you can explain who can reach it, how they are authenticated, which agents they can trigger, and which tools those agents can use; when in doubt, return to loopback-only access and re-run the audit.

The runbook is a linear flow: choose the narrowest exposure pattern, take a pre-flight inventory, run baseline checks, apply the minimum-safe-baseline config, then review each exposed surface (DM/group, reverse proxy, tool/sandbox), validate after every change, and keep a tested rollback plan. It closes with a review checklist.

## Choose the exposure pattern

Prefer the narrowest pattern that satisfies the workflow. The page tabulates five patterns, when each is recommended, and the controls each requires:

| Pattern | Recommended when | Required controls |
| --- | --- | --- |
| Loopback + SSH tunnel | Personal use, admin access, debugging | Keep `gateway.bind: "loopback"` and tunnel `127.0.0.1:18789` |
| Loopback + Tailscale Serve | Personal tailnet access to Control UI/WebSocket | Keep Gateway loopback-only; rely on Tailscale identity headers only for supported surfaces |
| Tailnet/LAN bind | Dedicated private network with known devices | Gateway auth, firewall allowlist, no public port-forward |
| Trusted reverse proxy | Organization SSO/OIDC in front of Gateway | `trusted-proxy` auth, strict `trustedProxies`, header overwrite/strip rules, explicit allowed users |
| Public internet | Rare, high-risk deployments | Identity-aware proxy, TLS, rate limits, strict allowlists, sandboxed non-main sessions |

Avoid direct public port-forwarding to the Gateway. If you need public access, put an identity-aware proxy in front of it and make the proxy the only network path to the Gateway.

## Pre-flight inventory

Record these before changing bind, proxy, Tailscale, or channel policy:

- Gateway host, OS user, and state directory.
- Gateway URL and bind mode.
- Auth mode, token/password source, or trusted proxy identity source.
- All enabled channels and whether they accept DMs, groups, or webhooks.
- Agents reachable from non-local senders.
- Tool profile, sandbox mode, and elevated tool policy for each reachable agent.
- External credentials available to those agents.
- Backup location for `~/.openclaw/openclaw.json` and credentials.

If more than one person can message the bot, treat this as shared delegated tool authority, not as per-user host isolation.

## Baseline checks

Run these before opening access:

```bash
openclaw doctor
openclaw security audit
openclaw security audit --deep
openclaw health
```

Resolve critical findings first. Warnings may be acceptable only when they are intentional and documented for the deployment.

For remote CLI validation, pass credentials explicitly:

```bash
openclaw gateway probe --url ws://127.0.0.1:18789 --token "$OPENCLAW_GATEWAY_TOKEN"
```

Do not assume local config credentials apply to an explicit remote URL.

## Minimum safe baseline

Use this shape as the starting point for exposed deployments:

```json5
{
  gateway: {
    bind: "loopback",
    auth: {
      mode: "token",
      token: "replace-with-a-long-random-token",
    },
  },
  session: {
    dmScope: "per-channel-peer",
  },
  agents: {
    defaults: {
      sandbox: { mode: "non-main" },
    },
  },
  tools: {
    profile: "messaging",
    exec: { security: "deny", ask: "always" },
    elevated: { enabled: false },
  },
}
```

Then widen one control at a time. For example, add a specific channel allowlist before enabling write-capable tools, or enable a reverse proxy before accepting remote Control UI traffic. The strict `exec.security: "deny"` baseline blocks all exec calls, including benign diagnostics. If diagnostics or low-risk commands are required, relax this only after choosing the specific senders, agents, commands, and approval mode that match your threat model.

## DM and group exposure

Messaging channels are untrusted input surfaces. Before allowing DMs or groups:

- Prefer `dmPolicy: "pairing"` or strict `allowFrom` lists.
- Avoid `dmPolicy: "open"` unless every sender is trusted.
- Do not combine `"*"` allowlists with broad tool access.
- Require mentions in groups unless the room is tightly controlled.
- Use `session.dmScope: "per-channel-peer"` when multiple people can DM the bot.
- Route shared channels to agents with minimal tools and no personal credentials.

Pairing approves the sender to trigger the bot. It does not make that sender a separate host security boundary.

## Reverse proxy checks

For identity-aware proxies:

- The proxy must authenticate users before forwarding to the Gateway.
- Direct access to the Gateway port must be blocked by firewall or network policy.
- `gateway.trustedProxies` must contain only the proxy source IPs.
- The proxy must strip or overwrite client-supplied identity and forwarding headers.
- `gateway.auth.trustedProxy.allowUsers` should list expected users when the proxy serves more than one audience.
- Same-host loopback proxy mode should use `allowLoopback` only when local processes are trusted and the proxy owns the identity headers.

Run `openclaw security audit --deep` after proxy changes. Trusted-proxy findings are intentionally high-signal because the proxy becomes the authentication boundary.

## Tool and sandbox review

Before exposing an agent to remote senders:

- Confirm which sessions run on host versus sandbox.
- Deny or require approval for host exec.
- Keep elevated tools disabled unless a specific, trusted sender needs them.
- Avoid browser, canvas, node, cron, gateway, and session-spawn tools for open or semi-open messaging surfaces.
- Keep bind mounts narrow and avoid credential, home, Docker socket, and system paths.
- Use separate gateways, OS users, or hosts for materially different trust boundaries.

If remote users are not fully trusted, isolation must come from separate deployments, not only from prompts or session labels.

## Post-change validation

After each exposure change:

1. Re-run `openclaw security audit --deep`.
2. Test a successful authorized connection.
3. Test that an unauthorized sender or browser session is denied.
4. Confirm logs redact secrets.
5. Confirm DM/group routing reaches only the intended agent.
6. Confirm high-impact tools ask for approval or are denied.
7. Document the accepted residual warnings.

Do not proceed to the next exposure change until the current one is understood.

## Rollback plan

If the Gateway may be overexposed, apply this config to return to a safe posture:

```json5
{
  gateway: {
    bind: "loopback",
  },
  channels: {
    whatsapp: { dmPolicy: "disabled" },
    telegram: { dmPolicy: "disabled" },
    discord: { dmPolicy: "disabled" },
    slack: { dmPolicy: "disabled" },
  },
  tools: {
    exec: { security: "deny", ask: "always" },
    elevated: { enabled: false },
  },
}
```

Then:

1. Stop public forwarding, Tailscale Funnel, or reverse proxy routes.
2. Rotate Gateway tokens/passwords and affected integration credentials.
3. Remove `"*"` and unexpected senders from allowlists.
4. Review recent audit logs, run history, tool calls, and config changes.
5. Re-run `openclaw security audit --deep`.
6. Re-enable access with the narrowest pattern that satisfies the workflow.

## Review checklist

The page closes with the operator sign-off checklist:

- Gateway remains loopback-only unless there is a documented reason.
- Non-loopback access has auth, firewalling, and no public direct route.
- Trusted-proxy deployments have strict proxy IPs and header controls.
- DMs use pairing or allowlists, not open access by default.
- Groups require mentions or explicit allowlists.
- Shared channels do not reach personal credentials.
- Non-main sessions run in sandbox mode.
- Host exec and elevated tools are denied or approval-gated.
- Logs redact secrets.
- Critical audit findings are resolved.
- Rollback steps are tested and documented.

**Source**: OpenClaw documentation — `gateway/security/exposure-runbook` (mirror `inbox/openclaw_docs/gateway/security/exposure-runbook.md`)
**Last Updated**: 2026-06-22
**Status**: Active
