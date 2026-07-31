---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - proxy
keywords:
  - openclaw proxy cli
  - managed proxy validate preflight
  - debug capture proxy
  - apns reachability probe
  - proxy ca file tls
  - allowed denied url
  - proxy query presets
  - OPENCLAW_PROXY_URL
topics:
  - OpenClaw
  - CLI Proxy
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/proxy
access_control_group: ["general"]
---

# OpenClaw — `openclaw proxy` (Managed-Proxy Validation + Debug Capture)

## Overview

This note is the operator procedure for `openclaw proxy`, mirroring the `cli/proxy` source page. The command has two jobs: (1) `validate` preflights an operator-managed forward proxy before OpenClaw proxy routing is enabled, and (2) the remaining subcommands (`start` / `run` / `coverage` / `sessions` / `query` / `blob` / `purge`) are transport-level debugging tools that run a local explicit debug proxy and inspect the traffic it captures. It covers the full subcommand surface, every `validate` flag (including the APNs reachability probe), the built-in query presets, and the operational notes (default host, managed-proxy direct-forwarding gate, exit code, and local-capture cleanup).

## Command Surface

The full subcommand list, copied verbatim from the source:

```bash
openclaw proxy start [--host <host>] [--port <port>]
openclaw proxy run [--host <host>] [--port <port>] -- <cmd...>
openclaw proxy validate [--json] [--proxy-url <url>] [--proxy-ca-file <path>] [--allowed-url <url>] [--denied-url <url>] [--apns-reachable] [--apns-authority <url>] [--timeout-ms <ms>]
openclaw proxy coverage
openclaw proxy sessions [--limit <count>]
openclaw proxy query --preset <name> [--session <id>]
openclaw proxy blob --id <blobId>
openclaw proxy purge
```

`start` launches a local explicit debug proxy. `run` starts a local debug proxy and then runs the command supplied after `--` with capture enabled. `sessions` lists capture sessions (`--limit <count>` caps how many). `query --preset <name>` runs a built-in traffic-pattern query (optionally scoped to one `--session <id>`). `blob --id <blobId>` reads a single captured blob. `coverage` and `purge` operate on the local capture store; `purge` deletes the local capture data. `validate` is the only non-debugging subcommand — it preflights the operator-managed proxy and does not capture traffic.

## `openclaw proxy validate` — Managed-Proxy Preflight

`openclaw proxy validate` checks the effective operator-managed proxy URL resolved from `--proxy-url`, config, or the `OPENCLAW_PROXY_URL` environment variable. Managed proxy URLs can use `http://` for a plain forward-proxy listener, or `https://` when OpenClaw must open TLS to the proxy endpoint before sending proxy requests. The command reports a config problem when no proxy is enabled and configured; use `--proxy-url` for a one-off preflight before changing config. Add `--proxy-ca-file` to trust a private CA for the TLS connection to an HTTPS proxy endpoint.

By default `validate` verifies two things: that a public destination succeeds through the proxy, and that the proxy *cannot* reach a temporary loopback canary (the loopback-denial check). Custom denied destinations are fail-closed — HTTP responses and ambiguous transport failures both fail unless you can verify a deployment-specific denial signal separately. The APNs reachability probe (`--apns-reachable`) additionally opens an APNs HTTP/2 CONNECT tunnel through the proxy and confirms sandbox APNs responds; because the probe deliberately uses an intentionally invalid provider token, an APNs `403 InvalidProviderToken` response is the *successful* reachability signal.

### `validate` flags

The flags, with source wording preserved:

- `--json` — print machine-readable JSON.
- `--proxy-url <url>` — validate this `http://` or `https://` proxy URL instead of config or env.
- `--proxy-ca-file <path>` — trust this PEM CA file for TLS verification of an HTTPS proxy endpoint.
- `--allowed-url <url>` — add a destination expected to succeed through the proxy. Repeat to check multiple destinations.
- `--denied-url <url>` — add a destination expected to be blocked by the proxy. Repeat to check multiple destinations.
- `--apns-reachable` — also verify sandbox APNs HTTP/2 is reachable through the proxy.
- `--apns-authority <url>` — APNs authority to probe with `--apns-reachable` (`https://api.sandbox.push.apple.com` by default; production is `https://api.push.apple.com`).
- `--timeout-ms <ms>` — per-request timeout in milliseconds.

The source page points to `/security/network-proxy` for deployment guidance and denial semantics (see Related Notes / References — those internals are linked, not duplicated here).

## Debug-Capture Query Presets

`openclaw proxy query --preset <name>` accepts these built-in preset names (verbatim):

- `double-sends`
- `retry-storms`
- `cache-busting`
- `ws-duplicate-frames`
- `missing-ack`
- `error-bursts`

These query the captured transport traffic for common anomaly patterns (duplicate sends, retry storms, cache-busting, duplicated WebSocket frames, missing acknowledgements, and bursts of errors). A preset query can be scoped to a single capture with `--session <id>`.

## Operational Notes

The source "Notes" section, preserved point-for-point:

- `start` defaults to `127.0.0.1` unless `--host` is set.
- `run` starts a local debug proxy and then runs the command after `--`.
- The debug proxy's direct upstream forwarding opens upstream sockets for diagnostics. When OpenClaw managed proxy mode is active, direct forwarding for proxy requests and CONNECT tunnels is disabled by default; set `OPENCLAW_DEBUG_PROXY_ALLOW_DIRECT_CONNECT_WITH_MANAGED_PROXY=1` only for approved local diagnostics.
- `validate` exits with code `1` when proxy config or destination checks fail.
- Captures are local debugging data; use `openclaw proxy purge` when finished.

**Source**: OpenClaw documentation — `cli/proxy` (mirror `inbox/openclaw_docs/cli/proxy.md`)
**Last Updated**: 2026-06-22
**Status**: Active
