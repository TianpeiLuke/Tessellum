---
tags:
  - resource
  - analysis
  - synthesis
  - skill_design
  - decomposer_pipeline
  - knowledge_auto_digestion
  - architecture
  - central_design_proposal
keywords:
  - knowledge auto-digestion
  - planner-centric architecture
  - five-role pipeline
  - add-to-plan sub-skills
  - Cursus orchestration
  - context management mechanisms
  - validator criteria
  - plan-doc-as-state
  - configuration-driven
  - mitigation tiers
topics:
  - Skill Design
  - Architecture Synthesis
  - Knowledge Ingestion
  - Decomposer Pipeline
language: markdown
date of note: 2026-04-30
status: active
building_block: argument
folgezettel: "10d1e1a5"
folgezettel_parent: "10d1e1a"
---

# ★ Synthesis: A Central Design Proposal for Knowledge Auto-Digestion — Skills + Context Management + Programmatic Orchestration on a Plan-Doc-as-State Substrate

## Thesis

The four sibling notes under [FZ 10d1e1a](thought_planner_centric_paradigm_plan_as_state.md) (the planner-centric paradigm) — [FZ 10d1e1a1](thought_agentic_plan_evaluator_full_automation.md) (Evaluator role), [FZ 10d1e1a2](thought_cursus_orchestrator_for_decomposer_pipeline.md) (Cursus orchestrator), [FZ 10d1e1a3](thought_long_task_failure_modes_validator_plus_context_management.md) + [FZ 10d1e1a3a](thought_long_task_failure_modes_literature_survey.md) + [FZ 10d1e1a3b](thought_long_task_failure_modes_proposed_solution_architecture.md) (validator insufficiency + context management), and [FZ 10d1e1a4](thought_deferred_subcategory_routing_via_add_to_plan_skill.md) (deferred sub-category routing) — together specify a complete architecture for knowledge auto-digestion. This note pulls them into one canonical reference.

The architecture has three orthogonal axes — **roles**, **mechanisms**, **configurations** — each addressing a specific concern that no single axis can solve alone:

1. **Roles** (skill identities): five canonical roles (Planner, Add-to-Plan sub-skills, Evaluator, Executor, Validator) plus a sixth that addresses session boundaries (Session Resume Protocol). Each role has one responsibility; together they form the pipeline shape.
2. **Mechanisms** (context-management defenses): seven concrete defenses (M1–M7) against three systematic agent failure modes (cutting corners, not reading source, format/content degradation), composed into mitigation tiers.
3. **Configurations** (per-pipeline parameterization): one YAML configuration per source type, declaring expected BB shape, content verification tiers, sub-category routing mode, mitigation tier, FZ 7g inlink wiring policy, and the orchestrator's programmatic-vs-agentic node DAG.

The three axes share **one substrate**: the plan_doc. State updates happen *in the plan doc*, not by passing typed objects between skills. This is the structural commitment that makes the architecture coherent — every role reads the plan_doc and either appends an annotation, transforms a state field, or writes vault notes per the plan's instructions.

The contribution is the **synthesis**, not the individual pieces. Each axis was developed in dialectic with prior pieces (FZ 10d1e1 counter motivated FZ 10d1e1a; FZ 10d1e1a3 counter to FZ 10d1e1a's chained-enricher draft motivated FZ 10d1e1a3b's MVP; FZ 10b's messy-contextual-axis problem motivated FZ 10d1e1a4's deferred routing). What was discovered by exhaustive negative example is now named: **a configuration-driven, plan-centric pipeline of typed roles with explicit failure-mode defenses, deployable per source type via YAML**.

## The Architecture in One Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CONFIGURATION (one YAML per source type — wiki, paper, mtr, …)         │
│   adapter_id, fetcher, expected_bb_shape, content_verification (tiers), │
│   subcategory_routing (mode/candidates/coherence_bias/escalation),      │
│   mitigation_tier (1=MVP / 2 / 3 / 4), require_user_approval,           │
│   multi_doc_strategy (per_doc_tree | hybrid | flat_corpus),              │
│   next_step_routing, output_dir, filename_template                      │
└─────────────────────────────────────────────────────────────────────────┘
                                  ↓ instantiates pipeline
┌─────────────────────────────────────────────────────────────────────────┐
│  PLANNER  (one heavy invocation per source document, Cursus 3-phase)    │
│   Phase 1 — Initialize: load adapter contracts, ingest source content   │
│   Phase 2 — Propagate: build tree with semantic matching (FZ 7g σ),     │
│              lazy-bind cross-leaf inlink candidates                     │
│   Phase 3 — Instantiate: emit plan_doc with leaves having               │
│              {building_block, covers_source_sections, draft_body_summary,│
│               format_template, output_path: PROVISIONAL or null,         │
│               candidate_inlinks (raw)}                                  │
│   Outputs: plan_doc (the only shared artifact going forward)            │
└─────────────────────────────────────────────────────────────────────────┘
                                  ↓ plan_doc
┌─────────────────────────────────────────────────────────────────────────┐
│  ADD-TO-PLAN SUB-SKILLS  (independently invocable, additive only)       │
│   slipbox-plan-add-format       → format_template per leaf              │
│   slipbox-plan-add-routes       → para_category per leaf                │
│   slipbox-plan-add-subcategory  → second_category + final output_path   │
│                                    (NEW per FZ 10d1e1a4; deferred)      │
│   slipbox-plan-add-cross-refs   → refined FZ 7g inlink candidates       │
│   slipbox-plan-add-validation   → per-leaf validation_criteria          │
│   slipbox-plan-add-followups    → suggested followup skills             │
│                                                                         │
│   Each: reads plan_doc → appends one annotation field → writes back     │
│   Idempotent; downstream sub-skills never modify upstream's fields      │
└─────────────────────────────────────────────────────────────────────────┘
                                  ↓ plan_doc (annotated)
┌─────────────────────────────────────────────────────────────────────────┐
│  EVALUATOR  (5th role — replaces user-approval gate by default)         │
│   Reads plan_doc; runs 12 criteria:                                     │
│    C1  Coverage completeness                                            │
│    C2  BB purity                                                        │
│    C3  Atomicity (per-BB thresholds, FZ 10d1f)                          │
│    C4★ Tree well-formedness                                              │
│    C5  FZ 7g edge sanity                                                │
│    C6★ Output path validity                                              │
│    C7★ Plan provenance completeness                                      │
│    C8  Body fullness (per FZ 10d1e1a3 / 3b)                             │
│    C9  Source contact (per FZ 10d1e1a3 / 3b)                            │
│    C10 Cross-leaf quality drift                                         │
│    C11 Tier 1 dual-agreement (per FZ 10d1e1a3 M6)                       │
│    C12 Sub-category consistency (per FZ 10d1e1a4)                       │
│                                                                         │
│   ★ = critical (failure bypasses auto_revise → escalate_to_user)        │
│                                                                         │
│   Decision: approved | auto_revise (max 2 rounds) | escalate_to_user    │
└─────────────────────────────────────────────────────────────────────────┘
                                  ↓ approved
┌─────────────────────────────────────────────────────────────────────────┐
│  EXECUTOR  (per-leaf write with M1/M2/M5/M7 active per mitigation_tier) │
│                                                                         │
│  M7 Session Resume Protocol (always active):                            │
│    - acquire workspace lock                                             │
│    - per-leaf execution_state: pending → in_progress → completed        │
│    - on resume: skip already-completed leaves (verify by content_hash)  │
│                                                                         │
│  M1 Per-leaf source re-fetch (mitigation_tier ≥ 1):                     │
│    - before each leaf write, re-load relevant source spans              │
│    - log to .fetch_log.jsonl (M5)                                       │
│                                                                         │
│  M2 Batch context reset (mitigation_tier ≥ 1):                          │
│    - process leaves in batches of N (default 5)                         │
│    - between batches, fresh agent context with plan_doc summary        │
│                                                                         │
│  M5 Source-fetch audit trail (mitigation_tier ≥ 1):                     │
│    - .fetch_log.jsonl: append-only log of every source-read event       │
│                                                                         │
│  M3 Adversarial validator (mitigation_tier ≥ 2)                         │
│  M4 Cut-corner detector (mitigation_tier ≥ 3)                           │
│  M6 Two-agent pair programming for Tier 1 (mitigation_tier = 4)         │
└─────────────────────────────────────────────────────────────────────────┘
                                  ↓ written notes + updated plan_doc
┌─────────────────────────────────────────────────────────────────────────┐
│  VALIDATOR  (post-write quality gate)                                   │
│   - Reads written notes + plan_doc                                      │
│   - Runs C8/C9/C10 with stricter rubric than Evaluator (different       │
│     prompt/temperature/optionally cross-LLM-family)                     │
│   - Per-leaf: validation_state = passed | failed: <reason>              │
│   - On any failure: writes plan.validation_failures; re-invokes         │
│     Executor for the failed leaves (max 2 retry rounds) before          │
│     escalating to user                                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                  ↓ all leaves passed
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 5 — CROSS-LINK + REGISTER  (unchanged from FZ 10d1)              │
│   - Wire FZ 7g inlink candidates into actual cross-links                │
│   - Run DB incremental update (build_unified_db.py --incremental)       │
│   - Update entry-point tables (per FZ 10b BB × category routing)        │
│   - Mark plan.status = done                                             │
└─────────────────────────────────────────────────────────────────────────┘
```

## Provenance — Each Component → Source Note

| Component | Source note | What it contributed |
|---|---|---|
| **5 roles + plan-doc-as-state substrate** | [FZ 10d1e1a](thought_planner_centric_paradigm_plan_as_state.md) | Planner / Add-to-plan / Evaluator / Executor / Validator + the plan_doc as the only shared artifact |
| **Evaluator decisions: approved / auto_revise / escalate_to_user** | [FZ 10d1e1a1](thought_agentic_plan_evaluator_full_automation.md) | The 5th role + 7 base criteria (C1–C7) + automation-with-escape-hatch principle |
| **Cursus 3-phase orchestrator** (Initialize / Propagate / Instantiate) | [FZ 10d1e1a2](thought_cursus_orchestrator_for_decomposer_pipeline.md) | The Planner's internal algorithm + Resolution Engine semantic matching + Tool Library + Verification Layer mapping; YAML configurations replacing specialized skills |
| **3 failure modes (F1/F2/F3)** + 6 mitigation mechanisms (M1–M6) + 4 new criteria (C8–C11) | [FZ 10d1e1a3](thought_long_task_failure_modes_validator_plus_context_management.md) | The defensive layer — what fails and how to defend against it |
| **Literature grounding** for each M and C | [FZ 10d1e1a3a](thought_long_task_failure_modes_literature_survey.md) | Validates the mechanisms are not vault-idiosyncratic (Self-RAG, Multi-Agent Debate, MemAgent, RAGAS, RDC, Context Rot) |
| **MVP scope** (M1+M2+M5) + **M7 Session Resume** + **mitigation_tier configuration** | [FZ 10d1e1a3b](thought_long_task_failure_modes_proposed_solution_architecture.md) | Phased rollout plan + the missing 7th mechanism (workspace lock + per-leaf written_hash) |
| **Deferred sub-category routing** + **slipbox-plan-add-subcategory** + **C12** | [FZ 10d1e1a4](thought_deferred_subcategory_routing_via_add_to_plan_skill.md) | Resolves FZ 10b1b5's messy-contextual-axis problem by deferring the decision to the add-to-plan stage |

The synthesis reads cleanly: roles + sub-skills come from FZ 10d1e1a; the evaluator gate from FZ 10d1e1a1; the orchestrator pattern from FZ 10d1e1a2; the failure-mode defenses from the FZ 10d1e1a3 family; one new add-to-plan sub-skill from FZ 10d1e1a4. The architecture's coherence is the ★ contribution; no single piece is novel in isolation.

## Three Axes, Three Concerns

### Axis 1 — Roles (skill identities)

Five canonical roles + one infrastructure protocol:

| Role | Responsibility | Number of skills | Invocation cardinality |
|---|---|---|---|
| Planner | Build the tree with full source context in one heavy pass | 1 (`slipbox-decomposer-orchestrator`) | One per corpus |
| Add-to-Plan Sub-Skills | Append annotations to plan_doc fields | 6 today, extensible (`-format`, `-routes`, `-subcategory`, `-cross-refs`, `-validation`, `-followups`) | Each runs once per plan; can be re-invoked |
| Evaluator | Decide if plan is ready for execution (12 criteria → approved / auto_revise / escalate) | 1 (`slipbox-evaluate-plan`) | Once per plan; max 2 auto_revise rounds |
| Executor | Walk the tree, write vault notes per the plan | 1 (`slipbox-execute-plan`) | Once per batch (M2 batch reset); resumes via M7 |
| Validator | Post-write quality gate (12 criteria, stricter rubric than Evaluator) | 1 (`slipbox-validate-plan`) | Once per plan after execution; can re-invoke Executor for failed leaves |
| **M7 Session Resume Protocol** (infrastructure) | Workspace lock + per-leaf written_hash for crash-safe resume | Library function used by Executor | Always active |

This is a **closed taxonomy** of roles. New skills don't break the architecture; they fit into existing slots (a new add-to-plan sub-skill, a new format template in the Tool Library, a new mitigation tier).

### Axis 2 — Mechanisms (context-management defenses)

Seven mechanisms defending against three failure modes, organized into mitigation tiers:

| Tier | Mechanisms enabled | Defends | Cost |
|---|---|---|---|
| **0 (legacy)** | None — the today behavior of the 12 specialized digest skills | Nothing systematic | Lowest, but high failure rate on long corpora |
| **1 (MVP)** | M1 source re-fetch + M2 batch reset + M5 fetch audit + M7 session resume + Validator C8/C9 | F1/F2/F3 with 80% coverage; session-end failures recover all in-flight work | Moderate (~3 weeks to build; +30-50% token cost per leaf) |
| **2 (Adversarial)** | + M3 adversarial validator with separate context + Validator C10 cross-leaf drift | Catches what MVP misses (corpus-level quality drift, sophisticated paraphrase) | + ~$0.10 per validation pass; +1 week to build |
| **3 (Cut-corner)** | + M4 per-leaf token-budget cut-corner detection | Catches "structurally complete but suspiciously thin" leaves | + minimal cost; +3 days to build |
| **4 (Tier 1 hardening)** | + M6 two-agent pair programming for Tier 1 verbatim content + Validator C11 | Hardens highest-stakes verbatim content (code blocks, equations, version numbers) | + 100% LLM cost on Tier 1 spans; +2 weeks to build |

Tier escalation is **per-corpus**, not global — the configuration declares which tier to use per source type. A paper digest may run at tier 1 (well-shaped, low blast radius); a wiki-site digest of production runbooks may run at tier 4 (heterogeneous + high blast radius).

### Axis 3 — Configurations (per-pipeline parameterization)

One YAML file per source type declares everything that varies across pipelines:

```yaml
# scripts/decomposer/configs/wiki_site.yaml
adapter_id: wiki_site
fetcher: ReadInternalWebsites
discover_subpages: regex_w_amazon_links
expected_bb_shape: dynamic                           # planner classifies per page
multi_doc_strategy: hybrid                           # corpus root + per-page sub-trees
corpus_root_filename: "tutorial_{prefix}_index.md"

content_verification:
  - {tier: 1, fields: [code_blocks, command_line_examples, config_snippets]}
  - {tier: 2, fields: [section_titles, step_instructions, faq_questions]}
  - {tier: 3, fields: [yaml_keywords, tutorial_structure_table]}

subcategory_routing:
  mode: deferred                                     # FZ 10d1e1a4
  candidate_subcategories: [tutorials, how_to, policy_sops, faqs]
  use_corpus_coherence_bias: true
  min_confidence_for_auto_route: 0.6
  on_low_confidence: escalate_to_user

mitigation_tier: 2                                   # FZ 10d1e1a3b
require_user_approval: true                          # multi-page sources are unpredictable

next_step_routing:
  on_success: [slipbox-add-inlinks]

para_category: resource                              # planning-time decision
output_dir: resources/documentation/                 # base; subcategory_routing refines
filename_template: "tutorial_{prefix}_{doc_slug}_{nn}_{leaf_name}"
```

The 12 specialized digest skills (`-paper`, `-wiki-site`, `-mtr-quip`, `-oncall-quip`, `-newsflash-quip`, `-external`, `-ruleset`, `-launch-announcement`, `-table-update-email`, `-reorg-announcement`, `-team-flash`, `-decompose-note`) collapse to 12 YAML configurations. New input types add 30-line YAMLs, not 150-line skill files.

## Why This Synthesis Is the Right Shape

Three architectural-coherence checks the synthesis passes:

### 1. Single Substrate (plan-doc-as-state)

Every role reads from and writes to the plan_doc. There are no out-of-band shared state objects, no in-memory typed dicts threaded between sub-skills, no implicit handshakes. The plan_doc IS the state machine; its YAML schema (v3.0) is the typed contract.

This was the load-bearing decision from [FZ 10d1e1a](thought_planner_centric_paradigm_plan_as_state.md), originally motivated by [FZ 10d1e1's counter](counter_pipeline_of_skills_breaks_context.md) that "context information is not breakable without semantic loss." The plan_doc preserves what threading-typed-state cannot — the planner's accumulated source-reading context, in prose form, in the `Source Context` section.

### 2. Closed Role Taxonomy + Open Sub-Skill Set

There are exactly five canonical roles (Planner, Add-to-Plan sub-skills *as a class*, Evaluator, Executor, Validator) plus one protocol (M7). New skills don't add roles — they slot into the Add-to-Plan class as additional annotations on existing leaves.

This passes the "what if we need a new feature?" test: every plausible new feature (e.g., "automatically suggest related vault notes for cross-reference") is an add-to-plan sub-skill (`slipbox-plan-add-related-notes`), not a new role. The architecture stays five roles wide regardless of how many sub-skills accumulate.

### 3. Configuration ≠ Code

Source-type-specific behavior is in YAML, not Python. The orchestrator (Planner role) reads the configuration and parameterizes its 3-phase algorithm. Adding a `slipbox-digest-pdf-book` adapter is editing one YAML, not writing one skill.

This passes the "compression ratio" test: 12 specialized skills × ~150 LOC = ~1,800 LOC today; the synthesis target is 12 YAML × ~30 LOC + 1 orchestrator × ~250 LOC = ~610 LOC. ~3× compression, confirmed by the same pattern Cursus achieves on SageMaker pipelines (4-6 weeks → minutes-of-spec).

## Implementation Roadmap

Six phases tracking the implementation cost of each piece:

### Phase A — Plan-Doc-as-State Foundation (1 week)

Build the plan_doc schema v3.0 reader/writer library + workspace lock + per-leaf execution_state field. Nothing new behavioral; this is infrastructure for everything else.

**Deliverables**: `scripts/decomposer/plan_spec_io.py`, `scripts/decomposer/lock.py`, plan_doc schema docs.

### Phase B — Planner + Executor MVP (2 weeks)

Implement the Planner skill (Cursus 3-phase) with a hardcoded path for paper-digest as the v0 adapter. Implement the Executor with M7 session resume + M1 source re-fetch + M5 fetch audit + M2 batch context reset.

**Deliverables**: `scripts/decomposer/orchestrator.py`, `scripts/decomposer/executor.py`, `scripts/decomposer/source_refetch.py`, `scripts/decomposer/source_cache.py`, `scripts/decomposer/fetch_audit.py`. End-to-end works for paper digestion.

### Phase C — Configurations + Tool Library (1 week)

Migrate paper-digest's behavior into a YAML configuration. Build the Tool Library as in-vault `procedure` notes under `resources/skills/templates/`. Add a second adapter (wiki-site) by writing only a YAML config.

**Deliverables**: `scripts/decomposer/configs/paper.yaml`, `scripts/decomposer/configs/wiki_site.yaml`, Tool Library notes; `slipbox-tool-library-add` skill.

### Phase D — Evaluator + Validator (1 week)

Implement Evaluator with criteria C1–C9 (skipping C10/C11/C12 which require Phase E). Implement Validator with the same criteria but stricter rubric.

**Deliverables**: `scripts/decomposer/evaluator.py`, `scripts/decomposer/validator.py`, criterion implementations. End-to-end with full automation pathway (no user-approval gate by default).

### Phase E — Add-to-Plan Sub-Skills (2 weeks)

Build the 6 add-to-plan sub-skills, including `slipbox-plan-add-subcategory` (FZ 10d1e1a4). Add C12 (sub-category consistency) to Evaluator + Validator.

**Deliverables**: 6 sub-skill scripts, full add-to-plan pipeline operational.

### Phase F — Mitigation Tier Escalations (3 weeks)

Implement M3 adversarial validator + C10 (tier 2). Implement M4 cut-corner (tier 3). Implement M6 two-agent pair programming + C11 (tier 4).

**Deliverables**: tier 2/3/4 mitigation infrastructure; per-config `mitigation_tier` setting wired through.

**Total**: 10 weeks for the full system. MVP (Phases A–C) delivers in 4 weeks and is independently usable.

## What This Synthesis Is NOT Claiming

- **Not** that this architecture is the final word. Open questions OQ44–OQ115 (across the source notes) catalog 70+ unresolved design decisions.
- **Not** that the existing 12 specialized digest skills should be deleted before Phase F completes. They keep working through the migration; configurations replace them only after the infrastructure is operational.
- **Not** that all decomposer skills should be subsumed. Skills with high blast radius (touching production paths) remain user-approval-gated indefinitely; the Evaluator's `escalate_to_user` decision keeps them human-in-the-loop.
- **Not** that the architecture eliminates LLM hallucination or content drift. M1–M7 reduce failure rates; they do not eliminate them. Sample-based human audit ([FZ 10d1e1a1](thought_agentic_plan_evaluator_full_automation.md) counter-consideration #4) remains the final calibration.
- **Not** independent of the FZ 10b mapping or the FZ 7g ontology. Both are *upstream substrates* this architecture builds on; this note does not replace either.

## Open Questions (Residual After Synthesis)

The synthesis closes some open questions from the source notes (e.g., the role taxonomy is now decided; the 5 + 1 structure is fixed). These remain genuinely open:

| # | Open Question | Source |
|---|---|---|
| **OQ116** | Is the Tool Library best stored as in-vault `procedure` notes (dogfoods typed-substrate thesis, FZ 10d1e1a2 OQ89) or as YAML files (simpler tooling)? Can it be both — `procedure` notes that compile down to YAML at runtime? |  |
| **OQ117** | The Planner's prompt at full corpus + 8 sub-tasks + response format may exceed context limits at very large corpora (>50 documents). Is corpus-chunking-with-summarization the right escape, or should there be a meta-Planner that decomposes the corpus into sub-corpora first? | FZ 10d1e1a2 OQ91 |
| **OQ118** | When Add-to-Plan sub-skills are run in parallel (e.g., format + cross-refs + subcategory all running on the same plan_doc), how are concurrent writes to the plan_doc resolved? File-level locks would serialize; field-level CRDT-style merges allow parallel but add complexity. | New |
| **OQ119** | The architecture has 12 criteria (C1–C12). What's the natural growth ceiling? At 20 criteria the Evaluator's prompt becomes unwieldy. Should related criteria be grouped into "criterion families" (structural / semantic / quality / faithfulness) and reported in aggregate? | New |
| **OQ120** | M1 + M2 + M5 + M7 covers the MVP. Will real-corpus deployment surface failure modes M3–M6 don't address? Need to instrument the MVP to detect "novel failure mode" signals. | New |
| **OQ121** | The configurations parameterize behavior; the Tool Library parameterizes *content*. Is there a third layer — a "Decision Library" that parameterizes the Evaluator's per-criterion thresholds per-corpus? Today thresholds are hardcoded in scripts. | New |

## Related Notes

### Folgezettel Trail
- **Parent [FZ 10d1e1a]**: [Planner-Centric Paradigm](thought_planner_centric_paradigm_plan_as_state.md) — the foundation; this synthesis consolidates its four sibling extensions
- **Sibling [FZ 10d1e1a1]**: [Agentic Plan Evaluator](thought_agentic_plan_evaluator_full_automation.md) — Evaluator role + first 7 criteria
- **Sibling [FZ 10d1e1a2]**: [Cursus-Style Orchestrator](thought_cursus_orchestrator_for_decomposer_pipeline.md) — 4-subsystem orchestrator + YAML-configuration pattern
- **Sibling [FZ 10d1e1a3]** + [FZ 10d1e1a3a](thought_long_task_failure_modes_literature_survey.md) + [FZ 10d1e1a3b](thought_long_task_failure_modes_proposed_solution_architecture.md): Failure modes + mechanisms M1–M7 + criteria C8–C11 + tier escalation
- **Sibling [FZ 10d1e1a4]**: [Deferred Sub-Category Routing](thought_deferred_subcategory_routing_via_add_to_plan_skill.md) — the 7th add-to-plan sub-skill + criterion C12

### Upstream Substrates (this architecture stands on these)
- **[FZ 7](thought_atomicity_as_universal_scaling_principle.md)**: Atomicity as universal scaling principle — the "one BB per leaf" rule
- **[FZ 7g](thought_building_block_ontology_relationships.md)**: BB ontology with 10 directed edges — the FZ 7g semantic matching σ runs on
- **[FZ 9](analysis_cursus_innovations_and_generalizability.md)** + [FZ 9f4](analysis_cursus_as_agentic_system_architecture.md): Cursus 4-subsystem TSA pattern — the orchestrator's algorithmic spine
- **[FZ 10b](thought_bb_category_directory_mapping.md)**: BB × category × directory mapping — the routing reference table
- **[FZ 10c1b1](thought_classify_bb_para_synthesis.md)**: Classify = BB + PARA — the two-axis classification this architecture splits across stages

### What Remains To Build
- 7 new scripts (Phases A–B): plan_spec_io, lock, orchestrator, executor, source_refetch, source_cache, fetch_audit
- 12 YAML configurations (Phase C): one per existing digest skill family
- Tool Library: in-vault `procedure` notes for per-BB format templates
- 6 add-to-plan sub-skills (Phase E)
- Evaluator + Validator skills (Phase D)
- Mitigation tier 2/3/4 infrastructure (Phase F)
- ~1,500 LOC total

### Entry Points
- [Folgezettel Trails Master Index](../../0_entry_points/entry_folgezettel_trails.md) — this note is FZ 10d1e1a5
- [Knowledge Ingestion Automation](../../0_entry_points/entry_knowledge_ingestion_automation.md) — Trail 10 entry; ★ this synthesis is the canonical Trail 10 design reference

---

**Last Updated**: 2026-04-30
