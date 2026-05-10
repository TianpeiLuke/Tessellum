"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.26"

__status__ = (
    "alpha — Two capture skills ported from AbuseSlipBox and adapted to "
    "Tessellum: skill_tessellum_capture_code_repo_note (9-step DAG, "
    "main+sub-notes for a repo) and skill_tessellum_capture_code_snippet "
    "(7-step DAG, snippet note with BB-typed Patterns shape). Both validate "
    "via `tessellum composer validate` and compile via `tessellum composer "
    "compile`. Closes plan_code_artifacts_port across three phases. "
    "See CHANGELOG.md."
)
