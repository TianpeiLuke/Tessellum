"""tessellum.composer.overlay_index — read-through index over ``base ⊕ delta``.

P3 (A3.1/A3.2) of the dynamic-digestion plan "Dynamic Digestion as a
Snapshot-Pinned Knowledge Transaction". The P2 :class:`~tessellum.composer.overlay.OverlayWriter`
stages *files*; this module answers *queries* over the staged transaction so
gates, dedup, backlink, and ghost-resolution checks see the same
read-your-writes view the promotion will publish — WITHOUT touching the base
index.

Why not ``base UNION delta``:

- A plain union RETAINS stale base rows under an update or delete. An update to
  a base note must SHADOW the base row (the delta row wins, not both); a delete
  must TOMBSTONE it (the base row disappears from every query). A naive union
  does neither and silently double-counts or resurrects deleted notes.
- Ghost/broken-link resolution must be RECOMPUTED over the merged state: a link
  whose target this transaction deletes becomes a fresh ghost; a link that was
  a ghost in the base becomes resolved when this transaction creates its target
  (including inbound backlinks from as-yet-unwritten notes, which are absent
  from the base ``note_links`` — b2).

So this is an explicit overlay with three delta classes — **added** (create),
**shadowed** (update: tombstone-base + add-delta), **tombstoned** (delete) — and
a deterministic merge, not a SQL union. All reads are pure over an immutable
snapshot of the delta plus the (read-only) base ``Database``. Determinism: every
listing is sorted; no clock/random.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from tessellum.indexer.db import Database, LinkRow, NoteRow


@dataclass
class DeltaState:
    """The staged effects of one knowledge transaction, layered over a base.

    - ``added``: new/updated note rows keyed by ``note_id`` (a create, or the
      post-image of an update). An update ALSO tombstones the base id if the
      ``note_id`` (path) changes; a same-path update just shadows via ``added``.
    - ``tombstoned``: ``note_id`` values removed from the effective view
      (deletes, and the old id of a rename/merge source).
    - ``links``: staged ``note_links`` rows (outbound links of new notes AND
      inbound backlinks from unwritten notes — absent from the base index).
    - ``removed_links``: (source, target) pairs the transaction retracts.
    """

    added: dict[str, NoteRow] = field(default_factory=dict)
    tombstoned: set[str] = field(default_factory=set)
    links: list[LinkRow] = field(default_factory=list)
    removed_links: set[tuple[str, str]] = field(default_factory=set)


class OverlayIndex:
    """A read-through view of ``base ⊕ delta`` (P3).

    Mirrors the read surface of :class:`tessellum.indexer.db.Database`
    (``note_by_id`` / ``all_notes`` / ``links_from`` / ``links_to`` /
    ``note_count`` / ``link_count``) so gates and dedup can run against the
    staged transaction unchanged, plus ghost-resolution helpers. Never mutates
    the base. The base ``Database`` is used read-only; all overlay state lives
    in an immutable-by-convention :class:`DeltaState` the caller supplies via
    the staging methods.
    """

    def __init__(self, base: Database, delta: DeltaState | None = None) -> None:
        self._base = base
        self._delta = delta if delta is not None else DeltaState()

    # ── staging (returns the mutated delta; deterministic, no I/O) ──────────

    def stage_add(self, note: NoteRow) -> None:
        """Stage a created (or post-image-of-updated) note. If the id was
        tombstoned earlier in this transaction, the add un-tombstones it (a
        create-after-delete resolves to the new content)."""
        self._delta.added[note.note_id] = note
        self._delta.tombstoned.discard(note.note_id)

    def stage_update(self, old_note_id: str, new_note: NoteRow) -> None:
        """Stage an update. Same-path update shadows via ``added``; a path
        change (rename) tombstones the old id and adds the new one."""
        if old_note_id != new_note.note_id:
            self._delta.tombstoned.add(old_note_id)
            self._delta.added.pop(old_note_id, None)
        self.stage_add(new_note)

    def stage_delete(self, note_id: str) -> None:
        """Tombstone a note. It disappears from every effective query; its own
        OUTBOUND base links vanish (a deleted note authors nothing — handled in
        :meth:`_effective_links` by dropping links whose source is tombstoned);
        and any surviving link pointing AT it becomes a fresh ghost."""
        self._delta.tombstoned.add(note_id)
        self._delta.added.pop(note_id, None)

    def stage_link(self, link: LinkRow) -> None:
        """Stage an edge. If the edge was unlinked earlier in this transaction,
        re-staging it un-retracts it (read-your-writes — mirrors how
        :meth:`stage_add` un-tombstones a re-created note)."""
        self._delta.removed_links.discard(
            (link.source_note_id, link.target_note_id)
        )
        self._delta.links.append(link)

    def stage_unlink(self, source_note_id: str, target_note_id: str) -> None:
        """Retract a specific edge (base or staged) from the effective view."""
        self._delta.removed_links.add((source_note_id, target_note_id))

    # ── read-through queries (base ⊕ delta) ─────────────────────────────────

    def note_by_id(self, note_id: str) -> NoteRow | None:
        if note_id in self._delta.tombstoned and note_id not in self._delta.added:
            return None
        if note_id in self._delta.added:
            return self._delta.added[note_id]
        return self._base.note_by_id(note_id)

    def exists(self, note_id: str) -> bool:
        return self.note_by_id(note_id) is not None

    def all_notes(self) -> list[NoteRow]:
        merged: dict[str, NoteRow] = {}
        for row in self._base.all_notes():
            merged[row.note_id] = row
        # deltas shadow the base; tombstones remove.
        merged.update(self._delta.added)
        for dead in self._delta.tombstoned:
            if dead not in self._delta.added:
                merged.pop(dead, None)
        return [merged[k] for k in sorted(merged)]

    def note_count(self) -> int:
        return len(self.all_notes())

    def all_links(self) -> list[LinkRow]:
        """Effective ``base ⊕ delta`` edges, deduped by ``(source, target)``.

        Rules (NOT a naive union — mirrors the notes merge):

        - A base link is kept only if its SOURCE is neither tombstoned nor
          RE-AUTHORED. A re-authored note (any id in ``added`` — a create, a
          create-after-delete, or a same-path update) DECLARES its own edges
          via staged links, exactly as a re-index would re-parse them; it does
          NOT inherit its pre-edit base outbound edges (which may no longer be
          in its content). This is what a real rebuild does.
        - A staged link is kept unless explicitly retracted via
          :meth:`stage_unlink`.
        - Base and staged copies of the SAME ``(source, target)`` collapse to
          one (published ``note_links`` enforces ``UNIQUE(source, target)``).

        Deterministic (sorted)."""
        by_key: dict[tuple[str, str], LinkRow] = {}
        # Base links: source must survive tombstoning AND must not be a
        # re-authored note (which supersedes its base edges with staged ones).
        for link in self._base.all_links():
            src = link.source_note_id
            if src in self._delta.tombstoned or src in self._delta.added:
                continue
            key = (src, link.target_note_id)
            if key in self._delta.removed_links:
                continue
            by_key.setdefault(key, link)
        # Staged links: a deleted (tombstoned-and-not-readded) source authors
        # nothing; otherwise the staged edge is authoritative.
        for link in self._delta.links:
            src = link.source_note_id
            if src in self._delta.tombstoned and src not in self._delta.added:
                continue
            key = (src, link.target_note_id)
            if key in self._delta.removed_links:
                continue
            by_key.setdefault(key, link)
        return [by_key[k] for k in sorted(by_key)]

    def link_count(self) -> int:
        return len(self.all_links())

    def links_from(self, note_id: str) -> list[LinkRow]:
        return [l for l in self.all_links() if l.source_note_id == note_id]

    def links_to(self, note_id: str) -> list[LinkRow]:
        return [l for l in self.all_links() if l.target_note_id == note_id]

    # ── ghost / broken-link resolution over the merged state ─────────────────

    def ghost_links(self) -> list[LinkRow]:
        """Links whose TARGET does not exist in the effective ``base ⊕ delta``
        view — recomputed, not read from a base diagnostic table.

        Catches both directions the plan calls out (b2): a base link whose
        target this transaction TOMBSTONED becomes a ghost; a staged link
        pointing at a not-yet-existing target is a ghost until its note is
        staged. Deterministic (sorted)."""
        ghosts = [
            link for link in self.all_links() if not self.exists(link.target_note_id)
        ]
        return sorted(ghosts, key=lambda l: (l.source_note_id, l.target_note_id))

    def resolves_ghost(self, target_note_id: str) -> bool:
        """True if this transaction CREATES ``target_note_id`` and some link in
        the effective view points at it — i.e. the staged note satisfies a
        dangling reference.

        NOTE on the base index: the shipped indexer does NOT retain broken
        links (they are dropped at build time), so a "base ghost" only exists
        as a link the transaction itself surfaces — either a staged inbound
        backlink from an unwritten note (b2) or a base link whose original
        target this transaction renamed/tombstoned. This checks the effective
        ``base ⊕ delta`` link set, which covers both."""
        if target_note_id not in self._delta.added:
            return False
        if self._base.note_by_id(target_note_id) is not None:
            return False  # already existed in the base — nothing to resolve
        return any(l.target_note_id == target_note_id for l in self.all_links())

    @property
    def delta(self) -> DeltaState:
        return self._delta


__all__ = ["OverlayIndex", "DeltaState"]
