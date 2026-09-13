"""tessellum.dks.entity_registry — canonical entities, aliases, and the O(N) authored seed.

P1 of the query-time DKS plan (step 1 of the query pipeline). A query has to be
*anchored* before anything widens it: the mention the user wrote has to become a
canonical, typed entity, or the protocol has to abstain. This module holds the
data model that anchoring resolves against, plus two pure projections over it:

- **the spine** (:func:`project_spine`) — one canonical entity per
  entity-DEFINING note, with its aliases. Deterministic, model-free: the same
  notes yield byte-identical entities (see :func:`registry_content_digest`).
- **the authored relations seed** (:func:`seed_authored_relations`) — the thin
  ``origin='authored'`` projection of relation-bearing frontmatter fields into
  relation rows. It reads **one attribute per node** and is therefore O(N) in
  entities; it never enumerates entity *pairs*, which is the bound the whole
  design exists to respect. :func:`audit_authored_seed` makes that checkable.

**The measured lesson this module encodes as a constraint.** In the reference
implementation a *keyword-dump* alias source (every note's frontmatter
``keywords`` list) was folded into resolution and produced false entity links —
a note listing a generic neighbouring term resolved that term to itself. Only
``canonical`` / ``acronym`` / ``variant`` aliases are reliable enough to drive
resolution. That is not a comment here: :class:`ResolutionIndex` **refuses**
(:class:`UnreliableAliasError`) any alias offered outside
:data:`RELIABLE_ALIAS_KINDS`, so a keyword alias cannot reach the resolver even
by accident. Keyword aliases are still *retained* on the registry for lexical
and full-text use — they simply cannot key an exact match.

All pure (the Dependency Rule): no runtime import, no disk, no vault write.
Persistence is a runtime concern reached through the :class:`RegistrySource` /
:class:`RegistrySink` ports at the bottom of this module; ``dks`` only reads and
proposes rows.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Iterable, Literal, Mapping, Protocol, Sequence, runtime_checkable

# ── normalization: the one deterministic lookup key ──────────────────────────

_WHITESPACE = re.compile(r"\s+")


def norm(surface: str | None) -> str:
    """The deterministic alias lookup key: casefold + collapse whitespace.

    Every alias, mention and exclusion is keyed by this and nothing else, so a
    lookup never depends on how a caller spaced or cased a surface form."""
    return _WHITESPACE.sub(" ", (surface or "").strip()).casefold()


# ── alias kinds, and the reliability constraint ──────────────────────────────

AliasKind = Literal["canonical", "acronym", "variant", "keyword", "exclusion"]
"""How an alias was obtained. Reliability differs by kind — see below."""

RELIABLE_ALIAS_KINDS: frozenset[str] = frozenset({"canonical", "acronym", "variant"})
"""The ONLY kinds admitted to resolution (the measured lesson, encoded).

``keyword`` is deliberately absent: a frontmatter keyword list names *related*
terms as often as it names the note's own entity, and folding it into exact
resolution produced false links in the reference build. ``exclusion`` is absent
because it is a negative signal — it removes a candidate, it never supplies one.
"""

EXCLUSION_ALIAS_KIND: str = "exclusion"
"""Alias kind that BLOCKS a (alias_norm, entity_id) pair — a collision breaker."""

ANY_OBJECT_TYPE: str = "*"
"""Relation-object type meaning "accept any confident entity match"."""


class UnreliableAliasError(ValueError):
    """Raised when an alias outside :data:`RELIABLE_ALIAS_KINDS` is offered to a
    :class:`ResolutionIndex`. The point of failing loudly is that the
    keyword-dump regression was silent: nothing crashed, resolution just got
    quietly wrong. Filter with :meth:`EntityRegistry.resolution_index` instead of
    reaching for a broader alias set."""


# ── the registry data model ─────────────────────────────────────────────────


@dataclass(frozen=True)
class Entity:
    """One canonical, typed entity — the thing a mention resolves TO.

    ``entity_id`` is the defining note's id for a spine entity, so the registry
    inherits the vault's identity rather than minting a parallel one.
    ``scope`` partitions entities by provenance breadth (by convention
    ``"local"`` | ``"external"`` | ``"research"``); a caller that gates a
    predicate on locally-authored entities filters on it."""

    entity_id: str
    canonical_name: str
    entity_type: str
    note_id: str = ""
    file_path: str = ""
    folgezettel: str | None = None
    source_layer: Literal["spine", "promoted"] = "spine"
    scope: str = "local"
    content_hash: str | None = None


@dataclass(frozen=True)
class EntityAlias:
    """One surface form for an entity, tagged with HOW it was obtained.

    The kind is load-bearing, not descriptive: :data:`RELIABLE_ALIAS_KINDS`
    decides whether this alias may key a resolution."""

    entity_id: str
    alias: str
    alias_kind: AliasKind
    source: str = ""

    @property
    def alias_norm(self) -> str:
        """The deterministic lookup key for :attr:`alias`."""
        return norm(self.alias)

    @property
    def is_reliable(self) -> bool:
        """Whether this alias may drive resolution (see the class docstring)."""
        return self.alias_kind in RELIABLE_ALIAS_KINDS


@dataclass(frozen=True)
class CandidateEntity:
    """A surface form seen in the corpus that is not (yet) a canonical entity.

    The promotion queue / ghost-note bridge: ``status='linked'`` once it maps
    onto a spine entity, otherwise it stays ``'candidate'`` and is evidence that
    a note is missing. ``confidence`` is a soft frequency signal in [0, 1) —
    never a truth claim."""

    candidate_id: str
    surface_form: str
    surface_norm: str
    entity_type: str
    mention_count: int
    distinct_notes: int
    confidence: float
    scope: str = "local"
    resolved_entity_id: str | None = None
    status: Literal["candidate", "linked", "promoted", "demoted"] = "candidate"


@dataclass(frozen=True)
class EntityCandidateRef:
    """One member of an ambiguous resolution's candidate set (id + type only)."""

    entity_id: str
    entity_type: str


def candidate_id(surface_norm: str, entity_type: str) -> str:
    """Stable content id for a candidate surface — hash, never a counter."""
    return hashlib.sha256(f"{surface_norm}|{entity_type}".encode()).hexdigest()[:24]


# ── the resolution index: reliable kinds ONLY, enforced ─────────────────────


@dataclass(frozen=True)
class ResolutionIndex:
    """``alias_norm`` → candidate entities, plus the exclusion map.

    Constructed only through :meth:`build`, which **raises** on any alias whose
    kind is not reliable. That refusal is the constraint: the index is the single
    door to exact resolution, so a keyword alias cannot get in."""

    by_alias_norm: Mapping[str, tuple[EntityCandidateRef, ...]]
    exclusions: Mapping[str, frozenset[str]]

    @classmethod
    def build(
        cls,
        aliases: Iterable[EntityAlias],
        entity_types: Mapping[str, str],
    ) -> "ResolutionIndex":
        """Build the index from aliases that are ALREADY reliability-filtered.

        Args:
            aliases: Only ``canonical`` / ``acronym`` / ``variant`` (positive)
                and ``exclusion`` (negative) aliases. Anything else raises.
            entity_types: ``entity_id`` → ``entity_type``, for type preference.

        Raises:
            UnreliableAliasError: when an alias of an unreliable kind is
                offered. Use :meth:`EntityRegistry.resolution_index`, which
                filters, rather than widening the input here.
        """
        positive: dict[str, list[EntityCandidateRef]] = defaultdict(list)
        excluded: dict[str, set[str]] = defaultdict(set)
        for alias in aliases:
            if alias.alias_kind == EXCLUSION_ALIAS_KIND:
                excluded[alias.alias_norm].add(alias.entity_id)
                continue
            if not alias.is_reliable:
                raise UnreliableAliasError(
                    f"alias kind {alias.alias_kind!r} may not drive resolution "
                    f"(reliable kinds: {sorted(RELIABLE_ALIAS_KINDS)}); "
                    f"offered {alias.alias!r} for {alias.entity_id!r}"
                )
            ref = EntityCandidateRef(
                entity_id=alias.entity_id,
                entity_type=entity_types.get(alias.entity_id, ""),
            )
            if ref not in positive[alias.alias_norm]:
                positive[alias.alias_norm].append(ref)
        return cls(
            by_alias_norm={
                key: tuple(sorted(refs, key=lambda r: r.entity_id))
                for key, refs in positive.items()
            },
            exclusions={key: frozenset(ids) for key, ids in excluded.items()},
        )

    def candidates_for(self, alias_norm: str) -> tuple[EntityCandidateRef, ...]:
        """Exclusion-filtered candidates for a normalized surface form."""
        blocked = self.exclusions.get(alias_norm, frozenset())
        return tuple(
            ref for ref in self.by_alias_norm.get(alias_norm, ()) if ref.entity_id not in blocked
        )

    def is_excluded(self, alias_norm: str, entity_id: str) -> bool:
        """Whether an authored exclusion blocks this (surface, entity) pair."""
        return entity_id in self.exclusions.get(alias_norm, frozenset())


@dataclass(frozen=True)
class EntityRegistry:
    """The canonical entity set with all of its aliases and candidates.

    Holds *every* alias kind — keyword aliases stay available for lexical and
    full-text use — while :meth:`resolution_index` exposes only the reliable
    subset. That split is the whole design: retain broadly, resolve narrowly."""

    entities: tuple[Entity, ...] = ()
    aliases: tuple[EntityAlias, ...] = ()
    candidates: tuple[CandidateEntity, ...] = ()
    # id index, built once at construction. Excluded from repr/eq so the
    # registry's identity stays its content (the digest contract), and set
    # through object.__setattr__ because the dataclass is frozen.
    _by_id: dict[str, Entity] = field(
        default_factory=dict, init=False, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "_by_id", {e.entity_id: e for e in self.entities})

    def entity(self, entity_id: str) -> Entity | None:
        """Look up one entity by id; ``None`` when absent."""
        return self._by_id.get(entity_id)

    def entity_types(self) -> dict[str, str]:
        """``entity_id`` → ``entity_type`` for every registered entity."""
        return {e.entity_id: e.entity_type for e in self.entities}

    def of_type(self, entity_type: str) -> tuple[Entity, ...]:
        """Every entity of one type, in id order."""
        return tuple(e for e in self.entities if e.entity_type == entity_type)

    def resolution_index(self) -> ResolutionIndex:
        """The reliable-kinds-only index the resolver reads.

        Filters :attr:`aliases` down to :data:`RELIABLE_ALIAS_KINDS` plus
        exclusions before building, so this call can never raise
        :class:`UnreliableAliasError` however wide the registry's alias set is."""
        admissible = tuple(
            a
            for a in self.aliases
            if a.is_reliable or a.alias_kind == EXCLUSION_ALIAS_KIND
        )
        return ResolutionIndex.build(admissible, self.entity_types())


def registry_content_digest(registry: EntityRegistry) -> str:
    """Order-invariant digest of the registry's CONTENT (no timestamps).

    The determinism contract: the same notes projected twice yield the same
    digest. Build metadata lives in the store's meta table, never here, so a
    determinism diff over content stays clean."""
    entities = sorted(
        (
            e.entity_id,
            e.canonical_name,
            e.entity_type,
            e.file_path,
            e.folgezettel or "",
            e.source_layer,
            e.scope,
        )
        for e in registry.entities
    )
    aliases = sorted(
        (a.entity_id, a.alias_norm, a.alias_kind, a.source) for a in registry.aliases
    )
    candidates = sorted(
        (
            c.candidate_id,
            c.surface_norm,
            c.entity_type,
            c.mention_count,
            c.distinct_notes,
            c.resolved_entity_id or "",
            c.status,
        )
        for c in registry.candidates
    )
    digest = hashlib.sha256()
    for part in (entities, aliases, candidates):
        digest.update(repr(part).encode("utf-8"))
    return digest.hexdigest()


# ── the spine projection: one canonical entity per DEFINING note ────────────


@dataclass(frozen=True)
class NoteFacts:
    """The authored facts one note contributes — the projection's only input.

    A caller-supplied record, so this module never reads a file. ``frontmatter``
    is the note's already-parsed YAML mapping; :func:`seed_authored_relations`
    reads ONE attribute per field spec out of it and nothing else."""

    note_id: str
    note_name: str = ""
    second_category: str = ""
    keywords: tuple[str, ...] = ()
    folgezettel: str | None = None
    file_path: str = ""
    content_hash: str | None = None
    frontmatter: Mapping[str, Any] = field(default_factory=dict)


DEFAULT_DEFINING_CATEGORIES: Mapping[str, str] = {
    # note second-category (tags[1]) → registry entity_type. One canonical
    # entity per note of these categories; everything else MENTIONS entities
    # rather than defining one. Deliberately a caller-overridable default: the
    # second-category vocabulary is open, so every vault names its own.
    "terminology": "concept",
    "team": "team",
    "tool": "tool",
    "table": "table",
    "dataset": "dataset",
    "model": "model",
    "service": "service",
    "code_repo": "repository",
    "project": "project",
    "variable": "variable",
}

DEFAULT_NOISE_PREFIXES: tuple[str, ...] = ("entry_", "catalog_", "glossary_", "index_")
"""Note-name prefixes that mark a HUB, not a leaf entity."""

DEFAULT_NOISE_SUFFIXES: tuple[str, ...] = ("_index", "_overview")
"""Note-name suffixes that mark a section/overview sub-note, not an entity."""


@dataclass(frozen=True)
class SpineSpec:
    """Which notes define an entity, and which are structural noise.

    Every field is data, not code, so a vault configures the projection instead
    of forking it."""

    defining_categories: Mapping[str, str] = field(
        default_factory=lambda: dict(DEFAULT_DEFINING_CATEGORIES)
    )
    noise_prefixes: tuple[str, ...] = DEFAULT_NOISE_PREFIXES
    noise_suffixes: tuple[str, ...] = DEFAULT_NOISE_SUFFIXES
    default_scope: str = "local"

    def entity_type_for(self, second_category: str | None) -> str | None:
        """The entity type a second-category defines; ``None`` if it defines none."""
        return self.defining_categories.get((second_category or "").strip())

    def is_non_entity(self, note_name: str | None) -> bool:
        """Whether a note name is a hub / README / section sub-note.

        These carry a defining second-category but are not leaf entities;
        admitting them puts an index page into the resolution pool."""
        name = (note_name or "").strip()
        if not name or name.startswith("README"):
            return True
        return name.startswith(self.noise_prefixes) or name.endswith(self.noise_suffixes)


def project_spine(
    notes: Iterable[NoteFacts],
    *,
    spec: SpineSpec | None = None,
) -> tuple[tuple[Entity, ...], tuple[EntityAlias, ...]]:
    """Project entity-DEFINING notes into entities + aliases. Pure, model-free.

    One canonical entity per defining note; its aliases are the canonical name
    (kind ``canonical``) plus each frontmatter keyword (kind ``keyword``). The
    keyword aliases are retained for lexical use and are *structurally* barred
    from resolution — see :class:`ResolutionIndex`.

    Args:
        notes: The candidate notes. Non-defining categories and structural hubs
            are skipped.
        spec: Which categories define which entity types. Defaults to
            :class:`SpineSpec`.

    Returns:
        ``(entities, aliases)``, both sorted by id so the projection is
        deterministic regardless of input order.
    """
    spine_spec = spec or SpineSpec()
    entities: list[Entity] = []
    aliases: list[EntityAlias] = []
    for note in sorted(notes, key=lambda n: n.note_id):
        entity_type = spine_spec.entity_type_for(note.second_category)
        if entity_type is None or spine_spec.is_non_entity(note.note_name):
            continue
        canonical = note.note_name or note.note_id
        entities.append(
            Entity(
                entity_id=note.note_id,
                canonical_name=canonical,
                entity_type=entity_type,
                note_id=note.note_id,
                file_path=note.file_path or note.note_id,
                folgezettel=note.folgezettel,
                source_layer="spine",
                scope=spine_spec.default_scope,
                content_hash=note.content_hash,
            )
        )
        seen: set[tuple[str, str]] = set()
        offered: list[tuple[str, AliasKind, str]] = [(canonical, "canonical", "note_name")]
        offered.extend((kw, "keyword", "keywords") for kw in note.keywords)
        for surface, kind, source in offered:
            key = (norm(surface), kind)
            if not surface.strip() or key in seen:
                continue
            seen.add(key)
            aliases.append(
                EntityAlias(
                    entity_id=note.note_id,
                    alias=surface,
                    alias_kind=kind,
                    source=source,
                )
            )
    return tuple(entities), tuple(aliases)


# ── candidate aggregation: the promotion queue (deterministic, model-free) ───


@dataclass(frozen=True)
class MentionRecord:
    """One (note, surface, type) mention observed in the corpus.

    Supplied by the caller from whatever extraction pass produced it; this
    module only *aggregates*, so the aggregation stays deterministic even when
    the extraction upstream was not."""

    note_id: str
    surface_form: str
    entity_type: str


def aggregate_candidates(
    mentions: Iterable[MentionRecord],
    *,
    scope: str = "local",
) -> tuple[CandidateEntity, ...]:
    """Aggregate mentions into candidates by ``(surface_norm, entity_type)``.

    Deterministic: the surface form kept is the most-voted one with ties broken
    lexicographically, and rows come back in ``candidate_id`` order. Confidence
    is ``distinct/(distinct+3)`` — a frequency prior for the promotion queue,
    not a probability."""
    totals: Counter[tuple[str, str]] = Counter()
    note_sets: dict[tuple[str, str], set[str]] = defaultdict(set)
    surfaces: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for mention in mentions:
        surface = (mention.surface_form or "").strip()
        entity_type = (mention.entity_type or "").strip()
        key = (norm(surface), entity_type)
        if not key[0] or not key[1]:
            continue
        totals[key] += 1
        note_sets[key].add(mention.note_id)
        surfaces[key][surface] += 1
    rows: list[CandidateEntity] = []
    for (surface_norm, entity_type), total in totals.items():
        distinct = len(note_sets[(surface_norm, entity_type)])
        best_surface = sorted(
            surfaces[(surface_norm, entity_type)].items(), key=lambda kv: (-kv[1], kv[0])
        )[0][0]
        rows.append(
            CandidateEntity(
                candidate_id=candidate_id(surface_norm, entity_type),
                surface_form=best_surface,
                surface_norm=surface_norm,
                entity_type=entity_type,
                mention_count=total,
                distinct_notes=distinct,
                confidence=round(distinct / (distinct + 3), 3),
                scope=scope,
            )
        )
    return tuple(sorted(rows, key=lambda c: c.candidate_id))


def link_candidates(
    candidates: Iterable[CandidateEntity],
    index: ResolutionIndex,
) -> tuple[CandidateEntity, ...]:
    """Link candidates to spine entities by exact reliable alias, type-preferring.

    A candidate links only when the match is UNAMBIGUOUS — one same-type entity,
    or (absent any same-type match) one entity of any type. Anything else stays
    ``'candidate'``: the promotion queue is allowed to be incomplete, it is not
    allowed to guess."""
    linked: list[CandidateEntity] = []
    for cand in candidates:
        refs = index.candidates_for(cand.surface_norm)
        same_type = sorted({r.entity_id for r in refs if r.entity_type == cand.entity_type})
        any_type = sorted({r.entity_id for r in refs})
        resolved: str | None = None
        if len(same_type) == 1:
            resolved = same_type[0]
        elif not same_type and len(any_type) == 1:
            resolved = any_type[0]
        linked.append(
            CandidateEntity(
                candidate_id=cand.candidate_id,
                surface_form=cand.surface_form,
                surface_norm=cand.surface_norm,
                entity_type=cand.entity_type,
                mention_count=cand.mention_count,
                distinct_notes=cand.distinct_notes,
                confidence=cand.confidence,
                scope=cand.scope,
                resolved_entity_id=resolved,
                status="linked" if resolved else "candidate",
            )
        )
    return tuple(sorted(linked, key=lambda c: c.candidate_id))


# ── the authored relations seed: O(N) in entities, never O(N²) ───────────────


@dataclass(frozen=True)
class RelationFieldSpec:
    """One authored frontmatter field, and what its value means.

    ``object_type`` constrains resolution of the object: a concrete type accepts
    an entity match only of that type, :data:`ANY_OBJECT_TYPE` accepts any
    confident match, and ``None`` never resolves (the value stays a literal —
    correct for external references, URLs and people). The type gate is what
    keeps a row precise: an ``owned_by`` must land on a team, not on whatever
    entity happens to share the surface form."""

    predicate: str
    object_type: str | None = ANY_OBJECT_TYPE


DEFAULT_RELATION_FIELDS: Mapping[str, RelationFieldSpec] = {
    # Authored frontmatter field → (predicate, expected object type). Every one
    # is a single attribute read from the SUBJECT's own frontmatter — which is
    # exactly why the seed is O(N). Caller-overridable: a vault authors its own
    # relation-bearing fields.
    "owner": RelationFieldSpec("owned_by", "team"),
    "parent_note": RelationFieldSpec("part_of", ANY_OBJECT_TYPE),
    "derived_from": RelationFieldSpec("derived_from", ANY_OBJECT_TYPE),
    "inputs": RelationFieldSpec("consumes", ANY_OBJECT_TYPE),
    "implemented_by": RelationFieldSpec("implemented_by", "repository"),
    "folgezettel_parent": RelationFieldSpec("continues", None),
    "source_url": RelationFieldSpec("cites_source", None),
    "related_wiki": RelationFieldSpec("references_document", None),
}

_NULLISH: frozenset[str] = frozenset({"", "none", "null", "n/a", "na", "tbd", "unknown"})
"""Authored placeholders that assert nothing and must not become a relation."""


@dataclass(frozen=True)
class AuthoredRelation:
    """One row of the Tier-A ``relations`` cache, projected from frontmatter.

    ``origin='authored'`` by construction: this projection cannot produce any
    other origin, so a resolved (query-derived) row can never be mistaken for an
    authored fact. ``valid_from`` / ``valid_to`` carry the validity interval —
    not optional in the schema, because a role relation without one confidently
    returns a *former* holder — and stay ``None`` for an undated authored fact.
    ``evidence_note`` is always the subject's OWN note: that invariant is what
    :func:`audit_authored_seed` checks to prove no row was pair-enumerated."""

    relation_id: str
    subject_id: str
    predicate: str
    object_ref: str
    object_kind: Literal["entity", "literal"]
    evidence_note: str
    evidence_locator: str
    valid_from: str | None = None
    valid_to: str | None = None
    epistemic_status: str = "asserted"
    origin: Literal["authored"] = "authored"
    superseded_by: str | None = None
    content_hash: str | None = None


def relation_id(subject_id: str, predicate: str, object_ref: str, locator: str) -> str:
    """Stable content id for a relation row — hash, so replay is idempotent."""
    return hashlib.sha256(
        f"{subject_id}|{predicate}|{object_ref}|{locator}".encode()
    ).hexdigest()[:24]


class ObjectResolver(Protocol):
    """Port for turning an authored object VALUE into an entity id, or not.

    Injected so the seed stays deterministic and testable: the reference
    implementation :class:`LiteralObjectResolver` never resolves, and
    ``resolve_entity.TypedObjectResolver`` wires the real tiered resolver in.
    Returns ``(object_ref, kind)`` — the caller keeps the literal when the
    expected type is not confidently matched."""

    def __call__(
        self, value: str, expected_type: str | None
    ) -> tuple[str, Literal["entity", "literal"]]:
        ...


@dataclass(frozen=True)
class LiteralObjectResolver:
    """Deterministic reference resolver: every object stays a literal.

    The honest default. A seed built with this is still complete — every
    authored fact is present with its locator — it just has not attempted entity
    linkage, so nothing is silently mis-linked."""

    def __call__(
        self, value: str, expected_type: str | None
    ) -> tuple[str, Literal["entity", "literal"]]:
        return value, "literal"


def _field_values(frontmatter: Mapping[str, Any], field_name: str) -> tuple[str, ...]:
    """Normalized, deduped, non-nullish string values for ONE frontmatter field."""
    raw = frontmatter.get(field_name)
    if raw is None:
        return ()
    values = [str(v) for v in raw] if isinstance(raw, (list, tuple)) else [str(raw)]
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        cleaned = value.strip()
        key = cleaned.casefold()
        if not cleaned or key in _NULLISH or key in seen:
            continue
        seen.add(key)
        out.append(cleaned)
    return tuple(out)


def seed_authored_relations(
    nodes: Iterable[NoteFacts],
    *,
    fields: Mapping[str, RelationFieldSpec] | None = None,
    resolver: ObjectResolver | None = None,
) -> tuple[AuthoredRelation, ...]:
    """Project authored frontmatter facts into Tier-A rows. O(N) in entities.

    For each node this reads **one attribute per configured field** and emits a
    row per authored value. It never looks at a second node while handling the
    first, so no row can be a pair enumeration; the cost is
    ``O(nodes × len(fields))`` and the field set is a small constant. This is the
    design's Increment 1 and the reason it is not forbidden by the scaling
    bound: the bound rules out enumerating entity *pairs*, not reading one
    authored attribute per node.

    Args:
        nodes: The entity-defining notes (typically the spine), each carrying
            its already-parsed ``frontmatter``.
        fields: Field → :class:`RelationFieldSpec`. Defaults to
            :data:`DEFAULT_RELATION_FIELDS`.
        resolver: Optional :class:`ObjectResolver` for entity linkage. Defaults
            to :class:`LiteralObjectResolver` (everything stays a literal).

    Returns:
        Rows in ``relation_id`` order — deterministic regardless of input order.
        Emits; does NOT persist (the runtime's registry store does that).
    """
    field_specs = dict(DEFAULT_RELATION_FIELDS if fields is None else fields)
    resolve = resolver or LiteralObjectResolver()
    rows: list[AuthoredRelation] = []
    for node in sorted(nodes, key=lambda n: n.note_id):
        frontmatter = node.frontmatter or {}
        if not frontmatter:
            continue
        for field_name, spec in field_specs.items():
            values = _field_values(frontmatter, field_name)
            for ordinal, value in enumerate(values):
                if spec.object_type is None:
                    object_ref, object_kind = value, "literal"
                else:
                    object_ref, object_kind = resolve(value, spec.object_type)
                # the locator carries the ordinal so a multi-valued authored
                # field keeps one addressable row per value (still bounded by
                # THIS node's frontmatter, never by the entity count).
                locator = (
                    f"frontmatter:{field_name}"
                    if len(values) == 1
                    else f"frontmatter:{field_name}[{ordinal}]"
                )
                rows.append(
                    AuthoredRelation(
                        relation_id=relation_id(
                            node.note_id, spec.predicate, object_ref, locator
                        ),
                        subject_id=node.note_id,
                        predicate=spec.predicate,
                        object_ref=object_ref,
                        object_kind=object_kind,
                        evidence_note=node.note_id,
                        evidence_locator=locator,
                        content_hash=node.content_hash,
                    )
                )
    return tuple(sorted(rows, key=lambda r: r.relation_id))


@dataclass(frozen=True)
class SeedAudit:
    """Evidence that a seed is a per-node projection and not a pair enumeration.

    ``pair_enumerated_rows`` is the decisive number: an authored row must be
    witnessed by its own subject's note, so any row whose ``evidence_note``
    differs from its ``subject_id`` came from somewhere other than that node's
    frontmatter — which is what a pair enumeration looks like. ``row_bound`` is
    the O(N) ceiling ``subjects × fields``; a quadratic build would blow past
    it as soon as the corpus grew."""

    subject_count: int
    row_count: int
    row_bound: int
    max_rows_per_subject: int
    max_rows_per_subject_predicate: int
    pair_enumerated_rows: int
    non_authored_rows: int

    @property
    def is_linear(self) -> bool:
        """Whether the row count respects the O(N) ceiling."""
        return self.row_count <= self.row_bound


def audit_authored_seed(
    rows: Sequence[AuthoredRelation],
    *,
    field_count: int,
) -> SeedAudit:
    """Audit a seed for linearity and for zero pair-enumerated rows.

    Args:
        rows: The seed as returned by :func:`seed_authored_relations`.
        field_count: How many relation fields the seed was built with — the
            per-subject row ceiling before multi-valued fields.
    """
    per_subject: Counter[str] = Counter()
    per_subject_predicate: Counter[tuple[str, str]] = Counter()
    pair_enumerated = 0
    non_authored = 0
    for row in rows:
        per_subject[row.subject_id] += 1
        per_subject_predicate[(row.subject_id, row.predicate)] += 1
        if row.evidence_note != row.subject_id:
            pair_enumerated += 1
        if row.origin != "authored":
            non_authored += 1
    subjects = len(per_subject)
    return SeedAudit(
        subject_count=subjects,
        row_count=len(rows),
        row_bound=subjects * max(field_count, 0),
        max_rows_per_subject=max(per_subject.values(), default=0),
        max_rows_per_subject_predicate=max(per_subject_predicate.values(), default=0),
        pair_enumerated_rows=pair_enumerated,
        non_authored_rows=non_authored,
    )


# ── ports: DKS reads and proposes; the runtime stores ───────────────────────


@runtime_checkable
class RegistrySource(Protocol):
    """Read port. The runtime backs it; ``dks`` never opens a database."""

    def load_registry(self) -> EntityRegistry: ...

    def relations_for(
        self, subject_id: str, predicate: str | None = None
    ) -> tuple[AuthoredRelation, ...]: ...


@runtime_checkable
class RegistrySink(Protocol):
    """Write port for the REBUILDABLE registry projection.

    Deliberately not an append-only log: the registry and the Tier-A cache are
    projections over authored notes, so a rebuild replaces a layer wholesale and
    dropping them costs latency, never knowledge. The append-only discipline
    belongs to the claim/edge log, which is a different table with a different
    lifecycle."""

    def replace_spine(
        self, entities: Sequence[Entity], aliases: Sequence[EntityAlias]
    ) -> int: ...

    def replace_candidates(self, candidates: Sequence[CandidateEntity]) -> int: ...

    def replace_authored_relations(self, rows: Sequence[AuthoredRelation]) -> int: ...


__all__ = [
    "ANY_OBJECT_TYPE",
    "AliasKind",
    "AuthoredRelation",
    "CandidateEntity",
    "DEFAULT_DEFINING_CATEGORIES",
    "DEFAULT_NOISE_PREFIXES",
    "DEFAULT_NOISE_SUFFIXES",
    "DEFAULT_RELATION_FIELDS",
    "EXCLUSION_ALIAS_KIND",
    "Entity",
    "EntityAlias",
    "EntityCandidateRef",
    "EntityRegistry",
    "LiteralObjectResolver",
    "MentionRecord",
    "NoteFacts",
    "ObjectResolver",
    "RELIABLE_ALIAS_KINDS",
    "RegistrySink",
    "RegistrySource",
    "RelationFieldSpec",
    "ResolutionIndex",
    "SeedAudit",
    "SpineSpec",
    "UnreliableAliasError",
    "aggregate_candidates",
    "audit_authored_seed",
    "candidate_id",
    "link_candidates",
    "norm",
    "project_spine",
    "registry_content_digest",
    "relation_id",
    "seed_authored_relations",
]
