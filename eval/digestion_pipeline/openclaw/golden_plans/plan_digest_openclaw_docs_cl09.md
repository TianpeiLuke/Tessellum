---
title: Sub-Plan cl09 — OpenClaw Docs: CLI (wiki, workboard)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["cli/wiki", "cli/workboard"]
---

# Sub-Plan cl09: CLI

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_` prefix) / format / dedup / 9-GATE /
> cross-references / entry-point (`entry_openclaw_docs.md`) are all inherited from the master.

## Scope

The two tail CLI-reference pages for OpenClaw's bundled-plugin command surfaces: `openclaw wiki`
(the `memory-wiki` vault CLI — status, search, compile, lint, apply, bridge/Obsidian helpers) and
`openclaw workboard` (the Workboard plugin CLI — list/create/show cards and dispatch subagent
worker runs). Both are operator-facing terminal references provided by bundled plugins.
**Priority P1 (Phase A)** — these complete the CLI command-vocabulary surface (`cl01`–`cl09`) that
the gateway/automation/concepts sub-plans reference. Code-side counterparts (`repo_openclaw_memory`,
`repo_openclaw_skills`, `repo_openclaw_agents`) are LINKED, not recreated.

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| wiki | `cli/wiki` | 1,116 | 4 | 7 | 12 | procedure |
| workboard | `cli/workboard` | 1,165 | 13 | 9 | 3 | procedure (split: CLI usage vs dispatch mechanics) |

(Code = fence-pairs, i.e. ```` ``` ```` count ÷ 2: wiki 8/2=4, workboard 26/2=13.)

## Content Strategy

- **Prioritize**: the operator command flows that other docs reference — the `wiki` subcommand family
  (status/search/get/apply/compile/lint and the search modes) and the `workboard` card lifecycle
  (list/create/show) plus the `dispatch` mechanics (the conservative selection loop + Gateway-RPC vs
  data-only fallback), which is the load-bearing concept the Workboard plugin/automation docs lean on.
- **Split**: `workboard.md` → a CLI-usage procedure note (subcommands, flags, slash-command parity,
  permissions, troubleshooting) + a dispatch-mechanics note (the 7-step dispatch loop, conservative
  selection rules, claim/block/fallback behavior). The dispatch section is a distinct denser cluster
  that mixes a procedure with an event/loop model and would otherwise dominate the usage note.
- **Keep whole**: `wiki.md` (1,116w, single cohesive `openclaw wiki` command family, one procedure BB)
  → 1 note.
- **Link-out, do not redefine**: the Memory-Wiki plugin config model (`plugins/memory-wiki`, owned by
  the `pl04`/`pl14` plugin sub-plans), Memory Overview (`concepts/memory`, `co03`), `cli/memory`
  (`cl04`), `tools/slash-commands` (`to07`), `web/control-ui` (`wb01`), Workboard plugin
  (`plugins/workboard`, `pl22`/`pl25`) — referenced as sibling docs, never inlined. OKF (Open Knowledge
  Format) and bridge/`unsafe-local` modes are described in-note as `wiki` behavior, not as new terms.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_cli_wiki.md` | procedure | wiki.md: What it is for; Common commands; Commands (status, doctor, init, ingest, okf import, compile, lint, search, get, apply, bridge import, unsafe-local import, obsidian ...); Practical usage guidance; Configuration tie-ins; Related | 700 | The `openclaw wiki` CLI for the bundled memory-wiki vault: inspect/init/ingest/OKF-import content, compile indexes + digests, lint for contradictions/staleness, search (modes + corpus/backend) and read pages, apply narrow mutations, bridge-import memory artifacts, and Obsidian helpers — plus the memory-wiki config keys that shape behavior. |
| 2 | `oc_cli_workboard.md` | procedure | workboard.md: intro + enable; Usage; `list`; `create`; `show`; Slash Command Parity; Permissions; Troubleshooting (No Cards Appear, Dispatch Says Data-Only, Dispatch Starts Nothing) | 650 | The `openclaw workboard` CLI for the bundled Workboard plugin: enable the plugin, list/create/show cards against the plugin-owned SQLite state, the per-subcommand flags, slash-command parity and required operator scopes, and the read/write permission model — with the three common troubleshooting paths. |
| 3 | `oc_cli_workboard_dispatch.md` | procedure | workboard.md: `dispatch` (Gateway RPC `workboard.cards.dispatch`, the 7-step dispatch loop, conservative selection, claim/block-on-failure, data-only fallback, text/JSON output) | 550 | How `openclaw workboard dispatch` turns ready cards into subagent worker runs: the Gateway-RPC path and its 7-step loop (promote → block-expired → record → select → claim → start worker → store linkage), the conservative one-pass selection limits, claimed-card block-on-failure, and the data-only local fallback when no live Gateway is reachable. |

## Section Coverage Map

```
cli/wiki.md
├── (intro: "Inspect and maintain the memory-wiki vault" + Related links) → note 1 (oc_cli_wiki) Overview
├── ## What it is for ─────────────────────────────────── → note 1
├── ## Common commands ───────────────────────────────── → note 1
├── ## Commands
│   ├── ### wiki status ──────────────────────────────── → note 1
│   ├── ### wiki doctor ──────────────────────────────── → note 1
│   ├── ### wiki init ────────────────────────────────── → note 1
│   ├── ### wiki ingest <path-or-url> ────────────────── → note 1
│   ├── ### wiki okf import <path> ───────────────────── → note 1
│   ├── ### wiki compile ─────────────────────────────── → note 1
│   ├── ### wiki lint ────────────────────────────────── → note 1
│   ├── ### wiki search <query> ──────────────────────── → note 1
│   ├── ### wiki get <lookup> ────────────────────────── → note 1
│   ├── ### wiki apply ───────────────────────────────── → note 1
│   ├── ### wiki bridge import ───────────────────────── → note 1
│   ├── ### wiki unsafe-local import ─────────────────── → note 1
│   └── ### wiki obsidian ... ────────────────────────── → note 1
├── ## Practical usage guidance ──────────────────────── → note 1
├── ## Configuration tie-ins ─────────────────────────── → note 1
└── ## Related ───────────────────────────────────────── → note 1 References / Related Notes

cli/workboard.md
├── (intro + "Enable the plugin before using" snippet) ── → note 2 (oc_cli_workboard) Overview
├── ## Usage (synopsis block) ────────────────────────── → note 2
├── ## list ──────────────────────────────────────────── → note 2
├── ## create ────────────────────────────────────────── → note 2
├── ## show ──────────────────────────────────────────── → note 2
├── ## dispatch ──────────────────────────────────────── → note 3 (oc_cli_workboard_dispatch)
│     (RPC method, 7-step loop, selection limits, block-on-fail, data-only fallback, output)
├── ## Slash Command Parity ──────────────────────────── → note 2
├── ## Permissions ───────────────────────────────────── → note 2 (dispatch scopes cross-ref'd in note 3)
├── ## Troubleshooting
│   ├── ### No Cards Appear ──────────────────────────── → note 2
│   ├── ### Dispatch Says Data-Only ──────────────────── → note 2 (links note 3 for fallback meaning)
│   └── ### Dispatch Starts Nothing ──────────────────── → note 2 (links note 3 for selection rules)
└── ## Related ───────────────────────────────────────── → notes 2 + 3 References / Related Notes
```

No orphaned sections. Every H2/H3 of both pages maps to exactly one planned note. The Memory-Wiki
plugin config model, `concepts/memory`, `cli/memory`, `tools/slash-commands`, `web/control-ui`, and the
Workboard plugin page are link-outs (owned by other sub-plans), not duplicated here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| `workboard.md` (1,165w, 9 H2 / 3 H3, 13 fences) | notes 2 + 3 | Under the 2,500w cap, but the `## dispatch` section is a distinct, dense cluster: the Gateway-RPC `workboard.cards.dispatch` call, a 7-step loop, conservative one-pass selection limits, claim/block-on-failure, and the data-only fallback — a "how dispatch works" model mixed with a usage procedure. Splitting keeps the card-lifecycle usage note (list/create/show/permissions/troubleshooting) focused and gives the dispatch mechanics its own atomic note, matching the master's 3-note allotment for cl09. |
| `wiki.md` (1,116w, 7 H2 / 12 H3) | note 1 (no split) | Single cohesive `openclaw wiki` subcommand family, one procedure BB, under the word/code caps; splitting would fragment one command reference. |

## Summary Statistics & Building Block Distribution

- Source pages: **2** (`cli/wiki` 1,116w + `cli/workboard` 1,165w = **2,281 measured words**).
- New `oc_` notes: **3** (`oc_cli_wiki`, `oc_cli_workboard`, `oc_cli_workboard_dispatch`).
- New `term_dictionary` notes: **0** (OpenClaw CLI vocab is digested as `oc_` doc content; existing terms linked).
- BB distribution: procedure ×3 (all three notes are CLI/operational references).
- Est. digest words: ~1,900 (avg ~630/note). Source has 17 code fences total (4 wiki + 13 workboard);
  each note keeps ≤6 (reproduce the synopsis/example blocks selectively, verbatim).
- Cross-refs (LOCKED at xref-augment 2026-06-21, raised floors): each note carries ≥8 relevancy-selected
  toward the floor) PLUS relevant `repo_openclaw*`. Per-note counts: `oc_cli_wiki` 9t·11s·11d,

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


false-positives discarded). Relative paths are FROM a note at `resources/documentation/openclaw/oc_X.md`:
terms `../../term_dictionary/term_Y.md`; sibling oc docs `oc_Y.md`; other docs `../<folder>/<file>.md`;
repos `../../../areas/code_repos/repo_Y.md`; snippets `../../code_snippets/snippet_Y.md`; entry points
the 10-doc floor. MISSING terms (`term_obsidian`, `term_slash_command`, `term_session`, `term_skill`,
`term_plugin`, `term_active_memory`, `term_okf`) are NOT cited — re-verified MISSING 2026-06-21.

### oc_cli_wiki (9t · 11s · 11d)

Source: the `openclaw wiki` CLI for the bundled memory-wiki vault (status/doctor/init/ingest/OKF
import/compile/lint/search/get/apply/bridge import/unsafe-local import/obsidian helpers + config tie-ins).

**Terms** (9)
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the self-hosted OpenClaw gateway; relevance: `openclaw wiki` is a bundled subcommand of this gateway and its bridge mode routes through the running Gateway.
- [term_knowledge_graph](../../term_dictionary/term_knowledge_graph.md) — a linked graph of entities/claims with provenance; relevance: the memory-wiki vault IS a compiled, linked knowledge store with provenance-rich syntheses, contradiction and freshness reports.
- [term_markdown](../../term_dictionary/term_markdown.md) — lightweight markup with frontmatter; relevance: wiki pages are markdown with provenance frontmatter and `wiki okf import` reads every non-reserved `.md` concept doc.
- [term_zettelkasten](../../term_dictionary/term_zettelkasten.md) — linked atomic note method; relevance: a vault of linked synthesis/source/concept pages with `wiki obsidian` helpers is a Zettelkasten-style note system.
- [term_information_retrieval](../../term_dictionary/term_information_retrieval.md) — ranked search over a corpus; relevance: `wiki search` is the retrieval surface, ranking pages/claims by backend/corpus/mode with `Claim:`/`Evidence:` output.
- [term_hybrid_search](../../term_dictionary/term_hybrid_search.md) — combined lexical + semantic retrieval; relevance: `search.backend` (`shared`/`local`) over `search.corpus` (`wiki`/`memory`/`all`) blends surfaces hybrid-search style.
- [term_rag](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: provenance-rich syntheses plus the compiled `agent-digest.json` feed retrieval-augmented agent context (`context.includeCompiledDigestPrompt`).
- [term_rpc](../../term_dictionary/term_rpc.md) — remote procedure call; relevance: in bridge mode `wiki status`/`doctor`/`bridge import` query the running Gateway over RPC for the runtime memory-plugin context.
- [term_agentic_memory](../../term_dictionary/term_agentic_memory.md) — persistent agent memory store; relevance: `wiki bridge import` pulls public memory artifacts from the active memory plugin into the wiki vault so wiki sees the same agent memory context.

- [hermes_persistent_memory](../hermes_agent/hermes_persistent_memory.md) — Hermes persistent memory subsystem; relevance: the closest coding-agent analog of a compiled, persistent knowledge vault the agent reads/writes.
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — catalog of pluggable memory backends; relevance: memory-wiki is one bundled memory/knowledge provider in the same family.
- [hermes_memory_provider_plugin](../hermes_agent/hermes_memory_provider_plugin.md) — the memory-provider plugin contract; relevance: parallels the bundled `memory-wiki` plugin that provides `openclaw wiki` and its config keys.
- [hermes_memory_providers_honcho](../hermes_agent/hermes_memory_providers_honcho.md) — a concrete external memory provider; relevance: another compiled/searchable memory backend, contrasting wiki's vault model.
- [cc_memory_overview](../claude_code/cc_memory_overview.md) — Claude Code memory model; relevance: cross-tool comparison of how a coding agent persists and recalls knowledge.
- [cc_auto_memory](../claude_code/cc_auto_memory.md) — automatic memory capture/compile; relevance: analog of `wiki ingest`/`wiki compile` auto-compile-after-ingest behavior.
- [cc_claude_md_files](../claude_code/cc_claude_md_files.md) — markdown knowledge files an agent reads; relevance: same pattern as wiki concept/source pages being plain markdown with frontmatter.
- [band_agent_api_memories](../band/band_agent_api_memories.md) — agent memory API; relevance: programmatic memory read/write analog to `wiki get`/`wiki apply`.
- [hermes_cli_commands_session_ops](../hermes_agent/hermes_cli_commands_session_ops.md) — Hermes CLI command reference; relevance: same `agent <subcommand>` CLI shape and operator-facing terminal reference style.
- [cc_cli_commands](../claude_code/cc_cli_commands.md) — Claude Code CLI command reference; relevance: cross-tool precedent for the CLI-reference note format this note follows.
- [oc_cli_workboard](oc_cli_workboard.md) — (planned, this series) sibling bundled-plugin CLI reference; relevance: same `openclaw <plugin>` command pattern as `openclaw wiki`.

**Repos** (3)
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — code-side memory/wiki engine; relevance: backs this CLI (vault compile, embeddings, on-disk schema for claims/digests).
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills/knowledge surfaces; relevance: knowledge/skill content adjacent to the memory-wiki vault.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella OpenClaw repo; relevance: hosts CLI entrypoints and the bundled `memory-wiki` plugin.

- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — the memory/wiki engine; relevance: the engine `wiki compile`/`search` drive.
- [snippet_openclaw_memory_host_memory_schema](../../code_snippets/snippet_openclaw_memory_host_memory_schema.md) — on-disk schema; relevance: the layout for compiled wiki artifacts/claims (`claims.jsonl`, digest cache).
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding inputs; relevance: powers `wiki search` ranking and corpus selection.
- [snippet_openclaw_memory_runtime](../../code_snippets/snippet_openclaw_memory_runtime.md) — memory runtime wiring; relevance: the runtime context bridge-mode `wiki` commands query via the Gateway.
- [snippet_openclaw_memory_root_files](../../code_snippets/snippet_openclaw_memory_root_files.md) — root vault layout; relevance: `wiki init` creates this root structure and indexes.
- [snippet_openclaw_memory_host_internal_walker](../../code_snippets/snippet_openclaw_memory_host_internal_walker.md) — vault file walker; relevance: how `wiki ingest`/`okf import` traverse and read `.md` source/concept files.
- [snippet_openclaw_memory_host_session_files_classify](../../code_snippets/snippet_openclaw_memory_host_session_files_classify.md) — classifies ingested files; relevance: import-time classification of source vs concept pages.
- [snippet_openclaw_memory_host_session_files_text](../../code_snippets/snippet_openclaw_memory_host_session_files_text.md) — extracts page text; relevance: text extraction feeding compile/search indexing.
- [snippet_openclaw_sessions_input_provenance](../../code_snippets/snippet_openclaw_sessions_input_provenance.md) — input provenance tracking; relevance: the provenance frontmatter `wiki ingest` preserves on imported pages.

### oc_cli_workboard (8t · 11s · 11d)

Source: the `openclaw workboard` CLI — enable + list/create/show cards on plugin-owned SQLite state,
flags, slash-command parity, permission scopes, troubleshooting.

**Terms** (8)
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway/CLI; relevance: `openclaw workboard` is a bundled subcommand and `--dev`/`--profile` select its state root.
- [term_subagent](../../term_dictionary/term_subagent.md) — a spawned worker agent; relevance: Workboard cards are the inputs that dispatch turns into subagent worker runs (mechanics in note 3).
- [term_kanban_multi_agent](../../term_dictionary/term_kanban_multi_agent.md) — a multi-agent kanban board; relevance: Workboard IS a card/board surface for routing work to agents — the direct conceptual match.
- [term_agent_orchestration](../../term_dictionary/term_agent_orchestration.md) — coordinating multiple agents over a work queue; relevance: the board orchestrates which cards go to which agent.
- [term_orchestration](../../term_dictionary/term_orchestration.md) — general work coordination; relevance: list/create/show plus dispatch form a work-orchestration surface over plugin SQLite state.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — invocable command surface; relevance: `/workboard …` slash commands and Workboard agent tools are agent-invocable command surfaces.
- [term_access_control](../../term_dictionary/term_access_control.md) — permission scoping; relevance: read vs mutating commands require owner status or `operator.read`/`operator.write`/`operator.admin` scopes.
- [term_rpc](../../term_dictionary/term_rpc.md) — remote procedure call; relevance: the dispatch path calls Gateway RPC, and read-only Gateway tokens are restricted from mutations.

- [hermes_kanban_dashboard_cli](../hermes_agent/hermes_kanban_dashboard_cli.md) — the kanban dashboard + CLI in the sibling ecosystem; relevance: the closest analog — a card-board CLI plus dashboard over shared state.
- [hermes_kanban_multi_agent_board](../hermes_agent/hermes_kanban_multi_agent_board.md) — multi-agent kanban board model; relevance: the board/card lifecycle Workboard mirrors (status, priority, agent assignment).
- [hermes_kanban_tutorial_walkthrough](../hermes_agent/hermes_kanban_tutorial_walkthrough.md) — end-to-end kanban usage; relevance: parallels the list/create/show operator flow this note documents.
- [hermes_subagent_delegation](../hermes_agent/hermes_subagent_delegation.md) — delegating work to subagents; relevance: cards delegated to an `--agent` become subagent work.
- [hermes_slash_commands_messaging](../hermes_agent/hermes_slash_commands_messaging.md) — slash commands on chat surfaces; relevance: the Slash Command Parity section (`/workboard list/show/create/dispatch`) on command-capable channels.
- [hermes_security_command_approval](../hermes_agent/hermes_security_command_approval.md) — command approval / authorization; relevance: the owner-status and operator-scope gating for mutating Workboard commands.
- [cc_managed_permission_settings_and_precedence](../claude_code/cc_managed_permission_settings_and_precedence.md) — permission model and precedence; relevance: cross-tool analog of read-vs-write scope gating.
- [cc_cli_commands](../claude_code/cc_cli_commands.md) — Claude Code CLI command reference; relevance: precedent for the subcommand/flag CLI-reference format.
- [hermes_cli_commands_session_ops](../hermes_agent/hermes_cli_commands_session_ops.md) — Hermes CLI command reference; relevance: same operator-facing terminal command-reference shape.
- [oc_cli_workboard_dispatch](oc_cli_workboard_dispatch.md) — (planned, this series) the dispatch mechanics; relevance: this note's troubleshooting (Data-Only, Starts Nothing) points to it.
- [oc_cli_wiki](oc_cli_wiki.md) — (planned, this series) sibling bundled-plugin CLI; relevance: same `openclaw <plugin>` enable-then-use pattern.

**Repos** (3)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: owns the assigned-agent scoping a card's `--agent` references.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella repo; relevance: hosts the bundled Workboard plugin and CLI route.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions store; relevance: session keys link dispatched worker runs back to cards.

- [snippet_hermes_agent_cli_kanban_commands](../../code_snippets/snippet_hermes_agent_cli_kanban_commands.md) — kanban CLI command set; relevance: the closest analog of the `workboard` subcommand surface.
- [snippet_hermes_agent_cli_kanban_crud](../../code_snippets/snippet_hermes_agent_cli_kanban_crud.md) — card create/read/update CLI; relevance: maps to `workboard create`/`show` writes against SQLite state.
- [snippet_hermes_agent_cli_kanban_query](../../code_snippets/snippet_hermes_agent_cli_kanban_query.md) — card list/query CLI; relevance: maps to `workboard list --board/--status/--json`.
- [snippet_hermes_agent_cli_kanban_diagnostics](../../code_snippets/snippet_hermes_agent_cli_kanban_diagnostics.md) — kanban CLI diagnostics; relevance: analog of the No-Cards-Appear / plugin-inspect troubleshooting.
- [snippet_hermes_agent_tools_kanban_mutate](../../code_snippets/snippet_hermes_agent_tools_kanban_mutate.md) — card-mutating agent tool; relevance: the tool-side write path that mutations and slash-create share with the CLI.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — OpenClaw CLI command routing; relevance: how `openclaw workboard <sub>` is parsed and routed to the plugin.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — plugin runtime load; relevance: `openclaw plugins enable workboard` + `gateway restart` loads the plugin runtime.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — RPC method scope gating; relevance: the `operator.read`/`operator.write` gating of Workboard read vs mutate methods.
- [snippet_hermes_agent_skills_devops_kanban_orchestrator](../../code_snippets/snippet_hermes_agent_skills_devops_kanban_orchestrator.md) — kanban orchestrator; relevance: the board-orchestration role Workboard plays over its cards.
- [snippet_hermes_agent_skills_devops_kanban_worker](../../code_snippets/snippet_hermes_agent_skills_devops_kanban_worker.md) — kanban worker; relevance: the worker side that consumes a claimed card.

### oc_cli_workboard_dispatch (9t · 12s · 11d)

Source: `openclaw workboard dispatch` — Gateway-RPC `workboard.cards.dispatch`, the 7-step dispatch
loop, conservative selection limits, claim/block-on-failure, data-only fallback, text/JSON output.

**Terms** (9)
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway runtime; relevance: hosts the `workboard.cards.dispatch` RPC and the subagent runtime dispatch uses.
- [term_subagent](../../term_dictionary/term_subagent.md) — a spawned worker agent; relevance: dispatch starts subagent worker runs with agent-scoped or unscoped session keys.
- [term_orchestration](../../term_dictionary/term_orchestration.md) — work coordination/scheduling; relevance: the 7-step promote→block→record→select→claim→start→store loop IS a work scheduler.
- [term_agent_orchestration](../../term_dictionary/term_agent_orchestration.md) — multi-agent work coordination; relevance: dispatch routes ready cards to per-owner/per-agent worker runs, one card per owner per pass.
- [term_rpc](../../term_dictionary/term_rpc.md) — remote procedure call; relevance: dispatch first calls Gateway RPC `workboard.cards.dispatch`; data-only is the no-Gateway fallback.
- [term_dag](../../term_dictionary/term_dag.md) — directed acyclic dependency graph; relevance: "promote dependency-ready children to ready" is dependency-DAG traversal over cards.
- [term_access_control](../../term_dictionary/term_access_control.md) — permission scoping; relevance: dispatch needs `operator.read` + `operator.write`; auth/permission failures for explicit `--url`/`--token` targets are surfaced.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — invocable command/tool surface; relevance: bounded card context plus the claim token are passed into the worker-run invocation.
- [term_circuit_breaker](../../term_dictionary/term_circuit_breaker.md) — fail-fast / block-on-failure pattern; relevance: a claimed card whose worker start fails is blocked (claim cleared, failure recorded) instead of silently re-queued.

- [hermes_kanban_worker_orchestrator](../hermes_agent/hermes_kanban_worker_orchestrator.md) — worker-orchestrator that turns cards into runs; relevance: the direct analog of the dispatch loop (select, claim, start workers).
- [hermes_kanban_worker_lanes](../hermes_agent/hermes_kanban_worker_lanes.md) — bounded concurrent worker lanes; relevance: parallels the conservative one-pass selection limits (at most three workers, one per owner).
- [hermes_kanban_multi_agent_board](../hermes_agent/hermes_kanban_multi_agent_board.md) — multi-agent board model; relevance: the assigned-agent vs unassigned card scoping dispatch keys on.
- [hermes_subagent_delegation](../hermes_agent/hermes_subagent_delegation.md) — delegating to subagents; relevance: dispatch is the delegation step (card → subagent worker run with session key).
- [hermes_guide_delegation_patterns](../hermes_agent/hermes_guide_delegation_patterns.md) — delegation patterns guide; relevance: the conservative selection + claim/block patterns dispatch implements.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway operations; relevance: dispatch routes through the running Gateway and falls back to data-only when it is unavailable.
- [cc_dispatch_background_agents](../claude_code/cc_dispatch_background_agents.md) — dispatching background agents; relevance: cross-tool analog of turning queued work into tracked background worker runs.
- [cc_run_agents_in_parallel](../claude_code/cc_run_agents_in_parallel.md) — running agents in parallel; relevance: analog of the bounded multi-worker fan-out per dispatch pass.
- [cc_work_with_subagents](../claude_code/cc_work_with_subagents.md) — working with subagents; relevance: the subagent worker-run model dispatch produces.
- [band_acp_server](../band/band_acp_server.md) — ACP server / agent invocation surface; relevance: cross-ecosystem analog of an RPC-invoked agent dispatch path.
- [oc_cli_workboard](oc_cli_workboard.md) — (planned, this series) card-lifecycle CLI; relevance: this dispatch note continues the workboard CLI it covers.

**Repos** (3)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: exposes `workboard.cards.dispatch` RPC and the task ledger dispatch records into.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions store; relevance: holds the session-key linkage and worker-run/task linkage dispatch stores on cards.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: provides the agent-scoped vs unscoped subagent session keys dispatch chooses.

- [snippet_hermes_agent_cli_gateway_dispatch](../../code_snippets/snippet_hermes_agent_cli_gateway_dispatch.md) — CLI→Gateway dispatch path; relevance: the closest analog of the `dispatch` RPC-call-then-fallback path.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — RPC scope gating; relevance: the `operator.read`/`operator.write` gating dispatch requires on the RPC call.
- [snippet_openclaw_gateway_server_startup_post_attach_runtime](../../code_snippets/snippet_openclaw_gateway_server_startup_post_attach_runtime.md) — gateway runtime attach; relevance: the running-Gateway runtime dispatch needs (absent it → data-only fallback).
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — subagent spawn policy; relevance: the agent-scoped vs unscoped session-key decision when starting a card's worker.
- [snippet_openclaw_agents_subagent_registry_lifecycle](../../code_snippets/snippet_openclaw_agents_subagent_registry_lifecycle.md) — subagent lifecycle/registry; relevance: tracking started worker runs and timed-out runs (step 2 block-expired).
- [snippet_hermes_agent_gw_runner_supervisor](../../code_snippets/snippet_hermes_agent_gw_runner_supervisor.md) — worker-run supervisor; relevance: supervises started worker runs analogous to dispatch's worker-start + status recording.
- [snippet_hermes_agent_gw_runner_errors](../../code_snippets/snippet_hermes_agent_gw_runner_errors.md) — worker-run error handling; relevance: block-on-failure (clear claim, record failure) when worker start fails.
- [snippet_hermes_agent_gw_runner_acl](../../code_snippets/snippet_hermes_agent_gw_runner_acl.md) — runner ACL/scope checks; relevance: the operator-scope/auth checks before dispatch starts work.
- [snippet_hermes_agent_skills_devops_kanban_worker](../../code_snippets/snippet_hermes_agent_skills_devops_kanban_worker.md) — kanban worker; relevance: the worker that consumes a claimed card with bounded context + claim token.

> `term_session`, `term_skill`, `term_plugin`, `term_active_memory`, `term_okf`) NOT cited; if any becomes
> genuinely cross-cutting and reusable it is handled in the Undigested Terms Plan, not invented here. All

## Undigested Terms Plan

Per master: OpenClaw CLI vocabulary is digested as `oc_` doc content (these notes ARE the home for
`openclaw wiki`/`openclaw workboard` terminology), and existing `term_dictionary` terms are linked, not
redefined. Expected **0 new `term_dictionary` captures**.

| Term | Disposition |
|---|---|
| `openclaw wiki` / `wiki status/doctor/init/ingest/compile/lint/search/get/apply/bridge import` | OpenClaw CLI vocab → digested IN `oc_cli_wiki.md` (this note is its home). No term note. |
| `memory-wiki` (bundled plugin / vault) | Plugin/product vocab → described in `oc_cli_wiki`; full config model link-out to `plugins/memory-wiki` (`pl04`/`pl14`). Link `term_knowledge_graph`. No new term. |
| OKF / Open Knowledge Format | Import-format detail → described in `oc_cli_wiki` (`wiki okf import` behavior). Not vault-reusable beyond OpenClaw docs; no term note. If it recurs cross-corpus at augment, candidate `acronym_glossary_data_formats.md` (deferred, not now). |
| bridge mode / `unsafe-local` mode | `wiki` config-mode vocab → described in `oc_cli_wiki`. Link `term_rpc` (bridge routes through Gateway RPC). No new term. |
| search modes (`find-person`, `route-question`, `source-evidence`, `raw-claim`) | `wiki search` flag vocab → enumerated in `oc_cli_wiki`. Link `term_information_retrieval`. No new term. |
| `openclaw workboard` / `list/create/show/dispatch`, card, board, status, priority, labels | OpenClaw CLI vocab → digested IN `oc_cli_workboard.md` / `oc_cli_workboard_dispatch.md`. No term note. |
| Workboard (bundled plugin) | Plugin/product vocab → described in `oc_cli_workboard`; full model link-out to `plugins/workboard` (`pl22`/`pl25`). No new term. |
| dispatch loop / claim token / worker run / subagent worker | Mechanics vocab → digested IN `oc_cli_workboard_dispatch.md`. Link existing `term_subagent`, `term_orchestration`. No new term. |
| `workboard.cards.dispatch` (Gateway RPC method) | RPC method name → described in `oc_cli_workboard_dispatch`. Link `term_rpc`. No new term. |
| `operator.read` / `operator.write` / `operator.admin` (scopes) | Permission vocab → described in `oc_cli_workboard` / `_dispatch`. Link `term_access_control`. No new term. |
| slash-command parity (`/workboard …`, `/workboard create/dispatch`) | Cross-surface vocab → described in `oc_cli_workboard`; link-out `tools/slash-commands` (`to07`). Link `term_function_calling`. No new term. |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term lacking an existing note
and lacking a doc-page home was found in these two pages.

## Term-Note Authoring Requirements

**N/A (0 new terms.)** This sub-plan creates no `term_dictionary` notes. (Inherited requirement, master
W5: were any new term proposed, it would be captured via `/tessellum-capture-term-note` with multi-source
research and added to its best-fit `acronym_glossary_*.md`; not applicable here.)

## Per-Phase Validation Gate (G1–G9)

Single execution phase (3 notes). Inherited 9-GATE per master.

| Gate | Check | Tooling / Pass criterion |
|---|---|---|
| G1 | Format + YAML | `/tessellum-check-note-format` + `python3 scripts/check_yaml_frontmatter.py` — fixed field order; first 3 tags `resource`/`documentation`/`openclaw`; `building_block: procedure`; `source_url` present; no forbidden fields; required `## Overview` + `## Related Notes`. |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/cli/<page>.md` — every claim traceable to source; no invented flags/behavior. |
| G3 | Density + Coverage | ≤400 lines / ≤2,500 words / ≤6 code blocks per note; every H2/H3 from the Section Coverage Map present; one BB per note. |
| G4 | Cross-Reference | Each note's `## Related Notes` has ≥6 relevancy-selected `term_dictionary` links + sibling `oc_*` + `repo_openclaw*` + entry hub, each with a relevance statement, indexed `[text](path.md)` format. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` — relative paths resolve; 0 broken links after reindex. |
| G7 | Discoverability (in-degree ≥1) | Each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (via `entry_openclaw_docs.md` + see Inlinks); `note_links` confirms in_degree ≥1. |
| G8 | Anti-island | No new note is an island; entry-hub rows + inlinks added before commit; verified in DB. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
# Run from repo root /path/to/vault
GATE_DIR="resources/documentation/openclaw"
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_cli_wiki oc_cli_workboard oc_cli_workboard_dispatch"

# G1 — format + YAML frontmatter
for n in ${=NOTES}; do
  python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR/$n.md"
done
python3 scripts/check_note_format.py --path "$GATE_DIR"   # or /tessellum-check-note-format

# G1/G3 — required sections present + source_url present + density caps
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  echo "== $f =="
  grep -Eq "$REQ_SECTIONS" "$f" || echo "  MISSING required section"
  if [ "$REQUIRE_SOURCE_URL" = "1" ]; then grep -q '^source_url:' "$f" || echo "  MISSING source_url"; fi
  wc -l "$f"; wc -w "$f"
  fences=$(grep -c '```' "$f"); echo "  code_fences/2 = $((fences/2))  (cap 6)"
done

# G4 — Related Notes references a sibling oc_ note + a repo_openclaw + a term_
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  grep -q "($SIBLING_PREFIX" "$f" || echo "$f: no sibling oc_ link"
  grep -q "repo_openclaw" "$f"    || echo "$f: no repo_openclaw link"
  grep -q "term_"          "$f"   || echo "$f: no term_ link"
done

# G5/G6 — reindex then ghost + broken-link sweep
bash scripts/update_notes_database.sh --force
# /tessellum-fix-ghost-references   (G5)
# /tessellum-fix-broken-links       (G6)

# G7/G8 — discoverability: each new note has in_degree >= 1 from outside the folder
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
done
```

## Density Re-Assessment

| Note | Source words | Est. words | Est. lines | Code blocks (≤6) | Within caps? |
|---|---:|---:|---:|---:|---|
| oc_cli_wiki | 1,116 | ~700 | ~230 | ≤4 (Common commands + okf/get/search examples, selective) | yes |
| oc_cli_workboard | (workboard 1,165, usage share) | ~650 | ~210 | ≤6 (Usage synopsis + list/create/show + slash + troubleshooting cmds) | yes |
| oc_cli_workboard_dispatch | (workboard 1,165, dispatch share) | ~550 | ~180 | ≤4 (dispatch examples + text/fallback output) | yes |

All three comfortably under ≤400 lines / ≤2,500 words / ≤6 code blocks. No note is borderline-overlong;
no further split warranted. (workboard's 13 fences are distributed across notes 2+3, each kept ≤6.)

## Entry Point Decision (inherited from master)

No standalone entry point for this 3-note sub-plan. These notes contribute their rows to the
series-level hub **`0_entry_points/entry_openclaw_docs.md`** (created as a master pre-step, W1, before the
first sub-plan executes; >30-note series threshold met at the corpus level). Rows to add under the CLI
section of that hub:

| Note | Section | One-line |
|---|---|---|
| `oc_cli_wiki` | CLI | `openclaw wiki` — memory-wiki vault CLI (status/search/compile/lint/apply/bridge/obsidian). |
| `oc_cli_workboard` | CLI | `openclaw workboard` — list/create/show cards + slash parity + permissions. |
| `oc_cli_workboard_dispatch` | CLI | `openclaw workboard dispatch` — Gateway-RPC dispatch loop + data-only fallback. |

## Inlinks (existing notes → new notes)

Candidate OUTSIDE-folder inbound links to satisfy G7/G8 (each new note must RECEIVE ≥1). All targets

| New note | Candidate inbound source(s) (outside documentation/openclaw/) | Link rationale |
|---|---|---|
| `oc_cli_wiki` | `0_entry_points/entry_openclaw_docs.md` (W1 hub); `areas/code_repos/repo_openclaw_memory.md`; `resources/term_dictionary/term_openclaw.md` (W3 docs back-link) | hub row; code↔docs cross-link from the memory engine that backs `openclaw wiki`. |
| `oc_cli_workboard` | `0_entry_points/entry_openclaw_docs.md`; `areas/code_repos/repo_openclaw_agents.md`; `resources/term_dictionary/term_subagent.md` | hub row; agent-runtime repo + subagent term naturally reference the card→worker CLI. |
| `oc_cli_workboard_dispatch` | `0_entry_points/entry_openclaw_docs.md`; `areas/code_repos/repo_openclaw_gateway.md`; `areas/code_repos/repo_openclaw_sessions.md` | hub row; Gateway repo exposes the dispatch RPC; sessions repo holds the worker-run/session-key linkage. |

Primary guarantee is via `entry_openclaw_docs.md` (every new note gets a hub row). Repo/term inbound
links are added during execution (use `/tessellum-add-inlinks` if the hub link alone is insufficient),
then verified in `note_links` (in_degree ≥1) before commit.

## Pacing Rules (inherited from master)

Cap dynamic-workflow fan-out at ~30 agents/run; embed manifests in the script; `git pull --rebase
--autostash origin main` before committing; no Claude co-author trailer; commit per sub-plan / per wave;
reindex incrementally per wave; verify `note_links` + 0 broken links before commit; push after each
commit. This sub-plan is small (3 notes, single wave).

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | 🟢 DONE (this file) |
| 2. Augment | `/tessellum-augment-digestion-plan` | 🟢 DONE (xref-augment 2026-06-21 — see Augmentation Report) |
| 3. Review | `/tessellum-review-digestion-plan` | 🟢 DONE — READY (9/9 CP pass, see Review Sign-Off) |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending |

## Augmentation Report (2026-06-21)



**Per-note counts (floors met).**

| Note | Terms | Snippets | Docs (existing + planned-sibling) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| `oc_cli_wiki` | 9 | 11 | 11 (10 existing + 1 planned) | 3 | ✅ ≥8t · ≥10s · ≥10d |
| `oc_cli_workboard` | 8 | 11 | 11 (9 existing + 2 planned) | 3 | ✅ ≥8t · ≥10s · ≥10d |
| `oc_cli_workboard_dispatch` | 9 | 12 | 11 (10 existing + 1 planned) | 3 | ✅ ≥8t · ≥10s · ≥10d |

**New-term candidates + best-fit glossary.** None. Both pages are pure OpenClaw CLI vocabulary, which the master's corpus-wide design routes to `oc_*` documentation concept notes (these three notes ARE the home for `openclaw wiki` / `openclaw workboard` terminology), with existing `term_dictionary` terms linked, not redefined. The re-read surfaced no genuinely cross-cutting, vault-reusable term lacking BOTH an existing note AND a doc-page home. The seven MISSING terms checked (`term_obsidian`, `term_slash_command`, `term_session`, `term_skill`, `term_plugin`, `term_active_memory`, `term_okf`) are each either (a) owned by another sub-plan's doc page, or (b) not vault-reusable beyond OpenClaw docs (OKF/`unsafe-local`); none is captured here. If `term_okf` (Open Knowledge Format) recurs cross-corpus in later sub-plans, best-fit glossary would be `acronym_glossary_data_formats.md` (deferred, not now) — recorded in the Undigested Terms Plan, not invented.

**Issues.** None blocking. (`entry_openclaw_docs.md` is intentionally not in the per-note Related lists — it is the W1 master pre-step hub referenced in the Inlinks + Entry Point Decision sections; it provides the G7/G8 inbound link at execution.)

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review of `plan_digest_openclaw_docs_cl09.md` (status: pending) after the xref-augment pass. CP7 spot-check re-read both source pages (measured wiki 1,116w / workboard 1,165w = within ±5% of plan estimates). Format precedent (CP5) confirmed against existing `resources/documentation/claude_code/cc_cli_commands.md` (tags `resource`/`documentation`/`<tool>`/area/subtopic; `## Overview` + `## Related Notes`; footer bold `**Source**`/`**Last Updated**`/`**Status**`).

| CP | Checkpoint | Verdict | Evidence |
|---|---|---|---|
| CP2 | 9-GATE present per batch (G1-G6 + G7/G8 + G9) | PASS | `## Per-Phase Validation Gate (G1–G9)` table covers G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost detect+redirect, G6 Broken-link fix, G7 Discoverability (in-degree ≥1), G8 Anti-island; G5/G6 skill-driven, single execution phase. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | PASS | `## Entry Point Decision` defers to series hub `0_entry_points/entry_openclaw_docs.md` (master W1 pre-step, >30-note series threshold met at corpus level); 3 CLI-section rows specified. Hub confirmed not-yet-created (created before first sub-plan executes). |
| CP4 | Size (≤30 or split) | PASS | 3 planned notes (single wave) — far under 30. |
| CP5 | Format derived from existing target-dir notes | PASS | Master Format Definition derived from `cc_*`/`pi_*` doc corpora; verified against `cc_cli_commands.md` YAML field order + `## Overview`/`## Related Notes` H2 conventions (not invented). |
| CP6 | Density / borderline → split | PASS | `## Density Re-Assessment`: all 3 notes ~550-700w, ~180-230 lines, ≤6 code blocks — comfortably under ≤400 lines / ≤2,500 words / ≤6 fences. `workboard.md` already split into usage + dispatch notes (documented in Split Decisions). No borderline note. |
| CP7 | Sources measured (not under-estimated) | PASS | Re-read measured wiki 1,116w / workboard 1,165w = 2,281w; matches plan's Source table (ratio ~1.0, within 0.7-1.3). No under-estimation; no re-split needed. |
| CP8 | Undigested terms + authoring reqs | PASS | `## Undigested Terms Plan` present, every row dispositioned (digest-in-`oc_*` / link-existing-term); **0 new term captures** by design (master corpus-wide ownership). `## Term-Note Authoring Requirements` present (N/A with inherited master W5 reference). Must-language used. |
| CP8f | Slug specificity + collision audit | PASS | 0 new `term_*` slugs proposed → no too-general slugs and no slug collisions possible. All-notes dedup: the 3 `oc_cli_*` planned slugs are distinct CLI surfaces with no existing `term_*`/doc duplicate (existing OpenClaw coverage is code-side repo/snippet notes; these are the product-doc home). MISSING terms re-verified excluded. |
| CP9 | Discoverability / inlinks (G8) | PASS | `## Inlinks (existing → new)` maps each of the 3 new notes to ≥1 outside-folder inbound source (entry hub + a `repo_openclaw*` + a term), G8-Discoverability is in the gate table, and inlinks are an EXECUTED phase verified via `note_links` in_degree ≥1 before commit. |

RESULT: 9/9 CP PASS → READY FOR EXECUTION. Plan status advanced `pending` → `ready`.
</content>
</invoke>
