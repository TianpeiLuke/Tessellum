---
title: Hermes Agent Docs Digestion — Sub-Plan 18 — Developer: Internals
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/
pages:
  - developer-guide/architecture.md
  - developer-guide/agent-loop.md
  - developer-guide/prompt-assembly.md
  - developer-guide/context-compression-and-caching.md
  - developer-guide/gateway-internals.md
  - developer-guide/session-storage.md
  - developer-guide/provider-runtime.md
  - developer-guide/tools-runtime.md
  - developer-guide/cron-internals.md
  - developer-guide/acp-internals.md
  - developer-guide/trajectory-format.md
  - developer-guide/browser-supervisor.md
  - developer-guide/plugin-llm-access.md
---

# Sub-Plan 18: Developer: Internals

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP18's note
> filenames/BBs/coverage are defined.

## Scope

The developer-facing internals layer of the Hermes Agent docs: how each subsystem actually behaves at
runtime — the top-level architecture map, the agent loop, prompt assembly, the dual context-compression
system + prompt caching, the messaging-gateway dispatch path, the SQLite/FTS5 session store, provider
runtime resolution, the tool registry/dispatch, cron scheduling, the ACP server, the ShareGPT trajectory
format, the browser CDP supervisor, and the `ctx.llm` plugin LLM-access lane. Source = 13 mirrored pages
in `inbox/hermes_agent_docs/developer-guide/` (all substantive). **P3 / Developer wave.** These are
**subsystem-behavior/architecture** descriptions — the dominant BB is **model** (1 per page); each note
documents *how a subsystem behaves* and **cross-links down** to the existing `snippet_hermes_agent_*`
implementation corpus and the `repo_hermes_agent_*` repo notes for *how it is implemented*. Concepts
already captured as term notes are **linked, not recreated**.

## Content Strategy

- **One BB per note.** Every page is a single cohesive subsystem-behavior description → **model** BB.
  Each of the 13 pages maps 1→1 to one note (no splits needed — see Density Re-Assessment; even the two
  pages master-marked `[SPLIT]` on a code-block count, `context-compression-and-caching` (14 code) and
  `session-storage` (17 code), are single-BB clusters that stay ≤2500w by curating code to ≤6 blocks).
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: the
  user-facing config knobs for compression/context-engine (SP02 `hermes_runtime_context_settings`),
  the user-facing session/CLI surface (SP02 `hermes_sessions_lifecycle_resume`/`hermes_session_search_storage`),
  the messaging-platform setup pages (SP11-13), the provider catalog (SP14), the MCP/ACP/provider-routing
  feature pages (SP09), cron/delegation/code-exec/hooks/plugins feature pages (SP06), browser/voice/vision
  feature pages (SP08), and the developer *extending* pages (SP19 plugin-authoring: adding-providers,
  creating-skills, context-engine-plugin, model-provider-plugin). SP18 is the **behavior** layer; SP19 is
  the **how-to-extend** layer.
- **SP18 owns 1 NEW term capture: `term_context_compression`** (Hermes' dual-threshold compaction —
  85% gateway session hygiene + 50% in-loop agent `ContextCompressor`). Collision-audited below against
  the existing generic `term_compaction` and `term_context_engine` (both LINK, not dup).
- **Collision (augment): `term_compaction.md` (97L, active) is the GENERIC industry-wide compaction
  concept** (OpenClaw-rooted; explicitly cross-references Anthropic `context_management.compaction`,
  Microsoft `ChatHistoryCompaction`, LangChain `ConversationSummaryMemory`). The planned
  `term_context_compression` is **NOT a duplicate** — it is the Hermes-specific *dual-threshold two-layer*
  mechanism (gateway 85% safety net + agent 50% configurable + 4-phase algorithm + Codex gpt-5.5 autoraise).
  CREATE `term_context_compression`; LINK `term_compaction` (generic foundation) + `term_context_engine`
  (the pluggable ABC the compressor implements).
- **Collision: `term_context_engine.md` (81L, active) covers the pluggable ContextEngine concept** — the
  planned `hermes_context_compression_caching` doc note documents Hermes' compressor *behavior*; different
  BB scope → LINK, do not recreate.
- **Collision: `term_session_persistence.md` (131L, active) covers the generic sticky-sessions concept** —
  the planned `hermes_session_storage` is a model note for Hermes' concrete SQLite/FTS5 schema → LINK.

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — wc)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| developer-guide/architecture.md | 1644 | 6 | model | 1 |
| developer-guide/agent-loop.md | 1382 | 5 | model | 1 |
| developer-guide/prompt-assembly.md | 1777 | 5 | model | 1 |
| developer-guide/context-compression-and-caching.md | 2049 | 14 | model | 1 (curate code) |
| developer-guide/gateway-internals.md | 1546 | 6 | model | 1 |
| developer-guide/session-storage.md | 1555 | 17 | model | 1 (curate code) |
| developer-guide/provider-runtime.md | 1156 | 0 | model | 1 |
| developer-guide/tools-runtime.md | 1266 | 4 | model | 1 |
| developer-guide/cron-internals.md | 1820 | 6 | model | 1 |
| developer-guide/acp-internals.md | 693 | 3 | model | 1 |
| developer-guide/trajectory-format.md | 1012 | 8 | model | 1 (curate code) |
| developer-guide/browser-supervisor.md | 1163 | 2 | model | 1 |
| developer-guide/plugin-llm-access.md | 2254 | 10 | model | 1 (curate code) |

(Re-measured 2026-06-19 against mirror c253b07 using the ledger convention — BODY only, frontmatter
stripped; code-block count = `^\s*```` lines ÷ 2 — so these now match the master ledger exactly. All
within the ≤2500w / ≤6-code cap.)

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **13 notes — all model BB.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_architecture.md` | model | architecture §System Overview, §Directory Structure, §Data Flow (CLI/Gateway/Cron), §Recommended Reading Order, §Major Subsystems (×10), §Design Principles, §File Dependency Chain | ~1450 | Top-level internals map: the six entry points feeding one `AIAgent` (`run_agent.py`), the prompt/provider/tool/compression sub-blocks, session+tool backends, the three data-flow paths, the 10 major subsystems with reading order, the 6 design principles, and the import-time tool-registration dependency chain. |
| 2 | `hermes_agent_loop.md` | model | agent-loop §Core Responsibilities, §Two Entry Points, §API Modes, §Turn Lifecycle (+Message Format, Alternation Rules), §Interruptible API Calls, §Tool Execution (Sequential/Concurrent, Flow, Agent-Level Tools), §Callback Surfaces, §Budget and Fallback Behavior, §Compression and Persistence, §Key Source Files | ~1300 | The `AIAgent` orchestration engine: `chat()`/`run_conversation()` entry points, the 3 API modes + resolution order, the 9-step turn lifecycle, OpenAI message format + strict role-alternation rules, interruptible threaded API calls, sequential-vs-concurrent tool execution + the 4 intercepted agent-level tools, the 8 callback surfaces, iteration budget + fallback chain, and compression/persistence hooks. |
| 3 | `hermes_prompt_assembly.md` | model | prompt-assembly §Cached system prompt layers (+example), §Persistent Memory, §User Profile, §Skills, §AGENTS.md, §How SOUL.md appears, §How context files are injected (+discovery), §API-call-time-only layers, §Memory snapshots, §Context files, §Skills index, §Supported customization surfaces, §Why split this way | ~1600 | The system-prompt assembly model: the three ordered cached tiers (`stable`→`context`→`volatile`), SOUL.md identity loading + fallback, the first-match-wins context-file priority (`.hermes.md`/`AGENTS.md`/`CLAUDE.md`/`.cursorrules`) with security-scan + 20K truncation, the API-call-time-only ephemeral layers kept out of the cached prefix, and the supported customization surfaces vs editing code. |
| 4 | `hermes_context_compression_caching.md` | model | context-compression §Pluggable Context Engine, §Dual Compression System (Gateway 85% / Agent 50%), §Configuration (+Parameter Details, Codex gpt-5.5 autoraise, Computed Values), §Compression Algorithm (Phases 1-4 + Iterative Re-compression), §Before/After Example, §Prompt Caching (system_and_3, How It Works, Cache-Aware Patterns, Enabling), §Context Pressure Warnings | ~1900 | The dual context-compression + Anthropic prompt-caching model: the `ContextEngine` ABC with config-driven engine selection, the two independent compression layers (gateway hygiene 85% safety net + agent `ContextCompressor` 50% primary, configurable), the Codex gpt-5.5 272K autoraise, the 4-phase compress algorithm (prune→boundaries→structured summary→assemble) + iterative re-compression, and the `system_and_3` 4-breakpoint caching strategy. Owns `term_context_compression`. |
| 5 | `hermes_gateway_internals.md` | model | gateway-internals §Key Files, §Architecture Overview, §Message Flow (+Session Key Format, Two-Level Guard), §Authorization (+DM Pairing), §Slash Command Dispatch (+Running-Agent Guard), §Config Sources, §Platform Adapters (+Token Locks), §Delivery Path, §Hooks (+Events), §Memory Provider Integration (+Flush Lifecycle), §Background Maintenance, §Process Management | ~1450 | The messaging-gateway runtime model: `GatewayRunner` boot + the `agent:main:{platform}:{chat_type}:{chat_id}` session key, the two-level message guard, the 5-layer authorization chain + DM pairing, slash-command dispatch + running-agent guard, the 20+ platform-adapter interface + token locks, the delivery paths, the gateway hook events, memory-provider integration + flush lifecycle, background maintenance (cron tick/expiry/flush), and profile-scoped process management. |
| 6 | `hermes_session_storage.md` | model | session-storage §Architecture Overview, §SQLite Schema (Sessions/Messages/FTS5 + triggers), §Schema Version and Migrations (v1-11), §Write Contention Handling, §Common Operations (init/sessions/messages/titles), §Full-Text Search (basic/FTS5 syntax/filtered/results), §Session Lineage (queries), §Export and Cleanup, §Database Location | ~1750 | The `state.db` session-storage model: WAL-mode SQLite with `sessions`/`messages`/`messages_fts`/`messages_fts_trigram` tables + INSERT/UPDATE/DELETE FTS sync triggers, the 11-version migration chain + declarative `_reconcile_columns()`, write-contention handling (1s timeout, jittered retry, BEGIN IMMEDIATE, periodic WAL checkpoints), the FTS5 query syntax + sanitizer, `parent_session_id` lineage chains (compression splits), and export/prune/cleanup. |
| 7 | `hermes_provider_runtime.md` | model | provider-runtime §Resolution precedence, §Providers, §Output of runtime resolution, §Why this matters, §OpenRouter and custom base URLs, §Native Anthropic path, §OpenAI Codex path, §Auxiliary model routing, §Fallback models (+How it works, What does NOT support fallback, Test coverage) | ~1100 | The shared provider-runtime resolver model (CLI/gateway/cron/ACP/aux): the 4-level resolution precedence, the plugin-backed `ProviderProfile` registry mapping `(provider, model)` → `(api_mode, api_key, base_url)` across 25+ provider families, per-base-URL API-key scoping, the native-Anthropic and Codex Responses paths, auxiliary-task routing, and the `(provider, model)` fallback chain with its 3 trigger points + what does NOT support fallback (subagents, aux tasks). |
| 8 | `hermes_tools_runtime.md` | model | tools-runtime §Tool registration model (+`registry.register()`, Discovery), §Tool availability (`check_fn`), §Toolset resolution (+`get_tool_definitions()`, Legacy names), §Dispatch (+flow, Error wrapping, Agent-loop tools, Async bridging), §DANGEROUS_PATTERNS approval flow, §Terminal/runtime environments, §Concurrency | ~1200 | The tool registry/dispatch runtime model: import-time `registry.register()` self-registration into the singleton `ToolRegistry`, AST-based `discover_builtin_tools()` auto-discovery + MCP/plugin discovery, `check_fn` availability gating, toolset resolution + `get_tool_definitions()` filtering + dynamic schema patching, the model-tool-call→handler dispatch flow + two-level error wrapping, the 4 intercepted agent-loop tools, async bridging across CLI/gateway/worker paths, and the DANGEROUS_PATTERNS approval flow. |
| 9 | `hermes_cron_internals.md` | model | cron-internals §Key Files, §Scheduling Model, §Job Storage (+Lifecycle States, Backward Compat), §Scheduler Runtime (Tick Cycle, Gateway Integration, Fresh Session Isolation), §Skill-Backed Jobs (+Script-Backed, Provider Recovery), §Delivery Model (+Response Wrapping, Session Isolation), §Recursion Guard, §Locking, §CLI Interface | ~1550 | The cron subsystem model: the 4 schedule formats + single `cronjob` action tool, atomic `jobs.json` storage + 4 lifecycle states, the 60s tick cycle with fresh-session isolation, skill-backed + script-backed jobs (3-layer script timeout) + provider recovery (fallback + credential pool), the platform delivery model + `[SILENT]` suppression + session-isolation (no gateway mirroring), the recursion guard (cronjob toolset disabled), and cross-process file locking. |
| 10 | `hermes_acp_internals.md` | model | acp-internals §Boot flow, §Major components (HermesACPAgent, SessionManager, Event bridge, Permission bridge, Tool rendering), §Session lifecycle (+Cancelation, Forking), §Provider/auth behavior, §Working directory binding, §Duplicate same-name tool calls, §Approval callback restoration, §Current limitations | ~900 | The ACP-adapter model: wrapping the sync `AIAgent` in an async JSON-RPC stdio server, the boot flow (`hermes acp` → `HermesACPAgent` over stdio), the 5 components (agent/SessionManager/event-bridge/permission-bridge/tool-rendering), the session lifecycle (new/prompt/cancel/fork), reuse of the shared runtime resolver for auth, editor-cwd binding, FIFO duplicate-tool-call tracking, approval-callback restoration, and current limitations. |
| 11 | `hermes_trajectory_format.md` | model | trajectory-format §File Naming Convention, §JSONL Entry Format (CLI/Batch), §Conversations Array (ShareGPT + Complete Example), §Normalization Rules (Reasoning markup, Tool Call, Tool Response, System Message), §Loading Trajectories (+HuggingFace), §Controlling Trajectory Saving | ~1000 | The ShareGPT trajectory data-format model: the success/failure JSONL files + batch-runner variant with `tool_stats`/`tool_error_counts`, the ShareGPT role mapping (system/human/gpt/tool), the normalization rules (`<think>` reasoning markup, XML-wrapped `<tool_call>`/`<tool_response>`, save-time system message), JSONL + HuggingFace loading, and the `agent.save_trajectories` controls. |
| 12 | `hermes_browser_supervisor.md` | model | browser-supervisor §Backend support, §Architecture (CDPSupervisor, Lifecycle, Dialog policy), §Agent surface (`browser_dialog`, `browser_snapshot` extension, Availability gating), §Cross-origin iframe interaction, §File layout, §Non-goals, §Testing | ~1100 | The browser CDP-supervisor model: a persistent per-`task_id` WebSocket to the backend CDP endpoint that closes the native-JS-dialog and cross-origin-iframe gaps, the 3-backend support matrix (local Chrome/Browserbase/Camofox) + the Browserbase fetch-bridge quirk, the supervisor's dialog queue / frame tree / session map, the 3 dialog policies, the `browser_dialog` tool + `browser_snapshot` extension fields, and OOPIF interaction via `browser_cdp(frame_id=...)`. |
| 13 | `hermes_plugin_llm_access.md` | model | plugin-llm-access §The smallest call, §A more complete chat example, §Structured output, §What this lane gives you, §Quick start (`/tldr`, `/paste-to-tasks`), §When to use which, §API surface (`complete()`, `complete_structured()`, Async, Result attributes), §Trust gate (+What the gate enforces/doesn't), §What the host owns, §What the plugin owns, §Where this fits | ~1900 | The `ctx.llm` plugin LLM-access model: the four-shape surface (`complete`/`complete_structured` × sync/async), host-owned credentials + provider resolution + vision routing + fallback + audit, the fail-closed trust gate (provider/model/agent_id/profile overrides denied until `plugins.entries` opt-in, each independently gated), the result attributes (`text`/`parsed`/`usage`/`audit`), and where `ctx.llm` fits among the other `ctx.register_*` plugin surfaces. |

**SP18 totals:** 13 notes · model 13 · (no procedure/concept/navigation — every page is a subsystem-behavior
description). 13 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 13 · model 13 · (concepts referenced are existing/owned term notes, not doc notes).
- Source: 13 digested pages (~18.7K words measured body+code) → ~16.7K words of notes (modest compression
  via code-curation + link-outs to feature pages).
- BB mix: model 100% (this is the architecture/internals sub-plan — by design dominated by model BB,
  matching the master's note that SP18 is "mostly model BB — these describe how subsystems behave").

## Section Coverage Map

```
architecture.md (1644w) ── ALL sections ─────────────────── → Note 1 (subsystem deep-dives link to Notes 2-13; reading-order links resolve at finalization)
agent-loop.md (1382w) ── ALL sections ───────────────────── → Note 2 (compression detail→Note 4; provider→Note 7; tools→Note 8; sessions→Note 6)
prompt-assembly.md (1777w) ── ALL sections ──────────────── → Note 3 (SOUL/AGENTS user-facing→SP05; caching→Note 4; hooks pre_llm_call→SP06)
context-compression-and-caching.md (2049w)
├── Pluggable Context Engine / Dual Compression / Configuration / Codex autoraise / Computed Values → Note 4 (config knobs→SP02; engine plugin→SP19)
├── Compression Algorithm (Phases 1-4 + Iterative Re-compression) ─────────────────────────────── → Note 4
├── Before/After Example ──────────────────────────────────────────────────────────────────────── → Note 4
└── Prompt Caching (system_and_3 / How It Works / Cache-Aware / Enabling) / Context Pressure Warnings → Note 4
gateway-internals.md (1546w) ── ALL sections ────────────── → Note 5 (platform setup→SP11-13; hooks feature→SP06; memory providers→SP05; sessions→Note 6)
session-storage.md (1555w) ── ALL sections ──────────────── → Note 6 (user-facing session CLI→SP02; lineage on compression→Note 4)
provider-runtime.md (1156w) ── ALL sections ─────────────── → Note 7 (provider catalog→SP14; routing/fallback feature→SP09; adding providers→SP19)
tools-runtime.md (1266w) ── ALL sections ────────────────── → Note 8 (toolsets/tools reference→SP21; code-exec/delegation feature→SP06; adding tools→SP19)
cron-internals.md (1820w) ── ALL sections ───────────────── → Note 9 (cron feature guide→SP06; gateway→Note 5; fallback→Note 7)
acp-internals.md (693w) ── ALL sections ─────────────────── → Note 10 (acp feature→SP09; sessions→Note 6; provider→Note 7)
trajectory-format.md (1012w) ── ALL sections ────────────── → Note 11 (batch/RL→repo_hermes_agent_trajectory_research)
browser-supervisor.md (1163w) ── ALL sections ───────────── → Note 12 (browser feature→SP08; computer-use→SP08)
plugin-llm-access.md (2254w) ── ALL sections ────────────── → Note 13 (provider runtime→Note 7; hooks/plugins feature→SP06; build-plugin guide→SP17; adding providers→SP19)
```

No source H2/H3 orphaned. All 13 pages fully covered; cross-subsystem detail intentionally routed to the
owning notes (within SP18) or owning SPs (as link-outs).

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| (none) | — | All 13 pages are single-BB (model) subsystem-behavior descriptions ≤2500w. The two pages the master ledger tagged `[SPLIT]` were flagged on a *code-block* heuristic (`context-compression-and-caching` 14 code, `session-storage` 17 code) — not a word-count or BB-mixing trigger. Per the density caps, code-heavy notes are kept as ONE note by **curating** the source code blocks to ≤6 load-bearing examples (kept verbatim) and summarizing the rest in prose; no BB mixing exists to force a split. Confirmed by re-read (Density Re-Assessment). |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; search term_dictionary AND documentation/)

| Planned note / slug | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `term_context_compression` (OWNED new term) | `term_compaction.md` (97L active), `term_context_engine.md` (81L active), `term_progressive_summarization.md`, `term_compound_ai_system.md` | **NOT a dup** — `term_compaction` is the *generic* industry-wide concept (OpenClaw-rooted, cross-refs Anthropic/MS/LangChain); `term_context_engine` is the *pluggable ABC*. `term_context_compression` is the **Hermes-specific dual-threshold two-layer mechanism** (gateway 85% hygiene + agent 50% configurable + 4-phase algorithm + Codex gpt-5.5 autoraise) | CREATE `term_context_compression`; LINK `term_compaction` (foundation) + `term_context_engine` (component). Specificity OK — slug is scope-qualified ("context compression", distinct from bare "compaction"). |
| `hermes_context_compression_caching` (doc) | `term_compaction`, `term_context_engine` | **NOT a dup** — those are concept terms; this is the doc note for Hermes' compressor *behavior* (model BB) | CREATE; LINK both terms + the new `term_context_compression`. |
| `hermes_session_storage` (doc) | `term_session_persistence.md` (131L active, "sticky sessions"), `term_fts5`, `term_sqlite_vec` | **NOT a dup** — `term_session_persistence` is the generic concept; this is Hermes' concrete `state.db` SQLite/FTS5 schema model | CREATE; LINK `term_session_persistence`/`term_fts5`/`term_sqlite_vec`. |
| `hermes_agent_loop`, `hermes_provider_runtime` (doc) | `term_agent_harness`, `term_agent_orchestration`, `term_provider_plugin`, `term_failover` | **NOT a dup** — those are component concepts the notes use | CREATE; LINK as related. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords;
**0 substantive same-concept duplicates** (the `term_compaction`/`term_context_engine`/`term_session_persistence`
hits are LINK-not-dup, confirmed by reading the notes). New `hermes_agent/` folder → no doc-doc collisions
(intra-series links resolve at finalization).

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **FOUR-FLOOR standard set 2026-06-19 (user directive — supersedes all prior floors).** Each note's
> `## Related Notes` now carries **four COUNTED floors**, all relevancy-selected to the note's actual page
> content and each rendered as `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`:
>   the 13 `repo_hermes_agent_*` notes that digest the Hermes SOURCE CODE; the chosen repos are the ones whose
>   modules implement what THIS doc note describes),
>   517-note Hermes implementation corpus; the chosen snippets are the ones whose CODE this note documents). **This
>   is now a COUNTED floor (raised from the prior 8 and promoted from "bonus"), no longer optional.**
> - **≥10 DOCUMENTATION notes** (`../../documentation/`, relevancy-selected — sibling `hermes_*` in this series
>
> The prior floor was ≥8 term + ≥8 snippet + ≥5 doc. This levelling-up is **additive**: every previously-mapped
> term/snippet/doc that is still relevant is kept; snippets are raised 8→≥10 and counted; a ≥5 code-repo floor and a
> ≥10 doc floor are added. Relevancy first, never pad.
> `resources/documentation/hermes_agent/` at finalization (G5/G8) and are allowed to not-yet-exist. Snippet IDs are
> shown as bare suffixes — the full note id is `resources/code_snippets/snippet_hermes_agent_<suffix>.md`.
> Owned/other-SP not-yet-existing terms are marked `[own]`/`(+fin …)` and are ADDITIONAL forward-refs, NOT counted to
> the ≥8 term floor: `term_context_compression` `[own]`→SP18, `term_messaging_gateway`→SP11,
> `term_credential_pool`/`term_fallback_provider`/`term_provider_routing`→SP09.
> (Correction 2026-06-19: the ACP concept term is `term_acp_agent_client_protocol` — the bare `term_acp` slug
> does not exist; used in Note 10 and the Inlinks table.)

**Note 1 `hermes_architecture`** (model)
- Terms (8): term_compound_ai_system, term_agent_harness, term_autonomous_coding_agents, term_agent_orchestration, term_multi_agent_systems, term_subagent, term_context_engine, term_sandbox_backend — relevance: the architecture is one `AIAgent` harness serving 6 entry points, with pluggable context-engine + 6 sandbox backends + subagent delegation; a compound-AI-system map.
- Code-Repos (6): repo_hermes_agent (top-level repo whose module tree IS this map), repo_hermes_agent_agent_core (`run_agent.py`/`agent/` — the `AIAgent` core + prompt/compression sub-blocks), repo_hermes_agent_cli (`cli.py`/`hermes_cli/` — the CLI entry point + provider resolver), repo_hermes_agent_tools (`tools/registry.py` + 70+ tools + 6 terminal backends), repo_hermes_agent_gateway_messaging (`gateway/` — the gateway entry point + session store), repo_hermes_agent_mcp_toolsets (`toolsets.py` + MCP — the 28-toolset grouping the map cites) — relevance: these repos implement the subsystem boxes the architecture diagram enumerates.
- Snippets (10): core_aiagent_orchestrator, core_run_agent_cli, tools_registry, core_context_engine_abc, core_hermes_state, cli_gateway_dispatch, acp_entry, cron_tick, toolsets_definitions, core_prompt_builder_environment — relevance: the `AIAgent` core, CLI entry, tool-registry + toolset definitions, context-engine ABC, state store, prompt-builder, and gateway/ACP/cron entry points the System-Overview + File-Dependency-Chain diagrams enumerate.
- Docs (10): hermes_agent_loop, hermes_prompt_assembly, hermes_provider_runtime, hermes_tools_runtime, hermes_session_storage, hermes_gateway_internals, hermes_cron_internals, hermes_acp_internals (the 8 subsystem deep-dives this map links to via the Recommended Reading Order); cc_agent_sdk_overview (analogous top-level agent-tool architecture overview), cc_agentic_loop (the analogous one-engine-many-surfaces agent loop) — relevance: the in-series subsystem docs the reading-order points at, plus the closest external-agent-tool architecture overviews.

**Note 2 `hermes_agent_loop`** (model)
- Terms (8): term_agent_harness, term_agent_orchestration, term_autonomous_coding_agents, term_function_calling, term_subagent, term_failover, term_context_window, term_llm — relevance: the loop is the orchestration harness — function-calling tool dispatch, fallback on provider errors, iteration budget against the context window, subagent delegation. (+fin: term_context_compression [own])
- Code-Repos (5): repo_hermes_agent_agent_core (`run_agent.py` `AIAgent` — the loop itself + `chat()`/`run_conversation()`), repo_hermes_agent (top-level `model_tools.py` dispatch the loop calls), repo_hermes_agent_tools (`tools/registry.py` handlers the loop dispatches sequentially/concurrently), repo_hermes_agent_providers_adapters (the `(provider,model)` clients + fallback the loop switches), repo_hermes_agent_mcp_toolsets (the tool schemas + agent-level tool interception the loop applies) — relevance: these repos implement the turn lifecycle, tool execution, and fallback the page walks through.
- Snippets (10): core_aiagent_orchestrator, core_conversation_loop_main_loop_entry, core_chat_helpers_interruptible_call, core_chat_helpers_activate_fallback, core_tool_executor_concurrent, core_tool_executor_sequential, core_iteration_budget, core_agent_init_api_mode_resolution, core_conversation_loop_turn_setup, core_chat_helpers_max_iter — relevance: the main loop, interruptible call, fallback activation, sequential/concurrent tool execution, iteration budget, API-mode resolution, per-turn setup, and max-iteration cap code the 9-step turn lifecycle documents.
- Docs (10): hermes_architecture, hermes_provider_runtime, hermes_prompt_assembly, hermes_context_compression_caching, hermes_tools_runtime, hermes_session_storage (in-series: the loop assembles prompts, resolves providers, dispatches tools, compresses, persists); cc_agent_sdk_agent_loop, cc_agentic_loop, cc_agent_sdk_loop_controls, cc_agent_sdk_tool_execution — relevance: the in-series subsystems the loop drives, plus the analogous external agent-loop / loop-controls / tool-execution docs.

**Note 3 `hermes_prompt_assembly`** (model)
- Terms (8): term_prompt_caching, term_context_window, term_persona, term_skills, term_skill_manifest, term_prompt_injection, term_agent_harness, term_llm — relevance: the cached-prefix tiering is built for prompt caching; SOUL.md=persona, skills index, context-file security scan guards prompt injection, all assembled by the harness. (+fin: term_messaging_gateway)
- Code-Repos (5): repo_hermes_agent_agent_core (`agent/prompt_builder.py` + `agent/system_prompt.py` — the tier assembler this page is about), repo_hermes_agent (`run_agent.py` injecting the cached prompt + ephemeral layers), repo_hermes_agent_skills (the bundled skills feeding the stable-tier skills index), repo_hermes_agent_plugins (`pre_llm_call` plugin context appended to the user message), repo_hermes_agent_cli (the SOUL.md / MEMORY.md / context-file customization surfaces) — relevance: these repos implement the stable/context/volatile tiers and the supported customization surfaces.
- Snippets (10): core_prompt_builder_environment, core_prompt_builder_context_loaders, core_prompt_builder_context_helpers, core_prompt_builder_skills_snapshot, core_prompt_caching, core_context_references_parser, core_context_references_expander, core_message_sanitization, core_prompt_builder_subscription_truncate, core_context_references_path_safety — relevance: the prompt-builder tier assembly, first-match context-file loaders, skills snapshot, cache markers, context-reference parse/expand, sanitization, 20K truncation, and path-safety scan code (SOUL.md/AGENTS.md/CLAUDE.md/.cursorrules) this page documents.
- Docs (10): hermes_context_compression_caching, hermes_agent_loop, hermes_session_storage, hermes_architecture, hermes_gateway_internals (in-series: prompt caching, loop, session, gateway-injected context); cc_sdk_customize_system_prompt, cc_sdk_system_prompts, cc_cli_system_prompt_flags, cc_prompt_caching_mechanism, cc_memory_overview — relevance: the in-series subsystems the assembled prompt feeds, plus the analogous system-prompt-customization, prompt-caching, and memory-snapshot docs.

**Note 4 `hermes_context_compression_caching`** (model) — owns `term_context_compression`
- Terms (8): term_context_engine, term_compaction, term_progressive_summarization, term_prompt_caching, term_context_window, term_caching, term_tokenization, term_llm — relevance: Hermes' dual compression implements the `ContextEngine` ABC (generic `compaction`/`progressive_summarization`) over the context window, paired with Anthropic prompt caching measured in tokens. (+own: term_context_compression)
- Code-Repos (5): repo_hermes_agent_agent_core (`agent/context_engine.py` ABC + `agent/context_compressor.py` + `agent/prompt_caching.py` — the compressor + caching this page is about), repo_hermes_agent (`run_agent.py` `_compress_context` preflight 50% trigger), repo_hermes_agent_gateway_messaging (`gateway/run.py` 85% session-hygiene safety net), repo_hermes_agent_plugins (the pluggable context-engine plugin slot, e.g. LCM), repo_hermes_agent_providers_adapters (the auxiliary/summary-model routing + Codex gpt-5.5 272K autoraise) — relevance: these repos implement the dual layers, the 4-phase algorithm, and prompt caching.
- Snippets (10): core_context_engine_abc, core_conversation_compression_entry, core_conversation_compression_strategy, core_manual_compression_feedback, core_prompt_caching, core_conversation_loop_context_overflow, core_aiagent_orchestrator, cli_gateway_dispatch, core_conversation_loop_length_recovery, core_codex_runtime — relevance: the context-engine ABC, compression entry/strategy/feedback, prompt-caching markers, overflow + length recovery, the gateway-hygiene compression path, and the Codex runtime (gpt-5.5 272K autoraise) this page documents.
- Docs (10): hermes_agent_loop, hermes_prompt_assembly, hermes_provider_runtime, hermes_session_storage, hermes_architecture (in-series: the loop triggers compression, prompt assembly caches the prefix, provider runtime routes the summary model, lineage splits land in sessions); cc_prompt_caching_mechanism, cc_what_survives_compaction, cc_reduce_token_usage, cc_cache_lifetime_and_scope, cc_context_window_anatomy — relevance: the analogous prompt-caching mechanism, compaction-survival, token-reduction, cache-lifetime, and context-window-anatomy docs.

**Note 5 `hermes_gateway_internals`** (model)
- Terms (8): term_session_persistence, term_authentication, term_oauth_token, term_human_in_the_loop, term_subagent, term_agent_orchestration, term_websocket, term_idempotency — relevance: the gateway routes sessions, authorizes users (allowlist + DM pairing), runs human-in-the-loop approvals, dispatches over WebSocket adapters, and spawns one `AIAgent` per message. (+fin: term_messaging_gateway, term_credential_pool)
- Code-Repos (5): repo_hermes_agent_gateway_messaging (`gateway/run.py` `GatewayRunner` + `session.py`/`delivery.py`/`pairing.py`/`hooks.py`/`status.py` + 20+ platform adapters — this page IS this repo), repo_hermes_agent_agent_core (the `AIAgent` the gateway spawns per message), repo_hermes_agent_cli (`hermes_cli/commands.py` slash-command resolution + `hermes gateway` lifecycle), repo_hermes_agent_cron (cron ticking the gateway runs as background maintenance), repo_hermes_agent_plugins (memory-provider integration + gateway hook events) — relevance: these repos implement the boot, dispatch, authorization, delivery, and maintenance the page covers.
- Snippets (10): cli_gateway_dispatch, cli_gateway_lifecycle, tools_clarify_gateway, core_shell_hooks_callback, tools_send_dispatch, tools_send_format, core_hermes_state, cli_gateway_pid_discovery, tools_send_attach, cli_gateway_systemd — relevance: the gateway dispatch/lifecycle, approval + hook callbacks, send-message delivery (text/attach), session store, PID-tracking, and systemd/launchctl process-management code this page documents.
- Docs (10): hermes_session_storage, hermes_cron_internals, hermes_acp_internals, hermes_agent_loop, hermes_architecture (in-series: the gateway persists sessions, ticks cron, shares the runtime with ACP, spawns the loop); cc_sessions, cc_hooks_overview, cc_hook_session_lifecycle_events, cc_permission_system_and_rules, cc_channel_permission_relay — relevance: the analogous session-management, hooks, session-lifecycle-events, permission-system, and channel-permission-relay docs (the gateway's authorization + approval + hook surface).

**Note 6 `hermes_session_storage`** (model)
- Terms (8): term_fts5, term_sqlite_vec, term_session_persistence, term_idempotency, term_caching, term_context_window, term_subagent, term_multi_agent_systems — relevance: the model is FTS5 over WAL-mode SQLite with idempotent migrations, write-contention handling for concurrent (multi-agent) writers, and lineage chains spawned by context-window compression. (+fin: term_context_compression [own])
- Code-Repos (5): repo_hermes_agent (`hermes_state.py` `SessionDB` — the `state.db` schema/migrations/FTS5/contention this page is about), repo_hermes_agent_agent_core (`run_agent.py` per-turn session persist + lineage on compression), repo_hermes_agent_gateway_messaging (`gateway/session.py` multi-platform concurrent writer + session-key construction), repo_hermes_agent_cli (`hermes_cli` `/resume` + `session_search` handlers), repo_hermes_agent_acp (ACP sessions persisted to the shared `state.db`) — relevance: these repos implement the writers and readers of the session store the page documents.
- Snippets (10): core_hermes_state, core_hermes_state_schema, core_hermes_state_writes, core_insights_collection, core_insights_reporting, core_conversation_loop_session_persist, cli_hermescli_session_handlers, cli_gateway_dispatch, core_conversation_loop_usage_accounting, cli_hermescli_chat — relevance: the state.db schema, write path with contention handling, insights collection/reporting, per-turn session persist, usage/token accounting (billing columns), and CLI session/resume handler code this page documents.
- Docs (10): hermes_gateway_internals, hermes_agent_loop, hermes_context_compression_caching, hermes_acp_internals, hermes_architecture (in-series: the gateway + loop + ACP write here, compression spawns lineage); cc_sdk_session_store, cc_sdk_session_store_setup, cc_sdk_sessions_overview, cc_sdk_session_management_api, cc_sdk_python_session_functions — relevance: the analogous SDK session-store / session-store-setup / sessions-overview / session-management-API / python-session-function docs (the closest external session-persistence model).

**Note 7 `hermes_provider_runtime`** (model)
- Terms (8): term_provider_plugin, term_model_catalog, term_failover, term_round_robin, term_rate_limiting, term_oauth_token, term_authentication, term_llm — relevance: the resolver maps providers→credentials/api_mode, drives the failover chain on rate-limit/auth errors, rotates pooled keys (round-robin), and resolves OAuth/api-key auth across the model catalog. (+fin: term_fallback_provider, term_provider_routing, term_credential_pool)
- Code-Repos (5): repo_hermes_agent_providers_adapters (`providers/` `ProviderProfile` ABC/registry + `plugins/model-providers/` 25+ families + Anthropic/Codex adapters — this page IS this repo), repo_hermes_agent_cli (`hermes_cli/runtime_provider.py` + `auth.py` + `model_switch.py` — the shared resolver), repo_hermes_agent_agent_core (`agent/auxiliary_client.py` aux routing + `run_agent.py` `_try_activate_fallback`), repo_hermes_agent_plugins (per-provider model-provider plugins that self-register), repo_hermes_agent_cron (cron `run_job()` passing fallback + credential pool into `AIAgent`) — relevance: these repos implement resolution precedence, the fallback chain, and per-base-URL key scoping.
- Snippets (10): providers_base_abc, providers_init_dispatch, cli_auth_resolve_provider, core_auxiliary_auth_resolution, core_auxiliary_normalization, core_runtime_helpers_switch_client, core_chat_helpers_activate_fallback, core_credential_pool_selection, core_anthropic_adapter_client, core_codex_responses_adapter_init — relevance: the `ProviderProfile` ABC/registry, auth resolution, auxiliary routing, fallback client-switch, credential-pool selection, native-Anthropic client, and Codex Responses init code this page documents.
- Docs (10): hermes_agent_loop, hermes_acp_internals, hermes_cron_internals, hermes_context_compression_caching, hermes_architecture, hermes_plugin_llm_access (in-series: the loop/ACP/cron/compression/plugin-LLM lanes all call this resolver); cc_model_selection, cc_authentication, cc_fallback_models, cc_restrict_model_selection — relevance: the analogous model-selection, authentication, fallback-models, and model-restriction docs (the external provider-resolution + fallback surface).

**Note 8 `hermes_tools_runtime`** (model)
- Terms (8): term_function_calling, term_structured_output, term_subagent, term_human_in_the_loop, term_sandbox_backend, term_docker, term_mcp, term_prompt_injection — relevance: the registry serves function-calling schemas, gates dangerous commands via human-in-the-loop approval, dispatches across sandbox/docker terminal backends + MCP tools, and the DANGEROUS_PATTERNS flow guards destructive/injection actions.
- Code-Repos (5): repo_hermes_agent_tools (`tools/registry.py` + `approval.py` + `terminal_tool.py` + `environments/` 6 backends — this page IS this repo), repo_hermes_agent_mcp_toolsets (`toolsets.py` + `mcp_tool.py` — toolset resolution + MCP/plugin discovery), repo_hermes_agent (`model_tools.py` `handle_function_call` dispatch + AST `discover_builtin_tools`), repo_hermes_agent_agent_core (the 4 agent-level tools intercepted before registry dispatch), repo_hermes_agent_plugins (plugin-registered tools + pre/post-tool hooks) — relevance: these repos implement self-registration, discovery, `check_fn` gating, dispatch, and the approval flow.
- Snippets (10): tools_registry, tools_schema_sanitizer, toolsets_definitions, toolsets_materialize, core_tool_dispatch_helpers, tools_approval_policy, tools_approval_ui, tools_environments_base, tools_lazy_deps, core_tool_result_classification — relevance: the registry, schema sanitizer, toolset definitions/materialization, dispatch helpers, approval policy/UI, environment-base, lazy-dependency loading, and tool-result classification code this page documents.
- Docs (10): hermes_agent_loop, hermes_architecture, hermes_acp_internals, hermes_browser_supervisor, hermes_plugin_llm_access (in-series: the loop dispatches tools, ACP renders them, browser/plugin-LLM are tool surfaces); cc_built_in_tools, cc_tools_catalog, cc_sdk_custom_tool_definition, cc_sdk_tool_access_control, cc_sandbox_modes — relevance: the analogous built-in-tools, tools-catalog, custom-tool-definition, tool-access-control, and sandbox-modes docs (the external tool-registry + dispatch + sandbox surface).

**Note 9 `hermes_cron_internals`** (model)
- Terms (8): term_cron, term_idempotency, term_failover, term_round_robin, term_skills, term_skill_manifest, term_agent_orchestration, term_session_persistence — relevance: cron stores jobs idempotently, runs fresh isolated sessions, injects attached skills, and recovers via the fallback chain + round-robin credential pool. (+fin: term_fallback_provider, term_credential_pool)
- Code-Repos (5): repo_hermes_agent_cron (`cron/jobs.py` + `cron/scheduler.py` + `scheduler_provider.py` — the job model, tick cycle, and pluggable trigger this page is about), repo_hermes_agent_tools (`tools/cronjob_tools.py` — the model-facing `cronjob` action tool), repo_hermes_agent_cli (`hermes_cli/cron.py` `hermes cron` subcommands), repo_hermes_agent_gateway_messaging (`gateway/run.py` cron-ticking + Chronos webhook fire path), repo_hermes_agent_skills (the skills cron jobs attach + inject at execution) — relevance: these repos implement scheduling, storage, the tick cycle, delivery, and the recursion guard.
- Snippets (10): cron_job_schema, cron_job_crud, cron_tick, cron_run_job_execute, cron_run_job_setup, cron_helpers, cron_job_state, cli_gateway_dispatch, cron_job_validate, tools_cronjob_register — relevance: the job schema/CRUD, tick cycle, run-job execute/setup, helpers, lifecycle-state transitions, schedule-format validation, gateway integration, and the `cronjob` tool registration code this page documents.
- Docs (10): hermes_gateway_internals, hermes_agent_loop, hermes_provider_runtime, hermes_session_storage, hermes_architecture (in-series: the gateway ticks cron, each job runs a fresh loop, recovers via provider runtime, isolates its session); cc_scheduled_task_execution_model, cc_loop_scheduled_tasks, cc_scheduling_options_comparison, cc_dispatch_background_agents, cc_desktop_scheduled_tasks — relevance: the analogous scheduled-task-execution, scheduled-tasks, scheduling-options, background-dispatch, and desktop-scheduled-task docs.

**Note 10 `hermes_acp_internals`** (model)
- Terms (8): term_acp_agent_client_protocol, term_json_rpc, term_session_persistence, term_subagent, term_human_in_the_loop, term_authentication, term_agent_harness, term_multi_agent_systems — relevance: ACP (Agent Client Protocol) wraps the sync agent harness as an async JSON-RPC server, reuses the runtime auth resolver, bridges human-in-the-loop approvals, and persists/forks sessions in the shared state.db. (+fin: term_provider_routing)
- Code-Repos (5): repo_hermes_agent_acp (`acp_adapter/entry.py` + `server.py` + `session.py` + `events.py` + `permissions.py` + `tools.py` — this page IS this repo), repo_hermes_agent_agent_core (the sync `AIAgent` ACP wraps in a worker thread), repo_hermes_agent_providers_adapters (the runtime resolver ACP reuses for auth via `acp_adapter/auth.py`), repo_hermes_agent (`hermes_state.py` SessionDB ACP persists sessions to), repo_hermes_agent_tools (the terminal approval callback ACP installs/restores + tool-kind rendering) — relevance: these repos implement the boot flow, components, session lifecycle, and approval bridge.
- Snippets (10): acp_entry, acp_server_init, acp_session, acp_events, acp_tools_permission, acp_tools_register, acp_server_session_methods, acp_server_prompt, acp_auth, acp_server_cancel_config — relevance: the ACP boot entry, server init, session manager, event bridge, permission bridge, tool registration, session methods, prompt execution, runtime-resolver auth reuse, and cancelation-config code this page documents.
- Docs (10): hermes_agent_loop, hermes_provider_runtime, hermes_session_storage, hermes_tools_runtime, hermes_architecture, hermes_gateway_internals (in-series: ACP wraps the loop, reuses provider runtime, persists to sessions, renders tools, parallels the gateway adapter pattern); cc_sdk_session_management_api, cc_sdk_python_session_functions, cc_async_hooks, cc_permission_system_and_rules — relevance: the analogous SDK session-management-API, python-session-functions, async-hooks (async-over-sync bridging), and permission-system docs.

**Note 11 `hermes_trajectory_format`** (model)
- Terms (8): term_rl, term_rlhf, term_rlaif, term_function_calling, term_structured_output, term_llm, term_autonomous_coding_agents, term_tokenization — relevance: trajectories are ShareGPT-format RL/RLHF training data capturing function-calling turns + reasoning markup; tool-stats normalization keeps the schema HuggingFace-loadable.
- Code-Repos (5): repo_hermes_agent_trajectory_research (`agent/trajectory.py` + `batch_runner.py` — the ShareGPT export, normalization, and batch metadata this page is about), repo_hermes_agent_agent_core (`run_agent.py` `_save_trajectory` + reasoning/`<think>` capture), repo_hermes_agent (`model_tools.TOOL_TO_TOOLSET_MAP` driving `tool_stats` normalization), repo_hermes_agent_tools (the tool calls/results the trajectory serializes as `<tool_call>`/`<tool_response>`), repo_hermes_agent_cli (`agent.save_trajectories` config + `--save-trajectories` flag) — relevance: these repos implement trajectory saving, normalization, and the batch runner.
- Snippets (10): trajectory_schema, trajectory_canonicalize, trajectory_config_dataclasses, trajectory_redact_export, trajectory_overlap_suppression, core_think_scrubber, core_runtime_helpers_reasoning, core_run_agent_cli, batch_runner, batch_runner_aggregate — relevance: the trajectory schema, canonicalization, config dataclasses, redacted export, overlap suppression, reasoning/think-tag scrubbing, the CLI save path, and the batch-runner spawn/aggregate (per-batch `tool_stats`) code this page documents.
- Docs (10): hermes_agent_loop, hermes_architecture, hermes_session_storage, hermes_provider_runtime, hermes_tools_runtime, hermes_context_compression_caching (in-series: the loop produces turns, sessions are the source, tools/reasoning are serialized, compression-aware summaries appear in trajectories); cc_agent_sdk_message_types, cc_sdk_stream_text_and_tool_calls, cc_built_in_tools, cc_agent_sdk_agent_loop — relevance: the analogous SDK message-types, stream-text-and-tool-calls, built-in-tools, and agent-loop docs (the closest external turn/message serialization model).

**Note 12 `hermes_browser_supervisor`** (model)
- Terms (8): term_cdp, term_iframe_sandbox, term_websocket, term_human_in_the_loop, term_function_calling, term_structured_output, term_idempotency, term_computer_vision — relevance: the supervisor holds a persistent CDP WebSocket, surfaces cross-origin iframes (OOPIF) + native dialogs, exposes the `browser_dialog`/`browser_snapshot` function-calling surface with structured output, and idempotent get-or-start lifecycle. (+fin: term_browser_automation)
- Code-Repos (5): repo_hermes_agent_tools (`tools/browser_supervisor.py` + `browser_dialog_tool.py` + `browser_tool.py` — the `CDPSupervisor`, `SupervisorRegistry`, and browser tools this page is about), repo_hermes_agent_mcp_toolsets (`toolsets.py` registering `browser_dialog` in `browser`/`hermes-acp`/`hermes-api-server` toolsets, gated on CDP reachability), repo_hermes_agent_cli (`hermes_cli/config.py` `browser.dialog_policy`/`dialog_timeout_s` defaults + `/browser connect`), repo_hermes_agent_agent_core (the agent loop reading `browser_snapshot` + calling `browser_dialog`), repo_hermes_agent_acp (the `hermes-acp` toolset surfacing the gated browser tool) — relevance: these repos implement the supervisor, the tool surface, the backend matrix, and availability gating.
- Snippets (10): tools_browser_supervisor_lifecycle, tools_browser_supervisor_recovery, tools_browser_cdp, tools_browser_dom, tools_browser_navigate, tools_browser_intercept, tools_browser_session, tools_browser_camofox, tools_browser_screenshot, tools_computer_use_tool — relevance: the supervisor lifecycle/recovery, CDP routing (OOPIF `frame_id`), DOM snapshot, navigate start-hook, fetch-interception bridge (Browserbase), session teardown, Camofox backend, screenshot, and computer-use tool code this page documents.
- Docs (10): hermes_tools_runtime, hermes_architecture, hermes_agent_loop, hermes_acp_internals, hermes_plugin_llm_access, hermes_gateway_internals (in-series: browser is a tool surface in the registry/loop, gated per ACP/gateway/api-server toolset); cc_chrome_browser_automation, cc_computer_use, cc_computer_use_safety, cc_built_in_tools — relevance: the analogous chrome-browser-automation, computer-use, computer-use-safety, and built-in-tools docs (the external browser/computer-control surface).

**Note 13 `hermes_plugin_llm_access`** (model)
- Terms (8): term_provider_plugin, term_structured_output, term_json_rpc, term_llm, term_oauth_token, term_authentication, term_multimodal, term_prompt_injection — relevance: `ctx.llm` resolves the user's provider/credentials, supports structured (JSON-schema) output + multimodal image input, and the fail-closed trust gate guards provider/model/profile overrides (a prompt-injection / privilege boundary). (+fin: term_fallback_provider, term_provider_routing)
- Code-Repos (5): repo_hermes_agent_plugins (`hermes_cli/plugins.py` PluginManager + the `ctx.register_*` plugin context surface `ctx.llm` joins — this page's home repo), repo_hermes_agent_agent_core (`agent/plugin_llm.py` `PluginLlm` + `agent/auxiliary_client.py` `call_llm()` the lane runs on), repo_hermes_agent_providers_adapters (the host-owned provider resolution + vision routing + fallback `ctx.llm` delegates to), repo_hermes_agent_cli (`plugins.entries` trust-gate config + credential resolution), repo_hermes_agent_gateway_messaging (async `acomplete()` callers — gateway adapters/hooks) — relevance: these repos implement the four-shape surface, host-owned auth, and the fail-closed trust gate.
- Snippets (10): core_auxiliary_auth_resolution, core_auxiliary_normalization, core_auxiliary_headers, core_auxiliary_proxy_url, core_runtime_helpers_switch_client, core_credential_sources, providers_base_abc, core_chat_helpers_build_kwargs, core_auxiliary_anthropic_adapter, core_auxiliary_pool_content — relevance: the auxiliary-client auth resolution, normalization, headers, proxy URL, client switch, credential sources, provider ABC, request-kwargs build, native-Anthropic aux adapter, and credential-pool content code the `ctx.llm` lane runs on.
- Docs (10): hermes_provider_runtime, hermes_agent_loop, hermes_tools_runtime, hermes_architecture, hermes_context_compression_caching, hermes_gateway_internals (in-series: the lane reuses the provider runtime + aux client, parallels tool registration, is called from gateway hooks); cc_sdk_structured_outputs, cc_sdk_structured_output_schemas, cc_sdk_custom_tool_definition, cc_authentication — relevance: the analogous SDK structured-outputs, structured-output-schemas, custom-tool-definition (the `ctx.register_*` surface family), and authentication docs.

All 13 notes meet the FOUR-FLOOR standard: **≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc** (owned/other-SP
not-yet-existing terms excluded from the term floor, marked `[own]`/`(+fin …)`). Snippet IDs are under
(intra-series links land at finalization, verified by G5/G8). **Placeholder/non-existent slugs caught + replaced at
finalization before lock-in:** `term_reinforcement_learning` (→ `term_rl`, canonical acronym), `term_tool_use` (→
`term_function_calling`), `term_chrome_devtools_protocol` (→ `term_cdp`), `term_browser_automation` (MISSING →
forward-ref +fin only, owned by SP08), `term_summarization` (→ `term_progressive_summarization`), `term_acp` (MISSING
→ replaced by `term_acp_agent_client_protocol` in Note 10, the canonical active slug). Every cited term, code-repo, and

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 13 source pages from `inbox/hermes_agent_docs/developer-guide/`; measured counts match the
Source Pages table (no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 architecture | model | 1450 | ≤6 (curate from 6 ascii/text diagrams; keep system-overview + dependency-chain) | ✓ |
| 2 agent-loop | model | 1300 | ≤6 (from 5; tables in prose) | ✓ |
| 3 prompt-assembly | model | 1600 | ≤6 (from 5; keep tier example + context-file priority code) | ✓ |
| 4 context-compression-caching | model | 1900 | ≤6 (curate from 14 → keep config YAML, 4-phase boundaries, summary template, system_and_3, enabling) | ✓ |
| 5 gateway-internals | model | 1450 | ≤6 (from 6; keep arch diagram + session-key + running-agent guard) | ✓ |
| 6 session-storage | model | 1750 | ≤6 (curate from 17 → keep sessions DDL, messages DDL, FTS5 + one trigger, one lineage CTE) | ✓ |
| 7 provider-runtime | model | 1100 | 0 (page has no code; prose + tables) | ✓ |
| 8 tools-runtime | model | 1200 | ≤6 (from 4; keep register() signature + discover + dispatch flow + check_fn) | ✓ |
| 9 cron-internals | model | 1550 | ≤6 (from 6; keep job JSON + tick cycle) | ✓ |
| 10 acp-internals | model | 900 | ≤3 (from 3; keep boot flow + session lifecycle) | ✓ |
| 11 trajectory-format | model | 1000 | ≤6 (curate from 8 → keep CLI/batch entry, one complete ShareGPT example, tool_call/response markup, loader) | ✓ |
| 12 browser-supervisor | model | 1100 | ≤2 (from 2; keep snapshot extension JSON + browser_dialog signature) | ✓ |
| 13 plugin-llm-access | model | 1900 | ≤6 (curate from 10 → keep smallest call, structured example, complete() signature, result dataclass, trust-gate YAML, enforce table) | ✓ |

No further splits needed — all 13 notes are single-BB (model) clusters ≤2500w. Code-heavy notes (4/6/11/13)
are kept as ONE note each by curating the source code blocks to ≤6 load-bearing examples (kept verbatim) and
summarizing the rest in prose. Borderline notes by word count (4/6/13 at ~1750-1900w) were checked for
further split: each is one topically-cohesive subsystem with no BB mixing → KEEP (per review CP6
default-to-keep justification). If any note exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it IS,
NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; FOUR-FLOOR ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP18)

**SP18 owns 1 new term capture: `term_context_compression`** (Hermes' dual-threshold context compaction).
Captured via `/tessellum-capture-term-note` (NOT inline) BEFORE writing Note 4, which links it. All other
Hermes-specific concepts SP18 touches are owned by another sub-plan (link at finalization) or are an
existing verified term. Augment re-read surfaced **0 additional new** undigested terms SP18 should own.

| Term Slug | Best-Fit Glossary | Capture Phase | Stub or Full | Source Page | Notes |
|---|---|---|---|---|---|
| `term_context_compression` | acronym_glossary_llm.md | Phase 1 (pre-digest, before Note 4) | full term note | context-compression-and-caching.md | OWNED. Hermes-specific **dual-threshold** mechanism (gateway 85% hygiene + agent 50% ContextCompressor + 4-phase algorithm + Codex gpt-5.5 autoraise). NOT a dup of generic `term_compaction` (97L) or `term_context_engine` (81L) — see Collision Audit. Specificity OK (scope-qualified slug). |
| `term_messaging_gateway` | acronym_glossary_systems.md | LINK only (+fin) | — | gateway-internals.md | Owned by SP11 (platform↔agent bridge). SP18 documents the internals; concept home is SP11. |
| `term_credential_pool`, `term_fallback_provider`, `term_provider_routing` | acronym_glossary_systems/llm | LINK only (+fin) | — | provider-runtime.md, cron-internals.md | Owned by SP09. SP18 documents the runtime behavior; concept homes are SP09 protocols/providers. |

### Renamed (general → specific)

| Original (would-be) slug | Renamed to | Reason |
|---|---|---|
| `term_compression` / `term_compaction` (for the Hermes mechanism) | `term_context_compression` | A bare `term_compression`/`term_compaction` would (a) collide with the existing generic `term_compaction.md` (97L active, OpenClaw/industry-wide concept) and (b) be too general for the Hermes-specific dual-threshold two-layer mechanism. Scope-qualified to `term_context_compression` (context-window compaction) to distinguish from generic compaction and from data/file compression. |

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, lines, status) | Action |
|---|---|---|
| `term_session_storage` / session-store concept | `term_session_persistence.md` (131L, active) | Not captured — link the existing term from the `hermes_session_storage` doc note (different BB: doc note is the concrete Hermes SQLite/FTS5 model). |
| `term_context_engine` (would re-capture) | `term_context_engine.md` (81L, active) | Not captured — link the existing term from the `hermes_context_compression_caching` doc note. |
| `term_provider_runtime` / provider-resolution concept | `term_provider_plugin.md` (active) + `term_failover.md` (active) cover the component concepts | Not captured — link existing terms from the `hermes_provider_runtime` doc note. |

## Term-Note Authoring Requirements (Per Undigested Term — Inherited from `/tessellum-capture-term-note` canonical)

`term_context_compression` MUST be authored via **`/tessellum-capture-term-note "context compression"`**
(interactive or via ENRICHER_INPUTS), NOT inline-authored within a digest note. The capture skill enforces
the requirements below; this plan invokes them, it does not bypass them.

- **YAML frontmatter** (required): `tags`, `keywords`, `topics`, `language: markdown`, `date of note`,
  `status: active`, `building_block: concept`, `access_control_group: ["general"]`, `related_wiki`
  (Hermes docs URL or null). No forbidden fields.
- **H1**: `# Context Compression` (no canonical acronym → full name; drop trivial trailing words).
- **Required H2 sections in order**: `## Definition` (1-2 paragraphs: dual-threshold two-layer mechanism,
  what problem it solves) → `## Context` (Hermes Agent runtime; gateway vs agent loop) → `## Key
  Characteristics` (gateway 85% hygiene safety net vs agent 50% configurable primary; 4-phase algorithm;
  Codex gpt-5.5 272K autoraise; iterative re-compression; structured-summary template) → `## Performance /
  Metrics` (OPTIONAL — omit unless found) → `## Related Terms` (**8-15 links**, in-domain + cross-domain;
  e.g. Foundation: `term_compaction`/`term_context_engine`/`term_context_window`; Component:
  `term_progressive_summarization`/`term_tokenization`; Contrast: `term_prompt_caching`; Application:
  `term_session_persistence`/`term_agent_harness`) → `## References` (external URLs only — Hermes docs +
  Anthropic context-engineering + ≥1 more; NO `term_*.md` links here).
  external (Hermes docs page, Anthropic "Effective context engineering" / `context_management` docs,
  LangChain ConversationSummaryMemory docs) + vault cross-reference. Do NOT single-source from the Hermes
  doc page alone (doc-trapped scope). Research dry-fall → pause for user URL or `status: stub` +
  `research_pending: true`.
- **MathJax** for any token/threshold formula (e.g. `$\text{threshold\_tokens} = \text{threshold} \times
  \text{context\_length}$`), never plain-text math.
- **Fleeting-content guard**: no person aliases/ETAs/bare numbers without `(as of YYYY)`.
- **Glossary entry** (`acronym_glossary_llm.md`): 4-5 sentence Description max, no metrics, bold the single
  most distinguishing fact (the **dual-threshold two-layer** design), exact `**Full Name** / **Description**
  / **Documentation** / **Wiki** / **Related**` template.
- **Depth-scaled Related Terms minimum**: target Moderate tier (80-150 lines) → **10** links; if it lands
  Simple (40-80 lines) → 8. >200 lines → Step-7 decomposition.
- **Backlink expansion** (Step 6e): add `term_context_compression` to the `## Related Terms` of the
  existing `term_compaction`, `term_context_engine`, `term_context_window`, `term_progressive_summarization`
  (5-10 inlink target, in-domain + cross-domain).
- **ENRICHER_INPUTS non-interactive pattern** acceptable for batch capture (key_terms, acronym=null,
  domain="Hermes Agent context window compression dual threshold", summary_snippets from the source page,
  references=[the docs URL]).

## Execution Phases (per-phase 8-GATE)

- **Phase 0 (term capture):** `/tessellum-capture-term-note "context compression"` → reindex → verify the new
  `term_context_compression.md` exists + ≥8-10 Related Terms + glossary entry, BEFORE Note 4 links it.
- **Phase 1 (core agent internals, P-wave pilot):** Notes 1, 2, 3, 4. Pilot Note 1 (`hermes_architecture`)
  first → reindex → verify format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (runtime subsystems):** Notes 5, 6, 7, 8. GATE G1–G8.
- **Phase 3 (peripheral subsystems + plugin lane):** Notes 9, 10, 11, 12, 13. GATE G1–G8.
- **Phase 3b (inlinks — EXECUTED, G8):** add the inlink-table rows (existing → new) — gated, not a recommendation.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/developer-guide/<page>`
(code verbatim for kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost
(Script 4, DB-verify every ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** ·
G7 single-BB (model) · **G8 in-degree ≥1 from outside the folder**.

## Validation Scripts

```bash
DB_PATH=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
VAULT=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import VAULT_PATH_STR;print(VAULT_PATH_STR)")
TARGET="$VAULT/resources/documentation/hermes_agent"; PREFIX="hermes_"
# Script 1: format + density
for f in "$TARGET"/${PREFIX}*.md; do python3 scripts/check_note_format.py "$f";
  w=$(sed -n '/^---$/,/^---$/!p' "$f"|wc -w); c=$(( $(grep -c '^```' "$f")/2 )); l=$(wc -l <"$f")
  [ "$w" -gt 2500 ]||[ "$c" -gt 6 ]||[ "$l" -gt 400 ] && echo "DENSITY: $(basename $f)"; done
# Script 4: G5 ghost detection
for f in "$TARGET"/${PREFIX}*.md; do grep -oE '\]\(([^)]+\.md)[^)]*\)' "$f"|sed -E 's/.*\(([^)]+\.md).*/\1/'|while read l; do
  c=$(echo "$l"|sed -E 's/#.*$//'); r=$(cd "$(dirname "$f")"&&realpath -q -m "$c" 2>/dev/null); [ -z "$r" ]&&continue
# G8: in-degree ≥1 from outside the folder
for n in hermes_architecture hermes_agent_loop hermes_prompt_assembly hermes_context_compression_caching hermes_gateway_internals hermes_session_storage hermes_provider_runtime hermes_tools_runtime hermes_cron_internals hermes_acp_internals hermes_trajectory_format hermes_browser_supervisor hermes_plugin_llm_access; do
```

## Entry Point Decision (inherited)

Contributes 13 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Developer: Internals" section. Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP18 does NOT create a separate entry point —
the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent.md` | → `hermes_architecture` | implementation ↔ top-level internals map |
| `repo_hermes_agent_agent_core.md` | → `hermes_agent_loop`, `hermes_prompt_assembly`, `hermes_context_compression_caching` | agent core repo ↔ loop/prompt/compression docs |
| `repo_hermes_agent_gateway_messaging.md` | → `hermes_gateway_internals`, `hermes_session_storage` | gateway repo ↔ gateway/session-store docs |
| `repo_hermes_agent_providers_adapters.md` | → `hermes_provider_runtime` | provider adapters repo ↔ provider-runtime doc |
| `repo_hermes_agent_tools.md` | → `hermes_tools_runtime`, `hermes_browser_supervisor` | tools repo ↔ tools-runtime/browser-supervisor docs |
| `repo_hermes_agent_cron.md` | → `hermes_cron_internals` | cron repo ↔ cron-internals doc |
| `repo_hermes_agent_acp.md` | → `hermes_acp_internals` | ACP repo ↔ ACP-internals doc |
| `repo_hermes_agent_trajectory_research.md` | → `hermes_trajectory_format` | trajectory/RL repo ↔ trajectory-format doc |
| `repo_hermes_agent_plugins.md` | → `hermes_plugin_llm_access` | plugins repo ↔ plugin LLM-access doc |
| `term_context_engine.md` | → `hermes_context_compression_caching` | concept term → compressor-behavior doc |
| `term_compaction.md` | → `hermes_context_compression_caching` | generic compaction term → Hermes dual-threshold doc |
| `term_context_compression.md` (new, Phase 0) | → `hermes_context_compression_caching` | owned term → its behavior doc |
| `term_session_persistence.md` | → `hermes_session_storage` | concept term → concrete SQLite/FTS5 model doc |
| `term_acp_agent_client_protocol.md` | → `hermes_acp_internals` | concept term → ACP-internals doc |
| `entry_code_snippets_hermes_agent.md` | → `hermes_architecture`, `hermes_agent_loop` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 13 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Run Phase 0 (`term_context_compression` capture) FIRST so Note 4 has a real link target. Pilot Note 1
(`hermes_architecture`) → reindex → verify format/ghost/in-degree BEFORE authoring the rest. Commit per phase
(per-wave commits for multi-agent runs). Re-read the source page before writing each note — do NOT work from
memory. Code blocks verbatim for kept blocks; curate code-heavy notes (4/6/11/13) to ≤6 load-bearing
examples, summarize the rest in prose. If a note exceeds 350 lines during writing, STOP and split. If
multi-agent: agents return note content, master writes serially where there is write-contention; ≤30
agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP18 lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 13 rows to
  the master-created entry point; backfill the `repo_hermes_agent_*` / `term_*` inlinks (G8); run
  `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After P1+P3 waves: cross-link the SP18 internals notes ↔ SP02 config notes (compression/context-engine
  config↔behavior), SP09 (provider routing/fallback feature↔runtime), SP06 (cron/delegation feature↔internals),
  SP08 (browser feature↔supervisor), SP19 (plugin-authoring how-to↔plugin LLM-access behavior).
- Consider one `thought_` note comparing Hermes' docs-stated internals vs the code-digestion findings in
  `snippet_hermes_agent_core_*` (the master's Follow-up #3).

## Augmentation Report

- Sections added/updated: Collision&Dedup Audit (3 LINK-not-dup confirmed by reading `term_compaction`/
  `term_context_engine`/`term_session_persistence`), finalized Per-Note Mapping (FOUR-FLOOR ≥8 term + ≥5
  term, Doc-Note Authoring Spec (derived from `cc_*.md`), Density Re-Assessment (re-read confirmed), G5 ghost +
  G8 scripts, Inlinks.
- Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  raised 8→≥10 and promoted from "bonus" to a counted floor, a ≥5 `repo_hermes_agent_*` code-repo floor added,
  and the doc floor raised 5→≥10 (in-series `hermes_*` + analogous `claude_code/cc_*`); no existing relevant
  cross-ref dropped. Note 10 term `term_acp` (non-existent) corrected to `term_acp_agent_client_protocol`.
- Density re-read: counts match measured; **no splits** — all 13 pages are single-BB (model) ≤2500w; the two
  master-ledger `[SPLIT]` flags were code-block counts, resolved by curating code to ≤6 per note (KEEP one note each).
- Collision audit: **0 removals of doc notes**; `term_context_compression` confirmed NOT a dup of the generic
  `term_compaction` (97L) — CREATE with scope-qualified slug; 3 existing terms confirmed LINK-not-dup.
- Term placeholder catch: **5 non-existent/non-canonical slugs caught at finalization** (`term_reinforcement_learning`
  →`term_rl`, `term_tool_use`→`term_function_calling`, `term_chrome_devtools_protocol`→`term_cdp`,
  `term_summarization`→`term_progressive_summarization`, `term_browser_automation` MISSING→+fin only) and
- Undigested terms surfaced at augment: **1 owned** (`term_context_compression`); 4 forward-refs to SP09/SP11.
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions (none; justified) ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution (model 13) ✓
Note Format Def (derived from `cc_*.md`) ✓ Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓
Follow-up ✓ Undigested Terms Plan ✓ Capture Phase per term (Phase 0 for `term_context_compression`) ✓ best-fit
glossary (acronym_glossary_llm.md) ✓ Term-Note Auth Reqs (full, for the 1 owned term) ✓ invokes
capture-term-note ✓ Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (renamed
`term_compression`→`term_context_compression`) ✓ Slug Collision (`term_compaction` LINK-not-dup + 5
placeholders caught) ✓ dedup generalized to ALL notes incl doc, searched term_dictionary AND documentation/ ✓
G8 in every phase + inlinks EXECUTED (Phase 3b) ✓ Doc-Note Authoring Spec derived ✓).

## Review Sign-Off

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass).**
**Independent FOUR-FLOOR re-review 2026-06-19 — READY (9/9). Re-confirmed below.**

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | Phase 0 + 3 phases + Phase 3b, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (13 rows under a Developer: Internals section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 13 notes ≤30; master holds the corpus-level split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); not invented. |
| CP6 | Borderline density → split | PASS | All 13 single-BB (model) ≤2500w; code-heavy notes (4/6/11/13) curated ≤6; the two master-ledger `[SPLIT]` flags were code-counts, KEEP-as-one-note justified. |
| CP7 | Source counts measured | PASS | Re-read 2026-06-15, re-measured 2026-06-19 (mirror c253b07, body-only convention): plugin-llm-access 2254, context-compression 2049, architecture 1644, cron 1820, prompt-assembly 1777, session-storage 1555, gateway 1546, agent-loop 1382, tools-runtime 1266, browser-supervisor 1163, provider-runtime 1156, trajectory 1012, acp 693 — measured == plan (ratio ~1.0; prompt-assembly + cron grew upstream, re-synced below). Independent spot re-measure 2026-06-19 from inbox mirror: acp-internals 672w/3code (plan 693/3), provider-runtime 1135w/0code (plan 1156/0) — code counts exact, words within ~3% tokenization noise; all 13 source pages present in inbox. |
| CP8 | Undigested Terms + Authoring Reqs | PASS | SP18 owns 1 term capture (`term_context_compression`, Phase 0, acronym_glossary_llm.md); full Term-Note Authoring Requirements present (multi-source mandate, depth-scaled Related Terms, glossary template, backlink expansion); forward-refs to SP09/SP11 marked +fin. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit table covers all 13 doc notes + the 1 term (term_dictionary AND documentation/); `term_compaction`/`term_context_engine`/`term_session_persistence` confirmed LINK-not-dup by reading the notes; Renamed (`term_compression`→`term_context_compression`) + Removed sub-tables present; 5 placeholder slugs caught + replaced. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 13 notes from repo_*/term_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION.** (Independent four-floor re-review 2026-06-19 confirms 9/9 READY — no factual fixes required; CP1/CP7 evidence refreshed with measured counts.)

## Re-Sync Note (2026-06-19)

Doc mirror re-downloaded from `NousResearch/hermes-agent` `website/docs/` at main HEAD `c253b07` (was pinned
`95715dc`). Two SP18-owned pages grew upstream; independently re-measured against the fresh mirror with the
ledger convention (BODY only, frontmatter stripped; code-block count = `^\s*```` lines ÷ 2). My measurement
matched the manifest exactly. Stable spot-checks: architecture.md (1622 body / 6 code), session-storage.md
(1555 / 17), plugin-llm-access.md (2219 / 10) — unchanged, no drift.

Changed pages (old → new):
- developer-guide/prompt-assembly.md — 1529w/4code → 1777w/5code
- developer-guide/cron-internals.md — 1344w/5code → 1820w/6code

Density re-evaluation: **no split**. Both pages are still single-BB (model) subsystem-behavior descriptions
and both remain under every cap — 1777w and 1820w are well below the ≤2500w cap; new raw code counts (5, 6)
are at or below the ≤6 code-block cap. The derived planned-note estimates were nudged sensibly (Note 3
~1450→~1600, Note 9 ~1300→~1550) to track the larger source while staying comfortably within caps; code
curation for Note 9 now keeps the source's 6 blocks as-is (no curation cut needed) and Note 3 keeps its tier
example + context-file priority block (5 source blocks). No planned-note filename, BB, or gate changed. (The
cross-ref floor was subsequently raised on 2026-06-19 to the FOUR-FLOOR standard — see the Per-Note Mapping
preamble and Augmentation Report.) Plan remains **READY**.

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; FOUR-FLOOR re-augment 2026-06-19) · Review: **DONE** (2026-06-15, 9/9 READY; independent FOUR-FLOOR re-review 2026-06-19, 9/9 READY) · Execute: pending · Re-synced 2026-06-19

**Source**: `inbox/hermes_agent_docs/developer-guide/{architecture,agent-loop,prompt-assembly,context-compression-and-caching,gateway-internals,session-storage,provider-runtime,tools-runtime,cron-internals,acp-internals,trajectory-format,browser-supervisor,plugin-llm-access}.md`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
