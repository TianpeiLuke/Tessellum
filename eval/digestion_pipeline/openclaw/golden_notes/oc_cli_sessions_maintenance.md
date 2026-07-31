---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - sessions
keywords:
  - openclaw sessions cleanup
  - openclaw sessions compact
  - session.maintenance pruneAfter
  - sessions.compact rpc
  - dry-run enforce fix-missing fix-dm-scope
  - active-key disk-budget eviction
  - max-lines truncate bak sidecar
  - gateway-routed session writer
topics:
  - OpenClaw
  - CLI Sessions Maintenance
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/sessions
access_control_group: ["general"]
---

# OpenClaw — `openclaw sessions` Maintenance and Compaction

## Overview

This note is the maintenance/lifecycle half of the `openclaw sessions` CLI command, covering the two destructive state-management workflows on the `cli/sessions` source page: `sessions cleanup` (prune/cap stored session rows and prune unreferenced transcripts/sidecars per `session.maintenance`) and `sessions compact` (reclaim context budget for a wedged or oversized session, either by LLM summarization or `--max-lines` truncation, via the `sessions.compact` gateway RPC). The read-only discovery half (list, scope flags, `tail`, `export-trajectory`) lives in the sibling note `oc_cli_sessions_inspect`. Every flag, default, JSON field, and RPC field below is mirrored verbatim from `inbox/openclaw_docs/cli/sessions.md`.

## Cleanup Maintenance (`openclaw sessions cleanup`)

`openclaw sessions cleanup` runs session-store maintenance immediately instead of waiting for the next write cycle. It uses the `session.maintenance` settings from config and decides what to prune/cap based on age, count, and disk budget. The example invocations on the source page are:

```bash
openclaw sessions cleanup --dry-run
openclaw sessions cleanup --agent work --dry-run
openclaw sessions cleanup --all-agents --dry-run
openclaw sessions cleanup --enforce
openclaw sessions cleanup --enforce --active-key "agent:main:telegram:direct:123"
openclaw sessions cleanup --dry-run --fix-dm-scope
openclaw sessions cleanup --json
```

### Scope of Cleanup

`openclaw sessions cleanup` maintains session stores, transcripts, and trajectory sidecars. It does NOT prune cron run history — that is managed by `cron.runLog.keepLines` in the Cron configuration (`/automation/cron-jobs#configuration`) and explained in Cron maintenance (`/automation/cron-jobs#maintenance`). Beyond pruning/capping rows in `sessions.json`, cleanup also prunes unreferenced primary transcripts, compaction checkpoints, and trajectory sidecars older than `session.maintenance.pruneAfter`; files still referenced by `sessions.json` are preserved.

### Cleanup Flags

- `--dry-run` — preview how many entries would be pruned/capped without writing. In text mode, dry-run prints a per-session action table with columns `Action`, `Key`, `Age`, `Model`, `Flags`, plus a summary grouped by session label so the operator can see what would be kept versus removed.
- `--enforce` — apply maintenance even when `session.maintenance.mode` is `warn`.
- `--fix-missing` — remove entries whose transcript files are missing or header-only/empty, even if they would not normally age out or count out yet.
- `--fix-dm-scope` — when `session.dmScope` is `main`, retire stale peer-keyed direct-DM rows left behind by earlier `per-peer`, `per-channel-peer`, or `per-account-channel-peer` routing. Use `--dry-run` first; applying the cleanup removes those rows from `sessions.json` and preserves their transcripts as deleted archives.
- `--active-key <key>` — protect a specific active key from disk-budget eviction. Durable external conversation pointers, such as group sessions and thread-scoped chat sessions, are also kept by age/count/disk-budget maintenance.
- `--agent <id>` — run cleanup for one configured agent store.
- `--all-agents` — run cleanup for all configured agent stores.
- `--store <path>` — run against a specific `sessions.json` file.
- `--json` — print a JSON summary. With `--all-agents`, output includes one summary per store.

### Gateway-Routed Writes

When a Gateway is reachable, non-dry-run cleanup for configured agent stores is sent through the Gateway so it shares the same session-store writer as runtime traffic. Use `--store <path>` for explicit offline repair of a store file.

### Cleanup JSON Summary

`openclaw sessions cleanup --all-agents --dry-run --json` returns a per-store summary; each store object carries before/after counts and the breakdown of what maintenance would do:

```json
{
  "allAgents": true,
  "mode": "warn",
  "dryRun": true,
  "stores": [
    {
      "agentId": "main",
      "storePath": "/home/user/.openclaw/agents/main/sessions/sessions.json",
      "beforeCount": 120,
      "afterCount": 80,
      "missing": 0,
      "dmScopeRetired": 0,
      "pruned": 40,
      "capped": 0
    },
    {
      "agentId": "work",
      "storePath": "/home/user/.openclaw/agents/work/sessions/sessions.json",
      "beforeCount": 18,
      "afterCount": 18,
      "missing": 0,
      "dmScopeRetired": 0,
      "pruned": 0,
      "capped": 0
    }
  ]
}
```

The summary fields are `agentId`, `storePath`, `beforeCount`, `afterCount`, `missing`, `dmScopeRetired`, `pruned`, and `capped`; the top-level object reports `allAgents`, `mode` (`warn` here), and `dryRun`.

## Compact a Session (`openclaw sessions compact`)

`openclaw sessions compact <key>` reclaims context budget for a wedged or oversized session. It is the first-class wrapper around the `sessions.compact` gateway RPC and requires a running gateway. The example invocations on the source page are:

```bash
openclaw sessions compact "agent:main:main"
openclaw sessions compact "agent:main:main" --max-lines 200
openclaw sessions compact "agent:work:main" --agent work --json
```

### Compaction Modes and Flags

- Without `--max-lines`, the gateway LLM-summarizes the transcript. This can be slow, so the default `--timeout` is `180000` ms.
- With `--max-lines <n>`, it truncates to the last `n` transcript lines and archives the prior transcript as a `.bak` sidecar.
- `--agent <id>` — agent that owns the session; required for `global` keys.
- `--url` / `--token` / `--password` — gateway connection overrides.
- `--timeout <ms>` — RPC timeout in milliseconds.
- `--json` — print the raw RPC payload.

The command exits non-zero when the gateway reports a failed compaction or is unreachable, so crons and scripts never mistake a silent no-op for success.

> Note: `openclaw agent --message '/compact ...'` is **not** a compaction path. Slash commands from the CLI are rejected by the authorized-sender check; that invocation exits non-zero with guidance pointing here instead of silently no-opping.

### `sessions.compact` RPC

`openclaw gateway call sessions.compact --params '<json>'` accepts the following parameters:

| Field      | Type        | Required | Description                                                |
| ---------- | ----------- | -------- | ---------------------------------------------------------- |
| `key`      | string      | yes      | Session key to compact (for example `agent:main:main`).    |
| `agentId`  | string      | no       | Agent id that owns the session (for `global` keys).        |
| `maxLines` | integer ≥ 1 | no       | Truncate to the last N lines instead of LLM summarization. |

An LLM-summarize response reports the token reduction in `result.tokensBefore` / `result.tokensAfter`:

```json
{
  "ok": true,
  "key": "agent:main:main",
  "compacted": true,
  "result": { "tokensBefore": 243868, "tokensAfter": 34941 }
}
```

A truncate response (`--max-lines 200`) reports the archived `.bak` sidecar path and the number of lines `kept`:

```json
{
  "ok": true,
  "key": "agent:main:main",
  "compacted": true,
  "archived": "/home/user/.openclaw/agents/main/sessions/transcripts/<id>.jsonl.bak",
  "kept": 200
}
```

**Source**: OpenClaw documentation — `cli/sessions` (mirror `inbox/openclaw_docs/cli/sessions.md`), maintenance/compaction sections
**Last Updated**: 2026-06-22
**Status**: Active
