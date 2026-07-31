---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - update
keywords:
  - openclaw update internals
  - channel install method alignment
  - staged npm install temporary prefix
  - managed-service handoff
  - update.run control-plane response
  - git checkout update steps
  - post-core plugin convergence
  - restart and verify gateway
topics:
  - OpenClaw
  - CLI Update Flow
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/update
access_control_group: ["general"]
---

# OpenClaw — How `openclaw update` Works Internally

## Overview

This note documents the internal mechanics half of the `openclaw update` command, mirroring the **What it does**, **Control-plane response shape**, and **Git checkout flow** sections of the `cli/update` source page. It covers how channel selection aligns the install method (dev git checkout vs stable/beta npm), the staged-npm install with verify-then-swap, the managed-service handoff and restart-and-verify sequence, the `update.run` control-plane response shapes and restart sentinel, and the 9-step git-checkout flow with mandatory post-core plugin convergence. The operator-facing command/option surface (usage, options, `status`/`repair`/`wizard`, `--update` shorthand) is its sibling [oc_cli_update_commands](oc_cli_update_commands.md).

## What it does — channel ↔ install-method alignment

When you switch channels explicitly (`--channel ...`), OpenClaw keeps the install method aligned with the channel:

- `dev` → ensures a git checkout (default: `~/openclaw`, or `$OPENCLAW_HOME/openclaw` when `OPENCLAW_HOME` is set; override with `OPENCLAW_GIT_DIR`), updates it, and installs the global CLI from that checkout.
- `stable` → installs from npm using `latest`.
- `beta` → prefers npm dist-tag `beta`, but falls back to `latest` when beta is missing or older than the current stable release.

The Gateway core auto-updater (when enabled via config) launches the CLI update path outside the live Gateway request handler. Control-plane `update.run` package-manager updates and supervised git-checkout updates also use a **managed-service handoff** instead of replacing the package tree or rebuilding `dist/` inside the live Gateway process. The Gateway starts a detached helper, exits, and the helper runs the normal `openclaw update --yes --json` CLI path from outside the Gateway process tree. If that handoff is unavailable, `update.run` returns a structured response with the safe shell command to run manually.

## Staged npm install (verify-then-swap)

For package-manager installs, `openclaw update` resolves the target package version before invoking the package manager. npm global installs use a **staged install**: OpenClaw installs the new package into a temporary npm prefix, verifies the packaged `dist` inventory there, then swaps that clean package tree into the real global prefix. If verification fails, post-update doctor, plugin sync, and restart work do not run from the suspect tree. Even when the installed version already matches the target, the command refreshes the global package install, then runs plugin sync, a core-command completion refresh, and restart work. This keeps packaged sidecars and channel-owned plugin records aligned with the installed OpenClaw build while leaving full plugin-command completion rebuilds to explicit `openclaw completion --write-state` runs.

## Managed-service stop, restart, and verify

When a local managed Gateway service is installed and restart is enabled, package-manager and git-checkout updates stop the running service before replacing the package tree or mutating the checkout/build output. The updater then refreshes the service metadata from the updated install, restarts the service, and verifies the restarted Gateway before reporting `Gateway: restarted and verified.`. Package-manager updates additionally verify the restarted Gateway reports the expected package version; git-checkout updates verify gateway health and service readiness after the rebuild. On macOS, the post-update check also verifies the LaunchAgent is loaded/running for the active profile and the configured loopback port is healthy. If the plist is installed but launchd is not supervising it, OpenClaw re-bootstraps the LaunchAgent automatically, then reruns the health/version/channel readiness checks. A fresh bootstrap loads the RunAtLoad job directly, so update recovery does not immediately `kickstart -k` the newly spawned Gateway. If the Gateway still does not become healthy, the command exits non-zero and prints the restart log path plus explicit restart, reinstall, and package rollback instructions. If restart cannot run, the command prints `Gateway: restart skipped (...)` or `Gateway: restart failed: ...` with a manual `openclaw gateway restart` hint. With `--no-restart`, package replacement or git rebuild still runs but the managed service is not stopped or restarted, so the running Gateway may keep old code until you restart it manually.

## Control-plane response shape (`update.run`)

When `update.run` is invoked through the Gateway control plane on a package-manager install or supervised git checkout, the handler reports the handoff initiation separately from the CLI update that continues after the Gateway exits:

- `ok: true`, `result.status: "skipped"`, `result.reason: "managed-service-handoff-started"`, and `handoff.status: "started"` mean the Gateway created the managed-service handoff and scheduled its own restart so the detached helper can run `openclaw update --yes --json` outside the live service process.
- `ok: false`, `result.reason: "managed-service-handoff-unavailable"`, and `handoff.status: "unavailable"` mean OpenClaw could not find a supervising service boundary and durable service identity for a safe handoff. For example, systemd handoff requires the OpenClaw unit identity (`OPENCLAW_SYSTEMD_UNIT`), not only ambient systemd process markers. The response includes `handoff.command`, the shell command to run from outside the Gateway.
- `ok: false`, `result.reason: "managed-service-handoff-failed"` means the Gateway tried to create the handoff but could not spawn the detached helper.

The `sentinel` payload is still written before the Gateway exits, and the CLI handoff updates the same restart sentinel after the managed-service restart health checks complete. During the handoff, the sentinel can carry `stats.reason: "restart-health-pending"` with no success continuation; the restarted Gateway keeps polling it and only fires the continuation after the CLI has verified service health and rewritten the sentinel with the final `ok` result. `openclaw status` and `openclaw status --all` show an `Update restart` row while that sentinel is pending or failed, and `update.status` refreshes and returns the latest sentinel.

## Git checkout flow

### Channel selection

- `stable`: checkout the latest non-beta tag, then build and doctor.
- `beta`: prefer the latest `-beta` tag, but fall back to the latest stable tag when beta is missing or older.
- `dev`: checkout `main`, then fetch and rebase.

### Update steps

The dev/git-checkout update proceeds through 9 `<Step>`s:

1. **Verify clean worktree** — requires no uncommitted changes.
2. **Switch channel** — switches to the selected channel (tag or branch).
3. **Fetch upstream** — dev only.
4. **Preflight build (dev only)** — runs the TypeScript build in a temp worktree. If the tip fails, walks back up to 10 commits to find the newest buildable commit. Set `OPENCLAW_UPDATE_PREFLIGHT_LINT=1` to also run lint during this preflight; lint runs in constrained serial mode because user update hosts are often smaller than CI runners.
5. **Rebase** — rebases onto the selected commit (dev only).
6. **Install dependencies** — uses the repo package manager. For pnpm checkouts, the updater bootstraps `pnpm` on demand (via `corepack` first, then a temporary `npm install pnpm@11` fallback) instead of running `npm run build` inside a pnpm workspace.
7. **Build Control UI** — builds the gateway and the Control UI.
8. **Run doctor** — `openclaw doctor` runs as the final safe-update check.
9. **Sync plugins** — syncs plugins to the active channel. Dev uses bundled plugins; stable and beta use npm. Updates tracked plugin installs.

### Beta-channel plugin fallback

On the beta update channel, tracked npm and ClawHub plugin installs that follow the default/latest line try a plugin `@beta` release first. If the plugin has no beta release, OpenClaw falls back to the recorded default/latest spec and reports that as a warning. For npm plugins, OpenClaw also falls back when the beta package exists but fails install validation. These plugin fallback warnings do not make the core update fail. Exact versions and explicit tags are not rewritten.

### Integrity-drift abort

If an exact pinned npm plugin update resolves to an artifact whose integrity differs from the stored install record, `openclaw update` aborts that plugin artifact update instead of installing it. Reinstall or update the plugin explicitly only after verifying that you trust the new artifact.

### Post-core convergence pass

Post-update plugin sync failures that are scoped to a managed plugin and that the sync path can route around (e.g. an unreachable npm registry for a non-essential plugin) are reported as warnings after the core update succeeds. The JSON result keeps the top-level update `status: "ok"` and reports `postUpdate.plugins.status: "warning"` with `openclaw update repair` and `openclaw plugins inspect <id> --runtime --json` guidance. Unexpected updater or sync exceptions still fail the update result. Fix the plugin install or update error, then rerun `openclaw update repair`.

After the per-plugin sync step, `openclaw update` runs a mandatory **post-core convergence** pass before the gateway is restarted: it repairs missing configured plugin payloads, validates each _active_ tracked install record on disk, and statically verifies its `package.json` is parseable (and any explicitly-declared `main` exists). Failures from this pass — and an invalid OpenClaw config snapshot — return `postUpdate.plugins.status: "error"` and flip the top-level update `status` to `"error"`, so `openclaw update` exits non-zero and the gateway is _not_ restarted with an unverified plugin set. The error includes structured `postUpdate.plugins.warnings[].guidance` lines pointing at `openclaw update repair` and `openclaw plugins inspect <id> --runtime --json` for follow-up. Disabled plugin entries and records that are not trusted-source-linked official sync targets are skipped here, mirroring the `skipDisabledPlugins` policy used by the missing-payload check, so a stale disabled plugin record cannot block an otherwise valid update.

When the updated Gateway starts, plugin loading is **verify-only**: startup does not run package managers or mutate dependency trees. Package-manager `update.run` restarts are handed to the CLI managed-service path, so the package swap happens outside the old Gateway process and the service health checks decide whether the update can be reported as complete. If pnpm bootstrap still fails, the updater stops early with a package-manager-specific error instead of trying `npm run build` inside the checkout.

**Source**: OpenClaw documentation — `cli/update` (mirror `inbox/openclaw_docs/cli/update.md`), internal-mechanics half (What it does, Control-plane response shape, Git checkout flow)
**Last Updated**: 2026-06-22
**Status**: Active
