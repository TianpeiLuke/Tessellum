"""P0 smoke — typed change proposals + snapshot-pinned merge/canonicalize/hash.

Covers the four P0 action items and the gate-to-P1 acceptance:
  - A0.2: frozen effect union + ChangeProposal (discriminated, forbid-extra).
  - A0.3: three-tier merge (CRDT commute / grow-only union+dedup /
          reject-on-overlap) keyed by effect footprint.
  - A0.4: canonical_json_bytes (sorted / compact / UTF-8) + float ban.
  - A0.5: plan_revision_hash as a SEPARATE sha256 identity domain.
  - GATE-TO-P1: shuffling a proposal set yields a byte-identical
          plan_revision_hash; two proposals against one parent merge
          canonically OR raise/return a declared conflict.
"""

from __future__ import annotations

import hashlib
import itertools

import pytest
from pydantic import ValidationError

from tessellum.composer import (
    AddNavigation,
    AddNote,
    AddReference,
    ChangeProposal,
    DropNote,
    Effect,
    FloatInCanonicalPayloadError,
    MergeConflict,
    MergeNotes,
    MergeResult,
    ProposalConflictError,
    Reroute,
    UpdateNote,
    canonical_json_bytes,
    content_hash,
    effect_footprint,
    effect_key,
    merge_or_raise,
    merge_proposals,
    plan_revision_hash,
)

PARENT = "parent_revision_0"


def _prop(effect, *, proposer="p", parent=PARENT, evidence=None) -> ChangeProposal:
    return ChangeProposal(
        proposer=proposer,
        target_revision_hash=parent,
        effect=effect,
        evidence=evidence or {},
    )


# ── A0.2 — model / typing cases ────────────────────────────────────────────


def test_effect_models_frozen() -> None:
    effects = [
        AddNote(note_id="n", target_path="a/n.md", content_hash="c"),
        UpdateNote(note_id="n", target_path="a/n.md", content_hash="c"),
        MergeNotes(sources=("x", "y"), dest="z", content_hash="c"),
        DropNote(note_id="n"),
        Reroute(edge_src="s", edge_dst_old="o", edge_dst_new="w"),
        AddReference(src="a", dst="b", ref_type="cites"),
        AddNavigation(note_id="n", entry_point="entry_x"),
    ]
    for e in effects:
        # frozen → attribute reassignment rejected.
        with pytest.raises(ValidationError):
            e.kind = "mutated"  # type: ignore[misc]
    # extra="forbid" → unknown field rejected at construction.
    with pytest.raises(ValidationError):
        AddNote(note_id="n", target_path="a/n.md", content_hash="c", bogus=1)


def test_change_proposal_typed_union() -> None:
    cp = ChangeProposal.model_validate(
        {
            "proposer": "p",
            "target_revision_hash": "h",
            "effect": {
                "kind": "add_note",
                "note_id": "n",
                "target_path": "a/n.md",
                "content_hash": "c",
            },
        }
    )
    assert isinstance(cp.effect, AddNote)
    assert cp.evidence == {}
    # A bad discriminator is rejected by the discriminated union.
    with pytest.raises(ValidationError):
        ChangeProposal.model_validate(
            {
                "proposer": "p",
                "target_revision_hash": "h",
                "effect": {"kind": "not_a_kind", "note_id": "n"},
            }
        )
    # ChangeProposal is itself frozen.
    with pytest.raises(ValidationError):
        cp.proposer = "q"  # type: ignore[misc]


def test_footprint_and_effect_key() -> None:
    add = AddNote(note_id="n", target_path="a/n.md", content_hash="c")
    fp = effect_footprint(add)
    assert fp.writes == {"node:n", "path:a/n.md"}
    assert fp.reads == frozenset()

    # grow-only add_reference writes a single edge token.
    ref = AddReference(src="a", dst="b", ref_type="cites")
    ref_writes = effect_footprint(ref).writes
    assert len(ref_writes) == 1
    assert next(iter(ref_writes)).startswith("edge:")

    # update_note reads AND writes its node.
    upd = UpdateNote(note_id="X", target_path="a/x.md", content_hash="c")
    ufp = effect_footprint(upd)
    assert ufp.writes == {"node:X"} == ufp.reads

    # merge_notes touches dest + all sources.
    mrg = MergeNotes(sources=("X", "Y"), dest="Z", content_hash="c")
    assert effect_footprint(mrg).writes == {"node:Z", "node:X", "node:Y"}

    # effect_key EXCLUDES evidence (same effect, different evidence → equal).
    p1 = _prop(add, evidence={"why": "one"})
    p2 = _prop(add, evidence={"why": "two"})
    assert effect_key(p1.effect) == effect_key(p2.effect) == ("add_note", "n")
    # ...but the whole-proposal content hash DIFFERS on evidence.
    assert content_hash(p1) != content_hash(p2)


# ── A0.4 — canonicalizer cases ─────────────────────────────────────────────


def test_canonical_float_ban() -> None:
    with pytest.raises(FloatInCanonicalPayloadError):
        canonical_json_bytes({"a": 1.0})
    with pytest.raises(FloatInCanonicalPayloadError):
        canonical_json_bytes({"a": [1, {"b": 2.5}]})
    # A float smuggled through a proposal dump also raises.
    with pytest.raises(FloatInCanonicalPayloadError):
        canonical_json_bytes(
            _prop(
                AddNote(note_id="n", target_path="a/n.md", content_hash="c"),
                evidence={"score": 0.5},
            ).model_dump(mode="json")
        )
    # int / bool / None / str / nested containers all pass.
    ok = canonical_json_bytes(
        {"i": 1, "b": True, "f": False, "n": None, "s": "x", "l": [1, {"k": "v"}]}
    )
    assert isinstance(ok, bytes)
    # bool is NOT rejected as a float (bool ⊂ int subtlety).
    assert canonical_json_bytes({"t": True, "f": False}) == b'{"f":false,"t":true}'


def test_canonical_sorted_compact_utf8() -> None:
    # Sorted keys, no insignificant whitespace.
    assert canonical_json_bytes({"b": 1, "a": 2}) == b'{"a":2,"b":1}'
    # ensure_ascii=False → raw UTF-8, not \uXXXX escapes.
    out = canonical_json_bytes({"name": "café"})
    assert "café".encode("utf-8") in out
    assert b"\\u" not in out
    # Non-str dict key raises TypeError.
    with pytest.raises(TypeError):
        canonical_json_bytes({1: "a"})


def test_plan_revision_hash_is_hex_sha256_and_separate() -> None:
    effA = AddNote(note_id="n", target_path="a/n.md", content_hash="c")
    prh = plan_revision_hash("parent", [effA])
    assert len(prh) == 64 and all(ch in "0123456789abcdef" for ch in prh)

    # Distinct identity domain: scheduler-style program hash over the same
    # logical inputs is a DIFFERENT value (proves the domains are separate).
    skill_bytes = b"parent"
    ver = "n"
    scheduler_style = hashlib.sha256(
        skill_bytes + b"\0" + ver.encode("utf-8")
    ).hexdigest()
    assert prh != scheduler_style


# ── A0.3 — merge tier cases ────────────────────────────────────────────────


def test_disjoint_footprints_commute() -> None:
    a = _prop(AddNote(note_id="n1", target_path="a/n1.md", content_hash="c1"))
    b = _prop(AddNote(note_id="n2", target_path="a/n2.md", content_hash="c2"))
    r = merge_proposals(PARENT, [a, b])
    assert r.conflicts == ()
    assert r.plan_revision_hash is not None
    assert len(r.accepted_effects) == 2


def test_grow_only_union_and_dedup() -> None:
    ref = AddReference(src="a", dst="b", ref_type="cites")
    # Two IDENTICAL grow-only effects (diff proposers) → dedup to 1.
    r = merge_proposals(PARENT, [_prop(ref, proposer="p1"), _prop(ref, proposer="p2")])
    assert r.conflicts == ()
    assert len(r.accepted_effects) == 1

    # Two DIFFERENT grow-only effects → both accepted (disjoint tokens).
    ref2 = AddReference(src="a", dst="c", ref_type="cites")
    r2 = merge_proposals(PARENT, [_prop(ref), _prop(ref2)])
    assert r2.conflicts == ()
    assert len(r2.accepted_effects) == 2


def test_same_note_body_conflict() -> None:
    a = _prop(AddNote(note_id="n", target_path="a/n.md", content_hash="AAA"))
    b = _prop(AddNote(note_id="n", target_path="a/n.md", content_hash="BBB"))
    r = merge_proposals(PARENT, [a, b])
    assert len(r.conflicts) == 1
    assert r.conflicts[0].kind == "same_key_divergent"
    assert r.accepted_effects == ()
    assert r.plan_revision_hash is None


def test_structural_write_overlap_conflict() -> None:
    upd = _prop(UpdateNote(note_id="X", target_path="a/x.md", content_hash="c"))
    mrg = _prop(MergeNotes(sources=("X", "Y"), dest="Z", content_hash="c"))
    r = merge_proposals(PARENT, [upd, mrg])
    kinds = {c.kind for c in r.conflicts}
    assert "write_overlap" in kinds
    assert any(c.region == "node:X" for c in r.conflicts)
    assert r.plan_revision_hash is None


def test_stale_parent_fence() -> None:
    fresh = _prop(AddNote(note_id="n1", target_path="a/n1.md", content_hash="c1"))
    stale = _prop(
        AddNote(note_id="n2", target_path="a/n2.md", content_hash="c2"),
        parent="some_other_revision",
    )
    r = merge_proposals(PARENT, [fresh, stale])
    assert len(r.accepted_effects) == 1  # stale excluded
    assert r.stale_dropped == (content_hash(stale),)
    # The accepted set + hash equal a merge of the fresh proposal ALONE.
    r_alone = merge_proposals(PARENT, [fresh])
    assert r.plan_revision_hash == r_alone.plan_revision_hash


def test_merge_or_raise() -> None:
    a = _prop(AddNote(note_id="n", target_path="a/n.md", content_hash="AAA"))
    b = _prop(AddNote(note_id="n", target_path="a/n.md", content_hash="BBB"))
    with pytest.raises(ProposalConflictError) as ei:
        merge_or_raise(PARENT, [a, b])
    assert len(ei.value.conflicts) == 1
    # A disjoint pair returns a clean MergeResult.
    c = _prop(AddNote(note_id="n2", target_path="a/n2.md", content_hash="c2"))
    r = merge_or_raise(PARENT, [a, c])
    assert isinstance(r, MergeResult)
    assert r.conflicts == ()
    assert r.plan_revision_hash is not None


# ── GATE-TO-P1 property tests (deterministic; exhaustive permutations) ─────


def _fixed_set() -> list[ChangeProposal]:
    return [
        _prop(AddNote(note_id="n1", target_path="a/n1.md", content_hash="c1")),
        _prop(AddNote(note_id="n2", target_path="a/n2.md", content_hash="c2")),
        _prop(AddReference(src="n1", dst="n2", ref_type="cites")),
        _prop(AddNavigation(note_id="n1", entry_point="entry_x")),
    ]


def test_shuffle_order_independent_hash() -> None:
    s = _fixed_set()
    first = merge_proposals(PARENT, list(s))
    assert first.plan_revision_hash is not None
    for order in itertools.permutations(s):
        r = merge_proposals(PARENT, list(order))
        assert r.plan_revision_hash == first.plan_revision_hash
        assert r.accepted_effects == first.accepted_effects


def test_two_proposals_same_parent_merge_or_conflict() -> None:
    # (a) DISJOINT pair → canonical result, order-independent.
    d1 = _prop(AddNote(note_id="n1", target_path="a/n1.md", content_hash="c1"))
    d2 = _prop(AddNote(note_id="n2", target_path="a/n2.md", content_hash="c2"))
    ra = merge_proposals(PARENT, [d1, d2])
    rb = merge_proposals(PARENT, [d2, d1])
    assert ra.conflicts == () and rb.conflicts == ()
    assert ra.plan_revision_hash is not None
    assert ra.plan_revision_hash == rb.plan_revision_hash

    # (b) OVERLAPPING pair → declared conflict, order-independent record.
    o1 = _prop(AddNote(note_id="n", target_path="a/n.md", content_hash="AAA"))
    o2 = _prop(AddNote(note_id="n", target_path="a/n.md", content_hash="BBB"))
    ca = merge_proposals(PARENT, [o1, o2])
    cb = merge_proposals(PARENT, [o2, o1])
    assert ca.plan_revision_hash is None and cb.plan_revision_hash is None
    assert ca.conflicts == cb.conflicts  # frozen dataclasses compare by value
    assert all(isinstance(c, MergeConflict) for c in ca.conflicts)

    # update-vs-merge structural overlap is likewise order-independent.
    u = _prop(UpdateNote(note_id="X", target_path="a/x.md", content_hash="c"))
    m = _prop(MergeNotes(sources=("X", "Y"), dest="Z", content_hash="c"))
    assert merge_proposals(PARENT, [u, m]).conflicts == merge_proposals(
        PARENT, [m, u]
    ).conflicts


def test_no_randomness_or_clock() -> None:
    s = _fixed_set()
    r1 = merge_proposals(PARENT, list(s))
    r2 = merge_proposals(PARENT, list(s))
    assert r1.plan_revision_hash == r2.plan_revision_hash
    assert r1.accepted_effects == r2.accepted_effects
    effs = [p.effect for p in s]
    assert plan_revision_hash(PARENT, effs) == plan_revision_hash(PARENT, effs)


def _all_kinds_disjoint_set() -> list[ChangeProposal]:
    """One proposal of EACH of the 7 effect kinds, footprint-disjoint so the
    whole set merges cleanly (no conflicts) — lets us prove the plan_revision
    hash is order-independent across every effect kind, not just the three in
    ``_fixed_set``."""
    return [
        _prop(AddNote(note_id="a1", target_path="x/a1.md", content_hash="h1")),
        _prop(UpdateNote(note_id="u1", target_path="x/u1.md", content_hash="h2")),
        _prop(MergeNotes(sources=("m1", "m2"), dest="m3", content_hash="h3")),
        _prop(DropNote(note_id="d1")),
        _prop(Reroute(edge_src="r1", edge_dst_old="ro", edge_dst_new="rn")),
        _prop(AddReference(src="ref_s", dst="ref_d", ref_type="cites")),
        _prop(AddNavigation(note_id="nav1", entry_point="entry_y")),
    ]


def test_shuffle_order_independent_hash_all_effect_kinds() -> None:
    """GATE-TO-P1 coverage nit closed: order-independence holds for a clean
    merge spanning ALL seven effect kinds. 7! = 5040 permutations is heavy;
    sample a deterministic rotation set (no clock/random) instead."""
    s = _all_kinds_disjoint_set()
    first = merge_proposals(PARENT, list(s))
    assert first.conflicts == ()
    assert first.plan_revision_hash is not None
    assert len(first.accepted_effects) == 7
    n = len(s)
    # Deterministic orders: every cyclic rotation + the full reversal.
    orders = [s[i:] + s[:i] for i in range(n)] + [list(reversed(s))]
    for order in orders:
        r = merge_proposals(PARENT, list(order))
        assert r.plan_revision_hash == first.plan_revision_hash
        assert r.accepted_effects == first.accepted_effects


def test_plan_revision_hash_order_independent_on_unsorted_input() -> None:
    """Directly exercise ``plan_revision_hash`` with an unsorted iterable (it
    sorts internally by ``effect_content_hash``), independent of the
    merge_proposals pre-sort — closes the reviewer's coverage gap on line
    501."""
    effs = [p.effect for p in _all_kinds_disjoint_set()]
    base = plan_revision_hash(PARENT, effs)
    assert plan_revision_hash(PARENT, list(reversed(effs))) == base
    for i in range(len(effs)):
        assert plan_revision_hash(PARENT, effs[i:] + effs[:i]) == base
    # A different parent must change the hash (parent is bound into it).
    assert plan_revision_hash("other_parent", effs) != base
