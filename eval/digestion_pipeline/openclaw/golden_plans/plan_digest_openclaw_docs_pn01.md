---
title: Sub-Plan pn01 — OpenClaw Docs: Plan / Design Specs (Codex Context-Engine Harness + UI-Channels Presentation Refactor)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plan/codex-context-engine-harness", "plan/ui-channels"]
---

# Sub-Plan pn01: Plan

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML field order, `## Overview` →
> body → `## Related Notes` → `## References` → footer), dedup-before-create (term_dictionary + documentation/
> + repo_openclaw*), the 9-GATE per phase, cross-references, undigested-terms ownership, and entry-point
> wiring are all INHERITED from the master and are not restated except where this sub-plan locks specifics.

## Scope

The two pages under `docs.openclaw.ai/plan/` — OpenClaw's internal **design / implementation specifications**
(the only `plan/` section in the docs). They are not user how-tos; they are architecture/refactor plans that
argue for a target design and lay out an implementation:

1. `plan/codex-context-engine-harness` — spec for making the bundled **Codex app-server harness** honor the
   same OpenClaw **context-engine lifecycle** (bootstrap / assemble / afterTurn / maintenance / compaction)
   that built-in OpenClaw turns already honor.
2. `plan/ui-channels` — the **channel presentation refactor** plan that decouples semantic message
   presentation (`ReplyPayload.presentation` / `delivery`) from each channel's native UI renderer.

**Priority: P2 (Phase B).** These are design-rationale notes that complement, but are not prerequisites for,
the conceptual/operational core (concepts/CLI/gateway/channels). They are most valuable as **argument /
design-decision** anchors that the runtime (`concepts/context-engine`, `concepts/agent-runtimes`,
`plugins/message-presentation`, `channels`) and the existing FZ-15 OpenClaw architecture analysis can cite.

**Source**: OpenClaw docs, 2 pages, **4,158 measured words**. **Planned: 3 notes.**

The code-side counterparts (`repo_openclaw_agents`, `repo_openclaw_sessions`, `repo_openclaw_channels*`,
`repo_openclaw_memory`, and the FZ-15 analysis notes) are LINKED, not recreated.

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| codex-context-engine-harness | plan/codex-context-engine-harness | 2,712 | 5 | 13 | 17 (+2 H4) | argument (split: rationale concept vs implementation procedure) |
| ui-channels | plan/ui-channels | 1,446 | 3 | 12 | 0 | argument (design/refactor plan) |

Both pages carry a front-matter `summary` + `read_when` block and a `## Status` section (Draft / Implemented)
— captured in each note's `## Overview` as design context, NOT reproduced as a YAML field (forbidden fields).

## Content Strategy

- **Prioritize** the *design rationale* and *target contract* on each page (the durable, citable content): the
  context-engine lifecycle contract Codex must honor, and the semantic `MessagePresentation`/`delivery`
  capability contract. These are the parts the runtime concept notes and FZ-15 analysis will link.
- **Split** `codex-context-engine-harness.md` (2,712w, >2,500w cap, mixed BB): a *rationale/contract* half
  (Goal / Non-goals / Current architecture / Current gap / Desired behavior / Design constraints / Open
  questions / Acceptance criteria) and an *implementation* half (the 10-step Implementation plan + Test plan +
  Observability + Migration). One BB per note (see Split Decisions).
- **Keep `ui-channels.md` as 1 note** (1,446w, single coherent refactor argument; one BB).
- **Reproduce TypeScript snippets selectively, verbatim, ≤6 per note** — the `MessagePresentation` / capability
  type blocks (ui-channels) and the projection-API / pseudo-flow blocks (codex harness) are load-bearing
  contract shapes; quote the essential ones and link out for the rest.
- **Link-out, do not redefine:** `term_context_engine`, `term_compaction`, `term_agent_harness`,
  `term_channel_adapter`, `term_block_kit`, etc. are LINKED; provider/model/codex internals are documented in
  their home sub-plans (co02 `concepts/context-engine`, co04 `concepts/compaction`, pl02
  `plugins/codex-harness*`) and cross-referenced, not duplicated here.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plan_codex_context_engine_harness_design.md` | argument | codex-context-engine-harness.md: Status, Goal, Non-goals, Current architecture, Current gap, Desired behavior, Design constraints (4 H3), Open questions, Acceptance criteria | 750 | Design rationale + target contract for porting the OpenClaw context-engine lifecycle (bootstrap / assemble / afterTurn / maintenance / compaction) onto the bundled Codex app-server harness — the gap, the desired per-turn behavior, the projection/cache/runtime-selection constraints, and acceptance criteria. |
| 2 | `oc_plan_codex_context_engine_harness_implementation.md` | procedure | codex-context-engine-harness.md: Implementation plan (steps 1-10, incl. compaction-policy H4s), Test plan (unit / existing / integration), Observability, Migration / compatibility | 800 | The 10-step implementation procedure for the Codex context-engine port: relocate harness-neutral lifecycle helpers, add the Codex context-projection layer, wire bootstrap / assemble / post-turn / usage, the two-system compaction policy, error handling, plus the unit/integration test matrix and observability fields. |
| 3 | `oc_plan_ui_channels.md` | argument | ui-channels.md: Status, Problem, Goals, Non goals, Target model, Delivery metadata, Runtime capability contract, Channel mapping, Refactor steps, Tests, Open questions, Related | 700 | The channel presentation refactor: why core must stop knowing native UI shapes, the semantic `ReplyPayload.presentation` + `delivery` target model, the runtime outbound capability/render contract with auto-degrade, the per-channel mapping (Discord/Slack/Telegram/Mattermost/Teams/Feishu/LINE), and the 15-step refactor sequence. |

Filename rule applied (master): `oc_` + full slug with `/` and `-` → `_`. Both pages live under `plan/`, so the
base is `oc_plan_codex_context_engine_harness` / `oc_plan_ui_channels`; note 1/2 append the aspect suffix
`_design` / `_implementation` for the split page (per master split-suffix rule). One BB per note.

## Section Coverage Map

```
plan/codex-context-engine-harness.md  (13 H2 / 17 H3 / 2 H4)
├── ## Status ─────────────────────────────────────────────── → note 1 (design) — Overview
├── ## Goal ───────────────────────────────────────────────── → note 1
├── ## Non-goals ──────────────────────────────────────────── → note 1
├── ## Current architecture ───────────────────────────────── → note 1
├── ## Current gap ────────────────────────────────────────── → note 1
├── ## Desired behavior ───────────────────────────────────── → note 1
├── ## Design constraints
│   ├── ### Codex app-server remains canonical … ──────────── → note 1
│   ├── ### Context engine assembly must be projected … ───── → note 1
│   ├── ### Prompt-cache stability matters ─────────────────── → note 1
│   └── ### Runtime selection semantics do not change ──────── → note 1
├── ## Implementation plan
│   ├── ### 1. Export/relocate reusable helpers ───────────── → note 2 (implementation)
│   ├── ### 2. Add a Codex context projection helper ──────── → note 2
│   ├── ### 3. Wire bootstrap before thread startup ───────── → note 2
│   ├── ### 4. Wire assemble before thread/turn start ─────── → note 2
│   ├── ### 5. Preserve prompt-cache stable formatting ────── → note 2
│   ├── ### 6. Wire post-turn after transcript mirroring ──── → note 2
│   ├── ### 7. Normalize usage and prompt-cache context ───── → note 2
│   ├── ### 8. Compaction policy
│   │   ├── #### /compact and explicit OpenClaw compaction ── → note 2
│   │   └── #### In-turn Codex native contextCompaction ───── → note 2
│   ├── ### 9. Session reset and binding behavior ─────────── → note 2
│   └── ### 10. Error handling ────────────────────────────── → note 2
├── ## Test plan
│   ├── ### Unit tests ────────────────────────────────────── → note 2
│   ├── ### Existing tests to update ──────────────────────── → note 2
│   └── ### Integration / live tests ─────────────────────── → note 2
├── ## Observability ──────────────────────────────────────── → note 2
├── ## Migration / compatibility ──────────────────────────── → note 2
├── ## Open questions ─────────────────────────────────────── → note 1 (design decisions/recommendations)
└── ## Acceptance criteria ────────────────────────────────── → note 1

plan/ui-channels.md  (12 H2 / 0 H3)
├── ## Status ─────────────────────────────────────────────── → note 3 — Overview (Implemented)
├── ## Problem ────────────────────────────────────────────── → note 3
├── ## Goals ──────────────────────────────────────────────── → note 3
├── ## Non goals ──────────────────────────────────────────── → note 3
├── ## Target model ───────────────────────────────────────── → note 3 (MessagePresentation schema)
├── ## Delivery metadata ──────────────────────────────────── → note 3 (ReplyPayloadDelivery)
├── ## Runtime capability contract ────────────────────────── → note 3 (capability + render hooks)
├── ## Channel mapping ────────────────────────────────────── → note 3
├── ## Refactor steps ─────────────────────────────────────── → note 3 (15 steps)
├── ## Tests ──────────────────────────────────────────────── → note 3
├── ## Open questions ─────────────────────────────────────── → note 3
└── ## Related ────────────────────────────────────────────── → note 3 (→ References / cross-links)
```
No orphaned sections. Both pages' `## Status` + front-matter `summary`/`read_when` fold into each note's
`## Overview`. Runtime internals (context-engine, compaction, Codex plugin, message-presentation, channels)
are LINKED to their home sub-plans (co02/co04, pl02, plugins/message-presentation, channels), not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| `codex-context-engine-harness.md` (2,712w, 13 H2 / 17 H3, mixed BB) | note 1 `..._design` (argument) + note 2 `..._implementation` (procedure) | Exceeds the 2,500-word density cap AND mixes two building blocks: a design-rationale/target-contract argument (why + desired behavior + constraints + acceptance criteria) vs a sequential implementation procedure (10 build steps + test plan + observability + migration). Split per the master word-cap + one-BB-per-note rules; the rationale note is the durable citable anchor, the implementation note is the build runbook. |
| `ui-channels.md` (1,446w, 12 H2) | (none — 1 note) | Under the word cap; a single coherent refactor argument (problem → target model → contract → mapping → steps). Keeping it whole preserves the design narrative; one BB (argument). |

## Summary Statistics & Building Block Distribution

- Source pages: **2** (4,158 measured words). New `oc_` notes: **3**. New `term_dictionary` notes: **0**.
- BB distribution: **argument ×2** (notes 1, 3) · **procedure ×1** (note 2).
- Est. digest words: ~2,250 (avg ~750/note); each note ≤2,500w, ≤400 lines, ≤6 code blocks.
- Source code fences total **8** (5 in codex-harness, 3 in ui-channels); distributed so each note keeps ≤6
  (the codex-harness 5 fences split ~2 design / ~3 implementation; ui-channels 3 fences all in note 3).
- Cross-refs LOCKED at augment (2026-06-21) in `## Per-Note Related Notes Mapping` at RAISED floors — per
  toward the 10) plus 4 repos each. Actual: N1 9t/12s/12d, N2 9t/12s/11d, N3 9t/12s/11d. All EXISTING cited

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> 2026-06-21). Relative paths are FROM `resources/documentation/openclaw/oc_*.md`:
> term → `../../term_dictionary/`, snippet → `../../code_snippets/`, sibling oc_ → `oc_*.md`,
> other doc → `../<folder>/`, repo → `../../../areas/code_repos/`, analysis → `../../analysis_thoughts/`,
> entry → `../../../0_entry_points/`. Sibling `oc_*` docs (this series) do not exist yet → marked
> "(planned, this series)" and counted toward the 10-doc floor; ≥5 of the 10 docs per note are EXISTING

### oc_plan_codex_context_engine_harness_design (9t · 12s · 12d · 4 repos)

**Terms**
- [Context Engine](../../term_dictionary/term_context_engine.md) — OpenClaw's pluggable per-turn context lifecycle (bootstrap/assemble/afterTurn/maintain/compact); relevance: the EXACT lifecycle contract this spec ports onto the Codex harness — the spec's central subject.
- [Compaction](../../term_dictionary/term_compaction.md) — transcript/history reduction to fit the window; relevance: the "two compaction systems" design constraint (OpenClaw context-engine `compact()` vs Codex native `thread/compact`) the design must not conflate.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime that drives the model loop (tools, turns, transcript); relevance: the harness boundary this spec spans (built-in OpenClaw harness vs bundled Codex app-server harness).
- [Context Window](../../term_dictionary/term_context_window.md) — the model's bounded token budget; relevance: the `contextTokenBudget` the assemble step honors when projecting assembled context into Codex inputs.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — reuse of stable prompt prefixes across calls; relevance: the "prompt-cache stability matters" constraint — assembled context must be byte-deterministic (no timestamps/random ids) for lossless-claw.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — the discipline of deterministic context assembly/selection; relevance: names the assemble/bootstrap construction the desired per-turn behavior performs.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: the product whose context-engine lifecycle and trust boundary this design targets.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — the JSON-RPC agent/client session protocol; relevance: the explicitly-EXCLUDED non-goal ("do not change ACP/acpx session behavior") — this spec is the non-ACP embedded harness path.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agent class Codex belongs to; relevance: scopes the `agentRuntime.id: "codex"` / `codex/*` model runtime this design wires.

**Docs**
- [oc_plan_codex_context_engine_harness_implementation](oc_plan_codex_context_engine_harness_implementation.md) (planned, this series) — the 10-step build runbook; relevance: the implementation note that realizes every constraint/acceptance-criterion this design states.
- [oc_concepts_context_engine](oc_concepts_context_engine.md) (planned, this series, co02) — the context-engine concept home; relevance: owns the lifecycle definition this design only links, never redefines.
- [oc_concepts_compaction](oc_concepts_compaction.md) (planned, this series, co04) — the compaction concept home; relevance: owns the OpenClaw-vs-native compaction distinction this design constrains.
- [oc_concepts_agent_runtimes](oc_concepts_agent_runtimes.md) (planned, this series, co01) — agent-runtime/harness-selection concept; relevance: documents the `runtime: openclaw/codex/auto` selection semantics this design says "do not change".
- [oc_plugins_codex_harness](oc_plugins_codex_harness.md) (planned, this series, pl02) — the Codex harness plugin home; relevance: owns the bundled Codex app-server harness internals this design treats as canonical for native thread state.
- [hermes_context_engine_plugin](../hermes_agent/hermes_context_engine_plugin.md) — Hermes' context-engine plugin contract; relevance: the closest existing-corpus analog of a pluggable assemble/ingest/compact lifecycle, validating the design's plugin boundary.
- [hermes_context_compression_caching](../hermes_agent/hermes_context_compression_caching.md) — Hermes context compression + prompt caching; relevance: prior art for the prompt-cache-stability + deterministic-context constraint.
- [pi_extensions_context](../pi/pi_extensions_context.md) — Pi's context-assembly extension hooks; relevance: cross-tool analog of injecting assembled context around a turn via extension hooks.
- [cc_agent_sdk_context_window](../claude_code/cc_agent_sdk_context_window.md) — Claude Code SDK context-window/budget management; relevance: cross-tool reference for the token-budget assembly the design's constraints govern.
- [cc_hook_session_lifecycle_events](../claude_code/cc_hook_session_lifecycle_events.md) — Claude Code session-lifecycle hook events; relevance: analog for the bootstrap/before-turn/after-turn lifecycle points this design enumerates.
- [band_adapter_codex](../band/band_adapter_codex.md) — BAND's Codex adapter integration; relevance: an independent Codex-app-server adapter, corroborating the "Codex owns native thread; integrate via protocol calls" design stance.
- [bedrock_agentcore_harness](../aws_bedrock_agentcore/bedrock_agentcore_harness.md) — Bedrock AgentCore harness/runtime model; relevance: managed-runtime analog of a harness boundary an external app-server owns — a contrast point for the projection-not-mutation design choice.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the embedded-agent-runner / harness code; relevance: where `resolveContextEngine`, `runEmbeddedAttemptWithBackend`, and the built-in lifecycle calls live — the code this design's gap describes.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — `SessionManager`, transcript mirror, session lifecycle; relevance: the OpenClaw transcript-mirror this design names as the source-of-truth for chat history/search/reset.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — context-engine memory store; relevance: the memory the context-engine lifecycle feeds via ingest/afterTurn.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled extensions incl. `extensions/codex/`; relevance: hosts the Codex plugin (`index.ts`, `harness.ts`, `app-server/run-attempt.ts`) this design references by path.

**Snippets**
- [snippet_openclaw_context_engine_delegate](../../code_snippets/snippet_openclaw_context_engine_delegate.md) — the context-engine delegate dispatch; relevance: shows the `assemble/afterTurn/maintain/compact` delegate surface the Codex harness must call.
- [snippet_openclaw_context_engine_registry_factories](../../code_snippets/snippet_openclaw_context_engine_registry_factories.md) — context-engine plugin registry/factories; relevance: how `resolveContextEngine(config)` selects the active engine (e.g. lossless-claw) the design assumes.
- [snippet_openclaw_context_engine_registry_compat](../../code_snippets/snippet_openclaw_context_engine_registry_compat.md) — registry legacy/compat shim; relevance: backs the migration constraint "legacy context-engine behavior equivalent to today's Codex harness when none configured".
- [snippet_openclaw_agents_context_window_guard](../../code_snippets/snippet_openclaw_agents_context_window_guard.md) — token-budget guard; relevance: the `contextTokenBudget` enforcement the assemble step honors.
- [snippet_openclaw_agents_context_lookup](../../code_snippets/snippet_openclaw_agents_context_lookup.md) — context lookup/resolution; relevance: the per-run context resolution the "current architecture" section describes.
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — bootstrap + budget wiring; relevance: the bootstrap/maintenance-before-attempt step the desired behavior preserves.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — system-prompt context injection; relevance: how `systemPromptAddition` is folded into the prompt — the projection design's developer-instruction target.
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — cache-stable prompt sections; relevance: concrete prior art for the byte-stable formatting constraint.
- [snippet_openclaw_agents_btw_harness_transcript](../../code_snippets/snippet_openclaw_agents_btw_harness_transcript.md) — harness transcript mirroring; relevance: the transcript-mirror read the desired-behavior step 1 ("read mirrored OpenClaw transcript") depends on.
- [snippet_hermes_agent_core_codex_runtime](../../code_snippets/snippet_hermes_agent_core_codex_runtime.md) — Hermes Codex runtime adapter; relevance: an independent Codex-runtime integration corroborating the "control what you send to thread/turn, observe notifications" boundary.
- [snippet_hermes_agent_core_auxiliary_codex_adapter](../../code_snippets/snippet_hermes_agent_core_auxiliary_codex_adapter.md) — auxiliary Codex adapter; relevance: cross-corpus analog of projecting OpenClaw context into a Codex-shaped input.

### oc_plan_codex_context_engine_harness_implementation (9t · 12s · 11d · 4 repos)

**Terms**
- [Context Engine](../../term_dictionary/term_context_engine.md) — the per-turn lifecycle being wired; relevance: every implementation step (1-10) calls a context-engine method (bootstrap/assemble/afterTurn/ingest/maintain/compact).
- [Compaction](../../term_dictionary/term_compaction.md) — history reduction; relevance: step 8's two-system compaction policy (`ownsCompaction` branch + native `thread/compact`) and the in-turn `contextCompaction` event handling.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime loop; relevance: step 1 relocates helpers into a harness-neutral module so both built-in and Codex harnesses share lifecycle code.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — stable-prefix reuse; relevance: step 5's byte-stable projection output + the migration rule "context-engine output must not enter the dynamic-tool fingerprint".
- [Context Window](../../term_dictionary/term_context_window.md) — token budget; relevance: step 7 normalizes usage and maps app-server token notifications into the context-engine runtime context.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: step 4 builds dynamic tools FIRST so the context engine sees actual tool names; tool catalog (not context) drives the dynamic-tool fingerprint.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — model reasoning content; relevance: the thinking/reasoning material the assemble + afterTurn snapshot steps must carry through the projection without corrupting it.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — the request/notification wire format; relevance: the Codex app-server calls steps 3-4 wire (`thread/start`, `thread/resume`, `turn/start`) and the notifications step 7 observes.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session/transcript storage; relevance: step 3's `fs.stat(sessionFile)` "had session file" check + step 6's read-mirrored-session-history finalizer and step 9's reset/binding behavior.

**Docs**
- [oc_plan_codex_context_engine_harness_design](oc_plan_codex_context_engine_harness_design.md) (planned, this series) — the design/contract; relevance: the rationale + acceptance criteria this runbook implements step-by-step.
- [oc_concepts_context_engine](oc_concepts_context_engine.md) (planned, this series, co02) — context-engine concept home; relevance: defines the lifecycle methods (`assemble`, `afterTurn`, `ingestBatch`, `maintain`, `compact`) the steps invoke.
- [oc_concepts_compaction](oc_concepts_compaction.md) (planned, this series, co04) — compaction concept home; relevance: owns the `ownsCompaction` semantics step 8's policy branches on.
- [oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md) (planned, this series, pl02) — Codex harness runtime plugin; relevance: the `extensions/codex/src/app-server/*` modules (run-attempt, thread-lifecycle, event-projector, compact) the steps modify.
- [oc_concepts_session](oc_concepts_session.md) (planned, this series, co06) — session concept home; relevance: the `SessionManager`/session-file semantics steps 3, 6, 9 use for bootstrap-existence, finalize-snapshot, and reset.
- [hermes_prompt_assembly](../hermes_agent/hermes_prompt_assembly.md) — Hermes prompt-assembly pipeline; relevance: a worked analog of step-4's "assemble → project → before_prompt_build → start thread" ordering.
- [hermes_runtime_context_settings](../hermes_agent/hermes_runtime_context_settings.md) — Hermes runtime context settings; relevance: analog for step 7's runtime-context normalization (usage, budget, cache info).
- [pi_compaction_extensions](../pi/pi_compaction_extensions.md) — Pi's compaction extension hooks; relevance: cross-tool analog of the owns-compaction-vs-native split step 8 encodes.
- [pi_extensions_events_lifecycle](../pi/pi_extensions_events_lifecycle.md) — Pi's lifecycle event hooks; relevance: analog for the bootstrap/post-turn/maintenance event ordering steps 3, 6, 9 implement and the error-handling rules step 10 sets.
- [cc_sdk_subagents_lifecycle](../claude_code/cc_sdk_subagents_lifecycle.md) — Claude Code SDK lifecycle hooks; relevance: cross-tool reference for the deterministic lifecycle-call ordering the test plan pins.
- [bedrock_agentcore_sessions_usage](../aws_bedrock_agentcore/bedrock_agentcore_sessions_usage.md) — Bedrock AgentCore session + usage model; relevance: managed-runtime analog of step 7's "normalize usage from app-server token notifications".

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — embedded-agent-runner + harness helpers; relevance: step 1 relocates `runAttemptContextEngineBootstrap` / `assembleAttemptContextEngine` / `finalizeAttemptContextEngineTurn` from here into a harness-neutral module.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — `SessionManager` + transcript mirror + reset; relevance: steps 3/6/9 open the session manager, read mirrored history, and preserve reset-binding behavior.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — context-engine memory; relevance: the afterTurn/ingestBatch finalizer target in step 6.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled extensions incl. Codex; relevance: hosts `extensions/codex/src/app-server/context-engine-projection.ts` (new, step 2) and the modules steps 3-9 edit.

**Snippets**
- [snippet_openclaw_agents_btw_harness_transcript](../../code_snippets/snippet_openclaw_agents_btw_harness_transcript.md) — harness transcript mirror; relevance: step 6's `mirrorTranscriptBestEffort` + read-mirrored-session-history finalize path.
- [snippet_openclaw_agents_compaction_chunk_safety](../../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md) — safe compaction chunking; relevance: backs step 8's compaction-policy correctness when the context engine owns compaction.
- [snippet_openclaw_agents_compaction_identifier_handoff](../../code_snippets/snippet_openclaw_agents_compaction_identifier_handoff.md) — compaction identifier handoff; relevance: the auditable native-vs-owned compaction handoff step 8's `details.codexNativeCompaction` records.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — system-prompt injection; relevance: step 4 appends `systemPromptAddition` to developer instructions before `before_prompt_build`.
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — bootstrap + budget; relevance: step 3's `bootstrapHarnessContextEngine({hadSessionFile, …})` pseudo-flow.
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — session compact + reset; relevance: step 9's "reset clears Codex app-server binding from the OpenClaw session file" behavior to preserve.
- [snippet_openclaw_gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md) — reset helper hooks; relevance: the existing OpenClaw session-lifecycle reset/delete paths step 9 says context-engine cleanup must continue to flow through.
- [snippet_openclaw_sessions_model_overrides](../../code_snippets/snippet_openclaw_sessions_model_overrides.md) — per-session model overrides; relevance: the `codex/*` model / `agentRuntime.id="codex"` selection the integration tests configure.
- [snippet_openclaw_gateway_sessions_read_methods](../../code_snippets/snippet_openclaw_gateway_sessions_read_methods.md) — session read methods; relevance: `buildSessionContext().messages` / read-mirrored-history the bootstrap + finalize steps call.
- [snippet_hermes_agent_core_conversation_loop_session_persist](../../code_snippets/snippet_hermes_agent_core_conversation_loop_session_persist.md) — Hermes session-persist in the loop; relevance: cross-corpus analog of mirror-then-finalize ordering step 6 mandates.
- [snippet_hermes_agent_core_conversation_loop_usage_accounting](../../code_snippets/snippet_hermes_agent_core_conversation_loop_usage_accounting.md) — Hermes usage accounting; relevance: analog for step 7's usage normalization into runtime context (omit promptCache rather than invent zeros).
- [snippet_hermes_agent_core_conversation_compression_strategy](../../code_snippets/snippet_hermes_agent_core_conversation_compression_strategy.md) — Hermes compression strategy; relevance: cross-corpus analog of the owns-compaction primary-result rule in step 8.

### oc_plan_ui_channels (9t · 12s · 11d · 4 repos)

**Terms**
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — the per-channel outbound renderer/transport adapter; relevance: the `ChannelOutboundAdapter` getting the new `renderPresentation` / `pinDeliveredMessage` / capability hooks — the refactor's central object.
- [Adapter Pattern](../../term_dictionary/term_adapter_pattern.md) — wrapping an interface so a core talks to many backends; relevance: the exact pattern this plan applies — core emits semantic `presentation`, adapters render to native (Block Kit, Carbon, Adaptive Cards, Flex).
- [Block Kit](../../term_dictionary/term_block_kit.md) — Slack's structured-message UI framework; relevance: the Slack render target the channel-mapping section maps `presentation` blocks onto.
- [Slack](../../term_dictionary/term_slack.md) — a mapped chat channel; relevance: one of the seven channels whose native escape hatch (`blocks`) is removed in favor of semantic presentation.
- [Markdown](../../term_dictionary/term_markdown.md) — lightweight text markup; relevance: the `text.markdownDialect` capability (`plain`/`markdown`/`html`/`slack-mrkdwn`/`discord-markdown`) and the auto-degrade-to-text fallback.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — the channel control-plane dispatch core; relevance: the control-plane the refactor keeps free of native UI libraries (no `DiscordUiContainer` / Carbon imports).
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the multi-channel message routing layer; relevance: the surface where `ReplyPayload.presentation` + `delivery` flow through outbound normalization and delivery summaries.
- [Hexagonal Architecture](../../term_dictionary/term_hexagonal_architecture.md) — ports-and-adapters core/edge separation; relevance: the architectural principle behind "core decides semantic presentation; extensions adapt to native transports" and "no core imports of channel-native UI".
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent bidirectional channel transport; relevance: the live channel transports (Slack socket mode, Discord gateway) the runtime outbound adapter sends rendered presentation over.

**Docs**
- [oc_plugins_message_presentation](oc_plugins_message_presentation.md) (planned, this series, pl04) — the canonical Message Presentation guide; relevance: the doc this plan explicitly points to as the now-authoritative home for the contract/renderer/fallback behavior.
- [oc_channels](oc_channels.md) (planned, this series, rt01) — channels overview; relevance: the channels hub this plan's "Related" section links and whose adapters consume the new contract.
- [oc_channels_discord](oc_channels_discord.md) (planned, this series, ch01) — Discord channel; relevance: the Carbon/components-v2 render target + the `DiscordUiContainer` import removal step 1.
- [oc_channels_slack](oc_channels_slack.md) (planned, this series, ch05) — Slack channel; relevance: the Block Kit render target + `blocks` input removal.
- [oc_channels_telegram](oc_channels_telegram.md) (planned, this series, ch05) — Telegram channel; relevance: the inline-keyboard render + ACP-topic `delivery.pin` migration the plan specifies.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — Hermes messaging gateway architecture; relevance: the closest existing-corpus analog of a core that routes to per-channel outbound adapters — validates the capability/render-hook contract.
- [hermes_adding_platform_adapter_plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — Hermes platform-adapter plugin guide; relevance: prior art for declaring a channel adapter's render/capability hooks the way `ChannelOutboundAdapter` does.
- [hermes_plugin_extensions_hooks](../hermes_agent/hermes_plugin_extensions_hooks.md) — Hermes plugin extension hooks; relevance: analog for adding render/delivery hooks to the runtime outbound adapter rather than the control-plane plugin.
- [hermes_gateway_feishu_features](../hermes_agent/hermes_gateway_feishu_features.md) — Hermes Feishu interactive-card features; relevance: the Feishu interactive-card render target the channel-mapping section covers.
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — Claude Code channels setup; relevance: cross-tool reference for the per-channel surface configuration the rendered presentation targets.
- [band_integration_methods](../band/band_integration_methods.md) — BAND integration/adapter methods; relevance: cross-corpus view of decoupling a core message model from many platform integrations.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel plugin control plane; relevance: the control-plane code (`extensions/discord/src/channel.ts`, channel plugin types) refactored to drop native-UI imports and `buildCrossContextComponents`.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel renderers; relevance: the Discord/Slack/Telegram/Mattermost/Teams/Feishu/LINE renderers (step 13) that consume the generic contract.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — Web Control UI app; relevance: the "Web Control UI remains separate from chat native UI" goal explicitly kept out of this refactor.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway / outbound delivery surface; relevance: outbound payload normalization, delivery summaries, and the send path that calls `renderPresentation` then `pinDeliveredMessage`.

**Snippets**
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — the channel outbound-adapter contract; relevance: the exact `ChannelOutboundAdapter` shape this plan extends with presentation/delivery hooks.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel dispatch; relevance: the core resolve-adapter / ask-capabilities / render / send flow the "Core behavior" list describes.
- [snippet_openclaw_channels_kernel_durable](../../code_snippets/snippet_openclaw_channels_kernel_durable.md) — durable kernel delivery; relevance: the post-send delivery summary + `pinDeliveredMessage` continuation (auto-degrade on failed pin) the delivery semantics require.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord gateway intents; relevance: the Discord channel whose control-plane must stop importing Carbon UI (steps 1, 13).
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack socket-mode connection; relevance: the Slack transport the Block-Kit-rendered presentation is sent over.
- [snippet_openclaw_channels_telegram_dispatcher](../../code_snippets/snippet_openclaw_channels_telegram_dispatcher.md) — Telegram dispatcher; relevance: the inline-keyboard render + text-fallback + `delivery.pin` migration the Telegram mapping specifies.
- [snippet_openclaw_gateway_openai_http_message_build](../../code_snippets/snippet_openclaw_gateway_openai_http_message_build.md) — outbound message build; relevance: the outbound payload normalization where `presentation`/`delivery` are attached (step 2).
- [snippet_hermes_agent_gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — Hermes outbound runner; relevance: cross-corpus analog of a runtime outbound adapter that renders + delivers per-channel.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — Hermes delivery layer; relevance: analog of the generic `delivery` metadata (pin/notify/required) this plan formalizes.
- [snippet_hermes_agent_gw_platform_feishu_message_card](../../code_snippets/snippet_hermes_agent_gw_platform_feishu_message_card.md) — Hermes Feishu interactive-card render; relevance: cross-corpus example of rendering a generic message into a channel's native card (Feishu mapping).
- [snippet_hermes_agent_gw_platform_telegram_markdown](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_markdown.md) — Hermes Telegram markdown render; relevance: analog of the markdown-dialect + text-fallback capability the Telegram/plain-channel mappings use.

## Undigested Terms Plan

> Per master: OpenClaw vocabulary on these pages is digested as the `oc_*` doc notes themselves (or owned by a
> home sub-plan) and existing `term_dictionary` terms are LINKED, never redefined inline. Expected **0 new
> `term_dictionary` captures** for pn01. Augment re-runs the Step 2d scan.

| Term | Disposition |
|---|---|
| context engine / context-engine lifecycle | Concept owned by co02 (`oc_concepts_context_engine`); LINK existing `term_context_engine`. Not redefined here. |
| Codex app-server harness | Plugin/harness owned by pl02 (`oc_plugins_codex_harness*`); the design/impl is documented in notes 1-2; LINK `term_agent_harness` + `repo_openclaw_agents`. No new term. |
| compaction (OpenClaw context-engine vs Codex native `thread/compact`) | Concept owned by co04 (`oc_concepts_compaction`); LINK existing `term_compaction`. The two-system distinction is documented in note 2, not a new term. |
| assemble / bootstrap / afterTurn / ingest / maintain (lifecycle methods) | Method vocabulary of the context-engine contract; documented as the lifecycle in notes 1-2; covered by `term_context_engine` + `term_context_engineering`. No new term. |
| prompt-cache stability / deterministic projection | LINK existing `term_prompt_caching`. No new term. |
| `MessagePresentation` / `ReplyPayload.presentation` / `delivery` | Contract documented in note 3; canonical guide owned by `plugins/message-presentation` (cross-series). LINK `term_channel_adapter` + `term_adapter_pattern`. No new term. |
| presentation capabilities / auto-degrade / render hooks | Documented in note 3; covered by `term_channel_adapter`. No new term. |
| Block Kit / Adaptive Cards / Carbon / Flex (native UI surfaces) | Channel-render targets; LINK existing `term_block_kit`; the rest are per-channel detail in note 3 + channels sub-plans. No new term. |
| ACP / acpx (explicitly excluded path) | LINK existing `term_acp_agent_client_protocol`. No new term. |
| `thread/start` / `turn/start` / `thread/resume` (Codex protocol) | Protocol-call detail in notes 1-2; LINK `term_json_rpc`. No new term. |

**New-term candidates:** **none.** No genuinely cross-cutting, vault-reusable term lacks an existing note here.
Two terms referenced have no note (`term_codex`, `term_session`) but are NOT proposed: `codex` is a specific
plugin/runtime owned by pl02 (`oc_plugins_codex_*`) and the broader vendor model family, documented as docs not
a dictionary term per the master ownership rule; `session` is too general and is already covered by the more
specific existing notes (`term_session_data`, `term_session_persistence`, `term_sessionid`, …) plus
`repo_openclaw_sessions` — link those rather than mint a new generic `term_session`.

## Term-Note Authoring Requirements

**N/A (0 new terms).** pn01 authors zero `term_dictionary` notes; it only LINKS existing terms (inherited from
master). If augment's Step 2d re-scan surfaces a genuinely reusable cross-cutting term with no doc-page home and
best-fit `acronym_glossary_*.md` — not expected for these two design-spec pages.

## Per-Phase Validation Gate (G1-G9)

Single execution phase (3 notes, P2). Inherited verbatim from master; all gates must pass before commit.

| Gate | Name | Check |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `python3 scripts/check_yaml_frontmatter.py --path <openclaw dir>`; YAML field order, `# OpenClaw — …` H1, `## Overview` + `## Related Notes` present, footer (`**Source**`/`**Last Updated**`/`**Status**`). |
| G2 | Grounding | Diff each note against its `inbox/openclaw_docs/plan/<page>.md` source section(s); every claim traceable; verbatim code blocks. |
| G3 | Density + Coverage | ≤400 lines, ≤2,500 words, ≤6 code blocks, one building_block; every mapped H2/H3 covered (Section Coverage Map), no over-compression of the split page. |
| G4 | Cross-Reference | `## Related Notes` has ≥6 relevance-selected terms + repo_openclaw*/sibling oc_*/other vault notes, each an indexed `[text](path.md)` link with a relevance statement. |
| G5 | Ghost-reference detect + redirect | Every link target resolves in the DB; ghosts redirected or removed (run after reindex). |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` → 0 broken relative paths. |
| G7/G8 | Discoverability / in-degree ≥1 | Each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (anti-island), satisfied via `entry_openclaw_docs.md` + the inlinks below; `in_degree ≥ 1` verified post-reindex. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plan_codex_context_engine_harness_design oc_plan_codex_context_engine_harness_implementation oc_plan_ui_channels"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required H2 sections
  for sec in "## Overview" "## Related Notes"; do
    grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"
  done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density (strip YAML frontmatter before counting words)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w)
  cb=$(( $(grep -c '^```' "$f") / 2 ))
  lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code / $lines L)"
  # G4 sibling-prefix cross-ref presence (at least one oc_ sibling link expected)
  grep -q "$SIBLING_PREFIX" "$f" || echo "$n: no $SIBLING_PREFIX sibling reference found"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# After reindex: G5 ghost + G6 broken-link sweep + G8 in-degree
bash scripts/update_notes_database.sh --force
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2500w / ≤6 code / ≤400L)? |
|---|---|---|---:|---:|---|
| 1 | oc_plan_codex_context_engine_harness_design | argument | 750 | ≤3 | ✅ |
| 2 | oc_plan_codex_context_engine_harness_implementation | procedure | 800 | ≤4 | ✅ |
| 3 | oc_plan_ui_channels | argument | 700 | ≤3 | ✅ |

No note approaches the caps. The 2,712-word `codex-context-engine-harness.md` is split (notes 1+2) precisely so
each stays well under 2,500w and keeps a single BB; the 5 source fences distribute so neither note exceeds 6.
`ui-channels.md` (1,446w / 3 fences) is comfortably one note.

## Entry Point Decision (inherited from master)

Contributes **3 rows** to `entry_openclaw_docs.md` (CREATED as the W1 master pre-step before the first sub-plan
executes) under a **"Plan / Design Specs"** cluster — one row per planned note (notes 1-3). Each note receives
its entry-point back-link at finalization (this is the primary G7/G8 inbound-link source). No new entry point is
created by pn01 itself (only 3 notes; the series-level hub is the master's responsibility).

## Inlinks (existing notes -> new notes)

Candidate outside-`documentation/openclaw/` inbound links (DB-verify + add at execution for G7/G8 in-degree ≥1):

- `entry_openclaw_docs.md` (planned, master pre-step) → all 3 notes (primary anti-island source).

## Pacing Rules (inherited from master)

One execution phase; cap dynamic-workflow fan-out at ~30 agents/run; embed the per-note manifest in the
dispatch script. Re-read each source page before authoring each note; reproduce code/config blocks verbatim
(≤6/note); one building_block per note. Reindex incrementally after the phase; verify `note_links` +
0 broken links + in-degree ≥1 before commit. `git pull --rebase --autostash origin main` first; commit + push
per wave; **no Claude co-author trailer**.

## Augmentation Report (2026-06-21)

**What was locked.** Re-read both source pages under `inbox/openclaw_docs/plan/` in full and the master.
Replaced the candidate `## Candidate Cross-References` with a `## Per-Note Related Notes Mapping (LOCKED)` at
RAISED floors (≥8 terms · ≥10 snippets · ≥10 docs per note, plus 4 repos each), each link relevance-stated and
Statistics cross-ref line to the locked counts.

**Per-note locked counts (all floors MET):**

| Note | BB | Terms | Snippets | Docs (existing / planned-sibling) | Repos | Floors met |
|---|---|---:|---:|---|---:|---|
| oc_plan_codex_context_engine_harness_design | argument | 9 | 12 | 12 (7 existing / 5 planned) | 4 | ✅ ≥8t ≥10s ≥10d |
| oc_plan_codex_context_engine_harness_implementation | procedure | 9 | 12 | 11 (6 existing / 5 planned) | 4 | ✅ ≥8t ≥10s ≥10d |
| oc_plan_ui_channels | argument | 9 | 12 | 11 (6 existing / 5 planned) | 4 | ✅ ≥8t ≥10s ≥10d |

all existing-doc citations (19 distinct existing docs across cc_*/pi_*/hermes_*/band_*/aws_bedrock_agentcore_*)
existing set. `term_codex` and `term_session` confirmed ABSENT (DB MISS) — consistent with the Undigested Terms
decision (link runtime analogs, not mint generic terms). `entry_openclaw_docs.md` confirmed ABSENT (planned W1
master pre-step) — cited as the primary anti-island inbound source, not counted toward existing-doc floor.

**Step 2d new-term re-scan.** Re-read surfaced no genuinely cross-cutting, vault-reusable term lacking a home.
Vocabulary on these pages (`MessagePresentation`/`ReplyPayload.presentation`/`delivery`, `thread/start`/
`turn/start`, assemble/bootstrap/afterTurn/ingest/maintain, presentation-capabilities/auto-degrade,
Block Kit/Adaptive Cards/Carbon/Flex, `ownsCompaction`) is doc-page-owned by its home sub-plan (co02/co04,
pl02/pl04, channels) or covered by an existing term. **New-term candidates: none** (best-fit glossary N/A —
0 new captures). Undigested Terms Plan + Term-Note Authoring Requirements (N/A, 0 terms) carried forward intact.

**Adjustments vs original candidate set.** Original candidate `oc_plan_ui_channels` listed
`term_agent_orchestration`; the locked mapping keeps the more directly relevant terms (`term_channel_kernel`,
`term_messaging_gateway`, `term_hexagonal_architecture`) that match the refactor's core/edge decoupling thesis.
Added the `band/` and `aws_bedrock_agentcore/` cross-tool corpora to reach the 10-doc floor with EXISTING notes.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; each note 9 terms / 12 snippets / ≥11 docs / 4 repos, every link relevance-stated (`— … ; relevance: …`); exceeds master ≥6-term floor and the raised ≥8t·≥10s·≥10d standard. |
| CP2 | 9-GATE present per phase | **PASS** | `## Per-Phase Validation Gate (G1-G9)` table covers G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost detect+redirect, G6 Broken-link fix, G7/G8 Discoverability/in-degree≥1. Single execution phase. |
| CP3 | Entry point inherited (entry_openclaw_docs planned W1) | **PASS** | `## Entry Point Decision` contributes 3 rows to `entry_openclaw_docs.md` (CREATED at master W1 pre-step) under a "Plan / Design Specs" cluster; no per-sub-plan entry point (only 3 notes). DB-confirmed `entry_openclaw_docs` absent now (planned). |
| CP4 | Size | **PASS** | 3 planned notes ≤30 cap; each ≤2,500w / ≤6 code / ≤400L per Density Re-Assessment. |
| CP5 | Format derived | **PASS** | Format inherited verbatim from master Format Definition, derived from existing `claude_code/`+`pi/` doc corpora (`## Overview` → body → `## Related Notes` → `## References` → footer; fixed YAML field order; forbidden fields listed). |
| CP6 | Density (borderline → split) | **PASS** | codex-harness 2,712w (>2,500 cap) + mixed BB SPLIT into note 1 (argument) + note 2 (procedure) per Split Decisions; ui-channels 1,396w single coherent argument kept whole. No borderline note unaddressed. |
| CP7 | Sources measured | **PASS** | Re-measured (YAML-stripped): codex-context-engine-harness 2,653w / 5 code / 13 H2 / 17 H3; ui-channels 1,396w / 3 code / 12 H2. Within 0.7-1.3× plan estimates (2,712 / 1,446); total fences 8 matches plan. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` (10 rows, all dispositioned to existing terms or home sub-plans) + `## Term-Note Authoring Requirements` (N/A, 0 new terms, with capture-skill fallback statement) both present. |
| CP8f | Slug specificity / collision | **PASS** | 0 new term slugs to audit (Undigested Terms Plan creates none). Collision audit generalized to the 3 planned DOC notes: none duplicates an existing term/doc — `oc_plan_*` design-spec aspects have no existing equivalent; verified `term_codex`/`term_session` absent and intentionally not minted. |

**RESULT: 10/10 (CP1-CP9 incl. CP8f) PASS → READY FOR EXECUTION.**

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-21 (10/10 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |
