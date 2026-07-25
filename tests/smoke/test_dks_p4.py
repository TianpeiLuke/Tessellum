"""DKS refactor P4 — claim-type router + conformal gate (decision b3a).

Gate-to-P5 deliverables:
 - each warrant's claim is routed to a type-specific scorer (definitional /
   support / predictive / deployed);
 - the predictive temporal-holdout scorer is deterministic + fail-closed on
   leakage / un-recorded outcomes;
 - a claim with no available independent check ABSTAINS (dialectically-adequate-
   only, not true — Dung-IN no longer self-certifies);
 - the router feeds the SHIPPED certify(...) and yields the GroundingVerdict the
   runtime grounding seam consumes.
"""

from __future__ import annotations

from tessellum.composer.gates import grounding_predicate
from tessellum.composer.semantic_certificate import (
    Claim,
    ClaimScore,
    LabeledExample,
    calibrate,
)
from tessellum.dks import (
    ClaimTypeRouter,
    DKSWarrant,
    classify_claim,
    temporal_holdout_scorer,
    validate_claims,
)


def _warrant(**kw) -> DKSWarrant:
    base = dict(claim="c", data="d", warrant="w")
    base.update(kw)
    return DKSWarrant(**base)


def _claim(cid="c1", cls="grounding") -> Claim:
    return Claim(claim_id=cid, text="a claim", source_ref="src#1", failure_class=cls)


def _thresholds(t=0.8, domains=("dks",)):
    return calibrate(
        [LabeledExample("grounding", t, True) for _ in range(10)],
        alpha=0.05, domains=domains,
    )


# ── A4.1 — claim-type classification ────────────────────────────────────────


def test_classify_defaults_to_definitional() -> None:
    assert classify_claim(_warrant()) == "definitional"


def test_classify_predictive_when_outcome_time_present() -> None:
    w = _warrant(t_claim="2026-01-01T00:00:00Z", t_outcome="2026-02-01T00:00:00Z")
    assert classify_claim(w) == "predictive"


def test_classify_deployed_and_support_via_qualifier() -> None:
    assert classify_claim(_warrant(qualifier="deployed: RnR A/B")) == "deployed"
    assert classify_claim(_warrant(qualifier="support: FEVER")) == "support"


# ── temporal-holdout scorer (deterministic, fail-closed) ────────────────────


def test_temporal_holdout_scorer_abstains_on_leakage() -> None:
    # outcome == evidence → leakage → abstain
    w = _warrant(
        t_claim="2026-01-01T00:00:00Z", t_evidence="2026-02-01T00:00:00Z",
        t_outcome="2026-02-01T00:00:00Z", rebuttal="confirmed",
    )
    s = temporal_holdout_scorer(_claim(), w)
    assert s.abstained is True


def test_temporal_holdout_scorer_abstains_without_recorded_outcome() -> None:
    w = _warrant(
        t_claim="2026-01-01T00:00:00Z", t_outcome="2026-03-01T00:00:00Z",
        rebuttal="",  # no recorded outcome
    )
    assert temporal_holdout_scorer(_claim(), w).abstained is True


def test_temporal_holdout_scorer_grounds_confirmed_prediction() -> None:
    w = _warrant(
        t_claim="2026-01-01T00:00:00Z", t_outcome="2026-03-01T00:00:00Z",
        rebuttal="outcome confirmed on holdout",
    )
    s = temporal_holdout_scorer(_claim(), w)
    assert s.abstained is False and s.score == 1.0


# ── router: no independent check → abstain (Dung-IN does not self-certify) ──


def test_router_abstains_when_no_scorer_for_type() -> None:
    # definitional needs an injected NLI scorer; none registered → abstain.
    router = ClaimTypeRouter()  # only the deterministic predictive scorer
    s = router.score_one(_claim(), _warrant())  # definitional
    assert s.abstained is True  # dialectically-adequate-only, not true


def test_router_uses_injected_scorer_for_definitional() -> None:
    def nli(claim, warrant):
        return ClaimScore(claim.claim_id, 0.95, abstained=False)
    router = ClaimTypeRouter(scorers={"definitional": nli})
    s = router.score_one(_claim(), _warrant())
    assert s.abstained is False and s.score == 0.95


# ── A4.2 — end-to-end through the shipped certify(...) ──────────────────────


def test_validate_claims_accepts_confirmed_predictive() -> None:
    w = _warrant(
        t_claim="2026-01-01T00:00:00Z", t_outcome="2026-03-01T00:00:00Z",
        rebuttal="confirmed",
    )
    res = validate_claims(
        [_claim("c1", "grounding")], {"c1": w},
        thresholds=_thresholds(0.8), note_domain="dks",
    )
    assert res.decision == "accept"
    assert res.verdict.status == "grounded"
    # the verdict is exactly what the grounding gate consumes
    assert grounding_predicate("x", verdict=res.verdict) == []


def test_validate_claims_abstains_when_unchecked_and_gate_fails_closed() -> None:
    # a definitional claim with no injected NLI scorer → abstain → gate fails.
    res = validate_claims(
        [_claim("c1", "grounding")], {"c1": _warrant()},
        thresholds=_thresholds(0.8), note_domain="dks",
    )
    assert res.decision == "abstain"
    issues = grounding_predicate("x", verdict=res.verdict)
    assert issues and issues[0].rule_id == "GROUND-001"  # fail-closed


def test_validate_claims_missing_warrant_abstains() -> None:
    res = validate_claims(
        [_claim("c1")], {},  # no warrant for c1
        thresholds=_thresholds(0.8), note_domain="dks",
    )
    assert res.decision == "abstain"
