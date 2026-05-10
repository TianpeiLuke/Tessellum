"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.19"

__status__ = (
    "alpha — Composer Wave 2 (compiler) shipped. tessellum composer compile "
    "produces a typed DAG with contract validation, zero LLM calls. "
    "Wave 3 (executor + materializers) and Wave 4 (LLM bridge) are the only "
    "v0.1 scope remaining. See CHANGELOG.md."
)
