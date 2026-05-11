---
tags:
  - resource
  - skill
  - procedure
  - dks
  - dialectic
  - folgezettel
keywords:
  - dks cycle
  - tessellum-dks-cycle
  - dialectic knowledge system
  - 7-component closed loop
  - toulmin failure modes
  - in-vault skill canonical
topics:
  - Skill Procedures
  - Dialectic Knowledge System
  - System P Runtime
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
pipeline_metadata: ./skill_tessellum_dks_cycle.pipeline.yaml
---

# Procedure: tessellum-dks-cycle (Canonical Body)

This is the **single canonical body** for the `tessellum-dks-cycle` skill — the agent-invocable surface of the Dialectic Knowledge System (DKS) Phase 2 runtime. The skill drives one complete 7-component closed loop from an observation to a revised warrant, producing six typed notes (one per non-edge component) plus one `contradicts` link. It is invoked directly by Tessellum's composer; no ecosystem shims are needed.

DKS Phase 1 (v0.0.40) shipped the Python API; v0.0.43 lifted it to its own top-level package at [`src/tessellum/dks/`](../../../src/tessellum/dks/) (peer to `tessellum.composer`, not nested inside it). This skill is the Composer-pipeline counterpart, mapping each of the 7 components to one Composer step.

## Skill description <!-- :: section_id = skill_description :: -->

Run one **DKS cycle**: take a single observation (a typed record of what happened) and drive it through the 7-component closed loop documented in [`thought_dks_design_synthesis`](../analysis_thoughts/thought_dks_design_synthesis.md) (FZ 2a) and [`thought_dks_fz_integration`](../analysis_thoughts/thought_dks_fz_integration.md) (FZ 2a1). Produces six typed atomic notes plus a `contradicts` link that together form a 6-node Folgezettel subtree.

Use when an observation surfaces possible disagreement with the current warrant set — a model output that contradicts a procedure, a failed experiment that defies the prevailing theory, a counter-example to an established concept. The cycle's deposited subtree IS the dialectic trace: future runs can extend, attack, or branch from any of its six nodes.

The full multi-cycle orchestration (Phase 3), P-side retrieval client (Phase 4), and confidence gating (Phase 5) layer on top of this skill without changing its contract.

## Setup <!-- :: section_id = setup :: -->

```bash
source .venv/bin/activate
tessellum --version
# tessellum 0.0.42 or later

tessellum composer validate vault/resources/skills/skill_tessellum_dks_cycle.md
tessellum composer compile  vault/resources/skills/skill_tessellum_dks_cycle.md
tessellum index build       # so step 1 / step 6 can read the current warrants
```

Default DB / vault paths follow the standard Tessellum convention (`./vault/`, `./data/tessellum.db`).

## Resources <!-- :: section_id = resources :: -->

- **Sidecar**: `./skill_tessellum_dks_cycle.pipeline.yaml` (mapped via the frontmatter `pipeline_metadata` field)
- **Core API**: [`src/tessellum/dks/`](../../../src/tessellum/dks/) — `DKSObservation`, `DKSArgument`, `DKSWarrant`, `DKSContradicts`, `DKSCounterArgument`, `DKSPattern`, `DKSRuleRevision`, `DKSCycleResult`, `DKSRunner`, `DKSRunResult` (import from `tessellum.dks`)
- **FZ allocator**: `allocate_cycle_fz(existing_trails, mode, parent_fz)` — three modes (`fresh` / `extend` / `branch`)
- **Trail explorer**: `tessellum fz` (v0.0.41) — inspect the produced FZ subtree after the run
- **Method references**:
  - [`term_dialectic_knowledge_system`](../term_dictionary/term_dialectic_knowledge_system.md) — DKS canonical
  - [`term_folgezettel`](../term_dictionary/term_folgezettel.md) — the FZ mechanism
  - [`thought_dks_design_synthesis`](../analysis_thoughts/thought_dks_design_synthesis.md) — FZ 2a — the 7-component design
  - [`thought_dks_fz_integration`](../analysis_thoughts/thought_dks_fz_integration.md) — FZ 2a1 — the 6-node-trail mapping

### BB type per step <!-- :: section_id = bb_type_per_step :: -->

| Step | Component | BB type produced | FZ position |
|--:|-----------|------------------|-------------|
| 1 | Observation source | `empirical_observation` | cycle root (FZ N) |
| 2 | Argument generator A (conservative) | `argument` | FZ N.a |
| 3 | Argument generator B (exploratory) | `argument` | FZ N.b |
| 4 | Disagreement detection | (edge — no node, no FZ) | link from attacker to attacked |
| 5 | Counter-argument capture | `counter_argument` | FZ `<attacked_fz>`.a |
| 6 | Pattern discovery | `model` | FZ `<counter_fz>`.a |
| 7 | Rule improvement | `procedure` or `concept` | FZ `<pattern_fz>`.a (leaf) |

Each row except step 4 corresponds to one materialised note. Step 4 produces a link inside the body of the attacking argument note, not a separate file.

## Step 1: Observation Capture <!-- :: section_id = step_1_observation_capture :: -->

Take the leaf metadata's `summary` (and optional `timestamp`) and emit a single `empirical_observation` note at the cycle root FZ.

**Required output schema** (matches `DKSObservation` in `dks.py`):

- `summary` (string) — concise description of what happened, in present-tense factual prose
- `timestamp` (string, optional) — ISO-8601 if known, else `null`
- `folgezettel` (string) — the cycle root, allocated via `allocate_cycle_fz(..., mode="fresh"|"extend"|"branch")`
- `folgezettel_parent` (string | null) — null for `fresh` mode; the parent's FZ for `extend` / `branch`

**File location**: `archives/experiments/observation_<slug>.md`

**Writing rules**:
- The summary is a *fact*, not an interpretation. Save interpretation for steps 2 and 3.
- Quote verbatim error messages, tool outputs, or sensor readings where applicable.
- If the observation comes from the active Claude Code session, the agent SHOULD use `session-mcp` to extract the exact transcript context — same pattern as `skill_tessellum_write_coe` step 1.

## Step 2: Argument Generator A <!-- :: section_id = step_2_argument_a :: -->

Generate the **conservative** argument: which existing warrant in the current rule set best explains the observation? The argument inherits a warrant from the existing set (no novel rules at this step).

**Required output schema** (matches `DKSArgument` + `DKSWarrant`):

- `claim` (string) — what this argument concludes about the observation
- `data` (string) — the observation features cited as support
- `warrant` (string) — the existing rule licensing data → claim
- `backing` (string, may be empty) — the deeper authority for the warrant
- `qualifier` (string, may be empty) — the strength qualifier (e.g. "generally", "always", "in retrieval contexts")
- `rebuttal` (string, may be empty) — known exceptions where the warrant doesn't apply
- `evidence` (string) — link to or quotation from the observation that makes the data citable
- `folgezettel` (string) — `<cycle_root>.a`, allocated by Phase 1 core
- `folgezettel_parent` (string) — equals the cycle root FZ (step 1's output)

**File location**: `resources/analysis_thoughts/argument_a_<slug>.md`

**Conservative perspective rule**: Argument A MUST reuse a warrant from the input warrant set. If the input warrant set is empty, A authors a minimal warrant from the observation's most stable feature. A never *revises* the warrant; that is step 7's job.

## Step 3: Argument Generator B <!-- :: section_id = step_3_argument_b :: -->

Generate the **exploratory** argument: an alternative reading of the same observation, taking a different warrant. B's role is to surface latent disagreement — its claim must be *substantively different* from A's, not a paraphrase.

**Required output schema**: identical to step 2 (`DKSArgument` + `DKSWarrant`), with `folgezettel = <cycle_root>.b` and `folgezettel_parent = <cycle_root>`.

**File location**: `resources/analysis_thoughts/argument_b_<slug>.md`

**Exploratory perspective rule**: Argument B is allowed to draw on warrants outside the current set OR to weaken / qualify a warrant that A used. If B genuinely produces the same claim as A (no exploratory angle exists for this observation), B SHOULD say so explicitly in `rebuttal`. The cycle will short-circuit at step 4 in that case.

## Step 4: Disagreement Detection <!-- :: section_id = step_4_disagreement_detection :: -->

Compare A's `claim` and B's `claim`. If they substantively agree (same or paraphrased), produce **no contradicts edge**; the cycle short-circuits and steps 5-7 do not run. If they disagree, produce a typed `DKSContradicts` edge.

**Required output schema** (matches `DKSContradicts`; absent when arguments agree):

- `attacker_fz` (string) — the FZ of the argument doing the attacking (typically B)
- `attacked_fz` (string) — the FZ of the argument being attacked (typically A)
- `reason` (string) — what specifically B contradicts about A (premise / warrant / scope / qualifier)

**Materialisation**: the contradicts edge is a markdown link in the attacker's note body, NOT a separate file. The attacker's `## Contradicts` section names the attacked argument by FZ and links to it.

**Short-circuit case**: if A and B agree, the cycle still produces a 3-node FZ subtree (observation + 2 arguments) and `closed_loop` is False. The skill exits at the end of step 3.

## Step 5: Counter-Argument Capture <!-- :: section_id = step_5_counter_argument_capture :: -->

Author a typed `counter_argument` note that names **which Toulmin component is broken** in the attacked argument. The Toulmin failure mode classifies the repair: a broken `premise` calls for new data; a broken `warrant` calls for rule revision (step 7); a `counter-example` calls for a scoped exception; an `undercutting` calls for tightening the qualifier.

**Required output schema** (matches `DKSCounterArgument`):

- `attacked_fz` (string) — equals `contradicts.attacked_fz` from step 4
- `broken_component` (enum) — one of: `"premise"`, `"warrant"`, `"counter-example"`, `"undercutting"`
- `counter_claim` (string) — what the counter-argument concludes instead
- `reason` (string) — the argument from the broken component to the counter_claim
- `strength` (enum) — one of: `"weak"`, `"moderate"`, `"strong"`
- `folgezettel` (string) — `<attacked_fz>.a`
- `folgezettel_parent` (string) — equals `attacked_fz` (this is what TESS-004 will check in Phase 4)

**File location**: `resources/analysis_thoughts/counter_<slug>.md`

**Authoring rule**: a counter-argument MUST name exactly one broken component. Multi-component attacks split into separate counters at sibling FZ positions (`<attacked_fz>.a`, `<attacked_fz>.b`, ...) in subsequent cycles.

## Step 6: Pattern Discovery <!-- :: section_id = step_6_pattern_discovery :: -->

Look back across the counter-argument and any *prior* counters this cycle observed (via leaf metadata `observed_contradictions`) and emit a typed `model` note describing the structural regularity. A pattern is a generalisation: "counters of this kind keep attacking warrants of that kind."

**Required output schema** (matches `DKSPattern`):

- `description` (string) — the pattern: "counters with broken `<component>` keep firing on warrants with `<feature>`"
- `observed` (array of strings) — FZ IDs (or short descriptions) of the contradictions that feed this pattern; minimum length 1 (the current counter); can include prior counters from leaf metadata
- `folgezettel` (string) — `<counter_fz>.a`
- `folgezettel_parent` (string) — equals the counter's FZ (step 5's output)

**File location**: `areas/models/pattern_<slug>.md`

**Insufficient-data rule**: if the agent cannot honestly identify a regularity (single counter, no related history), it MUST return `description: "no new pattern — insufficient instances"` with `observed: [<this counter's FZ>]`. The skill still emits a typed model note so the FZ subtree stays well-formed; step 7 reads the description and may decide to revise nothing.

## Step 7: Rule Improvement <!-- :: section_id = step_7_rule_improvement :: -->

Translate the pattern into a **revised warrant** — either a new `procedure` (operational rule: "when X, do Y") or a new `concept` (definitional rule: "X is now defined as Y"). The decision between `procedure` and `concept` is the agent's, based on whether the revision is an action policy or a typology change.

**Required output schema** (matches `DKSRuleRevision` + `DKSWarrant`):

- `revised_warrant` (object) — the new Toulmin-typed warrant with the same six fields as steps 2/3 (`claim`, `data`, `warrant`, `backing`, `qualifier`, `rebuttal`)
- `supersedes` (string | null) — the FZ of the warrant this revision replaces; null if it's a wholly new rule
- `bb_type` (enum) — one of: `"procedure"`, `"concept"`
- `folgezettel` (string) — `<pattern_fz>.a` (the cycle's leaf)
- `folgezettel_parent` (string) — equals the pattern's FZ (step 6's output)

**File location**:
- `bb_type: procedure` → `resources/skills/procedure_<slug>.md`
- `bb_type: concept`   → `resources/term_dictionary/concept_<slug>.md`

**No-revision rule**: if step 6 emitted `"no new pattern"`, step 7 SHOULD emit a revision whose `revised_warrant.qualifier` notes the pattern was insufficient and `supersedes: null`. The cycle still produces a leaf note so the FZ subtree closes; future cycles can revise this revision once more data accumulates.

## Error Handling <!-- :: section_id = error_handling :: -->

| Error | Recovery |
|-------|----------|
| Observation summary is too vague to support arguments | Mark the observation as a stub (`status: stub`); ask the user to expand before re-running the cycle |
| A and B agree → cycle short-circuits | Expected — emit the 3-node subtree (observation + 2 args) and report `closed_loop: False`. The observation is dialectically uncontroversial. |
| `broken_component` is none of the 4 Toulmin literals | Loader rejects the run — fix the prompt or the model output. The literal set is fixed by `ToulminComponent` in `dks.py`. |
| Pattern step has only one observation | Emit `description: "no new pattern — insufficient instances"` (rule above). Do NOT fabricate regularities. |
| Step 7 fires with no genuine revision | Emit a revision that supersedes nothing and qualifies itself as "pending more data". Better than skipping — the leaf-note discipline keeps R-P enforceable. |
| FZ allocator collides | Bug in the allocator state; report the existing-trail set the cycle saw versus the actual vault state. |

## Important Constraints <!-- :: section_id = important_constraints :: -->

1. **Each non-edge component produces exactly one typed atomic note.** Six notes per cycle when the loop closes; three when it short-circuits. No more, no less.
2. **The contradicts edge (step 4) is a relation, not a node.** Materialised as a markdown link in the attacker's body; no separate file.
3. **The FZ subtree is non-optional.** Every produced note has both `folgezettel:` and `folgezettel_parent:` fields set. TESS-001 / TESS-002 enforce the pair; TESS-004 (Phase 4) will additionally enforce that `counter_argument`'s `folgezettel_parent` resolves to a `building_block: argument` note.
4. **Toulmin component vocabulary is closed.** `premise` / `warrant` / `counter-example` / `undercutting`. Any other label is a validator error.
5. **The skill does not write to `entry_folgezettel_trails.md`.** That update happens out-of-band — either by the multi-cycle orchestrator (Phase 3) or by the `tessellum-append-to-trail` skill if a human curates the cycle's output. Single-cycle scope.

## Related Entry Point <!-- :: section_id = related_entry_point :: -->

- [Folgezettel Trails Master](../../0_entry_points/entry_folgezettel_trails.md) — vault-wide FZ trail index; DKS-produced trails register alongside hand-authored ones
- [Dialectic Trail](../../0_entry_points/entry_dialectic_trail.md) — Trail 2 (DKS design); this skill is the *runtime* that the trail's argument chain specifies
