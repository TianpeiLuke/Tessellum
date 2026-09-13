"""tessellum.dks.memory_port — the three-call protocol↔memory boundary.

P6 of the query-time-DKS plan. An ephemeral reasoning episode has to read and
write durable memory without corrupting it, and every *additional* way for a
reasoning step to write is another way for an unverified conclusion to become
permanent knowledge. So the boundary is deliberately narrow: **three calls**,
and committing is not a fourth because committing *is* appending.

===========================  ============  ==================================
Call                         Direction     Returns
===========================  ============  ==================================
``retrieve(query)``          read          candidate CLAIMS (+ Tier-A
                                           relations + the note-level hits)
``status`` / ``explain``     read          the computed label, and its
                                           support/attack chain with locators
``append_batch()``           **write**     the appended batch; the log grows
===========================  ============  ==================================

Four rules, and the last two are enforced here rather than requested:

1. **Append is the only write.** No status is ever written (statuses are
   computed) and nothing is mutated or deleted. The kernel does not even append
   directly: :meth:`EpisodeMemory.append_batch` emits
   :class:`~tessellum.dks.capability.CapabilityEffect` records and hands them to
   an injected :class:`LogAppendPort` the runtime backs.
2. **Nothing enters the log without a locator** — see the admission gate below.
3. **Status is read-only to the protocol.** It asks whether a claim is
   warranted; it does not get to declare it.
4. **Read at a snapshot, append at the end.** Every read in an episode resolves
   against ONE pinned edge-set digest, and staged records land in a single batch
   afterwards. Without the pin, a protocol that appended a proposal and re-read
   statuses would read *its own uncommitted proposal as evidence* and confirm
   itself. :meth:`EpisodeMemory.retrieve` and :meth:`EpisodeMemory.status` read
   only :attr:`EpisodeMemory.snapshot`, so that is structurally impossible.
   :meth:`EpisodeMemory.speculative_statuses` exists for consequence-checking
   and is labelled **non-citable** for exactly this reason.

   This is *not* snapshot isolation, which explicitly permits
   read-your-own-writes. It is a read-only snapshot plus a deferred batch
   commit. The guarantee is also **intra-episode only**: once the batch lands,
   the next episode's snapshot contains the agent's own claim, indistinguishable
   from third-party evidence. Closing that channel needs author identity on
   support edges or a no-circular-justification check, and neither is
   implemented anywhere yet.

**The admission gate — four conditions, in code.** A record crosses from
working memory into the log only with *(a)* an evidence locator and *(b)* an
operator label, and for a claim additionally *(c)* a provenance in the closed
set and *(d)* **claim-eligibility of its source note**. Condition (d) is the one
that earns its keep: a mechanically located string from a definition, a
procedure or an index is *evidence*, not a claim — measured on a real corpus,
roughly three quarters of statically located claim strings are not truth-apt as
written, and only about half of a vault's notes are claim-eligible at all.
Without (d) those strings enter the log and receive corpus-level verdicts, which
launders a document title into a verdict. See :class:`BuildingBlockEligibility`.

**The cache-READ path.** The read side previously stopped at note-level hits,
so nothing consulted memory before re-deriving and the memory tiers had no
measurable purpose. :meth:`EpisodeMemory.retrieve` composes over the read-only
note search (:class:`RetrievalNoteSearch`, a thin adapter — the retrieval client
is not modified) and returns, at the pinned snapshot: memoized **claims** with
their computed status, current **Tier-A relations** by subject, and the note
hits themselves. :meth:`EpisodeMemory.metrics` reports the Increment-1 numbers —
cache-hit rate and latency — so the tiers can be measured rather than assumed.

**Locator staleness.** Claims cite spans in notes that change, the status cache
invalidates on *append*, and a vault edit is not an append. Each claim is bound
to its cited note's content hash at derivation time (``source_note_hash``), and
:meth:`EpisodeMemory.detect_stale_claims` compares that against the current
hashes an index rebuild computed. :meth:`EpisodeMemory.stage_staleness_flags`
then stages the flag as an *append*: an undercutting ``attack`` from a
constructed flag claim, which moves the dependent claim to ``challenged`` and
therefore marks it as needing re-derivation. **This is DETECTION ONLY.**
Repairing stale claims at scale — incremental re-derivation over a base that
churns daily — is an acknowledged open engineering problem and is not solved
here, or anywhere else in this codebase.

Pure (the Dependency Rule): no ``runtime`` import, no disk, no vault write, and
no model call — every step above is a presence check, a lookup, graph arithmetic
or batching. Storage lives in ``runtime`` and is reached only through the ports
at the top of this module; the closed vocabularies are restated here because
``dks`` may not import the log module that mirrors them in a column CHECK.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from typing import (
    Callable,
    Iterable,
    Literal,
    Mapping,
    Protocol,
    Sequence,
    runtime_checkable,
)

from tessellum.bb.types import BBType
from tessellum.dks.capability import (
    CapabilityEffect,
    CapabilityResult,
    DKSCandidate,
    validate_effect_kind,
)
from tessellum.dks.claim_identity import anchor_locator, derivation_id
from tessellum.dks.dung import DungAF, grounded_labelling
from tessellum.dks.retrieval_client import RetrievalClient


class MemoryPortError(RuntimeError):
    """Raised when the boundary is asked to do something it must not do."""


class AdmissionError(MemoryPortError):
    """Raised by a strict :meth:`EpisodeMemory.append_batch` on a refusal.

    The default is record-level refusal (the batch appends what passed and
    reports what did not), because one un-admissible record should not cost an
    episode its whole memoization. ``strict=True`` turns the gate into a
    batch-level fail-closed check for callers that prefer it.
    """


# ── the closed vocabularies ─────────────────────────────────────────────────

Operator = Literal["support", "attack", "revise", "supersede"]
"""The only fixed relation vocabulary — four epistemic operators, no domain
predicates. Restated here rather than imported: the log module that mirrors it
in a column CHECK lives in ``runtime``, which ``dks`` may not import."""

OPERATORS: frozenset[str] = frozenset({"support", "attack", "revise", "supersede"})

Provenance = Literal["stub", "constructed"]
"""How a claim arrived: located mechanically, or stated after reading."""

PROVENANCES: frozenset[str] = frozenset({"stub", "constructed"})

ClaimStatus = Literal["proposed", "challenged", "warranted", "superseded"]
"""The four computed statuses. "Undecided" is deliberately absent: a live
unresolved dispute and a defeated claim have the same consequence for
answering, so both report as ``challenged``."""

STATUS_UNKNOWN: str = "unknown"
"""What :meth:`EpisodeMemory.status` reports for a claim the pinned snapshot
does not hold — including, by design, one the episode has merely staged."""

ORIGIN_STALENESS: str = "staleness"
"""``edges.origin`` for a locator-staleness undercut.

An addition to the origin vocabulary rather than a new operator: ``origin`` is a
free-text column with no CHECK precisely so a new *kind of act* can be recorded
without widening the four-operator set."""

STALENESS_SECTION: str = "staleness"
"""Locator section scoping a staleness flag's derivation, so a flag can never
collide with the claim it flags."""

CLAIM_ELIGIBLE_BLOCKS: frozenset[str] = frozenset(
    {
        BBType.ARGUMENT.value,
        BBType.COUNTER_ARGUMENT.value,
        BBType.HYPOTHESIS.value,
        BBType.EMPIRICAL_OBSERVATION.value,
        BBType.MODEL.value,
    }
)
"""Building blocks whose notes may be claim VERTICES — assertions and proposals.

``model`` belongs here even though it reads like a description: a design note
asserts "this is the right design" and is routinely attacked, so excluding
models would drop the most contested edges in a design trail."""

EVIDENCE_ONLY_BLOCKS: frozenset[str] = frozenset(
    {
        BBType.CONCEPT.value,
        BBType.PROCEDURE.value,
        BBType.NAVIGATION.value,
    }
)
"""Building blocks that are EVIDENCE, never claims. A definition, a procedure
and an index are things a locator points *into*; none of them is truth-apt, so
none of them may receive a corpus-level verdict."""

# ── admission reason codes ──────────────────────────────────────────────────

REASON_NO_LOCATOR: str = "no_evidence_locator"
REASON_NO_OPERATOR: str = "no_operator_label"
REASON_BAD_PROVENANCE: str = "provenance_not_in_closed_set"
REASON_NOT_CLAIM_ELIGIBLE: str = "source_note_not_claim_eligible"
REASON_ENDPOINT_REFUSED: str = "endpoint_claim_refused"
"""Not a fifth condition — the integrity consequence of one. An edge whose
endpoint claim was refused in the same batch would name a claim the log does not
hold, so it cannot be appended either."""


# ── content identity (mirrors the log's construction, deliberately) ─────────


def _content_id(*parts: str | None) -> str:
    """``sha256`` over NUL-joined parts — the log's 64-hex convention."""
    raw = "\0".join("" if part is None else part for part in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def text_content_hash(text: str) -> str:
    """``text_hash`` for a claim — a change here is a MATERIAL change."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def claim_content_id(derivation: str, text: str) -> str:
    """The log's content address for a claim: ``hash(derivation_id, text_hash)``.

    Duplicated from the runtime log on purpose. A content address has to be
    computed identically on both sides of the boundary — the protocol needs a
    staged claim's id *before* the append, so that a staged edge can name it —
    and ``dks`` may not import the log module. The duplication is pinned by a
    test that asserts the two constructions agree; if they ever diverge, staged
    edges would name ids the log never wrote and the foreign key would refuse
    the batch.
    """
    return _content_id(derivation, text_content_hash(text))


def edge_content_id(
    op: str, src: str, dst: str, evidence_locator: str | None = None
) -> str:
    """The log's content address for an operator edge — so replays dedup."""
    return _content_id(op, src, dst, evidence_locator)


def edgeset_digest(edges: Iterable["EdgeRow"]) -> str:
    """Digest of an edge SET, order-independent — the episode's snapshot pin.

    Reused as ``base_snapshot_id`` (see :meth:`EpisodeMemory.pinned_candidate`)
    rather than inventing a second pin: every append yields a new digest, so a
    result is bound to the exact edge set it was computed over and a stale
    reading is simply never read again.
    """
    return _content_id(*sorted(edge.edge_id for edge in edges))


# ── row shapes: structural, so a runtime record satisfies them as-is ────────


@runtime_checkable
class ClaimRow(Protocol):
    """One logged claim, as the boundary reads it.

    A Protocol rather than a mirrored dataclass: the runtime log's own record
    type already has exactly these attributes, so the read ports need no
    conversion layer and there is one less place for the two shapes to drift.
    """

    claim_id: str
    derivation_id: str
    text: str
    note_id: str
    locator: str | None
    provenance: str
    source_note_hash: str | None
    text_hash: str
    seq: int


@runtime_checkable
class EdgeRow(Protocol):
    """One logged operator edge, as the boundary reads it."""

    edge_id: str
    op: str
    src: str
    dst: str
    evidence_locator: str | None
    origin: str
    seq: int


@runtime_checkable
class RelationRow(Protocol):
    """One Tier-A ``relations`` row — a node-attached authored attribute.

    Read BY SUBJECT and never enumerated across pairs, which is what keeps this
    a cache rather than a typed-edge graph. ``valid_to`` and ``superseded_by``
    are load-bearing: a role-style relation without a validity interval
    confidently returns a *former* holder.
    """

    relation_id: str
    subject_id: str
    predicate: str
    object_ref: str
    valid_from: str | None
    valid_to: str | None
    evidence_note: str
    evidence_locator: str
    epistemic_status: str
    origin: str
    superseded_by: str | None


# ── ports: DKS reads and proposes; the runtime stores ───────────────────────


@runtime_checkable
class ClaimLogReader(Protocol):
    """Read port over the append-only claim/edge log. The runtime backs it.

    Deliberately the whole log rather than a query language: the snapshot is
    pinned once per episode, and a labelling is a function of the *whole* edge
    set, so a partial read would either be wrong or need a second consistency
    argument."""

    def read_claims(self) -> Sequence[ClaimRow]: ...

    def read_edges(self) -> Sequence[EdgeRow]: ...


@runtime_checkable
class RelationReader(Protocol):
    """Read port over the Tier-A relations cache, BY SUBJECT.

    The registry phase's ``RegistrySource`` already has this shape, so wiring
    Tier-A into the boundary needs no second adapter."""

    def relations_for(
        self, subject_id: str, predicate: str | None = None
    ) -> Sequence[RelationRow]: ...


@dataclass(frozen=True)
class NoteHit:
    """One note-level hit from the composed search seam.

    Mirrors the retrieval port's hit rather than re-exporting it, so the
    boundary's contract does not move when retrieval's does."""

    note_id: str
    note_name: str
    score: float
    snippet: str | None = None


class NoteSearch(Protocol):
    """Port for note-level search — ranked, best-first, read-only.

    Two shipped implementations mirror the pattern the resolver uses:
    :class:`MappingNoteSearch` (deterministic, for tests and for callers with no
    index) and :class:`RetrievalNoteSearch` (the real hybrid index, read through
    the existing read-only retrieval port)."""

    def __call__(self, query: str, *, k: int) -> Sequence[NoteHit]: ...


@dataclass(frozen=True)
class RetrievalNoteSearch:
    """Adapter over the read-only DKS retrieval port — the compose seam.

    The retrieval client returns note-level hits and nothing else; the boundary
    needs candidate *claims*. Rather than widening the client, this composes
    over its ``search`` and :meth:`EpisodeMemory.retrieve` joins the hits to the
    memoized claims at the pinned snapshot. The client has no
    ``index``/``update``/``delete`` surface, so no read path here can mutate the
    index."""

    client: RetrievalClient

    def __call__(self, query: str, *, k: int) -> Sequence[NoteHit]:
        return tuple(
            NoteHit(
                note_id=hit.note_id,
                note_name=hit.note_name,
                score=hit.score,
                snippet=getattr(hit, "snippet", None),
            )
            for hit in self.client.search(query, k=k)
        )


@dataclass(frozen=True)
class MappingNoteSearch:
    """Deterministic note search over a fixed ``query → hits`` mapping.

    Returns hits in the order given, truncated to ``k`` — no ranking of its own,
    so a test controls the seam's input exactly."""

    hits: Mapping[str, tuple[NoteHit, ...]] = field(default_factory=dict)

    def __call__(self, query: str, *, k: int) -> Sequence[NoteHit]:
        return self.hits.get(query, ())[:k]


@runtime_checkable
class ClaimEligibility(Protocol):
    """Port for condition (d) of the admission gate.

    A presence check, not a judgement: the source note's building block already
    records whether it asserts something. No model is needed or wanted here."""

    def is_claim_eligible(self, note_id: str) -> bool: ...


@dataclass(frozen=True)
class BuildingBlockEligibility:
    """Claim-eligibility by building block — deterministic and model-free.

    ``blocks`` maps a note id to its ``building_block``. A note whose block is
    in :data:`CLAIM_ELIGIBLE_BLOCKS` is a claim vertex; one in
    :data:`EVIDENCE_ONLY_BLOCKS` is evidence only. An **unknown** note is
    ineligible, which is the fail-closed reading: admitting a claim from a note
    whose type nobody could establish is how un-truth-apt strings get into the
    log in the first place.

    ``promoted`` is the one authored exception, and it is opt-in: an
    evidence-only note that an authored counter-argument attacks has been
    *contested*, and a contested note is a claim whether or not its block says
    so. Passing the promoted set explicitly keeps that a decision rather than a
    silent widening of the gate.
    """

    blocks: Mapping[str, str] = field(default_factory=dict)
    promoted: frozenset[str] = frozenset()

    def is_claim_eligible(self, note_id: str) -> bool:
        if note_id in self.promoted:
            return True
        return self.blocks.get(note_id, "") in CLAIM_ELIGIBLE_BLOCKS


class StatusLabeller(Protocol):
    """Port for the computed labelling — injected, and model-free by design.

    Status is what the system acts and abstains on, so a model must never decide
    it: a model's verdict is not replayable and cannot be audited. The default
    is :func:`grounded_status_labeller`; the status phase's implementation
    replaces it by injection, not by an edit here."""

    def __call__(
        self, claims: Sequence[ClaimRow], edges: Sequence[EdgeRow]
    ) -> Mapping[str, str]: ...


@runtime_checkable
class LogAppendPort(Protocol):
    """The write port. The runtime backs it; the kernel never writes.

    Takes :class:`~tessellum.dks.capability.CapabilityEffect` records — the
    existing proposal envelope — rather than storage drafts, so "append is an
    effect the deterministic promotion path renders" stays true at this boundary
    too. Returns the number of rows ACTUALLY appended, which is how a replayed
    batch reports itself as the no-op it is."""

    def append_effects(
        self, effects: Sequence[CapabilityEffect], *, base_snapshot_id: str
    ) -> int: ...


# ── the reference labeller (three layers, in order) ─────────────────────────


def grounded_status_labeller(
    claims: Sequence[ClaimRow], edges: Sequence[EdgeRow]
) -> dict[str, str]:
    """The four statuses, computed from the edge set. Pure; no model.

    Three layers, in the order the design requires — and *not* one fixed point
    over the whole edge set, which would treat support and supersession as
    attacks and forfeit the least-fixed-point guarantee the solver is used for:

    1. **Pre-filter — ``supersede``.** A supersession counts when the
       superseding claim is not ``out`` in a first provisional pass; the
       superseded claim then leaves the framework entirely. Being replaced is
       not being defeated.
    2. **The fixed point — ``attack`` only.** The ``attack`` projection is
       handed to the shipped :func:`~tessellum.dks.dung.grounded_labelling`
       unchanged.
    3. **Post-classification — ``support``.** ``in`` with a support edge is
       ``warranted``; ``in`` without one is ``proposed``; anything else
       (``out`` or ``undec``) is ``challenged``.

    ``revise`` carries no force in the labelling: it records that one claim
    answers an attack on another, and the keep/drop and carry consequences are
    real logged edges rather than inferences drawn here.

    This is the deterministic *reference* implementation for the
    :class:`StatusLabeller` port, so the boundary is usable and testable before
    the status phase lands its own; that phase's extra policy — refusing to
    report a verdict whose chain touches a ``stub`` — is surfaced here as
    :attr:`Explanation.provisional` rather than duplicated as a decision.
    """
    claim_ids = tuple(record.claim_id for record in claims)
    attacks = tuple((edge.src, edge.dst) for edge in edges if edge.op == "attack")
    supported = {edge.dst for edge in edges if edge.op == "support"}

    provisional = grounded_labelling(DungAF(arguments=claim_ids, attacks=attacks))
    superseded = {
        edge.dst
        for edge in edges
        if edge.op == "supersede" and provisional.get(edge.src) != "out"
    }
    live = tuple(claim_id for claim_id in claim_ids if claim_id not in superseded)
    live_set = set(live)
    labels = grounded_labelling(
        DungAF(
            arguments=live,
            attacks=tuple(
                (src, dst)
                for src, dst in attacks
                if src in live_set and dst in live_set
            ),
        )
    )

    statuses: dict[str, str] = {}
    for claim_id in claim_ids:
        if claim_id in superseded:
            statuses[claim_id] = "superseded"
        elif labels.get(claim_id) != "in":
            statuses[claim_id] = "challenged"
        elif claim_id in supported:
            statuses[claim_id] = "warranted"
        else:
            statuses[claim_id] = "proposed"
    return statuses


# ── what the protocol stages ────────────────────────────────────────────────


@dataclass(frozen=True)
class ClaimProposal:
    """A claim the episode wants to log — staged, not written.

    ``operator`` is condition (b) of the gate applied to a claim: what crosses
    the boundary is what has a locator *and* an operator label, and a claim
    crosses as part of an epistemic act ("stage the claim + a ``support``
    edge"). Naming that act is therefore not decoration — an unattached claim is
    a context-window thought that happened to be serialised.

    ``claim_id`` is content-derived, so it is known before the write: a staged
    edge can name it, and a replay is a no-op rather than a duplicate.
    """

    derivation_id: str
    text: str
    note_id: str
    locator: str | None = None
    provenance: str = "stub"
    source_note_hash: str | None = None
    operator: str = ""
    bb_role: str = ""

    @property
    def text_hash(self) -> str:
        return text_content_hash(self.text)

    @property
    def claim_id(self) -> str:
        return claim_content_id(self.derivation_id, self.text)


@dataclass(frozen=True)
class EdgeProposal:
    """An operator edge the episode wants to log — staged, not written.

    ``origin`` is required: an act whose provenance is unrecorded cannot later
    be audited for self-confirmation, which is the one channel this boundary
    does not close."""

    op: str
    src: str
    dst: str
    origin: str
    evidence_locator: str | None = None

    @property
    def edge_id(self) -> str:
        return edge_content_id(self.op, self.src, self.dst, self.evidence_locator)


Proposal = ClaimProposal | EdgeProposal


@dataclass(frozen=True)
class AdmissionVerdict:
    """The gate's answer for one record, with every failed condition named."""

    admitted: bool
    reasons: tuple[str, ...] = ()

    def __bool__(self) -> bool:
        return self.admitted


@dataclass(frozen=True)
class AppendOutcome:
    """The result of the episode's single append.

    ``appended`` counts rows the log actually wrote, so a replayed batch reports
    ``0`` while still reporting its effects as admitted — the distinction a
    retried episode needs. ``base_snapshot_id`` is the pinned edge-set digest
    the batch was reasoned against."""

    effects: tuple[CapabilityEffect, ...]
    admitted: tuple[Proposal, ...]
    refused: tuple[tuple[Proposal, AdmissionVerdict], ...]
    appended: int
    base_snapshot_id: str


@dataclass(frozen=True)
class StaleClaim:
    """A claim whose cited note changed after the claim was derived."""

    claim_id: str
    note_id: str
    locator: str | None
    recorded_note_hash: str
    current_note_hash: str


# ── what the protocol reads ─────────────────────────────────────────────────

CandidateSource = Literal["log", "relations", "note"]


@dataclass(frozen=True)
class ClaimCandidate:
    """One memoized claim returned by :meth:`EpisodeMemory.retrieve`.

    ``status`` is the label computed at the pinned snapshot, so a caller can
    apply the read flow — answer on ``warranted``, surface the conflict on
    ``challenged``, abstain otherwise — without a second read. ``score`` is the
    note-level retrieval score that surfaced the claim's source note; it ranks,
    it does not license."""

    claim_id: str
    text: str
    note_id: str
    locator: str | None
    provenance: str
    source_note_hash: str | None
    status: str
    score: float
    source: CandidateSource = "log"


@dataclass(frozen=True)
class RelationCandidate:
    """One current Tier-A relation returned for a resolved subject."""

    relation_id: str
    subject_id: str
    predicate: str
    object_ref: str
    valid_from: str | None
    valid_to: str | None
    evidence_note: str
    evidence_locator: str
    epistemic_status: str
    origin: str
    source: CandidateSource = "relations"


@dataclass(frozen=True)
class RetrieveResult:
    """One ``retrieve`` call's answer, at the pinned snapshot.

    Three tiers in one call, cheapest first: memoized ``claims``, current
    ``relations`` for the resolved subjects, and the ``notes`` the search seam
    ranked. ``cache_hit`` is true when memory answered at all — the numerator of
    the hit rate :meth:`EpisodeMemory.metrics` reports."""

    query: str
    claims: tuple[ClaimCandidate, ...]
    relations: tuple[RelationCandidate, ...]
    notes: tuple[NoteHit, ...]
    cache_hit: bool
    latency_ms: float
    base_snapshot_id: str


@dataclass(frozen=True)
class ChainLink:
    """One step of a support/attack chain, with the locator that licenses it."""

    op: str
    claim_id: str
    status: str
    evidence_locator: str | None
    direction: Literal["incoming", "outgoing"]


@dataclass(frozen=True)
class Explanation:
    """``explain(claim)`` — the computed label plus the chain behind it.

    ``provisional`` is true when the claim or any chain neighbour has
    ``provenance='stub'``. A stub is a located string, not a constructed claim,
    and reporting a verdict over one launders a document title into a verdict —
    so the flag travels with the explanation and the *policy* (refuse, or
    hard-label) belongs to the status phase rather than being decided here."""

    claim_id: str
    status: str
    links: tuple[ChainLink, ...]
    provisional: bool
    base_snapshot_id: str


@dataclass(frozen=True)
class MemorySnapshot:
    """The pinned read state of one episode. Immutable by construction.

    Everything the episode reads comes from here, which is what makes rule 4 a
    property of the code rather than a discipline: there is no path from the
    staging buffer into this object."""

    base_snapshot_id: str
    claims: tuple[ClaimRow, ...]
    edges: tuple[EdgeRow, ...]
    statuses: Mapping[str, str]

    def claim(self, claim_id: str) -> ClaimRow | None:
        for record in self.claims:
            if record.claim_id == claim_id:
                return record
        return None

    def status(self, claim_id: str) -> str:
        return self.statuses.get(claim_id, STATUS_UNKNOWN)

    def claims_for_note(self, note_id: str) -> tuple[ClaimRow, ...]:
        return tuple(record for record in self.claims if record.note_id == note_id)


@dataclass(frozen=True)
class MemoryMetrics:
    """The Increment-1 numbers: is the cache read, and what does a read cost?

    Reported rather than assumed, because a memory tier nobody consults has no
    measurable purpose — which is precisely the state the audit found."""

    calls: int = 0
    hits: int = 0
    claim_hits: int = 0
    relation_hits: int = 0
    latency_ms_total: float = 0.0

    @property
    def hit_rate(self) -> float:
        """Fraction of ``retrieve`` calls memory answered. ``0.0`` for no calls
        — an unmeasured cache is not a perfect one."""
        return self.hits / self.calls if self.calls else 0.0

    @property
    def mean_latency_ms(self) -> float:
        return self.latency_ms_total / self.calls if self.calls else 0.0


# ── the three-call port ─────────────────────────────────────────────────────


@runtime_checkable
class MemoryPort(Protocol):
    """The ONLY protocol↔memory interface: retrieve, status/explain, append.

    Anything wider is another way for an unverified conclusion to become
    permanent knowledge. :class:`EpisodeMemory` is the shipped implementation."""

    def retrieve(
        self, query: str, *, subject_ids: Sequence[str] = (), k: int = ...
    ) -> RetrieveResult: ...

    def status(self, claim_id: str) -> str: ...

    def explain(self, claim_id: str) -> Explanation: ...

    def append_batch(self) -> AppendOutcome: ...


# ── row stand-ins for the speculative overlay ───────────────────────────────


@dataclass(frozen=True)
class _StagedClaimRow:
    """A staged claim shaped as a :class:`ClaimRow` — for consequence-checking
    only. Never returned by a read call."""

    claim_id: str
    derivation_id: str
    text: str
    note_id: str
    locator: str | None
    provenance: str
    source_note_hash: str | None
    text_hash: str
    seq: int


@dataclass(frozen=True)
class _StagedEdgeRow:
    """A staged edge shaped as an :class:`EdgeRow` — consequence-checking only."""

    edge_id: str
    op: str
    src: str
    dst: str
    evidence_locator: str | None
    origin: str
    seq: int


class EpisodeMemory:
    """One episode's view of durable memory: pinned reads, one batched append.

    Construct per episode. The first read pins the snapshot; every later read in
    the same episode resolves against that same edge-set digest, and staged
    records are invisible to all of them.

    Args:
        log: read port over the append-only claim/edge log.
        relations: optional read port over the Tier-A relations cache.
        note_search: optional note-level search seam (see
            :class:`RetrievalNoteSearch`). Without it, ``retrieve`` still
            answers from the log by explicit ``note_ids``.
        eligibility: condition (d) of the admission gate. Omitting it makes the
            gate fail closed — nothing is claim-eligible — because a missing
            eligibility source must not read as "everything is admissible".
        labeller: the :class:`StatusLabeller`;
            :func:`grounded_status_labeller` by default.
        appender: the write port. Optional: without one, use
            :meth:`pending_effects` and route the effects through the commit
            tail. ``append_batch`` raises without one.
        clock: monotonic seconds source, injected so latency is deterministic
            under test.
    """

    def __init__(
        self,
        log: ClaimLogReader,
        *,
        relations: RelationReader | None = None,
        note_search: NoteSearch | None = None,
        eligibility: ClaimEligibility | None = None,
        labeller: StatusLabeller = grounded_status_labeller,
        appender: LogAppendPort | None = None,
        clock: Callable[[], float] = time.perf_counter,
    ) -> None:
        self._log = log
        self._relations = relations
        self._note_search = note_search
        self._eligibility = eligibility
        self._labeller = labeller
        self._appender = appender
        self._clock = clock
        self._snapshot: MemorySnapshot | None = None
        self._staged: list[Proposal] = []
        self._calls = 0
        self._hits = 0
        self._claim_hits = 0
        self._relation_hits = 0
        self._latency_ms_total = 0.0

    # ── the pin ─────────────────────────────────────────────────────────────

    @property
    def snapshot(self) -> MemorySnapshot:
        """The episode's pinned read state, taken on first access.

        Taken lazily and then never re-taken: an episode that re-read the log
        mid-flight would see appends from concurrent episodes and lose the
        round-based property (round *n+1* reads only round *n*)."""
        if self._snapshot is None:
            self._snapshot = self._read_snapshot()
        return self._snapshot

    def _read_snapshot(self) -> MemorySnapshot:
        claims = tuple(self._log.read_claims())
        edges = tuple(self._log.read_edges())
        return MemorySnapshot(
            base_snapshot_id=edgeset_digest(edges),
            claims=claims,
            edges=edges,
            statuses=dict(self._labeller(claims, edges)),
        )

    @property
    def base_snapshot_id(self) -> str:
        """The pinned edge-set digest — reused as the candidate transaction's
        ``base_snapshot_id`` rather than a second pin of our own."""
        return self.snapshot.base_snapshot_id

    def pinned_candidate(
        self, result: CapabilityResult, *, parent_fz: str | None = None
    ) -> DKSCandidate:
        """Wrap a result as a candidate transaction pinned to this episode.

        The snapshot pin already exists in the capability contract; this only
        fills it in from the edge-set digest the episode actually read at."""
        return DKSCandidate(
            result=result,
            base_snapshot_id=self.base_snapshot_id,
            parent_fz=parent_fz,
        )

    # ── call 1: retrieve ────────────────────────────────────────────────────

    def retrieve(
        self,
        query: str,
        *,
        subject_ids: Sequence[str] = (),
        k: int = 20,
        note_ids: Sequence[str] = (),
        predicate: str | None = None,
        include_expired: bool = False,
    ) -> RetrieveResult:
        """Consult memory BEFORE deriving — the cache-read path.

        Joins three reads at the pinned snapshot: the note-level hits from the
        search seam, the memoized claims on those notes (plus any ``note_ids``
        the caller resolved itself), and the current Tier-A relations for
        ``subject_ids``. Model-free throughout: a lookup and a join, never a
        judgement about meaning.

        ``include_expired`` admits relations whose validity interval has closed
        or which a later row superseded. It defaults to ``False`` because a
        role-style relation read without that filter confidently returns a
        former holder.
        """
        started = self._clock()
        snapshot = self.snapshot

        notes = tuple(self._note_search(query, k=k)) if self._note_search else ()
        scores = {hit.note_id: hit.score for hit in notes}
        wanted = set(scores) | set(note_ids)
        claims = tuple(
            sorted(
                (
                    ClaimCandidate(
                        claim_id=record.claim_id,
                        text=record.text,
                        note_id=record.note_id,
                        locator=record.locator,
                        provenance=record.provenance,
                        source_note_hash=record.source_note_hash,
                        status=snapshot.status(record.claim_id),
                        score=scores.get(record.note_id, 0.0),
                    )
                    for record in snapshot.claims
                    if record.note_id in wanted
                ),
                key=lambda candidate: (-candidate.score, candidate.claim_id),
            )
        )

        relations: list[RelationCandidate] = []
        if self._relations is not None:
            for subject_id in subject_ids:
                for row in self._relations.relations_for(subject_id, predicate):
                    if not include_expired and not _is_current(row):
                        continue
                    relations.append(
                        RelationCandidate(
                            relation_id=row.relation_id,
                            subject_id=row.subject_id,
                            predicate=row.predicate,
                            object_ref=row.object_ref,
                            valid_from=row.valid_from,
                            valid_to=row.valid_to,
                            evidence_note=row.evidence_note,
                            evidence_locator=row.evidence_locator,
                            epistemic_status=row.epistemic_status,
                            origin=row.origin,
                        )
                    )

        latency_ms = (self._clock() - started) * 1000.0
        self._calls += 1
        self._latency_ms_total += latency_ms
        self._claim_hits += len(claims)
        self._relation_hits += len(relations)
        hit = bool(claims or relations)
        self._hits += int(hit)
        return RetrieveResult(
            query=query,
            claims=claims,
            relations=tuple(relations),
            notes=notes,
            cache_hit=hit,
            latency_ms=latency_ms,
            base_snapshot_id=snapshot.base_snapshot_id,
        )

    def metrics(self) -> MemoryMetrics:
        """Cache-hit rate and latency for this episode's reads."""
        return MemoryMetrics(
            calls=self._calls,
            hits=self._hits,
            claim_hits=self._claim_hits,
            relation_hits=self._relation_hits,
            latency_ms_total=self._latency_ms_total,
        )

    # ── call 2: status / explain ────────────────────────────────────────────

    def status(self, claim_id: str) -> str:
        """The computed label at the pinned snapshot.

        Returns :data:`STATUS_UNKNOWN` for a claim the snapshot does not hold —
        including one this episode staged, which is rule 4 observable from the
        outside rather than merely documented."""
        return self.snapshot.status(claim_id)

    def explain(self, claim_id: str) -> Explanation:
        """The label plus the support/attack chain that produced it."""
        snapshot = self.snapshot
        record = snapshot.claim(claim_id)
        links: list[ChainLink] = []
        for edge in snapshot.edges:
            if edge.dst == claim_id:
                other, direction = edge.src, "incoming"
            elif edge.src == claim_id:
                other, direction = edge.dst, "outgoing"
            else:
                continue
            links.append(
                ChainLink(
                    op=edge.op,
                    claim_id=other,
                    status=snapshot.status(other),
                    evidence_locator=edge.evidence_locator,
                    direction=direction,
                )
            )
        touched = [record] if record is not None else []
        touched += [snapshot.claim(link.claim_id) for link in links]
        provisional = any(
            other is not None and other.provenance == "stub" for other in touched
        )
        return Explanation(
            claim_id=claim_id,
            status=snapshot.status(claim_id),
            links=tuple(links),
            provisional=provisional,
            base_snapshot_id=snapshot.base_snapshot_id,
        )

    # ── staging (working memory — not the log) ──────────────────────────────

    def stage(self, *proposals: Proposal) -> None:
        """Buffer records for the episode's single append.

        Staged records live in working memory: no read call can see them, and
        nothing reaches the log until :meth:`append_batch`."""
        self._staged.extend(proposals)

    @property
    def staged(self) -> tuple[Proposal, ...]:
        return tuple(self._staged)

    def speculative_statuses(self) -> Mapping[str, str]:
        """Statuses over the snapshot PLUS the staged batch.

        **Consequence-checking only, and non-citable as evidence.** Because
        staged records are unreadable, the protocol otherwise cannot evaluate
        what its own batch would do to the labelling before committing — the one
        known cost of rule 4. This exposes that consequence explicitly, under a
        name no read path uses, so the anti-self-confirmation property survives:
        :meth:`retrieve`, :meth:`status` and :meth:`explain` never consult it.
        """
        snapshot = self.snapshot
        seq = max((record.seq for record in snapshot.claims), default=0)
        seq = max(seq, max((edge.seq for edge in snapshot.edges), default=0))
        claims: list[ClaimRow] = list(snapshot.claims)
        edges: list[EdgeRow] = list(snapshot.edges)
        for proposal in self._staged:
            seq += 1
            if isinstance(proposal, ClaimProposal):
                claims.append(
                    _StagedClaimRow(
                        claim_id=proposal.claim_id,
                        derivation_id=proposal.derivation_id,
                        text=proposal.text,
                        note_id=proposal.note_id,
                        locator=proposal.locator,
                        provenance=proposal.provenance,
                        source_note_hash=proposal.source_note_hash,
                        text_hash=proposal.text_hash,
                        seq=seq,
                    )
                )
            else:
                edges.append(
                    _StagedEdgeRow(
                        edge_id=proposal.edge_id,
                        op=proposal.op,
                        src=proposal.src,
                        dst=proposal.dst,
                        evidence_locator=proposal.evidence_locator,
                        origin=proposal.origin,
                        seq=seq,
                    )
                )
        return dict(self._labeller(tuple(claims), tuple(edges)))

    # ── gate (i): the four admission conditions ─────────────────────────────

    def admit(self, proposal: Proposal) -> AdmissionVerdict:
        """Check one record against the four conditions. No model, no I/O.

        (a) an evidence locator, (b) an operator label from the closed set,
        (c) — claims only — a provenance from the closed set, and (d) — claims
        only — claim-eligibility of the source note. An edge inherits (c) and
        (d) through its endpoints: both must be claims that passed the gate,
        which the log's foreign key then enforces as existence.

        Every failed condition is reported, not just the first: a record refused
        for three reasons should not have to be resubmitted three times.
        """
        reasons: list[str] = []
        if isinstance(proposal, ClaimProposal):
            if not (proposal.locator or "").strip():
                reasons.append(REASON_NO_LOCATOR)
            if proposal.operator not in OPERATORS:
                reasons.append(REASON_NO_OPERATOR)
            if proposal.provenance not in PROVENANCES:
                reasons.append(REASON_BAD_PROVENANCE)
            if not self._is_claim_eligible(proposal.note_id):
                reasons.append(REASON_NOT_CLAIM_ELIGIBLE)
        else:
            if not (proposal.evidence_locator or "").strip():
                reasons.append(REASON_NO_LOCATOR)
            if proposal.op not in OPERATORS:
                reasons.append(REASON_NO_OPERATOR)
        return AdmissionVerdict(admitted=not reasons, reasons=tuple(reasons))

    def _is_claim_eligible(self, note_id: str) -> bool:
        if self._eligibility is None:
            return False
        return self._eligibility.is_claim_eligible(note_id)

    def gate_batch(
        self, *, strict: bool = False
    ) -> tuple[tuple[Proposal, ...], tuple[tuple[Proposal, AdmissionVerdict], ...]]:
        """Run the gate over the staged batch. Writes nothing, stages nothing.

        Returns ``(admitted, refused)`` with claims ordered before edges, so a
        renderer never emits an edge ahead of a claim it names. Refusal is
        record-level by default; ``strict`` makes one refusal refuse the batch.
        """
        claims: list[ClaimProposal] = []
        edges: list[EdgeProposal] = []
        refused: list[tuple[Proposal, AdmissionVerdict]] = []
        refused_claim_ids: set[str] = set()

        for proposal in self._staged:
            verdict = self.admit(proposal)
            if not verdict.admitted:
                refused.append((proposal, verdict))
                if isinstance(proposal, ClaimProposal):
                    refused_claim_ids.add(proposal.claim_id)
                continue
            if isinstance(proposal, ClaimProposal):
                claims.append(proposal)
            else:
                edges.append(proposal)

        kept_edges: list[EdgeProposal] = []
        for edge in edges:
            if edge.src in refused_claim_ids or edge.dst in refused_claim_ids:
                refused.append(
                    (edge, AdmissionVerdict(False, (REASON_ENDPOINT_REFUSED,)))
                )
                continue
            kept_edges.append(edge)

        if refused and strict:
            raise AdmissionError(
                "refused "
                + ", ".join(
                    f"{_proposal_id(proposal)}: {'/'.join(verdict.reasons)}"
                    for proposal, verdict in refused
                )
            )
        return (*claims, *kept_edges), tuple(refused)

    def pending_effects(self, *, strict: bool = False) -> tuple[CapabilityEffect, ...]:
        """The gated batch rendered as proposed effects — nothing is written.

        This is the primary shape of an append at this boundary: the kernel
        proposes :class:`~tessellum.dks.capability.CapabilityEffect`s and the
        deterministic promotion path renders them through the single write
        boundary. :meth:`append_batch` is the same thing with the runtime's
        adapter already wired in."""
        admitted, _refused = self.gate_batch(strict=strict)
        return tuple(effect_for_proposal(proposal) for proposal in admitted)

    # ── call 3: append_batch ────────────────────────────────────────────────

    def append_batch(self, *, strict: bool = False, clear: bool = True) -> AppendOutcome:
        """Run the gate, render the survivors as effects, append once.

        Claims are emitted before edges so an edge never names a claim the log
        has not yet written. An edge whose endpoint claim was refused in the
        same batch is refused too (:data:`REASON_ENDPOINT_REFUSED`) rather than
        being sent on to fail at the foreign key.

        Replay is a no-op: ids are content-derived, so a retried episode
        re-submits the same rows and the log reports ``appended=0``.

        A caller that routes the batch through the commit tail itself wants
        :meth:`pending_effects` instead and needs no append port at all — the
        effects *are* the append, and :class:`LogAppendPort` is only the adapter
        that renders them.
        """
        if self._appender is None:
            raise MemoryPortError(
                "append_batch needs a LogAppendPort; use pending_effects() to "
                "render the batch and route it through the commit tail instead"
            )
        admitted, refused_records = self.gate_batch(strict=strict)
        effects = tuple(effect_for_proposal(proposal) for proposal in admitted)
        base_snapshot_id = self.base_snapshot_id
        appended = (
            self._appender.append_effects(effects, base_snapshot_id=base_snapshot_id)
            if effects
            else 0
        )
        if clear:
            self._staged.clear()
        return AppendOutcome(
            effects=effects,
            admitted=admitted,
            refused=refused_records,
            appended=appended,
            base_snapshot_id=base_snapshot_id,
        )

    # ── locator staleness: DETECTION ONLY ───────────────────────────────────

    def detect_stale_claims(
        self, current_note_hashes: Mapping[str, str]
    ) -> tuple[StaleClaim, ...]:
        """Claims whose cited note has changed since derivation.

        ``current_note_hashes`` is what an index rebuild computed. Two silences
        are deliberate: a claim with no recorded ``source_note_hash`` cannot be
        checked (an honest detection gap, not a pass), and a note absent from
        the mapping is *unknown*, never asserted stale — a partial rebuild must
        not flag the whole log.

        Detection only. Re-deriving the affected claims over a base that churns
        daily is an open engineering problem, and nothing here solves it.
        """
        stale: list[StaleClaim] = []
        for record in self.snapshot.claims:
            recorded = record.source_note_hash
            if not recorded:
                continue
            current = current_note_hashes.get(record.note_id)
            if current is None or current == recorded:
                continue
            stale.append(
                StaleClaim(
                    claim_id=record.claim_id,
                    note_id=record.note_id,
                    locator=record.locator,
                    recorded_note_hash=recorded,
                    current_note_hash=current,
                )
            )
        return tuple(stale)

    def stage_staleness_flags(
        self, stale: Sequence[StaleClaim]
    ) -> tuple[Proposal, ...]:
        """Stage each staleness finding as an APPEND — an undercutting attack.

        A flag has to be an append, because the log is the only of-record tier
        and it holds exactly claims and edges. So the flag *is* a constructed
        claim ("the cited span has changed") plus an ``attack`` on the claim
        that cited it: the dependent claim moves to ``challenged``, which is the
        computed way of saying "needs re-derivation", and no new vocabulary,
        table or mutable flag column is invented to say it.

        The flag's derivation is keyed on the flagged claim, so re-running
        detection replays onto the same rows, while a *further* edit re-renders
        the same derivation — the flag revises rather than multiplies.
        """
        staged: list[Proposal] = []
        for finding in stale:
            locator = finding.locator or f"claim:{finding.claim_id}"
            flag = ClaimProposal(
                derivation_id=derivation_id(
                    finding.note_id,
                    anchor_locator(
                        f"stale:{finding.claim_id}", section=STALENESS_SECTION
                    ),
                ),
                text=(
                    f"The source span cited by claim {finding.claim_id} has changed "
                    f"since derivation (recorded {finding.recorded_note_hash}, "
                    f"current {finding.current_note_hash}); the claim needs "
                    f"re-derivation."
                ),
                note_id=finding.note_id,
                locator=locator,
                provenance="constructed",
                source_note_hash=finding.current_note_hash,
                operator="attack",
                bb_role="staleness_flag",
            )
            staged.append(flag)
            staged.append(
                EdgeProposal(
                    op="attack",
                    src=flag.claim_id,
                    dst=finding.claim_id,
                    origin=ORIGIN_STALENESS,
                    evidence_locator=locator,
                )
            )
        self.stage(*staged)
        return tuple(staged)


# ── proposals → effects (the kernel proposes; the runtime renders) ──────────


def effect_for_proposal(proposal: Proposal) -> CapabilityEffect:
    """Render one staged record as a proposed effect.

    The ``kind`` goes through :func:`~tessellum.dks.capability.validate_effect_kind`
    so the free-form field is checked against a closed vocabulary at ingestion
    — the same discipline the operator and provenance columns get."""
    if isinstance(proposal, ClaimProposal):
        return CapabilityEffect(
            kind=validate_effect_kind("claim"),
            folgezettel=proposal.note_id,
            bb_role=proposal.bb_role,
            payload={
                "claim_id": proposal.claim_id,
                "derivation_id": proposal.derivation_id,
                "text": proposal.text,
                "note_id": proposal.note_id,
                "locator": proposal.locator,
                "provenance": proposal.provenance,
                "source_note_hash": proposal.source_note_hash,
                "text_hash": proposal.text_hash,
                "operator": proposal.operator,
            },
        )
    return CapabilityEffect(
        kind=validate_effect_kind("edge"),
        folgezettel=proposal.src,
        bb_role=proposal.op,
        payload={
            "edge_id": proposal.edge_id,
            "op": proposal.op,
            "src": proposal.src,
            "dst": proposal.dst,
            "evidence_locator": proposal.evidence_locator,
            "origin": proposal.origin,
        },
    )


def _proposal_id(proposal: Proposal) -> str:
    if isinstance(proposal, ClaimProposal):
        return proposal.claim_id
    return proposal.edge_id


def _is_current(row: RelationRow) -> bool:
    """A relation row is current when nothing superseded it and its validity
    interval is still open."""
    if row.superseded_by:
        return False
    return not (row.valid_to or "").strip()


__all__ = [
    "AdmissionError",
    "AdmissionVerdict",
    "AppendOutcome",
    "BuildingBlockEligibility",
    "CLAIM_ELIGIBLE_BLOCKS",
    "CandidateSource",
    "ChainLink",
    "ClaimCandidate",
    "ClaimEligibility",
    "ClaimLogReader",
    "ClaimProposal",
    "ClaimRow",
    "ClaimStatus",
    "EVIDENCE_ONLY_BLOCKS",
    "EdgeProposal",
    "EdgeRow",
    "EpisodeMemory",
    "Explanation",
    "LogAppendPort",
    "MappingNoteSearch",
    "MemoryMetrics",
    "MemoryPort",
    "MemoryPortError",
    "MemorySnapshot",
    "NoteHit",
    "NoteSearch",
    "OPERATORS",
    "ORIGIN_STALENESS",
    "Operator",
    "PROVENANCES",
    "Proposal",
    "Provenance",
    "REASON_BAD_PROVENANCE",
    "REASON_ENDPOINT_REFUSED",
    "REASON_NOT_CLAIM_ELIGIBLE",
    "REASON_NO_LOCATOR",
    "REASON_NO_OPERATOR",
    "RelationCandidate",
    "RelationReader",
    "RelationRow",
    "RetrievalNoteSearch",
    "RetrieveResult",
    "STALENESS_SECTION",
    "STATUS_UNKNOWN",
    "StaleClaim",
    "StatusLabeller",
    "claim_content_id",
    "edge_content_id",
    "edgeset_digest",
    "effect_for_proposal",
    "grounded_status_labeller",
    "text_content_hash",
]
