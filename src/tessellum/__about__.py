"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.17"

__status__ = (
    "alpha — Retrieval Wave 4.5 (`tessellum filter`) shipped — direct SQL "
    "filtering on YAML metadata. Five retrieval surfaces live: bm25, dense, "
    "hybrid (default), bfs, filter. Skill orchestration (Wave 5) is the last "
    "v0.1 retrieval milestone. See CHANGELOG.md."
)
