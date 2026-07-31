---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - loop_detection
keywords:
  - openclaw loop detection
  - tools.loopDetection config
  - post-compaction guard
  - compaction_loop_persisted abort
  - globalCircuitBreakerThreshold
  - repetitive tool-call guardrail
  - genericRepeat pingPong knownPollNoProgress
  - per-agent loopDetection override
topics:
  - OpenClaw
  - Loop Detection
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/loop-detection
access_control_group: ["general"]
---

# OpenClaw — Tool-Loop Detection and the Post-Compaction Guard

## Overview

This note is the procedure for enabling and tuning OpenClaw's two cooperating guardrails against repetitive tool-call loops, mirroring the `tools/loop-detection` source page. The first guardrail is **Loop detection** (`tools.loopDetection.enabled`), which is disabled by default and watches the rolling tool-call history for repeated patterns and unknown-tool retries. The second is the **Post-compaction guard** (`tools.loopDetection.postCompactionGuard`), which is enabled by default unless `tools.loopDetection.enabled` is explicitly `false`; it arms after every compaction-retry and aborts the run when the agent emits the same `(tool, args, result)` triple within the window. Both surfaces are configured under the same `tools.loopDetection` block, but the post-compaction guard runs whenever the master switch is not explicitly off. Setting `tools.loopDetection.enabled: false` silences both surfaces. This note covers why the guardrails exist, the full configuration block and per-field behavior, the recommended setup and false-positive tuning, the post-compaction guard semantics, and the log lines and expected blocking behavior.

## Why this exists

The guardrails address four runaway-loop conditions the source page enumerates:

- Detect repetitive sequences that do not make progress.
- Detect high-frequency no-result loops (same tool, same inputs, repeated errors).
- Detect specific repeated-call patterns for known polling tools.
- Prevent context-overflow then compaction then same-loop cycles from running indefinitely.

The fourth condition is the reason the post-compaction guard stays on by default: it exists to escape compaction loops that would otherwise burn unbounded tokens.

## Configuration block

Both surfaces live under one `tools.loopDetection` block. The global defaults, with every documented field shown, are:

```json5
{
  tools: {
    loopDetection: {
      enabled: false, // master switch for the rolling-history detectors
      historySize: 30,
      warningThreshold: 10,
      criticalThreshold: 20,
      unknownToolThreshold: 10,
      globalCircuitBreakerThreshold: 30,
      detectors: {
        genericRepeat: true,
        knownPollNoProgress: true,
        pingPong: true,
      },
      postCompactionGuard: {
        windowSize: 3, // armed after compaction-retry; runs unless enabled is explicitly false
      },
    },
  },
}
```

A per-agent override is optional and is placed under `agents.list[].tools.loopDetection`, where it merges over the global defaults for that one agent:

```json5
{
  agents: {
    list: [
      {
        id: "safe-runner",
        tools: {
          loopDetection: {
            enabled: true,
            warningThreshold: 8,
            criticalThreshold: 16,
          },
        },
      },
    ],
  },
}
```

### Field behavior

| Field | Default | Effect |
| --- | --- | --- |
| `enabled` | `false` | Master switch for the rolling-history detectors. Setting `false` also disables the post-compaction guard. |
| `historySize` | `30` | Number of recent tool calls kept for analysis. |
| `warningThreshold` | `10` | Threshold before a pattern is classified as warning-only. |
| `criticalThreshold` | `20` | Threshold for blocking repetitive no-progress loop patterns. |
| `unknownToolThreshold` | `10` | Block repeated calls to the same unavailable tool after this many misses. |
| `globalCircuitBreakerThreshold` | `30` | Global no-progress breaker threshold across all detectors. |
| `detectors.genericRepeat` | `true` | Warns on repeated same-tool + same-params patterns and blocks when the same calls also return identical outcomes. |
| `detectors.knownPollNoProgress` | `true` | Detects known polling-like patterns with no state change. |
| `detectors.pingPong` | `true` | Detects alternating ping-pong patterns. |
| `postCompactionGuard.windowSize` | `3` | Number of post-compaction tool calls during which the guard stays armed and the count of identical triples that aborts the run. |

For `exec`, no-progress checks compare stable command outcomes and ignore volatile runtime metadata such as duration, PID, session ID, and working directory. When a run id is available, recent tool-call history is evaluated only within that run, so scheduled heartbeat cycles and fresh runs do not inherit stale loop counts from earlier runs.

## Recommended setup

- For smaller models, set `enabled: true` and leave the thresholds at their defaults. Flagship models rarely need rolling-history detection and can leave the master switch at `false` while still benefiting from the post-compaction guard.
- Keep thresholds ordered as `warningThreshold < criticalThreshold < globalCircuitBreakerThreshold`.
- If false positives occur: raise `warningThreshold` and/or `criticalThreshold`; optionally raise `globalCircuitBreakerThreshold`; disable only the specific detector causing issues (`detectors.<name>: false`); or reduce `historySize` for less strict historical context.
- To disable everything (including the post-compaction guard), set `tools.loopDetection.enabled: false` explicitly.

## Post-compaction guard

When the runner completes a compaction-retry after a context-overflow, it arms a short-window guard that watches the next few tool calls. If the agent emits the same `(toolName, argsHash, resultHash)` triple multiple times within the window, the guard concludes that compaction did not break the loop and aborts the run with a `compaction_loop_persisted` error.

The guard is gated by the master `tools.loopDetection.enabled` flag with one twist: it stays **enabled when the flag is unset or `true`** and only deactivates when the flag is explicitly `false`. This is intentional — the guard exists to escape compaction loops that would otherwise burn unbounded tokens, so a no-config user still gets the protection. The guard can be expressed explicitly:

```json5
{
  tools: {
    loopDetection: {
      // master switch; set false to disable the guard along with the rolling detectors
      enabled: true,
      postCompactionGuard: {
        windowSize: 3, // default
      },
    },
  },
}
```

Guard tuning and scope:

- Lower `windowSize` is stricter (fewer attempts before abort).
- Higher `windowSize` gives the agent more recovery attempts.
- The guard never aborts when results are changing, only when results are byte-identical across the window.
- It is intentionally narrow: it fires only in the immediate aftermath of a compaction-retry.

A source Note warns that the post-compaction guard runs whenever the master flag is not explicitly `false`, even if you never wrote a `tools.loopDetection` block. To verify, look for `post-compaction guard armed for N attempts` in the gateway log immediately after a compaction event.

## Logs and expected behavior

When a loop is detected, OpenClaw reports a loop event and either dampens or blocks the next tool-cycle depending on severity. This protects users from runaway token spend and lockups while preserving normal tool access. The severity progression is:

- Warnings come first.
- Suppression follows when patterns persist past the warning threshold.
- Critical thresholds block the next tool-cycle and surface a clear loop-detection reason in the run record.
- The post-compaction guard emits `compaction_loop_persisted` errors with the offending tool name and identical-call count.

**Source**: OpenClaw documentation — `tools/loop-detection` (mirror `inbox/openclaw_docs/tools/loop-detection.md`)
**Last Updated**: 2026-06-22
**Status**: Active
