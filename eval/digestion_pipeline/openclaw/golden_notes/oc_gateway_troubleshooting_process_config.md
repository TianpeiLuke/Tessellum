---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - troubleshooting
keywords:
  - openclaw gateway troubleshooting
  - gateway command ladder
  - split brain installs newer config guard
  - protocol mismatch after rollback
  - gateway service not running
  - macos maintenance sleep gateway crash
  - gateway high memory pressure oom
  - gateway rejected invalid config
  - gateway probe warnings
  - skill symlink path escape
topics:
  - OpenClaw
  - Gateway Troubleshooting
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/troubleshooting
access_control_group: ["general"]
---

# OpenClaw — Gateway Process & Config Troubleshooting Runbook

## Overview

This note is the gateway process/config cluster of the OpenClaw `gateway/troubleshooting` deep runbook — the symptom→command→fix flow used when the gateway binary, service, config, or version state is broken. It covers the command ladder, post-update recovery, the split-brain / newer-config-guard refusal, protocol-mismatch-after-rollback, skill-symlink path-escape, service-not-running, the macOS maintenance-sleep silent-stop pattern, high-memory/OOM exits, invalid-config rejection/repair, and `gateway probe` warnings. Auth/connectivity and message-flow/runtime symptoms live in the sibling cluster notes; the fast triage flow is `/help/troubleshooting`.

## Command ladder

Run these first, in this order:

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Expected healthy signals: `openclaw gateway status` shows `Runtime: running`, `Connectivity probe: ok`, and a `Capability: ...` line; `openclaw doctor` reports no blocking config/service issues; `openclaw channels status --probe` shows live per-account transport status and, where supported, probe/audit results (`works`, `audit ok`).

## After an update

Use this when an update finishes but the Gateway is down, channels are empty, or model calls fail with 401s. Run `openclaw status --all`, `openclaw update status --json`, `openclaw gateway status --deep`, `openclaw doctor --fix`, then `openclaw gateway restart`. Look for `Update restart` in `openclaw status` (pending/failed handoffs include the next command); `plugin load failed: dependency tree corrupted; run openclaw doctor --fix` under Channels means channel config exists but plugin registration failed before load; for provider 401s after re-auth, `openclaw doctor --fix` removes stale per-agent OAuth auth shadows so all agents resolve the current shared profile.

## Split brain installs and newer config guard

Use this when a gateway service unexpectedly stops after an update, or logs show one `openclaw` binary is older than the version that last wrote `openclaw.json`. OpenClaw stamps config writes with `meta.lastTouchedVersion`. Read-only commands can still inspect a config written by a newer OpenClaw, but process/service mutations refuse to continue from an older binary — blocked actions include service start/stop/restart/uninstall, forced reinstall, service-mode startup, and `gateway --force` port cleanup. Diagnose with `which openclaw`, `openclaw --version`, `openclaw gateway status --deep`, and `openclaw config get meta.lastTouchedVersion`.

To fix: (1) fix `PATH` so `openclaw` resolves to the newer install, then rerun; (2) reinstall the service with `openclaw gateway install --force` then `openclaw gateway restart`; (3) remove stale system-package or old wrapper entries pointing at an old `openclaw` binary. For intentional downgrade or emergency recovery only, set `OPENCLAW_ALLOW_OLDER_BINARY_DESTRUCTIVE_ACTIONS=1` for the single command and leave it unset otherwise.

## Protocol mismatch after rollback

Use this when logs keep printing `protocol mismatch` after a downgrade/rollback: an older Gateway is running but a newer local client keeps reconnecting with a protocol range the older Gateway cannot speak. Inspect with `openclaw --version`, `which -a openclaw`, `openclaw gateway status --deep`, `openclaw doctor --deep`, and `openclaw logs --follow`. Look for `protocol mismatch ... client=... v<version> min=<n> max=<n> expected=<n>` in Gateway logs; `Established clients:` in `gateway status --deep` or `Gateway clients` in `doctor --deep` (active TCP clients on the Gateway port, with PIDs/command lines when the OS allows); and a client whose command line points at the newer install/wrapper you rolled back from.

Fix: (1) stop/restart the stale client process shown by `gateway status --deep`; (2) restart apps/wrappers embedding OpenClaw (dashboards, editors, app-server helpers, long-running `logs --follow` shells); (3) re-run `gateway status --deep` or `doctor --deep` and confirm the stale PID is gone. Do not make an older Gateway accept a newer incompatible protocol — protocol bumps protect the wire contract; rollback recovery is a process/version cleanup problem.

## Skill symlink skipped as path escape

Use this when logs include `Skipping escaped skill path outside its configured root: ... reason=symlink-escape`. OpenClaw treats every skill root as a containment boundary: a symlink under `~/.agents/skills`, `<workspace>/.agents/skills`, `<workspace>/skills`, or `~/.openclaw/skills` is skipped when its real target resolves outside that root unless explicitly trusted. Inspect with `ls -l ~/.agents/skills/<name>`, `realpath ~/.agents/skills/<name>`, and `openclaw config get skills.load`. If the target is intentional, configure both the direct skill root and the allowed symlink target:

```json5
{
  skills: {
    load: {
      extraDirs: ["~/Projects/manager/skills"],
      allowSymlinkTargets: ["~/Projects/manager/skills"],
    },
  },
}
```

Then start a new session or let the skills watcher refresh; restart the gateway if the running process predates the change. Do not use broad targets (`~`, `/`, or a whole synced project folder) — keep `allowSymlinkTargets` scoped to the real skill root containing trusted `SKILL.md` directories. For Skill Workshop apply to write through those symlinked workspace skill paths, enable `skills.workshop.allowSymlinkTargetWrites`; keep it disabled for read-only shared roots.

## Gateway service not running

Use this when the service is installed but the process does not stay up:

```bash
openclaw gateway status
openclaw status
openclaw logs --follow
openclaw doctor
openclaw gateway status --deep   # also scan system-level services
```

Look for `Runtime: stopped` with exit hints; service config mismatch (`Config (cli)` vs `Config (service)`); port/listener conflicts; extra launchd/systemd/schtasks installs under `--deep`; and `Other gateway-like services detected (best effort)` cleanup hints. Common signatures and fixes:

- `Gateway start blocked: set gateway.mode=local` / `existing config is missing gateway.mode` → local mode not enabled or config clobbered; set `gateway.mode="local"` or re-run `openclaw onboard --mode local` / `openclaw setup` (Podman default config is `~/.openclaw/openclaw.json`).
- `refusing to bind gateway ... without auth` → non-loopback bind without a valid auth path (token/password, or trusted-proxy where configured).
- `another gateway instance is already listening` / `EADDRINUSE` → port conflict.
- `Other gateway-like services detected (best effort)` → stale/parallel launchd/systemd/schtasks units; keep one gateway per machine or isolate ports + config/state/workspace (`/gateway#multiple-gateways-same-host`).
- `System-level OpenClaw gateway service detected` from doctor → a systemd system unit exists while the user-level service is missing; remove/disable the duplicate, or set `OPENCLAW_SERVICE_REPAIR_POLICY=external` if the system unit is intended.
- `Gateway service port does not match current gateway config` → supervisor still pins the old `--port`; run `openclaw doctor --fix` or `openclaw gateway install --force`, then restart.

## macOS gateway silently stops responding, then resumes when you touch the dashboard

Use this when channels on a macOS host go quiet for minutes to hours and the gateway appears to recover the moment you open the Control UI or SSH in — usually with no `openclaw status` symptom by then:

```bash
ls ~/.openclaw/logs/stability/ | tail -5
openclaw gateway stability --bundle latest
pmset -g log | grep -iE "sleep|wake|maintenance" | tail -50
launchctl print gui/$UID/ai.openclaw.gateway | grep -E "state|last exit|runs"
```

Look for `*-uncaught_exception.json` bundles in `~/.openclaw/logs/stability/` with `error.code` a transient network code (`ENETDOWN`, `ENETUNREACH`, `EHOSTUNREACH`, `ECONNREFUSED`) and a call stack into Node `net` `lookupAndConnect` / `Socket.connect`; `pmset -g log` lines like `Entering Sleep state due to 'Maintenance Sleep'` or `en0 driver is slow (msg: WillChangeState to 0)` aligned with crash timestamps (Power Nap / Maintenance Sleep briefly puts the Wi-Fi driver into state 0, so an outbound `connect()` then fails with `ENETDOWN`); and `launchctl print` showing `state = not running` with multiple recent `runs` and an exit code, especially when the crash-to-relaunch gap is ~an hour (launchd applies an undocumented respawn-protection gate after a crash burst that stops honoring `KeepAlive=true` until an external trigger re-arms it). OpenClaw `2026.5.26`+ classify these as benign so they no longer reach the top-level uncaught handler; clean shutdowns log `received SIG*; shutting down` in `~/Library/Logs/openclaw/gateway.log` while transient crashes do not.

What to do: (1) upgrade if before `2026.5.26` — afterward `ENETDOWN` logs a warning instead of terminating; (2) reduce maintenance sleep on always-on Mac hosts with `sudo pmset -a sleep 0 disksleep 0 standby 0 powernap 0` (reduces but does not eliminate the flap); (3) add a liveness watchdog to catch a crash burst parked by launchd:

```bash
# launchd-aware liveness check (run from a 5-minute cron or LaunchAgent)
state=$(launchctl print gui/$UID/ai.openclaw.gateway 2>/dev/null | awk -F'= ' '/state =/ {print $2; exit}')
if [ "$state" != "running" ]; then
  launchctl kickstart -k gui/$UID/ai.openclaw.gateway
fi
```

This externally re-arms the respawn gate — `KeepAlive=true` alone is insufficient on macOS after a crash burst.

## Gateway exits during high memory use

Use this when the Gateway disappears under load, the supervisor reports an OOM-style restart, or logs mention `critical memory pressure bundle written`. Inspect with `openclaw gateway status --deep`, `openclaw logs --follow`, `openclaw gateway stability --bundle latest`, and `openclaw gateway diagnostics export`. Look for `Reason: diagnostic.memory.pressure.critical`; `Memory pressure:` with `critical/rss_threshold`, `critical/heap_threshold`, or `critical/rss_growth`; `V8 heap:` near the limit; `Largest session files:` like `agents/<agent>/sessions/<session>.jsonl`; and Linux cgroup counters inside a container.

Common signatures: `critical memory pressure bundle written` shortly before restart → a pre-OOM bundle was captured (inspect with `openclaw gateway stability --bundle latest`); `memory pressure: level=critical ... memoryPressureSnapshot=disabled` → pressure detected but the snapshot is off; `Largest session files:` at a huge redacted transcript → reduce retained history or move old transcripts out before restarting; `V8 heap:` near the limit → lower prompt/session pressure, reduce concurrency, or raise the Node heap limit only after confirming the workload; `critical/rss_growth` → memory grew fast in one window (check logs for a large import, runaway tool output, retries, or queued work); critical pressure but no bundle → the default — set `diagnostics.memoryPressureSnapshot: true` to capture it next time. The bundle is payload-free (operational memory evidence + redacted relative paths only — no message text, credentials, tokens, cookies, or session ids); attach the diagnostics export to bug reports instead of raw logs.

## Gateway rejected invalid config

Use this when Gateway startup fails with `Invalid config` or hot reload logs say it skipped an invalid edit. Run `openclaw logs --follow`, `openclaw config file`, `openclaw config validate`, and `openclaw doctor`. Look for `Invalid config at ...`; `config reload skipped (invalid config): ...`; `Config write rejected: ...`; a timestamped `openclaw.json.rejected.*` file beside the active config; and a timestamped `openclaw.json.clobbered.*` file if `doctor --fix` repaired a broken direct edit. OpenClaw keeps the latest 32 `.clobbered.*` files for each config path and rotates older ones.

What happened: validation failed during startup, hot reload, or an OpenClaw-owned write. Startup fails closed instead of rewriting `openclaw.json`; hot reload skips invalid external edits; owned writes reject invalid/destructive payloads before commit and save `.rejected.*`. `openclaw doctor --fix` owns repair — removing non-JSON prefixes or restoring last-known-good while preserving the rejected payload as `.clobbered.*`. Inspect and repair:

```bash
CONFIG="$(openclaw config file)"
ls -lt "$CONFIG".clobbered.* "$CONFIG".rejected.* 2>/dev/null | head
diff -u "$CONFIG" "$(ls -t "$CONFIG".clobbered.* 2>/dev/null | head -n 1)"
openclaw config validate
openclaw doctor
```

Common signatures: `.clobbered.*` → doctor preserved a broken external edit while repairing; `.rejected.*` → an owned write failed schema/clobber checks before commit; `Config write rejected:` → the write tried to drop required shape, shrink the file, or persist invalid config; `config reload skipped (invalid config):` → a direct edit failed validation and was ignored; `Invalid config at ...` → startup failed before services booted; `missing-meta-vs-last-good`, `gateway-mode-missing-vs-last-good`, `size-drop-vs-last-good:*` → a write lost fields or size vs last-known-good; `Config last-known-good promotion skipped` → the candidate held redacted secret placeholders (`***`). Fix: (1) `openclaw doctor --fix` to repair prefixed/clobbered config or restore last-known-good; (2) copy only the intended keys from `.clobbered.*`/`.rejected.*` and apply with `openclaw config set` / `config.patch`; (3) `openclaw config validate` before restarting; (4) when editing by hand keep the full JSON5 config, not just the partial object.

## Gateway probe warnings

Use this when `openclaw gateway probe` reaches something but still prints a warning block. Run `openclaw gateway probe`, `openclaw gateway probe --json`, and `openclaw gateway probe --ssh user@gateway-host`; look for `warnings[].code` and `primaryTargetId` in JSON. Common signatures:

- `SSH tunnel failed to start; falling back to direct probes.` → SSH setup failed; the command still tried direct configured/loopback targets.
- `multiple reachable gateway identities detected` → distinct gateways answered, or OpenClaw could not prove reachable targets are the same gateway (one gateway reached via SSH tunnel / proxy / remote URL counts as one with multiple transports, even on different ports).
- `Read-probe diagnostics are limited by gateway scopes (missing operator.read)` → connect worked but detail RPC is scope-limited; pair device identity or use `operator.read` credentials.
- `Gateway accepted the WebSocket connection, but follow-up read diagnostics failed` → reachable Gateway, degraded diagnostics; compare `connect.ok` and `connect.rpcOk` in `--json`.
- `Capability: pairing-pending` or `gateway closed (1008): pairing required` → the gateway answered but this client needs pairing/approval.
- unresolved `gateway.auth.*` / `gateway.remote.*` SecretRef text → auth material was unavailable in this command path for the failed target.

**Source**: OpenClaw documentation — `gateway/troubleshooting` (process/config cluster; mirror `inbox/openclaw_docs/gateway/troubleshooting.md`)
**Last Updated**: 2026-06-22
**Status**: Active
