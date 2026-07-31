---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - diagnostics
keywords:
  - openclaw diagnostics flags
  - opclaw_diagnostics env override
  - targeted debug logs subsystem
  - profiler reply.profiler codex.profiler
  - timeline jsonl openclaw.diagnostics.v1
  - logging.redactsensitive jsonl log
  - diagnostics wildcard flags
  - extract logs rg tail
topics:
  - OpenClaw
  - Diagnostics
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/diagnostics/flags
access_control_group: ["general"]
---

# OpenClaw — Diagnostics Flags (Targeted Debug Logs)

## Overview

This note is the operator/support procedure for OpenClaw's opt-in **diagnostics flags**: how to enable targeted, subsystem-scoped debug logs (and profiler/timeline timing spans) **without** raising global logging levels. Flags are opt-in and have no effect unless a subsystem checks them. It mirrors the `diagnostics/flags` source page end to end — flag syntax and wildcards, enabling via the `diagnostics.flags` config key versus the one-off `OPENCLAW_DIAGNOSTICS` env override, the `OPENCLAW_DIAGNOSTICS=0` process-level disable, the profiler flags (`profiler` / `reply.profiler` / `codex.profiler`), the `timeline` JSONL artifact and `openclaw.diagnostics.v1` envelope, where logs land (`/tmp/openclaw/openclaw-YYYY-MM-DD.log`, JSONL, `logging.redactSensitive` redaction), and the `rg` / `tail` extraction recipes.

## How It Works

Flags are strings and are case-insensitive. You can enable flags two ways: in config (the `diagnostics.flags` array) or via an env override (`OPENCLAW_DIAGNOSTICS`). Wildcards are supported: `telegram.*` matches `telegram.http`, and `*` enables all flags.

## Enable via Config

Add the flag(s) to the `diagnostics.flags` array in config:

```json
{
  "diagnostics": {
    "flags": ["telegram.http"]
  }
}
```

Multiple flags can be listed, including wildcards:

```json
{
  "diagnostics": {
    "flags": ["telegram.http", "brave.http", "gateway.*"]
  }
}
```

Restart the gateway after changing flags.

## Env Override (One-Off)

For a single run, set `OPENCLAW_DIAGNOSTICS` to a comma-separated list of flags instead of editing config:

```bash
OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload
```

`OPENCLAW_DIAGNOSTICS=0` is a process-level disable override: it disables flags from BOTH env and config for that process. This is the way to turn diagnostics off for one process even when config enables flags.

## Profiling Flags

Profiler flags enable targeted timing spans without raising global logging levels, and they are disabled by default. There are three relevant flags: `profiler` (all profiler-gated spans), `reply.profiler` (reply-dispatch spans only), and `codex.profiler` (Codex app-server startup/tool/thread spans only). Enable all profiler-gated spans for one gateway run:

```bash
OPENCLAW_DIAGNOSTICS=profiler openclaw gateway run
```

Enable only reply-dispatch profiler spans with `OPENCLAW_DIAGNOSTICS=reply.profiler openclaw gateway run`, or only Codex app-server startup/tool/thread profiler spans with `OPENCLAW_DIAGNOSTICS=codex.profiler openclaw gateway run`. To enable profiler flags from config, add them to `diagnostics.flags` (for example `["reply.profiler", "codex.profiler"]`) and restart the gateway. To disable a profiler flag, remove it from `diagnostics.flags` and restart. To temporarily disable every diagnostics flag even when config enables profiler flags, start the process with `OPENCLAW_DIAGNOSTICS=0 openclaw gateway run`.

## Timeline Artifacts

The `timeline` flag writes structured startup and runtime timing events for external QA harnesses. The timeline file path comes from `OPENCLAW_DIAGNOSTICS_TIMELINE_PATH`:

```bash
OPENCLAW_DIAGNOSTICS=timeline \
OPENCLAW_DIAGNOSTICS_TIMELINE_PATH=/tmp/openclaw-timeline.jsonl \
openclaw gateway run
```

You can also enable `timeline` in config via `diagnostics.flags: ["timeline"]`; the timeline file path still comes from `OPENCLAW_DIAGNOSTICS_TIMELINE_PATH`. When `timeline` is enabled only from config, the earliest config-loading spans are not emitted because OpenClaw has not read config yet; subsequent startup spans use the config flag. `OPENCLAW_DIAGNOSTICS=1`, `OPENCLAW_DIAGNOSTICS=all`, and `OPENCLAW_DIAGNOSTICS=*` also enable the timeline because they enable every diagnostics flag — prefer `timeline` when you only want the JSONL timing artifact. Timeline records use the `openclaw.diagnostics.v1` envelope; events can include process ids, phase names, span names, durations, plugin ids, dependency counts, event-loop delay samples, provider operation names, child-process exit state, and startup error names/messages. Treat timeline files as local diagnostics artifacts; review them before sharing outside your machine.

## Where Logs Go

Flags emit logs into the standard diagnostics log file. By default this is `/tmp/openclaw/openclaw-YYYY-MM-DD.log`. If you set `logging.file`, that path is used instead. Logs are JSONL (one JSON object per line), and redaction still applies based on `logging.redactSensitive`.

## Extract Logs

Pick the latest log file with `ls -t /tmp/openclaw/openclaw-*.log | head -n 1`, then filter for the subsystem you enabled. Filter for Telegram HTTP diagnostics with `rg "telegram http error" /tmp/openclaw/openclaw-*.log`, or for Brave Search HTTP diagnostics with `rg "brave http" /tmp/openclaw/openclaw-*.log`. To tail while reproducing an issue:

```bash
tail -f /tmp/openclaw/openclaw-$(date +%F).log | rg "telegram http error"
```

For remote gateways, you can also use `openclaw logs --follow` (see the `oc_cli_logs` note below).

## Notes

If `logging.level` is set higher than `warn`, these logs may be suppressed; the default `info` is fine. The `brave.http` flag logs Brave Search request URLs/query params, response status/timing, and cache hit/miss/write events — it does not log API keys or response bodies, but search queries can be sensitive. Flags are safe to leave enabled; they only affect log volume for the specific subsystem. Use the `oc_logging` note below to change log destinations, levels, and redaction.

**Source**: OpenClaw documentation — `diagnostics/flags` (mirror `inbox/openclaw_docs/diagnostics/flags.md`)
**Last Updated**: 2026-06-22
**Status**: Active
