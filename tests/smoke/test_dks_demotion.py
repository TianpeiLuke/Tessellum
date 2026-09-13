"""P10 smoke tests — the periodic re-derivation gate, its three triggers, and the
five outcomes it must not collapse into "false".

Covers each clause of the phase's acceptance line:

1. **Three separate tests, one per trigger.** (a) A promoted claim whose
   **re-derivation fails** is demoted **even with no attack against it** — proved
   against the real computed status, so "no attack" is a property of the edge set
   rather than a stubbed label. (b) A claim under a **surviving** contradiction is
   retracted while one whose **attacker is itself defeated is NOT** — the
   reinstatement case, driven from a folded log so the reinstatement is *computed*
   rather than asserted, and joined by the undecided case, which is quarantined
   because *"attacked" does not mean "retracted"*. (c) A claim whose
   **independence drops below floor** is demoted.
2. **The counter's distinguishing fixtures**, which are the point of A10: a
   **valid paraphrase** is not demoted; **two legitimate abstractions** of the
   same sources do not demote each other (both directions); a **reproducible but
   contradicted** claim is separated from a non-reproducible one, because a frozen
   model reproducing a source's *error* faithfully is evidence of fidelity and not
   of truth; an ungrounded claim is a **grounding failure** rather than a
   reproduction failure; and a check run against a **moved base** is withheld
   rather than read as a refutation.
3. **History survives every demotion** — the ledger is append-only, the ledger
   handed to a sweep is unchanged by it, a revoked certificate leaves the issued
   one readable, and the retracted claim's own row is never touched.
4. **The recovery path restores a wrongly-demoted claim** — by APPENDING an
   attack on the retraction, which the real fixed point turns back into a
   ``warranted`` verdict, with both acts still in the ledger afterwards.

Plus the properties those clauses rest on: the model is a pinned (frozen)
injected seam, the promoted claim is **suppressed** from what the model sees, the
comparison and all three triggers are arithmetic, an inconclusive finding
**quarantines or requests review with a recorded reason** instead of demoting,
nothing is ever hard-deleted, the gate proposes effects instead of writing, and
the schedule makes the gate required rather than available.

All pure; no network, no model, no disk.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, fields
from pathlib import Path

import pytest

from tessellum.dks.demotion import (
    ACTION_SEVERITY,
    DEFAULT_DEMOTION_POLICY,
    DISPOSITIONS,
    CitedSource,
    DemotionEntry,
    DemotionLedger,
    DemotionOutcome,
    DemotionPolicy,
    FrozenModelError,
    FrozenReDerivationModel,
    GateNotArmedError,
    INDEPENDENCE_FLOOR,
    ORIGIN_DEMOTION,
    ORIGIN_RECOVERY,
    OUTCOME_FAILED_GENERALISATION,
    OUTCOME_FAILED_REPRODUCTION,
    OUTCOME_GROUNDING_FAILURE,
    OUTCOME_STALE_EVIDENCE,
    OUTCOME_SURVIVING_CONTRADICTION,
    OUTCOMES,
    PromotedClaimRecord,
    REGENERATION_COMPARISON_DEVIATION,
    REGENERATION_FLOOR,
    SOURCE_SUPPORT_FLOOR,
    ReDerivationGate,
    ReDerivationOutput,
    ReDerivationRequest,
    RecoveryError,
    ScriptedReDerivationModel,
    StaticIndependenceSource,
    StaticSourceReader,
    StaticStatusSource,
    SuppressionError,
    TRIGGER_CONTRADICTION,
    TRIGGER_INDEPENDENCE_BELOW_FLOOR,
    TRIGGER_REDERIVATION_FAILURE,
    TRIGGERS,
    VerdictQueryStatusSource,
    agreement,
    as_capability_result,
    build_request,
    check_evidence_freshness,
    check_regeneration,
    down_rank_order,
    due_at,
    due_records,
    entry_for_review,
    independence_from_events,
    is_due,
    recover,
    recovery_capability_result,
    require_armed,
    require_frozen,
    retraction_proposals,
    source_support,
    strongest_action,
    strongest_disposition,
    tokenize,
)
from tessellum.dks.elevation import (
    CertificateError,
    MaturityProfile,
    RewardInputs,
    issue_certificate,
    revoke,
)
from tessellum.dks.memory_port import ClaimProposal, EdgeProposal
from tessellum.dks.memory_tiers import FeedbackEvent
from tessellum.dks.status import EdgeSet, StatusQuery, compute_statuses

SRC = Path(__file__).resolve().parents[2] / "src" / "tessellum"
DEMOTION_SOURCE = SRC / "dks" / "demotion.py"

DAY = 86400.0
CLAIM_TEXT = "The archived records are retained for thirty days after closure."
SOURCE_TEXT = "Closure starts a thirty day clock, and an archived record is kept until it expires."
PARAPHRASE = "Archived records are retained thirty days after a case closes."
CONTRADICTION_TEXT = "Nothing is kept: every archived record is purged on arrival."
INVERSION = "The archived records are not retained for thirty days after closure."

# One source span, and TWO abstractions of it that are both legitimate. Neither is
# a paraphrase of the other (they disagree below the regeneration floor) and both
# stay inside the span, which is the shape the counter raised: a frozen model that
# produces the second when the first was promoted has not refuted anything.
SHARED_SOURCE = (
    "A closed case is archived on the day it closes, and the archive keeps each "
    "record for thirty days before the retention clock expires and the record is "
    "removed."
)
ABSTRACTION_A = "Archived records are kept for thirty days after a case is closed."
ABSTRACTION_B = (
    "The retention clock for an archived record expires thirty days after closing."
)

# A source that is simply WRONG, and a claim that restates it faithfully. The
# frozen model reproduces the error perfectly, which is why reproduction is
# evidence of fidelity and not of truth.
ERRONEOUS_SOURCE = (
    "The retention window is ninety days, and no record leaves the archive before "
    "that window closes."
)
FAITHFUL_CLAIM = "The retention window is ninety days for every archived record."


# ── in-memory fixtures: every collaborator is a port ────────────────────────


@dataclass(frozen=True)
class _C:
    """A :class:`~tessellum.dks.status.ClaimView`."""

    claim_id: str
    provenance: str = "constructed"


@dataclass(frozen=True)
class _E:
    """An :class:`~tessellum.dks.status.EdgeView`."""

    op: str
    src: str
    dst: str
    seq: int
    evidence_locator: str | None = "note-1#h2:Retention"
    origin: str = "query"


def _record(**overrides: object) -> PromotedClaimRecord:
    """A promoted claim record with a plausible, fully-populated handle."""
    base = dict(
        claim_id="claim-retention",
        derivation_id="derivation-retention",
        text=CLAIM_TEXT,
        note_id="note-1",
        locator="h2:Retention",
        status_at_promotion="warranted",
        episode_ids=("episode-1", "episode-2", "episode-3"),
        occurrences=3,
        promoted_at=0.0,
        last_checked_at=None,
        base_snapshot_id="snapshot-1",
    )
    base.update(overrides)
    return PromotedClaimRecord(**base)  # type: ignore[arg-type]


def _frozen(outputs: dict[str, str] | None = None) -> FrozenReDerivationModel:
    """The deterministic reference model, pinned — the only way to run the gate."""
    return FrozenReDerivationModel(
        ScriptedReDerivationModel(outputs or {}),
        model_id="reference-rederiver-1",
        frozen_at=1.0,
        corpus_snapshot_id="snapshot-0",
    )


def _sources(text: str = SOURCE_TEXT) -> StaticSourceReader:
    return StaticSourceReader(
        {"claim-retention": (CitedSource("note-1", "h2:Retention", text),)}
    )


def _gate(
    *,
    outputs: dict[str, str] | None = None,
    statuses: object | None = None,
    contexts: tuple[str, ...] = ("episode-1", "episode-2", "episode-3"),
    policy: DemotionPolicy = DEFAULT_DEMOTION_POLICY,
    sources: StaticSourceReader | None = None,
) -> ReDerivationGate:
    return ReDerivationGate(
        model=_frozen(outputs if outputs is not None else {"derivation-retention": PARAPHRASE}),
        sources=sources or _sources(),
        statuses=statuses or StaticStatusSource({"claim-retention": "warranted"}),
        independence=StaticIndependenceSource({"derivation-retention": contexts}),
        policy=policy,
    )


def _live_log(*, attacked: bool) -> EdgeSet:
    """The real claim/edge set the computed status runs over.

    ``claim-retention`` is supported (therefore ``warranted``); ``attacked`` adds
    one real ``attack`` edge, which is the only difference between the (a) and
    (b) trigger tests."""
    claims = [_C("claim-retention"), _C("support-1")]
    edges = [_E("support", "support-1", "claim-retention", 1)]
    if attacked:
        claims.append(_C("counter-1"))
        edges.append(_E("attack", "counter-1", "claim-retention", 2))
    return EdgeSet(claims=tuple(claims), edges=tuple(edges))


def _status_source(edge_set: EdgeSet) -> VerdictQueryStatusSource:
    """The status phase's own query, adapted to this gate's read port."""
    return VerdictQueryStatusSource(StatusQuery(edge_set))


# ── the Dependency Rule, and "never writes / never deletes" ─────────────────


def test_the_demotion_module_is_pure_and_deletes_nothing() -> None:
    """DKS stays pure, and the gate has no write or delete path at all.

    Both are structural, so they are asserted against the source: a demotion that
    could delete would make the ledger's history a courtesy, and a module that
    imported the runtime would turn the kernel into a runtime plugin.
    """
    source = DEMOTION_SOURCE.read_text(encoding="utf-8")
    assert "tessellum.runtime" not in source
    assert not re.search(r"^\s*(from|import)\s+.*\bruntime\b", source, re.MULTILINE)
    for statement in ("DELETE", "UPDATE ", "INSERT", "DROP", "executescript"):
        assert statement not in source, f"demotion.py must not {statement.strip()}"
    assert "sqlite3" not in source
    assert "open(" not in source


def test_the_ledger_has_no_removal_surface() -> None:
    """Append-only as a TYPE: ``record`` is the only mutator and it returns a new
    ledger, so no caller can shorten a history."""
    for forbidden in ("delete", "remove", "pop", "clear", "evict", "prune"):
        assert not hasattr(DemotionLedger, forbidden)
    ledger = DemotionLedger()
    entry = DemotionEntry(
        kind="demotion", claim_id="c", derivation_id="d", at=1.0,
        triggers=(TRIGGER_CONTRADICTION,), action="flag",
    )
    grown = ledger.record(entry)
    assert len(ledger) == 0 and len(grown) == 1  # the original is untouched
    assert grown.record(entry) is grown  # content-addressed: a replay is a no-op


# ── step 2: the model is an injected, PINNED seam ───────────────────────────


def test_an_unpinned_model_cannot_run_the_gate() -> None:
    """Frozen means pinned, and the pin is enforced rather than requested.

    An unpinned model may re-tune on the corpus it is checking, regenerate a
    promoted claim *from the promotion*, and certify itself — so the bare
    reference model is refused until it is wrapped.
    """
    bare = ScriptedReDerivationModel({"derivation-retention": CLAIM_TEXT})
    with pytest.raises(FrozenModelError, match="not frozen"):
        require_frozen(bare)
    with pytest.raises(FrozenModelError):
        ReDerivationGate(
            model=bare,  # type: ignore[arg-type]
            sources=_sources(),
            statuses=StaticStatusSource({}),
            independence=StaticIndependenceSource({}),
        )
    assert require_frozen(_frozen()) == ("reference-rederiver-1", 1.0)
    with pytest.raises(FrozenModelError, match="model_id"):
        FrozenReDerivationModel(bare, model_id="   ")


# ── step 1: the promoted claim is SUPPRESSED ────────────────────────────────


def test_the_request_cannot_carry_the_promoted_claim() -> None:
    """Suppression is a property of the request's shape, not a discipline.

    There is no field for the claim's text and none for its ``claim_id``; the
    ``derivation_id`` that is there is a hash of ``(note_id, span_locator)`` and
    asserts nothing, so a model cannot read the answer out of it.
    """
    names = {f.name for f in fields(ReDerivationRequest)}
    assert names == {"derivation_id", "note_id", "sources", "question"}
    record = _record()
    request = build_request(record, _sources().cited_sources(record.claim_id))
    assert record.text not in str(request)
    assert record.claim_id not in str(request)


def test_suppression_refuses_a_leaked_claim_and_a_self_citation() -> None:
    """Two real leaks: the claim in the question, and the claim as its own source.

    A model shown the answer measures nothing, and an abstraction cited as its
    own evidence regenerates forever.
    """
    record = _record()
    with pytest.raises(SuppressionError, match="question"):
        build_request(
            record,
            _sources().cited_sources(record.claim_id),
            question=f"Does the span support: {CLAIM_TEXT}",
        )
    with pytest.raises(SuppressionError, match="own"):
        build_request(
            record, (CitedSource("note-1", "h2:Retention", CLAIM_TEXT.upper()),)
        )
    # A source that merely CONTAINS the claim is grounding, not self-citation.
    quoted = CitedSource("note-1", "h2:Retention", f"The policy states: {CLAIM_TEXT}")
    assert build_request(record, (quoted,)).sources == (quoted,)


# ── step 3: the comparison stays arithmetic ─────────────────────────────────


def test_the_regeneration_comparison_is_arithmetic() -> None:
    """A token-overlap ratio against a floor — recomputable, and model-free.

    The model produces text; the verdict is a comparison. Both directions are
    exercised: a paraphrase that shares enough vocabulary regenerates, a
    contradiction that shares little does not, and an abstention is a failure.
    """
    assert agreement(CLAIM_TEXT, CLAIM_TEXT) == 1.0
    assert agreement("", "") == 1.0
    assert agreement(CLAIM_TEXT, "") == 0.0
    assert agreement(CLAIM_TEXT, PARAPHRASE) >= REGENERATION_FLOOR
    assert agreement(CLAIM_TEXT, CONTRADICTION_TEXT) < REGENERATION_FLOOR
    # Punctuation and casing are not disagreements.
    assert tokenize("Thirty days.") == tokenize("thirty  DAYS")

    record = _record()
    passing = check_regeneration(
        record,
        model=_frozen({"derivation-retention": PARAPHRASE}),
        sources=_sources().cited_sources(record.claim_id),
    )
    assert passing.regenerated and not passing.exact
    assert passing.model_id == "reference-rederiver-1"

    failing = check_regeneration(
        record,
        model=_frozen({"derivation-retention": CONTRADICTION_TEXT}),
        sources=_sources().cited_sources(record.claim_id),
    )
    assert failing.failed and not failing.abstained

    abstained = check_regeneration(
        record, model=_frozen({}), sources=_sources().cited_sources(record.claim_id)
    )
    assert abstained.failed and abstained.abstained

    unsourced = check_regeneration(record, model=_frozen(), sources=())
    assert unsourced.failed and unsourced.source_count == 0


def test_the_lexical_proxy_records_its_own_limit() -> None:
    """The comparison is lexical, and this is what that costs — asserted, not hidden.

    A regeneration that reuses the claim's vocabulary while INVERTING the
    assertion passes this gate. That is the deviation the module records rather
    than papers over: deciding two renderings state the same fact needs the
    cross-span fact layer, which is specified and not built, and entailment is a
    separate model-backed condition at promotion time.
    """
    assert agreement(CLAIM_TEXT, INVERSION) >= REGENERATION_FLOOR
    passed = check_regeneration(
        _record(),
        model=_frozen({"derivation-retention": INVERSION}),
        sources=_sources().cited_sources("claim-retention"),
    )
    assert passed.regenerated  # the known hole, in a test rather than a comment
    for phrase in ("TOKEN OVERLAP", "entailment"):
        assert phrase in REGENERATION_COMPARISON_DEVIATION


# ── ACCEPTANCE (a): re-derivation failure, with NO attack anywhere ──────────


def test_trigger_a_rederivation_failure_demotes_an_unattacked_claim() -> None:
    """A promoted claim that no longer follows from its own sources is demoted
    **even though nothing attacks it**.

    This is the trigger an attack-driven system cannot have. The log here holds
    one ``support`` edge and no ``attack`` at all, and the real computed status
    says ``warranted`` — so the demotion is not a status flip in disguise, and it
    is not thin independence either. It is the gate scoring a produced
    abstraction for truth, which is the whole point of the phase.
    """
    edge_set = _live_log(attacked=False)
    assert compute_statuses(edge_set).statuses["claim-retention"].status == "warranted"
    assert not [e for e in edge_set.edges if e.op == "attack"]

    record = _record()
    review = _gate(
        outputs={"derivation-retention": CONTRADICTION_TEXT},
        statuses=_status_source(edge_set),
    ).review(record, now=30 * DAY)

    assert review.triggers == (TRIGGER_REDERIVATION_FAILURE,)
    assert review.status_flip.flipped is False  # nothing attacked it
    assert review.independence.below_floor is False  # three contexts still stand
    # The evidence IS there and the claim did not come back out of it — which is a
    # reproduction failure, not a grounding failure and not an alternative reading.
    assert review.outcome_kinds == (OUTCOME_FAILED_REPRODUCTION,)
    assert not review.regeneration.ungrounded
    assert not review.regeneration.alternative_abstraction
    assert review.demoted and review.promotion_eligibility == "ineligible"
    assert review.action == "flag"
    assert review.retracted  # the demotion appended a retraction
    assert as_capability_result(review).promotion_eligibility == "ineligible"


# ── ACCEPTANCE (b): a SURVIVING contradiction is retracted ──────────────────


def test_trigger_b_a_surviving_contradiction_is_retracted() -> None:
    """One appended ``attack`` that SURVIVES flips the computed status, and the gate
    retracts.

    "Nearly free" is a property of the design, not luck: status is a pure function
    of the edge set, so the contradiction trigger is a comparison of two labels.
    The attacker here is undefeated — the claim labels ``out`` — which is what makes
    the contradiction a surviving one; the companion test below is the same log with
    the attacker itself attacked, where the gate must NOT fire.

    The retraction is an APPEND — a constructed retraction claim plus a
    ``supersede`` edge carrying the check time, and the claim that grounds it — and
    the retracted claim's own row is untouched by it.
    """
    attacked = _live_log(attacked=True)
    assert compute_statuses(attacked).statuses["claim-retention"].status == "challenged"

    record = _record()
    review = _gate(
        outputs={"derivation-retention": PARAPHRASE},
        statuses=_status_source(attacked),
    ).review(record, now=30 * DAY)

    assert review.triggers == (TRIGGER_CONTRADICTION,)
    assert review.regeneration.regenerated  # it still re-derives; it is contradicted
    assert review.status_flip.status_now == "challenged"
    assert review.outcome_kinds == (OUTCOME_SURVIVING_CONTRADICTION,)
    assert review.action == "supersede_with_timestamp"

    claim_proposal, grounding, support_edge, edge_proposal = review.proposals
    assert isinstance(claim_proposal, ClaimProposal)
    assert isinstance(edge_proposal, EdgeProposal)
    assert claim_proposal.provenance == "constructed"
    assert f"t={30 * DAY:.3f}" in claim_proposal.text  # supersede-WITH-TIMESTAMP
    assert edge_proposal.op == "supersede"
    assert edge_proposal.dst == record.claim_id
    assert edge_proposal.origin == ORIGIN_DEMOTION

    # The supersession carries its own grounding, because the pre-filter admits a
    # replacement only when the replacement is itself WARRANTED: an unsupported
    # retraction is `proposed` and retires nothing, which would make the strongest
    # action silently inert.
    assert isinstance(grounding, ClaimProposal)
    assert isinstance(support_edge, EdgeProposal)
    assert support_edge.op == "support"
    assert support_edge.src == grounding.claim_id
    assert support_edge.dst == claim_proposal.claim_id

    # The retraction leaves as proposed EFFECTS for the commit tail; the gate
    # writes nothing itself.
    kinds = [effect.kind for effect in review.effects]
    assert kinds == ["claim", "claim", "edge", "edge"]

    # And the retraction actually retracts: folded into the log, the claim reads
    # `superseded`, so the read flow abstains instead of answering.
    retracted = EdgeSet(
        claims=attacked.claims
        + (_C(claim_proposal.claim_id), _C(grounding.claim_id)),
        edges=attacked.edges
        + (
            _E("support", grounding.claim_id, claim_proposal.claim_id, 3),
            _E("supersede", claim_proposal.claim_id, record.claim_id, 4),
        ),
    )
    assert compute_statuses(retracted).statuses[record.claim_id].status == "superseded"


# ── ACCEPTANCE (c): independence below floor ────────────────────────────────


def test_trigger_c_independence_below_floor_demotes() -> None:
    """A claim promoted on three contexts, now standing on one, is demoted.

    Counted over episodes, which is the weaker reading the identity phase
    recorded; the action is the mildest one, because nothing contradicted the
    claim — its evidence base thinned.
    """
    record = _record()
    review = _gate(
        outputs={"derivation-retention": PARAPHRASE}, contexts=("episode-1",)
    ).review(record, now=30 * DAY)

    assert review.triggers == (TRIGGER_INDEPENDENCE_BELOW_FLOOR,)
    assert review.outcome_kinds == (OUTCOME_STALE_EVIDENCE,)  # corroboration went
    assert review.independence.count == 1
    assert review.independence.floor == INDEPENDENCE_FLOOR
    assert review.independence.at_promotion == 3
    assert review.regeneration.regenerated and not review.status_flip.flipped
    assert review.demoted and review.promotion_eligibility == "ineligible"
    assert review.action == "down_rank"
    # A down-rank is a demotion that appends NO epistemic act: standing is a
    # projection, and demoting a projection is not an epistemic act.
    assert review.proposals == () and review.effects == ()
    assert not review.retracted

    # At the floor exactly, nothing fires.
    held = _gate(
        outputs={"derivation-retention": PARAPHRASE},
        contexts=("episode-1", "episode-2"),
    ).review(record, now=30 * DAY)
    assert held.triggers == () and held.promotion_eligibility == "eligible"


def test_independence_counts_distinct_episodes_from_a_trial_stream() -> None:
    """The independence port composes with the feedback tier's own events.

    Structural, not imported into the module: a deployment's trial stream already
    has the three attributes this counter reads. A correction flag is not a use,
    so raising one cannot inflate independence.
    """
    events = [
        FeedbackEvent(kind="trial", subject_id="d1", subject_kind="promoted_claim",
                      episode_id="e1", at=1.0),
        FeedbackEvent(kind="verdict", subject_id="d1", subject_kind="promoted_claim",
                      episode_id="e1", at=2.0, verdict="correct"),
        FeedbackEvent(kind="trial", subject_id="d1", subject_kind="promoted_claim",
                      episode_id="e2", at=3.0),
        FeedbackEvent(kind="correction_raise", subject_id="d1",
                      subject_kind="promoted_claim", episode_id="e9", at=4.0),
        FeedbackEvent(kind="trial", subject_id="other", subject_kind="promoted_claim",
                      episode_id="e3", at=5.0),
    ]
    assert independence_from_events(events, "d1") == ("e1", "e2")


# ── all three at once, and the severity rule ────────────────────────────────


def test_every_trigger_is_reported_and_the_strongest_action_wins() -> None:
    """A demotion reports every reason it happened; the severest action applies.

    Applying the mildest of several findings would keep answering from a claim
    the gate has already contradicted.
    """
    review = _gate(
        outputs={"derivation-retention": CONTRADICTION_TEXT},
        statuses=StaticStatusSource({"claim-retention": "challenged"}),
        contexts=(),
    ).review(_record(), now=30 * DAY)

    assert set(review.triggers) == TRIGGERS
    assert len(review.reasons) == 3
    # A status source that cannot report a Dung label reads as SETTLED, not as
    # undecided: quarantining every refutation whose source declines to expose its
    # internals would make the withholding state a way to never demote at all.
    assert review.status_flip.label is None and review.status_flip.settled
    assert review.demoted and review.action == "supersede_with_timestamp"
    assert ACTION_SEVERITY[review.action] == max(ACTION_SEVERITY.values())
    assert strongest_action(("down_rank", "flag")) == "flag"
    assert strongest_action(()) is None
    with pytest.raises(ValueError, match="unknown demotion action"):
        strongest_action(("hard_delete",))


def test_a_claim_the_log_no_longer_holds_reads_as_a_flip() -> None:
    """An unknown status is fail-closed: a promoted claim that cannot be found is
    not a claim that still answers. And the benign direction is not a
    contradiction — a claim that GAINED standing is reported, not demoted.

    Fail-closed, but not fail-*retracted*: not finding a claim is a finding about
    the read (a partial fold, a wrong id), so the claim is withheld with the reason
    recorded rather than retracted on evidence the gate never saw."""
    unknown = _gate(
        outputs={"derivation-retention": PARAPHRASE},
        statuses=StaticStatusSource({}),
    ).review(_record(), now=30 * DAY)
    assert unknown.triggers == (TRIGGER_CONTRADICTION,)
    assert unknown.status_flip.status_now == "unknown"
    assert unknown.outcome_kinds == (OUTCOME_STALE_EVIDENCE,)
    assert unknown.quarantined and not unknown.demoted
    assert unknown.proposals == ()  # nothing appended against a claim it cannot see
    assert unknown.promotion_eligibility == "needs_validation"  # still not promotable

    improved = _gate(
        outputs={"derivation-retention": PARAPHRASE},
        statuses=StaticStatusSource({"claim-retention": "warranted"}),
    ).review(_record(status_at_promotion="proposed"), now=30 * DAY)
    assert improved.triggers == () and improved.status_flip.improved


# ── A10: five outcomes, and an inconclusive signal does NOT demote ──────────


def _sources_for(
    record: PromotedClaimRecord, text: str, *, content_hash: str = ""
) -> StaticSourceReader:
    """One cited span for one record, at the record's own locator."""
    return StaticSourceReader(
        {
            record.claim_id: (
                CitedSource(
                    record.note_id,
                    record.locator or "h2:Retention",
                    text,
                    content_hash,
                ),
            )
        }
    )


def _gate_for(
    record: PromotedClaimRecord,
    *,
    source_text: str,
    output: str | None = None,
    statuses: object | None = None,
    contexts: tuple[str, ...] = ("episode-1", "episode-2", "episode-3"),
    content_hash: str = "",
) -> ReDerivationGate:
    """A gate wired for one specific record — for the multi-claim fixtures.

    ``output=None`` scripts nothing, so the reference model abstains."""
    return ReDerivationGate(
        model=_frozen({} if output is None else {record.derivation_id: output}),
        sources=_sources_for(record, source_text, content_hash=content_hash),
        statuses=statuses or StaticStatusSource({record.claim_id: "warranted"}),
        independence=StaticIndependenceSource({record.derivation_id: contexts}),
    )


def test_the_vocabulary_is_five_outcomes_over_three_triggers() -> None:
    """Three triggers, five outcomes, four dispositions — and only one demotes.

    The counts differ on purpose: a trigger says the gate LOOKED and found
    something, an outcome says what the finding establishes. Collapsing the two is
    exactly the overstatement this phase was corrected for."""
    assert OUTCOMES == {
        OUTCOME_STALE_EVIDENCE,
        OUTCOME_FAILED_REPRODUCTION,
        OUTCOME_SURVIVING_CONTRADICTION,
        OUTCOME_GROUNDING_FAILURE,
        OUTCOME_FAILED_GENERALISATION,
    }
    assert len(TRIGGERS) == 3 and len(OUTCOMES) == 5
    assert DISPOSITIONS == {"hold", "demote", "quarantine", "request_review"}

    # Precedence: a conclusive finding is not softened by an open question, and a
    # finding needing judgement outranks one needing only a re-check.
    assert strongest_disposition(()) == "hold"
    assert strongest_disposition(("quarantine", "request_review")) == "request_review"
    assert strongest_disposition(("request_review", "demote")) == "demote"
    with pytest.raises(ValueError, match="unknown demotion disposition"):
        strongest_disposition(("delete",))

    # Only a conclusive outcome may demote, and a conclusive one may not be
    # quietly downgraded to a withholding — the pairing is enforced, not trusted.
    with pytest.raises(ValueError, match="conclusive"):
        DemotionOutcome(
            kind="failed_reproduction",
            conclusive=False,
            disposition="demote",
            reason="x",
        )
    with pytest.raises(ValueError, match="may not be withheld"):
        DemotionOutcome(
            kind="surviving_contradiction",
            conclusive=True,
            disposition="quarantine",
            reason="x",
        )
    with pytest.raises(ValueError, match="unknown demotion outcome"):
        DemotionOutcome(
            kind="false",  # type: ignore[arg-type]
            conclusive=True,
            disposition="demote",
            reason="x",
        )


def test_a_surviving_contradiction_retracts_but_a_defeated_attacker_does_not() -> None:
    """The reinstatement case, computed rather than asserted.

    *"Attacked" does not mean "retracted."* Both halves run against the real
    computed status over a folded log, so the difference is one appended edge and
    the labelling does the rest:

    * the attacker stands → the claim is ``out`` → a **surviving** contradiction,
      and the gate retracts;
    * the attacker is **itself attacked** → the attacker is ``out``, the claim is
      reinstated to ``warranted``, and the gate does not fire at all — even though
      the attack edge is still right there in the log.

    A stubbed status label could not express the second case, which is why this is
    driven from the log: the reinstatement is *derived*.
    """
    attacked = _live_log(attacked=True)
    reinstated = EdgeSet(
        claims=attacked.claims + (_C("rebuttal-1"),),
        edges=attacked.edges + (_E("attack", "rebuttal-1", "counter-1", 3),),
    )

    # The attack on the promoted claim is still in the log; it is just defeated.
    assert [
        edge
        for edge in reinstated.edges
        if edge.op == "attack" and edge.dst == "claim-retention"
    ]
    table = compute_statuses(reinstated)
    assert table.statuses["counter-1"].label == "out"
    assert table.statuses["claim-retention"].label == "in"
    assert table.statuses["claim-retention"].status == "warranted"

    held = _gate(
        outputs={"derivation-retention": PARAPHRASE},
        statuses=_status_source(reinstated),
    ).review(_record(), now=30 * DAY)
    assert held.status_flip.flipped is False
    assert held.triggers == () and held.outcomes == ()
    assert held.disposition == "hold"
    assert not held.demoted and not held.withheld and not held.retracted
    assert held.promotion_eligibility == "eligible"

    # The same claim, the same gate, one fewer edge: now the contradiction survives.
    assert compute_statuses(attacked).statuses["claim-retention"].label == "out"
    surviving = _gate(
        outputs={"derivation-retention": PARAPHRASE},
        statuses=_status_source(attacked),
    ).review(_record(), now=30 * DAY)
    assert surviving.triggers == (TRIGGER_CONTRADICTION,)
    assert surviving.status_flip.label == "out" and surviving.status_flip.settled
    assert surviving.outcome_kinds == (OUTCOME_SURVIVING_CONTRADICTION,)
    assert surviving.demoted and surviving.action == "supersede_with_timestamp"
    assert surviving.retracted


def test_an_undecided_contradiction_is_quarantined_rather_than_retracted() -> None:
    """A contradiction that has not SETTLED is not a surviving contradiction.

    Two claims attacking each other leave the grounded labelling ``undec``: the
    dispute is live and unresolved, and the four-status vocabulary reports both a
    defeated claim and an undecided one as ``challenged`` because they have the same
    consequence for *answering*. They have opposite consequences for *retracting*,
    so the gate reads the label, records that the labelling has not settled, and
    withholds the claim instead of appending a retraction it cannot justify.
    """
    attacked = _live_log(attacked=True)
    disputed = EdgeSet(
        claims=attacked.claims,
        edges=attacked.edges + (_E("attack", "claim-retention", "counter-1", 3),),
    )
    table = compute_statuses(disputed)
    assert table.statuses["claim-retention"].label == "undec"
    assert table.statuses["claim-retention"].status == "challenged"

    certificate = issue_certificate(
        "derivation-retention",
        _validated_profile(),
        issuer="validator-1",
        reasoning_backend_id="reasoner-1",
    )
    review = _gate(
        outputs={"derivation-retention": PARAPHRASE},
        statuses=_status_source(disputed),
    ).review(_record(certificate=certificate), now=30 * DAY)

    # The gate DID look and DID find something — that part is unchanged.
    assert review.triggers == (TRIGGER_CONTRADICTION,)
    assert review.status_flip.flipped and not review.status_flip.settled
    # What changed is what it concludes from it.
    assert review.outcome_kinds == (OUTCOME_SURVIVING_CONTRADICTION,)
    assert review.inconclusive == review.outcomes
    assert review.disposition == "quarantine"
    assert review.quarantined and review.withheld and not review.demoted
    assert review.action is None and review.proposals == () and review.effects == ()
    assert review.revoked_certificate is None  # nothing was established to revoke
    assert review.promotion_eligibility == "needs_validation"
    assert any("has NOT settled" in reason for reason in review.outcome_reasons)

    # "with a recorded reason" is a ledger row, not a comment.
    entry = entry_for_review(review)
    assert entry.kind == "quarantine" and entry.withholding
    assert entry.outcomes == (OUTCOME_SURVIVING_CONTRADICTION,)
    assert any("has NOT settled" in reason for reason in entry.reasons)
    result = as_capability_result(review)
    assert result.status == "ok"  # something happened; it was not a demotion
    assert result.promotion_eligibility == "needs_validation"
    assert "withheld" in result.qualifier and "NOT retracted" in result.qualifier


def test_two_legitimate_abstractions_of_the_same_sources_do_not_demote_each_other() -> None:
    """Both directions of the same pair, and neither is a refutation.

    A frozen model given one span can produce either of two true summaries of it.
    Whichever one was promoted, regenerating the other looks exactly like a failure
    to a token-overlap comparison — so the gate checks whether BOTH statements stay
    inside the cited span, and when they do it asks for review instead of
    retracting. This is the fixture the counter asked for, run symmetrically so the
    result cannot be an artifact of which claim happens to be the promoted one.
    """
    # The arithmetic the classification rests on: the two disagree, and both are
    # inside the span.
    assert agreement(ABSTRACTION_A, ABSTRACTION_B) < REGENERATION_FLOOR
    assert source_support(ABSTRACTION_A, SHARED_SOURCE) >= SOURCE_SUPPORT_FLOOR
    assert source_support(ABSTRACTION_B, SHARED_SOURCE) >= SOURCE_SUPPORT_FLOOR

    first = _record(
        claim_id="claim-abstraction-a",
        derivation_id="derivation-abstraction-a",
        text=ABSTRACTION_A,
    )
    second = _record(
        claim_id="claim-abstraction-b",
        derivation_id="derivation-abstraction-b",
        text=ABSTRACTION_B,
    )
    for promoted, regenerated in ((first, ABSTRACTION_B), (second, ABSTRACTION_A)):
        review = _gate_for(
            promoted, source_text=SHARED_SOURCE, output=regenerated
        ).review(promoted, now=30 * DAY)
        assert review.triggers == (TRIGGER_REDERIVATION_FAILURE,)
        assert review.regeneration.failed and not review.regeneration.abstained
        assert review.regeneration.alternative_abstraction
        assert review.outcome_kinds == (OUTCOME_FAILED_GENERALISATION,)
        assert review.disposition == "request_review"
        assert not review.demoted and review.withheld and review.review_requested
        assert review.action is None and review.proposals == ()
        assert review.promotion_eligibility == "needs_validation"
        assert any(
            "two legitimate abstractions" in reason
            for reason in review.outcome_reasons
        )
        assert entry_for_review(review).kind == "review_requested"


def test_a_valid_paraphrase_is_not_demoted() -> None:
    """The gate compares meaning-bearing vocabulary, not bytes.

    A regeneration that restates the claim in different words is the SUCCESS case,
    not a near miss: it clears the floor, nothing fires, no outcome is recorded and
    the ledger refuses a row for it. Byte equality here would demote every claim
    whose paraphrase differs, which is most of them.
    """
    score = agreement(CLAIM_TEXT, PARAPHRASE)
    assert REGENERATION_FLOOR <= score < 1.0  # different words, same claim
    review = _gate(outputs={"derivation-retention": PARAPHRASE}).review(
        _record(), now=30 * DAY
    )
    assert review.regeneration.regenerated and not review.regeneration.exact
    assert review.triggers == () and review.outcomes == ()
    assert review.disposition == "hold"
    assert not review.demoted and not review.withheld
    assert review.promotion_eligibility == "eligible"
    with pytest.raises(ValueError, match="demoted nothing"):
        entry_for_review(review)


def test_a_reproducible_source_error_is_not_a_reproduction_failure() -> None:
    """Reproduction is evidence of FIDELITY, not of truth — and the outcomes say so.

    Two claims, and the point is that they must not receive the same finding:

    * one cites a span that is simply wrong and restates it faithfully. The frozen
      model reproduces it exactly, so reproduction *passed* — and the log
      contradicts the claim anyway. The outcome is a surviving contradiction, and
      the review still reports the regeneration as having succeeded;
    * the other does not come back from its sources at all, and nothing attacks it.
      That is the reproduction failure.

    Recording both as "the claim is false" would be the overstatement this phase
    was corrected for: a frozen model reproducing an error is behaving correctly.
    """
    faithful = _record(
        claim_id="claim-window",
        derivation_id="derivation-window",
        text=FAITHFUL_CLAIM,
    )
    # The corpus knows better than the source it cites: a corrective claim attacks
    # the faithful restatement, and the labelling settles against it.
    corrected = EdgeSet(
        claims=(_C("claim-window"), _C("support-window"), _C("correction-1")),
        edges=(
            _E("support", "support-window", "claim-window", 1),
            _E("attack", "correction-1", "claim-window", 2),
        ),
    )
    assert compute_statuses(corrected).statuses["claim-window"].label == "out"

    contradicted = _gate_for(
        faithful,
        source_text=ERRONEOUS_SOURCE,
        output=FAITHFUL_CLAIM,
        statuses=_status_source(corrected),
    ).review(faithful, now=30 * DAY)
    assert contradicted.regeneration.regenerated and contradicted.regeneration.exact
    assert contradicted.triggers == (TRIGGER_CONTRADICTION,)
    assert contradicted.outcome_kinds == (OUTCOME_SURVIVING_CONTRADICTION,)
    assert OUTCOME_FAILED_REPRODUCTION not in contradicted.outcome_kinds
    assert contradicted.demoted and contradicted.action == "supersede_with_timestamp"

    # The other kind of failure, on a claim nothing attacks.
    unreproducible = _record(
        claim_id="claim-unreproducible", derivation_id="derivation-unreproducible"
    )
    missed = _gate_for(
        unreproducible, source_text=SOURCE_TEXT, output=CONTRADICTION_TEXT
    ).review(unreproducible, now=30 * DAY)
    assert missed.triggers == (TRIGGER_REDERIVATION_FAILURE,)
    assert missed.outcome_kinds == (OUTCOME_FAILED_REPRODUCTION,)
    assert missed.demoted and missed.action == "flag"

    # Same demotion verdict, different findings — which is the whole point.
    assert contradicted.demoted and missed.demoted
    assert contradicted.outcome_kinds != missed.outcome_kinds


def test_an_ungrounded_claim_is_a_grounding_failure_not_a_reproduction_failure() -> None:
    """Nothing to derive from is a different finding from "it did not come back".

    A promoted claim citing no usable evidence is the defect the gate exists to
    catch, and naming it a reproduction failure would blame the model for the
    absence of a source. Both still demote — the distinction is what the demotion
    SAYS, which is what an appeal argues about.
    """
    record = _record()
    review = ReDerivationGate(
        model=_frozen({"derivation-retention": PARAPHRASE}),
        sources=StaticSourceReader({}),  # no cited spans at all
        statuses=StaticStatusSource({"claim-retention": "warranted"}),
        independence=StaticIndependenceSource(
            {"derivation-retention": ("episode-1", "episode-2")}
        ),
    ).review(record, now=30 * DAY)
    assert review.regeneration.ungrounded and review.regeneration.source_count == 0
    assert review.triggers == (TRIGGER_REDERIVATION_FAILURE,)
    assert review.outcome_kinds == (OUTCOME_GROUNDING_FAILURE,)
    assert review.demoted and review.action == "flag"

    # A cited span that is EMPTY is the same defect wearing a locator.
    blank = _gate_for(record, source_text="   ", output=CONTRADICTION_TEXT).review(
        record, now=30 * DAY
    )
    assert blank.regeneration.ungrounded
    assert blank.outcome_kinds == (OUTCOME_GROUNDING_FAILURE,)


def test_a_moved_cited_base_quarantines_the_failure_instead_of_demoting() -> None:
    """Stale evidence: the same failure, quarantined because the base moved.

    The protocol asks whether the claim comes back out of *the sources it cited*.
    If those spans are not the ones it cited, then a failure is a finding about the
    base, not about the claim — so the identical model output demotes against an
    unchanged span and only withholds against a changed one. The two halves differ
    by one content hash, which is the whole difference the gate is entitled to see.
    """
    record = _record(source_hashes=(("h2:Retention", "hash-at-promotion"),))
    unchanged = _gate_for(
        record,
        source_text=SOURCE_TEXT,
        output=CONTRADICTION_TEXT,
        content_hash="hash-at-promotion",
    ).review(record, now=30 * DAY)
    assert unchanged.freshness.stale is False and unchanged.freshness.compared == 1
    assert unchanged.outcome_kinds == (OUTCOME_FAILED_REPRODUCTION,)
    assert unchanged.demoted

    moved = _gate_for(
        record,
        source_text=SOURCE_TEXT,
        output=CONTRADICTION_TEXT,
        content_hash="hash-after-an-edit",
    ).review(record, now=30 * DAY)
    assert moved.freshness.stale and moved.freshness.moved == ("h2:Retention",)
    assert moved.triggers == (TRIGGER_REDERIVATION_FAILURE,)  # the gate still looked
    assert moved.outcome_kinds == (OUTCOME_STALE_EVIDENCE,)
    assert moved.quarantined and not moved.demoted
    assert moved.proposals == () and moved.action is None
    assert any("held pending a re-check" in r for r in moved.outcome_reasons)

    # A PASS against a moved base certifies nothing either, so it is withheld too:
    # the protocol's question was about the spans the claim cited.
    regenerated = _gate_for(
        record,
        source_text=SOURCE_TEXT,
        output=PARAPHRASE,
        content_hash="hash-after-an-edit",
    ).review(record, now=30 * DAY)
    assert regenerated.regeneration.regenerated and regenerated.triggers == ()
    assert regenerated.outcome_kinds == (OUTCOME_STALE_EVIDENCE,)
    assert regenerated.quarantined and not regenerated.demoted

    # A record that never recorded its promotion-time hashes gets no staleness
    # finding at all, and the check SAYS so rather than reporting "fresh".
    silent = check_evidence_freshness(_record(), _sources().cited_sources("claim-retention"))
    assert silent.stale is False and silent.compared == 0
    assert "cannot be judged" in silent.reason


def test_a_quarantine_is_recorded_and_does_not_discharge_a_demotion() -> None:
    """The withholding state is real: recorded, re-checked, and not a reinstatement.

    Three properties the ledger has to hold for quarantine to mean anything:

    1. a quarantine is a row with its reason, readable without re-running the gate;
    2. it does not change standing — a quarantine appended after a demotion must not
       silently reinstate the claim, because only the recovery path may do that and
       it needs a certificate;
    3. a quarantined claim is NOT skipped by the next sweep, since re-checking it is
       exactly the remedy for "the gate could not conclude".
    """
    attacked = _live_log(attacked=True)
    disputed = EdgeSet(
        claims=attacked.claims,
        edges=attacked.edges + (_E("attack", "claim-retention", "counter-1", 3),),
    )
    record = _record(promoted_at=0.0)
    gate = _gate(
        outputs={"derivation-retention": PARAPHRASE},
        statuses=_status_source(disputed),
    )
    sweep = gate.sweep((record,), now=30 * DAY)

    assert sweep.demoted == () and sweep.quarantined == ("claim-retention",)
    assert sweep.withheld == ("claim-retention",)
    assert sweep.effects == ()  # nothing is appended for a finding it cannot conclude
    assert sweep.by_trigger()[TRIGGER_CONTRADICTION] == ("claim-retention",)
    assert sweep.by_outcome()[OUTCOME_SURVIVING_CONTRADICTION] == ("claim-retention",)
    assert sweep.by_disposition()["quarantine"] == ("claim-retention",)
    assert len(sweep.ledger) == 1
    assert sweep.ledger.is_quarantined("claim-retention")
    assert not sweep.ledger.is_demoted("claim-retention")
    assert sweep.ledger.quarantined_claim_ids() == ("claim-retention",)
    assert sweep.ledger.reasons_for("claim-retention")

    # Re-checked next pass, not skipped — and once the dispute settles against it,
    # the same claim demotes on the same trigger.
    settled = gate.sweep((record,), now=60 * DAY, ledger=sweep.ledger)
    assert settled.skipped_already_demoted == ()
    assert [review.claim_id for review in settled.reviews] == ["claim-retention"]

    # A quarantine after a demotion changes nothing about the demotion.
    demoted_then_quarantined = DemotionLedger().record(
        DemotionEntry(
            kind="demotion", claim_id="claim-x", derivation_id="d-x", at=1.0,
            triggers=(TRIGGER_REDERIVATION_FAILURE,), action="flag",
        ),
        DemotionEntry(
            kind="quarantine", claim_id="claim-x", derivation_id="d-x", at=2.0,
            triggers=(TRIGGER_CONTRADICTION,), reasons=("undecided",),
        ),
    )
    assert demoted_then_quarantined.is_demoted("claim-x")
    assert not demoted_then_quarantined.is_quarantined("claim-x")
    assert down_rank_order(
        {
            "claim-x": RewardInputs(node_id="claim-x", validated=True,
                                    inbound_from=("a", "b")),
            "claim-y": RewardInputs(node_id="claim-y", validated=True,
                                    inbound_from=("a",)),
        },
        ledger=demoted_then_quarantined,
    ) == ["claim-y", "claim-x"]


# ── the schedule: required, not available ──────────────────────────────────


def test_the_gate_is_scheduled_and_being_unrun_is_an_error() -> None:
    """"Not run yet" must not read as "nothing to demote".

    A claim promoted and never re-derived is due one interval after promotion, and
    a promotion path calls :func:`require_armed` before promoting anything else.
    """
    record = _record(promoted_at=0.0)
    assert due_at(record) == DEFAULT_DEMOTION_POLICY.interval_days * DAY
    assert not is_due(record, 6 * DAY)
    assert is_due(record, 7 * DAY)

    checked = _record(promoted_at=0.0, last_checked_at=7 * DAY)
    assert due_at(checked) == 14 * DAY
    assert due_records((record, checked), 8 * DAY) == (record,)

    require_armed((record,), 6 * DAY)  # not yet due — no refusal
    with pytest.raises(GateNotArmedError, match="overdue"):
        require_armed((record, checked), 20 * DAY)
    # A late batch can be tolerated explicitly, which is not the same as by
    # default.
    require_armed((record,), 8 * DAY, grace_days=2.0)


def test_a_sweep_reports_its_own_coverage_and_appends_the_ledger() -> None:
    """The scheduled pass: review what is due, name what was skipped, and hand
    back a LONGER ledger — never a shorter one."""
    due = _record(claim_id="claim-retention", promoted_at=0.0)
    fresh = _record(
        claim_id="claim-fresh",
        derivation_id="derivation-fresh",
        promoted_at=20 * DAY,
    )
    gate = _gate(
        outputs={"derivation-retention": CONTRADICTION_TEXT},
        statuses=StaticStatusSource({"claim-retention": "warranted"}),
    )
    sweep = gate.sweep((due, fresh), now=21 * DAY)

    assert sweep.demoted == ("claim-retention",)
    assert sweep.skipped_not_due == ("claim-fresh",)
    assert len(sweep.ledger) == 1
    assert sweep.by_trigger()[TRIGGER_REDERIVATION_FAILURE] == ("claim-retention",)
    assert [effect.kind for effect in sweep.effects] == ["claim", "edge"]

    # A second sweep does not re-demote what is already demoted — it reviews what
    # has since come due, and the first entry is still the first entry.
    again = gate.sweep((due, fresh), now=40 * DAY, ledger=sweep.ledger)
    assert again.skipped_already_demoted == ("claim-retention",)
    assert again.skipped_not_due == ()
    assert [review.claim_id for review in again.reviews] == ["claim-fresh"]
    assert again.ledger.entries[0] == sweep.ledger.entries[0]
    assert [entry.claim_id for entry in again.ledger.entries] == [
        "claim-retention", "claim-fresh"
    ]


# ── history survives every demotion ────────────────────────────────────────


def test_history_survives_every_demotion() -> None:
    """Nothing is deleted, mutated or shortened by a demotion.

    Four ways, because "append-only" has to hold for every artifact the demotion
    touches: the ledger handed in is unchanged, the promotion record is unchanged,
    the issued certificate is still readable after revocation, and the retracted
    claim's own row is never rewritten — the retraction is a new row beside it.
    """
    profile = MaturityProfile(
        levels={
            "independent_validation": "VALIDATED",
            "warrant": "VALIDATED",
            "provenance": "VALIDATED",
        }
    )
    certificate = issue_certificate(
        "derivation-retention",
        profile,
        issuer="validator-1",
        reasoning_backend_id="reasoner-1",
    )
    record = _record(certificate=certificate)
    ledger = DemotionLedger()

    sweep = ReDerivationGate(
        model=_frozen({"derivation-retention": CONTRADICTION_TEXT}),
        sources=_sources(),
        statuses=StaticStatusSource({"claim-retention": "warranted"}),
        independence=StaticIndependenceSource(
            {"derivation-retention": ("episode-1", "episode-2")}
        ),
    ).sweep((record,), now=30 * DAY, ledger=ledger)

    assert len(ledger) == 0 and len(sweep.ledger) == 1  # the input is untouched
    assert record.text == CLAIM_TEXT and record.certificate is certificate
    review = sweep.reviews[0]
    assert review.revoked_certificate is not None
    assert review.revoked_certificate.revoked
    assert TRIGGER_REDERIVATION_FAILURE in review.revoked_certificate.revoked_reason
    assert review.revoked_certificate.revoked_at == 30 * DAY
    assert certificate.revoked is False  # the attestation as issued still reads

    entry = sweep.ledger.entries[0]
    assert entry.kind == "demotion"
    assert entry.retraction_claim_id == review.retraction_claim_id
    assert sweep.ledger.history_for("claim-retention") == (entry,)
    assert sweep.ledger.is_demoted("claim-retention")

    # The retraction is a new claim beside the retracted one, never a rewrite of
    # it: different ids, and the retracted claim's id appears only as the edge's
    # destination.
    claim_proposal = review.proposals[0]
    assert isinstance(claim_proposal, ClaimProposal)
    assert claim_proposal.claim_id != record.claim_id
    assert claim_proposal.derivation_id != record.derivation_id


def test_a_passing_review_is_reported_not_logged() -> None:
    """A review that demotes nothing is still evidence the gate ran — and it is
    not a ledger entry, because nothing happened to the claim."""
    review = _gate(outputs={"derivation-retention": PARAPHRASE}).review(
        _record(), now=30 * DAY
    )
    assert not review.demoted and review.action is None
    assert as_capability_result(review).status == "empty"
    with pytest.raises(ValueError, match="demoted nothing"):
        entry_for_review(review)


# ── the recovery path ──────────────────────────────────────────────────────


def _validated_profile() -> MaturityProfile:
    return MaturityProfile(
        levels={
            "independent_validation": "VALIDATED",
            "warrant": "VALIDATED",
            "provenance": "VALIDATED",
        }
    )


def test_the_recovery_path_restores_a_wrongly_demoted_claim() -> None:
    """A wrongly-demoted claim comes back — by APPENDING, and by a judge.

    The demotion here is the one that can be *wrong*: a re-derivation failure on
    a claim nothing attacks, which is exactly where a lexical comparison
    misfires. The retraction is discharged with an ``attack`` on it, and the real
    fixed point does the rest — the retraction goes ``out`` and the original claim
    is ``warranted`` again. Nothing was deleted and no status was written; both
    acts remain in the ledger.
    """
    unattacked = _live_log(attacked=False)
    record = _record()
    review = _gate(
        outputs={"derivation-retention": CONTRADICTION_TEXT},
        statuses=_status_source(unattacked),
    ).review(record, now=30 * DAY)
    assert review.triggers == (TRIGGER_REDERIVATION_FAILURE,)
    ledger = DemotionLedger().record(entry_for_review(review))
    retraction = review.proposals[0]
    assert isinstance(retraction, ClaimProposal)

    # The corpus as it stands after the demotion: the flag's attack makes the
    # claim `challenged`, so the read flow surfaces the conflict instead of
    # answering from it.
    demoted_log = EdgeSet(
        claims=unattacked.claims + (_C(retraction.claim_id),),
        edges=unattacked.edges
        + (_E("attack", retraction.claim_id, record.claim_id, 3),),
    )
    assert (
        compute_statuses(demoted_log).statuses[record.claim_id].status == "challenged"
    )

    outcome = recover(
        record,
        ledger=ledger,
        profile=_validated_profile(),
        validator_id="validator-1",
        reasoning_backend_id="reasoner-1",
        at=45 * DAY,
        detail="the counter-argument cited a superseded policy",
    )

    assert outcome.promotion_eligibility == "needs_validation"
    assert outcome.certificate.issuer == "validator-1"
    assert not outcome.certificate.revoked
    recovery_claim, recovery_edge = outcome.proposals
    assert isinstance(recovery_claim, ClaimProposal)
    assert isinstance(recovery_edge, EdgeProposal)
    assert recovery_edge.op == "attack"
    assert recovery_edge.dst == retraction.claim_id  # discharge the RETRACTION
    assert recovery_edge.origin == ORIGIN_RECOVERY
    assert [effect.kind for effect in outcome.effects] == ["claim", "edge"]
    assert recovery_capability_result(outcome).promotion_eligibility == (
        "needs_validation"
    )

    # History survives the recovery too: both acts are in the ledger, in order.
    assert len(ledger) == 1 and len(outcome.ledger) == 2
    kinds = [entry.kind for entry in outcome.ledger.history_for(record.claim_id)]
    assert kinds == ["demotion", "recovery"]
    assert not outcome.ledger.is_demoted(record.claim_id)

    # And the append actually restores the claim: the retraction is defeated, so
    # its attack stops counting and the original is reinstated — the labelling's
    # doing, which is why nothing had to be mutated.
    recovered_log = EdgeSet(
        claims=demoted_log.claims + (_C(recovery_claim.claim_id),),
        edges=demoted_log.edges
        + (_E("attack", recovery_claim.claim_id, retraction.claim_id, 4),),
    )
    table = compute_statuses(recovered_log)
    assert table.statuses[retraction.claim_id].status == "challenged"
    assert table.statuses[record.claim_id].status == "warranted"
    assert table.statuses[record.claim_id].answerable


def test_a_supersession_is_recoverable_because_the_pre_filter_reads_a_label() -> None:
    """Even the strongest action is reversible without deleting anything.

    A ``supersede`` counts only while the superseding claim itself computes as
    ``warranted``, so attacking the retraction — which makes it ``out``, and
    therefore no longer warranted — returns the retired claim to the framework.
    That is the pre-filter's rule doing the work: no row is rewritten, and no
    ``valid_to`` column has to be mutated for a claim to come back.
    """
    attacked = _live_log(attacked=True)
    record = _record()
    review = _gate(
        outputs={"derivation-retention": PARAPHRASE}, statuses=_status_source(attacked)
    ).review(record, now=30 * DAY)
    assert review.action == "supersede_with_timestamp"
    retraction, grounding = review.proposals[0], review.proposals[1]
    assert isinstance(retraction, ClaimProposal)
    assert isinstance(grounding, ClaimProposal)
    outcome = recover(
        record,
        ledger=DemotionLedger().record(entry_for_review(review)),
        profile=_validated_profile(),
        validator_id="validator-1",
        reasoning_backend_id="reasoner-1",
        at=45 * DAY,
    )
    discharge = outcome.proposals[0]
    assert isinstance(discharge, ClaimProposal)

    # First the supersession as the gate appended it: grounded, therefore counting.
    retired = EdgeSet(
        claims=attacked.claims + (_C(retraction.claim_id), _C(grounding.claim_id)),
        edges=attacked.edges
        + (
            _E("support", grounding.claim_id, retraction.claim_id, 3),
            _E("supersede", retraction.claim_id, record.claim_id, 4),
        ),
    )
    assert compute_statuses(retired).statuses[record.claim_id].status == "superseded"

    # Then the discharge, appended on top of exactly that log.
    log = EdgeSet(
        claims=retired.claims + (_C(discharge.claim_id),),
        edges=retired.edges
        + (_E("attack", discharge.claim_id, retraction.claim_id, 5),),
    )
    verdict = compute_statuses(log).statuses[record.claim_id]
    assert verdict.status != "superseded"  # back in the framework
    assert verdict.superseded_by is None


def test_recovery_is_not_self_service_and_needs_a_demotion_to_reverse() -> None:
    """Two refusals, both load-bearing.

    The mover is never the judge: the reasoning backend cannot attest its own
    claim back in. And a claim the ledger does not show demoted has nothing to
    recover from, so recovering it would mint an attestation nobody asked for.
    """
    review = _gate(
        outputs={"derivation-retention": CONTRADICTION_TEXT}
    ).review(_record(), now=30 * DAY)
    ledger = DemotionLedger().record(entry_for_review(review))

    with pytest.raises(CertificateError, match="mover is never the judge"):
        recover(
            _record(),
            ledger=ledger,
            profile=_validated_profile(),
            validator_id="reasoner-1",
            reasoning_backend_id="reasoner-1",
            at=45 * DAY,
        )
    with pytest.raises(CertificateError, match="mature"):
        recover(
            _record(),
            ledger=ledger,
            profile=MaturityProfile(),
            validator_id="validator-1",
            reasoning_backend_id="reasoner-1",
            at=45 * DAY,
        )
    with pytest.raises(RecoveryError, match="no active demotion"):
        recover(
            _record(claim_id="claim-never-demoted"),
            ledger=ledger,
            profile=_validated_profile(),
            validator_id="validator-1",
            reasoning_backend_id="reasoner-1",
            at=45 * DAY,
        )


# ── the mildest action, wired to the existing ranker ───────────────────────


def test_down_ranking_orders_demoted_claims_last() -> None:
    """Down-rank through the existing frozen-snapshot reward, not a second scheme.

    A demoted claim is marked un-validated, so its reward is ``0.0`` by
    construction and it sorts behind everything still standing. Nothing is
    removed, and a recovery that changes the ledger changes the order back.
    """
    candidates = {
        "claim-a": RewardInputs(node_id="claim-a", validated=True,
                                inbound_from=("x", "y")),
        "claim-b": RewardInputs(node_id="claim-b", validated=True,
                                inbound_from=("x",)),
    }
    ledger = DemotionLedger().record(
        DemotionEntry(kind="demotion", claim_id="claim-a", derivation_id="d-a",
                      at=1.0, triggers=(TRIGGER_INDEPENDENCE_BELOW_FLOOR,),
                      action="down_rank")
    )
    assert down_rank_order(candidates, ledger=DemotionLedger()) == [
        "claim-a", "claim-b"
    ]
    assert down_rank_order(candidates, ledger=ledger) == ["claim-b", "claim-a"]

    recovered = ledger.record(
        DemotionEntry(kind="recovery", claim_id="claim-a", derivation_id="d-a",
                      at=2.0, validator="validator-1")
    )
    assert down_rank_order(candidates, ledger=recovered) == ["claim-a", "claim-b"]


# ── the retraction vocabulary ──────────────────────────────────────────────


def test_a_flag_appends_an_attack_and_a_down_rank_appends_nothing() -> None:
    """Each action has exactly one meaning in the log, and none of them deletes.

    A flag becomes ``challenged`` (surface the conflict), a supersession becomes
    ``superseded`` (abstain), and a down-rank appends nothing at all."""
    record = _record()
    flagged = retraction_proposals(
        record, action="flag", triggers=(TRIGGER_REDERIVATION_FAILURE,), at=5.0
    )
    assert len(flagged) == 2  # a flag needs no grounding: an attacker need not be
    assert isinstance(flagged[1], EdgeProposal) and flagged[1].op == "attack"
    assert isinstance(flagged[0], ClaimProposal) and flagged[0].operator == "attack"
    superseded = retraction_proposals(
        record, action="supersede_with_timestamp",
        triggers=(TRIGGER_CONTRADICTION,), at=5.0,
    )
    # A supersession appends three rows, not one: the retraction, the finding that
    # grounds it, and the support edge between them — a replacement retires nothing
    # unless it is itself warranted.
    assert [type(p).__name__ for p in superseded] == [
        "ClaimProposal", "ClaimProposal", "EdgeProposal", "EdgeProposal"
    ]
    assert isinstance(superseded[3], EdgeProposal)
    assert superseded[3].op == "supersede"
    assert isinstance(superseded[2], EdgeProposal) and superseded[2].op == "support"
    assert retraction_proposals(
        record, action="down_rank",
        triggers=(TRIGGER_INDEPENDENCE_BELOW_FLOOR,), at=5.0,
    ) == ()
    with pytest.raises(ValueError, match="unknown demotion action"):
        retraction_proposals(record, action="hard_delete", triggers=(), at=5.0)  # type: ignore[arg-type]

    # Replay: the same check time renders the same rows, so a retried sweep is a
    # no-op rather than a second retraction of the same act.
    assert retraction_proposals(
        record, action="flag", triggers=(TRIGGER_REDERIVATION_FAILURE,), at=5.0
    ) == flagged


def test_revoke_keeps_the_issued_certificate_readable() -> None:
    """Revocation is an additional record, never an erasure — and the reason and
    timestamp are optional, so the existing caller is unaffected."""
    cert = issue_certificate(
        "inquiry-1",
        _validated_profile(),
        issuer="validator-1",
        reasoning_backend_id="reasoner-1",
    )
    plain = revoke(cert)
    assert plain.revoked and plain.revoked_reason == "" and plain.revoked_at is None
    detailed = revoke(cert, reason=TRIGGER_CONTRADICTION, at=9.0)
    assert detailed.revoked_reason == TRIGGER_CONTRADICTION
    assert detailed.revoked_at == 9.0
    assert cert.revoked is False
    assert detailed.profile is cert.profile and detailed.issuer == cert.issuer


def test_the_model_output_shape_is_an_answer_or_an_abstention() -> None:
    """An abstention is a first-class answer, and it counts as a failure: "I
    cannot state this claim from these sources" is the finding the gate wants."""
    assert ReDerivationOutput().abstained is False  # silence is not an abstention
    assert ReDerivationOutput(abstained=True).text == ""
