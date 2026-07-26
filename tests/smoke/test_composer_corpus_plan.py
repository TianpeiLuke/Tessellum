"""M1 + M2 smoke — typed plan-shape decision + hierarchical corpus plan.

Multi-document corpus digestion (FZ 20k9c1a1a1b7b1). Covers:
  - M1: classify_plan_shape thresholds (ported verbatim from skill §1d),
        the both-axes rule, and the non-negative guard.
  - M2: SubObjective validators (slice non-empty/unique/normalized, self-dep
        guard); CorpusPlan validators (shape gate, unique sub_id, dependency
        resolution + acyclicity, term-owner resolution, bundle partition);
        the PURE master_index derivation (no note-table duplication),
        deterministic wave_order, and stable corpus_plan_content_id.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from tessellum.composer import (
    PHASED_MAX_NOTES,
    PHASED_MAX_WORDS,
    SINGLE_PLAN_MAX_NOTES,
    SINGLE_PLAN_MAX_WORDS,
    CorpusPlan,
    SharedCrossRef,
    SubObjective,
    TermOwnerRow,
    classify_plan_shape,
    corpus_plan_content_id,
)


# ── M1: classify_plan_shape ─────────────────────────────────────────────────


def test_plan_shape_single_under_both_ceilings() -> None:
    assert classify_plan_shape(5_000, 8) == "single_plan"
    assert classify_plan_shape(0, 0) == "single_plan"
    # exactly at the single ceilings is still single (thresholds are strict >).
    assert classify_plan_shape(SINGLE_PLAN_MAX_WORDS, SINGLE_PLAN_MAX_NOTES) == "single_plan"


def test_plan_shape_phased_band() -> None:
    assert classify_plan_shape(SINGLE_PLAN_MAX_WORDS + 1, 8) == "single_plan_phased"
    assert classify_plan_shape(5_000, SINGLE_PLAN_MAX_NOTES + 1) == "single_plan_phased"
    assert classify_plan_shape(PHASED_MAX_WORDS, PHASED_MAX_NOTES) == "single_plan_phased"


def test_plan_shape_master_over_ceiling() -> None:
    assert classify_plan_shape(PHASED_MAX_WORDS + 1, 8) == "master_plus_subplans"
    assert classify_plan_shape(5_000, PHASED_MAX_NOTES + 1) == "master_plus_subplans"
    assert classify_plan_shape(100_000, 200) == "master_plus_subplans"


def test_plan_shape_stronger_axis_wins() -> None:
    # few words but a huge note count → still decomposed (the many-notes axis).
    assert classify_plan_shape(1_000, 40) == "master_plus_subplans"
    # huge words, few notes → decomposed (the word-dense axis).
    assert classify_plan_shape(80_000, 5) == "master_plus_subplans"


def test_plan_shape_rejects_negative() -> None:
    with pytest.raises(ValueError):
        classify_plan_shape(-1, 5)
    with pytest.raises(ValueError):
        classify_plan_shape(5, -1)


# ── M2: SubObjective ────────────────────────────────────────────────────────


def _sub(sub_id: str, ordinals: tuple[int, ...], *, priority: str = "P2",
         deps: tuple[str, ...] = (), notes: int = 5) -> SubObjective:
    return SubObjective(
        sub_id=sub_id, topic=f"topic-{sub_id}", priority=priority,
        member_ordinals=ordinals, est_note_count=notes, depends_on=deps,
    )


def test_subobjective_normalizes_ordinals() -> None:
    s = _sub("s1", (2, 0, 1))
    assert s.member_ordinals == (0, 1, 2)  # re-sorted ascending


def test_subobjective_rejects_empty_slice() -> None:
    with pytest.raises(ValidationError):
        SubObjective(sub_id="s1", topic="t", member_ordinals=(), est_note_count=1)


def test_subobjective_rejects_duplicate_ordinals() -> None:
    with pytest.raises(ValidationError):
        _sub("s1", (0, 0, 1))


def test_subobjective_rejects_negative_ordinals() -> None:
    with pytest.raises(ValidationError):
        _sub("s1", (0, -2))


def test_subobjective_rejects_self_dependency() -> None:
    with pytest.raises(ValidationError):
        _sub("s1", (0,), deps=("s1",))


def test_subobjective_frozen() -> None:
    s = _sub("s1", (0,))
    with pytest.raises(ValidationError):
        s.priority = "P1"  # type: ignore[misc]


# ── M2: CorpusPlan validators ───────────────────────────────────────────────


def _plan(**kw) -> CorpusPlan:
    base = dict(
        bundle_id="bundle-abc",
        objective="digest the corpus",
        sub_objectives=(
            _sub("s1", (0, 1), priority="P1"),
            _sub("s2", (2,), priority="P2", deps=("s1",)),
        ),
        bundle_member_count=3,
    )
    base.update(kw)
    return CorpusPlan(**base)


def test_corpus_plan_valid_partition() -> None:
    plan = _plan()
    assert plan.plan_shape == "master_plus_subplans"
    assert len(plan.sub_objectives) == 2


def test_corpus_plan_rejects_flat_shape() -> None:
    with pytest.raises(ValidationError):
        _plan(plan_shape="single_plan")


def test_corpus_plan_rejects_empty_sub_objectives() -> None:
    with pytest.raises(ValidationError):
        _plan(sub_objectives=())


def test_corpus_plan_rejects_duplicate_sub_id() -> None:
    with pytest.raises(ValidationError):
        _plan(sub_objectives=(_sub("s1", (0,)), _sub("s1", (1, 2))))


def test_corpus_plan_rejects_unknown_dependency() -> None:
    with pytest.raises(ValidationError):
        _plan(sub_objectives=(_sub("s1", (0, 1, 2), deps=("ghost",)),))


def test_corpus_plan_rejects_dependency_cycle() -> None:
    with pytest.raises(ValidationError):
        _plan(sub_objectives=(
            _sub("s1", (0,), deps=("s2",)),
            _sub("s2", (1, 2), deps=("s1",)),
        ))


def test_corpus_plan_rejects_orphaned_bundle_member() -> None:
    # member ordinal 2 owned by nobody, count=3 → orphan.
    with pytest.raises(ValidationError):
        _plan(sub_objectives=(_sub("s1", (0, 1)),), bundle_member_count=3)


def test_corpus_plan_rejects_ordinal_out_of_range() -> None:
    with pytest.raises(ValidationError):
        _plan(sub_objectives=(_sub("s1", (0, 1, 5)),), bundle_member_count=3)


def test_corpus_plan_skips_partition_when_count_unknown() -> None:
    # count=0 → range/coverage check skipped; uniqueness + acyclicity still run.
    plan = _plan(sub_objectives=(_sub("s1", (7, 9)),), bundle_member_count=0)
    assert plan.bundle_member_count == 0


def test_corpus_plan_rejects_unknown_term_owner() -> None:
    with pytest.raises(ValidationError):
        _plan(term_ownership=(TermOwnerRow(term="term_x", owner_sub_id="ghost"),))


def test_corpus_plan_accepts_resolved_term_owner() -> None:
    plan = _plan(term_ownership=(TermOwnerRow(term="term_x", owner_sub_id="s2"),))
    assert plan.term_ownership[0].owner_sub_id == "s2"


# ── M2: pure derivations ────────────────────────────────────────────────────


def test_master_index_is_pure_projection() -> None:
    plan = _plan()
    idx = plan.master_index()
    assert [r.sub_id for r in idx] == ["s1", "s2"]  # declared order
    assert [r.topic for r in idx] == ["topic-s1", "topic-s2"]
    assert [r.priority for r in idx] == ["P1", "P2"]
    # the index carries NO note table — only lightweight rows (id/topic/count/priority).
    assert all(hasattr(r, "est_note_count") and not hasattr(r, "member_ordinals") for r in idx)


def test_wave_order_priority_then_dependency() -> None:
    # s2 depends on s1 and s1 is P1 → s1 first regardless.
    assert _plan().wave_order() == ("s1", "s2")


def test_wave_order_priority_major_ties_by_id() -> None:
    plan = _plan(
        sub_objectives=(
            _sub("b", (0,), priority="P2"),
            _sub("a", (1,), priority="P1"),
            _sub("c", (2,), priority="P1"),
        ),
        bundle_member_count=3,
    )
    # P1 before P2; within P1, id order a<c; then b.
    assert plan.wave_order() == ("a", "c", "b")


def test_dependency_layers_independent_first_layer() -> None:
    # s1(P1) and s2(P2) both depend on nothing → same first layer, priority-major.
    plan = _plan()  # s1 P1 no deps, s2 P2 deps=(s1,)
    layers = plan.dependency_layers()
    assert layers == (("s1",), ("s2",))  # s2 depends on s1 → second layer


def test_dependency_layers_chain_is_all_singletons() -> None:
    plan = _plan(
        sub_objectives=(
            _sub("a", (0,), priority="P1"),
            _sub("b", (1,), priority="P1", deps=("a",)),
            _sub("c", (2,), priority="P1", deps=("b",)),
        ),
        bundle_member_count=3,
    )
    assert plan.dependency_layers() == (("a",), ("b",), ("c",))


def test_dependency_layers_independent_share_a_layer() -> None:
    # three mutually-independent sub-objectives → one layer, priority-major/id.
    plan = _plan(
        sub_objectives=(
            _sub("b", (0,), priority="P2"),
            _sub("a", (1,), priority="P1"),
            _sub("c", (2,), priority="P1"),
        ),
        bundle_member_count=3,
    )
    assert plan.dependency_layers() == (("a", "c", "b"),)  # P1 a,c then P2 b


def test_dependency_layers_diamond() -> None:
    # a → {b, c} → d : layers [a], [b,c], [d].
    plan = _plan(
        sub_objectives=(
            _sub("a", (0,), priority="P1"),
            _sub("b", (1,), priority="P1", deps=("a",)),
            _sub("c", (2,), priority="P1", deps=("a",)),
            _sub("d", (3,), priority="P1", deps=("b", "c")),
        ),
        bundle_member_count=4,
    )
    assert plan.dependency_layers() == (("a",), ("b", "c"), ("d",))


def test_dependency_layers_fails_loud_on_cycle_via_bypass() -> None:
    # Review (low): dependency_layers must raise (not hang) on a cyclic graph,
    # mirroring wave_order/_assert_acyclic, if ever reached via a validator
    # bypass (model_construct). The normal constructor rejects cycles earlier.
    plan = CorpusPlan.model_construct(
        bundle_id="b", objective="o", plan_shape="master_plus_subplans",
        sub_objectives=(
            SubObjective(sub_id="x", topic="x", member_ordinals=(0,),
                         est_note_count=1, depends_on=("y",)),
            SubObjective(sub_id="y", topic="y", member_ordinals=(1,),
                         est_note_count=1, depends_on=("x",)),
        ),
        term_ownership=(), shared_cross_refs=(), bundle_member_count=0,
    )
    with pytest.raises(ValueError, match="cyclic"):
        plan.dependency_layers()


def test_dependency_layers_respect_cross_layer_barrier() -> None:
    # flattening layers is a valid topological order (dep never before its dep).
    plan = _plan(
        sub_objectives=(
            _sub("hi", (0,), priority="P1", deps=("lo",)),
            _sub("lo", (1, 2), priority="P3"),
        ),
        bundle_member_count=3,
    )
    flat = [sid for layer in plan.dependency_layers() for sid in layer]
    assert flat.index("lo") < flat.index("hi")


def test_wave_order_dependency_beats_priority() -> None:
    # a P1 sub-plan that depends on a P3 sub-plan must still come AFTER it.
    plan = _plan(
        sub_objectives=(
            _sub("hi", (0,), priority="P1", deps=("lo",)),
            _sub("lo", (1, 2), priority="P3"),
        ),
        bundle_member_count=3,
    )
    assert plan.wave_order() == ("lo", "hi")


def test_content_id_stable_and_order_independent_of_shared_refs() -> None:
    p1 = _plan(shared_cross_refs=(
        SharedCrossRef(target="term_a"), SharedCrossRef(target="term_b"),
    ))
    p2 = _plan(shared_cross_refs=(
        SharedCrossRef(target="term_a"), SharedCrossRef(target="term_b"),
    ))
    assert corpus_plan_content_id(p1) == corpus_plan_content_id(p2)


def test_content_id_changes_with_content() -> None:
    a = corpus_plan_content_id(_plan())
    b = corpus_plan_content_id(_plan(objective="a different objective"))
    assert a != b
