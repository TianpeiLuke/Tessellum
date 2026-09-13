#!/usr/bin/env python3
"""Metrics for the role/relation answer A/B: GROUNDING rate, CONNECTED-REASONING
rate, ABSTENTION calibration, and the per-query MODEL BUDGET.

Why this exists
---------------
``eval/digestion_pipeline/answer_eval.py`` scores a reader over retrieved notes
and reports entity / polarity accuracy plus refusal rates. That is the right
instrument for the question it asks and the wrong one for this one. A role
question ("which team is accountable for X?") fails in a way accuracy cannot
see: the answer path returns a *name that appears near the entity* — the note's
own author rather than the thing's steward — and scores it as an answer. Three
measures the reader eval does not have are needed before that failure is
visible, and this module is exactly those three plus the cost counter:

  grounding rate            the answer is right AND cited at the locator it was
                            actually read from. A right answer with no locator,
                            or with a locator that points somewhere else, is not
                            a grounded answer, and separating the two is the
                            whole point.
  connected-reasoning rate  for a multi-hop question, every required hop of the
                            chain is cited AND the answer does not survive
                            suppression of the bridge hop. The second clause is
                            the anti-shortcut control: an arm that answers with
                            the bridge removed did not traverse the chain
                            (Trivedi et al.'s disconnected reasoning), and
                            crediting it would measure a lucky prior.
  abstention calibration    both halves, never one: how much of the deserving
                            abstention is taken, and how much abstention lands
                            on answerable questions. Abstention rises before
                            answer quality does on this path, so a single
                            "refusal rate" cannot distinguish a calibrated gate
                            from a regression.
  model budget              one relation-naming + k claim-reads + a BOUNDED
                            refutation per query, counted and checked. A budget
                            that grows with the corpus is the cost the node-first
                            design exists to avoid, so it is measured rather
                            than asserted.

Also here: the question-set data model and loader, because every metric above is
defined against it, and the harness's OWN uncertainty estimator — a paired
difference over questions, because both arms answer the same questions, so the
question is the pairing unit and the (large) between-question spread drops out of
the estimate. The historical build-noise interval from a different experiment is
kept as a reference object with its provenance and is deliberately not the
default threshold of anything; see :data:`HISTORICAL_BUILD_NOISE_INTERVAL`.

What this module is not
-----------------------
It computes no result. It calls no model and reads no vault: an arm hands it
:class:`AnswerAttempt` records and it grades them. No arm and no answer path is
supplied here (see ``arms.py`` and ``README.md`` for which arms can run at all).

Pure stdlib, deliberately. ``jsonschema`` is used for the structural pass when it
is importable and skipped with a warning when it is not, so a malformed question
set is still caught by the hand-written pass below. Importing
``answer_eval.py`` was rejected as the reuse route: it imports the indexer, the
retrieval layer and the LLM bridge at module scope, which would make grading a
JSON file depend on a working model backend. Its two scoring rules that this
module needs are re-stated below, and ``tests/eval/test_query_relation_harness.py``
asserts the two implementations agree so the convention cannot drift silently.
"""
from __future__ import annotations

import json
import random
import re
import statistics
import string
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Mapping, Sequence

# ─────────────────────────── the imported figure, as a reference object only ────


@dataclass(frozen=True)
class MeasuredInterval:
    """An interval somebody measured, kept as an INTERVAL.

    The type exists to make one specific mistake impossible: collapsing a
    measured ``[low, high]`` into a single ``±h`` number and then using that
    number as a significance threshold. An asymmetric interval has no ``±``
    form, so this class has no such attribute and renders as two bounds.

    ``task`` records what was measured. :meth:`transfers_to` is deliberately
    exact-match and deliberately pessimistic: an interval measured on one task
    is evidence about that task, and carrying it to another one is an import,
    not a derivation."""

    low: float
    high: float
    task: str
    provenance: str

    @property
    def symmetric(self) -> bool:
        """True only for an interval that really is ±h about zero."""
        return abs(self.low + self.high) < 1e-12

    @property
    def width(self) -> float:
        return self.high - self.low

    def contains(self, value: float) -> bool:
        return self.low <= value <= self.high

    def transfers_to(self, task: str) -> bool:
        return task == self.task

    def render(self) -> str:
        return f"[{self.low:+.3f}, {self.high:+.3f}]"


# REFERENCE ONLY. This is the pooled interval from the resume/noise experiment,
# and it is not the default threshold of any decision in this package — nothing
# here reads it unless a caller passes a value derived from it explicitly.
#
# What it is: ONE experiment built the same digestion plan TWICE with a
# stochastic writer over a 37-document source, scored both builds with a PROXY
# model, and recorded a model mismatch against the model the plan targets. The
# pooled per-question interval was [-0.047, +0.018].
#
# Why it cannot be a threshold here, in three parts. (1) It is ASYMMETRIC: there
# is no "±0.047", and writing one silently widens the positive side by 2.6x.
# (2) It was measured on a DIFFERENT task — a reader over two freshly built note
# sets, with build-to-build writer sampling as the only varying factor. This
# harness reads a FIXED vault and measures a grounding rate, a
# connected-reasoning rate and an abstention rate, none of which that experiment
# observed. (3) A proxy model with a stated mismatch bounds the noise of that
# proxy on that task, not of this arm on this one.
#
# What it is good for: it motivates REPEATED MEASUREMENT, which is why this
# harness requires n runs per arm and more than one question ordering. For a bar
# to compare a gain against, use `paired_uncertainty` below — estimated on this
# harness, from these arms, over these questions.
HISTORICAL_BUILD_NOISE_INTERVAL = MeasuredInterval(
    low=-0.047,
    high=0.018,
    task="one reader over two stochastically rebuilt note sets (build-noise probe)",
    provenance=(
        "Two stochastic builds of one digestion plan over a 37-document source, "
        "scored with a PROXY model against a stated model mismatch: pooled "
        "per-question interval [-0.047, +0.018] — asymmetric, not a ± figure. "
        "Reference only: it motivates repeated measurement and is NOT a "
        "significance threshold for this harness's fixed-vault lookup, grounding "
        "or connected-reasoning rates, which are a different task."
    ),
)

# ────────────────────────────────────────────────── the model-cost invariant ────

# Per query the model budget is one relation-naming call + k claim-reads + a
# BOUNDED refutation, plus an optional stop check. The caps below make "bounded"
# checkable. The refutation cap is the one that matters: judging incompatibility
# over every pair in the reached set is quadratic in k, so refutation runs only
# against candidate attackers surfaced by retrieval against the derived claim,
# one call per candidate, capped.
RELATION_NAMING_CAP = 1
CLAIM_READ_CAP = 8
REFUTATION_CAP = 3
STOP_CHECK_CAP = 1


@dataclass(frozen=True)
class ModelBudget:
    """Model calls one arm spent on one query, by role.

    Counted rather than timed: a call is the unit that scales with corpus size
    if the design is wrong, and it is comparable across backends."""

    relation_naming: int = 0
    claim_reads: int = 0
    refutations: int = 0
    stop_checks: int = 0

    @property
    def total(self) -> int:
        return self.relation_naming + self.claim_reads + self.refutations + self.stop_checks

    def plus(
        self,
        *,
        relation_naming: int = 0,
        claim_reads: int = 0,
        refutations: int = 0,
        stop_checks: int = 0,
    ) -> "ModelBudget":
        """A new budget with the given calls added (frozen: never mutated)."""
        return ModelBudget(
            relation_naming=self.relation_naming + relation_naming,
            claim_reads=self.claim_reads + claim_reads,
            refutations=self.refutations + refutations,
            stop_checks=self.stop_checks + stop_checks,
        )


@dataclass(frozen=True)
class BudgetPolicy:
    """The per-query caps an arm must respect for its numbers to be comparable.

    An arm that exceeds a cap has not beaten another arm at matched cost, so a
    violation is reported and the admission rule in ``arms.py`` refuses on it
    rather than averaging it away."""

    max_relation_naming: int = RELATION_NAMING_CAP
    max_claim_reads: int = CLAIM_READ_CAP
    max_refutations: int = REFUTATION_CAP
    max_stop_checks: int = STOP_CHECK_CAP

    def violations(self, budget: ModelBudget) -> tuple[str, ...]:
        """Human-readable cap breaches, empty when the budget is within policy."""
        out: list[str] = []
        for role, cap in (
            ("relation_naming", self.max_relation_naming),
            ("claim_reads", self.max_claim_reads),
            ("refutations", self.max_refutations),
            ("stop_checks", self.max_stop_checks),
        ):
            spent = getattr(budget, role)
            if spent > cap:
                out.append(f"{role}={spent} exceeds cap {cap}")
        return tuple(out)


# ──────────────────────────────────────────────────── the question-set model ────

ABSTAIN_REASONS: tuple[str, ...] = (
    "field_absent",
    "entity_unresolvable",
    "ambiguous_entity",
    "out_of_scope",
    "superseded_only",
)
LABELLINGS: tuple[str, ...] = ("human", "llm_judge", "synthetic_fixture")

# A set labelled this way exercises the harness; it must never decide a phase.
FIXTURE_LABELLING = "synthetic_fixture"


class QuestionSetError(ValueError):
    """Raised on a malformed question set — schema drift or a cross-field defect."""


@dataclass(frozen=True)
class Locator:
    """Where a claim is written down.

    ``note_id`` alone is note-level. A grounded role answer is expected to name
    the component it was read from — a frontmatter field, a line, or a character
    span — because "the right name appears somewhere in this note" is the
    failure mode this eval exists to separate from an answer."""

    note_id: str
    field: str | None = None
    line: int | None = None
    span: tuple[int, int] | None = None

    def satisfies(self, expected: "Locator") -> bool:
        """True iff this citation grounds ``expected``.

        The note must match, and ANY component ``expected`` names must match.
        Any-of rather than all-of: a set may record both a field name and a line
        for the same fact, and an arm that cites one of them has located the
        same span. When ``expected`` names no component, the note-level match is
        all that was asked for."""
        if self.note_id != expected.note_id:
            return False
        named = [k for k in ("field", "line", "span") if getattr(expected, k) is not None]
        if not named:
            return True
        return any(getattr(self, k) == getattr(expected, k) for k in named)


@dataclass(frozen=True)
class ExpectedAnswer:
    """The grounded answer and where it is written — both halves, always."""

    answer: str
    locator: Locator
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class Hop:
    """One step of the evidence chain. ``bridge`` marks the load-bearing step."""

    locator: Locator
    required: bool = True
    bridge: bool = False
    note: str = ""


@dataclass(frozen=True)
class ConflationTrap:
    """A value stated about the same entity under a DIFFERENT relation.

    Answering with one is the specific failure the role-question class exists to
    measure (the note's author is not the thing's steward), so it is graded apart
    from a plain wrong answer."""

    relation: str
    value: str
    locator: Locator | None = None


@dataclass(frozen=True)
class Target:
    """The entity the question is about. ``entity_id`` is None on purpose when no
    entity is the right answer (an unresolvable or ambiguous surface)."""

    surface: str
    entity_id: str | None = None
    entity_type: str | None = None


@dataclass(frozen=True)
class Question:
    qid: str
    question: str
    relation: str
    target: Target
    abstain: bool
    abstain_reason: str | None = None
    expected: ExpectedAnswer | None = None
    hops: tuple[Hop, ...] = ()
    conflation_traps: tuple[ConflationTrap, ...] = ()
    note: str = ""

    @property
    def required_hops(self) -> tuple[Hop, ...]:
        return tuple(h for h in self.hops if h.required)

    @property
    def bridge_hops(self) -> tuple[Hop, ...]:
        return tuple(h for h in self.hops if h.bridge and h.required)

    @property
    def multi_hop(self) -> bool:
        """Answerable and needing two or more required hops.

        The connected-reasoning rate is computed over exactly this subset; a
        one-hop question cannot exhibit connected reasoning or its absence."""
        return not self.abstain and len(self.required_hops) >= 2


@dataclass(frozen=True)
class QuestionSet:
    question_set: str
    labelling: str
    questions: tuple[Question, ...]
    version: str = "1.0"
    description: str = ""
    answer_path: str = ""

    @property
    def is_fixture(self) -> bool:
        """True for an invented set: it may exercise the harness, never decide."""
        return self.labelling == FIXTURE_LABELLING

    @property
    def answerable(self) -> tuple[Question, ...]:
        return tuple(q for q in self.questions if not q.abstain)

    @property
    def should_abstain(self) -> tuple[Question, ...]:
        return tuple(q for q in self.questions if q.abstain)

    @property
    def multi_hop(self) -> tuple[Question, ...]:
        return tuple(q for q in self.questions if q.multi_hop)

    def by_id(self, qid: str) -> Question:
        for q in self.questions:
            if q.qid == qid:
                return q
        raise KeyError(qid)


SCHEMA_PATH = Path(__file__).resolve().parent / "question_set.schema.json"
EXAMPLE_PATH = Path(__file__).resolve().parent / "question_set.example.json"


def _locator(raw: Mapping[str, Any], *, where: str) -> Locator:
    if not isinstance(raw, Mapping) or not raw.get("note_id"):
        raise QuestionSetError(f"{where}: locator needs a note_id")
    span = raw.get("span")
    return Locator(
        note_id=str(raw["note_id"]),
        field=raw.get("field"),
        line=raw.get("line"),
        span=(int(span[0]), int(span[1])) if span else None,
    )


def _validate_structural(data: Mapping[str, Any]) -> None:
    """Stage 1: draft-07 validation, when ``jsonschema`` is importable.

    Mirrors ``composer.loader``'s two-stage shape. Soft-imported so a malformed
    set is still rejected by stage 2 in an environment without the dependency;
    the warning is emitted once so a skipped stage 1 is never silent."""
    try:
        import jsonschema  # type: ignore[import-not-found]
    except ImportError:  # pragma: no cover — optional dependency
        warnings.warn(
            "jsonschema unavailable; question-set structural validation skipped "
            "(cross-field checks still run)",
            stacklevel=3,
        )
        return
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:  # pragma: no cover — message passthrough
        raise QuestionSetError(f"schema: {e.message} at {list(e.absolute_path)}") from e


def parse_question_set(data: Mapping[str, Any], *, structural: bool = True) -> QuestionSet:
    """Two-stage parse: draft-07 structure, then the cross-field rules.

    The cross-field rules are the ones that matter and are stated here rather
    than only in the schema: an abstention question carries no expected answer,
    an answerable question carries one WITH a locator, and a bridge hop is
    required by construction (a bridge that may be skipped is not a bridge, and
    the shortcut control would silently pass)."""
    if structural:
        _validate_structural(data)
    for key in ("version", "question_set", "labelling", "questions"):
        if key not in data:
            raise QuestionSetError(f"missing top-level key {key!r}")
    if data["labelling"] not in LABELLINGS:
        raise QuestionSetError(
            f"labelling {data['labelling']!r} not one of {', '.join(LABELLINGS)}"
        )
    rows = data["questions"]
    if not isinstance(rows, list) or not rows:
        raise QuestionSetError("questions: expected a non-empty list")

    seen: set[str] = set()
    questions: list[Question] = []
    for i, raw in enumerate(rows):
        qid = str(raw.get("qid") or f"q{i + 1:03d}")
        if qid in seen:
            raise QuestionSetError(f"duplicate qid {qid!r}")
        seen.add(qid)
        if not (raw.get("question") or "").strip():
            raise QuestionSetError(f"{qid}: question has no text")
        relation = (raw.get("relation") or "").strip()
        if not relation:
            raise QuestionSetError(f"{qid}: needs a relation")
        target_raw = raw.get("target") or {}
        if not (target_raw.get("surface") or "").strip():
            raise QuestionSetError(f"{qid}: target needs a surface form")
        if "abstain" not in raw or not isinstance(raw["abstain"], bool):
            raise QuestionSetError(f"{qid}: needs an explicit boolean abstain")
        abstain = bool(raw["abstain"])
        reason = raw.get("abstain_reason")
        expected_raw = raw.get("expected")
        if abstain:
            if reason not in ABSTAIN_REASONS:
                raise QuestionSetError(
                    f"{qid}: abstain question needs abstain_reason in "
                    f"{', '.join(ABSTAIN_REASONS)}"
                )
            if expected_raw:
                raise QuestionSetError(f"{qid}: an abstain question carries no expected answer")
            expected = None
        else:
            if reason is not None:
                raise QuestionSetError(f"{qid}: abstain_reason on an answerable question")
            if not isinstance(expected_raw, Mapping):
                raise QuestionSetError(f"{qid}: answerable question needs an expected answer")
            if not (expected_raw.get("answer") or "").strip():
                raise QuestionSetError(f"{qid}: expected.answer is empty")
            expected = ExpectedAnswer(
                answer=str(expected_raw["answer"]).strip(),
                locator=_locator(expected_raw.get("locator") or {}, where=f"{qid}.expected"),
                aliases=tuple(str(a) for a in expected_raw.get("aliases") or ()),
            )
        hops: list[Hop] = []
        for j, h in enumerate(raw.get("hops") or ()):
            required = bool(h.get("required", True))
            bridge = bool(h.get("bridge", False))
            if bridge and not required:
                raise QuestionSetError(
                    f"{qid}: hop {j} is a bridge but not required — the shortcut "
                    "control would pass vacuously"
                )
            hops.append(
                Hop(
                    locator=_locator(h.get("locator") or {}, where=f"{qid}.hops[{j}]"),
                    required=required,
                    bridge=bridge,
                    note=str(h.get("note") or ""),
                )
            )
        traps = tuple(
            ConflationTrap(
                relation=str(t["relation"]),
                value=str(t["value"]),
                locator=_locator(t["locator"], where=f"{qid}.trap") if t.get("locator") else None,
            )
            for t in raw.get("conflation_traps") or ()
        )
        questions.append(
            Question(
                qid=qid,
                question=str(raw["question"]).strip(),
                relation=relation,
                target=Target(
                    surface=str(target_raw["surface"]).strip(),
                    entity_id=target_raw.get("entity_id"),
                    entity_type=target_raw.get("entity_type"),
                ),
                abstain=abstain,
                abstain_reason=reason,
                expected=expected,
                hops=tuple(hops),
                conflation_traps=traps,
                note=str(raw.get("note") or ""),
            )
        )
    return QuestionSet(
        question_set=str(data["question_set"]),
        labelling=str(data["labelling"]),
        questions=tuple(questions),
        version=str(data["version"]),
        description=str(data.get("description") or ""),
        answer_path=str(data.get("answer_path") or ""),
    )


def load_question_set(path: Path | str, *, structural: bool = True) -> QuestionSet:
    """Read and validate a question set from disk."""
    p = Path(path)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise QuestionSetError(f"{p}: {e}") from e
    try:
        return parse_question_set(data, structural=structural)
    except QuestionSetError as e:
        raise QuestionSetError(f"{p}: {e}") from e


# ───────────────────────────────────────────────────────── one arm's answer ────

# warranted -> answer; challenged -> surface the conflict, returning both chains;
# proposed / superseded -> abstain. A surfaced conflict is neither an answer nor
# an abstention and is counted in its own bucket, because folding it into either
# one would hide the outcome the three-way decision was added for.
Outcome = Literal["answered", "conflict", "abstained"]
OUTCOMES: tuple[Outcome, ...] = ("answered", "conflict", "abstained")


@dataclass(frozen=True)
class AnswerAttempt:
    """What one arm returned for one question.

    ``locators`` is the evidence chain the arm cites, in the order it used them.
    ``suppressed`` records what was withheld from the arm on an ablation run, so
    a shortcut measurement cannot be confused with an ordinary attempt."""

    qid: str
    outcome: Outcome
    answer: str = ""
    locators: tuple[Locator, ...] = ()
    budget: ModelBudget = ModelBudget()
    reason: str = ""
    diagnostics: tuple[str, ...] = ()
    suppressed: tuple[Locator, ...] = ()


# ──────────────────────────────────────────────────────────── answer scoring ────
# The two rules below are answer_eval.normalise / answer_eval.tok_contains,
# re-stated here (see the module docstring for why the import was rejected) and
# pinned by an agreement test. Each fixed a real mis-scoring: punctuation
# DELETION collapsed a hyphenated name into one token, and character-substring
# containment found "no" inside "not".


def normalise(s: str) -> str:
    """Lower-case, map punctuation to SPACE, drop articles, collapse whitespace."""
    s = s.lower().strip()
    s = "".join(" " if c in string.punctuation else c for c in s)
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    return " ".join(s.split())


def tok_contains(answer: str, gold: str) -> bool:
    """True iff the normalised gold is a contiguous TOKEN subsequence of ``answer``."""
    g, a = normalise(gold).split(), normalise(answer).split()
    if not g:
        return False
    return any(a[i : i + len(g)] == g for i in range(len(a) - len(g) + 1))


def answer_matches(answer: str, expected: ExpectedAnswer) -> bool:
    """True iff the answer states the expected value or one of its aliases."""
    return any(tok_contains(answer, cand) for cand in (expected.answer, *expected.aliases))


# ──────────────────────────────────────────────────────────────── grading ────


@dataclass(frozen=True)
class Graded:
    """One attempt, graded against one question. Deterministic; no model."""

    qid: str
    should_abstain: bool
    multi_hop: bool
    outcome: Outcome
    answer_correct: bool
    locator_grounded: bool
    grounded: bool
    conflated: bool
    hops_required: int
    hops_cited: int
    hops_complete: bool
    budget: ModelBudget
    budget_violations: tuple[str, ...] = ()
    # carried from the question so a per-question row knows which denominators it
    # belongs to without the question set in hand — the paired estimator needs
    # exactly that, and the trap denominator is a property of the SET, not the arm
    has_conflation_traps: bool = False

    @property
    def answered(self) -> bool:
        return self.outcome == "answered"

    @property
    def abstained(self) -> bool:
        return self.outcome == "abstained"


def grade(
    question: Question,
    attempt: AnswerAttempt,
    *,
    policy: BudgetPolicy | None = None,
) -> Graded:
    """Grade one attempt.

    ``grounded`` requires all three of: the outcome is an answer, the answer is
    correct, and one cited locator satisfies the expected locator. A deserving
    abstention question has no expected answer, so nothing answered on it can be
    grounded — an answer there is scored as ungrounded, never as a near miss.

    ``conflated`` is reserved for an answer that states a trap value and is NOT
    correct: an answer carrying both the right value and a neighbouring one is
    scored as correct rather than as a conflation, so the conflation rate counts
    substitutions and not verbosity."""
    pol = policy or BudgetPolicy()
    answered = attempt.outcome == "answered"
    correct = bool(
        answered
        and question.expected is not None
        and answer_matches(attempt.answer, question.expected)
    )
    located = bool(
        answered
        and question.expected is not None
        and any(loc.satisfies(question.expected.locator) for loc in attempt.locators)
    )
    conflated = bool(
        answered
        and any(
            tok_contains(attempt.answer, t.value)
            for t in question.conflation_traps
        )
        and not correct
    )
    required = question.required_hops
    cited = sum(
        1 for h in required if any(loc.satisfies(h.locator) for loc in attempt.locators)
    )
    return Graded(
        qid=question.qid,
        should_abstain=question.abstain,
        multi_hop=question.multi_hop,
        outcome=attempt.outcome,
        answer_correct=correct,
        locator_grounded=located,
        grounded=bool(correct and located),
        conflated=conflated,
        hops_required=len(required),
        hops_cited=cited,
        hops_complete=bool(required) and cited == len(required),
        budget=attempt.budget,
        budget_violations=pol.violations(attempt.budget),
        has_conflation_traps=bool(question.conflation_traps),
    )


# ─────────────────────────────────────────────────────────────── the metrics ────


def _rate(numerator: int, denominator: int) -> float:
    """A share, or NaN when the denominator is empty.

    NaN rather than 0.0 on purpose: an empty stratum is a missing measurement,
    and reporting it as zero would let an arm look worse (or a gain look real)
    because a question class was absent from the set. Every consumer here drops
    NaN and reports how many it dropped."""
    return numerator / denominator if denominator else float("nan")


@dataclass(frozen=True)
class AbstentionCalibration:
    """Both halves of abstention, never pooled into one refusal rate."""

    n_should_abstain: int
    n_answerable: int
    n_abstentions: int
    # share of the deserving questions the arm actually abstained on
    abstained_on_deserving: float
    # share of ANSWERABLE questions it withheld — the unjustified-rise number
    abstained_on_answerable: float
    # of every abstention it took, how much landed where it belonged
    precision: float
    n_wasted: int
    # deserving-rate minus answerable-rate: 1.0 is perfect, 0.0 is uninformative
    calibration_gap: float
    # a surfaced conflict on a question that deserved abstention is neither
    # credited nor silently lost
    n_conflict_on_deserving: int


def abstention_calibration(graded: Sequence[Graded]) -> AbstentionCalibration:
    deserving = [g for g in graded if g.should_abstain]
    answerable = [g for g in graded if not g.should_abstain]
    took_deserving = sum(1 for g in deserving if g.abstained)
    took_answerable = sum(1 for g in answerable if g.abstained)
    total = took_deserving + took_answerable
    on_deserving = _rate(took_deserving, len(deserving))
    on_answerable = _rate(took_answerable, len(answerable))
    gap = (
        on_deserving - on_answerable
        if on_deserving == on_deserving and on_answerable == on_answerable
        else float("nan")
    )
    return AbstentionCalibration(
        n_should_abstain=len(deserving),
        n_answerable=len(answerable),
        n_abstentions=total,
        abstained_on_deserving=on_deserving,
        abstained_on_answerable=on_answerable,
        precision=_rate(took_deserving, total),
        n_wasted=took_answerable,
        calibration_gap=gap,
        n_conflict_on_deserving=sum(1 for g in deserving if g.outcome == "conflict"),
    )


@dataclass(frozen=True)
class ConnectedReasoning:
    """The connected-reasoning rate and the control that makes it meaningful."""

    n_multi_hop: int
    n_chain_complete: int
    n_shortcut: int
    n_connected: int
    rate: float
    # False when the bridge-ablated re-ask was not supplied for every multi-hop
    # question. The rate is then chain-completeness only, and must be read as
    # such: an arm that answers from a prior rather than from the chain is
    # indistinguishable from one that traversed it.
    shortcut_controlled: bool


def connected_reasoning(
    questions: Sequence[Question],
    graded: Mapping[str, Graded],
    *,
    ablated: Mapping[str, Graded] | None = None,
) -> ConnectedReasoning:
    """Rate over multi-hop questions: chain cited AND the bridge load-bearing.

    ``ablated`` holds the grading of a SECOND attempt at each multi-hop question
    made with its bridge hops suppressed. An attempt whose ablated twin is still
    correct is counted as a shortcut and not as connected reasoning — the
    disconnected-reasoning probe, applied per question instead of per dataset."""
    ablated = ablated or {}
    multi = [q for q in questions if q.multi_hop]
    complete = shortcut = connected = 0
    for q in multi:
        g = graded.get(q.qid)
        if g is None:
            continue
        chain_ok = g.grounded and g.hops_complete
        if chain_ok:
            complete += 1
        a = ablated.get(q.qid)
        took_shortcut = bool(a is not None and a.answer_correct)
        if took_shortcut:
            shortcut += 1
        if chain_ok and not took_shortcut:
            connected += 1
    controlled = bool(multi) and all(q.qid in ablated for q in multi)
    return ConnectedReasoning(
        n_multi_hop=len(multi),
        n_chain_complete=complete,
        n_shortcut=shortcut,
        n_connected=connected,
        rate=_rate(connected, len(multi)),
        shortcut_controlled=controlled,
    )


@dataclass(frozen=True)
class ArmMetrics:
    """Everything one arm scored on one pass over one question set."""

    arm: str
    n_questions: int
    n_answerable: int
    n_should_abstain: int
    n_answers_given: int
    n_grounded: int
    # grounded answers over the FIXED answerable set. The denominator is the
    # question set, not the answers the arm chose to give: with answers-given
    # underneath, an arm that abstains on everything except one easy question
    # scores 1.0, which is the opposite of what this measures.
    grounding_rate: float
    # of the answers it did give, how many were grounded — the diagnostic pair
    # to the headline, and the one that moves when a gate is added
    grounded_precision: float
    # answers that were not grounded, over every question: a wrong answer, a
    # right answer with no or a mislocated citation, and any answer to a
    # question that deserved abstention all count here
    ungrounded_answer_rate: float
    conflation_rate: float
    n_conflated: int
    conflict_rate: float
    abstention: AbstentionCalibration
    connected: ConnectedReasoning
    model_calls_per_query: float
    model_calls_max: int
    budget_violations: tuple[str, ...]
    graded: tuple[Graded, ...] = field(default_factory=tuple, repr=False)
    # the bridge-ablated re-ask, graded. Kept per question rather than only folded
    # into `connected` because the paired estimator needs the shortcut control at
    # the question level: without it a per-question connected score would silently
    # degrade to chain completeness.
    ablated_graded: tuple[Graded, ...] = field(default_factory=tuple, repr=False)


def score_arm(
    arm: str,
    question_set: QuestionSet,
    attempts: Mapping[str, AnswerAttempt],
    *,
    ablated_attempts: Mapping[str, AnswerAttempt] | None = None,
    policy: BudgetPolicy | None = None,
) -> ArmMetrics:
    """Grade one arm's pass over ``question_set``.

    A question with no attempt is not scored and not silently counted as a
    failure — a missing attempt is a harness fault and shows up as a smaller
    ``n_questions`` than the set."""
    pol = policy or BudgetPolicy()
    graded: dict[str, Graded] = {}
    for q in question_set.questions:
        a = attempts.get(q.qid)
        if a is not None:
            graded[q.qid] = grade(q, a, policy=pol)
    rows = tuple(graded.values())
    ablated_graded = {
        qid: grade(question_set.by_id(qid), a, policy=pol)
        for qid, a in (ablated_attempts or {}).items()
    }
    answerable = [g for g in rows if not g.should_abstain]
    answers_given = [g for g in rows if g.answered]
    grounded = [g for g in answerable if g.grounded]
    ungrounded = [g for g in answers_given if not g.grounded]
    trapped = [g for g in rows if question_set.by_id(g.qid).conflation_traps]
    budgets = [g.budget for g in rows]
    violations: list[str] = []
    for g in rows:
        violations.extend(f"{g.qid}: {v}" for v in g.budget_violations)
    return ArmMetrics(
        arm=arm,
        n_questions=len(rows),
        n_answerable=len(answerable),
        n_should_abstain=sum(1 for g in rows if g.should_abstain),
        n_answers_given=len(answers_given),
        n_grounded=len(grounded),
        grounding_rate=_rate(len(grounded), len(answerable)),
        grounded_precision=_rate(len(grounded), len(answers_given)),
        ungrounded_answer_rate=_rate(len(ungrounded), len(rows)),
        conflation_rate=_rate(sum(1 for g in trapped if g.conflated), len(trapped)),
        n_conflated=sum(1 for g in rows if g.conflated),
        conflict_rate=_rate(sum(1 for g in rows if g.outcome == "conflict"), len(rows)),
        abstention=abstention_calibration(rows),
        connected=connected_reasoning(
            question_set.questions, graded, ablated=ablated_graded
        ),
        model_calls_per_query=(
            statistics.fmean([b.total for b in budgets]) if budgets else float("nan")
        ),
        model_calls_max=max((b.total for b in budgets), default=0),
        budget_violations=tuple(violations),
        graded=rows,
        ablated_graded=tuple(ablated_graded.values()),
    )


# ─────────────────────────────────────────────── metric access + statistics ────

# The metrics an A/B may be gated on. `grounding_rate` is the primary: it is the
# one both admission gates are written against.
PRIMARY_METRIC = "grounding_rate"
METRIC_NAMES: tuple[str, ...] = (
    "grounding_rate",
    "grounded_precision",
    "ungrounded_answer_rate",
    "conflation_rate",
    "conflict_rate",
    "connected_reasoning_rate",
    "abstained_on_deserving",
    "abstained_on_answerable",
    "abstention_precision",
    "calibration_gap",
    "model_calls_per_query",
)


def metric_value(metrics: ArmMetrics, name: str) -> float:
    """One named scalar off an :class:`ArmMetrics`, including the nested ones."""
    if name == "connected_reasoning_rate":
        return metrics.connected.rate
    if name == "abstention_precision":
        return metrics.abstention.precision
    if name in ("abstained_on_deserving", "abstained_on_answerable", "calibration_gap"):
        return getattr(metrics.abstention, name)
    if name in METRIC_NAMES:
        return getattr(metrics, name)
    raise KeyError(f"unknown metric {name!r}; known: {', '.join(METRIC_NAMES)}")


@dataclass(frozen=True)
class MetricSummary:
    """One metric over n repeated runs: the mean and the spread, both reported.

    ``stdev`` is the SAMPLE standard deviation and is 0.0 for a single run — a
    single run has no measured spread, which is a reason to refuse a gain, not a
    reason to call the spread zero. ``n_missing`` counts runs whose value was NaN
    (an empty stratum), so a mean over two of five runs cannot pass as five."""

    metric: str
    values: tuple[float, ...]
    mean: float
    stdev: float
    n: int
    n_missing: int

    @property
    def measured(self) -> bool:
        return self.n > 0


def summarise(metric: str, values: Sequence[float]) -> MetricSummary:
    """Mean + sample stdev over the runs that produced a value."""
    kept = tuple(v for v in values if v == v)  # drop NaN
    return MetricSummary(
        metric=metric,
        values=kept,
        mean=statistics.fmean(kept) if kept else float("nan"),
        stdev=statistics.stdev(kept) if len(kept) > 1 else 0.0,
        n=len(kept),
        n_missing=len(values) - len(kept),
    )


# ──────────────────────────── paired uncertainty, estimated on THIS harness ────
# The arms answer the SAME questions, so the question is the pairing unit: score
# each question under each arm, take the per-question DIFFERENCE, and estimate the
# uncertainty of the mean of those differences. Pairing is what makes the estimate
# usable at these sizes — the between-question spread (some questions are easy,
# some are unanswerable) is far larger than the between-arm effect and is
# identical for both arms, so it cancels instead of drowning the signal.
#
# Two estimators, both reported, both deterministic:
#   paired_bootstrap        resample the per-question differences with
#                           replacement and take percentiles of the resampled
#                           means. The default. Deterministic because the RNG is
#                           seeded from a passed-in `seed`, which is recorded on
#                           the result — an unseeded estimator could not be
#                           replayed and a replayed run must reproduce its bar.
#   paired_standard_error   mean ± z·(stdev/sqrt(n)) on the differences. Cheap,
#                           seed-independent, and reported alongside so a
#                           bootstrap interval that disagrees with it is visible.
#
# What this is NOT: a claim about the population of all role questions. It is the
# uncertainty of THIS mean difference on THIS question set, which is the quantity
# the admission rule needs and the only one this harness can estimate.

# A paired estimate over a handful of questions cannot separate a gain from one
# question flipping, whatever the interval says. This is a structural minimum on
# the arithmetic, not a power calculation.
MIN_PAIRED_QUESTIONS = 10

PAIRED_BOOTSTRAP = "paired_bootstrap"
PAIRED_STANDARD_ERROR = "paired_standard_error"
PAIRED_METHODS: tuple[str, ...] = (PAIRED_BOOTSTRAP, PAIRED_STANDARD_ERROR)

DEFAULT_CONFIDENCE = 0.95
DEFAULT_BOOTSTRAP_RESAMPLES = 1000
# Any fixed value would do; what matters is that it is fixed, passed in, and
# REPORTED on the result, so a verdict can be recomputed exactly.
DEFAULT_BOOTSTRAP_SEED = 20260912

# Metrics whose denominator is a property of the QUESTION SET, so both arms are
# scored over the same questions and a per-question difference is defined.
PAIRABLE_METRICS: tuple[str, ...] = (
    "grounding_rate",
    "ungrounded_answer_rate",
    "conflation_rate",
    "conflict_rate",
    "connected_reasoning_rate",
    "abstained_on_deserving",
    "abstained_on_answerable",
    "model_calls_per_query",
)

# Metrics whose denominator is chosen by the ARM (or which are not per-question
# quantities at all). Pairing them would compare two different question sets, so
# they are refused rather than silently mispaired.
UNPAIRABLE_METRICS: tuple[str, ...] = (
    "grounded_precision",  # denominator: the answers this arm chose to give
    "abstention_precision",  # denominator: the abstentions this arm chose to take
    "calibration_gap",  # a difference of two strata rates, not a question score
)


class NotPairable(ValueError):
    """Raised for a metric that has no per-question observation to pair."""


def check_pairable(metric: str) -> None:
    """Raise unless ``metric`` has a per-question observation to pair.

    Checked on the metric NAME alone, so an empty run list still rejects a
    metric that could never have been paired — a silent empty result there would
    read as "no difference"."""
    if metric in UNPAIRABLE_METRICS:
        raise NotPairable(
            f"{metric!r} has an arm-chosen denominator, so there is no shared "
            "per-question unit to pair; pair one of: " + ", ".join(PAIRABLE_METRICS)
        )
    if metric not in PAIRABLE_METRICS:
        raise KeyError(f"unknown metric {metric!r}; pairable: {', '.join(PAIRABLE_METRICS)}")


def per_question_scores(metrics: ArmMetrics, metric: str) -> dict[str, float]:
    """One arm's per-question observation of ``metric``, keyed by qid.

    Only the questions in that metric's denominator appear — a grounding-rate
    score is defined on the answerable questions, an ``abstained_on_deserving``
    score on the deserving ones — so the mean of the returned values reproduces
    the aggregate rate exactly, and the keys are directly pairable across arms.

    ``connected_reasoning_rate`` uses the ablated re-ask recorded on the arm; a
    question whose re-ask is missing is scored on chain completeness alone, the
    same caveat ``ConnectedReasoning.shortcut_controlled`` reports."""
    check_pairable(metric)
    ablated = {g.qid: g for g in metrics.ablated_graded}
    out: dict[str, float] = {}
    for g in metrics.graded:
        if metric == "grounding_rate":
            if g.should_abstain:
                continue
            out[g.qid] = float(g.grounded)
        elif metric == "ungrounded_answer_rate":
            out[g.qid] = float(g.answered and not g.grounded)
        elif metric == "conflation_rate":
            if not g.has_conflation_traps:
                continue
            out[g.qid] = float(g.conflated)
        elif metric == "conflict_rate":
            out[g.qid] = float(g.outcome == "conflict")
        elif metric == "connected_reasoning_rate":
            if not g.multi_hop:
                continue
            a = ablated.get(g.qid)
            shortcut = bool(a is not None and a.answer_correct)
            out[g.qid] = float(g.grounded and g.hops_complete and not shortcut)
        elif metric == "abstained_on_deserving":
            if not g.should_abstain:
                continue
            out[g.qid] = float(g.abstained)
        elif metric == "abstained_on_answerable":
            if g.should_abstain:
                continue
            out[g.qid] = float(g.abstained)
        else:  # model_calls_per_query — a count, not a share
            out[g.qid] = float(g.budget.total)
    return out


@dataclass(frozen=True)
class PairedDifferences:
    """Per-question candidate-minus-baseline differences on one metric.

    ``unpaired_qids`` names questions one arm scored and the other did not. They
    are dropped from the estimate and reported, never filled in with a zero: a
    question only one arm attempted is a harness fault, and a zero difference
    would claim the arms tied on it."""

    metric: str
    qids: tuple[str, ...]
    differences: tuple[float, ...]
    baseline_runs: int
    candidate_runs: int
    unpaired_qids: tuple[str, ...] = ()

    @property
    def n(self) -> int:
        return len(self.differences)

    @property
    def mean(self) -> float:
        return statistics.fmean(self.differences) if self.differences else float("nan")


def paired_differences(
    metric: str,
    baseline: Sequence[ArmMetrics],
    candidate: Sequence[ArmMetrics],
) -> PairedDifferences:
    """Pair two arms question by question over their repeated runs.

    Each arm's per-question score is first averaged over ITS runs (so repeated
    measurement reduces the per-question noise it exists to reduce), and the
    difference is then taken per question. Order of the runs is irrelevant and no
    run is paired with a particular run of the other arm — the arms are not
    coupled run-to-run, only question-to-question."""
    check_pairable(metric)

    def per_arm(runs: Sequence[ArmMetrics]) -> dict[str, float]:
        acc: dict[str, list[float]] = {}
        for m in runs:
            for qid, value in per_question_scores(m, metric).items():
                acc.setdefault(qid, []).append(value)
        return {qid: statistics.fmean(values) for qid, values in acc.items()}

    b, c = per_arm(baseline), per_arm(candidate)
    shared = tuple(sorted(set(b) & set(c)))
    return PairedDifferences(
        metric=metric,
        qids=shared,
        differences=tuple(c[q] - b[q] for q in shared),
        baseline_runs=len(baseline),
        candidate_runs=len(candidate),
        unpaired_qids=tuple(sorted(set(b) ^ set(c))),
    )


@dataclass(frozen=True)
class PairedUncertainty:
    """The uncertainty of the mean per-question difference, estimated here.

    ``ci_low``/``ci_high`` bound the MEAN DIFFERENCE, so ``excludes_zero`` is the
    honest reading of "the gain is outside this harness's uncertainty". The
    interval is not assumed symmetric and is never rendered as ±."""

    metric: str
    method: str
    n_pairs: int
    baseline_runs: int
    candidate_runs: int
    mean_difference: float
    stdev_difference: float
    standard_error: float
    ci_low: float
    ci_high: float
    confidence: float = DEFAULT_CONFIDENCE
    resamples: int = 0
    seed: int = 0
    unpaired: int = 0

    @property
    def measured(self) -> bool:
        return self.n_pairs > 0

    @property
    def excludes_zero(self) -> bool:
        """True iff the whole interval sits strictly above zero."""
        return self.measured and self.ci_low > 0.0

    def render(self) -> str:
        return (
            f"{self.confidence:.0%} CI [{self.ci_low:+.3f}, {self.ci_high:+.3f}] "
            f"over {self.n_pairs} paired question(s)"
        )


def _percentile(sorted_values: Sequence[float], q: float) -> float:
    """Nearest-rank percentile of an already-sorted sample."""
    if not sorted_values:
        return float("nan")
    idx = int(round(q * (len(sorted_values) - 1)))
    return sorted_values[min(len(sorted_values) - 1, max(0, idx))]


def paired_uncertainty(
    differences: PairedDifferences,
    *,
    method: str = PAIRED_BOOTSTRAP,
    confidence: float = DEFAULT_CONFIDENCE,
    resamples: int = DEFAULT_BOOTSTRAP_RESAMPLES,
    seed: int = DEFAULT_BOOTSTRAP_SEED,
) -> PairedUncertainty:
    """Estimate the uncertainty of the mean paired difference.

    ``paired_bootstrap`` resamples the differences with replacement using a
    ``random.Random(seed)`` and takes percentiles of the resampled means; the
    same seed and the same differences always give the same interval, which is
    what makes a verdict replayable. ``paired_standard_error`` uses
    mean ± z·stdev/sqrt(n) instead and ignores the seed. The standard error is
    computed and reported either way."""
    if method not in PAIRED_METHODS:
        raise ValueError(f"unknown method {method!r}; expected one of {', '.join(PAIRED_METHODS)}")
    if not 0.0 < confidence < 1.0:
        raise ValueError(f"confidence must be in (0, 1); got {confidence}")
    d = differences.differences
    n = len(d)
    mean = statistics.fmean(d) if n else float("nan")
    stdev = statistics.stdev(d) if n > 1 else 0.0
    se = stdev / (n**0.5) if n else float("nan")
    if not n:
        low = high = float("nan")
    elif method == PAIRED_BOOTSTRAP:
        rng = random.Random(seed)
        means = sorted(statistics.fmean(rng.choices(d, k=n)) for _ in range(max(1, resamples)))
        alpha = 1.0 - confidence
        low = _percentile(means, alpha / 2)
        high = _percentile(means, 1.0 - alpha / 2)
    else:
        z = statistics.NormalDist().inv_cdf(1.0 - (1.0 - confidence) / 2)
        low, high = mean - z * se, mean + z * se
    return PairedUncertainty(
        metric=differences.metric,
        method=method,
        n_pairs=n,
        baseline_runs=differences.baseline_runs,
        candidate_runs=differences.candidate_runs,
        mean_difference=mean,
        stdev_difference=stdev,
        standard_error=se,
        ci_low=low,
        ci_high=high,
        confidence=confidence,
        resamples=resamples if method == PAIRED_BOOTSTRAP else 0,
        seed=seed if method == PAIRED_BOOTSTRAP else 0,
        unpaired=len(differences.unpaired_qids),
    )
