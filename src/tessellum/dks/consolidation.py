"""tessellum.dks.consolidation — gate (ii): the reviewed promotion batch (Tier C).

P12 of the query-time DKS plan, and the only phase whose output eventually
reaches durable authored notes — which is exactly why it is the one phase that
ships **refusing to run**. Two switches have to be thrown by a caller, and
neither has a permissive default:

- :func:`run_consolidation_batch` takes ``enabled`` and it defaults to
  ``False``. The entry condition is a *promotion A/B* — promotion-on vs
  promotion-off, shuffled task order, repeated runs, plus a post-promotion
  regression check on the relationship and multi-hop classes — and that
  measurement **has not been run**. So the caller must also hand over a
  :class:`PromotionABGate` recording the measurement, and
  :data:`UNRUN_PROMOTION_AB` (the shipped value) is refused. The literature the
  design cites is the reason for the belt and braces: consolidation dropped
  utility from 100% to 52.6% by round 10, so "promoting helps" is a hypothesis,
  not a premise.
- Sign-off must be **requested, not assumed**. ``SignOffPolicy`` defaults to
  ``use_agent=True, use_human=False`` and the shipped digestion entry points
  construct ``SignOffPolicy(use_agent=False, use_human=False)`` — a program-gate
  pass is terminal-approved with nobody in the loop. "Never inline, never
  silent" is therefore *not* inherited from that mechanism, so this batch
  refuses a policy whose ``use_human`` is ``False``
  (:func:`require_human_sign_off`).

**Six conditions, all parameterised, all fail-closed** (:class:`ConsolidationPolicy`):

===================== ===========================================================
recurrence            ``>= 3`` occurrences of one ``derivation_id``
independent contexts  ``>= 2``, counted over **episodes** — see the caveat below
reliability           ``η = (n_pass + 1) / (n_trial + 2) >= 0.8``, probationary
                      below, and **no open correction flag**
stability             the answer unchanged across a dwell window of 7–14 days
grounding             a hard entailment gate (NLI-class, injected, fail-closed)
dedup                 prior-art retrieval — embedding pre-filter at top-k ≈ 10,
                      synonymy ``τ ≈ 0.8`` — then **a model decides**
                      append-vs-create
===================== ===========================================================

The arithmetic (counting, ``η``, the dwell span, the cosine pre-filter, the
threshold comparison) is deterministic and stays that way. Three steps are
genuinely judgements about meaning and each is an **injected seam** with a
deterministic reference implementation: :class:`EntailmentJudge`,
:class:`DedupJudge` and :class:`PromotionProseAuthor`. No network call is
hard-coded anywhere in this module.

**The independence term is a recorded weakening, not a solved criterion.** Until
the cross-span fact layer lands a claim has exactly one source span by
construction, so "independent contexts" is read over *episodes that independently
derived the same* ``derivation_id`` rather than over distinct sources. The
promotion criteria are explicit that *the independence term, not the count,
carries the evidential weight, and in a single-author corpus a naive recurrence
counter counts your own habits of description*. Every
:class:`PromotionRecord` carries
:data:`~tessellum.dks.claim_identity.FACT_ID_DEVIATION` so no consumer adopts
the weaker reading silently.

**Promotion is coexistence, not supersession.** What a promoted claim produces is
an *additive* grounded block that competes at read time, scoped to the target
note's **neighbourhood only** — never a rewrite of authored prose. The measured
failure mode being defended against is that rewrites silently strip qualifiers
(dates survived 3% of the time; authority collapsed in 48 of 49 configurations),
so two artifacts are mandatory and both are checked here rather than hoped for:

1. **Qualifiers survive.** :func:`verify_qualifiers_intact` re-reads whatever the
   injected prose author returned and raises :class:`QualifierStrippedError` if a
   scope/authority/date qualifier or a provenance locator did not make it
   through. A stripping author is refused, not tolerated.
2. **A promotion record** — source claim ids, occurrence count, context ids,
   dates, ``η`` and ``base_snapshot_id`` — rides as a first-class effect. It is
   the demotion handle: without it the re-derivation gate has nothing to grab,
   which is why :meth:`PromotionRecord.demotion_handle` is asserted sufficient
   before anything is proposed.

**The kernel never writes.** The output is :class:`CapabilityEffect` proposals
plus a ``promotion_eligibility`` verdict per candidate; the note compiler maps
effects into the substrate's intent graph and the commit tail performs the only
write. :func:`evaluate_candidate` is deliberately callable *without* enabling
promotion — measuring the gate is not promoting — and it emits **no effects**:
effects are assembled only by :func:`run_consolidation_batch`, after every guard
has passed, so calling the evaluator directly cannot reach a renderable
proposal.

Pure (the Dependency Rule): no runtime import, no clock, no disk, no vault
write. ``η`` and the correction flag are read through
:mod:`tessellum.dks.memory_tiers` (the Tier-B tally) rather than re-derived here,
and the reviewed-batch discipline reuses the shipped authority cap
(:class:`~tessellum.dks.autonomy.AuthorityLadder` — ``ACCEPT`` is permanently
capped below ``auto``) and the mover-is-never-the-judge rule that
:func:`~tessellum.dks.elevation.issue_certificate` states for certificates.
"""

from __future__ import annotations

import difflib
import hashlib
import math
from dataclasses import dataclass, replace
from typing import Any, Literal, Mapping, Protocol, Sequence, runtime_checkable

from tessellum.composer.signoff import SignOffPolicy
from tessellum.dks.autonomy import AuthorityLadder, Stage
from tessellum.dks.capability import (
    CapabilityEffect,
    PromotionEligibility,
    validate_effect_kind,
)
from tessellum.dks.claim_identity import FACT_ID_DEVIATION, normalize_span_text
from tessellum.dks.memory_tiers import (
    RELIABILITY_FLOOR,
    RESOLVED_ORIGIN,
    QueryCacheSource,
    ResolvedRelation,
    TrialHistory,
    meets_reliability_gate,
)

# ── the parameters, as named constants ──────────────────────────────────────

PROMOTION_ENABLED_BY_DEFAULT: bool = False
"""Promotion is OFF unless a caller says otherwise, and this is not a tuning
choice: the promotion A/B has not run, so there is no measurement that licenses
a default-on path."""

MIN_RECURRENCE: int = 3
MIN_INDEPENDENT_CONTEXTS: int = 2

DWELL_WINDOW_DAYS_MIN: float = 7.0
DWELL_WINDOW_DAYS_MAX: float = 14.0
"""The stated dwell range. A window is *parameterised inside* it and a value
outside is refused rather than clamped — a bound a caller can drift past is not
a bound."""

DEFAULT_DWELL_DAYS: float = DWELL_WINDOW_DAYS_MIN

DEFAULT_PRIOR_ART_TOP_K: int = 10
DEFAULT_SYNONYMY_TAU: float = 0.8

SECONDS_PER_DAY: float = 86400.0

BUILD_NOISE_FLOOR: float = 0.047
"""The build-noise floor a measured A/B delta must clear to mean anything."""

MIN_AB_RUNS_PER_ARM: int = 2
MIN_AB_ORDERINGS: int = 2
REQUIRED_REGRESSION_CLASSES: frozenset[str] = frozenset({"relationship", "multi_hop"})
"""The post-promotion regression check that catches consolidation-degrades-recall.
Relationship and multi-hop are named because those are the classes the surveyed
failure landed on."""

PROMOTION_STAGE: Stage = "ACCEPT"
"""Promotion is an ``ACCEPT`` act, and ``ACCEPT`` is permanently capped below
``auto`` by the shipped authority ladder — the certificate never self-authorizes."""

SCOPE_NEIGHBOURHOOD: str = "neighbourhood"
"""The only writeback scope this module will propose. A whole-note rewrite is the
qualifier-stripping failure mode with a different name."""

INDEPENDENCE_BASIS_EPISODES: str = "episodes"
INDEPENDENCE_BASIS_FACTS: str = "facts"

ENTAILMENT_CALIBRATION_CAVEAT: str = (
    "The entailment gate is UN-CALIBRATED: the shipped grounding certificate is "
    "fail-closed until a real model has passed the calibration gate on a "
    "labelled corpus, and no such corpus covers query-time relation claims. So "
    "the default judge abstains on everything and an abstention is a REFUSAL, "
    "not a pass. Injecting a judge does not make it trustworthy; the calibration "
    "gate is what would."
)

# ── vocabularies ────────────────────────────────────────────────────────────

PromotionTarget = Literal["note", "registry", "relation"]
"""Where a promotion lands, chosen by what was derived: an authored note's
neighbourhood, the entity registry, or the Tier-A ``relations`` cache."""

PROMOTION_TARGETS: frozenset[str] = frozenset({"note", "registry", "relation"})

PromotionLifecycle = Literal["probationary", "active", "archived"]
"""A promoted claim's standing. ``probationary`` is the pre-active rung — below
the reliability floor, or short of any other condition — and ``archived`` is
where a demoted claim goes, because nothing is ever deleted."""

ConditionName = Literal[
    "recurrence",
    "independence",
    "reliability",
    "stability",
    "grounding",
    "dedup",
    "renderable",
]

CONDITIONS: tuple[ConditionName, ...] = (
    "recurrence",
    "independence",
    "reliability",
    "stability",
    "grounding",
    "dedup",
    "renderable",
)
"""The six criteria, plus ``renderable`` — which is not a seventh criterion but
the integrity consequence of the closed effect vocabulary: a candidate nobody can
render must not be reported as promotable."""

HARD_CONDITIONS: frozenset[str] = frozenset({"grounding", "dedup", "renderable"})
"""Conditions whose failure is a defect rather than a "not yet".

A short recurrence count, one context, a low ``η`` or a young claim can all
become true by waiting, so they report ``needs_validation``. An un-entailed
claim, a duplicate of existing prose and an un-renderable target cannot, so they
report ``ineligible``. An open correction flag joins them: it means *known
wrong*, not *not yet trusted*."""

QualifierKind = Literal["date", "authority", "scope"]
"""The three qualifier classes the measured failure mode strips. Kept closed on
purpose: an open vocabulary would let a caller label anything a qualifier and
dilute the survival check."""

QUALIFIER_KINDS: frozenset[str] = frozenset({"date", "authority", "scope"})

DedupAction = Literal["create", "append"]
"""What the dedup **model** decided. ``append`` is link-before-create: the fact
already has prose, so a new note would be a duplicate."""

# ── refusal reason codes ────────────────────────────────────────────────────

REASON_DERIVED_TOO_FEW_TIMES: str = "recurrence_below_floor"
REASON_TOO_FEW_CONTEXTS: str = "independent_contexts_below_floor"
REASON_ETA_BELOW_FLOOR: str = "reliability_below_floor"
REASON_OPEN_CORRECTION: str = "open_correction_flag"
REASON_INSIDE_DWELL_WINDOW: str = "inside_dwell_window"
REASON_ANSWER_CHANGED: str = "answer_changed_within_window"
REASON_ENTAILMENT_FAILED: str = "entailment_refuted"
REASON_ENTAILMENT_ABSTAINED: str = "entailment_abstained"
REASON_NO_SOURCE_SPAN: str = "no_cited_source_span"
REASON_NEAR_DUPLICATE: str = "near_duplicate_exists"
REASON_NO_EMBEDDING: str = "no_embedding_for_prior_art_prefilter"
REASON_NO_NEIGHBOURHOOD: str = "no_neighbourhood_anchor"
REASON_NO_RELATION_TRIPLE: str = "relation_target_without_subject_predicate_object"
REASON_NO_RENDERER: str = "no_effect_kind_renders_this_target"


# ── errors ──────────────────────────────────────────────────────────────────


class ConsolidationError(RuntimeError):
    """Base for every refusal this module makes. All of them are fail-closed."""


class ConsolidationDisabledError(ConsolidationError):
    """Raised when a batch is run without ``enabled=True`` — the default."""


class PromotionABNotRunError(ConsolidationError):
    """Raised when the promotion A/B has not been measured, or did not clear."""


class HumanGateError(ConsolidationError):
    """Raised when the sign-off policy would decide a promotion without a human."""


class MoverIsJudgeError(ConsolidationError):
    """Raised when the reasoning backend that derived the claims also reviews them.

    The mover is never the judge — the rule
    :func:`~tessellum.dks.elevation.issue_certificate` enforces for certificates,
    applied to the act it matters most for."""


class AuthorityCapError(ConsolidationError):
    """Raised when the authority ladder forbids an autonomous promotion act."""


class QualifierStrippedError(ConsolidationError):
    """Raised when a promoted rendering dropped a qualifier or a locator."""


# ── content identity ────────────────────────────────────────────────────────


def _content_id(*parts: str | None) -> str:
    """``sha256`` over NUL-joined parts — the log's 64-hex convention."""
    raw = "\0".join("" if part is None else part for part in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ── the A/B entry condition ─────────────────────────────────────────────────


@dataclass(frozen=True)
class PromotionABGate:
    """The measurement that admits promotion at all — stated, not assumed.

    Every field defaults to the un-measured value, so the shipped instance
    (:data:`UNRUN_PROMOTION_AB`) is *not* admitted and a caller has to write down
    what it actually measured. The two shape requirements are the ones the design
    insists on because the surveyed memory-loop gains were frequently curriculum
    artifacts: repeated runs per arm, and at least two shuffled task orderings
    with the gain holding under both."""

    runs_per_arm: int = 0
    orderings: int = 0
    delta: float = 0.0
    noise_floor: float = BUILD_NOISE_FLOOR
    holds_under_every_ordering: bool = False
    regression_checked: tuple[str, ...] = ()
    regression_free: bool = False
    note: str = ""

    @property
    def refusal_reason(self) -> str:
        """Why the gate is not admitted, or ``""`` when it is."""
        if self.runs_per_arm < MIN_AB_RUNS_PER_ARM:
            return (
                f"the promotion A/B needs >= {MIN_AB_RUNS_PER_ARM} runs per arm "
                f"(recorded: {self.runs_per_arm})"
            )
        if self.orderings < MIN_AB_ORDERINGS:
            return (
                f"the promotion A/B needs >= {MIN_AB_ORDERINGS} shuffled task "
                f"orderings (recorded: {self.orderings})"
            )
        if self.delta <= self.noise_floor:
            return (
                f"promotion-on beat promotion-off by {self.delta}, inside the "
                f"noise floor {self.noise_floor}"
            )
        if not self.holds_under_every_ordering:
            return "the gain did not hold under every task ordering"
        missing = sorted(REQUIRED_REGRESSION_CLASSES - set(self.regression_checked))
        if missing:
            return (
                "the post-promotion regression check is missing the classes "
                f"{missing} (consolidation degrades recall exactly there)"
            )
        if not self.regression_free:
            return "the post-promotion regression check found a regression"
        return ""

    @property
    def admitted(self) -> bool:
        return not self.refusal_reason


UNRUN_PROMOTION_AB: PromotionABGate = PromotionABGate(
    note="the promotion A/B has not been run"
)
"""What ships: an un-measured gate. Passing it (or ``None``) refuses the batch."""


# ── the injected seams: entailment, dedup, prose ────────────────────────────


@dataclass(frozen=True)
class EntailmentRequest:
    """One entailment question: does this cited span entail this claim?"""

    derivation_id: str
    claim_text: str
    locator: str
    span_text: str


@dataclass(frozen=True)
class EntailmentVerdict:
    """A judge's answer. ``abstained`` is a REFUSAL, never a pass.

    Keeping abstention distinct from refutation is what lets the un-calibrated
    default be honest: it does not claim the claim is false, it declines to say —
    and a gate that treats declining as passing is the whole failure this
    fail-closed reading avoids."""

    entailed: bool
    score: float = 0.0
    abstained: bool = False
    detail: str = ""
    judge_id: str = ""


@runtime_checkable
class EntailmentJudge(Protocol):
    """The NLI-class seam. A model produces the evidence; the gate decides.

    Injected rather than bundled for the reason the shipped certificate machinery
    already states: the entailment model is a dependency, and the *decision* over
    its outputs stays a pure function so a verdict is replayable."""

    def entails(self, request: EntailmentRequest) -> EntailmentVerdict: ...


@dataclass(frozen=True)
class UncalibratedEntailmentJudge:
    """The default: abstains on everything, and says why.

    Not a heuristic and not a stub that quietly passes — the deferral made
    callable, so "no calibrated entailment model yet" is a named object in the
    call graph instead of a ``None`` somebody forgets to check. With this judge
    installed nothing is ever promoted, which is the correct behaviour until a
    real model has passed a calibration gate."""

    judge_id: str = "uncalibrated"

    def entails(self, request: EntailmentRequest) -> EntailmentVerdict:
        return EntailmentVerdict(
            entailed=False,
            score=0.0,
            abstained=True,
            detail=ENTAILMENT_CALIBRATION_CAVEAT,
            judge_id=self.judge_id,
        )


@dataclass(frozen=True)
class StaticEntailmentJudge:
    """Deterministic reference judge over explicit span verdicts.

    For tests and for a deployment replaying human labels: ``entailing_spans``
    entail, ``refuted_spans`` do not, and anything else abstains — so the
    fail-closed path is the default here too rather than an afterthought."""

    entailing_spans: frozenset[str] = frozenset()
    refuted_spans: frozenset[str] = frozenset()
    judge_id: str = "static_reference"

    def entails(self, request: EntailmentRequest) -> EntailmentVerdict:
        span = normalize_span_text(request.span_text)
        if span in {normalize_span_text(s) for s in self.entailing_spans}:
            return EntailmentVerdict(
                entailed=True, score=1.0, detail="labelled entailing",
                judge_id=self.judge_id,
            )
        if span in {normalize_span_text(s) for s in self.refuted_spans}:
            return EntailmentVerdict(
                entailed=False, score=0.0, detail="labelled not entailing",
                judge_id=self.judge_id,
            )
        return EntailmentVerdict(
            entailed=False, score=0.0, abstained=True,
            detail="no label for this span; abstaining fail-closed",
            judge_id=self.judge_id,
        )


@dataclass(frozen=True)
class PriorArtEntry:
    """One thing that already says something — a note or an existing claim."""

    entry_id: str
    note_id: str
    text: str
    embedding: tuple[float, ...] = ()


@dataclass(frozen=True)
class PriorArtMatch:
    """A shortlisted prior-art entry and its similarity to the candidate."""

    entry: PriorArtEntry
    similarity: float


@runtime_checkable
class PriorArtIndex(Protocol):
    """The embedding pre-filter — arithmetic, and only a pre-filter.

    It narrows the field to ``top_k`` neighbours; it never decides anything. The
    decision is :class:`DedupJudge`'s, because "is this the same fact stated
    again, or a genuinely new one?" is a judgement about meaning that a cosine
    cannot make."""

    def neighbours(
        self, embedding: Sequence[float], *, k: int
    ) -> Sequence[PriorArtMatch]: ...


def cosine(left: Sequence[float], right: Sequence[float]) -> float:
    """Cosine similarity, ``0.0`` for an empty or zero vector. Pure."""
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    norm_left = math.sqrt(sum(a * a for a in left))
    norm_right = math.sqrt(sum(b * b for b in right))
    if norm_left == 0.0 or norm_right == 0.0:
        return 0.0
    return dot / (norm_left * norm_right)


@dataclass(frozen=True)
class StaticPriorArtIndex:
    """Deterministic reference :class:`PriorArtIndex` over fixed entries.

    Ranks by cosine, ties broken by ``entry_id`` so the shortlist is stable —
    a dedup decision that changed with dictionary order would not be replayable.
    """

    entries: tuple[PriorArtEntry, ...] = ()

    def neighbours(
        self, embedding: Sequence[float], *, k: int
    ) -> Sequence[PriorArtMatch]:
        scored = [
            PriorArtMatch(entry=entry, similarity=cosine(embedding, entry.embedding))
            for entry in self.entries
        ]
        scored.sort(key=lambda m: (-m.similarity, m.entry.entry_id))
        return tuple(scored[: max(0, k)])


@dataclass(frozen=True)
class DedupDecision:
    """Append to prior art, or create anew — and who decided.

    ``decided_by`` is recorded because the plan's own table originally called
    this step arithmetic and it is not: criterion 5 requires a **model** decision
    here, so a verdict that cannot name its decider cannot be audited."""

    action: DedupAction
    prior_art_id: str = ""
    prior_art_note_id: str = ""
    similarity: float = 0.0
    reason: str = ""
    decided_by: str = ""

    @property
    def creates(self) -> bool:
        return self.action == "create"


@dataclass(frozen=True)
class DedupRequest:
    """The candidate and its shortlist, as a dedup judge sees them."""

    derivation_id: str
    claim_text: str
    shortlist: tuple[PriorArtMatch, ...]


@runtime_checkable
class DedupJudge(Protocol):
    """The append-vs-create seam — a model decision, injected."""

    def decide(self, request: DedupRequest) -> DedupDecision: ...


@dataclass(frozen=True)
class LinkBeforeCreateJudge:
    """Deterministic reference judge: any prior art at all means append.

    The conservative reading of link-before-create, and the right *default*
    precisely because it is not the interesting answer: a real model can decide
    that a shortlisted neighbour is a different fact, and this reference cannot.
    It is a baseline for wiring, not a semantic judgement."""

    decided_by: str = "link_before_create_reference"

    def decide(self, request: DedupRequest) -> DedupDecision:
        if not request.shortlist:
            return DedupDecision(
                action="create",
                reason="no prior art above the synonymy threshold",
                decided_by=self.decided_by,
            )
        best = request.shortlist[0]
        return DedupDecision(
            action="append",
            prior_art_id=best.entry.entry_id,
            prior_art_note_id=best.entry.note_id,
            similarity=best.similarity,
            reason="prior art states this already; link before create",
            decided_by=self.decided_by,
        )


@dataclass(frozen=True)
class ProseRequest:
    """What an author is given, and everything it must carry through."""

    derivation_id: str
    claim_text: str
    qualifiers: tuple["Qualifier", ...]
    locators: tuple[str, ...]
    target_note_id: str
    neighbourhood_anchor: str


@runtime_checkable
class PromotionProseAuthor(Protocol):
    """The prose seam. Whatever it returns is CHECKED, never trusted.

    Authoring a promoted note's prose is a model act, so it is injected — but
    the measured failure mode is that a rewrite strips qualifiers, so
    :func:`verify_qualifiers_intact` re-reads the output and a stripping author
    is refused."""

    def author(self, request: ProseRequest) -> str: ...


@dataclass(frozen=True)
class AdditiveProseAuthor:
    """Deterministic reference author — additive, qualifier-preserving.

    Emits the claim, then the qualifiers verbatim, then the provenance locators,
    then a marker naming the derivation and its ``resolved`` origin. It rewrites
    nothing because it is never shown the authored text: coexistence is enforced
    by what the author can see, not only by what it is told."""

    marker: str = "promoted claim"

    def author(self, request: ProseRequest) -> str:
        parts = [request.claim_text.strip()]
        if request.qualifiers:
            parts.append(
                "Qualifiers — "
                + "; ".join(f"{q.kind}: {q.text}" for q in request.qualifiers)
                + "."
            )
        if request.locators:
            parts.append("Grounded in " + "; ".join(request.locators) + ".")
        parts.append(
            f"({self.marker}: {request.derivation_id}; origin={RESOLVED_ORIGIN}; "
            "coexists with the authored text — nothing above was rewritten.)"
        )
        return "\n".join(parts)


# ── the candidate ───────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Qualifier:
    """One scope / authority / date qualifier, with the locator that licenses it.

    ``locator`` is per-qualifier rather than per-claim because that is the thing
    that gets lost: a promoted sentence that keeps "as of March" but drops which
    note said so has kept the *word* and lost the qualifier."""

    kind: QualifierKind
    text: str
    locator: str = ""

    def __post_init__(self) -> None:
        if self.kind not in QUALIFIER_KINDS:
            raise ValueError(f"unknown qualifier kind {self.kind!r}")
        if not self.text.strip():
            raise ValueError("a qualifier needs non-empty text")


@dataclass(frozen=True)
class DerivationOccurrence:
    """One episode's derivation of a claim — the unit recurrence counts.

    ``answer_hash`` is what the stability window compares: the same claim
    derived three times with three different answers is not stable, however often
    it recurred. ``span_text`` is what the entailment gate reads, and it is per
    occurrence because each derivation cites its own span."""

    claim_id: str
    episode_id: str
    at: float
    answer_hash: str = ""
    locator: str = ""
    span_text: str = ""
    fact_id: str = ""

    def __post_init__(self) -> None:
        if not self.claim_id:
            raise ValueError("an occurrence needs a claim_id")
        if not self.episode_id:
            raise ValueError("an occurrence needs an episode_id")
        if self.at < 0:
            raise ValueError(f"an occurrence needs at >= 0, got {self.at}")


@dataclass(frozen=True)
class PromotionCandidate:
    """One claim proposed for promotion, with everything the gate measures.

    The candidate is assembled from the log by a caller; this module never reads
    a store. ``neighbourhood_text`` is the authored text the additive block will
    sit *beside* — supplied so the reviewed diff can be rendered over the
    neighbourhood alone, which is what makes the writeback scope checkable rather
    than declared."""

    derivation_id: str
    claim_text: str
    target: PromotionTarget
    target_note_id: str
    occurrences: tuple[DerivationOccurrence, ...]
    neighbourhood_anchor: str = ""
    neighbourhood_text: str = ""
    qualifiers: tuple[Qualifier, ...] = ()
    embedding: tuple[float, ...] = ()
    base_snapshot_id: str = ""
    bb_role: str = ""
    subject_id: str = ""
    predicate: str = ""
    object_ref: str = ""
    valid_from: str | None = None
    valid_to: str | None = None

    def __post_init__(self) -> None:
        if not self.derivation_id:
            raise ValueError("a candidate needs a derivation_id")
        if not self.claim_text.strip():
            raise ValueError("a candidate needs claim text")
        if self.target not in PROMOTION_TARGETS:
            raise ValueError(f"unknown promotion target {self.target!r}")
        if not self.target_note_id:
            raise ValueError("a candidate needs a target_note_id")
        if not self.occurrences:
            raise ValueError("a candidate needs at least one occurrence")

    @property
    def recurrence(self) -> int:
        """How many times the claim was derived — occurrences, not episodes."""
        return len(self.occurrences)

    @property
    def source_claim_ids(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(o.claim_id for o in self.occurrences))

    @property
    def context_ids(self) -> tuple[str, ...]:
        """The distinct episodes that derived it — the independence term's basis."""
        return tuple(sorted({o.episode_id for o in self.occurrences}))

    @property
    def fact_ids(self) -> tuple[str, ...]:
        return tuple(sorted({o.fact_id for o in self.occurrences if o.fact_id}))

    @property
    def observed_at(self) -> tuple[float, ...]:
        return tuple(sorted(o.at for o in self.occurrences))

    @property
    def dwell_days(self) -> float:
        """Span from first to last derivation, in days."""
        stamps = self.observed_at
        return (stamps[-1] - stamps[0]) / SECONDS_PER_DAY

    @property
    def answer_hashes(self) -> tuple[str, ...]:
        return tuple(sorted({o.answer_hash for o in self.occurrences}))

    @property
    def cited_locators(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(o.locator for o in self.occurrences if o.locator))

    @property
    def cited_spans(self) -> tuple[tuple[str, str], ...]:
        """Distinct ``(locator, span_text)`` pairs the entailment gate reads."""
        return tuple(
            dict.fromkeys((o.locator, o.span_text) for o in self.occurrences)
        )


# ── the policy ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ConsolidationPolicy:
    """Every threshold, as a plain number, validated at construction.

    Parameterised so the fail-closed rule is *checkable* rather than asserted:
    a deployment can tighten any of these without touching code, and a value
    outside the design's stated range is refused rather than clamped."""

    min_recurrence: int = MIN_RECURRENCE
    min_independent_contexts: int = MIN_INDEPENDENT_CONTEXTS
    reliability_floor: float = RELIABILITY_FLOOR
    dwell_days: float = DEFAULT_DWELL_DAYS
    prior_art_top_k: int = DEFAULT_PRIOR_ART_TOP_K
    synonymy_tau: float = DEFAULT_SYNONYMY_TAU
    require_embedding: bool = True
    independence_over: str = INDEPENDENCE_BASIS_EPISODES

    def __post_init__(self) -> None:
        if self.min_recurrence < 1:
            raise ValueError("min_recurrence must be >= 1")
        if self.min_independent_contexts < 1:
            raise ValueError("min_independent_contexts must be >= 1")
        if not 0.0 <= self.reliability_floor <= 1.0:
            raise ValueError("reliability_floor must be in [0, 1]")
        if not DWELL_WINDOW_DAYS_MIN <= self.dwell_days <= DWELL_WINDOW_DAYS_MAX:
            raise ValueError(
                "dwell_days must be inside the stated window "
                f"[{DWELL_WINDOW_DAYS_MIN}, {DWELL_WINDOW_DAYS_MAX}], got "
                f"{self.dwell_days}"
            )
        if self.prior_art_top_k < 1:
            raise ValueError("prior_art_top_k must be >= 1")
        if not 0.0 <= self.synonymy_tau <= 1.0:
            raise ValueError("synonymy_tau must be in [0, 1]")
        if self.independence_over not in {
            INDEPENDENCE_BASIS_EPISODES,
            INDEPENDENCE_BASIS_FACTS,
        }:
            raise ValueError(
                f"unknown independence basis {self.independence_over!r}"
            )


DEFAULT_CONSOLIDATION_POLICY: ConsolidationPolicy = ConsolidationPolicy()
"""Recurrence 3, two contexts, η ≥ 0.8, a 7-day dwell, top-k 10, τ = 0.8."""


# ── the conditions (pure arithmetic over already-collected inputs) ───────────


@dataclass(frozen=True)
class ConditionOutcome:
    """One condition's verdict, with the number behind it.

    ``measured`` / ``threshold`` are reported rather than only the boolean so a
    reviewer can see *how far* a candidate is from the floor — the difference
    between "derived twice" and "derived once" is what tells a batch whether to
    wait or to give up."""

    name: ConditionName
    passed: bool
    measured: float
    threshold: float
    detail: str = ""
    reasons: tuple[str, ...] = ()

    def __bool__(self) -> bool:
        return self.passed


def evaluate_recurrence(
    candidate: PromotionCandidate, policy: ConsolidationPolicy
) -> ConditionOutcome:
    """Occurrence count against the recurrence floor."""
    count = candidate.recurrence
    passed = count >= policy.min_recurrence
    return ConditionOutcome(
        name="recurrence",
        passed=passed,
        measured=float(count),
        threshold=float(policy.min_recurrence),
        detail=f"derived {count} time(s)",
        reasons=() if passed else (REASON_DERIVED_TOO_FEW_TIMES,),
    )


def independence_count(
    candidate: PromotionCandidate, policy: ConsolidationPolicy
) -> int:
    """The independence term, over the basis the policy names.

    Over episodes by default, because the cross-span fact layer is deferred and
    a claim therefore has exactly one source span by construction. Over facts
    only when a resolver has actually assigned them; an absent ``fact_id`` means
    *unresolved*, never "a distinct fact", so unresolved occurrences fall back to
    their episodes rather than being counted as diversity."""
    if policy.independence_over == INDEPENDENCE_BASIS_FACTS and candidate.fact_ids:
        return len(candidate.fact_ids)
    return len(candidate.context_ids)


def evaluate_independence(
    candidate: PromotionCandidate, policy: ConsolidationPolicy
) -> ConditionOutcome:
    """Independent contexts against the floor — see :func:`independence_count`."""
    count = independence_count(candidate, policy)
    passed = count >= policy.min_independent_contexts
    return ConditionOutcome(
        name="independence",
        passed=passed,
        measured=float(count),
        threshold=float(policy.min_independent_contexts),
        detail=(
            f"{count} independent {policy.independence_over}; "
            "WEAKENED CRITERION — " + FACT_ID_DEVIATION
        ),
        reasons=() if passed else (REASON_TOO_FEW_CONTEXTS,),
    )


def evaluate_reliability(
    history: TrialHistory, policy: ConsolidationPolicy
) -> ConditionOutcome:
    """Both halves of the shipped reliability gate: ``η`` and the correction flag.

    Delegates to :func:`~tessellum.dks.memory_tiers.meets_reliability_gate` — the
    tier that owns ``η`` also owns its floor, and re-deriving either here would
    let the two drift. The parts are inspected only to name *which* half failed,
    because they fail differently: a low ``η`` is "not yet trusted" and an open
    flag is "known wrong"."""
    passed = meets_reliability_gate(history, floor=policy.reliability_floor)
    reasons: list[str] = []
    if history.eta < policy.reliability_floor:
        reasons.append(REASON_ETA_BELOW_FLOOR)
    if history.has_open_correction:
        reasons.append(REASON_OPEN_CORRECTION)
    return ConditionOutcome(
        name="reliability",
        passed=passed,
        measured=history.eta,
        threshold=policy.reliability_floor,
        detail=(
            f"eta={history.eta:.4f} over n_pass={history.n_pass}/"
            f"n_trial={history.n_trial}, open corrections="
            f"{len(history.open_corrections)}"
        ),
        reasons=tuple(reasons),
    )


def evaluate_stability(
    candidate: PromotionCandidate, policy: ConsolidationPolicy
) -> ConditionOutcome:
    """The answer unchanged across the dwell window.

    Two ways to fail and both are reported: the claim is still *inside* the
    window (too young to have been stable), or the answer moved within it. A
    single occurrence is inside the window by definition — a span of zero days is
    not stability, it is one observation."""
    span = candidate.dwell_days
    hashes = candidate.answer_hashes
    reasons: list[str] = []
    if span < policy.dwell_days:
        reasons.append(REASON_INSIDE_DWELL_WINDOW)
    if len(hashes) > 1:
        reasons.append(REASON_ANSWER_CHANGED)
    return ConditionOutcome(
        name="stability",
        passed=not reasons,
        measured=span,
        threshold=policy.dwell_days,
        detail=(
            f"dwelled {span:.2f} day(s) with {len(hashes)} distinct answer(s)"
        ),
        reasons=tuple(reasons),
    )


def evaluate_grounding(
    candidate: PromotionCandidate, judge: EntailmentJudge
) -> tuple[ConditionOutcome, tuple[EntailmentVerdict, ...]]:
    """The hard entailment gate over every distinct cited span.

    Every span must entail: a claim derived three times whose third citation does
    not support it is not grounded, and taking the best of three would make the
    gate weaker the more often a claim recurred. An abstention refuses, per
    :data:`ENTAILMENT_CALIBRATION_CAVEAT`; a missing span refuses too, because
    there is nothing to judge."""
    verdicts: list[EntailmentVerdict] = []
    reasons: list[str] = []
    weakest = 1.0
    for locator, span in candidate.cited_spans:
        if not span.strip():
            reasons.append(REASON_NO_SOURCE_SPAN)
            weakest = 0.0
            continue
        verdict = judge.entails(
            EntailmentRequest(
                derivation_id=candidate.derivation_id,
                claim_text=candidate.claim_text,
                locator=locator,
                span_text=span,
            )
        )
        verdicts.append(verdict)
        weakest = min(weakest, verdict.score)
        if verdict.abstained:
            reasons.append(REASON_ENTAILMENT_ABSTAINED)
        elif not verdict.entailed:
            reasons.append(REASON_ENTAILMENT_FAILED)
    if not candidate.cited_spans:
        reasons.append(REASON_NO_SOURCE_SPAN)
        weakest = 0.0
    outcome = ConditionOutcome(
        name="grounding",
        passed=not reasons,
        measured=weakest,
        threshold=1.0,
        detail=(
            f"{len(verdicts)} span(s) judged by "
            f"{verdicts[0].judge_id if verdicts else 'no judge'}"
        ),
        reasons=tuple(dict.fromkeys(reasons)),
    )
    return outcome, tuple(verdicts)


def prior_art_shortlist(
    candidate: PromotionCandidate,
    index: PriorArtIndex,
    policy: ConsolidationPolicy,
) -> tuple[PriorArtMatch, ...]:
    """The embedding pre-filter: top-k neighbours at or above ``τ``. Arithmetic."""
    if not candidate.embedding:
        return ()
    return tuple(
        match
        for match in index.neighbours(candidate.embedding, k=policy.prior_art_top_k)
        if match.similarity >= policy.synonymy_tau
    )


def evaluate_dedup(
    candidate: PromotionCandidate,
    index: PriorArtIndex,
    judge: DedupJudge,
    policy: ConsolidationPolicy,
) -> tuple[ConditionOutcome, DedupDecision, tuple[PriorArtMatch, ...]]:
    """Link-before-create: pre-filter arithmetically, then let a MODEL decide.

    The condition passes only when the decision is ``create``. A ``append``
    decision is not a discard — the fact already has prose and the right move is
    to link to it — but it is not *this* promotion, so the verdict carries the
    prior art's id and the candidate is refused as a create. Appending to
    existing prose is itself a vault write against a different target and must
    face this same gate on that target; it is not smuggled through here.

    With no embedding there is no pre-filter, so under the default policy the
    condition refuses: an un-checkable duplicate is a duplicate as far as a
    fail-closed gate is concerned."""
    if policy.require_embedding and not candidate.embedding:
        return (
            ConditionOutcome(
                name="dedup",
                passed=False,
                measured=0.0,
                threshold=policy.synonymy_tau,
                detail="no embedding, so prior art could not be pre-filtered",
                reasons=(REASON_NO_EMBEDDING,),
            ),
            DedupDecision(
                action="append",
                reason="no embedding; cannot rule out prior art",
                decided_by="fail_closed",
            ),
            (),
        )
    shortlist = prior_art_shortlist(candidate, index, policy)
    decision = judge.decide(
        DedupRequest(
            derivation_id=candidate.derivation_id,
            claim_text=candidate.claim_text,
            shortlist=shortlist,
        )
    )
    passed = decision.creates
    return (
        ConditionOutcome(
            name="dedup",
            passed=passed,
            measured=shortlist[0].similarity if shortlist else 0.0,
            threshold=policy.synonymy_tau,
            detail=(
                f"{len(shortlist)} prior-art match(es) at or above tau; "
                f"{decision.decided_by} decided {decision.action!r}"
            ),
            reasons=() if passed else (REASON_NEAR_DUPLICATE,),
        ),
        decision,
        shortlist,
    )


def evaluate_renderable(candidate: PromotionCandidate) -> ConditionOutcome:
    """Can this target actually be proposed as an effect?

    Not a seventh criterion — the integrity consequence of a closed effect
    vocabulary. A ``note`` promotion needs a neighbourhood anchor, because an
    unscoped writeback is the qualifier-stripping failure with a different name.
    A ``relation`` promotion needs its subject/predicate/object. A ``registry``
    promotion has **no effect kind that renders it**: the vocabulary is closed
    and growing it means a renderer that stores it exists, which is the effect
    contract's decision and not this module's — so a registry candidate is
    refused with :data:`REASON_NO_RENDERER` rather than quietly riding in as
    something else."""
    reasons: list[str] = []
    if candidate.target == "note" and not candidate.neighbourhood_anchor.strip():
        reasons.append(REASON_NO_NEIGHBOURHOOD)
    if candidate.target == "relation" and not (
        candidate.subject_id and candidate.predicate and candidate.object_ref
    ):
        reasons.append(REASON_NO_RELATION_TRIPLE)
    if candidate.target == "registry":
        reasons.append(REASON_NO_RENDERER)
    return ConditionOutcome(
        name="renderable",
        passed=not reasons,
        measured=0.0 if reasons else 1.0,
        threshold=1.0,
        detail=f"target={candidate.target}",
        reasons=tuple(reasons),
    )


# ── qualifier survival ──────────────────────────────────────────────────────


def missing_qualifiers(
    text: str, qualifiers: Sequence[Qualifier]
) -> tuple[Qualifier, ...]:
    """Qualifiers whose text did not survive into ``text``. Normalised compare."""
    haystack = normalize_span_text(text)
    return tuple(
        q for q in qualifiers if normalize_span_text(q.text) not in haystack
    )


def missing_locators(text: str, locators: Sequence[str]) -> tuple[str, ...]:
    """Provenance locators that did not survive into ``text``."""
    haystack = normalize_span_text(text)
    return tuple(
        loc for loc in locators if normalize_span_text(loc) not in haystack
    )


def verify_qualifiers_intact(
    text: str, qualifiers: Sequence[Qualifier], locators: Sequence[str]
) -> None:
    """Refuse a rendering that dropped a qualifier or a provenance locator.

    The decisive measured failure mode: rewrites strip qualifiers (dates survived
    3% of the time; authority collapsed in 48 of 49 configurations). So the
    author's output is re-read rather than trusted, and a stripping author is
    refused with :class:`QualifierStrippedError`."""
    lost_q = missing_qualifiers(text, qualifiers)
    lost_l = missing_locators(text, locators)
    if lost_q or lost_l:
        raise QualifierStrippedError(
            "the promoted rendering dropped "
            f"qualifiers={[f'{q.kind}:{q.text}' for q in lost_q]} "
            f"locators={list(lost_l)}; a promotion that loses its scope, "
            "authority or date qualifiers is the failure this gate exists to "
            "prevent"
        )


# ── the promotion record: the demotion handle ───────────────────────────────


@dataclass(frozen=True)
class DemotionHandle:
    """What a re-derivation gate needs to demote a promoted claim.

    One field per demotion trigger, which is why sufficiency is checkable rather
    than asserted: ``cited_spans`` is what a frozen model is given when the claim
    is suppressed (re-derivation failure), ``source_claim_ids`` +
    ``base_snapshot_id`` are what a status flip is read against (contradiction),
    and ``context_ids`` is what the independence floor is recomputed over."""

    derivation_id: str
    source_claim_ids: tuple[str, ...]
    cited_locators: tuple[str, ...]
    cited_spans: tuple[str, ...]
    context_ids: tuple[str, ...]
    eta: float
    base_snapshot_id: str
    target: PromotionTarget
    target_note_id: str
    promoted_text_hash: str

    @property
    def is_sufficient(self) -> bool:
        """Whether all three triggers have their inputs. Fail-closed on any gap."""
        return bool(
            self.derivation_id
            and self.source_claim_ids
            and self.cited_spans
            and self.context_ids
            and self.base_snapshot_id
            and self.target_note_id
        )


@dataclass(frozen=True)
class PromotionRecord:
    """The promotion's provenance, attached as a first-class effect.

    Without it demotion has nothing to grab, which is why it is assembled before
    any effect is and why :meth:`demotion_handle` is asserted sufficient rather
    than assumed. ``independence_caveat`` travels with every record so the
    weakened independence term cannot be adopted silently downstream."""

    derivation_id: str
    source_claim_ids: tuple[str, ...]
    occurrence_count: int
    context_ids: tuple[str, ...]
    observed_at: tuple[float, ...]
    cited_locators: tuple[str, ...]
    cited_spans: tuple[str, ...]
    eta: float
    n_pass: int
    n_trial: int
    base_snapshot_id: str
    target: PromotionTarget
    target_note_id: str
    neighbourhood_anchor: str
    lifecycle: PromotionLifecycle
    qualifiers: tuple[Qualifier, ...] = ()
    promoted_text_hash: str = ""
    prior_art_considered: tuple[str, ...] = ()
    reviewer_id: str = ""
    reasoning_backend_id: str = ""
    independence_basis: str = INDEPENDENCE_BASIS_EPISODES
    independence_caveat: str = FACT_ID_DEVIATION
    entailment_caveat: str = ENTAILMENT_CALIBRATION_CAVEAT
    origin: str = RESOLVED_ORIGIN

    @property
    def record_id(self) -> str:
        """Content address — a replayed batch proposes the same record."""
        return _content_id(
            self.derivation_id,
            *self.source_claim_ids,
            *self.context_ids,
            self.base_snapshot_id,
            self.promoted_text_hash,
            self.target,
            self.target_note_id,
        )

    def demotion_handle(self) -> DemotionHandle:
        return DemotionHandle(
            derivation_id=self.derivation_id,
            source_claim_ids=self.source_claim_ids,
            cited_locators=self.cited_locators,
            cited_spans=self.cited_spans,
            context_ids=self.context_ids,
            eta=self.eta,
            base_snapshot_id=self.base_snapshot_id,
            target=self.target,
            target_note_id=self.target_note_id,
            promoted_text_hash=self.promoted_text_hash,
        )

    @property
    def sufficient_to_demote(self) -> bool:
        return self.demotion_handle().is_sufficient

    def as_payload(self) -> dict[str, Any]:
        """A JSON-shaped rendering for an effect payload. No behaviour."""
        return {
            "record_id": self.record_id,
            "derivation_id": self.derivation_id,
            "source_claim_ids": list(self.source_claim_ids),
            "occurrence_count": self.occurrence_count,
            "context_ids": list(self.context_ids),
            "observed_at": list(self.observed_at),
            "cited_locators": list(self.cited_locators),
            "cited_spans": list(self.cited_spans),
            "eta": self.eta,
            "n_pass": self.n_pass,
            "n_trial": self.n_trial,
            "base_snapshot_id": self.base_snapshot_id,
            "target": self.target,
            "target_note_id": self.target_note_id,
            "neighbourhood_anchor": self.neighbourhood_anchor,
            "lifecycle": self.lifecycle,
            "qualifiers": [
                {"kind": q.kind, "text": q.text, "locator": q.locator}
                for q in self.qualifiers
            ],
            "promoted_text_hash": self.promoted_text_hash,
            "prior_art_considered": list(self.prior_art_considered),
            "reviewer_id": self.reviewer_id,
            "reasoning_backend_id": self.reasoning_backend_id,
            "independence_basis": self.independence_basis,
            "independence_caveat": self.independence_caveat,
            "entailment_caveat": self.entailment_caveat,
            "origin": self.origin,
        }


# ── the reviewed diff ───────────────────────────────────────────────────────


@dataclass(frozen=True)
class PromotionDiff:
    """The reviewed diff — an addition to a neighbourhood, never a rewrite.

    ``before_text`` is the *neighbourhood* as authored, not the note, so the
    writeback's scope is visible in the artifact itself. ``after_text`` is
    ``before_text`` plus the additive block and nothing else, which is what makes
    :attr:`is_additive` a property of the diff rather than a promise about it:
    a unified diff with a removal line would fail it."""

    target_note_id: str
    neighbourhood_anchor: str
    before_text: str
    added_text: str
    record: PromotionRecord
    scope: str = SCOPE_NEIGHBOURHOOD

    @property
    def after_text(self) -> str:
        if not self.before_text:
            return self.added_text
        return f"{self.before_text}\n\n{self.added_text}"

    def unified(self) -> str:
        """A unified diff over the neighbourhood only — what a reviewer reads."""
        return "\n".join(
            difflib.unified_diff(
                self.before_text.splitlines(),
                self.after_text.splitlines(),
                fromfile=f"{self.target_note_id}#{self.neighbourhood_anchor} (authored)",
                tofile=f"{self.target_note_id}#{self.neighbourhood_anchor} (+promoted)",
                lineterm="",
            )
        )

    @property
    def removed_lines(self) -> tuple[str, ...]:
        """Lines the diff removes. Always empty — coexistence, not supersession."""
        return tuple(
            line
            for line in self.unified().splitlines()
            if line.startswith("-") and not line.startswith("---")
        )

    @property
    def is_additive(self) -> bool:
        return not self.removed_lines


# ── the verdict ─────────────────────────────────────────────────────────────


def lifecycle_for(
    *,
    all_conditions_met: bool,
    eta: float,
    floor: float,
    archived: bool = False,
) -> PromotionLifecycle:
    """probationary → active → archived, computed, never asserted.

    ``active`` needs every condition *and* ``η`` at the floor; below it a claim
    is probationary — recorded, competing at read time only once promoted, and
    never silently trusted. ``archived`` is where demotion puts a claim, since
    retraction is an append and nothing is deleted."""
    if archived:
        return "archived"
    if all_conditions_met and eta >= floor:
        return "active"
    return "probationary"


def _eligibility(
    conditions: Sequence[ConditionOutcome], *, has_open_correction: bool
) -> PromotionEligibility:
    failed = [c for c in conditions if not c.passed]
    if not failed:
        return "eligible"
    if has_open_correction or any(c.name in HARD_CONDITIONS for c in failed):
        return "ineligible"
    return "needs_validation"


@dataclass(frozen=True)
class PromotionVerdict:
    """One candidate's outcome: the gate's verdict, the diff, and the record.

    ``effects`` is empty unless :func:`run_consolidation_batch` assembled them
    after every guard passed — so a caller that evaluates candidates directly
    gets the measurement and nothing renderable, which is the whole point of
    keeping the guards at the batch and the arithmetic here."""

    derivation_id: str
    eligibility: PromotionEligibility
    lifecycle: PromotionLifecycle
    conditions: tuple[ConditionOutcome, ...]
    dedup: DedupDecision
    record: PromotionRecord | None = None
    diff: PromotionDiff | None = None
    effects: tuple[CapabilityEffect, ...] = ()
    entailment: tuple[EntailmentVerdict, ...] = ()

    @property
    def promoted(self) -> bool:
        return self.eligibility == "eligible"

    @property
    def failed_conditions(self) -> tuple[ConditionName, ...]:
        return tuple(c.name for c in self.conditions if not c.passed)

    @property
    def reasons(self) -> tuple[str, ...]:
        return tuple(r for c in self.conditions for r in c.reasons)

    def condition(self, name: ConditionName) -> ConditionOutcome:
        for outcome in self.conditions:
            if outcome.name == name:
                return outcome
        raise KeyError(name)


# ── evaluation (no guard, no effect) ────────────────────────────────────────


def evaluate_candidate(
    candidate: PromotionCandidate,
    *,
    policy: ConsolidationPolicy = DEFAULT_CONSOLIDATION_POLICY,
    history: TrialHistory | None = None,
    entailment: EntailmentJudge | None = None,
    prior_art: PriorArtIndex | None = None,
    dedup: DedupJudge | None = None,
    prose_author: PromotionProseAuthor | None = None,
    reviewer_id: str = "",
    reasoning_backend_id: str = "",
) -> PromotionVerdict:
    """Measure every condition for one candidate. Pure; emits no effects.

    Measuring the gate is not promoting, so this is callable without enabling
    anything — and it deliberately returns ``effects=()``: only
    :func:`run_consolidation_batch`, past the enable / A/B / human-sign-off /
    mover guards, assembles renderable proposals.

    The diff and the record are still built for a candidate that met every
    condition, because a *reviewed* diff is the artifact a human is asked to
    approve and it has to exist before the request is made."""
    judge = entailment if entailment is not None else UncalibratedEntailmentJudge()
    index = prior_art if prior_art is not None else StaticPriorArtIndex()
    dedup_judge = dedup if dedup is not None else LinkBeforeCreateJudge()
    author = prose_author if prose_author is not None else AdditiveProseAuthor()
    trials = history if history is not None else TrialHistory(
        subject_id=candidate.derivation_id, subject_kind="promoted_claim"
    )

    grounding, entail_verdicts = evaluate_grounding(candidate, judge)
    dedup_outcome, dedup_decision, shortlist = evaluate_dedup(
        candidate, index, dedup_judge, policy
    )
    conditions = (
        evaluate_recurrence(candidate, policy),
        evaluate_independence(candidate, policy),
        evaluate_reliability(trials, policy),
        evaluate_stability(candidate, policy),
        grounding,
        dedup_outcome,
        evaluate_renderable(candidate),
    )
    all_met = all(c.passed for c in conditions)
    eligibility = _eligibility(
        conditions, has_open_correction=trials.has_open_correction
    )
    lifecycle = lifecycle_for(
        all_conditions_met=all_met,
        eta=trials.eta,
        floor=policy.reliability_floor,
    )

    record: PromotionRecord | None = None
    diff: PromotionDiff | None = None
    if all_met:
        locators = candidate.cited_locators
        promoted_text = author.author(
            ProseRequest(
                derivation_id=candidate.derivation_id,
                claim_text=candidate.claim_text,
                qualifiers=candidate.qualifiers,
                locators=locators,
                target_note_id=candidate.target_note_id,
                neighbourhood_anchor=candidate.neighbourhood_anchor,
            )
        )
        verify_qualifiers_intact(promoted_text, candidate.qualifiers, locators)
        record = PromotionRecord(
            derivation_id=candidate.derivation_id,
            source_claim_ids=candidate.source_claim_ids,
            occurrence_count=candidate.recurrence,
            context_ids=candidate.context_ids,
            observed_at=candidate.observed_at,
            cited_locators=locators,
            cited_spans=tuple(span for _, span in candidate.cited_spans),
            eta=trials.eta,
            n_pass=trials.n_pass,
            n_trial=trials.n_trial,
            base_snapshot_id=candidate.base_snapshot_id,
            target=candidate.target,
            target_note_id=candidate.target_note_id,
            neighbourhood_anchor=candidate.neighbourhood_anchor,
            lifecycle=lifecycle,
            qualifiers=candidate.qualifiers,
            promoted_text_hash=_content_id(promoted_text),
            prior_art_considered=tuple(m.entry.entry_id for m in shortlist),
            reviewer_id=reviewer_id,
            reasoning_backend_id=reasoning_backend_id,
            independence_basis=policy.independence_over,
        )
        diff = PromotionDiff(
            target_note_id=candidate.target_note_id,
            neighbourhood_anchor=candidate.neighbourhood_anchor,
            before_text=candidate.neighbourhood_text,
            added_text=promoted_text,
            record=record,
        )
    return PromotionVerdict(
        derivation_id=candidate.derivation_id,
        eligibility=eligibility,
        lifecycle=lifecycle,
        conditions=conditions,
        dedup=dedup_decision,
        record=record,
        diff=diff,
        entailment=entail_verdicts,
    )


# ── effects (only past the guards) ──────────────────────────────────────────


def effects_for_promotion(
    candidate: PromotionCandidate,
    record: PromotionRecord,
    diff: PromotionDiff,
) -> tuple[CapabilityEffect, ...]:
    """Render one promotion as PROPOSED effects. Nothing here writes.

    Two effects, always in this order:

    1. the **promotion record**, as a ``claim`` effect — promotion appends the
       derived claim to the log and the record is that append's provenance. It
       rides as ``claim`` because the effect vocabulary is closed and growing it
       means a renderer that stores it exists; a dedicated ``promotion_record``
       kind is a reported follow-up on the effect contract, not something this
       module invents.
    2. the **target**: a ``note`` effect carrying the additive block, its
       neighbourhood anchor and the reviewed diff, or a ``relation`` effect
       carrying a Tier-A row with ``origin='resolved'`` layered on the authored
       seed.

    Every ``kind`` goes through the ingestion-side validator, so a kind nobody
    can render is refused here rather than dropped downstream."""
    record_effect = CapabilityEffect(
        kind=validate_effect_kind("claim"),
        folgezettel=candidate.target_note_id,
        bb_role="promotion_record",
        payload={
            "promotion_record": record.as_payload(),
            "record_id": record.record_id,
            "derivation_id": candidate.derivation_id,
            "text": diff.added_text,
            "provenance": "constructed",
            "origin": RESOLVED_ORIGIN,
            "demotion_handle_sufficient": record.sufficient_to_demote,
        },
    )
    if candidate.target == "relation":
        relation = ResolvedRelation(
            subject_id=candidate.subject_id,
            predicate=candidate.predicate,
            object_ref=candidate.object_ref,
            evidence_note=candidate.target_note_id,
            evidence_locator=record.cited_locators[0] if record.cited_locators else "",
            valid_from=candidate.valid_from,
            valid_to=candidate.valid_to,
        )
        target_effect = CapabilityEffect(
            kind=validate_effect_kind("relation"),
            folgezettel=candidate.target_note_id,
            bb_role=candidate.bb_role,
            payload={
                "relation_id": relation.relation_id,
                "subject_id": relation.subject_id,
                "predicate": relation.predicate,
                "object_ref": relation.object_ref,
                "object_kind": relation.object_kind,
                "evidence_note": relation.evidence_note,
                "evidence_locator": relation.evidence_locator,
                "valid_from": relation.valid_from,
                "valid_to": relation.valid_to,
                # The status a claim holds is computed from the edge set, never
                # asserted by the thing proposing the row.
                "epistemic_status": relation.epistemic_status,
                "origin": relation.origin,
                "record_id": record.record_id,
            },
        )
    else:
        target_effect = CapabilityEffect(
            kind=validate_effect_kind("note"),
            folgezettel=candidate.target_note_id,
            bb_role=candidate.bb_role,
            payload={
                "target_note_id": candidate.target_note_id,
                "neighbourhood_anchor": candidate.neighbourhood_anchor,
                "scope": SCOPE_NEIGHBOURHOOD,
                "added_text": diff.added_text,
                "unified_diff": diff.unified(),
                # Coexistence, not supersession: no authored line is rewritten,
                # and the empty tuple is the machine-readable form of that.
                "rewrites": [],
                "coexists": True,
                "record_id": record.record_id,
            },
        )
    return (record_effect, target_effect)


# ── the guards ──────────────────────────────────────────────────────────────


def require_promotion_enabled(
    *, enabled: bool, ab_gate: PromotionABGate | None
) -> PromotionABGate:
    """Refuse unless a caller enabled promotion AND recorded an admitting A/B."""
    if not enabled:
        raise ConsolidationDisabledError(
            "consolidation is DEFAULT-OFF: pass enabled=True explicitly. The "
            "entry condition is a promotion A/B (promotion-on vs promotion-off, "
            "shuffled task order, repeated runs, plus a post-promotion "
            "regression check on the relationship and multi-hop classes) and it "
            "has not been run"
        )
    gate = ab_gate if ab_gate is not None else UNRUN_PROMOTION_AB
    if not gate.admitted:
        raise PromotionABNotRunError(
            f"promotion is not admitted: {gate.refusal_reason}"
        )
    return gate


def require_human_sign_off(policy: SignOffPolicy) -> None:
    """Refuse a policy that would decide a promotion without a human.

    The human gate has to be *requested*: sign-off defaults to agent-only, and
    the shipped digestion entry points disable both the agent and the human
    rungs, so a program-gate pass is terminal-approved with nobody in the loop.
    "Never inline, never silent" is therefore not inherited — it is this
    refusal."""
    if not policy.use_human:
        raise HumanGateError(
            "consolidation must run with SignOffPolicy(use_human=True): "
            "sign-off defaults to agent-only (use_agent=True, use_human=False), "
            "so under the default policy a promotion would be approved with no "
            "human in the loop and 'human-gated' would be false"
        )


def require_independent_reviewer(
    *, reviewer_id: str, reasoning_backend_id: str
) -> None:
    """The mover is never the judge — normalised on both principals.

    Both ids are stripped and case-folded before comparison for the same reason
    the certificate issuer is: an id differing only by whitespace or case would
    otherwise let the backend that derived the claims sign off on promoting
    them."""
    reviewer = (reviewer_id or "").strip().casefold()
    backend = (reasoning_backend_id or "").strip().casefold()
    if not reviewer:
        raise MoverIsJudgeError(
            "a reviewed batch needs a reviewer_id; an unnamed reviewer cannot "
            "be shown to be independent of the reasoning backend"
        )
    if reviewer == backend:
        raise MoverIsJudgeError(
            "the reasoning backend that derived these claims may not review "
            "their promotion (the mover is never the judge)"
        )


def require_authority(ladder: AuthorityLadder | None) -> str:
    """Read the promotion act's authority rung, refusing a kill-switched ladder.

    Promotion is an ``ACCEPT`` act, and the shipped ladder caps ``ACCEPT``
    permanently below ``auto`` — so this returns a rung that can never be full
    ``auto``, which is the invariant the human gate rests on rather than a
    second copy of it."""
    if ladder is None:
        return "suggest"
    if ladder.kill_switched:
        raise AuthorityCapError(
            "the authority ladder is kill-switched; no promotion act may run"
        )
    rung = ladder.rung_for(PROMOTION_STAGE)
    if rung == "auto":  # pragma: no cover - the ladder's own invariant forbids it
        raise AuthorityCapError(
            f"stage {PROMOTION_STAGE!r} reported full 'auto'; it is permanently "
            "capped below it (the certificate never self-authorizes)"
        )
    return rung


# ── the batch ───────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class HumanReviewRequest:
    """The ask, not the answer: what a human is being handed and why.

    ``required`` is always ``True`` — a consolidation batch has no rung below the
    human one. The caller feeds this to the shipped approver ladder with
    ``SignOffPolicy(use_human=True)``; this module never decides that the review
    happened."""

    diff_count: int
    blast_radius: int
    authority_rung: str
    reviewer_id: str
    required: bool = True
    reason: str = (
        "promotion writes to durable authored notes; the human rung is the only "
        "terminal rung for this batch"
    )


@dataclass(frozen=True)
class ConsolidationBatch:
    """One reviewed batch: verdicts, diffs and proposed effects — no writes."""

    verdicts: tuple[PromotionVerdict, ...]
    policy: ConsolidationPolicy
    review: HumanReviewRequest
    ab_gate: PromotionABGate
    independence_basis: str = INDEPENDENCE_BASIS_EPISODES
    independence_caveat: str = FACT_ID_DEVIATION

    @property
    def promoted(self) -> tuple[PromotionVerdict, ...]:
        return tuple(v for v in self.verdicts if v.promoted)

    @property
    def deferred(self) -> tuple[PromotionVerdict, ...]:
        return tuple(v for v in self.verdicts if v.eligibility == "needs_validation")

    @property
    def refused(self) -> tuple[PromotionVerdict, ...]:
        return tuple(v for v in self.verdicts if v.eligibility == "ineligible")

    @property
    def diffs(self) -> tuple[PromotionDiff, ...]:
        return tuple(v.diff for v in self.promoted if v.diff is not None)

    @property
    def records(self) -> tuple[PromotionRecord, ...]:
        return tuple(v.record for v in self.promoted if v.record is not None)

    @property
    def effects(self) -> tuple[CapabilityEffect, ...]:
        return tuple(e for v in self.verdicts for e in v.effects)


def run_consolidation_batch(
    candidates: Sequence[PromotionCandidate],
    *,
    sign_off_policy: SignOffPolicy,
    reviewer_id: str,
    enabled: bool = PROMOTION_ENABLED_BY_DEFAULT,
    ab_gate: PromotionABGate | None = None,
    policy: ConsolidationPolicy = DEFAULT_CONSOLIDATION_POLICY,
    history_source: QueryCacheSource | None = None,
    histories: Mapping[str, TrialHistory] | None = None,
    entailment: EntailmentJudge | None = None,
    prior_art: PriorArtIndex | None = None,
    dedup: DedupJudge | None = None,
    prose_author: PromotionProseAuthor | None = None,
    authority: AuthorityLadder | None = None,
    reasoning_backend_id: str = "",
) -> ConsolidationBatch:
    """The periodic reviewed batch. Refuses by default, four times over.

    Guards, in order and all fail-closed: promotion must be explicitly
    ``enabled`` **and** carry an admitting :class:`PromotionABGate`; the sign-off
    policy must request the human rung; the reviewer must be independent of the
    reasoning backend; and a kill-switched authority ladder stops everything.
    Only past all four are effects assembled — a refused guard raises, it does
    not return a batch with a warning in it.

    ``η`` comes from the Tier-B tally: either an explicit ``histories`` mapping
    or a :class:`~tessellum.dks.memory_tiers.QueryCacheSource` read by
    ``derivation_id`` with ``subject_kind='promoted_claim'`` (a revision
    preserves its ``derivation_id``, so a revised claim inherits its own trial
    history instead of restarting at the fail-closed prior). With neither, every
    candidate scores the no-history ``η`` of 0.5 and stays probationary."""
    gate = require_promotion_enabled(enabled=enabled, ab_gate=ab_gate)
    require_human_sign_off(sign_off_policy)
    require_independent_reviewer(
        reviewer_id=reviewer_id, reasoning_backend_id=reasoning_backend_id
    )
    rung = require_authority(authority)

    verdicts: list[PromotionVerdict] = []
    for candidate in candidates:
        history = _history_for(candidate, histories, history_source)
        verdict = evaluate_candidate(
            candidate,
            policy=policy,
            history=history,
            entailment=entailment,
            prior_art=prior_art,
            dedup=dedup,
            prose_author=prose_author,
            reviewer_id=reviewer_id,
            reasoning_backend_id=reasoning_backend_id,
        )
        if verdict.promoted and verdict.record is not None and verdict.diff is not None:
            if not verdict.record.sufficient_to_demote:
                raise ConsolidationError(
                    "the promotion record is not sufficient to demote by "
                    f"({verdict.record.demotion_handle()}); promotion without a "
                    "demotion handle is the failure the criteria were written to "
                    "prevent"
                )
            verdict = replace(
                verdict,
                effects=effects_for_promotion(candidate, verdict.record, verdict.diff),
            )
        verdicts.append(verdict)

    promoted = tuple(v for v in verdicts if v.promoted)
    return ConsolidationBatch(
        verdicts=tuple(verdicts),
        policy=policy,
        review=HumanReviewRequest(
            diff_count=len(promoted),
            blast_radius=len(
                {v.record.target_note_id for v in promoted if v.record is not None}
            ),
            authority_rung=rung,
            reviewer_id=reviewer_id,
        ),
        ab_gate=gate,
        independence_basis=policy.independence_over,
    )


def _history_for(
    candidate: PromotionCandidate,
    histories: Mapping[str, TrialHistory] | None,
    source: QueryCacheSource | None,
) -> TrialHistory:
    if histories is not None and candidate.derivation_id in histories:
        return histories[candidate.derivation_id]
    if source is not None:
        return source.trial_history(
            candidate.derivation_id, subject_kind="promoted_claim"
        )
    return TrialHistory(
        subject_id=candidate.derivation_id, subject_kind="promoted_claim"
    )


__all__ = [
    "AdditiveProseAuthor",
    "AuthorityCapError",
    "BUILD_NOISE_FLOOR",
    "CONDITIONS",
    "ConditionName",
    "ConditionOutcome",
    "ConsolidationBatch",
    "ConsolidationDisabledError",
    "ConsolidationError",
    "ConsolidationPolicy",
    "DEFAULT_CONSOLIDATION_POLICY",
    "DEFAULT_DWELL_DAYS",
    "DEFAULT_PRIOR_ART_TOP_K",
    "DEFAULT_SYNONYMY_TAU",
    "DWELL_WINDOW_DAYS_MAX",
    "DWELL_WINDOW_DAYS_MIN",
    "DedupAction",
    "DedupDecision",
    "DedupJudge",
    "DedupRequest",
    "DemotionHandle",
    "DerivationOccurrence",
    "ENTAILMENT_CALIBRATION_CAVEAT",
    "EntailmentJudge",
    "EntailmentRequest",
    "EntailmentVerdict",
    "HARD_CONDITIONS",
    "HumanGateError",
    "HumanReviewRequest",
    "INDEPENDENCE_BASIS_EPISODES",
    "INDEPENDENCE_BASIS_FACTS",
    "LinkBeforeCreateJudge",
    "MIN_AB_ORDERINGS",
    "MIN_AB_RUNS_PER_ARM",
    "MIN_INDEPENDENT_CONTEXTS",
    "MIN_RECURRENCE",
    "MoverIsJudgeError",
    "PROMOTION_ENABLED_BY_DEFAULT",
    "PROMOTION_STAGE",
    "PROMOTION_TARGETS",
    "PriorArtEntry",
    "PriorArtIndex",
    "PriorArtMatch",
    "PromotionABGate",
    "PromotionABNotRunError",
    "PromotionCandidate",
    "PromotionDiff",
    "PromotionLifecycle",
    "PromotionProseAuthor",
    "PromotionRecord",
    "PromotionTarget",
    "PromotionVerdict",
    "ProseRequest",
    "QUALIFIER_KINDS",
    "Qualifier",
    "QualifierKind",
    "QualifierStrippedError",
    "REASON_ANSWER_CHANGED",
    "REASON_DERIVED_TOO_FEW_TIMES",
    "REASON_ENTAILMENT_ABSTAINED",
    "REASON_ENTAILMENT_FAILED",
    "REASON_ETA_BELOW_FLOOR",
    "REASON_INSIDE_DWELL_WINDOW",
    "REASON_NEAR_DUPLICATE",
    "REASON_NO_EMBEDDING",
    "REASON_NO_NEIGHBOURHOOD",
    "REASON_NO_RELATION_TRIPLE",
    "REASON_NO_RENDERER",
    "REASON_NO_SOURCE_SPAN",
    "REASON_OPEN_CORRECTION",
    "REQUIRED_REGRESSION_CLASSES",
    "SCOPE_NEIGHBOURHOOD",
    "SECONDS_PER_DAY",
    "StaticEntailmentJudge",
    "StaticPriorArtIndex",
    "UNRUN_PROMOTION_AB",
    "UncalibratedEntailmentJudge",
    "cosine",
    "effects_for_promotion",
    "evaluate_candidate",
    "evaluate_dedup",
    "evaluate_grounding",
    "evaluate_independence",
    "evaluate_recurrence",
    "evaluate_reliability",
    "evaluate_renderable",
    "evaluate_stability",
    "independence_count",
    "lifecycle_for",
    "missing_locators",
    "missing_qualifiers",
    "prior_art_shortlist",
    "require_authority",
    "require_human_sign_off",
    "require_independent_reviewer",
    "require_promotion_enabled",
    "run_consolidation_batch",
    "verify_qualifiers_intact",
]
