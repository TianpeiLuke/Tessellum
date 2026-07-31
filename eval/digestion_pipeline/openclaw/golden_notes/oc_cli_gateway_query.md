---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - gateway
keywords:
  - openclaw gateway query
  - gateway probe status
  - gateway health usage-cost stability
  - gateway call rpc method
  - gateway discover bonjour
  - websocket rpc query
  - probe capability classification
  - remote over ssh port-forward
topics:
  - OpenClaw
  - Gateway CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/gateway
access_control_group: ["general"]
---

# OpenClaw — Querying and Discovering a Running Gateway (`openclaw gateway`)

## Overview

This note is the procedure for querying, diagnosing, and discovering an already-running OpenClaw Gateway over WebSocket RPC, mirroring the "Query a running Gateway" and "Discover gateways (Bonjour)" sections of the `cli/gateway` source page. It covers output/auth/shared options for all query commands; the read-only diagnostic subcommands `gateway health`, `gateway usage-cost`, `gateway stability`, `gateway diagnostics export`, `gateway status`, and `gateway probe` (including capability classification, warning codes, and the SSH port-forward parity mode); the low-level `gateway call <method>` RPC helper; and the `gateway discover` Bonjour scan with its mDNS/wide-area DNS-SD beacons and TXT hints. The Gateway is OpenClaw's WebSocket server for channels, nodes, sessions, and hooks; running/restarting/installing the process is the sibling concern documented in `oc_cli_gateway_run`.

## Shared Options and Output Modes

All query commands use WebSocket RPC. The available **output modes** are: default human-readable (colored in TTY); `--json` for machine-readable JSON (no styling/spinner); and `--no-color` (or `NO_COLOR=1`) to disable ANSI while keeping the human layout. The **shared options** common across commands are `--url <url>` (Gateway WebSocket URL), `--token <token>`, `--password <password>`, `--timeout <ms>` (timeout/budget, varies per command), and `--expect-final` (wait for a "final" response on agent calls). A load-bearing credential rule applies: when you set `--url`, the CLI does **not** fall back to config or environment credentials — you must pass `--token` or `--password` explicitly, and missing explicit credentials is an error.

## `gateway health`

```bash
openclaw gateway health --url ws://127.0.0.1:18789
```

The HTTP `/healthz` endpoint is a **liveness** probe: it returns once the server can answer HTTP. The HTTP `/readyz` endpoint is stricter and stays red while startup plugin sidecars, channels, or configured hooks are still settling. Local or authenticated detailed-readiness responses include an `eventLoop` diagnostic block carrying event-loop delay, event-loop utilization, CPU core ratio, and a `degraded` flag. (The standalone `openclaw health` CLI overlaps this; see `oc_cli_health`.)

## `gateway usage-cost`

Fetch usage-cost summaries from session logs (`openclaw gateway usage-cost`, with `--json` for machine output). The `--days <days>` option (default `30`) sets the number of days to include, e.g. `openclaw gateway usage-cost --days 7`.

## `gateway stability`

Fetch the recent diagnostic stability recorder from a running Gateway. Options: `--limit <limit>` (default `25`, max `1000`) caps the number of recent events; `--type <type>` filters by diagnostic event type such as `payload.large` or `diagnostic.memory.pressure`; `--since-seq <seq>` includes only events after a diagnostic sequence number; `--bundle [path]` reads a persisted stability bundle instead of calling the running Gateway (use `--bundle latest`, or just `--bundle`, for the newest bundle under the state directory, or pass a bundle JSON path directly); `--export` writes a shareable support diagnostics zip instead of printing details; and `--output <path>` is the output path for `--export`.

```bash
openclaw gateway stability --type payload.large
openclaw gateway stability --bundle latest --export
```

**Privacy and bundle behavior.** Records keep operational metadata — event names, counts, byte sizes, memory readings, queue/session state, channel/plugin names, and redacted session summaries — but do **not** keep chat text, webhook bodies, tool outputs, raw request/response bodies, tokens, cookies, secret values, hostnames, or raw session ids. Set `diagnostics.enabled: false` to disable the recorder entirely. On fatal Gateway exits, shutdown timeouts, and restart-startup failures, OpenClaw writes the same diagnostic snapshot to `~/.openclaw/logs/stability/openclaw-stability-*.json` when the recorder has events; inspect the newest bundle with `openclaw gateway stability --bundle latest` (`--limit`, `--type`, and `--since-seq` also apply to bundle output).

## `gateway diagnostics export`

Write a local diagnostics zip designed to attach to bug reports (`openclaw gateway diagnostics export --output openclaw-diagnostics.zip --json`; for the privacy model and contents, see `/gateway/diagnostics`). Options: `--output <path>` (zip path; defaults to a support export under the state directory), `--log-lines <count>` (default `5000`, max sanitized log lines), `--log-bytes <bytes>` (default `1000000`, max log bytes to inspect), `--url`/`--token`/`--password` for the health snapshot, `--timeout <ms>` (default `3000`, status/health snapshot timeout), `--no-stability-bundle` (skip persisted bundle lookup), and `--json` (print the written path, size, and manifest as JSON).

The export contains a manifest, a Markdown summary, config shape, sanitized config details, sanitized log summaries, sanitized Gateway status/health snapshots, and the newest stability bundle when one exists. It is meant to be shared: it keeps operational details (safe OpenClaw log fields, subsystem names, status codes, durations, configured modes, ports, plugin ids, provider ids, non-secret feature settings, redacted operational log messages) but omits or redacts chat text, webhook bodies, tool outputs, credentials, cookies, account/message identifiers, prompt/instruction text, hostnames, and secret values. When a LogTape-style message looks like user/chat/tool payload text, the export keeps only that a message was omitted plus its byte count.

## `gateway status`

`gateway status` shows the Gateway service (launchd/systemd/schtasks) plus an optional probe of connectivity/auth capability (`openclaw gateway status --json`, `openclaw gateway status --require-rpc`). Options: `--url <url>` (add an explicit probe target; configured remote + localhost are still probed), `--token`/`--password` (probe auth), `--timeout <ms>` (default `10000`, probe timeout), `--no-probe` (service-only view), `--deep` (scan system-level services too), and `--require-rpc` (upgrade the default connectivity probe to a read probe and exit non-zero when that read probe fails — cannot be combined with `--no-probe`).

**Status semantics.** `gateway status` stays available for diagnostics even when the local CLI config is missing or invalid. The default proves service state, WebSocket connect, and the auth capability visible at handshake time — it does **not** prove read/write/admin operations. Diagnostic probes are non-mutating for first-time device auth: they reuse an existing cached device token when one exists, but do not create a new CLI device identity or read-only device pairing record just to check status. The command resolves configured auth SecretRefs for probe auth when possible; if a required auth SecretRef is unresolved in this command path, `gateway status --json` reports `rpc.authWarning` when probe connectivity/auth fails (pass `--token`/`--password` explicitly or resolve the secret source first), and if the probe succeeds, unresolved auth-ref warnings are suppressed to avoid false positives. When probing is enabled, JSON output includes `gateway.version` when the running Gateway reports it; `--require-rpc` can fall back to the `status.runtimeVersion` RPC payload if the follow-up handshake probe cannot provide version metadata. Use `--require-rpc` in scripts/automation when a listening service is not enough and read-scope RPC calls must be healthy too. `--deep` adds a best-effort scan for extra launchd/systemd/schtasks installs (printing cleanup hints and warning that most setups should run one gateway per machine), reports a recent Gateway supervisor restart handoff when the service process exited cleanly for an external supervisor restart, and runs config validation in plugin-aware mode (`pluginValidation: "full"`) to surface configured plugin manifest warnings; the default fast read-only path skips plugin validation. Human output includes the resolved file log path plus the CLI-vs-service config paths/validity snapshot to help diagnose profile or state-dir drift. On Linux systemd installs, service auth-drift checks read both `Environment=` and `EnvironmentFile=` values from the unit (including `%h`, quoted paths, multiple files, and optional `-` files), resolve `gateway.auth.token` SecretRefs using merged runtime env (service command env first, then process env fallback), and skip config token resolution when token auth is not effectively active.

## `gateway probe`

`gateway probe` is the "debug everything" command. It always probes your configured remote gateway (if set) **and** localhost (loopback) even if remote is configured; passing `--url` adds that explicit target ahead of both. Human output labels targets as `URL (explicit)`, `Remote (configured)` or `Remote (configured, inactive)`, and `Local loopback`. If multiple probe targets are reachable, it prints all of them; an SSH tunnel, TLS/proxy URL, and configured remote URL can all point at the same gateway even when their transport ports differ, and `multiple_gateways` is reserved for distinct or identity-ambiguous reachable gateways (multiple gateways are supported with isolated profiles such as a rescue bot, but most installs run a single gateway).

```bash
openclaw gateway probe
openclaw gateway probe --json
```

**Interpretation.** `Reachable: yes` means at least one target accepted a WebSocket connect. `Capability: read-only|write-capable|admin-capable|pairing-pending|connect-only` reports what the probe could prove about auth (separate from reachability). `Read probe: ok` means read-scope detail RPC calls (`health`/`status`/`system-presence`/`config.get`) also succeeded; `Read probe: limited - missing scope: operator.read` means connect succeeded but read-scope RPC is limited (reported as **degraded** reachability, not full failure); `Read probe: failed` after `Connect: ok` means the WebSocket connected but follow-up read diagnostics timed out or failed (also **degraded**, not unreachable). Like `gateway status`, probe reuses existing cached device auth but does not create first-time device identity or pairing state. Exit code is non-zero only when no probed target is reachable.

**JSON output (top level):** `ok` (at least one target reachable); `degraded` (at least one target connected but did not complete full detail RPC diagnostics); `capability` (best capability seen across reachable targets — `read_only`, `write_capable`, `admin_capable`, `pairing_pending`, `connected_no_operator_scope`, or `unknown`); `primaryTargetId` (best winner in order: explicit URL, SSH tunnel, configured remote, then local loopback); `warnings[]` (records with `code`, `message`, optional `targetIds`); `network` (loopback/tailnet URL hints); and `discovery.timeoutMs` / `discovery.count` (the actual discovery budget/result count for this probe pass). Per target, `targets[].connect` carries `ok` (reachability after connect + degraded classification), `rpcOk` (full detail RPC success), and `scopeLimited` (detail RPC failed due to missing operator scope); `targets[].auth` carries `role` (auth role in `hello-ok` when available), `scopes` (granted scopes in `hello-ok`), and `capability` (surfaced auth capability for that target). **Common warning codes:** `ssh_tunnel_failed` (SSH tunnel setup failed; fell back to direct probes), `multiple_gateways` (distinct gateway identities reachable, or OpenClaw could not prove they are the same gateway), `auth_secretref_unresolved` (a configured auth SecretRef could not be resolved for a failed target), and `probe_scope_limited` (WebSocket connect succeeded but the read probe was limited by missing `operator.read`).

### Remote over SSH (Mac app parity)

The macOS app "Remote over SSH" mode uses a local port-forward so a remote gateway bound to loopback only becomes reachable at `ws://127.0.0.1:<port>`. The CLI equivalent passes `--ssh`:

```bash
openclaw gateway probe --ssh user@gateway-host
```

Options: `--ssh <target>` (`user@host` or `user@host:port`, port defaults to `22`), `--ssh-identity <path>` (identity file), and `--ssh-auto` (pick the first discovered gateway host as SSH target from the resolved discovery endpoint — `local.` plus the configured wide-area domain, if any; TXT-only hints are ignored). Optional config defaults: `gateway.remote.sshTarget` and `gateway.remote.sshIdentity`.

## `gateway call <method>`

Low-level RPC helper for invoking a Gateway RPC method directly.

```bash
openclaw gateway call status
openclaw gateway call logs.tail --params '{"sinceMs": 60000}'
```

Options: `--params <json>` (default `{}`, JSON object string for params — must be valid JSON), `--url <url>`, `--token <token>`, `--password <password>`, `--timeout <ms>` (timeout budget), `--expect-final` (mainly for agent-style RPCs that stream intermediate events before a final payload), and `--json` (machine-readable JSON output). The `logs.tail` method shown here is the same RPC that `openclaw logs` wraps (see `oc_cli_logs`).

## Discover gateways (Bonjour)

`gateway discover` scans for Gateway beacons (`_openclaw-gw._tcp`) over multicast DNS-SD (`local.`) and unicast DNS-SD / Wide-Area Bonjour (choose a domain, for example `openclaw.internal.`, and set up split DNS plus a DNS server; see `/gateway/bonjour`). Only gateways with Bonjour discovery enabled (the default) advertise the beacon. Wide-area discovery records can include these TXT hints: `role` (gateway role hint), `transport` (transport hint, e.g. `gateway`), `gatewayPort` (WebSocket port, usually `18789`), `sshPort` (full discovery mode only; clients default SSH targets to `22` when it is absent), `tailnetDns` (MagicDNS hostname, when available), `gatewayTls` / `gatewayTlsSha256` (TLS enabled + cert fingerprint), and `cliPath` (full discovery mode only).

```bash
openclaw gateway discover
openclaw gateway discover --json | jq '.beacons[].wsUrl'
```

Options: `--timeout <ms>` (default `2000`, per-command browse/resolve timeout) and `--json` (machine-readable output, also disables styling/spinner). The CLI scans `local.` plus the configured wide-area domain when one is enabled; `wsUrl` in JSON output is derived from the resolved service endpoint, not from TXT-only hints such as `lanHost` or `tailnetDns`; and on both `local.` mDNS and wide-area DNS-SD, `sshPort` and `cliPath` are only published when `discovery.mdns.mode` is `full`.

**Source**: OpenClaw documentation — `cli/gateway` (mirror `inbox/openclaw_docs/cli/gateway.md`), "Query a running Gateway" + "Discover gateways (Bonjour)" sections
**Last Updated**: 2026-06-22
**Status**: Active
