"""Metadata filtering — direct SQL queries on structured YAML fields.

The simplest retrieval layer. Doesn't need BM25, dense, hybrid, or BFS;
it just SELECTs notes matching exact-value or array-contains filters on
the structured fields populated from each note's YAML frontmatter:

  tags[0]            note_category        (PARA bucket: resource/area/...)
  tags[1]            note_second_category (open vocabulary: terminology/skill/...)
  tags[2..]          tags                 JSON array (free-form topic tags)
  keywords           keywords             JSON array
  topics             topics               JSON array
  status             note_status
  date of note       note_creation_date
  building_block     building_block
  folgezettel        folgezettel + folgezettel_parent

This is the search you reach for when you know *what kind* of note you
want, not *what content*. "Show me all concept notes about CQRS that
are still in draft" is metadata, not content. Composer's
``applies_to_files_query`` (Wave 2) will likely route through this layer
for several of its query kinds.

JSON-array fields are matched via SQLite's built-in JSON1 ``json_each``
to avoid LIKE false-positives. SQLite ships JSON1 enabled by default
since 3.38; Python's bundled SQLite is fresh enough.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MetadataHit:
    """One note matching a metadata filter.

    Slimmer than ``NoteRow`` from ``tessellum.indexer.db`` — exposes the
    fields most filters care about; callers needing the full row can
    follow up with ``Database.note_by_id(hit.note_id)``.
    """

    note_id: str
    note_name: str
    note_category: str | None
    note_second_category: str | None
    note_status: str | None
    building_block: str | None
    note_creation_date: str | None
    folgezettel: str | None


def metadata_search(
    db_path: Path | str,
    *,
    building_block: str | None = None,
    status: str | None = None,
    category: str | None = None,
    second_category: str | None = None,
    tag: str | None = None,
    keyword: str | None = None,
    topic: str | None = None,
    date_after: str | None = None,
    date_before: str | None = None,
    folgezettel_prefix: str | None = None,
    has_folgezettel: bool | None = None,
    k: int = 100,
) -> list[MetadataHit]:
    """Filter notes by structured metadata fields. All filters AND-combine.

    Args:
        building_block: Exact match on the closed BB enum
            (concept / procedure / model / argument / etc.).
        status: Exact match on the closed status enum
            (active / draft / archived / template / etc.).
        category: Exact match on ``tags[0]`` / PARA bucket
            (resource / area / project / archive / entry_point).
        second_category: Exact match on ``tags[1]``
            (terminology / skill / how_to / analysis / ...).
        tag: Any-of match — note's ``tags[]`` JSON array contains this
            value. Uses ``json_each`` for exact-value comparison.
        keyword: Any-of match on ``keywords[]`` JSON array.
        topic: Any-of match on ``topics[]`` JSON array.
        date_after: ``YYYY-MM-DD`` — note's ``date of note`` >= this.
        date_before: ``YYYY-MM-DD`` — note's ``date of note`` <= this.
        folgezettel_prefix: Notes whose ``folgezettel`` starts with this
            prefix (string-prefix match — e.g. ``"7"`` matches 7, 7a,
            7a1, 7a1a, ...).
        has_folgezettel: ``True`` returns only trail notes (FZ field
            non-null); ``False`` returns only non-trail notes; ``None``
            (default) ignores this field.
        k: Maximum number of results. Default 100 (large because
            metadata queries often return broad slices of the vault).

    Returns:
        List of ``MetadataHit``, ordered by ``note_id`` ascending
        (deterministic across runs).

    Raises:
        FileNotFoundError: ``db_path`` doesn't exist.
        sqlite3.OperationalError: ``notes`` table missing — run
            ``tessellum index build``.
    """
    db = Path(db_path)
    if not db.is_file():
        raise FileNotFoundError(
            f"index DB not found at {db}. Run `tessellum index build` first."
        )

    if k <= 0:
        return []

    where_clauses: list[str] = []
    params: list[object] = []

    if building_block is not None:
        where_clauses.append("building_block = ?")
        params.append(building_block)
    if status is not None:
        where_clauses.append("note_status = ?")
        params.append(status)
    if category is not None:
        where_clauses.append("note_category = ?")
        params.append(category)
    if second_category is not None:
        where_clauses.append("note_second_category = ?")
        params.append(second_category)
    if date_after is not None:
        where_clauses.append("note_creation_date >= ?")
        params.append(date_after)
    if date_before is not None:
        where_clauses.append("note_creation_date <= ?")
        params.append(date_before)
    if folgezettel_prefix is not None:
        where_clauses.append("folgezettel LIKE ?")
        params.append(f"{folgezettel_prefix}%")
    if has_folgezettel is True:
        where_clauses.append("folgezettel IS NOT NULL")
    elif has_folgezettel is False:
        where_clauses.append("folgezettel IS NULL")

    # JSON-array filters via json_each — avoids LIKE false-positives
    # (e.g. ``tag='cqr'`` shouldn't match ``"cqrs"``). The EXISTS subquery
    # iterates the array and matches by exact value.
    if tag is not None:
        where_clauses.append(
            "EXISTS (SELECT 1 FROM json_each(notes.tags) WHERE value = ?)"
        )
        params.append(tag)
    if keyword is not None:
        where_clauses.append(
            "EXISTS (SELECT 1 FROM json_each(notes.keywords) WHERE value = ?)"
        )
        params.append(keyword)
    if topic is not None:
        where_clauses.append(
            "EXISTS (SELECT 1 FROM json_each(notes.topics) WHERE value = ?)"
        )
        params.append(topic)

    where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    sql = f"""
        SELECT
            note_id,
            note_name,
            note_category,
            note_second_category,
            note_status,
            building_block,
            note_creation_date,
            folgezettel
        FROM notes
        {where_sql}
        ORDER BY note_id
        LIMIT ?
    """
    params.append(k)

    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(sql, params).fetchall()
    finally:
        conn.close()

    return [
        MetadataHit(
            note_id=row["note_id"],
            note_name=row["note_name"],
            note_category=row["note_category"],
            note_second_category=row["note_second_category"],
            note_status=row["note_status"],
            building_block=row["building_block"],
            note_creation_date=row["note_creation_date"],
            folgezettel=row["folgezettel"],
        )
        for row in rows
    ]
