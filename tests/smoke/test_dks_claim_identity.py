"""P0 — derived-claim identity (``dks/claim_identity.py``).

**Three identities, not two.** The shipped two-level key
``(note_id, span_locator)`` is the model the plan's A7 correction rejected: one
span states several independent propositions, so the location-only key gave an
owner claim, a launch-date claim, a rival owner claim and a *negation* the SAME
id — and anything keying feedback on that id hands a changed proposition the
replaced one's history. Two tests here previously asserted that collapse as the
acceptance criterion; they are flipped.

The acceptance line, one test group each:
 1. two propositions in ONE span stay distinct (an owner and a launch date);
 2. one proposition citing THREE spans is one proposition;
 3. a harmless paraphrase coalesces — under a scripted resolver, never by
    wording;
 4. a NEGATION does not coalesce (fail-safe: no merge without a resolver, and no
    merge at all across a declared polarity);
 5. an ownership change inherits neither the old warrant nor the old feedback.

Plus the retained clause — inserting a sentence above a claim does not change any
later claim's id — and the properties that make those true rather than
accidental: no domain predicate in any key, the content-id construction agrees
with the replay token, the cross-span fact layer is a PORT with no lexical
heuristic behind it, and the module stays pure.
"""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

import tessellum.dks.claim_identity as claim_identity
from tessellum.composer.claim_extraction import extract_claims
from tessellum.composer.knowledge_plan import ClaimProvenance
from tessellum.dks.capability import _replay_token
from tessellum.dks.claim_identity import (
    FACT_ID_DEVIATION,
    FAIL_SAFE_MERGE_RULE,
    TRIAL_HISTORY_SUBJECT_RULE,
    UNPINNED_SOURCE_VERSION,
    ClaimRendering,
    DerivationEvent,
    DerivedClaimIdentity,
    EvidenceOccurrence,
    FactIdentityResolver,
    PropositionVersion,
    ScriptedFactIdentity,
    SpanLocator,
    UnresolvedFactIdentity,
    anchor_locator,
    char_range_locator,
    coalesce_propositions,
    derivation_event,
    derivation_event_id,
    derivation_id,
    derivation_ids_for_spans,
    evidence_occurrence,
    evidence_occurrence_id,
    evidence_occurrence_ids_for_spans,
    feedback_subject_id,
    identify,
    locators_for_spans,
    normalize_span_text,
    note_version_hash,
    proposition_version,
    proposition_version_id,
    text_hash,
)

_SPAN = "The scheduler retries a failed batch at most three times."

# One paragraph that states TWO independent facts — the A7 fixture.
_TWO_FACT_SPAN = (
    "The queue service is owned by team alpha, and it went live on the first "
    "of the month."
)
_OWNER = "Team Alpha owns the queue service."
_LAUNCH = "The queue service went live on the first of the month."
_RIVAL_OWNER = "Team Beta owns the queue service."
_OWNER_PARAPHRASE = "The queue service is owned by Team Alpha."
_OWNER_DENIED = "Team Alpha owns the queue service."  # denied via polarity


def _prov(*refs: str) -> tuple[ClaimProvenance, ...]:
    return tuple(ClaimProvenance(span_id=f"s{i}", source_ref=r)
                 for i, r in enumerate(refs))


def _module_source() -> str:
    """The module's own source, read via its ``__file__`` so the purity guards
    below do not depend on the test runner's working directory."""
    return Path(claim_identity.__file__).read_text(encoding="utf-8")


def _rendering(prop: PropositionVersion) -> ClaimRendering:
    return ClaimRendering(proposition=prop, context=_TWO_FACT_SPAN)


# ── acceptance 1: two propositions in ONE span stay distinct ────────────────


def test_two_propositions_in_one_span_stay_distinct() -> None:
    # The flip: this is the case the shipped two-level key collapsed. One span,
    # two independent facts read out of it -> ONE evidence occurrence, TWO
    # propositions.
    loc = anchor_locator(_TWO_FACT_SPAN)
    owner = identify("note-a", loc, _OWNER)
    launch = identify("note-a", loc, _LAUNCH)

    assert owner.evidence_id == launch.evidence_id  # same located string
    assert owner.proposition_id != launch.proposition_id  # different claims
    # and the legacy spelling names the EVIDENCE, so it is equal by design.
    assert owner.derivation_id == owner.evidence_id


def test_a_rival_claim_in_the_same_span_is_a_different_proposition() -> None:
    loc = anchor_locator(_TWO_FACT_SPAN)
    alpha = identify("note-a", loc, _OWNER)
    beta = identify("note-a", loc, _RIVAL_OWNER)
    assert alpha.evidence_id == beta.evidence_id
    assert alpha.proposition_id != beta.proposition_id


def test_four_readings_of_one_span_are_four_propositions() -> None:
    # owner, launch date, negation of the owner, rival owner — all one span. The
    # shipped key minted ONE id for all four; each must now be its own.
    loc = anchor_locator(_TWO_FACT_SPAN)
    ids = {
        identify("note-a", loc, _OWNER).proposition_id,
        identify("note-a", loc, _LAUNCH).proposition_id,
        identify("note-a", loc, _OWNER_DENIED, polarity="deny").proposition_id,
        identify("note-a", loc, _RIVAL_OWNER).proposition_id,
    }
    assert len(ids) == 4
    # ... over exactly one piece of evidence.
    assert len({identify("note-a", loc, t).evidence_id
                for t in (_OWNER, _LAUNCH, _RIVAL_OWNER)}) == 1


def test_a_declared_scope_or_qualifier_forks_the_proposition() -> None:
    base = proposition_version_id(_OWNER)
    assert proposition_version_id(_OWNER, scope={"region": "north"}) != base
    assert proposition_version_id(_OWNER, qualifiers={"as_of": "2026-01"}) != base
    # ... and the pairs are order-insensitive, so identity is not input-order.
    assert proposition_version_id(
        _OWNER, scope=[("region", "north"), ("tier", "gold")]
    ) == proposition_version_id(
        _OWNER, scope=[("tier", "gold"), ("region", "north")]
    )


def test_no_domain_predicate_enters_any_key() -> None:
    # A predicate is a model act; neither key has a slot for one.
    loc = anchor_locator(_SPAN, section="## Behaviour")
    canonical = loc.canonical()
    assert canonical.startswith("anchor|## Behaviour|")
    assert "predicate" not in canonical
    assert not any("predicate" in f for f in SpanLocator.__dataclass_fields__)
    assert not any("predicate" in f for f in PropositionVersion.__dataclass_fields__)


def test_same_span_in_two_notes_is_two_occurrences() -> None:
    loc = anchor_locator(_SPAN)
    assert evidence_occurrence_id("note-a", loc) != evidence_occurrence_id("note-b", loc)


def test_same_sentence_under_two_sections_is_two_spans() -> None:
    a = anchor_locator(_SPAN, section="## One")
    b = anchor_locator(_SPAN, section="## Two")
    assert evidence_occurrence_id("note-a", a) != evidence_occurrence_id("note-a", b)


def test_an_occurrence_is_a_located_string_at_a_source_version() -> None:
    loc = anchor_locator(_SPAN)
    v1 = EvidenceOccurrence("note-a", loc, note_version_hash("body one"))
    v2 = v1.at_version(note_version_hash("body one, edited"))
    assert v1.occurrence_id != v2.occurrence_id  # the staleness signal
    assert v1.version_pinned and v2.version_pinned
    assert EvidenceOccurrence("note-a", loc).version_pinned is False
    assert EvidenceOccurrence("note-a", loc).source_note_hash == UNPINNED_SOURCE_VERSION
    assert evidence_occurrence("note-a", _SPAN).occurrence_id == v1.at_version(
        UNPINNED_SOURCE_VERSION
    ).occurrence_id


# ── acceptance 2: one proposition citing three spans is ONE proposition ─────


def test_one_proposition_citing_three_spans_is_one_proposition() -> None:
    spans = [
        "The queue service is operated by the platform group.",
        "The platform group is led by Team Alpha.",
        "Team Alpha reports the queue service in its own review.",
    ]
    cited = [
        evidence_occurrence("note-a", spans[0]).occurrence_id,
        evidence_occurrence("note-b", spans[1]).occurrence_id,
        evidence_occurrence("note-c", spans[2]).occurrence_id,
    ]
    multi_hop = proposition_version(_OWNER, evidence=cited)

    assert len(multi_hop.evidence) == 3
    # identity excludes the citation set, so it is the SAME proposition as the
    # one-span version, and adding a fourth citation does not fork it.
    assert multi_hop.proposition_id == proposition_version(
        _OWNER, evidence=cited[:1]
    ).proposition_id
    assert multi_hop.proposition_id == proposition_version(_OWNER).proposition_id
    grown = multi_hop.citing(evidence_occurrence("note-d", _SPAN).occurrence_id)
    assert grown.proposition_id == multi_hop.proposition_id
    assert len(grown.evidence) == 4


def test_citation_order_and_repetition_do_not_fork_a_proposition() -> None:
    a, b = "evidence:aaa", "evidence:bbb"
    one = proposition_version(_OWNER, evidence=[a, b])
    other = proposition_version(_OWNER, evidence=[b, a, a])
    assert one.evidence == other.evidence == (a, b)
    assert one.proposition_id == other.proposition_id


def test_a_derivation_event_ties_a_premise_set_to_a_proposition() -> None:
    prop = proposition_version(_OWNER)
    premises = ["evidence:b", "evidence:a"]
    first = derivation_event("episode-1", prop, premises)
    # the premise SET is what identifies the act: order and repetition cannot
    # mint a second event.
    assert first.event_id == derivation_event_id(
        episode_id="episode-1",
        proposition_id=prop.proposition_id,
        premises=["evidence:a", "evidence:b", "evidence:a"],
    )
    assert first.premise_set == {"evidence:a", "evidence:b"}
    # the SAME proposition derived in a second episode is a second EVENT and
    # still one proposition — which is what makes recurrence countable.
    second = derivation_event("episode-2", prop, premises)
    assert second.event_id != first.event_id
    assert second.proposition_id == first.proposition_id
    with pytest.raises(ValueError, match="non-empty episode_id"):
        DerivationEvent(episode_id="", proposition_id=prop.proposition_id)
    with pytest.raises(ValueError, match="needs a proposition_id"):
        DerivationEvent(episode_id="e", proposition_id="")


# ── acceptance 3: a paraphrase coalesces, but only under a resolver ─────────


def test_a_paraphrase_coalesces_under_a_scripted_resolver() -> None:
    plain = proposition_version(_OWNER)
    para = proposition_version(_OWNER_PARAPHRASE)
    assert plain.proposition_id != para.proposition_id  # distinct renderings

    resolver = ScriptedFactIdentity(
        groups={"fact:queue-owner": (plain.proposition_id, para.proposition_id)}
    )
    result = coalesce_propositions(
        [_rendering(plain), _rendering(para)], resolver=resolver
    )
    # one canonical id for both, and the merge is recorded with its resolver.
    assert result.canonical_id(plain.proposition_id) == result.canonical_id(
        para.proposition_id
    )
    assert result.merged_any is True
    assert result.resolver_id == "scripted-fact-identity"
    assert len(result.groups) == 1


def test_wording_alone_never_coalesces() -> None:
    # No resolver -> fail-safe. The two renderings above are as close as
    # paraphrases get, and nothing merges them.
    plain = proposition_version(_OWNER)
    para = proposition_version(_OWNER_PARAPHRASE)
    result = coalesce_propositions([_rendering(plain), _rendering(para)])
    assert result.merged_any is False
    assert result.canonical_id(plain.proposition_id) == plain.proposition_id
    assert result.canonical_id(para.proposition_id) == para.proposition_id
    assert result.resolver_id == "unresolved-fact-identity"
    assert "FAIL-SAFE" in FAIL_SAFE_MERGE_RULE


def test_a_lone_fact_key_is_not_a_merge() -> None:
    plain = proposition_version(_OWNER)
    other = proposition_version(_LAUNCH)
    resolver = ScriptedFactIdentity(
        groups={"fact:a": (plain.proposition_id,), "fact:b": (other.proposition_id,)}
    )
    result = coalesce_propositions(
        [_rendering(plain), _rendering(other)], resolver=resolver
    )
    assert result.merges == ()


def test_a_resolver_returning_unknown_propositions_is_refused() -> None:
    plain = proposition_version(_OWNER)
    resolver = ScriptedFactIdentity(groups={"fact:x": (plain.proposition_id,)})
    # the scripted resolver filters to what it was given ...
    assert coalesce_propositions([_rendering(plain)], resolver=resolver).merges == ()

    class Rogue:
        resolver_id = "rogue"

        def resolve(self, claims):  # type: ignore[no-untyped-def]
            return {"prop:never-seen": "fact:x"}

    with pytest.raises(ValueError, match="propositions it was not given"):
        coalesce_propositions([_rendering(plain)], resolver=Rogue())


# ── acceptance 4: a NEGATION does not coalesce ──────────────────────────────


def test_a_negation_does_not_coalesce_deterministically() -> None:
    affirmed = proposition_version(_OWNER)
    denied = proposition_version(_OWNER, polarity="deny")
    assert affirmed.proposition_id != denied.proposition_id
    result = coalesce_propositions([_rendering(affirmed), _rendering(denied)])
    assert result.merged_any is False
    assert result.canonical_id(denied.proposition_id) == denied.proposition_id


def test_even_an_over_eager_resolver_cannot_merge_across_a_negation() -> None:
    affirmed = proposition_version(_OWNER)
    denied = proposition_version(_OWNER, polarity="deny")
    resolver = ScriptedFactIdentity(
        groups={"fact:queue-owner": (affirmed.proposition_id, denied.proposition_id)}
    )
    result = coalesce_propositions(
        [_rendering(affirmed), _rendering(denied)], resolver=resolver
    )
    assert result.merges == ()
    assert len(result.refused) == 1
    reason = result.refused[0].reason
    assert "declared polarity differs" in reason
    assert "a negation is not a paraphrase" in reason
    assert result.canonical_id(denied.proposition_id) == denied.proposition_id
    assert result.canonical_id(affirmed.proposition_id) == affirmed.proposition_id


def test_a_declared_scope_or_qualifier_conflict_also_refuses_a_merge() -> None:
    north = proposition_version(_OWNER, scope={"region": "north"})
    south = proposition_version(_OWNER, scope={"region": "south"})
    dated = proposition_version(_OWNER, qualifiers={"as_of": "2026-01"})
    later = proposition_version(_OWNER, qualifiers={"as_of": "2026-06"})
    scope_result = coalesce_propositions(
        [_rendering(north), _rendering(south)],
        resolver=ScriptedFactIdentity(
            groups={"f": (north.proposition_id, south.proposition_id)}
        ),
    )
    qual_result = coalesce_propositions(
        [_rendering(dated), _rendering(later)],
        resolver=ScriptedFactIdentity(
            groups={"f": (dated.proposition_id, later.proposition_id)}
        ),
    )
    assert scope_result.merges == ()
    assert "scope differs" in scope_result.refused[0].reason
    assert qual_result.merges == ()
    assert "as_of qualifier" in qual_result.refused[0].reason


# ── acceptance 5: an ownership change inherits nothing ──────────────────────


def test_an_ownership_change_inherits_neither_warrant_nor_feedback() -> None:
    # The locator holds and the source version holds; only the asserted content
    # changed. Under the rejected key this claim kept its id and silently
    # inherited the replaced claim's history.
    version = note_version_hash("... the queue service is owned by team alpha ...")
    loc = anchor_locator(_TWO_FACT_SPAN)
    old = identify("note-a", loc, _OWNER, source_note_hash=version, fact_id="fact:1")

    # a warrant store and a trial history, keyed the way the rule requires.
    warrants = {feedback_subject_id(old.proposition): "warrant:alpha-owns"}
    trials = {feedback_subject_id(old.proposition): (7, 8)}  # n_pass, n_trial

    new = old.revised(_RIVAL_OWNER)

    assert new.evidence_id == old.evidence_id  # the locator DID hold
    assert new.proposition_id != old.proposition_id  # ... and identity moved
    assert new.proposition.supersedes == old.proposition_id  # lineage, not identity
    assert feedback_subject_id(new.proposition) not in warrants
    assert feedback_subject_id(new.proposition) not in trials
    # a resolved cross-span sameness judgement about the OLD wording is not
    # evidence about the new one.
    assert old.fact_id == "fact:1"
    assert new.fact_id == ""
    assert "PROPOSITION VERSION" in TRIAL_HISTORY_SUBJECT_RULE


def test_feedback_keys_on_the_proposition_not_the_evidence() -> None:
    # The flipped rule, stated as a test: an evidence-occurrence id is shared by
    # every proposition read from that span, so it is never a feedback subject.
    loc = anchor_locator(_TWO_FACT_SPAN)
    owner = identify("note-a", loc, _OWNER)
    launch = identify("note-a", loc, _LAUNCH)
    assert owner.evidence_id == launch.evidence_id
    assert feedback_subject_id(owner.proposition) != feedback_subject_id(
        launch.proposition
    )
    assert feedback_subject_id(owner.proposition) == owner.proposition_id


def test_a_restatement_keeps_scope_and_citations_but_not_identity() -> None:
    original = proposition_version(
        _OWNER, scope={"region": "north"}, evidence=["evidence:a"]
    )
    successor = original.restated(_RIVAL_OWNER)
    assert successor.scope == original.scope
    assert successor.evidence == original.evidence
    assert successor.supersedes == original.proposition_id
    assert successor.proposition_id != original.proposition_id
    assert original.same_proposition_as(successor) is False
    assert original.same_proposition_as(proposition_version(_OWNER, scope=original.scope))


def test_a_rewrap_is_not_a_restatement() -> None:
    # Identity folds whitespace and case, so re-wrapping the same assertion is
    # the same proposition — the one merge that needs no model.
    assert proposition_version_id("Team Alpha owns\n  the queue service.") == (
        proposition_version_id("team alpha owns the queue service.")
    )
    assert text_hash("Retries are\n  capped.") == text_hash("Retries are capped.")
    assert text_hash("Retries are capped.") != text_hash("Retries are uncapped.")


# ── retained clause: an insertion above a claim does not move later ids ─────


def test_inserting_a_span_above_leaves_later_occurrence_ids_unchanged() -> None:
    before = ["First sentence about the queue.", "Second sentence about retries."]
    after = ["A brand new leading sentence.", *before]
    ids_before = evidence_occurrence_ids_for_spans("note-a", before)
    ids_after = evidence_occurrence_ids_for_spans("note-a", after)
    assert ids_after[1:] == ids_before  # every pre-existing id survived
    assert len(set(ids_after)) == len(ids_after)  # still many claims per note
    # the legacy spelling is the same function.
    assert derivation_ids_for_spans("note-a", before) == ids_before
    assert derivation_id("note-a", anchor_locator(before[0])) == ids_before[0]


def test_inserting_a_span_above_leaves_later_proposition_ids_unchanged() -> None:
    # The proposition level is location-free, so it survives the insertion even
    # when the source VERSION moves (which it does — the note changed).
    tail = "The queue drains oldest first. A failed batch retries three times."
    body = f"An unrelated new opening sentence. {tail}"
    base = extract_claims(tail, _prov("src://a"), note_id="n1",
                          claim_id_scheme="proposition",
                          source_note_hash=note_version_hash(tail))
    grown = extract_claims(body, _prov("src://a"), note_id="n1",
                           claim_id_scheme="proposition",
                           source_note_hash=note_version_hash(body))
    assert [c.claim_id for c in grown][1:] == [c.claim_id for c in base]


def test_extract_claims_evidence_scheme_is_insertion_stable() -> None:
    tail = "The queue drains oldest first. A failed batch retries three times."
    body = f"An unrelated new opening sentence. {tail}"
    prov = _prov("src://a")
    base = extract_claims(tail, prov, note_id="n1", claim_id_scheme="evidence")
    grown = extract_claims(body, prov, note_id="n1", claim_id_scheme="evidence")
    assert [c.claim_id for c in grown][1:] == [c.claim_id for c in base]
    assert [c.text for c in grown][1:] == [c.text for c in base]
    # "derivation" is the legacy spelling of the same scheme.
    legacy = extract_claims(tail, prov, note_id="n1", claim_id_scheme="derivation")
    assert [c.claim_id for c in legacy] == [c.claim_id for c in base]


def test_pinning_the_source_version_moves_evidence_ids_but_not_propositions() -> None:
    # An occurrence is a located string AT a version: an edit to the note mints
    # new occurrence ids on purpose (that is what a staleness flag consumes),
    # while the propositions read out of the unchanged spans are untouched.
    tail = "The queue drains oldest first. A failed batch retries three times."
    body = f"An unrelated new opening sentence. {tail}"
    prov = _prov("src://a")
    pinned_before = extract_claims(tail, prov, note_id="n1",
                                   claim_id_scheme="evidence",
                                   source_note_hash=note_version_hash(tail))
    pinned_after = extract_claims(body, prov, note_id="n1",
                                  claim_id_scheme="evidence",
                                  source_note_hash=note_version_hash(body))
    assert [c.claim_id for c in pinned_after][1:] != [
        c.claim_id for c in pinned_before
    ]
    assert [
        proposition_version_id(c.text) for c in pinned_after
    ][1:] == [proposition_version_id(c.text) for c in pinned_before]


def test_extract_claims_index_scheme_is_the_defect_being_replaced() -> None:
    # Documents WHY the content-derived schemes exist: positional ids renumber.
    tail = "The queue drains oldest first. A failed batch retries three times."
    body = f"An unrelated new opening sentence. {tail}"
    prov = _prov("src://a")
    base = extract_claims(tail, prov, note_id="n1")
    grown = extract_claims(body, prov, note_id="n1")
    assert [c.claim_id for c in base] == ["n1:c0", "n1:c1"]
    assert [c.claim_id for c in grown][1:] != [c.claim_id for c in base]


def test_index_scheme_is_still_the_default() -> None:
    # Nothing on an existing path changes until the plan's gates have run.
    claims = extract_claims("A real sentence with content here.", _prov("src://a"),
                            note_id="n1")
    assert claims[0].claim_id == "n1:c0"


def test_content_schemes_keep_many_claims_per_note() -> None:
    body = "The queue drains oldest first. A failed batch retries three times."
    evidence = extract_claims(body, _prov("src://a"), note_id="n1",
                              claim_id_scheme="evidence")
    propositions = extract_claims(body, _prov("src://a"), note_id="n1",
                                  claim_id_scheme="proposition")
    assert len(evidence) == len(propositions) == 2
    assert len({c.claim_id for c in evidence}) == 2
    assert len({c.claim_id for c in propositions}) == 2
    assert all(c.claim_id.startswith("evidence:") for c in evidence)
    assert all(c.claim_id.startswith("prop:") for c in propositions)


def test_repeated_sentences_split_by_level() -> None:
    # Two identical sentences: two located strings, one proposition. Both
    # answers are right at their own level, and the schemes say which is which.
    body = "The queue drains oldest first. The queue drains oldest first."
    evidence = extract_claims(body, _prov("src://a"), note_id="n1",
                              claim_id_scheme="evidence")
    propositions = extract_claims(body, _prov("src://a"), note_id="n1",
                                  claim_id_scheme="proposition")
    assert len({c.claim_id for c in evidence}) == 2
    assert len({c.claim_id for c in propositions}) == 1


def test_unknown_claim_id_scheme_is_refused() -> None:
    with pytest.raises(ValueError, match="unknown claim_id_scheme"):
        extract_claims("A real sentence with content here.", _prov("src://a"),
                       claim_id_scheme="positional")  # type: ignore[arg-type]


# ── the locator value type ─────────────────────────────────────────────────


def test_anchor_locator_is_insertion_stable_and_char_range_is_not() -> None:
    assert anchor_locator(_SPAN).insertion_stable is True
    assert char_range_locator(10, 40).insertion_stable is False


def test_char_range_locator_ids_shift_under_an_edit_above() -> None:
    # Offsets are offered but flagged; this test pins the reason for the flag.
    assert evidence_occurrence_id("n1", char_range_locator(10, 40)) != (
        evidence_occurrence_id("n1", char_range_locator(14, 44))
    )


def test_identical_spans_are_separated_by_an_occurrence_ordinal() -> None:
    locs = locators_for_spans(["Same sentence twice.", "Same sentence twice."])
    assert [loc.occurrence for loc in locs] == [0, 1]
    assert locs[0].anchor == locs[1].anchor
    assert evidence_occurrence_id("n1", locs[0]) != evidence_occurrence_id("n1", locs[1])


def test_normalisation_folds_wrapping_and_case_only_edits() -> None:
    assert normalize_span_text("The  queue\n drains.") == normalize_span_text(
        "the queue drains."
    )
    assert anchor_locator("The  queue\n drains.") == anchor_locator("the queue drains.")
    assert anchor_locator("The queue drains.") != anchor_locator("The queue stalls.")


def test_note_version_hash_notices_edits_a_span_anchor_folds() -> None:
    # The version hash is deliberately stricter than a span anchor: a case-only
    # edit is a new version of the note even though it is the same span.
    assert note_version_hash("The queue drains.") != note_version_hash(
        "the queue drains."
    )
    assert note_version_hash("The queue drains.") == note_version_hash(
        "The queue drains."
    )


def test_malformed_locators_and_propositions_are_refused() -> None:
    with pytest.raises(ValueError, match="cannot anchor an empty span"):
        anchor_locator("   \n ")
    with pytest.raises(ValueError, match="non-empty anchor"):
        SpanLocator(kind="anchor")
    with pytest.raises(ValueError, match="0 <= start <= end"):
        SpanLocator(kind="char_range", start=9, end=4)
    with pytest.raises(ValueError, match="unknown locator kind"):
        SpanLocator(kind="fuzzy")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="occurrence must be >= 0"):
        SpanLocator(kind="char_range", start=0, end=1, occurrence=-1)
    with pytest.raises(ValueError, match="non-empty note_id"):
        evidence_occurrence_id("", anchor_locator(_SPAN))
    with pytest.raises(ValueError, match="non-empty note_id"):
        EvidenceOccurrence("", anchor_locator(_SPAN))
    with pytest.raises(ValueError, match="non-empty statement"):
        proposition_version("   ")
    with pytest.raises(ValueError, match="unknown polarity"):
        proposition_version(_OWNER, polarity="maybe")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="conflicting scope values"):
        proposition_version(_OWNER, scope=[("region", "north"), ("region", "south")])
    with pytest.raises(ValueError, match="may not contain NUL"):
        proposition_version(_OWNER, scope=[("region", "north\x00south")])
    with pytest.raises(TypeError, match="must be str"):
        proposition_version(_OWNER, scope=[("region", 7)])  # type: ignore[list-item]


# ── the content-id construction agrees with the replay token ───────────────


def test_content_id_construction_matches_replay_token() -> None:
    # Same NUL-terminated SHA-256, same truncation — only the prefix differs, so
    # claim identity and replay identity agree on what "the same content" means.
    loc = anchor_locator(_SPAN)
    minted = evidence_occurrence_id("note-a", loc)
    assert minted.startswith("evidence:")
    assert minted.removeprefix("evidence:") == _replay_token(
        "note-a", loc.canonical(), ""
    ).removeprefix("dks:")


def test_ids_are_process_stable_sha256_not_python_hash() -> None:
    loc = anchor_locator(_SPAN)
    h = hashlib.sha256()
    for part in ("note-a", loc.canonical(), ""):
        h.update(part.encode("utf-8"))
        h.update(b"\0")
    assert evidence_occurrence_id("note-a", loc) == "evidence:" + h.hexdigest()[:32]


# ── the cross-span fact layer: a PORT, specified and deliberately not built ─


def test_fact_identity_resolver_is_a_protocol_with_no_shipped_heuristic() -> None:
    resolver = UnresolvedFactIdentity()
    assert isinstance(resolver, FactIdentityResolver)
    assert isinstance(ScriptedFactIdentity(groups={}), FactIdentityResolver)
    claims = [
        _rendering(proposition_version("Alpha owns the queue.")),
        _rendering(proposition_version("The queue is owned by Alpha.")),
    ]
    # Two spans stating the same fact are NOT merged by the shipped default:
    # that needs a model, and nothing here guesses. Unresolved is the honest
    # answer, and it is a REFUSAL TO MERGE, never a claim of distinctness.
    assert resolver.resolve(claims) == {}
    assert coalesce_propositions(claims).merged_any is False


def test_no_lexical_fact_matching_is_shipped() -> None:
    src = _module_source()
    # a similarity/threshold rule behind the fact port is exactly what P0 must
    # not ship; guard the absence so it cannot creep in unnoticed.
    for banned in ("difflib", "SequenceMatcher", "numpy", "sklearn"):
        assert banned not in src, f"{banned} suggests a heuristic fact resolver"


def test_the_scripted_resolver_infers_nothing() -> None:
    # The reference implementation behind the seam is a declaration table, not a
    # model and not a heuristic: with no declared group it merges nothing, even
    # for two renderings of one fact.
    plain = proposition_version(_OWNER)
    para = proposition_version(_OWNER_PARAPHRASE)
    empty = ScriptedFactIdentity(groups={})
    assert empty.resolve([_rendering(plain), _rendering(para)]) == {}


def test_the_independence_deviation_is_recorded_not_silent() -> None:
    assert "EPISODES" in FACT_ID_DEVIATION
    assert "independent contexts" in FACT_ID_DEVIATION
    assert "UNRESOLVED" in FACT_ID_DEVIATION


# ── purity (the Dependency Rule) ────────────────────────────────────────────


def test_module_is_pure_no_runtime_import_no_model_call() -> None:
    src = _module_source()
    assert "tessellum.runtime" not in src
    for banned in ("LLMBackend", "LLMRequest", "sqlite3", "open(", "datetime"):
        assert banned not in src, f"{banned} breaks the purity of dks/claim_identity"


def test_identities_are_frozen_and_hashable() -> None:
    ident = identify("n1", anchor_locator(_SPAN), _OWNER)
    assert isinstance(ident, DerivedClaimIdentity)
    assert {ident, ident.revised(_RIVAL_OWNER)}  # hashable → usable as dict keys
    assert {ident.proposition, ident.proposition.restated(_RIVAL_OWNER)}
    with pytest.raises(FrozenInstanceError):
        ident.note_id = "tampered"  # type: ignore[misc]
    with pytest.raises(AttributeError):
        # the ids are computed, so they cannot be set to disagree with the fields
        ident.proposition_id = "tampered"  # type: ignore[misc]
