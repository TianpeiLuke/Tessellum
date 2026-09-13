"""tessellum.dks.reach — seeded traversal with a hard hop budget (step 2).

P7 of the query-time DKS plan. Step 1 anchors the query on a canonical entity;
step 2 is what gets from that anchor to the notes an answer actually needs —
including the **bridge note**, the one that carries the connection between two
things the query mentions and that no ranker will ever rank highly, because it
is about the *joint*, not about either term. A retrieval pass that "merely
augments a prompt best-effort" cannot reach it; an authored link can. That gap
is the strongest single objection to answering at query time, so reaching it is
its own step with its own bound rather than an implicit detail of derivation.

Three properties are load-bearing and all three are tested:

- **The seed is the resolved entity, not the raw keywords.** A reach starts from
  what step 1 resolved (:class:`~tessellum.dks.resolve_entity.Resolution`).
  When resolution abstained there is no anchor, so the default is to abstain
  too (``stopping_reason="no_seed"``); widening to the ambiguous candidate set
  is available but **opt-in** (``on_ambiguous="widen"``), because a widened
  anchor is a guess wearing a traversal.
- **The budget is a hard parameter.** :class:`HopBudget` is a set of ceilings,
  validated at construction and refused rather than clamped. Unbounded
  iteration would reintroduce exactly the cost this design exists to avoid, so
  a third hop is not something a caller can drift into.
- **Stopping is recorded, not assumed.** Every result carries the hop count and
  a :data:`ReachStopReason`, and says whether the stop was a principled
  discharge or a truncation — the ``understood`` vs ``truncated`` distinction
  the shipped autonomy machinery already draws.

**Model-free.** The stop rule is
:func:`~tessellum.dks.autonomy.voi_stop_decision` — a deterministic ``λ``
comparison over the :class:`~tessellum.dks.autonomy.InquiryFrontier`, driven by
:func:`~tessellum.dks.autonomy.run_bounded_inquiry` (whose depth/fuel stops
prove halting independently of anything here). Expected information gain decays
with hop distance, so ``λ`` prunes far, weakly-anchored frontier nodes
arithmetically. No model is asked "does this evidence answer the question?" —
the deterministic rule goes first and the result records enough to measure
whether it sufficed.

Pure (the Dependency Rule): no runtime import, no disk, no vault write. The
index is read only through the :class:`LinkExpansionBackend` /
:class:`SimilarityBackend` ports, both of which
:class:`~tessellum.dks.retrieval_client.RetrievalClient` satisfies structurally.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal, Mapping, Protocol, Sequence

from tessellum.composer.planner_loop import LoopPolicy, Revision
from tessellum.dks.autonomy import (
    EpistemicObligation,
    InquiryFrontier,
    StopDecision,
    run_bounded_inquiry,
    voi_stop_decision,
)
from tessellum.dks.resolve_entity import Resolution
from tessellum.dks.retrieval_client import LinkNeighbour, RetrievalHit

HARD_MAX_HOPS: int = 2
"""The widest reach the design admits. ``1–2 hops`` is the stated range; a
budget past it is refused, which is what makes the bound a bound."""

DEFAULT_MAX_HOPS: int = 2
DEFAULT_MAX_NOTES: int = 50
"""Ceiling on notes held by one reach — the fan-out half of the budget. Two hops
through a densely linked neighbourhood is unbounded in practice without it."""

DEFAULT_LAMBDA_COST: float = 0.0
"""``λ`` for the VOI stop. ``0.0`` retires nothing (every gain here is positive),
so the default reach is bounded by hops and fan-out alone; a caller that wants
the frontier pruned by expected gain raises it deliberately."""

DEFAULT_SEED_K: int = 5
"""Similarity seeds taken alongside the entity's own note, when a similarity
backend is supplied at all."""

DEFAULT_MAX_RERETRIEVALS: int = 1
"""How many times derivation may report a missing hop and get another reach.
The re-retrieval trigger is bounded for the same reason the hops are."""

AMBIGUOUS_SEED_WEIGHT: float = 0.5
"""Weight of a candidate seed under the opt-in ``on_ambiguous="widen"`` policy —
half an anchor, because that is what an unresolved candidate is."""

ReachVia = Literal["entity", "similarity", "link"]
"""How a note entered the reached set. ``"link"`` is the interesting one: it is
the traversal reaching what the rankers did not rank."""

ReachStopReason = Literal[
    "fixpoint",              # nothing expandable is left — understood
    "retired_below_lambda",  # every open obligation's gain is below λ — understood
    "budget_exhausted",      # a ceiling fired — TRUNCATED, not understood
    "no_seed",               # step 1 gave no anchor — nothing was attempted
]
"""Why a reach stopped. The first three are
:data:`~tessellum.dks.autonomy.TerminationReason` verbatim; ``no_seed`` is this
step's own refusal, and it is not a traversal outcome at all."""

_UNDERSTOOD_REASONS: frozenset[str] = frozenset({"fixpoint", "retired_below_lambda"})


class BudgetError(ValueError):
    """A budget outside the admitted bounds. Raised at construction, so an
    over-wide reach cannot be requested at all."""


# ── ports ────────────────────────────────────────────────────────────────────


class LinkExpansionBackend(Protocol):
    """Port for one bounded expansion over the authored link graph.

    :class:`~tessellum.dks.retrieval_client.RetrievalClient` satisfies this
    structurally (its ``expand_links`` reads ``note_links`` through
    :mod:`tessellum.retrieval`), and :class:`MappingLinkBackend` satisfies it
    deterministically for tests — so ``reach`` never touches an index or an
    ``indexer`` import."""

    def expand_links(
        self, seed: str, *, hops: int = 1
    ) -> Sequence[LinkNeighbour]: ...


class SimilarityBackend(Protocol):
    """Port for the ranked read that *widens the seed set*.

    Deliberately narrow: reach uses similarity only to seed, never to reach.
    :class:`~tessellum.dks.retrieval_client.RetrievalClient` satisfies it."""

    def search(self, query: str, *, k: int = 20) -> Sequence[RetrievalHit]: ...


@dataclass(frozen=True)
class MappingLinkBackend:
    """Deterministic expansion over a fixed ``note_id → neighbours`` adjacency.

    Mirrors :class:`~tessellum.dks.resolve_entity.MappingSearchBackend`: the
    adjacency is given, undirected closure is computed here (an authored link
    relates both ends), and the walk is breadth-first in the order the mapping
    lists neighbours — so a test controls the reached set exactly."""

    adjacency: Mapping[str, tuple[str, ...]]

    def _undirected(self) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for source, targets in self.adjacency.items():
            out.setdefault(source, [])
            for target in targets:
                if target not in out[source]:
                    out[source].append(target)
                back = out.setdefault(target, [])
                if source not in back:
                    back.append(source)
        return out

    def expand_links(
        self, seed: str, *, hops: int = 1
    ) -> Sequence[LinkNeighbour]:
        if hops < 1:
            raise ValueError(f"hops={hops} must be at least 1")
        adjacency = self._undirected()
        seen: set[str] = {seed}
        ring: list[tuple[str, tuple[str, ...]]] = [(seed, (seed,))]
        found: list[LinkNeighbour] = []
        for depth in range(1, hops + 1):
            nxt: list[tuple[str, tuple[str, ...]]] = []
            for node, path in ring:
                for neighbour in adjacency.get(node, ()):
                    if neighbour in seen:
                        continue
                    seen.add(neighbour)
                    walked = path + (neighbour,)
                    found.append(
                        LinkNeighbour(
                            note_id=neighbour,
                            note_name=neighbour.rsplit("/", 1)[-1].removesuffix(".md"),
                            hops=depth,
                            path=walked,
                        )
                    )
                    nxt.append((neighbour, walked))
            ring = nxt
        return tuple(found)


@dataclass(frozen=True)
class MappingSimilarityBackend:
    """Deterministic ranked seeds over a fixed ``query → note ids`` mapping.

    The list is the ranking, best first. A test that needs similarity to
    *demonstrably exclude* a note simply leaves it out — which is how the
    bridge-note property is proved rather than assumed."""

    ranking: Mapping[str, tuple[str, ...]]

    def search(self, query: str, *, k: int = 20) -> Sequence[RetrievalHit]:
        ranked = self.ranking.get(query, ())[: max(k, 0)]
        return tuple(
            RetrievalHit(
                note_id=note_id,
                note_name=note_id.rsplit("/", 1)[-1].removesuffix(".md"),
                score=1.0 / (rank + 1),
                bm25_rank=rank,
                dense_rank=None,
            )
            for rank, note_id in enumerate(ranked)
        )


# ── the budget ───────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class HopBudget:
    """The hard bound on one reach. Every field is a ceiling, not advice.

    Args:
        max_hops: Link distance the traversal may spend, ``1..HARD_MAX_HOPS``.
        max_notes: Total notes the reached set may hold, seeds included.
        lambda_cost: ``λ`` for the VOI stop — an open frontier node whose
            expected gain falls below it is not worth expanding.
        seed_k: Similarity seeds taken when a similarity backend is supplied.
        max_reretrievals: How many missing-hop re-reaches are permitted.

    Raises:
        BudgetError: on any value outside the admitted range. Refusing beats
            clamping: a clamped budget silently answers a different question
            than the one asked.
    """

    max_hops: int = DEFAULT_MAX_HOPS
    max_notes: int = DEFAULT_MAX_NOTES
    lambda_cost: float = DEFAULT_LAMBDA_COST
    seed_k: int = DEFAULT_SEED_K
    max_reretrievals: int = DEFAULT_MAX_RERETRIEVALS

    def __post_init__(self) -> None:
        if not 1 <= self.max_hops <= HARD_MAX_HOPS:
            raise BudgetError(
                f"max_hops={self.max_hops} is outside the admitted reach "
                f"1..{HARD_MAX_HOPS}"
            )
        if self.max_notes < 1:
            raise BudgetError(f"max_notes={self.max_notes} must be at least 1")
        if self.lambda_cost < 0.0:
            raise BudgetError(f"lambda_cost={self.lambda_cost} must be non-negative")
        if self.seed_k < 0:
            raise BudgetError(f"seed_k={self.seed_k} must be non-negative")
        if self.max_reretrievals < 0:
            raise BudgetError(
                f"max_reretrievals={self.max_reretrievals} must be non-negative"
            )

    def loop_policy(self) -> LoopPolicy:
        """The shipped scheduler's ceilings, set one ring wider than the hop
        budget so the ring logic gets to observe its own fixpoint — and so
        halting still does not depend on that logic being right."""
        return LoopPolicy(
            depth_ceiling=self.max_hops + 1,
            fuel=self.max_hops + 1,
            oscillation_window=self.max_hops + 2,
            frozen_universe=False,  # a hop legitimately ADDS obligations
        )


# ── the result ───────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ReachedNote:
    """One note in the reached set, with the route that reached it.

    ``weight`` is ``seed_weight / (1 + hops)`` — the seed's anchor strength
    discounted by distance, the same shape the graph retrieval arm uses. It is
    the expected-information-gain input the ``λ`` stop compares, so the ordering
    of the traversal is a pure function of the fixture."""

    note_id: str
    hops: int
    via: ReachVia
    path: tuple[str, ...]
    weight: float

    @property
    def seed_note_id(self) -> str:
        """The seed this note was reached from — ``path[0]`` by construction."""
        return self.path[0]


@dataclass(frozen=True)
class MissingHop:
    """Derivation's report that it could not connect something (the P8 seam).

    ``from_note_id`` is where the chain dead-ended; the re-retrieval trigger
    re-seeds there rather than widening the original query, so the second reach
    is aimed at the actual gap. ``expected_information_gain`` is the caller's
    estimate, compared against the budget's ``λ`` exactly like any other
    obligation."""

    from_note_id: str
    question: str
    expected_information_gain: float = 1.0


@dataclass(frozen=True)
class ReachResult:
    """What one bounded reach reached, and why it stopped.

    The stopping fields are the point of the phase: ``hop_count`` and
    ``stopping_reason`` are recorded on every result, and ``understood``
    separates a principled discharge from a truncation so a caller cannot read
    a budget stop as an exhausted graph."""

    resolution: Resolution
    seeds: tuple[str, ...]
    notes: tuple[ReachedNote, ...]
    similarity_top_k: tuple[str, ...]
    hop_count: int
    hops_expanded: int
    stopping_reason: ReachStopReason
    budget: HopBudget
    reretrievals: int = 0
    missing_hops: tuple[MissingHop, ...] = ()

    @property
    def understood(self) -> bool:
        """Whether the stop was a principled discharge rather than a truncation."""
        return self.stopping_reason in _UNDERSTOOD_REASONS

    @property
    def note_ids(self) -> frozenset[str]:
        return frozenset(n.note_id for n in self.notes)

    def reached(self, note_id: str) -> ReachedNote | None:
        """The record for ``note_id``, or ``None`` if the reach never got there."""
        for note in self.notes:
            if note.note_id == note_id:
                return note
        return None

    @property
    def bridge_notes(self) -> tuple[ReachedNote, ...]:
        """Notes reached over links that the similarity ranking did not return.

        This is the property the phase exists to establish, exposed as a field
        rather than left for a caller to reconstruct: every note here is
        evidence the traversal found something the rankers could not rank."""
        ranked = frozenset(self.similarity_top_k)
        return tuple(
            n for n in self.notes if n.via == "link" and n.note_id not in ranked
        )

    def __str__(self) -> str:
        return (
            f"reach({len(self.seeds)} seeds) -> {len(self.notes)} notes "
            f"in {self.hop_count} hop(s) "
            f"[{self.stopping_reason}"
            f"{'' if self.understood else ' TRUNCATED'}]"
        )


# ── the traversal ────────────────────────────────────────────────────────────


class SeededReach:
    """Expand the resolved entity's neighbourhood under a hard budget.

    Args:
        expander: The bounded link-expansion port. Required — links are the
            whole point; a reach without them is just retrieval.
        similarity: Optional ranked port used **only to widen the seed set**,
            queried with the *resolved entity's canonical name* rather than the
            caller's raw mention. ``None`` seeds from the entity's own note
            alone.
        budget: The ceilings. Defaults to :class:`HopBudget`'s defaults.
        on_ambiguous: ``"abstain"`` (default) refuses to reach at all when step
            1 returned candidates instead of an entity; ``"widen"`` opts in to
            seeding from every candidate at :data:`AMBIGUOUS_SEED_WEIGHT`.
    """

    def __init__(
        self,
        *,
        expander: LinkExpansionBackend,
        similarity: SimilarityBackend | None = None,
        budget: HopBudget | None = None,
        on_ambiguous: Literal["abstain", "widen"] = "abstain",
    ) -> None:
        self.expander = expander
        self.similarity = similarity
        self.budget = budget or HopBudget()
        self.on_ambiguous = on_ambiguous

    # ── seeding ─────────────────────────────────────────────────────────────

    def _seed_notes(
        self, resolution: Resolution, similarity_top_k: Sequence[str]
    ) -> tuple[ReachedNote, ...]:
        """Seeds from the RESOLVED ENTITY, and from nothing else.

        The entity's note id and its ``entity_id`` are the same string by the
        registry's construction (the spine keys entities on their defining
        note), so no mapping table is needed here. The similarity seeds were
        queried on the canonical name — never on the caller's raw surface form,
        which is the keyword seeding this step replaces — and rank weight
        ``1/(rank+1)`` is the same discount the graph retrieval arm uses."""
        anchors: list[ReachedNote] = []
        if resolution.entity_id is not None:
            anchors.append(self._seed(resolution.entity_id, "entity", 1.0))
        elif resolution.is_ambiguous and self.on_ambiguous == "widen":
            anchors.extend(
                self._seed(candidate.entity_id, "entity", AMBIGUOUS_SEED_WEIGHT)
                for candidate in resolution.candidates
            )
        if not anchors:
            # No anchor: abstain rather than fall back on the raw mention. A
            # keyword seed here would silently reintroduce the failure step 1
            # exists to prevent.
            return ()
        widened = [
            self._seed(note_id, "similarity", 1.0 / (rank + 1))
            for rank, note_id in enumerate(similarity_top_k)
        ]
        return tuple(anchors) + tuple(widened)

    def _similarity_seed_ids(self, resolution: Resolution) -> tuple[str, ...]:
        """The similarity top-k, keyed on the resolved entity's canonical name.

        Recorded on the result whether or not it is used for seeding, because it
        is the comparison a bridge-note claim is made against: a note reached
        over links but absent here is one similarity could not rank."""
        if self.similarity is None or self.budget.seed_k <= 0:
            return ()
        query = resolution.canonical_name or resolution.mention
        return tuple(
            hit.note_id
            for hit in self.similarity.search(query, k=self.budget.seed_k)
        )

    @staticmethod
    def _seed(note_id: str, via: ReachVia, weight: float) -> ReachedNote:
        return ReachedNote(
            note_id=note_id, hops=0, via=via, path=(note_id,), weight=weight
        )

    # ── the reach ───────────────────────────────────────────────────────────

    def reach(self, resolution: Resolution) -> ReachResult:
        """Reach from one resolved entity, under the budget.

        Returns a :class:`ReachResult` in every case, including the refusals:
        an unresolved (or, by default, ambiguous) anchor yields an empty reach
        with ``stopping_reason="no_seed"``, which is a recorded abstention
        rather than a silent empty list."""
        similarity_top_k = self._similarity_seed_ids(resolution)
        seeds = self._seed_notes(resolution, similarity_top_k)
        if not seeds:
            return ReachResult(
                resolution=resolution,
                seeds=(),
                notes=(),
                similarity_top_k=similarity_top_k,
                hop_count=0,
                hops_expanded=0,
                stopping_reason="no_seed",
                budget=self.budget,
            )
        notes, hops_expanded, reason = self._walk(seeds)
        return ReachResult(
            resolution=resolution,
            seeds=tuple(s.note_id for s in seeds),
            notes=notes,
            similarity_top_k=similarity_top_k,
            hop_count=max((n.hops for n in notes), default=0),
            hops_expanded=hops_expanded,
            stopping_reason=reason,
            budget=self.budget,
        )

    def reach_again(
        self, previous: ReachResult, missing_hops: Sequence[MissingHop]
    ) -> ReachResult:
        """The re-retrieval trigger: derivation reported a missing hop.

        Re-seeds at the notes where the chain dead-ended and spends a *fresh*
        hop budget from there, keeping everything already reached. Bounded by
        ``budget.max_reretrievals``: past it the call is refused with
        ``stopping_reason="budget_exhausted"`` and the reached set unchanged, so
        a derivation that keeps asking cannot turn this into unbounded
        iteration."""
        already = tuple(previous.missing_hops) + tuple(missing_hops)
        if not missing_hops or previous.reretrievals >= self.budget.max_reretrievals:
            return replace(
                previous,
                stopping_reason="budget_exhausted"
                if missing_hops
                else previous.stopping_reason,
                missing_hops=already,
            )
        seeds = tuple(
            ReachedNote(
                note_id=hop.from_note_id,
                hops=0,
                via="entity",
                path=(hop.from_note_id,),
                weight=hop.expected_information_gain,
            )
            for hop in missing_hops
        )
        fresh, hops_expanded, reason = self._walk(seeds)
        # The fresh walk may traverse BACK through already-reached notes — that
        # is how it gets past the dead end — but a note already in the reached
        # set keeps its original record, so a re-reach never rewrites the
        # provenance of an earlier hop.
        merged = previous.notes + tuple(
            n for n in fresh if n.note_id not in previous.note_ids
        )
        return ReachResult(
            resolution=previous.resolution,
            seeds=previous.seeds + tuple(s.note_id for s in seeds),
            notes=merged,
            similarity_top_k=previous.similarity_top_k,
            hop_count=max((n.hops for n in merged), default=0),
            hops_expanded=previous.hops_expanded + hops_expanded,
            stopping_reason=reason,
            budget=self.budget,
            reretrievals=previous.reretrievals + 1,
            missing_hops=already,
        )

    # ── the bounded walk ────────────────────────────────────────────────────

    def _walk(
        self, seeds: Sequence[ReachedNote]
    ) -> tuple[tuple[ReachedNote, ...], int, ReachStopReason]:
        """One bounded, ring-by-ring expansion driven by the shipped scheduler.

        The frontier holds exactly the notes that are still *expandable*: a note
        already at the hop ceiling, or reached after the note cap, is recorded
        but never becomes an obligation, and sets ``truncated``. So the frontier
        emptying means the graph ran out — which is what lets ``fixpoint`` and
        ``budget_exhausted`` be told apart rather than conflated.

        Within one ring the obligations are taken in the frontier's own order
        (gain-descending, then shallower-first, then by id), and the first
        arrival at a note wins — so the recorded route is the strongest one and
        the whole walk is a pure function of the fixture."""
        budget = self.budget
        frontier = InquiryFrontier()
        reached: dict[str, ReachedNote] = {}
        truncated = False
        for seed in seeds:
            if seed.note_id in reached:
                continue
            if len(reached) >= budget.max_notes:
                truncated = True
                continue
            reached[seed.note_id] = seed
            frontier.add(_obligation(seed, budget.max_hops))
        stopped: StopDecision | None = None
        rings = 0

        def propose(_previous: Revision) -> Revision | None:
            nonlocal truncated, stopped, rings
            decision = voi_stop_decision(frontier, lambda_cost=budget.lambda_cost)
            if decision.should_stop:
                stopped = decision
                return None
            for obligation in frontier.open():
                frontier.resolve(obligation.obligation_id)
                if len(reached) >= budget.max_notes:
                    truncated = True
                    continue
                parent = reached[_note_id_of(obligation)]
                seed_weight = reached[parent.seed_note_id].weight
                for neighbour in self.expander.expand_links(parent.note_id, hops=1):
                    if neighbour.note_id in reached:
                        continue
                    hops = parent.hops + neighbour.hops
                    if hops > budget.max_hops:
                        truncated = True
                        continue
                    if len(reached) >= budget.max_notes:
                        truncated = True
                        break
                    record = ReachedNote(
                        note_id=neighbour.note_id,
                        hops=hops,
                        via="link",
                        path=parent.path + (neighbour.note_id,),
                        weight=seed_weight / (1 + hops),
                    )
                    reached[record.note_id] = record
                    if hops < budget.max_hops:
                        frontier.add(_obligation(record, budget.max_hops))
                    else:
                        # At the ceiling: recorded, never expanded. Whether it
                        # had further links is UNKNOWN — we did not look — so the
                        # reach must report truncation rather than a fixpoint.
                        truncated = True
            rings += 1
            return Revision(
                revision_id=f"reach:hop{rings}",
                route_signature=f"reach:hop{rings}",
                deficit=frontier.deficit(),
            )

        loop = run_bounded_inquiry(
            frontier, propose=propose, policy=budget.loop_policy()
        )
        notes = tuple(
            sorted(reached.values(), key=lambda n: (n.hops, -n.weight, n.note_id))
        )
        return notes, rings, _stop_reason(loop.outcome, stopped, truncated=truncated)


def _obligation(note: ReachedNote, max_hops: int) -> EpistemicObligation:
    """One frontier obligation: expanding this note's neighbourhood.

    Gain is the note's distance-discounted weight, so the ``λ`` comparison is a
    pure function of the fixture; ``priority`` prefers the shallower ring when
    two notes carry the same gain, keeping the walk breadth-first."""
    return EpistemicObligation(
        obligation_id=f"reach:{note.note_id}",
        question=f"expand the authored links of {note.note_id}",
        expected_information_gain=note.weight,
        priority=max_hops - note.hops,
    )


def _note_id_of(obligation: EpistemicObligation) -> str:
    return obligation.obligation_id.split(":", 1)[1]


def _stop_reason(
    outcome: str, stopped: StopDecision | None, *, truncated: bool
) -> ReachStopReason:
    """Map the scheduler's outcome and the VOI decision onto one recorded reason.

    A truncation dominates: if any frontier node was left unexpanded because a
    ceiling fired, the reach did not exhaust its graph and must not report that
    it did — a caller that reads ``fixpoint`` off a budget stop would treat an
    absent bridge note as an absent link."""
    if truncated:
        return "budget_exhausted"
    if stopped is not None and stopped.reason is not None:
        return stopped.reason
    if outcome == "complete":
        return "fixpoint"
    return "budget_exhausted"


__all__ = [
    "AMBIGUOUS_SEED_WEIGHT",
    "DEFAULT_LAMBDA_COST",
    "DEFAULT_MAX_HOPS",
    "DEFAULT_MAX_NOTES",
    "DEFAULT_MAX_RERETRIEVALS",
    "DEFAULT_SEED_K",
    "HARD_MAX_HOPS",
    "BudgetError",
    "HopBudget",
    "LinkExpansionBackend",
    "MappingLinkBackend",
    "MappingSimilarityBackend",
    "MissingHop",
    "ReachResult",
    "ReachStopReason",
    "ReachVia",
    "ReachedNote",
    "SeededReach",
    "SimilarityBackend",
]
