"""tessellum.dks.query_protocol — query-time derivation with a THREE-WAY decision.

P8 of the query-time-DKS plan, and the phase that composes the ones before it: a
**query** entry beside the existing observation-driven cycle, which it does not
touch. The order of operations is the design's read flow, and each step is a
module already built rather than a re-implementation:

===  =====================================  ===================================
1    consult memory FIRST                   :class:`~tessellum.dks.memory_port.EpisodeMemory`
2    reach the notes, under a hop budget    :class:`~tessellum.dks.reach.SeededReach`
3    name the relation the query asks       :class:`RelationNamer` (a MODEL seam)
4    derive the claim(s) WITH LOCATORS      :class:`ClaimDeriver` (a MODEL seam)
5    attempt the bounded refutation         :class:`~tessellum.dks.core.IncompatibilityJudge`
6    validate the support DEPENDENCIES      :func:`~tessellum.dks.support_dependency.validate_support_dependencies`
7    decide — three ways                    :func:`decide`, over status AND (6)
===  =====================================  ===================================

**The decision is three-way, and STATUS is the gate.** Not a scorer threshold, and
not answer-or-abstain — collapsing the middle case is what makes a system that
knows about a live dispute either assert one side of it or say nothing:

- ``warranted`` **and the support-dependency validator passing** → **answer**,
  citing the support chain and the locator.
- ``challenged`` → **surface the conflict**, returning BOTH chains
  (:attr:`QueryResult.conflict`). This is neither an answer nor an abstention,
  and it is the outcome a scorer-threshold gate cannot express.
- ``proposed`` or ``superseded`` → **abstain**, with the reason recorded.

Status comes from :mod:`tessellum.dks.status` — the attack-only fixed point with
``supersede`` as a pre-filter and ``support`` as a post-classification — so the
verdict this protocol acts on is graph arithmetic and stays replayable. No model
decides an outcome anywhere in this module.

**``warranted`` is NECESSARY, NOT SUFFICIENT — the second half of the gate.** The
labelling runs over the ``attack`` relation only and checks ``support`` afterwards
as "has at least one supporter", so it admits two graphs that must not be answered
from: a conclusion whose *necessary premise* has been defeated, and a pair of
claims that support only each other. Both compute as ``warranted`` and both are
reproduced as fixtures in this phase's tests. So the answer arm additionally
requires :func:`~tessellum.dks.support_dependency.is_grounded` — the separate,
model-free dependency validator, run over the SAME snapshot the labelling was
computed over and read from :attr:`QueryResult.dependency`. It gates the **answer**
arm only: a ``challenged`` claim is ungrounded by construction (it was defeated),
and hiding that dispute behind an abstention would destroy the information the
conflict outcome exists to hand back.

Two different "grounding" words meet in this module, and they are not the same
check. :class:`GroundingRecord` is the **certificate** — does the cited span
entail the claim? — and it gates *admission to the log*. ``dependency`` is the
:class:`~tessellum.dks.support_dependency.GroundingVerdict` — does a chain of
surviving evidence actually reach this claim? — and it gates *answering*.

**The certificate is a grounding PRE-CONDITION, not a second verdict.** It answers
one question — does the cited span entail the claim? — and its only power is to
refuse a derived claim admission to the log
(:class:`GroundingPolicy`). It is **default OFF** here for a reason that is not
timidity: the shipped certificate is deliberately fail-closed pending a
human-labelled calibration corpus, and an un-calibrated certificate abstains on
EVERY claim, so enabling it by default would turn this phase into an
abstain-always gate. When a caller does enable it, the reference path runs the
DETERMINISTIC lexical scorer through the injected
:data:`~tessellum.composer.semantic_certificate.ClaimScorer` seam and the verdict
carries :data:`~tessellum.dks.validation.A7_5_UNCALIBRATED_NOTICE` — **entailment
is UN-CALIBRATED until the A7.5 gate passes**, and a ``grounded`` reading from the
lexical proxy is a wiring result, not an entailment result. The independent
validator (:func:`~tessellum.dks.validation.independent_validation`, the call that
makes ``validate_claims`` live and the acceptance axis's ``accepted`` branch
reachable) is opt-in for the same reason and through the same seam.

**Ungrounded assertion is structurally impossible, not merely discouraged.** An
answer needs a locator on the answering claim AND a logged ``support`` edge
carrying an evidence locator; a derivation that cites nothing produces no support
edge, so its claim is ``proposed`` and the outcome is an abstention. :func:`decide`
refuses the answer outcome without both, and :attr:`QueryResult.grounded` is the
property a caller can assert.

**The abstention rate is BOUNDED, and that is the acceptance test.** "Returns an
answer or an abstention" is trivially satisfied by always abstaining, so
:func:`tally_outcomes` reports the rate and
:meth:`OutcomeTally.within_abstention_bound` is what a question set is measured
against — an abstain-always implementation must FAIL it.

**The model budget is bounded per query**: one relation naming, k claim reads over
the reached notes, and a refutation capped both per claim
(``max_attack_candidates``) and per query (``refutation_budget``). Refutation runs
against candidate attackers surfaced for the derived claim, never against every
pair in the reached set — the difference between a constant and an O(k²) model
bill. :class:`ModelBudget` reports the realised cost so the invariant is measured
rather than asserted.

**The kernel never writes.** :class:`DKSQueryCapability` implements the existing
:class:`~tessellum.dks.capability.Capability` port and returns
:class:`~tessellum.dks.capability.CapabilityEffect`s inside the existing
warrant-bearing envelope; the deterministic promotion path renders them through
the single write boundary. There is no second port, no second envelope, and no
write path in this module. A registered ``dks_query`` capability (see
``runtime.routing.register_dks_query``) is driven through the same commit tail as
``native_digestion``; a CLI or MCP entry is a **thin caller** of the capability,
never a parallel path.

Pure (the Dependency Rule): no ``runtime`` import, no disk, no vault write. Both
model steps are injected Protocols with deterministic reference implementations
(:class:`TableRelationNamer`, :class:`TableClaimDeriver`,
:class:`~tessellum.dks.core.TableIncompatibilityJudge`), so every test in this
phase runs with no network and no model.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Iterable, Literal, Mapping, Protocol, Sequence

from tessellum.composer.lexical_scorer import make_lexical_scorer
from tessellum.composer.semantic_certificate import (
    Claim,
    ClaimScorer,
    ConformalThresholds,
    certify,
)
from tessellum.dks.capability import (
    CapabilityEffect,
    CapabilityResult,
    CapabilityStatus,
    PromotionEligibility,
)
from tessellum.dks.claim_identity import anchor_locator, derivation_id
from tessellum.dks.core import (
    DEFAULT_MAX_ATTACK_CANDIDATES,
    DEFAULT_REFUTATION_BUDGET,
    AttackDirection,
    CandidateAttackerRanker,
    DKSArgument,
    DKSWarrant,
    IncompatibilityJudge,
    LexicalOverlapRanker,
)
from tessellum.dks.memory_port import (
    ClaimCandidate,
    ClaimProposal,
    EdgeProposal,
    EpisodeMemory,
    Proposal,
    effect_for_proposal,
)
from tessellum.dks.ontology import AcceptanceVerdict, acceptance_from_labelling
from tessellum.dks.reach import ReachResult, SeededReach
from tessellum.dks.resolve_entity import EntityResolver, Resolution
from tessellum.dks.status import ClaimStatus, EdgeSet, StatusTable, compute_statuses
from tessellum.dks.support_dependency import (
    CONSERVATIVE_SUPPORT_KINDS,
    GroundingTable,
    GroundingVerdict,
    SupportKindResolver,
    validate_support_dependencies,
)
from tessellum.dks.validation import (
    A7_5_UNCALIBRATED_NOTICE,
    ClaimTypeRouter,
    IndependentValidation,
    independent_validation,
    lexical_router,
    span_text_lookup,
    warrants_for_claims,
)

# ── the three outcomes ──────────────────────────────────────────────────────

QueryOutcome = Literal["answer", "conflict", "abstain"]
"""What one query episode decided.

``"conflict"`` is a first-class outcome, not a flavour of abstention: a surfaced
dispute hands the reader both chains and lets them see that the corpus disagrees
with itself, which is information an abstention destroys."""

OUTCOMES: frozenset[str] = frozenset({"answer", "conflict", "abstain"})

ANSWERING_STATUS: str = "warranted"
CONFLICT_STATUS: str = "challenged"
ABSTAINING_STATUSES: frozenset[str] = frozenset({"proposed", "superseded"})

_STATUS_PREFERENCE: Mapping[str, int] = {
    "warranted": 0,
    "challenged": 1,
    "proposed": 2,
    "superseded": 3,
}
"""Which derived claim decides the episode when several were derived. Answerable
first, then a surfaceable conflict, then the abstaining statuses — so a query
that derived one warranted and one proposed claim answers from the warranted one
rather than abstaining on the weakest."""

# ── abstention reason codes (recorded; never a bare empty answer) ────────────

ABSTAIN_UNRESOLVED: str = "entity_unresolved"
ABSTAIN_NO_REACH: str = "no_notes_reached"
ABSTAIN_NO_RELATION: str = "relation_not_named"
ABSTAIN_NO_CLAIM: str = "no_claim_derived"
ABSTAIN_NOT_ADMISSIBLE: str = "derivation_refused_by_admission_gate"
ABSTAIN_UNGROUNDED: str = "no_locator_or_support_chain"
ABSTAIN_GROUNDING: str = "grounding_precondition_failed"
ABSTAIN_PROVISIONAL: str = "verdict_chain_touches_a_stub"
ABSTAIN_STATUS: str = "status_not_answerable"
ABSTAIN_DEPENDENCY: str = "support_dependency_not_grounded"
"""Recorded when a ``warranted`` claim FAILS the support-dependency validator.

Its own reason code, distinct from :data:`ABSTAIN_UNGROUNDED`, because the two
refusals are different facts about the corpus: ``ABSTAIN_UNGROUNDED`` means the
derivation cited nothing, while this means it cited something whose own chain does
not survive — a defeated necessary premise, a fallen line of evidence, a support
cycle or a changed source version. The validator's reasons ride out on
:attr:`QueryResult.dependency` and in the diagnostics, so which one it was is never
lost."""

# ── edge origins for the two acts this phase performs ───────────────────────

ORIGIN_DERIVATION: str = "query_derivation"
"""``edges.origin`` for the ``support`` edge a derivation logs from its cited
span to the claim it read out of that span."""

ORIGIN_REFUTATION: str = "query_refutation"
"""``edges.origin`` for the ``attack`` edge a bounded refutation logs.

``origin`` is free text with no CHECK precisely so a new *kind of act* is
recordable without widening the four-operator set: the operator is still
``attack``, and what is new is who performed it."""

BB_ROLE_DERIVED: str = "derived_claim"
BB_ROLE_EVIDENCE: str = "cited_span"

DEFAULT_MEMORY_K: int = 20
"""Note-level hits the memory read asks for before anything is derived."""

SHORT_CIRCUIT_STATUSES: frozenset[str] = frozenset({"warranted", "challenged"})
"""Memory statuses that answer the query without deriving anything.

Both are decisive: a ``warranted`` memoized claim is an answer and a
``challenged`` one is a conflict to surface. ``proposed`` and ``superseded`` are
not — they would abstain, and abstaining on a cache hit while a fresh derivation
was available is a cache that costs recall."""

DEFAULT_ABSTENTION_BOUND: float = 0.5
"""The default ceiling :meth:`OutcomeTally.within_abstention_bound` checks.

A reference bound, not a calibrated one — the real ceiling is whatever the
measurement harness's question set justifies. It exists so a caller who forgets
to choose still gets a bound that an abstain-always implementation fails."""


class QueryProtocolError(RuntimeError):
    """Raised when the protocol is asked to do something it must not do."""


# ── the two model seams, each with a deterministic reference implementation ──


@dataclass(frozen=True)
class RelationNaming:
    """The relation a query asks for, as named by a model.

    ``predicate`` is a **claim-level** predicate: it appears in claim text and,
    once consolidated, in the Tier-A relations cache. It is deliberately NOT an
    operator, NOT a traversable typed edge and NOT part of any claim's identity —
    the four operators remain the only fixed relation vocabulary, and identity
    stays ``(note_id, span_locator)`` so that naming a relation cannot fork a
    claim.

    ``rationale`` is why this is the relation the query asks; it rides out on the
    envelope's Toulmin warrant, where an auditor can read the reason rather than
    infer it."""

    predicate: str
    rationale: str = ""


class RelationNamer(Protocol):
    """Name the relation a query asks for. **A model seam.**

    One of the few genuinely semantic steps here: deciding what a question is
    *asking about* is a judgement about meaning, so it is injected rather than
    approximated by a keyword rule. Exactly one call per query — the first term
    of the cost invariant.

    Returns ``None`` for "no judgement available" (an unavailable backend, an
    unparseable answer, a question outside competence). The caller abstains and
    records why; it never falls back on a guess, because an anchor invented here
    misdirects every step after it."""

    def __call__(
        self, query: str, *, subject: Resolution | None = None
    ) -> RelationNaming | None: ...


@dataclass(frozen=True)
class TableRelationNamer:
    """Deterministic reference namer over a fixed ``query → naming`` table.

    What tests inject, and what a caller runs with no model available. A query
    absent from the table returns ``None`` — the fail-closed answer, matching the
    model-backed seam's behaviour on a refusal."""

    namings: Mapping[str, RelationNaming] = field(default_factory=dict)

    def __call__(
        self, query: str, *, subject: Resolution | None = None
    ) -> RelationNaming | None:
        return self.namings.get(query.strip())


@dataclass(frozen=True)
class Grounding:
    """One cited span that licenses a derived claim.

    ``statement`` is the proposition the span states, as read; it defaults to the
    span text itself. The distinction matters because a span is *evidence* and a
    claim is *truth-apt*: the grounding is logged as its own claim so the
    ``support`` edge has a real source, and a reader can see what was read rather
    than only what was concluded."""

    note_id: str
    span_text: str
    statement: str = ""
    section: str = ""
    source_note_hash: str | None = None


@dataclass(frozen=True)
class DerivedClaimDraft:
    """One claim a model read out of prose, WITH the span it read it from.

    The span is not optional and there is no code path that supplies a default
    for it: a claim without a locator cannot be admitted to the log, so a
    derivation that cannot point at its source cannot be logged, cited or
    answered from.

    ``groundings`` are the spans that support the claim. Empty is allowed and is
    *meaningful*: the claim is then unsupported, its status is ``proposed``, and
    the episode abstains. That is how "never an ungrounded assertion" is a
    structural property rather than a check someone might forget."""

    text: str
    note_id: str
    span_text: str
    section: str = ""
    groundings: tuple[Grounding, ...] = ()
    source_note_hash: str | None = None


class ClaimDeriver(Protocol):
    """Read the queried relation out of the reached notes' prose. **A model seam.**

    The second genuinely semantic step: extracting a claim *and its span* from
    prose. Called once per query over the notes step 2 reached, so the realised
    cost is the ``k`` claim-reads of the cost invariant rather than a call per
    candidate pair.

    An implementation must return only claims whose ``note_id`` it was given; the
    protocol drops any others and records the drop, so a deriver cannot widen the
    reached set by returning claims from notes nobody reached."""

    def __call__(
        self, query: str, *, relation: str, note_ids: Sequence[str]
    ) -> Sequence[DerivedClaimDraft]: ...


@dataclass(frozen=True)
class TableClaimDeriver:
    """Deterministic reference deriver over a fixed ``query → drafts`` table.

    Filters to the reached ``note_ids`` itself, so the fixture states what the
    model would have read and the traversal still decides what it was allowed to
    read."""

    drafts: Mapping[str, tuple[DerivedClaimDraft, ...]] = field(default_factory=dict)

    def __call__(
        self, query: str, *, relation: str, note_ids: Sequence[str]
    ) -> Sequence[DerivedClaimDraft]:
        reachable = set(note_ids)
        return tuple(
            draft
            for draft in self.drafts.get(query.strip(), ())
            if draft.note_id in reachable
        )


# ── what a derivation becomes: identity, proposals, nothing written ─────────


@dataclass(frozen=True)
class DerivedClaim:
    """One derived claim with its identity, its locator and its staged records.

    ``claim`` and ``supports`` are *proposals*: staged in the episode's working
    memory and rendered as effects, never written here. ``claim_id`` is
    content-derived, so a replayed episode re-proposes the same rows and the log
    reports the append as the no-op it is."""

    text: str
    note_id: str
    locator: str
    derivation_id: str
    span_text: str
    claim: ClaimProposal
    supports: tuple[EdgeProposal, ...] = ()
    grounding_claims: tuple[ClaimProposal, ...] = ()

    @property
    def claim_id(self) -> str:
        return self.claim.claim_id

    @property
    def grounded(self) -> bool:
        """Whether any cited span supports this claim. ``False`` ⇒ ``proposed``
        ⇒ the episode abstains rather than asserting it."""
        return bool(self.supports)

    def proposals(self) -> tuple[Proposal, ...]:
        """Claims before edges, so no edge ever names a claim not yet written."""
        return (self.claim, *self.grounding_claims, *self.supports)


def derive_claim(draft: DerivedClaimDraft) -> DerivedClaim:
    """Turn one draft into identity + staged records. Pure; no model, no I/O.

    Both the claim and each of its groundings are anchored with
    :func:`~tessellum.dks.claim_identity.anchor_locator`, the insertion-stable
    kind: inserting a sentence above a span leaves the span's own content — and
    therefore its ``derivation_id`` — unchanged, which is what makes recurrence
    countable later.

    A grounding whose content address collides with the claim's own is DROPPED
    rather than logged: a claim that supports itself is a circular justification,
    and the one channel this boundary cannot close is not one to open on purpose.
    """
    locator = anchor_locator(draft.span_text, section=draft.section)
    claim = ClaimProposal(
        derivation_id=derivation_id(draft.note_id, locator),
        text=draft.text,
        note_id=draft.note_id,
        locator=locator.canonical(),
        provenance="constructed",
        source_note_hash=draft.source_note_hash,
        operator="support",
        bb_role=BB_ROLE_DERIVED,
    )
    grounding_claims: list[ClaimProposal] = []
    supports: list[EdgeProposal] = []
    for grounding in draft.groundings:
        span_locator = anchor_locator(grounding.span_text, section=grounding.section)
        evidence = ClaimProposal(
            derivation_id=derivation_id(grounding.note_id, span_locator),
            text=grounding.statement or grounding.span_text,
            note_id=grounding.note_id,
            locator=span_locator.canonical(),
            provenance="constructed",
            source_note_hash=grounding.source_note_hash,
            operator="support",
            bb_role=BB_ROLE_EVIDENCE,
        )
        if evidence.claim_id == claim.claim_id:
            continue
        grounding_claims.append(evidence)
        supports.append(
            EdgeProposal(
                op="support",
                src=evidence.claim_id,
                dst=claim.claim_id,
                origin=ORIGIN_DERIVATION,
                evidence_locator=span_locator.canonical(),
            )
        )
    return DerivedClaim(
        text=draft.text,
        note_id=draft.note_id,
        locator=locator.canonical(),
        derivation_id=claim.derivation_id,
        span_text=draft.span_text,
        claim=claim,
        supports=tuple(supports),
        grounding_claims=tuple(grounding_claims),
    )


# ── the bounded refutation ──────────────────────────────────────────────────


@dataclass(frozen=True)
class RefutationRecord:
    """One refutation ATTEMPT, recorded whether or not it produced an edge.

    Recording the attempt is the point: "no attack edge" from an adjudicated
    compatible pair and "no attack edge" because nobody looked are entirely
    different epistemic states, and only the first licenses an answer.

    ``judged`` is ``False`` when the judge returned no verdict (unavailable,
    unparseable, out of competence) — absence of adjudicated evidence is not
    evidence of disagreement, so no edge is emitted either way."""

    claim_id: str
    candidate_claim_id: str
    judged: bool
    incompatible: bool = False
    direction: AttackDirection = "undetermined"
    rationale: str = ""
    evidence_locator: str = ""
    edge_id: str = ""

    @property
    def produced_edge(self) -> bool:
        return bool(self.edge_id)


@dataclass(frozen=True)
class RefutationOutcome:
    """Everything one query's bounded refutation produced."""

    records: tuple[RefutationRecord, ...] = ()
    attacks: tuple[EdgeProposal, ...] = ()
    judgements: int = 0
    truncated: bool = False


def _as_argument(
    claim_id: str, text: str, note_id: str, locator: str | None
) -> DKSArgument:
    """Present a claim to the shipped judge/ranker as an argument.

    Reuses the incompatibility seam the input-fixes phase built rather than
    defining a second one: the judge reads the *evidence* (the warrant licensing
    the claim and the span it cites), and the ranker keys on content, so a claim
    from the log and a claim just derived are adjudicated the same way. The
    ``perspective`` slot carries the claim id — a stable, position-free tiebreak
    for the ranker's content key."""
    return DKSArgument(
        note_id=note_id,
        note_name=note_id,
        warrant=DKSWarrant(claim=text, data=locator or "", warrant=""),
        evidence=locator or "",
        perspective=claim_id,
    )


def refute(
    derived: Sequence[DerivedClaim],
    candidates: Sequence[tuple[str, str, str, str | None]],
    *,
    judge: IncompatibilityJudge,
    ranker: CandidateAttackerRanker | None = None,
    max_attack_candidates: int = DEFAULT_MAX_ATTACK_CANDIDATES,
    refutation_budget: int = DEFAULT_REFUTATION_BUDGET,
) -> RefutationOutcome:
    """Attempt to refute each derived claim, under a hard model budget.

    ``candidates`` are ``(claim_id, text, note_id, locator)`` tuples for the
    logged claims on the reached notes — the pool the ranker surfaces attackers
    from. Two caps make the model bill a constant: ``max_attack_candidates`` per
    derived claim and ``refutation_budget`` per query. Past the budget the
    remaining pairs are left unadjudicated and ``truncated`` is set, because a
    silent truncation would read as an adjudicated absence of disagreement.

    Direction comes from the judge's evidence, never from position:
    ``b_attacks_a`` logs ``attack(candidate → derived)`` and challenges the
    answer; ``a_attacks_b`` logs ``attack(derived → candidate)`` and challenges
    the *candidate* instead. ``undetermined`` — the evidence shows the two cannot
    both hold but not which one it defeats — logs nothing, since inventing a
    direction is exactly the defect the input-fixes phase removed.

    An adjudicated attack with no locator anywhere is dropped: the admission gate
    refuses a locator-less edge, so emitting one would only fail later.
    """
    rank = ranker or LexicalOverlapRanker()
    pool = {claim_id: (text, note_id, locator) for claim_id, text, note_id, locator in candidates}
    arguments = [
        _as_argument(claim_id, text, note_id, locator)
        for claim_id, (text, note_id, locator) in sorted(pool.items())
    ]
    records: list[RefutationRecord] = []
    attacks: list[EdgeProposal] = []
    judgements = 0
    truncated = False

    for claim in derived:
        claim_argument = _as_argument(
            claim.claim_id, claim.text, claim.note_id, claim.locator
        )
        surfaced = rank(claim.text, arguments, k=max_attack_candidates)
        for candidate in surfaced:
            candidate_id = candidate.perspective
            if candidate_id == claim.claim_id:
                continue
            if judgements >= refutation_budget:
                truncated = True
                break
            verdict = judge(claim_argument, candidate)
            judgements += 1
            if verdict is None:
                records.append(
                    RefutationRecord(
                        claim_id=claim.claim_id,
                        candidate_claim_id=candidate_id,
                        judged=False,
                        rationale="no verdict available; no attack edge emitted",
                    )
                )
                continue
            locator = (
                verdict.evidence_locator
                or pool.get(candidate_id, ("", "", None))[2]
                or claim.locator
            )
            edge: EdgeProposal | None = None
            if verdict.incompatible and verdict.direction == "b_attacks_a":
                edge = EdgeProposal(
                    op="attack",
                    src=candidate_id,
                    dst=claim.claim_id,
                    origin=ORIGIN_REFUTATION,
                    evidence_locator=locator,
                )
            elif verdict.incompatible and verdict.direction == "a_attacks_b":
                edge = EdgeProposal(
                    op="attack",
                    src=claim.claim_id,
                    dst=candidate_id,
                    origin=ORIGIN_REFUTATION,
                    evidence_locator=locator,
                )
            if edge is not None and not (edge.evidence_locator or "").strip():
                edge = None
            if edge is not None:
                attacks.append(edge)
            records.append(
                RefutationRecord(
                    claim_id=claim.claim_id,
                    candidate_claim_id=candidate_id,
                    judged=True,
                    incompatible=verdict.incompatible,
                    direction=verdict.direction,
                    rationale=verdict.rationale,
                    evidence_locator=locator if verdict.incompatible else "",
                    edge_id=edge.edge_id if edge is not None else "",
                )
            )
        if truncated:
            break
    return RefutationOutcome(
        records=tuple(records),
        attacks=tuple(attacks),
        judgements=judgements,
        truncated=truncated,
    )


# ── the grounding pre-condition (DEFAULT OFF, and un-calibrated) ────────────


@dataclass(frozen=True)
class GroundingPolicy:
    """Whether the certificate gates admission of a derived claim.

    ``enabled=False`` is the default and it is a *substantive* default, not a
    conservative one: the shipped certificate is fail-closed pending a
    human-labelled calibration corpus, so an enabled-but-uncalibrated gate
    abstains on every claim and this phase would become the abstain-always
    implementation its acceptance test is written to fail.

    When enabled, ``scorer`` is the injected
    :data:`~tessellum.composer.semantic_certificate.ClaimScorer`. Left ``None``
    it defaults to the deterministic lexical reference scorer, whose ceiling is
    sharp — it is bag-of-content-words and cannot see negation or reordering. It
    makes the loop runnable and measurable; it is not a verifier. ``thresholds``
    must be supplied by the caller; there is deliberately no default, because a
    default threshold is a calibration claim.
    """

    enabled: bool = False
    thresholds: ConformalThresholds | None = None
    scorer: ClaimScorer | None = None
    domain: str | None = None


@dataclass(frozen=True)
class GroundingRecord:
    """What the grounding pre-condition did, including when it did nothing."""

    enabled: bool
    admitted: tuple[str, ...] = ()
    rejected: tuple[str, ...] = ()
    min_score: float = 0.0
    notice: str = ""

    @property
    def ran(self) -> bool:
        return self.enabled and bool(self.admitted or self.rejected)


@dataclass(frozen=True)
class ValidationPolicy:
    """Whether the independent validator runs (the acceptance axis's second axis).

    Opt-in for the same calibration reason as :class:`GroundingPolicy`, and
    orthogonal to it: the certificate decides whether a claim may enter the log,
    while this decides whether a surviving claim is ``accepted`` rather than only
    ``dialectically_adequate``. ``router`` defaults to the deterministic lexical
    router over the spans the episode already read."""

    enabled: bool = False
    thresholds: ConformalThresholds | None = None
    router: ClaimTypeRouter | None = None
    domain: str | None = None


# ── chains: what an answer cites, and what a conflict surfaces ──────────────


@dataclass(frozen=True)
class ChainStep:
    """One logged step of a chain, with the locator that licenses it."""

    op: str
    claim_id: str
    text: str
    note_id: str
    locator: str | None
    status: str
    evidence_locator: str | None


@dataclass(frozen=True)
class Chain:
    """One side of the question: a head claim plus the steps that license it.

    An answer returns exactly one chain. A ``challenged`` verdict returns **two
    or more** — the derived claim's own chain and the chain of each claim
    attacking it — because a reader who is told only "there is a conflict" cannot
    weigh it, and a reader shown one side has been given an answer dressed as a
    dispute."""

    claim_id: str
    text: str
    note_id: str
    locator: str | None
    status: str
    steps: tuple[ChainStep, ...] = ()
    role: Literal["derived", "attacker"] = "derived"

    @property
    def supports(self) -> tuple[ChainStep, ...]:
        return tuple(step for step in self.steps if step.op == "support")

    @property
    def attacks(self) -> tuple[ChainStep, ...]:
        return tuple(step for step in self.steps if step.op == "attack")

    @property
    def cited(self) -> bool:
        """Whether this chain can be cited: a locator plus a support step whose
        evidence locator is present."""
        return bool(self.locator) and any(
            (step.evidence_locator or "").strip() for step in self.supports
        )


# ── the three-way decision ─────────────────────────────────────────────────


@dataclass(frozen=True)
class Decision:
    """The outcome and, when it is an abstention, the recorded reason."""

    outcome: QueryOutcome
    reason: str = ""


def decide(
    status: str,
    *,
    provisional: bool,
    has_locator: bool,
    has_support: bool,
    dependency_validated: bool,
) -> Decision:
    """Map a computed status onto one of the three outcomes. Pure; no model.

    The order of the checks is the design:

    1. **Grounding first.** No locator, or no support edge, and the answer
       outcome is unreachable regardless of status — this is where "never an
       ungrounded assertion" is enforced rather than requested.
    2. **A stub in the chain refuses a verdict.** A ``stub`` claim is a string
       located mechanically, and most such strings are not truth-apt as written,
       so neither answering from one nor surfacing a dispute over one is honest.
    3. ``warranted`` **and** ``dependency_validated`` answers; ``challenged``
       surfaces the conflict; everything else abstains with its status recorded.

    ``dependency_validated`` is
    :attr:`~tessellum.dks.support_dependency.GroundingVerdict.grounded` for this
    claim, and it is a **required** argument precisely so no caller can reproduce
    the gate this function used to be: ``warranted`` alone admits a conclusion
    resting on a defeated necessary premise and admits a mutually-supporting pair,
    because the labelling runs over ``attack`` only and reads ``support`` as mere
    presence. A default here would let that gate back in silently.

    The validator gates the **answer** arm alone. A ``challenged`` claim is
    ungrounded by construction — the labelling defeated it — so consulting the
    validator there would convert every surfaceable conflict into an abstention
    and throw away the one outcome that hands a reader both sides.
    """
    if not has_locator or not has_support:
        return Decision("abstain", ABSTAIN_UNGROUNDED)
    if provisional:
        return Decision("abstain", ABSTAIN_PROVISIONAL)
    if status == ANSWERING_STATUS:
        if not dependency_validated:
            return Decision("abstain", ABSTAIN_DEPENDENCY)
        return Decision("answer")
    if status == CONFLICT_STATUS:
        return Decision("conflict")
    return Decision("abstain", f"{ABSTAIN_STATUS}:{status}")


# ── what the episode reports ────────────────────────────────────────────────


@dataclass(frozen=True)
class MemoryReadRecord:
    """The cache-read that happens BEFORE anything is derived.

    ``short_circuited`` is the clause the phase is measured on: a decisive
    memoized claim ends the episode with no relation naming, no derivation and no
    refutation — the model budget for such a query is zero."""

    consulted: bool = False
    cache_hit: bool = False
    claims: int = 0
    relations: int = 0
    latency_ms: float = 0.0
    short_circuited: bool = False
    claim_id: str = ""


@dataclass(frozen=True)
class ModelBudget:
    """The realised per-query model cost — reported, not assumed.

    One relation naming, ``claim_reads`` notes handed to the deriver in a single
    call, and ``refutation_judgements`` bounded adjudications. A call per note
    pair would put this in the quadratic space the whole design exists to avoid,
    so the number is carried on every result where an A/B can read it."""

    relation_namings: int = 0
    claim_reads: int = 0
    refutation_judgements: int = 0
    refutation_truncated: bool = False

    @property
    def total(self) -> int:
        return self.relation_namings + self.claim_reads + self.refutation_judgements


@dataclass(frozen=True)
class QueryRequest:
    """One query, plus whatever step 1 already resolved.

    ``resolution`` is the resolver's output; supply it, or supply a ``mention``
    and give the protocol a resolver. Ambiguity is *not* resolved here — an
    ambiguous resolution reaches nothing by default, which is the abstention step
    1 already decided on."""

    query: str
    mention: str = ""
    resolution: Resolution | None = None
    subject_ids: tuple[str, ...] = ()
    note_ids: tuple[str, ...] = ()
    entity_type: str | None = None
    k: int = DEFAULT_MEMORY_K

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "QueryRequest":
        """Coerce a plain mapping (an MCP tool's arguments) into a request.

        Unknown keys are refused rather than ignored: a silently dropped
        ``note_ids`` would look like a reach that found nothing."""
        known = {f for f in cls.__dataclass_fields__}
        unknown = sorted(set(payload) - known)
        if unknown:
            raise QueryProtocolError(f"unknown request field(s): {', '.join(unknown)}")
        if "query" not in payload:
            raise QueryProtocolError("a query request needs a 'query'")
        data = dict(payload)
        for key in ("subject_ids", "note_ids"):
            if key in data and data[key] is not None:
                data[key] = tuple(data[key])
        return cls(**data)


@dataclass(frozen=True)
class QueryResult:
    """One query episode's decision, and everything it was decided from.

    Nothing here has been written. ``proposals`` are the records the admission
    gate admitted and ``effects`` is the same batch rendered as proposed vault
    effects for the commit tail; the episode's own append is a later, single
    call by the caller.
    """

    query: str
    outcome: QueryOutcome
    relation: str = ""
    rationale: str = ""
    answer: Chain | None = None
    conflict: tuple[Chain, ...] = ()
    abstention_reason: str = ""
    derived: tuple[DerivedClaim, ...] = ()
    proposals: tuple[Proposal, ...] = ()
    effects: tuple[CapabilityEffect, ...] = ()
    refutations: tuple[RefutationRecord, ...] = ()
    memory: MemoryReadRecord = field(default_factory=MemoryReadRecord)
    reach: ReachResult | None = None
    statuses: Mapping[str, str] = field(default_factory=dict)
    grounding: GroundingRecord | None = None
    dependency: GroundingVerdict | None = None
    """The support-dependency verdict for the deciding claim — the OTHER half of
    the answer gate, and not the same thing as ``grounding``.

    ``grounding`` is the entailment certificate deciding *admission*;
    ``dependency`` is the model-free validator deciding whether a surviving chain
    of evidence actually reaches this claim. ``None`` on the paths that never got
    as far as a labelling. When an answer was refused for
    :data:`ABSTAIN_DEPENDENCY`, this is where the reasons are — a defeated
    necessary premise, a fallen evidential group, a support cycle, or a changed
    cited source version."""

    validation: IndependentValidation | None = None
    acceptance: AcceptanceVerdict | None = None
    budget: ModelBudget = field(default_factory=ModelBudget)
    diagnostics: tuple[str, ...] = ()
    base_snapshot_id: str = ""

    @property
    def answered(self) -> bool:
        return self.outcome == "answer"

    @property
    def abstained(self) -> bool:
        return self.outcome == "abstain"

    @property
    def surfaced_conflict(self) -> bool:
        return self.outcome == "conflict"

    @property
    def grounded(self) -> bool:
        """Whether nothing was asserted without a source — assertable on ANY
        result.

        An abstention is trivially grounded: it asserts nothing. An **answer** is
        grounded only when its chain is citable — a locator plus a located
        support step. A **conflict** must show at least two chains, each carrying
        a locator; it does not additionally require each attacker to be
        supported, because an unsupported attacker is a real thing the corpus
        contains and hiding it would answer the question by omission."""
        if self.outcome == "answer":
            return self.answer is not None and self.answer.cited
        if self.outcome == "conflict":
            return len(self.conflict) >= 2 and all(
                chain.locator for chain in self.conflict
            )
        return True

    @property
    def attack_edges(self) -> tuple[EdgeProposal, ...]:
        return tuple(
            proposal
            for proposal in self.proposals
            if isinstance(proposal, EdgeProposal) and proposal.op == "attack"
        )

    def __str__(self) -> str:
        head = f"{self.outcome.upper()}"
        if self.outcome == "abstain":
            head += f"({self.abstention_reason})"
        elif self.outcome == "conflict":
            head += f"({len(self.conflict)} chains)"
        return f"{self.query!r} -> {head} [budget {self.budget.total}]"


# ── the protocol ────────────────────────────────────────────────────────────


class QueryProtocol:
    """Consult memory, reach, derive, refute, decide — and never write.

    Args:
        memory: the episode's three-call boundary. One instance is one episode:
            reads pin a single edge-set digest and staged records accumulate for
            one append at the end.
        reach: the bounded seeded traversal. Required — derivation runs over the
            notes step 2 reached, and a derivation over unbounded retrieval is
            the "merely augments a prompt best-effort" path this replaces.
        namer: the relation-naming model seam.
        deriver: the claim-reading model seam.
        judge: the incompatibility judge for the bounded refutation. Without one
            no refutation is attempted, and every result says so.
        ranker: surfaces candidate attackers; the deterministic lexical
            overlap ranker by default.
        resolver: optional step-1 resolver, used when a request carries a
            ``mention`` and no ``resolution``.
        grounding: the admission pre-condition. **Default OFF.**
        validation: the independent validator. **Default OFF.**
        support_kinds: how a ``support`` edge bears on its target, for the
            dependency validator. Conservative by default — every edge reads as
            ``necessary``, which can only *withhold* an answer. **Not** a
            default-off flag: the validator always runs, because ``warranted``
            alone is not an answer gate.
        current_note_hashes: what an index rebuild computed, so a claim citing a
            span whose note has changed cannot ground an answer. ``None`` means
            no rebuild has reported, which asserts nothing stale.
        max_attack_candidates: refutation cap per derived claim.
        refutation_budget: refutation cap per query.
        short_circuit_on: memory statuses that answer without deriving.
    """

    def __init__(
        self,
        *,
        memory: EpisodeMemory,
        reach: SeededReach,
        namer: RelationNamer,
        deriver: ClaimDeriver,
        judge: IncompatibilityJudge | None = None,
        ranker: CandidateAttackerRanker | None = None,
        resolver: EntityResolver | None = None,
        grounding: GroundingPolicy | None = None,
        validation: ValidationPolicy | None = None,
        support_kinds: SupportKindResolver = CONSERVATIVE_SUPPORT_KINDS,
        current_note_hashes: Mapping[str, str] | None = None,
        max_attack_candidates: int = DEFAULT_MAX_ATTACK_CANDIDATES,
        refutation_budget: int = DEFAULT_REFUTATION_BUDGET,
        short_circuit_on: frozenset[str] = SHORT_CIRCUIT_STATUSES,
    ) -> None:
        self.memory = memory
        self.reach = reach
        self.namer = namer
        self.deriver = deriver
        self.judge = judge
        self.ranker = ranker or LexicalOverlapRanker()
        self.resolver = resolver
        self.grounding = grounding or GroundingPolicy()
        self.validation = validation or ValidationPolicy()
        self.support_kinds = support_kinds
        self.current_note_hashes = (
            dict(current_note_hashes) if current_note_hashes else None
        )
        self.max_attack_candidates = max_attack_candidates
        self.refutation_budget = refutation_budget
        self.short_circuit_on = short_circuit_on

    # ── the episode ─────────────────────────────────────────────────────────

    def ask(self, request: QueryRequest) -> QueryResult:
        """Run one query episode and return its three-way decision."""
        diagnostics: list[str] = []
        retrieved = self.memory.retrieve(
            request.query,
            subject_ids=request.subject_ids,
            k=request.k,
            note_ids=request.note_ids,
        )
        memory_record = MemoryReadRecord(
            consulted=True,
            cache_hit=retrieved.cache_hit,
            claims=len(retrieved.claims),
            relations=len(retrieved.relations),
            latency_ms=retrieved.latency_ms,
        )

        short_circuit = self._short_circuit(retrieved.claims)
        if short_circuit is not None:
            return self._from_memory(
                request, short_circuit, memory_record, diagnostics
            )

        resolution = self._resolve(request)
        if resolution is None:
            return self._abstain(
                request, ABSTAIN_UNRESOLVED, memory_record, diagnostics
            )

        reached = self.reach.reach(resolution)
        diagnostics.append(f"reach:{reached.stopping_reason}")
        note_ids = tuple(note.note_id for note in reached.notes)
        if not note_ids:
            return self._abstain(
                request,
                ABSTAIN_NO_REACH,
                memory_record,
                diagnostics,
                reach=reached,
            )

        naming = self.namer(request.query, subject=resolution)
        if naming is None:
            return self._abstain(
                request,
                ABSTAIN_NO_RELATION,
                memory_record,
                diagnostics,
                reach=reached,
                budget=ModelBudget(relation_namings=1),
            )

        drafts = tuple(
            self.deriver(request.query, relation=naming.predicate, note_ids=note_ids)
        )
        reachable = set(note_ids)
        kept = tuple(draft for draft in drafts if draft.note_id in reachable)
        for draft in drafts:
            if draft.note_id not in reachable:
                diagnostics.append(f"derivation:note_not_reached:{draft.note_id}")
        budget = ModelBudget(relation_namings=1, claim_reads=len(note_ids))
        if not kept:
            return self._abstain(
                request,
                ABSTAIN_NO_CLAIM,
                memory_record,
                diagnostics,
                reach=reached,
                naming=naming,
                budget=budget,
            )

        derived = tuple(derive_claim(draft) for draft in kept)
        grounding_record = self._check_grounding(derived)
        if grounding_record.enabled:
            rejected = set(grounding_record.rejected)
            for claim_id in sorted(rejected):
                diagnostics.append(f"grounding:rejected:{claim_id}")
            derived = tuple(
                claim for claim in derived if claim.claim_id not in rejected
            )
            if not derived:
                return self._abstain(
                    request,
                    ABSTAIN_GROUNDING,
                    memory_record,
                    diagnostics,
                    reach=reached,
                    naming=naming,
                    budget=budget,
                    grounding=grounding_record,
                )

        refutation = self._refute(derived, note_ids)
        budget = ModelBudget(
            relation_namings=budget.relation_namings,
            claim_reads=budget.claim_reads,
            refutation_judgements=refutation.judgements,
            refutation_truncated=refutation.truncated,
        )
        if refutation.truncated:
            diagnostics.append("refutation:budget_exhausted")

        proposals: list[Proposal] = []
        for claim in derived:
            proposals.extend(claim.proposals())
        proposals.extend(refutation.attacks)
        admitted, refusals = self._gate(proposals)
        diagnostics.extend(refusals)
        if not admitted:
            return self._abstain(
                request,
                ABSTAIN_NOT_ADMISSIBLE,
                memory_record,
                diagnostics,
                reach=reached,
                naming=naming,
                budget=budget,
                grounding=grounding_record,
                derived=derived,
                refutations=refutation.records,
            )
        self.memory.stage(*admitted)

        table, dependencies = self._label(admitted)
        statuses = {
            claim_id: verdict.status for claim_id, verdict in table.statuses.items()
        }
        head, verdict = self._head_claim(derived, table, dependencies)
        dependency = dependencies.verdict(head.claim_id) if head is not None else None
        if dependency is not None and not dependency.grounded:
            for reason in dependency.reasons:
                diagnostics.append(f"dependency:{reason}")
        decision = decide(
            verdict.status if verdict else "unknown",
            provisional=bool(verdict and verdict.provisional),
            has_locator=bool(head and head.locator),
            # The ADMITTED support edges, read off the labelling — not the
            # proposals. A support edge the gate refused is not in the log and
            # cannot license an answer, so counting proposals here would let a
            # refused citation pass for a citation.
            has_support=bool(verdict and verdict.supporters),
            # The other half of the gate: a surviving chain of evidence has to
            # actually REACH this claim. `warranted` admits a defeated necessary
            # premise and admits circular support, so it cannot answer alone.
            dependency_validated=bool(dependency and dependency.grounded),
        )
        answer: Chain | None = None
        conflict: tuple[Chain, ...] = ()
        if head is not None and verdict is not None:
            if decision.outcome == "answer":
                answer = self._chain(head.claim_id, table, admitted, role="derived")
            elif decision.outcome == "conflict":
                conflict = self._conflict_chains(head.claim_id, table, admitted)
                if len(conflict) < 2:
                    # A challenged claim whose attacker the fold cannot show is
                    # a conflict we cannot surface honestly, so it abstains.
                    diagnostics.append("conflict:attacker_chain_missing")
                    decision = Decision("abstain", ABSTAIN_UNGROUNDED)
                    conflict = ()

        validation = self._validate(head, naming)
        return QueryResult(
            query=request.query,
            outcome=decision.outcome,
            relation=naming.predicate,
            rationale=naming.rationale,
            answer=answer,
            conflict=conflict,
            abstention_reason=decision.reason,
            derived=derived,
            proposals=tuple(admitted),
            effects=tuple(effect_for_proposal(p) for p in admitted),
            refutations=refutation.records,
            memory=memory_record,
            reach=reached,
            statuses=statuses,
            grounding=grounding_record,
            dependency=dependency,
            validation=validation,
            acceptance=self._acceptance(verdict, validation),
            budget=budget,
            diagnostics=tuple(diagnostics),
            base_snapshot_id=self.memory.base_snapshot_id,
        )

    # ── step 1: memory first ────────────────────────────────────────────────

    def _short_circuit(
        self, candidates: Sequence[ClaimCandidate]
    ) -> ClaimCandidate | None:
        """The best decisive memoized claim, or ``None`` to go on and derive.

        ``retrieve`` returns candidates best-scoring first, so this is the
        highest-ranked claim memory holds a decisive verdict for."""
        for candidate in candidates:
            if candidate.status in self.short_circuit_on:
                return candidate
        return None

    def _from_memory(
        self,
        request: QueryRequest,
        candidate: ClaimCandidate,
        memory_record: MemoryReadRecord,
        diagnostics: list[str],
    ) -> QueryResult:
        """Answer (or surface a conflict) from memory, deriving NOTHING.

        The model budget of this path is zero: no relation is named, no note is
        read and no refutation is attempted, which is the whole point of
        consulting memory before deriving.

        The dependency validator runs here too. A memoized ``warranted`` claim is
        exactly as exposed to a since-defeated premise as a freshly derived one —
        more so, because time has passed — so a cache hit is not a route around
        the answer gate."""
        table, dependencies = self._label(())
        verdict = table.get(candidate.claim_id)
        status = verdict.status if verdict else candidate.status
        provisional = bool(verdict and verdict.provisional)
        chain = self._chain(candidate.claim_id, table, (), role="derived")
        dependency = dependencies.verdict(candidate.claim_id)
        if not dependency.grounded:
            for reason in dependency.reasons:
                diagnostics.append(f"dependency:{reason}")
        decision = decide(
            status,
            provisional=provisional,
            has_locator=bool(candidate.locator),
            has_support=bool(chain.supports),
            dependency_validated=dependency.grounded,
        )
        conflict: tuple[Chain, ...] = ()
        answer: Chain | None = None
        if decision.outcome == "answer":
            answer = chain
        elif decision.outcome == "conflict":
            conflict = self._conflict_chains(candidate.claim_id, table, ())
            if len(conflict) < 2:
                diagnostics.append("conflict:attacker_chain_missing")
                decision = Decision("abstain", ABSTAIN_UNGROUNDED)
                conflict = ()
        diagnostics.append(f"memory:short_circuit:{status}")
        return QueryResult(
            query=request.query,
            outcome=decision.outcome,
            answer=answer,
            conflict=conflict,
            abstention_reason=decision.reason,
            memory=MemoryReadRecord(
                consulted=True,
                cache_hit=memory_record.cache_hit,
                claims=memory_record.claims,
                relations=memory_record.relations,
                latency_ms=memory_record.latency_ms,
                short_circuited=True,
                claim_id=candidate.claim_id,
            ),
            statuses={candidate.claim_id: status},
            dependency=dependency,
            diagnostics=tuple(diagnostics),
            base_snapshot_id=self.memory.base_snapshot_id,
        )

    def _resolve(self, request: QueryRequest) -> Resolution | None:
        """Step 1's output — supplied, or resolved here if a resolver was given.

        An ambiguous or unresolved mention returns the :class:`Resolution` as-is;
        the reach then abstains with ``no_seed`` rather than guessing an anchor.
        ``None`` means there was nothing to resolve *with*."""
        if request.resolution is not None:
            return request.resolution
        if self.resolver is None or not request.mention:
            return None
        return self.resolver.resolve(request.mention, entity_type=request.entity_type)

    # ── the grounding pre-condition ─────────────────────────────────────────

    def _check_grounding(self, derived: Sequence[DerivedClaim]) -> GroundingRecord:
        """Certify each derived claim against its cited span, if enabled.

        Per claim rather than per batch: the certificate's job here is admission,
        and one un-entailed claim should cost only itself. Returns a disabled
        record when the policy is off, which is the default — see
        :class:`GroundingPolicy` for why that is a substantive default."""
        policy = self.grounding
        if not policy.enabled:
            return GroundingRecord(enabled=False)
        if policy.thresholds is None:
            raise QueryProtocolError(
                "GroundingPolicy(enabled=True) needs thresholds; there is no "
                "default threshold because a default threshold is a calibration "
                "claim. See validation.uncalibrated_thresholds for the "
                "explicitly-uncalibrated option."
            )
        spans = {claim.locator: claim.span_text for claim in derived}
        scorer = policy.scorer or _lexical_claim_scorer(spans)
        admitted: list[str] = []
        rejected: list[str] = []
        min_score = 1.0
        for claim in derived:
            result = certify(
                [Claim(claim.claim_id, claim.text, claim.locator)],
                scorer=scorer,
                thresholds=policy.thresholds,
                note_domain=policy.domain,
            )
            min_score = min(min_score, result.min_score)
            if result.decision == "accept":
                admitted.append(claim.claim_id)
            else:
                rejected.append(claim.claim_id)
        return GroundingRecord(
            enabled=True,
            admitted=tuple(admitted),
            rejected=tuple(rejected),
            min_score=min_score if derived else 0.0,
            notice=_uncalibrated_notice(policy.thresholds),
        )

    # ── the bounded refutation ──────────────────────────────────────────────

    def _refute(
        self, derived: Sequence[DerivedClaim], note_ids: Sequence[str]
    ) -> RefutationOutcome:
        """Adjudicate candidate attackers from the reached notes' logged claims."""
        if self.judge is None:
            return RefutationOutcome()
        reached = set(note_ids)
        candidates = tuple(
            (record.claim_id, record.text, record.note_id, record.locator)
            for record in self.memory.snapshot.claims
            if record.note_id in reached
        )
        return refute(
            derived,
            candidates,
            judge=self.judge,
            ranker=self.ranker,
            max_attack_candidates=self.max_attack_candidates,
            refutation_budget=self.refutation_budget,
        )

    # ── gate (i), applied through the boundary's own admission check ─────────

    def _gate(
        self, proposals: Sequence[Proposal]
    ) -> tuple[tuple[Proposal, ...], tuple[str, ...]]:
        """Admit what the four conditions admit; report every refusal.

        Uses :meth:`~tessellum.dks.memory_port.EpisodeMemory.admit` rather than a
        second gate of its own, so there is exactly one place the conditions
        live. Claims are ordered before edges, and an edge naming a refused claim
        is refused too — it would otherwise name a claim the log does not hold.
        """
        claims: list[ClaimProposal] = []
        edges: list[EdgeProposal] = []
        refusals: list[str] = []
        refused_claim_ids: set[str] = set()
        for proposal in proposals:
            verdict = self.memory.admit(proposal)
            if not verdict.admitted:
                refusals.append(
                    f"admission:{'/'.join(verdict.reasons)}:{_proposal_id(proposal)}"
                )
                if isinstance(proposal, ClaimProposal):
                    refused_claim_ids.add(proposal.claim_id)
                continue
            if isinstance(proposal, ClaimProposal):
                claims.append(proposal)
            else:
                edges.append(proposal)
        known = {claim.claim_id for claim in claims} | {
            record.claim_id for record in self.memory.snapshot.claims
        }
        kept_edges: list[EdgeProposal] = []
        for edge in edges:
            if edge.src in refused_claim_ids or edge.dst in refused_claim_ids:
                refusals.append(f"admission:endpoint_claim_refused:{edge.edge_id}")
                continue
            if edge.src not in known or edge.dst not in known:
                refusals.append(f"admission:endpoint_claim_unknown:{edge.edge_id}")
                continue
            kept_edges.append(edge)
        return (*claims, *kept_edges), tuple(refusals)

    # ── status over the snapshot PLUS this episode's admitted batch ──────────

    def _fold(self, staged: Sequence[Proposal]) -> EdgeSet:
        """The pinned snapshot together with the episode's own batch, as one view.

        The derived claim is by construction NOT in the pinned snapshot — rule 4
        makes staged records unreadable — so a decision drawn from the snapshot
        alone could never be anything but ``unknown``. This is the boundary's
        consequence-check made explicit: the evidence the claim cites comes from
        the snapshot, and only the claim and its own edges come from the batch, so
        nothing here lets the episode read its own conclusion as third-party
        evidence.

        One view, built once, so the labelling and the dependency validator cannot
        be computed over different snapshots and disagree about which graph they
        were answering about.
        """
        snapshot = self.memory.snapshot
        seq = max(
            (record.seq for record in snapshot.claims),
            default=0,
        )
        seq = max(seq, max((edge.seq for edge in snapshot.edges), default=0))
        claims: list[Any] = list(snapshot.claims)
        edges: list[Any] = list(snapshot.edges)
        for proposal in staged:
            seq += 1
            if isinstance(proposal, ClaimProposal):
                claims.append(_PendingClaimRow.of(proposal, seq))
            else:
                edges.append(_PendingEdgeRow.of(proposal, seq))
        return EdgeSet(claims=tuple(claims), edges=tuple(edges))

    def _label(
        self, staged: Sequence[Proposal]
    ) -> tuple[StatusTable, GroundingTable]:
        """BOTH halves of the answer gate, over one view. Pure graph arithmetic.

        The labelling is the three layers the log's own status query uses; the
        dependency validator is the separate least fixed point over the
        grounding-relevant ``support`` subgraph, and it is handed the labelling
        rather than recomputing it — passing ``statuses`` is what makes "defeated
        premise" and "defeated claim" the same fact rather than two.
        """
        view = self._fold(staged)
        table = compute_statuses(view)
        dependencies = validate_support_dependencies(
            view,
            kinds=self.support_kinds,
            current_note_hashes=self.current_note_hashes,
            statuses=table,
        )
        return table, dependencies

    def _head_claim(
        self,
        derived: Sequence[DerivedClaim],
        table: StatusTable,
        dependencies: GroundingTable,
    ) -> tuple[DerivedClaim | None, ClaimStatus | None]:
        """Which derived claim decides the episode — the most answerable one.

        Status first, then grounding: among claims the labelling ranks equally, a
        claim whose evidence chain survives is preferred, so a query that derived
        one grounded and one ungrounded ``warranted`` claim answers from the
        grounded one instead of abstaining on the other. Both tiebreaks are
        content-stable, so the choice is deterministic.
        """
        best: tuple[int, int, str] | None = None
        chosen: DerivedClaim | None = None
        verdict: ClaimStatus | None = None
        for claim in derived:
            found = table.get(claim.claim_id)
            status = found.status if found else "unknown"
            key = (
                _STATUS_PREFERENCE.get(status, 9),
                0 if dependencies.is_grounded(claim.claim_id) else 1,
                claim.claim_id,
            )
            if best is None or key < best:
                best, chosen, verdict = key, claim, found
        return chosen, verdict

    # ── chains ──────────────────────────────────────────────────────────────

    def _rows(self, staged: Sequence[Proposal]) -> dict[str, Any]:
        rows: dict[str, Any] = {
            record.claim_id: record for record in self.memory.snapshot.claims
        }
        for proposal in staged:
            if isinstance(proposal, ClaimProposal):
                rows[proposal.claim_id] = proposal
        return rows

    def _edges(self, staged: Sequence[Proposal]) -> tuple[Any, ...]:
        return (
            *self.memory.snapshot.edges,
            *(p for p in staged if isinstance(p, EdgeProposal)),
        )

    def _chain(
        self,
        claim_id: str,
        table: StatusTable,
        staged: Sequence[Proposal],
        *,
        role: Literal["derived", "attacker"],
    ) -> Chain:
        """One claim's chain: its incoming support and attack steps, with
        locators."""
        rows = self._rows(staged)
        head = rows.get(claim_id)
        verdict = table.get(claim_id)
        steps: list[ChainStep] = []
        for edge in self._edges(staged):
            if edge.dst != claim_id or edge.op not in ("support", "attack"):
                continue
            source = rows.get(edge.src)
            source_verdict = table.get(edge.src)
            steps.append(
                ChainStep(
                    op=edge.op,
                    claim_id=edge.src,
                    text=getattr(source, "text", ""),
                    note_id=getattr(source, "note_id", ""),
                    locator=getattr(source, "locator", None),
                    status=source_verdict.status if source_verdict else "unknown",
                    evidence_locator=edge.evidence_locator,
                )
            )
        steps.sort(key=lambda step: (step.op, step.claim_id))
        return Chain(
            claim_id=claim_id,
            text=getattr(head, "text", ""),
            note_id=getattr(head, "note_id", ""),
            locator=getattr(head, "locator", None),
            status=verdict.status if verdict else "unknown",
            steps=tuple(steps),
            role=role,
        )

    def _conflict_chains(
        self, claim_id: str, table: StatusTable, staged: Sequence[Proposal]
    ) -> tuple[Chain, ...]:
        """BOTH sides: the challenged claim's chain, then each attacker's own.

        A conflict is only surfaceable when the other side is actually there —
        two or more chains — because handing back one chain and the word
        "conflict" is an answer with a disclaimer."""
        own = self._chain(claim_id, table, staged, role="derived")
        attackers = tuple(
            self._chain(step.claim_id, table, staged, role="attacker")
            for step in own.attacks
        )
        return (own, *attackers) if attackers else (own,)

    # ── the second axis: independent validation (opt-in) ─────────────────────

    def _validate(
        self, head: DerivedClaim | None, naming: RelationNaming
    ) -> IndependentValidation | None:
        """Run the independent validator over the deciding claim, if enabled.

        This is the call that makes ``validate_claims`` live, and the only route
        by which anything in this system becomes ``accepted`` rather than
        ``dialectically_adequate``. Whether the verdict means anything depends on
        the thresholds — see the module docstring on calibration."""
        policy = self.validation
        if not policy.enabled or head is None:
            return None
        if policy.thresholds is None:
            raise QueryProtocolError(
                "ValidationPolicy(enabled=True) needs thresholds; see "
                "validation.uncalibrated_thresholds for the explicitly-"
                "uncalibrated option."
            )
        claims = [Claim(head.claim_id, head.text, head.locator)]
        router = policy.router or lexical_router(
            span_text_lookup({head.locator: head.span_text})
        )
        warrant = DKSWarrant(
            claim=head.text,
            data=head.locator,
            warrant=naming.rationale or naming.predicate,
        )
        return independent_validation(
            claims,
            warrants_for_claims(claims, warrant),
            thresholds=policy.thresholds,
            router=router,
            note_domain=policy.domain,
        )

    @staticmethod
    def _acceptance(
        verdict: ClaimStatus | None, validation: IndependentValidation | None
    ) -> AcceptanceVerdict | None:
        """The acceptance axis, recomputed with the validator's answer.

        The status table already carries an acceptance verdict computed with
        independent validation hard-wired unavailable. When a validator DID run,
        the same Dung label is re-read with its answer, which is the one line the
        acceptance axis was written to wait for — the four computed statuses are
        untouched, because the two are different axes over the same label."""
        if verdict is None or validation is None or verdict.label is None:
            return verdict.acceptance if verdict else None
        return acceptance_from_labelling(
            verdict.claim_id,
            {verdict.claim_id: verdict.label},
            independently_validated=validation.validated,
        )

    # ── abstention ──────────────────────────────────────────────────────────

    def _abstain(
        self,
        request: QueryRequest,
        reason: str,
        memory_record: MemoryReadRecord,
        diagnostics: Sequence[str],
        *,
        reach: ReachResult | None = None,
        naming: RelationNaming | None = None,
        budget: ModelBudget | None = None,
        grounding: GroundingRecord | None = None,
        derived: tuple[DerivedClaim, ...] = (),
        refutations: tuple[RefutationRecord, ...] = (),
    ) -> QueryResult:
        """An EXPLICIT abstention: the reason is a code, never an empty answer."""
        return QueryResult(
            query=request.query,
            outcome="abstain",
            relation=naming.predicate if naming else "",
            rationale=naming.rationale if naming else "",
            abstention_reason=reason,
            derived=derived,
            refutations=refutations,
            memory=memory_record,
            reach=reach,
            grounding=grounding,
            budget=budget or ModelBudget(),
            diagnostics=tuple(diagnostics),
            base_snapshot_id=self.memory.base_snapshot_id,
        )


# ── row stand-ins for the consequence check ─────────────────────────────────


@dataclass(frozen=True)
class _PendingClaimRow:
    """A staged claim shaped as a log row — for labelling only, never returned
    by a read call."""

    claim_id: str
    derivation_id: str
    text: str
    note_id: str
    locator: str | None
    provenance: str
    source_note_hash: str | None
    text_hash: str
    seq: int

    @classmethod
    def of(cls, proposal: ClaimProposal, seq: int) -> "_PendingClaimRow":
        return cls(
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


@dataclass(frozen=True)
class _PendingEdgeRow:
    """A staged edge shaped as a log row — labelling only."""

    edge_id: str
    op: str
    src: str
    dst: str
    evidence_locator: str | None
    origin: str
    seq: int

    @classmethod
    def of(cls, proposal: EdgeProposal, seq: int) -> "_PendingEdgeRow":
        return cls(
            edge_id=proposal.edge_id,
            op=proposal.op,
            src=proposal.src,
            dst=proposal.dst,
            evidence_locator=proposal.evidence_locator,
            origin=proposal.origin,
            seq=seq,
        )


# ── the Capability port (no second envelope, no second port) ────────────────


_PROMOTION_BY_OUTCOME: Mapping[QueryOutcome, PromotionEligibility] = {
    "answer": "needs_validation",
    "conflict": "ineligible",
    "abstain": "ineligible",
}
"""Promotion eligibility from the outcome, in the vocabulary that already exists.

An answer ``needs_validation`` because a computed verdict is a dialectical
result, not an exogenous check; it becomes ``eligible`` only when the independent
validator actually ran and accepted. A surfaced conflict is ``ineligible`` by
construction — promoting a disputed claim is how a corpus ends up asserting both
sides of its own disagreement."""


class DKSQueryCapability:
    """The query protocol behind the existing ``Capability`` port.

    Registered under ``dks_query`` beside ``dks_inquiry`` so the supervisor drives
    it through the SAME commit tail as ``native_digestion``. It returns effects
    inside the existing warrant-bearing envelope and writes nothing: the
    ``DKSExecutor`` wraps the result as a candidate transaction pinned to the
    edge-set digest the episode read at, and the deterministic promotion path
    renders the effects.

    The computed verdict rides out on ``qualifier`` and feeds
    ``promotion_eligibility``, rather than becoming a separate return channel."""

    def __init__(self, protocol: QueryProtocol) -> None:
        self.protocol = protocol

    def invoke(self, request: Any) -> CapabilityResult:
        """Run one query episode and wrap it in the existing envelope."""
        query_request = _coerce_request(request)
        result = self.protocol.ask(query_request)
        status: CapabilityStatus = "ok" if result.outcome != "abstain" else "empty"
        eligibility = _PROMOTION_BY_OUTCOME[result.outcome]
        if (
            result.outcome == "answer"
            and result.validation is not None
            and result.validation.validated
        ):
            eligibility = "eligible"
        warrant = _warrant_for(result)
        return CapabilityResult(
            status=status,
            effects=result.effects,
            diagnostics=result.diagnostics,
            promotion_eligibility=eligibility,
            warrant=warrant,
            qualifier=_qualifier_for(result),
            replay_token=_replay_token(result),
            payload=result,
        )


def _coerce_request(request: Any) -> QueryRequest:
    if isinstance(request, QueryRequest):
        return request
    if isinstance(request, Mapping):
        return QueryRequest.from_mapping(request)
    if isinstance(request, str):
        return QueryRequest(query=request)
    raise QueryProtocolError(
        f"a query capability takes a QueryRequest, a mapping or a query string, "
        f"not {type(request).__name__}"
    )


def _warrant_for(result: QueryResult) -> DKSWarrant | None:
    """The Toulmin warrant an answer rides out on — ``None`` for an abstention.

    An abstention has no licensing warrant, and manufacturing one would let a
    downstream validator consume a reason nobody gave."""
    chain = result.answer or (result.conflict[0] if result.conflict else None)
    if chain is None:
        return None
    return DKSWarrant(
        claim=chain.text,
        data=chain.locator or "",
        warrant=result.rationale or result.relation,
        qualifier=chain.status,
        rebuttal="; ".join(step.claim_id for step in chain.attacks),
    )


def _qualifier_for(result: QueryResult) -> str:
    """The computed verdict, as the envelope's calibrated qualifier."""
    if result.outcome == "abstain":
        return f"abstained:{result.abstention_reason}"
    chain = result.answer or result.conflict[0]
    return f"{result.outcome}:{chain.status}"


def _replay_token(result: QueryResult) -> str:
    """Content id over what the episode decided from — the idempotency key.

    Same construction as the envelope's own replay token (NUL-terminated parts,
    fixed truncation) so a replayed query re-proposes the same rows and the
    append reports itself as the no-op it is."""
    h = hashlib.sha256()
    for part in (
        result.query,
        result.relation,
        result.outcome,
        result.base_snapshot_id,
        *sorted(_proposal_id(p) for p in result.proposals),
    ):
        h.update(part.encode("utf-8"))
        h.update(b"\0")
    return "dks:" + h.hexdigest()[:32]


# ── measurement: the abstention rate is BOUNDED ─────────────────────────────


@dataclass(frozen=True)
class OutcomeTally:
    """Outcome counts over a question set, and the bound on abstention.

    The bound exists because "returns an answer or an abstention" is trivially
    satisfied by an implementation that always abstains, and an always-abstaining
    query protocol is indistinguishable from not having one. So the rate is the
    measurement: :meth:`within_abstention_bound` is what a question set is
    checked against, and an abstain-always implementation must FAIL it."""

    answers: int = 0
    conflicts: int = 0
    abstentions: int = 0

    @property
    def total(self) -> int:
        return self.answers + self.conflicts + self.abstentions

    @property
    def abstention_rate(self) -> float:
        """Fraction abstained. ``0.0`` for an empty set — an unmeasured protocol
        is not a perfect one, and a caller must check :attr:`total`."""
        return self.abstentions / self.total if self.total else 0.0

    @property
    def answer_rate(self) -> float:
        return self.answers / self.total if self.total else 0.0

    @property
    def conflict_rate(self) -> float:
        return self.conflicts / self.total if self.total else 0.0

    @property
    def decided_rate(self) -> float:
        """Answers plus surfaced conflicts — a conflict IS a decision."""
        return (self.answers + self.conflicts) / self.total if self.total else 0.0

    def within_abstention_bound(
        self, max_rate: float = DEFAULT_ABSTENTION_BOUND
    ) -> bool:
        """Whether the abstention rate clears the bound over a NON-EMPTY set."""
        return self.total > 0 and self.abstention_rate <= max_rate


def tally_outcomes(results: Iterable[QueryResult]) -> OutcomeTally:
    """Count outcomes over a question set. Pure."""
    answers = conflicts = abstentions = 0
    for result in results:
        if result.outcome == "answer":
            answers += 1
        elif result.outcome == "conflict":
            conflicts += 1
        else:
            abstentions += 1
    return OutcomeTally(
        answers=answers, conflicts=conflicts, abstentions=abstentions
    )


# ── helpers ─────────────────────────────────────────────────────────────────


def _lexical_claim_scorer(spans: Mapping[str, str]) -> ClaimScorer:
    """The deterministic reference scorer over spans the episode already read.

    Ships behind the same injected seam a real NLI model uses, so enabling the
    grounding pre-condition never means hard-coding a network call. Its ceiling is
    the lexical proxy's: it cannot see negation or reordering, and entailment
    stays UN-CALIBRATED until the A7.5 gate passes on a real model and a real
    corpus."""
    return make_lexical_scorer(span_text_lookup(spans))


def _uncalibrated_notice(thresholds: ConformalThresholds) -> str:
    """The A7.5 caveat, attached whenever no calibration set backs the gate."""
    return A7_5_UNCALIBRATED_NOTICE if thresholds.n_calibration == 0 else ""


def _proposal_id(proposal: Proposal) -> str:
    if isinstance(proposal, ClaimProposal):
        return proposal.claim_id
    return proposal.edge_id


__all__ = [
    "ABSTAINING_STATUSES",
    "ABSTAIN_DEPENDENCY",
    "ABSTAIN_GROUNDING",
    "ABSTAIN_NOT_ADMISSIBLE",
    "ABSTAIN_NO_CLAIM",
    "ABSTAIN_NO_REACH",
    "ABSTAIN_NO_RELATION",
    "ABSTAIN_PROVISIONAL",
    "ABSTAIN_STATUS",
    "ABSTAIN_UNGROUNDED",
    "ABSTAIN_UNRESOLVED",
    "ANSWERING_STATUS",
    "BB_ROLE_DERIVED",
    "BB_ROLE_EVIDENCE",
    "CONFLICT_STATUS",
    "DEFAULT_ABSTENTION_BOUND",
    "DEFAULT_MEMORY_K",
    "ORIGIN_DERIVATION",
    "ORIGIN_REFUTATION",
    "OUTCOMES",
    "SHORT_CIRCUIT_STATUSES",
    "Chain",
    "ChainStep",
    "ClaimDeriver",
    "DKSQueryCapability",
    "Decision",
    "DerivedClaim",
    "DerivedClaimDraft",
    "Grounding",
    "GroundingPolicy",
    "GroundingRecord",
    "MemoryReadRecord",
    "ModelBudget",
    "OutcomeTally",
    "QueryOutcome",
    "QueryProtocol",
    "QueryProtocolError",
    "QueryRequest",
    "QueryResult",
    "RefutationOutcome",
    "RefutationRecord",
    "RelationNamer",
    "RelationNaming",
    "TableClaimDeriver",
    "TableRelationNamer",
    "ValidationPolicy",
    "decide",
    "derive_claim",
    "refute",
    "tally_outcomes",
]
