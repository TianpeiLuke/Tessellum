"""tessellum.dks.ontology — ECS four-axis separation (decision b7a).

P6 of the DKS refactor plan. Stops BB type from impersonating three axes it
never was (the P4 violation: ``fsm.py`` fused BB type with control state via the
``(BBType, BBType)``-keyed handler registry + ``rule_revision present →
PROCEDURE`` termination). BB role, inquiry move, dialectic relation, and runtime
state are FOUR INDEPENDENT axes:

- **BB role** (this module's ``BBContract``) — a note's epistemic output lens:
  its key question, required content, atomicity check, materializer. It is a
  data tag + a contract with NO ``next_bb`` — it never encodes control flow.
- **inquiry move** (``InquiryMove``) — the cognitive operation that advances
  knowledge (a policy over ``role × relation``), selected from obligations.
- **dialectic relation** (``DialecticRelation`` + the Dung label) — the
  argument-graph edge label; acceptance is computed HERE (on the relation
  axis), not from a BB-type sequence.
- **runtime state** — execution status; lives on the substrate manifest, not on
  the BB type (reused from the dynamic-digestion overlay/publication).

Built mostly by SUBTRACTION (retiring the dead handler registry) + this small
additive model. ``acceptance_from_labelling`` is the A6.2 reform: warrant
precision comes from GROUNDED ACCEPTANCE, not from having walked a type
sequence. All pure.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# ── axis 1: BB role (descriptive output lens — no next_bb) ──────────────────


@dataclass(frozen=True)
class BBContract:
    """A BB role as a DATA CONTRACT (A6.3), NOT a control-flow node.

    Carries what the role's atomic output must satisfy — its key question, the
    required content, an atomicity check, and its materializer key — but
    deliberately has NO ``next_bb`` field: a role never dictates its successor.
    The successor is chosen by the inquiry-move policy (axis 2)."""

    role: str
    key_question: str
    required_content: tuple[str, ...] = ()
    materializer: str = "body_markdown_frontmatter_to_file"
    # NOTE: intentionally NO `next_bb`. A role types an output; it never routes.


# ── axis 3: dialectic relation + acceptance (the relation axis) ─────────────

DialecticRelation = Literal["supports", "attacks", "rebuts", "undercuts"]
DungLabel = Literal["in", "out", "undec"]

AcceptanceStatus = Literal[
    "accepted",              # Dung-`in` AND independently validated (P4)
    "dialectically_adequate",  # Dung-`in` but no exogenous check yet — NOT true
    "defeated",              # Dung-`out`
    "undecided",             # Dung-`undec`
]


@dataclass(frozen=True)
class AcceptanceVerdict:
    """Acceptance computed on the RELATION axis (A6.2). ``status`` derives from
    the Dung grounded labelling — NOT from the BB-type sequence walked."""

    status: AcceptanceStatus
    label: DungLabel


def acceptance_from_labelling(
    argument_fz: str,
    grounded_labelling: dict[str, str],
    *,
    independently_validated: bool = False,
) -> AcceptanceVerdict:
    """Derive an argument's acceptance from the Dung grounded labelling (A6.2).

    A Dung-`in` argument is only ``accepted`` when it also passed an independent
    check (P4); absent that it is ``dialectically_adequate`` — surviving the
    dialectic is necessary but not sufficient for truth (Dung-`in` no longer
    self-certifies). `out` → defeated; `undec`/absent → undecided. Warrant
    precision comes from grounded acceptance, not from a type walk."""
    label = grounded_labelling.get(argument_fz, "undec")
    if label == "in":
        status: AcceptanceStatus = (
            "accepted" if independently_validated else "dialectically_adequate"
        )
    elif label == "out":
        status = "defeated"
    else:
        status = "undecided"
    return AcceptanceVerdict(status=status, label=label)  # type: ignore[arg-type]


# ── axis 2: the inquiry-move algebra (policy over role × relation) ──────────

InquiryMoveKind = Literal[
    "observe",    # ingest a new empirical observation
    "argue",      # produce a competing argument
    "challenge",  # attack an argument (produce a counter)
    "generalize", # aggregate contradictions into a pattern/model
    "revise",     # revise a warrant (close the loop)
    "connect",    # link/extend an existing note (memory reuse)
]


@dataclass(frozen=True)
class InquiryMove:
    """One cognitive operation (A6.4) — a POLICY over ``(role × relation)`` with
    obligation-typed pre/post-conditions. Built ON TOP of the axis split, after
    it is proven: a move is NOT a BB-type edge, it is what the planner selects
    to discharge an obligation. ``feeds`` names the P5 planner's next expected
    obligation kind (advisory), never a hard type transition."""

    kind: InquiryMoveKind
    produces_role: str            # the BB role its output takes (axis 1)
    relation: DialecticRelation | None = None  # the edge it creates (axis 3)
    preconditions: tuple[str, ...] = ()   # obligation kinds it requires open
    postconditions: tuple[str, ...] = ()  # obligation kinds it discharges/opens


# The canonical DKS move algebra — a policy layer, NOT a type walk. Each move
# names the role it produces and the relation it creates; the planner (P5)
# picks moves from open obligations, it does not walk BB→BB edges.
DKS_MOVE_ALGEBRA: dict[InquiryMoveKind, InquiryMove] = {
    "observe": InquiryMove("observe", "empirical_observation"),
    "argue": InquiryMove("argue", "argument", relation="supports"),
    "challenge": InquiryMove("challenge", "counter_argument", relation="attacks"),
    "generalize": InquiryMove("generalize", "model"),
    "revise": InquiryMove("revise", "procedure"),
    "connect": InquiryMove("connect", "concept", relation="supports"),
}


def plan_move(open_obligation_kinds: frozenset[str]) -> InquiryMove | None:
    """A minimal move policy (A6.4): pick the next move for the open
    obligations, in the canonical dialectic order. Returns None when nothing is
    open (the frontier is discharged). This is a POLICY over roles+relations —
    it never dispatches on a ``(BBType, BBType)`` pair."""
    order: tuple[tuple[str, InquiryMoveKind], ...] = (
        ("observation", "observe"),
        ("argument", "argue"),
        ("disagreement", "challenge"),
        ("pattern", "generalize"),
        ("warrant", "revise"),
        ("connection", "connect"),
    )
    for obligation_kind, move_kind in order:
        if obligation_kind in open_obligation_kinds:
            return DKS_MOVE_ALGEBRA[move_kind]
    return None


__all__ = [
    "BBContract",
    "DialecticRelation",
    "DungLabel",
    "AcceptanceStatus",
    "AcceptanceVerdict",
    "acceptance_from_labelling",
    "InquiryMoveKind",
    "InquiryMove",
    "DKS_MOVE_ALGEBRA",
    "plan_move",
]
