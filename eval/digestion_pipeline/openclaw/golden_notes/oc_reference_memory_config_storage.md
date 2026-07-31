---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - memory
keywords:
  - openclaw memory storage config
  - sqlite-vec vector acceleration
  - openclaw-agent.sqlite index storage
  - qmd backend config
  - memory.backend qmd
  - qmd searchMode rerank scope
  - memory dreaming config
  - plugins.entries.memory-core dreaming
topics:
  - OpenClaw
  - Memory Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/memory-config
access_control_group: ["general"]
---

# OpenClaw — Memory Storage & Backend Configuration (sqlite-vec, Index Storage, QMD, Dreaming)

## Overview

This note is the storage/backend half of the OpenClaw memory configuration reference (`reference/memory-config`), covering the knobs that govern WHERE and HOW memory indexes are stored and consolidated — distinct from the search/embedding-provider half digested in [oc_reference_memory_config_search](oc_reference_memory_config_search.md). It documents, verbatim from source: SQLite vector acceleration (`store.vector.*` / sqlite-vec), built-in index storage location and the FTS5 tokenizer knob (`store.fts.tokenizer`), the QMD local-first sidecar backend (`memory.backend = "qmd"` plus the full `memory.qmd.*` knob set: command, searchMode, rerank, includeDefaultMemory, paths, sessions, update schedule, limits, scope, citations), and the Dreaming background memory-consolidation config under `plugins.entries.memory-core.config.dreaming`.

## SQLite Vector Acceleration (sqlite-vec)

These knobs accelerate vector queries on the built-in SQLite backend.

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `store.vector.enabled` | `boolean` | `true` | Use sqlite-vec for vector queries |
| `store.vector.extensionPath` | `string` | bundled | Override sqlite-vec path |

When sqlite-vec is unavailable, OpenClaw falls back to in-process cosine similarity automatically — so vector search continues to work even if the native extension cannot be loaded, just without the acceleration.

## Index Storage

Built-in memory indexes live in each agent's OpenClaw SQLite database at `agents/<agentId>/agent/openclaw-agent.sqlite`. The only configurable index-storage knob on the built-in backend is the FTS5 tokenizer.

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `store.fts.tokenizer` | `string` | `unicode61` | FTS5 tokenizer (`unicode61` or `trigram`) |

## QMD Backend Config

Set `memory.backend = "qmd"` to enable the QMD local-first sidecar backend. All QMD settings live under `memory.qmd`.

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `command` | `string` | `qmd` | QMD executable path; set an absolute path when service `PATH` differs from your shell |
| `searchMode` | `string` | `search` | Search command: `search`, `vsearch`, `query` |
| `rerank` | `boolean` | -- | Set to `false` with `searchMode: "query"` and QMD 2.1+ to skip QMD reranking |
| `includeDefaultMemory` | `boolean` | `true` | Auto-index `MEMORY.md` + `memory/**/*.md` |
| `paths[]` | `array` | -- | Extra paths: `{ name, path, pattern? }` |
| `sessions.enabled` | `boolean` | `false` | Index session transcripts |
| `sessions.retentionDays` | `number` | -- | Transcript retention |
| `sessions.exportDir` | `string` | -- | Export directory |

`searchMode: "search"` is lexical/BM25-only. OpenClaw does not run semantic vector readiness probes or QMD embedding maintenance for that mode, including during `memory status --deep`; `vsearch` and `query` continue to require QMD vector readiness and embeddings. `rerank: false` only changes QMD `query` mode and requires QMD 2.1 or newer — in direct CLI mode OpenClaw passes `--no-rerank`; in mcporter-backed MCP mode it passes `rerank: false` to QMD's unified query tool. Leave `rerank` unset to use QMD's default query reranking behavior.

OpenClaw prefers current QMD collection and MCP query shapes, but keeps older QMD releases working by trying compatible collection pattern flags and older MCP tool names when needed. When QMD advertises support for multiple collection filters, same-source collections are searched with one QMD process, while older QMD builds keep the per-collection compatibility path. Same-source means durable memory collections are grouped together, while session transcript collections remain a separate group so source diversification still has both inputs. QMD model overrides stay on the QMD side, not OpenClaw config; to override QMD's models globally, set environment variables such as `QMD_EMBED_MODEL`, `QMD_RERANK_MODEL`, and `QMD_GENERATE_MODEL` in the gateway runtime environment.

### Update Schedule (`memory.qmd.update`)

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `update.interval` | `string` | `5m` | Refresh interval |
| `update.debounceMs` | `number` | `15000` | Debounce file changes |
| `update.onBoot` | `boolean` | `true` | Refresh when the long-lived QMD manager opens; set false to skip the immediate boot update |
| `update.startup` | `string` | `off` | Optional gateway-start QMD initialization: `off`, `idle`, or `immediate` |
| `update.startupDelayMs` | `number` | `120000` | Delay before `startup: "idle"` refresh runs |
| `update.waitForBootSync` | `boolean` | `false` | Block manager opening until its initial refresh completes |
| `update.embedInterval` | `string` | -- | Separate embed cadence |
| `update.commandTimeoutMs` | `number` | -- | Timeout for QMD commands |
| `update.updateTimeoutMs` | `number` | -- | Timeout for QMD update operations |
| `update.embedTimeoutMs` | `number` | -- | Timeout for QMD embed operations |

When gateway-start QMD initialization is enabled, OpenClaw starts QMD only for eligible agents. If `update.onBoot` is true and no interval/embed maintenance is configured, startup uses a one-shot manager for the boot refresh and closes it. If an update or embed interval is configured, startup opens the long-lived QMD manager so it can own the watcher and interval timers; `update.onBoot: false` skips only the immediate boot refresh.

### Limits (`memory.qmd.limits`)

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `limits.maxResults` | `number` | `6` | Max search results |
| `limits.maxSnippetChars` | `number` | -- | Clamp snippet length |
| `limits.maxInjectedChars` | `number` | -- | Clamp total injected chars |
| `limits.timeoutMs` | `number` | `4000` | Search timeout |

### Scope (`memory.qmd.scope`)

Scope controls which sessions can receive QMD search results, using the same schema as `session.sendPolicy`. The shipped default allows direct and channel sessions, while still denying groups; the documented default is DM-only. `match.keyPrefix` matches the normalized session key; `match.rawKeyPrefix` matches the raw key including `agent:<id>:`.

```json5
{
  memory: {
    qmd: {
      scope: {
        default: "deny",
        rules: [{ action: "allow", match: { chatType: "direct" } }],
      },
    },
  },
}
```

### Citations (`memory.citations`)

`memory.citations` applies to all backends, not just QMD.

| Value | Behavior |
| --- | --- |
| `auto` (default) | Include `Source: <path#line>` footer in snippets |
| `on` | Always include footer |
| `off` | Omit footer (path still passed to agent internally) |

### Full QMD Example

```json5
{
  memory: {
    backend: "qmd",
    citations: "auto",
    qmd: {
      includeDefaultMemory: true,
      update: { interval: "5m", debounceMs: 15000 },
      limits: { maxResults: 6, timeoutMs: 4000 },
      scope: {
        default: "deny",
        rules: [{ action: "allow", match: { chatType: "direct" } }],
      },
      paths: [{ name: "docs", path: "~/notes", pattern: "**/*.md" }],
    },
  },
}
```

For agent-scoped cross-agent transcript search, use `agents.list[].memorySearch.qmd.extraCollections` instead of `memory.qmd.paths`. Those extra collections follow the same `{ path, name, pattern? }` shape but are merged per agent and can preserve explicit shared names when the path points outside the current workspace. If the same resolved path appears in both `memory.qmd.paths` and `memorySearch.qmd.extraCollections`, QMD keeps the first entry and skips the duplicate.

## Dreaming

Dreaming is the background memory-consolidation sweep, configured under `plugins.entries.memory-core.config.dreaming` — NOT under `agents.defaults.memorySearch`. It runs as one scheduled sweep and uses internal light/deep/REM phases as an implementation detail (the phase policy and thresholds are internal behavior, not user-facing config; for conceptual behavior and slash commands, see the Dreaming concept page).

### User Settings (`plugins.entries.memory-core.config.dreaming`)

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `false` | Enable or disable dreaming entirely |
| `frequency` | `string` | `0 3 * * *` | Optional cron cadence for the full dreaming sweep |
| `model` | `string` | default model | Optional Dream Diary subagent model override |
| `phases.deep.maxPromotedSnippetTokens` | `number` | `160` | Maximum estimated tokens kept from each short-term recall snippet promoted into `MEMORY.md`; provenance metadata remains visible |

### Example

```json5
{
  plugins: {
    entries: {
      "memory-core": {
        subagent: {
          allowModelOverride: true,
          allowedModels: ["anthropic/claude-sonnet-4-6"],
        },
        config: {
          dreaming: {
            enabled: true,
            frequency: "0 3 * * *",
            model: "anthropic/claude-sonnet-4-6",
          },
        },
      },
    },
  },
}
```

Source notes on dreaming behavior: dreaming writes machine state to `memory/.dreams/` and human-readable narrative output to `DREAMS.md` (or an existing `dreams.md`). `dreaming.model` uses the existing plugin subagent trust gate, so set `plugins.entries.memory-core.subagent.allowModelOverride: true` before enabling it. The Dream Diary retries once with the session default model when the configured model is unavailable; trust or allowlist failures are logged and are not silently retried.

**Source**: OpenClaw documentation — `reference/memory-config` (mirror `inbox/openclaw_docs/reference/memory-config.md`), storage/backend half
**Last Updated**: 2026-06-22
**Status**: Active
