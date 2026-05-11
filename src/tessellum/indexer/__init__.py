"""tessellum.indexer — SQLite-backed unified index for vault notes.

System D's build output (per the CQRS layout): walks ``vault/``,
parses every typed atomic note, extracts markdown links, and writes
rows into a single SQLite database. The retrieval layer
(:mod:`tessellum.retrieval`) layers FTS5 (BM25) and sqlite-vec (dense)
on top of the same DB.

Public API:

    build(vault_path, db_path, *, force=False) -> BuildResult
        Full vault scan -> SQLite write. Idempotent — drops and
        re-creates the DB at db_path each run.

    Database(db_path)
        Read-oriented wrapper around the SQLite connection. Typed
        query helpers for the most common access patterns (by
        category, by BB, by FZ, links from/to).

    NoteRow, LinkRow, BuildResult — typed dataclasses for query
    results.
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
