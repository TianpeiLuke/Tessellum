"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.24"

__status__ = (
    "alpha — Capture surface adds `code_snippet` and `code_repo` flavors. "
    "`tessellum capture code_snippet my_algo` and `tessellum capture code_repo "
    "my_repo` produce well-formed notes from new templates "
    "(template_code_snippet.md / template_code_repo.md) — the snippet "
    "template carries the `## Patterns` shape with dual-block per pattern "
    "(verbatim source + adapted-to-different-domain). 14 capture flavors "
    "registered total. Composer + Retrieval ports remain complete. "
    "See CHANGELOG.md."
)
