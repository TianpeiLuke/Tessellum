"""Smoke tests for P4 — evidence-based incompatibility and direction.

Step 4 used to decide *that* two arguments disagreed by comparing claim
strings, and *which way* the attack ran by prompt-slot order. Both are
now derivable from the arguments' evidence through an injected judge,
behind the opt-in ``evidence_based_disagreement`` flag.

The three acceptance clauses:

1. Two differently worded claims about compatible facts produce **no**
   attack edge (``test_compatible_claims_worded_differently_*``).
2. The attack **direction** is unchanged when the two perspectives swap
   generation order (``test_direction_is_unchanged_when_generation_order_swaps``).
3. The N>2 pairwise **edge set is invariant** under permutation of the
   perspectives list (``test_n3_edge_set_is_invariant_under_permutation``).

Each clause is paired with a test that characterises the *default*
(legacy) path, so the fix is visible as a difference rather than
asserted. The remaining tests cover the fail-closed rule (no
string-compare fallback anywhere) and the bounded model budget.
"""

from __future__ import annotations

import itertools
import json

import pytest

from tessellum.composer.llm import MockBackend
from tessellum.dks.core import (
    DEFAULT_REFUTATION_BUDGET,
    DKSArgument,
    DKSCycle,
    DKSObservation,
    DKSWarrant,
    IncompatibilityVerdict,
    LexicalOverlapRanker,
    LLMIncompatibilityJudge,
    TableIncompatibilityJudge,
)


# ── Claims (generic, domain-neutral) ───────────────────────────────────────

# Two wordings of the same fact — differently worded, compatible.
_ASCENDING = "the sequence is sorted in ascending order"
_SMALLEST_FIRST = "the sequence is arranged from the smallest value upward"

# Two claims that cannot both hold; the evidence favours the bounded one.
_BOUNDED = "the retry budget is exhausted after three attempts"
_UNBOUNDED = "the retry budget permits unlimited attempts"

# A three-way set: two incompatible, the third compatible with both.
_DRAINS = "the queue drains within one interval"
_NEVER_DRAINS = "the queue does not drain within one interval"
_SAMPLED = "the queue length is recorded once per interval"


# ── Fixtures / helpers ─────────────────────────────────────────────────────


def _argument_response(claim: str) -> str:
    return json.dumps(
        {
            "claim": claim,
            "data": f"D[{claim}]",
            "warrant": f"W[{claim}]",
            "backing": "",
            "qualifier": "",
            "evidence": f"E[{claim}]",
        }
    )


_COUNTER_RESPONSE = json.dumps(
    {
        "broken_component": "warrant",
        "counter_claim": "c",
        "reason": "r",
        "strength": "moderate",
    }
)
_PATTERN_RESPONSE = json.dumps({"description": "p", "observed": ["t"]})
_REVISION_RESPONSE = json.dumps(
    {"claim": "R", "data": "D", "warrant": "Rw", "supersedes": ""}
)


def _tail_responses() -> dict[str, str]:
    """Canned responses for steps 5-7, which run once step 4 fires."""
    return {
        "counter-argument": _COUNTER_RESPONSE,
        "pattern discovery": _PATTERN_RESPONSE,
        "rule revision": _REVISION_RESPONSE,
    }


def _backend(claims: dict[str, str], **extra: str) -> MockBackend:
    """MockBackend keyed by perspective → claim, plus the step 5-7 tail."""
    responses = {
        f"({perspective})": _argument_response(claim)
        for perspective, claim in claims.items()
    }
    responses.update(_tail_responses())
    responses.update(extra)
    return MockBackend(responses=responses)


def _observation(fz: str = "7") -> DKSObservation:
    return DKSObservation(folgezettel=fz, summary="a measured observation")


def _argument(fz: str, claim: str, perspective: str) -> DKSArgument:
    """A standalone argument, for unit-testing the judges + the ranker."""
    return DKSArgument(
        folgezettel=fz,
        warrant=DKSWarrant(claim=claim, data="D", warrant=f"W[{claim}]"),
        evidence=f"E[{claim}]",
        perspective=perspective,
    )


class _CountingJudge:
    """Wraps a judge and records every pair it was asked about."""

    def __init__(self, inner) -> None:
        self.inner = inner
        self.calls: list[tuple[str, str]] = []

    def __call__(self, a: DKSArgument, b: DKSArgument):
        self.calls.append((a.perspective, b.perspective))
        return self.inner(a, b)


def _unavailable_judge(a: DKSArgument, b: DKSArgument) -> None:
    """A judge with no opinion — the "model is down" case."""
    return None


def _raising_judge(a: DKSArgument, b: DKSArgument):
    raise RuntimeError("judge offline")


def _perspective_edges(result) -> set[tuple[str, str]]:
    """The edge set expressed over perspectives rather than FZ positions.

    Permuting ``perspectives`` renames the FZ slots, so an FZ-level
    comparison across permutations is vacuous. The perspective label is
    the argument's position-free identity, which is exactly what the
    invariance clause is about.
    """
    by_fz = {arg.folgezettel: arg.perspective for arg in result.arguments}
    return {
        (by_fz[edge.attacker_fz], by_fz[edge.attacked_fz])
        for edge in result.contradicts_edges
    }


# ── Clause 1: differently worded, compatible → no attack edge ──────────────


def test_compatible_claims_worded_differently_produce_no_attack_edge():
    """The judge says the two wordings are compatible → no edge at all."""
    judge = _CountingJudge(
        TableIncompatibilityJudge(
            verdicts={
                (_ASCENDING, _SMALLEST_FIRST): IncompatibilityVerdict(
                    incompatible=False,
                    rationale="both wordings assert the same ordering",
                )
            }
        )
    )
    result = DKSCycle(
        _observation(),
        (),
        _backend({"conservative": _ASCENDING, "exploratory": _SMALLEST_FIRST}),
        incompatibility_judge=judge,
    ).run()

    assert result.argument_a.warrant.claim != result.argument_b.warrant.claim
    assert result.contradicts is None
    assert result.contradicts_edges == ()
    assert result.closed_loop is False
    # Exactly one adjudication for a two-argument cycle.
    assert len(judge.calls) == 1
    # And the decision is auditable rather than silent.
    assert any(
        "compatible" in line for line in result.disagreement_diagnostics
    )


def test_unadjudicated_pair_is_reported_compatible_by_the_reference_judge():
    """An empty table is not "everything disagrees" — absence of evidence
    is not evidence of disagreement."""
    result = DKSCycle(
        _observation(),
        (),
        _backend({"conservative": _ASCENDING, "exploratory": _SMALLEST_FIRST}),
        incompatibility_judge=TableIncompatibilityJudge(),
    ).run()
    assert result.contradicts_edges == ()


def test_default_path_still_attacks_on_a_wording_difference():
    """Characterises the DEFAULT path: string inequality alone fires an
    edge, which is the defect the evidence-based path replaces."""
    result = DKSCycle(
        _observation(),
        (),
        _backend({"conservative": _ASCENDING, "exploratory": _SMALLEST_FIRST}),
    ).run()
    assert result.contradicts is not None
    assert result.contradicts_edges == (result.contradicts,)
    assert result.disagreement_diagnostics == ()


# ── Clause 2: direction is invariant under swapping generation order ────────


def _bounded_beats_unbounded_judge() -> TableIncompatibilityJudge:
    """The evidence defeats the *unbounded* claim, whichever slot it is in."""
    return TableIncompatibilityJudge(
        verdicts={
            (_BOUNDED, _UNBOUNDED): IncompatibilityVerdict(
                incompatible=True,
                direction="a_attacks_b",
                rationale="the cited counter runs out at the third attempt",
                evidence_locator="E[bounded]:0-12",
            )
        }
    )


def _run_pair(order: tuple[str, str], **kwargs):
    """One N=2 cycle with the two perspectives in the given order."""
    claims = {"bounded_angle": _BOUNDED, "unbounded_angle": _UNBOUNDED}
    return DKSCycle(
        _observation(),
        (),
        _backend(claims),
        perspectives=order,
        **kwargs,
    ).run()


def test_direction_is_unchanged_when_generation_order_swaps():
    """Whichever perspective is generated second, the argument the
    evidence defeats is the one attacked."""
    forward = _run_pair(
        ("bounded_angle", "unbounded_angle"),
        incompatibility_judge=_bounded_beats_unbounded_judge(),
    )
    reversed_ = _run_pair(
        ("unbounded_angle", "bounded_angle"),
        incompatibility_judge=_bounded_beats_unbounded_judge(),
    )

    for result in (forward, reversed_):
        assert result.contradicts is not None
        assert _perspective_edges(result) == {
            ("bounded_angle", "unbounded_angle")
        }
    # The FZ slots swap with the generation order; the semantic direction
    # does not.
    assert forward.contradicts.attacker_fz == "7a"
    assert reversed_.contradicts.attacker_fz == "7b"
    # The evidence that settled it rides out on the edge.
    assert "the cited counter runs out" in forward.contradicts.reason
    assert "E[bounded]:0-12" in forward.contradicts.reason


def test_default_path_direction_follows_generation_order():
    """Characterises the DEFAULT path: the attacker is whichever
    perspective happened to be generated second."""
    forward = _run_pair(("bounded_angle", "unbounded_angle"))
    reversed_ = _run_pair(("unbounded_angle", "bounded_angle"))
    assert _perspective_edges(forward) == {("unbounded_angle", "bounded_angle")}
    assert _perspective_edges(reversed_) == {("bounded_angle", "unbounded_angle")}


# ── Clause 3: the N>2 edge set is permutation-invariant ────────────────────


def _queue_judge() -> TableIncompatibilityJudge:
    """Only one of the three pairs is a real disagreement, and the
    evidence defeats the "drains" claim."""
    return TableIncompatibilityJudge(
        verdicts={
            (_DRAINS, _NEVER_DRAINS): IncompatibilityVerdict(
                incompatible=True,
                direction="b_attacks_a",
                rationale="the sampled series never reaches zero",
            ),
            (_DRAINS, _SAMPLED): IncompatibilityVerdict(
                incompatible=False, rationale="different subjects"
            ),
            (_NEVER_DRAINS, _SAMPLED): IncompatibilityVerdict(
                incompatible=False, rationale="different subjects"
            ),
        }
    )


_QUEUE_CLAIMS = {
    "drains_angle": _DRAINS,
    "never_drains_angle": _NEVER_DRAINS,
    "sampling_angle": _SAMPLED,
}


def _run_queue_cycle(order: tuple[str, ...], **kwargs):
    return DKSCycle(
        _observation(),
        (),
        _backend(_QUEUE_CLAIMS),
        perspectives=order,
        **kwargs,
    ).run()


def test_n3_edge_set_is_invariant_under_permutation():
    """Every ordering of three perspectives yields the same edge set —
    and the same sequence of adjudications, so the judge's *input* is
    position-free too, not just its output."""
    edge_sets = []
    call_sequences = []
    for order in itertools.permutations(tuple(_QUEUE_CLAIMS)):
        judge = _CountingJudge(_queue_judge())
        result = _run_queue_cycle(order, incompatibility_judge=judge)
        assert len(result.arguments) == 3
        # All three pairs are adjudicated, so the invariance is not an
        # artefact of some pair never being looked at.
        assert len(judge.calls) == 3
        edge_sets.append(_perspective_edges(result))
        call_sequences.append(judge.calls)

    assert len(edge_sets) == 6
    assert all(edges == edge_sets[0] for edges in edge_sets)
    assert edge_sets[0] == {("never_drains_angle", "drains_angle")}
    assert all(calls == call_sequences[0] for calls in call_sequences)


def test_n3_grounded_labelling_is_invariant_under_permutation():
    """The verdict the solver computes moves with the edge set, so it is
    invariant too (read over perspectives, not FZ slots)."""
    labellings = []
    for order in itertools.permutations(tuple(_QUEUE_CLAIMS)):
        result = _run_queue_cycle(order, incompatibility_judge=_queue_judge())
        by_fz = {a.folgezettel: a.perspective for a in result.arguments}
        labellings.append(
            {by_fz[fz]: label for fz, label in result.grounded_labelling.items()}
        )
    assert all(labels == labellings[0] for labels in labellings)
    assert labellings[0]["drains_angle"] == "out"
    assert labellings[0]["never_drains_angle"] == "in"
    assert labellings[0]["sampling_angle"] == "in"


def test_default_n3_edge_set_is_not_permutation_invariant():
    """Characterises the DEFAULT path: the legacy builder's edge set
    depends on the order the perspectives were listed in."""
    first = _perspective_edges(
        _run_queue_cycle(("drains_angle", "never_drains_angle", "sampling_angle"))
    )
    second = _perspective_edges(
        _run_queue_cycle(("sampling_angle", "drains_angle", "never_drains_angle"))
    )
    assert len(first) == 3 and len(second) == 3
    assert first != second


# ── Fail closed: no string-compare fallback on any branch ──────────────────


def test_unavailable_judge_emits_no_edge_and_records_why():
    result = DKSCycle(
        _observation(),
        (),
        _backend({"conservative": _BOUNDED, "exploratory": _UNBOUNDED}),
        incompatibility_judge=_unavailable_judge,
    ).run()
    assert result.contradicts is None
    assert result.contradicts_edges == ()
    assert any(
        "no judgement available" in line
        for line in result.disagreement_diagnostics
    )


def test_raising_judge_emits_no_edge_and_is_recorded_as_a_silent_failure():
    result = DKSCycle(
        _observation(),
        (),
        _backend({"conservative": _BOUNDED, "exploratory": _UNBOUNDED}),
        incompatibility_judge=_raising_judge,
    ).run()
    assert result.contradicts_edges == ()
    assert any(
        "judge raised RuntimeError" in line
        for line in result.disagreement_diagnostics
    )
    assert any(
        line.startswith("_adjudicate_pair: RuntimeError")
        for line in result.silent_failures
    )


def test_incompatible_but_undetermined_direction_emits_no_edge():
    """Where the evidence does not determine a direction, none is
    invented."""
    judge = TableIncompatibilityJudge(
        verdicts={
            (_BOUNDED, _UNBOUNDED): IncompatibilityVerdict(
                incompatible=True,
                direction="undetermined",
                rationale="both counters are cited from the same span",
            )
        }
    )
    result = DKSCycle(
        _observation(),
        (),
        _backend({"conservative": _BOUNDED, "exploratory": _UNBOUNDED}),
        incompatibility_judge=judge,
    ).run()
    assert result.contradicts_edges == ()
    assert any(
        "determines no direction" in line
        for line in result.disagreement_diagnostics
    )


def test_unparseable_model_answer_emits_no_edge():
    """The end-to-end fail-closed path: ``evidence_based_disagreement=True``
    with a backend that answers garbage produces no edge — the wording
    difference is NOT used as a fallback."""
    backend = _backend(
        {"conservative": _BOUNDED, "exploratory": _UNBOUNDED},
        **{"evidence-based incompatibility check": "not even json"},
    )
    result = DKSCycle(
        _observation(),
        (),
        backend,
        evidence_based_disagreement=True,
    ).run()
    assert result.contradicts_edges == ()
    assert any(
        "no judgement available" in line
        for line in result.disagreement_diagnostics
    )
    # The judge really was consulted — one call, not zero.
    assert sum(
        1
        for call in backend.calls
        if "evidence-based incompatibility check" in call.user_prompt
    ) == 1


def test_flag_alone_uses_the_backend_and_can_emit_an_edge():
    """``evidence_based_disagreement=True`` with no judge builds the
    model-backed one over the cycle's backend."""
    backend = _backend(
        {"conservative": _BOUNDED, "exploratory": _UNBOUNDED},
        **{
            "evidence-based incompatibility check": json.dumps(
                {
                    "incompatible": True,
                    "direction": "a_attacks_b",
                    "rationale": "the counter is bounded by construction",
                    "evidence_locator": "span:3",
                }
            )
        },
    )
    result = DKSCycle(
        _observation(), (), backend, evidence_based_disagreement=True
    ).run()
    assert result.contradicts is not None
    assert "span:3" in result.contradicts.reason


# ── The judges + the ranker, as units ──────────────────────────────────────


def test_table_judge_is_symmetric_with_the_direction_flipped():
    verdict = IncompatibilityVerdict(
        incompatible=True, direction="a_attacks_b", rationale="why"
    )
    judge = TableIncompatibilityJudge(verdicts={(_BOUNDED, _UNBOUNDED): verdict})
    bounded = _argument("1a", _BOUNDED, "p1")
    unbounded = _argument("1b", _UNBOUNDED, "p2")
    assert judge(bounded, unbounded).direction == "a_attacks_b"
    assert judge(unbounded, bounded).direction == "b_attacks_a"


def test_llm_judge_returns_none_on_unparseable_answer():
    judge = LLMIncompatibilityJudge(
        backend=MockBackend(default="I think they might disagree?")
    )
    assert judge(_argument("1a", _BOUNDED, "p1"), _argument("1b", _UNBOUNDED, "p2")) is None


def test_llm_judge_returns_none_when_the_backend_raises():
    class _Boom:
        backend_id = "boom"

        def call(self, request):
            raise RuntimeError("no transport")

    judge = LLMIncompatibilityJudge(backend=_Boom())
    assert judge(_argument("1a", _BOUNDED, "p1"), _argument("1b", _UNBOUNDED, "p2")) is None


def test_llm_judge_coerces_string_booleans_and_rejects_unknown_directions():
    judge = LLMIncompatibilityJudge(
        backend=MockBackend(
            default=json.dumps(
                {"incompatible": "true", "direction": "whichever_is_newer"}
            )
        )
    )
    verdict = judge(
        _argument("1a", _BOUNDED, "p1"), _argument("1b", _UNBOUNDED, "p2")
    )
    assert verdict is not None
    assert verdict.incompatible is True
    # An out-of-vocabulary direction degrades to "no direction", which
    # emits no edge — a hallucinated direction must not become an attack.
    assert verdict.direction == "undetermined"


def test_lexical_ranker_is_order_independent_and_capped():
    ranker = LexicalOverlapRanker()
    candidates = [
        _argument("1b", _NEVER_DRAINS, "p2"),
        _argument("1c", _SAMPLED, "p3"),
        _argument("1d", _ASCENDING, "p4"),
    ]
    ranked = ranker(_DRAINS, candidates, k=2)
    shuffled = ranker(_DRAINS, list(reversed(candidates)), k=2)
    assert [a.perspective for a in ranked] == [a.perspective for a in shuffled]
    assert len(ranked) == 2
    # The unrelated claim never outranks the two that share vocabulary.
    assert "p4" not in [a.perspective for a in ranked]
    assert ranker(_DRAINS, candidates, k=0) == ()


# ── Bounded model cost ─────────────────────────────────────────────────────


def test_refutation_budget_caps_the_number_of_judgements():
    """Six perspectives → 15 pairs if every pair were adjudicated; the
    caps hold the model budget to the configured constant."""
    claims = {f"angle_{i}": f"reading {i} of the same interval" for i in range(6)}
    judge = _CountingJudge(TableIncompatibilityJudge())
    result = DKSCycle(
        _observation(),
        (),
        _backend(claims),
        perspectives=tuple(claims),
        incompatibility_judge=judge,
        max_attack_candidates=2,
        refutation_budget=3,
    ).run()
    assert len(judge.calls) == 3
    assert any(
        "refutation budget 3 reached" in line
        for line in result.disagreement_diagnostics
    )


def test_zero_candidates_means_no_judgements_and_no_edges():
    judge = _CountingJudge(_bounded_beats_unbounded_judge())
    result = DKSCycle(
        _observation(),
        (),
        _backend({"conservative": _BOUNDED, "exploratory": _UNBOUNDED}),
        incompatibility_judge=judge,
        max_attack_candidates=0,
    ).run()
    assert judge.calls == []
    assert result.contradicts_edges == ()


def test_negative_caps_are_rejected():
    backend = _backend({"conservative": _BOUNDED, "exploratory": _UNBOUNDED})
    with pytest.raises(ValueError, match="max_attack_candidates"):
        DKSCycle(_observation(), (), backend, max_attack_candidates=-1)
    with pytest.raises(ValueError, match="refutation_budget"):
        DKSCycle(_observation(), (), backend, refutation_budget=-1)


def test_default_budget_is_a_constant_not_a_function_of_n():
    assert DEFAULT_REFUTATION_BUDGET == 8


# ── Default-off guarantees ─────────────────────────────────────────────────


def test_feature_is_off_unless_opted_in():
    cycle = DKSCycle(
        _observation(),
        (),
        _backend({"conservative": _BOUNDED, "exploratory": _UNBOUNDED}),
    )
    assert cycle.evidence_based_disagreement is False
    assert cycle.incompatibility_judge is None


def test_supplying_a_judge_implies_the_flag():
    cycle = DKSCycle(
        _observation(),
        (),
        _backend({"conservative": _BOUNDED, "exploratory": _UNBOUNDED}),
        incompatibility_judge=TableIncompatibilityJudge(),
    )
    assert cycle.evidence_based_disagreement is True


def test_evidence_path_does_not_run_the_legacy_semantic_check():
    """``semantic_disagreement`` and the evidence path answer the same
    question; when both are set, only the evidence-weighing one runs."""
    backend = _backend({"conservative": _BOUNDED, "exploratory": _UNBOUNDED})
    DKSCycle(
        _observation(),
        (),
        backend,
        semantic_disagreement=True,
        incompatibility_judge=_bounded_beats_unbounded_judge(),
    ).run()
    assert all(
        "semantic disagreement check" not in call.user_prompt
        for call in backend.calls
    )
