"""P0 — derived-claim identity (``dks/claim_identity.py``).

The acceptance line, one test group each:
 - two differently-worded derivations of one fact from ONE span collapse to a
   single ``derivation_id``;
 - a revision preserves ``derivation_id`` while ``text_hash`` changes;
 - inserting a sentence above a claim does not change any later claim's id
   (checked at the identity layer AND through ``extract_claims``).

Plus the properties that make those three true rather than accidental: the id
carries no claim text and no domain predicate, the content-id construction
agrees with the replay token, the cross-span ``fact_id`` layer is a PORT with no
heuristic behind it, and the module stays pure (no ``runtime`` import).
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
    ClaimRendering,
    DerivedClaimIdentity,
    FactIdentityResolver,
    SpanLocator,
    UnresolvedFactIdentity,
    anchor_locator,
    char_range_locator,
    derivation_id,
    derivation_ids_for_spans,
    identify,
    locators_for_spans,
    normalize_span_text,
    text_hash,
)

_SPAN = "The scheduler retries a failed batch at most three times."


def _prov(*refs: str) -> tuple[ClaimProvenance, ...]:
    return tuple(ClaimProvenance(span_id=f"s{i}", source_ref=r)
                 for i, r in enumerate(refs))


def _module_source() -> str:
    """The module's own source, read via its ``__file__`` so the purity guards
    below do not depend on the test runner's working directory."""
    return Path(claim_identity.__file__).read_text(encoding="utf-8")


# ── acceptance 1: one span, two wordings, one derivation_id ─────────────────


def test_two_wordings_of_one_span_collapse_to_one_derivation_id() -> None:
    loc = anchor_locator(_SPAN)
    first = identify("note-a", loc, "A failed batch is retried up to three times.")
    second = identify("note-a", loc, "At most three retries follow a batch failure.")
    assert first.derivation_id == second.derivation_id
    # the WORDING is what differs, and only the rendering hash records it.
    assert first.text_hash != second.text_hash


def test_derivation_id_is_blind_to_the_claim_text_entirely() -> None:
    # identity is a function of (note_id, locator) alone — no text argument.
    loc = anchor_locator(_SPAN)
    assert derivation_id("note-a", loc) == identify("note-a", loc, "x").derivation_id
    assert derivation_id("note-a", loc) == identify("note-a", loc, "y" * 500).derivation_id


def test_no_domain_predicate_enters_either_key() -> None:
    # A predicate is a model act; the canonical locator form has no slot for one.
    loc = anchor_locator(_SPAN, section="## Behaviour")
    canonical = loc.canonical()
    assert canonical.startswith("anchor|## Behaviour|")
    assert "predicate" not in canonical
    # SpanLocator carries no predicate field at all.
    assert not any("predicate" in f for f in SpanLocator.__dataclass_fields__)


def test_same_span_in_two_notes_is_two_claims() -> None:
    loc = anchor_locator(_SPAN)
    assert derivation_id("note-a", loc) != derivation_id("note-b", loc)


def test_same_sentence_under_two_sections_is_two_spans() -> None:
    a = anchor_locator(_SPAN, section="## One")
    b = anchor_locator(_SPAN, section="## Two")
    assert derivation_id("note-a", a) != derivation_id("note-a", b)


# ── acceptance 2: a revision preserves the id, moves the text hash ──────────


def test_revision_preserves_derivation_id_and_moves_text_hash() -> None:
    original = identify("note-a", anchor_locator(_SPAN), "Retries are capped at three.")
    revised = original.revised("Retries are capped at three attempts per batch.")
    assert revised.derivation_id == original.derivation_id
    assert revised.locator == original.locator
    assert revised.text_hash != original.text_hash


def test_revision_carries_a_resolved_fact_id_forward() -> None:
    original = identify(
        "note-a", anchor_locator(_SPAN), "Retries are capped.", fact_id="fact:1",
    )
    assert original.revised("Retries are capped at three.").fact_id == "fact:1"


def test_text_hash_ignores_rewrapping_but_not_rewording() -> None:
    assert text_hash("Retries are\n  capped.") == text_hash("Retries are capped.")
    assert text_hash("Retries are capped.") != text_hash("Retries are uncapped.")


# ── acceptance 3: an insertion above a claim does not move later ids ────────


def test_inserting_a_span_above_leaves_later_ids_unchanged() -> None:
    before = ["First sentence about the queue.", "Second sentence about retries."]
    after = ["A brand new leading sentence.", *before]
    ids_before = derivation_ids_for_spans("note-a", before)
    ids_after = derivation_ids_for_spans("note-a", after)
    assert ids_after[1:] == ids_before  # every pre-existing id survived
    assert len(set(ids_after)) == len(ids_after)  # still many claims per note


def test_extract_claims_derivation_scheme_is_insertion_stable() -> None:
    tail = "The queue drains oldest first. A failed batch retries three times."
    body = f"An unrelated new opening sentence. {tail}"
    prov = _prov("src://a")
    base = extract_claims(tail, prov, note_id="n1", claim_id_scheme="derivation")
    grown = extract_claims(body, prov, note_id="n1", claim_id_scheme="derivation")
    assert [c.claim_id for c in grown][1:] == [c.claim_id for c in base]
    assert [c.text for c in grown][1:] == [c.text for c in base]


def test_extract_claims_index_scheme_is_the_defect_being_replaced() -> None:
    # Documents WHY the derivation scheme exists: the positional ids renumber.
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


def test_derivation_scheme_keeps_many_claims_per_note() -> None:
    body = "The queue drains oldest first. A failed batch retries three times."
    claims = extract_claims(body, _prov("src://a"), note_id="n1",
                            claim_id_scheme="derivation")
    assert len(claims) == 2
    assert len({c.claim_id for c in claims}) == 2
    assert all(c.claim_id.startswith("claim:") for c in claims)


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
    assert derivation_id("n1", char_range_locator(10, 40)) != derivation_id(
        "n1", char_range_locator(14, 44)
    )


def test_identical_spans_are_separated_by_an_occurrence_ordinal() -> None:
    locs = locators_for_spans(["Same sentence twice.", "Same sentence twice."])
    assert [loc.occurrence for loc in locs] == [0, 1]
    assert locs[0].anchor == locs[1].anchor
    assert derivation_id("n1", locs[0]) != derivation_id("n1", locs[1])


def test_normalisation_folds_wrapping_and_case_only_edits() -> None:
    assert normalize_span_text("The  queue\n drains.") == normalize_span_text(
        "the queue drains."
    )
    assert anchor_locator("The  queue\n drains.") == anchor_locator("the queue drains.")
    assert anchor_locator("The queue drains.") != anchor_locator("The queue stalls.")


def test_malformed_locators_are_refused() -> None:
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
        derivation_id("", anchor_locator(_SPAN))


# ── the content-id construction agrees with the replay token ───────────────


def test_content_id_construction_matches_replay_token() -> None:
    # Same NUL-terminated SHA-256, same truncation — only the prefix differs, so
    # claim identity and replay identity agree on what "the same content" means.
    loc = anchor_locator(_SPAN)
    minted = derivation_id("note-a", loc)
    assert minted.startswith("claim:")
    assert minted.removeprefix("claim:") == _replay_token(
        "note-a", loc.canonical()
    ).removeprefix("dks:")


def test_ids_are_process_stable_sha256_not_python_hash() -> None:
    loc = anchor_locator(_SPAN)
    h = hashlib.sha256()
    for part in ("note-a", loc.canonical()):
        h.update(part.encode("utf-8"))
        h.update(b"\0")
    assert derivation_id("note-a", loc) == "claim:" + h.hexdigest()[:32]


# ── level 2: fact_id is a PORT, specified and deliberately not built ────────


def test_fact_identity_resolver_is_a_protocol_with_no_shipped_heuristic() -> None:
    resolver = UnresolvedFactIdentity()
    assert isinstance(resolver, FactIdentityResolver)
    claims = [
        ClaimRendering(identify("n1", anchor_locator("Alpha owns the queue."), "x"),
                       "Alpha owns the queue."),
        ClaimRendering(identify("n2", anchor_locator("The queue is owned by Alpha."), "y"),
                       "The queue is owned by Alpha."),
    ]
    # Two spans stating the same fact are NOT merged: that needs a model, and
    # nothing here guesses. Unresolved is the honest answer.
    assert resolver.resolve(claims) == {}
    assert all(c.identity.fact_id == "" for c in claims)


def test_no_lexical_fact_matching_is_shipped() -> None:
    src = _module_source()
    # a similarity/threshold rule behind the fact port is exactly what P0 must
    # not ship; guard the absence so it cannot creep in unnoticed.
    for banned in ("difflib", "SequenceMatcher", "numpy", "sklearn"):
        assert banned not in src, f"{banned} suggests a heuristic fact resolver"


def test_the_independence_deviation_is_recorded_not_silent() -> None:
    assert "EPISODES" in FACT_ID_DEVIATION
    assert "independent contexts" in FACT_ID_DEVIATION


# ── purity (the Dependency Rule) ────────────────────────────────────────────


def test_module_is_pure_no_runtime_import_no_model_call() -> None:
    src = _module_source()
    assert "tessellum.runtime" not in src
    for banned in ("LLMBackend", "LLMRequest", "sqlite3", "open(", "datetime"):
        assert banned not in src, f"{banned} breaks the purity of dks/claim_identity"


def test_identity_is_frozen_and_hashable() -> None:
    ident = identify("n1", anchor_locator(_SPAN), "text")
    assert isinstance(ident, DerivedClaimIdentity)
    assert {ident, ident.revised("text")}  # hashable → usable as a dict key
    with pytest.raises(FrozenInstanceError):
        ident.derivation_id = "tampered"  # type: ignore[misc]
