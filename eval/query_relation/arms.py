#!/usr/bin/env python3
"""The three arms of the role/relation answer A/B, the statistical controls, and
the admission rule — plan phases P2 (node-first admission gate) and P11 (the
derivation A/B).

The three arms
--------------
    arm 1  status quo      the existing answer path, unchanged. It is the arm
                           that conflates the author of a note with the steward
                           of the thing the note describes, and in this
                           repository it CANNOT RUN: that path lives in the
                           application that embeds Tessellum, not here. It is
                           declared with :func:`external_arm` and reported as
                           NOT RUN — never as a row of zeros, which would read
                           as a measured loss.
    arm 2  node-first      resolve the mention to one entity, read THAT note's
                           own authored field with its locator, and ABSTAIN when
                           the field is absent. Model-free. Runnable here today
                           against an injected resolver + field reader.
    arm 3  derivation      consult memory / the authored read first, and only on
                           a miss name the relation, read the claim out of the
                           reached notes with its span, attempt a bounded
                           refutation, and decide three ways. Runnable here
                           against an injected derivation port; the port is
                           where a model would live, and it is never called
                           directly by this module.

The admission rule, encoded rather than described
-------------------------------------------------
Arm 3 is admitted only if it beats **arm 2** — not arm 1 — by more than THIS
harness's own estimated uncertainty. That is enforced by
:func:`admission_verdict`, which raises on a P11 comparison whose baseline is not
the node-first arm, so the cheap baseline cannot be swapped out for the
flattering one.

The bar is a **paired** estimate, computed here and nowhere else: both arms
answer the same questions, so the per-question difference is taken and the
uncertainty of ITS mean is estimated (paired bootstrap by default, seeded and
therefore replayable; the paired standard error is reported alongside). A gain
whose interval includes zero has not been separated from this harness's own
noise. No figure is imported from another experiment for this purpose — see
``metrics.HISTORICAL_BUILD_NOISE_INTERVAL`` for the one that exists, why it is
asymmetric, and why it is reference-only.

On top of that the rule requires, and refuses without:

  * n repeated runs per arm, with the run-to-run spread REPORTED (it is a
    reported quantity, not an ad-hoc subtraction from the gain);
  * at least two question orderings, with the gain required to hold under EVERY
    one of them (a gain that exists under one ordering and vanishes under
    another is an order artifact, and the literature this plan cites found
    memory-loop gains to be exactly that);
  * no unjustified rise in abstention on the answerable questions;
  * no per-query model-budget violation, since an arm that outspends its cap has
    not won at matched cost.

A caller who wants an ADDITIONAL absolute floor — a practical-significance
level, or a figure from some other experiment they are prepared to defend —
passes ``min_gain=`` explicitly. There is no default.

Arms are built by FACTORIES so every run and every ordering gets a fresh arm: an
arm that carries a cache would otherwise leak a warm state across runs, which is
the very artifact the ordering control exists to detect.

Nothing here calls a model or touches a vault, and no arm is wired to a live
answer path. See ``README.md`` for what must be supplied from outside, and for
the plain statement that no result has been produced.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import random
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Mapping, Protocol, Sequence


def _load_sibling(module_file: str, register_as: str):
    """Load a sibling eval module by path.

    ``eval/`` is not a package (the digestion-pipeline harness and its tools are
    plain scripts), so the sibling is loaded explicitly and registered under a
    qualified name rather than injected as a bare top-level ``metrics``, which
    would collide with any other module of that name in a test session."""
    path = Path(__file__).resolve().parent / module_file
    spec = importlib.util.spec_from_file_location(register_as, path)
    if spec is None or spec.loader is None:  # pragma: no cover — path is fixed
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[register_as] = module
    spec.loader.exec_module(module)
    return module


_m = _load_sibling("metrics.py", "query_relation_metrics")

# The sibling module object itself, so a caller reaches the metrics through THIS
# module rather than loading a second copy: two loads would define two distinct
# `Locator` classes, and frozen-dataclass equality is class-based, so locators
# built on one side would silently never match the other's.
metrics = _m

# Re-exported so a caller needs one import for the harness.
PRIMARY_METRIC = _m.PRIMARY_METRIC
METRIC_NAMES = _m.METRIC_NAMES
AnswerAttempt = _m.AnswerAttempt
ArmMetrics = _m.ArmMetrics
BudgetPolicy = _m.BudgetPolicy
Locator = _m.Locator
MetricSummary = _m.MetricSummary
ModelBudget = _m.ModelBudget
Question = _m.Question
QuestionSet = _m.QuestionSet
QuestionSetError = _m.QuestionSetError
load_question_set = _m.load_question_set
metric_value = _m.metric_value
score_arm = _m.score_arm
summarise = _m.summarise

# The paired estimator: the harness's own uncertainty, and the historical
# interval it deliberately does NOT use as a threshold.
HISTORICAL_BUILD_NOISE_INTERVAL = _m.HISTORICAL_BUILD_NOISE_INTERVAL
MeasuredInterval = _m.MeasuredInterval
NotPairable = _m.NotPairable
PairedDifferences = _m.PairedDifferences
PairedUncertainty = _m.PairedUncertainty
PAIRABLE_METRICS = _m.PAIRABLE_METRICS
PAIRED_BOOTSTRAP = _m.PAIRED_BOOTSTRAP
PAIRED_METHODS = _m.PAIRED_METHODS
PAIRED_STANDARD_ERROR = _m.PAIRED_STANDARD_ERROR
DEFAULT_BOOTSTRAP_RESAMPLES = _m.DEFAULT_BOOTSTRAP_RESAMPLES
DEFAULT_BOOTSTRAP_SEED = _m.DEFAULT_BOOTSTRAP_SEED
DEFAULT_CONFIDENCE = _m.DEFAULT_CONFIDENCE
MIN_PAIRED_QUESTIONS = _m.MIN_PAIRED_QUESTIONS
UNPAIRABLE_METRICS = _m.UNPAIRABLE_METRICS
check_pairable = _m.check_pairable
paired_differences = _m.paired_differences
paired_uncertainty = _m.paired_uncertainty
per_question_scores = _m.per_question_scores

ARM_STATUS_QUO = "arm1_status_quo"
ARM_NODE_FIRST = "arm2_node_first"
ARM_DERIVATION = "arm3_derivation"

# Repeated runs and at least two orderings are both required by the plan; these
# are the defaults the admission rule also enforces as minima.
DEFAULT_RUNS = 3
MIN_RUNS = 3
MIN_ORDERINGS = 2
DEFAULT_ORDERINGS: tuple[str, ...] = ("as_given", "shuffle:ordering_a", "shuffle:ordering_b")


class ArmUnavailable(RuntimeError):
    """Raised by an arm that cannot run here (its answer path is elsewhere).

    Caught by the runner and recorded as NOT RUN. It is never converted into a
    score: a missing arm and an arm that scored zero are different facts, and
    conflating them would let a comparison look decided when it is not."""


# ────────────────────────────────────────────────────────────────── the ports ────


@dataclass(frozen=True)
class Resolution:
    """What step 1 made of a surface mention.

    ``entity_id`` set = one canonical entity. ``candidates`` longer than one =
    ambiguous, and the arm must return candidates or abstain rather than pick;
    both empty = unresolvable."""

    entity_id: str | None = None
    candidates: tuple[str, ...] = ()
    entity_type: str | None = None

    @property
    def ambiguous(self) -> bool:
        return self.entity_id is None and len(self.candidates) > 1


@dataclass(frozen=True)
class FieldRead:
    """One authored, node-attached fact read off the resolved entity's own note.

    ``valid_to`` carries the validity interval's close. A closed interval is not
    a current answer — a role fact without one confidently returns a former
    holder — so the node-first arm abstains on it instead of answering."""

    value: str
    locator: Locator
    valid_from: str | None = None
    valid_to: str | None = None


@dataclass(frozen=True)
class DerivationRequest:
    """What arm 3 hands its derivation port after the cheap read missed."""

    question: Question
    resolution: Resolution
    suppressed: tuple[Locator, ...] = ()
    policy: BudgetPolicy = BudgetPolicy()


@dataclass(frozen=True)
class DerivationResult:
    """What the port returns: one of the three decisions, with its evidence.

    ``budget`` is the port's own model spend and is reported unchanged — the
    harness never estimates it."""

    outcome: str
    answer: str = ""
    locators: tuple[Locator, ...] = ()
    budget: ModelBudget = ModelBudget()
    reason: str = ""


# Every model-shaped step sits behind one of these. The default implementations
# in this module are deterministic and call nothing.
Resolver = Callable[[str], Resolution]
FieldReader = Callable[[str, str], "FieldRead | None"]
DerivationPort = Callable[[DerivationRequest], DerivationResult]


class ArmFn(Protocol):
    """One arm: a question in, one attempt out.

    ``suppressed`` withholds spans from the arm. The runner uses it for the
    bridge-ablated re-ask that the connected-reasoning control needs; an arm
    must not read a suppressed locator."""

    def __call__(
        self, question: Question, *, suppressed: tuple[Locator, ...] = ()
    ) -> AnswerAttempt: ...


ArmFactory = Callable[[], ArmFn]


def _suppressed(locator: Locator, suppressed: Sequence[Locator]) -> bool:
    """True when a span was withheld from the arm for this attempt."""
    return any(locator.satisfies(s) or s.satisfies(locator) for s in suppressed)


# ──────────────────────────────────────────────────────────── arm 1: baseline ────


def external_arm(name: str, reason: str) -> ArmFactory:
    """Declare an arm whose answer path is not in this repository.

    Every attempt to build it raises :class:`ArmUnavailable`, so the report says
    NOT RUN and the admission rule refuses to conclude anything that needed it.
    This is the only honest representation of arm 1 here: the status-quo answer
    path, the one that conflates authorship with stewardship, lives in the
    application that embeds Tessellum."""

    def factory() -> ArmFn:
        raise ArmUnavailable(f"{name}: {reason}")

    return factory


def status_quo_arm(reason: str = "") -> ArmFactory:
    """Arm 1, declared unavailable with the standing reason."""
    return external_arm(
        ARM_STATUS_QUO,
        reason
        or (
            "the status-quo answer path (and the entity/polarity answer eval it "
            "is scored by) lives outside this repository; supply it as an "
            "ArmFactory to run this arm"
        ),
    )


# ─────────────────────────────────────────────────────────── arm 2: node-first ────


def node_first_arm(resolve: Resolver, read_field: FieldReader) -> ArmFactory:
    """Arm 2: resolve, read the resolved note's own authored field, else abstain.

    Model-free by construction — resolution is matching and the read is one note
    access — so its per-query model budget is zero and every gain arm 3 claims is
    a gain over a free baseline. The four abstentions are all deliberate:
    unresolvable, ambiguous, field absent, and a field whose validity interval
    has closed."""

    def factory() -> ArmFn:
        def answer(
            question: Question, *, suppressed: tuple[Locator, ...] = ()
        ) -> AnswerAttempt:
            res = resolve(question.target.surface)
            if res.ambiguous:
                return AnswerAttempt(
                    qid=question.qid,
                    outcome="abstained",
                    reason="ambiguous_entity",
                    diagnostics=tuple(f"candidate={c}" for c in res.candidates),
                    suppressed=suppressed,
                )
            if res.entity_id is None:
                return AnswerAttempt(
                    qid=question.qid,
                    outcome="abstained",
                    reason="entity_unresolvable",
                    suppressed=suppressed,
                )
            read = read_field(res.entity_id, question.relation)
            if read is None or _suppressed(read.locator, suppressed):
                return AnswerAttempt(
                    qid=question.qid,
                    outcome="abstained",
                    reason="field_absent",
                    suppressed=suppressed,
                )
            if read.valid_to is not None:
                return AnswerAttempt(
                    qid=question.qid,
                    outcome="abstained",
                    reason="superseded_only",
                    diagnostics=(f"valid_to={read.valid_to}",),
                    suppressed=suppressed,
                )
            return AnswerAttempt(
                qid=question.qid,
                outcome="answered",
                answer=read.value,
                locators=(read.locator,),
                reason="authored_field",
                suppressed=suppressed,
            )

        return answer

    return factory


# ────────────────────────────────────────────────────────── arm 3: derivation ────


def derivation_arm(
    resolve: Resolver,
    read_field: FieldReader,
    derive: DerivationPort,
    *,
    policy: BudgetPolicy | None = None,
) -> ArmFactory:
    """Arm 3: the cheap read first, derivation only on a miss.

    Two rules are enforced here rather than left to the port, because both are
    acceptance conditions of the phases this measures:

      * an answer with no locator is converted to an abstention — the decision
        path must never produce an ungrounded assertion;
      * a budget over policy is recorded on the attempt as a diagnostic AND left
        in the counted budget, so the admission rule can refuse on it. It is not
        clipped, which would hide the overspend.

    Ordering of the two stages is the "consult memory before deriving" rule: an
    authored hit costs zero model calls, so the realised per-query budget depends
    on how often the cheap path already answers."""
    pol = policy or BudgetPolicy()

    def factory() -> ArmFn:
        def answer(
            question: Question, *, suppressed: tuple[Locator, ...] = ()
        ) -> AnswerAttempt:
            res = resolve(question.target.surface)
            if res.ambiguous:
                return AnswerAttempt(
                    qid=question.qid,
                    outcome="abstained",
                    reason="ambiguous_entity",
                    diagnostics=tuple(f"candidate={c}" for c in res.candidates),
                    suppressed=suppressed,
                )
            if res.entity_id is not None:
                read = read_field(res.entity_id, question.relation)
                if read is not None and not _suppressed(read.locator, suppressed):
                    if read.valid_to is not None:
                        return AnswerAttempt(
                            qid=question.qid,
                            outcome="abstained",
                            reason="superseded_only",
                            diagnostics=(f"valid_to={read.valid_to}",),
                            suppressed=suppressed,
                        )
                    return AnswerAttempt(
                        qid=question.qid,
                        outcome="answered",
                        answer=read.value,
                        locators=(read.locator,),
                        reason="authored_field",
                        diagnostics=("memory_hit: derivation not attempted",),
                        suppressed=suppressed,
                    )
            result = derive(
                DerivationRequest(
                    question=question,
                    resolution=res,
                    suppressed=suppressed,
                    policy=pol,
                )
            )
            diagnostics = [f"derived: {result.reason}"] if result.reason else []
            diagnostics.extend(f"budget: {v}" for v in pol.violations(result.budget))
            outcome = result.outcome
            answer_text = result.answer
            if outcome == "answered" and not result.locators:
                outcome = "abstained"
                answer_text = ""
                diagnostics.append("ungrounded answer withheld: no locator cited")
            return AnswerAttempt(
                qid=question.qid,
                outcome=outcome,  # type: ignore[arg-type]
                answer=answer_text,
                locators=tuple(result.locators),
                budget=result.budget,
                reason=result.reason,
                diagnostics=tuple(diagnostics),
                suppressed=suppressed,
            )

        return answer

    return factory


# ───────────────────────────────────────────── deterministic oracle test doubles ────
# These read the question set's own answer key. They exist so the harness can be
# exercised end to end with no model and no vault.
#
# A NUMBER PRODUCED WITH THEM IS NOT A MEASUREMENT. It is the answer key graded
# against itself, and it will look excellent. They are named `oracle_*` so that
# their appearance in a report is obvious, and `admission_verdict` additionally
# refuses any question set labelled `synthetic_fixture`.


def oracle_resolver(question_set: QuestionSet) -> Resolver:
    """Resolve a surface exactly as the set says it should resolve."""
    by_surface: dict[str, Question] = {q.target.surface: q for q in question_set.questions}

    def resolve(surface: str) -> Resolution:
        q = by_surface.get(surface)
        if q is None or q.target.entity_id is None:
            if q is not None and q.abstain_reason == "ambiguous_entity":
                return Resolution(candidates=("candidate_a", "candidate_b"))
            return Resolution()
        return Resolution(entity_id=q.target.entity_id, entity_type=q.target.entity_type)

    return resolve


def oracle_field_reader(question_set: QuestionSet) -> FieldReader:
    """Serve the authored field for the questions a single node read can answer.

    Faithful to what node-first can and cannot reach: a single-hop question's
    expected value is on the resolved entity's own note, a multi-hop question's
    is not, and a ``superseded_only`` question yields a read with its validity
    interval closed."""
    single: dict[tuple[str, str], FieldRead] = {}
    for q in question_set.questions:
        if q.target.entity_id is None:
            continue
        key = (q.target.entity_id, q.relation)
        if q.abstain:
            if q.abstain_reason == "superseded_only":
                single[key] = FieldRead(
                    value="a former holder of the role",
                    locator=Locator(note_id=f"{q.target.entity_id}.md", field=q.relation),
                    valid_to="closed",
                )
            continue
        if q.multi_hop or q.expected is None:
            continue
        single[key] = FieldRead(value=q.expected.answer, locator=q.expected.locator)

    def read(entity_id: str, relation: str) -> FieldRead | None:
        return single.get((entity_id, relation))

    return read


def oracle_derivation(
    question_set: QuestionSet,
    *,
    refutations: int = 1,
) -> DerivationPort:
    """Derive the expected answer with its full hop chain, or abstain.

    Honours ``suppressed``: with a bridge hop withheld the derivation abstains,
    which is what makes the shortcut control show connected reasoning rather than
    a lucky prior. Spends one relation-naming call, one claim-read per required
    hop, and a bounded refutation."""

    def derive(request: DerivationRequest) -> DerivationResult:
        q = request.question
        budget = ModelBudget(
            relation_naming=1,
            claim_reads=len(q.required_hops) or 1,
            refutations=refutations,
        )
        if q.abstain or q.expected is None:
            return DerivationResult(
                outcome="abstained", budget=budget, reason=q.abstain_reason or "no_claim"
            )
        chain = tuple(h.locator for h in q.required_hops) or (q.expected.locator,)
        if any(_suppressed(loc, request.suppressed) for loc in chain):
            return DerivationResult(
                outcome="abstained", budget=budget, reason="bridge_hop_suppressed"
            )
        return DerivationResult(
            outcome="answered",
            answer=q.expected.answer,
            locators=chain,
            budget=budget,
            reason="derived_from_chain",
        )

    return derive


# ──────────────────────────────────────────────────────────────── the orderings ────


def order_questions(questions: Sequence[Question], ordering: str) -> tuple[Question, ...]:
    """Deterministically order a question set.

    ``as_given`` | ``reversed`` | ``shuffle:<token>``. The token seeds a local
    ``random.Random``, so a named ordering is reproducible run to run and machine
    to machine — the ordering control is worthless if the orderings themselves
    move between runs."""
    if ordering == "as_given":
        return tuple(questions)
    if ordering == "reversed":
        return tuple(reversed(questions))
    if ordering.startswith("shuffle:"):
        out = list(questions)
        random.Random(ordering.split(":", 1)[1]).shuffle(out)
        return tuple(out)
    raise ValueError(
        f"unknown ordering {ordering!r}; expected as_given, reversed or shuffle:<token>"
    )


# ─────────────────────────────────────────────────────────────────── the runner ────


@dataclass(frozen=True)
class ArmRun:
    """One arm, one ordering, one run. ``unavailable`` set ⇒ nothing was scored."""

    arm: str
    ordering: str
    run: int
    metrics: ArmMetrics | None = None
    unavailable: str | None = None


@dataclass(frozen=True)
class ArmAggregate:
    """One arm under one ordering, over n runs: mean and spread per metric."""

    arm: str
    ordering: str
    n_runs: int
    summaries: Mapping[str, MetricSummary]
    unavailable: str | None = None

    def summary(self, metric: str) -> MetricSummary | None:
        return self.summaries.get(metric)


def run_arm(
    arm: str,
    factory: ArmFactory,
    question_set: QuestionSet,
    ordering: str,
    *,
    run: int = 0,
    ablate: bool = True,
    policy: BudgetPolicy | None = None,
) -> ArmRun:
    """One pass, plus the bridge-ablated re-ask the shortcut control needs.

    The ablation pass builds a SECOND arm from the factory: re-asking on the same
    instance would let the first pass's state answer the ablated question, which
    would defeat the control it exists to provide."""
    try:
        fn = factory()
    except ArmUnavailable as e:
        return ArmRun(arm=arm, ordering=ordering, run=run, unavailable=str(e))
    ordered = order_questions(question_set.questions, ordering)
    attempts: dict[str, AnswerAttempt] = {}
    try:
        for q in ordered:
            attempts[q.qid] = fn(q)
        ablated: dict[str, AnswerAttempt] = {}
        if ablate:
            fresh = factory()
            for q in ordered:
                if not q.multi_hop or not q.bridge_hops:
                    continue
                ablated[q.qid] = fresh(
                    q, suppressed=tuple(h.locator for h in q.bridge_hops)
                )
    except ArmUnavailable as e:
        return ArmRun(arm=arm, ordering=ordering, run=run, unavailable=str(e))
    return ArmRun(
        arm=arm,
        ordering=ordering,
        run=run,
        metrics=score_arm(
            arm, question_set, attempts, ablated_attempts=ablated, policy=policy
        ),
    )


def aggregate_runs(arm: str, ordering: str, runs: Sequence[ArmRun]) -> ArmAggregate:
    """Mean + sample spread of every metric over the runs that produced one."""
    unavailable = next((r.unavailable for r in runs if r.unavailable), None)
    scored = [r.metrics for r in runs if r.metrics is not None]
    summaries = {
        name: summarise(name, [metric_value(m, name) for m in scored])
        for name in METRIC_NAMES
    }
    return ArmAggregate(
        arm=arm,
        ordering=ordering,
        n_runs=len(scored),
        summaries=summaries,
        unavailable=unavailable,
    )


@dataclass(frozen=True)
class ABReport:
    """Every arm × ordering × run, plus what the set said about itself."""

    question_set: str
    labelling: str
    is_fixture: bool
    settings: Mapping[str, object]
    runs: tuple[ArmRun, ...]
    aggregates: tuple[ArmAggregate, ...]

    @property
    def arms(self) -> tuple[str, ...]:
        seen: list[str] = []
        for a in self.aggregates:
            if a.arm not in seen:
                seen.append(a.arm)
        return tuple(seen)

    @property
    def orderings(self) -> tuple[str, ...]:
        seen: list[str] = []
        for a in self.aggregates:
            if a.ordering not in seen:
                seen.append(a.ordering)
        return tuple(seen)

    @property
    def unavailable(self) -> Mapping[str, str]:
        return {a.arm: a.unavailable for a in self.aggregates if a.unavailable}

    def aggregate(self, arm: str, ordering: str) -> ArmAggregate | None:
        for a in self.aggregates:
            if a.arm == arm and a.ordering == ordering:
                return a
        return None


def run_ab(
    question_set: QuestionSet,
    arms: Mapping[str, ArmFactory],
    *,
    runs: int = DEFAULT_RUNS,
    orderings: Sequence[str] = DEFAULT_ORDERINGS,
    ablate: bool = True,
    policy: BudgetPolicy | None = None,
) -> ABReport:
    """Run every arm under every ordering ``runs`` times and aggregate."""
    if runs < 1:
        raise ValueError("runs must be >= 1")
    all_runs: list[ArmRun] = []
    aggregates: list[ArmAggregate] = []
    for arm, factory in arms.items():
        for ordering in orderings:
            per_ordering = [
                run_arm(
                    arm,
                    factory,
                    question_set,
                    ordering,
                    run=i,
                    ablate=ablate,
                    policy=policy,
                )
                for i in range(runs)
            ]
            all_runs.extend(per_ordering)
            aggregates.append(aggregate_runs(arm, ordering, per_ordering))
    return ABReport(
        question_set=question_set.question_set,
        labelling=question_set.labelling,
        is_fixture=question_set.is_fixture,
        settings={
            "n_questions": len(question_set.questions),
            "n_answerable": len(question_set.answerable),
            "n_should_abstain": len(question_set.should_abstain),
            "n_multi_hop": len(question_set.multi_hop),
            "runs_per_arm": runs,
            "orderings": list(orderings),
            "ablation": ablate,
            # No threshold is carried in the report: the bar is estimated at
            # admission time, from these runs, by pairing per question.
            "uncertainty": "paired per question at admission time",
        },
        runs=tuple(all_runs),
        aggregates=tuple(aggregates),
    )


# ───────────────────────────────────────────────────────────── the admission rule ────


@dataclass(frozen=True)
class OrderingGain:
    """The candidate's gain over the baseline under one ordering.

    Three separate quantities, kept separate on purpose:

      * ``gain`` — the difference of the two arms' mean metric values;
      * ``baseline_stdev`` / ``candidate_stdev`` — the run-to-run spread of each
        arm, REPORTED because the plan requires repeated runs with their variance
        reported. It is not subtracted from the gain: a spread over three runs is
        not an interval, and pretending it is one was the previous mistake here;
      * ``uncertainty`` — the paired estimate the decision actually uses, over
        per-question differences on this ordering's runs.

    ``clears_uncertainty`` is the uncertainty test alone. ``clears_min_gain`` is
    ``None`` unless the caller supplied an explicit extra floor."""

    ordering: str
    baseline_mean: float
    candidate_mean: float
    baseline_stdev: float
    candidate_stdev: float
    n_runs: int
    gain: float
    n_pairs: int
    uncertainty: PairedUncertainty | None
    clears_uncertainty: bool
    clears_min_gain: bool | None = None


@dataclass(frozen=True)
class AdmissionVerdict:
    """The decision object. ``admitted`` is fail-closed: any reason refuses.

    ``min_gain`` is ``None`` in the default configuration: the only bar is the
    paired uncertainty estimated on this harness. A caller may supply an extra
    absolute floor, and it is recorded here when they do."""

    phase: str
    metric: str
    baseline_arm: str
    candidate_arm: str
    method: str
    confidence: float
    seed: int
    admitted: bool
    per_ordering: tuple[OrderingGain, ...]
    reasons: tuple[str, ...]
    min_gain: float | None = None

    def render(self) -> str:
        bar = (
            f"bar = this harness's paired {self.confidence:.0%} CI "
            f"({self.method}, seed {self.seed})"
        )
        if self.min_gain is not None:
            bar += f" and a caller-supplied floor of {self.min_gain:+.3f}"
        head = (
            f"{self.phase}: {self.candidate_arm} vs {self.baseline_arm} on "
            f"{self.metric}, {bar} → {'ADMITTED' if self.admitted else 'REFUSED'}"
        )
        rows = []
        for g in self.per_ordering:
            ci = g.uncertainty.render() if g.uncertainty else "no paired estimate"
            rows.append(
                f"   {g.ordering:<22} base {g.baseline_mean:+.3f} (run sd "
                f"{g.baseline_stdev:.3f})  cand {g.candidate_mean:+.3f} (run sd "
                f"{g.candidate_stdev:.3f})  gain {g.gain:+.3f}  paired {ci}  "
                f"{'clears' if g.clears_uncertainty else 'INSIDE UNCERTAINTY'}"
            )
        why = [f"   - {r}" for r in self.reasons]
        return "\n".join([head, *rows, *why])


_PHASE_PAIRS = {
    # The rule that must not be negotiable: P11 compares arm 3 with the CHEAP
    # baseline. Comparing it with arm 1 would credit the expensive path with
    # everything node-first already buys.
    "P11": (ARM_DERIVATION, ARM_NODE_FIRST),
    "P2": (ARM_NODE_FIRST, ARM_STATUS_QUO),
}


def _arm_runs(report: ABReport, arm: str, ordering: str) -> list[ArmMetrics]:
    """The scored runs of one arm under one ordering, in run order."""
    return [
        r.metrics
        for r in report.runs
        if r.arm == arm and r.ordering == ordering and r.metrics is not None
    ]


def admission_verdict(
    report: ABReport,
    *,
    phase: str,
    candidate: str | None = None,
    baseline: str | None = None,
    metric: str = PRIMARY_METRIC,
    min_gain: float | None = None,
    method: str = PAIRED_BOOTSTRAP,
    confidence: float = DEFAULT_CONFIDENCE,
    resamples: int = DEFAULT_BOOTSTRAP_RESAMPLES,
    seed: int = DEFAULT_BOOTSTRAP_SEED,
    min_pairs: int = MIN_PAIRED_QUESTIONS,
    min_runs: int = MIN_RUNS,
    min_orderings: int = MIN_ORDERINGS,
    abstention_guard: bool = True,
    budget_guard: bool = True,
) -> AdmissionVerdict:
    """Decide one phase's gate. Fail-closed: any unmet condition refuses.

    ``phase`` fixes which arms may be compared. Passing a baseline other than
    the one the phase names raises, so the encoded rule cannot be relaxed by a
    keyword argument at the call site.

    The gain is compared against a paired uncertainty estimated on THIS report:
    per-question differences between the two arms under the same ordering, and
    a seeded interval on their mean. There is no imported threshold and no
    default absolute floor; ``min_gain`` adds one only if a caller asks for it.

    The two guards read in opposite directions on purpose, and both directions
    point at refusal. A GAIN must be demonstrated — its whole interval above
    zero. A HARM (abstention rising on answerable questions) refuses on weaker
    evidence: a rise larger than one paired standard error is enough, because
    the burden of proof sits with the candidate either way."""
    if phase not in _PHASE_PAIRS:
        raise ValueError(f"unknown phase {phase!r}; expected one of {', '.join(_PHASE_PAIRS)}")
    want_candidate, want_baseline = _PHASE_PAIRS[phase]
    candidate = candidate or want_candidate
    baseline = baseline or want_baseline
    if candidate != want_candidate or baseline != want_baseline:
        raise ValueError(
            f"{phase} compares {want_candidate} against {want_baseline}; refusing to "
            f"score {candidate} against {baseline}"
        )

    reasons: list[str] = []
    if report.is_fixture:
        reasons.append(
            f"question set {report.question_set!r} is labelled "
            f"{report.labelling!r}: it exercises the harness and cannot admit a phase"
        )
    for arm in (baseline, candidate):
        if arm in report.unavailable:
            reasons.append(f"{arm} did not run: {report.unavailable[arm]}")
    orderings = report.orderings
    if len(orderings) < min_orderings:
        reasons.append(
            f"{len(orderings)} ordering(s) run; the gain must hold under at least "
            f"{min_orderings}"
        )

    gains: list[OrderingGain] = []
    for ordering in orderings:
        base = report.aggregate(baseline, ordering)
        cand = report.aggregate(candidate, ordering)
        b = base.summary(metric) if base else None
        c = cand.summary(metric) if cand else None
        if b is None or c is None or not b.measured or not c.measured:
            reasons.append(f"{metric} not measured for both arms under {ordering}")
            continue
        n_runs = min(b.n, c.n)
        if n_runs < min_runs:
            reasons.append(
                f"{ordering}: {n_runs} scored run(s) per arm; {min_runs} required to "
                "report a spread"
            )
        gain = c.mean - b.mean
        base_runs = _arm_runs(report, baseline, ordering)
        cand_runs = _arm_runs(report, candidate, ordering)
        diffs = paired_differences(metric, base_runs, cand_runs)
        unc = (
            paired_uncertainty(
                diffs,
                method=method,
                confidence=confidence,
                resamples=resamples,
                seed=seed,
            )
            if diffs.n
            else None
        )
        enough_pairs = diffs.n >= min_pairs
        clears = bool(unc is not None and enough_pairs and unc.excludes_zero)
        clears_min_gain = None if min_gain is None else gain > min_gain
        gains.append(
            OrderingGain(
                ordering=ordering,
                baseline_mean=b.mean,
                candidate_mean=c.mean,
                baseline_stdev=b.stdev,
                candidate_stdev=c.stdev,
                n_runs=n_runs,
                gain=gain,
                n_pairs=diffs.n,
                uncertainty=unc,
                clears_uncertainty=clears,
                clears_min_gain=clears_min_gain,
            )
        )
        if diffs.unpaired_qids:
            reasons.append(
                f"{ordering}: {len(diffs.unpaired_qids)} question(s) were scored for "
                f"only one arm ({', '.join(diffs.unpaired_qids[:3])}); the paired "
                "estimate cannot cover them"
            )
        if unc is None:
            reasons.append(
                f"{ordering}: no per-question pair for {metric}; nothing to estimate "
                "an uncertainty from"
            )
        elif not enough_pairs:
            reasons.append(
                f"{ordering}: {diffs.n} paired question(s); {min_pairs} required before "
                "a paired estimate says anything a single question could not"
            )
        elif not clears:
            reasons.append(
                f"{ordering}: gain {gain:+.3f} lies inside this harness's paired "
                f"{unc.render()} ({unc.method}), so it is not separated from the "
                "harness's own uncertainty"
            )
        if clears_min_gain is False:
            reasons.append(
                f"{ordering}: gain {gain:+.3f} does not exceed the caller-supplied "
                f"floor of {min_gain:+.3f}"
            )
        if abstention_guard:
            rise_diffs = paired_differences(
                "abstained_on_answerable", base_runs, cand_runs
            )
            if rise_diffs.n:
                rise_unc = paired_uncertainty(
                    rise_diffs,
                    method=method,
                    confidence=confidence,
                    resamples=resamples,
                    seed=seed,
                )
                rise = rise_unc.mean_difference
                if rise > 0.0 and rise > rise_unc.standard_error:
                    reasons.append(
                        f"{ordering}: abstention on answerable questions rose "
                        f"{rise:+.3f} over {baseline}, more than the paired standard "
                        f"error of that rise ({rise_unc.standard_error:.3f})"
                    )
    if budget_guard:
        breaches = sorted(
            {
                v
                for r in report.runs
                if r.arm == candidate and r.metrics is not None
                for v in r.metrics.budget_violations
            }
        )
        if breaches:
            reasons.append(
                f"{candidate} exceeded its per-query model budget "
                f"({'; '.join(breaches[:3])}): the arms are not compared at matched cost"
            )
    if not gains:
        reasons.append("no ordering produced a comparable pair")

    return AdmissionVerdict(
        phase=phase,
        metric=metric,
        baseline_arm=baseline,
        candidate_arm=candidate,
        method=method,
        confidence=confidence,
        seed=seed if method == PAIRED_BOOTSTRAP else 0,
        admitted=not reasons,
        per_ordering=tuple(gains),
        reasons=tuple(reasons),
        min_gain=min_gain,
    )


def p11_verdict(report: ABReport, **kwargs) -> AdmissionVerdict:
    """P11: arm 3 is admitted only if it beats **arm 2** by more than this
    harness's own paired uncertainty."""
    return admission_verdict(report, phase="P11", **kwargs)


@dataclass(frozen=True)
class P2Verdict:
    """P2: is the cheap path enough, and are the expensive phases admitted?

    ``expensive_phases_admitted`` is a THREE-valued answer and ``None`` means
    inconclusive, not "yes". Refusing outright would kill the plan on missing
    data; admitting would spend the effort on an unmeasured bet."""

    comparison: AdmissionVerdict
    node_first_worst_ordering: MetricSummary | None
    target: float | None
    node_first_clears_target: bool | None
    expensive_phases_admitted: bool | None
    reasons: tuple[str, ...]

    def render(self) -> str:
        state = {True: "ADMITTED", False: "NOT ADMITTED", None: "INCONCLUSIVE"}[
            self.expensive_phases_admitted
        ]
        return "\n".join(
            [
                self.comparison.render(),
                f"P2: expensive phases (P4–P12) → {state}",
                *(f"   - {r}" for r in self.reasons),
            ]
        )


def p2_verdict(
    report: ABReport,
    *,
    target: float | None = None,
    metric: str = PRIMARY_METRIC,
    **kwargs,
) -> P2Verdict:
    """P2's gate: measure arm 2 against arm 1, then apply the stop rule.

    ``target`` is the preregistered level at which the cheap path is declared
    sufficient — *"if arm 2 already clears the target, stop"*. It has no default:
    a stop rule invented after the numbers are in is not a stop rule, so an
    absent target makes the verdict inconclusive rather than permissive. The
    level used is the WORST ordering, not the best."""
    comparison = admission_verdict(report, phase="P2", metric=metric, **kwargs)
    summaries = [
        s
        for o in report.orderings
        if (a := report.aggregate(ARM_NODE_FIRST, o)) is not None
        and (s := a.summary(metric)) is not None
        and s.measured
    ]
    worst = min(summaries, key=lambda s: s.mean) if summaries else None

    reasons: list[str] = []
    admitted: bool | None
    clears: bool | None = None
    if ARM_STATUS_QUO in report.unavailable:
        reasons.append(
            f"arm 1 did not run ({report.unavailable[ARM_STATUS_QUO]}); P2 cannot be "
            "settled here — the comparison it requires needs the external baseline"
        )
        admitted = None
    elif worst is None:
        reasons.append(f"{metric} not measured for {ARM_NODE_FIRST}")
        admitted = None
    elif target is None:
        reasons.append(
            "no target supplied; P2's stop rule needs a preregistered level for "
            "'the cheap path suffices'"
        )
        admitted = None
    else:
        clears = worst.mean >= target
        if clears:
            reasons.append(
                f"{ARM_NODE_FIRST} reaches {worst.mean:.3f} ≥ target {target:.3f} under "
                "its worst ordering: the expensive phases are not admitted"
            )
            admitted = False
        else:
            reasons.append(
                f"{ARM_NODE_FIRST} reaches {worst.mean:.3f} < target {target:.3f}: the "
                "cheap path is insufficient on this set"
            )
            admitted = True
    if report.is_fixture:
        reasons.append(
            f"question set is labelled {report.labelling!r}: no phase decision may rest on it"
        )
        admitted = None
    return P2Verdict(
        comparison=comparison,
        node_first_worst_ordering=worst,
        target=target,
        node_first_clears_target=clears,
        expensive_phases_admitted=admitted,
        reasons=tuple(reasons),
    )


# ────────────────────────────────────────────────────────────────────── driver ────


def describe_question_set(question_set: QuestionSet) -> str:
    """The composition of a set, per class — the thing to check before running."""
    reasons: dict[str, int] = {}
    for q in question_set.should_abstain:
        reasons[q.abstain_reason or "?"] = reasons.get(q.abstain_reason or "?", 0) + 1
    traps = sum(1 for q in question_set.questions if q.conflation_traps)
    bridges = sum(1 for q in question_set.questions if q.bridge_hops)
    breakdown = ", ".join(f"{k}={v}" for k, v in sorted(reasons.items()))
    return "\n".join(
        [
            f"question set   {question_set.question_set}  (format {question_set.version})",
            f"labelling      {question_set.labelling}"
            + ("   [fixture: cannot decide a phase]" if question_set.is_fixture else ""),
            f"questions      {len(question_set.questions)}",
            f"  answerable   {len(question_set.answerable)}"
            f"   (multi-hop {len(question_set.multi_hop)}, with a bridge hop {bridges})",
            f"  abstain      {len(question_set.should_abstain)}"
            + (f"   ({breakdown})" if reasons else ""),
            f"  conflation traps on {traps} question(s)",
            f"answer path    {question_set.answer_path or '(unrecorded)'}",
        ]
    )


# The four numbers the derivation A/B is required to report, plus the two
# diagnostics that make the headline readable. Order is the reading order.
REPORTED_METRICS: tuple[tuple[str, str], ...] = (
    ("grounding_rate", "grounded"),
    ("connected_reasoning_rate", "connected"),
    ("abstained_on_deserving", "abst|deserve"),
    ("abstained_on_answerable", "abst|answerable"),
    ("model_calls_per_query", "calls/query"),
    ("conflation_rate", "conflated"),
)


def render_report(report: ABReport) -> str:
    """The per-arm table: every metric the phase must report, with its run spread.

    Cells read ``mean sd<spread>``. Not ``mean ± spread``: a ± in this harness's
    output has already been read once as an interval it was not, and the only
    interval here is the paired one on the verdict, which is asymmetric.

    An arm that did not run gets one NOT RUN line and no numbers, so the table
    cannot be skim-read as though every arm were measured."""
    width = max((len(a.arm) for a in report.aggregates), default=8)
    lines = [
        f"{report.question_set}   labelling={report.labelling}"
        + ("   [FIXTURE: no phase decision may rest on this]" if report.is_fixture else ""),
        "   ".join(f"{k}={v}" for k, v in report.settings.items() if k != "orderings"),
        f"orderings: {', '.join(str(o) for o in report.orderings)}",
        "",
        f"{'arm':<{width}}  {'ordering':<20}{'runs':>5}"
        + "".join(f"{label:>18}" for _, label in REPORTED_METRICS),
    ]
    for a in report.aggregates:
        if a.unavailable:
            lines.append(f"{a.arm:<{width}}  {a.ordering:<20}  NOT RUN — {a.unavailable}")
            continue
        cells = []
        for name, _ in REPORTED_METRICS:
            s = a.summary(name)
            cells.append(
                f"{s.mean:>10.3f} sd{s.stdev:<5.3f}" if s and s.measured else f"{'—':>18}"
            )
        lines.append(f"{a.arm:<{width}}  {a.ordering:<20}{a.n_runs:>5}" + "".join(cells))
    controlled = {
        r.metrics.connected.shortcut_controlled for r in report.runs if r.metrics is not None
    }
    if controlled and not all(controlled):
        lines.append(
            "!! the bridge-ablated re-ask is missing for some multi-hop questions: "
            "'connected' is chain completeness only, not shortcut-controlled"
        )
    return "\n".join(lines)


NO_RESULT_BANNER = (
    "No measurement has been produced by this harness. Arm 1 is external to this "
    "repository, and arms 2 and 3 answer through injected ports that must be "
    "supplied by the caller. A run with the oracle test doubles grades the answer "
    "key against itself and is a harness self-check, not a result."
)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "question_set",
        type=Path,
        nargs="?",
        default=Path(__file__).resolve().parent / "question_set.example.json",
        help="question set to load (default: the example fixture)",
    )
    ap.add_argument(
        "--self-check",
        action="store_true",
        help="run the harness end to end with the ORACLE test doubles and print the "
        "verdict objects. The numbers are tautological by construction.",
    )
    ap.add_argument("--runs", type=int, default=DEFAULT_RUNS)
    ap.add_argument("--target", type=float, default=None, help="P2's preregistered target")
    ap.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_BOOTSTRAP_SEED,
        help="seed for the paired bootstrap, so a verdict replays exactly",
    )
    ap.add_argument(
        "--method",
        choices=PAIRED_METHODS,
        default=PAIRED_BOOTSTRAP,
        help="paired uncertainty estimator (default: %(default)s)",
    )
    ap.add_argument(
        "--min-gain",
        type=float,
        default=None,
        help="OPTIONAL extra absolute floor on the gain, on top of the paired "
        "uncertainty. There is no default: no figure from another experiment is "
        "imported as a threshold here",
    )
    ap.add_argument("--json", type=Path, help="write the report + verdicts here")
    args = ap.parse_args(argv)

    try:
        qset = load_question_set(args.question_set)
    except QuestionSetError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(describe_question_set(qset))
    print()
    print(f"arm 1 {ARM_STATUS_QUO:<20} NOT RUN — external answer path")
    print(f"arm 2 {ARM_NODE_FIRST:<20} runnable, given a resolver + field reader")
    print(f"arm 3 {ARM_DERIVATION:<20} runnable, given a derivation port")
    print()
    print(NO_RESULT_BANNER)
    if not args.self_check:
        return 0

    print("\n--- harness self-check with ORACLE doubles (tautological) ---")
    report = run_ab(
        qset,
        {
            ARM_STATUS_QUO: status_quo_arm(),
            ARM_NODE_FIRST: node_first_arm(oracle_resolver(qset), oracle_field_reader(qset)),
            ARM_DERIVATION: derivation_arm(
                oracle_resolver(qset), oracle_field_reader(qset), oracle_derivation(qset)
            ),
        },
        runs=args.runs,
    )
    stats = {"method": args.method, "seed": args.seed, "min_gain": args.min_gain}
    p2 = p2_verdict(report, target=args.target, **stats)
    p11 = p11_verdict(report, **stats)
    print(render_report(report))
    print()
    print(p2.render())
    print()
    print(p11.render())
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(
                {
                    "self_check": True,
                    "disclaimer": NO_RESULT_BANNER,
                    "report": asdict(report),
                    "p2": asdict(p2),
                    "p11": asdict(p11),
                },
                indent=1,
                default=str,
            ),
            encoding="utf-8",
        )
        print(f"\nwrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
