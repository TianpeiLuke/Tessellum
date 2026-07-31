---
tags:
  - resource
  - documentation
  - openclaw
  - nodes
  - capabilities
keywords:
  - openclaw nodes invoke
  - node command surface
  - canvas snapshot camera screen record
  - location sms android device commands
  - system.run system.which system.notify
  - exec node binding
  - node permissions map
  - node.invoke media attachment
topics:
  - OpenClaw
  - Node Capabilities
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/nodes
access_control_group: ["general"]
---

# OpenClaw — Node Capability and Command Surface (CLI Helpers)

## Overview

This note is the procedure-level reference for the OpenClaw **node command surface** — the device commands a paired node exposes (canvas, camera, screen recording, location, SMS, Android device/personal-data families, and node-host system commands) and the `openclaw nodes …` CLI helpers that invoke them. It mirrors the capability sections of the `nodes` source page (`Invoking commands` through `Permissions map`), reproducing every CLI command verbatim. Pairing/host setup is covered by `oc_nodes_pairing_host` and the two-gate command-policy/config schema is covered by `oc_nodes_command_policy`; this note focuses on WHAT each command does and HOW to invoke it.

## Invoking Commands

Node commands are reached either as low-level raw RPC or through higher-level CLI helpers. The low-level (raw RPC) form is `nodes invoke` (the canvas/snapshot/controls/A2UI helpers below are grouped into one block for density). Higher-level helpers exist for the common "give the agent a MEDIA attachment" workflows (canvas snapshot, camera, screen record, etc.), which write media into the agent transcript as MEDIA lines rather than requiring the operator to hand-build raw RPC params.

## Screenshots (Canvas Snapshots), Controls, and A2UI

If the node is showing the Canvas (WebView), `canvas.snapshot` returns `{ format, base64 }`; the snapshot CLI helper writes to a temp file and prints the saved path. Canvas presentation/scripting helpers drive the node's WebView, and A2UI helpers push or reset action-capable UI on the canvas:

```bash
# Raw RPC invoke
openclaw nodes invoke --node <idOrNameOrIp> --command canvas.eval --params '{"javaScript":"location.href"}'
# Snapshot
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format png
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format jpg --max-width 1200 --quality 0.9
# Controls
openclaw nodes canvas present --node <idOrNameOrIp> --target https://example.com
openclaw nodes canvas hide --node <idOrNameOrIp>
openclaw nodes canvas navigate https://example.com --node <idOrNameOrIp>
openclaw nodes canvas eval --node <idOrNameOrIp> --js "document.title"
# A2UI
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --text "Hello"
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --jsonl ./payload.jsonl
openclaw nodes canvas a2ui reset --node <idOrNameOrIp>
```

`canvas present` accepts URLs or local file paths (`--target`), plus optional `--x/--y/--width/--height` for positioning; `canvas eval` accepts inline JS (`--js`) or a positional arg. Mobile nodes use a bundled app-owned A2UI page for action-capable rendering. Only A2UI v0.8 JSONL is supported (v0.9/createSurface is rejected). iOS and Android render remote Gateway Canvas pages, but A2UI button actions are dispatched only from the bundled app-owned A2UI page — Gateway-hosted HTTP/HTTPS A2UI pages are render-only on those mobile clients.

## Photos + Videos (Node Camera)

Photos are returned as `jpg` (`camera snap` defaults to both facings = 2 MEDIA lines); video clips are returned as `mp4`:

```bash
openclaw nodes camera list --node <idOrNameOrIp>
openclaw nodes camera snap --node <idOrNameOrIp>            # default: both facings (2 MEDIA lines)
openclaw nodes camera snap --node <idOrNameOrIp> --facing front
openclaw nodes camera clip --node <idOrNameOrIp> --duration 10s
openclaw nodes camera clip --node <idOrNameOrIp> --duration 3000 --no-audio
```

The node must be **foregrounded** for `canvas.*` and `camera.*` (background calls return `NODE_BACKGROUND_UNAVAILABLE`). Clip duration is clamped (currently `<= 60s`) to avoid oversized base64 payloads. Android will prompt for `CAMERA`/`RECORD_AUDIO` permissions when possible; denied permissions fail with `*_PERMISSION_REQUIRED`.

## Screen Recordings (Nodes)

Supported nodes expose `screen.record` (mp4):

```bash
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10 --no-audio
```

`screen.record` availability depends on node platform. Screen recordings are clamped to `<= 60s`. `--no-audio` disables microphone capture on supported platforms. Use `--screen <index>` to select a display when multiple screens are available.

## Location (Nodes)

Nodes expose `location.get` when Location is enabled in settings:

```bash
openclaw nodes location get --node <idOrNameOrIp>
openclaw nodes location get --node <idOrNameOrIp> --accuracy precise --max-age 15000 --location-timeout 10000
```

Location is **off by default**. "Always" requires system permission; background fetch is best-effort. The response includes lat/lon, accuracy (meters), and timestamp.

## SMS (Android Nodes) and Android Device + Personal Data Commands

Android nodes can expose `sms.send` when the user grants **SMS** permission and the device supports telephony; the permission prompt must be accepted on the Android device before the capability is advertised, and Wi-Fi-only devices without telephony will not advertise `sms.send`. Android nodes can additionally advertise more command families when the corresponding capabilities are enabled. Available families: `device.status`, `device.info`, `device.permissions`, `device.health`; `device.apps` when Installed Apps sharing is enabled in Android Settings; `notifications.list`, `notifications.actions`; `photos.latest`; `contacts.search`, `contacts.add`; `calendar.events`, `calendar.add`; `callLog.search`; `sms.search`; and `motion.activity`, `motion.pedometer`. Example invokes (all are raw `nodes invoke` RPC):

```bash
openclaw nodes invoke --node <idOrNameOrIp> --command sms.send --params '{"to":"+15555550123","message":"Hello from OpenClaw"}'
openclaw nodes invoke --node <idOrNameOrIp> --command device.status --params '{}'
openclaw nodes invoke --node <idOrNameOrIp> --command device.apps --params '{"limit":10}'
openclaw nodes invoke --node <idOrNameOrIp> --command notifications.list --params '{}'
openclaw nodes invoke --node <idOrNameOrIp> --command photos.latest --params '{"limit":1}'
```

`device.apps` is opt-in and returns launcher-visible apps by default. Motion commands are capability-gated by available sensors.

## System Commands (Node Host / Mac Node)

The macOS node exposes `system.run`, `system.notify`, and `system.execApprovals.get/set`. The headless node host exposes `system.run`, `system.which`, and `system.execApprovals.get/set`. The `notify` and `which` helpers are the only `system.*` ones invocable through `nodes`; the trailing `config` commands bind exec to a node (see Exec Node Binding):

```bash
openclaw nodes notify --node <idOrNameOrIp> --title "Ping" --body "Gateway ready"
openclaw nodes invoke --node <idOrNameOrIp> --command system.which --params '{"name":"git"}'
# Exec node binding (global default, per-agent override, and unset)
openclaw config set tools.exec.node "node-id-or-name"
openclaw config get agents.list
openclaw config set 'agents.list[0].tools.exec.node' "node-id-or-name"
openclaw config unset tools.exec.node
openclaw config unset 'agents.list[0].tools.exec.node'
```

`system.run` returns stdout/stderr/exit code in the payload. Shell execution now goes through the `exec` tool with `host=node`; `nodes` remains the direct-RPC surface for explicit node commands. Critically, `nodes invoke` does **not** expose `system.run` or `system.run.prepare` — those stay on the exec path only. The exec path prepares a canonical `systemRunPlan` before approval; once an approval is granted, the gateway forwards that stored plan, not any later caller-edited command/cwd/session fields.

`system.notify` respects notification permission state on the macOS app and supports `--priority <passive|active|timeSensitive>` and `--delivery <system|overlay|auto>`. Unrecognized node `platform` / `deviceFamily` metadata uses a conservative default allowlist that excludes `system.run` and `system.which`; if those are intentionally needed for an unknown platform, add them explicitly via `gateway.nodes.allowCommands`. `system.run` supports `--cwd`, `--env KEY=VAL`, `--command-timeout`, and `--needs-screen-recording`. For shell wrappers (`bash|sh|zsh ... -c/-lc`), request-scoped `--env` values are reduced to an explicit allowlist (`TERM`, `LANG`, `LC_*`, `COLORTERM`, `NO_COLOR`, `FORCE_COLOR`). For allow-always decisions in allowlist mode, known dispatch wrappers (`env`, `flock`, `nice`, `nohup`, `stdbuf`, `timeout`) persist inner executable paths instead of wrapper paths; if unwrapping is not safe, no allowlist entry is persisted automatically. On Windows node hosts in allowlist mode, shell-wrapper runs via `cmd.exe /c` require approval (an allowlist entry alone does not auto-allow the wrapper form). Node hosts ignore `PATH` overrides and strip dangerous startup/shell keys (`DYLD_*`, `LD_*`, `BASHOPTS`, `FPATH`, `KSH_ENV`, `NODE_OPTIONS`, `NODE_REDIRECT_WARNINGS`, `NODE_REPL_EXTERNAL_MODULE`, `NODE_REPL_HISTORY`, `NODE_V8_COVERAGE`, `PYTHON*`, `PERL*`, `RUBYOPT`, `SHELLOPTS`, `PS4`, `TCLLIBPATH`); for extra PATH entries, configure the node host service environment instead of passing `PATH` via `--env`. On macOS node mode, `system.run` is gated by exec approvals in the macOS app (Settings → Exec approvals) — Ask/allowlist/full behave the same as the headless node host, and denied prompts return `SYSTEM_RUN_DENIED`. On the headless node host, `system.run` is gated by exec approvals at `~/.openclaw/exec-approvals.json`.

## Exec Node Binding

When multiple nodes are available, you can bind exec to a specific node, setting the default node for `exec host=node` (overridable per agent). The commands are shown in the System Commands block above: `openclaw config set tools.exec.node "node-id-or-name"` sets the global default node; `openclaw config set 'agents.list[0].tools.exec.node' "node-id-or-name"` sets a per-agent override (read the current list first with `openclaw config get agents.list`); and the matching `openclaw config unset` forms (global and per-agent) clear the binding to allow any node.

## Permissions Map

Nodes may include a `permissions` map in `node.list` / `node.describe`, keyed by permission name (e.g. `screenRecording`, `accessibility`) with boolean values (`true` = granted). This is how an operator or agent reads whether a capability (such as screen recording or accessibility) is actually granted on a given node before invoking the corresponding command.

**Source**: OpenClaw documentation — `nodes` (mirror `inbox/openclaw_docs/nodes.md`)
**Last Updated**: 2026-06-22
**Status**: Active
