"""Typed change proposals + a snapshot-pinned merge/canonicalize/hash core.

Phase **P0** of "Dynamic Digestion as a Snapshot-Pinned Knowledge
Transaction". This module is the typed, deterministic replacement for the
untyped last-writer-wins fold at :func:`digestion._collect_structured`
(``merged.update(r.materialized.structured)``): instead of arbitrary
top-level keys clobbering each other by arrival order, a *set* of typed,
proposer-identified :class:`ChangeProposal` objects is folded by **effect
footprint** into a canonical, order-independent result — or an explicit,
declared conflict.

Action items realized here (all four are pure — no clock, no randomness,
no I/O anywhere in this module):

* **A0.2** — A ``frozen`` pydantic-v2 :class:`ChangeProposal`
  ``{proposer, target_revision_hash, effect, evidence}`` over a closed,
  discriminated :data:`Effect` union of seven concrete effect models
  (``add_note`` | ``update_note`` | ``merge_notes`` | ``drop_note`` |
  ``reroute`` | ``add_reference`` | ``add_navigation``). The style mirrors
  :class:`tessellum.composer.loader.PipelineStep`
  (``ConfigDict(frozen=True, extra="forbid")`` + ``tuple[...]`` immutable
  collections + ``Literal`` discriminators). Effects are *closed* so they
  use ``extra="forbid"`` (unlike ``PipelineStep``'s ``extra="allow"``).

* **A0.3** — :func:`merge_proposals`, a three-tier typed merge keyed by
  effect footprint:

    - **Tier 1 (CRDT commute).** Disjoint footprints join commutatively.
    - **Tier 2 (grow-only / dedup).** Grow-only effects (references,
      navigation) set-union; byte-identical effects on the same semantic
      key dedup to one.
    - **Tier 3 (reject-on-overlap).** Divergent effects on the same key,
      or a structural write-token claimed by two distinct effect keys,
      raise an *explicit* :class:`MergeConflict` — never a silent drop.

* **A0.4** — :func:`canonical_json_bytes`, a canonical serialization with
  sorted keys, UTF-8, no insignificant whitespace, ``ensure_ascii=False``,
  and a **float ban** that raises :class:`FloatInCanonicalPayloadError` if
  any float reaches the hashed payload (see the JCS scope note below).

* **A0.5** — :func:`plan_revision_hash`, a *content* revision id =
  ``sha256`` over the canonical serialization of the accepted effect set.
  This is a NEW value in a SEPARATE identity domain from the shipped
  ``scheduler.plan_hash`` (``sha256(skill_bytes + b"\\0" + version)`` =
  *program-capability* identity). ``plan_revision_hash`` is
  *accepted-semantic-intent* identity. This module does not import
  ``scheduler``, so the two domains cannot accidentally couple.

Canonicalization scope (JCS honesty — read before trusting cross-tool):

    This is JCS-compatible for float-free payloads only. Full RFC 8785
    (JCS) additionally mandates ECMAScript Number canonicalization (the
    shortest round-tripping decimal for IEEE-754 doubles); we deliberately
    do NOT implement that. Instead we BAN floats from the hashed payload
    (raise FloatInCanonicalPayloadError), which sidesteps the
    number-canonicalization problem entirely — all our identity fields are
    str/int/bool/None. Two further, documented deviations from strict JCS:
    (a) json.dumps sort_keys orders keys by Unicode code point, whereas
    JCS orders by UTF-16 code unit — these differ only for non-BMP
    (astral) key strings, and every dict key in our payloads is an ASCII
    field name, so it never bites; (b) we NFC-normalize strings, which
    strict JCS does not, a deliberate strengthening for cross-process
    determinism. Guarantee: intra-CPython, cross-process byte-identity for
    logically-identical float-free payloads.

Order-independence proof sketch (why the hash is a function of the SET):
grouping by :func:`effect_key`, the per-group dedup, and the write-token
overlap map are all *set*-keyed; representatives use ``min(content_hash)``;
the final ``accepted_effects`` tuple and ``conflicts`` tuple are each
sorted by a total order (``effect_content_hash`` / ``(region, proposals)``)
that does not depend on arrival order. Therefore :class:`MergeResult` —
and in particular ``plan_revision_hash`` — is a pure function of the
proposal *set*, not its ordering.
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from dataclasses import dataclass
from typing import Annotated, Any, Iterable, Literal, Union

from pydantic import BaseModel, ConfigDict, Field

# ── A0.2 — frozen effect union + ChangeProposal ────────────────────────────


class _Effect(BaseModel):
    """Common base for every concrete effect — closed and immutable.

    ``frozen=True`` blocks attribute reassignment; ``extra="forbid"``
    rejects unknown fields (effects are a *closed* set, unlike
    :class:`~tessellum.composer.loader.PipelineStep` which is
    ``extra="allow"``). ``tuple[...]`` fields keep instances deeply
    immutable, mirroring the loader's idiom.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")


class AddNote(_Effect):
    """Create a new note at ``target_path`` with body hashing to
    ``content_hash``."""

    kind: Literal["add_note"] = "add_note"
    note_id: str
    target_path: str
    content_hash: str


class UpdateNote(_Effect):
    """Rewrite an existing note's body. ``preimage_hash`` (optional) pins
    the body the update was computed against for three-way reasoning."""

    kind: Literal["update_note"] = "update_note"
    note_id: str
    target_path: str
    content_hash: str
    preimage_hash: str | None = None


class MergeNotes(_Effect):
    """Fold ``sources`` into ``dest`` (dest body hashes to
    ``content_hash``)."""

    kind: Literal["merge_notes"] = "merge_notes"
    sources: tuple[str, ...]
    dest: str
    content_hash: str


class DropNote(_Effect):
    """Delete a note."""

    kind: Literal["drop_note"] = "drop_note"
    note_id: str


class Reroute(_Effect):
    """Repoint an edge from ``edge_src`` off ``edge_dst_old`` onto
    ``edge_dst_new``."""

    kind: Literal["reroute"] = "reroute"
    edge_src: str
    edge_dst_old: str
    edge_dst_new: str


class AddReference(_Effect):
    """Add one reference edge ``src -> dst`` of type ``ref_type``.

    Grow-only: adding the same reference twice is idempotent."""

    kind: Literal["add_reference"] = "add_reference"
    src: str
    dst: str
    ref_type: str


class AddNavigation(_Effect):
    """Register ``note_id`` under an ``entry_point``. Grow-only."""

    kind: Literal["add_navigation"] = "add_navigation"
    note_id: str
    entry_point: str


# Pydantic v2 discriminated union — validation dispatches on ``kind``.
Effect = Annotated[
    Union[
        AddNote,
        UpdateNote,
        MergeNotes,
        DropNote,
        Reroute,
        AddReference,
        AddNavigation,
    ],
    Field(discriminator="kind"),
]

EFFECT_KINDS = frozenset(
    {
        "add_note",
        "update_note",
        "merge_notes",
        "drop_note",
        "reroute",
        "add_reference",
        "add_navigation",
    }
)
"""Every valid effect ``kind`` discriminator."""

GROW_ONLY_KINDS = frozenset({"add_reference", "add_navigation"})
"""Effect kinds whose footprints are element-unique grow-only tokens — they
CRDT-join by set-union and can never structurally conflict with each other."""


class ChangeProposal(BaseModel):
    """One proposer's typed intent against a pinned parent revision.

    Attributes:
        proposer: Stable id of the agent/process that authored this.
        target_revision_hash: The ``plan_revision_hash`` this proposal was
            computed against (the snapshot pin). A proposal whose pin does
            not match the merge parent is *stale* and fenced out (see
            :func:`merge_proposals`).
        effect: The typed :data:`Effect` (discriminated on ``kind``).
        evidence: Free-form provenance (citations, rationale). Excluded
            from :func:`effect_key` and :func:`plan_revision_hash`; included
            in :func:`content_hash` for provenance + conflict tie-break.

    ``frozen=True`` blocks attribute reassignment. Because ``effect`` (a
    nested frozen model) and ``evidence`` (a plain dict) coexist, we never
    call ``hash(proposal)`` — identity is :func:`content_hash` over the
    canonical bytes, not ``__hash__``.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    proposer: str
    target_revision_hash: str
    effect: Effect
    evidence: dict[str, Any] = Field(default_factory=dict)


# ── Footprint key derivation ───────────────────────────────────────────────

# Region-token grammar. The unit-separator ``\x1f`` avoids delimiter
# ambiguity (ids may contain ``:`` or ``/`` but not the control char).
_US = "\x1f"


def _node_token(note_id: str) -> str:
    return f"node:{note_id}"


def _path_token(path: str) -> str:
    return f"path:{path}"


def _edge_token(src: str, dst: str, ref_type: str) -> str:
    return f"edge:{src}{_US}{dst}{_US}{ref_type}"


def _reroute_edge_token(src: str, dst: str) -> str:
    # A reroute edge is identified by (src, dst) — its "type" is implicit.
    return f"edge:{src}{_US}{dst}"


def _nav_token(entry_point: str, note_id: str) -> str:
    return f"nav:{entry_point}{_US}{note_id}"


@dataclass(frozen=True)
class Footprint:
    """The regions an effect reads and writes.

    Derived *only* from the effect's declared fields (no graph, no I/O), so
    it is fully deterministic. A conservative transitive ``closure()``
    over-approximation is future work (P4), not P0.
    """

    reads: frozenset[str] = frozenset()
    writes: frozenset[str] = frozenset()


def effect_footprint(e: Effect) -> Footprint:
    """Return the :class:`Footprint` an effect claims — pure, field-only.

    - ``add_note``      → writes {node, path}
    - ``update_note``   → writes {node}; reads {node}
    - ``merge_notes``   → writes {dest node} ∪ {source nodes}; reads same
    - ``drop_note``     → writes {node}
    - ``reroute``       → writes {edge:src->old, edge:src->new}; reads {node:src}
    - ``add_reference`` → writes {single edge token} (grow-only)
    - ``add_navigation``→ writes {single nav token} (grow-only)
    """
    if isinstance(e, AddNote):
        return Footprint(
            writes=frozenset({_node_token(e.note_id), _path_token(e.target_path)})
        )
    if isinstance(e, UpdateNote):
        node = _node_token(e.note_id)
        return Footprint(reads=frozenset({node}), writes=frozenset({node}))
    if isinstance(e, MergeNotes):
        nodes = {_node_token(e.dest)} | {_node_token(s) for s in e.sources}
        frozen_nodes = frozenset(nodes)
        return Footprint(reads=frozen_nodes, writes=frozen_nodes)
    if isinstance(e, DropNote):
        return Footprint(writes=frozenset({_node_token(e.note_id)}))
    if isinstance(e, Reroute):
        return Footprint(
            reads=frozenset({_node_token(e.edge_src)}),
            writes=frozenset(
                {
                    _reroute_edge_token(e.edge_src, e.edge_dst_old),
                    _reroute_edge_token(e.edge_src, e.edge_dst_new),
                }
            ),
        )
    if isinstance(e, AddReference):
        return Footprint(writes=frozenset({_edge_token(e.src, e.dst, e.ref_type)}))
    if isinstance(e, AddNavigation):
        return Footprint(writes=frozenset({_nav_token(e.entry_point, e.note_id)}))
    raise TypeError(f"unknown effect type: {type(e).__name__}")  # defensive


def effect_key(e: Effect) -> tuple:
    """Semantic identity of an effect for dedup / conflict grouping.

    EVIDENCE- and proposer-EXCLUDED (two proposals with the same effect but
    different evidence share an ``effect_key``). This is the grouping key
    for tier-2/tier-3a: divergent bodies under one key are a conflict.
    """
    if isinstance(e, AddNote):
        return ("add_note", e.note_id)
    if isinstance(e, UpdateNote):
        return ("update_note", e.note_id)
    if isinstance(e, MergeNotes):
        return ("merge_notes", tuple(sorted(e.sources)), e.dest)
    if isinstance(e, DropNote):
        return ("drop_note", e.note_id)
    if isinstance(e, Reroute):
        return ("reroute", e.edge_src, e.edge_dst_old)
    if isinstance(e, AddReference):
        return ("add_reference", e.src, e.dst, e.ref_type)
    if isinstance(e, AddNavigation):
        return ("add_navigation", e.note_id, e.entry_point)
    raise TypeError(f"unknown effect type: {type(e).__name__}")  # defensive


def is_grow_only(e: Effect) -> bool:
    """``True`` iff ``e`` is a grow-only (set-union / idempotent) effect."""
    return e.kind in GROW_ONLY_KINDS


def _effect_payload(e: Effect) -> dict:
    """The JSON-mode dump of an effect (the hashed representation)."""
    return e.model_dump(mode="json")


def effect_content_hash(e: Effect) -> str:
    """Hash the effect's body ONLY (proposer/evidence excluded).

    This is the canonical ordering key for the accepted-effect set and the
    representative for grow-only dedup — identical effects hash identically
    regardless of who proposed them."""
    return _sha256(canonical_json_bytes(_effect_payload(e)))


def content_hash(p: ChangeProposal) -> str:
    """Hash the WHOLE proposal (proposer + evidence + effect).

    Used for provenance and as the conflict tie-break representative, so
    two proposals differing only in evidence get distinct content hashes."""
    return _sha256(canonical_json_bytes(p.model_dump(mode="json")))


def _sha256(b: bytes) -> str:
    """Hex sha256 of ``b`` (copy of ``planning._sha256`` for isolation)."""
    return hashlib.sha256(b).hexdigest()


# ── A0.4 — canonical serialization + float ban ─────────────────────────────


class FloatInCanonicalPayloadError(TypeError):
    """A float reached the hashed payload — banned (see JCS scope note)."""


class ProposalConflictError(ValueError):
    """Raised by :func:`merge_or_raise` when a merge yields conflicts.

    Attributes:
        conflicts: The tuple of :class:`MergeConflict` records that blocked
            the merge (a canonical, order-independent set).
    """

    def __init__(self, conflicts: tuple["MergeConflict", ...]) -> None:
        self.conflicts = conflicts
        super().__init__(
            f"{len(conflicts)} unmergeable proposal conflict(s): "
            + ", ".join(f"{c.kind}@{c.region}" for c in conflicts)
        )


def _canonicalize(obj: Any) -> Any:
    """Recursive pre-walk that fails closed on non-canonical types.

    - ``dict`` → every key must be ``str`` (else ``TypeError``); recurse
      values.
    - ``list`` / ``tuple`` → list of recursed items.
    - ``str`` → NFC-normalized (idempotent; closes the Unicode-form hazard).
    - ``bool`` → passthrough (checked BEFORE int, since ``bool`` ⊂ ``int``).
    - ``int`` / ``None`` → passthrough.
    - ``float`` → raise :class:`FloatInCanonicalPayloadError`.
    - anything else → ``TypeError`` (fail closed — no ``default=str``
      coercion inside the hashed payload, unlike ``scheduler._stable_hash``).
    """
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for k, v in obj.items():
            if not isinstance(k, str):
                raise TypeError(
                    f"canonical payload dict key must be str, got "
                    f"{type(k).__name__}: {k!r}"
                )
            out[unicodedata.normalize("NFC", k)] = _canonicalize(v)
        return out
    if isinstance(obj, (list, tuple)):
        return [_canonicalize(x) for x in obj]
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    if isinstance(obj, bool):  # MUST precede int — bool is an int subclass.
        return obj
    if isinstance(obj, float):
        raise FloatInCanonicalPayloadError(
            f"floats are banned from the canonical payload: {obj!r}"
        )
    if isinstance(obj, int) or obj is None:
        return obj
    raise TypeError(
        f"non-canonicalizable type in hashed payload: {type(obj).__name__}"
    )


def canonical_json_bytes(obj: Any) -> bytes:
    """Serialize ``obj`` to canonical UTF-8 bytes (see module JCS note).

    Sorted keys, no insignificant whitespace (``separators=(",", ":")``),
    ``ensure_ascii=False`` (raw UTF-8, not ``\\uXXXX``). Floats raise; every
    string is NFC-normalized first for cross-process byte-identity.
    """
    norm = _canonicalize(obj)
    return json.dumps(
        norm, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")


# ── A0.3 / A0.5 — three-tier merge + separate content hash ─────────────────


@dataclass(frozen=True)
class MergeConflict:
    """One declared, explicit merge conflict (never a silent drop).

    Attributes:
        region: The contested region token (``key:...`` for a same-key
            divergence, or the write-token for a structural overlap).
        proposals: The sorted pair of the two representative content hashes
            (``effect_content_hash`` values) that collide.
        kind: ``"same_key_divergent"`` (two different bodies on one
            :func:`effect_key`) or ``"write_overlap"`` (one write token
            claimed by two distinct effect keys).
    """

    region: str
    proposals: tuple[str, str]
    kind: Literal["same_key_divergent", "write_overlap"]


@dataclass(frozen=True)
class MergeResult:
    """The pure result of folding a proposal set against a parent revision.

    Attributes:
        parent_revision_hash: The revision the merge was computed against.
        accepted_effects: The canonical, content-sorted tuple of accepted
            effects (empty when there are conflicts).
        conflicts: The canonical tuple of :class:`MergeConflict` records
            (empty on a clean merge).
        plan_revision_hash: The new revision id over ``accepted_effects``,
            or ``None`` iff ``conflicts`` is non-empty (reject-on-overlap
            mints NO revision).
        stale_dropped: Sorted content hashes of proposals fenced out because
            their ``target_revision_hash`` did not match the parent.
    """

    parent_revision_hash: str
    accepted_effects: tuple[Effect, ...]
    conflicts: tuple[MergeConflict, ...]
    plan_revision_hash: str | None
    stale_dropped: tuple[str, ...]


def plan_revision_hash(
    parent_revision_hash: str, effects: Iterable[Effect]
) -> str:
    """A0.5 — content revision id over the accepted effect SET.

    ``sha256`` over the canonical serialization of
    ``{"parent": parent_revision_hash, "effects": [<content-sorted effect
    dumps>]}``. Serializes EFFECTS ONLY (proposer/evidence excluded), so it
    is order-independent AND proposer-independent. This is a NEW value in a
    SEPARATE identity domain from ``scheduler.plan_hash`` (program identity)
    — do not conflate the two.
    """
    ordered = sorted(effects, key=effect_content_hash)
    payload = {
        "parent": parent_revision_hash,
        "effects": [_effect_payload(e) for e in ordered],
    }
    return _sha256(canonical_json_bytes(payload))


def merge_proposals(
    parent_revision_hash: str, proposals: Iterable[ChangeProposal]
) -> MergeResult:
    """A0.3 — the typed replacement for ``digestion``'s LWW fold.

    Pure and order-independent. Three tiers:

    0. **Stale fence.** Drop any proposal whose ``target_revision_hash`` !=
       ``parent_revision_hash`` (mirrors the manifest commit fence). Their
       content hashes surface in ``stale_dropped``; they affect nothing.
    1. **Group by** :func:`effect_key`. Per group, compute the distinct
       effect bodies (keyed by :func:`effect_content_hash`).

       - **Tier 2** (grow-only join / identical dedup): a grow-only group,
         or a group with exactly one distinct body, contributes that single
         canonical effect to ``accepted``.
       - **Tier 3a** (same-key divergent): a non-grow-only group with ≥2
         distinct bodies is a ``same_key_divergent`` conflict.
    2. **Tier 1 / Tier 3b** (footprint overlap across DISTINCT effect keys):
       build a write-token → {(effect_key, representative)} map over every
       accepted effect. Any write token claimed by ≥2 distinct effect keys
       is a ``write_overlap`` conflict (e.g. ``update_note X`` vs
       ``merge_notes {X,Y}→Z`` both write ``node:X``). Disjoint footprints
       simply commute. Grow-only tokens are element-unique, so distinct
       grow-only keys never share one.
    3. **Conflicts?** Return them sorted by ``(region, proposals)`` with
       ``accepted_effects=()`` and ``plan_revision_hash=None``.
    4. **Clean?** Sort ``accepted`` by ``effect_content_hash``, mint
       ``plan_revision_hash``, return.
    """
    proposals = list(proposals)

    # 0. Stale fence.
    admitted: list[ChangeProposal] = []
    stale: list[str] = []
    for p in proposals:
        if p.target_revision_hash == parent_revision_hash:
            admitted.append(p)
        else:
            stale.append(content_hash(p))
    stale_dropped = tuple(sorted(stale))

    # 1. Group by effect_key (order-independent).
    groups: dict[tuple, list[ChangeProposal]] = {}
    for p in admitted:
        groups.setdefault(effect_key(p.effect), []).append(p)

    accepted: list[Effect] = []
    conflicts: list[MergeConflict] = []

    for key, members in groups.items():
        # distinct effect bodies within the group, keyed by content hash.
        distinct: dict[str, Effect] = {}
        for p in members:
            distinct[effect_content_hash(p.effect)] = p.effect
        grow_only = is_grow_only(members[0].effect)
        if grow_only or len(distinct) == 1:
            # Tier 2: grow-only union collapses to one canonical element
            # (identical by construction), or an identical-dedup group has
            # a single distinct body. Pick the min-hash representative for
            # determinism (all grow-only bodies in a group are equal).
            rep_hash = min(distinct)
            accepted.append(distinct[rep_hash])
        else:
            # Tier 3a: same effect_key, divergent bodies → explicit conflict.
            pair = tuple(sorted(distinct.keys())[:2])
            conflicts.append(
                MergeConflict(
                    region=f"key:{key}",
                    proposals=(pair[0], pair[1]),
                    kind="same_key_divergent",
                )
            )

    # 2. Footprint overlap across DISTINCT accepted effect_keys (tier-3b).
    # writes_map: write token → {(effect_key, effect_content_hash)}.
    writes_map: dict[str, set[tuple[tuple, str]]] = {}
    for e in accepted:
        ek = effect_key(e)
        ech = effect_content_hash(e)
        for token in effect_footprint(e).writes:
            writes_map.setdefault(token, set()).add((ek, ech))
    for token, claimants in writes_map.items():
        distinct_keys = {ek for ek, _ in claimants}
        if len(distinct_keys) >= 2:
            reps = sorted(ech for _, ech in claimants)
            conflicts.append(
                MergeConflict(
                    region=token,
                    proposals=(reps[0], reps[1]),
                    kind="write_overlap",
                )
            )

    # 3. Any conflict ⇒ reject-on-overlap: no accepted set, no revision.
    if conflicts:
        conflicts_sorted = tuple(
            sorted(conflicts, key=lambda c: (c.region, c.proposals))
        )
        return MergeResult(
            parent_revision_hash=parent_revision_hash,
            accepted_effects=(),
            conflicts=conflicts_sorted,
            plan_revision_hash=None,
            stale_dropped=stale_dropped,
        )

    # 4. Clean merge — canonical accepted set + minted revision.
    accepted_sorted = tuple(sorted(accepted, key=effect_content_hash))
    prh = plan_revision_hash(parent_revision_hash, accepted_sorted)
    return MergeResult(
        parent_revision_hash=parent_revision_hash,
        accepted_effects=accepted_sorted,
        conflicts=(),
        plan_revision_hash=prh,
        stale_dropped=stale_dropped,
    )


def merge_or_raise(
    parent_revision_hash: str, proposals: Iterable[ChangeProposal]
) -> MergeResult:
    """:func:`merge_proposals`, but raise :class:`ProposalConflictError` on
    any conflict instead of returning a conflicted :class:`MergeResult`.

    Gives the "raise a declared conflict" form the gate-to-P1 acceptance
    names; a clean merge returns the :class:`MergeResult` unchanged.
    """
    r = merge_proposals(parent_revision_hash, proposals)
    if r.conflicts:
        raise ProposalConflictError(r.conflicts)
    return r


# ── Ingestion seam (P1 wiring — NOT the default P0 digestion flow) ─────────


def collect_proposals(run: Any) -> list[ChangeProposal]:
    """Extract typed :class:`ChangeProposal` objects from a run's results.

    A convenience seam for P1's durable-intent wiring — it is NOT called by
    the shipped P0 digestion path (:func:`digestion._collect_structured`
    stays byte-identical). Iterates ``run.step_results`` with the same guard
    as ``digestion`` (``r.error is None`` and ``structured`` is a dict), and
    for each result reads an optional ``structured["change_proposals"]``
    list, validating each entry via :meth:`ChangeProposal.model_validate`.

    Returns ``[]`` when no result carries typed proposals — so plain-dict
    skills are entirely untouched.
    """
    out: list[ChangeProposal] = []
    for r in run.step_results:
        if r.error is not None:
            continue
        structured = getattr(r.materialized, "structured", None)
        if not isinstance(structured, dict):
            continue
        raw = structured.get("change_proposals")
        if not isinstance(raw, list):
            continue
        for x in raw:
            out.append(ChangeProposal.model_validate(x))
    return out


__all__ = [
    # A0.2 — effect union + proposal
    "AddNote",
    "UpdateNote",
    "MergeNotes",
    "DropNote",
    "Reroute",
    "AddReference",
    "AddNavigation",
    "Effect",
    "EFFECT_KINDS",
    "GROW_ONLY_KINDS",
    "ChangeProposal",
    # Footprint + keys
    "Footprint",
    "effect_footprint",
    "effect_key",
    "is_grow_only",
    "effect_content_hash",
    "content_hash",
    # A0.4 — canonicalization + errors
    "canonical_json_bytes",
    "FloatInCanonicalPayloadError",
    "ProposalConflictError",
    # A0.3 / A0.5 — merge + hash
    "MergeConflict",
    "MergeResult",
    "plan_revision_hash",
    "merge_proposals",
    "merge_or_raise",
    # Ingestion seam
    "collect_proposals",
]
