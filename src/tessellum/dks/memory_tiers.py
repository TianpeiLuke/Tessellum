"""tessellum.dks.memory_tiers — the tier vocabulary, the reliability gate, the ports.

P9 of the query-time DKS plan. **Two different triples** run through this design,
and conflating them is the mistake this module exists to prevent:

* **T0 / T1 / T2** partition the *representation stack* of one epistemic act —
  working (discarded at commit) → log (append-only, of-record) → graph (exactly
  the fold of the log). See :data:`REPRESENTATIONS`.
* **Tier A / B / C** partition *memory by lifetime and purpose* — the resolution
  cache → the query→note cache with its feedback signal → promotion into durable
  authored notes. See :data:`TIERS`.

They are **orthogonal**: the Tier-B cache is itself a projection over records,
and one Tier-C promotion passes through all three representations. An earlier
reading treated the two triples as one and dropped Tier B entirely, which is why
this module states both vocabularies as data rather than as prose.

**Why the tier this module serves is load-bearing.** A consolidation gate turns
on a reliability estimate ``η = (n_pass + 1) / (n_trial + 2)`` and on there being
no open correction flag — and *neither has a data source in a working→log→graph
stack*. The claim/edge log records claims, edges and locators; it never records
whether an answer turned out to be right. Tier B is where that outcome lands, so
without it the promotion gate cannot be evaluated at all.

**The non-negotiable guard is demotion-first.** :func:`score_after` lowers or
evicts a mapping on a negative verdict unconditionally, while the reinforcement
path is gated by :attr:`FeedbackPolicy.reinforcement_enabled`, which is
**``False`` by default**. The ordering is deliberate and it is not stylistic: a
memory that can only be reinforced entrenches a wrong mapping, because every
episode that used it counts as evidence for it. Reinforcement ships second, after
the A/Bs that this plan's gates have not yet run.

**Both caches are rebuildable projections.** Tier A is a projection of authored
frontmatter plus query-derived rows; Tier B is a projection of a deployment's own
review stream, re-ingestible through :class:`VerdictSource`. Dropping either
costs latency and precision, never knowledge — which is what makes eviction a
legitimate operation here and an illegal one in the log.

Model-free by construction: cache keys, counters and eviction arithmetic are the
whole of it. The one genuinely semantic neighbour — deciding that two *spans*
state the same fact — lives behind ``claim_identity.FactIdentityResolver`` and is
not smuggled in here.

Pure (the Dependency Rule): no runtime import, no disk, no vault write. The
storage that backs :class:`QueryCacheSource` / :class:`FeedbackSink` lives in
``runtime.query_cache``.
"""

from __future__ import annotations

import hashlib
import re
from array import array
from dataclasses import dataclass, replace
from typing import Iterable, Literal, Mapping, Protocol, Sequence, runtime_checkable

# ── the two vocabularies, as data ───────────────────────────────────────────

TierName = Literal["A", "B", "C"]
"""The memory layers, by lifetime and purpose."""

RepresentationName = Literal["working", "log", "graph"]
"""The representation stack of one epistemic act (T0 / T1 / T2)."""


@dataclass(frozen=True)
class TierSpec:
    """What one memory tier is, and the three properties consumers depend on.

    ``rebuildable`` and ``evictable`` travel together for a projection and are
    both false for the of-record log. ``demotable`` is the property Tier B adds
    and Tier A does not have: a mapping can be *scored down* by feedback, where a
    projected authored fact is simply re-projected."""

    tier: TierName
    what: str
    realised_by: str
    lifetime: str
    rebuildable: bool
    evictable: bool
    demotable: bool


TIERS: Mapping[str, TierSpec] = {
    "A": TierSpec(
        tier="A",
        what="resolution memory — the thin relations hot set, origin in {authored, resolved}",
        realised_by="runtime.registry_store (authored seed) + runtime.query_cache (resolved rows)",
        lifetime="rebuildable cache",
        rebuildable=True,
        evictable=True,
        demotable=False,
    ),
    "B": TierSpec(
        tier="B",
        what="query→note memory with a feedback signal — the query cache",
        realised_by="runtime.query_cache",
        lifetime="rebuildable cache; re-ingestible from the deployment's verdict stream",
        rebuildable=True,
        evictable=True,
        demotable=True,
    ),
    "C": TierSpec(
        tier="C",
        what="promotion into durable authored notes",
        realised_by="the consolidation phase, gated by the demotion gate and an A/B",
        lifetime="durable — the notes themselves",
        rebuildable=False,
        evictable=False,
        demotable=True,
    ),
}
"""Tier A / B / C. Tier C is the only durable one; A and B are projections."""


@dataclass(frozen=True)
class RepresentationSpec:
    """One rung of the representation stack.

    ``of_record_for_epistemics`` is the distinction that actually matters and the
    one an implementation gets wrong first: a working store paged to disk for
    context-budget reasons is *durable* without being *of-record*, and calling it
    T1 would put un-adjudicated scratch into the epistemic record."""

    name: RepresentationName
    what: str
    of_record_for_epistemics: bool
    discarded_at_commit: bool
    rebuildable_from: str


REPRESENTATIONS: Mapping[str, RepresentationSpec] = {
    "working": RepresentationSpec(
        name="working",
        what="the episode's scratch state",
        of_record_for_epistemics=False,
        discarded_at_commit=True,
        rebuildable_from="nothing — it is re-derived by re-running the episode",
    ),
    "log": RepresentationSpec(
        name="log",
        what="the append-only claim/edge log",
        of_record_for_epistemics=True,
        discarded_at_commit=False,
        rebuildable_from="only authored structure; runtime-derived records are of-record",
    ),
    "graph": RepresentationSpec(
        name="graph",
        what="the folded view the labelling runs over",
        of_record_for_epistemics=False,
        discarded_at_commit=False,
        rebuildable_from="the log, exactly — it is the fold",
    ),
}
"""T0 / T1 / T2. Orthogonal to :data:`TIERS`; neither table refines the other."""


def is_rebuildable_projection(tier: str) -> bool:
    """Whether dropping ``tier`` costs latency/precision rather than knowledge."""
    spec = TIERS.get(tier)
    if spec is None:
        raise ValueError(f"unknown memory tier: {tier!r}")
    return spec.rebuildable and spec.evictable


# ── the feedback vocabulary ─────────────────────────────────────────────────

SubjectKind = Literal["cached_mapping", "promoted_claim"]
"""What a trial was a trial OF — the two things a query episode can lean on.

``subject_id`` is opaque here. The convention consumers follow is a
``query_key`` for a ``cached_mapping`` and a ``derivation_id`` for a
``promoted_claim`` — the latter because a revision preserves its
``derivation_id``, so a revised claim inherits its own trial history instead of
starting over with the fail-closed prior."""

SUBJECT_KINDS: frozenset[str] = frozenset({"cached_mapping", "promoted_claim"})

EventKind = Literal["trial", "verdict", "correction_raise", "correction_release"]
"""The four things the feedback log records.

A ``trial`` says an episode *used* the subject; a ``verdict`` says how it turned
out; the two correction kinds are the open/closed lifecycle of a flag. Separating
trial from verdict is what makes feedback *coverage* measurable rather than
invisible: an episode with no verdict is un-adjudicated, not a failure."""

EVENT_KINDS: frozenset[str] = frozenset(
    {"trial", "verdict", "correction_raise", "correction_release"}
)

Verdict = Literal["correct", "incorrect", "partial", "unknown"]
"""How a reviewer judged one episode's answer."""

VERDICTS: frozenset[str] = frozenset({"correct", "incorrect", "partial", "unknown"})

NEGATIVE_VERDICTS: frozenset[str] = frozenset({"incorrect", "partial"})
"""The verdicts that MUST be able to lower or evict a mapping (demotion-first)."""

SOURCE_REVIEWED_QA: str = "reviewed_qa"
"""Verdicts from a deployment's own reviewed question-and-answer workflow.

Deliberately generic: this package names no deployment's review tool. A
deployment supplies its own stream through :class:`VerdictSource`."""

SOURCE_EXPLICIT_THUMB: str = "explicit_thumb"
"""A reader's explicit up/down signal on one answer."""


class FeedbackEventError(ValueError):
    """A feedback event whose kind and payload disagree.

    Raised at construction rather than at write time, so a malformed event
    cannot reach a store and quietly become a counted trial."""


@dataclass(frozen=True)
class FeedbackEvent:
    """One immutable row of the feedback log.

    ``event_id`` is content-derived and **excludes ``at`` and ``seq``**, so
    re-pulling a deployment's verdict stream is a no-op however many times it is
    pulled and whatever clock the pull happens on. ``seq`` is the store's log
    position (``0`` for an event that a source produced and nothing has stored
    yet); ordering is by ``(at, seq, event_id)``, which is total in both cases.
    """

    kind: EventKind
    subject_id: str
    subject_kind: SubjectKind
    episode_id: str
    at: float
    verdict: Verdict | None = None
    source: str = SOURCE_REVIEWED_QA
    detail: str = ""
    releases: str | None = None
    seq: int = 0

    def __post_init__(self) -> None:
        if self.kind not in EVENT_KINDS:
            raise FeedbackEventError(f"unknown feedback event kind: {self.kind!r}")
        if self.subject_kind not in SUBJECT_KINDS:
            raise FeedbackEventError(f"unknown subject kind: {self.subject_kind!r}")
        if self.verdict is not None and self.verdict not in VERDICTS:
            raise FeedbackEventError(f"unknown verdict: {self.verdict!r}")
        if self.kind == "verdict" and self.verdict is None:
            raise FeedbackEventError("a 'verdict' event must carry a verdict")
        if self.kind != "verdict" and self.verdict is not None:
            raise FeedbackEventError(f"a {self.kind!r} event carries no verdict")
        if self.kind == "correction_release" and not self.releases:
            raise FeedbackEventError(
                "a 'correction_release' event must name the flag it releases"
            )
        if self.kind != "correction_release" and self.releases is not None:
            raise FeedbackEventError(f"a {self.kind!r} event releases nothing")

    @property
    def event_id(self) -> str:
        """The content address of this event — its idempotency key."""
        return _content_id(
            self.kind,
            self.subject_id,
            self.subject_kind,
            self.episode_id,
            self.verdict,
            self.source,
            self.detail,
            self.releases,
        )

    @property
    def is_negative(self) -> bool:
        return self.verdict in NEGATIVE_VERDICTS


@dataclass(frozen=True)
class CorrectionFlag:
    """An open-or-closed correction flag — the gate condition, as real state.

    Not a boolean on a row: a flag is *raised* by one event and *released* by a
    later one that names it, so the whole history of a subject's corrections
    stays readable and a release cannot be confused with the flag never having
    existed. A consolidation gate reads :attr:`is_open`."""

    flag_id: str
    subject_id: str
    subject_kind: str
    episode_id: str
    raised_at: float
    reason: str = ""
    released_at: float | None = None
    release_detail: str = ""

    @property
    def is_open(self) -> bool:
        return self.released_at is None


@dataclass(frozen=True)
class TrialHistory:
    """The counts a reliability gate needs, and the coverage figure beside them.

    ``n_trial`` counts **adjudicated** trials — distinct episodes that used the
    subject *and* received a verdict. ``n_unadjudicated`` counts episodes that
    used it and were never judged. The split is the precise definition the gate
    needs, and it is chosen over the alternative (count every use as a trial and
    treat silence as failure) because that alternative makes η a function of
    feedback *coverage* rather than of reliability: a well-instrumented mapping
    would score below a barely-observed one. Coverage is reported here instead,
    so a gate can require it separately.

    Repeated verdicts for one episode do not inflate anything: the tally keeps
    the LAST verdict per episode, so a correction supersedes an earlier
    judgement."""

    subject_id: str
    subject_kind: str = ""
    n_trial: int = 0
    n_pass: int = 0
    n_fail: int = 0
    n_partial: int = 0
    n_unknown: int = 0
    n_unadjudicated: int = 0
    open_corrections: tuple[CorrectionFlag, ...] = ()

    @property
    def eta(self) -> float:
        """η = (n_pass + 1) / (n_trial + 2) — the reliability estimate."""
        return reliability(self.n_pass, self.n_trial)

    @property
    def has_open_correction(self) -> bool:
        return bool(self.open_corrections)

    @property
    def coverage(self) -> float:
        """Fraction of observed uses that were adjudicated (1.0 for no uses)."""
        total = self.n_trial + self.n_unadjudicated
        return 1.0 if total == 0 else self.n_trial / total


RELIABILITY_FLOOR: float = 0.8
"""The consolidation gate's η floor. Below it a claim is probationary, not active."""


def reliability(n_pass: int, n_trial: int) -> float:
    """η = (n_pass + 1) / (n_trial + 2) — Laplace-smoothed, so it is fail-closed.

    With no trial history at all this is ``0.5``, comfortably under
    :data:`RELIABILITY_FLOOR`: an unobserved claim cannot pass a reliability gate
    by having nothing recorded against it. The ``+1/+2`` is also what keeps a
    single lucky pass from reading as certainty (1 of 1 → ``0.667``).

    Raises:
        ValueError: on negative counts or ``n_pass > n_trial`` — an impossible
            history is a bug in the caller's tally, not a low score.
    """
    if n_trial < 0 or n_pass < 0:
        raise ValueError(f"negative trial counts: n_pass={n_pass}, n_trial={n_trial}")
    if n_pass > n_trial:
        raise ValueError(f"more passes than trials: n_pass={n_pass}, n_trial={n_trial}")
    return (n_pass + 1) / (n_trial + 2)


def meets_reliability_gate(
    history: TrialHistory, *, floor: float = RELIABILITY_FLOOR
) -> bool:
    """Both halves of the gate: η at or above ``floor`` AND no open correction.

    The two conditions are ANDed here rather than at each call site because they
    fail differently — a low η is "not yet trusted", an open flag is "known
    wrong" — and a consumer that checked only the first would promote a mapping
    somebody has already reported as broken."""
    return history.eta >= floor and not history.has_open_correction


# ── the tally: events → counts (pure) ───────────────────────────────────────


def _ordering_key(event: FeedbackEvent) -> tuple[float, int, str]:
    return (event.at, event.seq, event.event_id)


def _for_subject(
    events: Iterable[FeedbackEvent], subject_id: str | None
) -> list[FeedbackEvent]:
    return sorted(
        (
            event
            for event in events
            if subject_id is None or event.subject_id == subject_id
        ),
        key=_ordering_key,
    )


def correction_flags(
    events: Iterable[FeedbackEvent], *, subject_id: str | None = None
) -> tuple[CorrectionFlag, ...]:
    """Every correction flag in ``events``, open or released, in raise order."""
    ordered = _for_subject(events, subject_id)
    releases: dict[str, FeedbackEvent] = {}
    for event in ordered:
        if event.kind == "correction_release" and event.releases is not None:
            releases.setdefault(event.releases, event)
    flags: list[CorrectionFlag] = []
    for event in ordered:
        if event.kind != "correction_raise":
            continue
        release = releases.get(event.event_id)
        flags.append(
            CorrectionFlag(
                flag_id=event.event_id,
                subject_id=event.subject_id,
                subject_kind=event.subject_kind,
                episode_id=event.episode_id,
                raised_at=event.at,
                reason=event.detail,
                released_at=None if release is None else release.at,
                release_detail="" if release is None else release.detail,
            )
        )
    return tuple(flags)


def open_correction_flags(
    events: Iterable[FeedbackEvent], *, subject_id: str | None = None
) -> tuple[CorrectionFlag, ...]:
    return tuple(
        flag for flag in correction_flags(events, subject_id=subject_id) if flag.is_open
    )


def has_open_correction(
    events: Iterable[FeedbackEvent], *, subject_id: str | None = None
) -> bool:
    """The gate's second condition, over raw events."""
    return bool(open_correction_flags(events, subject_id=subject_id))


def tally_trials(
    events: Iterable[FeedbackEvent],
    *,
    subject_id: str,
    subject_kind: str | None = None,
) -> TrialHistory:
    """Count one subject's trial history — pure, no clock, no I/O.

    A verdict is itself evidence that its episode used the subject, so an
    episode with a verdict and no ``trial`` row still counts as a trial; the
    ``trial`` rows are what let un-adjudicated *uses* be counted separately.
    """
    ordered = [
        event
        for event in _for_subject(events, subject_id)
        if subject_kind is None or event.subject_kind == subject_kind
    ]
    used: set[str] = set()
    latest: dict[str, FeedbackEvent] = {}
    for event in ordered:
        if event.kind == "trial":
            used.add(event.episode_id)
        elif event.kind == "verdict":
            used.add(event.episode_id)
            latest[event.episode_id] = event  # ordered ascending: the last one wins
    counts = {"correct": 0, "incorrect": 0, "partial": 0, "unknown": 0}
    for event in latest.values():
        assert event.verdict is not None  # guaranteed by FeedbackEvent.__post_init__
        counts[event.verdict] += 1
    kinds = {event.subject_kind for event in ordered}
    return TrialHistory(
        subject_id=subject_id,
        subject_kind=subject_kind or (kinds.pop() if len(kinds) == 1 else ""),
        n_trial=len(latest),
        n_pass=counts["correct"],
        n_fail=counts["incorrect"],
        n_partial=counts["partial"],
        n_unknown=counts["unknown"],
        n_unadjudicated=len(used - set(latest)),
        open_corrections=open_correction_flags(ordered, subject_id=subject_id),
    )


# ── demotion first: the scoring policy (pure) ───────────────────────────────

ScoreAction = Literal["hold", "demote", "evict", "reinforce"]
"""What a verdict did to a cached mapping's standing."""

INITIAL_FEEDBACK_SCORE: float = 1.0
"""A freshly written mapping starts trusted — it was derived, not guessed.

Demotion is therefore the only thing that moves the score until reinforcement is
enabled, which is exactly the asymmetry the guard wants."""


@dataclass(frozen=True)
class FeedbackPolicy:
    """The arithmetic of demotion, and the switch that keeps reinforcement off.

    ``reinforcement_enabled`` defaults to ``False`` and that default is the
    phase's non-negotiable, not a tuning choice: the reinforcement path ships
    *after* the A/Bs, because a memory that can only be reinforced entrenches a
    wrong mapping. Every field is a plain number so the policy is auditable and
    a deployment can tighten it without touching code."""

    demotion_step: float = 0.5
    partial_demotion_step: float = 0.25
    eviction_floor: float = 0.0
    reinforcement_enabled: bool = False
    reinforcement_step: float = 0.25
    max_score: float = 1.0
    raise_correction_on_negative: bool = True


DEFAULT_FEEDBACK_POLICY: FeedbackPolicy = FeedbackPolicy()
"""Demotion-first, reinforcement OFF. Two negative verdicts evict a mapping."""


@dataclass(frozen=True)
class ScoreDecision:
    """What ``score_after`` decided, and why — reported, never silent."""

    action: ScoreAction
    score: float
    previous_score: float
    reason: str


def score_after(
    score: float,
    verdict: Verdict,
    *,
    policy: FeedbackPolicy = DEFAULT_FEEDBACK_POLICY,
) -> ScoreDecision:
    """The demotion-first scoring rule — pure arithmetic over one verdict.

    * ``incorrect`` / ``partial`` lower the score, and take it to eviction once
      it reaches :attr:`FeedbackPolicy.eviction_floor`. This path is
      unconditional; there is no flag that can switch it off.
    * ``correct`` reinforces **only** when the policy enables it, and otherwise
      holds — the returned ``reason`` says so, so a caller cannot mistake the
      default for "the mapping was reinforced".
    * ``unknown`` holds: a reviewer who could not judge is not evidence.
    """
    if verdict not in VERDICTS:
        raise ValueError(f"unknown verdict: {verdict!r}")
    if verdict == "unknown":
        return ScoreDecision(
            action="hold",
            score=score,
            previous_score=score,
            reason="verdict 'unknown' carries no evidence either way",
        )
    if verdict == "correct":
        if not policy.reinforcement_enabled:
            return ScoreDecision(
                action="hold",
                score=score,
                previous_score=score,
                reason=(
                    "reinforcement is default-off (FeedbackPolicy."
                    "reinforcement_enabled): the demotion path ships first"
                ),
            )
        raised = min(policy.max_score, score + policy.reinforcement_step)
        return ScoreDecision(
            action="reinforce",
            score=raised,
            previous_score=score,
            reason="positive verdict, reinforcement explicitly enabled",
        )
    step = policy.demotion_step if verdict == "incorrect" else policy.partial_demotion_step
    lowered = max(policy.eviction_floor, score - step)
    if lowered <= policy.eviction_floor:
        return ScoreDecision(
            action="evict",
            score=policy.eviction_floor,
            previous_score=score,
            reason=f"verdict {verdict!r} took the score to the eviction floor",
        )
    return ScoreDecision(
        action="demote",
        score=lowered,
        previous_score=score,
        reason=f"verdict {verdict!r} lowered the score by {step}",
    )


# ── the Tier-A and Tier-B row shapes ────────────────────────────────────────

_WHITESPACE = re.compile(r"\s+")


def _content_id(*parts: str | None) -> str:
    """``sha256`` over NUL-joined parts — the runtime's 64-hex convention."""
    raw = "\0".join("" if part is None else part for part in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def query_key_for(query: str) -> str:
    """The Tier-B cache key: casefold + collapse whitespace, then hash.

    Deterministic and model-free — the same question asked with different
    spacing or capitalisation is one key. Semantic near-misses are deliberately
    NOT collapsed here: that would need the embedding, and folding it into the
    key would make a cache hit depend on a model's opinion of similarity."""
    return _content_id(_WHITESPACE.sub(" ", query.strip()).casefold())


def pack_embedding(values: Sequence[float]) -> bytes:
    """Pack a query embedding for storage — little-endian float32, stdlib only."""
    packed = array("f", values)
    if packed.itemsize != 4:  # pragma: no cover - defensive: 'f' is float32
        raise ValueError("array('f') is not 4 bytes wide on this platform")
    return packed.tobytes()


def unpack_embedding(blob: bytes | None) -> tuple[float, ...]:
    """Unpack :func:`pack_embedding`. ``None`` is an absent embedding, not zeros."""
    if not blob:
        return ()
    values = array("f")
    values.frombytes(blob)
    return tuple(values)


@dataclass(frozen=True)
class CachedMapping:
    """One Tier-B row: a query key and the notes it resolved to.

    ``feedback_score`` is standing, not truth — a demotable number in
    ``[eviction_floor, max_score]``. ``hits`` and ``last_used`` are the eviction
    inputs (and the coverage denominator for cached mappings), never evidence of
    correctness: a mapping used a hundred times without a verdict has learned
    nothing."""

    query_key: str
    target_note_ids: tuple[str, ...]
    feedback_score: float = INITIAL_FEEDBACK_SCORE
    hits: int = 0
    last_used: float | None = None
    query_embedding: bytes | None = None
    created_at: float = 0.0

    @property
    def embedding(self) -> tuple[float, ...]:
        return unpack_embedding(self.query_embedding)


RESOLVED_ORIGIN: str = "resolved"
"""The origin of a Tier-A row grown from query traffic, layered on the seed."""


@dataclass(frozen=True)
class ResolvedRelation:
    """One Tier-A row written on a cache MISS — ``origin='resolved'``.

    The counterpart of ``entity_registry.AuthoredRelation``, and deliberately a
    separate type rather than that one with a widened ``origin``: the authored
    seed is a projection of frontmatter, and a resolved row must not be able to
    ride in through the seed's door (nor the seed's rebuild delete a resolved
    row). ``relation_id`` folds the origin in, so the authored and resolved
    readings of one fact coexist instead of colliding.

    ``valid_from`` / ``valid_to`` are not decoration. A role-style relation
    without a validity interval confidently returns a FORMER holder; that failure
    is the reason the interval is in the row shape rather than in a follow-up."""

    subject_id: str
    predicate: str
    object_ref: str
    object_kind: Literal["entity", "literal"] = "literal"
    evidence_note: str = ""
    evidence_locator: str = ""
    valid_from: str | None = None
    valid_to: str | None = None
    epistemic_status: str = "proposed"
    origin: Literal["resolved"] = "resolved"
    superseded_by: str | None = None
    content_hash: str | None = None

    @property
    def relation_id(self) -> str:
        """Content address — a replayed write lands on the same row."""
        return _content_id(
            self.origin,
            self.subject_id,
            self.predicate,
            self.object_ref,
            self.evidence_locator,
            self.valid_from,
            self.valid_to,
        )[:24]


# ── the precision harness (pure) ────────────────────────────────────────────


@dataclass(frozen=True)
class PrecisionProbe:
    """One measured query: what is relevant, and what each arm returned.

    ``cached_note_ids`` is ``None`` for a cache MISS, and the with-cache arm then
    falls through to ``uncached_note_ids`` — which is what a real miss does, so
    the comparison measures the cache's effect rather than pretending a miss
    returns nothing."""

    query_key: str
    relevant_note_ids: tuple[str, ...]
    uncached_note_ids: tuple[str, ...]
    cached_note_ids: tuple[str, ...] | None = None

    def with_cached(self, note_ids: Sequence[str] | None) -> "PrecisionProbe":
        return replace(
            self, cached_note_ids=None if note_ids is None else tuple(note_ids)
        )


def precision(retrieved: Sequence[str], relevant: Sequence[str]) -> float:
    """|retrieved ∩ relevant| / |retrieved|. An empty retrieval scores ``0.0``.

    Scoring an empty return as zero rather than skipping it is deliberate: a
    cache that returns nothing has not abstained, it has failed to answer, and a
    metric that quietly drops those episodes flatters it."""
    if not retrieved:
        return 0.0
    wanted = set(relevant)
    return sum(1 for note_id in retrieved if note_id in wanted) / len(retrieved)


@dataclass(frozen=True)
class CachePrecisionComparison:
    """Target-note precision with vs. without the Tier-B cache.

    ``delta`` is the only number a gate should read, and it is signed on
    purpose: a cache that lowers precision must be visible as a negative, which
    is the measurement demotion-first exists to make possible."""

    episodes: int
    cache_hits: int
    precision_with_cache: float
    precision_without_cache: float

    @property
    def delta(self) -> float:
        return self.precision_with_cache - self.precision_without_cache

    @property
    def cache_hit_rate(self) -> float:
        return 0.0 if self.episodes == 0 else self.cache_hits / self.episodes


def compare_target_note_precision(
    probes: Sequence[PrecisionProbe],
) -> CachePrecisionComparison:
    """Mean target-note precision for both arms over the same probe set.

    Pure arithmetic over already-collected retrievals — no corpus, no model, no
    I/O. The runtime harness fills in the cached arm from a live store and
    delegates here, so the comparison itself stays testable without one."""
    if not probes:
        return CachePrecisionComparison(
            episodes=0, cache_hits=0, precision_with_cache=0.0, precision_without_cache=0.0
        )
    with_cache = 0.0
    without_cache = 0.0
    hits = 0
    for probe in probes:
        cached = (
            probe.uncached_note_ids
            if probe.cached_note_ids is None
            else probe.cached_note_ids
        )
        if probe.cached_note_ids is not None:
            hits += 1
        with_cache += precision(cached, probe.relevant_note_ids)
        without_cache += precision(probe.uncached_note_ids, probe.relevant_note_ids)
    count = len(probes)
    return CachePrecisionComparison(
        episodes=count,
        cache_hits=hits,
        precision_with_cache=with_cache / count,
        precision_without_cache=without_cache / count,
    )


# ── ports: DKS reads and proposes; the runtime stores ───────────────────────


@runtime_checkable
class VerdictSource(Protocol):
    """Adapter port for a deployment's own review stream.

    The supervised signal is *reviewed question-and-answer verdicts* plus
    explicit thumbs, and every deployment collects those differently — so this
    package ships no collector and names no tool. A deployment implements
    :meth:`verdicts` over whatever it already has and the store ingests it
    idempotently, which is also what makes the Tier-B table a rebuildable
    projection rather than a source of truth."""

    def verdicts(self, *, since: float | None = None) -> Sequence[FeedbackEvent]: ...


@dataclass(frozen=True)
class StaticVerdictSource:
    """Deterministic reference :class:`VerdictSource` over a fixed sequence.

    The shipped implementation for tests and for a deployment replaying an
    export: no network, no clock, no model. ``since`` is exclusive, matching the
    watermark a puller keeps."""

    events: tuple[FeedbackEvent, ...] = ()

    def verdicts(self, *, since: float | None = None) -> Sequence[FeedbackEvent]:
        return tuple(
            event
            for event in sorted(self.events, key=_ordering_key)
            if since is None or event.at > since
        )


@runtime_checkable
class QueryCacheSource(Protocol):
    """Read port over Tier B. The runtime backs it; ``dks`` opens no database."""

    def cached_targets(self, query_key: str) -> CachedMapping | None: ...

    def trial_history(
        self, subject_id: str, *, subject_kind: str | None = None
    ) -> TrialHistory: ...


@runtime_checkable
class FeedbackSink(Protocol):
    """Write port for the Tier-B projection — the demotion path.

    Not a breach of "the kernel never writes": these writes are the runtime's
    bookkeeping about its own cache, not epistemic acts on the vault. An
    epistemic retraction is an append to the claim log proposed as an effect; a
    demotion here only lowers a projection's standing.

    Deliberately not append-only *as a table* — the cache row is mutable and
    evictable — but the feedback events behind it are appended and never
    rewritten, which is what keeps η recomputable after an eviction."""

    def record_trial(
        self,
        *,
        subject_id: str,
        subject_kind: SubjectKind,
        episode_id: str,
        at: float | None = None,
    ) -> FeedbackEvent: ...

    def apply_verdict(
        self,
        *,
        subject_id: str,
        subject_kind: SubjectKind,
        episode_id: str,
        verdict: Verdict,
        source: str = SOURCE_REVIEWED_QA,
        detail: str = "",
        at: float | None = None,
        policy: FeedbackPolicy | None = None,
    ) -> "VerdictOutcome": ...

    def release_correction(
        self, flag_id: str, *, detail: str = "", at: float | None = None
    ) -> FeedbackEvent: ...


@dataclass(frozen=True)
class VerdictOutcome:
    """What one verdict did: the logged event, plus the demotion it triggered.

    ``score`` / ``previous_score`` are ``None`` when the subject has no cached
    mapping to score (a promoted claim, whose demotion is the re-derivation
    gate's business — here the verdict only feeds η and the correction flag)."""

    event: FeedbackEvent
    action: ScoreAction
    reason: str
    previous_score: float | None = None
    score: float | None = None
    evicted: bool = False
    correction_flag_id: str | None = None


__all__ = [
    "CachePrecisionComparison",
    "CachedMapping",
    "CorrectionFlag",
    "DEFAULT_FEEDBACK_POLICY",
    "EVENT_KINDS",
    "EventKind",
    "FeedbackEvent",
    "FeedbackEventError",
    "FeedbackPolicy",
    "FeedbackSink",
    "INITIAL_FEEDBACK_SCORE",
    "NEGATIVE_VERDICTS",
    "PrecisionProbe",
    "QueryCacheSource",
    "RELIABILITY_FLOOR",
    "REPRESENTATIONS",
    "RESOLVED_ORIGIN",
    "RepresentationName",
    "RepresentationSpec",
    "ResolvedRelation",
    "SOURCE_EXPLICIT_THUMB",
    "SOURCE_REVIEWED_QA",
    "SUBJECT_KINDS",
    "ScoreAction",
    "ScoreDecision",
    "StaticVerdictSource",
    "SubjectKind",
    "TIERS",
    "TierName",
    "TierSpec",
    "TrialHistory",
    "VERDICTS",
    "Verdict",
    "VerdictOutcome",
    "VerdictSource",
    "compare_target_note_precision",
    "correction_flags",
    "has_open_correction",
    "is_rebuildable_projection",
    "meets_reliability_gate",
    "open_correction_flags",
    "pack_embedding",
    "precision",
    "query_key_for",
    "reliability",
    "score_after",
    "tally_trials",
    "unpack_embedding",
]
