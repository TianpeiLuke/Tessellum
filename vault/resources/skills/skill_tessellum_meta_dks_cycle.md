---
tags:
  - resource
  - skill
  - procedure
  - dks
  - meta_dks
  - dialectic
keywords:
  - meta-dks cycle
  - tessellum-meta-dks-cycle
  - schema mutation runtime
  - SchemaEditProposal
  - MetaCounterArgument
  - in-vault skill canonical
topics:
  - Skill Procedures
  - Meta-DKS
  - Schema Evolution
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
pipeline_metadata: ./skill_tessellum_meta_dks_cycle.pipeline.yaml
---

# Procedure: tessellum-meta-dks-cycle (Canonical Body)

This is the **single canonical body** for the `tessellum-meta-dks-cycle` skill — the agent-invocable surface of the meta-DKS schema-mutation runtime. The skill drives one complete meta-cycle from a `MetaObservation` (telemetry aggregate) to zero or more landed `SchemaEditEvent`s. It is invoked directly by Tessellum's composer; no ecosystem shims are needed.

Meta-DKS Phase 9 (v0.0.52) shipped the Python API at `tessellum.dks.meta`. v0.0.53 adds the LLM-driven proposer + attacker that this skill canonical specifies. v0.0.52's heuristic proposer remains as the default fallback when `--proposer heuristic` is selected.

## Skill description <!-- :: section_id = skill_description :: -->

Run one **meta-DKS cycle**: take a `MetaObservation` (aggregated cycle-level telemetry — Toulmin failure counts, top attacked warrants, unrealised schema edges, sample counter-argument quotes) and produce a set of `SchemaEditProposal`s, then optionally attack and aggregate them, and finally emit `SchemaEditEvent`s for proposals that survive the dialectic.

Use after `tessellum dks` has accumulated ≥ 20 cycles of telemetry (the cold-start guard). The four cycle stages mirror cycle-level DKS at one level of abstraction up: instead of arguments about an observation, the meta-cycle produces *schema-edit proposals* about the *aggregate of past observations*. The recursion stops at one level because `META_SCHEMA` itself is human-authored and PR-gated.

The CLI `tessellum dks --meta --proposer llm --attacker llm --apply` is this skill's primary caller. The heuristic-only path (`--proposer heuristic --attacker none`) is v0.0.52's behaviour and exists as a default fallback.

## Setup <!-- :: section_id = setup :: -->

```bash
source .venv/bin/activate
tessellum --version
# tessellum 0.0.53 or later

tessellum composer validate vault/resources/skills/skill_tessellum_meta_dks_cycle.md
tessellum composer compile  vault/resources/skills/skill_tessellum_meta_dks_cycle.md
```

The skill reads cycle-level telemetry under `--runs-dir` (default `./runs/dks/`); the orchestrator builds the `MetaObservation` before invoking step 1.

## Resources <!-- :: section_id = resources :: -->

- **Sidecar**: `./skill_tessellum_meta_dks_cycle.pipeline.yaml`
- **Core API**: [`src/tessellum/dks/meta/`](../../../src/tessellum/dks/meta/) — `MetaObservation`, `SchemaEditProposal`, `MetaCounterArgument` (v0.0.53), `MetaCycle`, `MetaCycleResult`, `LLMProposer`, `HeuristicProposer`, `MetaAttacker`, `load_event_log`, `write_event_log`
- **Schema event log**: `runs/dks/meta/schema_events.jsonl` — append-only `SchemaEditEvent` history (D3)
- **Meta-meta-schema**: `tessellum.dks.meta.types.META_SCHEMA` — 4 transitions; human-authored, PR-gated (D4)
- **Method reference**: [`thought_meta_dks_design`](../analysis_thoughts/thought_meta_dks_design.md) (FZ 2c1) — the design synthesis
- **Validation evidence**: [`thought_meta_dks_validation_v053`](../analysis_thoughts/thought_meta_dks_validation_v053.md) (FZ 2c1a) — the Phase V findings that inform this skill's prompts

### Step-to-meta-state map <!-- :: section_id = step_to_meta_state_map :: -->

| Step | Meta-state transition | Produces | Materialisation |
|--:|------------------------|----------|-----------------|
| 1 | meta_observation → meta_argument (`proposing`) | `SchemaEditProposal[]` | JSON only — no file |
| 2 | meta_argument → meta_counter (`attacking`) | `MetaCounterArgument[]` per proposal | JSON only — no file |
| 3 | meta_counter → meta_pattern (`aggregating`) | survival decision per proposal | JSON only — no file |
| 4 | meta_pattern → meta_revision (`landing`) | `SchemaEditEvent[]` | JSONL append to `runs/dks/meta/schema_events.jsonl` + migration note |

Unlike `tessellum-dks-cycle`, the meta-cycle does **not** materialise vault notes. Outputs are dataclass instances that flow through the in-memory `MetaCycle.run()` and ultimately land in the schema-event log + an auto-generated migration note. Vault content (FZ 2c1a-class validation notes) is authored separately by the human curator after a meta-cycle lands.

## Step 1: Propose <!-- :: section_id = step_1_propose :: -->

Read the `MetaObservation` and emit zero or more `SchemaEditProposal`s. Each proposal names one schema edit (add / retract / refine) the proposer believes will close a gap surfaced by the telemetry.

**Required output schema** (matches `SchemaEditProposal`):

- `kind` (enum) — one of: `"add"`, `"retract"`, `"refine"`
- `edge.source` (enum) — one of the 8 `BBType` values
- `edge.target` (enum) — one of the 8 `BBType` values
- `edge.label` (string) — the proposed edge label (snake_case, short)
- `motivating_observation` (string) — narrative justification grounded in the MetaObservation
- `expected_impact` (string) — what the proposer predicts will improve once landed
- `input_bias_risk` (enum) — one of: `"low"`, `"medium"`, `"high"` — proposer's own assessment of whether this proposal might be responding to input bias rather than a real schema gap (Phase V constraint C4)
- `supersedes` (object or null) — populated only for `"refine"`; same `{source, target, label}` shape as `edge`

**Authoring rules**:

1. **All four Toulmin components are first-class.** Do not privilege `warrant` over `premise`, `counter-example`, or `undercutting`. Each component, when dominant, signals a distinct kind of schema gap. (Phase V constraint C2.)
2. **Counter strengths weight the signal.** Treat one `strong` counter as outweighing two `weak` counters when judging dominance. The MetaObservation may include per-strength breakdowns. (C3.)
3. **Quote sample counters, don't trust aggregates alone.** The proposer prompt receives sample counter-argument quotes for each Toulmin component; ground proposals in these quotes' specifics, not the aggregate percentage alone. (C1.)
4. **Self-report input-bias risk.** If the MetaObservation shows the observation source has a structural skew (e.g., 80% are open-architectural questions, which mechanically invite warrant attacks), set `input_bias_risk: "high"` and qualify `motivating_observation` accordingly. (C4.)
5. **Don't propose adding edges already in BB_SCHEMA.** The downstream filter catches this, but the proposer should not waste a slot.

**No-proposal rule**: when telemetry surfaces no actionable gap, return an empty array. Better than fabricating proposals; the meta-cycle is allowed to do nothing.

## Step 2: Attack <!-- :: section_id = step_2_attack :: -->

For each proposal from step 1, produce zero or more `MetaCounterArgument`s naming a weakness. The attacker plays the dialectical role: every well-formed proposal deserves an attempt to refute it.

**Required output schema** (matches `MetaCounterArgument`):

- `attacked_proposal_index` (integer) — index into step 1's proposal array
- `attack_kind` (enum) — one of:
  - `"insufficient_evidence"` — the motivating telemetry doesn't actually support the proposed edge
  - `"input_bias"` — the dominance is input-induced, not a real schema gap (Phase V constraint C5)
  - `"overgeneralisation"` — the edge is too broad / would over-fire on the corpus
  - `"collides_with_existing"` — the edge duplicates or contradicts an active schema entry
  - `"weak_signal"` — counts cross the threshold but strength distribution is too soft
- `reason` (string) — the actual counter-argument; specific, evidence-grounded prose
- `strength` (enum) — `"weak"` / `"moderate"` / `"strong"`

**Authoring rules**:

1. **One proposal can receive multiple attacks.** Each attack must name a distinct `attack_kind`; duplicate-kind attacks against the same proposal are deduplicated by the aggregator.
2. **Attack the proposal, not the proposer.** Cite specific telemetry counts, sample quotes, or schema state — never "the proposer was wrong."
3. **Use `"input_bias"` when warranted.** If the proposer flagged `input_bias_risk: "medium"` or `"high"`, the attacker SHOULD fire an `"input_bias"` counter to make the risk explicit in the dialectic.
4. **Empty array is valid.** If a proposal has no defensible attack, return an empty array for it; the aggregator will survive it. The attacker is allowed to find nothing wrong.

## Step 3: Aggregate <!-- :: section_id = step_3_aggregate :: -->

For each proposal, decide whether it *survives*. Survival is determined by the attack distribution; the default rule is **majority**: a proposal survives iff `len(strong_attacks) <= 1 and len(moderate_attacks) <= 2`. Configurable via `--survive-threshold {strict|majority|permissive}`.

**This step is deterministic, not LLM-driven.** It is included in the skill canonical for completeness; the materialiser computes the survival decision from step 2's output without re-prompting the model.

**Required output schema**:

- `proposal_index` (integer)
- `survives` (boolean)
- `surviving_reason` (string) — short prose: "1 strong attack outweighed; proposal stands" / "3 attacks all of kind input_bias; proposal rejected"

## Step 4: Land <!-- :: section_id = step_4_land :: -->

For each surviving proposal, materialise it as a `SchemaEditEvent` and append to the event log. Author one migration note per cycle documenting the landed events.

**This step is deterministic, not LLM-driven.** The orchestrator writes events to `runs/dks/meta/schema_events.jsonl` and authors a migration note from a fixed template; the skill does not need to prompt the model again.

**Side effects**:

- Append zero or more JSONL lines to `runs/dks/meta/schema_events.jsonl` (one per surviving proposal)
- Increment `BB_SCHEMA_VERSION` (in-memory; persistence happens on next `set_user_extensions_from_events()` call)
- Write `runs/dks/meta/migration_<UTC-ts>.md` documenting the landed events

## Error Handling <!-- :: section_id = error_handling :: -->

| Error | Recovery |
|-------|----------|
| MetaObservation has < `min_cycles` cycles | Skip — cold-start guard fires; return empty proposal array. The orchestrator handles this before invoking the skill. |
| Step 1 returns malformed JSON | Loader rejects; orchestrator falls back to `HeuristicProposer` if `--proposer-fallback heuristic` is set, else exits non-zero. |
| Step 1 proposes an edge with invalid BBType | Filter drops it before step 2; logged as a warning. |
| Step 2 returns `attacked_proposal_index` out of range | Filter drops the attack; logged as a warning. |
| Aggregation reports 0 survivors | Valid outcome — emit empty events array; no migration note authored. |
| `runs/dks/meta/schema_events.jsonl` is unwritable | Orchestrator exits non-zero with the OS error; no partial write. |

## Important Constraints <!-- :: section_id = important_constraints :: -->

1. **The skill does not mutate `META_SCHEMA`.** That is the recursion stop; `META_SCHEMA` is human-authored and PR-gated (D4). The skill produces `SchemaEditEvent`s for `BB_SCHEMA_USER_EXTENSIONS` only.
2. **Outputs are JSON only.** No vault notes are written by this skill — only `runs/dks/meta/` artifacts. Vault content describing the meta-cycle's findings is authored separately by humans.
3. **Counter strength feeds the metric.** Treat strength as evidential weight; `strong` > `moderate` > `weak`. (Phase V constraint C3.)
4. **Toulmin components are symmetric.** None is privileged over another. Lookup tables are an anti-pattern for the LLM-driven proposer. (Phase V constraint C2.)
5. **Input-bias risk is a first-class output field.** Every proposal must include it; downstream attackers and human reviewers depend on it. (Phase V constraint C4.)
6. **The skill runs at most one meta-cycle per invocation.** Multi-cycle meta-DKS orchestration is not part of this skill; the CLI calls the skill once per `--meta` invocation.

## Related Entry Point <!-- :: section_id = related_entry_point :: -->

- [Dialectic Trail](../../0_entry_points/entry_dialectic_trail.md) — Trail 2 (DKS design); FZ 2c1 is this skill's design synthesis, FZ 2c1a is the validation evidence
- [`skill_tessellum_dks_cycle`](skill_tessellum_dks_cycle.md) — the cycle-level skill whose telemetry feeds this skill's `MetaObservation`
