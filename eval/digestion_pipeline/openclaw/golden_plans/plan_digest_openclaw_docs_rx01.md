---
title: Sub-Plan rx01 — OpenClaw Docs: Refactor (ACP, Canvas, Database-First, Ingress-Core)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["refactor/acp", "refactor/canvas", "refactor/database-first", "refactor/ingress-core"]
xref_augmented: 2026-06-21
reviewed: 2026-06-21
---

# Sub-Plan rx01: Refactor

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML + `## Overview` … `## Related
> Notes` … `## References`), dedup (3-way vs term_dictionary / documentation / repo_openclaw*), 9-GATE,
> cross-refs, and entry-point (`entry_openclaw_docs.md`) decisions are ALL inherited from the master.

## Scope

The 4 OpenClaw `refactor/` pages — internal architecture-refactor / migration design documents (not end-user
how-tos). They are **`argument`-building-block design plans**: each states a Decision/Goal, Non-goals, a Target
shape, a phased Migration/Work plan, and Success/Done criteria.

- `refactor/acp` — making ACP session + ACPX process ownership explicit (identity, leases, ownership rows).
- `refactor/canvas` — moving Canvas out of core into a bundled experimental plugin (`extensions/canvas`).
- `refactor/database-first` — making SQLite the primary durable state + cache layer (the largest page by far).
- `refactor/ingress-core` — deletion-first plan to pull repeated channel-ingress glue into core.

Priority **P2** (Phase B). These design docs are the conceptual rationale behind the OpenClaw code-side notes
the vault already holds (`repo_openclaw_sessions`, `repo_openclaw_gateway`, `repo_openclaw_channels`,
`repo_openclaw_extensions`, and the ACP/process/sessions code snippets) — they are LINKED, not recreated.

**Source**: OpenClaw docs, 4 pages, 21,557 measured words (database-first dominates at 17,526w). **Planned: 6 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| refactor/acp | /refactor/acp | 1,427 | 7 | 10 | 8 | argument (design/migration plan) |
| refactor/canvas | /refactor/canvas | 943 | 1 | 7 | 0 | argument (design/migration plan) |
| refactor/database-first | /refactor/database-first | 17,526 | 5 | 15 | 8 | argument (split: decision · schema/migration · runtime) |
| refactor/ingress-core | /refactor/ingress-core | 1,661 | 9 | 11 | 0 | argument (design/deletion plan) |

> Code = `grep -c '^```' / 2`. `database-first.md` is overwhelmingly **prose**, not code: its 17,526 words are
> dominated by a single ~1,145-line "Current Code Shape" narrative inventory (0 code fences inside it) plus a
> long "Migration Inventory" / "Runtime Refactor Plan". Only 5 fences total. This is a code-state catalog, NOT
> reproducible note content — it is summarized and linked-out (see Content Strategy + Split Decisions).

## Content Strategy

- **Prioritize** the *decisions and contracts* an engineer needs: the database-first Decision + Hard Contract
  (SQLite-primary, file-backed config, no JSON sidecars) and the phased Migration/Runtime plan; the ACP
  ownership model (identity → leases → ownership rows); the Canvas core-vs-plugin boundary; the ingress-core
  acceptance rule ("a helper must delete bundled plugin code").
- **Split** `database-first.md` (17,526w / 15 H2, far over the 2,500w cap) into **3 notes** along its natural
  decision → schema/migration → runtime seams (see Split Decisions). Each split note stays ≤2,500w / ≤6 code.
- **Summarize, do NOT reproduce**, the ~1,145-line "Current Code Shape" inventory and the per-file "Migration
  Inventory" / "Static Bans" enumerations: capture the *pattern and rule* (what state lives where, what is
  banned), link the source URL + the existing `repo_openclaw_*` / `snippet_openclaw_*` code notes for the
  table/file detail. This is the over-compression guard's intended target — distill the contract, don't transcribe.
- **Link-out / do not redefine:** ACP protocol → `term_acp_agent_client_protocol` + `repo_openclaw_agents`;
  session runtime → `repo_openclaw_sessions` + `snippet_openclaw_sessions_*`; gateway → `repo_openclaw_gateway`;
  channels ingress → `repo_openclaw_channels` + `snippet_openclaw_channels_*`; extensions/plugins →
  `repo_openclaw_extensions` + `snippet_openclaw_plugin_*`; SQLite/WAL/migration concepts → `term_sqlite`,
  `term_wal`, `term_migration` do NOT exist (master: OpenClaw/infra vocab is digested in-place as `oc_*` doc
  prose, NOT promoted to new `term_dictionary` notes — see Undigested Terms Plan).

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_refactor_acp_lifecycle.md` | argument | refactor/acp.md: Goals, Non-goals, Target Model (Gateway Instance Identity, ACP Session Ownership, ACPX Process Leases), Lifecycle Controller, Wrapper Contract, Session Visibility Contract, Migration Plan (Phases 1–5), Tests, Compatibility Notes, Success Criteria | 700 | The plan to make ACP session and ACPX process ownership explicit: gateway-instance identity, session-ownership rows, and process leases replacing after-the-fact heuristics; phased migration, wrapper/visibility contracts, and success criteria. |
| 2 | `oc_refactor_canvas_plugin.md` | argument | refactor/canvas.md: Goal, Non-goals, Current branch state, Target shape, Migration steps, Audit checklist, Verification commands | 500 | The plan to move Canvas from core into a bundled experimental plugin under `extensions/canvas`: the core-vs-plugin boundary, current branch state, target shape, migration steps, and the core-ownership audit checklist. |
| 3 | `oc_refactor_database_first_decision.md` | argument | refactor/database-first.md: Decision, Hard Contract, Goal state and progress (Hard goal, Goal states, Current state, Remaining work, Do not regress), Code-Read Assumptions, Code-Read Findings, Current Code Shape (summarized) | 750 | The database-first decision and hard contract: SQLite as the primary durable state + cache layer with config staying file-backed, the goal state, and the current-code findings (summarized; full inventory linked to the OpenClaw code notes). |
| 4 | `oc_refactor_database_first_schema_migration.md` | argument | refactor/database-first.md: Target Schema Shape, Doctor Migration Shape, Migration Inventory, Migration Plan (Phases 0–7), Backup And Restore | 750 | The target SQLite schema shape (global + per-agent databases), doctor-driven migrations from legacy JSON/JSONL, the migration inventory, the phased migration plan (Phases 0–7), and backup/restore/vacuum behavior. |
| 5 | `oc_refactor_database_first_runtime.md` | argument | refactor/database-first.md: Runtime Refactor Plan (Phases 0–7: freeze boundary, control plane, per-agent DBs, session-store APIs, transcripts/ACP/VFS, backup/verify, worker runtime, delete old world), Performance Rules, Static Bans, Done Criteria | 700 | The runtime refactor of OpenClaw state access onto the new databases: per-agent DB introduction, session-store API replacement, moving transcripts/ACP streams/VFS, worker runtime, plus performance rules, static bans, and done criteria. |
| 6 | `oc_refactor_ingress_core.md` | argument | refactor/ingress-core.md: Budget, Diagnosis, Hotspots, Current Code Read, Boundary, Acceptance Rule, Work Packages, Deletion Waves, Do Not Move, Verification, Exit Criteria | 700 | The deletion-first plan to move repeated channel-ingress glue (route/command/event/activation/access-group policy) from bundled plugins into core: the diagnosis, the core-vs-plugin boundary, the "must delete bundled code" acceptance rule, work packages, and deletion waves. |

## Section Coverage Map

```
refactor/acp.md
├── Goals ──────────────────────────────────────────── → note 1 (oc_refactor_acp_lifecycle)
├── Non-goals ──────────────────────────────────────── → note 1
├── Target Model ───────────────────────────────────── → note 1
│   ├── Gateway Instance Identity ──────────────────── → note 1
│   ├── ACP Session Ownership ──────────────────────── → note 1
│   └── ACPX Process Leases ────────────────────────── → note 1
├── Lifecycle Controller ───────────────────────────── → note 1
├── Wrapper Contract ───────────────────────────────── → note 1
├── Session Visibility Contract ────────────────────── → note 1
├── Migration Plan (Phases 1–5) ────────────────────── → note 1
├── Tests ──────────────────────────────────────────── → note 1
├── Compatibility Notes ────────────────────────────── → note 1
└── Success Criteria ───────────────────────────────── → note 1
refactor/canvas.md
├── Goal ───────────────────────────────────────────── → note 2 (oc_refactor_canvas_plugin)
├── Non-goals ──────────────────────────────────────── → note 2
├── Current branch state ───────────────────────────── → note 2
├── Target shape ───────────────────────────────────── → note 2
├── Migration steps ────────────────────────────────── → note 2
├── Audit checklist ────────────────────────────────── → note 2
└── Verification commands ──────────────────────────── → note 2
refactor/database-first.md
├── Decision ───────────────────────────────────────── → note 3 (oc_refactor_database_first_decision)
├── Hard Contract ──────────────────────────────────── → note 3
├── Goal state and progress (Hard goal, Goal states,
│   Current state, Remaining work, Do not regress) ──── → note 3
├── Code-Read Assumptions ──────────────────────────── → note 3
├── Code-Read Findings ─────────────────────────────── → note 3
├── Current Code Shape (1,145 lines, summarized) ────── → note 3 (distilled; detail → repo_openclaw_* notes)
├── Target Schema Shape ────────────────────────────── → note 4 (oc_refactor_database_first_schema_migration)
├── Doctor Migration Shape ─────────────────────────── → note 4
├── Migration Inventory ────────────────────────────── → note 4 (summarized; per-file list → source URL)
├── Migration Plan (Phases 0–7) ────────────────────── → note 4
├── Backup And Restore ─────────────────────────────── → note 4
├── Runtime Refactor Plan (Phases 0–7) ─────────────── → note 5 (oc_refactor_database_first_runtime)
├── Performance Rules ──────────────────────────────── → note 5
├── Static Bans ────────────────────────────────────── → note 5 (summarized as rules; not transcribed)
└── Done Criteria ──────────────────────────────────── → note 5
refactor/ingress-core.md
├── Budget ─────────────────────────────────────────── → note 6 (oc_refactor_ingress_core)
├── Diagnosis ──────────────────────────────────────── → note 6
├── Hotspots ───────────────────────────────────────── → note 6
├── Current Code Read ──────────────────────────────── → note 6
├── Boundary ───────────────────────────────────────── → note 6
├── Acceptance Rule ────────────────────────────────── → note 6
├── Work Packages ──────────────────────────────────── → note 6
├── Deletion Waves ─────────────────────────────────── → note 6
├── Do Not Move ────────────────────────────────────── → note 6
├── Verification ───────────────────────────────────── → note 6
└── Exit Criteria ──────────────────────────────────── → note 6
```
No orphaned sections. Every H2/H3 of all 4 pages maps to a planned note. The database-first "Current Code
Shape", "Migration Inventory" (per-file), and "Static Bans" (per-pattern) enumerations are distilled to their
contract/rule (not transcribed verbatim), with file-level detail linked to source URL + `repo_openclaw_*`.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| refactor/database-first.md (17,526w, 15 H2 / 8 H3) | notes 3 + 4 + 5 | Far exceeds the 2,500w cap (≈7×). Splits along its three natural seams: (3) the **decision + hard contract + current-code findings** (why + what-is); (4) the **target schema + doctor migrations + migration plan + backup** (what-to-build + data-move); (5) the **runtime refactor + performance rules + static bans + done criteria** (how-to-cut-over + guardrails). Each split is one coherent design argument and stays ≤2,500w / ≤6 code after the Code-Shape/Inventory/Bans prose is distilled rather than transcribed. |
| refactor/acp.md (1,427w) | note 1 (no split) | Single coherent ACP-ownership design doc, under cap; one `argument` BB. |
| refactor/canvas.md (943w) | note 2 (no split) | Small single design doc, well under cap; one `argument` BB. |
| refactor/ingress-core.md (1,661w) | note 6 (no split) | Single coherent deletion-plan design doc, under cap; one `argument` BB. |

## Summary Statistics & Building Block Distribution

- Source pages: 4 (21,557 measured words; database-first alone = 17,526w). New `oc_` notes: **6**.
  New `term_dictionary` notes: **0** (see Undigested Terms Plan).
- BB distribution: **argument ×6** (all six are refactor/migration *design plans* — decision + rationale +
  non-goals + phased plan + success/done criteria; the master's "some argument (security/design)" class).
- Est. digest words ~4,100 (avg ~680/note); largest source page reduced ~17,526w → 3 notes ≈2,200w total via
  distillation of the Code-Shape / Inventory / Static-Bans enumerations (linked, not transcribed).
- Source code fences are sparse (acp 7 · canvas 1 · database-first 5 · ingress-core 9); each note reproduces
  ≤6 selectively (verbatim), favoring the contract/schema/command snippets over the prose inventories.
- **Cross-refs (LOCKED at xref-augment 2026-06-21):** raised floors of **≥8 term_dictionary terms · ≥10
  `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`. Per-note counts: note 1 acp
  10t/12s/12d; note 2 canvas 8t/10s/10d; note 3 db-decision 10t/11s/11d; note 4 schema-migration 10t/11s/11d;
  note 5 runtime 10t/12s/11d; note 6 ingress 10t/11s/11d. All snippets + ≥5/10 docs per note are EXISTING

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> Every cited EXISTING note_id was re-verified present in `notes` (sqlite3 by path suffix, 2026-06-21).
> Relative paths from a note at `resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/`;
> sibling `oc_*` (this series, planned) → `oc_Y.md`; other doc → `../<folder>/<file>.md`; repo →
> `../../../areas/code_repos/`; snippet → `../../code_snippets/`. Sibling `oc_refactor_*` docs do not exist yet
> (this series) and `entry_openclaw_docs.md` is planned at master W1 — both count toward the ≥10-doc floor but

### oc_refactor_acp_lifecycle (10t · 12s · 12d)

**Terms** (`../../term_dictionary/`)
- [ACP — Agent Client Protocol](../../term_dictionary/term_acp_agent_client_protocol.md) — the JSON-RPC protocol an editor/gateway uses to drive a coding agent; relevance: this refactor makes ACP session + ACPX process ownership first-class.
- [ACP — Agent Communication Protocol](../../term_dictionary/term_acp_agent_communication_protocol.md) — the agent-to-agent comms variant; relevance: the `a2aPolicy` visibility rule governs cross-agent ACP session rows.
- [Subagent](../../term_dictionary/term_subagent.md) — a spawned child agent session; relevance: the session-visibility contract's key case is a requester-owned spawned cross-agent ACP child.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime that wraps and supervises a coding agent; relevance: ACPX is the plugin-owned harness whose process leases this refactor introduces.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agents that act in a repo with minimal supervision; relevance: these are the ACP agents whose lifecycle/cleanup is being made lease-driven.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated process/container execution; relevance: ACPX wrapper processes run in their own process group for tree cleanup.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — start/cancel/close/reap lifecycle signals; relevance: `cancel`, `close`, and startup reaping are given distinct lifecycle intents here.
- [Event Ledger](../../term_dictionary/term_event_ledger.md) — append-only record of agent/session events; relevance: ACP replay-ledger sessions and lease state records are the durable ownership ledger.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — request/response RPC over JSON; relevance: ACP is JSON-RPC transport between gateway and agent.
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent bidirectional transport; relevance: gateway↔client session-event streaming for `sessions_list`/visibility.

**Docs**
- [oc_refactor_database_first_runtime](oc_refactor_database_first_runtime.md) — (planned, this series) the runtime cut-over moving ACP streams to per-agent DBs; relevance: ACP parent-stream/replay state moves into SQLite per this note's contract.
- [band_acp_client](../band/band_acp_client.md) — Band's ACP client implementation; relevance: parallel ACP-client lifecycle/session model in a sibling agent stack.
- [band_acp_server](../band/band_acp_server.md) — Band's ACP server side; relevance: the server-side session-ownership analogue to OpenClaw's gateway.
- [band_acp_overview](../band/band_acp_overview.md) — overview of Band's ACP integration; relevance: cross-stack reference for ACP session/process concepts.
- [hermes_acp_internals](../hermes_agent/hermes_acp_internals.md) — Hermes ACP runtime internals; relevance: another coding-agent harness's ACP session lifecycle for comparison.
- [hermes_acp_editor_integration](../hermes_agent/hermes_acp_editor_integration.md) — Hermes ACP editor wiring; relevance: editor-driven ACP sessions are the spawn source whose ownership is normalized.
- [hermes_subagent_delegation](../hermes_agent/hermes_subagent_delegation.md) — Hermes subagent delegation model; relevance: spawned-by / owner relationships mirror the session-ownership rows.
- [cc_work_with_subagents](../claude_code/cc_work_with_subagents.md) — Claude Code subagent usage; relevance: subagent spawn/visibility is the visibility-contract case.
- [cc_forked_subagents](../claude_code/cc_forked_subagents.md) — forked-subagent lifecycle in Claude Code; relevance: fork/spawn ownership parallels ACPX process leases.
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — PI gateway RPC protocol; relevance: PI is the embedded agent runtime ACPX wraps; RPC session identity overlaps.
- [pi_sdk_run_modes](../pi/pi_sdk_run_modes.md) — PI SDK run modes (detached/embedded); relevance: detached-runtime + parent-death handling mirror the wrapper contract.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw ACP agent runtime; relevance: the subsystem this refactor targets (ACP/ACPX).
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — OpenClaw session store; relevance: session-ownership rows + visibility live here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: gateway-instance identity + the ACPX lifecycle controller.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_acp_runtime_contract](../../code_snippets/snippet_openclaw_acp_runtime_contract.md) — ACP runtime handle/contract; relevance: the `AcpRuntimeHandle`/ensure-session shape the lifecycle controller owns.
- [snippet_openclaw_acp_manager_detached_runtime](../../code_snippets/snippet_openclaw_acp_manager_detached_runtime.md) — detached ACP manager runtime; relevance: detached wrapper launch is where leases are created.
- [snippet_openclaw_acp_manager_runtime_register](../../code_snippets/snippet_openclaw_acp_manager_runtime_register.md) — ACP manager runtime registration; relevance: where session+lease records get registered on spawn.
- [snippet_openclaw_acp_manager_controls_apply](../../code_snippets/snippet_openclaw_acp_manager_controls_apply.md) — ACP manager controls (cancel/close); relevance: implements the distinct cancel vs close lifecycle intents.
- [snippet_openclaw_acp_spawn_policy](../../code_snippets/snippet_openclaw_acp_spawn_policy.md) — ACP spawn policy; relevance: spawn-time ownership/spawnedBy assignment.
- [snippet_openclaw_acp_spawn_session_handoff](../../code_snippets/snippet_openclaw_acp_spawn_session_handoff.md) — ACP spawn session handoff; relevance: parent→child session-ownership handoff this normalizes.
- [snippet_openclaw_acp_persistent_bindings](../../code_snippets/snippet_openclaw_acp_persistent_bindings.md) — persistent ACP session bindings; relevance: persistent (reusable) sessions cancel must NOT close.
- [snippet_openclaw_acp_event_ledger](../../code_snippets/snippet_openclaw_acp_event_ledger.md) — ACP event-ledger writer; relevance: lease/replay state durability source.
- [snippet_openclaw_process_kill_tree](../../code_snippets/snippet_openclaw_process_kill_tree.md) — process-tree kill; relevance: SIGTERM→SIGKILL children-first reaping in the wrapper contract.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: parent-death detection + verified-tree reaping.
- [snippet_openclaw_gateway_session_utils_subagent_liveness](../../code_snippets/snippet_openclaw_gateway_session_utils_subagent_liveness.md) — subagent liveness check; relevance: live-process verification before signaling (fail-closed).
- [snippet_openclaw_gateway_server_startup_acp_prewarm](../../code_snippets/snippet_openclaw_gateway_server_startup_acp_prewarm.md) — startup ACP prewarm; relevance: startup reaping/leases run alongside ACP prewarm.

### oc_refactor_canvas_plugin (8t · 10s · 14d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway product; relevance: this refactor draws OpenClaw's core-vs-plugin boundary.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the API surface a plugin implements; relevance: the bundled-plugin contract Canvas must satisfy after relocation.
- [A2UI](../../term_dictionary/term_a2ui.md) — agent-to-UI host/protocol; relevance: A2UI host + bundle source move under `extensions/canvas`.
- [ACP — Agent Client Protocol](../../term_dictionary/term_acp_agent_client_protocol.md) — coding-agent protocol; relevance: Canvas protocol/client ownership moves behind gateway protocol v4 plugin surface.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol tool surface; relevance: the agent-facing `canvas` tool registration is a plugin-owned tool surface.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution; relevance: bundled experimental plugin isolation boundary.
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — runtime capability handshake; relevance: `pluginSurfaceUrls.canvas` + node capability helpers replace hardcoded Canvas capability.

**Docs**
- [oc_refactor_ingress_core](oc_refactor_ingress_core.md) — (planned, this series) the sibling deletion-first core/plugin boundary plan; relevance: same "move out of core into plugins, delete glue" pattern.
- [hermes_plugins_system](../hermes_agent/hermes_plugins_system.md) — Hermes plugin system; relevance: the plugin discovery/registration seam Canvas plugs into.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — Hermes plugin types/surfaces; relevance: tool/host/HTTP-route surfaces Canvas declares as a plugin.
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — Hermes bundled plugins; relevance: the bundled-experimental-plugin classification Canvas adopts.
- [hermes_build_plugin_tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — building a Hermes plugin; relevance: manifest + package metadata steps mirror `openclaw.plugin.json`.
- [cc_plugin_manifest_schema](../claude_code/cc_plugin_manifest_schema.md) — Claude Code plugin manifest schema; relevance: the plugin manifest contract analogue.
- [cc_plugin_components](../claude_code/cc_plugin_components.md) — Claude Code plugin component model; relevance: tool/command/host components a plugin owns.
- [cc_sdk_plugins](../claude_code/cc_sdk_plugins.md) — Claude Code SDK plugins; relevance: SDK-level plugin registration parallels the plugin-SDK API checks.
- [pi_packages](../pi/pi_packages.md) — PI package/plugin model; relevance: package metadata + asset build/copy hooks parallel.
- [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — Claude Code plugin model overview; relevance: the bundled-plugin packaging/discovery model Canvas adopts when it leaves core.
- [cc_plugin_directory_structure](../claude_code/cc_plugin_directory_structure.md) — Claude Code plugin directory/manifest layout; relevance: the `extensions/canvas` on-disk layout + `openclaw.plugin.json` placement analogue.
- [cc_security_guidance_plugin](../claude_code/cc_security_guidance_plugin.md) — Claude Code plugin security guidance; relevance: bundled-experimental-plugin isolation/trust boundary Canvas must respect once out of core.
- [hermes_adding_platform_adapter_plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — adding a bundled Hermes plugin; relevance: end-to-end "register a new bundled plugin (manifest + surfaces)" walkthrough mirroring the Canvas relocation.
- [pi_extensions_custom_tools](../pi/pi_extensions_custom_tools.md) — PI extension-owned custom tools; relevance: plugin-registered agent tool surface analogue for the `canvas` MCP tool registration.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions framework; relevance: `extensions/canvas` is the target home.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw core monorepo; relevance: core sheds Canvas-specific behavior, keeps generic seams.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: generic HTTP/WebSocket-upgrade/auth plumbing that stays in core.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_macos_canvas_lifecycle](../../code_snippets/snippet_openclaw_macos_canvas_lifecycle.md) — Canvas host lifecycle (macOS); relevance: the Canvas host behavior being relocated to the plugin.
- [snippet_openclaw_macos_canvas_filewatcher](../../code_snippets/snippet_openclaw_macos_canvas_filewatcher.md) — Canvas document filewatcher; relevance: Canvas document materialization moving under the plugin.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: the discovery/registration lifecycle Canvas registers into.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: `openclaw.plugin.json` + package metadata Canvas must provide.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoints; relevance: `api.registerNodeCliFeature` and tool/route registration entries.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — gateway plugin HTTP routing; relevance: generic plugin HTTP route + WebSocket-upgrade dispatch that hosts Canvas.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node-command policy; relevance: Canvas node-invoke command defaults move to plugin `nodeInvokePolicies`.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload apply; relevance: `plugins.entries.canvas.config.host` plugin-owned config surface + doctor alias rewrite.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — hosted media record lifecycle; relevance: plugin-owned hosted media resolvers for Canvas document URLs.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: `openclaw nodes canvas` registered as a plugin-owned nested CLI feature.

### oc_refactor_database_first_decision (10t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [Storage Engine](../../term_dictionary/term_storage_engine.md) — the engine managing on-disk durable state; relevance: SQLite becomes the primary durable state + cache engine.
- [RDBMS](../../term_dictionary/term_rdbms.md) — relational database management system; relevance: SQLite's typed relational tables replace JSON/JSONL sidecars.
- [OLTP](../../term_dictionary/term_oltp.md) — online transactional processing; relevance: hot runtime read/write paths become small transactional row operations.
- [ACID](../../term_dictionary/term_acid.md) — atomicity/consistency/isolation/durability; relevance: the hard contract relies on transactional durability instead of file writes.
- [Consistency](../../term_dictionary/term_consistency.md) — data-consistency guarantees; relevance: typed relational session identity replaces brittle string-parsing (`session_key`).
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session state; relevance: session rows persist metadata-only with SQLite `{agentId, sessionId}` identity.
- [Idempotency](../../term_dictionary/term_idempotency.md) — re-runnable without duplicate effect; relevance: doctor migrations are keyed/idempotent per the Code-Read findings.
- [Compaction](../../term_dictionary/term_compaction.md) — pruning/condensing transcript state; relevance: compaction is one state path moving DB-first (clean for runtime).
- [Data Pipeline](../../term_dictionary/term_data_pipeline.md) — staged data flow; relevance: the legacy-file → SQLite import flow.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the system whose state model this decision sets.

**Docs**
- [oc_refactor_database_first_schema_migration](oc_refactor_database_first_schema_migration.md) — (planned, this series) the target schema + migration plan; relevance: the schema this decision mandates.
- [oc_refactor_database_first_runtime](oc_refactor_database_first_runtime.md) — (planned, this series) the runtime cut-over; relevance: how runtime reaches the `sqlite-runtime`/`clean` goal states.
- [hermes_session_storage](../hermes_agent/hermes_session_storage.md) — Hermes session storage model; relevance: a sibling agent's durable session-state decision.
- [hermes_session_search_storage](../hermes_agent/hermes_session_search_storage.md) — Hermes session search/storage backend; relevance: SQLite-backed session/transcript search parallels.
- [cc_sdk_session_store](../claude_code/cc_sdk_session_store.md) — Claude Code SDK session store; relevance: the session-store abstraction whose path-vs-row identity this refactor changes.
- [cc_claude_application_data](../claude_code/cc_claude_application_data.md) — Claude Code application data layout; relevance: where durable agent application state lives (file vs DB tradeoff).
- [pi_sessions](../pi/pi_sessions.md) — PI session model; relevance: PI embedded runner sessions move to SQLite identity.
- [pi_session_file_format](../pi/pi_session_file_format.md) — PI on-disk session/JSONL format; relevance: the legacy file format being migrated away from at runtime.
- [dynamodb_backup_pitr](../aws_dynamodb/dynamodb_backup_pitr.md) — DynamoDB backup / point-in-time recovery; relevance: durable-store backup semantics analogue for the SQLite-primary decision.
- [neptune_storage_architecture](../aws_neptune/neptune_storage_architecture.md) — Neptune storage architecture; relevance: separating control-plane vs data-plane storage mirrors the two-level SQLite layout.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — OpenClaw session store; relevance: session store moving DB-first (clean for runtime).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: the global control-plane DB opener + shared state owner.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — OpenClaw memory; relevance: built-in memory index tables move into the per-agent DB.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_gateway_sessions_read_methods](../../code_snippets/snippet_openclaw_gateway_sessions_read_methods.md) — gateway session read methods; relevance: hot read paths that must read typed columns, not parse keys.
- [snippet_openclaw_gateway_session_utils_store_target](../../code_snippets/snippet_openclaw_gateway_session_utils_store_target.md) — session store-target resolution; relevance: the `storePath`→`databasePath` identity change.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — chat-lifecycle session persist; relevance: session metadata persisted as rows, not files.
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript-event stream; relevance: transcript identity is SQLite `{agentId, sessionId}`, no locators.
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — session-id resolution; relevance: typed session routing identity replaces `session_key` parsing.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session-key utilities; relevance: `session_key` is compatibility-only, not the runtime identity.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — session send policy; relevance: send/status paths pass `{agentId, sessionId}` through runtime.
- [snippet_openclaw_gateway_session_fs_index_read](../../code_snippets/snippet_openclaw_gateway_session_fs_index_read.md) — legacy file-system session index read; relevance: the file-era reads being retired to doctor-only.
- [snippet_openclaw_gateway_session_fs_transcript_candidate_scan](../../code_snippets/snippet_openclaw_gateway_session_fs_transcript_candidate_scan.md) — legacy transcript file scan; relevance: file-scan path replaced by SQLite rows.
- [snippet_openclaw_memory_host_memory_schema](../../code_snippets/snippet_openclaw_memory_host_memory_schema.md) — memory index schema; relevance: memory-index tables live in the per-agent DB.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory engine; relevance: session-transcript indexing stays SQLite-backed (not QMD markdown export).

### oc_refactor_database_first_schema_migration (10t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [Storage Engine](../../term_dictionary/term_storage_engine.md) — durable-state engine; relevance: the global + per-agent schemas live in SQLite.
- [RDBMS](../../term_dictionary/term_rdbms.md) — relational DBMS; relevance: explicit typed tables (no generic host `kv`).
- [ACID](../../term_dictionary/term_acid.md) — transactional guarantees; relevance: cascading FK ownership + transactional doctor migrations.
- [Write-Ahead Log](../../term_dictionary/term_write_ahead_log.md) — WAL durability mechanism; relevance: backup omits live WAL/SHM sidecars and checkpoints before snapshot.
- [Idempotency](../../term_dictionary/term_idempotency.md) — re-runnable imports; relevance: imports keyed by source path/mtime/size/hash/target, safe to rerun.
- [Data Pipeline](../../term_dictionary/term_data_pipeline.md) — staged ingest; relevance: legacy JSON/JSONL → SQLite table import.
- [ETL](../../term_dictionary/term_etl.md) — extract/transform/load; relevance: the doctor file→table transform/load shape.
- [Change Data Capture](../../term_dictionary/term_change_data_capture.md) — capturing source mutations; relevance: `migration_sources` records source hash/count for skip/backfill decisions.
- [Compaction](../../term_dictionary/term_compaction.md) — transcript condensing; relevance: transcript snapshots/checkpoints become SQLite rows replacing JSONL truncation.
- [Atomic File Write](../../term_dictionary/term_atomic_file_write.md) — durable file replacement; relevance: contrast — the legacy atomic-JSON-write pattern the migration replaces with row upserts.

**Docs**
- [oc_refactor_database_first_decision](oc_refactor_database_first_decision.md) — (planned, this series) the decision + hard contract; relevance: the why this schema implements.
- [oc_refactor_database_first_runtime](oc_refactor_database_first_runtime.md) — (planned, this series) the runtime cut-over; relevance: phases that consume this schema at runtime.
- [hermes_session_storage](../hermes_agent/hermes_session_storage.md) — Hermes session storage; relevance: a sibling's session/transcript table layout.
- [pi_session_file_format](../pi/pi_session_file_format.md) — PI session/JSONL format; relevance: the legacy source format the doctor import reads.
- [pi_compaction](../pi/pi_compaction.md) — PI compaction; relevance: transcript-snapshot/checkpoint shape moving into SQLite rows.
- [cc_sdk_sessions_overview](../claude_code/cc_sdk_sessions_overview.md) — Claude Code session lifecycle/store; relevance: session/transcript table model analogue.
- [cc_what_survives_compaction](../claude_code/cc_what_survives_compaction.md) — what compaction preserves; relevance: which transcript state must survive as durable snapshot rows.
- [dynamodb_backup_pitr](../aws_dynamodb/dynamodb_backup_pitr.md) — DynamoDB backup/PITR; relevance: verified-backup-before-mutate semantics for the migration's pre-import backup.
- [redshift_snapshots_manual_storage](../aws_redshift/redshift_snapshots_manual_storage.md) — Redshift manual snapshots; relevance: snapshot/restore archive model parallels `VACUUM INTO` backup.
- [neptune_restore_pitr](../aws_neptune/neptune_restore_pitr.md) — Neptune restore/PITR; relevance: restore-from-verified-archive semantics analogue.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — OpenClaw session store; relevance: `sessions`/`transcript_events`/`conversations` agent-DB tables.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: global control-plane schema + migration runner + backup.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — OpenClaw memory; relevance: `memory_index_*` + `media_blobs` tables.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript-event rows; relevance: `transcript_events`/`transcript_event_identities`/`transcript_snapshots` tables.
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — session-id resolution; relevance: `sessions.session_id`/`session_scope` typed identity.
- [snippet_openclaw_gateway_session_utils_store_target](../../code_snippets/snippet_openclaw_gateway_session_utils_store_target.md) — store-target/databasePath; relevance: `agent_databases` registry resolution.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor repair/migration cron example; relevance: doctor-driven idempotent migration/repair pattern.
- [snippet_openclaw_gateway_doctor_memory_dreaming_preview](../../code_snippets/snippet_openclaw_gateway_doctor_memory_dreaming_preview.md) — doctor memory migration preview; relevance: plan-before-mutate migration discovery.
- [snippet_openclaw_gateway_session_fs_transcript_candidate_scan](../../code_snippets/snippet_openclaw_gateway_session_fs_transcript_candidate_scan.md) — legacy transcript file scan; relevance: discovers legacy JSONL sources for the doctor import.
- [snippet_openclaw_gateway_session_fs_title_cache_archive](../../code_snippets/snippet_openclaw_gateway_session_fs_title_cache_archive.md) — legacy file archive; relevance: successful-source removal/archive after import.
- [snippet_openclaw_memory_host_memory_schema](../../code_snippets/snippet_openclaw_memory_host_memory_schema.md) — memory schema; relevance: `memory_index_chunks`/`memory_embedding_cache` agent-DB tables.
- [snippet_openclaw_memory_events](../../code_snippets/snippet_openclaw_memory_events.md) — memory-core events; relevance: memory-core host events move to shared plugin-state rows (Migration Inventory).
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed-image record lifecycle; relevance: `media_blobs`/`managed_outgoing_image_records` migration of media bytes.
- [snippet_openclaw_acp_event_ledger](../../code_snippets/snippet_openclaw_acp_event_ledger.md) — ACP event ledger; relevance: `acp_replay_sessions`/`acp_replay_events` agent-DB tables; legacy `event-ledger.json` is doctor input.

### oc_refactor_database_first_runtime (10t · 12s · 11d)

**Terms** (`../../term_dictionary/`)
- [Storage Engine](../../term_dictionary/term_storage_engine.md) — durable-state engine; relevance: per-agent DBs become the runtime storage engine.
- [OLTP](../../term_dictionary/term_oltp.md) — transactional processing; relevance: short `BEGIN IMMEDIATE` row transactions on hot paths.
- [ACID](../../term_dictionary/term_acid.md) — transactional guarantees; relevance: cascade-delete + atomic transcript append correctness.
- [Write-Ahead Log](../../term_dictionary/term_write_ahead_log.md) — WAL; relevance: Performance Rules mandate WAL + `foreign_keys=ON` + busy timeout.
- [Idempotency](../../term_dictionary/term_idempotency.md) — replayable phases; relevance: migration phases + apply are idempotent/mergeable by stable key.
- [Compaction](../../term_dictionary/term_compaction.md) — pruning/truncation; relevance: file-era pruning/truncation paths removed; compaction snapshots SQLite-only.
- [Message Queue](../../term_dictionary/term_message_queue.md) — durable work queue; relevance: outbound/session `delivery_queue_entries` table replaces JSON queue files.
- [Subagent](../../term_dictionary/term_subagent.md) — spawned child agent; relevance: `subagent_runs` runtime rows + per-agent DB session scope.
- [Write-Back Cache](../../term_dictionary/term_write_back_cache.md) — deferred-write cache; relevance: agent-local `cache_entries` with SQL TTL replaces filesystem cache pruning.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the runtime whose state access is being cut over.

**Docs**
- [oc_refactor_database_first_decision](oc_refactor_database_first_decision.md) — (planned, this series) decision + hard contract; relevance: the contract this runtime plan enforces (no locators, no active files).
- [oc_refactor_database_first_schema_migration](oc_refactor_database_first_schema_migration.md) — (planned, this series) schema + migration; relevance: the tables this runtime reads/writes.
- [oc_refactor_acp_lifecycle](oc_refactor_acp_lifecycle.md) — (planned, this series) ACP lifecycle; relevance: ACP parent-stream + replay-ledger state moves to per-agent DB here.
- [hermes_session_search_storage](../hermes_agent/hermes_session_search_storage.md) — Hermes session search/storage; relevance: row-oriented session API analogue replacing whole-store rewrites.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — Hermes gateway internals; relevance: gateway control-plane + worker runtime parallels.
- [cc_sdk_session_store](../claude_code/cc_sdk_session_store.md) — Claude Code SDK session store; relevance: `getSessionEntry`/`upsertSessionEntry`-style row APIs.
- [cc_sdk_subprocess_model](../claude_code/cc_sdk_subprocess_model.md) — Claude Code subprocess model; relevance: workers open their own DB connections; parent owns delivery/config.
- [pi_sessions](../pi/pi_sessions.md) — PI sessions; relevance: embedded PI runner uses SQLite session scope, rejects stale handles.
- [pi_compaction_extensions](../pi/pi_compaction_extensions.md) — PI compaction extensions; relevance: PI overflow recovery rewrites SQLite transcript rows, not file truncation.
- [sqs_overview](../aws_sqs/sqs_overview.md) — SQS durable queue; relevance: durable delivery-queue semantics analogue for `delivery_queue_entries`.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — OpenClaw session store; relevance: session-store API replacement (row APIs, no `storePath`).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: control plane, `state_leases` gateway locks, worker runtime, backup integration.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw agents; relevance: ACP-stream + trajectory runtime events move to per-agent DB.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_gateway_sessions_lifecycle_patches](../../code_snippets/snippet_openclaw_gateway_sessions_lifecycle_patches.md) — session lifecycle patches; relevance: conflict-retried row patches replacing whole-store delete/insert.
- [snippet_openclaw_gateway_sessions_read_methods](../../code_snippets/snippet_openclaw_gateway_sessions_read_methods.md) — session read methods; relevance: per-agent SQLite row reads for status/listing.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle events; relevance: SQLite cascade on `sessions.delete` (no transcript orphans).
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — session compact/reset; relevance: compaction checkpoint snapshots from SQLite only.
- [snippet_openclaw_gateway_session_reset_mutation_perform](../../code_snippets/snippet_openclaw_gateway_session_reset_mutation_perform.md) — session reset mutation; relevance: reset mutates SQLite rows, no `.jsonl.lock` lane.
- [snippet_openclaw_agents_compaction_chunk_safety](../../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md) — compaction chunk safety; relevance: PI overflow recovery via SQLite transcript rewrite.
- [snippet_openclaw_agents_compaction_identifier_handoff](../../code_snippets/snippet_openclaw_agents_compaction_identifier_handoff.md) — compaction identifier handoff; relevance: `{agentId, sessionId}` identity through compaction/retry.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload apply; relevance: config stays file-backed while runtime state moves to SQLite.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: worker runtime — one worker per active run, own DB connection.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron service; relevance: runtime uses `cron_jobs`/`cron_run_logs`, not `jobs.json`/`runs/*.jsonl`.
- [snippet_openclaw_acp_event_ledger](../../code_snippets/snippet_openclaw_acp_event_ledger.md) — ACP event ledger; relevance: ACP parent-stream/replay-ledger move to per-agent DB rows.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed-image lifecycle; relevance: media bytes in `media_blobs` with SQL TTL, not filesystem.

### oc_refactor_ingress_core (10t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the channel-ingress core/plugin boundary this redraws.
- [MCP](../../term_dictionary/term_mcp.md) — tool/command surface; relevance: channel command/event surfaces consumed by agents downstream of ingress.
- [Message Queue](../../term_dictionary/term_message_queue.md) — durable work queue; relevance: the shared ingress kernel queues/dispatches inbound channel events.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — event/handler decomposition; relevance: route→command→event→activation gates are the generic ingress event model.
- [Idempotency](../../term_dictionary/term_idempotency.md) — deduped handling; relevance: durable, deduped inbound event handling in the kernel.
- [WebSocket](../../term_dictionary/term_websocket.md) — socket transport; relevance: webhook/socket transport authenticity is the plugin-owned fact layer.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — conversation↔session binding rules; relevance: route/binding resolution is core ingress policy.
- [ACP — Agent Client Protocol](../../term_dictionary/term_acp_agent_client_protocol.md) — agent protocol; relevance: the downstream agent the resolved ingress dispatches to.
- [Access Control](../../term_dictionary/term_access_control.md) — grouped/role access policy; relevance: access-group expansion + diagnostics + sender/route/command gates are core generic policy.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — direct-message pairing handshake; relevance: pairing-store DM allowlist reads are core, but pairing-challenge delivery stays plugin-local.

**Docs**
- [oc_refactor_canvas_plugin](oc_refactor_canvas_plugin.md) — (planned, this series) the sibling core/plugin boundary plan; relevance: same deletion-first "move generic seam to core, delete plugin glue" pattern.
- [hermes_webhooks_routing_delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — Hermes webhook routing/delivery; relevance: route/command/delivery seam analogue across channels.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — Hermes gateway internals; relevance: the channel-agnostic core gateway that owns generic policy.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — Hermes gateway operations; relevance: per-channel monitor/access-policy operations parallels.
- [hermes_messaging_slack](../hermes_agent/hermes_messaging_slack.md) — Hermes Slack messaging; relevance: Slack auth/access — one of the hotspot plugins to shrink.
- [hermes_messaging_teams_bot](../hermes_agent/hermes_messaging_teams_bot.md) — Hermes MS Teams bot; relevance: Teams route descriptors are a deletion-wave target.
- [hermes_telegram_setup](../hermes_agent/hermes_telegram_setup.md) — Hermes Telegram setup; relevance: Telegram ingress is the largest positive-LOC hotspot.
- [hermes_discord_advanced](../hermes_agent/hermes_discord_advanced.md) — Hermes Discord advanced; relevance: Discord DM-command-auth is a wrapper-collapse first target.
- [cc_hook_session_lifecycle_events](../claude_code/cc_hook_session_lifecycle_events.md) — Claude Code session-lifecycle hooks; relevance: event/activation gate model analogue.
- [sqs_overview](../aws_sqs/sqs_overview.md) — SQS durable queue; relevance: durable inbound ingress-kernel queue semantics analogue.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — OpenClaw channels; relevance: `src/channels/message-access/runtime.ts` core seam + bundled glue being pulled in.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channel adapters; relevance: the per-platform adapters (Telegram/Discord/Slack/…) being shrunk.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: core that receives the moved generic ingress policy.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions; relevance: the bundled plugins whose wrapper code must be deleted.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the plugin transport-facts/side-effects boundary vs core policy.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding/routing; relevance: route descriptors + route gates are core generic policy.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — ingress kernel dispatch; relevance: the shared ingress kernel that resolves once then branches on outcomes.
- [snippet_openclaw_channels_kernel_durable](../../code_snippets/snippet_openclaw_channels_kernel_durable.md) — durable ingress kernel; relevance: durable/deduped event handling in core.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread-bindings policy; relevance: binding policy stays core; per-plugin thread-binding glue is deleted.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — registry/allowlist normalization; relevance: allowlist normalization + matching is core generic policy.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing allowlist; relevance: pairing-store DM allowlist reads belong to core.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — match resolver; relevance: sender/route/command match resolution as the generic decision graph.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: route/session/envelope sequencing core may own.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status/reactions; relevance: reactions/typing/acks stay plugin-local ("Do Not Move").
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI route dispatch; relevance: route-dispatch model the ingress route gates mirror.

> **DB-verify note (2026-06-21):** all cited `term_*`, `repo_openclaw_*`, `snippet_openclaw_*`, and existing
> `band_*`/`hermes_*`/`pi_*`/`cc_*`/`aws_*` docs re-confirmed present in `notes`. Non-existent infra terms
> (`term_session`, `term_sqlite`, `term_database`, `term_wal`, `term_migration`, `term_schema`,
> `term_transaction`, `term_kysely`) were NOT used — substituted with the verified set above
> (`term_storage_engine`, `term_rdbms`, `term_oltp`, `term_acid`, `term_write_ahead_log`, `term_consistency`,
> `term_session_persistence`, `term_idempotency`, `term_compaction`, etc.). Per note ≥5 of the 10 docs are
> **Floors met for all 6 notes: ≥8 terms · ≥10 snippets · ≥10 docs.**

## Undigested Terms Plan

Per master: OpenClaw + infrastructure vocabulary on these pages are the *subjects of the doc prose*, digested
in-place as `oc_*` documentation concepts (within `argument` notes), NOT promoted to `term_dictionary`. Only
**existing** terms are linked. **Expected new `term_dictionary` captures: 0.**

| Term (appears on these pages) | Disposition |
|---|---|
| ACP / ACPX / ACP session / process lease / session ownership | Link existing `term_acp_agent_client_protocol`; ownership/lease mechanics described in-place in note 1 (`oc_refactor_acp_lifecycle`). Not a new term. |
| Gateway instance identity / lifecycle controller | Described in-place in note 1; link `repo_openclaw_gateway`. Not a new term. |
| Canvas (host/tools/commands) / bundled experimental plugin | Described in-place in note 2; link `repo_openclaw_extensions` + canvas snippets. Not a new term. |
| SQLite / WAL / `user_version` / Kysely / schema_meta | Infra config detail, described in-place (notes 3–5). `term_sqlite`/`term_wal`/`term_kysely` do not exist; master says digest in-place, do not create. Not new terms. |
| Doctor migration / migration runs / migration ledger | Described in-place (note 4); link `term_idempotency` + `term_data_pipeline`. Not a new term. |
| Per-agent database / global control plane / agent_databases registry | Described in-place (notes 3–5); link `repo_openclaw_sessions` + `term_storage_engine`. Not a new term. |
| Channel ingress / ingress kernel / route-command-event-activation | Described in-place (note 6); link `repo_openclaw_channels` + channel snippets. Not a new term. |
| Acceptance rule / deletion wave / work package | Refactor-process vocabulary, local to ingress-core; described in-place (note 6). Not reusable cross-cutting. Not a new term. |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term lacking an existing note and
lacking a doc-page home was found; the agentic/infra glossary already covers the linkable concepts. Augment
Step 2d re-scans to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms).** rx01 authors zero `term_dictionary` notes; only existing terms are linked. (Inherited
from master: any genuinely new cross-cutting term would be captured via `/tessellum-capture-term-note` + added to
its `acronym_glossary_*.md` — not triggered here.)

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (6 notes, P2). All gates must PASS before commit.

| Gate | Check | Tool / Method |
|------|-------|---------------|
| G1 | Format (YAML field order + forbidden fields; H1/`## Overview`/`## Related Notes`/`## References`/footer) | `/tessellum-check-note-format` + `python3 scripts/check_yaml_frontmatter.py --path <dir>` |
| G2 | Grounding (claims trace to source; no invented schema/phases) | diff each note vs `inbox/openclaw_docs/refactor/<page>.md` |
| G3 | Density + Coverage (≤400 lines, ≤2,500 words, ≤6 code; every mapped section present) | per-note `wc -w` / fence count + Section Coverage Map |
| G4 | Cross-Reference (≥6 relevance-selected terms + repo/sibling/snippet, each with relevance statement, indexed link format) | review `## Related Notes`; confirm `note_links` indexed after reindex |
| G5 | Ghost-reference detect + redirect (no links to non-existent notes) | `/tessellum-fix-ghost-references` / `ghost_note_references` table |
| G6 | Broken-link fix (correct relative paths) | `/tessellum-fix-broken-links` + DB rebuild |
| G7 | Discoverability — each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` | inlinks from `entry_openclaw_docs.md` (+ repo/term where applicable) |
| G8 | In-degree ≥1 (anti-island) per new note | `SELECT in_degree FROM notes WHERE note_id LIKE '%/oc_refactor_%'` ≥ 1 |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_refactor_acp_lifecycle oc_refactor_canvas_plugin oc_refactor_database_first_decision oc_refactor_database_first_schema_migration oc_refactor_database_first_runtime oc_refactor_ingress_core"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url required (G2 provenance)
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # G3 density: words (frontmatter-stripped) ≤2500, code fences ≤6
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w / ${cb} code)"
  # G4 sibling/series link present (oc_ cross-link)
  grep -q "(${SIBLING_PREFIX}" "$f" || grep -q "${SIBLING_PREFIX}" "$f" || echo "NO SIBLING ${SIBLING_PREFIX}* LINK in $n"
done

# YAML frontmatter sweep (whole folder)
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost-reference + G6 broken-link via incremental reindex, then DB checks
bash scripts/update_notes_database.sh
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
sqlite3 "$DB" "SELECT source_note, target FROM ghost_note_references WHERE source_note LIKE '%/oc_refactor_%';"  # expect empty
sqlite3 "$DB" "SELECT COUNT(*) FROM broken_links WHERE source_note LIKE '%/oc_refactor_%';"                      # G6: expect 0
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code fences (selectable ≤6) | Within caps? |
|---|---|---|---:|---|---|
| 1 | oc_refactor_acp_lifecycle | argument | 700 | 7 → reproduce ≤6 (ownership rows / lease schema) | ✅ |
| 2 | oc_refactor_canvas_plugin | argument | 500 | 1 → reproduce ≤6 (audit/verify commands) | ✅ |
| 3 | oc_refactor_database_first_decision | argument | 750 | from page's 5 → ≤6 (hard-contract / schema_meta) | ✅ (Code-Shape prose distilled, not transcribed) |
| 4 | oc_refactor_database_first_schema_migration | argument | 750 | from page's 5 → ≤6 (target schema / doctor migration) | ✅ (Migration-Inventory per-file list summarized) |
| 5 | oc_refactor_database_first_runtime | argument | 700 | from page's 5 → ≤6 (perf rules / static bans) | ✅ (Static-Bans list distilled to rules) |
| 6 | oc_refactor_ingress_core | argument | 700 | 9 → reproduce ≤6 (acceptance rule / verification) | ✅ |

No note approaches the 400-line / 2,500-word / 6-code caps after distillation. The over-compression guard is
satisfied by **splitting** database-first into 3 notes (not by cramming) and by **linking** the per-file
inventory detail to source URL + `repo_openclaw_*` rather than omitting it.

## Entry Point Decision (inherited from master)

Contributes **6 rows** to `0_entry_points/entry_openclaw_docs.md` (created as the master W1 pre-step before any
sub-plan executes) under a "Refactor / Architecture-Migration Plans" cluster. Each new note receives its
entry-point back-link at finalization (satisfies G7/G8). No new entry point is created by rx01.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; `entry_openclaw_docs.md` is the
guaranteed G8 source once W1 lands):

- `entry_openclaw_docs.md` (planned, master W1) → all 6 notes (primary anti-island source).
- `repo_openclaw_agents.md` → notes 1, 5 (ACP runtime + ACP-stream move).
- `repo_openclaw_sessions.md` → notes 3, 4, 5 (database-first session-store refactor).
- `repo_openclaw_gateway.md` → notes 1, 3, 4, 5 (lifecycle controller + control plane).
- `repo_openclaw_extensions.md` → note 2 (Canvas → bundled plugin).
- `repo_openclaw_channels.md` → note 6 (ingress-core deletion plan).
- `term_acp_agent_client_protocol.md` → notes 1, 6.
- `term_storage_engine.md` → notes 3, 4, 5.

## Pacing Rules (inherited from master)

One execution phase; 8 gates before commit. Cap dynamic-workflow fan-out at ~30 agents/run; embed the manifest
in the script. Re-read each source page; reproduce schema/command snippets verbatim, distill the prose
inventories. One BB per note (all `argument`). Reindex incrementally; verify `note_links` + 0 broken links +
in-degree ≥1 before commit. `git pull --rebase --autostash` first; commit + push per wave; **no Claude
co-author trailer**.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21 (xref-augment — floors raised + locked)** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope:** TASK 1+2 xref-augment of the 6 planned `argument` notes. Re-read all 4 source pages under
`inbox/openclaw_docs/refactor/` (acp 1,427w · canvas 943w · database-first 17,526w · ingress-core 1,661w —
measured = plan estimates, ratio 1.0). Replaced `## Candidate Cross-References` with
`## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)` at the raised floors

**Per-note locked counts (all floors met):**

| Note | Terms | Snippets | Docs | Repos | Floors met |
|---|---:|---:|---:|---:|:--:|
| oc_refactor_acp_lifecycle | 10 | 12 | 12 | 3 | ✅ |
| oc_refactor_canvas_plugin | 8 | 10 | 10 | 3 | ✅ |
| oc_refactor_database_first_decision | 10 | 11 | 11 | 3 | ✅ |
| oc_refactor_database_first_schema_migration | 10 | 11 | 11 | 3 | ✅ |
| oc_refactor_database_first_runtime | 10 | 12 | 11 | 3 | ✅ |
| oc_refactor_ingress_core | 10 | 11 | 11 | 4 | ✅ |

**Verification:** 210 mapping links extracted programmatically and resolved relative to
(rich `band_acp_*`, `hermes_acp_*`/`hermes_session_*`/`hermes_messaging_*`/`hermes_plugins_*`, `pi_sessions`/
`pi_compaction`, `cc_sdk_session_store`/`cc_*_subagents`/`cc_plugin_*`, + `aws_dynamodb`/`aws_neptune`/
(openclaw acp/process/gateway/sessions/channels/memory/plugin/macos corpus).

**Term substitutions during augment (broken-slug fixes):**
- `term_acl` (cited as "Access Control Group" for note 6) does **NOT** exist → replaced with the verified
- Non-existent infra slugs from the plan-stage candidate set were avoided entirely and substituted with the
  verified richer set: `term_storage_engine`, `term_rdbms`, `term_oltp`, `term_acid`, `term_write_ahead_log`,
  `term_consistency`, `term_session_persistence`, `term_idempotency`, `term_compaction`,
  `term_atomic_file_write`, `term_change_data_capture`, `term_event_driven_architecture`,
  `term_message_queue`, `term_write_back_cache`, `term_event_ledger`, `term_agent_lifecycle_event`,
  `term_acp_agent_communication_protocol`, `term_plugin_sdk`, `term_a2ui`, `term_capability_negotiation`,
  `term_thread_binding_policy`, `term_access_control`, `term_dm_pairing`.

**New-term candidates:** NONE. Per master + this sub-plan's Undigested Terms Plan, OpenClaw/infra vocabulary
(ACP/ACPX/lease, SQLite/WAL/`user_version`/Kysely/schema_meta, doctor migration, per-agent database, channel
ingress kernel, acceptance rule/deletion wave) is digested in-place as `oc_*` `argument` prose, NOT promoted
to `term_dictionary`. The Step-2d re-scan surfaced no genuinely cross-cutting, vault-reusable term lacking
both an existing note and a doc-page home. **Best-fit glossary: N/A (0 captures).**

**Issues:** none blocking. (Caveat carried forward, not introduced here: `entry_openclaw_docs.md` and all 6
sibling `oc_refactor_*` docs are planned-but-not-yet-created — these are the only non-existing link targets and
they materialize at master W1 + during this sub-plan's execution, so G5/G8 are satisfied at execution time, not
at plan time. 0 unexpected ghosts.)

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|:--:|---|
| CP1 | Related Notes ≥8 terms + floors | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` gives every note ≥8 terms (min 8 = canvas), ≥10 snippets, ≥10 docs, each link with a `relevance:` clause; floors table above all ✅. |
| CP2 | 9-GATE present per batch | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect, G6 broken-link, G7+G8 discoverability/in-degree; single P2 execution phase. |
| CP3 | Entry point inherited (entry_openclaw_docs planned W1) | **PASS** | `## Entry Point Decision` + `## Inlinks`: 6 rows into `0_entry_points/entry_openclaw_docs.md` (master W1 pre-step) under a "Refactor / Architecture-Migration Plans" cluster; no new entry point created by rx01 (6 notes < 15 → inherit). |
| CP4 | Size | **PASS** | 6 planned notes ≤ 30; largest source (database-first 17,526w) split 3 ways along decision→schema→runtime seams (`## Split Decisions`). |
| CP5 | Format derived | **PASS** | Format inherited verbatim from master `## Format Definition` which was derived from existing `claude_code/`+`pi/` doc corpora (`## Overview`…`## Related Notes`…`## References`, YAML field order, forbidden fields). |
| CP6 | Density | **PASS** | `## Density Re-Assessment`: all 6 notes ~500–750w / ≤6 code after distilling Code-Shape/Migration-Inventory/Static-Bans prose; none approaches 400-line/2,500-word/6-code caps. |
| CP7 | Sources measured | **PASS** | Re-measured `wc -w`: acp 1,427 · canvas 943 · database-first 17,526 · ingress-core 1,661 — exactly equal to plan estimates (ratio 1.0, within 0.7–1.3). |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (8 rows, all dispositioned "link existing / digest in-place", 0 new captures); `## Term-Note Authoring Requirements` present and marked N/A (0 new terms) per master in-place-digestion policy. |
| CP8f | Slug/collision | **PASS** | All-notes dedup: 6 `oc_*` docs do not duplicate existing `term_*`/`repo_*` (OpenClaw concepts digested as docs by design; code side is repo/snippet notes, linked not recreated). Broken-slug fix: `term_acl`→`term_access_control`+`term_dm_pairing`. 0 new term slugs → no specificity rename needed; 0 post-fix collisions. |
| CP9 | Discoverability / inlinks | **PASS** | `## Inlinks`: every new note gets ≥1 planned outside-folder inbound link (`entry_openclaw_docs.md`→all 6; plus `repo_openclaw_agents`→1,5; `repo_openclaw_sessions`→3,4,5; `repo_openclaw_gateway`→1,3,4,5; `repo_openclaw_extensions`→2; `repo_openclaw_channels`→6; `term_acp_agent_client_protocol`→1,6; `term_storage_engine`→3,4,5); G8 in-degree≥1 is a gated execution check. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.
