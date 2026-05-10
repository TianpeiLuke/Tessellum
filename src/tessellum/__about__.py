"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.33"

__status__ = (
    "alpha — Seed vault adds Trail 3 (Retrieval / System D): 2 thought "
    "notes (FZ 3 + FZ 3a) plus a per-trail entry point. The trail "
    "documents the 14-strategy bake-off and follow-up experiments that "
    "produced Tessellum's shipped design: unified SQLite+sqlite-vec+FTS5 "
    "engine, hybrid RRF default (+12pp lift), best-first BFS (no PPR — "
    "Hit@K/answer-quality disconnect ρ=0.37), direct metadata filter. "
    "Three trails total, eight nodes."
)
