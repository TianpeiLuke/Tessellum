"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.12"

__status__ = (
    "alpha — `tessellum index build` ships (System D substrate). "
    "FTS5 + sqlite-vec + retrieval CLI ship in v0.0.13+. "
    "See CHANGELOG.md for what's available now and the v0.1 roadmap."
)
