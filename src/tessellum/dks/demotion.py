"""tessellum.dks.demotion — the periodic re-derivation gate, and the three triggers.

P10 of the query-time-DKS plan, and the phase that has to exist *before* anything
is promoted. Promotion turns an episodic derivation into durable knowledge; a
promoted claim that stops being true has no way to notice on its own, so a
promotion path without a demotion path is a mechanism for entrenching whatever
was believed first. That is not a hypothetical failure mode — it is the one the
memory literature documents most consistently — which is why this gate ships
ahead of consolidation rather than beside it.

**The re-derivation gate is REQUIRED AND SCHEDULED, not an optional check.** It
is also the novel part: systems that abstract memory score an abstraction for
*utility* (was it recalled? did it help?) and none of them scores a produced
abstraction for *truth*. The protocol, in three steps, is what does that:

1. **Suppress** the promoted claim — the gate hands over neither its text nor its
   id. :class:`ReDerivationRequest` has nowhere to put them, and
   :func:`require_suppression` refuses a caller who smuggles the claim into the
   question or cites the claim's own rendering as its own source.
2. Give a **frozen** model **only its cited sources**. Frozen means pinned: an
   explicit ``model_id`` and ``frozen_at``, enforced by :func:`require_frozen`
   and satisfied by wrapping any model in :class:`FrozenReDerivationModel`. A
   model that re-tunes on the corpus it is checking would eventually regenerate
   its own promoted claim from the promotion, and the gate would certify itself.
3. Check whether the claim **regenerates**. The model produces text; the
   **comparison is arithmetic** (:func:`agreement`, a token-overlap ratio against
   a floor) and so is every trigger below. A model must never decide the verdict:
   a demotion nobody can recompute is a demotion nobody can appeal.

**Three triggers, not one.** Each fires independently, and the first is the one
an attack-driven system misses entirely:

=================================  ====================================================
Trigger                            Fires when
=================================  ====================================================
``rederivation_failure``           the frozen model does not regenerate the claim from
                                   its cited sources (or abstains) — **even with no
                                   attack against it anywhere in the log**
``contradiction``                  the computed status flipped out of answerable. Nearly
                                   free: status is a pure function of the edge set, so
                                   an appended attack changes it with no extra work
``independence_below_floor``       the number of independent contexts behind the claim
                                   fell under :data:`DemotionPolicy.independence_floor`
=================================  ====================================================

**Nothing is ever deleted.** The three actions are **down-rank**, **flag** and
**supersede-with-timestamp** — never a hard delete, and never a mutation. A
retraction is an **append**: a constructed retraction claim plus one operator
edge (``attack`` for a flag, ``supersede`` for a supersession), rendered as
:class:`~tessellum.dks.capability.CapabilityEffect` records that the commit tail
writes. The gate itself writes nothing, and it flips
``promotion_eligibility`` to ``ineligible`` rather than removing anything.

**A wrongly-demoted claim can come back**, and the recovery path is not
self-service. :func:`recover` requires a certificate issued by an *independent
validator* (:func:`~tessellum.dks.elevation.issue_certificate` refuses the
reasoning backend its own certificate), and it restores standing by **appending**
an attack on the retraction claim rather than by removing it: the fixed point
then reinstates the original claim, and both the demotion and the recovery stay
in :class:`DemotionLedger` forever. Recovery returns a claim to
``needs_validation``, never straight to ``eligible`` — a recovered claim
re-enters the gate, it does not skip it.

Pure (the Dependency Rule): no ``runtime`` import, no disk, no vault write, and
the single model call goes through an injected port. The log, the statuses, the
cited sources and the independence counts are all read through the ports at the
top of this module; storage and scheduling live in the runtime.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field, replace
from typing import Iterable, Literal, Mapping, Protocol, Sequence, runtime_checkable

from tessellum.dks.capability import (
    CapabilityEffect,
    CapabilityResult,
    PromotionEligibility,
)
from tessellum.dks.claim_identity import (
    FACT_ID_DEVIATION,
    anchor_locator,
    derivation_id,
    normalize_span_text,
)
from tessellum.dks.elevation import (
    DeepUnderstandingCertificate,
    MaturityProfile,
    MoveRanker,
    RewardInputs,
    issue_certificate,
    revoke,
)
from tessellum.dks.memory_port import (
    ClaimProposal,
    EdgeProposal,
    Proposal,
    effect_for_proposal,
)
from tessellum.dks.status import StatusError

# ── the trigger vocabulary ──────────────────────────────────────────────────

DemotionTrigger = Literal[
    "rederivation_failure", "contradiction", "independence_below_floor"
]
"""The three reasons a promoted claim loses its standing."""

TRIGGER_REDERIVATION_FAILURE: str = "rederivation_failure"
TRIGGER_CONTRADICTION: str = "contradiction"
TRIGGER_INDEPENDENCE_BELOW_FLOOR: str = "independence_below_floor"

TRIGGERS: frozenset[str] = frozenset(
    {
        TRIGGER_REDERIVATION_FAILURE,
        TRIGGER_CONTRADICTION,
        TRIGGER_INDEPENDENCE_BELOW_FLOOR,
    }
)
"""All three, and exactly three. A fourth would need its own arithmetic and its
own action; reliability (η) and the open-correction flag belong to the promotion
gate, which is a different decision made at a different time."""

DemotionAction = Literal["down_rank", "flag", "supersede_with_timestamp"]
"""What a demotion DOES. Deletion is deliberately not among them.

- ``down_rank`` — standing only: the claim keeps answering but sorts last (see
  :func:`down_rank_order`). Nothing is appended, because nothing about the claim
  was contradicted; its evidence base merely thinned.
- ``flag`` — an appended ``attack``. The claim becomes ``challenged``, so the
  read flow surfaces the conflict instead of answering from it.
- ``supersede_with_timestamp`` — an appended ``supersede`` carrying the check
  time in the retraction claim's own text. The claim becomes ``superseded``, so
  the read flow abstains, and the timestamp is in the log rather than in a
  mutable column somebody has to keep true.
"""

ACTIONS: frozenset[str] = frozenset(
    {"down_rank", "flag", "supersede_with_timestamp"}
)

ACTION_SEVERITY: Mapping[str, int] = {
    "down_rank": 1,
    "flag": 2,
    "supersede_with_timestamp": 3,
}
"""Severity order, used when more than one trigger fires: the strongest action
wins, because applying the mildest of several findings would answer from a claim
the gate has already contradicted."""

ANSWERABLE_STATUSES: frozenset[str] = frozenset({"warranted"})
"""The computed statuses a caller may answer from — the set a contradiction
leaves. ``challenged`` surfaces a conflict and ``proposed`` / ``superseded``
abstain, so all three are equally "no longer answerable"."""

STATUS_UNKNOWN: str = "unknown"
"""What a status source reports for a claim the log no longer holds. Treated as a
flip: a promoted claim that cannot be found is not a claim that still answers."""

ORIGIN_DEMOTION: str = "demotion"
"""``edges.origin`` for a retraction appended by this gate.

An addition to the origin vocabulary, not a fifth operator: ``origin`` records
what KIND of act produced an edge, and the four operators stay four."""

ORIGIN_RECOVERY: str = "recovery"
"""``edges.origin`` for the discharge that reverses a retraction."""

RETRACTION_SECTION: str = "retraction"
"""Locator section scoping a retraction's derivation, so a retraction can never
collide with the claim it retracts."""

RECOVERY_SECTION: str = "recovery"
"""Locator section scoping a recovery's derivation."""

# ── the arithmetic constants ────────────────────────────────────────────────

REGENERATION_FLOOR: float = 0.6
"""Token-overlap floor at which a regeneration counts as the same claim."""

INDEPENDENCE_FLOOR: int = 2
"""The promotion criteria's "≥ 2 independent contexts", read as a demotion floor:
what earned promotion is what must keep holding, or the claim goes back."""

DEFAULT_INTERVAL_DAYS: float = 7.0
"""Default cadence. The gate is scheduled, so "when someone remembers" is not an
option; the dwell window promotion uses is 7–14 days and re-checking at the low
end of it keeps a demotion no more than one window late."""

SECONDS_PER_DAY: float = 86400.0

REGENERATION_COMPARISON_DEVIATION: str = (
    "The gate compares a regeneration to the promoted claim by TOKEN OVERLAP "
    "(agreement() against a floor), not by meaning. Byte equality would demote "
    "every claim whose paraphrase differs, and claim identity deliberately "
    "treats text as a rendering; deciding that two renderings state the same "
    "fact is the cross-span fact layer, which is specified and not built. So a "
    "regeneration that says the same thing in different words can fail this "
    "gate, and one that reuses the vocabulary while inverting the assertion can "
    "pass it. Recorded here so no consumer reads a passed gate as an entailment "
    "check — the entailment gate is a separate, model-backed condition at "
    "promotion time."
)
"""The recorded deviation this gate owes its consumers. Cited beside
:data:`~tessellum.dks.claim_identity.FACT_ID_DEVIATION`, which is why the
comparison cannot be sharper yet."""

INDEPENDENCE_DEVIATION: str = FACT_ID_DEVIATION
"""Independence is counted over EPISODES, and that is weaker than counting
sources. The reason is not local to this module — see
:data:`~tessellum.dks.claim_identity.FACT_ID_DEVIATION`."""


# ── errors ──────────────────────────────────────────────────────────────────


class DemotionError(RuntimeError):
    """Base for every refusal this module makes."""


class FrozenModelError(DemotionError):
    """The re-derivation model is not pinned, so the check is not repeatable.

    Raised rather than defaulted: an unpinned model can drift onto the corpus it
    is checking and regenerate a promoted claim *from the promotion*, at which
    point the gate certifies its own output."""


class SuppressionError(DemotionError):
    """The promoted claim leaked into what the model was shown.

    A gate that shows the model the answer measures nothing. Both leaks are
    refused: the claim's text inside the question, and the claim's own rendering
    offered as one of its cited sources."""


class GateNotArmedError(DemotionError):
    """A promoted claim is overdue for re-derivation.

    The gate is required and scheduled, so "not run yet" must be an error a
    promotion path trips over rather than a silence it benefits from."""


class RecoveryError(DemotionError):
    """A recovery was asked for on a claim the ledger does not show demoted."""


# ── ports: the gate reads and proposes; the runtime stores ──────────────────


@dataclass(frozen=True)
class CitedSource:
    """One span a promoted claim cited — all the model is allowed to see.

    ``content_hash`` is the cited note's hash at the time the source was read,
    so a re-derivation that ran against a changed base is visible after the fact
    rather than being silently attributed to the model."""

    note_id: str
    locator: str
    text: str
    content_hash: str = ""


@runtime_checkable
class SourceReader(Protocol):
    """Read port over a promoted claim's cited sources. The runtime backs it."""

    def cited_sources(self, claim_id: str) -> Sequence[CitedSource]: ...


@dataclass(frozen=True)
class StaticSourceReader:
    """Deterministic reference :class:`SourceReader` over a fixed mapping.

    The shipped implementation for tests and for a replayed export: no index, no
    vault read. A claim with no entry has **no** cited sources, which the gate
    reads as a re-derivation failure — an ungrounded promoted claim is exactly
    what this gate exists to catch."""

    sources: Mapping[str, Sequence[CitedSource]] = field(default_factory=dict)

    def cited_sources(self, claim_id: str) -> Sequence[CitedSource]:
        return tuple(self.sources.get(claim_id, ()))


@dataclass(frozen=True)
class ReDerivationRequest:
    """What the frozen model is given — and what it is structurally NOT given.

    There is no field for the promoted claim's text and none for its
    ``claim_id``: suppression is a property of this shape rather than a
    discipline a caller has to remember. ``derivation_id`` is admissible because
    it is a hash of ``(note_id, span_locator)`` and carries no assertion; a model
    cannot read the answer out of it.
    """

    derivation_id: str
    note_id: str
    sources: tuple[CitedSource, ...] = ()
    question: str = ""

    @property
    def source_locators(self) -> tuple[str, ...]:
        return tuple(source.locator for source in self.sources)


@dataclass(frozen=True)
class ReDerivationOutput:
    """What the model returned: a regeneration, or an abstention.

    An abstention is a first-class answer and it counts as a **failure** here.
    That asymmetry is deliberate: "I cannot state this claim from these sources"
    is precisely the finding the gate is looking for."""

    text: str = ""
    abstained: bool = False
    detail: str = ""


@runtime_checkable
class ReDerivationModel(Protocol):
    """The one model seam in this module — injected, never constructed here.

    Regenerating a claim from prose is a judgement about meaning, so it needs a
    model. Everything the gate then DOES with the regeneration is arithmetic."""

    def re_derive(self, request: ReDerivationRequest) -> ReDerivationOutput: ...


@dataclass(frozen=True)
class FrozenReDerivationModel:
    """A :class:`ReDerivationModel` pinned to a version — the frozen wrapper.

    ``model_id`` and ``frozen_at`` are what :func:`require_frozen` checks, and
    the wrapper exists so freezing is a visible act at the call site rather than
    an assumption. ``corpus_snapshot_id`` records which corpus the pin was taken
    against, for the same reason the reward construction reads a frozen snapshot:
    a model that has seen the promotion is not an independent check of it."""

    model: ReDerivationModel
    model_id: str
    frozen_at: float = 0.0
    corpus_snapshot_id: str = ""

    def __post_init__(self) -> None:
        if not (self.model_id or "").strip():
            raise FrozenModelError(
                "a frozen re-derivation model needs a non-empty model_id: an "
                "unpinned model cannot be shown not to have re-tuned"
            )

    def re_derive(self, request: ReDerivationRequest) -> ReDerivationOutput:
        return self.model.re_derive(request)


@dataclass(frozen=True)
class ScriptedReDerivationModel:
    """Deterministic reference :class:`ReDerivationModel` — a replayed script.

    Keyed by ``derivation_id``, which is the only claim-identifying field the
    request carries, so the reference implementation cannot see more than a real
    model would. A missing key **abstains** rather than guessing: the fail-closed
    reading, and the one that keeps an unscripted claim from passing by accident.

    It deliberately carries no ``model_id``: a caller must wrap it in
    :class:`FrozenReDerivationModel` to run the gate, which is the enforcement
    exercised rather than described."""

    outputs: Mapping[str, str] = field(default_factory=dict)
    detail: str = "scripted regeneration"

    def re_derive(self, request: ReDerivationRequest) -> ReDerivationOutput:
        if request.derivation_id not in self.outputs:
            return ReDerivationOutput(
                abstained=True,
                detail="no scripted regeneration for this derivation",
            )
        return ReDerivationOutput(
            text=self.outputs[request.derivation_id], detail=self.detail
        )


@runtime_checkable
class CurrentStatusSource(Protocol):
    """Read port over the computed status of a claim, at read time.

    A plain label rather than a verdict object, so the status phase's query
    surface, the boundary's ``status`` call and a replayed table all satisfy it.
    The gate never computes a status itself and never writes one."""

    def status_of(self, claim_id: str) -> str: ...


@dataclass(frozen=True)
class StaticStatusSource:
    """Deterministic reference :class:`CurrentStatusSource` over a mapping.

    An absent claim reports :data:`STATUS_UNKNOWN`, which the contradiction check
    reads as a flip."""

    statuses: Mapping[str, str] = field(default_factory=dict)

    def status_of(self, claim_id: str) -> str:
        return self.statuses.get(claim_id, STATUS_UNKNOWN)


class _Verdict(Protocol):
    @property
    def status(self) -> str: ...


@runtime_checkable
class VerdictQuery(Protocol):
    """The status phase's ``status`` query, as this gate reads it."""

    def status(self, claim_id: str, *, allow_provisional: bool = False) -> _Verdict: ...


@dataclass(frozen=True)
class VerdictQueryStatusSource:
    """Adapter from the status phase's :class:`VerdictQuery` to this gate's port.

    An adapter rather than a change to the status module: ``status`` /
    ``explain`` already compute everything the contradiction trigger needs, and a
    gate that reached into them would give the labelling a second caller to keep
    happy. ``allow_provisional`` defaults to ``True`` because a verdict the status
    phase REFUSES to report is still information here — a promoted claim whose
    chain has decayed into a stub is not a claim that still answers — and a
    refusal is mapped to :data:`STATUS_UNKNOWN`, never to "still warranted"."""

    query: VerdictQuery
    allow_provisional: bool = True

    def status_of(self, claim_id: str) -> str:
        try:
            verdict = self.query.status(
                claim_id, allow_provisional=self.allow_provisional
            )
        except StatusError:
            return STATUS_UNKNOWN
        return verdict.status


@runtime_checkable
class IndependenceSource(Protocol):
    """Read port over the contexts standing behind a claim, NOW.

    Returns context ids rather than a count so the gate can report *which*
    contexts remain, and so a caller can see when a count fell because one
    context was withdrawn rather than because the arithmetic changed."""

    def independent_contexts(self, derivation: str) -> Sequence[str]: ...


@dataclass(frozen=True)
class StaticIndependenceSource:
    """Deterministic reference :class:`IndependenceSource` over a mapping."""

    contexts: Mapping[str, Sequence[str]] = field(default_factory=dict)

    def independent_contexts(self, derivation: str) -> Sequence[str]:
        return tuple(self.contexts.get(derivation, ()))


class TrialEventView(Protocol):
    """The feedback fields :func:`independence_from_events` reads.

    Structural on purpose: the feedback tier's event record already has exactly
    these attributes, so counting independence over a deployment's own trial
    stream needs no adapter and this module needs no import of it."""

    @property
    def kind(self) -> str: ...

    @property
    def subject_id(self) -> str: ...

    @property
    def episode_id(self) -> str: ...


USE_EVENT_KINDS: frozenset[str] = frozenset({"trial", "verdict"})
"""The event kinds that evidence a context USED the subject. A correction flag is
not a use, so raising one never inflates independence."""


def independence_from_events(
    events: Iterable[TrialEventView], subject_id: str
) -> tuple[str, ...]:
    """Distinct episodes that used ``subject_id`` — independence, as arithmetic.

    Episodes rather than sources, which is the weaker reading
    :data:`INDEPENDENCE_DEVIATION` records. Sorted, so the count and its report
    are both deterministic."""
    return tuple(
        sorted(
            {
                event.episode_id
                for event in events
                if event.subject_id == subject_id and event.kind in USE_EVENT_KINDS
            }
        )
    )


# ── the promotion record: this gate's handle on a promoted claim ────────────


@runtime_checkable
class PromotionRecordView(Protocol):
    """The promotion record, as the demotion gate reads it.

    A port rather than a type this module owns: the consolidation phase emits the
    record as a first-class effect, and the gate is its consumer. Every field
    here is a *handle* the gate needs — without ``status_at_promotion`` there is
    no flip to detect, without ``episode_ids`` no independence to compare, and
    without ``last_checked_at`` no schedule."""

    claim_id: str
    derivation_id: str
    text: str
    note_id: str
    locator: str | None
    status_at_promotion: str
    episode_ids: tuple[str, ...]
    occurrences: int
    promoted_at: float
    last_checked_at: float | None
    base_snapshot_id: str
    certificate: DeepUnderstandingCertificate | None


@dataclass(frozen=True)
class PromotedClaimRecord:
    """Deterministic reference :class:`PromotionRecordView`.

    Shipped so the gate is exercisable before consolidation exists, and so the
    fields the gate depends on are written down in one place the promotion phase
    can satisfy structurally."""

    claim_id: str
    derivation_id: str
    text: str
    note_id: str
    locator: str | None = None
    status_at_promotion: str = "warranted"
    episode_ids: tuple[str, ...] = ()
    occurrences: int = 0
    promoted_at: float = 0.0
    last_checked_at: float | None = None
    base_snapshot_id: str = ""
    certificate: DeepUnderstandingCertificate | None = None


# ── step 1 + 2: suppression, and the frozen model ──────────────────────────


def require_frozen(model: object) -> tuple[str, float]:
    """Return ``(model_id, frozen_at)`` for a pinned model, else refuse.

    Duck-typed rather than an ``isinstance`` check so a deployment can pin its
    own model however it already versions things; what is not negotiable is that
    a pin EXISTS. Wrap an unpinned model in :class:`FrozenReDerivationModel`."""
    model_id = str(getattr(model, "model_id", "") or "").strip()
    if not model_id:
        raise FrozenModelError(
            "the re-derivation model is not frozen: it carries no model_id. "
            "Wrap it in FrozenReDerivationModel(model, model_id=..., "
            "frozen_at=...) — an unpinned model can re-tune onto the corpus it "
            "is checking and regenerate a promoted claim from the promotion"
        )
    frozen_at = getattr(model, "frozen_at", None)
    if frozen_at is None:
        raise FrozenModelError(
            f"the re-derivation model {model_id!r} carries no frozen_at pin"
        )
    return model_id, float(frozen_at)


def require_suppression(
    claim_text: str, *, question: str, sources: Sequence[CitedSource]
) -> None:
    """Refuse a request that shows the model the claim it is meant to regenerate.

    Two leaks, both real and both cheap to make: putting the claim into the
    question ("does this span support: <claim>?"), and listing the claim's own
    rendering as one of its cited sources — abstraction citing itself, which
    would make every promoted claim regenerate forever.

    A source that *contains* the claim verbatim is fine and is not refused: a
    claim quoted from its own note is exactly what grounding looks like. Only an
    exact normalised match is a self-citation."""
    normalized = normalize_span_text(claim_text)
    if not normalized:
        return
    if normalized in normalize_span_text(question):
        raise SuppressionError(
            "the promoted claim appears in the re-derivation question: the gate "
            "measures whether the claim REGENERATES, and a model shown the "
            "answer measures nothing"
        )
    for source in sources:
        if normalize_span_text(source.text) == normalized:
            raise SuppressionError(
                f"cited source {source.locator!r} is the promoted claim's own "
                "rendering: a claim may not be its own evidence"
            )


def build_request(
    record: PromotionRecordView,
    sources: Sequence[CitedSource],
    *,
    question: str = "",
) -> ReDerivationRequest:
    """Assemble the suppressed request. Refuses on a leak; no model call here."""
    require_suppression(record.text, question=question, sources=sources)
    return ReDerivationRequest(
        derivation_id=record.derivation_id,
        note_id=record.note_id,
        sources=tuple(sources),
        question=question,
    )


# ── step 3: the comparison, which stays arithmetic ─────────────────────────


_TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)


def tokenize(text: str) -> frozenset[str]:
    """The token set :func:`agreement` compares — normalised, punctuation dropped.

    Punctuation is dropped because ``days.`` and ``days`` are the same word and a
    sentence-final period is not a disagreement. A SET rather than a multiset:
    repeating a word is emphasis, not evidence."""
    return frozenset(_TOKEN_RE.findall(normalize_span_text(text)))


def agreement(left: str, right: str) -> float:
    """Symmetric token overlap in ``[0, 1]`` — the comparison, as arithmetic.

    The Dice coefficient ``2|a ∩ b| / (|a| + |b|)`` over normalised token sets:
    deterministic, explainable to whoever the demotion affects, and recomputable
    years later. Dice rather than Jaccard because Jaccard charges a regeneration
    twice for saying the same thing at greater length, and a re-derivation that
    adds context is not a re-derivation that failed.

    Two empty strings agree — there is nothing to disagree about; one empty string
    agrees with nothing. See :data:`REGENERATION_COMPARISON_DEVIATION` for what
    this proxy cannot do, and expect a deployment to re-fit
    :attr:`DemotionPolicy.regeneration_floor` on its own corpus."""
    a, b = tokenize(left), tokenize(right)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return 2 * len(a & b) / (len(a) + len(b))


@dataclass(frozen=True)
class RegenerationCheck:
    """Trigger 1: did the claim come back out of its own sources?

    ``exact`` is normalised-text equality and ``score`` the overlap ratio;
    ``regenerated`` is the gate's answer and it is a pure comparison against a
    floor. ``model_id`` / ``frozen_at`` travel with the finding so a demotion
    names the model that produced it."""

    regenerated: bool
    exact: bool
    score: float
    floor: float
    abstained: bool
    regenerated_text: str
    model_id: str
    frozen_at: float
    source_count: int
    reason: str

    @property
    def failed(self) -> bool:
        return not self.regenerated


def check_regeneration(
    record: PromotionRecordView,
    *,
    model: ReDerivationModel,
    sources: Sequence[CitedSource],
    floor: float = REGENERATION_FLOOR,
    question: str = "",
) -> RegenerationCheck:
    """Run the three-step protocol for one claim and compare arithmetically.

    Suppress (:func:`build_request`), require the pin (:func:`require_frozen`),
    call the injected model exactly once, then decide with :func:`agreement`. No
    cited sources at all is a failure without a model call: there is nothing to
    regenerate from, and calling a model to confirm that would only add cost and
    variance."""
    model_id, frozen_at = require_frozen(model)
    if not sources:
        return RegenerationCheck(
            regenerated=False,
            exact=False,
            score=0.0,
            floor=floor,
            abstained=False,
            regenerated_text="",
            model_id=model_id,
            frozen_at=frozen_at,
            source_count=0,
            reason="the promoted claim cites no sources, so it cannot regenerate",
        )
    request = build_request(record, sources, question=question)
    output = model.re_derive(request)
    if output.abstained:
        return RegenerationCheck(
            regenerated=False,
            exact=False,
            score=0.0,
            floor=floor,
            abstained=True,
            regenerated_text=output.text,
            model_id=model_id,
            frozen_at=frozen_at,
            source_count=len(request.sources),
            reason=(
                "the frozen model abstained from the cited sources"
                + (f": {output.detail}" if output.detail else "")
            ),
        )
    score = agreement(record.text, output.text)
    exact = normalize_span_text(record.text) == normalize_span_text(output.text)
    regenerated = exact or score >= floor
    return RegenerationCheck(
        regenerated=regenerated,
        exact=exact,
        score=score,
        floor=floor,
        abstained=False,
        regenerated_text=output.text,
        model_id=model_id,
        frozen_at=frozen_at,
        source_count=len(request.sources),
        reason=(
            f"regeneration agreement {score:.3f} "
            f"{'>=' if regenerated else '<'} floor {floor:.3f}"
        ),
    )


# ── triggers 2 and 3, both arithmetic ──────────────────────────────────────


@dataclass(frozen=True)
class StatusFlipCheck:
    """Trigger 2: is the claim still answerable?

    Nearly free, and that is a property of the design rather than luck: status is
    a pure function of the edge set, so one appended attack changes it and this
    check is a comparison of two labels. ``improved`` marks the benign direction
    — a claim that gained support is not a contradiction — so a caller can see
    that the gate looked and declined to fire."""

    flipped: bool
    improved: bool
    status_at_promotion: str
    status_now: str
    reason: str


def check_status_flip(
    record: PromotionRecordView, statuses: CurrentStatusSource
) -> StatusFlipCheck:
    """Compare the promoted status with the computed one now. Model-free."""
    now = statuses.status_of(record.claim_id)
    was_answerable = record.status_at_promotion in ANSWERABLE_STATUSES
    is_answerable = now in ANSWERABLE_STATUSES
    flipped = was_answerable and not is_answerable
    improved = is_answerable and not was_answerable
    if flipped:
        reason = (
            f"status flipped out of answerable: {record.status_at_promotion} → {now}"
        )
    elif improved:
        reason = f"status improved: {record.status_at_promotion} → {now}"
    else:
        reason = f"status unchanged for answering: {record.status_at_promotion} → {now}"
    return StatusFlipCheck(
        flipped=flipped,
        improved=improved,
        status_at_promotion=record.status_at_promotion,
        status_now=now,
        reason=reason,
    )


@dataclass(frozen=True)
class IndependenceCheck:
    """Trigger 3: do enough independent contexts still stand behind the claim?

    ``contexts`` is reported, not just ``count``, because "which context went
    away" is the first thing anybody asks about this demotion — and because a
    count alone cannot distinguish a withdrawn context from an arithmetic
    change."""

    below_floor: bool
    count: int
    floor: int
    contexts: tuple[str, ...]
    at_promotion: int
    reason: str


def check_independence(
    record: PromotionRecordView,
    source: IndependenceSource,
    *,
    floor: int = INDEPENDENCE_FLOOR,
) -> IndependenceCheck:
    """Count the contexts standing behind the claim now, against the floor.

    Counted over EPISODES — see :data:`INDEPENDENCE_DEVIATION`. Model-free."""
    contexts = tuple(sorted(set(source.independent_contexts(record.derivation_id))))
    count = len(contexts)
    below = count < floor
    return IndependenceCheck(
        below_floor=below,
        count=count,
        floor=floor,
        contexts=contexts,
        at_promotion=len(set(record.episode_ids)),
        reason=(
            f"{count} independent context(s) "
            f"{'<' if below else '>='} floor {floor} "
            f"(was {len(set(record.episode_ids))} at promotion)"
        ),
    )


# ── the policy and the schedule ────────────────────────────────────────────


@dataclass(frozen=True)
class DemotionPolicy:
    """The gate's arithmetic and its trigger → action mapping.

    Each default action is a judgement about what the finding means, and each is
    stated rather than tuned:

    * a **re-derivation failure** flags — the claim no longer follows from its
      own sources, so the conflict must surface, but a model's inability to
      restate a claim is not by itself a refutation of it;
    * a **contradiction** supersedes with a timestamp — something in the corpus
      now defeats it, and a claim the log itself contradicts must stop answering;
    * **independence below floor** down-ranks — the claim was not contradicted,
      its evidence base thinned, so it keeps answering and sorts last.
    """

    regeneration_floor: float = REGENERATION_FLOOR
    independence_floor: int = INDEPENDENCE_FLOOR
    interval_days: float = DEFAULT_INTERVAL_DAYS
    action_on_rederivation_failure: DemotionAction = "flag"
    action_on_contradiction: DemotionAction = "supersede_with_timestamp"
    action_on_independence_below_floor: DemotionAction = "down_rank"

    def action_for(self, trigger: str) -> DemotionAction:
        if trigger == TRIGGER_REDERIVATION_FAILURE:
            return self.action_on_rederivation_failure
        if trigger == TRIGGER_CONTRADICTION:
            return self.action_on_contradiction
        if trigger == TRIGGER_INDEPENDENCE_BELOW_FLOOR:
            return self.action_on_independence_below_floor
        raise ValueError(f"unknown demotion trigger: {trigger!r}")


DEFAULT_DEMOTION_POLICY: DemotionPolicy = DemotionPolicy()
"""Flag on failure, supersede on contradiction, down-rank on thin independence."""


def strongest_action(actions: Iterable[str]) -> DemotionAction | None:
    """The severest of several actions, or ``None`` for none at all."""
    ranked = sorted(actions)
    for action in ranked:
        if action not in ACTIONS:
            raise ValueError(f"unknown demotion action: {action!r}")
    ranked.sort(key=lambda action: -ACTION_SEVERITY[action])
    if not ranked:
        return None
    return ranked[0]  # type: ignore[return-value]


def due_at(
    record: PromotionRecordView, *, policy: DemotionPolicy = DEFAULT_DEMOTION_POLICY
) -> float:
    """When this claim's next re-derivation is due.

    Measured from the last check, or from promotion when there has never been
    one — a claim promoted and never re-derived is due one interval later, not
    exempt."""
    since = record.promoted_at if record.last_checked_at is None else record.last_checked_at
    return since + policy.interval_days * SECONDS_PER_DAY


def is_due(
    record: PromotionRecordView,
    now: float,
    *,
    policy: DemotionPolicy = DEFAULT_DEMOTION_POLICY,
) -> bool:
    return now >= due_at(record, policy=policy)


def due_records(
    records: Iterable[PromotionRecordView],
    now: float,
    *,
    policy: DemotionPolicy = DEFAULT_DEMOTION_POLICY,
) -> tuple[PromotionRecordView, ...]:
    """The scheduled batch: every promoted claim whose check has come due."""
    return tuple(
        record for record in records if is_due(record, now, policy=policy)
    )


def require_armed(
    records: Iterable[PromotionRecordView],
    now: float,
    *,
    policy: DemotionPolicy = DEFAULT_DEMOTION_POLICY,
    grace_days: float = 0.0,
) -> None:
    """Refuse to proceed while any promoted claim is overdue for re-derivation.

    This is what makes the gate *required* rather than available: a promotion
    path calls this first, and an un-run gate is an error instead of a silence
    that flatters everything already promoted. ``grace_days`` exists so a
    deployment can tolerate a late batch explicitly, which is different from
    tolerating it by default."""
    slack = grace_days * SECONDS_PER_DAY
    overdue = sorted(
        record.claim_id
        for record in records
        if now >= due_at(record, policy=policy) + slack
    )
    if overdue:
        raise GateNotArmedError(
            f"{len(overdue)} promoted claim(s) overdue for the re-derivation "
            f"gate ({', '.join(overdue[:3])}"
            f"{', …' if len(overdue) > 3 else ''}). The gate is required and "
            "scheduled: run it before promoting anything further"
        )


# ── the review, and the retraction it appends ──────────────────────────────


def _timestamp(at: float) -> str:
    """A stable rendering of a check time for the retraction's own text."""
    return f"{at:.3f}"


def _content_id(prefix: str, *parts: str) -> str:
    """The content-id construction ``capability._replay_token`` uses.

    Duplicated rather than imported for the reason
    :mod:`~tessellum.dks.claim_identity` duplicates it: the prefix belongs to the
    caller's contract, the NUL-terminated digest is what has to match."""
    h = hashlib.sha256()
    for part in parts:
        h.update(part.encode("utf-8"))
        h.update(b"\0")
    return prefix + h.hexdigest()[:32]


@dataclass(frozen=True)
class DemotionReview:
    """One claim's re-derivation review — the whole finding, nothing applied.

    Every check is reported whether or not it fired, so a review that demotes
    nothing is still evidence the gate ran. ``effects`` are *proposed*: the
    retraction reaches the log through the commit tail, and this object touches
    nothing.
    """

    claim_id: str
    derivation_id: str
    checked_at: float
    regeneration: RegenerationCheck
    status_flip: StatusFlipCheck
    independence: IndependenceCheck
    triggers: tuple[str, ...] = ()
    action: DemotionAction | None = None
    proposals: tuple[Proposal, ...] = ()
    effects: tuple[CapabilityEffect, ...] = ()
    retraction_claim_id: str = ""
    revoked_certificate: DeepUnderstandingCertificate | None = None
    reasons: tuple[str, ...] = ()

    @property
    def demoted(self) -> bool:
        return bool(self.triggers)

    @property
    def retracted(self) -> bool:
        """``True`` when the demotion appended a retraction to the log.

        A ``down_rank`` demotes standing without appending an epistemic act, so
        it is a demotion that is not a retraction — the distinction matters to a
        reader deciding whether the claim still answers."""
        return bool(self.proposals)

    @property
    def promotion_eligibility(self) -> PromotionEligibility:
        """The verdict in the vocabulary that already exists, not a parallel one.

        ``ineligible`` once any trigger fired. Otherwise ``eligible`` in the sense
        the contract defines — *"structurally sound; may proceed to gated
        promotion"* — which is emphatically not a promotion: this gate is one
        condition, and recurrence, reliability, stability, entailment and dedup
        are all still ahead of the claim."""
        return "ineligible" if self.demoted else "eligible"


def retraction_proposals(
    record: PromotionRecordView,
    *,
    action: DemotionAction,
    triggers: Sequence[str],
    at: float,
    reasons: Sequence[str] = (),
) -> tuple[Proposal, ...]:
    """Render a demotion as an APPEND: a retraction claim plus one edge.

    ``flag`` appends an ``attack`` (the claim becomes ``challenged``);
    ``supersede_with_timestamp`` appends a ``supersede`` and carries the check
    time in the retraction claim's own text, so the timestamp is in the log
    rather than in a mutable column. ``down_rank`` appends **nothing** and
    returns ``()``: standing is a projection, and demoting a projection is not an
    epistemic act.

    The retraction's derivation is keyed on the retracted claim under
    :data:`RETRACTION_SECTION`, so re-running the gate at the same check time
    replays onto the same rows, while a later check re-renders the same
    derivation — a retraction revises rather than multiplies.
    """
    if action not in ACTIONS:
        raise ValueError(f"unknown demotion action: {action!r}")
    if action == "down_rank":
        return ()
    operator = "supersede" if action == "supersede_with_timestamp" else "attack"
    locator = record.locator or f"claim:{record.claim_id}"
    detail = "; ".join(reasons) if reasons else ", ".join(triggers)
    retraction = ClaimProposal(
        derivation_id=derivation_id(
            record.note_id,
            anchor_locator(
                f"retraction:{record.claim_id}", section=RETRACTION_SECTION
            ),
        ),
        text=(
            f"The promoted claim {record.claim_id} is retracted as of "
            f"t={_timestamp(at)} by the re-derivation gate "
            f"({', '.join(triggers)}): {detail}."
        ),
        note_id=record.note_id,
        locator=locator,
        provenance="constructed",
        operator=operator,
        bb_role="retraction",
    )
    return (
        retraction,
        EdgeProposal(
            op=operator,
            src=retraction.claim_id,
            dst=record.claim_id,
            origin=ORIGIN_DEMOTION,
            evidence_locator=locator,
        ),
    )


class ReDerivationGate:
    """The scheduled gate: three triggers, one review per promoted claim.

    All four collaborators are required. A gate missing one of them would be a
    gate with two of three triggers, and there is no default that makes an
    unchecked trigger safe — an absent status source cannot mean "still
    warranted", and an absent independence source cannot mean "still
    independent".

    Args:
        model: the injected re-derivation model, which must be pinned (see
            :func:`require_frozen`).
        sources: read port over each promoted claim's cited sources.
        statuses: read port over the computed status now.
        independence: read port over the contexts standing behind the claim now.
        policy: the arithmetic and the trigger → action mapping.
    """

    def __init__(
        self,
        *,
        model: ReDerivationModel,
        sources: SourceReader,
        statuses: CurrentStatusSource,
        independence: IndependenceSource,
        policy: DemotionPolicy = DEFAULT_DEMOTION_POLICY,
    ) -> None:
        require_frozen(model)
        self._model = model
        self._sources = sources
        self._statuses = statuses
        self._independence = independence
        self._policy = policy

    @property
    def policy(self) -> DemotionPolicy:
        return self._policy

    def review(
        self,
        record: PromotionRecordView,
        *,
        now: float,
        question: str = "",
    ) -> DemotionReview:
        """Run all three triggers over one promoted claim. Writes nothing.

        Every trigger runs even when an earlier one fired: a demotion should
        report every reason it happened, and re-running the gate to discover the
        second reason would cost another model call for information already
        available."""
        regeneration = check_regeneration(
            record,
            model=self._model,
            sources=self._sources.cited_sources(record.claim_id),
            floor=self._policy.regeneration_floor,
            question=question,
        )
        flip = check_status_flip(record, self._statuses)
        independence = check_independence(
            record, self._independence, floor=self._policy.independence_floor
        )

        triggers: list[str] = []
        reasons: list[str] = []
        if regeneration.failed:
            triggers.append(TRIGGER_REDERIVATION_FAILURE)
            reasons.append(f"{TRIGGER_REDERIVATION_FAILURE}: {regeneration.reason}")
        if flip.flipped:
            triggers.append(TRIGGER_CONTRADICTION)
            reasons.append(f"{TRIGGER_CONTRADICTION}: {flip.reason}")
        if independence.below_floor:
            triggers.append(TRIGGER_INDEPENDENCE_BELOW_FLOOR)
            reasons.append(
                f"{TRIGGER_INDEPENDENCE_BELOW_FLOOR}: {independence.reason}"
            )

        action = strongest_action(
            self._policy.action_for(trigger) for trigger in triggers
        )
        proposals: tuple[Proposal, ...] = ()
        if action is not None:
            proposals = retraction_proposals(
                record, action=action, triggers=triggers, at=now, reasons=reasons
            )
        revoked = None
        if triggers and record.certificate is not None:
            revoked = revoke(
                record.certificate,
                reason="; ".join(reasons),
                at=now,
            )
        return DemotionReview(
            claim_id=record.claim_id,
            derivation_id=record.derivation_id,
            checked_at=now,
            regeneration=regeneration,
            status_flip=flip,
            independence=independence,
            triggers=tuple(triggers),
            action=action,
            proposals=proposals,
            effects=tuple(effect_for_proposal(p) for p in proposals),
            retraction_claim_id=(
                proposals[0].claim_id
                if proposals and isinstance(proposals[0], ClaimProposal)
                else ""
            ),
            revoked_certificate=revoked,
            reasons=tuple(reasons),
        )

    def sweep(
        self,
        records: Iterable[PromotionRecordView],
        *,
        now: float,
        ledger: "DemotionLedger | None" = None,
        force: bool = False,
        question: str = "",
    ) -> "DemotionSweep":
        """The scheduled pass: review every claim that is due, append the ledger.

        Claims not yet due are skipped and named, so a sweep reports its own
        coverage. A claim the ledger already shows demoted is skipped too —
        demoting it again would append a second retraction of the same act — and
        ``force`` re-checks everything, which is what a caller re-running after a
        recovery wants.
        """
        history = ledger or DemotionLedger()
        reviews: list[DemotionReview] = []
        skipped: list[str] = []
        already: list[str] = []
        for record in records:
            if not force and history.is_demoted(record.claim_id):
                already.append(record.claim_id)
                continue
            if not force and not is_due(record, now, policy=self._policy):
                skipped.append(record.claim_id)
                continue
            reviews.append(self.review(record, now=now, question=question))
        entries = tuple(
            entry_for_review(review) for review in reviews if review.demoted
        )
        return DemotionSweep(
            checked_at=now,
            reviews=tuple(reviews),
            skipped_not_due=tuple(sorted(skipped)),
            skipped_already_demoted=tuple(sorted(already)),
            ledger=history.record(*entries),
        )


@dataclass(frozen=True)
class DemotionSweep:
    """One scheduled pass over the promoted claims.

    ``ledger`` is the NEW ledger — the one handed in is unchanged, which is how
    an append-only history survives a sweep that demotes half the corpus."""

    checked_at: float
    reviews: tuple[DemotionReview, ...]
    ledger: "DemotionLedger"
    skipped_not_due: tuple[str, ...] = ()
    skipped_already_demoted: tuple[str, ...] = ()

    @property
    def demoted(self) -> tuple[str, ...]:
        return tuple(
            sorted(review.claim_id for review in self.reviews if review.demoted)
        )

    @property
    def effects(self) -> tuple[CapabilityEffect, ...]:
        """Every proposed retraction effect, claims before edges within a review."""
        return tuple(effect for review in self.reviews for effect in review.effects)

    def by_trigger(self) -> dict[str, tuple[str, ...]]:
        """Which claims each trigger fired on — the sweep's own report."""
        out: dict[str, list[str]] = {trigger: [] for trigger in sorted(TRIGGERS)}
        for review in self.reviews:
            for trigger in review.triggers:
                out[trigger].append(review.claim_id)
        return {trigger: tuple(sorted(ids)) for trigger, ids in out.items()}


# ── the ledger: append-only, and the only thing a recovery reads ───────────

LedgerEntryKind = Literal["demotion", "recovery"]


@dataclass(frozen=True)
class DemotionEntry:
    """One immutable row of the demotion history — a demotion or a recovery.

    Both kinds share one ordered sequence rather than living in two tables,
    because "is this claim demoted right now" is a question about the LATEST act
    and answering it from two sequences invites the two to disagree."""

    kind: LedgerEntryKind
    claim_id: str
    derivation_id: str
    at: float
    triggers: tuple[str, ...] = ()
    action: DemotionAction | None = None
    retraction_claim_id: str = ""
    validator: str = ""
    reasons: tuple[str, ...] = ()
    detail: str = ""

    @property
    def entry_id(self) -> str:
        """Content address — a replayed sweep records the same row once."""
        return _content_id(
            "demotion:",
            self.kind,
            self.claim_id,
            self.derivation_id,
            _timestamp(self.at),
            "|".join(self.triggers),
            self.action or "",
            self.retraction_claim_id,
            self.validator,
        )


def entry_for_review(review: DemotionReview) -> DemotionEntry:
    """The ledger row for a demoting review."""
    if not review.demoted:
        raise ValueError(
            f"review of {review.claim_id} demoted nothing; there is no entry to "
            "record (a passing review is reported, not logged as a demotion)"
        )
    return DemotionEntry(
        kind="demotion",
        claim_id=review.claim_id,
        derivation_id=review.derivation_id,
        at=review.checked_at,
        triggers=review.triggers,
        action=review.action,
        retraction_claim_id=review.retraction_claim_id,
        reasons=review.reasons,
    )


@dataclass(frozen=True)
class DemotionLedger:
    """The demotion history — **append-only**, and never a delete.

    :meth:`record` returns a NEW ledger rather than mutating this one, so every
    earlier state of the history is still a live object and "history survives the
    demotion" is a property of the type instead of a discipline. There is no
    method that removes an entry, and a recovery is an appended entry rather than
    the erasure of one: a claim that was wrongly demoted has a demotion in its
    history forever, and that is the honest record."""

    entries: tuple[DemotionEntry, ...] = ()

    def record(self, *entries: DemotionEntry) -> "DemotionLedger":
        """Append entries, skipping any whose content id is already present.

        Content-addressed, so a replayed sweep is a no-op the same way a replayed
        append is — a retried batch must not read as a second demotion."""
        known = {entry.entry_id for entry in self.entries}
        fresh: list[DemotionEntry] = []
        for entry in entries:
            if entry.entry_id in known:
                continue
            known.add(entry.entry_id)
            fresh.append(entry)
        if not fresh:
            return self
        return DemotionLedger(entries=self.entries + tuple(fresh))

    def history_for(self, claim_id: str) -> tuple[DemotionEntry, ...]:
        """Every act about one claim, in the order they were recorded."""
        return tuple(entry for entry in self.entries if entry.claim_id == claim_id)

    def latest(self, claim_id: str) -> DemotionEntry | None:
        history = self.history_for(claim_id)
        return history[-1] if history else None

    def is_demoted(self, claim_id: str) -> bool:
        """Whether the claim's most recent act was a demotion."""
        latest = self.latest(claim_id)
        return latest is not None and latest.kind == "demotion"

    def demoted_claim_ids(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                {
                    entry.claim_id
                    for entry in self.entries
                    if self.is_demoted(entry.claim_id)
                }
            )
        )

    def __len__(self) -> int:
        return len(self.entries)


# ── the recovery path ──────────────────────────────────────────────────────


@dataclass(frozen=True)
class RecoveryOutcome:
    """A wrongly-demoted claim restored — by appending, and by a judge.

    ``promotion_eligibility`` is ``needs_validation`` rather than ``eligible``:
    the claim is out of the penalty box, but a claim that has been demoted once
    re-enters the gate rather than skipping it."""

    claim_id: str
    recovered_at: float
    validator: str
    certificate: DeepUnderstandingCertificate
    entry: DemotionEntry
    ledger: DemotionLedger
    proposals: tuple[Proposal, ...] = ()
    effects: tuple[CapabilityEffect, ...] = ()
    reasons: tuple[str, ...] = ()

    @property
    def promotion_eligibility(self) -> PromotionEligibility:
        return "needs_validation"


def recovery_proposals(
    record: PromotionRecordView,
    *,
    retraction_claim_id: str,
    validator: str,
    at: float,
    detail: str = "",
) -> tuple[Proposal, ...]:
    """Discharge a retraction by APPENDING an attack on it.

    Not by deleting the retraction, and not by rewriting a status: the retraction
    claim is attacked, the fixed point labels it ``out``, and the original claim
    is reinstated — a ``supersede`` from an ``out`` claim stops counting in the
    pre-filter, and an ``attack`` from one stops defeating. The reinstatement is
    the labelling's doing, which is exactly why nothing had to be mutated."""
    locator = record.locator or f"claim:{record.claim_id}"
    recovery = ClaimProposal(
        derivation_id=derivation_id(
            record.note_id,
            anchor_locator(
                f"recovery:{retraction_claim_id}", section=RECOVERY_SECTION
            ),
        ),
        text=(
            f"The retraction {retraction_claim_id} of claim {record.claim_id} was "
            f"in error and is discharged as of t={_timestamp(at)} on the "
            f"attestation of validator {validator}"
            f"{f': {detail}' if detail else ''}."
        ),
        note_id=record.note_id,
        locator=locator,
        provenance="constructed",
        operator="attack",
        bb_role="recovery",
    )
    return (
        recovery,
        EdgeProposal(
            op="attack",
            src=recovery.claim_id,
            dst=retraction_claim_id,
            origin=ORIGIN_RECOVERY,
            evidence_locator=locator,
        ),
    )


def recover(
    record: PromotionRecordView,
    *,
    ledger: DemotionLedger,
    profile: MaturityProfile,
    validator_id: str,
    reasoning_backend_id: str,
    at: float,
    detail: str = "",
) -> RecoveryOutcome:
    """Restore a wrongly-demoted claim — history intact, and not self-service.

    Three properties, in the order they are enforced:

    1. **There must be a demotion to reverse.** Recovering a claim the ledger
       does not show demoted is refused, because it would mint an attestation
       nobody asked for.
    2. **A judge, not the mover.**
       :func:`~tessellum.dks.elevation.issue_certificate` refuses the reasoning
       backend its own certificate and refuses an immature profile, so a claim
       cannot talk itself back in.
    3. **Restoration is an append.** The retraction is discharged by an attack on
       it (:func:`recovery_proposals`) and the demotion entry stays in the
       ledger forever; the returned ledger is longer, never shorter.

    Raises:
        RecoveryError: the ledger shows no active demotion for this claim.
        ~tessellum.dks.elevation.CertificateError: the issuer is the reasoning
            backend, or the profile is not mature enough.
    """
    latest = ledger.latest(record.claim_id)
    if latest is None or latest.kind != "demotion":
        raise RecoveryError(
            f"{record.claim_id} has no active demotion to recover from "
            f"(latest ledger act: {latest.kind if latest else 'none'})"
        )
    certificate = issue_certificate(
        record.derivation_id,
        profile,
        issuer=validator_id,
        reasoning_backend_id=reasoning_backend_id,
        invalidation_triggers=tuple(sorted(TRIGGERS)),
    )
    proposals: tuple[Proposal, ...] = ()
    if latest.retraction_claim_id:
        proposals = recovery_proposals(
            record,
            retraction_claim_id=latest.retraction_claim_id,
            validator=validator_id,
            at=at,
            detail=detail,
        )
    reasons = (
        f"recovery of {latest.action or 'demotion'} "
        f"({', '.join(latest.triggers) or 'unrecorded'}) attested by "
        f"{validator_id}",
    )
    entry = DemotionEntry(
        kind="recovery",
        claim_id=record.claim_id,
        derivation_id=record.derivation_id,
        at=at,
        retraction_claim_id=latest.retraction_claim_id,
        validator=validator_id,
        reasons=reasons,
        detail=detail,
    )
    return RecoveryOutcome(
        claim_id=record.claim_id,
        recovered_at=at,
        validator=validator_id,
        certificate=certificate,
        entry=entry,
        ledger=ledger.record(entry),
        proposals=proposals,
        effects=tuple(effect_for_proposal(p) for p in proposals),
        reasons=reasons,
    )


# ── down-ranking: the mildest action, wired to the move ranker ─────────────


def down_rank_order(
    candidates: Mapping[str, RewardInputs],
    *,
    ledger: DemotionLedger,
    ranker: MoveRanker | None = None,
) -> list[str]:
    """Order candidate claims with the demoted ones last.

    The down-rank action, realised through the existing frozen-snapshot reward
    (:class:`~tessellum.dks.elevation.MoveRanker`) rather than a second scoring
    scheme: a demoted claim is marked un-validated, its reward is therefore
    ``0.0`` by construction, and it sorts behind everything still standing. The
    ranker only ORDERS — it is never the commit authority and never a
    certificate — so down-ranking removes nothing and can be undone by a
    recovery that changes the ledger."""
    demoted = set(ledger.demoted_claim_ids())
    adjusted = {
        claim_id: (
            replace(inputs, validated=False) if claim_id in demoted else inputs
        )
        for claim_id, inputs in candidates.items()
    }
    return (ranker or MoveRanker()).order(adjusted)


# ── the envelope: a demotion rides out as effects, not as a write ──────────


def as_capability_result(review: DemotionReview) -> CapabilityResult:
    """Wrap a review in the existing envelope — no second result type.

    The retraction leaves as ``effects`` for the commit tail to render, and
    ``promotion_eligibility`` carries the verdict in the vocabulary that already
    exists. ``warrant`` is ``None`` because a demotion licenses no conclusion: it
    withdraws one."""
    return CapabilityResult(
        status="ok" if review.demoted else "empty",
        effects=review.effects,
        diagnostics=review.reasons,
        promotion_eligibility=review.promotion_eligibility,
        warrant=None,
        qualifier=(
            f"demoted by {', '.join(review.triggers)} "
            f"(action: {review.action})"
            if review.demoted
            else "re-derivation gate passed; no trigger fired"
        ),
        replay_token=_content_id(
            "dks:",
            "demotion",
            review.claim_id,
            review.derivation_id,
            _timestamp(review.checked_at),
            "|".join(review.triggers),
            review.action or "",
        ),
        payload=review,
    )


def recovery_capability_result(outcome: RecoveryOutcome) -> CapabilityResult:
    """The same envelope for a recovery — an append, and ``needs_validation``."""
    return CapabilityResult(
        status="ok",
        effects=outcome.effects,
        diagnostics=outcome.reasons,
        promotion_eligibility=outcome.promotion_eligibility,
        warrant=None,
        qualifier=(
            f"recovered on the attestation of {outcome.validator}; the claim "
            "re-enters the gate rather than skipping it"
        ),
        replay_token=_content_id(
            "dks:",
            "recovery",
            outcome.claim_id,
            outcome.validator,
            _timestamp(outcome.recovered_at),
        ),
        payload=outcome,
    )


__all__ = [
    "ACTIONS",
    "ACTION_SEVERITY",
    "ANSWERABLE_STATUSES",
    "CitedSource",
    "CurrentStatusSource",
    "DEFAULT_DEMOTION_POLICY",
    "DEFAULT_INTERVAL_DAYS",
    "DemotionAction",
    "DemotionEntry",
    "DemotionError",
    "DemotionLedger",
    "DemotionPolicy",
    "DemotionReview",
    "DemotionSweep",
    "DemotionTrigger",
    "FrozenModelError",
    "FrozenReDerivationModel",
    "GateNotArmedError",
    "INDEPENDENCE_DEVIATION",
    "INDEPENDENCE_FLOOR",
    "IndependenceCheck",
    "IndependenceSource",
    "LedgerEntryKind",
    "ORIGIN_DEMOTION",
    "ORIGIN_RECOVERY",
    "PromotedClaimRecord",
    "PromotionRecordView",
    "REGENERATION_COMPARISON_DEVIATION",
    "REGENERATION_FLOOR",
    "RECOVERY_SECTION",
    "RETRACTION_SECTION",
    "ReDerivationGate",
    "ReDerivationModel",
    "ReDerivationOutput",
    "ReDerivationRequest",
    "RecoveryError",
    "RecoveryOutcome",
    "RegenerationCheck",
    "SECONDS_PER_DAY",
    "STATUS_UNKNOWN",
    "ScriptedReDerivationModel",
    "SourceReader",
    "StaticIndependenceSource",
    "StaticSourceReader",
    "StaticStatusSource",
    "StatusFlipCheck",
    "SuppressionError",
    "TRIGGERS",
    "TRIGGER_CONTRADICTION",
    "TRIGGER_INDEPENDENCE_BELOW_FLOOR",
    "TRIGGER_REDERIVATION_FAILURE",
    "TrialEventView",
    "USE_EVENT_KINDS",
    "VerdictQuery",
    "VerdictQueryStatusSource",
    "agreement",
    "as_capability_result",
    "build_request",
    "check_independence",
    "check_regeneration",
    "check_status_flip",
    "down_rank_order",
    "due_at",
    "due_records",
    "entry_for_review",
    "independence_from_events",
    "is_due",
    "recover",
    "recovery_capability_result",
    "recovery_proposals",
    "require_armed",
    "require_frozen",
    "require_suppression",
    "retraction_proposals",
    "strongest_action",
    "tokenize",
]
