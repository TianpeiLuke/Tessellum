"""Read-oriented Database wrapper around the SQLite index.

Typed query helpers for the most common access patterns. Held deliberately
lean for v0.0.12 — six methods covering the substrate-level queries the
retrieval layer (Wave 6) and Composer's ``applies_to_files_query``
resolution (Composer Wave 2+) will need first.

Specialized queries (folgezettel trail traversal, orphan detection, graph
PPR) layer in v0.0.13+ once the schema gains the supporting tables.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class NoteRow:
    """One row in the ``notes`` table, with JSON columns parsed."""

    note_id: str
    note_name: str
    note_location: str
    note_category: str | None
    note_second_category: str | None
    note_status: str | None
    note_creation_date: str | None
    note_update_date: str | None
    file_path: str
    file_size_bytes: int | None
    tags: tuple[str, ...]
    keywords: tuple[str, ...]
    topics: tuple[str, ...]
    language: str | None
    building_block: str | None
    folgezettel: str | None
    folgezettel_parent: str | None
    indexed_at: str | None
    last_indexed_mtime: float | None


@dataclass(frozen=True)
class LinkRow:
    """One row in the ``note_links`` table."""

    link_id: int
    source_note_id: str
    target_note_id: str
    link_context: str | None
    link_type: str | None
    created_at: str | None


class Database:
    """Lightweight wrapper around the indexed SQLite DB.

    Use as a context manager OR call ``close()`` explicitly. Methods are
    read-oriented; callers needing to mutate rows should rebuild via
    :func:`tessellum.indexer.build`.

    Example::

        with Database("data/tessellum.db") as db:
            for note in db.notes_by_building_block("concept"):
                print(note.note_name)
    """

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path)
        if not self.db_path.is_file():
            raise FileNotFoundError(
                f"index database not found at {self.db_path}. "
                f"Run `tessellum index build` first."
            )
        self._conn = sqlite3.connect(str(self.db_path))
        self._conn.row_factory = sqlite3.Row

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()

    def close(self) -> None:
        self._conn.close()

    # ── Notes queries ─────────────────────────────────────────────────────

    def all_notes(self) -> list[NoteRow]:
        rows = self._conn.execute("SELECT * FROM notes ORDER BY note_id")
        return [_row_to_note(r) for r in rows]

    def note_by_id(self, note_id: str) -> NoteRow | None:
        row = self._conn.execute(
            "SELECT * FROM notes WHERE note_id = ?", (note_id,)
        ).fetchone()
        return _row_to_note(row) if row else None

    def notes_by_building_block(self, building_block: str) -> list[NoteRow]:
        rows = self._conn.execute(
            "SELECT * FROM notes WHERE building_block = ? ORDER BY note_id",
            (building_block,),
        )
        return [_row_to_note(r) for r in rows]

    def notes_by_category(self, category: str) -> list[NoteRow]:
        """Notes by PARA bucket (tags[0])."""
        rows = self._conn.execute(
            "SELECT * FROM notes WHERE note_category = ? ORDER BY note_id",
            (category,),
        )
        return [_row_to_note(r) for r in rows]

    def notes_by_second_category(self, second_category: str) -> list[NoteRow]:
        """Notes by tags[1] (open vocabulary: terminology, skill, how_to, etc.)."""
        rows = self._conn.execute(
            "SELECT * FROM notes WHERE note_second_category = ? ORDER BY note_id",
            (second_category,),
        )
        return [_row_to_note(r) for r in rows]

    def notes_by_folgezettel_root(self, root_fz: str) -> list[NoteRow]:
        """All notes whose ``folgezettel`` starts with ``root_fz`` (trail subset).

        E.g. ``notes_by_folgezettel_root("7")`` returns every note in trail 7
        (root 7 plus 7a, 7a1, 7a1a, ...). Match is by string-prefix; the
        compiler's full topological sort lives in v0.0.13+ as a dedicated
        ``folgezettel_trails`` table.
        """
        rows = self._conn.execute(
            "SELECT * FROM notes WHERE folgezettel LIKE ? ORDER BY folgezettel",
            (f"{root_fz}%",),
        )
        return [_row_to_note(r) for r in rows]

    # ── Link queries ─────────────────────────────────────────────────────

    def links_from(self, note_id: str) -> list[LinkRow]:
        """Outbound links from a note (note_id -> targets)."""
        rows = self._conn.execute(
            "SELECT * FROM note_links WHERE source_note_id = ? ORDER BY target_note_id",
            (note_id,),
        )
        return [_row_to_link(r) for r in rows]

    def links_to(self, note_id: str) -> list[LinkRow]:
        """Inbound links to a note (sources -> note_id)."""
        rows = self._conn.execute(
            "SELECT * FROM note_links WHERE target_note_id = ? ORDER BY source_note_id",
            (note_id,),
        )
        return [_row_to_link(r) for r in rows]

    # ── Aggregate stats ──────────────────────────────────────────────────

    def note_count(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) AS n FROM notes").fetchone()
        return int(row["n"]) if row else 0

    def link_count(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) AS n FROM note_links").fetchone()
        return int(row["n"]) if row else 0


# ── Row converters ────────────────────────────────────────────────────────


def _parse_json_list(raw: str | None) -> tuple[str, ...]:
    if raw is None:
        return ()
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return ()
    if not isinstance(data, list):
        return ()
    return tuple(str(x) for x in data)


def _row_to_note(row: sqlite3.Row) -> NoteRow:
    return NoteRow(
        note_id=row["note_id"],
        note_name=row["note_name"],
        note_location=row["note_location"],
        note_category=row["note_category"],
        note_second_category=row["note_second_category"],
        note_status=row["note_status"],
        note_creation_date=row["note_creation_date"],
        note_update_date=row["note_update_date"],
        file_path=row["file_path"],
        file_size_bytes=row["file_size_bytes"],
        tags=_parse_json_list(row["tags"]),
        keywords=_parse_json_list(row["keywords"]),
        topics=_parse_json_list(row["topics"]),
        language=row["language"],
        building_block=row["building_block"],
        folgezettel=row["folgezettel"],
        folgezettel_parent=row["folgezettel_parent"],
        indexed_at=row["indexed_at"],
        last_indexed_mtime=row["last_indexed_mtime"],
    )


def _row_to_link(row: sqlite3.Row) -> LinkRow:
    return LinkRow(
        link_id=row["link_id"],
        source_note_id=row["source_note_id"],
        target_note_id=row["target_note_id"],
        link_context=row["link_context"],
        link_type=row["link_type"],
        created_at=row["created_at"],
    )
