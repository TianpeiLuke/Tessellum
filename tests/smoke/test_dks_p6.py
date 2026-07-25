"""DKS refactor P6 — ECS four-axis separation (decision b7a).

Gate deliverables:
 - BB role is a descriptive data contract with NO next_bb (never routes);
 - acceptance is computed on the DUNG RELATION axis, not the BB-type sequence,
   and Dung-`in` alone is `dialectically_adequate`, not `accepted` (needs the
   independent P4 check);
 - the inquiry-move algebra is a POLICY over (role × relation), not a
   (BBType, BBType) type walk.
"""

from __future__ import annotations

from tessellum.dks import (
    DKS_MOVE_ALGEBRA,
    BBContract,
    acceptance_from_labelling,
    plan_move,
)


# ── axis 1: BB role is a contract with no next_bb ───────────────────────────


def test_bb_contract_has_no_next_bb() -> None:
    c = BBContract(role="argument", key_question="what is claimed?")
    assert not hasattr(c, "next_bb")  # a role types an output; it never routes
    assert c.role == "argument"
    assert c.materializer  # carries a materializer, not a successor


# ── axis 3: acceptance on the relation axis (Dung), not the type axis ───────


def test_acceptance_dung_in_is_dialectically_adequate_not_accepted() -> None:
    # a surviving (Dung-`in`) argument is NOT `true` without an independent
    # check — it is dialectically-adequate-only (Dung-IN does not self-certify).
    v = acceptance_from_labelling("5a", {"5a": "in", "5b": "out"})
    assert v.status == "dialectically_adequate"
    assert v.label == "in"


def test_acceptance_requires_independent_validation_to_be_accepted() -> None:
    v = acceptance_from_labelling(
        "5a", {"5a": "in"}, independently_validated=True,
    )
    assert v.status == "accepted"  # Dung-in AND validated (P4)


def test_acceptance_defeated_and_undecided() -> None:
    assert acceptance_from_labelling("5b", {"5b": "out"}).status == "defeated"
    assert acceptance_from_labelling("x", {}).status == "undecided"  # absent → undec
    assert acceptance_from_labelling(
        "5a", {"5a": "undec", "5b": "undec"},
    ).status == "undecided"  # mutual attack → undecided (not accepted)


def test_acceptance_is_not_derived_from_bb_type_sequence() -> None:
    # the same argument FZ flips acceptance purely on the RELATION label —
    # nothing about a BB-type walk changes; only the Dung labelling does.
    a_in = acceptance_from_labelling("5a", {"5a": "in"})
    a_out = acceptance_from_labelling("5a", {"5a": "out"})
    assert a_in.status != a_out.status  # relation axis drives acceptance


# ── axis 2: the move algebra is a policy, not a type walk ───────────────────


def test_move_algebra_maps_kinds_to_roles_and_relations() -> None:
    assert DKS_MOVE_ALGEBRA["challenge"].produces_role == "counter_argument"
    assert DKS_MOVE_ALGEBRA["challenge"].relation == "attacks"
    assert DKS_MOVE_ALGEBRA["argue"].relation == "supports"
    assert DKS_MOVE_ALGEBRA["observe"].relation is None  # observing creates no edge


def test_plan_move_selects_by_open_obligation_not_type_edge() -> None:
    # the planner picks a move from the OPEN obligations (policy), never by
    # dispatching on a (BBType, BBType) pair.
    assert plan_move(frozenset({"argument"})).kind == "argue"
    assert plan_move(frozenset({"disagreement"})).kind == "challenge"
    # canonical dialectic order when several are open
    assert plan_move(frozenset({"warrant", "observation"})).kind == "observe"
    # nothing open → frontier discharged → no move
    assert plan_move(frozenset()) is None
