"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.13"

__status__ = (
    "alpha — Retrieval Wave 1 (BM25 + FTS5) shipped. "
    "Dense + Hybrid RRF + Best-first BFS in Waves 2-4. "
    "See CHANGELOG.md for what's available now and the v0.1 roadmap."
)
