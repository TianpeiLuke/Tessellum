---
title: Hermes Agent Docs Digestion — Sub-Plan 06b — Plugins, Hooks & Kanban
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/
pages:
  - user-guide/features/plugins.md
  - user-guide/features/built-in-plugins.md
  - user-guide/features/hooks.md
  - user-guide/features/kanban.md
  - user-guide/features/kanban-tutorial.md
---

# Sub-Plan 06b: Plugins, Hooks & Kanban

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP06b's note
> filenames/BBs/coverage are defined. Part **b** of the SP06 split (extensibility + multi-agent
> coordination half); part **a** owns cron/delegation/goals/code-execution/batch.

## Scope

The extensibility + multi-agent-coordination surface of Hermes: the **plugin system**
(`~/.hermes/plugins/` + `plugin.yaml` + `register(ctx)`), the **bundled plugins** that ship in-tree, the
**three hook systems** (gateway / plugin / shell lifecycle hooks), and the **Kanban multi-agent task
board** (durable SQLite work queue spanning multiple named profiles, its dashboard, and a four-story
tutorial). Source = 5 mirrored pages in `inbox/hermes_agent_docs/user-guide/features/` (all substantive).
**P2 / features.** Downstream sub-plans link back to `hermes_plugins_system`, `hermes_event_hooks`, and
`hermes_kanban_multi_agent_board`. SP06b OWNS 3 new term captures (`term_hermes_plugin`,
`term_gateway_hooks`, `term_kanban_multi_agent`) — captured BEFORE the digest notes that link them.

## Content Strategy

- **One BB per note.** `plugins.md` mixes a concept overview (what the plugin system IS) with a
  procedural management/discovery workflow → split into 2. `hooks.md` (6903w, 62 code) mixes the three
  hook systems' conceptual model with the long plugin-hook callback reference → split into 2.
  `kanban.md` (10308w, 29 code) mixes the durable-board model, the worker/orchestrator procedure, and the
  dashboard surface → split into 3. `built-in-plugins.md` → 1. `kanban-tutorial.md` → 1.
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content:
  delegation/`delegate_task` + cron + code-execution + goals/Ralph loop (SP06a), the platform-adapter and
  memory/context-engine/model-provider plugin *authoring* developer guides (SP18/SP19), TTS/STT/browser/
  image-gen feature pages (SP08), the dashboard-plugin contract (SP10), MCP config-driven tools (SP09),
  Skills Hub + `register_skill` (SP05), the `config.yaml` plugin/hook/kanban settings blocks (SP02).
- **Collision (augment): `term_plugin_sdk.md` (active, ~12.6KB) is the OpenClaw TypeScript Plugin SDK
  authoring surface** (`definePluginEntry`, `OpenClawPluginApi`) — a broader cross-tool concept, NOT
  Hermes' specific Python `register(ctx)` plugin system. The planned `term_hermes_plugin` is a different,
  Hermes-scoped BB → CREATE new term + LINK `term_plugin_sdk`. Confirmed by reading the note.
- **Collision: `term_kanban.md` (active, ~10KB) is the generic Agile/WIP flow-based project-management
  methodology** (To Do → In Progress → Done, WIP limits). The planned `term_kanban_multi_agent` is
  Hermes' durable SQLite-backed multi-profile *agent* board (dispatcher, runs, claims, fan-out) — a
  different, narrower BB → CREATE new term + LINK `term_kanban`. Confirmed by reading the note.
- **Collision: no `term_gateway_hooks` / no `term_*hook*` term exists** → CREATE new; LINK
  `term_observer_pattern` + `term_agent_lifecycle_event` (the generic concepts the hooks instantiate).

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/features/kanban.md | 10308 | 29 | MIXED model+procedure+dashboard | 3 (split) |
| user-guide/features/hooks.md | 6903 | 62 | MIXED concept+procedure(ref) | 2 (split) |
| user-guide/features/plugins.md | 2802 | 10 | MIXED concept+procedure | 2 (split) |
| user-guide/features/built-in-plugins.md | 2589 | 9 | model | 1 |
| user-guide/features/kanban-tutorial.md | 2840 | 12 | empirical_observation | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **9 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_plugins_system.md` | concept | plugins §intro, §Quick overview (+Minimal working example), §What plugins can do (the `ctx.*` API table), §Plugin discovery (+sub-categories), §Plugins are opt-in (+allow-list exceptions, migration), §Plugin types, §Pluggable interfaces table, §Injecting Messages | ~1500 | What the Hermes plugin system IS: a `register(ctx)` Python extension point under `~/.hermes/plugins/`; the `ctx.*` capability surface (tools/hooks/commands/skills/providers), the 5 discovery sources + sub-category routing, the opt-in `plugins.enabled` allow-list (and what it does NOT gate), the four plugin kinds, and `inject_message`. |
| 2 | `hermes_plugins_management.md` | procedure | plugins §Plugins are opt-in (the three toggle commands), §NixOS declarative plugins, §Managing plugins (+Interactive UI, Enabled vs disabled vs neither) | ~900 | Managing plugins from the CLI: `hermes plugins` interactive UI, `install/update/remove/enable/disable`, the three plugin states (enabled/disabled/not-enabled), provider-plugin radio pickers written to `config.yaml`, and NixOS declarative `extraPlugins`. |
| 3 | `hermes_built_in_plugins.md` | model | built-in-plugins §intro, §How discovery works, §Bundled plugins are opt-in, §Currently shipped (the table + disk-cleanup, security-guidance, observability/langfuse, google_meet, hermes-achievements detail), §Adding a bundled plugin | ~1600 | The bundled in-tree plugin catalog: the `<repo>/plugins/` discovery order + opt-in rule, the shipped set (disk-cleanup, security-guidance, langfuse/nemo observability, teams_pipeline, spotify, google_meet, image-gen backends, hermes-achievements, kanban dashboard), per-plugin hooks/state/safety, and what makes a good bundling candidate. |
| 4 | `hermes_event_hooks.md` | concept | hooks §intro (three-system table), §Gateway Event Hooks (Creating, HOOK.yaml/handler.py, Available Events, Wildcard, How It Works, info callout), §Shell Hooks (intro, Comparison at a glance, Configuration schema, JSON wire protocol, Consent model, `hermes hooks` CLI, Security, Ordering and precedence) | ~1700 | The three hook systems model: gateway hooks (`HOOK.yaml`+`handler.py`, `gateway:*`/`agent:*`/`command:*` events, gateway-only), plugin hooks (`ctx.register_hook`, CLI+gateway), and shell hooks (config-driven subprocesses, JSON stdin/stdout protocol, per-`(event,command)` consent allowlist, ordering/precedence, security boundary). |
| 5 | `hermes_plugin_hook_reference.md` | procedure | hooks §Plugin Hooks (intro, general rules, Quick reference), §the 14 per-hook subsections (`pre_tool_call`…`transform_llm_output`), §Gateway BOOT.md tutorial, §worked shell-hook examples | ~2300 | The plugin-hook callback reference: the 14 lifecycle hooks (tool pre/post + block, `pre_llm_call` context injection, session start/end/finalize/reset, `subagent_stop`, `pre_gateway_dispatch` skip/rewrite, approval pre/post, the three `transform_*` rewriters), each with signature/fires-when/return contract, plus the BOOT.md startup-checklist pattern and shell-hook worked examples. |
| 6 | `hermes_kanban_multi_agent_board.md` | model | kanban §intro (two surfaces), §Kanban vs `delegate_task`, §Core concepts, §Boards (multi-project), §File attachments, §Runs — one row per attempt, §Event reference, §Out of scope, §Design spec | ~2300 | The Kanban data model: durable `~/.hermes/kanban.db` task board (task/link/comment/workspace/dispatcher/tenant), tool-surface vs CLI-surface duality, `delegate_task` vs Kanban contrast, multi-board isolation, file attachments, the task↔run two-table model + structured handoff, the full `task_events` vocabulary, single-host scope. |
| 7 | `hermes_kanban_worker_orchestrator.md` | procedure | kanban §Quick start (+gateway dispatcher, idempotent create, bulk verbs), §How workers interact with the board (+why tools, handoff evidence, worker skill, pinning skills, goal-mode, orchestrator skill), §Multi-tenant usage, §Collaboration patterns | ~2100 | Running Kanban: human CLI setup (`init`/`create`/`watch`), the `kanban_*` worker toolset lifecycle (`kanban_show`→work→`heartbeat`→`complete`/`block`), the kanban-worker + kanban-orchestrator skills, `--goal` Ralph loop cards, pinning per-task skills, multi-tenant tagging, and the 9 collaboration patterns. |
| 8 | `hermes_kanban_dashboard_cli.md` | procedure | kanban §Dashboard (GUI) (+what the plugin gives you, Auto vs Manual orchestration, Architecture, REST surface, Dashboard config, Security model, Live updates, Extending, Scope boundary, drag-to-delete, worker-visibility endpoints, swarm helper), §CLI command reference (+concurrency config, scheduled starts, respawn guard), §`/kanban` slash command | ~2000 | Operating the board through its surfaces: the bundled dashboard plugin (columns, drag-drop, drawer, Auto/Manual decompose, REST + WebSocket, localhost-auth security model, swarm helper), the full `hermes kanban` CLI verb set + concurrency/scheduling config, and the `/kanban` slash command (gateway-exempt, auto-subscribe). |
| 9 | `hermes_kanban_tutorial_walkthrough.md` | empirical_observation | kanban-tutorial §Setup, §The board at a glance (+flat view), §Story 1 Solo dev, §Story 2 Fleet farming, §Story 3 Role pipeline with retry, §Story 4 Circuit breaker and crash recovery, §Structured handoff, §Inspecting a running task, §Next steps | ~1400 | A narrated four-story walkthrough showing the board in action: solo-dev dependency chain, fleet-farming N-parallel workers, role-pipeline with a block→unblock retry (two runs), and circuit-breaker/crash-recovery — each illustrating dependency promotion, structured `summary`/`metadata` handoff, and attempt history. |

**SP06b totals:** 9 notes · concept 2 · procedure 4 · model 2 · empirical_observation 1. 5 source pages
digested (all substantive), 0 skipped. **Owns 3 new term captures** (Phase 0, interleaved): see Undigested
Terms Plan.

## Summary Statistics & Building Block Distribution

- Notes: 9 · concept 2 · procedure 4 · model 2 · empirical_observation 1.
- Source: 5 digested pages (~25.4K words) → ~15.8K words of notes (compression via link-outs to SP06a/08/
  09/10/18/19 owners; the 62 hook + 29 kanban + 19 plugin code blocks are curated to ≤6 load-bearing
  examples per note).
- BB mix: procedure 45%, concept 22%, model 22%, empirical_observation 11%.

## Section Coverage Map

```
plugins.md (2802w)
├── intro / Quick overview (+Minimal working example) ─────── → Note 1 (build-plugin guide→SP17/SP19)
├── What plugins can do (ctx.* API table) ────────────────── → Note 1 (provider/adapter authoring→SP18/19)
├── Plugin discovery (+sub-categories) ───────────────────── → Note 1
├── Plugins are opt-in (allow-list, exceptions, migration) ── → Note 1 (concept) + Note 2 (toggle commands)
├── Available hooks (table) ──────────────────────────────── → Note 1 (full hook detail→Note 5)
├── Plugin types / Pluggable interfaces table ────────────── → Note 1 (TTS/STT→SP08; MCP→SP09; skills→SP05)
├── Injecting Messages ───────────────────────────────────── → Note 1
├── NixOS declarative plugins ────────────────────────────── → Note 2 (nix-setup→SP01)
└── Managing plugins (+Interactive UI, Enabled/disabled/neither) → Note 2
built-in-plugins.md (2589w)
├── intro / How discovery works / Bundled plugins are opt-in → Note 3
├── Currently shipped (table + disk-cleanup, security-guidance, observability/langfuse, google_meet, hermes-achievements) → Note 3 (memory/context-engine→SP05; kanban tab→Note 8; spotify/image-gen→SP08)
└── Adding a bundled plugin ──────────────────────────────── → Note 3
hooks.md (6903w)
├── intro (three-system table) ───────────────────────────── → Note 4
├── Gateway Event Hooks (Creating, HOOK.yaml/handler.py, Events, Wildcard, How It Works, info) → Note 4
├── Gateway BOOT.md tutorial ─────────────────────────────── → Note 5 (delegation→SP06a; [SILENT]→SP11)
├── Plugin Hooks (intro, rules, Quick reference) ─────────── → Note 5
├── 14 per-hook subsections (pre_tool_call … transform_llm_output) → Note 5 (delegate_task→SP06a)
├── Shell Hooks (intro, Comparison, schema, JSON protocol) ─ → Note 4
├── Shell-hook worked examples (auto-format/block/inject/log) → Note 5
└── Consent model / hermes hooks CLI / Security / Ordering ── → Note 4
kanban.md (10308w)
├── intro (two surfaces) / Kanban vs delegate_task / Core concepts → Note 6 (delegate_task→SP06a)
├── Boards (multi-project) / File attachments ────────────── → Note 6
├── Quick start (+gateway dispatcher, idempotent, bulk verbs) → Note 7
├── How workers interact (+why tools, handoff, worker/orchestrator skill, goal-mode, pinning skills) → Note 7 (goal loop→SP06a; skills→SP05)
├── Multi-tenant usage / Collaboration patterns ──────────── → Note 7
├── Dashboard (GUI) (+Auto/Manual, Architecture, REST, config, Security, Live updates, Extending, Scope, drag-delete, worker endpoints, swarm) → Note 8 (dashboard contract→SP10)
├── CLI command reference (+concurrency config, scheduled, respawn guard) → Note 8
├── /kanban slash command ────────────────────────────────── → Note 8 (gateway platforms→SP11-13)
├── Runs — one row per attempt / Event reference ─────────── → Note 6
└── Out of scope / Design spec ───────────────────────────── → Note 6
kanban-tutorial.md (2840w) ── ALL sections (Setup, board glance, Stories 1-4, Structured handoff, in-flight, Next steps) → Note 9 (overview→Note 6)
```

No source H2/H3 orphaned. All 5 pages fully covered; feature-page detail intentionally routed to owning SPs
as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| plugins.md (2802w, 10 code) | Note 1 (system concept) + Note 2 (management procedure) | >2500w; BB mixing — what the plugin system IS (concept: discovery, kinds, ctx.* surface) vs how you manage/toggle/install plugins (procedure). |
| hooks.md (6903w, 62 code) | Note 4 (three-systems concept + gateway/shell config) + Note 5 (plugin-hook callback reference, procedure) | >4000w → 2 notes; the conceptual three-system model + gateway/shell config is a distinct BB from the 14-hook callback-signature reference (procedure); 62 code blocks split across the two keep each ≤6 curated. |
| kanban.md (10308w, 29 code) | Note 6 (board data model) + Note 7 (worker/orchestrator procedure) + Note 8 (dashboard + CLI + slash procedure) | >4000w → 3 notes; the durable-board data model (tasks/runs/events/boards — model BB) is distinct from the worker/orchestrator tool lifecycle (procedure) and from the dashboard/CLI operating surfaces (procedure); keeps each ≤2500w and ≤6 curated code blocks from 29 source blocks. |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; search term_dictionary AND documentation/)

| Planned note / slug | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `term_hermes_plugin` (owned) | `term_plugin_sdk.md` (active, ~12.6KB), `term_plugin_manifest.md` (active, ~15.9KB), `term_provider_plugin.md` (active) | **NOT a dup** — `term_plugin_sdk` is the *OpenClaw TypeScript* SDK authoring surface (broader cross-tool concept); `term_plugin_manifest`/`term_provider_plugin` are component concepts. The owned term is Hermes' specific Python `register(ctx)` / `plugin.yaml` system. | CAPTURE new `term_hermes_plugin`; LINK all three as related. |
| `term_gateway_hooks` (owned) | none (`term_%hook%` returns 0 rows) | **NEW** — no term covers Hermes' three-system lifecycle hooks | CAPTURE new `term_gateway_hooks`; LINK `term_observer_pattern`, `term_agent_lifecycle_event`, `term_event_driven_architecture`. |
| `term_kanban_multi_agent` (owned) | `term_kanban.md` (active, ~10KB) | **NOT a dup** — `term_kanban` is the generic *Agile/WIP project-management methodology*; this is Hermes' durable SQLite multi-profile *agent* board (dispatcher/runs/claims/fan-out) | CAPTURE new `term_kanban_multi_agent`; LINK `term_kanban` (foundation) + `term_multi_agent_systems`. |
| `hermes_plugins_system`, `hermes_plugins_management`, `hermes_built_in_plugins` | no substantive doc note in `hermes_agent/`; `term_plugin_sdk`/`term_plugin_manifest` are concept terms not doc duplicates | NEW | CREATE. |
| `hermes_event_hooks`, `hermes_plugin_hook_reference` | no `hermes_agent/` doc note; no term covers these | NEW | CREATE. |
| `hermes_kanban_multi_agent_board`, `hermes_kanban_worker_orchestrator`, `hermes_kanban_dashboard_cli`, `hermes_kanban_tutorial_walkthrough` | `term_kanban` (generic methodology — LINK not dup) | NEW | CREATE; LINK `term_kanban` / `term_kanban_multi_agent`. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords;
**0 substantive same-concept duplicates** (the `term_plugin_sdk` and `term_kanban` hits are confirmed
different-concept by reading both notes). New `hermes_agent/` folder → no doc-doc collisions (intra-series
links resolve at finalization). Owned-term collision audit visually confirmed per the master caution list.

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **Four-floor standard set 2026-06-19 (user directive — supersedes all prior floors).** Each note's
> `## Related Notes` now carries FOUR COUNTED groups, all relevancy-selected and each rendered as
> `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`:
>   the 13 `repo_hermes_agent_*` notes that digest the Hermes SOURCE CODE; each note links the repos whose
>   modules implement what THIS doc note documents (plugins↔`repo_hermes_agent_plugins`, hooks↔`…gateway_messaging`,
>   kanban↔`…agent_core`/`…cli`, etc.).
>   Hermes implementation corpus (517 notes); each note links the ≥10 snippets whose CODE this doc note
>   documents, selected by the planned note's content. **This is now a COUNTED floor** (raised from the prior 8
>   and promoted from a "bonus" group — snippets are NO LONGER a bonus group).
> - **≥10 DOCUMENTATION notes** (`../../documentation/`) — sibling `hermes_*` notes in this series (resolve at
>
> The PRIOR floor was ≥8 term + ≥5 code-repo + ≥10 doc with snippets as a bonus group (itself a 2026-06-19
> revision of the original ≥8 term + ≥8 snippet + ≥5 doc). The snippet group is now a COUNTED floor at ≥10,
> later in execution). SP06b-owned terms (`term_hermes_plugin`, `term_gateway_hooks`, `term_kanban_multi_agent`)
> are captured in Phase 0 (so they are real link targets, NOT +fin) — like the sibling `hermes_*` docs they are
> created within this execution; terms owned by OTHER SPs that don't yet exist are marked `[own]` in `(+fin …)`
> and EXCLUDED from the ≥8 floor.

**Note 1 `hermes_plugins_system`** (concept)
- Terms (8): [Hermes Plugin](../../term_dictionary/term_hermes_plugin.md) — Hermes' Python `register(ctx)` extension point; relevance: this note IS the plugin-system concept the term names. · [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — OpenClaw TS plugin SDK; relevance: the cross-tool authoring analogue the page contrasts with the Python `ctx.*` surface. · [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — the `plugin.yaml` manifest concept; relevance: every Hermes plugin dir carries a `plugin.yaml` manifest the loader reads. · [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — single-select backend plugin; relevance: memory/context-engine/model providers are the "provider plugin" kind among the four plugin types. · [Skills](../../term_dictionary/term_skills.md) — agent skill packages; relevance: `ctx.register_skill()` lets a plugin bundle namespaced `plugin:skill` skills. · [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — skill descriptor; relevance: bundled-skill registration mirrors the skill-manifest contract. · [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the page routes "external tools via MCP" as a config-driven alternative to Python plugins. · [Self-Evolving Agent](../../term_dictionary/term_self_evolving_agent.md) — agent that extends itself; relevance: the plugin surface is how Hermes grows new tools/hooks/commands without core edits. (+fin: term_messaging_gateway [own SP11])
- Code-Repos (5): [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — the `plugins/` PluginManager + `register(ctx)` loader; relevance: this is the exact module that implements the plugin system, sub-categories, and discovery this note documents. · [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider/adapter registries; relevance: implements the memory/context-engine/model-provider "provider plugin" loaders and `register_provider`. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — toolset + tool registry; relevance: `ctx.register_tool()` wires plugin tools into the same registry as built-in tools. · [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — skills loader; relevance: backs `ctx.register_skill()` namespaced `plugin:skill` bundling. · [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — repo root; relevance: defines `~/.hermes/plugins/` layout, `HERMES_ENABLE_PROJECT_PLUGINS`, and the pip entry-point discovery source. · [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP toolset bridge; relevance: implements the config-driven MCP extension surface the Pluggable-interfaces table points to.
- Docs (10): [hermes_plugins_management](hermes_plugins_management.md) — managing/toggling plugins; relevance: the operational sibling to this concept note. · [hermes_built_in_plugins](hermes_built_in_plugins.md) — bundled plugin catalog; relevance: the bundled-source row of the discovery table. · [hermes_event_hooks](hermes_event_hooks.md) — hook systems; relevance: the "Available hooks" table here links the full hook detail. · [hermes_plugin_hook_reference](hermes_plugin_hook_reference.md) — the 14 hooks; relevance: `ctx.register_hook` callbacks the plugin surface exposes. · [hermes_kanban_dashboard_cli](hermes_kanban_dashboard_cli.md) — dashboard plugin; relevance: the kanban dashboard is itself a bundled plugin using this surface. · [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — Claude Code plugin model; relevance: closest external-agent plugin-system analogue. · [cc_plugin_components](../claude_code/cc_plugin_components.md) — plugin component kinds; relevance: parallels Hermes' tools/hooks/commands/skills capability slots. · [cc_plugin_manifest_schema](../claude_code/cc_plugin_manifest_schema.md) — plugin manifest schema; relevance: analogue of `plugin.yaml`. · [cc_extending_claude_code](../claude_code/cc_extending_claude_code.md) — extension-surface overview; relevance: same "pick the right extension surface" decision the Pluggable-interfaces table makes. · [cc_sdk_plugins](../claude_code/cc_sdk_plugins.md) — SDK plugin loading; relevance: programmatic plugin registration analogue to `register(ctx)`.
- Snippets (11): [plugins_namespace_init](../../code_snippets/snippet_hermes_agent_plugins_namespace_init.md) — `plugins/__init__.py` PluginManager + four-source discovery; relevance: implements the discovery table + sub-category routing this concept note describes. · [plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — `plugin.yaml` manifest fields; relevance: the manifest every `~/.hermes/plugins/<name>/` dir carries (`requires_env`, name, version). · [plugins_interfaces_abcs](../../code_snippets/snippet_hermes_agent_plugins_interfaces_abcs.md) — `PluginContext` ABC + `ctx.*` registration methods; relevance: the exact `ctx.register_tool/hook/command/skill` surface in the "What plugins can do" table. · [plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK/loader architecture; relevance: how `register(ctx)` wires schemas→handlers at load time. · [plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-plugin registry; relevance: backs the memory/context-engine/model "provider plugin" kind among the four types. · [plugins_memory_discovery](../../code_snippets/snippet_hermes_agent_plugins_memory_discovery.md) — `plugins/memory/__init__.py` own loader; relevance: the single-select exclusive memory discovery system the sub-category table names. · [plugins_context_engine_discovery](../../code_snippets/snippet_hermes_agent_plugins_context_engine_discovery.md) — context-engine own loader; relevance: the one-active context-compression discovery path. · [skills_vs_plugins](../../code_snippets/snippet_hermes_agent_skills_vs_plugins.md) — skill vs plugin distinction; relevance: clarifies `ctx.register_skill()` bundling vs standalone plugins. · [plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — bundled `web` plugin example; relevance: a concrete `register(ctx)` plugin showing the tool/hook surface. · [tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: `ctx.register_tool()` wires plugin tools into this same registry as built-ins. · [tools_skill_manager](../../code_snippets/snippet_hermes_agent_tools_skill_manager.md) — skill manager; relevance: backs `ctx.register_skill()` namespaced `plugin:skill` loading.

**Note 2 `hermes_plugins_management`** (procedure)
- Terms (8): [Hermes Plugin](../../term_dictionary/term_hermes_plugin.md) — the Python plugin system; relevance: this note manages those plugins via the `hermes plugins` CLI/UI. · [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `plugin.yaml`; relevance: `requires_env` keys in the manifest drive the install-time prompts. · [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — single-select backend; relevance: the Provider-Plugins UI section is a radio picker written to `config.yaml`. · [Context Engine](../../term_dictionary/term_context_engine.md) — context-compression backend; relevance: `context.engine` selection is one of the provider radios this note writes. · [MCP](../../term_dictionary/term_mcp.md) — MCP servers; relevance: config-driven tools coexist with the managed plugin allow-list. · [OAuth Token](../../term_dictionary/term_oauth_token.md) — OAuth credential; relevance: provider/backend plugins gate on `requires_env` secrets prompted during install. · [Idempotency](../../term_dictionary/term_idempotency.md) — repeat-safe operation; relevance: `--enable`/`--no-enable` scripted installs are designed to be re-runnable without prompts. · [Self-Evolving Agent](../../term_dictionary/term_self_evolving_agent.md) — self-extending agent; relevance: enable/disable/install is how the user grows the agent's capability set. (+fin: term_tool_gateway [own SP05])
- Code-Repos (5): [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — PluginManager + enable/disable state; relevance: implements `plugins.enabled`/`plugins.disabled`, the three states, and grandfathering this note documents. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes` CLI; relevance: implements `hermes plugins install/update/remove/enable/disable` and the interactive UI. · [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider registries; relevance: backs the provider radio pickers (`memory.provider`, `context.engine`) saved to config. · [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — TUI/interactive screens; relevance: implements the composite `hermes plugins` interactive toggle screen. · [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — repo root + config schema; relevance: defines config schema v21+ opt-in migration and the NixOS `extraPlugins` module options. · [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — skills loader; relevance: bundled-skill plugins are synced/managed alongside the plugin install flow.
- Docs (10): [hermes_plugins_system](hermes_plugins_system.md) — the concept note; relevance: this procedure operates the system that note defines. · [hermes_built_in_plugins](hermes_built_in_plugins.md) — bundled catalog; relevance: bundled plugins are enabled with the same `hermes plugins enable` verb. · [hermes_event_hooks](hermes_event_hooks.md) — hook systems; relevance: enabling a plugin loads its registered hooks. · [hermes_config_files_precedence](hermes_config_files_precedence.md) — config layering; relevance: enable/provider selections persist to `~/.hermes/config.yaml`. · [hermes_install_nixos_module](hermes_install_nixos_module.md) — NixOS module; relevance: the declarative `extraPlugins`/`extraPythonPackages` path documented here. · [cc_plugin_cli_commands](../claude_code/cc_plugin_cli_commands.md) — plugin CLI verbs; relevance: closest analogue to the `hermes plugins` verb set. · [cc_plugin_marketplaces_and_install](../claude_code/cc_plugin_marketplaces_and_install.md) — install-from-source flow; relevance: parallels `hermes plugins install user/repo`. · [cc_plugin_user_config_and_env](../claude_code/cc_plugin_user_config_and_env.md) — per-plugin config/env; relevance: analogue of `requires_env` prompts and provider config keys. · [cc_managed_plugin_policy_settings](../claude_code/cc_managed_plugin_policy_settings.md) — enable/deny policy; relevance: analogue of the enabled/disabled allow-list semantics. · [cc_plugin_caching_and_troubleshooting](../claude_code/cc_plugin_caching_and_troubleshooting.md) — plugin state/troubleshooting; relevance: parallels enabled-vs-disabled-vs-neither state diagnosis.
- Snippets (10): [cli_plugins_install](../../code_snippets/snippet_hermes_agent_cli_plugins_install.md) — `hermes plugins install user/repo` flow; relevance: implements the git-clone install + Enable? prompt this procedure documents. · [cli_plugins_discover](../../code_snippets/snippet_hermes_agent_cli_plugins_discover.md) — plugin discovery for the CLI; relevance: feeds the `hermes plugins list` three-state table. · [cli_plugins_cmd_list_info](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_list_info.md) — `plugins list`/`info` verbs; relevance: renders enabled/disabled/not-enabled state per plugin. · [cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — `install` subcommand + `--enable`/`--no-enable`; relevance: the scripted-install flags this note covers. · [cli_plugins_cmd_remove](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_remove.md) — `remove`/`update` verbs; relevance: `hermes plugins remove`/`update my-plugin`. · [cli_plugins_cmd_doctor](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_doctor.md) — plugin doctor diagnostics; relevance: diagnoses enabled-vs-disabled-vs-neither state. · [plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-plugin registry; relevance: backs the provider radio pickers (`memory.provider`, `context.engine`) written to config. · [plugins_namespace_init](../../code_snippets/snippet_hermes_agent_plugins_namespace_init.md) — PluginManager enable/disable state; relevance: implements `plugins.enabled`/`plugins.disabled` and grandfathering. · [cli_tools_config](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — `hermes tools` interactive config; relevance: the provider-setup wizard (e.g. langfuse) that adds entries to `plugins.enabled`. · [cli_setup_skills](../../code_snippets/snippet_hermes_agent_cli_setup_skills.md) — bundled-skill sync on install; relevance: bundled-skill plugins are synced alongside the plugin install flow.

**Note 3 `hermes_built_in_plugins`** (model)
- Terms (8): [Hermes Plugin](../../term_dictionary/term_hermes_plugin.md) — the plugin surface; relevance: bundled plugins use the identical hooks/tools/commands surface, just maintained in-tree. · [Observability for Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — agent tracing; relevance: the langfuse/nemo_relay bundled plugins emit per-turn/LLM/tool observability spans. · [Data Observability](../../term_dictionary/term_data_observability.md) — data/trace visibility; relevance: the observability plugins surface token/cost breakdowns to external dashboards. · [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — malicious-input class; relevance: security-guidance pattern-matches dangerous code (incl. injection sinks) on file writes. · [PII](../../term_dictionary/term_pii.md) — sensitive data; relevance: security-guidance + the metadata-secrets guidance keep PII/secrets out of tracked artifacts. · [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — skill descriptor; relevance: bundled plugins (kanban) ship skills declared via manifest. · [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — backend plugin; relevance: bundled image-gen backends (`image_gen/openai`, `xai`) are provider-style backends. · [Self-Evolving Agent](../../term_dictionary/term_self_evolving_agent.md) — self-extending agent; relevance: hermes-achievements/disk-cleanup show the agent maintaining its own state/history. (+fin: term_text_to_speech [own SP08])
- Code-Repos (5): [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — `<repo>/plugins/` tree; relevance: this catalog documents the bundled plugins that live in exactly this module. · [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider registries; relevance: backs the bundled image-gen backends and observability provider wiring. · [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — dashboard backend; relevance: hosts the dashboard-tab plugins (hermes-achievements, kanban) and their `dashboard/manifest.json`. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tool registry; relevance: spotify (7 tools) + google_meet (`meet_*`) register model-visible tools through it. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway lifecycle; relevance: disk-cleanup/security-guidance/langfuse hook into the gateway+CLI lifecycle events this catalog describes. · [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — repo root; relevance: defines the four-source discovery order and the bundled-opt-in rule.
- Docs (10): [hermes_plugins_system](hermes_plugins_system.md) — the plugin concept; relevance: bundled plugins are a specialization of that system. · [hermes_plugins_management](hermes_plugins_management.md) — enable/disable; relevance: bundled plugins opt in via the same `hermes plugins enable <name>`. · [hermes_event_hooks](hermes_event_hooks.md) — hook systems; relevance: most bundled plugins (disk-cleanup, langfuse, security-guidance) are hooks-based. · [hermes_kanban_dashboard_cli](hermes_kanban_dashboard_cli.md) — kanban dashboard plugin; relevance: `kanban/dashboard` is one of the shipped bundled plugins. · [hermes_plugin_hook_reference](hermes_plugin_hook_reference.md) — hook callbacks; relevance: documents the exact hooks (`post_tool_call`, `on_session_end`, `pre_api_request`) these bundled plugins register. · [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — CC plugin model; relevance: external bundled-plugin analogue. · [cc_security_guidance_plugin](../claude_code/cc_security_guidance_plugin.md) — CC security-guidance plugin; relevance: Hermes' security-guidance is a verbatim Apache-2.0 fork of exactly this. · [cc_security_guidance_layers_and_rules](../claude_code/cc_security_guidance_layers_and_rules.md) — the rule layers; relevance: documents the upstream rule set (and the two unported LLM-review layers Hermes notes). · [cc_monitoring_opentelemetry_setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — OTel observability; relevance: analogue of the langfuse/nemo observability bundled plugins. · [cc_large_codebase_skills_and_plugins](../claude_code/cc_large_codebase_skills_and_plugins.md) — bundling skills+plugins; relevance: parallels the "good bundling candidate" criteria this note ends on.
- Snippets (10): [plugins_disk_cleanup](../../code_snippets/snippet_hermes_agent_plugins_disk_cleanup.md) — disk-cleanup bundled plugin; relevance: the `post_tool_call`/`on_session_end` ephemeral-file tracker this catalog details. · [plugins_observability_langfuse](../../code_snippets/snippet_hermes_agent_plugins_observability_langfuse.md) — langfuse observability plugin; relevance: the per-turn/LLM/tool span tracer the catalog documents hook-by-hook. · [plugins_google_meet](../../code_snippets/snippet_hermes_agent_plugins_google_meet.md) — google_meet plugin; relevance: the `meet_*` toolset + transcription bundled plugin. · [plugins_hermes_achievements](../../code_snippets/snippet_hermes_agent_plugins_hermes_achievements.md) — achievements dashboard plugin; relevance: the dashboard-only `state.db`-scanning tab the catalog describes. · [plugins_spotify](../../code_snippets/snippet_hermes_agent_plugins_spotify.md) — spotify backend plugin; relevance: the 7-tool playback/queue backend plugin row. · [plugins_teams_pipeline](../../code_snippets/snippet_hermes_agent_plugins_teams_pipeline.md) — teams_pipeline plugin; relevance: the Graph-backed Teams meeting-summary standalone plugin. · [plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen backend dispatch; relevance: the `image_gen/openai`/`xai` provider-style backends shipped in-tree. · [plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen backend dispatch; relevance: the sibling provider-backend dispatch pattern bundled backends use. · [plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: backs the bundled image-gen backend + observability provider wiring. · [cli_security_advisories](../../code_snippets/snippet_hermes_agent_cli_security_advisories.md) — security-advisory pattern data; relevance: the security-guidance plugin's 25-rule Apache-2.0 fork the catalog calls out.

**Note 4 `hermes_event_hooks`** (concept)
- Terms (8): [Gateway Hooks](../../term_dictionary/term_gateway_hooks.md) — Hermes' three-system lifecycle hooks; relevance: this note IS the three-hook-systems concept the term names. · [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — callback-on-event pattern; relevance: all three hook systems are observers registered against lifecycle events. · [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — agent-loop event; relevance: hooks fire on `gateway:*`/`agent:*`/`session:*`/`command:*` lifecycle events. · [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — event-dispatch design; relevance: `hooks.emit()` is an event dispatcher fanning out to matching handlers. · [Hermes Plugin](../../term_dictionary/term_hermes_plugin.md) — the plugin surface; relevance: plugin hooks are registered via `ctx.register_hook()` inside `register()`. · [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — input-attack class; relevance: `pre_tool_call` block + shell-hook consent are defenses against unsafe agent actions. · [Guardrails](../../term_dictionary/term_guardrails.md) — safety controls; relevance: tool-blocking and per-`(event,command)` consent are the hook guardrail surface. · [Pub-Sub](../../term_dictionary/term_pub_sub.md) — publish/subscribe; relevance: handlers subscribe to event types (incl. `command:*` wildcards) and the emitter publishes. (+fin: term_messaging_gateway [own SP11])
- Code-Repos (5): [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway runner + `HookRegistry`; relevance: implements `discover_and_load()`, `hooks.emit()`, the gateway event vocabulary, and `pre_gateway_dispatch`. · [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — `ctx.register_hook`; relevance: the plugin-hook registration path (CLI + gateway). · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `run_agent.py` turn loop; relevance: hosts `pre_llm_call`/`post_llm_call`/session-lifecycle hook fire sites. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tool dispatch; relevance: `pre_tool_call`/`post_tool_call`/`transform_*` fire inside `handle_function_call()` / the terminal tool. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI startup; relevance: registers shell hooks via `register_from_config()` and the `hermes hooks` CLI. · [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — repo root; relevance: defines `VALID_HOOKS`, `~/.hermes/hooks/`, and the shell-hook allowlist file.
- Docs (10): [hermes_plugin_hook_reference](hermes_plugin_hook_reference.md) — the 14 plugin hooks; relevance: this concept note's companion reference. · [hermes_plugins_system](hermes_plugins_system.md) — plugin surface; relevance: plugin hooks are part of `register(ctx)`. · [hermes_built_in_plugins](hermes_built_in_plugins.md) — bundled plugins; relevance: most bundled plugins are hooks-based consumers of this model. · [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — security/consent config; relevance: the `hooks:` block + `hooks_auto_accept` consent settings live there. · [hermes_messaging_media_settings](hermes_messaging_media_settings.md) — gateway/platform config; relevance: gateway hooks fire only on messaging platforms configured there. · [cc_hooks_overview](../claude_code/cc_hooks_overview.md) — CC hooks model; relevance: closest external lifecycle-hook analogue. · [cc_hook_events_catalog](../claude_code/cc_hook_events_catalog.md) — CC event catalog; relevance: parallels the gateway "Available Events" table. · [cc_hook_session_lifecycle_events](../claude_code/cc_hook_session_lifecycle_events.md) — session lifecycle hooks; relevance: analogue of `on_session_start/end/finalize/reset`. · [cc_hook_tool_loop_events](../claude_code/cc_hook_tool_loop_events.md) — tool-loop hooks; relevance: analogue of `pre/post_tool_call` and `transform_*`. · [cc_hooks_guardrail_and_audit_recipes](../claude_code/cc_hooks_guardrail_and_audit_recipes.md) — guardrail/audit recipes; relevance: parallels the block/auto-format/inject/audit shell-hook examples.
- Snippets (10): [gw_hooks](../../code_snippets/snippet_hermes_agent_gw_hooks.md) — `HookRegistry.discover_and_load()` + `hooks.emit()`; relevance: implements the gateway hook system (HOOK.yaml/handler.py, event vocabulary, wildcard) this concept note describes. · [core_shell_hooks_allowlist](../../code_snippets/snippet_hermes_agent_core_shell_hooks_allowlist.md) — `shell-hooks-allowlist.json` consent store; relevance: the per-`(event,command)` first-use consent model the shell-hooks section documents. · [core_shell_hooks_callback](../../code_snippets/snippet_hermes_agent_core_shell_hooks_callback.md) — shell-hook subprocess dispatch + JSON wire protocol; relevance: the stdin/stdout JSON protocol + `register_from_config()`. · [plugins_interfaces_abcs](../../code_snippets/snippet_hermes_agent_plugins_interfaces_abcs.md) — `ctx.register_hook` ABC; relevance: the plugin-hook registration path (CLI + gateway). · [tui_server_panic_hooks](../../code_snippets/snippet_hermes_agent_tui_server_panic_hooks.md) — TUI panic/error hook handling; relevance: shows the non-blocking error-catch discipline ("errors caught and logged, never crash") all three systems share. · [conv_loop_post_api_hook](../../code_snippets/snippet_hermes_agent_conv_loop_post_api_hook.md) — per-turn hook fire site in the conversation loop; relevance: where `pre/post_llm_call` and the transform hooks fire. · [cli_security_advisories](../../code_snippets/snippet_hermes_agent_cli_security_advisories.md) — security advisories; relevance: the security boundary the shell-hook consent + `pre_tool_call` block guard. · [tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — approval policy; relevance: the consent/guardrail surface the hook-block path integrates with. · [gw_runner_router](../../code_snippets/snippet_hermes_agent_gw_runner_router.md) — `GatewayRunner` message router; relevance: hosts `pre_gateway_dispatch` and the gateway event-emit sites. · [gw_session_lifecycle](../../code_snippets/snippet_hermes_agent_gw_session_lifecycle.md) — gateway session lifecycle; relevance: fires `session:start/end/reset` gateway events the Available-Events table lists.

**Note 5 `hermes_plugin_hook_reference`** (procedure)
- Terms (8): [Gateway Hooks](../../term_dictionary/term_gateway_hooks.md) — the hook systems; relevance: this reference enumerates the plugin-hook half of that model. · [Hermes Plugin](../../term_dictionary/term_hermes_plugin.md) — plugin surface; relevance: all 14 hooks are registered via `ctx.register_hook()` in a plugin. · [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — observer callbacks; relevance: most hooks are fire-and-forget observers receiving keyword args. · [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — human approval step; relevance: `pre_approval_request`/`post_approval_response` fire around the user-approval prompt. · [Subagent](../../term_dictionary/term_subagent.md) — delegated child agent; relevance: `subagent_stop` fires once per `delegate_task` child. · [PII](../../term_dictionary/term_pii.md) — sensitive data; relevance: `transform_tool_result`/`transform_terminal_output` are the redaction surface (secret/PII scrubbing). · [Guardrails](../../term_dictionary/term_guardrails.md) — safety controls; relevance: `pre_tool_call` block is the canonical tool-veto guardrail hook. · [Context Window](../../term_dictionary/term_context_window.md) — model context budget; relevance: `pre_llm_call` injects context into the user message while preserving the system-prompt cache. (+fin: term_delegate_task [own SP06a])
- Code-Repos (5): [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `run_agent.py`; relevance: hosts `pre_llm_call`/`post_llm_call`/`on_session_*` fire sites described per-hook. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — `model_tools.py`/`delegate_tool.py`/`approval.py`; relevance: implements `pre/post_tool_call`, `transform_*`, `subagent_stop`, approval hooks. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — `gateway/run.py`; relevance: `pre_gateway_dispatch` + the shell-hook dispatcher/`invoke_hook()` ordering. · [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — `ctx.register_hook`; relevance: the registration entry point every callback signature here uses. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI atexit + shell-hook config; relevance: the second `on_session_end` fire site and shell-hook examples (`auto-format`, `block-rm-rf`). · [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — repo root; relevance: defines the JSON wire protocol + `shell-hooks-allowlist.json` the worked examples use.
- Docs (10): [hermes_event_hooks](hermes_event_hooks.md) — the three-systems concept; relevance: this is its callback-signature reference half. · [hermes_plugins_system](hermes_plugins_system.md) — plugin surface; relevance: `register(ctx)` is where these hooks are wired. · [hermes_built_in_plugins](hermes_built_in_plugins.md) — bundled plugins; relevance: concrete hook consumers (langfuse uses `pre_api_request`/`post_tool_call`, etc.). · [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — consent/security config; relevance: shell-hook consent + auto-accept settings. · [hermes_kanban_worker_orchestrator](hermes_kanban_worker_orchestrator.md) — delegation/worker lifecycle; relevance: `subagent_stop` ties hooks to delegation/orchestration. · [cc_hook_tool_loop_events](../claude_code/cc_hook_tool_loop_events.md) — tool-loop hooks; relevance: per-hook analogue for `pre/post_tool_call`. · [cc_hook_session_lifecycle_events](../claude_code/cc_hook_session_lifecycle_events.md) — session hooks; relevance: analogue for the session-lifecycle hooks. · [cc_async_hooks](../claude_code/cc_async_hooks.md) — async hook handlers; relevance: Hermes handlers may be `async def`; same execution model. · [cc_prompt_and_agent_hooks](../claude_code/cc_prompt_and_agent_hooks.md) — prompt/agent hooks; relevance: analogue of `pre_llm_call` context injection (`UserPromptSubmit`). · [cc_hooks_guardrail_and_audit_recipes](../claude_code/cc_hooks_guardrail_and_audit_recipes.md) — block/audit recipes; relevance: parallels the block + redact + audit hook use cases.
- Snippets (10): [gw_hooks](../../code_snippets/snippet_hermes_agent_gw_hooks.md) — hook dispatcher/`invoke_hook()`; relevance: the `pre_gateway_dispatch` + shell-hook ordering/precedence this reference enumerates. · [conv_loop_post_api_hook](../../code_snippets/snippet_hermes_agent_conv_loop_post_api_hook.md) — per-turn hook fire site; relevance: the exact `pre_llm_call`/`post_llm_call` fire location each per-hook subsection cites. · [core_shell_hooks_callback](../../code_snippets/snippet_hermes_agent_core_shell_hooks_callback.md) — shell-hook JSON callback; relevance: the worked shell-hook examples (auto-format, block-rm-rf, inject git status). · [tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — approval policy; relevance: where `pre_approval_request`/`post_approval_response` fire around the user prompt. · [tools_approval_ui](../../code_snippets/snippet_hermes_agent_tools_approval_ui.md) — approval UI surfaces; relevance: the CLI/TUI/gateway surfaces the approval hooks observe. · [core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — redaction patterns; relevance: the secret/PII scrubbing the `transform_tool_result`/`transform_terminal_output` hooks perform. · [tools_delegate_aggregate](../../code_snippets/snippet_hermes_agent_tools_delegate_aggregate.md) — `delegate_task` child aggregation; relevance: the `subagent_stop` fire-per-child path marshalled to the parent thread. · [core_tool_dispatch_helpers](../../code_snippets/snippet_hermes_agent_core_tool_dispatch_helpers.md) — tool-dispatch helpers; relevance: `pre/post_tool_call` fire inside `handle_function_call()`. · [conv_loop_post_api_retry](../../code_snippets/snippet_hermes_agent_conv_loop_post_api_retry.md) — post-API retry path; relevance: shows the guarded `if final_response and not interrupted` `post_llm_call` firing condition. · [core_tool_executor_concurrent](../../code_snippets/snippet_hermes_agent_core_tool_executor_concurrent.md) — concurrent tool executor; relevance: the parallel tool-call path where `pre_tool_call` fires once per parallel call.

**Note 6 `hermes_kanban_multi_agent_board`** (model)
- Terms (8): [Kanban Multi-Agent](../../term_dictionary/term_kanban_multi_agent.md) — Hermes' durable multi-profile board; relevance: this note IS the data model the term names. · [Kanban](../../term_dictionary/term_kanban.md) — generic Agile/WIP methodology; relevance: the foundation the multi-agent board specializes (status columns, WIP). · [Multi-Agent Systems](../../term_dictionary/term_multi_agent_systems.md) — coordinated agents; relevance: the board coordinates N named profiles as full OS processes. · [Message Queue](../../term_dictionary/term_message_queue.md) — durable work queue; relevance: Kanban is a durable message-queue + state machine, contrasted with `delegate_task` RPC. · [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — event sourcing; relevance: every transition appends a row to the append-only `task_events` log. · [Idempotency](../../term_dictionary/term_idempotency.md) — dedup on retry; relevance: optional idempotency key dedups retried automation creates. · [FTS5](../../term_dictionary/term_fts5.md) — SQLite full-text search; relevance: the board is a SQLite (`kanban.db`) store queried/filtered for tasks. · [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — coordinating agent work; relevance: the dispatcher promotes/claims/spawns across the task graph. (+fin: term_delegate_task [own SP06a])
- Code-Repos (5): [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — dispatcher + `kanban_db` kernel; relevance: implements claim/promote/reclaim, the task/run/event schema, and the dispatcher loop this model describes. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes kanban` tree; relevance: the CLI surface over the same `kanban_db` (init/create/runs/events). · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — `kanban_*` toolset; relevance: the model-facing read/mutate surface over the board. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway-embedded dispatcher; relevance: the dispatcher runs inside the gateway (`dispatch_in_gateway`) and spawns workers. · [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — repo root; relevance: defines `~/.hermes/kanban.db`, boards layout, `task_runs`/`task_events` tables, and the v2-reserved columns. · [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — scheduled/recurring jobs; relevance: `scheduled_at` starts + recurring-ops patterns share the dispatcher's tick model.
- Docs (10): [hermes_kanban_worker_orchestrator](hermes_kanban_worker_orchestrator.md) — worker/orchestrator procedure; relevance: how agents drive the model defined here. · [hermes_kanban_dashboard_cli](hermes_kanban_dashboard_cli.md) — dashboard + CLI; relevance: the human surfaces over this data model. · [hermes_kanban_tutorial_walkthrough](hermes_kanban_tutorial_walkthrough.md) — four stories; relevance: the model demonstrated end-to-end. · [hermes_event_hooks](hermes_event_hooks.md) — hook systems; relevance: gateway/`subagent_stop` hooks observe dispatcher/worker lifecycle. · [hermes_session_search_storage](hermes_session_search_storage.md) — SQLite state/storage; relevance: kanban.db sits alongside the session/state DB storage model. · [cc_orchestrate_agent_teams](../claude_code/cc_orchestrate_agent_teams.md) — agent-team orchestration; relevance: closest external multi-agent-coordination analogue. · [cc_agent_teams_overview](../claude_code/cc_agent_teams_overview.md) — agent teams; relevance: parallels the named-profile collaboration primitive. · [cc_run_agents_in_parallel](../claude_code/cc_run_agents_in_parallel.md) — parallel agents; relevance: analogue of fan-out over independent worker processes. · [cc_sdk_todo_and_task_tracking](../claude_code/cc_sdk_todo_and_task_tracking.md) — task tracking; relevance: analogue of the task/status/dependency model. · [cc_worktree_isolation](../claude_code/cc_worktree_isolation.md) — git-worktree isolation; relevance: the `worktree:` workspace kind for coding tasks.
- Snippets (10): [plugins_kanban](../../code_snippets/snippet_hermes_agent_plugins_kanban.md) — bundled kanban plugin + dispatcher; relevance: the durable-board kernel (claim/promote/reclaim) this data model describes. · [cli_kanban_schema](../../code_snippets/snippet_hermes_agent_cli_kanban_schema.md) — `kanban.db` schema (tasks/links/comments/runs/events); relevance: the exact task/link/run/event tables + v2-reserved columns this model enumerates. · [cli_kanban_crud](../../code_snippets/snippet_hermes_agent_cli_kanban_crud.md) — task/link/comment CRUD; relevance: the create/link/comment writes that populate the model. · [tools_kanban_query](../../code_snippets/snippet_hermes_agent_tools_kanban_query.md) — `kanban_show`/`kanban_list` read layer; relevance: the model-facing read surface over the board. · [core_hermes_state_schema](../../code_snippets/snippet_hermes_agent_core_hermes_state_schema.md) — Hermes state schema; relevance: `kanban.db` sits alongside the session/state DB storage model. · [cli_kanban_diagnostics](../../code_snippets/snippet_hermes_agent_cli_kanban_diagnostics.md) — board diagnostics; relevance: surfaces the board-health invariants (current_run_id ↔ terminal run) the model guarantees. · [gw_session_state](../../code_snippets/snippet_hermes_agent_gw_session_state.md) — gateway session state; relevance: the gateway hosts the embedded dispatcher (`dispatch_in_gateway`) over this state. · [cron_job_state](../../code_snippets/snippet_hermes_agent_cron_job_state.md) — cron job state; relevance: `scheduled_at` starts + recurring-ops share the dispatcher tick model. · [tools_kanban_register](../../code_snippets/snippet_hermes_agent_tools_kanban_register.md) — `kanban_*` toolset registration; relevance: shows how `HERMES_KANBAN_TASK` flips on the board toolset over this model. · [cli_kanban_query](../../code_snippets/snippet_hermes_agent_cli_kanban_query.md) — `runs`/`stats`/`list` query verbs; relevance: the run/event read views that expose the task↔run two-table model.

**Note 7 `hermes_kanban_worker_orchestrator`** (procedure)
- Terms (8): [Kanban Multi-Agent](../../term_dictionary/term_kanban_multi_agent.md) — the board; relevance: this procedure runs workers/orchestrators against it. · [Subagent](../../term_dictionary/term_subagent.md) — spawned child agent; relevance: dispatcher-spawned workers are task-scoped agents driving `kanban_*` tools. · [Multi-Agent Systems](../../term_dictionary/term_multi_agent_systems.md) — agent coordination; relevance: worker + orchestrator roles are the multi-agent coordination pattern. · [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — fan-out/route; relevance: the kanban-orchestrator skill decomposes/links/assigns without doing the work. · [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — long-running coding agents; relevance: `--goal` runs a Ralph-style loop until a judge agrees. · [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — human checkpoint; relevance: block→comment→unblock is the human-input path. · [Circuit Breaker](../../term_dictionary/term_circuit_breaker.md) — failure cutoff; relevance: `failure_limit`/`--max-retries` auto-blocks thrashing tasks. · [Self-Evolving Agent](../../term_dictionary/term_self_evolving_agent.md) — self-improving agent; relevance: retry workers read prior-attempt failures and pick a different strategy. (+fin: term_delegate_task [own SP06a], term_persistent_goal [own SP06a])
- Code-Repos (5): [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — `kanban_*` toolset; relevance: implements `kanban_show/heartbeat/complete/block/create/link/unblock` the worker lifecycle calls. · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — dispatcher + worker spawn; relevance: sets `HERMES_KANBAN_TASK`, spawns profiles, runs the goal loop + circuit breaker. · [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — bundled skills; relevance: ships the `kanban-worker`/`kanban-orchestrator` skills synced into every profile. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes kanban`/`hermes -p`; relevance: the human setup verbs + per-profile skills list/reset commands. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway dispatcher host; relevance: hosts the dispatcher that spawns workers and routes goal-mode cards. · [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — recurring jobs; relevance: the long-running-journal (P4) pattern pairs cron with a shared-dir worker.
- Docs (10): [hermes_kanban_multi_agent_board](hermes_kanban_multi_agent_board.md) — the data model; relevance: what this procedure operates on. · [hermes_kanban_dashboard_cli](hermes_kanban_dashboard_cli.md) — dashboard/CLI; relevance: the human side of the worker/orchestrator flow. · [hermes_kanban_tutorial_walkthrough](hermes_kanban_tutorial_walkthrough.md) — four stories; relevance: shows the worker/orchestrator loop end-to-end. · [hermes_plugin_hook_reference](hermes_plugin_hook_reference.md) — `subagent_stop`; relevance: the hook fired when a delegated child (or worker) finishes. · [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — skills/memory config; relevance: pinned skills + per-tenant memory prefixes the worker uses. · [cc_orchestrate_agent_teams](../claude_code/cc_orchestrate_agent_teams.md) — team orchestration; relevance: analogue of the orchestrator decomposition playbook. · [cc_run_agents_in_parallel](../claude_code/cc_run_agents_in_parallel.md) — parallel workers; relevance: analogue of fleet-farming N workers. · [cc_goal_command](../claude_code/cc_goal_command.md) — goal/Ralph loop; relevance: `--goal` cards run the same Ralph engine behind `/goal`. · [cc_work_with_subagents](../claude_code/cc_work_with_subagents.md) — driving subagents; relevance: parallels worker-skill tool-call discipline. · [cc_create_a_subagent](../claude_code/cc_create_a_subagent.md) — defining a subagent; relevance: analogue of assigning a profile + skills to a task.
- Snippets (10): [tools_kanban_mutate](../../code_snippets/snippet_hermes_agent_tools_kanban_mutate.md) — `kanban_complete/block/heartbeat/create/link/unblock`; relevance: the worker-lifecycle mutate tools (`kanban_show`→work→`heartbeat`→`complete`/`block`) this procedure runs. · [tools_kanban_register](../../code_snippets/snippet_hermes_agent_tools_kanban_register.md) — `kanban` toolset registration; relevance: `HERMES_KANBAN_TASK` flips the toolset on for dispatcher-spawned workers + orchestrator profiles. · [tools_kanban_query](../../code_snippets/snippet_hermes_agent_tools_kanban_query.md) — `kanban_show`/`kanban_list`; relevance: how the worker reads its task + how orchestrators discover board work. · [cli_kanban_commands](../../code_snippets/snippet_hermes_agent_cli_kanban_commands.md) — `hermes kanban` verb tree; relevance: the human setup verbs (`init`/`create`/`watch`) + `-p` per-profile skills commands. · [skills_devops_kanban_worker](../../code_snippets/snippet_hermes_agent_skills_devops_kanban_worker.md) — `kanban-worker` bundled skill; relevance: teaches the worker the tool-call lifecycle (and the protocol-violation guard) this note documents. · [skills_devops_kanban_orchestrator](../../code_snippets/snippet_hermes_agent_skills_devops_kanban_orchestrator.md) — `kanban-orchestrator` bundled skill; relevance: the decompose/link/assign playbook + anti-temptation rules. · [tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — child-agent spawn; relevance: the worker-spawn pattern the dispatcher reuses to launch assigned profiles. · [core_run_agent_cli](../../code_snippets/snippet_hermes_agent_core_run_agent_cli.md) — `run_agent` CLI entry; relevance: how a spawned worker boots with its task-scoped session + `--skills kanban-worker`. · [gw_runner_cron](../../code_snippets/snippet_hermes_agent_gw_runner_cron.md) — gateway cron runner; relevance: the P4 long-running-journal pattern pairs cron with a shared-dir worker. · [gw_session_lifecycle](../../code_snippets/snippet_hermes_agent_gw_session_lifecycle.md) — gateway session lifecycle; relevance: hosts the dispatcher that spawns workers + routes `--goal` Ralph-loop cards.

**Note 8 `hermes_kanban_dashboard_cli`** (procedure)
- Terms (8): [Kanban Multi-Agent](../../term_dictionary/term_kanban_multi_agent.md) — the board; relevance: the dashboard + CLI are its operating surfaces. · [Kanban](../../term_dictionary/term_kanban.md) — Agile board UI; relevance: the dashboard renders the familiar column/drag-drop board. · [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — event observers; relevance: the dashboard tails the append-only `task_events` table via WebSocket. · [Pub-Sub](../../term_dictionary/term_pub_sub.md) — publish/subscribe; relevance: the WebSocket `/events?since=` stream is a pub-sub feed of new event rows. · [Circuit Breaker](../../term_dictionary/term_circuit_breaker.md) — failure cutoff; relevance: the respawn guard + `failure_limit` are exposed in the CLI/config surface. · [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throughput caps; relevance: `max_in_progress`/`max_in_progress_per_profile`/`auto_decompose_per_tick` cap concurrency/spend. · [Idempotency](../../term_dictionary/term_idempotency.md) — repeat-safe create; relevance: `--idempotency-key` makes scripted/webhook creates safe. · [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — auto/manual decompose; relevance: the Auto/Manual orchestration pill + decomposer fan-out are dashboard controls. (+fin: term_messaging_gateway [own SP11])
- Code-Repos (5): [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — dashboard backend; relevance: hosts the FastAPI router + WebSocket tail the kanban dashboard plugin mounts under `/api/plugins/kanban/`. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes kanban` verbs; relevance: implements the full CLI command reference, concurrency/scheduling config, and `run_slash()`. · [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — bundled dashboard plugin; relevance: the dashboard ships as the `plugins/kanban/` bundled plugin via the dashboard-plugin contract. · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `kanban_db` + decomposer; relevance: every REST/drag-drop write routes through the same `kanban_db` and the decomposer kernel. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — `/kanban` slash + notifier; relevance: the gateway-exempt `/kanban` command, auto-subscribe, and terminal-event notifications. · [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — repo root; relevance: defines localhost-bind security model + `dashboard.kanban` config keys.
- Docs (10): [hermes_kanban_multi_agent_board](hermes_kanban_multi_agent_board.md) — data model; relevance: what these surfaces read/write. · [hermes_kanban_worker_orchestrator](hermes_kanban_worker_orchestrator.md) — worker procedure; relevance: the model-facing counterpart to these human surfaces. · [hermes_kanban_tutorial_walkthrough](hermes_kanban_tutorial_walkthrough.md) — stories; relevance: every story uses the dashboard + CLI shown here. · [hermes_built_in_plugins](hermes_built_in_plugins.md) — bundled catalog; relevance: lists `kanban/dashboard` as the bundled dashboard plugin. · [hermes_web_dashboard](hermes_web_dashboard.md) — dashboard framework; relevance: the kanban tab follows the dashboard-plugin contract documented there. · [cc_analytics_dashboards](../claude_code/cc_analytics_dashboards.md) — analytics dashboard; relevance: analogue of a web board UI over agent activity. · [cc_agent_view_monitor](../claude_code/cc_agent_view_monitor.md) — live agent monitor; relevance: analogue of the worker-visibility endpoints + live updates. · [cc_move_tasks_web_terminal](../claude_code/cc_move_tasks_web_terminal.md) — task UI over web/terminal; relevance: parallels the dual dashboard/CLI/slash surfaces. · [cc_create_and_run_workflows](../claude_code/cc_create_and_run_workflows.md) — workflow runner; relevance: analogue of decompose→fan-out→synthesize via the dashboard. · [cc_dynamic_workflows](../claude_code/cc_dynamic_workflows.md) — dynamic workflow graphs; relevance: analogue of the auto-decompose task-graph fan-out.
- Snippets (10): [plugins_kanban](../../code_snippets/snippet_hermes_agent_plugins_kanban.md) — bundled kanban dashboard plugin (FastAPI router + WebSocket tail); relevance: the `plugins/kanban/` dashboard REST/WS surface mounted under `/api/plugins/kanban/`. · [cli_kanban_commands](../../code_snippets/snippet_hermes_agent_cli_kanban_commands.md) — `hermes kanban` verb tree; relevance: the full CLI command reference + `run_slash()` `/kanban` entry. · [cli_kanban_crud](../../code_snippets/snippet_hermes_agent_cli_kanban_crud.md) — create/edit/assign/link CRUD; relevance: the writes drag-drop + inline-create route through the same `kanban_db`. · [cli_kanban_query](../../code_snippets/snippet_hermes_agent_cli_kanban_query.md) — `list`/`stats`/`runs`/`watch`; relevance: the board/worker-visibility read endpoints + live `watch`. · [cli_kanban_decompose](../../code_snippets/snippet_hermes_agent_cli_kanban_decompose.md) — decompose/specify path; relevance: the Auto/Manual decompose + `auxiliary.kanban_decomposer` controls. · [cli_kanban_diagnostics](../../code_snippets/snippet_hermes_agent_cli_kanban_diagnostics.md) — `diagnostics`/`inspect`; relevance: the combined dispatcher-snapshot worker-visibility endpoint. · [plugins_example_dashboard](../../code_snippets/snippet_hermes_agent_plugins_example_dashboard.md) — dashboard-plugin example contract; relevance: the dashboard-plugin manifest/contract the kanban tab follows. · [gw_session_state](../../code_snippets/snippet_hermes_agent_gw_session_state.md) — gateway session state; relevance: the `/kanban` slash command + auto-subscribe live in the gateway. · [gw_slash_access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — gateway slash-command access; relevance: the gateway-exempt `/kanban` running-agent-guard bypass this note documents. · [gw_status_snapshot](../../code_snippets/snippet_hermes_agent_gw_status_snapshot.md) — gateway status snapshot; relevance: the dispatcher in-progress/`max_in_progress` inspect surface + Nudge-dispatcher button.

**Note 9 `hermes_kanban_tutorial_walkthrough`** (empirical_observation)
- Terms (8): [Kanban Multi-Agent](../../term_dictionary/term_kanban_multi_agent.md) — the board; relevance: the four stories all exercise it. · [Multi-Agent Systems](../../term_dictionary/term_multi_agent_systems.md) — coordinated agents; relevance: Story 2/3 show N workers + role pipelines collaborating. · [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — dependency promotion; relevance: parent→child promotion drives the solo-dev and pipeline stories. · [Circuit Breaker](../../term_dictionary/term_circuit_breaker.md) — failure cutoff; relevance: Story 4 demonstrates `spawn_failed → gave_up` after `--max-retries 3`. · [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — block/unblock; relevance: Story 3's reviewer block→unblock retry is the HITL path. · [Subagent](../../term_dictionary/term_subagent.md) — spawned worker; relevance: each story spawns task-scoped worker agents. · [Idempotency](../../term_dictionary/term_idempotency.md) — repeat-safe runs; relevance: retried runs re-execute safely and append new `task_runs` rows. · [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — coding agents; relevance: the schema/API/test pipeline workers are autonomous coders. (+fin: term_delegate_task [own SP06a])
- Code-Repos (5): [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — dispatcher + runs; relevance: implements dependency promotion, run history, crash-detection/circuit-breaker the stories exercise. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — `kanban_*` tools; relevance: the worker tool-call loops shown in each story. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes kanban` verbs; relevance: the `create/runs/show/unblock` commands the human runs in each story. · [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — kanban-worker skill; relevance: teaches the worker the tool-call lifecycle the stories illustrate. · [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — dashboard; relevance: every story is narrated with dashboard drawer/Run-History screenshots. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway dispatcher; relevance: `hermes gateway start` hosts the dispatcher that drains the fleet in Story 2.
- Docs (10): [hermes_kanban_multi_agent_board](hermes_kanban_multi_agent_board.md) — data model; relevance: the prerequisite overview the tutorial assumes. · [hermes_kanban_worker_orchestrator](hermes_kanban_worker_orchestrator.md) — worker procedure; relevance: the lifecycle the stories narrate. · [hermes_kanban_dashboard_cli](hermes_kanban_dashboard_cli.md) — dashboard/CLI; relevance: the surfaces shown throughout. · [hermes_plugins_system](hermes_plugins_system.md) — plugin surface; relevance: the dashboard tab the tutorial uses is a bundled plugin. · [hermes_event_hooks](hermes_event_hooks.md) — hooks; relevance: gateway notifications on `gave_up`/`completed` are hook-driven. · [cc_orchestrate_agent_teams](../claude_code/cc_orchestrate_agent_teams.md) — team orchestration; relevance: analogue of the role-pipeline story. · [cc_run_agents_in_parallel](../claude_code/cc_run_agents_in_parallel.md) — parallel agents; relevance: analogue of the fleet-farming story. · [cc_verification_loop](../claude_code/cc_verification_loop.md) — verify/retry loop; relevance: analogue of the block→fix→complete retry in Story 3. · [cc_subagents_overview](../claude_code/cc_subagents_overview.md) — subagent model; relevance: analogue of the task-scoped worker agents each story spawns. · [cc_goal_command](../claude_code/cc_goal_command.md) — goal loop; relevance: analogue of the "keep going until acceptance criteria met" worker behavior.
- Snippets (10): [plugins_kanban](../../code_snippets/snippet_hermes_agent_plugins_kanban.md) — dispatcher + dependency promotion + circuit breaker; relevance: implements the parent→child promotion, run history, and `spawn_failed → gave_up` the four stories exercise. · [cli_kanban_crud](../../code_snippets/snippet_hermes_agent_cli_kanban_crud.md) — `create`/`link`/`unblock`; relevance: the `hermes kanban create --parent`/`unblock` commands each story runs. · [cli_kanban_query](../../code_snippets/snippet_hermes_agent_cli_kanban_query.md) — `runs`/`show`/`stats`; relevance: the `hermes kanban runs` attempt-history the retry/crash stories print. · [tools_kanban_mutate](../../code_snippets/snippet_hermes_agent_tools_kanban_mutate.md) — `kanban_show`/`complete`/`block`/`heartbeat`; relevance: the worker tool-call loops shown verbatim in every story. · [skills_devops_kanban_worker](../../code_snippets/snippet_hermes_agent_skills_devops_kanban_worker.md) — `kanban-worker` skill; relevance: teaches the worker the show→work→complete lifecycle the stories illustrate. · [cli_kanban_commands](../../code_snippets/snippet_hermes_agent_cli_kanban_commands.md) — `hermes kanban` verb tree; relevance: the `init`/`create`/`runs` commands the human runs in each story. · [core_hermes_state_schema](../../code_snippets/snippet_hermes_agent_core_hermes_state_schema.md) — state schema; relevance: the `task_runs`/`task_events` rows the stories' drawers and Run-History sections read. · [skills_devops_kanban_orchestrator](../../code_snippets/snippet_hermes_agent_skills_devops_kanban_orchestrator.md) — `kanban-orchestrator` skill; relevance: the role-pipeline (Story 3) decomposition/handoff pattern. · [cli_kanban_decompose](../../code_snippets/snippet_hermes_agent_cli_kanban_decompose.md) — decompose/specify; relevance: the triage auto-decompose the board-glance section describes. · [gw_session_state](../../code_snippets/snippet_hermes_agent_gw_session_state.md) — gateway session state; relevance: `hermes gateway start` hosts the dispatcher that drains the fleet (Story 2) and fires `gave_up` notifications.

All 9 notes meet ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc (four-floor standard). **Finalization catch:** `term_state_machine`
event-sourced via the append-only `task_events` log). Net Note-6 term list: term_kanban_multi_agent, term_kanban,
term_multi_agent_systems, term_message_queue, term_event_driven_architecture, term_idempotency, term_fts5,

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 5 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages table
(no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 plugins-system | concept | 1500 | 6 (minimal example + ctx table samples; rest in prose) | ✓ |
| 2 plugins-management | procedure | 900 | ≤6 (from CLI/UI/nix blocks) | ✓ |
| 3 built-in-plugins | model | 1600 | ≤6 (curate from 9 blocks; one per plugin in prose tables) | ✓ |
| 4 event-hooks | concept | 1700 | ≤6 (HOOK.yaml + handler + shell schema + JSON protocol) | ✓ |
| 5 plugin-hook-reference | procedure | 2300 | ≤6 (curate from 62 short blocks; one canonical signature per hook in prose) | ✓ |
| 6 kanban-board-model | model | 2300 | ≤6 (curate from concepts/runs/events blocks) | ✓ |
| 7 kanban-worker-orchestrator | procedure | 2100 | ≤6 (worker loop + orchestrator fan-out + goal-mode) | ✓ |
| 8 kanban-dashboard-cli | procedure | 2000 | ≤6 (CLI ref + config + slash blocks) | ✓ |
| 9 kanban-tutorial | empirical_observation | 1400 | ≤6 (one worker-tool-call block per story) | ✓ |

No further splits needed — all 9 notes ≤2500w. Notes 5/6/7/8 (the code-heavy refs at ~2000-2300w) are each
one topically-cohesive single-BB cluster; the 62 hook + 29 kanban source code blocks are curated to ≤6
load-bearing examples per note (kept VERBATIM), the rest summarized in prose tables (per review CP6
default-to-keep justification: cohesive single theme, no BB mixing). If any note exceeds 350 lines during
writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it
IS, NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; **≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc**
a bonus group]) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP06b)

**SP06b owns 3 new term captures** (Pattern B, interleaved — captured in **Phase 0** BEFORE the digest
notes that link them, so they are real link targets from the start). Capture uses
`/tessellum-capture-term-note <term>` (NOT inline authoring). Augment re-read surfaced **0 additional** new
undigested terms beyond the master inventory.

| Term Slug | Best-Fit Glossary | Capture Phase | Stub or Full | Source Page | Notes (collision verdict) |
|---|---|---|---|---|---|
| `term_hermes_plugin` | acronym_glossary_developer.md | Phase 0 (interleaved, pre-digest) | full term note | plugins.md, built-in-plugins.md | NEW; `term_plugin_sdk` (OpenClaw TS SDK) + `term_plugin_manifest` are DIFFERENT concepts → LINK, do not merge. DF 14 in master. |
| `term_gateway_hooks` | acronym_glossary_developer.md | Phase 0 (interleaved, pre-digest) | full term note | hooks.md | NEW; no `term_*hook*` exists. Hermes' three-system lifecycle hooks (gateway/plugin/shell). DF 9. |
| `term_kanban_multi_agent` | acronym_glossary_workflows.md | Phase 0 (interleaved, pre-digest) | full term note | kanban.md, kanban-tutorial.md | NEW; `term_kanban` (generic Agile/WIP methodology, active) is a DIFFERENT concept → LINK as foundation, do not overwrite. DF 13. |

`term_kanban`, `term_plugin_sdk`, `term_plugin_manifest`, `term_provider_plugin`, `term_subagent`,
`term_multi_agent_systems`, `term_autonomous_coding_agents`, `term_agent_orchestration`, `term_self_evolving_agent`,
`term_skills`, `term_skill_manifest`, `term_mcp`, `term_context_engine`, `term_observer_pattern`,
`term_agent_lifecycle_event`, `term_event_driven_architecture`, `term_pub_sub`, `term_message_queue`,
`term_circuit_breaker`, `term_rate_limiting`, `term_idempotency`, `term_fts5`, `term_human_in_the_loop`,
`term_guardrails`, `term_prompt_injection`, `term_pii`, `term_observability_agent_systems`,
`term_data_observability`, `term_oauth_token`, `term_context_window`.

### Renamed (general → specific)

| Original (would-be) slug | Renamed to | Reason |
|---|---|---|
| `term_plugin` | `term_hermes_plugin` | Bare "plugin" collides with the generic plugin-system concept AND the existing `term_plugin_sdk` (OpenClaw); scope-qualify to the Hermes Python `register(ctx)` system. |
| `term_hooks` | `term_gateway_hooks` | One-word common noun; "hooks" collides with React hooks / git hooks / shell hooks. Use the literature/source scope (Hermes lifecycle/gateway hooks). |
| `term_kanban` (would duplicate) | `term_kanban_multi_agent` | `term_kanban` already exists as the generic Agile methodology; the Hermes board is a scope-specific multi-agent variant — qualify the slug to avoid overwriting the substantive existing note. |

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, status, ~size) | Action |
|---|---|---|
| `term_plugin_sdk` (would duplicate) | `resources/term_dictionary/term_plugin_sdk.md` (active, ~12.6KB) | Not captured — DIFFERENT concept (OpenClaw TS SDK); LINK from `hermes_plugins_system` / `term_hermes_plugin`. |
| `term_kanban` (would duplicate) | `resources/term_dictionary/term_kanban.md` (active, ~10KB) | Not captured — generic Agile methodology; LINK as foundation from `term_kanban_multi_agent` and the kanban doc notes. |
| `term_observability` (would-be) | `resources/term_dictionary/term_observability_agent_systems.md` + `term_data_observability.md` (both active) | Not captured — existing agent-systems/data observability terms cover it; LINK from `hermes_built_in_plugins`. |

Re-ran the Step 4e.2 pre-flight against the 3 renamed-to slugs (`term_hermes_plugin`, `term_gateway_hooks`,
`term_kanban_multi_agent`) — all 3 are confirmed NEW (DB returns no row), no post-rename collision.

## Term-Note Authoring Requirements (Per Undigested Term — Inherited from `/tessellum-capture-term-note` canonical)

Every term in the Undigested Terms Plan MUST be authored via **`/tessellum-capture-term-note <term>`** (interactive
or via ENRICHER_INPUTS), NOT inline-authored within a digest note. The capture skill enforces the requirements
below; SP06b respects them (no bypass, no requirement reduction).

### YAML Frontmatter (Required Fields)

`tags` (resource, terminology, + 2 domain tags e.g. `agent_systems`, `plugin_system` / `multi_agent` / `lifecycle_hooks`);
`keywords` (acronym + full name + variant spellings); `topics`; `language: markdown`; `date of note`;
`status: active`; `building_block: concept` (MUST be concept); `access_control_group: ["general"]`;
`related_wiki` (primary URL or null). Forbidden fields: `title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `note_second_category`.

### Required H1 + H2 Sections (in order)

`# <Name>` H1 → `## Definition` (1-2 paragraphs: what it is, problem it solves, who uses it) →
`## Context` (teams/systems/programs — here, Hermes Agent / Nous Research, the gateway/dispatcher) →
`## Key Characteristics` (bullet list of distinctive properties) → `## Performance / Metrics` (OPTIONAL —
omit unless metrics found) → `## Related Terms` (**8-15 vault term-note links minimum**, mix in-domain +
cross-domain, INDEXED `**[Term Name](term_X.md)** — one-line description`) → `## References` (EXTERNAL URLs
ONLY; the Hermes docs URL + ≥1 broader source; NO `term_*.md` links here).


The Hermes docs page is ONE viewpoint. Each capture MUST research across multiple sources (the source doc is
docs site, plus an orthogonal source — e.g. for `term_hermes_plugin`: the VS Code / Obsidian plugin-API
analogy and the existing `term_plugin_sdk` note; for `term_gateway_hooks`: the observer/lifecycle-hook
pattern literature; for `term_kanban_multi_agent`: the message-queue / work-queue + multi-agent-systems
literature and the existing `term_kanban`); (6) vault cross-reference via `/tessellum-search-notes` + DB query
for in-domain + cross-domain related terms.

### Cross-Domain Diversity for Related Terms (8-15 links minimum)

Per capture-term-note Step 3e, Related Terms MUST include cross-domain connections (≥3 in-domain + ≥3
cross-domain = ≥8-15 total verified links): **Foundation** (e.g. `term_kanban` → `term_kanban_multi_agent`;
`term_observer_pattern` → `term_gateway_hooks`; `term_plugin_sdk` → `term_hermes_plugin`); **Application**;
**Analogy**; **Contrast** (`term_kanban_multi_agent` vs `term_delegate_task` RPC; `term_hermes_plugin` vs
MCP server); **Component** (`term_plugin_manifest` → `term_hermes_plugin`); **Successor/Predecessor**. All

### Math Notation, Fleeting-Content Guard, Glossary Entry, Pre-Flight Routing, File Naming, Depth-Scaled Minimums, Backlinks, Section Ordering, >200-Line Decomposition

- **MathJax** for any formula (`$...$` inline, `$$...$$` display) — verbatim from source, never plain-text math.
- **Fleeting content guard**: no person aliases as POCs (use team aliases — "Nous Research team"); no bare
  ETAs; bare dollar amounts get `(as of YYYY)`; no bare headcounts.
- **Glossary entry** (Step 5): update the best-fit `acronym_glossary_developer.md` (plugin/hooks) /
  `acronym_glossary_workflows.md` (kanban) with the exact `**Full Name** / **Description** (4-5 sentences MAX,
  bold the single most distinguishing fact, NO metrics) / **Documentation** / **Wiki** / **Related**` template.
- **Pre-flight routing**: all 3 owned slugs return NO matching note (verified) → `Stub or Full: full`,
  proceed to create. (No substantive note exists at the 3 owned paths — verified; no overwrite risk.)
- **File naming**: `term_hermes_plugin.md`, `term_gateway_hooks.md`, `term_kanban_multi_agent.md` (already
  scope-canonical; no acronym normalization applies).
- **Depth-scaled Related Terms minimums**: full term notes target ≥8 (simple), ≥10 (moderate), ≥12 (complex).
  These three are expected moderate-to-complex → target ≥10-12.
- **Backlink expansion (Step 6e, REVERSE)**: add the new term to 5-10 existing in-domain + cross-domain term
  notes' `## Related Terms` (e.g. add `term_hermes_plugin` to `term_plugin_sdk`, `term_plugin_manifest`,
  `term_provider_plugin`, `term_skills`; `term_kanban_multi_agent` to `term_kanban`, `term_multi_agent_systems`,
  `term_agent_orchestration`, `term_subagent`; `term_gateway_hooks` to `term_observer_pattern`,
  `term_agent_lifecycle_event`, `term_event_driven_architecture`).
- **Section ordering**: `## Related Terms` (all `.md` links) BEFORE `## References` (external URLs only); footer last.
- **>200-line decomposition**: if a captured term note exceeds 200 lines, decompose per Step 7
  (Procedure→`sop_*`, Model/Argument→`thought_*`); keep concept + Related Terms in parent.
  OR mark `status: stub` with `research_pending: true` — do NOT silently emit a digest-doc-only stub.

### ENRICHER_INPUTS Non-Interactive Pattern

For batch dispatch, supply `ENRICHER_INPUTS` (key_terms, acronym, domain context keywords, summary_snippets
from the digest doc, references) + SOURCE CONTENT (verbatim excerpt). The skill may then skip interactive

### Acceptance — term-note authoring is NOT done if

Single-source (digest-doc-only) trapped scope; Related Terms < depth-scaled minimum or lacking cross-domain
diversity; no Step-6e inlink expansion (5-10 target); `## References` contains `term_*.md` links or
`## Related Terms` contains external URLs; section ordering violated; YAML uses a forbidden field;
`building_block ≠ concept`; fleeting content without temporal qualifier; glossary Description >5 sentences or
contains metrics; note >200 lines without Step-7 decomposition; non-canonical file naming; a substantive note
was OVERWRITTEN instead of redirected; math in plain-text instead of MathJax. → any one = **FAIL**.

## Execution Phases (per-phase 8-GATE)

- **Phase 0 (term captures — interleaved, BEFORE digest notes):** capture `term_hermes_plugin`,
  ≥10-12 Related Terms + glossary entry + Step-6e backlinks). Reindex → verify the 3 term notes exist + are
  active BEFORE digesting. GATE G1 (format) + G5 (ghost-free Related Terms) + G6 + G8.
- **Phase 1 (plugins + hooks concept, P-pilot):** Notes 1, 2, 4. Pilot Note 1 (`hermes_plugins_system`) first
  → reindex → verify format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (bundled + hook reference):** Notes 3, 5. GATE G1–G8.
- **Phase 3 (kanban cluster):** Notes 6, 7, 8, 9. GATE G1–G8.
- **Phase 3b (inlinks — EXECUTED, G8):** add the inlink-table backlinks from existing notes; verify every new
  note (3 terms + 9 docs) has DB in-degree ≥1 from outside the folder.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` (code verbatim for
kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify every
ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB ·
**G8 in-degree ≥1 from outside the folder**.

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
# G8: in-degree ≥1 from outside the folder (3 owned terms + 9 docs)
for n in resources/term_dictionary/term_hermes_plugin resources/term_dictionary/term_gateway_hooks resources/term_dictionary/term_kanban_multi_agent \
  resources/documentation/hermes_agent/hermes_plugins_system resources/documentation/hermes_agent/hermes_plugins_management resources/documentation/hermes_agent/hermes_built_in_plugins \
  resources/documentation/hermes_agent/hermes_event_hooks resources/documentation/hermes_agent/hermes_plugin_hook_reference resources/documentation/hermes_agent/hermes_kanban_multi_agent_board \
  resources/documentation/hermes_agent/hermes_kanban_worker_orchestrator resources/documentation/hermes_agent/hermes_kanban_dashboard_cli resources/documentation/hermes_agent/hermes_kanban_tutorial_walkthrough; do
```

## Entry Point Decision (inherited)

Contributes **9 doc rows + 3 term rows** to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE —
master Step 4c, >30-note series) under a "Plugins, Hooks & Kanban" section. Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP06b does NOT create a separate entry point —
the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).
The 3 owned term captures also update their glossaries (`acronym_glossary_developer.md` ×2,
`acronym_glossary_workflows.md` ×1) per the term-note authoring spec.

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_plugins.md` | → `hermes_plugins_system`, `hermes_built_in_plugins`, `term_hermes_plugin` | plugins repo ↔ plugin usage docs + concept term |
| `repo_hermes_agent_gateway_messaging.md` | → `hermes_event_hooks`, `hermes_plugin_hook_reference`, `term_gateway_hooks` | gateway repo ↔ hook docs + concept term |
| `repo_hermes_agent_agent_core.md` | → `hermes_kanban_multi_agent_board`, `hermes_kanban_worker_orchestrator` | agent-core (dispatcher/runs) ↔ kanban model/procedure |
| `repo_hermes_agent_cli.md` | → `hermes_kanban_dashboard_cli`, `hermes_plugins_management` | CLI repo ↔ kanban/plugins CLI docs |
| `repo_hermes_agent_tui_gateway.md` | → `hermes_kanban_dashboard_cli` | dashboard/gateway repo ↔ dashboard doc |
| `term_kanban.md` | → `term_kanban_multi_agent`, `hermes_kanban_multi_agent_board` | generic methodology → Hermes multi-agent variant + board doc |
| `term_plugin_sdk.md` | → `term_hermes_plugin`, `hermes_plugins_system` | adjacent SDK concept → Hermes plugin term + system doc |
| `term_plugin_manifest.md` | → `term_hermes_plugin` | component concept → Hermes plugin term |
| `term_observer_pattern.md` | → `term_gateway_hooks`, `hermes_event_hooks` | observer pattern → lifecycle-hook term + hooks doc |
| `term_multi_agent_systems.md` | → `term_kanban_multi_agent`, `hermes_kanban_worker_orchestrator` | concept → Hermes multi-agent board term + procedure |
| `entry_code_snippets_hermes_agent.md` | → `hermes_plugins_system`, `hermes_kanban_multi_agent_board`, `hermes_event_hooks` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 9 doc notes + 3 term notes | navigation hub |

Guarantees every new note (3 terms + 9 docs) in-degree ≥1 from outside the folder (G8). Inlink addition is a
gated execution phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Capture the 3 owned terms in Phase 0 FIRST (reindex + verify they exist) so digest notes link real targets.
Pilot Note 1 (`hermes_plugins_system`) → reindex → verify format/ghost/in-degree BEFORE authoring the rest.
Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before writing each note —
do NOT work from memory. Code blocks verbatim for kept blocks; curate code-heavy notes (5/6/7/8) to ≤6
load-bearing examples, summarize the rest in prose. If a note exceeds 350 lines during writing, STOP and split.
If multi-agent: agents return note content, master writes serially where there is write-contention; ≤30
agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP06b lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 9 doc + 3
  term rows to the master-created entry point; backfill the `repo_hermes_agent_*` / `term_*` inlinks (G8); run
  `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- Cross-link with SP06a (cron/delegation/goals/code-exec) once it lands — `term_delegate_task` ↔
  `term_kanban_multi_agent` (RPC vs work-queue contrast), `term_persistent_goal` ↔ `--goal` kanban cards,
  the `subagent_stop` hook ↔ delegation.
- Backfill the `config.yaml` plugin/hook/kanban settings cross-links from SP02's
  `hermes_security_skill_memory_settings` / `hermes_messaging_media_settings` (bidirectional config↔feature).
- Cross-link the dashboard doc with SP10 `hermes_web_dashboard` once it lands (dashboard-plugin contract).

## Augmentation Report

- Sections added/updated: Collision&Dedup Audit (2 LIKE different-concept confirmations by reading
  `term_plugin_sdk` + `term_kanban`; 3 owned-slug NEW verdicts), finalized Per-Note Mapping (four-floor: ≥8 term
  `cc_*.md`), Undigested Terms Plan + full Term-Note Authoring Requirements (3 owned captures), Density
  Re-Assessment (re-read confirmed), G5 ghost + G8 scripts, Inlinks.
- **Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  (snippets-as-bonus) state and the original ≥8 term / ≥8 snippet / ≥5 doc floor. All 9 notes' Per-Note Mapping
  blocks rebuilt against the four-floor standard: each keeps its relevant terms (≥8 with relevance clauses),
  its Code-Repos (≥5) drawn from the 13 `repo_hermes_agent_*` notes whose modules implement the documented
  surface, **promotes snippets from a bonus group to a COUNTED ≥10 floor (each now a full `snippet_hermes_agent_*`
  analogous `cc_*` agent-tool docs). Re-read all 5 source pages from `inbox/hermes_agent_docs/` to ground every
  relevance clause. Every term + code-repo + snippet ID, and every cited `cc_*` doc ID, re-verified DB-active
  2026-06-19; the 3 SP06b-owned terms + sibling `hermes_*` doc IDs resolve within this execution (Phase 0 /
  finalization per G5/G8).
- Density re-read: counts match measured (kanban 10308 / hooks 6903 / plugins 2802 / built-in 2589 /
  tutorial 2840); **no additional splits** beyond the planned 6 (plugins→2, hooks→2, kanban→3).
- Collision audit: **0 removals of doc notes**; 2 term-collision confirmations (`term_plugin_sdk`,
  `term_kanban` = LINK not dup, different concepts); 3 owned-slug renames recorded (general→specific);
  `term_observability` candidate removed (existing terms cover it).
- Term placeholder catch: **`term_state_machine` caught at finalization (DOES NOT exist)** — replaced inline
- Undigested terms surfaced at augment: **0 new** beyond the 3 owned (master inventory complete for SP06b).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs (four-floor
terms + 9 docs) ✓ Phase GATEs incl G5/G6/G8 ✓ Note Format Def
(derived) ✓ Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan
(3 owned) ✓ Capture Phase per term (Phase 0 each) ✓ best-fit glossary (developer ×2, workflows ×1) ✓
Term-Note Auth Reqs (full, multi-source mandate) ✓ invokes capture-term-note per term ✓ Entry-Point Decision
✓ matches size threshold ✓ Slug Specificity (3 renames general→specific) ✓ Slug Collision (2 LIKE
different-concept + 1 removed-candidate; re-ran pre-flight post-rename) ✓ dedup generalized to ALL notes incl
doc, searched term_dictionary AND documentation/ ✓ G8 in every phase + inlinks EXECUTED (Phase 3b) ✓ Doc-Note
Authoring Spec derived ✓).

## Review Sign-Off

**Independently re-reviewed 2026-06-19 (post four-floor re-augmentation) — READY FOR EXECUTION (9/9 checkpoints pass).** Supersedes the 2026-06-15 sign-off below; CP1 evaluated against the FOUR-FLOOR standard (≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note).

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP1 | Related Notes step (FOUR-FLOOR) | PASS | Programmatic count of all 9 notes' `## Per-Note Related Notes Mapping`: every note has ≥8 term (=8), ≥5 code-repo (=6 each), ≥10 snippet (N1=11, N2-9=10), ≥10 doc (=10) — 0 notes below any floor; 307 link entries, **0 bare links** (all carry `relevance:`). Anti-fabrication: full-population DB-verify — 30/30 existing term IDs active (3 owned `term_hermes_plugin`/`term_gateway_hooks`/`term_kanban_multi_agent` exempt Phase-0), 11/11 repo active, 63/63 snippet active, 36/36 `cc_*` doc active, 15 sibling `hermes_*` docs exempt. `term_state_machine` finalization-catch confirmed (DB MISSING → correctly replaced by active `term_event_driven_architecture` in N6). |
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | Phase 0 + 3 digest phases + Phase 3b, each with G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (9 doc + 3 term rows under a Plugins/Hooks/Kanban section); parent hub at master level; glossary updates named (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 9 doc notes + 3 term notes ≤30; master holds the corpus-level split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); spec minimum updated to four-floor (≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc); term spec lifted from capture-term-note canonical; not invented. |
| CP6 | Borderline density → split | PASS | plugins→2, hooks→2, kanban→3; all notes ≤2500w; code-heavy notes (5/6/7/8) curated ≤6; checked → cohesive single-BB clusters, KEEP justified. |
| CP7 | Source counts measured | PASS | Independently re-measured 2026-06-19 (body words after YAML strip; code=```÷2): plugins 2802/10, hooks 6903/62, kanban 10308/29, built-in-plugins 2589/9, kanban-tutorial 2840/12 — **measured == plan exactly (0 word delta on all 5)**. |
| CP8 | Undigested Terms + Authoring Reqs | PASS | SP06b owns 3 term captures (Phase 0); Undigested Terms Plan + full Term-Note Authoring Requirements present; multi-source mandate uses MUST-language; capture invokes `/tessellum-capture-term-note` per term. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit covers all 9 doc + 3 term slugs (term_dictionary AND documentation/); 2 LIKE different-concept confirmed (`term_plugin_sdk`, `term_kanban`, `term_plugin_manifest` all DB-active = LINK not dup); 3 specificity renames + Removed sub-table present; pre-flight re-run post-rename (no collision). |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 3 terms + 9 docs from repo_*/term_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION (re-reviewed 2026-06-19, four-floor CP1).**

---

**Prior sign-off — Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass)** (retained for history; CP1 then evaluated against the pre-four-floor mapping).

## Re-Sync Note (2026-06-19)

Mirror re-downloaded from NousResearch/hermes-agent `website/docs/` at main HEAD **c253b07** (was pinned
95715dc); inbox is byte-identical to upstream main. Re-measured all 5 owned pages with the ledger convention
(body words after stripping YAML frontmatter; code-block count = `^\s*```` lines ÷ 2).

- **user-guide/features/kanban.md — 10243w/29code -> 10308w/29code** (+65 words, code unchanged). My fresh
  measurement matches the manifest's NEW number exactly (no discrepancy).
- Unchanged pages spot-re-measured and confirmed stable: hooks.md 6903w/62code, plugins.md 2802w/10code,
  built-in-plugins.md 2589w/9code, kanban-tutorial.md 2840w/12code (all identical to the prior ledger).

**Density re-evaluation:** the +65-word growth on kanban.md was re-checked against the 3-way split (Notes 6/7/8
at ~2300/~2100/~2000w). The delta is immaterial — all three split notes remain well under the ≤2500w / ≤6 code /
≤400 line caps and each stays a single cohesive BB. **Outcome: no new split** (the planned plugins→2, hooks→2,
kanban→3 split set is unchanged). No planned-note filename, BB type, or gate was altered.

**Cross-ref floor (as of the 2026-06-19 re-sync, then RAISED twice that day):** the 2026-06-14 floor of ≥8 term
+ ≥8 snippet + ≥5 doc was preserved verbatim at re-sync, then superseded the same day by an interim ≥8 term +
≥5 code-repo + ≥10 doc (snippets-as-bonus) re-augmentation, and finally **levelled up the same day to the
FOUR-FLOOR standard: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note (all COUNTED, relevancy-selected,
requirement weakened (the change is purely additive: code-repos added, docs expanded, and snippets promoted
from a bonus group to a counted ≥10 floor). **Plan remains READY for execution.**

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented four-floor 2026-06-19) · Review: **DONE** (re-reviewed 2026-06-19, 9/9 READY, four-floor CP1; orig 2026-06-15 9/9) · Execute: pending · Re-synced 2026-06-19

**Source**: `inbox/hermes_agent_docs/user-guide/features/{plugins,built-in-plugins,hooks,kanban,kanban-tutorial}.md`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
