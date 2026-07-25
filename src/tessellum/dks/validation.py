"""tessellum.dks.validation — claim-type router + conformal gate (decision b3a).

P4 of the DKS refactor plan. Makes Dung-`IN` stop self-certifying: promotion is
authorized by an EXOGENOUS signal keyed to claim type, not by the reasoning
model asserting its own conclusion (P3 — the mover is never the judge).

**The conformal machinery is already shipped** by the substrate's P7
(`composer/semantic_certificate.py`): `certify(claims, scorer, thresholds) ->
CertificateResult` runs the calibration + fail-closed abstain over a *pluggable*
`ClaimScorer` and PRODUCES the `GroundingVerdict` the grounding gate consumes.
So DKS builds only:

- A4.1 — a **claim-type router**: tag each atomic warrant with an epistemic
  type, then dispatch to a `ClaimScorer` per type —
    * definitional / coherence → NLI entailment against the cited span
      (injected model);
    * support / existence → FEVER-style retrieval with an ABSTAIN as a
      first-class outcome (injected model);
    * predictive / causal → a prequential **temporal-holdout** scorer over the
      P1 tri-temporal fields — DETERMINISTIC, no external model (it is the one
      scorer DKS can ship whole);
    * deployed causal (Athelas-Conv) → the A/B + McNemar oracle (injected).
- A4.2 — the **wiring**: build the `GroundingVerdict` from `certify(...)` and
  hand it to the runtime's `grounding_verifier` seam (unfed today);
- A4.3 — **Dung as a pre-filter**, never the terminal verdict: a claim with no
  available independent check is `dialectically-adequate-only`, not `true`.

The real NLI / FEVER / A/B scorers are injected dependencies (the same seam
`semantic_certificate` already expects); this module ships the router, the
contracts, and the deterministic temporal-holdout scorer. It never bundles a
model.
"""

from __future__ import annotations

from typing import Callable, Literal

from tessellum.composer.semantic_certificate import (
    Claim,
    ClaimScore,
    ConformalThresholds,
    certify,
)
from tessellum.dks.core import DKSWarrant, temporal_holdout_valid

# The epistemic type of a warrant's claim decides WHICH exogenous check applies.
ClaimType = Literal[
    "definitional",  # true by meaning/coherence → NLI entailment vs the span
    "support",       # an existence/support claim → FEVER retrieval (may abstain)
    "predictive",    # forecasts an outcome → prequential temporal holdout
    "deployed",      # a deployed causal claim → A/B + McNemar oracle
]

# A per-type scorer: (claim, warrant) -> ClaimScore. Injected for the model-
# backed types; DKS ships the deterministic temporal-holdout scorer.
TypeScorer = Callable[[Claim, DKSWarrant], ClaimScore]


def classify_claim(warrant: DKSWarrant) -> ClaimType:
    """Assign an epistemic type to a warrant's claim (A4.1).

    Deterministic + conservative: a warrant carrying tri-temporal outcome time
    is `predictive` (it forecasts something observable later); otherwise it
    defaults to `definitional` (checkable by coherence/entailment against its
    cited span). `support` and `deployed` are opt-in via an explicit marker in
    the warrant's ``qualifier`` (e.g. "deployed:" / "support:") so the router
    never silently mis-routes to a model that cannot judge the claim."""
    q = (warrant.qualifier or "").lower()
    if q.startswith("deployed"):
        return "deployed"
    if q.startswith("support"):
        return "support"
    if warrant.t_outcome is not None:
        return "predictive"
    return "definitional"


def temporal_holdout_scorer(claim: Claim, warrant: DKSWarrant) -> ClaimScore:
    """The DETERMINISTIC predictive-claim scorer (no external model).

    A predictive warrant is scorable only when its outcome is leakage-free
    (``temporal_holdout_valid`` on the P1 tri-temporal fields). When it is not,
    the score ABSTAINS (fail-closed — an un-scorable prediction must never be
    auto-accepted). When it is, we score it as fully grounded ONLY if the
    warrant's ``rebuttal`` (the observed-outcome record) confirms the claim;
    absent a recorded outcome the scorer abstains rather than guess."""
    if not temporal_holdout_valid(warrant.t_claim, warrant.t_evidence, warrant.t_outcome):
        return ClaimScore(claim.claim_id, 0.0, abstained=True)
    # A recorded, confirmed outcome (the prequential result) grounds it; an
    # un-recorded outcome is un-scorable → abstain.
    if not warrant.rebuttal:
        return ClaimScore(claim.claim_id, 0.0, abstained=True)
    confirmed = "confirmed" in warrant.rebuttal.lower() or "held" in warrant.rebuttal.lower()
    return ClaimScore(claim.claim_id, 1.0 if confirmed else 0.0, abstained=False)


class ClaimTypeRouter:
    """Routes each warrant's claim to its type-specific scorer, then produces a
    single `ClaimScorer` the shipped `certify(...)` consumes (A4.1 + A4.2).

    Model-backed scorers (definitional/support/deployed) are INJECTED; the
    deterministic temporal-holdout scorer is the default for `predictive`.
    A claim whose type has no registered scorer ABSTAINS (fail-closed) — it is
    ``dialectically-adequate-only``, not ``true`` (A4.3: no independent check
    available)."""

    def __init__(self, scorers: dict[ClaimType, TypeScorer] | None = None) -> None:
        self._scorers: dict[ClaimType, TypeScorer] = {
            "predictive": temporal_holdout_scorer,
        }
        if scorers:
            self._scorers.update(scorers)

    def score_one(self, claim: Claim, warrant: DKSWarrant) -> ClaimScore:
        ctype = classify_claim(warrant)
        scorer = self._scorers.get(ctype)
        if scorer is None:
            # no independent check available for this type → abstain (A4.3).
            return ClaimScore(claim.claim_id, 0.0, abstained=True)
        return scorer(claim, warrant)

    def as_claim_scorer(
        self, warrants_by_claim_id: dict[str, DKSWarrant]
    ) -> Callable[[list[Claim]], list[ClaimScore]]:
        """Adapt the router into the `ClaimScorer` signature `certify` expects.
        Each claim is scored by its warrant's type-routed scorer; a claim with
        no matching warrant abstains (fail-closed)."""
        def _scorer(claims: list[Claim]) -> list[ClaimScore]:
            out: list[ClaimScore] = []
            for c in claims:
                w = warrants_by_claim_id.get(c.claim_id)
                if w is None:
                    out.append(ClaimScore(c.claim_id, 0.0, abstained=True))
                else:
                    out.append(self.score_one(c, w))
            return out
        return _scorer


def validate_claims(
    claims: list[Claim],
    warrants_by_claim_id: dict[str, DKSWarrant],
    *,
    thresholds: ConformalThresholds,
    router: ClaimTypeRouter | None = None,
    note_domain: str | None = None,
):
    """A4.1 + A4.2 end-to-end: route each warrant's claim to its type scorer and
    run the SHIPPED conformal `certify(...)`. Returns the `CertificateResult`
    (accept / abstain) whose `.verdict` is the `GroundingVerdict` the runtime's
    `grounding_verifier` seam consumes — Dung-`IN` no longer self-certifies."""
    router = router or ClaimTypeRouter()
    return certify(
        claims,
        scorer=router.as_claim_scorer(warrants_by_claim_id),
        thresholds=thresholds,
        note_domain=note_domain,
    )


__all__ = [
    "ClaimType",
    "TypeScorer",
    "classify_claim",
    "temporal_holdout_scorer",
    "ClaimTypeRouter",
    "validate_claims",
]
