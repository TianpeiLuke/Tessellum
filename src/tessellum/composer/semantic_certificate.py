"""tessellum.composer.semantic_certificate — calibrated semantic certificate.

P7 of the dynamic-digestion plan "Dynamic Digestion as a Snapshot-Pinned
Knowledge Transaction". This is the deepest-risk phase: the semantic gate that
lets a capsule promote WITHOUT the P6 human-approval artifact, inside a measured
domain. It PRODUCES the :class:`~tessellum.composer.gates.GroundingVerdict` the
shipped grounding gate consumes (feeding the currently-unfed ``grounding_verifier``
seam) — so the composer boundary holds: a model produces evidence, a calibrated
program decides accept / abstain.

Scope of THIS module (what a code phase can honestly deliver):

- the **conformal-STYLE calibration** machinery and the **fail-closed
  abstain** decision, over a PLUGGABLE per-claim scorer. The actual NLI/SummaC
  entailment model is an injected dependency (``ClaimScorer``) — this module
  never bundles a model or a labeled corpus (that is the gating experiment,
  b3/A7.5, and must be run before the certificate gates anything unattended);
- **per-claim min-aggregation** (A7.2), NOT a holistic LLM-judge score;
- **separate calibration per failure class** (A7.3): claim grounding, omitted
  coverage, duplicate/merge disposition, and edge relevance;
- **per-class thresholds** (A7.4): a calibration set of labelled examples fixes
  the score threshold whose EMPIRICAL, IN-SAMPLE false-accept rate is at or under
  a target risk α; below the calibrated confidence → **abstain** (route to the
  human artifact / a coarser epoch), never a plausibility pass. This is a
  conformal-STYLE bound, not yet the finite-sample distribution-free guarantee
  the name "conformal risk control" formally denotes — the out-of-sample check is
  :func:`measure_false_accept_rate` on a held-out corpus, required below α before
  the certificate gates anything unattended (A7.5).

Determinism: given the same scorer outputs, the certificate decision is a pure
function (thresholds are frozen after calibration). No clock/randomness here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Literal

from tessellum.composer.gates import GroundingVerdict

# The four semantic failure classes the plan calibrates SEPARATELY (A7.3).
FailureClass = Literal["grounding", "coverage", "duplicate", "edge_relevance"]
FAILURE_CLASSES: tuple[FailureClass, ...] = (
    "grounding", "coverage", "duplicate", "edge_relevance",
)


@dataclass(frozen=True)
class Claim:
    """One checkable claim extracted from a note, with its cited source span."""

    claim_id: str
    text: str
    source_ref: str
    failure_class: FailureClass = "grounding"


@dataclass(frozen=True)
class ClaimScore:
    """A per-claim entailment score in [0, 1] from the injected scorer.

    ``score`` is the entailment probability of the claim against its cited span
    (1 = fully entailed). ``abstained`` marks a claim the scorer could not judge
    (out-of-distribution / source unreadable) — an abstain is fail-closed."""

    claim_id: str
    score: float
    abstained: bool = False


# A ClaimScorer is the injected NLI/SummaC-style model: claims -> scores. The
# real model lives behind this seam; the certificate never bundles one.
ClaimScorer = Callable[[list[Claim]], list[ClaimScore]]


@dataclass(frozen=True)
class ConformalThresholds:
    """Per-failure-class score thresholds fixed by conformal-style calibration.

    A claim of class ``c`` is accepted iff its score >= ``thresholds[c]``. The
    threshold is chosen so the empirical false-accept rate on the calibration
    set is bounded by the target risk α (A7.4). ``alpha`` and ``n_calibration``
    are recorded for audit; ``domains`` names the calibrated domain(s) — outside
    them the certificate must abstain."""

    thresholds: dict[FailureClass, float]
    alpha: float
    n_calibration: int
    domains: tuple[str, ...] = ()

    def threshold_for(self, cls: FailureClass) -> float | None:
        return self.thresholds.get(cls)


@dataclass(frozen=True)
class LabeledExample:
    """A calibration/eval example: a claim + its scorer score + ground-truth
    label (``True`` = the claim IS correct/faithful)."""

    failure_class: FailureClass
    score: float
    correct: bool


def calibrate(
    examples: list[LabeledExample],
    *,
    alpha: float,
    domains: tuple[str, ...] = (),
) -> ConformalThresholds:
    """Fix per-class thresholds so the false-ACCEPT rate is bounded by ``alpha``.

    For each failure class, choose the LOWEST threshold ``t`` such that among
    calibration claims with score >= t, the fraction that are actually INCORRECT
    (false accepts) is <= ``alpha``. This is the EMPIRICAL, IN-SAMPLE bound: we
    only accept in a score region whose observed error on THIS calibration set is
    under the target. It applies no finite-sample correction, so it is a
    conformal-STYLE bound, not yet the distribution-free coverage the name
    "conformal risk control" formally denotes — the out-of-sample validation is
    :func:`measure_false_accept_rate` on a held-out corpus, which must pass below
    ``alpha`` before this gates anything unattended (A7.5). A class with no example
    that can meet the bound gets threshold 1.01 (unreachable → always abstain for
    that class, fail-closed).

    Deterministic (sorts by score; no randomness)."""
    thresholds: dict[FailureClass, float] = {}
    for cls in FAILURE_CLASSES:
        cls_examples = sorted(
            (e for e in examples if e.failure_class == cls),
            key=lambda e: e.score,
        )
        chosen = 1.01  # unreachable → abstain unless a valid threshold is found
        # candidate thresholds = each distinct score; pick the lowest that
        # bounds the false-accept rate over the accepted (score >= t) region.
        candidate_scores = sorted({e.score for e in cls_examples})
        for t in candidate_scores:
            accepted = [e for e in cls_examples if e.score >= t]
            if not accepted:
                continue
            false_accepts = sum(1 for e in accepted if not e.correct)
            if false_accepts / len(accepted) <= alpha:
                chosen = t
                break
        thresholds[cls] = chosen
    return ConformalThresholds(
        thresholds=thresholds,
        alpha=alpha,
        n_calibration=len(examples),
        domains=domains,
    )


CertificateDecision = Literal["accept", "abstain"]


@dataclass(frozen=True)
class CertificateResult:
    """The certificate's decision over a note's claims (A7.4).

    ``decision`` is ``accept`` only when every claim's class threshold is met
    and no claim abstained; otherwise ``abstain`` (fail-closed). ``min_score``
    is the min-aggregated per-claim score (A7.2 — a note is only as grounded as
    its weakest claim). ``verdict`` is the :class:`GroundingVerdict` the shipped
    grounding gate consumes."""

    decision: CertificateDecision
    min_score: float
    verdict: GroundingVerdict
    failing_claims: tuple[str, ...] = field(default_factory=tuple)
    detail: str = ""


def certify(
    claims: list[Claim],
    *,
    scorer: ClaimScorer,
    thresholds: ConformalThresholds,
    note_domain: str | None = None,
) -> CertificateResult:
    """Certify a note's claims → an accept/abstain decision + a GroundingVerdict.

    Fail-closed at every uncertainty (A7.4):
    - no claims → abstain (nothing to ground on; a note with no checkable claim
      is not auto-accepted);
    - the note's domain is outside the calibrated ``domains`` → abstain;
    - any claim the scorer abstained on → abstain;
    - any claim whose score is below its class threshold → abstain;
    - only when EVERY claim clears its calibrated class threshold → accept.

    Aggregation is per-claim min (A7.2), never a holistic score."""
    if not claims:
        return CertificateResult(
            "abstain", 0.0,
            GroundingVerdict("ungrounded", "no checkable claims — fail-closed"),
            detail="empty claim set",
        )
    # Fail-closed domain gate: an EMPTY calibrated-domain set means "no domain
    # has passed A7.5" → abstain everywhere (NOT "accept everywhere"). Only a
    # note whose domain is explicitly in a non-empty calibrated set proceeds.
    # (A calibration that legitimately spans all domains records a sentinel
    # domain and passes it as note_domain — it never leaves domains empty.)
    if not thresholds.domains or note_domain not in thresholds.domains:
        return CertificateResult(
            "abstain", 0.0,
            GroundingVerdict("ungrounded",
                             f"domain {note_domain!r} not in calibrated {thresholds.domains} "
                             "(empty = no domain passed A7.5)"),
            detail="out-of-calibrated-domain",
        )

    scores = {s.claim_id: s for s in scorer(claims)}
    failing: list[str] = []
    min_score = 1.0
    for claim in claims:
        s = scores.get(claim.claim_id)
        if s is None or s.abstained:
            failing.append(claim.claim_id)
            min_score = 0.0
            continue
        min_score = min(min_score, s.score)
        t = thresholds.threshold_for(claim.failure_class)
        if t is None or s.score < t:
            failing.append(claim.claim_id)

    if failing:
        return CertificateResult(
            "abstain", min_score,
            GroundingVerdict("ungrounded",
                             f"{len(failing)} claim(s) below calibrated threshold / abstained"),
            failing_claims=tuple(sorted(failing)),
            detail="below-threshold or scorer-abstain (fail-closed)",
        )
    return CertificateResult(
        "accept", min_score,
        GroundingVerdict("grounded",
                         f"all {len(claims)} claims cleared calibrated thresholds "
                         f"(min score {min_score:.3f}, α={thresholds.alpha})"),
    )


def measure_false_accept_rate(
    examples: list[LabeledExample],
    thresholds: ConformalThresholds,
) -> dict[FailureClass, float]:
    """A7.5 gating measurement: the empirical false-accept rate per class on a
    (held-out) labelled set under the calibrated thresholds. This is what must
    be shown below the target α on a real wrong-but-well-formed corpus BEFORE
    the certificate gates anything unattended."""
    out: dict[FailureClass, float] = {}
    for cls in FAILURE_CLASSES:
        t = thresholds.threshold_for(cls)
        cls_examples = [e for e in examples if e.failure_class == cls]
        accepted = [e for e in cls_examples if t is not None and e.score >= t]
        if not accepted:
            out[cls] = 0.0
            continue
        out[cls] = sum(1 for e in accepted if not e.correct) / len(accepted)
    return out


__all__ = [
    "FailureClass",
    "FAILURE_CLASSES",
    "Claim",
    "ClaimScore",
    "ClaimScorer",
    "ConformalThresholds",
    "LabeledExample",
    "calibrate",
    "CertificateResult",
    "CertificateDecision",
    "certify",
    "measure_false_accept_rate",
]
