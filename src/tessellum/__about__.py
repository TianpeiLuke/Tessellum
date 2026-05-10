"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.20"

__status__ = (
    "alpha — Composer Wave 3 (executor + scheduler + materializers + mock LLM) "
    "shipped. `tessellum composer run` executes a compiled DAG end-to-end "
    "against a leaves list, dispatching through MockBackend by default and "
    "writing a JSON trace to runs/composer/. Wave 4 (Anthropic SDK backend "
    "behind [agent] extras) and Wave 5+ (batch runner + eval framework) are "
    "the only v0.1 scope remaining. See CHANGELOG.md."
)
