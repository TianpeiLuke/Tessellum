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
    * deployed causal (a model already serving traffic) → the A/B + McNemar
      oracle (injected).
- A4.2 — the **wiring**: build the `GroundingVerdict` from `certify(...)` and
  hand it to the runtime's `grounding_verifier` seam (unfed today);
- A4.3 — **Dung as a pre-filter**, never the terminal verdict: a claim with no
  available independent check is `dialectically-adequate-only`, not `true`.

The real NLI / FEVER / A/B scorers are injected dependencies (the same seam
`semantic_certificate` already expects); this module ships the router, the
contracts, and the deterministic temporal-holdout scorer. It never bundles a
model.

**The query-time wiring (P8), and why it is opt-in.** `validate_claims` was
written, behaviour-tested and never called — it is the independent check the
acceptance axis needs before anything can be `accepted` rather than merely
`dialectically_adequate`. The query-time protocol calls it now, through
:func:`independent_validation`, and the call is **opt-in for one substantive
reason, not for caution's sake**: `certify` takes `ConformalThresholds` fixed on
a labelled calibration corpus, and no such corpus exists for query-time relation
claims. So the last section of this module ships three things and nothing more —
a deterministic lexical :data:`TypeScorer` (:func:`lexical_type_scorer`) over the
same injected seam, an explicitly labelled :func:`uncalibrated_thresholds` that
can only ever admit the :data:`UNCALIBRATED_DOMAIN` sentinel, and
:func:`independent_validation`, which reduces a `CertificateResult` to the single
boolean the acceptance axis consumes. All three carry
:data:`A7_5_UNCALIBRATED_NOTICE`, because "validated" from an un-calibrated
threshold is a wiring result, not an entailment result.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal, Mapping, Sequence

from tessellum.composer.lexical_scorer import make_lexical_scorer
from tessellum.composer.semantic_certificate import (
    FAILURE_CLASSES,
    CertificateResult,
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


# ── P8 wiring: the independent validator, run UN-CALIBRATED and opt-in ──────

A7_5_UNCALIBRATED_NOTICE = (
    "ENTAILMENT IS UN-CALIBRATED. The shipped grounding certificate is "
    "fail-closed until it is calibrated on a real model plus a human-labelled "
    "corpus (the semantic-certificate A7.5 prereq), and no such corpus exists "
    "for query-time relation claims — the one shipped calibration artifact "
    "covers note-grounding on a single slice. A 'validated' verdict obtained "
    "with uncalibrated_thresholds() therefore records that the certify -> "
    "verdict -> acceptance loop RUNS, not that the claim is entailed by its "
    "cited span. Nothing may be promoted on this basis; the deterministic "
    "lexical scorer behind it cannot see negation or reordering at all."
)
"""The caveat every un-calibrated validation verdict carries, in the verdict.

Recorded as data rather than a comment so a caller cannot obtain a ``validated``
answer without also holding the reason it does not mean what it looks like."""

UNCALIBRATED_DOMAIN: str = "uncalibrated"
"""The sentinel domain :func:`uncalibrated_thresholds` calibrates.

Load-bearing rather than cosmetic. ``certify`` abstains unless ``note_domain`` is
in the thresholds' ``domains``, so pinning the sentinel means a caller that
passes a *real* domain still abstains: un-calibrated thresholds cannot be
pointed at production traffic by accident, only by naming the sentinel."""


def uncalibrated_thresholds(
    accept_at: float, *, alpha: float = 1.0
) -> ConformalThresholds:
    """Thresholds for running the certificate with **no calibration corpus**.

    ``accept_at`` is applied to every failure class, and ``alpha`` defaults to
    ``1.0`` — "no risk bound established" — because recording a tighter α would
    claim a guarantee no calibration set backs. ``n_calibration=0`` says the same
    thing in the audit field, and ``domains`` is :data:`UNCALIBRATED_DOMAIN`
    alone, so these thresholds admit nothing outside the sentinel.

    For wiring, A/B measurement and tests. Read
    :data:`A7_5_UNCALIBRATED_NOTICE` before using the result for anything else;
    calibrated thresholds come from
    :func:`~tessellum.composer.semantic_certificate.calibrate` over labelled
    examples, which is a research prerequisite and not this module's to fake.
    """
    return ConformalThresholds(
        thresholds={cls: accept_at for cls in FAILURE_CLASSES},
        alpha=alpha,
        n_calibration=0,
        domains=(UNCALIBRATED_DOMAIN,),
    )


def lexical_type_scorer(span_text_of: Callable[[str], str | None]) -> TypeScorer:
    """A deterministic, model-free :data:`TypeScorer` over the injected seam.

    Wraps the shipped reference
    :func:`~tessellum.composer.lexical_scorer.make_lexical_scorer` into the
    per-``(claim, warrant)`` shape the router dispatches on. The warrant is
    unused: the lexical proxy scores the claim against its cited span and nothing
    else, which is exactly why it is a baseline — it is the analogue of the
    deterministic temporal-holdout scorer, not a stand-in for entailment. It
    abstains (fail-closed) when the span is unresolvable.
    """
    scorer = make_lexical_scorer(span_text_of)

    def _score(claim: Claim, _warrant: DKSWarrant) -> ClaimScore:
        return scorer([claim])[0]

    return _score


def lexical_router(
    span_text_of: Callable[[str], str | None],
    *,
    types: Sequence[ClaimType] = ("definitional", "support"),
) -> ClaimTypeRouter:
    """A :class:`ClaimTypeRouter` whose text-judging types use the lexical proxy.

    ``predictive`` keeps the deterministic temporal-holdout scorer (the router's
    own default) and ``deployed`` deliberately gets none, so a deployed causal
    claim still abstains for want of an A/B oracle. This is the reference router
    a caller injects when no entailment model is available — the real NLI/FEVER
    scorers drop into the same seam without touching this module.
    """
    scorer = lexical_type_scorer(span_text_of)
    return ClaimTypeRouter({ctype: scorer for ctype in types})


@dataclass(frozen=True)
class IndependentValidation:
    """The exogenous check reduced to what the acceptance axis consumes.

    ``validated`` is the single boolean
    :func:`~tessellum.dks.ontology.acceptance_from_labelling` takes as
    ``independently_validated``: ``True`` promotes a surviving claim from
    ``dialectically_adequate`` to ``accepted``. It is ``True`` only on an
    ``accept`` decision, so every fail-closed path in ``certify`` — no claims,
    out-of-calibrated-domain, a scorer abstention, a below-threshold score —
    lands as ``False``.

    ``notice`` is non-empty exactly when the thresholds were un-calibrated, and
    it travels with the verdict so the caveat cannot be separated from the
    result. ``result`` is the untouched ``CertificateResult`` for a caller that
    wants the ``GroundingVerdict`` the runtime's ``grounding_verifier`` seam
    consumes.
    """

    validated: bool
    decision: str
    min_score: float
    failing_claims: tuple[str, ...] = ()
    notice: str = ""
    result: CertificateResult | None = None


def independent_validation(
    claims: list[Claim],
    warrants_by_claim_id: dict[str, DKSWarrant],
    *,
    thresholds: ConformalThresholds,
    router: ClaimTypeRouter | None = None,
    note_domain: str | None = None,
) -> IndependentValidation:
    """Run :func:`validate_claims` and reduce it to an acceptance-axis verdict.

    This is the call that makes ``validate_claims`` live. It changes no default:
    a caller that does not ask for validation gets none, and the acceptance axis
    then reports ``dialectically_adequate`` exactly as it does today. Whether the
    verdict means anything depends entirely on the thresholds — see
    :data:`A7_5_UNCALIBRATED_NOTICE`.
    """
    result = validate_claims(
        claims,
        warrants_by_claim_id,
        thresholds=thresholds,
        router=router,
        note_domain=note_domain,
    )
    return IndependentValidation(
        validated=result.decision == "accept",
        decision=result.decision,
        min_score=result.min_score,
        failing_claims=tuple(result.failing_claims),
        notice=(
            A7_5_UNCALIBRATED_NOTICE if thresholds.n_calibration == 0 else ""
        ),
        result=result,
    )


def warrants_for_claims(
    claims: Sequence[Claim], warrant: DKSWarrant
) -> dict[str, DKSWarrant]:
    """Map every claim id onto one warrant — the single-warrant router input.

    A query-time derivation licenses its claims with one Toulmin warrant (the
    named relation and the reason it applies), so the per-claim mapping
    ``validate_claims`` wants is a fan-out rather than a lookup. Kept here beside
    the router so the query path does not rebuild the router's input shape."""
    return {claim.claim_id: warrant for claim in claims}


def span_text_lookup(spans: Mapping[str, str]) -> Callable[[str], str | None]:
    """A pure ``source_ref -> span text`` resolver over an in-memory mapping.

    The certificate resolves a claim's cited span through an injected callable so
    the composer stays free of vault I/O. A query-time derivation already holds
    the spans it read, so the mapping *is* the resolver — no file is opened to
    re-read text the episode has in hand."""

    def _lookup(source_ref: str) -> str | None:
        return spans.get(source_ref)

    return _lookup


__all__ = [
    "A7_5_UNCALIBRATED_NOTICE",
    "UNCALIBRATED_DOMAIN",
    "ClaimType",
    "ClaimTypeRouter",
    "IndependentValidation",
    "TypeScorer",
    "classify_claim",
    "independent_validation",
    "lexical_router",
    "lexical_type_scorer",
    "span_text_lookup",
    "temporal_holdout_scorer",
    "uncalibrated_thresholds",
    "validate_claims",
    "warrants_for_claims",
]
