"""tessellum.dks.resolve_entity — the tiered mention→entity resolver (step 1).

P1 of the query-time DKS plan. Anchoring a query is *matching*, not
understanding, so this whole module is model-free apart from the dense tier's
vector backend: three tiers, cheapest first.

1. **exact alias** — :func:`~tessellum.dks.entity_registry.norm` of the mention
   against the registry's reliable-kinds-only
   :class:`~tessellum.dks.entity_registry.ResolutionIndex`. Type-preferring;
   authored exclusions break collisions.
2. **full text** — a lexical backend, restricted to registered entities and
   type-preferring, relaxing the type constraint only if nothing typed matched.
3. **dense** — a vector backend, same restriction and same relaxation.

Two properties are load-bearing and both are tested:

- **Ambiguity abstains.** An exact match onto two entities returns a
  :class:`Resolution` with ``entity_id=None``, ``method="ambiguous"`` and the
  candidate set — never a ranked pick. Resolution is what everything downstream
  is anchored on, so a wrong anchor is worse than no anchor. Prominence
  tie-breaking exists (the reference implementation's behaviour) but is
  **opt-in**: pass ``ambiguity="prominence"`` with a prominence map.
- **Exclusions apply at every tier**, not only the exact one. An authored
  exclusion says "this surface is NOT that entity"; a lexical or dense hit is no
  more entitled to override it than an alias is.

The search backends are a :class:`EntitySearchBackend` Protocol, so tests run on
a deterministic in-memory backend (:class:`MappingSearchBackend`) and production
reads through the existing read-only retrieval port
(:class:`RetrievalSearchBackend` over
:class:`~tessellum.dks.retrieval_client.RetrievalClient`) — never the index
directly.

Pure (the Dependency Rule): no runtime import, no disk, no vault write. The
registry arrives already loaded, through the
:class:`~tessellum.dks.entity_registry.RegistrySource` port.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Mapping, Protocol, Sequence

from tessellum.dks.entity_registry import (
    ANY_OBJECT_TYPE,
    EntityCandidateRef,
    EntityRegistry,
    ResolutionIndex,
    norm,
)
from tessellum.dks.retrieval_client import RetrievalClient

ResolutionMethod = Literal[
    "exact_alias",              # unique reliable-alias match
    "exact_alias_disambiguated",  # >1 alias match, broken by opt-in prominence
    "full_text",                # lexical backend
    "dense",                    # vector backend
    "ambiguous",                # candidates returned; NO entity chosen
    "unresolved",               # no tier produced a candidate
]

EXACT_SCORE: float = 1.0
"""Score for a unique exact reliable-alias match — the only certainty here."""

DISAMBIGUATED_SCORE: float = 0.9
"""Score for an opt-in prominence-broken exact match (a ranked pick, not a fact)."""

FULL_TEXT_TYPED_SCORE: float = 0.7
"""Score for a lexical hit that also matched the requested entity type."""

FULL_TEXT_RELAXED_SCORE: float = 0.6
"""Score for a lexical hit found only after relaxing the type constraint."""

DEFAULT_SEARCH_LIMIT: int = 50
"""How many backend hits to scan per tier before giving up."""


@dataclass(frozen=True)
class EntitySearchHit:
    """One ranked hit from a search backend, best-first.

    ``ref_id`` is whatever id the backend ranks — a note id for the retrieval
    port, which is also the spine's ``entity_id``, so no mapping table is
    needed."""

    ref_id: str
    score: float


class EntitySearchBackend(Protocol):
    """Port for one search tier. Ranked, best-first, read-only.

    Two shipped implementations mirror the confidence-model pattern:
    :class:`MappingSearchBackend` (deterministic, for tests and for callers with
    no index) and :class:`RetrievalSearchBackend` (the real hybrid index, read
    through the DKS retrieval port)."""

    def __call__(self, mention: str, *, limit: int) -> Sequence[EntitySearchHit]: ...


@dataclass(frozen=True)
class MappingSearchBackend:
    """Deterministic backend over a fixed ``mention → hits`` mapping.

    Keyed by :func:`~tessellum.dks.entity_registry.norm` of the mention so a
    test does not have to reproduce the caller's casing. Returns hits in the
    order given, truncated to ``limit`` — no ranking of its own, so a test
    controls the tier's input exactly."""

    hits: Mapping[str, tuple[EntitySearchHit, ...]] = field(default_factory=dict)

    def __call__(self, mention: str, *, limit: int) -> Sequence[EntitySearchHit]:
        return self.hits.get(norm(mention), ())[:limit]


@dataclass(frozen=True)
class RetrievalSearchBackend:
    """Adapter over the read-only DKS retrieval port.

    Wraps :meth:`~tessellum.dks.retrieval_client.RetrievalClient.search`, whose
    hybrid (BM25 + dense) fusion can back either the lexical or the dense tier —
    wiring it to both makes tier 3 redundant rather than wrong. The client has no
    ``index``/``update``/``delete`` surface, so resolution cannot mutate the
    index through this seam."""

    client: RetrievalClient

    def __call__(self, mention: str, *, limit: int) -> Sequence[EntitySearchHit]:
        return tuple(
            EntitySearchHit(ref_id=hit.note_id, score=hit.score)
            for hit in self.client.search(mention, k=limit)
        )


@dataclass(frozen=True)
class Resolution:
    """What one mention resolved to — or why it did not.

    ``entity_id is None`` covers two very different outcomes and the ``method``
    distinguishes them: ``"unresolved"`` (nothing matched) and ``"ambiguous"``
    (several things matched and the resolver refused to pick). Only the second
    carries a non-empty ``candidates``; a caller that wants to widen the query
    reads it, and a caller that wants to abstain has everything it needs to say
    why."""

    mention: str
    entity_id: str | None
    canonical_name: str | None
    entity_type: str | None
    method: ResolutionMethod
    score: float
    candidates: tuple[EntityCandidateRef, ...] = ()
    requested_type: str | None = None

    @property
    def resolved(self) -> bool:
        """Whether a single canonical entity was chosen."""
        return self.entity_id is not None

    @property
    def is_ambiguous(self) -> bool:
        """Whether the resolver refused to choose between candidates."""
        return self.method == "ambiguous"

    def __str__(self) -> str:
        if self.entity_id is None:
            suffix = f" ({len(self.candidates)} candidates)" if self.candidates else ""
            return f"{self.mention!r} -> {self.method.upper()}{suffix}"
        return (
            f"{self.mention!r} -> {self.entity_id} "
            f"({self.canonical_name} :: {self.entity_type}) "
            f"[{self.method} {self.score:.3f}]"
        )


class EntityResolver:
    """Resolve a mention to a canonical typed entity, or abstain.

    Args:
        registry: The loaded registry. Its
            :meth:`~tessellum.dks.entity_registry.EntityRegistry.resolution_index`
            is reliable-kinds-only by construction, so a keyword alias can never
            key an exact match here.
        full_text: Optional lexical backend (tier 2). ``None`` skips the tier.
        dense: Optional vector backend (tier 3). ``None`` skips the tier.
        ambiguity: ``"abstain"`` (default) returns candidates on an ambiguous
            exact match; ``"prominence"`` opts in to the reference
            implementation's tie-break and needs ``prominence``.
        prominence: ``entity_id`` → prominence score, consulted only under
            ``ambiguity="prominence"``. A missing entity scores 0.
        search_limit: Hits scanned per search tier.
    """

    def __init__(
        self,
        registry: EntityRegistry,
        *,
        full_text: EntitySearchBackend | None = None,
        dense: EntitySearchBackend | None = None,
        ambiguity: Literal["abstain", "prominence"] = "abstain",
        prominence: Mapping[str, float] | None = None,
        search_limit: int = DEFAULT_SEARCH_LIMIT,
    ) -> None:
        self.registry = registry
        self.index: ResolutionIndex = registry.resolution_index()
        self.full_text = full_text
        self.dense = dense
        self.ambiguity = ambiguity
        self.prominence: Mapping[str, float] = prominence or {}
        self.search_limit = search_limit
        self._types = registry.entity_types()

    # ── tiers ───────────────────────────────────────────────────────────────

    def _exact(self, alias_norm: str, entity_type: str | None) -> Resolution | None:
        """Tier 1 — reliable exact alias, exclusion-aware and type-preferring."""
        refs = self.index.candidates_for(alias_norm)
        if not refs:
            return None
        same_type = tuple(r for r in refs if entity_type and r.entity_type == entity_type)
        pool = same_type or refs
        unique = sorted({r.entity_id for r in pool})
        if len(unique) == 1:
            return self._hit(unique[0], "exact_alias", EXACT_SCORE, entity_type)
        candidates = tuple(sorted(pool, key=lambda r: r.entity_id))
        if self.ambiguity == "prominence":
            best = max(unique, key=lambda eid: (self.prominence.get(eid, 0.0), eid))
            return self._hit(
                best,
                "exact_alias_disambiguated",
                DISAMBIGUATED_SCORE,
                entity_type,
                candidates=candidates,
            )
        # Default: refuse to guess. The anchor everything downstream depends on
        # is either unique or it is a candidate set.
        return Resolution(
            mention="",
            entity_id=None,
            canonical_name=None,
            entity_type=None,
            method="ambiguous",
            score=0.0,
            candidates=candidates,
            requested_type=entity_type,
        )

    def _search(
        self,
        backend: EntitySearchBackend,
        mention: str,
        alias_norm: str,
        entity_type: str | None,
        *,
        method: ResolutionMethod,
        typed_score: float | None,
        relaxed_score: float | None,
    ) -> Resolution | None:
        """One ranked search tier, restricted to registered, non-excluded entities.

        Scans best-first for a type match; falls back to the best hit of any type
        only if the typed scan found nothing. ``typed_score``/``relaxed_score``
        of ``None`` mean "use the backend's own score" (the dense tier reports a
        real similarity; a lexical rank does not)."""
        relaxed: Resolution | None = None
        for hit in backend(mention, limit=self.search_limit):
            registered_type = self._types.get(hit.ref_id)
            if registered_type is None:
                continue  # not a registered entity — a plain note, not an anchor
            if self.index.is_excluded(alias_norm, hit.ref_id):
                continue  # an authored exclusion outranks any retrieval score
            if not entity_type or registered_type == entity_type:
                score = hit.score if typed_score is None else typed_score
                return self._hit(hit.ref_id, method, score, entity_type)
            if relaxed is None:
                score = hit.score if relaxed_score is None else relaxed_score
                relaxed = self._hit(hit.ref_id, method, score, entity_type)
        return relaxed

    def _hit(
        self,
        entity_id: str,
        method: ResolutionMethod,
        score: float,
        requested_type: str | None,
        *,
        candidates: tuple[EntityCandidateRef, ...] = (),
    ) -> Resolution:
        entity = self.registry.entity(entity_id)
        return Resolution(
            mention="",
            entity_id=entity_id,
            canonical_name=entity.canonical_name if entity else None,
            entity_type=entity.entity_type if entity else None,
            method=method,
            score=score,
            candidates=candidates,
            requested_type=requested_type,
        )

    # ── the resolver ────────────────────────────────────────────────────────

    def resolve(self, mention: str, entity_type: str | None = None) -> Resolution:
        """Resolve one mention through the tiers, cheapest first.

        An ambiguous exact match short-circuits: the later tiers are *rankers*,
        and letting a ranker pick between two exact alias matches would
        reintroduce the guess tier 1 just refused."""
        alias_norm = norm(mention)
        exact = self._exact(alias_norm, entity_type)
        if exact is not None:
            return _with_mention(exact, mention)
        if self.full_text is not None:
            hit = self._search(
                self.full_text,
                mention,
                alias_norm,
                entity_type,
                method="full_text",
                typed_score=FULL_TEXT_TYPED_SCORE,
                relaxed_score=FULL_TEXT_RELAXED_SCORE,
            )
            if hit is not None:
                return _with_mention(hit, mention)
        if self.dense is not None:
            hit = self._search(
                self.dense,
                mention,
                alias_norm,
                entity_type,
                method="dense",
                typed_score=None,
                relaxed_score=None,
            )
            if hit is not None:
                return _with_mention(hit, mention)
        return Resolution(
            mention=mention,
            entity_id=None,
            canonical_name=None,
            entity_type=None,
            method="unresolved",
            score=0.0,
            requested_type=entity_type,
        )


def _with_mention(resolution: Resolution, mention: str) -> Resolution:
    """Stamp the caller's surface form onto a tier's result (tiers work on norms)."""
    return Resolution(
        mention=mention,
        entity_id=resolution.entity_id,
        canonical_name=resolution.canonical_name,
        entity_type=resolution.entity_type,
        method=resolution.method,
        score=resolution.score,
        candidates=resolution.candidates,
        requested_type=resolution.requested_type,
    )


@dataclass(frozen=True)
class TypedObjectResolver:
    """The authored seed's object resolver, wired to a real :class:`EntityResolver`.

    Implements ``entity_registry.ObjectResolver``: a relation object becomes an
    ``entity`` reference only when the match is confident (``score >=
    min_score``) AND the entity's type is the one the predicate expects.
    Otherwise the authored value is kept verbatim as a ``literal`` — which is the
    right answer for external references and for anything the registry does not
    know. The type gate is what keeps a seeded relation precise instead of
    landing on whatever entity shares a surface form."""

    resolver: EntityResolver
    min_score: float = DISAMBIGUATED_SCORE

    def __call__(
        self, value: str, expected_type: str | None
    ) -> tuple[str, Literal["entity", "literal"]]:
        if expected_type is None:
            return value, "literal"
        requested = None if expected_type == ANY_OBJECT_TYPE else expected_type
        result = self.resolver.resolve(value, requested)
        if (
            result.entity_id is not None
            and result.score >= self.min_score
            and (expected_type == ANY_OBJECT_TYPE or result.entity_type == expected_type)
        ):
            return result.entity_id, "entity"
        return value, "literal"


__all__ = [
    "DEFAULT_SEARCH_LIMIT",
    "DISAMBIGUATED_SCORE",
    "EXACT_SCORE",
    "FULL_TEXT_RELAXED_SCORE",
    "FULL_TEXT_TYPED_SCORE",
    "EntityResolver",
    "EntitySearchBackend",
    "EntitySearchHit",
    "MappingSearchBackend",
    "Resolution",
    "ResolutionMethod",
    "RetrievalSearchBackend",
    "TypedObjectResolver",
]
