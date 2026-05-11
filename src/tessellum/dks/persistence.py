"""DKS warrant persistence — Phase 5 v0.0.45.

Two surfaces:

- :class:`WarrantRegistry`: typed wrapper holding the *current* warrant
  set. DKS reads it at the start of each cycle and writes new
  revisions at the end. The registry has no opinion about where the
  warrants come from — callers feed it via ``add()``, ``supersede()``,
  or by loading from a vault directory via
  :func:`load_warrants_from_vault`.

- :class:`WarrantHistory`: append-only JSONL log at
  ``runs/dks/warrant_history.jsonl``. Each line is one
  :class:`WarrantChange` event with a UTC timestamp; readable in
  insertion order via ``all()`` / ``tail()``. The history is *log*,
  not *state* — the current warrant set lives in the registry; the
  history records how the registry got there.

Neither class mutates the file substrate. They produce JSON-line
records; ``tessellum dks`` writes them to ``runs/dks/``. The actual
warrant *files* (``procedure_*.md`` / ``concept_*.md``) are written by
the DKS Composer skill's step-7 materialiser, separately.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator

from tessellum.dks.core import DKSWarrant, WarrantChange


# ── WarrantRegistry ─────────────────────────────────────────────────────────


@dataclass
class _RegisteredWarrant:
    """One entry in the registry — pairs a warrant body with its FZ id."""

    folgezettel: str
    warrant: DKSWarrant


class WarrantRegistry:
    """In-memory current warrant set, keyed by Folgezettel id.

    The registry is a thin wrapper: a list of (FZ, DKSWarrant) pairs
    with ``add()`` / ``supersede()`` / ``snapshot()`` / ``__contains__``
    / ``__iter__`` / ``__len__``. ``supersede(old_fz, new_fz, warrant)``
    keeps the old entry in the *audit history* (via ``WarrantHistory``)
    but removes it from the *active set*. Lookups by FZ are O(1) via a
    lazy index.

    The registry is intentionally simple — DKS Phase 5 ships the
    *mechanism*; learned-warrant-quality scoring + dependency tracking
    are deferred to v0.2+ per the plan.
    """

    def __init__(
        self,
        warrants: Iterable[tuple[str, DKSWarrant]] = (),
    ) -> None:
        self._entries: list[_RegisteredWarrant] = []
        self._index: dict[str, int] = {}
        for fz, w in warrants:
            self.add(fz, w)

    def add(self, folgezettel: str, warrant: DKSWarrant) -> None:
        """Add a new warrant to the active set.

        Raises:
            ValueError: if a warrant with this FZ is already registered.
                Use :meth:`supersede` to replace.
        """
        if folgezettel in self._index:
            raise ValueError(
                f"FZ {folgezettel!r} already registered; use supersede() to replace"
            )
        self._index[folgezettel] = len(self._entries)
        self._entries.append(_RegisteredWarrant(folgezettel, warrant))

    def supersede(
        self,
        old_folgezettel: str,
        new_folgezettel: str,
        new_warrant: DKSWarrant,
    ) -> None:
        """Replace an existing warrant with a revised one.

        The old entry is removed from the active set; the new entry
        is added. If ``old_folgezettel`` is not in the registry the
        new entry is still added — callers may pass an FZ from a
        prior session that the in-memory registry never saw.
        """
        if old_folgezettel in self._index:
            idx = self._index.pop(old_folgezettel)
            # Rebuild list + index, dropping the displaced entry. Done
            # cleanly rather than tombstoning so iteration is simple.
            self._entries = [e for i, e in enumerate(self._entries) if i != idx]
            self._index = {e.folgezettel: i for i, e in enumerate(self._entries)}
        self.add(new_folgezettel, new_warrant)

    def snapshot(self) -> tuple[DKSWarrant, ...]:
        """Materialise the current set as a tuple (for ``DKSRunner.run``)."""
        return tuple(e.warrant for e in self._entries)

    def snapshot_with_fz(self) -> tuple[tuple[str, DKSWarrant], ...]:
        """Same as :meth:`snapshot` but each entry is paired with its FZ id."""
        return tuple((e.folgezettel, e.warrant) for e in self._entries)

    def __contains__(self, folgezettel: object) -> bool:
        return isinstance(folgezettel, str) and folgezettel in self._index

    def __iter__(self) -> Iterator[tuple[str, DKSWarrant]]:
        for e in self._entries:
            yield e.folgezettel, e.warrant

    def __len__(self) -> int:
        return len(self._entries)


# ── WarrantHistory ──────────────────────────────────────────────────────────


@dataclass(frozen=True)
class HistoryEntry:
    """One line of the warrant_history.jsonl log.

    ``change`` is the original :class:`WarrantChange` from the DKS
    cycle; ``timestamp`` is a UTC ISO-8601 stamp recorded at
    persistence time (i.e. when :meth:`WarrantHistory.record_change`
    fires, not when the cycle ran).
    """

    timestamp: str
    change: WarrantChange


class WarrantHistory:
    """Append-only JSONL log of warrant revisions.

    Each ``WarrantChange`` from a DKS cycle becomes one line in
    ``<path>``. The log is human- and tool-readable, replayable, and
    survives across sessions. Default path:
    ``runs/dks/warrant_history.jsonl`` — placed there by the
    ``tessellum dks`` CLI when ``--no-trace`` is not set.

    Reading API: :meth:`all` returns every entry in insertion order;
    :meth:`tail` returns the most recent N.
    """

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    def record_change(self, change: WarrantChange) -> HistoryEntry:
        """Append one change as a new JSONL line. Returns the entry."""
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        entry = HistoryEntry(timestamp=timestamp, change=change)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(_serialise_entry(entry)) + "\n")
        return entry

    def record_changes(
        self, changes: Iterable[WarrantChange]
    ) -> list[HistoryEntry]:
        """Append a batch of changes; returns the entries written."""
        out: list[HistoryEntry] = []
        for c in changes:
            out.append(self.record_change(c))
        return out

    def all(self) -> list[HistoryEntry]:
        """Read every line in the log. Empty list if the file is absent."""
        if not self.path.is_file():
            return []
        entries: list[HistoryEntry] = []
        with self.path.open("r", encoding="utf-8") as fh:
            for line in fh:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    entries.append(_parse_entry(json.loads(stripped)))
                except (json.JSONDecodeError, KeyError, TypeError):
                    # Tolerant — a malformed line is skipped, not fatal.
                    continue
        return entries

    def tail(self, n: int = 10) -> list[HistoryEntry]:
        """Read the most recent ``n`` entries."""
        if n <= 0:
            return []
        return self.all()[-n:]


def _serialise_entry(entry: HistoryEntry) -> dict:
    change = entry.change
    return {
        "timestamp": entry.timestamp,
        "cycle_id": change.cycle_id,
        "kind": change.kind,
        "revision_fz": change.revision_fz,
        "superseded_fz": change.superseded_fz,
        "warrant": (
            None
            if change.warrant is None
            else {
                "claim": change.warrant.claim,
                "data": change.warrant.data,
                "warrant": change.warrant.warrant,
                "backing": change.warrant.backing,
                "qualifier": change.warrant.qualifier,
                "rebuttal": change.warrant.rebuttal,
            }
        ),
    }


def _parse_entry(payload: dict) -> HistoryEntry:
    w = payload.get("warrant")
    warrant = (
        None
        if w is None
        else DKSWarrant(
            claim=str(w.get("claim", "")),
            data=str(w.get("data", "")),
            warrant=str(w.get("warrant", "")),
            backing=str(w.get("backing", "")),
            qualifier=str(w.get("qualifier", "")),
            rebuttal=str(w.get("rebuttal", "")),
        )
    )
    return HistoryEntry(
        timestamp=str(payload["timestamp"]),
        change=WarrantChange(
            cycle_id=str(payload["cycle_id"]),
            kind=payload["kind"],
            warrant=warrant,
            revision_fz=payload.get("revision_fz"),
            superseded_fz=payload.get("superseded_fz"),
        ),
    )


# ── Vault loader ────────────────────────────────────────────────────────────


def load_warrants_from_vault(
    vault_path: Path | str,
) -> WarrantRegistry:
    """Load DKS-tagged warrants from a vault directory.

    Walks ``<vault>/resources/skills/procedure_*.md`` and
    ``<vault>/resources/term_dictionary/concept_*.md``, returning a
    :class:`WarrantRegistry` containing one entry per note that:

    - has ``building_block`` of ``procedure`` or ``concept``, AND
    - has ``"dks"`` somewhere in its ``tags`` list, AND
    - has a non-empty ``folgezettel`` field.

    The DKS skill's step 7 materialises revised warrants with
    ``tags[2]=dks``, so this filter picks up exactly the warrants
    DKS itself produced (not arbitrary procedures or terms).

    Notes whose frontmatter cannot be parsed are silently skipped.
    The function never raises on a bad note; a bad vault returns an
    empty registry rather than crashing the cycle.
    """
    from tessellum.format.parser import parse_note

    root = Path(vault_path)
    candidates: list[Path] = []
    for sub, prefix in (
        ("resources/skills", "procedure_"),
        ("resources/term_dictionary", "concept_"),
    ):
        d = root / sub
        if d.is_dir():
            candidates.extend(sorted(d.glob(f"{prefix}*.md")))

    registry = WarrantRegistry()
    for path in candidates:
        try:
            note = parse_note(path)
        except Exception:
            continue
        fm = note.frontmatter
        if fm.get("building_block") not in ("procedure", "concept"):
            continue
        tags = fm.get("tags") or []
        if not isinstance(tags, list) or "dks" not in tags:
            continue
        fz = fm.get("folgezettel")
        if not isinstance(fz, str) or not fz.strip():
            continue
        registry.add(
            fz.strip(),
            DKSWarrant(
                claim=str(fm.get("claim", "")),
                data=str(fm.get("data", "")),
                warrant=str(fm.get("warrant", "")),
                backing=str(fm.get("backing", "")),
                qualifier=str(fm.get("qualifier", "")),
                rebuttal=str(fm.get("rebuttal", "")),
            ),
        )
    return registry


__all__ = [
    "WarrantRegistry",
    "WarrantHistory",
    "HistoryEntry",
    "load_warrants_from_vault",
]
