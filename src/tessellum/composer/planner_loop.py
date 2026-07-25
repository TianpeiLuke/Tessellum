"""tessellum.composer.planner_loop — bounded planner search with proven halt.

P8 of the dynamic-digestion plan "Dynamic Digestion as a Snapshot-Pinned
Knowledge Transaction". Lets the planner re-plan from review evidence with a
proven TERMINATION bound — deliberately NOT a claimed convergence guarantee
(counter secondary correction, A8.1):

    Dynamic discovery may legitimately ADD obligations (a new note surfaces new
    undigested terms), so an LLM planner is not a monotone transfer function
    over a bounded lattice in general. Convergence language is justified ONLY
    per episode, when the episode FREEZES a finite obligation universe and a
    deterministic reducer proves strict monotone progress within it.

So this module gives BOTH:

- a **monotone variant** over a DETERMINISTIC DB-gate deficit (A8.2) — ghost +
  broken-link + undigested-term + coverage-gap counts, never a nondeterministic
  judge score — that must strictly decrease for a revision to be accepted when
  an episode froze its obligation universe;
- three hard STOPS that guarantee halting regardless (A8.3): a revision-depth
  ceiling, a fuel/gas budget, and oscillation detection on the route/contract
  dimension. A revision that fails to reduce the frozen-universe deficit OR
  exceeds a ceiling terminates the loop as ``blocked`` — never a livelock.

Determinism: the deficit is a pure function of typed gate counts; the loop is a
pure driver over an injected ``propose`` callable (the LLM planner lives behind
that seam). No clock/randomness here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal


@dataclass(frozen=True)
class Deficit:
    """A DETERMINISTIC, well-founded progress measure (A8.2).

    Every component is a non-negative integer count from a DB/gate scan — never
    a model score. ``total`` is the variant function: a revision is progress
    iff its total strictly decreases. Zero total = the frozen obligation
    universe is discharged (``complete``)."""

    ghosts: int = 0
    broken_links: int = 0
    undigested_terms: int = 0
    coverage_gaps: int = 0

    def __post_init__(self) -> None:
        # A well-founded ℕ measure: negative components would let ``total`` hit
        # 0 by cancellation with real obligations still open (a false
        # ``complete``). Reject them so the variant is genuinely non-negative.
        for name in ("ghosts", "broken_links", "undigested_terms", "coverage_gaps"):
            if getattr(self, name) < 0:
                raise ValueError(f"Deficit.{name} must be non-negative")

    @property
    def total(self) -> int:
        return self.ghosts + self.broken_links + self.undigested_terms + self.coverage_gaps

    def as_tuple(self) -> tuple[int, int, int, int]:
        return (self.ghosts, self.broken_links, self.undigested_terms, self.coverage_gaps)


@dataclass(frozen=True)
class Revision:
    """One planner revision: its route/contract signature (for oscillation
    detection) and the deterministic deficit it achieved."""

    revision_id: str
    route_signature: str
    deficit: Deficit


PlannerOutcome = Literal["complete", "blocked"]


@dataclass(frozen=True)
class LoopResult:
    outcome: PlannerOutcome
    revisions: tuple[Revision, ...]
    reason: str
    fuel_spent: int

    @property
    def deficit_trace(self) -> tuple[int, ...]:
        return tuple(r.deficit.total for r in self.revisions)


class PlannerLoopError(Exception):
    pass


@dataclass
class LoopPolicy:
    """The three hard stops that guarantee halting (A8.3)."""

    depth_ceiling: int = 8          # max accepted revisions in one episode
    fuel: int = 16                  # max propose() calls (generalizes RunBudget)
    oscillation_window: int = 4     # a route signature seen this often → stop
    frozen_universe: bool = True    # True: episode froze obligations → require
                                    # strict deficit decrease (convergence claim
                                    # is valid). False: bounded SEARCH only.


def run_planner_loop(
    initial: Revision,
    *,
    propose: Callable[[Revision], Revision | None],
    policy: LoopPolicy | None = None,
) -> LoopResult:
    """Drive the bounded planner search to a terminal ``complete`` or ``blocked``.

    ``propose(prev) -> next_revision | None`` is the injected planner (the LLM
    lives here). The loop:

    - accepts ``complete`` immediately when the deficit total hits zero;
    - in a FROZEN-universe episode, requires each revision's deficit total to
      STRICTLY DECREASE — a non-decreasing revision terminates as ``blocked``
      (the monotone variant over a well-founded ℕ measure guarantees this loop
      cannot run forever);
    - even in bounded-SEARCH mode (no monotonicity assumed), the depth ceiling,
      the fuel budget, and oscillation detection each force a terminal
      ``blocked`` — so halting never depends on the planner being monotone;
    - a ``propose`` returning None (the planner gives up) terminates as
      ``blocked``.

    NEVER livelocks: every path out of the loop is a terminal LoopResult."""
    policy = policy or LoopPolicy()
    revisions: list[Revision] = [initial]
    # stall count per route signature (consecutive non-progressing reuses).
    seen_signatures: dict[str, int] = {}
    fuel_spent = 0

    if initial.deficit.total == 0:
        return LoopResult("complete", tuple(revisions),
                          "initial revision already discharges the obligation universe", 0)

    while True:
        # depth ceiling (counts accepted revisions).
        if len(revisions) - 1 >= policy.depth_ceiling:
            return LoopResult("blocked", tuple(revisions),
                              f"revision-depth ceiling {policy.depth_ceiling} reached",
                              fuel_spent)
        # fuel budget on propose() calls.
        if fuel_spent >= policy.fuel:
            return LoopResult("blocked", tuple(revisions),
                              f"fuel budget {policy.fuel} exhausted", fuel_spent)

        prev = revisions[-1]
        nxt = propose(prev)
        fuel_spent += 1
        if nxt is None:
            return LoopResult("blocked", tuple(revisions),
                              "planner declined to propose a further revision", fuel_spent)

        made_progress = nxt.deficit.total < prev.deficit.total
        revisions.append(nxt)

        # COMPLETION is checked FIRST: a revision that discharges the obligation
        # universe (deficit 0) is a success even if it reuses a route signature
        # or is the last of many same-route steps — it must never be reported
        # as blocked/oscillation.
        if nxt.deficit.total == 0:
            return LoopResult("complete", tuple(revisions),
                              "obligation universe discharged (deficit 0)", fuel_spent)

        # frozen-universe monotonicity: the deficit MUST strictly decrease.
        if policy.frozen_universe and not made_progress:
            return LoopResult("blocked", tuple(revisions),
                              f"deficit did not strictly decrease "
                              f"({prev.deficit.total} -> {nxt.deficit.total}) in a "
                              "frozen-universe episode", fuel_spent)

        # oscillation counts only NON-PROGRESSING repeats of a route signature:
        # a flip-flop that reuses a route/contract WITHOUT reducing the deficit.
        # A monotonically-progressing loop naturally keeps the same route
        # signature (route != deficit) and must NOT be flagged — so a step that
        # reduced the deficit resets that signature's stall count.
        if made_progress:
            seen_signatures[nxt.route_signature] = 0
        else:
            stalls = seen_signatures.get(nxt.route_signature, 0) + 1
            seen_signatures[nxt.route_signature] = stalls
            if stalls >= policy.oscillation_window:
                return LoopResult("blocked", tuple(revisions),
                                  f"oscillation: route signature {nxt.route_signature!r} "
                                  f"stalled {stalls}x (window {policy.oscillation_window})",
                                  fuel_spent)


__all__ = [
    "Deficit",
    "Revision",
    "PlannerOutcome",
    "LoopResult",
    "LoopPolicy",
    "PlannerLoopError",
    "run_planner_loop",
]
