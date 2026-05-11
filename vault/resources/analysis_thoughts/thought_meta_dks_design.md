---
tags:
  - resource
  - analysis
  - argument
  - dks
  - meta_dks
  - schema_evolution
  - r_p_productive_half
  - event_sourcing
keywords:
  - meta-DKS design
  - schema mutation runtime
  - meta-meta-schema
  - SchemaEditEvent
  - SchemaEditProposal
  - MetaCycle
  - BB_SCHEMA_USER_EXTENSIONS
  - recursion stop
  - R-P productive half
topics:
  - Dialectic Knowledge System
  - Schema Evolution
  - System Architecture
  - Meta-DKS
language: markdown
date of note: 2026-05-10
status: active
building_block: argument
folgezettel: "2c1"
folgezettel_parent: "2c"
---

# Meta-DKS Design: How DKS Mutates Its Own Schema (FZ 2c1)

## Thesis

[FZ 2c](thought_dks_transition_model_adaptation.md) (the adaptation-strategy parent) proposed a three-stage hybrid pipeline (corpus statistics → LLM-validated formalisation → meta-DKS-driven governance) for learning the BB-internal transition model over time. **Meta-DKS is the third stage's runtime.** This note synthesises the design that ships in v0.0.52.

The load-bearing claim: meta-DKS is *cycle-level DKS at one level of abstraction up*. The same 7-component dialectic — observation, two arguments, contradicts, counter, pattern, revision — but the *substrate* is the schema itself, not the corpus. Where cycle-level DKS produces typed atomic notes, meta-DKS produces typed `SchemaEditEvent`s. Where cycle-level DKS walks `BB_SCHEMA`, meta-DKS walks `META_SCHEMA`. The recursion is intentional and bounded — `META_SCHEMA` is human-authored at the project layer (D4); there is no meta-meta-meta level.

## The four design commitments

Four resolutions from `plan_dks_expansion`'s Resolved-Decisions block constrain the meta-DKS implementation. Each is load-bearing for the recursion to halt safely and the schema growth to be auditable.

### D3 — Event-sourced schema (retractable state, append-only history)

`BB_SCHEMA_USER_EXTENSIONS` is **not** a constant tuple in code. It is the fold over an append-only log of `SchemaEditEvent`s. The log lives at `runs/dks/meta/schema_events.jsonl` — parallel to Phase 5's `warrant_history.jsonl`. Three event kinds:

- **`added`**: a new edge enters the active set
- **`retracted`**: an existing edge leaves the active set (corpus edges that instantiated it become *untyped*; TESS-005 surfaces them as a migration signal)
- **`refined`**: drop the old version (matched by source + target, any label) + add the new

The state is retractable; the history is immutable. A schema edit that proves wrong is itself a counter-argument input to a future meta-cycle — the dialectical pattern applies at the meta level just as at the cycle level. The log is never rewritten; compaction (folding old events into a snapshot) is a v0.3+ concern.

### D4 — Meta-meta-schema in code (`META_SCHEMA`)

The meta-FSM has 5 states (meta-observation, meta-argument, meta-counter, meta-pattern, meta-revision) and 4 transitions (proposing, attacking, aggregating, landing). They live as `MetaEdgeType` instances in `tessellum.dks.meta.types.META_SCHEMA`. **The meta-FSM does not mutate at runtime.** It is human-authored at the project layer; PR review is the only path to amend.

This is the recursion stop. Why one level and not infinite: the architectural commitment per D4 is that a self-mutating substrate needs at least one fixed authority to anchor identity — without it, "schema" is a meaningless category because what counts as a schema-edit is itself in flux. The meta-meta-schema is that anchor.

Concretely: meta-DKS *can* propose adding a CTR → MOD edge to `BB_SCHEMA`. Meta-DKS *cannot* propose adding a new state to `META_SCHEMA`. The first ships at v0.0.52; the second requires a human PR to amend the `META_SCHEMA` constant.

### D8 — Frozen-at-creation corpus validation

Schema edits don't retroactively invalidate corpus notes. Per D8, every note carries a `bb_schema_version: int` field (defaulted to 1 for v0.0.47-era notes); TESS-005 validates against that recorded version. The opt-in `tessellum bb migrate --target-version current` command reports which corpus edges would be flagged under the current schema — separating *was this valid when written?* from *is this valid now?*.

For v0.0.52: the field exists in the spec but isn't yet auto-populated by the capture pipeline. New notes default to version 1; meta-DKS's events bump `BB_SCHEMA_VERSION` (in-memory) per landed edit. The migrate command is Phase 11-class follow-up; the *event-sourcing discipline* is what makes the future migrate command possible.

### D3 + D8 composition

D3 and D8 together: schema state is event-sourced (D3); corpus state is version-pinned (D8). Migration becomes a query — "which corpus edges instantiate edges that exist in the current schema but not in the corpus note's recorded schema version?". The event log + the per-note version field together support that query without rewriting anything.

## The meta-cycle architecture

### Inputs — `MetaObservation`

Three signal channels feed the meta-cycle's reasoning, each derived from cycle-level telemetry under `runs/dks/`:

1. **Top attacked warrants** — warrant FZs that have been superseded frequently. Counter from per-aggregate `warrant_changes` events of kind `revised` and `superseded`. Signal: "this warrant shape is contested; the schema may be missing a constraint."

2. **Toulmin failure distribution** — counts of each `broken_component` value across per-cycle counters. A lopsided distribution (e.g. 80% `counter-example`) suggests the schema lacks a specific edge or constraint relevant to that failure mode.

3. **Unrealised schema edges** — BB-pairs in `BB_SCHEMA` with zero realised instances in the corpus. v0.0.52 ships this as `tuple()` (the BBGraph audit + index integration that populates it lands at Phase 11+); meta-cycle's heuristic-2 (retract-unused-edge) is therefore inert until that integration ships.

### Mechanism — `MetaCycle`

Four stages, each a method on the dataclass:

1. **`_generate_proposals`** — v0.0.52 uses *rule-based heuristics*. The Toulmin-dominance heuristic: when one `broken_component` exceeds 50% of counters, propose adding the related schema edge from a hand-authored lookup table (e.g. `warrant` dominance → propose `MODEL → PROCEDURE warrant_codification`). Phase 11+ replaces this with the Stage-2 LLM-validated proposer the parent FZ 2c describes.

2. **`_filter_proposals`** — sanity gate. Drop duplicates; drop proposals to add edges already in `BB_SCHEMA`; drop proposals to retract edges that aren't in `BB_SCHEMA_USER_EXTENSIONS` (we don't retract human-authored extensions or core epistemic edges via this path).

3. **Survive** — v0.0.52 is a pass-through. Phase 11+ runs the meta-cycle's *attack* step (the dialectical part) via the LLM-driven proposer.

4. **`_proposals_to_events`** — when `dry_run=False`, materialise surviving proposals as `SchemaEditEvent`s. The CLI writes them to `runs/dks/meta/schema_events.jsonl` and emits a migration note documenting the changes.

### Cold-start guard

Below `min_cycles` (default 20, configurable via `--min-cycles`), `MetaCycle.run()` returns immediately with zero proposals. Toulmin-failure distributions need ≥ ~20 cycles to be statistically meaningful; without the guard, early-deployment meta-DKS would propose schema edits from 1-2 cycles of noise.

### The CLI surface — `tessellum dks meta`

```
tessellum dks --meta [--runs-dir <dir>] [--target-failure <component>] \
    [--min-cycles N] [--apply] [--format human|json]
```

Default `--dry-run` (proposals printed but events not written). `--apply` activates `write_event_log` + emits a migration note. `--target-failure` filters proposals to a specific Toulmin component when you want to address a known failure mode without changing the rest of the schema.

## What ships in v0.0.52 vs deferred

| Surface | v0.0.52 | Deferred |
|---|---|---|
| `BB_SCHEMA_USER_EXTENSIONS` event sourcing (D3) | ✓ | — |
| `BB_SCHEMA_VERSION` int + bump-per-event (D3) | ✓ | — |
| `META_SCHEMA` in code, PR-gated (D4) | ✓ | — |
| `MetaObservation` + `SchemaEditProposal` + `MetaCycle` shapes | ✓ | — |
| Heuristic-based proposer | ✓ | Phase 11+: LLM-driven |
| Survive stage (dialectical attack) | pass-through | Phase 11+: LLM-driven |
| `tessellum dks --meta --dry-run` + `--apply` | ✓ | — |
| Migration note authoring | ✓ (minimal) | Phase 11+: richer template + entry-point integration |
| Composer skill canonical for the meta-cycle | — | Phase 11+ |
| `bb_schema_version` field auto-populated on capture | — | Phase 11+ (D8) |
| `tessellum bb migrate` retroactive validation | — | Phase 11+ (D8) |
| Unrealised-schema-edge signal in MetaObservation | empty tuple | Phase 11+ (BBGraph integration) |

The mechanism ships now; the polish + the LLM-driven dialectic + the migration tooling are Phase 11+ deliverables.

## Why this is the centrepiece phase

Three reasons meta-DKS is the largest single phase of `plan_dks_expansion`:

1. **R-P's productive half lands here at full strength.** [FZ 1a1b1](thought_cqrs_r_cross_gap_audit.md) (the R-Cross gap audit) named "the schema co-evolves with the runtime that exercises it" as R-P's productive-half claim. Phase 4 (v0.0.44) landed the *defensive* half — TESS-004 enforces declared edges. Phase 9 is the first phase where the schema *changes* in response to runtime evidence. Without meta-DKS the productive half is documentation; with it, it is mechanism.

2. **The recursion is real but bounded.** A system that mutates its own substrate is novel; one that mutates its own *schema for substrate-mutation* would be either incoherent (the term "schema" loses meaning) or infinitely deep (no fixed point). Phase 9 establishes the *one* level of meta the project commits to. Any future system claiming "meta-DKS" can be evaluated by asking: does it have an analogue of `META_SCHEMA` somewhere in code, PR-gated?

3. **Event sourcing makes mistakes recoverable.** A schema edit that proves wrong is a counter-argument input to a future meta-cycle. The retract event reverses the bad edit; the original event stays in the log as historical evidence. Without event sourcing, meta-DKS would be a write-only system — once edited, the schema's *prior* state would be lost. With it, the schema's full evolutionary history is the substrate the next meta-cycle reasons over.

## Open questions

| # | Question |
|--:|----------|
| **OQ-2c1-a** | What's the right cadence for running `tessellum dks meta`? — leans weekly initially; tune from observed event frequency once data accumulates. |
| **OQ-2c1-b** | Should retracts require *more* evidence than additions? — leans yes (retracts can break existing corpus edges; additions only declare new typed relationships). Heuristic-2 sets a 50-cycle minimum vs Heuristic-1's 20; tunable. |
| **OQ-2c1-c** | How does meta-DKS interact with multi-perspective (Phase 10)? — meta-cycle's MetaObservation will need per-perspective stratification once Phase 10 lands (Toulmin failure distribution × perspective). Forward-compatible at the data-shape layer; runtime will need a small extension. |
| **OQ-2c1-d** | Where do migration notes live? — v0.0.52 writes them under `runs/dks/meta/`; Phase 11+ may move them to `vault/resources/analysis_thoughts/schema_edit_*.md` per the original FZ 2c proposal. |

## Related Notes

- **Parent**: [FZ 2c: `thought_dks_transition_model_adaptation`](thought_dks_transition_model_adaptation.md) — the adaptation strategy this note's runtime operationalises
- **Sibling family (the design synthesis branch)**:
  - [FZ 2a: `thought_dks_design_synthesis`](thought_dks_design_synthesis.md)
  - [FZ 2a1: `thought_dks_fz_integration`](thought_dks_fz_integration.md)
  - [FZ 2a2: `thought_dks_as_fsm_on_bb_graph`](thought_dks_as_fsm_on_bb_graph.md) — the FSM formalism meta-DKS extends
- **Sibling family (the runtime branch)**:
  - [FZ 2b: `thought_dks_runtime_integration`](thought_dks_runtime_integration.md)
- **Cross-trail (evidence + gaps)**:
  - [FZ 1c: `thought_bb_internal_transitions_evidence`](thought_bb_internal_transitions_evidence.md)
  - [FZ 1a1b1: `thought_cqrs_r_cross_gap_audit`](thought_cqrs_r_cross_gap_audit.md)
- **Plan reference**: [`plan_dks_expansion`](../../../plans/plan_dks_expansion.md) — Phase 9 is this note's implementation; D3/D4/D8 are its load-bearing resolutions

## See Also

- [`entry_dialectic_trail`](../../0_entry_points/entry_dialectic_trail.md) — Trail 2 per-trail entry point (this note is FZ 2c1)
- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — master FZ trail map

---

**Last Updated**: 2026-05-10
**Status**: Active — FZ 2c1, Dialectic trail (child of 2c; meta-DKS design synthesis shipping at v0.0.52)
