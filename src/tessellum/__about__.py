"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.21"

__status__ = (
    "alpha — Composer Wave 4 (Anthropic LLM bridge) shipped. "
    "`tessellum composer run --backend=anthropic` dispatches the compiled "
    "DAG through the real Anthropic Messages API behind the [agent] extras "
    "(`pip install tessellum[agent]`) — install once, set ANTHROPIC_API_KEY, "
    "and pipelines run end-to-end against any Claude model. MockBackend "
    "remains the default. Wave 5+ (batch runner + eval framework) are the "
    "only v0.1 scope remaining. See CHANGELOG.md."
)
