"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.27"

__status__ = (
    "alpha — `tessellum composer scaffold-sidecar <skill.md>` generates a "
    "starter pipeline sidecar by scanning the canonical's section anchors — "
    "fills the gap between hand-authoring a canonical and getting Composer "
    "integration. Plus a dependency cleanup: pruned 9 unused declared deps "
    "(matplotlib, Pillow, igraph, fa2, tiktoken, numpy, click, rich, "
    "rank-bm25) — install footprint goes from ~600MB to ~250MB. Wheel build "
    "fix (sdist exclude was dropping src/tessellum/data/__init__.py)."
)
