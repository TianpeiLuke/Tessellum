---
tags:
  - resource
  - terminology
  - openclaw
  - memory-dreaming
  - memory-consolidation
  - background-task
keywords:
  - Dreaming
  - memory dreaming
  - sleep-cycle memory consolidation
  - light deep REM phases
  - background memory consolidation
  - recovery threshold
topics:
  - Agent memory
  - Memory consolidation
  - OpenClaw memory architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://docs.openclaw.ai/concepts/dreaming
access_control_group: ["general"]
---

# Dreaming — OpenClaw Memory Consolidation

## Definition

**Dreaming** is OpenClaw's experimental, opt-in **background memory-consolidation subsystem**, implemented in `src/memory-host-sdk/dreaming.ts` (659 LOC). It runs **outside the agent's interactive turn** on a cron schedule and promotes high-signal short-term traces (recent daily memory files, redacted session transcripts, recall state) into the agent's durable long-term store. The design borrows its phase architecture from **mammalian sleep-driven memory consolidation**: a closed three-element phase discriminant `"light" | "deep" | "rem"` mirrors the slow-wave-sleep (SWS) / REM cycling that neuroscience identifies as the substrate of systems-level consolidation — SWS supports replay of hippocampal traces into neocortex while REM supports cross-trace pattern synthesis, the same division of labour OpenClaw assigns to its **deep** and **REM** phases.

The metaphor is not decorative: the three phases run at different cadences and cost profiles (light every ~6 h cheap-and-fast, deep nightly balanced, REM weekly slow-and-expensive), each with its own threshold gates, source set, and `MemoryDreamingExecutionConfig` (speed / thinking / budget). A separate **recovery** sub-system inside the deep phase re-promotes memories whose health score drops below `triggerBelowHealth` (default `0.35`), and any candidate above `autoWriteMinConfidence` (default `0.97`) is auto-written without further review.

## Context

Dreaming is the **OpenClaw-specific instance of the broader industry pattern** of moving memory consolidation off the agent's hot path. LangChain calls the same pattern **"sleep-time compute"** — a separate consolidation agent reviewing recent conversations on a cron schedule and merging key facts into the long-term store, recommended when "you need to reduce latency or improve memory quality across many conversations." LangMem ships an equivalent background memory manager bound to LangGraph's Long-term Memory Store.

What distinguishes OpenClaw's variant is the **neurally-inspired phasing**: instead of one undifferentiated background pass, the three phases each model a distinct cognitive role (dedup-and-stage / score-and-promote / cross-memory synthesis), and the recovery subsystem mirrors the way mammalian sleep re-stabilises previously-consolidated traces that have decayed. Like mammalian sleep, Dreaming is **disabled by default** (`DEFAULT_MEMORY_DREAMING_ENABLED = false`) — it is an opt-in feature, not a hard runtime dependency.

## Key Characteristics

- **Three named phases with distinct cadences (sleep-stage prefix):**
  - **Light** (every ~6 h via `0 */6 * * *`, lookback 2 days, limit 100) — ambient dedup-and-stage pass over `["daily", "sessions", "recall"]`, gated by a `dedupeSimilarity` threshold.
  - **Deep** (daily at 03:00 via `0 3 * * *`) — long-term consolidation gated by `minScore` / `minRecallCount` / `minUniqueQueries` / `recencyHalfLifeDays`, sourced from `["daily", "memory", "sessions", "logs", "recall"]`, with optional `maxAgeDays` cutoff.
  - **REM** (weekly Sunday 05:00, lookback 7 days) — cross-memory pattern synthesis at `minPatternStrength` ≥ `0.75`, sourced from `["memory", "daily", "deep"]`.
- **Deep-phase recovery sub-system** — when memory health drops below `triggerBelowHealth` (default `0.35`), the recovery resolver re-promotes candidates with `minRecoveryConfidence`; candidates above `autoWriteMinConfidence` (default `0.97`) auto-write to durable storage.
- **Per-phase resolvers + projection wrappers** — `resolveMemoryDeepDreamingConfig`, `resolveMemoryLightDreamingConfig`, `resolveMemoryRemDreamingConfig` each call the unified `resolveMemoryDreamingConfig` and AND-combine global `enabled` with the phase's `enabled` so a globally-disabled flag kills every phase regardless of per-phase settings.
- **Phase-specialized default execution overrides** — light pins `{speed: "fast", thinking: "low", budget: "cheap"}`, deep pins `{speed: "balanced", thinking: "high", budget: "medium"}`, REM pins `{speed: "slow", thinking: "high", budget: "expensive"}`, each layered on top of a shared `defaultExecution`.
- **Timezone-aware day-key formatter** — `formatMemoryDreamingDay(epochMs, timezone)` produces `YYYY-MM-DD` via `Intl.DateTimeFormat("en-CA")` so daily-report buckets respect the user's local midnight, with a host-local fallback for invalid IANA zones.
- **Canonical-path workspace dedupe** — `resolveMemoryDreamingWorkspaces` buckets agents by `normalizePathForComparison(workspaceDir)` so trailing-slash / case differences collapse into one workspace with merged `agentIds`, ensuring the scheduler visits each workspace exactly once.
- **Normalizer family** — `normalizeBoolean`, `normalizeScore` (clamped to `[0,1]`, NaN/Infinity-safe), `normalizeSimilarity` (alias), `normalizeStringArray` (closed-set allowed list with dedupe), and the `normalizeSpeed/Thinking/Budget/StorageMode` literal-coerce quartet — every config field flows through one of these total `(value: unknown, fallback) => T` coercers.
- **Plugin-id resolver with sentinel rejection** — `resolveMemoryDreamingPluginId` reads `plugins.slots.memory` but rejects the `"none"` sentinel (case-insensitive), falling back to `DEFAULT_MEMORY_DREAMING_PLUGIN_ID = "memory-core"`.
- **Storage mode** — `inline` | `separate` | `both` controls whether promoted memories are written to the agent's primary memory file or to dedicated dream reports.

## Related Terms


## Related Code Snippets

- [OpenClaw Memory — dreaming.ts (split 1 of 2) — Constants, Type Taxonomy, and Normalizers](../code_snippets/snippet_openclaw_memory_dreaming_constants.md)
- [OpenClaw Memory — dreaming.ts (split 2 of 2) — Config Resolvers and Day/Workspace Utilities](../code_snippets/snippet_openclaw_memory_dreaming_resolvers.md)

## Related Analysis (FZ 15)


## References

- [Memory consolidation — Wikipedia](https://en.wikipedia.org/wiki/Memory_consolidation) — Class-1 reference on systems-level consolidation; the "Sleep consolidation" subsection covers neocortex-hippocampus interactions during sleep that motivate Dreaming's phase split.
- [Sleep and memory — Wikipedia](https://en.wikipedia.org/wiki/Sleep_and_memory) — Class-1 reference covering SWS, REM, hippocampal replay, and sleep spindles as the neural substrate the OpenClaw phase architecture mirrors.
- [Deep Agents — Memory (LangChain docs)](https://docs.langchain.com/oss/python/deepagents/memory) — Class-2 industry reference on background "sleep-time compute" memory consolidation; defines the cron-scheduled consolidation-agent pattern that Dreaming instantiates with neurally-inspired phasing.
- [Dreaming — OpenClaw docs](https://docs.openclaw.ai/concepts/dreaming) — Primary upstream documentation for the subsystem.
- [OpenClaw `dreaming.ts` source](https://github.com/openclaw/openclaw/blob/main/src/memory-host-sdk/dreaming.ts) — Verbatim source of the 659-LOC consolidation host (constants, type taxonomy, normalizers, resolvers).
