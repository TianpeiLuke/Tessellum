"""P4 — exact write closure + validation heuristic + partition (A4.2-A4.5).

Proves the load-bearing distinction (plan guardrail 3): typed materialization
invariants define the EXACT write set (mandatory nav/backlink/index writes are
always included, even for entry-point/hub targets); the bounded reverse walk is
a VALIDATION heuristic only (entry-point drop + hub cut + fail-closed spill,
never truncation); the boundary witness fails closed on escaping/unknown edges;
partition splits disjoint closures and unions coupled ones.
"""

from __future__ import annotations

from tessellum.composer.knowledge_plan import ClaimProvenance, NoteIntent, NoteIntentGraph
from tessellum.composer.write_closure import (
    ClosurePolicy,
    boundary_witness,
    classify_edge,
    partition_capsules,
    validation_set,
    write_closure,
)


def _intent(note_id, *, navigation=(), required_inlinks=(), depends_on=()):
    return NoteIntent(
        note_id=note_id, thesis="t", building_block="concept",
        target_path=f"areas/{note_id}.md",
        provenance=(ClaimProvenance(span_id="s", source_ref="r"),),
        navigation=tuple(navigation),
        required_inlinks=tuple(required_inlinks),
        depends_on=tuple(depends_on),
    )


# ── A4.2 exact write closure ────────────────────────────────────────────────


def test_write_closure_includes_note_and_index() -> None:
    wc = write_closure((_intent("n1"),))
    kinds = {(w.note_id, w.kind) for w in wc.writes}
    assert ("n1", "note") in kinds
    assert ("n1", "index") in kinds


def test_navigation_row_always_written_even_for_hub_entry_point() -> None:
    # The entry point is a high-degree hub, but a note registering under it is
    # a MANDATORY navigation write — never pruned by a hub cut.
    wc = write_closure((_intent("n1", navigation=("entry_hub",)),))
    assert ("entry_hub", "navigation") in {(w.note_id, w.kind) for w in wc.writes}
    assert "entry_hub" in wc.touched_note_ids


def test_navigation_via_injected_entry_point_map() -> None:
    wc = write_closure((_intent("n1"),), entry_point_of={"n1": "entry_x"})
    assert ("entry_x", "navigation") in {(w.note_id, w.kind) for w in wc.writes}


def test_required_reverse_inlink_is_a_write_on_the_source() -> None:
    # a note that must gain a backlink to n1 is a mandatory write on THAT note.
    wc = write_closure((_intent("n1", required_inlinks=("existing_note",)),))
    assert ("existing_note", "reverse_inlink") in {(w.note_id, w.kind) for w in wc.writes}
    assert "existing_note" in wc.touched_note_ids


def test_write_closure_deterministic_and_accepts_graph() -> None:
    g = NoteIntentGraph(objective_id="o", intents=(_intent("b"), _intent("a")))
    wc1 = write_closure(g)
    wc2 = write_closure(g)
    assert wc1.writes == wc2.writes  # deterministic
    # sorted by (note_id, kind, origin)
    keys = [(w.note_id, w.kind) for w in wc1.writes]
    assert keys == sorted(keys)


# ── A4.2 edge classification + boundary witness ─────────────────────────────


def test_classify_edge_navigation_fz_backlink_reference_unknown() -> None:
    cat = {"ep": "entry_point", "a": "resource", "b": "resource"}
    fzp = {"b": "a"}  # b's FZ parent is a
    assert classify_edge("ep", "x", note_category_of=cat, fz_parent_of=fzp, reciprocal=False) == "navigation"
    assert classify_edge("b", "a", note_category_of=cat, fz_parent_of=fzp, reciprocal=False) == "fz_parent"
    assert classify_edge("a", "b", note_category_of={"a": "resource"}, fz_parent_of={}, reciprocal=True) == "backlink"
    assert classify_edge("a", "b", note_category_of={"a": "resource"}, fz_parent_of={}, reciprocal=False) == "reference"
    assert classify_edge("ghost", "b", note_category_of={}, fz_parent_of={}, reciprocal=False) == "unknown"


def test_boundary_witness_ok_when_closed() -> None:
    wc = write_closure((_intent("a", required_inlinks=("b",)),))  # touches a, b
    # a -> b is a backlink edge (reciprocal), both touched → closed.
    w = boundary_witness(
        wc, edges=[("a", "b")],
        note_category_of={"a": "resource", "b": "resource"},
        fz_parent_of={}, reciprocal_pairs={("a", "b")},
    )
    assert w.ok and not w.escaping and not w.unknown


def test_boundary_witness_detects_escaping_propagating_edge() -> None:
    wc = write_closure((_intent("a"),))  # touches only a (+index)
    # a -> b is an fz_parent edge (propagates), b NOT touched → escapes.
    w = boundary_witness(
        wc, edges=[("a", "b")],
        note_category_of={"a": "resource", "b": "resource"},
        fz_parent_of={"a": "b"}, reciprocal_pairs=set(),
    )
    assert not w.ok
    assert ("a", "b", "fz_parent") in w.escaping


def test_boundary_witness_fails_closed_on_unknown_edge() -> None:
    wc = write_closure((_intent("a"),))
    w = boundary_witness(
        wc, edges=[("a", "b")],
        note_category_of={},  # a's category unknown → edge class unknown
        fz_parent_of={}, reciprocal_pairs=set(),
    )
    assert not w.ok
    assert ("a", "b") in w.unknown


def test_boundary_witness_ignores_plain_reference_escape() -> None:
    # a plain content reference does NOT propagate a write, so an escaping
    # reference edge does not break closure.
    wc = write_closure((_intent("a"),))
    w = boundary_witness(
        wc, edges=[("a", "b")],
        note_category_of={"a": "resource", "b": "resource"},
        fz_parent_of={}, reciprocal_pairs=set(),  # plain reference
    )
    assert w.ok


# ── A4.3/A4.4 validation heuristic + spill ──────────────────────────────────


def test_validation_reverse_reachability_depth_bounded() -> None:
    # chain: d -> c -> b -> a  (reverse_adj[a]=[b], [b]=[c], [c]=[d])
    reverse_adj = {"a": ["b"], "b": ["c"], "c": ["d"]}
    res = validation_set(
        frozenset({"a"}), reverse_adj=reverse_adj, corpus_size=100,
        note_category_of={}, in_degree_of={},
        policy=ClosurePolicy(validation_depth=2, spill_fraction=1.0),
    )
    # depth-2 reverse from a: b (d1), c (d2). d is depth-3 → excluded.
    assert res.to_revalidate == frozenset({"b", "c"})


def test_validation_drops_entry_point_predecessors() -> None:
    reverse_adj = {"a": ["ep", "b"]}
    res = validation_set(
        frozenset({"a"}), reverse_adj=reverse_adj, corpus_size=100,
        note_category_of={"ep": "entry_point"}, in_degree_of={},
        policy=ClosurePolicy(validation_depth=2, spill_fraction=1.0),
    )
    assert res.to_revalidate == frozenset({"b"})  # ep dropped


def test_validation_hub_cut_includes_but_does_not_expand() -> None:
    # hub -> a ; x -> hub. hub is over threshold: include hub as a leaf but do
    # NOT expand to x.
    reverse_adj = {"a": ["hub"], "hub": ["x"]}
    res = validation_set(
        frozenset({"a"}), reverse_adj=reverse_adj, corpus_size=100,
        note_category_of={}, in_degree_of={"hub": 999},
        policy=ClosurePolicy(validation_depth=3, hub_threshold=50, spill_fraction=1.0),
    )
    assert "hub" in res.to_revalidate
    assert "x" not in res.to_revalidate  # not expanded through the hub


def test_validation_spill_trips_and_never_truncates() -> None:
    # 5 predecessors of a; bound = 10% of corpus=20 → 2. Size 5 > 2 → spill.
    reverse_adj = {"a": ["p1", "p2", "p3", "p4", "p5"]}
    res = validation_set(
        frozenset({"a"}), reverse_adj=reverse_adj, corpus_size=20,
        note_category_of={}, in_degree_of={},
        policy=ClosurePolicy(validation_depth=1, spill_fraction=0.10),
    )
    assert res.spilled is True
    assert res.size == 5  # full set returned, NOT truncated to the bound
    assert res.bound == 2


# ── A4.5 partition into invariant-closed capsules ───────────────────────────


def test_partition_disjoint_intents_separate_capsules() -> None:
    g = (_intent("a"), _intent("b"))  # no shared touched notes
    capsules = partition_capsules(g)
    assert len(capsules) == 2
    touched = [c.touched_note_ids for c in capsules]
    assert frozenset({"a"}) in [frozenset(t & {"a", "b"}) for t in touched]


def test_partition_shared_entry_point_unions_capsules() -> None:
    # both a and b register under the same entry point → one capsule.
    g = (_intent("a", navigation=("ep",)), _intent("b", navigation=("ep",)))
    capsules = partition_capsules(g)
    assert len(capsules) == 1
    assert {"a", "b", "ep"} <= capsules[0].touched_note_ids


def test_partition_reverse_inlink_coupling_unions() -> None:
    # a requires a reverse inlink from b → they share the write on b → one capsule.
    g = (_intent("a", required_inlinks=("b",)), _intent("b"))
    capsules = partition_capsules(g)
    assert len(capsules) == 1
    assert {"a", "b"} <= capsules[0].touched_note_ids


def test_partition_deterministic_order() -> None:
    g = (_intent("z"), _intent("a"), _intent("m"))
    c1 = partition_capsules(g)
    c2 = partition_capsules(g)
    assert [min(c.touched_note_ids) for c in c1] == [min(c.touched_note_ids) for c in c2]
    assert [min(c.touched_note_ids) for c in c1] == sorted(
        min(c.touched_note_ids) for c in c1
    )
