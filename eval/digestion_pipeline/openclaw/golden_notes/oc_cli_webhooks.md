---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - webhooks
keywords:
  - openclaw webhooks
  - gmail pub/sub
  - gog watch serve
  - webhooks gmail setup
  - webhooks gmail run
  - tailscale funnel
  - hook-url delivery
  - watch auto-renew
topics:
  - OpenClaw
  - CLI Webhooks
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/webhooks
access_control_group: ["general"]
---

# OpenClaw — The `openclaw webhooks` Command (Gmail Pub/Sub Setup and Runner)

## Overview

This note documents the `openclaw webhooks` command as a procedure: how an operator wires Gmail change notifications into OpenClaw through Gmail Pub/Sub and the bundled `gog` watcher. Today the surface is scoped entirely to Gmail Pub/Sub flows, exposed through two subcommands — `webhooks gmail setup` (configure the Gmail watch, the Pub/Sub topic/subscription, the OpenClaw webhook delivery target, the `gog watch serve` listener, and the Tailscale exposure of the push endpoint) and `webhooks gmail run` (run `gog watch serve` plus the watch auto-renew loop in the foreground). It mirrors the `cli/webhooks` source page: the subcommand table, the full `gmail setup` flag/default tables (Required, Pub/Sub, OpenClaw delivery, `gog watch serve`, Tailscale, Output), the `gmail run` flag inheritance and exceptions, and the end-to-end flow link-out.

## Subcommands

Webhook helpers and integrations. Today this surface is scoped to Gmail Pub/Sub flows that integrate with the bundled `gog` watcher. The two invocation forms are:

```bash
openclaw webhooks gmail setup --account <email> [...]
openclaw webhooks gmail run   [--account <email>] [...]
```

| Subcommand | Description |
| --- | --- |
| `gmail setup` | Configure Gmail watch, Pub/Sub topic/subscription, and the OpenClaw webhook delivery target. |
| `gmail run` | Run `gog watch serve` plus the watch auto-renew loop. |

## `webhooks gmail setup`

Configure Gmail watch, Pub/Sub, and OpenClaw webhook delivery. Representative invocations from the source page:

```bash
openclaw webhooks gmail setup --account you@example.com
openclaw webhooks gmail setup --account you@example.com --project my-gcp-project --json
openclaw webhooks gmail setup --account you@example.com --hook-url https://gateway.example.com/hooks/gmail
```

### Required

| Flag | Description |
| --- | --- |
| `--account <email>` | Gmail account to watch. |

### Pub/Sub options

| Flag | Default | Description |
| --- | --- | --- |
| `--project <id>` | (none) | GCP project id (the OAuth client owner). |
| `--topic <name>` | `gog-gmail-watch` | Pub/Sub topic name. |
| `--subscription <name>` | `gog-gmail-watch-push` | Pub/Sub subscription name. |
| `--label <label>` | `INBOX` | Gmail label to watch. |
| `--push-endpoint <url>` | (none) | Explicit Pub/Sub push endpoint. Overrides Tailscale. |

### OpenClaw delivery options

| Flag | Default | Description |
| --- | --- | --- |
| `--hook-url <url>` | (none) | OpenClaw webhook URL. |
| `--hook-token <token>` | (none) | OpenClaw webhook token. |
| `--push-token <token>` | (none) | Push token forwarded to `gog watch serve`. |

### `gog watch serve` options

| Flag | Default | Description |
| --- | --- | --- |
| `--bind <host>` | `127.0.0.1` | `gog watch serve` bind host. |
| `--port <port>` | `8788` | `gog watch serve` port. |
| `--path <path>` | `/gmail-pubsub` | `gog watch serve` path. |
| `--include-body` | `true` | Include email body snippets. Pass `--no-include-body` to disable. |
| `--max-bytes <n>` | `20000` | Max bytes per body snippet. |
| `--renew-minutes <n>` | `720` (12h) | Renew Gmail watch every N minutes. |

### Tailscale exposure

| Flag | Default | Description |
| --- | --- | --- |
| `--tailscale <mode>` | `funnel` | Expose push endpoint via tailscale: `funnel`, `serve`, or `off`. |
| `--tailscale-path <path>` | (none) | Path for tailscale serve/funnel. |
| `--tailscale-target <t>` | (none) | Tailscale serve/funnel target (port, `host:port`, or URL). |

### Output

| Flag | Description |
| --- | --- |
| `--json` | Print a machine-readable summary instead of text. |

## `webhooks gmail run`

Run `gog watch serve` plus the watch auto-renew loop in the foreground:

```bash
openclaw webhooks gmail run --account you@example.com
```

`run` accepts the same `gog watch serve`, OpenClaw delivery, Pub/Sub, and Tailscale flags as `setup`, except: `--account` is **optional** on `run` (it falls back to the configured account); `run` does **not** accept `--project`, `--push-endpoint`, or `--json`; and `run` flags have no built-in defaults — missing values fall back to the values written by `setup`. The flags grouped by category for `run` are:

| Category | Flags |
| --- | --- |
| Pub/Sub | `--account`, `--topic`, `--subscription`, `--label` |
| OpenClaw delivery | `--hook-url`, `--hook-token`, `--push-token` |
| `gog watch serve` | `--bind`, `--port`, `--path`, `--include-body`, `--max-bytes`, `--renew-minutes` |
| Tailscale | `--tailscale`, `--tailscale-path`, `--tailscale-target` |

A source `<Note>` clarifies one `run`-specific value semantics: for `run`, the `--topic` value is the full Pub/Sub topic path (`projects/.../topics/...`), not just the short topic name (whereas `setup` accepts the short topic name, defaulting to `gog-gmail-watch`).

## End-to-end flow

The CLI commands are only the operator-side half of the integration. The source page points operators to the Gmail Pub/Sub integration guide for the GCP project, OAuth, and gateway-side setup that pairs with these CLI commands (the GCP project + OAuth client, the Pub/Sub topic/subscription wiring on the Google Cloud side, and the OpenClaw gateway webhook endpoint that receives the pushed events). That backend setup is documented at `/automation/cron-jobs#gmail-pubsub-integration` and is not duplicated here.

**Source**: OpenClaw documentation — `cli/webhooks` (mirror `inbox/openclaw_docs/cli/webhooks.md`)
**Last Updated**: 2026-06-22
**Status**: Active
