---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - diagnostics
keywords:
  - openclaw gateway diagnostics export
  - openclaw gateway diagnostics export json
  - diagnostics chat command
  - diagnostics privacy redaction model
  - stability recorder bundle
  - diagnostic liveness warning
  - memorypressuresnapshot
  - disable diagnostics enabled false
  - codex harness feedback upload
topics:
  - OpenClaw
  - Gateway Diagnostics
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/diagnostics
access_control_group: ["general"]
---

# OpenClaw — Gateway Diagnostics Export

## Overview

This note is a procedure for creating shareable OpenClaw **Gateway diagnostics bundles** for bug reports and support requests, mirroring the `gateway/diagnostics` source page. OpenClaw can create a local diagnostics zip that combines sanitized Gateway status, health, logs, config shape, and recent payload-free stability events. It covers the `openclaw gateway diagnostics export` command and its options, the `/diagnostics` chat command and its single-exec-approval flow (including the Codex-harness feedback-upload path), the contents of the export zip, the redaction/privacy model that makes a bundle shareable, the always-on stability recorder and its `diagnostic.liveness.warning` / `diagnostic.phase.completed` events, and how to disable diagnostics or enable the critical-memory-pressure snapshot. Per the source, treat diagnostics bundles like secrets until reviewed: they are designed to omit or redact payloads and credentials, but they still summarize local Gateway logs and host-level runtime state.

## Quick start

Create a local diagnostics zip with the export command; it prints the written zip path:

```bash
openclaw gateway diagnostics export
```

To choose a path, pass `--output`; for automation, pass `--json` to print machine-readable export metadata:

```bash
openclaw gateway diagnostics export --output openclaw-diagnostics.zip
openclaw gateway diagnostics export --json
```

## Chat command

Owners can use `/diagnostics [note]` in chat to request a local Gateway export. Use this when the bug happened in a real conversation and you want one copy-pasteable report for support. The flow is:

1. Send `/diagnostics` in the conversation where you noticed the problem. Add a short note if it helps, for example `/diagnostics bad tool choice`.
2. OpenClaw sends the diagnostics preamble and asks for one explicit exec approval. The approval runs `openclaw gateway diagnostics export --json`. **Do not approve diagnostics through an allow-all rule.**
3. After approval, OpenClaw replies with a pasteable report containing the local bundle path, manifest summary, privacy notes, and relevant session ids.

In group chats, an owner can still run `/diagnostics`, but OpenClaw does not post the diagnostic details back into the shared chat. It sends the preamble, approval prompts, Gateway export result, and Codex session/thread breakdown to the owner through the private approval route. The group only gets a short notice that the diagnostics flow was sent privately. If OpenClaw cannot find a private owner route, the command fails closed and asks the owner to run it from a DM.

When the active OpenClaw session is using the native OpenAI Codex harness, the same exec approval also covers an OpenAI feedback upload for the Codex runtime threads OpenClaw knows about. That upload is separate from the local Gateway zip and appears only for Codex harness sessions. Before approval, the prompt explains that approving diagnostics will also send Codex feedback, but it does not list Codex session or thread ids. After approval, the chat reply lists the channels, OpenClaw session ids, Codex thread ids, and local resume commands for the threads that were sent to OpenAI servers. If you deny or ignore the approval, OpenClaw does not run the export, does not send Codex feedback, and does not print the Codex ids. The common Codex debugging loop is therefore short: notice the bad behavior in a channel, run `/diagnostics`, approve once, share the report with support, then run the printed `codex resume <thread-id>` command locally if you want to inspect the native Codex thread yourself.

## What the export contains

The zip includes a human-readable `summary.md` overview for support; a machine-readable `diagnostics.json` summary of config, logs, status, health, and stability data; a `manifest.json` of export metadata and the file list; the sanitized config shape and non-secret config details; sanitized log summaries and recent redacted log lines; best-effort Gateway status and health snapshots; and `stability/latest.json`, the newest persisted stability bundle, when available. The export is useful even when the Gateway is unhealthy: if the Gateway cannot answer status or health requests, the local logs, config shape, and latest stability bundle are still collected when available.

## Privacy model

Diagnostics are designed to be shareable. The export **keeps** operational data that helps debugging: subsystem names, plugin ids, provider ids, channel ids, and configured modes; status codes, durations, byte counts, queue state, and memory readings; sanitized log metadata and redacted operational messages; and config shape and non-secret feature settings. The export **omits or redacts**: chat text, prompts, instructions, webhook bodies, and tool outputs; credentials, API keys, tokens, cookies, and secret values; raw request or response bodies; and account ids, message ids, raw session ids, hostnames, and local usernames. When a log message looks like user, chat, prompt, or tool payload text, the export keeps only that a message was omitted and the byte count.

## Stability recorder

The Gateway records a bounded, payload-free stability stream by default when diagnostics are enabled; it is for operational facts, not content. The same diagnostic heartbeat records liveness samples when the Gateway keeps running but the Node.js event loop or CPU looks saturated. These `diagnostic.liveness.warning` events include event-loop delay, event-loop utilization, CPU-core ratio, active/waiting/queued session counts, the current startup/runtime phase when known, recent phase spans, and bounded active/queued work labels. Idle samples stay in telemetry at `info` level. Liveness samples become Gateway warnings only when work is waiting or queued, or when active work overlaps with sustained event-loop delay. Transient max-delay spikes during otherwise healthy background work stay in debug logs and do not restart the Gateway by themselves. Startup phases also emit `diagnostic.phase.completed` events with wall-clock and CPU timing. Stalled embedded-run diagnostics mark `terminalProgressStale=true` when the last bridge progress looked terminal, such as a raw response item or response completion event, but the Gateway still considers the embedded run active.

Inspect the live recorder, and the newest persisted stability bundle after a fatal exit, shutdown timeout, or restart startup failure:

```bash
openclaw gateway stability
openclaw gateway stability --type payload.large
openclaw gateway stability --json
openclaw gateway stability --bundle latest
openclaw gateway stability --bundle latest --export
```

`openclaw gateway stability --bundle latest --export` creates a diagnostics zip from the newest persisted bundle. Persisted bundles live under `~/.openclaw/logs/stability/` when events exist.

## Useful options

```bash
openclaw gateway diagnostics export \
  --output openclaw-diagnostics.zip \
  --log-lines 5000 \
  --log-bytes 1000000
```

- `--output <path>`: write to a specific zip path.
- `--log-lines <count>`: maximum sanitized log lines to include.
- `--log-bytes <bytes>`: maximum log bytes to inspect.
- `--url <url>`: Gateway WebSocket URL for status and health snapshots.
- `--token <token>`: Gateway token for status and health snapshots.
- `--password <password>`: Gateway password for status and health snapshots.
- `--timeout <ms>`: status and health snapshot timeout.
- `--no-stability-bundle`: skip persisted stability bundle lookup.
- `--json`: print machine-readable export metadata.

## Disable diagnostics

Diagnostics are enabled by default. To disable the stability recorder and diagnostic event collection, set `diagnostics.enabled` to `false`:

```json5
{
  diagnostics: {
    enabled: false,
  },
}
```

Disabling diagnostics reduces bug-report detail; it does not affect normal Gateway logging. Critical memory pressure snapshots are off by default. To keep diagnostics events and also capture the pre-OOM stability snapshot, set `diagnostics.memoryPressureSnapshot` to `true`:

```json5
{
  diagnostics: {
    memoryPressureSnapshot: true,
  },
}
```

Use this only on hosts that can tolerate the extra file-system scan and snapshot write during critical memory pressure. Normal memory pressure events still record RSS, heap, threshold, and growth facts when the snapshot is off.

**Source**: OpenClaw documentation — `gateway/diagnostics` (mirror `inbox/openclaw_docs/gateway/diagnostics.md`)
**Last Updated**: 2026-06-22
**Status**: Active
