---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - debugging
keywords:
  - openclaw debugging
  - gateway watch mode
  - raw stream logging
  - reasoning leakage
  - plugin lifecycle trace
  - cli startup profiling
  - dev profile dev gateway
  - openclaw debug trace verbose
  - vscode debug gateway
  - cpuprofile benchmark
topics:
  - OpenClaw
  - Debugging
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/debugging
access_control_group: ["general"]
---

# OpenClaw — Debugging Toolkit (Watch Mode, Traces, Raw Streams)

## Overview

This note is the procedure for debugging an OpenClaw Gateway/CLI, mirroring the `help/debugging` source page. It exists primarily to diagnose streaming output — especially when a provider mixes reasoning into normal text — and to give a repeatable workflow for iterating on the Gateway. It walks through the in-chat runtime overrides (`/debug`, `/trace`), the plugin-lifecycle phase trace, CLI startup and command profiling, Gateway watch mode (tmux + CPU benchmarking), the `--dev` dev profile/gateway, raw assistant-stream and raw OpenAI-compatible chunk logging, the safety rules for those logs, and attaching the VSCode debugger to the built Gateway.

## Runtime debug overrides and session trace output

Use `/debug` in chat to set **runtime-only** config overrides (memory, not disk). `/debug` is disabled by default; enable it with `commands.debug: true`. This is handy when you need to toggle obscure settings without editing `openclaw.json`; `/debug reset` clears all overrides and returns to the on-disk config. Separately, use `/trace` to see plugin-owned trace/debug lines in one session without turning on full verbose mode — for plugin diagnostics such as Active Memory debug summaries. Keep using `/verbose` for normal verbose status/tool output, and `/debug` for runtime-only config overrides. The in-chat commands:

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug unset messages.responsePrefix
/debug reset
/trace
/trace on
/trace off
```

## Plugin lifecycle trace

Use `OPENCLAW_PLUGIN_LIFECYCLE_TRACE=1` when plugin lifecycle commands feel slow and you need a built-in phase breakdown for plugin metadata, discovery, registry, runtime mirror, config mutation, and refresh work. The trace is opt-in and writes to stderr, so JSON command output remains parseable. Use this for plugin lifecycle investigation before reaching for a CPU profiler. If the command runs from a source checkout, prefer measuring the built runtime with `node dist/entry.js ...` after `pnpm build`; `pnpm openclaw ...` also measures source-runner overhead. Example output:

```text
$ OPENCLAW_PLUGIN_LIFECYCLE_TRACE=1 openclaw plugins install tokenjuice --force
[plugins:lifecycle] phase="config read" ms=6.83 status=ok command="install"
[plugins:lifecycle] phase="slot selection" ms=94.31 status=ok command="install" pluginId="tokenjuice"
[plugins:lifecycle] phase="registry refresh" ms=51.56 status=ok command="install" reason="source-changed"
```

## CLI startup and command profiling

Use the checked-in startup benchmark when a command feels slow. The source runner adds Node CPU profile flags and writes a `.cpuprofile` for the command via `OPENCLAW_RUN_NODE_CPU_PROF_DIR`; use this before adding temporary instrumentation to command code. For startup stalls that look like synchronous filesystem or module-loader work, add Node's sync I/O trace flag (`OPENCLAW_TRACE_SYNC_IO=1`) through the source runner. `pnpm gateway:watch` leaves `OPENCLAW_TRACE_SYNC_IO` disabled by default for the watched Gateway child; set it explicitly when you want Node sync I/O trace output in watch mode. The benchmark, profiling, and sync-I/O commands:

```bash
pnpm test:startup:bench:smoke
pnpm tsx scripts/bench-cli-startup.ts --preset real --case status --runs 3
pnpm tsx scripts/bench-cli-startup.ts --preset real --cpu-prof-dir .artifacts/cli-cpu
OPENCLAW_RUN_NODE_CPU_PROF_DIR=.artifacts/cli-cpu pnpm openclaw status
OPENCLAW_TRACE_SYNC_IO=1 pnpm openclaw gateway --force
```

## Gateway watch mode

For fast iteration, run the gateway under the file watcher with `pnpm gateway:watch`. By default this starts or restarts a tmux session named `openclaw-gateway-watch-main` (or a profile/port-specific variant such as `openclaw-gateway-watch-dev-19001`) and auto-attaches from interactive terminals. Non-interactive shells, CI, and agent exec calls stay detached and print attach instructions instead. The tmux pane runs the raw watcher `node scripts/watch-node.mjs gateway --force`. Use foreground mode (`pnpm gateway:watch:raw` or `OPENCLAW_GATEWAY_WATCH_TMUX=0`) when tmux is not wanted, and `OPENCLAW_GATEWAY_WATCH_ATTACH=0` to disable auto-attach while keeping tmux management. Profile watched Gateway CPU time with `pnpm gateway:watch --benchmark`: the watch wrapper consumes `--benchmark` before invoking the Gateway and writes one V8 `.cpuprofile` per Gateway child exit under `.artifacts/gateway-watch-profiles/`; stop or restart the watched gateway to flush the current profile, then open it with Chrome DevTools or Speedscope. The watch, attach, benchmark, and profile-open commands:

```bash
pnpm gateway:watch
tmux attach -t openclaw-gateway-watch-main
pnpm gateway:watch:raw
OPENCLAW_GATEWAY_WATCH_TMUX=0 pnpm gateway:watch
OPENCLAW_GATEWAY_WATCH_ATTACH=0 pnpm gateway:watch
pnpm gateway:watch --benchmark
npx speedscope .artifacts/gateway-watch-profiles/*.cpuprofile
```

Use `--benchmark-dir <path>` for a different profile output location, and `--benchmark-no-force` when you want the benchmarked child to skip the default `--force` port cleanup and fail fast if the Gateway port is already in use. Benchmark mode suppresses sync-I/O trace spam by default; set `OPENCLAW_TRACE_SYNC_IO=1` with `--benchmark` to get both CPU profiles and Node sync-I/O stack traces (those trace blocks are written to `gateway-watch-output.log` under the benchmark directory and filtered from the terminal pane; normal Gateway logs remain visible). The tmux wrapper carries common non-secret runtime selectors such as `OPENCLAW_PROFILE`, `OPENCLAW_CONFIG_PATH`, `OPENCLAW_STATE_DIR`, `OPENCLAW_GATEWAY_PORT`, and `OPENCLAW_SKIP_CHANNELS` into the pane. Put provider credentials in your normal profile/config, or use raw foreground mode for one-off ephemeral secrets. If the watched Gateway exits during startup, the watcher runs `openclaw doctor --fix --non-interactive` once and restarts the Gateway child; use `OPENCLAW_GATEWAY_WATCH_AUTO_DOCTOR=0` to get the original startup failure without the dev-only repair pass. The managed tmux pane defaults to colored Gateway logs; set `FORCE_COLOR=0` when starting `pnpm gateway:watch` to disable ANSI output. The watcher restarts on build-relevant files under `src/`, extension source files, extension `package.json` and `openclaw.plugin.json` metadata, `tsconfig.json`, `package.json`, and `tsdown.config.ts` — extension metadata changes restart the gateway without forcing a `tsdown` rebuild, while source and config changes still rebuild `dist` first. Any gateway CLI flags added after `gateway:watch` are passed through on each restart; re-running the same watch command respawns the named tmux pane, and the raw watcher keeps its single-watcher lock so duplicate watcher parents are replaced instead of piling up.

## Dev profile + dev gateway (`--dev`)

Use the dev profile to isolate state and spin up a safe, disposable setup for debugging. There are **two** `--dev` flags: the **global `--dev` (profile)** isolates state under `~/.openclaw-dev` and defaults the gateway port to `19001` (derived ports shift with it), while **`gateway --dev`** tells the Gateway to auto-create a default config + workspace when missing (and skip BOOTSTRAP.md). What the dev mode does: **(1) Profile isolation** (global `--dev`) sets `OPENCLAW_PROFILE=dev`, `OPENCLAW_STATE_DIR=~/.openclaw-dev`, `OPENCLAW_CONFIG_PATH=~/.openclaw-dev/openclaw.json`, and `OPENCLAW_GATEWAY_PORT=19001` (browser/canvas shift accordingly). **(2) Dev bootstrap** (`gateway --dev`) writes a minimal config if missing (`gateway.mode=local`, bind loopback), sets `agent.workspace` to the dev workspace, sets `agent.skipBootstrap=true` (no BOOTSTRAP.md), seeds the workspace files if missing (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`), uses the default identity **C3-PO** (protocol droid), and skips channel providers in dev mode (`OPENCLAW_SKIP_CHANNELS=1`). The `--reset` flow wipes config, credentials, sessions, and the dev workspace (using `trash`, not `rm`), then recreates the default dev setup. Because `--dev` is a **global** profile flag and gets eaten by some runners, use the env-var form to spell it out, and stop any already-running non-dev gateway (launchd or systemd) first. The recommended flow, reset flow, env-var form, and stop command:

```bash
pnpm gateway:dev
OPENCLAW_PROFILE=dev openclaw tui
pnpm gateway:dev:reset
OPENCLAW_PROFILE=dev openclaw gateway --dev --reset
openclaw gateway stop
```

If you don't have a global install yet, run the CLI via `pnpm openclaw ...`.

## Raw stream logging and raw OpenAI-compatible chunk logging

OpenClaw can log the **raw assistant stream** before any filtering/formatting — the best way to see whether reasoning is arriving as plain text deltas or as separate thinking blocks. Enable it via the `--raw-stream` CLI flag (with an optional `--raw-stream-path` override) or the equivalent env vars; the default file is `~/.openclaw/logs/raw-stream.jsonl`. To capture **raw OpenAI-compat chunks** before they are parsed into blocks, enable the transport logger with `OPENCLAW_RAW_STREAM=1` and optionally set `OPENCLAW_RAW_STREAM_PATH`; the default file for this transport logger is `~/.openclaw/logs/raw-openai-completions.jsonl`. The raw-stream CLI flags and env vars:

```bash
pnpm gateway:watch --raw-stream
pnpm gateway:watch --raw-stream --raw-stream-path ~/.openclaw/logs/raw-stream.jsonl
OPENCLAW_RAW_STREAM=1
OPENCLAW_RAW_STREAM_PATH=~/.openclaw/logs/raw-stream.jsonl
OPENCLAW_RAW_STREAM_PATH=~/.openclaw/logs/raw-openai-completions.jsonl
```

## Safety notes

Raw stream logs can include full prompts, tool output, and user data. Keep logs local and delete them after debugging. If you share logs, scrub secrets and PII first.

## Debugging in VSCode

Source maps are required to enable debugging in VSCode-based IDEs because many of the generated files end up with hashed names as part of the build process. The included `launch.json` configurations target the Gateway service but can be adapted quickly for other purposes: **Rebuild and Debug Gateway** debugs the Gateway service after creating a new build, and **Debug Gateway** debugs the Gateway service of a pre-existing build.

### Setup

The default **Rebuild and Debug Gateway** configuration is batteries-included — it automatically deletes the `/dist` folder and rebuilds the project with debugging enabled: open the **Run and Debug** panel from the Activity Bar or press `Ctrl`+`Shift`+`D`, ensure **Rebuild and Debug Gateway** is selected in the configuration dropdown, then press the **Start Debugging** button. Alternatively, to manage the build and debug processes manually: (1) open a terminal and enable source maps — `export OUTPUT_SOURCE_MAPS=1` on Linux/macOS, `$env:OUTPUT_SOURCE_MAPS="1"` on Windows (PowerShell), or `set OUTPUT_SOURCE_MAPS=1` on Windows (CMD); (2) in the same terminal rebuild with `pnpm clean:dist && pnpm build`; (3) in the IDE select **Debug Gateway** in the **Run and Debug** configuration dropdown and press **Start Debugging**. You can then set breakpoints in your TypeScript source files (`src/` directory) and the debugger will correctly map them to the compiled JavaScript via source maps, letting you inspect variables, step through code, and examine call stacks as expected.

### Notes

If using **Rebuild and Debug Gateway**, each debugger launch completely deletes the `/dist` folder and runs a full `pnpm build` with source maps enabled before starting the Gateway. If using **Debug Gateway**, debug sessions can be started and stopped at any time without affecting the `/dist` folder, but you must use a separate terminal process to both enable debugging and manage the build cycle. Modify the `launch.json` `args` setting to debug other sections of the project. If you need to use the built OpenClaw CLI for other tasks (e.g. `dashboard --no-open` if your debug session spawns a new auth token), execute it in another terminal as `node ./openclaw.mjs` or create a shell alias like `alias openclaw-build="node $(pwd)/openclaw.mjs"`.

**Source**: OpenClaw documentation — `help/debugging` (mirror `inbox/openclaw_docs/help/debugging.md`)
**Last Updated**: 2026-06-22
**Status**: Active
