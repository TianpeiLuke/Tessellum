# Role / Relation Query A/B — the harness and the contract

**No result has been produced here.** This directory contains a measurement
harness, a question-set format, and an encoded admission rule. It contains no
measurement, no question set drawn from a real corpus, and no wiring to a live
answer path. Nothing in it should be read as evidence that any arm beats any
other arm.

It exists for two phases of the query-time-DKS plan:

- **P2 — the node-first admission gate.** Measure the cheap path (resolve the
  mention to one entity, read that note's own authored field with its locator,
  abstain when the field is absent) against the status quo. *If the cheap path
  already clears the target, the expensive phases are not admitted.*
- **P11 — the derivation A/B.** Measure the full derivation path against the
  cheap one. *Arm 3 is admitted only if it beats arm 2 — not arm 1 — outside the
  noise floor, under repeated runs and more than one question ordering.*

## Which arm can be run today, and which cannot

| Arm | State here | What it needs |
|---|---|---|
| **1 — status quo** | **CANNOT RUN.** Declared with `external_arm(...)`; every report says `NOT RUN`. | The existing answer path — the one that answers a stewardship question with the note's author — lives in the application that embeds Tessellum, not in this repository. Supply it as an `ArmFactory` that proxies that path. |
| **2 — node-first** | **Runnable**, against an injected `Resolver` and `FieldReader`. Model-free: its per-query model budget is zero. | A resolver over a real entity registry, and a reader for the resolved note's authored field. Plan phase P1 supplies the first (`dks.entity_registry` / `dks.resolve_entity`); the adapter from its resolver to this harness's `Resolver` port, and a field reader over the vault, are **not written here** — see the note below. |
| **3 — derivation** | **Runnable**, against an injected `DerivationPort`. | The port is the whole of plan phases P1→P8 — reach, relation naming, claim reads with span locators, the bounded refutation, the three-way decision. The port is where a model would live; this harness never calls one. |

An arm that cannot run is recorded as `NOT RUN` and is **never** scored zero. A
missing arm and a losing arm are different facts, and the admission rule refuses
to conclude anything that depended on an arm that did not run — which is why the
P2 verdict here is `INCONCLUSIVE` rather than a decision.

**Why the ports are not wired to the package.** Both modules here are pure
stdlib and import nothing from `tessellum`. Adapting the P1 resolver and the P8
query capability into `Resolver` / `FieldReader` / `DerivationPort` is a shim of a
few lines each, and it belongs with whoever owns those modules: writing it here
would put a measurement harness on the package's import path and would couple the
grading of a JSON file to a working index, an embedding model and a vault. The
seam is a callable on purpose.

The `oracle_*` helpers in `arms.py` are deterministic test doubles that read the
question set's own answer key. They exist so the harness can be exercised end to
end with no model and no vault. **A number produced with them is the answer key
graded against itself.** `admission_verdict` additionally refuses any question
set whose `labelling` is `synthetic_fixture`, so the shipped example cannot admit
or refuse a phase even by accident.

## What has to come from outside

1. **The baseline answer path (arm 1).** Not present here. Until it is supplied,
   P2's comparison cannot be run at all and the P2 stop rule cannot fire.
2. **The cross-repository direction, written down.** The chosen wiring is: the
   host application's answer path **calls Tessellum**, through an `ask` tool on
   the MCP surface backed by the query capability plan phase P8 registers. The
   harness deliberately sits on this side of that seam — an arm is just a
   callable — so the host supplies an `ArmFactory` that proxies its own path and
   nothing in `eval/` needs to import it.
3. **Adapters for the two live ports.** `Resolver` and `FieldReader` for arm 2,
   `DerivationPort` for arm 3 — thin shims over the P1 resolver and the P8 query
   capability, owned by those phases rather than by this directory.
4. **A real question set with human labels.** The example set is invented. The
   `labelling` field is required for exactly this reason: an admission gate this
   decisive should rest on `human`, and `llm_judge` records that a model graded
   itself somewhere in the loop.
5. **A preregistered target for P2's stop rule.** `p2_verdict(target=...)` has no
   default. A threshold chosen after the numbers are in is not a stop rule, so an
   absent target yields `INCONCLUSIVE`.
6. **A noise floor measured on this harness.** See the caveat below.

## The question-set format

`question_set.schema.json` (draft-07) is the contract;
`question_set.example.json` is a small, entirely invented instance of it. Per
question:

| Field | Why it is there |
|---|---|
| `question` | the natural-language query as asked |
| `relation` | the relation/role the query asks for, as a stable label. Arm 2 reads the authored field of this name. It is never part of a claim's identity. |
| `target` | the surface mention and the entity it must resolve to (`entity_id: null` when nothing should resolve) |
| `expected` | the grounded answer **and its locator**. Both halves are required — an answer without a locator is not a grounded answer, and the grounding rate scores exactly that difference. |
| `abstain` + `abstain_reason` | **whether abstention is the correct response**, and why. First-class: `field_absent`, `entity_unresolvable`, `ambiguous_entity`, `out_of_scope`, `superseded_only`. |
| `hops` | the ordered evidence chain; two or more `required` hops make a question multi-hop, and `bridge: true` marks the load-bearing hop the shortcut control suppresses |
| `conflation_traps` | a value stated about the same entity under a *different* relation — the note's author beside the thing's steward. Answering with one is graded separately from a plain miss, because it is the specific failure this question class exists to expose. |

Unanswerable questions are half the measurement, not an appendix. This path
raises abstention before it raises answer quality, so a set without deserving
abstentions cannot tell a calibrated refusal from a regression.

## The metrics (`metrics.py`)

`answer_eval.py` next door reports entity / polarity accuracy and refusal rates.
None of the three measures below is among them, which is why they are here.

**Grounding rate** — grounded answers over the **fixed answerable set**. An
answer is grounded when it is correct *and* one cited locator satisfies the
expected locator. The denominator is the question set, not the answers the arm
chose to give: with answers-given underneath, an arm that abstains on everything
except one easy question scores 1.0. `grounded_precision` (grounded over answers
given) is reported beside it as the diagnostic pair, and
`ungrounded_answer_rate` counts every answer that was not grounded — a wrong
answer, a right answer with no or a mislocated citation, and any answer to a
question that deserved abstention.

**Connected-reasoning rate** — over multi-hop questions only: every required hop
is cited **and** the answer does not survive suppression of the bridge hop. The
harness re-asks each multi-hop question with its bridge hops withheld, from a
fresh arm instance; an arm that still answers correctly reached the answer
without traversing the chain, and that attempt is counted as a **shortcut**
rather than as connected reasoning. When the ablated re-ask is missing for any
multi-hop question, `shortcut_controlled` is `False` and the rate must be read as
chain completeness only.

**Abstention calibration** — both halves, never pooled into one refusal rate:
`abstained_on_deserving` (how much of the deserving abstention was taken),
`abstained_on_answerable` (how much abstention landed on answerable questions —
the unjustified-rise number the admission rule guards), the precision of all
abstention taken, and `calibration_gap` = the first minus the second. A surfaced
conflict on a deserving question is counted separately and is neither credited
nor lost.

**Model budget** — the cost invariant, counted per query: one relation-naming
call + *k* claim-reads + a **bounded** refutation, plus an optional stop check.
The caps are `BudgetPolicy`; a breach is reported, not clipped, and the admission
rule refuses on it, because an arm that outspends its cap has not won at matched
cost. (An earlier statement of this invariant claimed O(1) refutation; that was
wrong for a pairwise incompatibility judgement, which is quadratic in *k*.
Refutation runs against retrieval-surfaced candidate attackers only, capped.)

## The noise floor, and what it is not

`BUILD_NOISE_FLOOR = 0.047` with its provenance attached in the source. It comes
from **one** experiment that built the same digestion plan twice with a
stochastic writer and answered the same questions against both builds: pooled
per-question interval `[-0.047, +0.018]`, with a reader-model mismatch recorded.
So it measures how much a metric moves when nothing but the writer's sampling
changes.

Two limits ride along, and both are honoured rather than argued away. It is a
**floor, not a significance test** — clearing it says a gain is larger than one
known noise source, which is why this harness also requires repeated runs and
more than one ordering. And it was measured on a **different task** (a reader
over freshly built notes), so applying it to a grounding rate on a fixed corpus
is an import, not a derivation. `noise_floor` is a parameter at every call site
so a floor estimated on this harness can replace it.

## The admission rule, encoded

`admission_verdict` is fail-closed: any unmet condition refuses, and the reasons
are returned rather than printed. It enforces:

- **The comparison pair.** P11 compares arm 3 with **arm 2**; passing any other
  baseline raises `ValueError`, so the cheap baseline cannot be swapped for the
  flattering one at a call site. P2 compares arm 2 with arm 1.
- **Repeated runs with reported variance.** Every arm is run *n* times per
  ordering (default 3, minimum 3 to admit). The run-to-run standard deviations of
  both arms are **subtracted from the gain** before it is compared with the
  floor. That margin is deliberately conservative and is not a confidence
  interval — with three runs there is no distributional claim to make.
- **At least two orderings, and the gain must hold under every one.** Arms are
  built by factories, so each run and each ordering gets a fresh arm; an arm that
  carries a cache would otherwise leak a warm state between runs, which is the
  artifact the control exists to detect. A gain that exists under one ordering
  and vanishes under another is refused, and the reason names the ordering.
- **No unjustified rise in abstention** on the answerable questions, beyond the
  floor.
- **No per-query model-budget breach** by the candidate.
- **No fixture-labelled question set.**

## How to run

Describe a question set and the arm availability (no measurement, exit 2 on a
malformed set):

```bash
python eval/query_relation/arms.py eval/query_relation/question_set.example.json
```

Exercise the harness end to end with the oracle doubles — tautological by
construction, and refused as an admission decision:

```bash
python eval/query_relation/arms.py --self-check --target 0.9 --json /tmp/self_check.json
```

In code, with your own ports:

```python
report = run_ab(
    load_question_set("my_question_set.json"),
    {
        ARM_STATUS_QUO: external_arm(ARM_STATUS_QUO, "proxied from the host app"),
        ARM_NODE_FIRST: node_first_arm(my_resolver, my_field_reader),
        ARM_DERIVATION: derivation_arm(my_resolver, my_field_reader, my_derivation_port),
    },
    runs=5,
)
p2 = p2_verdict(report, target=0.85)   # target must be preregistered
p11 = p11_verdict(report)              # baseline is arm 2, not negotiable
print(render_report(report))           # the four required numbers, mean ± run spread
```

`render_report` prints one row per arm × ordering carrying `REPORTED_METRICS` —
grounding rate, connected-reasoning rate, both halves of abstention, realised
model calls per query, and the conflation rate — each as mean ± run-to-run
spread. An arm that did not run gets a `NOT RUN` line and no numbers, and a
connected-reasoning rate computed without the ablated re-ask is flagged in the
table as not shortcut-controlled.

## Files

```
query_relation/
  README.md                    ← this file
  question_set.schema.json     ← draft-07 contract for a role/relation question set
  question_set.example.json    ← a small INVENTED example (labelling: synthetic_fixture)
  metrics.py                   ← grounding / connected-reasoning / abstention +
                                 the model-budget counter, the noise floor, and the
                                 question-set model. Pure stdlib.
  arms.py                      ← the three arms, the ports, the ordering + run
                                 controls, the admission rule, and a describe/
                                 self-check CLI. Pure stdlib.
```

Both modules are pure stdlib on purpose (`jsonschema` is used for the structural
validation pass when importable and skipped with a warning otherwise). Importing
`answer_eval.py` to reuse its scoring rules was rejected: it imports the indexer,
the retrieval layer and the LLM bridge at module scope, which would make grading
a JSON file depend on a working model backend. Its two rules this harness needs —
punctuation-to-space normalisation and contiguous-token containment — are
re-stated in `metrics.py`, and `tests/eval/test_query_relation_harness.py` asserts
the two implementations agree so the convention cannot drift silently.
