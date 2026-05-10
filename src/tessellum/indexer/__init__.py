"""tessellum.indexer — SQLite-backed unified index for vault notes.

The indexer is System D's build output (per the CQRS layout): walks
``vault/``, parses every typed atomic note, extracts markdown links, and
writes rows into a single SQLite database. Subsequent waves layer FTS5
(lexical retrieval) and sqlite-vec (dense retrieval) on top of the same
DB; v0.0.12 ships only the structural substrate (notes + note_links).

Public API:

    build(vault_path, db_path, *, force=False) -> BuildResult
        Full vault scan -> SQLite write. Idempotent — drops and re-creates
        the DB at db_path each run.

    Database(db_path)
        Read-oriented wrapper around the SQLite connection. Typed query
        helpers for the most common access patterns (by category, by BB,
        by FZ, links from/to).

    NoteRow, LinkRow, BuildResult — typed dataclasses for query results.

Future waves (deferred):

    v0.0.13 — ghost_notes + broken_links diagnostic tables;
              folgezettel_trails table + traversal helpers
    v0.0.13 — incremental ``tessellum index update`` (mtime-based)
    v0.0.14 — FTS5 (BM25 lexical retrieval) + ``tessellum search --bm25``
    v0.0.15 — sqlite-vec (dense retrieval) + ``tessellum search --dense``
    v0.1.0  — RRF fusion (``tessellum search`` with hybrid default)
"""

from tessellum.indexer.build import BuildResult, build
from tessellum.indexer.db import Database, LinkRow, NoteRow

__all__ = [
    "build",
    "BuildResult",
    "Database",
    "NoteRow",
    "LinkRow",
]
