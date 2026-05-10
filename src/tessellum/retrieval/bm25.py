"""BM25 lexical retrieval over the FTS5 index.

Reads the ``notes_fts`` virtual table populated by
:func:`tessellum.indexer.build` and ranks notes by BM25 score.

Three details worth knowing:

1. **Score sign**: SQLite's ``bm25()`` function returns a NEGATIVE score
   (lower-is-better is FTS5's convention). We negate it so the public
   ``BM25Hit.score`` is "higher = more relevant", matching how users
   read scores. ``ORDER BY bm25(notes_fts)`` (no negation) gives the
   correct ranking — the negation only flips the displayed sign.

2. **Snippet generation**: SQLite's ``snippet()`` function returns an
   excerpt with matched terms wrapped in markers. We use ``<<<>>>`` as
   the open/close (terminal-friendly, easy to grep). Set
   ``snippet_length=None`` to skip snippet generation entirely (small
   speedup for batch queries).

3. **Query syntax**: The ``query`` argument is passed straight to FTS5's
   ``MATCH`` operator. FTS5 supports prefix queries (``foo*``), phrase
   queries (``"exact phrase"``), boolean operators (``AND``, ``OR``,
   ``NOT``), and column filters (``note_name:term``). Free-text queries
   work as implicit AND. Errors from malformed query syntax bubble up
   as ``sqlite3.OperationalError``.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BM25Hit:
    """One ranked hit from a BM25 search.

    Attributes:
        note_id: vault-relative path of the matching note.
        note_name: filename stem (e.g. ``term_zettelkasten``).
        score: BM25 relevance score, **higher = more relevant**.
            (Internally we negate FTS5's lower-is-better score.)
        snippet: Excerpt highlighting matched terms with ``<<<term>>>``
            markers. ``None`` if ``snippet_length=None`` was passed.
    """

    note_id: str
    note_name: str
    score: float
    snippet: str | None = None


def bm25_search(
    db_path: Path | str,
    query: str,
    *,
    k: int = 20,
    snippet_length: int | None = 30,
) -> list[BM25Hit]:
    """Rank notes by BM25 lexical match against ``query``.

    Args:
        db_path: Index DB (output of ``tessellum index build``). Must
            already contain the ``notes_fts`` virtual table.
        query: Free-form search query. Passed to FTS5's MATCH operator;
            supports prefix (``foo*``), phrase (``"x y"``), and column
            filters (``note_name:term``).
        k: Maximum number of results.
        snippet_length: Max tokens in returned snippet. Set to ``None``
            to skip snippet generation. Default ``30`` matches the FTS5
            documentation's recommended size.

    Returns:
        List of ``BM25Hit``, sorted by descending relevance.
        Empty list if no notes match.

    Raises:
        FileNotFoundError: ``db_path`` doesn't exist.
        sqlite3.OperationalError: Malformed FTS5 query syntax, or the
            ``notes_fts`` table is missing (run ``tessellum index build``).
    """
    db = Path(db_path)
    if not db.is_file():
        raise FileNotFoundError(
            f"index DB not found at {db}. Run `tessellum index build` first."
        )

    if k <= 0:
        return []

    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    try:
        if snippet_length is not None:
            sql = """
                SELECT
                    note_id,
                    note_name,
                    -bm25(notes_fts) AS score,
                    snippet(notes_fts, 2, '<<<', '>>>', '...', ?) AS snippet
                FROM notes_fts
                WHERE notes_fts MATCH ?
                ORDER BY bm25(notes_fts)
                LIMIT ?
            """
            rows = conn.execute(sql, (snippet_length, query, k)).fetchall()
            return [
                BM25Hit(
                    note_id=r["note_id"],
                    note_name=r["note_name"],
                    score=r["score"],
                    snippet=r["snippet"],
                )
                for r in rows
            ]

        sql = """
            SELECT
                note_id,
                note_name,
                -bm25(notes_fts) AS score
            FROM notes_fts
            WHERE notes_fts MATCH ?
            ORDER BY bm25(notes_fts)
            LIMIT ?
        """
        rows = conn.execute(sql, (query, k)).fetchall()
        return [
            BM25Hit(
                note_id=r["note_id"],
                note_name=r["note_name"],
                score=r["score"],
            )
            for r in rows
        ]
    finally:
        conn.close()
