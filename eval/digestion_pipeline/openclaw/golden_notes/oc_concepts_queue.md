---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - queue
keywords:
  - openclaw command queue
  - auto-reply queue
  - lane-aware fifo queue
  - queue modes steer followup collect interrupt
  - messages.queue config
  - per-session queue override
  - session lane global lane concurrency
  - debounce cap drop
topics:
  - OpenClaw
  - Command Queue
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/queue
access_control_group: ["general"]
---

# OpenClaw — The Command Queue (Auto-Reply Lane Queue)

## Overview

This note describes the OpenClaw **command queue**: a tiny in-process queue that serializes inbound auto-reply runs across all channels to prevent multiple agent runs from colliding, while still allowing safe parallelism across sessions. It covers why the queue exists, the lane-aware FIFO mechanics under `runEmbeddedAgent`, the unset defaults, the four `/queue` modes (`steer` / `followup` / `collect` / `interrupt`), the queue options (`debounceMs` / `cap` / `drop`), how steering interacts with streaming, the mode/option resolution precedence, per-session overrides, scope and guarantees, and troubleshooting — mirroring the `concepts/queue` source page. It is a `concept` note; the runtime-boundary timing of `steer` mode and the explicit `/steer` command are owned by sibling notes and linked, not redefined here.

## Why

OpenClaw serializes inbound auto-reply runs (all channels) through a tiny in-process queue to prevent multiple agent runs from colliding, while still allowing safe parallelism across sessions. Two motivations drive this: auto-reply runs can be expensive (LLM calls) and can collide when multiple inbound messages arrive close together; and serializing avoids competing for shared resources (session files, logs, CLI stdin) and reduces the chance of upstream rate limits.

## How it works

A **lane-aware FIFO queue** drains each lane with a configurable concurrency cap — default 1 for unconfigured lanes, with `main` defaulting to 4 and `subagent` to 8. `runEmbeddedAgent` enqueues by **session key** (lane `session:<key>`) to guarantee only one active run per session. Each session run is then queued into a **global lane** (`main` by default) so overall parallelism is capped by `agents.defaults.maxConcurrent`. When verbose logging is enabled, queued runs emit a short notice if they waited more than ~2s before starting. Typing indicators still fire immediately on enqueue (when supported by the channel) so user experience is unchanged while the run waits its turn.

## Defaults

When unset, all inbound channel surfaces use `mode: "steer"`, `debounceMs: 500`, `cap: 20`, and `drop: "summarize"`. Same-turn steering is the default: a prompt that arrives mid-run is injected into the active runtime when the run can accept steering, so no second session run is started. If the active run cannot accept steering, OpenClaw waits for the active run to finish before starting the prompt.

## Queue modes

`/queue` controls what normal inbound messages do while a session already has an active run. The four modes are:

- `steer`: inject messages into the active runtime. OpenClaw delivers all pending steering messages **after the current assistant turn finishes executing its tool calls**, before the next LLM call; Codex app-server receives one batched `turn/steer`. If the run is not actively streaming or steering is unavailable, OpenClaw waits until the active run ends before starting the prompt.
- `followup`: do not steer. Enqueue each message for a later agent turn after the current run ends.
- `collect`: do not steer. Coalesce queued messages into a **single** followup turn after the quiet window. If messages target different channels/threads, they drain individually to preserve routing.
- `interrupt`: abort the active run for that session, then run the newest message.

For runtime-specific timing and dependency behavior, see Steering queue (sibling `oc_concepts_queue_steering`); for the explicit `/steer <message>` command, see Steer (sibling `oc_tools_steer`). The queue is configured globally or per channel via `messages.queue`:

```json5
{
  messages: {
    queue: {
      mode: "steer",
      debounceMs: 500,
      cap: 20,
      drop: "summarize",
      byChannel: { discord: "collect" },
    },
  },
}
```

## Queue options

Options apply to queued delivery. `debounceMs` also sets the Codex steering quiet window in `steer` mode:

- `debounceMs`: quiet window before draining queued followups or collect batches; in Codex `steer` mode, the quiet window before sending batched `turn/steer`. Bare numbers are milliseconds; units `ms`, `s`, `m`, `h`, and `d` are accepted by `/queue` options.
- `cap`: max queued messages per session. Values below `1` are ignored.
- `drop: "summarize"`: default. Drop the oldest queued entries as needed, keep compact summaries, and inject them as a synthetic followup prompt.
- `drop: "old"`: drop the oldest queued entries as needed, without preserving summaries.
- `drop: "new"`: reject the newest message when the queue is already full.

Defaults: `debounceMs: 500`, `cap: 20`, `drop: summarize`.

## Steer and streaming

When channel streaming is `partial` or `block`, steering can look like several short visible replies while the active run reaches runtime boundaries. With `partial`, the preview may finalize early, then a new preview starts after steering is accepted; with `block`, draft-sized blocks can create the same sequential appearance; without streaming, steering falls back to a followup after the active run when the runtime cannot accept same-turn steering. `steer` does not abort in-flight tools — use `/queue interrupt` when the newest message should abort the current run.

## Precedence

For mode selection, OpenClaw resolves in this order: (1) inline or stored per-session `/queue` override; (2) `messages.queue.byChannel.<channel>`; (3) `messages.queue.mode`; (4) the default `steer`. For options, inline or stored `/queue` options win over config; then channel-specific debounce (`messages.queue.debounceMsByChannel`), plugin debounce defaults, global `messages.queue` options, and built-in defaults are applied. `cap` and `drop` are global/session options, not per-channel config keys.

## Per-session overrides

Send `/queue <steer|followup|collect|interrupt>` as a standalone command to store the queue mode for the current session. Options can be combined, e.g. `/queue collect debounce:0.5s cap:25 drop:summarize`. `/queue default` or `/queue reset` clears the session override.

## Scope and guarantees

The queue applies to auto-reply agent runs across all inbound channels that use the gateway reply pipeline (WhatsApp web, Telegram, Slack, Discord, Signal, iMessage, webchat, etc.). The default lane (`main`) is process-wide for inbound plus main heartbeats; set `agents.defaults.maxConcurrent` to allow multiple sessions in parallel. Additional lanes may exist (e.g. `cron`, `cron-nested`, `nested`, `subagent`) so background jobs can run in parallel without blocking inbound replies: isolated cron agent turns hold a `cron` slot while their inner agent execution uses `cron-nested`, and both use `cron.maxConcurrentRuns`, while shared non-cron `nested` flows keep their own lane behavior. These detached runs are tracked as background tasks (sibling `oc_automation_tasks`). Per-session lanes guarantee that only one agent run touches a given session at a time. There are no external dependencies or background worker threads — the queue is pure TypeScript plus promises.

## Troubleshooting

If commands seem stuck, enable verbose logs and look for "queued for ...ms" lines to confirm the queue is draining; if you need queue depth, enable verbose logs and watch for queue timing lines. Codex app-server runs that accept a turn and then stop emitting progress are interrupted by the Codex adapter so the active session lane can release instead of waiting for the outer run timeout. When diagnostics are enabled, sessions that remain in `processing` past `diagnostics.stuckSessionWarnMs` with no observed reply, tool, status, block, or ACP progress are classified by current activity: active work logs as `session.long_running` (owned silent model calls also stay `session.long_running` until `diagnostics.stuckSessionAbortMs` so slow or non-streaming providers are not reported as stalled too early); active work with no recent progress logs as `session.stalled` (owned model calls switch to `session.stalled` at or after the abort threshold, and ownerless stale model/tool activity is not hidden as long-running); and `session.stuck` is reserved for recoverable stale session bookkeeping — including idle queued sessions with stale ownerless model/tool activity — and only that path can release the affected session lane so queued work drains, with repeated `session.stuck` diagnostics backing off while the session remains unchanged.

**Source**: OpenClaw documentation — `concepts/queue` (mirror `inbox/openclaw_docs/concepts/queue.md`)
**Last Updated**: 2026-06-22
**Status**: Active
