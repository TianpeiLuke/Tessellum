"""P7 — calibrated semantic certificate (A7.2-A7.5).

Proves the certificate machinery over a PLUGGABLE (fake, deterministic) claim
scorer: conformal calibration bounds the false-accept rate at α per failure
class; certify accepts only when every claim clears its calibrated threshold,
and fail-closed ABSTAINS on any below-threshold / scorer-abstain / empty /
out-of-domain case; aggregation is per-claim min. The real NLI model + a
labelled wrong-but-well-formed corpus (A7.5) are out of scope — this ships the
framework the gating experiment plugs into.
"""

from __future__ import annotations

from tessellum.composer.semantic_certificate import (
    Claim,
    ClaimScore,
    LabeledExample,
    calibrate,
    certify,
    measure_false_accept_rate,
)


def _scorer(score_map):
    """A deterministic fake ClaimScorer from claim_id -> (score, abstained)."""
    def scorer(claims):
        out = []
        for c in claims:
            s = score_map.get(c.claim_id, (0.0, False))
            if isinstance(s, tuple):
                out.append(ClaimScore(c.claim_id, s[0], s[1]))
            else:
                out.append(ClaimScore(c.claim_id, s, False))
        return out
    return scorer


def _claim(cid, cls="grounding"):
    return Claim(claim_id=cid, text=f"claim {cid}", source_ref="src#1", failure_class=cls)


# ── calibration ─────────────────────────────────────────────────────────────


def test_calibrate_bounds_false_accept_rate() -> None:
    # grounding class: high scores are mostly correct, low scores mostly wrong.
    examples = (
        [LabeledExample("grounding", 0.95, True) for _ in range(9)]
        + [LabeledExample("grounding", 0.95, False)]      # 10% wrong at 0.95
        + [LabeledExample("grounding", 0.5, False) for _ in range(8)]
        + [LabeledExample("grounding", 0.5, True) for _ in range(2)]
    )
    th = calibrate(examples, alpha=0.10, domains=("terminology",))
    # the chosen threshold must keep the accepted region's error <= 0.10.
    far = measure_false_accept_rate(examples, th)
    assert far["grounding"] <= 0.10 + 1e-9
    # a class with no examples is unreachable (1.01) → always abstain.
    assert th.threshold_for("coverage") == 1.01


def test_calibrate_unmeetable_bound_yields_unreachable_threshold() -> None:
    # every accepted region has >50% error → no threshold meets alpha=0.01.
    examples = [LabeledExample("grounding", 0.9, i % 2 == 0) for i in range(10)]
    th = calibrate(examples, alpha=0.01)
    assert th.threshold_for("grounding") == 1.01  # abstain always (fail-closed)


# ── certify: accept / abstain (fail-closed) ─────────────────────────────────


def _th(threshold=0.8, domains=("terminology",)):
    return calibrate(
        [LabeledExample("grounding", threshold, True) for _ in range(10)]
        + [LabeledExample("coverage", threshold, True) for _ in range(10)]
        + [LabeledExample("duplicate", threshold, True) for _ in range(10)]
        + [LabeledExample("edge_relevance", threshold, True) for _ in range(10)],
        alpha=0.05, domains=domains,
    )


def test_certify_accepts_when_all_claims_clear_threshold() -> None:
    th = _th(0.8)
    claims = [_claim("c1"), _claim("c2")]
    scorer = _scorer({"c1": 0.9, "c2": 0.85})
    res = certify(claims, scorer=scorer, thresholds=th, note_domain="terminology")
    assert res.decision == "accept"
    assert res.verdict.status == "grounded"
    assert res.min_score == 0.85  # per-claim min-aggregation


def test_certify_abstains_when_any_claim_below_threshold() -> None:
    th = _th(0.8)
    claims = [_claim("c1"), _claim("c2")]
    scorer = _scorer({"c1": 0.9, "c2": 0.5})  # c2 below 0.8
    res = certify(claims, scorer=scorer, thresholds=th, note_domain="terminology")
    assert res.decision == "abstain"
    assert res.verdict.status == "ungrounded"
    assert "c2" in res.failing_claims


def test_certify_abstains_on_scorer_abstain() -> None:
    th = _th(0.8)
    claims = [_claim("c1")]
    scorer = _scorer({"c1": (0.99, True)})  # high score but scorer abstained
    res = certify(claims, scorer=scorer, thresholds=th, note_domain="terminology")
    assert res.decision == "abstain"
    assert "c1" in res.failing_claims


def test_certify_abstains_on_empty_claims() -> None:
    th = _th(0.8)
    res = certify([], scorer=_scorer({}), thresholds=th, note_domain="terminology")
    assert res.decision == "abstain"
    assert res.verdict.status == "ungrounded"


def test_certify_abstains_out_of_calibrated_domain() -> None:
    th = _th(0.8, domains=("terminology",))
    claims = [_claim("c1")]
    scorer = _scorer({"c1": 0.99})
    res = certify(claims, scorer=scorer, thresholds=th, note_domain="finance")
    assert res.decision == "abstain"
    assert "outside calibrated" in (res.verdict.detail or "")


def test_certify_per_class_thresholds_independent() -> None:
    # calibrate different thresholds per class; a claim is judged by ITS class.
    th = calibrate(
        [LabeledExample("grounding", 0.6, True) for _ in range(10)]
        + [LabeledExample("edge_relevance", 0.9, True) for _ in range(10)],
        alpha=0.05, domains=("d",),
    )
    # grounding threshold ~0.6, edge_relevance ~0.9.
    g = _claim("g", "grounding")
    e = _claim("e", "edge_relevance")
    # score 0.7 clears grounding but NOT edge_relevance.
    res_g = certify([g], scorer=_scorer({"g": 0.7}), thresholds=th, note_domain="d")
    res_e = certify([e], scorer=_scorer({"e": 0.7}), thresholds=th, note_domain="d")
    assert res_g.decision == "accept"
    assert res_e.decision == "abstain"


def test_certificate_verdict_feeds_grounding_gate() -> None:
    # the produced GroundingVerdict is exactly what the shipped grounding gate
    # consumes — an accept → "grounded", an abstain → "ungrounded" (fail-closed).
    from tessellum.composer.gates import grounding_predicate
    th = _th(0.8)
    accept = certify([_claim("c1")], scorer=_scorer({"c1": 0.95}),
                     thresholds=th, note_domain="terminology")
    assert grounding_predicate("x", verdict=accept.verdict) == []  # gate passes
    abstain = certify([_claim("c1")], scorer=_scorer({"c1": 0.1}),
                      thresholds=th, note_domain="terminology")
    issues = grounding_predicate("x", verdict=abstain.verdict)
    assert issues and issues[0].rule_id == "GROUND-001"  # gate fails closed
