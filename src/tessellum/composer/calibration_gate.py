"""tessellum.composer.calibration_gate — the A7.5 go/no-go harness.

The calibrated certificate may gate UNATTENDED promotion only after its
held-out false-accept rate is shown at or under the target risk α on a real
corpus of wrong-but-well-formed notes (A7.5). ``semantic_certificate`` ships the
pieces — ``calibrate`` (fit thresholds on a train split) and
``measure_false_accept_rate`` (score a held-out split) — but nothing ties them
into a single train/held-out **decision** a release can hinge on. This module is
that harness, plus the typed corpus it consumes.

What it delivers (all pure — no clock/randomness/I/O in the gate itself):

- :class:`CorpusExample` / :class:`CalibrationCorpus` — the typed labelled
  corpus (per-claim ``failure_class`` + scorer ``score`` + ground-truth
  ``correct``), with a deterministic train/held-out split by index.
- :func:`run_calibration_gate` — calibrate on train, measure held-out
  false-accept per class, and return a :class:`CalibrationGateResult` whose
  ``unattended_ok`` is ``True`` ONLY when EVERY class's held-out FAR ≤ α AND the
  held-out split is non-trivially populated. Fail-closed: an empty/one-sided
  split, or any class over α, is a NO-GO.

**Honest ceiling.** A go/no-go on a SYNTHETIC seed corpus proves the harness
computes the right verdict; it does NOT license unattended promotion. The
release criterion is this gate returning GO on a REAL, human-labelled corpus of
wrong-but-well-formed notes, scored by the REAL injected model — the standing
research prerequisite. Until then the certificate abstains and promotion stays
human-supervised (M4 / P6).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from tessellum.composer.semantic_certificate import (
    FAILURE_CLASSES,
    ConformalThresholds,
    FailureClass,
    LabeledExample,
    calibrate,
    measure_false_accept_rate,
)


@dataclass(frozen=True)
class CorpusExample:
    """One labelled calibration/eval example (a superset of
    :class:`~tessellum.composer.semantic_certificate.LabeledExample` carrying an
    id + domain for audit + stratification).

    ``score`` is the scorer's entailment score for the claim; ``correct`` is the
    human ground truth (``True`` = the claim IS faithful). A ``correct=False``
    example with a HIGH score is exactly the wrong-but-well-formed case the
    certificate must not false-accept."""

    example_id: str
    failure_class: FailureClass
    score: float
    correct: bool
    domain: str = ""

    def as_labeled(self) -> LabeledExample:
        return LabeledExample(
            failure_class=self.failure_class, score=self.score, correct=self.correct
        )


@dataclass(frozen=True)
class CalibrationCorpus:
    """A typed labelled corpus for the A7.5 gate.

    ``examples`` are split deterministically by index (even indices → train,
    odd → held-out) so the gate is reproducible and needs no RNG; ``domains``
    records the domain(s) the calibrated thresholds will claim (outside them the
    certificate abstains)."""

    examples: tuple[CorpusExample, ...]
    domains: tuple[str, ...] = ()

    def split(self) -> tuple[list[CorpusExample], list[CorpusExample]]:
        """Deterministic, STRATIFIED (train, held_out) split — pure.

        Grouping by ``(failure_class, correct)`` and alternating within each
        stratum (rather than a raw even/odd index split) keeps both splits
        representative of the label distribution, so a hand-ordered corpus can't
        accidentally segregate all correct claims into one split. Order within a
        stratum is the corpus's declared order; strata are visited in a stable
        sorted key order for reproducibility."""
        strata: dict[tuple[str, bool], list[CorpusExample]] = {}
        for e in self.examples:
            strata.setdefault((e.failure_class, e.correct), []).append(e)
        train: list[CorpusExample] = []
        held_out: list[CorpusExample] = []
        for key in sorted(strata):
            for i, e in enumerate(strata[key]):
                (train if i % 2 == 0 else held_out).append(e)
        return train, held_out


@dataclass(frozen=True)
class CalibrationGateResult:
    """The A7.5 go/no-go verdict.

    Attributes:
        unattended_ok: ``True`` iff the certificate MAY gate unattended in the
            calibrated domain — every class's held-out FAR ≤ α, the certificate
            actually ACCEPTS a non-trivial fraction of genuinely-correct held-out
            claims (not a degenerate always-abstain), AND the held-out split is
            populated. This is the release criterion.
        alpha: the target risk the gate was run at.
        thresholds: the per-class thresholds fitted on the TRAIN split.
        held_out_far: per-class false-accept rate measured on the HELD-OUT split.
        held_out_recall: per-class fraction of genuinely-CORRECT held-out claims
            the calibrated threshold accepts (usefulness — a threshold that
            abstains on everything is sound but useless).
        n_train / n_held_out: split sizes (a tiny/empty held-out split is a
            NO-GO regardless of FAR — you can't certify on no evidence).
        reasons: per-class / structural NO-GO causes (empty on GO).
    """

    unattended_ok: bool
    alpha: float
    thresholds: ConformalThresholds
    held_out_far: dict[FailureClass, float]
    held_out_recall: dict[FailureClass, float]
    n_train: int
    n_held_out: int
    reasons: tuple[str, ...] = field(default_factory=tuple)


# A held-out split must have at least this many examples to certify on — a gate
# that "passes" on one or two held-out points is not evidence. Conservative.
MIN_HELD_OUT = 8

# A calibrated threshold must accept at least this fraction of genuinely-CORRECT
# held-out claims (per class that HAS correct held-out examples) — otherwise it
# is a degenerate always-abstain: sound (FAR 0) but useless (it never enables
# unattended promotion, it just routes everything to the human). Usefulness bar.
MIN_HELD_OUT_RECALL = 0.5

# Each PRESENT class must have at least this many held-out examples AND at least
# one CORRECT and one INCORRECT held-out example — otherwise its held-out FAR
# (needs an incorrect, high-scoring example to be non-vacuous) and its recall
# (needs a correct example) are unmeasured, and MIN_HELD_OUT over the TOTAL
# split does not catch a starved class. Fail-closed: you cannot certify a class
# unattended on evidence it doesn't have.
MIN_HELD_OUT_PER_CLASS = 4


def _held_out_recall(
    held_out: list[CorpusExample], thresholds: ConformalThresholds
) -> dict[FailureClass, float]:
    """Per-class fraction of genuinely-correct held-out claims the calibrated
    threshold ACCEPTS (score ≥ threshold). A class with no correct held-out
    example is reported as 1.0 (vacuously fine — nothing to accept). Pure."""
    out: dict[FailureClass, float] = {}
    for cls in FAILURE_CLASSES:
        t = thresholds.threshold_for(cls)
        correct = [e for e in held_out if e.failure_class == cls and e.correct]
        if not correct:
            out[cls] = 1.0
            continue
        accepted = sum(1 for e in correct if t is not None and e.score >= t)
        out[cls] = accepted / len(correct)
    return out


def run_calibration_gate(
    corpus: CalibrationCorpus,
    *,
    alpha: float,
    min_held_out: int = MIN_HELD_OUT,
    min_recall: float = MIN_HELD_OUT_RECALL,
    min_held_out_per_class: int = MIN_HELD_OUT_PER_CLASS,
) -> CalibrationGateResult:
    """Run the A7.5 train/held-out go/no-go (pure, deterministic).

    Fit per-class thresholds on the TRAIN split at target risk ``alpha``, then on
    the disjoint HELD-OUT split measure both the false-accept rate (soundness)
    and the acceptance rate over genuinely-correct claims (usefulness).
    ``unattended_ok`` is ``True`` only when:

    - the held-out split has ≥ ``min_held_out`` examples (enough to certify on);
    - every failure class's held-out FAR ≤ ``alpha`` (SOUND); AND
    - every class that has correct held-out claims accepts ≥ ``min_recall`` of
      them (USEFUL — not a degenerate always-abstain that "passes" FAR by
      accepting nothing).

    Otherwise it is a fail-closed NO-GO with the causes in ``reasons``. This
    measures the fitted thresholds on UNSEEN data — the out-of-sample check the
    certificate docstring names as the gate before anything runs unattended.
    """
    train, held_out = corpus.split()
    thresholds = calibrate(
        [e.as_labeled() for e in train], alpha=alpha, domains=corpus.domains
    )
    held_out_far = measure_false_accept_rate(
        [e.as_labeled() for e in held_out], thresholds
    )
    held_out_recall = _held_out_recall(held_out, thresholds)

    reasons: list[str] = []
    if len(held_out) < min_held_out:
        reasons.append(
            f"held-out split too small ({len(held_out)} < {min_held_out}) — "
            "insufficient evidence to certify unattended"
        )
    # Which classes actually occur in this corpus (a class with no examples is
    # not gated — it simply isn't in the calibrated domain's claim mix).
    present = {e.failure_class for e in corpus.examples}
    for cls in FAILURE_CLASSES:
        if cls not in present:
            continue
        # Per-class held-out evidence FIRST: FAR needs an incorrect held-out
        # example to be non-vacuous, recall needs a correct one, and the total
        # MIN_HELD_OUT does not catch a class starved of held-out data. Without
        # this a class present only in train (or with all-one-label held-out)
        # would auto-pass on vacuous FAR=0 / recall=1.0 — a false GO.
        cls_held = [e for e in held_out if e.failure_class == cls]
        n_correct = sum(1 for e in cls_held if e.correct)
        n_incorrect = len(cls_held) - n_correct
        if len(cls_held) < min_held_out_per_class or n_correct == 0 or n_incorrect == 0:
            reasons.append(
                f"{cls}: insufficient held-out evidence "
                f"({len(cls_held)} examples, {n_correct} correct, "
                f"{n_incorrect} incorrect; need ≥{min_held_out_per_class} with "
                "both labels) — FAR/recall unmeasurable, cannot certify unattended"
            )
            continue
        t = thresholds.threshold_for(cls)
        if t is None or t > 1.0:
            # calibration found NO score region meeting α on train → the only
            # "sound" threshold is unreachable (always-abstain). Sound but
            # useless: a fail-closed NO-GO, independent of the split.
            reasons.append(
                f"{cls}: no calibrated threshold meets α {alpha:.3f} on train — "
                "always-abstain, no unattended gain"
            )
            continue
        far = held_out_far.get(cls, 0.0)
        if far > alpha:
            reasons.append(f"{cls}: held-out FAR {far:.3f} > α {alpha:.3f}")
        recall = held_out_recall.get(cls, 1.0)
        if recall < min_recall:
            reasons.append(
                f"{cls}: held-out acceptance of correct claims {recall:.3f} < "
                f"{min_recall:.3f} — degenerate always-abstain, no unattended gain"
            )

    return CalibrationGateResult(
        unattended_ok=not reasons,
        alpha=alpha,
        thresholds=thresholds,
        held_out_far=held_out_far,
        held_out_recall=held_out_recall,
        n_train=len(train),
        n_held_out=len(held_out),
        reasons=tuple(reasons),
    )


__all__ = [
    "CorpusExample",
    "CalibrationCorpus",
    "CalibrationGateResult",
    "MIN_HELD_OUT",
    "run_calibration_gate",
]
