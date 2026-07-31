---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - dreaming
keywords:
  - openclaw dreaming
  - memory consolidation phases
  - light deep rem phase
  - dream diary
  - memory promote MEMORY.md
  - deep ranking signals
  - dreaming cron sweep
  - memory-core dreaming config
topics:
  - OpenClaw
  - Dreaming
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/dreaming
access_control_group: ["general"]
---

# OpenClaw — Dreaming: Background Memory Consolidation

## Overview

This note documents the **dreaming** procedure — OpenClaw's opt-in background memory-consolidation system in the `memory-core` plugin that moves strong short-term signals into durable memory while keeping the process explainable and reviewable. It mirrors the `concepts/dreaming` source page: what each phase writes, the light/deep/REM phase model, session-transcript ingestion, the human-readable Dream Diary plus its grounded backfill lane, the six weighted deep-ranking signals, the report-only QA shadow trial, the auto-managed cron sweep and cadence, how to enable dreaming via config / the `/dreaming` slash command / the `openclaw memory` CLI, the key default knobs under `plugins.entries.memory-core.config.dreaming`, the Dreams UI, and the "blocked" heartbeat troubleshooting path. Dreaming is **opt-in and disabled by default**; long-term promotion writes only to `MEMORY.md`.

## What Dreaming Writes

Dreaming keeps two kinds of output. **Machine state** lives in `memory/.dreams/` (recall store, phase signals, ingestion checkpoints, locks). **Human-readable output** lives in `DREAMS.md` (or an existing `dreams.md`) and optional phase report files under `memory/dreaming/<phase>/YYYY-MM-DD.md`. Long-term promotion still writes only to `MEMORY.md` — no other output path promotes durable memory.

## Phase Model

Dreaming uses three cooperative phases. Each sweep runs them in the order light → REM → deep. These phases are internal implementation details, not separate user-configured "modes."

| Phase | Purpose | Durable write |
| ----- | ----------------------------------------- | ----------------- |
| Light | Sort and stage recent short-term material | No |
| Deep | Score and promote durable candidates | Yes (`MEMORY.md`) |
| REM | Reflect on themes and recurring ideas | No |

The **Light phase** ingests recent daily memory signals and recall traces, dedupes them, and stages candidate lines: it reads from short-term recall state, recent daily memory files, and redacted session transcripts when available; writes a managed `## Light Sleep` block when storage includes inline output; records reinforcement signals for later deep ranking; and never writes to `MEMORY.md`. The **Deep phase** decides what becomes long-term memory: it ranks candidates using weighted scoring and threshold gates, requires `minScore`, `minRecallCount`, and `minUniqueQueries` to pass, rehydrates snippets from live daily files before writing (so stale or deleted snippets are skipped), appends promoted entries to `MEMORY.md`, writes a `## Deep Sleep` summary into `DREAMS.md`, and optionally writes `memory/dreaming/deep/YYYY-MM-DD.md`. The **REM phase** extracts patterns and reflective signals: it builds theme and reflection summaries from recent short-term traces, writes a managed `## REM Sleep` block when storage includes inline output, records REM reinforcement signals used by deep ranking, and never writes to `MEMORY.md`.

## Session Transcript Ingestion

Dreaming can ingest redacted session transcripts into the dreaming corpus. When transcripts are available, they are fed into the light phase alongside daily memory signals and recall traces. Personal and sensitive content is redacted before ingestion.

## Dream Diary

Dreaming keeps a narrative **Dream Diary** in `DREAMS.md`. After each phase has enough material, `memory-core` runs a best-effort background subagent turn and appends a short diary entry. It uses the default runtime model unless `dreaming.model` is configured; if the configured model is unavailable, Dream Diary retries once with the session default model. The diary is for human reading in the Dreams UI, not a promotion source — dreaming-generated diary/report artifacts are excluded from short-term promotion, and only grounded memory snippets are eligible to promote into `MEMORY.md`.

There is also a grounded historical backfill lane for review and recovery work, exposed both as CLI commands and through the Control UI:

- `memory rem-harness --path ... --grounded` previews grounded diary output from historical `YYYY-MM-DD.md` notes.
- `memory rem-backfill --path ...` writes reversible grounded diary entries into `DREAMS.md`.
- `memory rem-backfill --path ... --stage-short-term` stages grounded durable candidates into the same short-term evidence store the normal deep phase already uses.
- `memory rem-backfill --rollback` and `--rollback-short-term` remove those staged backfill artifacts without touching ordinary diary entries or live short-term recall.

The Control UI exposes the same diary backfill/reset flow so you can inspect results in the Dreams scene before deciding whether the grounded candidates deserve promotion. The Scene also shows a distinct grounded lane so you can see which staged short-term entries came from historical replay, which promoted items were grounded-led, and clear only grounded-only staged entries without touching ordinary live short-term state.

## Deep Ranking Signals

Deep ranking uses six weighted base signals plus phase reinforcement. Light and REM phase hits add a small recency-decayed boost from `memory/.dreams/phase-signals.json`.

| Signal | Weight | Description |
| ------------------- | ------ | ------------------------------------------------- |
| Frequency | 0.24 | How many short-term signals the entry accumulated |
| Relevance | 0.30 | Average retrieval quality for the entry |
| Query diversity | 0.15 | Distinct query/day contexts that surfaced it |
| Recency | 0.15 | Time-decayed freshness score |
| Consolidation | 0.10 | Multi-day recurrence strength |
| Conceptual richness | 0.06 | Concept-tag density from snippet/path |

Shadow-trial results can be layered on top of that base score as a review signal before any durable write. A helpful trial gives the candidate a small bounded boost, a neutral trial keeps it deferred, and a harmful trial marks it as rejected for that scoring pass. This signal is still report-only: it can change candidate ordering or review metadata, but it does not write to `MEMORY.md` or promote the candidate by itself.

## QA Shadow Trial Report Coverage

QA Lab includes a report-only scenario for exploring how a future dreaming shadow trial could review a candidate memory before promotion. The scenario asks an agent to compare a baseline answer with an answer that can use the candidate memory, then write a local report with a verdict, reason, and risk flags. This coverage is intentionally scoped to QA: it verifies that the report artifact stays separate from `MEMORY.md` and that the agent does not claim the candidate was promoted, and it does not add production shadow-trial behavior or change the deep-phase promotion engine.

The `memory-core` shadow-trial runner keeps that same report-only contract for code paths that need a stable artifact. It accepts the candidate, trial prompt, baseline outcome, candidate outcome, verdict, reason, risk flags, and evidence references, then writes a report with `promotion action: report-only`. Helpful verdicts map to a `promote` recommendation, neutral verdicts map to `defer`, and harmful verdicts map to `reject`; none of those recommendations writes to `MEMORY.md` or applies deep-phase promotion.

## Scheduling

When enabled, `memory-core` auto-manages one cron job for a full dreaming sweep, and each sweep runs phases in order: light → REM → deep. The sweep includes the primary runtime workspace and any configured agent workspaces, deduped by path, so subagent workspace fan-out does not exclude the main agent's `DREAMS.md` and memory state.

| Setting | Default |
| -------------------- | ------------- |
| `dreaming.frequency` | `0 3 * * *` |
| `dreaming.model` | default model |

## Quick Start

Enable dreaming by setting `enabled: true` under `plugins.entries.memory-core.config.dreaming`; a custom sweep cadence adds `timezone` and `frequency` (cron expression):

```json
{
  "plugins": {
    "entries": {
      "memory-core": {
        "config": {
          "dreaming": {
            "enabled": true,
            "timezone": "America/Los_Angeles",
            "frequency": "0 */6 * * *"
          }
        }
      }
    }
  }
}
```

## Slash Command

The `/dreaming` slash command controls dreaming from within a session:

```
/dreaming status
/dreaming on
/dreaming off
/dreaming help
```

## CLI Workflow

The `openclaw memory` CLI drives promotion preview/apply, explanation, and REM-harness preview. Manual `memory promote` uses deep-phase thresholds by default unless overridden with CLI flags. `promote-explain` explains why a specific candidate would or would not promote, and `rem-harness` previews REM reflections, candidate truths, and deep promotion output without writing anything:

```bash
openclaw memory promote
openclaw memory promote --apply
openclaw memory promote --limit 5
openclaw memory status --deep
openclaw memory promote-explain "router vlan"
openclaw memory rem-harness
```

## Key Defaults

All settings live under `plugins.entries.memory-core.config.dreaming`. The documented keys and defaults: `enabled` (boolean, default `false`) enables or disables the dreaming sweep; `frequency` (string, default `0 3 * * *`) is the cron cadence for the full sweep; `model` (string) is an optional Dream Diary subagent model override — use a canonical `provider/model` value when also setting a subagent `allowedModels` allowlist; and `phases.deep.maxPromotedSnippetTokens` (number, default `160`) is the maximum estimated token count kept from each short-term recall snippet promoted into `MEMORY.md`, with ranking provenance remaining visible.

Note that `dreaming.model` requires `plugins.entries.memory-core.subagent.allowModelOverride: true`; to restrict it, also set `plugins.entries.memory-core.subagent.allowedModels`. Trust or allowlist failures stay visible instead of falling back silently, and the retry only covers model-unavailable errors. Most phase policy, thresholds, and storage behavior are internal implementation details — see the Memory configuration reference for the full key list.

## Dreams UI

When enabled, the Gateway **Dreams** tab shows the current dreaming enabled state; phase-level status and managed-sweep presence; short-term, grounded, signal, and promoted-today counts; next scheduled run timing; a distinct grounded Scene lane for staged historical replay entries; and an expandable Dream Diary reader backed by `doctor.memory.dreamDiary`.

## Dreaming Never Runs: Status Shows Blocked

If `openclaw memory status` reports `Dreaming status: blocked`, the managed cron exists but the default agent heartbeat is not firing. Check that heartbeat is enabled for the default agent and that its target is not `none`, then run `openclaw memory status --deep` again after the next heartbeat interval.

**Source**: OpenClaw documentation — `concepts/dreaming` (mirror `inbox/openclaw_docs/concepts/dreaming.md`)
**Last Updated**: 2026-06-22
**Status**: Active
