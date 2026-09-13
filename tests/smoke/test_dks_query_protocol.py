"""P8 smoke tests — query-time derivation with a three-way decision.

One test (or one group) per clause of the phase's acceptance line:

1. Each of the three outcomes is EXERCISED — a located answer, a surfaced
   conflict WITH BOTH CHAINS, and an explicit abstention — and the decision is
   driven by computed STATUS, not by a scorer threshold.
2. NEVER AN UNGROUNDED ASSERTION: every asserted chain carries a locator and a
   located support step, across all three outcomes, and a derivation that cites
   nothing structurally cannot answer.
3. A FAILED REFUTATION PRODUCES AN EXECUTION RECORD AND NO ``attack`` EDGE; a
   successful one produces the edge WITH its evidence locator. The attempt is
   recorded either way, because "no attack edge" from an adjudicated compatible
   pair and "no attack edge" because nobody looked are different states — but a
   recorder must never invent an epistemic act to prove that it ran, so an
   unrefuted claim leaves the attack relation untouched.
4. THE ABSTENTION RATE IS BOUNDED. The bound test is written so that an
   abstain-always implementation FAILS it, and the companion test proves that by
   running one.
5. A MEMORY HIT SHORT-CIRCUITS DERIVATION — with the model seams wired to raise
   if called, so the short-circuit is proved rather than reported.
6. A CLAIM THAT IS ``warranted`` BUT FAILS THE SUPPORT-DEPENDENCY VALIDATOR IS
   NOT ANSWERED. The attack-only labelling is a dialectical check, not a grounded
   justification: it admits a conclusion whose necessary premise has been defeated
   and admits a mutually-supporting pair. Both graphs are built END TO END through
   the protocol — the labelling is asserted to say ``warranted``, and the episode
   is asserted to abstain anyway.

Plus the properties those clauses rest on: the grounding pre-condition is
default-OFF and un-calibrated (an enabled uncalibrated gate abstains on
everything, which is why it is not the default), ``validate_claims`` is wired and
opt-in, the capability registers on the existing registry and is driven through
``DKSExecutor``, lane routing is unchanged, the MCP tool is a thin caller with no
fallback path, the kernel writes nothing, and the module never imports the
runtime.

The runtime side is exercised for real: the append-only ``ClaimLog`` supplies the
snapshot the episode reads and the candidate attackers the refutation adjudicates.

All local; no network, no model — both model seams run their deterministic
reference implementations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import pytest

from tessellum.dks.capability import Capability, CapabilityResult, DKSCandidate, DKSExecutor
from tessellum.dks.core import (
    DKSArgument,
    IncompatibilityVerdict,
    TableIncompatibilityJudge,
)
from tessellum.dks.entity_registry import Entity, EntityAlias, EntityRegistry
from tessellum.dks.memory_port import (
    BuildingBlockEligibility,
    ClaimProposal,
    EpisodeMemory,
    MappingNoteSearch,
    NoteHit,
)
from tessellum.dks.query_protocol import (
    ABSTAIN_DEPENDENCY,
    ABSTAIN_GROUNDING,
    ABSTAIN_NO_CLAIM,
    ABSTAIN_NO_REACH,
    ABSTAIN_NO_RELATION,
    ABSTAIN_STATUS,
    ABSTAIN_UNGROUNDED,
    ABSTAIN_UNRESOLVED,
    ABSTAINING_STATUSES,
    ANSWERING_STATUS,
    CONFLICT_STATUS,
    ClaimDeriver,
    DKSQueryCapability,
    DerivedClaimDraft,
    Grounding,
    GroundingPolicy,
    ModelBudget,
    OutcomeTally,
    QueryProtocol,
    QueryProtocolError,
    QueryRequest,
    QueryResult,
    RelationNamer,
    RelationNaming,
    TableClaimDeriver,
    TableRelationNamer,
    ValidationPolicy,
    decide,
    derive_claim,
    tally_outcomes,
)
from tessellum.dks.reach import HopBudget, MappingLinkBackend, SeededReach
from tessellum.dks.resolve_entity import EntityResolver, Resolution
from tessellum.dks.status import EdgeSet
from tessellum.dks.support_dependency import (
    REASON_CYCLIC_SUPPORT,
    REASON_DEFEATED,
    REASON_NECESSARY_PREMISE_NOT_GROUNDED,
    grounding_verdict,
)
from tessellum.dks.validation import (
    A7_5_UNCALIBRATED_NOTICE,
    UNCALIBRATED_DOMAIN,
    uncalibrated_thresholds,
)
from tessellum.runtime.claim_log import ClaimDraft, ClaimLog, EdgeDraft
from tessellum.runtime.routing import (
    DKS_QUERY,
    NATIVE_DIGESTION,
    get_capability_factory,
    is_capability_registered,
    register_dks_query,
    route_lane,
)

QUERY_PROTOCOL_SOURCE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "tessellum"
    / "dks"
    / "query_protocol.py"
)

NOTE_A = "note-a"
NOTE_B = "note-b"
NOTE_INDEX = "note-index"
NOTE_UNREACHED = "note-unreached"

BLOCKS = {
    NOTE_A: "argument",
    NOTE_B: "empirical_observation",
    NOTE_UNREACHED: "argument",
    NOTE_INDEX: "navigation",  # evidence only — never a claim vertex
}

QUERY = "which component holds the retention rule"
RELATION = "holds_rule"

# The span the derivation reads the answer out of, and the answer it reads.
ANSWER_SPAN = "The retention rule is held by the archival component."
ANSWER_TEXT = "The archival component holds the retention rule."
EVIDENCE_SPAN = "Retention is applied by the archival component on write."

# The corpus's competing claim, seeded in the log on a note the reach reaches.
RIVAL_TEXT = "The retention rule is held by the ingest component."
RIVAL_LOCATOR = "anchor||rival|0"
RIVAL_EVIDENCE = "Ingest applies retention before the archival component sees it."


# ── fixtures: a real log, a bounded reach, deterministic model seams ─────────


def _log(tmp_path: Path) -> ClaimLog:
    return ClaimLog.open(tmp_path / "runtime.db")


def _episode(
    log: ClaimLog, *, hits: dict[str, tuple[NoteHit, ...]] | None = None
) -> EpisodeMemory:
    """One episode's boundary. No appender: this phase proposes, never writes."""
    return EpisodeMemory(
        log,
        note_search=MappingNoteSearch(hits=hits) if hits else None,
        eligibility=BuildingBlockEligibility(blocks=BLOCKS),
    )


def _reach(*, extra: dict[str, tuple[str, ...]] | None = None) -> SeededReach:
    """A one-hop reach from ``NOTE_A``, which links to ``NOTE_B``."""
    adjacency: dict[str, tuple[str, ...]] = {NOTE_A: (NOTE_B,)}
    adjacency.update(extra or {})
    return SeededReach(
        expander=MappingLinkBackend(adjacency=adjacency),
        budget=HopBudget(max_hops=1),
    )


MENTION = "archival component"


def _resolution() -> Resolution:
    return Resolution(
        mention=MENTION,
        entity_id=NOTE_A,
        canonical_name=MENTION,
        entity_type="model",
        method="exact_alias",
        score=1.0,
    )


def _resolver() -> EntityResolver:
    """A one-entity registry, so the step-1 → step-2 path runs for real."""
    return EntityResolver(
        EntityRegistry(
            entities=(
                Entity(entity_id=NOTE_A, canonical_name=MENTION, entity_type="model"),
            ),
            aliases=(
                EntityAlias(entity_id=NOTE_A, alias=MENTION, alias_kind="canonical"),
            ),
        )
    )


def _grounded_draft(
    *, note_id: str = NOTE_A, groundings: bool = True
) -> DerivedClaimDraft:
    return DerivedClaimDraft(
        text=ANSWER_TEXT,
        note_id=note_id,
        span_text=ANSWER_SPAN,
        source_note_hash="hash-a",
        groundings=(
            (
                Grounding(
                    note_id=NOTE_B,
                    span_text=EVIDENCE_SPAN,
                    statement=EVIDENCE_SPAN,
                    source_note_hash="hash-b",
                ),
            )
            if groundings
            else ()
        ),
    )


def _protocol(
    log: ClaimLog,
    *,
    query: str = QUERY,
    drafts: tuple[DerivedClaimDraft, ...] = (),
    verdicts: dict[tuple[str, str], IncompatibilityVerdict] | None = None,
    hits: dict[str, tuple[NoteHit, ...]] | None = None,
    namer: RelationNamer | None = None,
    deriver: ClaimDeriver | None = None,
    grounding: GroundingPolicy | None = None,
    validation: ValidationPolicy | None = None,
    refutation_budget: int = 8,
    extra_links: dict[str, tuple[str, ...]] | None = None,
    memory: EpisodeMemory | None = None,
    resolver: EntityResolver | None = None,
) -> QueryProtocol:
    return QueryProtocol(
        memory=memory or _episode(log, hits=hits),
        reach=_reach(extra=extra_links),
        namer=namer
        or TableRelationNamer(
            {query: RelationNaming(RELATION, "the query asks which part holds it")}
        ),
        deriver=deriver or TableClaimDeriver({query: drafts}),
        judge=TableIncompatibilityJudge(verdicts or {}),
        resolver=resolver,
        grounding=grounding,
        validation=validation,
        refutation_budget=refutation_budget,
    )


def _request(*, query: str = QUERY, **kwargs) -> QueryRequest:
    return QueryRequest(query=query, resolution=_resolution(), **kwargs)


def _seed_rival(log: ClaimLog) -> tuple[str, str]:
    """A supported rival claim on ``NOTE_B`` — the corpus disagreeing already.

    Seeded through the runtime log directly (a pre-existing corpus claim, not
    something this episode derived), so the refutation adjudicates a real logged
    row rather than a stand-in."""
    evidence = ClaimDraft(
        derivation_id="derivation-rival-evidence",
        text=RIVAL_EVIDENCE,
        note_id=NOTE_B,
        locator="anchor||rival-evidence|0",
        provenance="constructed",
        source_note_hash="hash-b",
    )
    rival = ClaimDraft(
        derivation_id="derivation-rival",
        text=RIVAL_TEXT,
        note_id=NOTE_B,
        locator=RIVAL_LOCATOR,
        provenance="constructed",
        source_note_hash="hash-b",
    )
    log.append(
        (
            evidence,
            rival,
            EdgeDraft(
                op="support",
                src=evidence.claim_id,
                dst=rival.claim_id,
                origin="authored",
                evidence_locator="anchor||rival-evidence|0",
            ),
        )
    )
    return evidence.claim_id, rival.claim_id


def _rival_defeats_answer() -> dict[tuple[str, str], IncompatibilityVerdict]:
    """The judge's adjudication: the two cannot both hold, and the RIVAL wins.

    ``b_attacks_a`` — the direction comes from the evidence, not from which claim
    was generated first."""
    return {
        (ANSWER_TEXT, RIVAL_TEXT): IncompatibilityVerdict(
            incompatible=True,
            direction="b_attacks_a",
            rationale="only one component can apply retention first",
            evidence_locator=RIVAL_LOCATOR,
        )
    }


class _RaisingNamer:
    """A relation namer that must never be called."""

    def __call__(self, query: str, *, subject: Resolution | None = None):
        raise AssertionError("the relation was named after a memory hit")


class _RaisingDeriver:
    """A claim deriver that must never be called."""

    def __call__(
        self, query: str, *, relation: str, note_ids: Sequence[str]
    ) -> Sequence[DerivedClaimDraft]:
        raise AssertionError("derivation ran after a memory hit")


class _WideningDeriver:
    """A deriver that ignores the reached set — the misbehaviour the protocol
    must contain, since a deriver returning claims from unreached notes would
    otherwise widen the traversal from inside the model seam."""

    def __init__(self, *drafts: DerivedClaimDraft) -> None:
        self.drafts = drafts

    def __call__(
        self, query: str, *, relation: str, note_ids: Sequence[str]
    ) -> Sequence[DerivedClaimDraft]:
        return self.drafts


# ── clause 1a: a LOCATED ANSWER ─────────────────────────────────────────────


def test_a_warranted_claim_answers_citing_its_support_chain_and_locator(
    tmp_path: Path,
) -> None:
    log = _log(tmp_path)
    protocol = _protocol(log, drafts=(_grounded_draft(),))

    result = protocol.ask(_request())

    assert result.outcome == "answer"
    assert result.answer is not None
    assert result.answer.status == "warranted"
    assert result.answer.text == ANSWER_TEXT
    # the locator is a content anchor, so an insertion above the span cannot move it
    assert result.answer.locator and result.answer.locator.startswith("anchor|")
    supports = result.answer.supports
    assert len(supports) == 1
    assert supports[0].text == EVIDENCE_SPAN
    assert supports[0].evidence_locator  # the citation, not just the claim
    assert result.grounded
    assert result.relation == RELATION


def test_the_answer_rides_out_on_the_existing_envelope(tmp_path: Path) -> None:
    log = _log(tmp_path)
    capability = DKSQueryCapability(_protocol(log, drafts=(_grounded_draft(),)))

    envelope = capability.invoke(_request())

    assert isinstance(envelope, CapabilityResult)
    assert envelope.status == "ok"
    # the COMPUTED verdict rides on the qualifier and feeds promotion eligibility
    assert envelope.qualifier == "answer:warranted"
    assert envelope.promotion_eligibility == "needs_validation"
    assert envelope.warrant is not None
    assert envelope.warrant.claim == ANSWER_TEXT
    assert {effect.kind for effect in envelope.effects} == {"claim", "edge"}
    assert envelope.replay_token.startswith("dks:")


# ── clause 1b: a SURFACED CONFLICT, with BOTH chains ────────────────────────


def test_a_challenged_claim_surfaces_the_conflict_with_both_chains(
    tmp_path: Path,
) -> None:
    log = _log(tmp_path)
    _rival_evidence_id, rival_id = _seed_rival(log)
    protocol = _protocol(
        log, drafts=(_grounded_draft(),), verdicts=_rival_defeats_answer()
    )

    result = protocol.ask(_request())

    assert result.outcome == "conflict"
    assert result.answer is None  # a conflict is NOT an answer
    assert result.abstention_reason == ""  # nor an abstention
    assert len(result.conflict) == 2
    own, attacker = result.conflict
    assert own.role == "derived" and own.status == "challenged"
    assert own.text == ANSWER_TEXT
    assert attacker.role == "attacker" and attacker.claim_id == rival_id
    assert attacker.text == RIVAL_TEXT
    # BOTH chains are citable in their own right: each has a locator, and each
    # carries the support that licenses it.
    assert own.locator and attacker.locator
    assert own.supports and attacker.supports
    assert {chain.claim_id for chain in result.conflict} == {own.claim_id, rival_id}
    assert result.grounded


def test_the_conflict_rides_out_as_a_result_that_is_neither_ok_nor_promotable(
    tmp_path: Path,
) -> None:
    log = _log(tmp_path)
    _seed_rival(log)
    capability = DKSQueryCapability(
        _protocol(log, drafts=(_grounded_draft(),), verdicts=_rival_defeats_answer())
    )

    envelope = capability.invoke(_request())

    assert envelope.qualifier == "conflict:challenged"
    # a disputed claim must never be promoted — that is how a corpus ends up
    # asserting both sides of its own disagreement.
    assert envelope.promotion_eligibility == "ineligible"


# ── clause 1c: an EXPLICIT abstention ───────────────────────────────────────


def test_a_derivation_that_cites_nothing_abstains_explicitly(tmp_path: Path) -> None:
    log = _log(tmp_path)
    protocol = _protocol(log, drafts=(_grounded_draft(groundings=False),))

    result = protocol.ask(_request())

    assert result.outcome == "abstain"
    assert result.abstention_reason == ABSTAIN_UNGROUNDED
    assert result.answer is None
    assert result.conflict == ()
    # the claim was still derived and staged — the abstention is about the
    # VERDICT, not about having failed to read anything.
    assert len(result.derived) == 1
    assert result.grounded  # an abstention asserts nothing


def test_every_abstention_names_its_reason(tmp_path: Path) -> None:
    """Four abstaining paths, four distinct recorded reasons — never a blank."""
    log = _log(tmp_path)
    unresolved = Resolution(
        mention="unknown thing",
        entity_id=None,
        canonical_name=None,
        entity_type=None,
        method="unresolved",
        score=0.0,
    )
    no_seed = _protocol(log, drafts=(_grounded_draft(),)).ask(
        QueryRequest(query=QUERY, resolution=unresolved)
    )
    unnamed = _protocol(
        log, drafts=(_grounded_draft(),), namer=TableRelationNamer({})
    ).ask(_request())
    nothing_derived = _protocol(log, drafts=()).ask(_request())
    uncited = _protocol(log, drafts=(_grounded_draft(groundings=False),)).ask(
        _request()
    )
    # nothing to resolve WITH is a different refusal from resolving to nothing
    nothing_to_resolve = _protocol(log, drafts=(_grounded_draft(),)).ask(
        QueryRequest(query=QUERY)
    )

    assert no_seed.abstention_reason == ABSTAIN_NO_REACH
    assert unnamed.abstention_reason == ABSTAIN_NO_RELATION
    assert nothing_derived.abstention_reason == ABSTAIN_NO_CLAIM
    assert uncited.abstention_reason == ABSTAIN_UNGROUNDED
    assert nothing_to_resolve.abstention_reason == ABSTAIN_UNRESOLVED
    assert all(
        result.outcome == "abstain"
        for result in (
            no_seed,
            unnamed,
            nothing_derived,
            uncited,
            nothing_to_resolve,
        )
    )


# ── clause 2: never an ungrounded assertion ─────────────────────────────────


def test_no_outcome_ever_asserts_without_a_locator_and_a_support_chain(
    tmp_path: Path,
) -> None:
    answer = _protocol(_log(tmp_path / "a"), drafts=(_grounded_draft(),)).ask(
        _request()
    )
    conflict_log = _log(tmp_path / "b")
    _seed_rival(conflict_log)
    conflict = _protocol(
        conflict_log, drafts=(_grounded_draft(),), verdicts=_rival_defeats_answer()
    ).ask(_request())
    abstention = _protocol(
        _log(tmp_path / "c"), drafts=(_grounded_draft(groundings=False),)
    ).ask(_request())

    for result in (answer, conflict, abstention):
        assert result.grounded, result
        for chain in ((result.answer,) if result.answer else ()) + result.conflict:
            assert chain.locator
            assert any(step.evidence_locator for step in chain.supports)


def test_status_is_the_gate_and_a_stub_chain_refuses_a_verdict() -> None:
    """The decision function, exhaustively — no scorer appears in it."""
    validated = {
        "provisional": False,
        "has_locator": True,
        "has_support": True,
        "dependency_validated": True,
    }
    assert decide("warranted", **validated).outcome == "answer"
    assert decide("challenged", **validated).outcome == "conflict"
    for status in ("proposed", "superseded", "unknown"):
        decision = decide(status, **validated)
        assert decision.outcome == "abstain"
        assert decision.reason == f"{ABSTAIN_STATUS}:{status}"
    # grounding is checked FIRST: a warranted claim with nothing cited abstains
    assert (
        decide(
            "warranted",
            provisional=False,
            has_locator=False,
            has_support=True,
            dependency_validated=True,
        ).reason
        == ABSTAIN_UNGROUNDED
    )
    assert (
        decide(
            "warranted",
            provisional=False,
            has_locator=True,
            has_support=False,
            dependency_validated=True,
        ).reason
        == ABSTAIN_UNGROUNDED
    )
    # and a stub anywhere in the chain refuses the verdict rather than laundering it
    assert (
        decide(
            "warranted",
            provisional=True,
            has_locator=True,
            has_support=True,
            dependency_validated=True,
        ).outcome
        == "abstain"
    )


def test_warranted_alone_is_not_the_answer_gate() -> None:
    """``warranted`` is NECESSARY, NOT SUFFICIENT — the flipped clause.

    An earlier version of this file asserted that ``decide("warranted", ...)``
    answers on the strength of the status alone. That is the gate the attack-only
    labelling cannot support: it checks that a claim survived criticism and that
    *something* supports it, never that the support grounds it. So the answer arm
    also requires the dependency validator, and there is deliberately no default
    for that argument — a caller cannot omit its way back to the old gate."""
    refused = decide(
        "warranted",
        provisional=False,
        has_locator=True,
        has_support=True,
        dependency_validated=False,
    )

    assert refused.outcome == "abstain"
    assert refused.reason == ABSTAIN_DEPENDENCY
    # a distinct reason from "cited nothing": this claim DID cite, and what it
    # cited is what failed.
    assert refused.reason != ABSTAIN_UNGROUNDED
    # the validator gates the ANSWER arm only — a challenged claim still surfaces
    # its conflict, because an abstention would destroy the dispute.
    assert (
        decide(
            "challenged",
            provisional=False,
            has_locator=True,
            has_support=True,
            dependency_validated=False,
        ).outcome
        == "conflict"
    )
    with pytest.raises(TypeError):
        decide(  # type: ignore[call-arg]
            "warranted", provisional=False, has_locator=True, has_support=True
        )


def test_the_three_way_partition_covers_every_computed_status() -> None:
    """A fifth status must not silently fall through to an abstention.

    The four computed statuses are the gate, so the three decision arms have to
    partition them exactly — a new status added upstream should break this test
    rather than quietly become "abstain"."""
    from tessellum.dks.status import STATUSES

    assert {ANSWERING_STATUS, CONFLICT_STATUS} | ABSTAINING_STATUSES == STATUSES
    assert ANSWERING_STATUS not in ABSTAINING_STATUSES
    assert CONFLICT_STATUS not in ABSTAINING_STATUSES


def test_a_derivation_from_a_non_claim_eligible_note_is_refused(
    tmp_path: Path,
) -> None:
    """Admission condition (d) still applies to a query-time derivation.

    An index note is a thing a locator points *into*; it is not truth-apt, so a
    claim located on one may not enter the log or receive a verdict."""
    log = _log(tmp_path)
    protocol = _protocol(
        log,
        drafts=(_grounded_draft(note_id=NOTE_INDEX),),
        extra_links={NOTE_A: (NOTE_B, NOTE_INDEX)},
    )

    result = protocol.ask(_request())

    assert result.outcome == "abstain"
    assert any(
        "source_note_not_claim_eligible" in diagnostic
        for diagnostic in result.diagnostics
    )
    assert all(
        proposal.note_id != NOTE_INDEX
        for proposal in result.proposals
        if isinstance(proposal, ClaimProposal)
    )


def test_derivation_is_confined_to_the_notes_the_reach_reached(
    tmp_path: Path,
) -> None:
    log = _log(tmp_path)
    protocol = _protocol(
        log, deriver=_WideningDeriver(_grounded_draft(note_id=NOTE_UNREACHED))
    )

    result = protocol.ask(_request())

    assert result.reach is not None
    assert NOTE_UNREACHED not in result.reach.note_ids
    assert result.outcome == "abstain"
    assert result.abstention_reason == ABSTAIN_NO_CLAIM
    assert f"derivation:note_not_reached:{NOTE_UNREACHED}" in result.diagnostics


# ── clause 6: `warranted` is NECESSARY, NOT SUFFICIENT ──────────────────────
#
# The two graphs the attack-only labelling reports as `warranted` and must not be
# answered from, each built END TO END through the protocol. Both are seeded into
# the real log: a claim id is a content address on both sides of the boundary, so
# re-stating the derivation's own cited span as a log row yields the same id the
# episode will stage — which is what lets a fixture put an edge on the derived
# claim's PREMISE before the episode runs.


COUNTER_TEXT = "The retention rule was withdrawn; no component holds it."
PEER_TEXT = "The archival component is the retention holder of record."


def _seeded_premise_draft() -> ClaimDraft:
    """The derivation's own cited span, as a pre-existing log row."""
    evidence = derive_claim(_grounded_draft()).grounding_claims[0]
    return ClaimDraft(
        derivation_id=evidence.derivation_id,
        text=evidence.text,
        note_id=evidence.note_id,
        locator=evidence.locator,
        provenance=evidence.provenance,
        source_note_hash=evidence.source_note_hash,
    )


def _defeated_premise_graph(log: ClaimLog) -> tuple[str, str, str]:
    """``premise`` supports ``conclusion``; ``counter`` defeats ``premise``."""
    conclusion = derive_claim(_grounded_draft())
    premise = _seeded_premise_draft()
    counter = ClaimDraft(
        derivation_id="derivation-counter",
        text=COUNTER_TEXT,
        note_id=NOTE_B,
        locator="anchor||counter|0",
        provenance="constructed",
        source_note_hash="hash-b",
    )
    log.append(
        (
            premise,
            counter,
            EdgeDraft(
                op="attack",
                src=counter.claim_id,
                dst=premise.claim_id,
                origin="authored",
                evidence_locator="anchor||counter|0",
            ),
        )
    )
    return conclusion.claim_id, premise.claim_id, counter.claim_id


def _circular_support_graph(log: ClaimLog) -> tuple[str, str, str]:
    """``premise`` and ``peer`` support only each other — no external anchor."""
    conclusion = derive_claim(_grounded_draft())
    premise = _seeded_premise_draft()
    peer = ClaimDraft(
        derivation_id="derivation-peer",
        text=PEER_TEXT,
        note_id=NOTE_B,
        locator="anchor||peer|0",
        provenance="constructed",
        source_note_hash="hash-b",
    )
    log.append(
        (
            premise,
            peer,
            EdgeDraft(
                op="support",
                src=peer.claim_id,
                dst=premise.claim_id,
                origin="authored",
                evidence_locator="anchor||peer|0",
            ),
            EdgeDraft(
                op="support",
                src=premise.claim_id,
                dst=peer.claim_id,
                origin="authored",
                evidence_locator=premise.locator,
            ),
        )
    )
    return conclusion.claim_id, premise.claim_id, peer.claim_id


def test_a_warranted_conclusion_on_a_defeated_premise_is_not_answered(
    tmp_path: Path,
) -> None:
    """A supported conclusion does not inherit the defeat of its premise.

    The labelling is right and unchanged — it runs over ``attack`` only and reads
    ``support`` as mere presence. What it cannot say is whether the support
    *grounds* the conclusion, so the answer arm asks the dependency validator too
    and this episode abstains with the premise named."""
    log = _log(tmp_path)
    conclusion_id, premise_id, _counter_id = _defeated_premise_graph(log)
    protocol = _protocol(log, drafts=(_grounded_draft(),))

    result = protocol.ask(_request())

    # the LABELLING admits it — this is the finding, reproduced rather than fixed
    assert result.statuses[conclusion_id] == ANSWERING_STATUS
    assert result.statuses[premise_id] == CONFLICT_STATUS
    # ...and nothing is answered from it
    assert result.outcome == "abstain"
    assert result.abstention_reason == ABSTAIN_DEPENDENCY
    assert result.answer is None
    assert result.conflict == ()
    assert result.dependency is not None
    assert not result.dependency.grounded
    assert REASON_NECESSARY_PREMISE_NOT_GROUNDED in result.dependency.reasons
    assert result.dependency.failed_premises == (premise_id,)
    # the refusal is auditable, not just recorded as a code
    assert f"dependency:{REASON_NECESSARY_PREMISE_NOT_GROUNDED}" in result.diagnostics
    view = EdgeSet(claims=log.read_claims(), edges=log.read_edges())
    assert REASON_DEFEATED in grounding_verdict(view, premise_id).reasons


def test_a_warranted_claim_standing_on_circular_support_is_not_answered(
    tmp_path: Path,
) -> None:
    """Support existence alone admits circular justification.

    Two claims that support only each other are both ``warranted``, and a
    conclusion resting on either of them is too. None of the three rests on
    anything, so the episode abstains and the cycle is named."""
    log = _log(tmp_path)
    conclusion_id, premise_id, peer_id = _circular_support_graph(log)
    protocol = _protocol(log, drafts=(_grounded_draft(),))

    result = protocol.ask(_request())

    # all three compute as warranted — the labelling cannot see the cycle
    assert result.statuses[conclusion_id] == ANSWERING_STATUS
    assert result.statuses[premise_id] == ANSWERING_STATUS
    assert result.statuses[peer_id] == ANSWERING_STATUS
    # ...and nothing is answered from a pair that stands only on itself
    assert result.outcome == "abstain"
    assert result.abstention_reason == ABSTAIN_DEPENDENCY
    assert result.answer is None
    assert result.dependency is not None
    assert not result.dependency.grounded
    assert result.dependency.failed_premises == (premise_id,)
    # the cycle is DIAGNOSED, not merely refused
    view = EdgeSet(claims=log.read_claims(), edges=log.read_edges())
    cycle = grounding_verdict(view, premise_id)
    assert not cycle.grounded
    assert REASON_CYCLIC_SUPPORT in cycle.reasons
    assert set(cycle.cycle) == {premise_id, peer_id}


def _memoized_claim_on_a_defeated_premise(log: ClaimLog) -> tuple[str, str]:
    """A memoized ``warranted`` claim whose only premise has since been defeated.

    The premise and its defeater sit on ``NOTE_A`` and the memoized claim on
    ``NOTE_B``, so the note-level memory read surfaces exactly one candidate and
    the short-circuit is deterministic."""
    premise = ClaimDraft(
        derivation_id="derivation-memo-premise",
        text=EVIDENCE_SPAN,
        note_id=NOTE_A,
        locator="anchor||memo-premise|0",
        provenance="constructed",
        source_note_hash="hash-a",
    )
    counter = ClaimDraft(
        derivation_id="derivation-memo-counter",
        text=COUNTER_TEXT,
        note_id=NOTE_A,
        locator="anchor||memo-counter|0",
        provenance="constructed",
        source_note_hash="hash-a",
    )
    memoized = ClaimDraft(
        derivation_id="derivation-memoized",
        text=ANSWER_TEXT,
        note_id=NOTE_B,
        locator="anchor||memoized|0",
        provenance="constructed",
        source_note_hash="hash-b",
    )
    log.append(
        (
            premise,
            counter,
            memoized,
            EdgeDraft(
                op="support",
                src=premise.claim_id,
                dst=memoized.claim_id,
                origin="authored",
                evidence_locator="anchor||memo-premise|0",
            ),
            EdgeDraft(
                op="attack",
                src=counter.claim_id,
                dst=premise.claim_id,
                origin="authored",
                evidence_locator="anchor||memo-counter|0",
            ),
        )
    )
    return memoized.claim_id, premise.claim_id


def test_a_memory_hit_is_not_a_route_around_the_dependency_gate(
    tmp_path: Path,
) -> None:
    """The cache-read path decides through the SAME gate.

    A memoized ``warranted`` claim is at least as exposed to a since-defeated
    premise as a freshly derived one, so the short-circuit still consults the
    validator — and still derives nothing when it refuses."""
    log = _log(tmp_path)
    memoized_id, premise_id = _memoized_claim_on_a_defeated_premise(log)
    memory = _episode(log, hits={QUERY: (NoteHit(NOTE_B, "note-b", 1.0),)})
    protocol = QueryProtocol(
        memory=memory,
        reach=_reach(),
        namer=_RaisingNamer(),      # must never be called
        deriver=_RaisingDeriver(),  # must never be called
    )

    result = protocol.ask(_request())

    assert result.memory.short_circuited  # memory DID decide the episode
    assert result.memory.claim_id == memoized_id
    assert result.statuses[memoized_id] == ANSWERING_STATUS  # the label still says so
    assert result.outcome == "abstain"
    assert result.abstention_reason == ABSTAIN_DEPENDENCY
    assert result.dependency is not None and not result.dependency.grounded
    assert result.dependency.failed_premises == (premise_id,)
    assert result.budget.total == 0  # and nothing was derived to get there


# ── clause 3: a failed refutation records the attempt and emits NO edge ──────


def test_refutation_is_recorded_as_an_attack_edge_with_a_locator(
    tmp_path: Path,
) -> None:
    log = _log(tmp_path)
    _evidence_id, rival_id = _seed_rival(log)
    protocol = _protocol(
        log, drafts=(_grounded_draft(),), verdicts=_rival_defeats_answer()
    )

    result = protocol.ask(_request())

    assert len(result.attack_edges) == 1
    attack = result.attack_edges[0]
    assert attack.op == "attack"
    assert attack.src == rival_id  # direction from the evidence, not from order
    assert attack.dst == result.derived[0].claim_id
    assert attack.evidence_locator == RIVAL_LOCATOR
    record = next(r for r in result.refutations if r.candidate_claim_id == rival_id)
    assert record.judged and record.incompatible
    assert record.direction == "b_attacks_a"
    assert record.produced_edge


def test_an_adjudicated_compatible_pair_is_recorded_and_produces_no_edge(
    tmp_path: Path,
) -> None:
    """The attempt is recorded even when it finds no disagreement.

    "No attack edge because the pair was adjudicated compatible" and "no attack
    edge because nobody looked" are different epistemic states, and only the
    first licenses an answer."""
    log = _log(tmp_path)
    _evidence_id, rival_id = _seed_rival(log)
    protocol = _protocol(log, drafts=(_grounded_draft(),))  # empty verdict table

    result = protocol.ask(_request())

    assert result.outcome == "answer"
    assert result.attack_edges == ()
    assert any(
        record.candidate_claim_id == rival_id
        and record.judged
        and not record.incompatible
        for record in result.refutations
    )
    assert result.budget.refutation_judgements >= 1


def test_an_unavailable_judge_emits_no_edge_and_records_the_absence(
    tmp_path: Path,
) -> None:
    """Absence of adjudicated evidence is not evidence of disagreement."""

    def _silent(a: DKSArgument, b: DKSArgument) -> None:
        return None

    log = _log(tmp_path)
    _seed_rival(log)
    protocol = QueryProtocol(
        memory=_episode(log),
        reach=_reach(),
        namer=TableRelationNamer({QUERY: RelationNaming(RELATION)}),
        deriver=TableClaimDeriver({QUERY: (_grounded_draft(),)}),
        judge=_silent,
    )

    result = protocol.ask(_request())

    assert result.outcome == "answer"
    assert result.attack_edges == ()
    assert result.refutations and not any(r.judged for r in result.refutations)


def test_the_refutation_model_budget_is_capped_per_query(tmp_path: Path) -> None:
    log = _log(tmp_path)
    drafts: list[ClaimDraft] = []
    for index in range(6):
        drafts.append(
            ClaimDraft(
                derivation_id=f"derivation-candidate-{index}",
                text=f"{RIVAL_TEXT} variant {index}",
                note_id=NOTE_B,
                locator=f"anchor||candidate-{index}|0",
                provenance="constructed",
            )
        )
    log.append(tuple(drafts))
    protocol = _protocol(log, drafts=(_grounded_draft(),), refutation_budget=2)

    result = protocol.ask(_request())

    assert result.budget.refutation_judgements == 2
    assert result.budget.refutation_truncated
    assert "refutation:budget_exhausted" in result.diagnostics
    # one relation naming + k claim reads + a bounded refutation — a constant,
    # not a call per candidate pair.
    assert result.budget.relation_namings == 1
    assert result.budget.total == 1 + result.budget.claim_reads + 2


# ── clause 4: the abstention rate is BOUNDED ────────────────────────────────


def _question_set(tmp_path: Path) -> list[QueryResult]:
    """Four questions: two answerable, one disputed, one uncitable."""
    answer_log = _log(tmp_path / "q1")
    second_log = _log(tmp_path / "q2")
    conflict_log = _log(tmp_path / "q3")
    _seed_rival(conflict_log)
    abstain_log = _log(tmp_path / "q4")
    return [
        _protocol(answer_log, drafts=(_grounded_draft(),)).ask(_request()),
        _protocol(second_log, drafts=(_grounded_draft(),)).ask(_request()),
        _protocol(
            conflict_log, drafts=(_grounded_draft(),), verdicts=_rival_defeats_answer()
        ).ask(_request()),
        _protocol(abstain_log, drafts=(_grounded_draft(groundings=False),)).ask(
            _request()
        ),
    ]


def test_the_abstention_rate_over_a_question_set_is_bounded(tmp_path: Path) -> None:
    tally = tally_outcomes(_question_set(tmp_path))

    assert tally.total == 4
    assert (tally.answers, tally.conflicts, tally.abstentions) == (2, 1, 1)
    assert tally.abstention_rate == 0.25
    assert tally.within_abstention_bound(0.5)
    # a surfaced conflict IS a decision, so it counts on the decided side
    assert tally.decided_rate == 0.75


def test_an_abstain_always_implementation_fails_the_same_bound(
    tmp_path: Path,
) -> None:
    """The guard on clause 4: the bound must be falsifiable.

    "Returns an answer or an abstention" is trivially satisfied by always
    abstaining, so this runs a protocol that derives nothing over the same set
    and asserts it FAILS the bound the honest one passes."""
    always_abstains = [
        _protocol(_log(tmp_path / f"a{index}"), drafts=()).ask(_request())
        for index in range(4)
    ]

    tally = tally_outcomes(always_abstains)

    assert tally.abstentions == 4
    assert tally.abstention_rate == 1.0
    assert not tally.within_abstention_bound(0.5)
    assert not tally.within_abstention_bound()


def test_an_empty_question_set_is_not_a_passing_measurement() -> None:
    """A protocol nobody measured is not a protocol that cleared the bound."""
    assert not OutcomeTally().within_abstention_bound(0.5)
    assert OutcomeTally().abstention_rate == 0.0


# ── clause 4b: the bound over a MULTI-QUESTION FIXTURE (not a measurement) ───
#
# What follows is a FIXTURE, and saying so is the point. The outcome of each
# question is authored here — three located answers, one surfaced conflict, two
# abstentions for two different reasons — so the number below bounds the rate the
# protocol computes over an authored distribution and NOTHING ELSE. It is not a
# corpus measurement, and it must not be quoted as one.
#
# What is genuinely missing, stated as the missing thing rather than as a phase
# name: (a) an EXTERNAL ANSWER PATH over a real vault — the answer path this
# protocol would be compared against lives in another package, and the wiring
# between them (an `ask` tool over the boundary) does not exist here; and (b)
# HUMAN LABELS for what a correct located answer is, without which the grounding
# rate and the connected-reasoning rate cannot be scored at all and an LLM judge
# would only move the unlabelled question one layer down. Neither is a code gap in
# this repository, and no synthetic fixture substitutes for either.

FIXTURE_QUESTIONS: tuple[str, ...] = (
    "which component holds the retention rule",
    "which component applies retention on write",
    "which component owns the retention schedule",
    "which component records the retention decision",
    "which component publishes the retention report",
    "which component archives the retention log",
)


def _fixture_question_set(tmp_path: Path) -> list[QueryResult]:
    """Six distinct queries with an authored outcome each, one log apiece."""
    logs = [_log(tmp_path / f"fixture-{index}") for index in range(6)]
    _seed_rival(logs[3])  # the corpus already disagrees on question 4
    answerable = [
        _protocol(log, query=query, drafts=(_grounded_draft(),)).ask(
            _request(query=query)
        )
        for log, query in zip(logs[:3], FIXTURE_QUESTIONS[:3])
    ]
    conflicted = _protocol(
        logs[3],
        query=FIXTURE_QUESTIONS[3],
        drafts=(_grounded_draft(),),
        verdicts=_rival_defeats_answer(),
    ).ask(_request(query=FIXTURE_QUESTIONS[3]))
    uncited = _protocol(
        logs[4],
        query=FIXTURE_QUESTIONS[4],
        drafts=(_grounded_draft(groundings=False),),
    ).ask(_request(query=FIXTURE_QUESTIONS[4]))
    unnamed = _protocol(
        logs[5],
        query=FIXTURE_QUESTIONS[5],
        drafts=(_grounded_draft(),),
        namer=TableRelationNamer({}),
    ).ask(_request(query=FIXTURE_QUESTIONS[5]))
    return [*answerable, conflicted, uncited, unnamed]


def test_the_abstention_rate_over_the_fixture_question_set_is_bounded(
    tmp_path: Path,
) -> None:
    """The bound, over six distinct queries — a FIXTURE, honestly labelled.

    The falsifiability guard travels with it: the same six queries run through a
    protocol that derives nothing must FAIL the same bound, so a passing number
    here cannot be produced by abstaining."""
    results = _fixture_question_set(tmp_path)
    tally = tally_outcomes(results)

    assert tally.total == len(FIXTURE_QUESTIONS) == 6
    assert (tally.answers, tally.conflicts, tally.abstentions) == (3, 1, 2)
    assert {result.query for result in results} == set(FIXTURE_QUESTIONS)
    assert tally.abstention_rate == pytest.approx(1 / 3)
    assert tally.within_abstention_bound(0.5)
    assert tally.decided_rate == pytest.approx(2 / 3)
    # the two abstentions are for two DIFFERENT recorded reasons, never a blank
    reasons = {r.abstention_reason for r in results if r.outcome == "abstain"}
    assert reasons == {ABSTAIN_UNGROUNDED, ABSTAIN_NO_RELATION}

    abstain_always = [
        _protocol(_log(tmp_path / f"empty-{index}"), query=query, drafts=()).ask(
            _request(query=query)
        )
        for index, query in enumerate(FIXTURE_QUESTIONS)
    ]
    empty = tally_outcomes(abstain_always)

    assert empty.abstention_rate == 1.0
    assert not empty.within_abstention_bound(0.5)


# ── clause 5: a memory hit short-circuits derivation ────────────────────────


def test_a_memory_hit_answers_without_deriving_anything(tmp_path: Path) -> None:
    log = _log(tmp_path)
    evidence_id, rival_id = _seed_rival(log)  # a warranted memoized claim
    memory = _episode(log, hits={QUERY: (NoteHit(NOTE_B, "note-b", 1.0),)})
    protocol = QueryProtocol(
        memory=memory,
        reach=_reach(),
        namer=_RaisingNamer(),      # must never be called
        deriver=_RaisingDeriver(),  # must never be called
    )

    result = protocol.ask(_request())

    assert result.outcome == "answer"
    assert result.memory.short_circuited
    assert result.memory.cache_hit
    assert result.memory.claim_id in {evidence_id, rival_id}
    assert result.answer is not None and result.answer.locator
    # the cache path ran the dependency validator too, and it passed: the rival's
    # own premise is anchored and undefeated.
    assert result.dependency is not None and result.dependency.grounded
    # the model budget of a cache hit is zero — that is the point of consulting
    # memory before deriving.
    assert result.budget == ModelBudget()
    assert result.budget.total == 0
    assert result.reach is None
    assert result.derived == ()
    assert result.proposals == ()


def test_an_indecisive_memory_hit_does_not_short_circuit(tmp_path: Path) -> None:
    """A ``proposed`` memoized claim would abstain, so it must not pre-empt a
    fresh derivation — a cache that costs recall is not a cache."""
    log = _log(tmp_path)
    log.append(
        (
            ClaimDraft(
                derivation_id="derivation-unsupported",
                text="An unsupported note about retention.",
                note_id=NOTE_B,
                locator="anchor||unsupported|0",
                provenance="constructed",
            ),
        )
    )
    memory = _episode(log, hits={QUERY: (NoteHit(NOTE_B, "note-b", 1.0),)})
    protocol = _protocol(log, drafts=(_grounded_draft(),), memory=memory)

    result = protocol.ask(_request())

    assert result.memory.cache_hit          # memory answered the READ
    assert not result.memory.short_circuited  # but not the QUESTION
    assert result.outcome == "answer"
    assert result.budget.total > 0


# ── the grounding pre-condition: default OFF, and un-calibrated ─────────────


def test_the_grounding_precondition_is_off_by_default(tmp_path: Path) -> None:
    log = _log(tmp_path)

    result = _protocol(log, drafts=(_grounded_draft(),)).ask(_request())

    assert GroundingPolicy().enabled is False
    assert result.grounding is not None
    assert result.grounding.enabled is False
    assert result.grounding.ran is False


def test_an_enabled_uncalibrated_gate_admits_only_a_lexically_supported_claim(
    tmp_path: Path,
) -> None:
    """The certificate gates ADMISSION, and its verdict carries the A7.5 caveat."""
    log = _log(tmp_path)
    protocol = _protocol(
        log,
        drafts=(_grounded_draft(),),
        grounding=GroundingPolicy(
            enabled=True,
            thresholds=uncalibrated_thresholds(0.5),
            domain=UNCALIBRATED_DOMAIN,
        ),
    )

    result = protocol.ask(_request())

    assert result.grounding is not None and result.grounding.ran
    assert result.grounding.admitted == (result.derived[0].claim_id,)
    assert result.grounding.rejected == ()
    assert result.grounding.notice == A7_5_UNCALIBRATED_NOTICE
    assert result.outcome == "answer"


def test_an_uncalibrated_gate_pointed_at_a_real_domain_abstains_on_everything(
    tmp_path: Path,
) -> None:
    """Why the gate is not the default: fail-closed means abstain-always.

    ``certify`` refuses any domain outside its calibrated set, so un-calibrated
    thresholds aimed at production traffic reject every claim — which would make
    this phase the abstain-always implementation its own acceptance test is
    written to fail."""
    log = _log(tmp_path)
    protocol = _protocol(
        log,
        drafts=(_grounded_draft(),),
        grounding=GroundingPolicy(
            enabled=True,
            thresholds=uncalibrated_thresholds(0.5),
            domain="a_real_domain",
        ),
    )

    result = protocol.ask(_request())

    assert result.outcome == "abstain"
    assert result.abstention_reason == ABSTAIN_GROUNDING
    assert result.grounding is not None and result.grounding.rejected


def test_enabling_the_gate_without_thresholds_is_refused(tmp_path: Path) -> None:
    """There is no default threshold, because a default threshold is a
    calibration claim."""
    log = _log(tmp_path)
    protocol = _protocol(
        log, drafts=(_grounded_draft(),), grounding=GroundingPolicy(enabled=True)
    )

    with pytest.raises(QueryProtocolError, match="calibration claim"):
        protocol.ask(_request())


# ── validate_claims is wired, and opt-in ────────────────────────────────────


def test_nothing_is_accepted_while_the_validator_is_not_asked_for(
    tmp_path: Path,
) -> None:
    log = _log(tmp_path)

    result = _protocol(log, drafts=(_grounded_draft(),)).ask(_request())

    assert result.validation is None
    assert result.acceptance is not None
    assert result.acceptance.status == "dialectically_adequate"


def test_the_independent_validator_makes_the_accepted_branch_reachable(
    tmp_path: Path,
) -> None:
    """The wiring of ``validate_claims`` — inert until this phase called it.

    The four computed statuses are untouched: acceptance is a SECOND axis over
    the same Dung label, and this is the one input it was written to wait for."""
    log = _log(tmp_path)
    protocol = _protocol(
        log,
        drafts=(_grounded_draft(),),
        validation=ValidationPolicy(
            enabled=True,
            thresholds=uncalibrated_thresholds(0.0),
            domain=UNCALIBRATED_DOMAIN,
        ),
    )

    result = protocol.ask(_request())

    assert result.validation is not None
    assert result.validation.validated
    assert result.validation.notice == A7_5_UNCALIBRATED_NOTICE
    assert result.acceptance is not None
    assert result.acceptance.status == "accepted"
    assert result.acceptance.label == "in"
    assert result.statuses[result.derived[0].claim_id] == "warranted"


def test_a_validated_answer_becomes_promotion_eligible(tmp_path: Path) -> None:
    log = _log(tmp_path)
    capability = DKSQueryCapability(
        _protocol(
            log,
            drafts=(_grounded_draft(),),
            validation=ValidationPolicy(
                enabled=True,
                thresholds=uncalibrated_thresholds(0.0),
                domain=UNCALIBRATED_DOMAIN,
            ),
        )
    )

    envelope = capability.invoke(_request())

    assert envelope.promotion_eligibility == "eligible"


# ── the integration seam: one capability, one commit tail, no parallel path ──


def test_the_query_capability_registers_on_the_existing_registry(
    tmp_path: Path,
) -> None:
    log = _log(tmp_path)
    register_dks_query(
        lambda: DKSQueryCapability(_protocol(log, drafts=(_grounded_draft(),)))
    )

    assert is_capability_registered(DKS_QUERY)
    capability = get_capability_factory(DKS_QUERY)()
    assert isinstance(capability, Capability)


def test_the_capability_is_driven_through_the_executor_and_never_writes(
    tmp_path: Path,
) -> None:
    log = _log(tmp_path)
    before = len(log.read_claims())
    executor = DKSExecutor(DKSQueryCapability(_protocol(log, drafts=(_grounded_draft(),))))

    candidate = executor.execute(_request(), base_snapshot_id="pinned")

    assert isinstance(candidate, DKSCandidate)
    assert candidate.base_snapshot_id == "pinned"
    assert candidate.result.effects  # proposals for the commit tail
    assert len(log.read_claims()) == before  # nothing was written
    for surface in ("commit", "promote", "write", "append"):
        assert not hasattr(executor, surface)


def test_the_candidate_pin_is_the_edge_set_digest_the_episode_read_at(
    tmp_path: Path,
) -> None:
    """The snapshot pin already exists in the contract; this phase fills it in
    rather than carrying a second pin of its own."""
    log = _log(tmp_path)
    protocol = _protocol(log, drafts=(_grounded_draft(),))
    envelope = DKSQueryCapability(protocol).invoke(_request())

    candidate = protocol.memory.pinned_candidate(envelope)

    assert candidate.base_snapshot_id == protocol.memory.base_snapshot_id
    assert candidate.base_snapshot_id == envelope.payload.base_snapshot_id


def test_the_kernel_proposes_effects_and_the_log_is_untouched(tmp_path: Path) -> None:
    log = _log(tmp_path)
    protocol = _protocol(log, drafts=(_grounded_draft(),))

    result = protocol.ask(_request())

    assert log.read_claims() == ()
    assert log.read_edges() == ()
    assert len(result.effects) == len(result.proposals)
    # the episode's batch is staged for ONE append the caller makes later
    assert len(protocol.memory.staged) == len(result.proposals)
    for surface in ("commit", "write", "append_batch"):
        assert not hasattr(protocol, surface)


def test_lane_routing_is_unchanged_by_the_query_capability(tmp_path: Path) -> None:
    """P8 is additive: no lane, flag or heuristic selects ``dks_query``."""
    from tessellum.composer.digestion import PHASE_SKILLS

    skills = tmp_path / "skills"
    skills.mkdir()
    for phase in ("plan", "augment", "review", "execute"):
        (skills / f"{PHASE_SKILLS[phase]}.md").write_text("# skill\n", encoding="utf-8")

    for lane in ("papers", "book", "general"):
        assert route_lane(lane, skills_dir=skills).capability == NATIVE_DIGESTION


def test_replaying_a_query_re_proposes_the_same_rows(tmp_path: Path) -> None:
    """Content-derived ids: a retried episode is a no-op, not a duplicate."""
    first = _protocol(_log(tmp_path / "one"), drafts=(_grounded_draft(),)).ask(
        _request()
    )
    second = _protocol(_log(tmp_path / "two"), drafts=(_grounded_draft(),)).ask(
        _request()
    )

    assert first.derived[0].claim_id == second.derived[0].claim_id
    assert first.base_snapshot_id == second.base_snapshot_id
    capability_first = DKSQueryCapability(
        _protocol(_log(tmp_path / "three"), drafts=(_grounded_draft(),))
    )
    capability_second = DKSQueryCapability(
        _protocol(_log(tmp_path / "four"), drafts=(_grounded_draft(),))
    )
    assert (
        capability_first.invoke(_request()).replay_token
        == capability_second.invoke(_request()).replay_token
    )


# ── the MCP tool is a THIN CALLER of the capability ─────────────────────────


def test_the_mcp_tool_drives_the_registered_capability(tmp_path: Path) -> None:
    from tessellum.mcp.server import _dispatch

    log = _log(tmp_path)
    _seed_rival(log)
    register_dks_query(
        lambda: DKSQueryCapability(
            _protocol(
                log,
                drafts=(_grounded_draft(),),
                verdicts=_rival_defeats_answer(),
                resolver=_resolver(),
            )
        )
    )

    # a JSON payload carries a MENTION, not a Resolution — step 1 runs inside
    # the capability, which is what makes the tool a thin caller.
    payload = _dispatch(
        "tessellum_dks_query", {"query": QUERY, "mention": MENTION}
    )

    assert payload["capability"] == DKS_QUERY
    assert payload["outcome"] == "conflict"
    assert len(payload["conflict"]) == 2
    assert all(chain["locator"] for chain in payload["conflict"])
    assert payload["grounded"] is True
    assert payload["wrote_anything"] is False
    assert payload["model_budget"]["total"] > 0


def test_the_mcp_tool_has_no_fallback_answer_path(monkeypatch) -> None:
    from tessellum.mcp.server import _dispatch
    from tessellum.runtime import routing

    monkeypatch.setattr(routing, "_CAPABILITY_REGISTRY", {})

    payload = _dispatch("tessellum_dks_query", {"query": QUERY})

    assert "error" in payload
    assert "register_dks_query" in payload["hint"]
    assert "outcome" not in payload


# ── the properties the composition rests on ─────────────────────────────────


def test_the_module_never_imports_the_runtime() -> None:
    source = QUERY_PROTOCOL_SOURCE.read_text(encoding="utf-8")
    code = "\n".join(
        line for line in source.splitlines() if not line.lstrip().startswith("#")
    )
    body = code.split('"""', 2)[-1]  # drop the module docstring, which names it
    assert "tessellum.runtime" not in body
    assert "import sqlite3" not in body


def test_a_derived_claim_is_anchored_by_content_not_by_position() -> None:
    """Identity survives an insertion above the span — the recurrence
    prerequisite."""
    first = derive_claim(_grounded_draft())
    second = derive_claim(_grounded_draft())

    assert first.claim.derivation_id == second.claim.derivation_id
    assert first.claim_id == second.claim_id
    assert first.locator.startswith("anchor|")
    # a claim never supports itself: the grounding cites a different span
    assert first.supports[0].src != first.claim_id
    assert first.supports[0].dst == first.claim_id


def test_a_grounding_that_would_cite_the_claims_own_span_is_dropped() -> None:
    """A claim supporting itself is a circular justification, not a citation."""
    draft = DerivedClaimDraft(
        text=ANSWER_SPAN,  # identical text
        note_id=NOTE_A,
        span_text=ANSWER_SPAN,
        groundings=(Grounding(note_id=NOTE_A, span_text=ANSWER_SPAN),),
    )

    derived = derive_claim(draft)

    assert derived.supports == ()
    assert derived.grounding_claims == ()
    assert not derived.grounded


def test_a_request_refuses_an_unknown_field() -> None:
    """A silently dropped field would look like a reach that found nothing."""
    assert QueryRequest.from_mapping({"query": QUERY}).query == QUERY
    assert QueryRequest.from_mapping(
        {"query": QUERY, "note_ids": [NOTE_A]}
    ).note_ids == (NOTE_A,)
    with pytest.raises(QueryProtocolError, match="unknown request field"):
        QueryRequest.from_mapping({"query": QUERY, "topk": 3})
    with pytest.raises(QueryProtocolError, match="needs a 'query'"):
        QueryRequest.from_mapping({"mention": "x"})


def test_the_episode_cannot_read_its_own_staged_proposal_as_evidence(
    tmp_path: Path,
) -> None:
    """Rule 4 survives this phase: the pinned snapshot never grows mid-episode.

    The decision is drawn from the snapshot PLUS the episode's own batch — the
    boundary's consequence check — but no READ call can see the batch, so the
    next query in the same episode cannot cite the previous one's conclusion."""
    log = _log(tmp_path)
    protocol = _protocol(log, drafts=(_grounded_draft(),))

    result = protocol.ask(_request())
    derived_id = result.derived[0].claim_id

    assert protocol.memory.status(derived_id) == "unknown"
    assert protocol.memory.snapshot.claim(derived_id) is None
    assert result.statuses[derived_id] == "warranted"
