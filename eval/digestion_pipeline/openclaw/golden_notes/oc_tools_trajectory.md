---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - trajectory
keywords:
  - openclaw trajectory bundle
  - export-trajectory support bundle
  - per-session flight recorder
  - trajectory jsonl runtime events
  - openclaw_trajectory_dir capture location
  - trajectory redaction privacy limits
  - openclaw-trajectory schemaVersion
  - openclaw_trajectory_flush_timeout_ms
topics:
  - OpenClaw
  - Trajectory Bundles
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/trajectory
access_control_group: ["general"]
---

# OpenClaw — Exporting Trajectory Bundles (Per-Session Flight Recorder)

## Overview

This note is the procedure for OpenClaw **trajectory capture** — the per-session flight recorder that records a structured timeline for each agent run, and the `/export-trajectory` slash command that packages the current session into a redacted support bundle. It mirrors the `tools/trajectory` source page end-to-end: the quick-start export and CLI fallback, owner-only access, what runtime/transcript events get recorded, the bundle file schema, where sidecars are captured (`OPENCLAW_TRAJECTORY_DIR`), how to disable capture (`OPENCLAW_TRAJECTORY=0`) and tune the flush timeout (`OPENCLAW_TRAJECTORY_FLUSH_TIMEOUT_MS`), the redaction-and-size privacy limits, and troubleshooting. Use this when debugging why an agent answered, failed, or called tools a certain way, or when exporting a support bundle for an OpenClaw session.

Trajectory capture answers questions like: what prompt, system prompt, and tools were sent to the model; which transcript messages and tool calls led to an answer; whether the run timed out, aborted, compacted, or hit a provider error; which model, plugins, skills, and runtime settings were active; and what usage and prompt-cache metadata the provider returned. For a broad support report on a live Gateway issue, start with `/diagnostics` (the sanitized Gateway bundle, which for OpenAI Codex harness sessions can also send Codex feedback to OpenAI servers after approval); use `/export-trajectory` when you specifically need the detailed per-session prompt, tool, and transcript timeline.

## Quick Start — Exporting a Bundle

Send `/export-trajectory` (alias `/trajectory`) in the active session. OpenClaw writes the bundle under the workspace at `.openclaw/trajectory-exports/openclaw-trajectory-<session>-<timestamp>/`. You can choose a relative output directory name by passing it as an argument:

```text
/export-trajectory bug-1234
```

The custom path is resolved inside `.openclaw/trajectory-exports/`; absolute paths and `~` paths are rejected. Because trajectory bundles can contain prompts, model messages, tool schemas, tool results, runtime events, and local paths, the chat slash command runs through **exec approval every time** — approve the export once when you intend to create the bundle, and do not use allow-all. In group chats, OpenClaw sends the approval prompt and export result to the owner privately instead of posting the trajectory details back to the shared room.

For local inspection or support workflows you can also run the approved command path directly via the CLI:

```bash
openclaw sessions export-trajectory --session-key "agent:main:telegram:direct:123" --workspace .
```

## Access

Trajectory export is an **owner command**. The sender must pass the normal command authorization checks and owner checks for the channel.

## What Gets Recorded

Trajectory capture is **on by default** for OpenClaw agent runs. Two classes of events are captured. **Runtime events** include `session.started`, `trace.metadata`, `context.compiled`, `prompt.submitted`, `model.fallback_step` (including the source model, next model, failure reason/detail, chain position, and whether fallback advanced, succeeded, or exhausted the chain), `model.completed`, `trace.artifacts`, and `session.ended`. **Transcript events** are also reconstructed from the active session branch: user messages, assistant messages, tool calls, tool results, compactions, model changes, and labels and custom session entries.

Events are written as JSON Lines with this schema marker:

```json
{
  "traceSchema": "openclaw-trajectory",
  "schemaVersion": 1
}
```

## Bundle Files

An exported bundle can contain the following files. `manifest.json` lists the files present in that bundle; some files are omitted when the session did not capture the corresponding runtime data.

| File | Contents |
| --- | --- |
| `manifest.json` | Bundle schema, source files, event counts, and generated file list |
| `events.jsonl` | Ordered runtime and transcript timeline |
| `session-branch.json` | Redacted active transcript branch and session header |
| `metadata.json` | OpenClaw version, OS/runtime, model, config snapshot, plugins, skills, and prompt metadata |
| `artifacts.json` | Final status, errors, usage, prompt cache, compaction count, assistant text, and tool metadata |
| `prompts.json` | Submitted prompts and selected prompt-building details |
| `system-prompt.txt` | Latest compiled system prompt, when captured |
| `tools.json` | Tool definitions sent to the model, when captured |

## Capture Location

By default, runtime trajectory events are written **beside the session file** as `<session>.trajectory.jsonl`, and OpenClaw also writes a best-effort pointer file beside the session as `<session>.trajectory-path.json`. To store runtime trajectory sidecars in a dedicated directory, set `OPENCLAW_TRAJECTORY_DIR`:

```bash
export OPENCLAW_TRAJECTORY_DIR=/var/lib/openclaw/trajectories
```

When this variable is set, OpenClaw writes one JSONL file per session id in that directory. Session maintenance removes trajectory sidecars when their owning session entry is pruned, capped, or evicted by the sessions disk budget; runtime files outside the sessions directory are removed only when the pointer target still proves it belongs to that session.

## Disable Capture

Set `OPENCLAW_TRAJECTORY=0` before starting OpenClaw to disable runtime trajectory capture:

```bash
export OPENCLAW_TRAJECTORY=0
```

With capture disabled, `/export-trajectory` can still export the transcript branch, but runtime-only files such as compiled context, provider artifacts, and prompt metadata may be missing.

## Tune Flush Timeout

OpenClaw flushes runtime trajectory sidecars during agent cleanup, with a default cleanup timeout of **10,000 ms**. On slow disks or large stores, set `OPENCLAW_TRAJECTORY_FLUSH_TIMEOUT_MS` before starting OpenClaw (e.g. `export OPENCLAW_TRAJECTORY_FLUSH_TIMEOUT_MS=30000`). This controls when OpenClaw logs an `openclaw-trajectory-flush` timeout and continues; it does not change the trajectory size caps. To tune all agent cleanup steps that do not pass an explicit timeout, set `OPENCLAW_AGENT_CLEANUP_TIMEOUT_MS`.

## Privacy and Limits

Trajectory bundles are designed for support and debugging, not public posting. OpenClaw **redacts** sensitive values before writing export files: credentials and known secret-like payload fields; image data; local state paths; workspace paths (replaced with `$WORKSPACE_DIR`); and home directory paths, where detected. The exporter also bounds input size: runtime sidecar files — live capture stops at 10 MiB and records a truncation event when space remains, while export accepts existing runtime sidecars up to 50 MiB; session files up to 50 MiB; runtime events up to 200,000; total exported events up to 250,000; and individual runtime event lines are truncated above 256 KiB. Review bundles before sharing them outside your team, because redaction is best-effort and cannot know every application-specific secret.

## Troubleshooting

If the export has no runtime events: confirm OpenClaw was started without `OPENCLAW_TRAJECTORY=0`; check whether `OPENCLAW_TRAJECTORY_DIR` points to a writable directory; run another message in the session, then export again; and inspect `manifest.json` for `runtimeEventCount`. If the command rejects the output path: use a relative name like `bug-1234`; do not pass `/tmp/...` or `~/...`; and keep the export inside `.openclaw/trajectory-exports/`. If the export fails with a size error, the session or sidecar exceeded the export safety limits — start a new session or export a smaller reproduction.

**Source**: OpenClaw documentation — `tools/trajectory` (mirror `inbox/openclaw_docs/tools/trajectory.md`)
**Last Updated**: 2026-06-22
**Status**: Active
