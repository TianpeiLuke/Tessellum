"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.16"

__status__ = (
    "alpha — Retrieval Wave 4 (Best-first BFS) shipped. "
    "Four strategies live: BM25, dense, hybrid (default), BFS. "
    "PPR deliberately not ported (FZ 5e2b1c). Wave 5 (skill orchestration) "
    "is the last v0.1 retrieval milestone. See CHANGELOG.md."
)
