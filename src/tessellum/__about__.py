"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.22"

__status__ = (
    "alpha — Composer Wave 5a (batch runner) shipped. `tessellum composer "
    "batch <jobs.json>` runs many (skill, leaves) jobs in parallel through "
    "ThreadPoolExecutor with deterministic resume — restart after a crash "
    "and completed jobs are skipped (cached results re-loaded from "
    "<runs_dir>/<job_id>.result.json). Wave 5b (eval framework with "
    "LLMJudge 5-dim rubric) is the last v0.1 scope remaining. "
    "See CHANGELOG.md."
)
