"""Dung Abstract Argumentation Framework (AF) + grounded semantics.

When a DKS cycle runs with N > 2 perspectives, the disagreement
detector produces a *graph* of pairwise contradicts edges, not a
single edge. Deciding which arguments survive the dialectic in that
multi-attack setting needs a principled answer to: *given an argument
graph + an attack relation between arguments, which arguments are
acceptable?*

That is exactly Dung's 1995 abstract argumentation framework. This
module ships the minimal API needed by multi-perspective DKS:

- :class:`DungAF` — frozen dataclass of ``(arguments, attacks)``.
- :func:`grounded_labelling` — Dung's grounded semantics; returns
  a ``{arg_id: "in" | "out" | "undec"}`` mapping.

The grounded extension is the *minimal complete* extension — the
intersection of all complete extensions — and it always exists +
is unique. For DKS adequacy termination (warrant survives iff
grounded-label is ``"in"``) this is the right semantics:
non-controversial, deterministic, and always defined.

For N = 2 (Tessellum's default cycle), the grounded labelling
collapses to the existing single-edge "B attacks A" outcome and
returns the identical result as the closed-loop logic — i.e., the
Dung integration is *additive*, not a replacement.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


# ── Types ──────────────────────────────────────────────────────────────────


DungLabel = Literal["in", "out", "undec"]
"""Closed vocabulary for grounded-labelling output.

- ``"in"``     — the argument is acceptable (survives all attacks).
- ``"out"``    — the argument is rejected (attacked by an ``"in"``).
- ``"undec"``  — neither acceptable nor rejected (mutually attacking
                 with no defender). Treated as "not surviving" for
                 DKS adequacy termination.
"""


@dataclass(frozen=True)
class DungAF:
    """A Dung Abstract Argumentation Framework.

    Arguments are identified by opaque string IDs (in DKS context, FZ
    IDs of argument notes). Attacks are directed pairs
    ``(attacker_id, attacked_id)``; ``attacker_id`` attacks
    ``attacked_id``.

    Attacks referencing arguments not in :attr:`arguments` are
    *silently ignored* by :func:`grounded_labelling` — this matters
    when constructing the AF from a partial corpus snapshot.
    """

    arguments: tuple[str, ...]
    attacks: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def attackers_of(self, arg_id: str) -> set[str]:
        """Set of arguments that attack ``arg_id``."""
        return {a for a, b in self.attacks if b == arg_id}

    def attackees_of(self, arg_id: str) -> set[str]:
        """Set of arguments that ``arg_id`` attacks."""
        return {b for a, b in self.attacks if a == arg_id}


# ── Grounded semantics ─────────────────────────────────────────────────────


def grounded_labelling(af: DungAF) -> dict[str, DungLabel]:
    """Compute Dung's grounded labelling for the given AF.

    Algorithm (fixpoint iteration):

    1. Initialise: every argument is ``"undec"``.
    2. Mark as ``"in"`` every argument whose attackers are all
       ``"out"`` (vacuously true when there are no attackers).
    3. Mark as ``"out"`` every ``"undec"`` argument that has at
       least one ``"in"`` attacker.
    4. Repeat 2–3 until no labels change.
    5. Any argument still ``"undec"`` at the fixpoint stays
       ``"undec"`` (mutually-attacking cycles without external
       defenders).

    The grounded labelling is *unique* — independent of attack
    enumeration order.

    Complexity is O(|attacks| × |arguments|) in the worst case; for
    DKS cycles with N ≤ 8 perspectives this is trivial.

    Arguments referenced in :attr:`DungAF.attacks` but not present in
    :attr:`DungAF.arguments` are silently ignored.
    """
    args = set(af.arguments)
    attackers: dict[str, set[str]] = {a: set() for a in args}
    for attacker, attacked in af.attacks:
        if attacker not in args or attacked not in args:
            continue
        attackers[attacked].add(attacker)

    labels: dict[str, DungLabel] = {a: "undec" for a in args}

    changed = True
    while changed:
        changed = False
        # Rule 1: any undec arg whose attackers are all OUT becomes IN.
        for arg in args:
            if labels[arg] != "undec":
                continue
            if all(labels[att] == "out" for att in attackers[arg]):
                labels[arg] = "in"
                changed = True
        # Rule 2: any undec arg attacked by an IN becomes OUT.
        for arg in args:
            if labels[arg] != "undec":
                continue
            if any(labels[att] == "in" for att in attackers[arg]):
                labels[arg] = "out"
                changed = True

    return labels


def grounded_extension(af: DungAF) -> tuple[str, ...]:
    """Return the set of arguments labelled ``"in"`` by
    :func:`grounded_labelling`. Sorted by argument ID for stable
    iteration order.

    The grounded *extension* is the standard way to refer to "the
    surviving arguments under Dung's grounded semantics" — semantically
    equivalent to ``[a for a, l in grounded_labelling(af).items() if l == "in"]``,
    just sorted.
    """
    labels = grounded_labelling(af)
    return tuple(sorted(a for a, lbl in labels.items() if lbl == "in"))


__all__ = [
    "DungAF",
    "DungLabel",
    "grounded_extension",
    "grounded_labelling",
]
