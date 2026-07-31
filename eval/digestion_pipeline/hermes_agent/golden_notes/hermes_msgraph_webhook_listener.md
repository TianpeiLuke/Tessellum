---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - webhooks
keywords:
  - microsoft graph webhook listener
  - msgraph_webhook gateway platform
  - clientState timing-safe auth
  - change notification listener
  - source-IP CIDR allowlist
  - teams meeting transcript pipeline
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/msgraph-webhook
access_control_group: ["general"]
---

# Hermes Agent — Microsoft Graph Webhook Listener

## Overview

The `msgraph_webhook` gateway platform is an **inbound event listener** — it is how Hermes receives Microsoft Graph **change notifications** (a Teams meeting ended, a new chat message landed, a calendar event was updated). It is deliberately distinct from the `teams` platform (a chat bot users type to): here M365 is *telling Hermes something happened*, not a person conversing. Today the primary consumer is the **Teams meeting summary pipeline** — Graph notifies when a meeting produces a transcript, the pipeline fetches it, and Hermes posts a summary back into Teams; other Graph resources (`/chats/.../messages`, `/users/.../events`) ride the same listener as their pipeline consumers land. Setup is a short procedure: register a Graph application, expose a public HTTPS endpoint Graph can reach, configure a strong `clientState` shared secret, and (for non-loopback binds) allowlist Microsoft's published source-IP ranges. The listener speaks plain HTTP and expects TLS to be terminated at a reverse proxy.

## Prerequisites

- **Microsoft Graph application credentials** — register an app (see the [app-registration guide](#related-notes), routed to SP17), out of scope for this listener page.
- **A public HTTPS URL** Microsoft Graph can reach. Graph does not call private endpoints; a dev tunnel works for testing, production needs a real domain with a valid certificate.
- **A strong shared secret** for `clientState`. Generate it with `openssl rand -hex 32` and store it in `~/.hermes/.env` as `MSGRAPH_WEBHOOK_CLIENT_STATE`.

## Quick Start

Minimum `~/.hermes/config.yaml`:

```yaml
platforms:
  msgraph_webhook:
    enabled: true
    extra:
      host: 127.0.0.1
      port: 8646
      client_state: "replace-with-a-strong-secret"
      accepted_resources:
        - "communications/onlineMeetings"
```

Or via env vars in `~/.hermes/.env` (auto-merged on startup):

```bash
MSGRAPH_WEBHOOK_ENABLED=true
MSGRAPH_WEBHOOK_PORT=8646
MSGRAPH_WEBHOOK_CLIENT_STATE=<generate-with-openssl-rand-hex-32>
MSGRAPH_WEBHOOK_ACCEPTED_RESOURCES=communications/onlineMeetings
```

The bind host is read from `extra.host` in `config.yaml` (above); there is **no** `MSGRAPH_WEBHOOK_HOST` env-var override. Start the gateway with `hermes gateway run`. The listener exposes three endpoints:

- `POST /msgraph/webhook` — change notifications from Graph.
- `GET /msgraph/webhook?validationToken=...` — the Graph subscription **validation handshake** (echoes the token verbatim).
- `GET /health` — readiness probe with accepted/duplicate counters.

Expose the listener publicly via reverse proxy, dev tunnel, or ingress. Your notification URL for Graph subscriptions is the public HTTPS origin followed by `/msgraph/webhook` (e.g. `https://ops.example.com/msgraph/webhook`).

## Configuration

All settings go under `platforms.msgraph_webhook.extra`:

| Setting | Default | Description |
|---------|---------|-------------|
| `host` | `0.0.0.0` | Bind address. Non-loopback binds require `allowed_source_cidrs`; loopback (`127.0.0.1` / `::1`) is the easiest dev-tunnel / reverse-proxy setup. |
| `port` | `8646` | Bind port. |
| `webhook_path` | `/msgraph/webhook` | URL path Graph POSTs to. |
| `health_path` | `/health` | Readiness endpoint. |
| `client_state` | — | Shared secret Graph echoes in every notification. Compared with `hmac.compare_digest` — generate with `openssl rand -hex 32`. |
| `accepted_resources` | `[]` (accept all) | Allowlist of Graph resource paths/patterns. Trailing `*` is a prefix match; leading `/` is tolerated. Example: `["communications/onlineMeetings", "chats/*/messages"]`. |
| `max_seen_receipts` | `5000` | Dedupe cache size for notification IDs; oldest entries evicted when the cap is hit. |
| `allowed_source_cidrs` | `[]` | Required for non-loopback binds. Leave empty only when bound to loopback behind a local tunnel / reverse proxy. |

Most settings also have a `MSGRAPH_WEBHOOK_*` env var that merges into the config at gateway startup — the exception is `host`, which is config-only.

## Security Hardening

**clientState is the primary auth check.** Every Graph notification includes the `clientState` string the subscription registered with. The listener rejects any notification whose `clientState` doesn't match, using **timing-safe comparison** — this is Microsoft's documented mechanism, so treat the value as a strong shared secret. If `client_state` is unset, the listener **refuses to start**.

**Source-IP allowlisting (production).** Restrict the listener to Microsoft's published Graph webhook source-IP ranges. Microsoft documents the egress ranges under the [Office 365 IP Address and URL Web service](https://learn.microsoft.com/en-us/microsoft-365/enterprise/urls-and-ip-address-ranges). Configure them as:

```yaml
platforms:
  msgraph_webhook:
    enabled: true
    extra:
      host: 0.0.0.0
      client_state: "..."
      allowed_source_cidrs:
        - "52.96.0.0/14"
        - "52.104.0.0/14"
        # ...add the current Microsoft 365 "Common" + "Teams" category egress ranges
```

Or as an env var: `MSGRAPH_WEBHOOK_ALLOWED_SOURCE_CIDRS="52.96.0.0/14,52.104.0.0/14"`. Binding a non-loopback host (`0.0.0.0`, `::`, a LAN IP) without `allowed_source_cidrs` is refused at startup. On the same machine as a dev tunnel / reverse proxy, bind to `127.0.0.1` or `::1` and leave the allowlist empty. Invalid CIDR strings log a warning and are ignored. **Review the Microsoft IP list quarterly** — it changes.

**HTTPS termination.** The listener speaks plain HTTP. Terminate TLS at your reverse proxy (Caddy, Nginx, Cloudflare Tunnel, AWS ALB) and proxy to the listener over the local network. Graph refuses to deliver to non-HTTPS endpoints, so there is no path for unencrypted traffic to reach you from Graph itself.

**Response hygiene.** On success the listener returns `202 Accepted` with an **empty body** — internal counters stay out of the wire response. Operators observe counts via `/health`, which is guarded by the same source-IP rules as the webhook path.

Status code table:

| Outcome | Status |
|---------|--------|
| Notification(s) accepted or deduped | 202 |
| Validation handshake (GET with `validationToken`) | 200 (echoes the token) |
| Every item in batch failed clientState | 403 |
| Malformed JSON / missing `value` array / unknown resource | 400 |
| Source IP not in allowlist | 403 |
| Bare GET without `validationToken` | 400 |

## Troubleshooting

| Problem | What to check |
|---------|---------------|
| Graph subscription validation fails | Public URL is reachable, `/msgraph/webhook` path matches, GET with `validationToken` echoes the token verbatim as `text/plain` within 10 seconds. |
| Notifications POST but nothing ingests | `client_state` matches what you registered the subscription with; re-run `openssl rand -hex 32` and create a new subscription if the value drifted. Check `accepted_resources` includes the resource path Graph is sending. |
| Every notification 403s | `clientState` mismatch (forged, or subscription registered with a different value). Re-create with `hermes teams-pipeline subscribe --client-state "$MSGRAPH_WEBHOOK_CLIENT_STATE" ...` (ships with the pipeline runtime PR). |
| Listener refuses to start on `0.0.0.0` | Set `allowed_source_cidrs` to Microsoft's current webhook egress ranges, or bind to `127.0.0.1` / `::1` behind your tunnel or reverse proxy. |
| `/health` hangs | Port-binding collision. Check `ss -tlnp \| grep 8646` and change `port:` if needed. |
| Real Graph requests get 403'd | Source-IP allowlist is too narrow. Widen it to the current Microsoft egress ranges; while still validating the tunnel path, bind to loopback and let the tunnel handle public exposure. |

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/msgraph-webhook.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/msgraph-webhook
**Last Updated**: 2026-06-19
**Status**: Active
