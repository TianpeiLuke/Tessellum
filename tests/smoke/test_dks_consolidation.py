"""P12 smoke tests — gate (ii), the reviewed promotion batch.

One test per clause of the phase's acceptance line, and the six conditions are
each exercised on a candidate that meets **every other** condition, so a failure
is attributable:

1. derived too few times → only ``recurrence`` fails;
2. one context → only ``independence`` fails;
3. ``η`` below the floor → only ``reliability`` fails (and the claim is
   probationary, not active);
4. inside the dwell window → only ``stability`` fails;
5. entailment refuted (and, separately, abstained) → only ``grounding`` fails;
6. a near-duplicate exists → only ``dedup`` fails.

Plus the four artifacts the phase owes: a claim meeting every condition produces
a **reviewed diff** and proposed effects rather than a silent write; a promoted
claim **retains** its date and authority qualifiers (and a stripping author is
refused); a **promotion record** exists and is sufficient to demote by; and the
batch **refuses to run with** ``use_human=False``.

**And the independence clause the phase names in its own acceptance line: ten
restatements of the same self-authored claim do not satisfy the independence
term.** That clause is why the baseline candidate here reads *three different
authored notes* rather than one span three times: independence is
**origin-distinct**, so three re-readings of one note are one witness, and a
fixture that met the criterion on episode ids alone would have been asserting the
defect. Four fixtures pin the rule — ten restatements off one promoted claim; a
restatement that cannot corroborate the sources it came from (the commit
boundary); three spans of one note; and an occurrence that declares no origin at
all — and one control shows the rule still *passes* a genuinely new source, since
a gate that never opens is not a gate.

The subject of every count is the **proposition version**, never the evidence
occurrence it was read from, so a revised proposition starts with no feedback
history instead of inheriting the replaced one's.

And the properties those clauses rest on: promotion is default-OFF, the un-run
promotion A/B is refused, the mover is never the judge, the writeback is scoped
to the neighbourhood with no rewrite lines in the diff, the dedup *decision*
belongs to the injected model rather than to the threshold, the weakened
independence term is recorded, and the module never imports the runtime.

The record's sufficiency is checked twice over: field-by-field per demotion
trigger, and then end-to-end *through* P10's re-derivation gate
(``dks.demotion``), whose every port is wired out of the promotion handle and
nothing else. The second check is what the first can only approximate — a handle
that looked sufficient but did not satisfy the gate's ports would pass the
field-by-field assertions and fail there.

All local; no network, no model — the entailment, dedup and prose seams are
exercised through their deterministic reference implementations.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

import tessellum.dks.consolidation as consolidation_module
from tessellum.composer.signoff import SignOffPolicy
from tessellum.dks.autonomy import AuthorityLadder, AuthorityLadderError
from tessellum.dks.capability import EFFECT_KINDS
from tessellum.dks.claim_identity import (
    FACT_ID_DEVIATION,
    anchor_locator,
    identify,
    note_version_hash,
)
from tessellum.dks.consolidation import (
    DWELL_WINDOW_DAYS_MAX,
    DWELL_WINDOW_DAYS_MIN,
    INDEPENDENCE_BASIS_FACTS,
    INDEPENDENCE_ORIGIN_RULE,
    PROMOTION_ENABLED_BY_DEFAULT,
    REASON_ANSWER_CHANGED,
    REASON_DERIVED_TOO_FEW_TIMES,
    REASON_ENTAILMENT_ABSTAINED,
    REASON_ENTAILMENT_FAILED,
    REASON_ETA_BELOW_FLOOR,
    REASON_INSIDE_DWELL_WINDOW,
    REASON_NEAR_DUPLICATE,
    REASON_NO_EMBEDDING,
    REASON_NO_RENDERER,
    REASON_OPEN_CORRECTION,
    REASON_ORIGIN_UNATTRIBUTED,
    REASON_SHARED_ORIGIN,
    REASON_TOO_FEW_CONTEXTS,
    SCOPE_NEIGHBOURHOOD,
    UNRUN_PROMOTION_AB,
    AdditiveProseAuthor,
    AuthorityCapError,
    ClaimOrigin,
    ConsolidationDisabledError,
    ConsolidationPolicy,
    DedupDecision,
    DedupJudge,
    DedupRequest,
    DerivationOccurrence,
    EntailmentRequest,
    EntailmentVerdict,
    HumanGateError,
    LinkBeforeCreateJudge,
    MoverIsJudgeError,
    PriorArtEntry,
    PromotionABGate,
    PromotionABNotRunError,
    PromotionCandidate,
    PromotionProseAuthor,
    ProseRequest,
    Qualifier,
    QualifierStrippedError,
    StaticEntailmentJudge,
    StaticPriorArtIndex,
    UncalibratedEntailmentJudge,
    corpus_origin,
    cosine,
    evaluate_candidate,
    independence_count,
    independence_measurement,
    lifecycle_for,
    origin_after_promotion,
    prior_art_shortlist,
    require_authority,
    run_consolidation_batch,
    self_authored_origin,
)
from tessellum.dks.demotion import (
    TRIGGER_REDERIVATION_FAILURE,
    CitedSource,
    FrozenReDerivationModel,
    PromotedClaimRecord,
    ReDerivationGate,
    ScriptedReDerivationModel,
    StaticIndependenceSource,
    StaticSourceReader,
    StaticStatusSource,
)
from tessellum.dks.memory_tiers import (
    RESOLVED_ORIGIN,
    CachedMapping,
    CorrectionFlag,
    FeedbackEvent,
    QueryCacheSource,
    TrialHistory,
    tally_trials,
)

CONSOLIDATION_SOURCE = Path(consolidation_module.__file__)

# ── fixtures: an all-conditions-met candidate, and the seams around it ───────

BASE_AT = 1_700_000_000.0
DAY = 86400.0

PROPOSITION = "The accounts team owns the platform."
PROPOSITION_ID = "prop:0f1e2d"

# THREE distinct authored notes, because independence is origin-distinct: one
# note read three times is one witness, so a baseline that met the criterion off
# a single span would be asserting the very defect this file pins.
FIRST_NOTE = "note-accounts-charter"
SECOND_NOTE = "note-service-registry"
THIRD_NOTE = "note-onboarding-runbook"
FOURTH_NOTE = "note-quarterly-review"

SPAN = "The platform owner of record is the accounts team, as of 2026-03-01."
LOCATOR = f"{FIRST_NOTE}#anchor-1c4f"
SECOND_SPAN = "Platform ownership sits with the accounts team, as of 2026-03-01."
SECOND_LOCATOR = f"{SECOND_NOTE}#anchor-77ab"
THIRD_SPAN = "Send platform questions to the accounts team, who own it."
THIRD_LOCATOR = f"{THIRD_NOTE}#anchor-0b12"

SOURCE_BY_EPISODE: dict[str, tuple[str, str, str]] = {
    "episode-a": (FIRST_NOTE, SPAN, LOCATOR),
    "episode-b": (SECOND_NOTE, SECOND_SPAN, SECOND_LOCATOR),
    "episode-c": (THIRD_NOTE, THIRD_SPAN, THIRD_LOCATOR),
}
ENTAILING_SPANS = frozenset({SPAN, SECOND_SPAN, THIRD_SPAN})

NEIGHBOURHOOD = "## Ownership\n\nThe authored paragraph, which nobody may rewrite."

DATE_QUALIFIER = Qualifier(kind="date", text="as of 2026-03-01", locator=LOCATOR)
AUTHORITY_QUALIFIER = Qualifier(
    kind="authority", text="per the accounts team's own note", locator=LOCATOR
)

REVIEWER = "independent-reviewer"
BACKEND = "derivation-backend"

ADMITTED_AB = PromotionABGate(
    runs_per_arm=3,
    orderings=2,
    delta=0.12,
    holds_under_every_ordering=True,
    regression_checked=("relationship", "multi_hop"),
    regression_free=True,
    note="synthetic measurement for the test only",
)

HUMAN_POLICY = SignOffPolicy(use_agent=True, use_human=True)


def _occurrence(
    episode: str, *, day: float, answer: str = "answer-1", source: str | None = None
) -> DerivationOccurrence:
    """One derivation, carrying the ORIGIN it traced to.

    Each baseline episode reads a *different* authored note by default, so the
    baseline has three origins and therefore three independent contexts.
    ``source`` names another episode's note instead, which is how the
    same-origin fixtures below are built."""
    note_id, span, locator = SOURCE_BY_EPISODE[source or episode]
    return DerivationOccurrence(
        claim_id=f"claim-{episode}",
        episode_id=episode,
        at=BASE_AT + day * DAY,
        answer_hash=answer,
        locator=locator,
        span_text=span,
        origin=corpus_origin(note_id),
    )


def _candidate(**overrides: object) -> PromotionCandidate:
    """A candidate that meets EVERY condition — the isolation baseline."""
    base = dict(
        proposition_id=PROPOSITION_ID,
        claim_text=PROPOSITION,
        target="note",
        target_note_id="note-ownership",
        occurrences=(
            _occurrence("episode-a", day=0.0),
            _occurrence("episode-b", day=5.0),
            _occurrence("episode-c", day=10.0),
        ),
        neighbourhood_anchor="ownership",
        neighbourhood_text=NEIGHBOURHOOD,
        qualifiers=(DATE_QUALIFIER, AUTHORITY_QUALIFIER),
        embedding=(1.0, 0.0, 0.0),
        base_snapshot_id="edgeset-digest-9a",
        bb_role="argument",
    )
    base.update(overrides)
    return PromotionCandidate(**base)  # type: ignore[arg-type]


def _reliable_history(candidate: PromotionCandidate) -> TrialHistory:
    """η = 0.9, keyed on the PROPOSITION version — never on an evidence id."""
    return TrialHistory(
        subject_id=candidate.proposition_id,
        subject_kind="promoted_claim",
        n_trial=8,
        n_pass=8,
    )


def _judge() -> StaticEntailmentJudge:
    return StaticEntailmentJudge(entailing_spans=ENTAILING_SPANS)


def _evaluate(candidate: PromotionCandidate, **overrides: object):
    kwargs = dict(
        history=_reliable_history(candidate),
        entailment=_judge(),
        prior_art=StaticPriorArtIndex(),
        dedup=LinkBeforeCreateJudge(),
        reviewer_id=REVIEWER,
        reasoning_backend_id=BACKEND,
    )
    kwargs.update(overrides)
    return evaluate_candidate(candidate, **kwargs)  # type: ignore[arg-type]


def _batch(candidates, **overrides):
    kwargs = dict(
        sign_off_policy=HUMAN_POLICY,
        reviewer_id=REVIEWER,
        reasoning_backend_id=BACKEND,
        enabled=True,
        ab_gate=ADMITTED_AB,
        entailment=_judge(),
        prior_art=StaticPriorArtIndex(),
        dedup=LinkBeforeCreateJudge(),
        histories={c.proposition_id: _reliable_history(c) for c in candidates},
    )
    kwargs.update(overrides)
    return run_consolidation_batch(candidates, **kwargs)  # type: ignore[arg-type]


def _failed(verdict) -> tuple[str, ...]:
    return verdict.failed_conditions


# ── the baseline: every condition met ───────────────────────────────────────


def test_the_baseline_candidate_meets_every_condition() -> None:
    """The isolation baseline: if this ever fails, every test below is vacuous.

    It meets the independence term the honest way — three episodes reading three
    *different* authored notes — so the fixture cannot pass by counting episode
    ids."""
    candidate = _candidate()
    assert len(candidate.origin_ids) == 3
    assert candidate.unattributed_occurrences == 0
    verdict = _evaluate(candidate)
    assert _failed(verdict) == ()
    assert verdict.condition("independence").measured == 3.0
    assert verdict.eligibility == "eligible"
    assert verdict.lifecycle == "active"


# ── condition 1: recurrence ─────────────────────────────────────────────────


def test_derived_too_few_times_fails_only_the_recurrence_condition() -> None:
    """Two derivations from two episodes ten days apart: only recurrence fails.

    Isolation is possible here and taken, which the plan's own phrasing ("derived
    once") cannot give — a single occurrence necessarily has one context and a
    zero-day dwell, so it fails three conditions at once. Both cases are asserted:
    the isolated one, and the literal one."""
    two = _candidate(
        occurrences=(
            _occurrence("episode-a", day=0.0),
            _occurrence("episode-b", day=10.0),
        )
    )
    verdict = _evaluate(two)
    assert _failed(verdict) == ("recurrence",)
    assert verdict.condition("recurrence").reasons == (REASON_DERIVED_TOO_FEW_TIMES,)
    assert verdict.condition("recurrence").measured == 2.0
    assert verdict.condition("recurrence").threshold == 3.0
    assert verdict.eligibility == "needs_validation"
    assert verdict.record is None and verdict.diff is None

    once = _candidate(occurrences=(_occurrence("episode-a", day=0.0),))
    assert "recurrence" in _failed(_evaluate(once))


# ── condition 2: independent contexts ───────────────────────────────────────


def test_one_context_fails_only_the_independence_condition() -> None:
    """Three derivations, all in ONE episode: recurrence passes, independence does
    not — which is the whole reason the two are separate conditions."""
    candidate = _candidate(
        occurrences=(
            _occurrence("episode-a", day=0.0),
            replace(_occurrence("episode-a", day=5.0), claim_id="claim-a2"),
            replace(_occurrence("episode-a", day=10.0), claim_id="claim-a3"),
        )
    )
    verdict = _evaluate(candidate)
    assert _failed(verdict) == ("independence",)
    assert verdict.condition("recurrence").passed
    assert verdict.condition("independence").measured == 1.0
    assert verdict.eligibility == "needs_validation"


def test_ten_restatements_of_a_self_authored_claim_are_not_ten_witnesses() -> None:
    """The acceptance clause: *ten restatements of the same self-authored claim do
    not satisfy the independence term.*

    Ten derivations, ten **distinct episode ids**, one origin — the claim this
    system promoted earlier. Counting episodes would report ten independent
    contexts and promote a claim on the strength of its own echo; counting origins
    reports one. The failure is named as a shared origin, not merely as a short
    count, because those are different findings for a reviewer."""
    promoted = _batch([_candidate()]).promoted[0].record
    assert promoted is not None
    inherited = origin_after_promotion(promoted)

    restatements = tuple(
        DerivationOccurrence(
            claim_id=f"claim-restatement-{index}",
            episode_id=f"episode-restatement-{index}",
            at=BASE_AT + index * DAY,
            answer_hash="answer-1",
            locator=LOCATOR,
            span_text=SPAN,
            origin=inherited,
        )
        for index in range(10)
    )
    candidate = _candidate(
        proposition_id="prop:restated-by-the-system", occurrences=restatements
    )
    # The ten episode ids really are there — the count below is not an artifact
    # of a fixture that forgot to vary them.
    assert len(candidate.context_ids) == 10

    verdict = _evaluate(candidate)
    assert verdict.condition("recurrence").measured == 10.0
    assert verdict.condition("recurrence").passed
    assert verdict.condition("independence").measured == 1.0
    assert _failed(verdict) == ("independence",)
    assert verdict.condition("independence").reasons == (
        REASON_TOO_FEW_CONTEXTS,
        REASON_SHARED_ORIGIN,
    )
    assert verdict.eligibility == "needs_validation"
    assert not verdict.promoted
    assert verdict.record is None and verdict.diff is None


def test_origin_dependencies_survive_the_commit_boundary() -> None:
    """A restatement cannot corroborate the sources that produced the claim.

    Promotion is where an origin dependency gets lost if nothing carries it, so
    the record carries the origins and :func:`origin_after_promotion` inherits
    them. A derivation off the promoted claim therefore shares an ancestor with
    every original source, and the three of them collapse to one context."""
    record = _batch([_candidate()]).promoted[0].record
    assert record is not None
    assert len(record.origin_ids) == 3
    assert record.independent_contexts == 3

    inherited = origin_after_promotion(record)
    assert inherited.kind == RESOLVED_ORIGIN
    assert inherited.self_authored
    assert inherited.provenance == "constructed"
    assert set(record.origin_ids) < set(inherited.ancestry)
    # ...and a reading of authored prose does not present as self-authored
    assert not corpus_origin(FIRST_NOTE).self_authored
    assert inherited.depends_on(corpus_origin(SECOND_NOTE))

    mixed = _candidate(
        proposition_id="prop:restated-by-the-system",
        occurrences=(
            replace(_occurrence("episode-a", day=0.0), origin=inherited),
            _occurrence("episode-b", day=5.0),
            _occurrence("episode-c", day=10.0),
        ),
    )
    verdict = _evaluate(mixed)
    assert verdict.condition("independence").measured == 1.0
    assert _failed(verdict) == ("independence",)
    assert REASON_SHARED_ORIGIN in verdict.condition("independence").reasons


def test_a_genuinely_new_source_does_corroborate_a_restatement() -> None:
    """The control: origin-distinctness is a discriminator, not a blanket refusal.

    A rule that refused everything would pass every fixture above and be
    worthless. One restatement plus a note that was *not* among the promoted
    claim's origins is two independent contexts, and the candidate promotes."""
    record = _batch([_candidate()]).promoted[0].record
    assert record is not None
    inherited = origin_after_promotion(record)
    fresh = corpus_origin(FOURTH_NOTE)
    assert not inherited.depends_on(fresh)

    candidate = _candidate(
        proposition_id="prop:restated-by-the-system",
        occurrences=(
            replace(_occurrence("episode-a", day=0.0), origin=inherited),
            replace(
                _occurrence("episode-b", day=5.0), origin=inherited, span_text=SPAN
            ),
            replace(
                _occurrence("episode-c", day=10.0),
                origin=fresh,
                locator=f"{FOURTH_NOTE}#anchor-4d31",
            ),
        ),
    )
    verdict = _evaluate(candidate)
    assert verdict.condition("independence").measured == 2.0
    assert _failed(verdict) == ()
    assert verdict.promoted


def test_two_spans_of_one_note_are_one_origin() -> None:
    """One note is one authorial act, so its paragraphs do not corroborate.

    The span locator is deliberately outside the origin key: counting spans would
    reinstate the same failure one level down, since in a single-author corpus a
    naive counter counts habits of description."""
    one_note = tuple(
        replace(
            _occurrence(episode, day=day),
            origin=corpus_origin(FIRST_NOTE),
            locator=f"{FIRST_NOTE}#anchor-{index}",
        )
        for index, (episode, day) in enumerate(
            (("episode-a", 0.0), ("episode-b", 5.0), ("episode-c", 10.0))
        )
    )
    verdict = _evaluate(_candidate(occurrences=one_note))
    assert verdict.condition("recurrence").passed
    assert verdict.condition("independence").measured == 1.0
    assert _failed(verdict) == ("independence",)
    assert REASON_SHARED_ORIGIN in verdict.condition("independence").reasons
    # a LATER version of that note is a later reading, and does count
    assert corpus_origin(FIRST_NOTE, source_note_hash="nv:1") != corpus_origin(
        FIRST_NOTE, source_note_hash="nv:2"
    )


def test_an_occurrence_without_a_declared_origin_is_not_counted() -> None:
    """Fail-closed: an untracked origin cannot be shown to be a distinct one.

    Excluded from independence rather than counted as fresh — and still counted by
    recurrence, because the two conditions ask different questions."""
    candidate = _candidate(
        occurrences=(
            _occurrence("episode-a", day=0.0),
            replace(_occurrence("episode-b", day=5.0), origin=None),
            replace(_occurrence("episode-c", day=10.0), origin=None),
        )
    )
    assert candidate.unattributed_occurrences == 2
    verdict = _evaluate(candidate)
    assert verdict.condition("recurrence").measured == 3.0
    assert verdict.condition("independence").measured == 1.0
    assert _failed(verdict) == ("independence",)
    assert verdict.condition("independence").reasons == (
        REASON_TOO_FEW_CONTEXTS,
        REASON_ORIGIN_UNATTRIBUTED,
    )


def test_the_independence_count_does_not_depend_on_occurrence_order() -> None:
    """A replayed batch measures the same number — the union-find is canonical."""
    policy = ConsolidationPolicy()
    candidate = _candidate()
    reversed_candidate = _candidate(
        occurrences=tuple(reversed(candidate.occurrences))
    )
    forward = independence_measurement(candidate, policy)
    backward = independence_measurement(reversed_candidate, policy)
    assert forward == backward
    assert forward.count == 3
    assert not forward.collapsed_by_origin
    assert independence_count(candidate, policy) == 3


def test_the_facts_basis_is_origin_distinct_too() -> None:
    """Origin-distinctness is a second condition on the count, not an alternative.

    Three resolved ``fact_id``s that all trace to one note are still one witness;
    two that trace to two notes are two."""
    facts = ConsolidationPolicy(independence_over=INDEPENDENCE_BASIS_FACTS)
    one_origin = tuple(
        replace(
            _occurrence(episode, day=day),
            origin=corpus_origin(FIRST_NOTE),
            fact_id=f"fact-{index}",
        )
        for index, (episode, day) in enumerate(
            (("episode-a", 0.0), ("episode-b", 5.0), ("episode-c", 10.0))
        )
    )
    assert independence_count(_candidate(occurrences=one_origin), facts) == 1
    two_origins = (
        replace(_occurrence("episode-a", day=0.0), fact_id="fact-0"),
        replace(_occurrence("episode-b", day=5.0), fact_id="fact-1"),
        replace(
            _occurrence("episode-c", day=10.0, source="episode-b"), fact_id="fact-2"
        ),
    )
    assert independence_count(_candidate(occurrences=two_origins), facts) == 2


def test_the_independence_term_records_its_weakening_and_its_origin_rule() -> None:
    """Both halves are reported wherever the criterion is: it is read over
    EPISODES (weaker than distinct sources) and it is ORIGIN-DISTINCT.

    A recorded weakening, not a solved criterion: in a single-author corpus a
    naive recurrence counter counts habits of description, so both statements
    travel with the condition AND with the record."""
    verdict = _evaluate(_candidate())
    detail = verdict.condition("independence").detail
    assert FACT_ID_DEVIATION in detail
    assert INDEPENDENCE_ORIGIN_RULE in detail
    assert verdict.record is not None
    assert verdict.record.independence_basis == "episodes"
    assert verdict.record.independence_caveat == FACT_ID_DEVIATION
    assert verdict.record.independence_origin_rule == INDEPENDENCE_ORIGIN_RULE
    assert verdict.record.origin_ids == _candidate().origin_ids
    assert verdict.record.as_payload()["origin_ids"] == list(
        _candidate().origin_ids
    )


def test_an_origin_states_its_own_vocabulary() -> None:
    """The origin vocabulary is closed, and the schema columns behind it are the
    inputs: ``edges.origin`` for the kind, ``claims.provenance`` for provenance."""
    with pytest.raises(ValueError, match="note_id"):
        corpus_origin("   ")
    with pytest.raises(ValueError, match="proposition_id"):
        self_authored_origin("")
    with pytest.raises(ValueError, match="origin kind"):
        ClaimOrigin(origin_id="x", kind="invented")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="provenance"):
        ClaimOrigin(origin_id="x", provenance="hearsay")
    # an origin never inherits itself, however a caller spells it
    self_inherited = self_authored_origin("prop:x", inherited=("resolved:prop:x", ""))
    assert self_inherited.inherited == ()
    assert self_inherited.ancestry == ("resolved:prop:x",)
    assert ClaimOrigin(origin_id="a").depends_on(ClaimOrigin(origin_id="a"))
    assert not ClaimOrigin(origin_id="a").depends_on(ClaimOrigin(origin_id="b"))


# ── what every count keys on: the proposition version ───────────────────────


def test_a_revised_proposition_does_not_inherit_the_replaced_ones_feedback() -> None:
    """The subject of the trial history is the PROPOSITION VERSION.

    *"A owns X"* becoming *"B owns X"* holds the locator and changes the claim, so
    the two are one evidence occurrence and two propositions. Keying the tally on
    the evidence occurrence — the located string — handed the replacement the
    replaced claim's 8-from-8 pass record; keying it on the proposition version
    starts the replacement at the fail-closed prior of 0.5, which is what
    ``TRIAL_HISTORY_SUBJECT_RULE`` requires."""
    body = f"# Ownership\n\n{SPAN}\n"
    original = identify(
        FIRST_NOTE,
        anchor_locator(SPAN),
        PROPOSITION,
        source_note_hash=note_version_hash(body),
    )
    revised = original.revised("The billing team owns the platform.")
    assert revised.evidence_id == original.evidence_id  # one located string
    assert revised.proposition_id != original.proposition_id  # two claims

    histories = {
        original.proposition_id: TrialHistory(
            subject_id=original.proposition_id,
            subject_kind="promoted_claim",
            n_trial=8,
            n_pass=8,
        )
    }
    kept = _candidate(proposition_id=original.proposition_id)
    changed = _candidate(
        proposition_id=revised.proposition_id,
        claim_text="The billing team owns the platform.",
    )
    batch = _batch([kept, changed], histories=histories)

    assert [v.proposition_id for v in batch.promoted] == [original.proposition_id]
    inheritor = next(
        v for v in batch.verdicts if v.proposition_id == revised.proposition_id
    )
    assert inheritor.condition("reliability").measured == pytest.approx(0.5)
    assert inheritor.condition("reliability").reasons == (REASON_ETA_BELOW_FLOOR,)
    assert inheritor.lifecycle == "probationary"
    assert not inheritor.promoted


def test_the_tier_b_read_asks_for_the_proposition_version() -> None:
    """The Tier-B port is read by ``proposition_id``, not by an evidence id."""

    class RecordingHistorySource:
        def __init__(self) -> None:
            self.asked: list[tuple[str, str | None]] = []

        def cached_targets(self, query_key: str) -> CachedMapping | None:
            return None

        def trial_history(
            self, subject_id: str, *, subject_kind: str | None = None
        ) -> TrialHistory:
            self.asked.append((subject_id, subject_kind))
            return TrialHistory(
                subject_id=subject_id,
                subject_kind="promoted_claim",
                n_trial=8,
                n_pass=8,
            )

    source = RecordingHistorySource()
    assert isinstance(source, QueryCacheSource)
    batch = _batch([_candidate()], histories=None, history_source=source)
    assert source.asked == [(PROPOSITION_ID, "promoted_claim")]
    assert len(batch.promoted) == 1


def test_the_model_seams_are_asked_about_the_proposition_version() -> None:
    """Entailment, dedup and prose all name the proposition, not the evidence."""
    entailment_subjects: list[str] = []
    dedup_subjects: list[str] = []
    prose_subjects: list[str] = []

    class RecordingJudge:
        def entails(self, request: EntailmentRequest) -> EntailmentVerdict:
            entailment_subjects.append(request.proposition_id)
            return EntailmentVerdict(entailed=True, score=1.0, judge_id="test-model")

    class RecordingDedup:
        def decide(self, request: DedupRequest) -> DedupDecision:
            dedup_subjects.append(request.proposition_id)
            return DedupDecision(
                action="create", reason="no prior art", decided_by="test-model"
            )

    class RecordingAuthor:
        def author(self, request: ProseRequest) -> str:
            prose_subjects.append(request.proposition_id)
            return AdditiveProseAuthor().author(request)

    verdict = _evaluate(
        _candidate(),
        entailment=RecordingJudge(),
        dedup=RecordingDedup(),
        prose_author=RecordingAuthor(),
    )
    assert _failed(verdict) == ()
    assert set(entailment_subjects) == {PROPOSITION_ID}
    assert dedup_subjects == [PROPOSITION_ID]
    assert prose_subjects == [PROPOSITION_ID]


def test_occurrences_of_another_proposition_version_are_refused() -> None:
    """A candidate may not fold in another proposition's derivations.

    Recurrence and feedback are counted per proposition version, so a stamped
    occurrence that names a different one is a defect at the door rather than an
    inflated count later."""
    stamped = replace(
        _occurrence("episode-a", day=0.0), proposition_id=PROPOSITION_ID
    )
    foreign = replace(
        _occurrence("episode-b", day=5.0), proposition_id="prop:something-else"
    )
    assert _candidate(occurrences=(stamped,)).recurrence == 1
    with pytest.raises(ValueError, match="another proposition version"):
        _candidate(occurrences=(stamped, foreign))


# ── condition 3: reliability (eta + the correction flag) ─────────────────────


def test_eta_below_the_floor_fails_only_the_reliability_condition() -> None:
    """η = (5+1)/(8+2) = 0.6 < 0.8 → probationary, not active, and not promoted."""
    candidate = _candidate()
    history = TrialHistory(
        subject_id=candidate.proposition_id,
        subject_kind="promoted_claim",
        n_trial=8,
        n_pass=5,
    )
    verdict = _evaluate(candidate, history=history)
    assert _failed(verdict) == ("reliability",)
    assert verdict.condition("reliability").reasons == (REASON_ETA_BELOW_FLOOR,)
    assert verdict.condition("reliability").measured == pytest.approx(0.6)
    assert verdict.lifecycle == "probationary"
    assert verdict.eligibility == "needs_validation"


def test_no_trial_history_is_probationary_rather_than_promotable() -> None:
    """The Laplace prior is fail-closed: η = 1/2 with nothing recorded."""
    verdict = _evaluate(_candidate(), history=None)
    assert verdict.condition("reliability").measured == pytest.approx(0.5)
    assert not verdict.promoted
    assert verdict.lifecycle == "probationary"


def test_an_open_correction_flag_refuses_rather_than_defers() -> None:
    """A low η is "not yet trusted"; an open flag is "known wrong" — ineligible."""
    candidate = _candidate()
    history = TrialHistory(
        subject_id=candidate.proposition_id,
        subject_kind="promoted_claim",
        n_trial=8,
        n_pass=8,
        open_corrections=(
            CorrectionFlag(
                flag_id="flag-1",
                subject_id=candidate.proposition_id,
                subject_kind="promoted_claim",
                episode_id="episode-d",
                raised_at=BASE_AT,
                reason="a reader reported the wrong owner",
            ),
        ),
    )
    verdict = _evaluate(candidate, history=history)
    assert _failed(verdict) == ("reliability",)
    assert REASON_OPEN_CORRECTION in verdict.condition("reliability").reasons
    assert verdict.eligibility == "ineligible"


def test_reliability_reads_the_shipped_tier_b_tally() -> None:
    """η comes from the tier that owns it, over real feedback events.

    The gate is not a second implementation of the arithmetic: the events go
    through ``tally_trials`` and the outcome through ``meets_reliability_gate``,
    so a change to either lands here rather than drifting."""
    candidate = _candidate()
    events = [
        FeedbackEvent(
            kind="verdict",
            subject_id=candidate.proposition_id,
            subject_kind="promoted_claim",
            episode_id=f"episode-{i}",
            at=BASE_AT + i,
            verdict="correct",
        )
        for i in range(8)
    ]
    history = tally_trials(
        events, subject_id=candidate.proposition_id, subject_kind="promoted_claim"
    )
    assert history.eta == pytest.approx(0.9)
    verdict = _evaluate(candidate, history=history)
    assert verdict.condition("reliability").passed
    assert verdict.condition("reliability").measured == pytest.approx(0.9)


# ── condition 4: stability across the dwell window ──────────────────────────


def test_inside_the_dwell_window_fails_only_the_stability_condition() -> None:
    """Three episodes over two days: too young to have been stable."""
    candidate = _candidate(
        occurrences=(
            _occurrence("episode-a", day=0.0),
            _occurrence("episode-b", day=1.0),
            _occurrence("episode-c", day=2.0),
        )
    )
    verdict = _evaluate(candidate)
    assert _failed(verdict) == ("stability",)
    assert verdict.condition("stability").reasons == (REASON_INSIDE_DWELL_WINDOW,)
    assert verdict.condition("stability").measured == pytest.approx(2.0)
    assert verdict.condition("stability").threshold == pytest.approx(7.0)


def test_an_answer_that_moved_inside_the_window_fails_stability() -> None:
    """A long enough dwell is not stability if the answer changed within it."""
    candidate = _candidate(
        occurrences=(
            _occurrence("episode-a", day=0.0),
            _occurrence("episode-b", day=5.0, answer="answer-2"),
            _occurrence("episode-c", day=10.0),
        )
    )
    verdict = _evaluate(candidate)
    assert _failed(verdict) == ("stability",)
    assert REASON_ANSWER_CHANGED in verdict.condition("stability").reasons


def test_the_dwell_window_is_parameterised_inside_the_stated_range() -> None:
    """7–14 days, validated at construction and refused rather than clamped."""
    strict = ConsolidationPolicy(dwell_days=DWELL_WINDOW_DAYS_MAX)
    candidate = _candidate()  # a 10-day dwell
    assert not _evaluate(candidate, policy=strict).condition("stability").passed
    lenient = ConsolidationPolicy(dwell_days=DWELL_WINDOW_DAYS_MIN)
    assert _evaluate(candidate, policy=lenient).condition("stability").passed
    with pytest.raises(ValueError, match="dwell_days"):
        ConsolidationPolicy(dwell_days=DWELL_WINDOW_DAYS_MAX + 1)
    with pytest.raises(ValueError, match="dwell_days"):
        ConsolidationPolicy(dwell_days=DWELL_WINDOW_DAYS_MIN - 1)


# ── condition 5: grounding (the hard entailment gate) ───────────────────────


def test_a_refuted_entailment_fails_only_the_grounding_condition() -> None:
    candidate = _candidate()
    verdict = _evaluate(
        candidate, entailment=StaticEntailmentJudge(refuted_spans=ENTAILING_SPANS)
    )
    assert _failed(verdict) == ("grounding",)
    assert verdict.condition("grounding").reasons == (REASON_ENTAILMENT_FAILED,)
    assert verdict.eligibility == "ineligible"
    assert verdict.record is None


def test_an_uncalibrated_judge_abstains_and_that_refuses() -> None:
    """Abstention is a refusal, never a pass — the fail-closed reading.

    The shipped default judge abstains on everything precisely because no
    calibrated entailment model exists for query-time relation claims, so the
    default configuration promotes nothing at all."""
    verdict = _evaluate(_candidate(), entailment=UncalibratedEntailmentJudge())
    assert _failed(verdict) == ("grounding",)
    assert verdict.condition("grounding").reasons == (REASON_ENTAILMENT_ABSTAINED,)
    assert verdict.entailment[0].abstained
    assert not verdict.entailment[0].entailed


def test_every_cited_span_must_entail_not_merely_the_best_one() -> None:
    """Taking the best of k would make the gate weaker the more a claim recurred."""
    candidate = _candidate(
        occurrences=(
            _occurrence("episode-a", day=0.0),
            _occurrence("episode-b", day=5.0),
            replace(
                _occurrence("episode-c", day=10.0),
                locator="note-ownership#anchor-other",
                span_text="An unrelated span that says nothing about ownership.",
            ),
        )
    )
    verdict = _evaluate(candidate)
    assert _failed(verdict) == ("grounding",)
    assert REASON_ENTAILMENT_ABSTAINED in verdict.condition("grounding").reasons


# ── condition 6: dedup / link-before-create ─────────────────────────────────


def test_a_near_duplicate_fails_only_the_dedup_condition() -> None:
    """Prior art above τ → the reference judge links instead of creating."""
    index = StaticPriorArtIndex(
        entries=(
            PriorArtEntry(
                entry_id="prior-1",
                note_id="note-ownership-existing",
                text="The accounts team owns the platform.",
                embedding=(1.0, 0.0, 0.0),
            ),
        )
    )
    verdict = _evaluate(_candidate(), prior_art=index)
    assert _failed(verdict) == ("dedup",)
    assert verdict.condition("dedup").reasons == (REASON_NEAR_DUPLICATE,)
    assert verdict.dedup.action == "append"
    assert verdict.dedup.prior_art_id == "prior-1"
    assert verdict.eligibility == "ineligible"


def test_the_prefilter_is_arithmetic_and_the_decision_is_the_models() -> None:
    """τ and top-k shortlist; a MODEL decides append-vs-create over the shortlist.

    An injected judge that reads the shortlisted neighbour as a *different* fact
    lets the candidate through — proving the threshold does not decide. That is
    criterion 5 as written, and an earlier reading of it as arithmetic was wrong.
    """

    class AlwaysCreateJudge:
        def decide(self, request: DedupRequest) -> DedupDecision:
            assert request.shortlist, "the pre-filter should have shortlisted"
            return DedupDecision(
                action="create",
                reason="the shortlisted neighbour states a different fact",
                decided_by="test-model",
            )

    index = StaticPriorArtIndex(
        entries=(
            PriorArtEntry(
                entry_id="prior-1",
                note_id="note-other",
                text="A superficially similar sentence.",
                embedding=(1.0, 0.0, 0.0),
            ),
        )
    )
    judge: DedupJudge = AlwaysCreateJudge()
    assert isinstance(judge, DedupJudge)
    verdict = _evaluate(_candidate(), prior_art=index, dedup=judge)
    assert _failed(verdict) == ()
    assert verdict.dedup.decided_by == "test-model"
    # ...and the shortlist itself was purely arithmetic.
    shortlist = prior_art_shortlist(
        _candidate(), index, ConsolidationPolicy()
    )
    assert [m.entry.entry_id for m in shortlist] == ["prior-1"]
    assert cosine((1.0, 0.0, 0.0), (1.0, 0.0, 0.0)) == pytest.approx(1.0)
    assert cosine((1.0, 0.0, 0.0), ()) == 0.0


def test_a_candidate_without_an_embedding_cannot_be_dedup_checked() -> None:
    """No pre-filter means an unruled-out duplicate, and that refuses."""
    verdict = _evaluate(_candidate(embedding=()))
    assert _failed(verdict) == ("dedup",)
    assert verdict.condition("dedup").reasons == (REASON_NO_EMBEDDING,)


# ── renderability: the closed effect vocabulary ─────────────────────────────


def test_a_registry_target_is_refused_because_no_effect_kind_renders_it() -> None:
    """Growing the effect vocabulary means a renderer exists — not this module's
    call, so a registry promotion is refused rather than smuggled in as
    something else."""
    verdict = _evaluate(_candidate(target="registry"))
    assert _failed(verdict) == ("renderable",)
    assert verdict.condition("renderable").reasons == (REASON_NO_RENDERER,)
    assert verdict.eligibility == "ineligible"


def test_a_note_promotion_without_a_neighbourhood_anchor_is_refused() -> None:
    """An unscoped writeback is the qualifier-stripping failure with another name."""
    verdict = _evaluate(_candidate(neighbourhood_anchor=""))
    assert _failed(verdict) == ("renderable",)


# ── the guards ──────────────────────────────────────────────────────────────


def test_promotion_is_default_off() -> None:
    assert PROMOTION_ENABLED_BY_DEFAULT is False
    with pytest.raises(ConsolidationDisabledError, match="DEFAULT-OFF"):
        run_consolidation_batch(
            [_candidate()],
            sign_off_policy=HUMAN_POLICY,
            reviewer_id=REVIEWER,
            reasoning_backend_id=BACKEND,
            ab_gate=ADMITTED_AB,
        )


def test_the_unrun_promotion_ab_refuses_even_when_enabled() -> None:
    """The entry condition is a measurement, and the shipped one is un-measured."""
    assert not UNRUN_PROMOTION_AB.admitted
    for gate in (None, UNRUN_PROMOTION_AB):
        with pytest.raises(PromotionABNotRunError):
            _batch([_candidate()], ab_gate=gate)
    # every shape requirement is enforced, not just the delta
    for broken in (
        replace(ADMITTED_AB, runs_per_arm=1),
        replace(ADMITTED_AB, orderings=1),
        replace(ADMITTED_AB, delta=0.01),
        replace(ADMITTED_AB, holds_under_every_ordering=False),
        replace(ADMITTED_AB, regression_checked=("relationship",)),
        replace(ADMITTED_AB, regression_free=False),
    ):
        assert not broken.admitted
        with pytest.raises(PromotionABNotRunError):
            _batch([_candidate()], ab_gate=broken)


def test_the_batch_refuses_to_run_with_use_human_false() -> None:
    """The acceptance clause: the human gate is REQUESTED, never assumed.

    Both shipped defaults are refused — the policy's own default
    (``use_agent=True, use_human=False``) and the digestion entry points'
    (``use_agent=False, use_human=False``), the latter of which would make a
    program-gate pass terminal with nobody in the loop."""
    assert SignOffPolicy().use_human is False
    for policy in (
        SignOffPolicy(),
        SignOffPolicy(use_agent=False, use_human=False),
        SignOffPolicy(use_agent=True, use_human=False),
    ):
        with pytest.raises(HumanGateError, match="use_human=True"):
            _batch([_candidate()], sign_off_policy=policy)


def test_the_batch_refuses_when_the_mover_is_the_judge() -> None:
    """The reasoning backend may not review its own promotion — normalised."""
    with pytest.raises(MoverIsJudgeError):
        _batch([_candidate()], reviewer_id=BACKEND)
    with pytest.raises(MoverIsJudgeError):
        _batch([_candidate()], reviewer_id=f"  {BACKEND.upper()} ")
    with pytest.raises(MoverIsJudgeError, match="reviewer_id"):
        _batch([_candidate()], reviewer_id="")


def test_the_authority_ladder_caps_the_promotion_act() -> None:
    """Promotion is an ACCEPT act, permanently capped below ``auto``."""
    with pytest.raises(AuthorityLadderError):
        AuthorityLadder(rungs={"ACCEPT": "auto"})
    ladder = AuthorityLadder(rungs={"ACCEPT": "auto_in_odd"})
    assert require_authority(ladder) != "auto"
    assert require_authority(None) == "suggest"
    ladder.kill()
    with pytest.raises(AuthorityCapError):
        _batch([_candidate()], authority=ladder)


# ── the reviewed diff, not a silent write ───────────────────────────────────


def test_a_claim_meeting_every_condition_produces_a_reviewed_diff() -> None:
    """The acceptance clause: a reviewed diff and proposed effects, no write.

    Three things are asserted together because they are one property: a human is
    ASKED (``review.required``), the artifact they read is a unified diff over the
    neighbourhood, and what reaches the vault is a proposal the commit tail
    renders — never a write from here."""
    batch = _batch([_candidate()])
    assert len(batch.promoted) == 1
    verdict = batch.promoted[0]
    assert verdict.diff is not None

    diff = verdict.diff
    assert diff.scope == SCOPE_NEIGHBOURHOOD
    assert diff.before_text == NEIGHBOURHOOD
    assert diff.before_text in diff.after_text
    unified = diff.unified()
    assert unified, "a reviewed diff has to be renderable"
    assert any(line.startswith("+") and not line.startswith("+++") for line in unified.splitlines())

    # coexistence, not supersession: no authored line is removed or rewritten
    assert diff.removed_lines == ()
    assert diff.is_additive

    # the human gate is a REQUEST the caller must satisfy, not a decision here
    assert batch.review.required is True
    assert batch.review.diff_count == 1
    assert batch.review.blast_radius == 1
    assert batch.review.reviewer_id == REVIEWER

    # the only output is proposed effects, in the validated closed vocabulary
    kinds = [effect.kind for effect in batch.effects]
    assert kinds == ["claim", "note"]
    assert set(kinds) <= EFFECT_KINDS
    note_effect = batch.effects[1]
    assert note_effect.payload["scope"] == SCOPE_NEIGHBOURHOOD
    assert note_effect.payload["neighbourhood_anchor"] == "ownership"
    assert note_effect.payload["rewrites"] == []
    assert note_effect.payload["coexists"] is True


def test_evaluating_a_candidate_proposes_nothing_renderable() -> None:
    """Measuring the gate is not promoting: the evaluator emits no effects.

    So the guards cannot be bypassed by calling the arithmetic directly — the
    effects only exist past ``run_consolidation_batch``."""
    verdict = _evaluate(_candidate())
    assert verdict.promoted
    assert verdict.effects == ()
    assert _batch([_candidate()]).promoted[0].effects != ()


def test_a_relation_promotion_lands_as_a_resolved_tier_a_row() -> None:
    """The other renderable target: ``origin='resolved'``, layered on the seed.

    Grown from query traffic — the row exists because an episode derived it, not
    because anything enumerated entity pairs."""
    candidate = _candidate(
        target="relation",
        subject_id="entity-accounts-team",
        predicate="owns",
        object_ref="entity-platform",
        valid_from="2026-03-01",
    )
    batch = _batch([candidate])
    assert len(batch.promoted) == 1
    relation_effect = batch.effects[1]
    assert relation_effect.kind == "relation"
    assert relation_effect.payload["origin"] == RESOLVED_ORIGIN
    assert relation_effect.payload["subject_id"] == "entity-accounts-team"
    assert relation_effect.payload["valid_from"] == "2026-03-01"
    assert relation_effect.payload["evidence_locator"] == LOCATOR
    # status stays computed elsewhere; promotion never mints a verdict
    assert relation_effect.payload["epistemic_status"] == "proposed"


def test_a_relation_promotion_without_its_triple_is_refused() -> None:
    verdict = _evaluate(_candidate(target="relation"))
    assert _failed(verdict) == ("renderable",)


# ── qualifiers survive ──────────────────────────────────────────────────────


def test_a_promoted_claim_retains_its_date_and_authority_qualifiers() -> None:
    """The acceptance clause, against the measured failure mode.

    Rewrites strip qualifiers — dates survived 3% of the time and authority
    collapsed in 48 of 49 configurations — so the qualifier text and the
    provenance locator are asserted present in the promoted rendering, in the
    diff a reviewer reads, and in the record."""
    batch = _batch([_candidate()])
    diff = batch.promoted[0].diff
    assert diff is not None
    for qualifier in (DATE_QUALIFIER, AUTHORITY_QUALIFIER):
        assert qualifier.text in diff.added_text
        assert qualifier.text in diff.after_text
        assert qualifier.text in diff.unified()
    assert LOCATOR in diff.added_text

    record = batch.promoted[0].record
    assert record is not None
    assert record.qualifiers == (DATE_QUALIFIER, AUTHORITY_QUALIFIER)
    kinds = {q["kind"] for q in record.as_payload()["qualifiers"]}
    assert kinds == {"date", "authority"}


def test_a_stripping_prose_author_is_refused() -> None:
    """The author's output is re-read, not trusted: a strip raises."""

    class StrippingAuthor:
        def author(self, request: ProseRequest) -> str:
            return request.claim_text  # drops every qualifier and locator

    author: PromotionProseAuthor = StrippingAuthor()
    assert isinstance(author, PromotionProseAuthor)
    with pytest.raises(QualifierStrippedError, match="date"):
        _evaluate(_candidate(), prose_author=author)


def test_the_reference_author_is_additive_and_never_rewrites() -> None:
    """It is never shown the authored text, so it cannot rewrite it."""
    request = ProseRequest(
        proposition_id=PROPOSITION_ID,
        claim_text=PROPOSITION,
        qualifiers=(DATE_QUALIFIER,),
        locators=(LOCATOR,),
        target_note_id="note-ownership",
        neighbourhood_anchor="ownership",
    )
    text = AdditiveProseAuthor().author(request)
    assert DATE_QUALIFIER.text in text
    assert LOCATOR in text
    assert RESOLVED_ORIGIN in text
    assert NEIGHBOURHOOD not in text


# ── the promotion record: the demotion handle ───────────────────────────────


def test_a_promotion_record_exists_and_is_sufficient_to_demote_by() -> None:
    """The acceptance clause: without the record, demotion has nothing to grab.

    Sufficiency is checked per demotion trigger — the cited spans a suppressed
    claim would be re-derived from, the source claim ids plus the snapshot pin a
    status flip is read against, and the context ids **with the origin ids** the
    independence floor is recomputed over. Episodes alone would let a
    re-derivation off this very claim hold the floor up on its own."""
    batch = _batch([_candidate()])
    record = batch.promoted[0].record
    assert record is not None

    assert record.source_claim_ids == ("claim-episode-a", "claim-episode-b", "claim-episode-c")
    assert record.occurrence_count == 3
    assert record.context_ids == ("episode-a", "episode-b", "episode-c")
    assert len(record.observed_at) == 3
    assert record.eta == pytest.approx(0.9)
    assert record.base_snapshot_id == "edgeset-digest-9a"
    assert record.lifecycle == "active"
    assert record.reviewer_id == REVIEWER
    assert record.reasoning_backend_id == BACKEND

    handle = record.demotion_handle()
    assert record.sufficient_to_demote
    assert handle.is_sufficient
    # what a frozen re-derivation is given: every cited span, one per source
    assert handle.cited_spans == (SPAN, SECOND_SPAN, THIRD_SPAN)
    assert handle.cited_locators == (LOCATOR, SECOND_LOCATOR, THIRD_LOCATOR)
    assert handle.context_ids == record.context_ids
    assert handle.origin_ids == record.origin_ids
    assert handle.base_snapshot_id == record.base_snapshot_id

    # a gap in ANY trigger's inputs makes the handle insufficient, fail-closed
    assert not replace(handle, cited_spans=()).is_sufficient
    assert not replace(handle, base_snapshot_id="").is_sufficient
    assert not replace(handle, context_ids=()).is_sufficient
    assert not replace(handle, origin_ids=()).is_sufficient
    assert not replace(handle, source_claim_ids=()).is_sufficient

    # and it rides as a first-class effect, not as a side note
    record_effect = batch.effects[0]
    assert record_effect.kind == "claim"
    assert record_effect.bb_role == "promotion_record"
    payload = record_effect.payload["promotion_record"]
    assert payload["record_id"] == record.record_id
    assert payload["context_ids"] == list(record.context_ids)
    assert payload["origin_ids"] == list(record.origin_ids)
    assert payload["eta"] == pytest.approx(0.9)
    assert record_effect.payload["demotion_handle_sufficient"] is True


def _gate_over_handle(
    handle,
    *,
    regenerates: str | None,
    status: str = "warranted",
) -> ReDerivationGate:
    """A re-derivation gate wired from the promotion handle and nothing else.

    Every port is filled from a handle field, which is the claim under test: the
    cited spans become the only thing the frozen model is shown, the context ids
    become the independence count, and the claim id comes from the record's own
    source claims. ``regenerates=None`` scripts nothing, so the reference model
    ABSTAINS — the fail-closed reading of "the claim did not come back".

    P10 still keys its own ports on a field it calls ``derivation_id`` and still
    counts *episodes* for the independence trigger; the handle's
    ``proposition_id`` is what is fed to it here, and its ``origin_ids`` are what
    that trigger will need once it is origin-distinct too."""
    claim_id = handle.source_claim_ids[0]
    return ReDerivationGate(
        model=FrozenReDerivationModel(
            ScriptedReDerivationModel(
                outputs=(
                    {} if regenerates is None else {handle.proposition_id: regenerates}
                )
            ),
            model_id="scripted-reference-model",
            frozen_at=BASE_AT,
            corpus_snapshot_id=handle.base_snapshot_id,
        ),
        sources=StaticSourceReader(
            {
                claim_id: tuple(
                    CitedSource(
                        note_id=handle.target_note_id, locator=locator, text=span
                    )
                    for locator, span in zip(handle.cited_locators, handle.cited_spans)
                )
            }
        ),
        statuses=StaticStatusSource({claim_id: status}),
        independence=StaticIndependenceSource(
            {handle.proposition_id: handle.context_ids}
        ),
    )


def _view_from_handle(handle, promoted_text: str) -> PromotedClaimRecord:
    """P10's record view, assembled out of P12's handle — the seam under test."""
    return PromotedClaimRecord(
        claim_id=handle.source_claim_ids[0],
        derivation_id=handle.proposition_id,
        text=promoted_text,
        note_id=handle.target_note_id,
        locator=handle.cited_locators[0],
        status_at_promotion="warranted",
        episode_ids=handle.context_ids,
        occurrences=len(handle.context_ids),
        promoted_at=BASE_AT,
        base_snapshot_id=handle.base_snapshot_id,
    )


def test_the_demotion_gate_can_demote_from_the_record_alone() -> None:
    """End-to-end through P10: suppress the promoted claim, re-derive from the
    handle's cited sources with a frozen model, and demote on failure — wiring
    every port out of the promotion record and nothing else.

    This is the clause the field-by-field checks above can only approximate. A
    handle that looked sufficient but did not actually satisfy the gate's ports
    would pass those and fail here, which is the whole reason the record exists:
    *without it demotion has nothing to grab.*"""
    verdict = _batch([_candidate()]).promoted[0]
    record = verdict.record
    assert record is not None and verdict.diff is not None
    handle = record.demotion_handle()
    assert handle.is_sufficient

    view = _view_from_handle(handle, verdict.diff.added_text)
    later = BASE_AT + 30 * DAY

    # The claim does not come back from its own cited sources → demoted, on the
    # trigger an attack-driven system would never see (nothing attacked it).
    failing = _gate_over_handle(handle, regenerates=None).review(view, now=later)
    assert failing.demoted
    assert failing.triggers == (TRIGGER_REDERIVATION_FAILURE,)
    assert not failing.status_flip.flipped  # still warranted
    assert not failing.independence.below_floor  # still independent
    assert failing.promotion_eligibility == "ineligible"

    # And the same handle CLEARS the gate when the claim does regenerate, so the
    # demotion above is a finding about the claim rather than about the wiring.
    holding = _gate_over_handle(handle, regenerates=view.text).review(view, now=later)
    assert not holding.demoted
    assert holding.triggers == ()
    assert holding.promotion_eligibility == "eligible"


def test_the_record_id_is_content_addressed_so_a_replay_matches() -> None:
    first = _batch([_candidate()]).promoted[0].record
    second = _batch([_candidate()]).promoted[0].record
    assert first is not None and second is not None
    assert first.record_id == second.record_id


# ── the lifecycle ───────────────────────────────────────────────────────────


def test_the_lifecycle_is_probationary_then_active_then_archived() -> None:
    assert lifecycle_for(all_conditions_met=True, eta=0.9, floor=0.8) == "active"
    assert lifecycle_for(all_conditions_met=True, eta=0.6, floor=0.8) == "probationary"
    assert lifecycle_for(all_conditions_met=False, eta=0.9, floor=0.8) == "probationary"
    assert (
        lifecycle_for(all_conditions_met=True, eta=0.9, floor=0.8, archived=True)
        == "archived"
    )


# ── the batch's own bookkeeping ─────────────────────────────────────────────


def test_the_batch_partitions_its_candidates_and_promotes_only_the_eligible() -> None:
    promotable = _candidate()
    deferred = _candidate(
        proposition_id="prop:deferred",
        occurrences=(
            _occurrence("episode-a", day=0.0),
            _occurrence("episode-b", day=10.0),
        ),
    )
    refused = _candidate(proposition_id="prop:refused", target="registry")
    batch = _batch([promotable, deferred, refused])
    assert [v.proposition_id for v in batch.promoted] == [PROPOSITION_ID]
    assert [v.proposition_id for v in batch.deferred] == ["prop:deferred"]
    assert [v.proposition_id for v in batch.refused] == ["prop:refused"]
    assert len(batch.effects) == 2  # only the promoted one proposes anything
    assert len(batch.diffs) == 1 and len(batch.records) == 1
    assert batch.independence_caveat == FACT_ID_DEVIATION


# ── the Dependency Rule ─────────────────────────────────────────────────────


def test_the_consolidation_module_never_imports_the_runtime() -> None:
    """Pure: no runtime import, no disk, no vault write from the kernel side."""
    source = CONSOLIDATION_SOURCE.read_text(encoding="utf-8")
    code = "\n".join(
        line for line in source.splitlines() if not line.lstrip().startswith("#")
    )
    body = code.split('"""', 2)[-1]  # drop the module docstring, which names it
    assert "tessellum.runtime" not in body
    assert "import sqlite3" not in body
    assert "open(" not in body
    assert "write_text" not in body


def test_the_log_and_edge_vocabularies_are_append_only_here() -> None:
    """No UPDATE and no DELETE: a retraction is an append, made elsewhere."""
    source = CONSOLIDATION_SOURCE.read_text(encoding="utf-8").upper()
    assert "UPDATE " not in source
    assert "DELETE " not in source


# ── seams are protocols, and the references satisfy them ────────────────────


def test_the_three_model_seams_are_injected_protocols() -> None:
    from tessellum.dks.consolidation import EntailmentJudge, PriorArtIndex

    assert isinstance(UncalibratedEntailmentJudge(), EntailmentJudge)
    assert isinstance(StaticEntailmentJudge(), EntailmentJudge)
    assert isinstance(StaticPriorArtIndex(), PriorArtIndex)
    assert isinstance(LinkBeforeCreateJudge(), DedupJudge)
    assert isinstance(AdditiveProseAuthor(), PromotionProseAuthor)
    # and the default judge really is the fail-closed one
    verdict = UncalibratedEntailmentJudge().entails(
        EntailmentRequest(
            proposition_id="prop:x",
            claim_text="anything",
            locator=LOCATOR,
            span_text=SPAN,
        )
    )
    assert isinstance(verdict, EntailmentVerdict)
    assert verdict.abstained and not verdict.entailed
