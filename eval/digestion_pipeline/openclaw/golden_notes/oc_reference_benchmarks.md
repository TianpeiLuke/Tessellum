---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - benchmarks
keywords:
  - openclaw performance benchmarks
  - bench-model latency
  - bench-cli-startup
  - bench-gateway-startup
  - bench-gateway-restart
  - healthz vs readyz
  - built entry vs source runner baseline
  - sigusr1 in-process restart
topics:
  - OpenClaw
  - Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/test
access_control_group: ["general"]
---

# OpenClaw — Running the Performance Benchmarks (`bench-*`)

## Overview

This note is the procedure for running OpenClaw's four performance benchmark scripts, mirroring the four `bench-*` sections of the `reference/test` source page: **Model latency bench (local keys)**, **CLI startup bench**, **Gateway startup bench**, and **Gateway restart bench**. It covers each script's path, invocation (`pnpm tsx` / `pnpm test:*:bench` / `node --import tsx`), presets and case ids, the `/healthz`-vs-`/readyz` readiness semantics, the built-entry (`dist/entry.js`) versus source-runner (`scripts/run-node.mjs`) baseline discipline, and the timing/trace artifacts each bench emits. The test-running half of the same page (the `pnpm test*` lane catalog, Local PR gate, and Docker smokes) is the sibling note **[oc_reference_test_commands](oc_reference_test_commands.md)** and is NOT repeated here.

## Model latency bench (local keys)

The model-latency benchmark measures per-model request latency against local provider keys. Script: `scripts/bench-model.ts`. Run it with `pnpm tsx scripts/bench-model.ts --runs 10`. Optional environment variables are `MINIMAX_API_KEY`, `MINIMAX_BASE_URL`, `MINIMAX_MODEL`, and `ANTHROPIC_API_KEY`. The default prompt is verbatim: `"Reply with a single word: ok. No punctuation or extra text."`

The page records one example run for reference (2025-12-31, 20 runs): minimax median 1279ms (min 1114, max 2431) and opus median 2454ms (min 1224, max 3170). These are historical sample numbers, not a checked-in baseline.

## CLI startup bench

The CLI-startup benchmark times cold-start CLI commands. Script: `scripts/bench-cli-startup.ts`. It is driven either through `pnpm test:startup:bench*` package scripts or directly via `pnpm tsx scripts/bench-cli-startup.ts`. The documented invocations are:

```bash
pnpm test:startup:bench
pnpm test:startup:bench:smoke
pnpm test:startup:bench:save
pnpm test:startup:bench:update
pnpm test:startup:bench:check
pnpm tsx scripts/bench-cli-startup.ts
pnpm tsx scripts/bench-cli-startup.ts --runs 12
pnpm tsx scripts/bench-cli-startup.ts --preset real
pnpm tsx scripts/bench-cli-startup.ts --preset real --case status --case gatewayStatus --runs 3
pnpm tsx scripts/bench-cli-startup.ts --preset real --case tasksJson --case tasksListJson --case tasksAuditJson --runs 3
pnpm tsx scripts/bench-cli-startup.ts --entry openclaw.mjs --entry-secondary dist/entry.js --preset all
pnpm tsx scripts/bench-cli-startup.ts --preset all --output .artifacts/cli-startup-bench-all.json
pnpm tsx scripts/bench-cli-startup.ts --preset real --case gatewayStatusJson --output .artifacts/cli-startup-bench-smoke.json
pnpm tsx scripts/bench-cli-startup.ts --preset real --cpu-prof-dir .artifacts/cli-cpu
pnpm tsx scripts/bench-cli-startup.ts --json
```

The three presets select which commands are timed. `startup` runs `--version`, `--help`, `health`, `health --json`, `status --json`, `status`. `real` runs `health`, `status`, `status --json`, `sessions`, `sessions --json`, `tasks --json`, `tasks list --json`, `tasks audit --json`, `agents list --json`, `gateway status`, `gateway status --json`, `gateway health --json`, `config get gateway.port`. `all` runs both presets. Individual cases inside a preset are selected with repeated `--case <id>` flags (e.g. `--case status --case gatewayStatus`).

Output for each command includes `sampleCount`, avg, p50, p95, min/max, exit-code/signal distribution, and max RSS summaries. The optional `--cpu-prof-dir` / `--heap-prof-dir` flags write V8 profiles per run so that timing and profile capture use the same harness.

Saved-output conventions tie the package scripts to fixed artifact paths. `pnpm test:startup:bench:smoke` writes the targeted smoke artifact at `.artifacts/cli-startup-bench-smoke.json`. `pnpm test:startup:bench:save` writes the full-suite artifact at `.artifacts/cli-startup-bench-all.json` using `runs=5` and `warmup=1`. `pnpm test:startup:bench:update` refreshes the checked-in baseline fixture at `test/fixtures/cli-startup-bench.json` using `runs=5` and `warmup=1`. The checked-in fixture is `test/fixtures/cli-startup-bench.json`; refresh it with `pnpm test:startup:bench:update`, and compare current results against it with `pnpm test:startup:bench:check`.

## Gateway startup bench

The gateway-startup benchmark times the Gateway process coming up. Script: `scripts/bench-gateway-startup.ts`. The benchmark defaults to the built CLI entry at `dist/entry.js`; run `pnpm build` before using the package-script commands. To measure the source runner instead, pass `--entry scripts/run-node.mjs` and keep those results separate from built-entry baselines.

Usage:

```bash
pnpm test:startup:gateway -- --runs 5 --warmup 1
pnpm test:startup:gateway -- --case default --runs 10 --warmup 1
pnpm test:startup:gateway -- --case skipChannels --case fiftyPlugins --runs 5
node --import tsx scripts/bench-gateway-startup.ts --case default --runs 5 --output .artifacts/gateway-startup.json
node --import tsx scripts/bench-gateway-startup.ts --case default --runs 3 --cpu-prof-dir .artifacts/gateway-startup-cpu
```

The case ids select the startup scenario: `default` (normal Gateway startup), `skipChannels` (Gateway startup with channel startup skipped), `oneInternalHook` (one configured internal hook), `allInternalHooks` (all internal hooks), `fiftyPlugins` (50 manifest plugins), and `fiftyStartupLazyPlugins` (50 startup-lazy manifest plugins).

Output includes first process output, `/healthz`, `/readyz`, HTTP listen log time, Gateway ready log time, CPU time, CPU core ratio, max RSS, heap, startup trace metrics, event-loop delay, and plugin lookup-table detail metrics. The script enables `OPENCLAW_GATEWAY_STARTUP_TRACE=1` in the child Gateway environment.

The two readiness probes have distinct meanings and must not be conflated. Read `/healthz` as **liveness**: the HTTP server can answer. Read `/readyz` as **usable readiness**: startup plugin sidecars, channels, and ready-critical post-attach work have settled. Gateway startup hooks are dispatched asynchronously and are NOT part of the readiness guarantee. The internal ready log timestamp ("Ready log time") is useful for process-side attribution but is not a substitute for the external `/readyz` probe. Use JSON output or `--output` when comparing changes, and use `--cpu-prof-dir` only after the trace output points at import, compile, or CPU-bound work that cannot be explained from phase timings alone. Do not compare source-runner results with built `dist/entry.js` results as the same baseline.

## Gateway restart bench

The gateway-restart benchmark times an in-process Gateway restart. Script: `scripts/bench-gateway-restart.ts`. It is supported on macOS and Linux only: it uses SIGUSR1 for in-process restarts and fails immediately on Windows. Like the startup bench, it defaults to the built CLI entry at `dist/entry.js` (run `pnpm build` first when using the package-script commands), and measuring the source runner requires `--entry scripts/run-node.mjs` with results kept separate from built-entry baselines.

Usage:

```bash
pnpm test:restart:gateway -- --case skipChannels --runs 1 --restarts 5
pnpm test:restart:gateway -- --case default --runs 3 --restarts 3 --warmup 1
pnpm test:restart:gateway -- --case skipChannelsAcpxProbe --case skipChannelsNoAcpxProbe --runs 1 --restarts 5
node --import tsx scripts/bench-gateway-restart.ts --case fiftyPlugins --runs 1 --restarts 5 --output .artifacts/gateway-restart.json
node --import tsx scripts/bench-gateway-restart.ts --json
```

The case ids are: `skipChannels` (restart with channels skipped), `skipChannelsAcpxProbe` (restart with channels skipped and ACPX startup probe on), `skipChannelsNoAcpxProbe` (restart with channels skipped and ACPX startup probe off), `default` (normal restart), and `fiftyPlugins` (restart with 50 manifest plugins).

Output includes next `/healthz`, next `/readyz`, downtime, restart ready timing, CPU, RSS, startup trace metrics for the replacement process, and restart trace metrics for signal handling, active-work drain, close phases, next start, ready timing, and memory snapshots. The script enables both `OPENCLAW_GATEWAY_STARTUP_TRACE=1` and `OPENCLAW_GATEWAY_RESTART_TRACE=1` in the child Gateway environment.

Use this benchmark when a change touches restart signaling, close handlers, startup-after-restart, sidecar shutdown, service handoff, or readiness after restart. Start with `skipChannels` when isolating Gateway mechanics from channel startup, and use `default` or plugin-heavy cases only after the narrow case explains the restart path. Trace metrics are attribution hints, not verdicts: a restart change should be judged from multiple samples, the matching owner span, `/healthz` and `/readyz` behavior, and the user-visible restart contract.

**Source**: OpenClaw documentation — `reference/test` (mirror `inbox/openclaw_docs/reference/test.md`), the four `bench-*` sections
**Last Updated**: 2026-06-22
**Status**: Active
