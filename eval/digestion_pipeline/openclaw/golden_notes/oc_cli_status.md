---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - diagnostics
keywords:
  - openclaw status command
  - status deep live probes
  - status usage provider windows
  - execution vs runtime
  - transcript fallback model label
  - session model pin override
  - read-only secretref resolution
  - status all secrets overview
topics:
  - OpenClaw
  - CLI Diagnostics
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/status
access_control_group: ["general"]
---

# OpenClaw — `openclaw status` CLI Diagnostics

## Overview

This note documents the `openclaw status` CLI command: a diagnostics surface for channels and sessions that prints channel health, recent session recipients, usage snapshots, and runtime/uptime overview information. It mirrors the `cli/status` source page, covering the four invocation forms (plain, `--all`, `--deep`, `--usage`), the fast read-only path versus deep live probes, the `Execution:` vs `Runtime:` distinction, transcript fallback for token/cache/model labels, session model-pin display, and read-only SecretRef resolution with degraded-output behavior. It is a procedure note: how to run the command and how to read what each mode reports.

## Purpose and Invocation

`openclaw status` produces diagnostics for channels + sessions. The four documented invocations are:

```bash
openclaw status
openclaw status --all
openclaw status --deep
openclaw status --usage
```

Plain `openclaw status` is the quick path for diagnosing channel health and recent session recipients; `status --all` produces a pasteable "all" status for debugging.

## Probe Depth: Fast Read-Only vs `--deep` vs `--all`

Plain `openclaw status` stays on the **fast read-only path** and marks memory as `not checked` (instead of `unavailable`) when it skips memory inspection. Heavy probes are deferred off the fast path: heavy security audit, plugin compatibility, and memory-vector probes are left to `openclaw status --all`, `openclaw status --deep`, `openclaw security audit`, and `openclaw memory status --deep`.

`--deep` runs **live probes** against WhatsApp Web, Telegram, Discord, Slack, and Signal.

`status --json --all` reports memory details from the active memory plugin runtime selected by `plugins.slots.memory`. Custom memory plugins can leave the built-in `agents.defaults.memorySearch.enabled` disabled and still report their own files, chunks, vector, and FTS state.

## `--usage`: Provider Usage Windows

`--usage` prints normalized provider usage windows as `X% left`. Provider-specific normalization applies: MiniMax's raw `usage_percent` / `usagePercent` fields are *remaining* quota, so OpenClaw inverts them before display; count-based fields win when present. `model_remains` responses prefer the chat-model entry, derive the window label from timestamps when needed, and include the model name in the plan label.

## Execution vs Runtime

Session status output separates `Execution:` from `Runtime:`. `Execution` is the sandbox path (`direct`, `docker/*`). `Runtime` tells you whether the session is using `OpenClaw Default`, `OpenAI Codex`, a CLI backend, or an ACP backend such as `codex (acp/acpx)`. The source page points to the Agent runtimes doc for the provider/model/runtime distinction.

## Transcript Fallback for Tokens, Cache, and Model Labels

When the current session snapshot is sparse, `/status` can backfill token and cache counters from the most recent transcript usage log; existing nonzero live values still win over transcript fallback values. Transcript fallback can also recover the active runtime model label when the live session entry is missing it — and if that transcript model differs from the selected model, status resolves the context window against the **recovered runtime model** instead of the selected one. For prompt-size accounting, transcript fallback prefers the larger prompt-oriented total when session metadata is missing or smaller, so custom-provider sessions do not collapse to `0` token displays.

## Session Model-Pin Display

When a session is pinned to a model that differs from the configured primary, status prints both values, the reason (`session override`), and the clear hint (`/model default`). The configured primary applies to new or unpinned sessions; existing pinned sessions keep their session selection until cleared.

## Overview Output Contents

The status overview aggregates several runtime signals:

- Per-agent session stores are included when multiple agents are configured.
- Gateway + node host service install/runtime status is included when available.
- Compact Gateway process uptime and host system uptime are included.
- Update channel + git SHA are included (for source checkouts).
- Update info surfaces in the Overview; if an update is available, status prints a hint to run `openclaw update` (see the Updating doc).
- Model pricing refresh failures are shown as optional pricing warnings — they do *not* mean the Gateway or channels are unhealthy.

## Read-Only SecretRef Resolution and Degraded Output

Read-only status surfaces (`status`, `status --json`, `status --all`) resolve supported SecretRefs for their targeted config paths when possible. If a supported channel SecretRef is configured but unavailable in the current command path, status stays read-only and reports **degraded output** instead of crashing: human output shows warnings such as "configured token unavailable in this command path", and JSON output includes `secretDiagnostics`. When command-local SecretRef resolution succeeds, status prefers the resolved snapshot and clears transient "secret unavailable" channel markers from the final output. `status --all` includes a Secrets overview row and a diagnosis section that summarizes secret diagnostics (truncated for readability) without stopping report generation.

**Source**: OpenClaw documentation — `cli/status` (mirror `inbox/openclaw_docs/cli/status.md`)
**Last Updated**: 2026-06-22
**Status**: Active
