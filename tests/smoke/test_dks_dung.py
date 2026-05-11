"""Smoke tests for tessellum.dks.dung — Dung AF + grounded semantics.

Covers the canonical AF shapes from Dung 1995 §3.3 and the
N>2 disagreement cases that motivate Phase 10:

- No attacks → all "in".
- Single attack (A attacks B) → A in, B out.
- Mutual attack (A↔B) → both undec.
- Defender chain (A→B→C) → A in, B out, C in.
- 3-cycle (A→B→C→A) → all undec.
- N-perspective DKS shape: arg_a, arg_b, arg_c with B attacks A → A out, B in, C in.
- Two-attackers-one-defender shape from Phase 10's plan.
- DungAF helpers: attackers_of / attackees_of.
- grounded_extension returns sorted tuple of IN labels.
"""

from __future__ import annotations

import pytest

from tessellum.dks.dung import (
    DungAF,
    grounded_extension,
    grounded_labelling,
)


# ── Canonical shapes ───────────────────────────────────────────────────────


def test_empty_af():
    """No arguments, no attacks → empty labelling."""
    af = DungAF(arguments=(), attacks=())
    assert grounded_labelling(af) == {}
    assert grounded_extension(af) == ()


def test_single_argument_no_attacks_is_in():
    af = DungAF(arguments=("A",), attacks=())
    assert grounded_labelling(af) == {"A": "in"}
    assert grounded_extension(af) == ("A",)


def test_unattacked_arguments_all_in():
    af = DungAF(arguments=("A", "B", "C"), attacks=())
    labels = grounded_labelling(af)
    assert all(lbl == "in" for lbl in labels.values())
    assert set(grounded_extension(af)) == {"A", "B", "C"}


def test_single_attack_attacker_in_attacked_out():
    """B attacks A → B in (no attackers), A out (attacked by IN)."""
    af = DungAF(arguments=("A", "B"), attacks=(("B", "A"),))
    labels = grounded_labelling(af)
    assert labels["B"] == "in"
    assert labels["A"] == "out"


def test_mutual_attack_both_undec():
    """A↔B mutually attack → neither becomes IN → both undec."""
    af = DungAF(
        arguments=("A", "B"),
        attacks=(("A", "B"), ("B", "A")),
    )
    labels = grounded_labelling(af)
    assert labels == {"A": "undec", "B": "undec"}
    assert grounded_extension(af) == ()


def test_defender_chain():
    """A→B→C: A in (no attackers), B out (A in), C in (B out)."""
    af = DungAF(
        arguments=("A", "B", "C"),
        attacks=(("A", "B"), ("B", "C")),
    )
    labels = grounded_labelling(af)
    assert labels == {"A": "in", "B": "out", "C": "in"}


def test_three_cycle_all_undec():
    """A→B→C→A: all three undec (no defender outside the cycle)."""
    af = DungAF(
        arguments=("A", "B", "C"),
        attacks=(("A", "B"), ("B", "C"), ("C", "A")),
    )
    labels = grounded_labelling(af)
    assert labels == {"A": "undec", "B": "undec", "C": "undec"}


# ── DKS-shaped scenarios (Phase 10) ────────────────────────────────────────


def test_phase10_n3_one_attacker_two_independent():
    """3-perspective DKS: B attacks A; C unchallenged.

    Expected: A out, B in, C in. Multi-survivor (B + C) → revision
    must pick or merge per DKSRuleRevision logic.
    """
    af = DungAF(
        arguments=("A", "B", "C"),
        attacks=(("B", "A"),),
    )
    labels = grounded_labelling(af)
    assert labels == {"A": "out", "B": "in", "C": "in"}
    assert set(grounded_extension(af)) == {"B", "C"}


def test_phase10_two_attackers_one_defender():
    """Two arguments attack A; one defends (attacks an attacker).

    Argument graph:
      B attacks A
      C attacks A
      D attacks B
    Expected: D in (no attackers), B out (D in), C in (no attackers),
    A out (C in — C still attacks A, and C is IN). The defender D
    rescues A only if D defeats all attackers; here D defeats B but
    C still stands → A stays out.
    """
    af = DungAF(
        arguments=("A", "B", "C", "D"),
        attacks=(("B", "A"), ("C", "A"), ("D", "B")),
    )
    labels = grounded_labelling(af)
    assert labels["D"] == "in"
    assert labels["B"] == "out"
    assert labels["C"] == "in"
    assert labels["A"] == "out"


def test_phase10_defender_rescues_attacked_argument():
    """A is attacked by B; B is attacked by C (C defends A).

    Expected: C in, B out, A in. This is the "A survives because its
    attacker has been defeated" scenario — the canonical Dung result.
    """
    af = DungAF(
        arguments=("A", "B", "C"),
        attacks=(("B", "A"), ("C", "B")),
    )
    labels = grounded_labelling(af)
    assert labels == {"C": "in", "B": "out", "A": "in"}


# ── Back-compat: N=2 collapses to today's A/B behaviour ────────────────────


def test_n2_default_dks_shape_matches_existing_logic():
    """The 2-perspective default DKS shape — B attacks A. Result:
    A out, B in. Same as today's closed-loop logic without Dung."""
    af = DungAF(arguments=("A", "B"), attacks=(("B", "A"),))
    extension = grounded_extension(af)
    assert extension == ("B",)


def test_n2_no_disagreement_both_in():
    """A and B agree (no contradicts edge) → both in (cycle short-circuits today)."""
    af = DungAF(arguments=("A", "B"), attacks=())
    labels = grounded_labelling(af)
    assert labels == {"A": "in", "B": "in"}


# ── Edge cases ─────────────────────────────────────────────────────────────


def test_attacks_referencing_unknown_args_silently_ignored():
    af = DungAF(
        arguments=("A", "B"),
        attacks=(("X", "A"), ("B", "Y"), ("B", "A")),
    )
    # Only ("B", "A") is in-scope; others ignored.
    labels = grounded_labelling(af)
    assert labels["A"] == "out"
    assert labels["B"] == "in"


def test_attackers_of_helper():
    af = DungAF(
        arguments=("A", "B", "C"),
        attacks=(("B", "A"), ("C", "A"), ("A", "B")),
    )
    assert af.attackers_of("A") == {"B", "C"}
    assert af.attackers_of("B") == {"A"}
    assert af.attackers_of("C") == set()


def test_attackees_of_helper():
    af = DungAF(
        arguments=("A", "B", "C"),
        attacks=(("B", "A"), ("C", "A"), ("A", "B")),
    )
    assert af.attackees_of("A") == {"B"}
    assert af.attackees_of("B") == {"A"}


def test_grounded_extension_sorted():
    af = DungAF(
        arguments=("zebra", "alpha", "beta"),
        attacks=(),
    )
    # All unattacked → all in. Extension must be sorted by argument ID.
    assert grounded_extension(af) == ("alpha", "beta", "zebra")
