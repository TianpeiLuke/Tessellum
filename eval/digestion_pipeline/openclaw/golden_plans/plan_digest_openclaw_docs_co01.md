---
title: Sub-Plan co01 — OpenClaw Docs: Concepts (Agent Runtime, Loop, Architecture, Workspace, Channel Docking, Active Memory)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["concepts/active-memory", "concepts/agent", "concepts/agent-loop", "concepts/agent-runtimes", "concepts/agent-workspace", "concepts/architecture", "concepts/channel-docking"]
---

# Sub-Plan co01: Concepts

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML field order, `## Overview` + `## Related Notes` + `## References`), dedup-before-create (term_dictionary AND documentation/ AND repo_openclaw*), the 9-GATE, cross-refs, and entry-point wiring are ALL inherited from the master and are NOT re-derived here.

## Scope

The seven foundational `concepts/` pages that define OpenClaw's agent runtime, execution loop, gateway
architecture, and conversational-memory model — the architecture/runtime vocabulary nearly every other
sub-plan (CLI, gateway, channels, tools, plugins) references. This is **Phase A, Priority P1**: these notes
must land early because they establish the canonical meaning of "agent runtime", "agent loop", "harness",
"workspace", "Gateway", "session", and "active memory" that the rest of the corpus links to.

Pages covered: `active-memory` (the optional blocking memory sub-agent), `agent` (the single embedded agent
runtime contract), `agent-loop` (the loop lifecycle, event streams, hook points, timeouts), `agent-runtimes`
(provider vs model vs runtime vs harness vs channel taxonomy, Codex surfaces, runtime selection),
`agent-workspace` (workspace layout + git backup), `architecture` (WebSocket Gateway architecture, nodes,
wire protocol, pairing), and `channel-docking` (move one session's reply route between linked channels).

The code-side counterparts — `repo_openclaw_agents`, `repo_openclaw_gateway`, `repo_openclaw_sessions`,
`repo_openclaw_memory`, `repo_openclaw_channels` — are LINKED, not recreated (master dedup policy).

**Source**: OpenClaw docs, 7 pages, **11,070 measured words**. **Planned: 8 notes** (one split).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Active memory | concepts/active-memory | 3,951 | 36 | 22 | 4 | concept + procedure (SPLIT) |
| Agent runtime | concepts/agent | 846 | 1 | 9 | 0 | concept |
| Agent loop | concepts/agent-loop | 1,703 | 0 | 14 | 2 | model |
| Agent runtimes | concepts/agent-runtimes | 1,950 | 3 | 8 | 0 | concept |
| Agent workspace | concepts/agent-workspace | 1,211 | 8 | 8 | 0 | procedure |
| Gateway architecture | concepts/architecture | 754 | 2 | 9 | 4 | concept |
| Channel docking | concepts/channel-docking | 655 | 3 | 7 | 0 | procedure |

H2/H3 counts are the rendered markdown headings (Active memory also carries MDX `<Tabs>`/`<Accordion>`
blocks counted as sub-sections of their parent H2). Code = fenced blocks (fence-line count / 2).

## Content Strategy

- **Prioritize**: the runtime/loop/architecture trio (`agent`, `agent-loop`, `agent-runtimes`,
  `architecture`) — these are the high-fan-in concept notes the rest of the corpus links back to. Capture
  the loop event-stream contract (`lifecycle`/`assistant`/`tool`), the runtime-selection precedence rules,
  the provider/model/runtime/harness/channel layer table, and the WS wire-protocol invariants faithfully.
- **Split**: `active-memory.md` (3,951w, 36 code) exceeds the 2,500w / 6-code caps AND mixes building
  blocks — it is part concept ("what/why/when/where it runs", the two gates, the runtime-shape diagram) and
  part operator procedure ("quick start", model/query-mode/prompt-style tuning, memory-tool wiring,
  transcript persistence, debugging). Split into a **concept** note (`oc_concepts_active_memory_overview`)
  and a **procedure** note (`oc_concepts_active_memory_config`). See Split Decisions.
- **Link-out, do not redefine**: provider/model/runtime vocabulary that has its own home page is linked, not
  inlined — `concepts/model-providers`, `concepts/models`, `concepts/streaming`, `concepts/compaction`,
  `concepts/queue`, `concepts/queue-steering`, `concepts/session`, `concepts/system-prompt`,
  `concepts/memory`, `concepts/memory-search`, `concepts/context-engine` are sibling concept pages owned by
  co02–co07 and are cited as cross-references (planned siblings) rather than digested here. Gateway config
  fields (`gateway/configuration`, `gateway/sandboxing`, `gateway/protocol`, `gateway/security`,
  `gateway/heartbeat`) belong to the gw0x sub-plans; plugin/hook reference (`plugins/hooks`,
  `plugins/sdk-setup`, `plugins/copilot`, `plugins/codex-harness-runtime`) to pl0x; CLI commands
  (`cli/status`, `cli/agent`) to cl0x; automation hooks (`automation/hooks`) to au01.
- **No term definitions inlined** (master rule): OpenClaw vocabulary is documented as `oc_` doc notes;
  existing `term_dictionary` notes (`term_openclaw`, `term_agent_harness`, `term_websocket`, etc.) are
  linked, never redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_concepts_active_memory_overview.md` | concept | active-memory.md: intro, How to see it, When it runs (2 gates), Session types, Where it runs (surface table), Why use it, How it works (runtime-shape diagram), Query modes (conceptual), Prompt styles (conceptual), Model fallback policy (concept), Common issues (conceptual) | 650 | What active memory is — an optional plugin-owned blocking memory sub-agent that runs before the main reply for eligible interactive sessions. Covers its two gates (config opt-in + strict runtime eligibility), where it runs and does not, the recall runtime shape (NONE vs hidden prompt-prefix injection), and query-mode/prompt-style/model-fallback concepts. |
| 2 | `oc_concepts_active_memory_config.md` | procedure | active-memory.md: Quick start, Speed recommendations (Cerebras setup), Session toggle, query/promptStyle config, Memory tools (memory-core / LanceDB / Lossless Claw), Advanced escape hatches, Transcript persistence, Configuration tables, Recommended setup, Cold-start grace, Debugging | 700 | How to enable and tune active memory in `openclaw.json`: safe-default quick start, dedicated fast recall models, `/active-memory` session toggle, query-mode/prompt-style/timeout/toolsAllow tuning, memory-tool wiring per memory plugin, transcript persistence, cold-start grace, and debugging. |
| 3 | `oc_concepts_agent.md` | concept | agent.md: Workspace, Bootstrap files, Built-in tools, Skills, Runtime boundaries, Sessions, Steering while streaming, Model refs, Configuration (minimal) | 600 | The single embedded agent runtime contract — one agent process per Gateway with its own workspace, injected bootstrap files (AGENTS/SOUL/TOOLS/BOOTSTRAP/IDENTITY/USER), skill-load precedence, JSONL session store, mid-run steering, and `provider/model` ref parsing. |
| 4 | `oc_concepts_agent_loop.md` | model | agent-loop.md: Entry points, How it works (5-step RPC flow), Queueing+concurrency, Session+workspace prep, Prompt assembly, Hook points (internal + plugin hooks), Streaming, Tool execution, Reply shaping, Compaction+retries, Event streams, Chat channel handling, Timeouts, Where things end early | 700 | The OpenClaw agent loop lifecycle — the serialized per-session run from `agent`/`agent.wait` RPC through `runEmbeddedAgent`, the `lifecycle`/`assistant`/`tool` event streams, internal + plugin hook points, session write-lock, reply shaping/suppression, compaction retries, and the timeout hierarchy. |
| 5 | `oc_concepts_agent_runtimes.md` | concept | agent-runtimes.md: layer table (provider/model/runtime/channel), harness definition, embedded vs CLI-backend families, Codex surfaces, Runtime ownership, Runtime selection precedence, GitHub Copilot runtime, Compatibility contract, Status labels | 700 | The provider vs model vs agent-runtime vs harness vs channel taxonomy — embedded harnesses (openclaw/codex/copilot) vs CLI backends (claude-cli), the five Codex surfaces, runtime-ownership split, the runtime-selection precedence order, and how to read Execution/Runtime status labels. |
| 6 | `oc_concepts_agent_workspace.md` | procedure | agent-workspace.md: Default location, Extra workspace folders, Workspace file map (AGENTS/SOUL/USER/IDENTITY/TOOLS/HEARTBEAT/BOOT/BOOTSTRAP/memory/MEMORY/skills/canvas), What is NOT in the workspace, Git backup (private), Do not commit secrets, Moving to a new machine, Advanced notes | 650 | The agent workspace — its default location (`~/.openclaw/workspace`), the standard file map and what is deliberately kept under `~/.openclaw/` instead, the recommended private-git backup workflow, secret hygiene, and migrating a workspace to a new machine. |
| 7 | `oc_concepts_architecture.md` | concept | architecture.md: Overview (single Gateway + WS), Components and flows (Gateway daemon / clients / nodes / WebChat), Connection lifecycle, Wire protocol summary, Pairing+local trust, Protocol typing+codegen (TypeBox), Remote access, Operations snapshot, Invariants | 600 | The OpenClaw Gateway architecture — one long-lived WebSocket Gateway per host owning all messaging surfaces, control-plane clients and `role: node` nodes over the same WS API, the req/res/event wire protocol, device-based pairing and auth modes, TypeBox→JSON-Schema→Swift codegen, and remote-access patterns. |
| 8 | `oc_concepts_channel_docking.md` | procedure | channel-docking.md: intro, Example, Why use it, Required config (session.identityLinks), Commands (/dock-* per channel), What changes (session delivery fields), What does not change, Troubleshooting | 500 | Channel docking — call-forwarding for one OpenClaw session: keep the same conversation context but move future replies between linked channels via `/dock-<channel>`. Covers the required `session.identityLinks` identity group, the bundled dock commands, the session delivery fields updated, and what docking deliberately does not change. |

## Section Coverage Map

```
concepts/active-memory.md  (3,951w — SPLIT: notes 1 + 2)
├── intro (blocking memory sub-agent, why) ───────────────── → note 1 (overview)
├── ## Quick start ───────────────────────────────────────── → note 2 (config)
├── ## Speed recommendations (+ ### Cerebras setup) ──────── → note 2
├── ## How to see it ─────────────────────────────────────── → note 1 (concept: hidden prefix, not exposed)
├── ## Session toggle ────────────────────────────────────── → note 2 (/active-memory on/off/status, --global)
├── ## When it runs (2 gates) ────────────────────────────── → note 1
├── ## Session types (allowedChatTypes/Ids/deniedChatIds) ── → note 1 concept + note 2 config detail
├── ## Where it runs (surface table) ─────────────────────── → note 1
├── ## Why use it ────────────────────────────────────────── → note 1
├── ## How it works (mermaid runtime shape) ──────────────── → note 1
├── ## Query modes (message/recent/full) ─────────────────── → note 1 concept + note 2 timeout tuning
├── ## Prompt styles ─────────────────────────────────────── → note 1 concept + note 2 config
├── ## Model fallback policy ─────────────────────────────── → note 1 (resolution order) + note 2 (modelFallback)
├── ## Memory tools (### memory-core / ### LanceDB / ### Lossless Claw) → note 2
├── ## Advanced escape hatches (thinking/promptAppend/promptOverride) → note 2
├── ## Transcript persistence ────────────────────────────── → note 2
├── ## Configuration (field tables) ──────────────────────── → note 2
├── ## Recommended setup (+ ### Cold-start grace) ────────── → note 2
├── ## Debugging ─────────────────────────────────────────── → note 2
├── ## Common issues (<AccordionGroup>) ──────────────────── → note 1 (concept) + note 2 (fixes)
└── ## Related pages ─────────────────────────────────────── → References of notes 1 + 2
concepts/agent.md  (846w — note 3)
├── intro (single embedded agent runtime) ────────────────── → note 3
├── ## Workspace (required) ──────────────────────────────── → note 3 (+ link note 6)
├── ## Bootstrap files (injected) ────────────────────────── → note 3
├── ## Built-in tools ────────────────────────────────────── → note 3
├── ## Skills ────────────────────────────────────────────── → note 3
├── ## Runtime boundaries ────────────────────────────────── → note 3
├── ## Sessions ──────────────────────────────────────────── → note 3
├── ## Steering while streaming ──────────────────────────── → note 3
├── ## Model refs ────────────────────────────────────────── → note 3
├── ## Configuration (minimal) ───────────────────────────── → note 3
└── ## Related ───────────────────────────────────────────── → References of note 3
concepts/agent-loop.md  (1,703w — note 4)
├── intro (agentic loop definition) ──────────────────────── → note 4
├── ## Entry points ──────────────────────────────────────── → note 4
├── ## How it works (high-level, 5 steps) ────────────────── → note 4
├── ## Queueing + concurrency ────────────────────────────── → note 4
├── ## Session + workspace preparation ───────────────────── → note 4
├── ## Prompt assembly + system prompt ───────────────────── → note 4
├── ## Hook points (### Internal hooks / ### Plugin hooks) ── → note 4
├── ## Streaming + partial replies ───────────────────────── → note 4
├── ## Tool execution + messaging tools ──────────────────── → note 4
├── ## Reply shaping + suppression ───────────────────────── → note 4
├── ## Compaction + retries ──────────────────────────────── → note 4
├── ## Event streams (today) ─────────────────────────────── → note 4
├── ## Chat channel handling ─────────────────────────────── → note 4
├── ## Timeouts ──────────────────────────────────────────── → note 4
├── ## Where things can end early ────────────────────────── → note 4
└── ## Related ───────────────────────────────────────────── → References of note 4
concepts/agent-runtimes.md  (1,950w — note 5)
├── intro + layer table (provider/model/runtime/channel) ─── → note 5
├── harness definition + embedded vs CLI-backend families ── → note 5
├── ## Codex surfaces (table + decision tree) ────────────── → note 5
├── ## Runtime ownership (ownership table) ────────────────── → note 5
├── ## Runtime selection (precedence) ────────────────────── → note 5
├── ## GitHub Copilot agent runtime ──────────────────────── → note 5
├── ## Compatibility contract ────────────────────────────── → note 5
├── ## Status labels ─────────────────────────────────────── → note 5
└── ## Related ───────────────────────────────────────────── → References of note 5
concepts/agent-workspace.md  (1,211w — note 6)
├── intro + <Warning> (cwd not a hard sandbox) ───────────── → note 6
├── ## Default location ──────────────────────────────────── → note 6
├── ## Extra workspace folders ───────────────────────────── → note 6
├── ## Workspace file map (<AccordionGroup>) ─────────────── → note 6
├── ## What is NOT in the workspace ──────────────────────── → note 6
├── ## Git backup (recommended, private) (<Steps>) ───────── → note 6
├── ## Do not commit secrets ─────────────────────────────── → note 6
├── ## Moving the workspace to a new machine ─────────────── → note 6
├── ## Advanced notes ────────────────────────────────────── → note 6
└── ## Related ───────────────────────────────────────────── → References of note 6
concepts/architecture.md  (754w — note 7)
├── ## Overview (single Gateway + WS) ────────────────────── → note 7
├── ## Components and flows (### Gateway/Clients/Nodes/WebChat) → note 7
├── ## Connection lifecycle (mermaid) ────────────────────── → note 7
├── ## Wire protocol (summary) ───────────────────────────── → note 7
├── ## Pairing + local trust ─────────────────────────────── → note 7
├── ## Protocol typing and codegen (TypeBox) ─────────────── → note 7
├── ## Remote access ─────────────────────────────────────── → note 7
├── ## Operations snapshot ───────────────────────────────── → note 7
├── ## Invariants ────────────────────────────────────────── → note 7
└── ## Related ───────────────────────────────────────────── → References of note 7
concepts/channel-docking.md  (655w — note 8)
├── intro (call forwarding for one session) ──────────────── → note 8
├── ## Example ───────────────────────────────────────────── → note 8
├── ## Why use it ────────────────────────────────────────── → note 8
├── ## Required config (session.identityLinks) ───────────── → note 8
├── ## Commands (/dock-* table) ──────────────────────────── → note 8
├── ## What changes (session delivery fields) ────────────── → note 8
├── ## What does not change ──────────────────────────────── → note 8
└── ## Troubleshooting ───────────────────────────────────── → note 8
```
No orphaned sections. Sibling concept pages (model-providers, models, streaming, compaction, queue, session,
system-prompt, memory, memory-search, context-engine) and gateway/plugin/cli/automation reference pages are
linked as cross-references, not duplicated (owned by co02–co07 / gw0x / pl0x / cl0x / au01).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| `concepts/active-memory.md` (3,951w, 36 code, 22 H2) | note 1 `oc_concepts_active_memory_overview` (concept) + note 2 `oc_concepts_active_memory_config` (procedure) | Exceeds the 2,500w word cap AND the 6-code cap, AND mixes two building blocks: a concept half (what active memory is, the two gates, where/why it runs, the runtime-shape diagram, query-mode/prompt-style/fallback concepts) and an operator-procedure half (quick start, Cerebras/fast-model setup, `/active-memory` toggle, config-field tuning, memory-tool wiring, transcript persistence, cold-start grace, debugging). Master "one BB per note" + word/code caps force the split. Each half lands ≤700w and ≤6 code blocks. |

All other six pages are ≤2,000w with a single dominant BB → 1 note each.

## Summary Statistics & Building Block Distribution

- Source pages: **7** (11,070 measured words). New `oc_` notes: **8**. New `term_dictionary` notes: **0**.
- BB distribution: **concept ×4** (notes 1, 3, 5, 7) · **procedure ×3** (notes 2, 6, 8) · **model ×1** (note 4).
- Est. digest words ~4,900 (avg ~610/note); all ≤700w. The 53 source code fences (36 in active-memory)
  distribute across notes; each note kept ≤6 (active-memory's config JSON5 blocks reproduced selectively in
  note 2; concept note 1 keeps only the mermaid runtime-shape + the gate/eligibility text blocks).
  every note maps **≥8 `term_dictionary` terms · ≥10 `code_snippets` · ≥10 docs under `resources/documentation/`**
  `repo_openclaw*`. See **## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)** below for the
  exact per-note locked lists.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

`hermes_agent/hermes_*`, `pi/pi_*`, `band/band_*`, `aws_bedrock_agentcore/*` coding-agent corpora); sibling
`oc_*` docs (this co01 series) and sibling concept pages (co02–co07) do not exist yet and are cited as
**(planned, this series)** / **(planned, co0x)** toward the 10-doc floor. ALL snippets are existing
term → `../../term_dictionary/`, sibling oc_ → `oc_Y.md`, other doc → `../<folder>/`, repo →
`../../../areas/code_repos/`, snippet → `../../code_snippets/`.

### oc_concepts_active_memory_overview (9t · 12s · 12d)

**Terms** (`../../term_dictionary/`)
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — agent long-term memory store/recall; relevance: active memory is the blocking recall pass over agentic memory.
- [Episodic Memory](../../term_dictionary/term_episodic_memory.md) — event/conversation-scoped recall; relevance: what active memory surfaces about prior turns.
- [Workflow Memory](../../term_dictionary/term_workflow_memory.md) — procedural/task memory; relevance: stable habits/routines active memory recalls.
- [Memory Dreaming](../../term_dictionary/term_memory_dreaming.md) — background memory consolidation; relevance: the offline counterpart to active memory's online recall.
- [Subagent](../../term_dictionary/term_subagent.md) — embedded helper agent; relevance: active memory IS a blocking memory sub-agent run before the main reply.
- [Context Engine](../../term_dictionary/term_context_engine.md) — context assembly/recall layer; relevance: Lossless Claw and recall tools live in the context-engine layer active memory uses.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — discipline of shaping model input; relevance: active memory injects a hidden prompt prefix — context engineering in practice.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the recall sub-agent runs an LLM (recall/fallback model resolution).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: umbrella concept this doc series documents.

**Docs**
- [oc_concepts_active_memory_config](oc_concepts_active_memory_config.md) — config/tuning half of this page (planned, this series); relevance: the procedure note this concept note pairs with (the split).
- [oc_concepts_agent_loop](oc_concepts_agent_loop.md) — agent loop lifecycle (planned, this series); relevance: active memory runs in the reply path of the loop (before_agent_reply).
- [oc_concepts_memory](../openclaw/oc_concepts_memory.md) — memory model (planned, co03); relevance: the memory store active memory recalls from.
- [oc_concepts_memory_search](../openclaw/oc_concepts_memory_search.md) — recall/embedding search (planned, co03); relevance: active memory rides the memory-search recall pipeline.
- [cc_auto_memory](../claude_code/cc_auto_memory.md) — Claude Code automatic-memory feature; relevance: closest cross-tool analog — automatic pre-reply memory injection.
- [cc_memory_overview](../claude_code/cc_memory_overview.md) — Claude Code memory model; relevance: comparison for how a coding-agent surfaces long-term memory.
- [hermes_persistent_memory](../hermes_agent/hermes_persistent_memory.md) — Hermes persistent memory; relevance: sibling-ecosystem long-term memory model (Hermes is the OpenClaw fork lineage).
- [hermes_memory_providers_honcho](../hermes_agent/hermes_memory_providers_honcho.md) — Honcho memory provider; relevance: a recall-provider contract like memory-core/LanceDB active memory calls.
- [hermes_context_engine_plugin](../hermes_agent/hermes_context_engine_plugin.md) — Hermes context engine; relevance: the Lossless-Claw-equivalent context-engine recall layer.
- [band_agent_api_memories](../band/band_agent_api_memories.md) — Band agent memory API; relevance: cross-platform memory-recall API shape.
- [bedrock_agentcore_memory_overview](../aws_bedrock_agentcore/bedrock_agentcore_memory_overview.md) — AgentCore managed memory; relevance: managed-service analog to active memory's recall sub-agent.
- [pi_extensions_context](../pi/pi_extensions_context.md) — Pi context injection extension; relevance: how a sibling harness injects recalled context into the prompt.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — OpenClaw memory subsystem; relevance: the code that implements recall (memory_search/memory_get/memory_recall).
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — embedded agent runtime; relevance: hosts the blocking memory sub-agent run.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory_search tool wiring; relevance: the recall tool active memory invokes.
- [snippet_openclaw_memory_runtime](../../code_snippets/snippet_openclaw_memory_runtime.md) — memory runtime; relevance: the runtime the recall sub-agent uses.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory engine; relevance: backing recall/index engine.
- [snippet_openclaw_agents_context_lookup](../../code_snippets/snippet_openclaw_agents_context_lookup.md) — context lookup; relevance: how recalled memory is looked up for prompt injection.
- [snippet_openclaw_memory_events](../../code_snippets/snippet_openclaw_memory_events.md) — memory event stream; relevance: the events emitted around a recall pass.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding inputs; relevance: embeddings that drive recall relevance.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — sub-agent spawn policy; relevance: gates whether the blocking memory sub-agent runs.
- [snippet_openclaw_gateway_doctor_memory_dreaming_preview](../../code_snippets/snippet_openclaw_gateway_doctor_memory_dreaming_preview.md) — dreaming preview; relevance: the consolidation counterpart to active recall.
- [snippet_openclaw_memory_dreaming_constants](../../code_snippets/snippet_openclaw_memory_dreaming_constants.md) — dreaming constants; relevance: tuning knobs for memory consolidation referenced near recall.
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — chat-type resolution; relevance: the allowedChatTypes gate that decides eligibility.
- [snippet_openclaw_memory_host_query_tokenizer](../../code_snippets/snippet_openclaw_memory_host_query_tokenizer.md) — query tokenizer; relevance: builds the memory query the recall sub-agent runs.
- [snippet_openclaw_memory_runtime_re_exports](../../code_snippets/snippet_openclaw_memory_runtime_re_exports.md) — memory runtime exports; relevance: the recall-runtime surface active memory binds to.

### oc_concepts_active_memory_config (9t · 12s · 12d)

**Terms** (`../../term_dictionary/`)
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — agent long-term memory; relevance: the subsystem this note configures recall against.
- [Vector Database](../../term_dictionary/term_vector_database.md) — embedding store (LanceDB); relevance: the memory-lancedb slot this note wires for recall.
- [Embedding](../../term_dictionary/term_embedding.md) — vector representation; relevance: `memorySearch.provider`/embedding model config tuned here.
- [Context Engine](../../term_dictionary/term_context_engine.md) — context recall layer; relevance: Lossless Claw context-engine plugin config (lcm_* tools).
- [Subagent](../../term_dictionary/term_subagent.md) — embedded helper agent; relevance: this note tunes the blocking memory sub-agent (model/timeout/thinking).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model provider; relevance: the Cerebras/Gemini providers configured for fast recall.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — discovered/configured models; relevance: `config.model`/`modelFallback` reference catalog entries.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — reasoning/thinking level; relevance: the `config.thinking` escape-hatch override this note documents.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: `openclaw.json` is the config surface this note edits.

**Docs**
- [oc_concepts_active_memory_overview](oc_concepts_active_memory_overview.md) — concept half (planned, this series); relevance: the concept note this procedure pairs with.
- [oc_concepts_agent](oc_concepts_agent.md) — agent runtime contract (planned, this series); relevance: plugin/agent targeting (`config.agents`) configured here.
- [oc_concepts_agent_workspace](oc_concepts_agent_workspace.md) — workspace/sessions paths (planned, this series); relevance: transcript persistence paths under the sessions folder.
- [oc_concepts_memory_search](../openclaw/oc_concepts_memory_search.md) — recall/embedding search (planned, co03); relevance: the recall providers and `memorySearch.*` config.
- [oc_concepts_compaction](../openclaw/oc_concepts_compaction.md) — compaction/Lossless Claw (planned, co02); relevance: Lossless Claw recall tools (lcm_grep) configured in toolsAllow.
- [cc_auto_memory](../claude_code/cc_auto_memory.md) — Claude Code auto-memory; relevance: comparable enable/scope toggles for automatic memory.
- [hermes_memory_provider_plugin](../hermes_agent/hermes_memory_provider_plugin.md) — Hermes memory-provider plugin; relevance: provider-plugin contract analogous to memory-core/LanceDB.
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — Hermes memory providers; relevance: the provider catalog you pick a recall backend from.
- [hermes_context_engine_plugin](../hermes_agent/hermes_context_engine_plugin.md) — Hermes context engine; relevance: Lossless-Claw-equivalent recall config.
- [pi_provider_auth](../pi/pi_provider_auth.md) — Pi provider auth; relevance: provider/API-key config (Cerebras key) for a recall model.
- [bedrock_agentcore_memory_overview](../aws_bedrock_agentcore/bedrock_agentcore_memory_overview.md) — managed memory config; relevance: managed-service memory-config analog.
- [hermes_memory_providers_honcho](../hermes_agent/hermes_memory_providers_honcho.md) — Honcho provider setup; relevance: a concrete recall-provider config example.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory subsystem; relevance: memory-core/LanceDB recall tools this note configures.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension host; relevance: where active-memory + memory plugins are registered.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: hosts the recall sub-agent the config tunes.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_memory_host_backend_config](../../code_snippets/snippet_openclaw_memory_host_backend_config.md) — memory backend config; relevance: the backend the config selects.
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — embeddings config; relevance: embedding provider/model tuning.
- [snippet_openclaw_memory_runtime](../../code_snippets/snippet_openclaw_memory_runtime.md) — memory runtime; relevance: runtime the recall config applies to.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory_search wiring; relevance: the default toolsAllow recall tool.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config; relevance: how plugin config flows into the sub-agent runtime.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — model fallback ladder; relevance: the model-resolution order `modelFallback` plugs into.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — fallback cooldown; relevance: the circuit-breaker cooldown fields documented here.
- [snippet_openclaw_context_engine_delegate](../../code_snippets/snippet_openclaw_context_engine_delegate.md) — context-engine delegate; relevance: Lossless Claw delegation (lcm_expand) referenced in toolsAllow notes.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding inputs; relevance: what embeddings the configured provider receives.
- [snippet_openclaw_context_engine_registry_compat](../../code_snippets/snippet_openclaw_context_engine_registry_compat.md) — context-engine registry; relevance: registering Lossless Claw as a context engine before active memory uses its recall tools.
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript events; relevance: persistTranscripts/transcriptDir behavior.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload apply; relevance: how openclaw.json edits take effect after restart.

### oc_concepts_agent (9t · 12s · 12d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: the embedded runtime is OpenClaw's core agent contract.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — harness that runs an agent loop; relevance: the embedded runtime is OpenClaw's harness implementation.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving coding agents; relevance: the agent process this contract defines is a coding agent.
- [Skills](../../term_dictionary/term_skills.md) — loadable agent capabilities; relevance: the skill-load precedence order this page specifies.
- [Persona](../../term_dictionary/term_persona.md) — agent personality/SOUL; relevance: SOUL.md persona injected via bootstrap files.
- [Steering Files](../../term_dictionary/term_steering_files.md) — AGENTS/TOOLS/USER guidance files; relevance: the injected bootstrap files this page enumerates.
- [Session ID](../../term_dictionary/term_sessionid.md) — stable session identifier; relevance: OpenClaw-chosen SessionId for the JSONL store.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session state; relevance: JSONL transcript store described here.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation boundary; relevance: `agents.defaults.sandbox` per-session workspace override.

**Docs**
- [oc_concepts_agent_workspace](oc_concepts_agent_workspace.md) — full workspace layout (planned, this series); relevance: the workspace this contract requires.
- [oc_concepts_agent_loop](oc_concepts_agent_loop.md) — loop lifecycle (planned, this series); relevance: how sessions run against this runtime.
- [oc_concepts_agent_runtimes](oc_concepts_agent_runtimes.md) — runtime families (planned, this series); relevance: where the embedded openclaw runtime sits in the taxonomy.
- [oc_concepts_architecture](oc_concepts_architecture.md) — gateway architecture (planned, this series); relevance: one agent runtime per Gateway.
- [oc_concepts_session](../openclaw/oc_concepts_session.md) — session model (planned, co06); relevance: the session store this contract uses.
- [cc_claude_md_files](../claude_code/cc_claude_md_files.md) — CLAUDE.md project files; relevance: the closest analog to AGENTS.md bootstrap injection.
- [cc_skills_overview](../claude_code/cc_skills_overview.md) — Claude Code skills; relevance: comparable skill-loading precedence model.
- [hermes_personality_soul](../hermes_agent/hermes_personality_soul.md) — Hermes SOUL.md; relevance: the persona-file equivalent of OpenClaw SOUL.md.
- [hermes_context_files](../hermes_agent/hermes_context_files.md) — Hermes context/bootstrap files; relevance: AGENTS/USER/TOOLS-equivalent injected files.
- [pi_sessions](../pi/pi_sessions.md) — Pi session model; relevance: sibling-harness session/runtime contract.
- [band_agent_lifecycle](../band/band_agent_lifecycle.md) — Band agent lifecycle; relevance: cross-platform agent-process lifecycle analog.
- [band_sdk_reference_agent_core](../band/band_sdk_reference_agent_core.md) — Band agent-core SDK; relevance: the agent-runtime contract counterpart.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — embedded agent runtime; relevance: implements this contract.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store; relevance: the JSONL transcript store.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skill loader; relevance: skill-load precedence implementation.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config; relevance: the agent runtime configuration surface.
- [snippet_openclaw_agents_identity](../../code_snippets/snippet_openclaw_agents_identity.md) — agent identity; relevance: IDENTITY.md / agent id wiring.
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — bootstrap budget; relevance: bootstrapMaxChars/total trimming of injected files.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — system-prompt injection; relevance: how bootstrap files enter Project Context.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skills planner; relevance: skill load + precedence resolution.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — skill availability; relevance: config/env skill gating.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: built-in tools available to the runtime.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy; relevance: apply_patch gating / tool availability subject to policy.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session-key utils; relevance: stable SessionId derivation.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle; relevance: bootstrap-on-first-turn lifecycle.
- [snippet_openclaw_agents_scope](../../code_snippets/snippet_openclaw_agents_scope.md) — agent scope; relevance: single-runtime-per-Gateway boundary.
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — system-prompt modes; relevance: prompt assembly the bootstrap files feed.

### oc_concepts_agent_loop (9t · 12s · 12d)

**Terms** (`../../term_dictionary/`)
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — harness running the loop; relevance: `runEmbeddedAgent` is the harness that drives this loop.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool-calling; relevance: the tool-execution phase of the loop.
- [Gateway Hooks](../../term_dictionary/term_gateway_hooks.md) — gateway event hooks; relevance: the internal + plugin hook points enumerated in the loop.
- [Message Queue](../../term_dictionary/term_message_queue.md) — serialized run queue; relevance: per-session + global lane serialization.
- [Agent Steering](../../term_dictionary/term_agent_steering.md) — mid-run prompt steering; relevance: steer/followup/collect/interrupt queue modes feed the lane.
- [Compaction](../../term_dictionary/term_compaction.md) — transcript summarization; relevance: auto-compaction + retry stage of the loop.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC protocol; relevance: `agent`/`agent.wait` RPC entry points.
- [Subagent](../../term_dictionary/term_subagent.md) — embedded helper run; relevance: hook points where sub-agent/plugin turns are claimed.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: the loop is OpenClaw's authoritative run path.

**Docs**
- [oc_concepts_agent](oc_concepts_agent.md) — runtime contract (planned, this series); relevance: the runtime the loop drives.
- [oc_concepts_agent_runtimes](oc_concepts_agent_runtimes.md) — runtime ownership (planned, this series); relevance: which runtime owns the loop (embedded vs Codex).
- [oc_concepts_architecture](oc_concepts_architecture.md) — gateway architecture (planned, this series); relevance: `agent`/`agent.wait` RPC over WS.
- [oc_concepts_compaction](../openclaw/oc_concepts_compaction.md) — compaction (planned, co02); relevance: the compaction+retry loop stage.
- [oc_concepts_streaming](../openclaw/oc_concepts_streaming.md) — streaming (planned, co07); relevance: assistant-delta / block-streaming stage.
- [cc_agentic_loop](../claude_code/cc_agentic_loop.md) — Claude Code agentic loop; relevance: direct cross-tool analog of the agent loop.
- [cc_agent_sdk_agent_loop](../claude_code/cc_agent_sdk_agent_loop.md) — Claude Agent SDK loop; relevance: the SDK-level loop walkthrough to compare against.
- [hermes_agent_loop](../hermes_agent/hermes_agent_loop.md) — Hermes agent loop; relevance: the OpenClaw-lineage loop documentation.
- [pi_extensions_events_lifecycle](../pi/pi_extensions_events_lifecycle.md) — Pi lifecycle events; relevance: the lifecycle/event-stream analog (start/end/error).
- [pi_rpc_events](../pi/pi_rpc_events.md) — Pi RPC events; relevance: RPC event-stream contract like assistant/tool/lifecycle streams.
- [hermes_event_hooks](../hermes_agent/hermes_event_hooks.md) — Hermes event hooks; relevance: internal-hook analog (agent:bootstrap, command hooks).
- [band_websocket_agent_events](../band/band_websocket_agent_events.md) — Band agent events; relevance: cross-platform agent event-stream shape.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — embedded runner; relevance: `runEmbeddedAgent` lives here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway dispatch; relevance: `agent`/`agent.wait` RPC + dispatch.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store/lock; relevance: session write-lock + transcript writes.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — agent dispatch; relevance: the `agent` RPC entry handler.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — chat lifecycle persist; relevance: lifecycle end/error + transcript persistence.
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — hooks request handler; relevance: internal/plugin hook dispatch in the loop.
- [snippet_openclaw_agents_compaction_chunk_safety](../../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md) — compaction chunk safety; relevance: the compaction+retry stage.
- [snippet_openclaw_agents_tool_loop_detectors_circuit](../../code_snippets/snippet_openclaw_agents_tool_loop_detectors_circuit.md) — tool-loop circuit breaker; relevance: where-things-end-early loop guards.
- [snippet_openclaw_agents_tool_loop_detectors_repeat](../../code_snippets/snippet_openclaw_agents_tool_loop_detectors_repeat.md) — repeat detector; relevance: loop-termination/early-exit guard.
- [snippet_openclaw_gateway_chat_abort_handler](../../code_snippets/snippet_openclaw_gateway_chat_abort_handler.md) — abort handler; relevance: timeout/AbortSignal early-end paths.
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript events; relevance: transcript writes under the session write lock.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — prompt assembly; relevance: prompt-assembly stage of the loop.
- [snippet_openclaw_gateway_session_utils_subagent_liveness](../../code_snippets/snippet_openclaw_gateway_session_utils_subagent_liveness.md) — sub-agent liveness; relevance: stuck/stalled session diagnostics in timeouts.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — buffered delta; relevance: assistant-delta buffering → chat final.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — chat send handler; relevance: reply shaping/suppression + messaging-tool dedupe.

### oc_concepts_agent_runtimes (9t · 12s · 12d)

**Terms** (`../../term_dictionary/`)
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — harness providing a runtime; relevance: this page defines harness vs runtime.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — external agent control plane; relevance: the ACP/acpx adapter path for Codex/Claude Code/external harnesses.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — coding agents; relevance: the runtime families (openclaw/codex/copilot/claude-cli) ARE coding agents.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic coding agent; relevance: claude-cli CLI-backend + Claude Code via ACP.
- [Model Router](../../term_dictionary/term_model_router.md) — model/runtime selection; relevance: the runtime-selection precedence order this page specifies.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider; relevance: provider vs model vs runtime layer distinction.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the model layer the runtime executes.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: `openclaw` is the default embedded runtime.
- [Pi Agent](../../term_dictionary/term_pi_agent.md) — Pi coding agent; relevance: PI vs Codex vs Copilot runtime decision referenced here.

**Docs**
- [oc_concepts_agent](oc_concepts_agent.md) — embedded runtime contract (planned, this series); relevance: the `openclaw` embedded runtime this taxonomy names.
- [oc_concepts_agent_loop](oc_concepts_agent_loop.md) — loop (planned, this series); relevance: the loop a runtime owns.
- [oc_concepts_model_providers](../openclaw/oc_concepts_model_providers.md) — model providers (planned, co04); relevance: the provider layer disambiguated from runtime.
- [oc_concepts_models](../openclaw/oc_concepts_models.md) — models (planned, co04); relevance: the model layer.
- [oc_concepts_model_failover](../openclaw/oc_concepts_model_failover.md) — model failover (planned, co04); relevance: runtime selection interacts with fallback.
- [hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md) — Hermes provider runtime; relevance: provider/runtime layering in the OpenClaw-lineage fork.
- [hermes_codex_runtime_setup](../hermes_agent/hermes_codex_runtime_setup.md) — Hermes Codex runtime; relevance: Codex app-server harness setup analog.
- [cc_agent_sdk_compare_to_other_tools](../claude_code/cc_agent_sdk_compare_to_other_tools.md) — Claude SDK vs other tools; relevance: cross-harness comparison framing.
- [pi_overview](../pi/pi_overview.md) — Pi harness overview; relevance: the PI runtime in the PI/Codex/Copilot decision.
- [band_acp_overview](../band/band_acp_overview.md) — Band ACP; relevance: ACP control-plane analog for external harnesses.
- [band_adapter_codex](../band/band_adapter_codex.md) — Band Codex adapter; relevance: Codex-runtime adapter counterpart.
- [band_coding_agents_deployment](../band/band_coding_agents_deployment.md) — coding-agent deployment; relevance: cross-platform runtime/harness deployment model.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — embedded runtime + harness selection; relevance: AgentHarness selection + runtime registry.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — Hermes agent core; relevance: sibling-fork runtime/harness core.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_acp_runtime_contract](../../code_snippets/snippet_openclaw_acp_runtime_contract.md) — ACP runtime contract; relevance: the external-runtime contract this page describes.
- [snippet_openclaw_acp_manager_runtime_register](../../code_snippets/snippet_openclaw_acp_manager_runtime_register.md) — runtime register; relevance: how plugin runtimes claim provider/model pairs.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config; relevance: `agentRuntime.id` model/provider-scoped policy.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — fallback ladder; relevance: runtime selection in auto mode + fallback.
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — ACP sub-agent spawn; relevance: spawning external harnesses via ACP.
- [snippet_openclaw_acp_manager_controls_apply](../../code_snippets/snippet_openclaw_acp_manager_controls_apply.md) — ACP controls; relevance: bind/resume/steer/stop control surface (Codex).
- [snippet_openclaw_acp_spawn_policy](../../code_snippets/snippet_openclaw_acp_spawn_policy.md) — ACP spawn policy; relevance: when ACP is used vs native runtime.
- [snippet_openclaw_acp_translator_init_session](../../code_snippets/snippet_openclaw_acp_translator_init_session.md) — ACP session init; relevance: ACP adapter session handshake.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth; relevance: claude-cli/Codex OAuth auth profiles.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: `openai/*` model refs routed to the Codex runtime.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: anthropic model + claude-cli backend example.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery; relevance: provider model discovery feeding runtime selection.

### oc_concepts_agent_workspace (9t · 12s · 12d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: `~/.openclaw/workspace` is the OpenClaw agent home.
- [Persona](../../term_dictionary/term_persona.md) — agent personality; relevance: SOUL.md persona file in the workspace map.
- [Steering Files](../../term_dictionary/term_steering_files.md) — AGENTS/TOOLS/USER files; relevance: the workspace bootstrap-file map.
- [Skills](../../term_dictionary/term_skills.md) — loadable capabilities; relevance: `<workspace>/skills` highest-precedence skill location.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable sessions; relevance: sessions kept under `~/.openclaw/`, NOT the workspace.
- [Session ID](../../term_dictionary/term_sessionid.md) — session identifier; relevance: per-agent sessions folder migration.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation; relevance: workspace is default cwd, NOT a hard sandbox (Warning callout).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — stored credential; relevance: auth-profiles.json kept out of the workspace repo (secret hygiene).

**Docs**
- [oc_concepts_agent](oc_concepts_agent.md) — runtime contract (planned, this series); relevance: bootstrap-file injection from this workspace.
- [oc_concepts_active_memory_config](oc_concepts_active_memory_config.md) — transcript persistence (planned, this series); relevance: transcript paths under the sessions folder.
- [oc_concepts_soul](../openclaw/oc_concepts_soul.md) — SOUL.md guide (planned, co07); relevance: persona workspace file detail.
- [oc_concepts_memory](../openclaw/oc_concepts_memory.md) — memory model (planned, co03); relevance: MEMORY.md / memory/YYYY-MM-DD.md log files.
- [oc_concepts_session](../openclaw/oc_concepts_session.md) — session storage (planned, co06); relevance: where sessions live vs the workspace.
- [cc_claude_md_files](../claude_code/cc_claude_md_files.md) — CLAUDE.md files; relevance: the closest analog to AGENTS.md workspace file.
- [cc_dot_claude_directory](../claude_code/cc_dot_claude_directory.md) — `.claude/` directory; relevance: the workspace-vs-config-dir split analog.
- [cc_settings_files](../claude_code/cc_settings_files.md) — settings files; relevance: config kept separate from the working tree (secret hygiene).
- [hermes_personality_soul](../hermes_agent/hermes_personality_soul.md) — Hermes SOUL.md; relevance: persona file equivalent.
- [hermes_context_files](../hermes_agent/hermes_context_files.md) — Hermes context files; relevance: AGENTS/USER/TOOLS workspace-file analog.
- [pi_session_file_format](../pi/pi_session_file_format.md) — Pi session format; relevance: session-storage layout kept out of workspace.
- [hermes_session_storage](../hermes_agent/hermes_session_storage.md) — Hermes session storage; relevance: session-dir migration analog.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: resolves/creates the workspace + bootstrap files.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions; relevance: the sessions dir kept outside the workspace.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills; relevance: `<workspace>/skills` loading.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_agents_identity](../../code_snippets/snippet_openclaw_agents_identity.md) — agent identity; relevance: IDENTITY.md workspace file.
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — bootstrap budget; relevance: bootstrapMaxChars trimming of workspace files.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session-key utils; relevance: sessions-folder layout outside workspace.
- [snippet_openclaw_memory_root_files](../../code_snippets/snippet_openclaw_memory_root_files.md) — memory root files; relevance: MEMORY.md / memory/ daily-log files in the map.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — auth-profile portability; relevance: auth-profiles.json kept out of the repo (migration).
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential order; relevance: credentials under ~/.openclaw, not workspace.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skills planner; relevance: workspace-skills precedence.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — context injection; relevance: workspace files injected into Project Context.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup config; relevance: `openclaw setup` seeds workspace bootstrap files.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — setup imports; relevance: workspace seeding/migration on a new machine.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration import; relevance: moving a workspace to a new machine.
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — session chat type; relevance: per-agent session paths referenced in migration.

### oc_concepts_architecture (8t · 12s · 12d)

**Terms** (`../../term_dictionary/`)
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: the Gateway's single long-lived WS API.
- [JSON Schema](../../term_dictionary/term_json_schema.md) — schema validation; relevance: inbound frames validated against JSON Schema (TypeBox-generated).
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — request/response RPC; relevance: the req/res/event wire protocol.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe-retry keys; relevance: idempotency keys required for side-effecting methods (send/agent).
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — device pairing; relevance: device-based pairing + device tokens for clients/nodes.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — chat-platform gateway; relevance: the Gateway owns all messaging surfaces.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — request entry hub; relevance: the Gateway is the single API surface for clients + nodes.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: this IS the OpenClaw Gateway architecture.

**Docs**
- [oc_concepts_agent_loop](oc_concepts_agent_loop.md) — loop (planned, this series); relevance: the `agent`/`agent.wait` RPC the Gateway dispatches.
- [oc_concepts_channel_docking](oc_concepts_channel_docking.md) — docking (planned, this series); relevance: reply delivery over the same Gateway.
- [oc_concepts_typebox](../openclaw/oc_concepts_typebox.md) — TypeBox schemas (planned, co07); relevance: the schema → JSON-Schema → Swift codegen layer.
- [oc_concepts_presence](../openclaw/oc_concepts_presence.md) — presence (planned, co05); relevance: the `presence` server-push event.
- [oc_concepts_queue](../openclaw/oc_concepts_queue.md) — command queue (planned, co06); relevance: concurrency/serialization over the WS API.
- [cc_remote_control](../claude_code/cc_remote_control.md) — Claude Code remote control; relevance: remote-access / tunnel analog for a coding-agent gateway.
- [hermes_architecture](../hermes_agent/hermes_architecture.md) — Hermes architecture; relevance: the OpenClaw-lineage gateway architecture.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — Hermes messaging gateway; relevance: single-gateway-owns-all-channels model.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — Hermes gateway internals; relevance: WS daemon + client/node connection internals.
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — Pi RPC protocol; relevance: req/res/event wire-protocol analog.
- [band_websocket_overview](../band/band_websocket_overview.md) — Band WebSocket; relevance: WS agent/human channel architecture analog.
- [bedrock_agentcore_gateway_overview](../aws_bedrock_agentcore/bedrock_agentcore_gateway_overview.md) — AgentCore gateway; relevance: managed agent-gateway architecture counterpart.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway daemon; relevance: implements the WS server + wire protocol.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels; relevance: the messaging surfaces the Gateway owns.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — client apps/nodes; relevance: control-plane clients + `role: node` nodes.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection; relevance: the connect handshake (first frame must be connect).
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: the `{type:req/res/event}` wire-protocol frames.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listen; relevance: the Gateway HTTP server (port 18789 + canvas host).
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — nodes pairing; relevance: device-based pairing + device tokens.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error codes; relevance: handshake error/close behavior.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity/TLS; relevance: device identity on connect + TLS pinning for remote.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — schema groups; relevance: hello-ok features.methods/events discovery metadata.
- [snippet_openclaw_gateway_rpc_protocol_error_codes_version](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_error_codes_version.md) — protocol versioning; relevance: wire-protocol error codes + version.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth modes; relevance: shared-secret / trusted-proxy / none auth modes.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — connect proxy; relevance: Tailscale/SSH-tunnel remote-access path.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS pinning; relevance: optional WS TLS + pinning for remote setups.
- [snippet_openclaw_gateway_entry_dispatch](../../code_snippets/snippet_openclaw_gateway_entry_dispatch.md) — entry dispatch; relevance: request routing into method handlers.

### oc_concepts_channel_docking (8t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: docking moves an OpenClaw session's reply route.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — identity linking; relevance: `session.identityLinks` proves sender/peer are the same person.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session; relevance: docking persists new delivery fields to the session store.
- [Session ID](../../term_dictionary/term_sessionid.md) — session identifier; relevance: the same session keeps its transcript while the route changes.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — chat gateway; relevance: the Gateway re-routes replies across linked channels.
- [Slack](../../term_dictionary/term_slack.md) — chat platform; relevance: `/dock-slack` is one bundled dock target.
- [Message Queue](../../term_dictionary/term_message_queue.md) — delivery queue; relevance: future replies for the session are delivered to the new channel.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — per-platform channel plugin; relevance: dock commands are generated from loaded channel adapters that support native commands.

**Docs**
- [oc_concepts_architecture](oc_concepts_architecture.md) — gateway architecture (planned, this series); relevance: the Gateway that delivers docked replies.
- [oc_concepts_agent](oc_concepts_agent.md) — agent/session contract (planned, this series); relevance: the session whose route docks.
- [oc_concepts_session](../openclaw/oc_concepts_session.md) — session model (planned, co06); relevance: the lastChannel/lastTo/lastAccountId delivery fields.
- [oc_concepts_multi_agent](../openclaw/oc_concepts_multi_agent.md) — multi-agent routing (planned, co05); relevance: channel routing / identity groups.
- [oc_concepts_messages](../openclaw/oc_concepts_messages.md) — message lifecycle (planned, co04); relevance: reply delivery the route change affects.
- [cc_channels_overview](../claude_code/cc_channels_overview.md) — Claude Code channels; relevance: cross-tool multi-channel delivery model.
- [cc_channel_reply_tool](../claude_code/cc_channel_reply_tool.md) — channel reply routing; relevance: how a reply is routed to a channel (analog).
- [cc_claude_code_in_slack](../claude_code/cc_claude_code_in_slack.md) — Claude Code in Slack; relevance: Slack as a dock target/channel analog.
- [hermes_messaging_slack](../hermes_agent/hermes_messaging_slack.md) — Hermes Slack; relevance: Slack channel adapter (`/dock-slack`).
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — Hermes messaging gateway; relevance: cross-channel routing architecture.
- [band_chat_rooms_and_routing](../band/band_chat_rooms_and_routing.md) — Band chat routing; relevance: cross-platform session/route forwarding analog.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels; relevance: dock-command generation from channel plugins.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: per-channel native dock commands.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions; relevance: persists the updated delivery route.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding/routing; relevance: how a session binds to a channel route.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: resolving the target peer id for docking.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — adapter contract; relevance: native-command-capable channel plugins generate dock commands.
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — session-id resolution; relevance: finding the active session to re-route.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing allowlist; relevance: identityLinks group membership check.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — match resolver; relevance: matching the channel-prefixed peer id.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread bindings; relevance: session-to-channel binding the dock updates.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send policy; relevance: docking does not bypass channel allowlists/DM policy.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalize; relevance: channel-prefixed peer-id normalization.
- [snippet_openclaw_sessions_session_label](../../code_snippets/snippet_openclaw_sessions_session_label.md) — session label; relevance: the session whose lastChannel/lastTo fields change.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel dispatch; relevance: delivering replies to the docked channel.

## Undigested Terms Plan

OpenClaw vocabulary on these pages is digested as `oc_` doc notes (this sub-plan) or links existing terms;
**0 new `term_dictionary` captures expected** (master design decision). Disposition per term-like token:

| Term | Disposition |
|---|---|
| active memory, blocking memory sub-agent | Digested as `oc_concepts_active_memory_overview` / `_config` (this sub-plan); link `term_agentic_memory`, `term_subagent`. |
| agent runtime, embedded agent runtime | Digested as `oc_concepts_agent` (this sub-plan); link existing `term_openclaw`, `term_agent_harness`. |
| agent loop, agentic loop | Digested as `oc_concepts_agent_loop` (this sub-plan); link `term_agent_harness`, `term_function_calling`. No existing `term_agent_loop` — concept owned by the doc note, not promoted. |
| harness | Link existing `term_agent_harness` (substantive note exists). Not redefined. |
| CLI backend (claude-cli) | Documented in `oc_concepts_agent_runtimes`; link `term_claude_code`, `term_autonomous_coding_agents`. |
| Codex / Codex app-server | Documented in `oc_concepts_agent_runtimes` (config surfaces); no `term_codex` exists — described as config, not promoted (matches master "provider names not promoted"). |
| GitHub Copilot runtime | Documented in `oc_concepts_agent_runtimes`; link `term_autonomous_coding_agents`. No `term_github_copilot`; not promoted (config/provider name). |
| ACP / acpx | Link existing `term_acp_agent_client_protocol`. |
| agent workspace | Digested as `oc_concepts_agent_workspace`; link `term_skills`, `term_persona`. |
| bootstrap files (AGENTS/SOUL/TOOLS/IDENTITY/USER/BOOTSTRAP/HEARTBEAT/BOOT) | Documented inline in workspace/agent notes; SOUL.md detail links `oc_concepts_soul` (planned, co07). Not term notes (file-name vocabulary, doc-owned). |
| Gateway, node, WebChat | Documented in `oc_concepts_architecture`; link `term_messaging_gateway`, `term_websocket`. No `term_gateway`/`term_node`; described in the doc note, not promoted (deep gateway treatment owned by gw0x). |
| TypeBox | Documented in `oc_concepts_architecture` (schema codegen); link `term_json_schema`. Dedicated `concepts/typebox` page owned by co07 → `oc_concepts_typebox` (planned). No `term_typebox`; not promoted. |
| pairing / device token | Link existing `term_dm_pairing`; deep treatment in `oc_concepts_architecture` + `channels/pairing` (ch0x). |
| channel docking, identityLinks, /dock | Digested as `oc_concepts_channel_docking`; link `term_messaging_gateway`, `term_session_persistence`. |
| steering, queue modes (steer/followup/collect/interrupt) | Link existing `term_agent_steering`, `term_message_queue`; deep treatment owned by `oc_concepts_queue` / `oc_concepts_queue_steering` (co06). |
| compaction, streaming, system prompt, session | Link to planned siblings `oc_concepts_compaction` (co02), `oc_concepts_streaming` (co07), `oc_concepts_system_prompt` (co07), `oc_concepts_session` (co06); not redefined here. |

**No genuinely cross-cutting reusable term lacking an existing note appears on these 7 pages.** All
architecture/runtime vocabulary either has an existing `term_dictionary` note to link or is doc-page-owned
(an `oc_` note). New-term candidates: **none**.

## Term-Note Authoring Requirements

**N/A (0 new terms)** — this sub-plan authors zero `term_dictionary` notes; it only LINKS existing terms.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P1). All gates must PASS before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format — YAML field order + body structure (`## Overview` + `## Related Notes` + `## References` + footer) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding — every claim traces to `inbox/openclaw_docs/concepts/<page>.md` | diff vs source mirror; no invented behavior |
| G3 | Density + Coverage — ≤400 lines, ≤2,500 words, ≤6 code blocks, one BB/note; every H2/H3 mapped | word/code count + Section Coverage Map |
| G4 | Cross-Reference — ≥6 relevancy-selected terms + repo/sibling/snippet links, each with a relevance statement | Related Notes audit |
| G5 | Ghost-reference detect + redirect — every cited note_id resolves in DB | `sqlite3` existence check (done at plan + re-run at execute) |
| G6 | Broken-link fix — correct relative paths | `/tessellum-fix-broken-links` after reindex |
| G7 | Discoverability — every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` | `entry_openclaw_docs.md` + repo/term inlinks |
| G8 | In-degree ≥1 (anti-island) | `note_links` query post-reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_concepts_active_memory_overview oc_concepts_active_memory_config oc_concepts_agent oc_concepts_agent_loop oc_concepts_agent_runtimes oc_concepts_agent_workspace oc_concepts_architecture oc_concepts_channel_docking"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1: required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "G1 MISSING SECTION '$sec': $n"; done
  # G1: source_url present
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "G1 MISSING source_url: $n"; }
  # G1: format check
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # G3: density (exclude frontmatter from word count)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
  # G4: at least one sibling oc_ cross-link
  grep -q "($SIBLING_PREFIX" "$f" || echo "G4 no sibling $SIBLING_PREFIX link: $n"
done

# G1 YAML frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost-reference: verify every cited note_id resolves in the DB
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
grep -rhoE '\]\(([.][.]/)+[^)]+\.md\)' "$GATE_DIR"/oc_concepts_*.md | sed -E 's#.*/([^/)]+)\.md\)#\1#' | sort -u | \
while read -r stem; do
  [ -z "$stem" ] && continue
  [ "$r" = "1" ] || echo "G5 GHOST (pre-reindex; OK if sibling oc_ planned): $stem"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps (≤2500w / ≤6 code / ≤400L)? |
|---|---|---|---:|---:|---|
| 1 | oc_concepts_active_memory_overview | concept | 650 | ≤3 | ✅ (mermaid runtime-shape + gate/eligibility text only) |
| 2 | oc_concepts_active_memory_config | procedure | 700 | ≤6 | ✅ (selective JSON5 config blocks; full field tables as markdown tables, not fences) |
| 3 | oc_concepts_agent | concept | 600 | ≤2 | ✅ |
| 4 | oc_concepts_agent_loop | model | 700 | 0 | ✅ (source has 0 fences; RPC flow as numbered prose) |
| 5 | oc_concepts_agent_runtimes | concept | 700 | ≤4 | ✅ (layer/ownership tables as markdown; ≤4 JSON5 config examples) |
| 6 | oc_concepts_agent_workspace | procedure | 650 | ≤6 | ✅ (git-backup bash + .gitignore + 1-2 JSON5; file map as accordion→markdown table) |
| 7 | oc_concepts_architecture | concept | 600 | ≤4 | ✅ (mermaid lifecycle + SSH-tunnel bash + ≤2 protocol blocks) |
| 8 | oc_concepts_channel_docking | procedure | 500 | ≤3 | ✅ (identityLinks JSON5 + dock-command text) |

No note approaches caps. The code-dense `active-memory.md` (36 fences) split so each half stays ≤6; MDX
`<Tabs>`/`<Accordion>`/`<Steps>`/`<Note>`/`<Warning>` wrappers are flattened into prose + markdown tables.

## Entry Point Decision (inherited from master)

This sub-plan contributes **8 rows** to `0_entry_points/entry_openclaw_docs.md` (created as a master W1
pre-step, before the first sub-plan executes) under a **"Concepts — Runtime & Architecture"** cluster. Each
new note receives its entry-point back-link at finalization (satisfies G7/G8 outside-folder inbound link).
`repo_openclaw`) is the master's responsibility, not re-done per sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; satisfies G7/G8 in-degree ≥1):

- `entry_openclaw_docs.md` → all 8 notes (master pre-step W1).
- `term_openclaw` → notes 1–8 (umbrella concept; add a "Documentation" cross-link row).
- `term_agent_harness` → notes 3, 4, 5 (runtime/loop/harness).
- `term_agentic_memory` → notes 1, 2 (active memory).
- `term_websocket` + `term_json_rpc` → note 7 (gateway architecture).
- `term_dm_pairing` → notes 7, 8 (pairing + cross-channel routing).
- `term_acp_agent_client_protocol` → note 5 (runtime families).
- `repo_openclaw_agents` → notes 3, 4, 6 (agent runtime/loop/workspace).
- `repo_openclaw_gateway` → notes 4, 7 (loop RPC + architecture).
- `repo_openclaw_memory` → notes 1, 2 (active memory recall).
- `repo_openclaw_channels` + `repo_openclaw_channels_messaging` → note 8 (channel docking).
- `repo_openclaw_sessions` → notes 3, 6, 8 (session store/routing).

## Pacing Rules (inherited from master)

One execution phase, 8 notes (≤30 fan-out cap). Re-read each source page before authoring; reproduce config
snippets verbatim and selectively (≤6/note). One building block per note. Run all 8 gates before commit;
`git pull --rebase --autostash` first, no Claude co-author trailer, incremental reindex + `note_links` +
0-broken-links verify before commit/push (snippet/DB-update/commit/push is one cycle).

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21 (xref-augment: per-note Related Notes locked at raised floors)** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending — ready to dispatch |

## Augmentation Report (2026-06-21)

**Scope of this augment pass (xref-augment):** locked the per-note `## Related Notes` mapping at the raised
floors and ran the review sign-off. Source was re-read in full (all 7 `inbox/openclaw_docs/concepts/*.md`
pages); measured word/code/heading counts matched the plan's Source table within tolerance (active-memory
3,897w/33c, agent 807w, agent-loop 1,663w, agent-runtimes 1,899w/3c, agent-workspace 1,171w/3c, architecture
732w, channel-docking 594w — the small deltas vs the plan are MDX-wrapper counting differences, not
under-estimation). No re-split needed; all 8 notes stay ≤700w / ≤6 code / ≤400 lines.

**What was locked.** Replaced the draft `## Candidate Cross-References` section with
`## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`. Standard:
`pi/pi_*`, `band/band_*`, `aws_bedrock_agentcore/*` corpora). Every cited EXISTING note_id (202 unique stems)
series + co02–co07) do not exist yet and are cited as planned, counting toward the 10-doc floor only.

**Per-note locked counts** (terms / docs / repos / snippets — all floorsMet=True; ≥5-existing-docs met):

| # | Note | Terms | Docs (existing/total) | Repos | Snippets |
|---|---|---:|---|---:|---:|
| 1 | oc_concepts_active_memory_overview | 9 | 8/12 | 2 | 12 |
| 2 | oc_concepts_active_memory_config | 9 | 7/12 | 3 | 12 |
| 3 | oc_concepts_agent | 9 | 7/12 | 3 | 12 |
| 4 | oc_concepts_agent_loop | 9 | 7/12 | 3 | 12 |
| 5 | oc_concepts_agent_runtimes | 9 | 7/12 | 4 | 12 |
| 6 | oc_concepts_agent_workspace | 8 | 7/12 | 3 | 12 |
| 7 | oc_concepts_architecture | 8 | 7/12 | 3 | 12 |
| 8 | oc_concepts_channel_docking | 8 | 6/11 | 3 | 11 |

**Dedup audit during locking.** Caught and fixed two intra-group duplicate anchors introduced while building
the lists: note 2 had `snippet_openclaw_memory_host_backend_config` listed twice (replaced the second with
`snippet_openclaw_context_engine_registry_compat`), and note 8 had `term_messaging_gateway` listed twice
(replaced the second with the distinct, relevant `term_channel_adapter`). Re-verified: 0 intra-group dups,
all floors still met.

**New-term candidates: none.** Re-read surfaced no genuinely cross-cutting, vault-reusable term lacking an
existing note. All architecture/runtime/memory/gateway vocabulary on these 7 pages either has an existing
`term_dictionary` note to LINK (best-fit glossary `acronym_glossary_agentic_coding` / the agentic-LLM
glossary — already rich) or is doc-page-owned (an `oc_*` note), matching the master "OpenClaw vocabulary is
documented as `oc_` doc notes, not promoted to terms" decision. The Undigested Terms Plan + Term-Note
Authoring Requirements (N/A, 0 new terms) sections are unchanged and remain valid.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + raised floors, relevance + relevancy statement per link) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; all 8 notes ≥8 terms · ≥10 snippets · ≥10 docs (min 8t/11s/11d on channel-docking); every link rendered `- [Name](relpath.md) — what; relevance: why THIS note`. Counts re-verified programmatically. |
| CP2 | 9-GATE present per batch (G1–G6 + G7/G8 discoverability) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present (single P1 phase); G5 ghost-detect + G6 broken-link-fix + G7/G8 in-degree all listed with tool/method. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at master W1) | **PASS** | `## Entry Point Decision (inherited from master)`: 8 rows into `0_entry_points/entry_openclaw_docs.md` (W1 pre-step, >30-note master ⇒ CREATE required); parent-hub wiring W2/W3 owned by master. Each note gets outside-folder back-link (G7/G8). |
| CP4 | Size manageable | **PASS** | 8 planned notes ≤ 30 cap; one split (active-memory) documented in `## Split Decisions`. |
| CP5 | Note format derived from existing target-dir notes | **PASS** | Format inherited from master Format Definition, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` + source-mirrored H2/H3 + `## Related Notes` + `## References` + bold footer; fixed YAML field order; forbidden-fields list). Not invented. |
| CP6 | Density (borderline → split) | **PASS** | `## Density Re-Assessment`: all 8 notes ≤700w / ≤6 code / ≤400L; no borderline note unaddressed. The only >2,500w/6-code source (active-memory) was split concept/procedure. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-read all 7 source pages 2026-06-21; measured words match the plan's Source table within ±5% (no page >1.5× estimate). Densest page (active-memory) measured 3,897w vs plan 3,951w — accurate, split already applied. |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements | **PASS** | `## Undigested Terms Plan` present (full disposition table, 0 new captures — master design); `## Term-Note Authoring Requirements` present (N/A, 0 new terms; multi-source mandate inherited from master if a term were proposed). |
| CP8f | Term-slug specificity + all-notes (term AND doc) dedup/collision audit | **PASS** | 0 new term slugs to rename (0 new terms). Doc-vs-term collision audit: each planned `oc_concepts_*` doc is a documentation concept/procedure note that does NOT duplicate an existing term (terms like `term_agent_harness`, `term_openclaw`, `term_agentic_memory` are LINKED, not recreated, per master dedup policy). No `oc_concepts_agent_loop`-style slug duplicates an existing substantive note (`term_agent_loop` does not exist; concept is doc-owned). |
| CP9 | Discoverability / inlinks executed (G8, no graph islands) | **PASS** | `## Inlinks (existing notes → new notes)` table covers all 8 notes with ≥1 planned outside-folder inbound link (entry_openclaw_docs → 1–8 + per-note term/repo inlinks); G7/G8 in the phase gate table mark in-degree ≥1 as a gated execution requirement, not a recommendation. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.

## Plan Boot Report (master agent, 2026-06-22)

- Source spot-check: re-read `inbox/openclaw_docs/concepts/agent-loop.md` (1703w measured, plan est. 1703 — exact) and `concepts/active-memory.md` (3,897w — confirms the documented concept/procedure SPLIT). All 7 source pages present in mirror; counts match the Source table within tolerance.
- No plan defects requiring amendment. BB taxonomy + density + section coverage map verified. No re-route / drop / new-note / URL change needed.

## Pilot + Gate Calibration (2026-06-22)

- **Pilot (hand-written):** `resources/documentation/openclaw/oc_concepts_agent_loop.md` (model BB; highest cross-ref note: 9t·12d·3r·12s). Gate result **PASS** (139 L, 1818 w, 36 indexed links, 0 code, only in-flight sibling WARNs).
- **Gate config (this campaign):** `GATE_DIR=.../documentation/openclaw REQUIRE_SOURCE_URL=1 SIBLING_PREFIX="oc_" MAX_LINES=400 REQ_SECTIONS="## Overview|## Related Notes|## References" MIN_LINKS=8 PARA_WRAP_CHECK=1`.
- **Known-bad test:** injected forbidden YAML `title:` + a mid-paragraph hard-wrap → gate correctly **FAILED** with `FAIL[yaml] forbidden field 'title'` + `FAIL[parawrap]`, and `check_note_format.py` raised `PROSE-001` (error). Confirms G9 Prose Integrity is genuinely enforced. Method calibrated; cleared for fan-out.
- **Contract:** `plans/contract_openclaw_docs_shared.md` (source = local mirror, read with Read tool; pilot is the worked example).

## Execution Report (2026-06-22)

| Metric | Value |
|---|---|
| Notes created | 8 / 8 planned |
| Pipeline | pilot (oc_concepts_agent_loop, hand-written) + 7 fanned-out; validate verdict=pass, 0 fix rounds |
| Agents | 7 capture + 1 validator = 8; ~987K subagent tokens; ~26 min |
| Gate (full sweep) | 8/8 PASS |
| Format check | 0 errors / 0 PROSE-001 (G9 clean) across all 8 |
| Broken links | 0 |
| Real ghosts | 0 (14 ghost-refs are in-flight oc_* siblings co02–co07, by design) |
| G8 anti-island | PASS (entry_openclaw_docs wires all 8) |
| Cross-ref floors | held after 4 density-driven drops on active_memory_config (8t·8d·3r·10s) |

Status: ready → completed.
