"""tessellum.composer.write_closure — exact write-set + validation heuristic + partition.

P4 of the dynamic-digestion plan "Dynamic Digestion as a Snapshot-Pinned
Knowledge Transaction". This is the critical-path piece: it derives WHAT a
knowledge transaction must atomically commit (the exact ``write_set``), what it
must merely RE-CHECK (the bounded ``validation_set``), and how to split a
multi-note objective into independently-promotable capsules (``partition``).

The single most important distinction (plan guardrail 3, counter
blocking-correction 1):

    Only typed MATERIALIZATION INVARIANTS define the write set. Bounded reverse
    reachability is a VALIDATION/INVALIDATION heuristic — it may widen what we
    re-check, but it must NEVER add to or subtract from what we commit.

So the write set is a fixpoint over an explicit, typed invariant relation:

- the created/edited note itself;
- its entry-point navigation row (create/update);
- its parent-hub backlink (via ``folgezettel_parent``);
- required reverse inlinks (notes that must gain a backlink to it);
- FZ parent/child inlinks;
- the index projection.

These are ALWAYS in the write set even when the target is an entry point or a
high-degree hub — a hub cut may prune the validation fan-out but can never drop
a mandatory write. A ``boundary_witness`` proves no classified write-propagating
edge exits the set; UNKNOWN edge classes fail closed (they force the edge into
the write set or trip the witness rather than being silently ignored).

Everything here is pure: no clock, no randomness, no I/O beyond reading the
supplied (read-only) graph / overlay. Deterministic (sorted) outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from tessellum.composer.knowledge_plan import NoteIntent, NoteIntentGraph
from tessellum.retrieval.graph import DEFAULT_HUB_THRESHOLD

# Edge propagation classes. ``note_links.link_type`` is uniformly ``markdown``
# in the shipped index, so propagation is derived from structural signals
# (source category, folgezettel parent/child, reciprocity) — NOT from a stored
# link_type (b1). An edge whose class cannot be determined is UNKNOWN and fails
# closed.
EdgeClass = Literal[
    "navigation",   # entry-point membership row (a note listed in an entry point)
    "fz_parent",    # folgezettel parent/child inlink
    "backlink",     # required reverse inlink
    "reference",    # ordinary content cross-reference (does NOT propagate writes)
    "unknown",      # unclassifiable — fail closed
]

# Edge classes that PROPAGATE a write (touching the target forces the target's
# row into the write set). A plain content reference does not.
_WRITE_PROPAGATING: frozenset[str] = frozenset({"navigation", "fz_parent", "backlink"})


@dataclass(frozen=True)
class WriteEffect:
    """One mandatory write derived from a note intent by a materialization
    invariant. ``note_id`` is the vault-relative path touched; ``kind`` records
    which invariant produced it (for the boundary witness + audit)."""

    note_id: str
    kind: Literal[
        "note", "navigation", "reverse_inlink", "fz_inlink", "index",
    ]
    origin: str  # the intent note_id this write was derived from


@dataclass(frozen=True)
class WriteClosure:
    """The exact transactional write set of an accepted effect set."""

    writes: tuple[WriteEffect, ...]

    @property
    def touched_note_ids(self) -> frozenset[str]:
        return frozenset(w.note_id for w in self.writes)


@dataclass(frozen=True)
class BoundaryWitness:
    """Proof that no classified write-propagating edge exits the write set.

    ``ok`` is True iff every write-propagating edge out of a touched note lands
    on another touched note (closure holds) and no edge class is UNKNOWN.
    ``escaping`` lists ``(source, target, edge_class)`` for propagating edges
    that leave the set; ``unknown`` lists edges whose class could not be
    determined (which fail closed)."""

    ok: bool
    escaping: tuple[tuple[str, str, str], ...] = ()
    unknown: tuple[tuple[str, str], ...] = ()


@dataclass
class ClosurePolicy:
    """Tunable bounds for the VALIDATION heuristic (never the write set)."""

    hub_threshold: int = DEFAULT_HUB_THRESHOLD
    validation_depth: int = 2
    # Spill trip: validation set larger than this fraction of the corpus (or
    # this absolute count) → spill (reject / widen to a coarse epoch), never
    # silent truncation. Calibrated by scripts/measure_closure_blastradius.py.
    spill_fraction: float = 0.10
    spill_abs: int | None = None


# ── exact write closure (typed invariants only) ─────────────────────────────


def write_closure(
    intents: tuple[NoteIntent, ...] | NoteIntentGraph,
    *,
    entry_point_of: dict[str, str] | None = None,
) -> WriteClosure:
    """Compute the EXACT write set as a fixpoint over materialization invariants.

    Args:
        intents: the accepted note intents (or a NoteIntentGraph).
        entry_point_of: optional map ``note_id -> entry_point note_id`` for the
            navigation invariant when an intent does not carry ``navigation``.

    Returns a :class:`WriteClosure`; deterministic (sorted by ``(note_id,
    kind)``). Mandatory writes are ALWAYS included — entry points and hubs are
    never pruned here (that is only a validation concern).
    """
    if isinstance(intents, NoteIntentGraph):
        intents = intents.intents
    entry_point_of = entry_point_of or {}

    writes: set[WriteEffect] = set()
    for intent in intents:
        nid = intent.note_id
        # 1. the note itself.
        writes.add(WriteEffect(nid, "note", nid))
        # 2. the index projection (every touched note re-projects into the index).
        writes.add(WriteEffect(nid, "index", nid))
        # 3. entry-point navigation rows — from the intent's declared
        #    membership OR an injected mapping. ALWAYS a write, even though the
        #    entry point is a high-degree hub.
        nav_targets = list(intent.navigation)
        if nid in entry_point_of:
            nav_targets.append(entry_point_of[nid])
        for ep in nav_targets:
            writes.add(WriteEffect(ep, "navigation", nid))
        # 4. required reverse inlinks — every note that must gain a backlink to
        #    this note is a mandatory write on THAT note. The parent-hub
        #    backlink is expressed this way: NoteIntent carries no folgezettel
        #    field, so the parent hub that must gain a child row is declared as
        #    a required_inlink (or a depends_on edge, below).
        for src in intent.required_inlinks:
            writes.add(WriteEffect(src, "reverse_inlink", nid))
        # 5. FZ parent/child dependency edges land as fz_inlink writes on the
        #    endpoint (the parent/dependency gains the reciprocal row). Outbound
        #    relevance_links live in the note's own body and are NOT writes on
        #    their targets; an undeclared reciprocal is caught (fail-closed) by
        #    boundary_witness as an escaping fz_parent/backlink edge.
        for dep in intent.depends_on:
            writes.add(WriteEffect(dep, "fz_inlink", nid))

    ordered = tuple(sorted(writes, key=lambda w: (w.note_id, w.kind, w.origin)))
    return WriteClosure(writes=ordered)


# ── edge classification (structural, not link_type) ─────────────────────────


def classify_edge(
    source_id: str,
    target_id: str,
    *,
    note_category_of: dict[str, str],
    fz_parent_of: dict[str, str],
    reciprocal: bool,
) -> EdgeClass:
    """Classify a directed edge by STRUCTURAL signals (b1) — the shipped
    ``link_type`` is uniformly ``markdown`` so it carries no propagation info.

    - an edge whose SOURCE is an entry point is ``navigation``;
    - an edge between an FZ parent and its child (either direction) is
      ``fz_parent``;
    - a reciprocated edge (both directions present) is a ``backlink``;
    - any other edge is a plain content ``reference`` (does not propagate);
    - if the source's category is unknown (absent from the maps), the class is
      ``unknown`` → fails closed.
    """
    src_cat = note_category_of.get(source_id)
    if src_cat is None:
        return "unknown"
    if src_cat == "entry_point":
        return "navigation"
    if fz_parent_of.get(source_id) == target_id or fz_parent_of.get(target_id) == source_id:
        return "fz_parent"
    if reciprocal:
        return "backlink"
    return "reference"


def boundary_witness(
    closure: WriteClosure,
    *,
    edges: list[tuple[str, str]],
    note_category_of: dict[str, str],
    fz_parent_of: dict[str, str],
    reciprocal_pairs: set[tuple[str, str]] | None = None,
) -> BoundaryWitness:
    """Prove no classified write-propagating edge exits the write set.

    ``edges`` are the directed edges incident to the touched notes (from the
    base graph ⊕ staged effects). For each edge whose SOURCE is a touched note:
    if its class propagates writes and its TARGET is not touched, the closure is
    incomplete (``escaping``). Unknown edge classes are collected and force
    ``ok=False`` (fail closed)."""
    reciprocal_pairs = reciprocal_pairs or set()
    touched = closure.touched_note_ids
    escaping: list[tuple[str, str, str]] = []
    unknown: list[tuple[str, str]] = []
    for src, tgt in edges:
        if src not in touched:
            continue
        cls = classify_edge(
            src, tgt,
            note_category_of=note_category_of,
            fz_parent_of=fz_parent_of,
            reciprocal=(src, tgt) in reciprocal_pairs or (tgt, src) in reciprocal_pairs,
        )
        if cls == "unknown":
            unknown.append((src, tgt))
            continue
        if cls in _WRITE_PROPAGATING and tgt not in touched:
            escaping.append((src, tgt, cls))
    ok = not escaping and not unknown
    return BoundaryWitness(
        ok=ok,
        escaping=tuple(sorted(escaping)),
        unknown=tuple(sorted(unknown)),
    )


# ── validation heuristic (bounded reverse reachability — NOT the write set) ──


@dataclass(frozen=True)
class ValidationResult:
    """The bounded set of notes to RE-CHECK after a transaction, plus a spill
    flag. ``spilled`` True means the fan-out exceeded the calibrated bound →
    the caller must reject or widen to a coarse epoch (never truncate)."""

    to_revalidate: frozenset[str]
    spilled: bool
    size: int
    bound: int


def validation_set(
    seed_ids: frozenset[str],
    *,
    reverse_adj: dict[str, list[str]],
    corpus_size: int,
    note_category_of: dict[str, str],
    in_degree_of: dict[str, int],
    policy: ClosurePolicy | None = None,
) -> ValidationResult:
    """Bounded depth-limited REVERSE reachability from the touched notes — the
    set of notes whose gates should be re-run because they may reference the
    changed cluster. This is a heuristic: it drops navigational entry-point
    edges and cuts expansion at hubs (``in_degree > hub_threshold``) to keep
    the fan-out small. It NEVER defines what to commit.

    Fail-closed spill: if the resulting set exceeds the calibrated bound, set
    ``spilled=True`` (caller rejects / widens); the set itself is still returned
    for diagnostics but must not be silently truncated into an "exact" scope."""
    policy = policy or ClosurePolicy()
    bound = policy.spill_abs
    if bound is None:
        bound = max(1, int(corpus_size * policy.spill_fraction))

    visited: set[str] = set()
    # BFS ring by ring up to validation_depth over reverse edges.
    frontier = set(seed_ids)
    for _depth in range(policy.validation_depth):
        nxt: set[str] = set()
        for node in frontier:
            for pred in reverse_adj.get(node, ()):  # predecessors: pred -> node
                if pred in visited or pred in seed_ids:
                    continue
                # drop navigational entry-point predecessors (an entry point
                # links to everything; it is not evidence of a real dependency).
                if note_category_of.get(pred) == "entry_point":
                    continue
                # hub cut: do not expand through a very-high-in-degree node.
                if in_degree_of.get(pred, 0) > policy.hub_threshold:
                    # include it as a leaf (it references the cluster) but do
                    # not expand its own predecessors.
                    visited.add(pred)
                    continue
                nxt.add(pred)
        visited |= nxt
        frontier = nxt
        if not frontier:
            break

    to_revalidate = frozenset(visited - set(seed_ids))
    size = len(to_revalidate)
    return ValidationResult(
        to_revalidate=to_revalidate,
        spilled=size > bound,
        size=size,
        bound=bound,
    )


# ── partition into invariant-closed capsules ────────────────────────────────


def partition_capsules(
    intents: tuple[NoteIntent, ...] | NoteIntentGraph,
    *,
    entry_point_of: dict[str, str] | None = None,
) -> list[WriteClosure]:
    """Split the accepted intents into invariant-closed capsules that can be
    promoted independently.

    Two intents belong in the SAME capsule iff their write closures OVERLAP
    (they touch a shared note — e.g. both register under one entry point, or
    one is the other's required reverse inlink). Disjoint write closures form
    separate capsules and may promote independently; a coupling invariant
    (shared navigation row / reciprocal link / merge) unions them. Deterministic:
    capsules are returned sorted by their smallest touched note_id.

    This is a union-find over the per-intent write closures keyed on shared
    touched note_ids."""
    if isinstance(intents, NoteIntentGraph):
        intents = intents.intents

    per_intent: list[tuple[str, WriteClosure]] = []
    for intent in intents:
        wc = write_closure((intent,), entry_point_of=entry_point_of)
        per_intent.append((intent.note_id, wc))

    # union-find over intent indices, joined when write closures share a note.
    parent = list(range(len(per_intent)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        parent[find(i)] = find(j)

    # map each touched note -> first intent index that touched it.
    owner: dict[str, int] = {}
    for idx, (_nid, wc) in enumerate(per_intent):
        for note_id in wc.touched_note_ids:
            if note_id in owner:
                union(idx, owner[note_id])
            else:
                owner[note_id] = idx

    groups: dict[int, list[int]] = {}
    for idx in range(len(per_intent)):
        groups.setdefault(find(idx), []).append(idx)

    capsules: list[WriteClosure] = []
    for members in groups.values():
        merged: set[WriteEffect] = set()
        for idx in members:
            merged |= set(per_intent[idx][1].writes)
        capsules.append(
            WriteClosure(
                writes=tuple(sorted(merged, key=lambda w: (w.note_id, w.kind, w.origin)))
            )
        )
    # deterministic order: by smallest touched note_id in each capsule.
    capsules.sort(key=lambda c: min(c.touched_note_ids) if c.writes else "")
    return capsules


__all__ = [
    "EdgeClass",
    "WriteEffect",
    "WriteClosure",
    "BoundaryWitness",
    "ClosurePolicy",
    "ValidationResult",
    "write_closure",
    "classify_edge",
    "boundary_witness",
    "validation_set",
    "partition_capsules",
]
