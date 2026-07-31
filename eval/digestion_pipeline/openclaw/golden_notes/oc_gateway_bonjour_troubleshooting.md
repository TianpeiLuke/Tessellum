---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - bonjour
keywords:
  - openclaw bonjour troubleshooting
  - dns-sd debugging macos
  - bonjour docker gotchas
  - openclaw_disable_bonjour
  - bonjour common failure modes
  - escaped instance names \032
  - bonjour advertiser stuck probing
  - ios discovery debug logs
topics:
  - OpenClaw
  - Bonjour Discovery
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/bonjour
access_control_group: ["general"]
---

# OpenClaw — Troubleshooting Bonjour / DNS-SD Discovery

## Overview

This procedure note covers the debugging and failure-recovery half of OpenClaw's Bonjour (mDNS / DNS-SD) Gateway discovery, mirroring the troubleshooting sections of the `gateway/bonjour` source page. The companion setup note `oc_gateway_bonjour` documents how wide-area Bonjour, service types, TXT hint keys, and listener security are configured; this note picks up where discovery has gone wrong. It walks through built-in debugging on macOS (`dns-sd`), reading `bonjour:` lines in the Gateway log, capturing iOS-node discovery logs, the Docker bridge-networking gotchas that silently disable advertising, how to triage and recover when Bonjour is disabled, the documented common failure modes, and why DNS-SD instance names appear with escaped `\DDD` byte sequences (e.g. `\032` for a space).

## Debugging on macOS

macOS ships built-in DNS-SD tools for inspecting whether the Gateway beacon is visible on the LAN. Browse for advertised instances of the gateway service type:

```bash
dns-sd -B _openclaw-gw._tcp local.
```

Resolve a single discovered instance to its host/port (substitute the instance name printed by the browse command):

```bash
dns-sd -L "<instance>" _openclaw-gw._tcp local.
```

If browsing returns instances but resolving fails, you are usually hitting a LAN policy or mDNS resolver issue rather than an advertiser fault.

## Debugging in Gateway Logs

The Gateway writes a rolling log file whose path is printed on startup as `gateway log file: ...`. Look for `bonjour:` lines — the most diagnostic ones are: `bonjour: advertise failed ...`, `bonjour: suppressing ciao cancellation ...`, `bonjour: ... name conflict resolved` / `hostname conflict resolved`, `bonjour: watchdog detected non-announced service ...`, and `bonjour: disabling advertiser after ... failed restarts ...`.

The watchdog treats active `probing`, `announcing`, and fresh conflict-renames as in-progress states. If the service never reaches the `announced` state, OpenClaw eventually recreates the advertiser and, after repeated failures, **disables Bonjour for that Gateway process** instead of re-advertising forever.

Bonjour uses the system hostname for the advertised `.local` host when it is a valid DNS label. If the system hostname contains spaces, underscores, or another invalid DNS-label character, OpenClaw falls back to `openclaw.local`. Set `OPENCLAW_MDNS_HOSTNAME=<name>` before starting the Gateway when you need an explicit host label.

## Debugging on iOS Node

The iOS node uses `NWBrowser` to discover `_openclaw-gw._tcp`. To capture discovery logs, enable and copy them from the node app: go to Settings → Gateway → Advanced → **Discovery Debug Logs**, then Settings → Gateway → Advanced → **Discovery Logs** → reproduce the issue → **Copy**. The captured log includes browser state transitions and result-set changes, which show whether the node ever saw the beacon and how its browse state evolved.

## Docker Gotchas

The bundled Bonjour plugin **auto-disables LAN multicast advertising in detected containers** when `OPENCLAW_DISABLE_BONJOUR` is unset. Docker bridge networks usually do not forward mDNS multicast (`224.0.0.251:5353`) between the container and the LAN, so advertising from inside the container rarely makes discovery work.

Important gotchas to keep in mind:

- Bonjour auto-starts on macOS hosts and is opt-in elsewhere. Leaving it disabled does not stop the Gateway; it only skips LAN multicast advertising.
- Disabling Bonjour does not change `gateway.bind`; Docker still defaults to `OPENCLAW_GATEWAY_BIND=lan` so the published host port can work.
- Disabling Bonjour does not disable wide-area DNS-SD. Use wide-area discovery or Tailnet when the Gateway and node are not on the same LAN.
- Reusing the same `OPENCLAW_CONFIG_DIR` outside Docker does not persist the container auto-disable policy.
- Set `OPENCLAW_DISABLE_BONJOUR=0` only for host networking, macvlan, or another network where mDNS multicast is known to pass; set it to `1` to force-disable.

## Troubleshooting Disabled Bonjour

If a node no longer auto-discovers the Gateway after Docker setup, work through this sequence. First, confirm whether the Gateway is running in auto, forced-on, or forced-off mode:

```bash
docker compose config | grep OPENCLAW_DISABLE_BONJOUR
```

Second, confirm the Gateway itself is reachable through the published port (this isolates a discovery fault from a reachability fault):

```bash
curl -fsS http://127.0.0.1:18789/healthz
```

Third, use a direct target when Bonjour is disabled — Control UI or local tools at `http://127.0.0.1:18789`, LAN clients at `http://<gateway-host>:18789`, and cross-network clients via Tailnet MagicDNS, Tailnet IP, SSH tunnel, or wide-area DNS-SD.

Fourth, if you deliberately enabled the Bonjour plugin in Docker and forced advertising with `OPENCLAW_DISABLE_BONJOUR=0`, test multicast from the host:

```bash
dns-sd -B _openclaw-gw._tcp local.
```

If browsing is empty or the Gateway logs show repeated ciao watchdog cancellations, restore `OPENCLAW_DISABLE_BONJOUR=1` and use a direct or Tailnet route.

## Common Failure Modes

The source page documents these recurring discovery failures and their remedies:

- **Bonjour doesn't cross networks** — use Tailnet or SSH.
- **Multicast blocked** — some Wi-Fi networks disable mDNS.
- **Advertiser stuck in probing/announcing** — hosts with blocked multicast, container bridges, WSL, or interface churn can leave the ciao advertiser in a non-announced state. OpenClaw retries a few times and then disables Bonjour for the current Gateway process instead of restarting the advertiser forever.
- **Docker bridge networking** — Bonjour auto-disables in detected containers. Set `OPENCLAW_DISABLE_BONJOUR=0` only for host, macvlan, or another mDNS-capable network.
- **Sleep / interface churn** — macOS may temporarily drop mDNS results; retry.
- **Browse works but resolve fails** — keep machine names simple (avoid emojis or punctuation), then restart the Gateway. The service instance name derives from the host name, so overly complex names can confuse some resolvers.

## Escaped Instance Names (`\032`)

Bonjour/DNS-SD often escapes bytes in service instance names as decimal `\DDD` sequences (for example, spaces become `\032`). This is normal at the protocol level, not a fault. UIs should decode these escapes for display — the iOS node uses `BonjourEscapes.decode` to render the human-readable instance name.

**Source**: OpenClaw documentation — `gateway/bonjour` (mirror `inbox/openclaw_docs/gateway/bonjour.md`)
**Last Updated**: 2026-06-22
**Status**: Active
