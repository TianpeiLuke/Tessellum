---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - troubleshooting
keywords:
  - clawhub login browser never completes
  - clawhub unauthorized 401
  - clawhub rate limit exceeded 429
  - clawhub proxy https_proxy
  - clawhub skill not in search
  - openclaw plugins install clawhub
  - clawhub public api requests fail
  - clawhub inspect owner diagnostics
topics:
  - OpenClaw
  - ClawHub Troubleshooting
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/clawhub/troubleshooting
access_control_group: ["general"]
---

# OpenClaw — ClawHub Troubleshooting: Sign-In, Install, and API Access

## Overview

This note collects the ClawHub diagnostic recipes for the **sign-in, install, and public-API-access** failures a user hits when consuming the registry, mirroring the auth/install half of the `clawhub/troubleshooting` source page. It walks through seven recipes: a `clawhub login` browser flow that opens but never completes, an `Unauthorized` (401) on `whoami`/`publish`, a `Rate limit exceeded` (429) on search/install, failures behind an HTTP proxy, a skill that does not appear in search, a plugin install that fails inside OpenClaw, and public-API requests that fail. The sibling note [oc_clawhub_troubleshooting_publish_sync](oc_clawhub_troubleshooting_publish_sync.md) covers the publish/sync/update half of the same page.

## `clawhub login` opens a browser but never completes

The CLI starts a short-lived local callback server during browser login, so the login hangs when the browser cannot reach that callback. Make sure your browser can reach `http://127.0.0.1:<port>/callback`. Check local firewall, VPN, and proxy rules if the callback never arrives — any of these can block the loopback callback the browser must redirect to. In headless environments, where no browser is available to complete the redirect, create an API token in the ClawHub web UI and pass it directly with the `--token` flag:

```bash
clawhub login --token clh_...
```

## `whoami` or `publish` returns `Unauthorized` (401)

A `401 Unauthorized` from `whoami` or `publish` means the CLI is not presenting a valid token. The source gives three checks, in order:

- Sign in again with `clawhub login` — this refreshes an expired or missing session token.
- If you use a custom config path, confirm `CLAWHUB_CONFIG_PATH` points at the file that contains your current token (a stale or wrong path is read as "no token").
- If you use an API token, confirm it was not revoked in the web UI.

## Search or install returns `Rate limit exceeded` (429)

When search or install returns `Rate limit exceeded` (429), read the retry information in the response headers rather than blindly retrying:

- `Retry-After`: seconds to wait before retrying.
- `RateLimit-Remaining` and `RateLimit-Limit`: your current budget.
- `RateLimit-Reset` or `X-RateLimit-Reset`: reset timing.

If many users share one egress IP, anonymous IP limits can be hit even when each person only sends a few requests. Sign in where possible (authenticated requests are budgeted per-account rather than per-IP) and retry after the reported delay.

## Search or install fails behind a proxy

The CLI respects standard proxy variables, so a search/install that fails behind a corporate proxy is usually fixed by exporting one. Set the proxy variable and re-run the command in the same shell:

```bash
export HTTPS_PROXY=http://proxy.example.com:3128
clawhub search "my query"
```

Supported names include `HTTPS_PROXY`, `HTTP_PROXY`, `https_proxy`, and `http_proxy`.

## A skill does not appear in search

When a skill you expect is missing from search results, the recipe is to confirm both its identity and its release state:

- Check the exact slug or owner page if you know it (search may miss a partial or wrong slug).
- Confirm the release is public and not held by scan or moderation — a held or non-public release is excluded from the listing.
- If you own the skill, sign in and inspect it directly:

```bash
clawhub inspect @openclaw/demo
```

Owner-visible diagnostics may explain scan, upload-gate, or moderation state — i.e. why a release you published is not yet listed.

## A plugin install fails in OpenClaw

When `openclaw plugins install` fails for a ClawHub package, the source recommends pinning the source and verifying compatibility:

- Use an explicit ClawHub source so OpenClaw resolves the package from the registry rather than another source:

```bash
openclaw plugins install clawhub:<package>
```

- Check the package detail page for scan status and compatibility metadata.
- Confirm your OpenClaw version satisfies the package's advertised compatibility range.
- If the package is hidden, held, or blocked, it may not be installable until the owner resolves the issue.

## Public API requests fail

For programmatic clients of the public ClawHub API, failures are usually a matter of API etiquette rather than a bug:

- Respect `429` retry headers and cache public list/search responses (do not hammer the endpoint).
- Link users back to the canonical ClawHub listing.
- Do not mirror hidden, private, held, or moderation-blocked content outside the public API surface.

See [HTTP API](https://docs.openclaw.ai/clawhub/http-api) for endpoint details.

**Source**: OpenClaw documentation — `clawhub/troubleshooting` (mirror `inbox/openclaw_docs/clawhub/troubleshooting.md`)
**Last Updated**: 2026-06-22
**Status**: Active
