---
tags:
  - project
  - plan
  - tessellum
  - dks
  - meta_dks
  - validation
  - dialectic
keywords:
  - meta-DKS validation
  - dogfood meta-DKS
  - LLM-driven proposer
  - meta-cycle attack stage
  - composer skill canonical for meta-DKS
  - bb_schema_version auto-population
  - tessellum bb migrate
  - BBGraph unrealised-edge integration
topics:
  - Dialectic Knowledge System
  - Meta-DKS
  - System Design
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
---

# Plan — Validate Meta-DKS on Real Telemetry, Then Backfill the Phase 9 Deferrals

## Problem

v0.0.52 shipped Phase 9 of `plan_dks_expansion.md` — the meta-DKS schema-mutation runtime. The mechanism is in place (event-sourced schema, META_SCHEMA, MetaCycle, the `--meta` CLI mode, cold-start guard, migration notes), but as a *deployable* runtime meta-DKS is a skeleton:

| Surface | v0.0.52 | What's missing |
|---|---|---|
| Proposal generator | rule-based lookup table mapping Toulmin component → schema edge | No LLM-driven proposer; can't reason about novel failure modes |
| Survive stage (attack) | pass-through — every well-formed proposal survives | No dialectical attack; meta-cycle's *dialectical* nature is documentation, not mechanism |
| Composer skill | not authored | No canonical to invoke meta-DKS from a Composer prompt graph |
| `bb_schema_version` field | spec'd, defaulted to 1, but not auto-populated | D8 frozen-at-creation discipline isn't yet enforced on capture |
| `tessellum bb migrate` | not implemented | No way to query "which corpus edges are invalid under the current schema?" |
| `unrealised_schema_edges` in MetaObservation | empty tuple | Heuristic-2 (retract-unused-edge) is inert; no corpus-side signal flowing in |

Before continuing to Phase 10 (multi-perspective DKS + Dung labelling, already specced in `plan_dks_expansion.md`), three things should happen in order:

1. **Validate** that the v0.0.52 mechanism produces useful proposals on *real* DKS telemetry, not synthesised fixtures.
2. **Backfill** the polish that makes meta-DKS practically deployable.
3. **Advance** to Phase 10 (deferred to the existing plan; not duplicated here).

The cost of skipping (1) is that we might build the LLM-driven proposer in (2) on top of a mechanism whose blind spots we haven't found. The cost of skipping (2) is that meta-DKS ships but no one uses it. The plan below addresses both before adding new surface area.

## What meta-DKS is now (v0.0.52 baseline)

| Layer | Module | Status |
|---|---|---|
| Event-sourced schema (D3) | `tessellum.bb.types` (SchemaEditEvent, fold_schema_events, BB_SCHEMA_USER_EXTENSIONS, BB_SCHEMA_VERSION) | ✓ shipped v0.0.52 |
| Meta-meta-schema (D4) | `tessellum.dks.meta.types` (META_SCHEMA — 5 states, 4 transitions) | ✓ shipped v0.0.52 |
| MetaObservation | `tessellum.dks.meta.types` | ✓ shipped — `unrealised_schema_edges` always empty |
| SchemaEditProposal | `tessellum.dks.meta.types` | ✓ shipped |
| MetaCycle runtime | `tessellum.dks.meta.runtime` (4 stages: build → filter → survive → emit) | ✓ shipped — heuristic build; pass-through survive |
| Heuristic proposer | `_TOULMIN_TO_PROPOSED_EDGE` lookup table | ✓ shipped — 3 mappings (warrant, counter-example, premise) |
| Event log JSONL I/O | `load_event_log` / `write_event_log` | ✓ shipped |
| CLI — `tessellum dks --meta` | `--apply / --min-cycles / --target-failure / --format json` | ✓ shipped |
| Migration note authoring | `_write_migration_note` in CLI | ✓ shipped — minimal template |
| FZ 2c1 design synthesis | `thought_meta_dks_design.md` | ✓ shipped |
| **Composer skill canonical** | `skill_tessellum_meta_dks_cycle.md` | not authored |
| **LLM-driven proposer** | replaces heuristic table with LLM call | not implemented |
| **Attack stage** | dialectical counter-argument generation against proposals | not implemented (pass-through) |
| **`bb_schema_version` capture** | auto-populated on note write | not implemented |
| **`tessellum bb migrate`** | retroactive corpus validation | not implemented |
| **`unrealised_schema_edges` population** | from BBGraph | empty tuple |

## Design principles inherited from prior plans

1. **Telemetry first, optimisation second** (from `plan_dks_expansion.md` §Design Principles). Validation lands before the LLM proposer; the validation findings inform the LLM proposer's prompt design.
2. **Schema edits follow R-P discipline.** Phase 9 already enforces this for cycle-level edits; the LLM-driven proposer must produce evidence-grounded proposals, not stylistic ones.
3. **Public API is stable.** v0.0.52's `MetaObservation` / `SchemaEditProposal` / `MetaCycle` shapes don't change. The LLM proposer and attack stage slot in via composition, not replacement.
4. **Frozen-at-creation `bb_schema_version` (D8)** ships incrementally — auto-population first, then the migrate command. The mechanism in v0.0.52 was field-level; v0.0.53 wires it into capture.
5. **Validation is itself a vault note.** Phase V's findings live at FZ 2c1a (child of 2c1), so future agents reading the trail see *what meta-DKS actually proposed against real telemetry* alongside the design.

## Resolved decisions (5 questions → 5 decided)

| # | Question | Resolution | Rationale |
|---|----------|------------|-----------|
| **V-1** | Generate validation telemetry with Anthropic backend or MockBackend? | **Anthropic backend** | Mock cycles produce trivial / scripted Toulmin distributions; the whole point of validation is seeing the heuristic against *naturally occurring* failure shapes. Estimated cost ≤ $5 for the 20+ cycles needed. |
| **V-2** | What observations to feed the validation run? | **Tessellum vault dogfood**: ~25 observations sourced from the project's own vault (FZ trail summaries, open questions, recent COE incidents, real PR review surfaces) | Dogfooding closes the loop — the slipbox reasons over the slipbox. Also keeps the observation curation reproducible (the source files don't change between runs). |
| **B-1** | Where does the LLM-driven proposer live? | **`tessellum.dks.meta.runtime.LLMProposer`** — a strategy class that `MetaCycle` accepts via constructor; default falls back to today's heuristic | Composition, not replacement. Tests can keep using the heuristic; production can swap in the LLM proposer; both code paths exercised. |
| **B-2** | Should the attack stage be a separate class or a method on MetaCycle? | **Separate `MetaAttacker` strategy** (parallel to `LLMProposer`) | Same composition argument as B-1. Lets tests keep pass-through behaviour while production uses LLM-driven attack. |
| **B-3** | Should `bb_schema_version` auto-population happen in `tessellum capture` or in the validator? | **Capture-side**, written as YAML frontmatter at write time | D8 specifies frozen-at-creation; capture is the only write path where "creation time" is well-defined. The validator only *reads* the field. |

## The three phases

### Phase V — Validate (v0.0.53.dev) — small, mostly dogfooding

**Goal:** prove that the v0.0.52 mechanism produces useful proposals on real telemetry, and that the proposals it does produce actually address the right failure modes. The output is *evidence*, not code.

**Deliverables:**

- **Validation observation set** — `runs/dks/validation_v0_0_53/observations.jsonl`, ~25 observations curated from the Tessellum vault. Each entry has `{summary, source_fz_or_file}`. Reproducible: the curation script reads from a fixed list of source paths.
- **Validation telemetry** — run `tessellum dks observations.jsonl --backend anthropic --runs-dir runs/dks/validation_v0_0_53/` against the set. Cap at 25 cycles. Cost: ≤ $5.
- **Meta-DKS dry run + apply** — run `tessellum dks --meta --runs-dir runs/dks/validation_v0_0_53/` (dry run) and `--apply` (the real edit). Inspect what got proposed.
- **Validation note (FZ 2c1a)** — `vault/resources/analysis_thoughts/thought_meta_dks_validation_v053.md`. Documents:
  - The 25-observation set + its provenance
  - The Toulmin failure distribution that actually emerged (vs the synthesised distributions in tests)
  - Which proposals the heuristic fired, and whether each looks right on inspection
  - Discovered blind spots: what failure shapes the lookup table *should* catch but doesn't
  - Recommendations for the LLM-driven proposer's prompt design (Phase B-2)
- **Smoke-test fixture** — copy the validation cycle traces to `tests/fixtures/dks_meta/validation_v053/` (anonymised if needed). The Phase B LLM proposer tests can replay against this real-shaped data, not handwritten counters.

**What this phase doesn't do:**

- Doesn't change any code outside curation scripts + the validation note.
- Doesn't tune the heuristic table — that's a Phase B decision informed by what V finds.
- Doesn't run multi-cycle DKS against the *full* Tessellum vault — capped at 25 observations for cost containment.

**Decisions:**

- **V-1, V-2** above.
- Curation script lives at `scripts/curate_validation_observations.py` (Tessellum, not vault); deterministic given the source-file list.

**Exit criteria:**

- The validation note documents at least one of: (a) "the heuristic fires correctly on the dominant failure shape; ship Phase B as planned," or (b) "the heuristic misses failure shape X; LLM proposer prompt should explicitly handle X." Both are valid outcomes — V exists to discover, not to bless.

---

### Phase B — Backfill (v0.0.53) — medium

**Goal:** turn meta-DKS from skeleton to deployable. Six deferred items from Phase 9, sequenced by what unblocks what.

#### B.1 — Composer skill canonical for the meta-cycle (~150 LOC vault content)

`vault/resources/skills/skill_tessellum_meta_dks_cycle.md` + sidecar JSON. Parallel to today's `skill_tessellum_dks_cycle.md` but with 4 meta-prompts (proposing / attacking / aggregating / landing) instead of 5 cycle prompts. The skill becomes the canonical for B.2 + B.3 to call into.

Per the [Capture-skill-canonical feedback](../../../memory/feedback_use_capture_skill_canonical_for_vault_notes.md) — read `skill_slipbox_capture_skill_note.md` BEFORE writing.

#### B.2 — LLM-driven proposer (~200 LOC + tests)

- New `LLMProposer` strategy class in `tessellum.dks.meta.runtime`. Constructor takes an `LLMBackend`; method `generate_proposals(observation: MetaObservation) -> list[SchemaEditProposal]`.
- Prompt sourced from the skill canonical's "proposing" step. Schema-validated JSON output (claim, edge source/target/label, motivating_observation, expected_impact).
- `MetaCycle` accepts an optional `proposer` kwarg; defaults to today's heuristic (`HeuristicProposer`, refactored from `_generate_proposals`).
- CLI: new `--proposer {heuristic,llm}` flag on `tessellum dks --meta`. LLM mode requires `--backend anthropic` to be set.
- Tests: mock-backend smoke test that proposer returns well-formed `SchemaEditProposal`s; replay against the Phase V fixture and assert proposal count + edge shapes match expectations.

#### B.3 — True dialectical attack stage (~250 LOC + tests)

- New `MetaAttacker` strategy class. Constructor takes an `LLMBackend`; method `attack(proposal: SchemaEditProposal, observation: MetaObservation) -> list[MetaCounterArgument]`. New dataclass `MetaCounterArgument` (parallel to `DKSCounterArgument`): names which aspect of the proposal is weak (insufficient evidence / overgeneralisation / collides with declared edge / etc).
- New `MetaCycle._survive_proposals(proposals, attacks) -> list[SchemaEditProposal]`: aggregates per-proposal attacks, survives iff defenses outweigh attacks (initial heuristic: `len(defenses) > len(attacks)` per proposal; refine after Phase V findings).
- CLI: `--attacker {none,llm}` flag; `none` is today's pass-through behaviour.
- Tests: a proposal with 3 attacks + 1 defense is filtered out; a proposal with 0 attacks survives; the survive stage's output count ≤ build stage's output count.

#### B.4 — `bb_schema_version` auto-population (~80 LOC + tests)

- Modify `tessellum.capture` to write `bb_schema_version: <int>` into YAML frontmatter at note creation. Source the int from `tessellum.bb.types.BB_SCHEMA_VERSION` (live value, not the package alias — per the [import-aliasing quirk noted in v0.0.52](../vault/resources/analysis_thoughts/thought_meta_dks_design.md)).
- TESS-001 / TESS-003 / TESS-005 validators: when checking BB-pair validity, prefer the note's `bb_schema_version` if present; fall back to current `BB_SCHEMA_VERSION` if absent (back-compat for v0.0.52-era notes).
- Tests: capture writes the field; validator reads from the field; missing-field notes don't error.

#### B.5 — `tessellum bb migrate` retroactive validation (~250 LOC + tests)

- New CLI subcommand `tessellum bb migrate [--target-version current] [--apply] [--format human|json]`.
- Dry run: lists every note whose recorded `bb_schema_version` < `BB_SCHEMA_VERSION` and whose body links would fail TESS-005 under the current schema. Reports counts + per-note diff.
- `--apply`: bumps the recorded version on notes that pass current TESS-005 (passive migration). Notes that *don't* pass under the current schema get a separate `--apply --rewrite-links` flow (manual review required for retargeting).
- Tests: synthetic vault with mixed-version notes; dry-run reports the right count; `--apply` updates versions; `--rewrite-links` errors when not confirmed.

#### B.6 — BBGraph integration in MetaObservation (~120 LOC + tests)

- Modify the CLI's `_run_dks_meta` to query `BBGraph.from_db()` (already available since v0.0.51) for unrealised schema edges. An edge is unrealised iff no corpus `BBEdge` instance matches its `(source_type, target_type, label)`.
- Populate `MetaObservation.unrealised_schema_edges` with the result.
- Activates Heuristic-2 (retract-unused-edge) in `MetaCycle._generate_proposals`. The ≥50-cycle gate stays — even with corpus-side signal, we don't retract from sparse evidence.
- Tests: synthetic BBGraph with 1 declared edge and 0 instances → unrealised list contains the edge; with 1 instance → empty list.

**Deliverables summary:**

| Item | Type | LOC | Depends on |
|---|---|--:|---|
| B.1 skill canonical | vault content | ~150 | Phase V findings |
| B.2 LLM proposer | code + tests | ~200 | B.1 |
| B.3 attack stage | code + tests | ~250 | B.1 |
| B.4 `bb_schema_version` capture | code + tests | ~80 | — |
| B.5 `tessellum bb migrate` | code + tests | ~250 | B.4 |
| B.6 BBGraph integration | code + tests | ~120 | — |
| **Total** | | **~1050 LOC** | |

**What this phase doesn't do:**

- Doesn't change `META_SCHEMA` — it stays human-authored per D4.
- Doesn't change `SchemaEditEvent` / `fold_schema_events` — v0.0.52's event-sourcing primitives are stable.
- Doesn't change the cold-start guard threshold (`DEFAULT_MIN_CYCLES = 20`). Phase V might recommend a different value; if so, that's a config tweak, not a code change.
- Doesn't add `bb migrate --rewrite-links` automation. Manual review only — retargeting links is a content decision, not a mechanism one.

**Decisions:**

- **B-1, B-2, B-3** above.
- LLM-driven proposer + attacker reuse `tessellum.composer.AnthropicBackend` — no new LLM client layer.
- Schema event log path stays `runs/dks/meta/schema_events.jsonl` — unchanged from v0.0.52.

**Exit criteria:**

- v0.0.53 ships with: composer skill canonical authored; LLM proposer + attacker behind `--proposer llm` / `--attacker llm` CLI flags; `bb_schema_version` auto-populated on new captures; `tessellum bb migrate` working in dry-run mode; unrealised-edge signal flowing into MetaObservation.
- Full pytest suite green. Clean-venv wheel smoke covers `tessellum dks --meta --proposer llm` import path.
- CHANGELOG documents the Phase V findings (one-paragraph summary) inline with the Phase B entry, so the *why* of B.2's prompt design is preserved.

---

### Phase A — Advance (v0.0.54) — deferred to existing plan

Phase 10 of `plan_dks_expansion.md` (Multi-perspective debate + Dung labelling) is already specced and not duplicated here. Sequencing: after v0.0.53 ships with validated, LLM-driven meta-DKS, the multi-perspective expansion becomes the next phase. Phase 10's `WarrantChange` aggregation stratified by perspective will feed naturally into the LLM-driven proposer from B.2 — meta-DKS will receive per-perspective Toulmin distributions and can propose perspective-specific schema edits.

The only Phase 10 surface that interacts with this plan is **OQ-2c1-c** (from the FZ 2c1 design note): *how does meta-DKS interact with multi-perspective?* Answer becomes: MetaObservation grows a per-perspective stratification; LLM proposer's prompt is amended to surface stratified failure modes; otherwise mechanism is unchanged.

## Integration points across phases V + B

| Subsystem | Phase V | Phase B |
|-----------|---------|---------|
| `tessellum.bb` | unchanged | B.4: `bb_schema_version` field becomes capture-default |
| `tessellum.bb.graph` | unchanged | B.6: queried for unrealised-edge signal |
| `tessellum.dks.meta` | unchanged | B.2 + B.3: new `LLMProposer`, `MetaAttacker`, `MetaCounterArgument`; `MetaCycle` accepts strategy kwargs |
| `tessellum.cli.dks` | unchanged | B.2: `--proposer` flag; B.3: `--attacker` flag |
| `tessellum.cli.bb` | unchanged | B.5: new `tessellum bb migrate` subcommand |
| `tessellum.capture` | unchanged | B.4: writes `bb_schema_version` to frontmatter |
| `tessellum.composer` | invoked via `--backend anthropic` for V's cycle run | B.2 + B.3: `AnthropicBackend` used by `LLMProposer` + `MetaAttacker` |
| `tessellum.format.validator` | unchanged | B.4: TESS-005 reads `bb_schema_version` if present |
| `vault/resources/skills/` | unchanged | B.1: new `skill_tessellum_meta_dks_cycle.md` + sidecar |
| `vault/resources/analysis_thoughts/` | V: new `thought_meta_dks_validation_v053.md` (FZ 2c1a) | unchanged |
| `tests/` | V: new `fixtures/dks_meta/validation_v053/` | B.2/B.3: smoke + CLI tests; B.5: CLI tests; B.6: smoke tests |
| `runs/dks/` | V: new `validation_v0_0_53/` directory | unchanged |
| `seed manifest` | V: add thought_meta_dks_validation_v053.md | B.1: add skill_tessellum_meta_dks_cycle.md |

## Open questions

| # | Question | Lean |
|---|----------|------|
| **OQ-V-a** | Should the validation observation set be regenerated each release, or frozen as a v0.0.53 artifact? | Frozen — reproducibility matters more than freshness; later versions can curate a v0.0.54+ set when their scope demands it. |
| **OQ-V-b** | What if Phase V's findings contradict the v0.0.52 heuristic design? | Document in the validation note + amend Phase B's deliverables. The plan is *informed by* V, not *blocked by* V. |
| **OQ-B-c** | Should `LLMProposer` and `MetaAttacker` use the same `LLMBackend` instance or separate instances? | Same — one Anthropic key, one rate limit budget. Multiple instances are a v0.3+ optimisation. |
| **OQ-B-d** | Should the survive heuristic in B.3 (`len(defenses) > len(attacks)`) be configurable? | Yes — add `--survive-threshold {majority,strict,permissive}` after Phase V findings show whether the simple count is enough. Default `majority` for v0.0.53. |
| **OQ-B-e** | What does `tessellum bb migrate --apply` do with notes that *can't* be passively migrated? | Skip + report. Manual review path via `--rewrite-links` in a future version; v0.0.53 reports them but doesn't auto-rewrite. |

## What this plan does NOT do

- **No new resolved decisions for Phase 10.** Phase 10 keeps its plan_dks_expansion specification. This plan only touches the OQ-2c1-c interaction point (multi-perspective × meta-DKS).
- **No tests-only release.** Phase V's exit produces a *vault note* and a *fixture*, but no version bump. v0.0.53 ships with V + B together; V is a prerequisite, not a release.
- **No retroactive corpus rewrites.** `bb migrate --rewrite-links` is explicitly deferred. Any corpus retargeting is manual.
- **No reinforcement learning over the proposer or attacker.** Same scope as Phase 10's exclusion of perspective-set RL — this is a v0.3+ research direction.
- **No public-API breakage.** v0.0.52's exports (`MetaCycle`, `MetaObservation`, `SchemaEditProposal`, etc.) all stay; B.2 + B.3 add new strategy classes via composition.

## Sequencing summary

```
v0.0.52  ┌─ Phase 9 SHIPPED (mechanism)
         │
         │   Phase V — Validate
v0.0.53  │   ├─ curate 25-obs validation set
.dev     │   ├─ run real DKS cycles (Anthropic backend, ≤$5)
         │   ├─ run --meta against produced telemetry
         │   ├─ author FZ 2c1a validation note
         │   └─ freeze cycle traces as tests/fixtures/dks_meta/validation_v053/
         │
v0.0.53  │   Phase B — Backfill
         │   ├─ B.1 composer skill canonical
         │   ├─ B.2 LLM-driven proposer
         │   ├─ B.3 dialectical attack stage
         │   ├─ B.4 bb_schema_version auto-population
         │   ├─ B.5 tessellum bb migrate
         │   └─ B.6 BBGraph → unrealised_schema_edges
         │
v0.0.54  └─ Phase 10 (see plan_dks_expansion.md §Phase 10)
            multi-perspective DKS + Dung grounded labelling
```

## Related notes

- **Parent plan**: [`plan_dks_expansion`](plan_dks_expansion.md) — this plan's Phases V + B sit between its Phase 9 (shipped v0.0.52) and Phase 10 (v0.0.54).
- **FZ 2c1**: [`thought_meta_dks_design`](../vault/resources/analysis_thoughts/thought_meta_dks_design.md) — the design synthesis whose deferrals this plan addresses.
- **Future**: FZ 2c1a (validation evidence) lands as Phase V's output; child of 2c1.

---

**Last Updated**: 2026-05-10
**Status**: Active — drafted after v0.0.52 ship. Phase V scheduled next; Phase B follows once V findings are documented. Phase 10 retains its slot in plan_dks_expansion.md.
