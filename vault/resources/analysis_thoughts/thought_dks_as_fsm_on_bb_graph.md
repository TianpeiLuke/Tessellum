---
tags:
  - resource
  - analysis
  - argument
  - dks
  - fsm
  - automata
  - bb_ontology
  - graph_theory
  - learning
keywords:
  - DKS as FSM
  - finite state machine
  - BB ontology graph
  - state machine on typed graph
  - schema-runtime co-evolution
  - three levels of learning
  - meta-DKS
  - dialectic walker
  - graph-first refactor
topics:
  - Dialectic Knowledge System
  - Building Block Ontology
  - Finite State Machines
  - System Design
language: markdown
date of note: 2026-05-10
status: active
building_block: argument
folgezettel: "2a2"
folgezettel_parent: "2a"
---

# DKS as a Finite-State Machine on the BB Ontology Graph (FZ 2a2)

## Thesis

[FZ 2a: `thought_dks_design_synthesis`](thought_dks_design_synthesis.md) said *"each of the 7 DKS components corresponds to one BB-to-BB epistemic edge in the typed ontology"*. [FZ 1b: `thought_bb_ontology_as_typed_graph`](thought_bb_ontology_as_typed_graph.md) sharpened the ontology side: the BB graph is a **schema graph** (8 nodes + 10 edges, closed) with a **corpus** (running instance trace, open).

This note closes the loop on both sides: **DKS is a finite-state machine ⟨Q, Σ, δ, q₀, F⟩ whose state set Q is the 8 BB types, whose transition relation δ is exactly the 10-edge schema, whose tape is the corpus graph, and whose seven canonical "steps" are seven prescribed walks along a specific 7-edge subset of δ**. The formalism is not decoration — it is the data structure the implementation should center on, and it makes the *three levels of learning* DKS does fall out as separate operations on the FSM:

- **Instance learning** = filling the tape with corpus walks (every cycle does this)
- **Edge-weight learning** = adjusting transition preferences from counter outcomes (inter-cycle)
- **Schema learning** = δ itself mutates when sustained Toulmin failures show the schema is wrong (meta-DKS; R-P's productive half at its strongest)

[FZ 2a1](thought_dks_fz_integration.md) covered the *spatial* axis (DKS deposits a 6-node FZ subtree); [FZ 2b](thought_dks_runtime_integration.md) covered the *integration* axis (DKS reads through D, writes through composer + format); this note covers the *formal* axis (DKS is a typed automaton).

## The FSM, formally

DKS is a finite-state machine ⟨Q, Σ, δ, q₀, F⟩ where:

| Component | DKS reading | Cardinality |
|---|---|---|
| **Q** (states) | The 8 BB types (from [FZ 1b's BB schema](thought_bb_ontology_as_typed_graph.md)) | 8 |
| **Σ** (input alphabet) | The set of admissible step-triggering events: observation-arrival, agreement-detected, contradiction-detected, gating-decision, ... | small finite alphabet (~6 events) |
| **δ** (transition relation) | The 10 epistemic edges of the BB schema, each labelled with its semantic verb | 10 |
| **q₀** (start state) | `empirical_observation` (every cycle begins when an observation arrives) | 1 |
| **F** (accepting states) | The leaf states a cycle can terminate in: `procedure` (codified action), `concept` (refined definition), and — for short-circuits — `argument` (gated cycles end at A) | 3 |

Two precise readings of "DKS is an FSM":

1. **Schema-FSM** (the type-level machine): states are the 8 BB *types*; transitions are the 10 *schema edges*. δ is partial — many `(state, event)` pairs have no transition (e.g., there is no transition out of `counter_argument` on the `naming` event because CTR→CON is not in the schema). This is the FSM the schema graph defines.

2. **Corpus-FSM** (the instance-level machine): the same δ, but the *current state* is a specific BB-typed *note* (not the type). The machine "walks" by writing new corpus nodes along schema-defined edges. The 6-node FZ subtree from [FZ 2a1](thought_dks_fz_integration.md) is one such walk, materialised as files.

The two FSMs share δ. The schema-FSM is what `tessellum.format` validates against ("is this corpus edge a valid instance of a schema edge?"); the corpus-FSM is what DKS *runs* ("from here, where can I go next?").

## The 7 DKS components as 7 transitions

Re-stating FZ 2a's seven components in FSM language:

| Step | Event triggering it | Transition (in δ) | Resulting state |
|-----:|----------------------|---------------------|------------------|
| 1 | `observation_arrives` | (none — initial state) | OBS = q₀ |
| 2 | `argument_requested(conservative)` | OBS → ARG (via CON/MOD/HYP collapsed via the warrant context) | ARG (sibling A) |
| 3 | `argument_requested(exploratory)` | OBS → ARG (same δ, different prompt) | ARG (sibling B) |
| 4 | `compare_claims` | (no state transition — annotates the corpus with a `contradicts` edge between the two A-state and B-state nodes) | ARG (unchanged) |
| 5 | `attack_detected` | ARG → CTR (`challenging`) | CTR |
| 6 | `pattern_requested` | CTR → MOD (**a schema edge not in the original 10 — see [FZ 1b's gap analysis](thought_bb_ontology_as_typed_graph.md)**) | MOD |
| 7 | `revision_requested` | MOD → PRO (`codifying`) **or** MOD → CON (reverse of `naming`) | PRO or CON (∈ F) |

Three things this surfaces:

1. **Step 4 is not a state transition.** It is an *edge annotation* — the FSM stays at ARG but writes a `contradicts` edge between the two sibling ARG nodes. The current implementation's `DKSContradicts` dataclass models exactly this: an *edge*, not a *node*, with no FZ ID. The FSM formalism makes the dataclass's design feel inevitable.
2. **Step 2 and Step 3 take the same δ-transition twice.** They differ in the perspective (conservative vs. exploratory) but produce the same kind of state change. In an FSM with input alphabet, this is "two reads of the alphabet symbol `argument_requested` distinguished by sub-event arguments". In code, this is exactly the two-call pattern in `DKSCycle._step_argument(perspective="conservative" | "exploratory")`.
3. **Step 6's edge isn't in the original schema.** `counter_argument → model` (CTR → MOD) is required by the runtime but not declared by FZ 1's spec. [FZ 1b](thought_bb_ontology_as_typed_graph.md) flagged this as a productive-half R-P opportunity: extend the schema to include `CTR → MOD` with label `pattern_of_failure` (or similar), bringing the total to 11 schema edges. Until that happens, step 6's corpus edge is a *plumbing* link rather than a typed epistemic edge — the only step where DKS doesn't fully type-check against the current schema.

## The three terminal paths (= F)

A DKS run terminates in one of three accepting states. Each is a *walk* through δ:

```
Closed loop  (escalation=full,  6-node FZ subtree):
    OBS ─→ ARG(A) ─┐
    OBS ─→ ARG(B) ─┴─[contradicts]─→ CTR ─→ MOD ─→ {PRO ∈ F  or  CON ∈ F}

Short-circuit (escalation=full,  3-node FZ subtree; agreement at step 4):
    OBS ─→ ARG(A)
    OBS ─→ ARG(B)
    (no further transitions — A and B agree; cycle accepts in the ARG state)

Gated      (escalation=gated, 2-node FZ subtree; Phase 5):
    OBS ─→ ARG(A)
    (no B, no contradicts, no further transitions; cycle accepts in ARG)
```

All three are valid acceptances of the FSM — and **the FSM is correct iff exactly these three are reachable**. Anything else (e.g. terminating at OBS with no argument; terminating at CTR with no pattern) is a bug in either δ or the dispatcher. This is a clean correctness statement that the per-component dataclass implementation makes hard to phrase but the FSM lens makes obvious.

## Three levels of learning

The graph-theoretic lens makes DKS's learning operate at three separable levels — none of which were named explicitly in FZ 2a or FZ 2b, but all of which exist in the current runtime (some implicit, some explicit).

### Level 1: Instance learning (fast — every cycle)

Each cycle walks δ once and writes 6 (or 3, or 2) new BBNodes + edges to the corpus. The substrate grows monotonically; this is just *filling the FSM's tape*.

**Operations the runtime does today**: every closed cycle deposits a 6-node FZ subtree.
**What changes per cycle**: the *count* of corpus instances per state grows. After N cycles the corpus has roughly 3N–6N more nodes than before.
**Learning signal**: zero per-cycle — but the *aggregate* distribution of corpus instances by BB type is the system's *fingerprint*. A vault with 200 arguments and 0 counter-arguments has a learning problem; a vault with 200 arguments and 200 counters is exercising the dialectic.

### Level 2: Edge-weight learning (medium — inter-cycle)

The same δ, but the *runtime's preference* over transitions out of a given state is biased by past counter-argument outcomes. Today this is approximated:

- The warrant set (passed to steps 2 + 3) carries every prior cycle's revision. So step 2's "draw a warrant from the existing rule set" implicitly prefers warrants that *exist* — and only warrants that *survived* attack go into the rule set.
- A warrant that has been attacked 5 times across prior cycles is *visible* but *flagged* (the `--report` mode's "top-attacked warrant FZs" surfaces exactly this).
- The confidence model (Phase 5) is the explicit reading of this: a high-confidence observation is one whose warrant set is unlikely to be attacked.

**Operations the runtime does today**: warrant threading via `DKSRunner`; `--report` top-attacked summary; `ConstantConfidence` placeholder.
**What changes per cycle**: the *weight* the runtime puts on each transition. δ doesn't change; the agent's *prior over δ-walks* does.
**Learning signal**: the WarrantChange log + the top-attacked-warrant ranking. Today these are summary statistics; v0.2+ they become the input to a learned `DKSConfidenceModel` that produces calibrated scores rather than constants.

### Level 3: Schema learning (slow — meta-DKS; R-P productive half at its strongest)

δ itself mutates when the *runtime* repeatedly hits a state that the *schema* cannot legitimately leave. Two failure modes drive schema edits:

**Failure mode A — recurring Toulmin failure of the same component.** Suppose `counter_arguments` with `broken_component=counter-example` keep firing on `warrants` whose `qualifier` is empty. The schema today has no way to *prevent* this — qualifier is a free-text field. A schema response: introduce a new BB type `scope_assertion` (or extend the warrant schema to require a non-empty qualifier with a structured shape) and add the edge `argument → scope_assertion` to δ. Now the static validator can flag warrants missing a scope; the cycle's argument step is forced to populate it; future counter-examples that exploit scope mismatches can't be authored.

**Failure mode B — a schema edge has 0 corpus instances after N cycles.** If `procedure → empirical_observation` (execution data, schema edge in FZ 1) has zero corpus instances across 50 cycles, the runtime is not closing the operational loop. Either the schema edge is wrong (delete it) or the runtime is mis-implemented (add code to walk it). Schema and runtime co-evolve via this kind of audit.

**Operations the runtime does today**: zero. Schema is closed at 8+10. This is the deliberate v0.2+ deferral.
**What would need to change**: a *meta-DKS* runtime — a runner whose observations are *failure-mode summaries from the cycle-level DKS*, whose arguments are *proposed schema edits*, whose counter-arguments attack the proposals, and whose rule revisions update `tessellum.format.frontmatter_spec.VALID_BUILDING_BLOCKS` (or the edge spec).
**Learning signal**: the gradient is the cycle-level `--report` data: top-attacked warrants, recurring `broken_component` distributions, zero-instance schema edges.

The three levels nest: instance learning generates the data for edge-weight learning; edge-weight learning generates the data for schema learning. None is supervised; all three are dialectical (every level's revisions are themselves subject to counter-argument).

## What this implies for the implementation

The current implementation (`tessellum.dks.core` + `tessellum.dks.confidence` + `tessellum.dks.persistence`) ships:

| Level | Today's surface | Adequate? |
|---|---|---|
| 1 (instance) | `DKSCycle.run()` deposits 6 nodes + 5 edges per closed loop | ✓ for v0.0.45 |
| 2 (edge-weight) | `DKSRunner` threads warrants; `--report` surfaces top-attacked; `ConstantConfidence` is the gate-mechanism placeholder | ✓ for v0.0.45; needs a learned model in v0.2+ |
| 3 (schema) | nothing — schema is closed at 8+10 | deliberate v0.2+ gap |

The proposed refactor (graph-first) doesn't change the public CLI/API behaviour for any of these. What it changes is the *internal data structure* — instead of seven per-component dataclasses, the implementation centres on:

```python
class DKSStateMachine:
    """One typed walk over the BB ontology graph."""

    def __init__(
        self,
        schema: BBGraph,                  # the static 8+10 graph from FZ 1b
        corpus: BBGraph,                  # the running corpus (read-only into DKS)
        backend: LLMBackend,
        confidence_model: DKSConfidenceModel | None = None,
    ) -> None: ...

    def walk(self, observation: BBNode) -> BBPath:
        """Drive the FSM from q₀=OBS to some f ∈ F, returning the walk."""
        # current_state: BBType
        # path: list[BBNode]
        # while current_state not in F:
        #     event = self._next_event(current_state, path)
        #     edge  = schema.lookup_transition(current_state, event)
        #     node  = self._execute_transition(edge, path)   # one LLM call
        #     path.append(node)
        #     current_state = edge.target
        # return BBPath(nodes=path, edges=corpus_edges_for(path))
```

The dispatcher loop is *one* method (`walk`), not 7 hand-coded steps. Adding a Phase 6+ step (e.g. an `argument_requested(skeptical)` perspective) becomes a δ extension + a new event, not seven new lines of dispatcher code.

The per-component dataclasses (`DKSObservation`, `DKSArgument`, `DKSCounterArgument`, `DKSPattern`, `DKSRuleRevision`) survive as *typed views* over `BBNode`. The public API doesn't break; the *internals* trade per-component code for shared graph-walker code.

### Why we wouldn't refactor today

Three reasons to defer:

1. **The per-component code works.** v0.0.40–v0.0.45 shipped on the per-component-dataclass shape; 627 tests pass. Refactoring without a forcing function means changing working code.
2. **The refactor's payoff is meta-DKS.** A schema-aware DKS dispatcher only pays back when there's a *second* runtime walking the same graph (the meta-runtime that mutates δ). Until meta-DKS lands, the per-component shape is locally fine.
3. **The schema is itself underspecified.** Step 6's `CTR → MOD` edge is informally present in the runtime but missing from the FZ-1 schema. Adding it formally is a Phase 4-class change (validator update, term doc update, FZ-trail row). That work is the *prerequisite* for a clean graph-first refactor; doing the refactor first would just expose the schema gap downstream.

### When we would refactor

Two triggers:

- **A second walker arrives**: e.g. a Phase 6 multi-cycle orchestrator that wants to *fork* a walk at step 4 instead of choosing one of A/B. A graph-first dispatcher makes that trivial; the per-component code makes it expensive.
- **Schema editing becomes operational** (the v0.2+ meta-DKS work): if δ can mutate at runtime, the dispatcher must be a function of δ, not of seven hard-coded steps. At that point the refactor becomes load-bearing rather than aesthetic.

Until either trigger fires, the current implementation is the right shape and the graph-first formalism is the *mental model* the maintainer should use when reasoning about extensions.

## What this is NOT saying

Four carve-outs to prevent over-reading the FSM framing:

1. **DKS is not "just" an FSM.** An FSM is a transition system over discrete states. DKS adds: *every transition is one LLM call*, *every state is a typed corpus note with structured content*, *the transition function is partial and the missing transitions are themselves a learning signal*. Calling DKS "an FSM" emphasises the graph; it does not reduce DKS *to* a pure automaton.
2. **The FSM is non-deterministic in choice, deterministic in shape.** From ARG, you can transition to either CTR (via challenging) or back to OBS-via-future-cycle. Which one happens depends on whether a contradiction was detected at step 4 — an event the agent generates, not a schema property. The δ relation says what *can* happen; the runtime chooses what *does* happen.
3. **Schema-learning is not "schema is mutable."** It's "schema is mutable *under specific procedural discipline* — a meta-DKS cycle that itself satisfies all five DKS properties." The schema cannot be edited by hand at will; that breaks R-P. It can be edited by a dialectic over the schema. The recursion stops because the meta-DKS's schema (a smaller, more abstract one) is human-authored and held fixed.
4. **The 8 BB types aren't sacrosanct.** They are *Tessellum's current ontology*, inherited from Sascha + extended with procedure and navigation. A meta-DKS may discover that the next stable ontology has 9 types or 7 types. Schema-learning is what answers "are 8 types the right number?" empirically.

## Open questions this framing creates

| # | Question |
|--:|----------|
| OQ-FSM-1 | Is `CTR → MOD` a missing schema edge (should be added, bringing the total to 11) or is step 6's pattern-discovery a *non-typed* runtime operation (no schema implication)? Phase-4-class work either way. |
| OQ-FSM-2 | Should the navigation BB participate in δ at all, or only as a routing layer over the corpus? FZ 1's text treats NAV as orthogonal to the cycle; FZ 1b agrees; this note assumes the same. But agents that *navigate* during reasoning might benefit from NAV being a first-class transition. |
| OQ-FSM-3 | The gated terminal (Phase 5) accepts at ARG with no B. Is `argument` correctly in F (accepting), or should there be a separate `gated_argument` state? Today we model it as ARG-with-no-sibling-B (no schema change); the FSM-purist alternative would distinguish. |
| OQ-FSM-4 | When meta-DKS proposes a schema edit, who plays the role of the "observation" — what's the empirical anchor that justifies adding an edge? Lean: top-K most-attacked warrant FZs over the last N cycles, with the proposed schema edit explicitly stating what failure mode it prevents. |
| OQ-FSM-5 | Is the corpus-FSM Markovian (next state depends only on current state) or does it carry history (warrant set is a thread across cycles)? Today it carries history via `DKSRunner.warrants`. This makes it not strictly Markovian — it is a *finite-state automaton with one scratchpad*. Whether to formalise that further is open. |

## Related Notes

- **Parent**: [FZ 2a: `thought_dks_design_synthesis`](thought_dks_design_synthesis.md) — the 7-component pattern this note formalises as a 7-transition FSM walk
- **Sibling**: [FZ 2a1: `thought_dks_fz_integration`](thought_dks_fz_integration.md) — the *spatial* sharpening (DKS deposits a 6-node FZ subtree)
- **Cross-trail**: [FZ 1b: `thought_bb_ontology_as_typed_graph`](thought_bb_ontology_as_typed_graph.md) — the BB ontology as a typed graph that this FSM walks; co-companion of this note
- **Runtime side**: [FZ 2b: `thought_dks_runtime_integration`](thought_dks_runtime_integration.md) — how the runtime today integrates with composer/retrieval/format/eval
- **R-rule basis**: [FZ 1a1b: `thought_cqrs_r_cross_rules`](thought_cqrs_r_cross_rules.md) — R-P (Schema ⊥ Runtime) is the rule schema-learning operationalises

## Related Terms

- [`term_dialectic_knowledge_system`](../term_dictionary/term_dialectic_knowledge_system.md) — DKS canonical
- [`term_building_block`](../term_dictionary/term_building_block.md) — the 8 BB types that are the FSM's states
- [`term_epistemic_function`](../term_dictionary/term_epistemic_function.md) — each transition realises an epistemic function

## See Also

- [`entry_dialectic_trail`](../../0_entry_points/entry_dialectic_trail.md) — Trail 2 per-trail entry point (this note is FZ 2a2)
- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — master FZ trail map
- [`plan_dks_implementation`](../../../plans/plan_dks_implementation.md) — the 5-phase plan now fully shipped at v0.0.45

---

**Last Updated**: 2026-05-10
**Status**: Active — FZ 2a2, Dialectic trail (sibling of 2a1; formalises DKS as an FSM on the BB graph from FZ 1b)
