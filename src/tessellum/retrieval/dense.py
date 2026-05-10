"""Dense (semantic) retrieval over the sqlite-vec index.

Reads the ``notes_vec`` virtual table populated by
:func:`tessellum.indexer.build` (with ``with_dense=True``, the default)
and ranks notes by cosine similarity to the query embedding.

Two notes worth knowing:

1. **Score sign**: sqlite-vec's ``MATCH`` returns ``distance`` (cosine
   distance, lower-is-better). Tessellum's ``DenseHit.score`` is
   ``1 - distance`` so users see "higher = more similar" — matches the
   ``BM25Hit.score`` convention from Wave 1.

2. **Lazy encoder**: the sentence-transformers model is loaded once per
   process via a module-level singleton. First call adds ~1.5s; the
   embedding library has its own model cache so subsequent process
   invocations only pay the import cost (~0.3s).
"""

from __future__ import annotations

import sqlite3
import struct
from dataclasses import dataclass
from pathlib import Path

import sqlite_vec

EMBEDDING_DIM = 384
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_ENCODER = None  # module-level singleton


def _get_encoder():
    """Lazy-load the sentence-transformers encoder (process-level cache)."""
    global _ENCODER
    if _ENCODER is not None:
        return _ENCODER
    from sentence_transformers import SentenceTransformer

    _ENCODER = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _ENCODER


def _vec_blob(vector) -> bytes:
    return struct.pack(f"{len(vector)}f", *vector)


@dataclass(frozen=True)
class DenseHit:
    """One ranked hit from a dense (semantic) search.

    Attributes:
        note_id: vault-relative path of the matching note.
        note_name: filename stem (e.g. ``term_zettelkasten``).
        distance: cosine distance from query to note embedding.
            Lower = closer. Returned by sqlite-vec's MATCH operator.
        score: ``1 - distance`` — cosine similarity. Higher = more similar.
            Mirrors ``BM25Hit.score``'s "higher = better" convention.
    """

    note_id: str
    note_name: str
    distance: float
    score: float


def dense_search(
    db_path: Path | str,
    query: str,
    *,
    k: int = 20,
) -> list[DenseHit]:
    """Rank notes by dense embedding similarity to ``query``.

    Args:
        db_path: Index DB (output of ``tessellum index build``). Must
            already contain the ``notes_vec`` virtual table — i.e. the
            build was run *with* ``with_dense=True`` (the default).
        query: Free-form natural-language query. Encoded by the same
            sentence-transformers model used at index time.
        k: Maximum number of results.

    Returns:
        List of ``DenseHit``, sorted by ascending distance (= descending
        similarity score). Empty list only if ``k <= 0`` or the index is
        empty; sqlite-vec always returns ``min(k, num_rows)`` results.

    Raises:
        FileNotFoundError: ``db_path`` doesn't exist.
        sqlite3.OperationalError: ``notes_vec`` table missing (run
            ``tessellum index build`` without ``--no-dense``).
    """
    db = Path(db_path)
    if not db.is_file():
        raise FileNotFoundError(
            f"index DB not found at {db}. Run `tessellum index build` first."
        )

    if k <= 0:
        return []

    encoder = _get_encoder()
    query_emb = encoder.encode([query], normalize_embeddings=True)[0]
    query_blob = _vec_blob(query_emb.astype("float32").tolist())

    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    try:
        sql = """
            SELECT
                n.note_id,
                n.note_name,
                v.distance
            FROM notes_vec v
            JOIN notes n ON n.note_int_id = v.note_int_id
            WHERE v.embedding MATCH ? AND k = ?
            ORDER BY v.distance
        """
        rows = conn.execute(sql, (query_blob, k)).fetchall()
        return [
            DenseHit(
                note_id=r["note_id"],
                note_name=r["note_name"],
                distance=r["distance"],
                score=1.0 - r["distance"],
            )
            for r in rows
        ]
    finally:
        conn.close()
