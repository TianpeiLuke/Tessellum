"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.23"

__status__ = (
    "alpha — Composer Wave 5b (eval framework) shipped. `tessellum composer "
    "eval <scenarios/>` runs structural assertions (no_errors, step_count_eq, "
    "file_written, response_contains) AND optional LLMJudge 5-dim rubric "
    "scoring (relevance, completeness, accuracy, clarity, structural_integrity) "
    "across YAML-defined scenarios. The full Composer port from "
    "AbuseSlipBox is now complete: capture (Wave 1) → compile (Wave 2) → "
    "execute (Wave 3) → real LLM (Wave 4) → batch + resume (Wave 5a) → "
    "evaluate (Wave 5b). See CHANGELOG.md."
)
