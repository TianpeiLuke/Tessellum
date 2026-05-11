"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.56"

__status__ = (
    "alpha — Phase II of plan_v01_completion_roadmap: CI workflow + "
    "ship-the-wheel discipline.\n"
    "\n"
    "Key contributions:\n"
    " • GitHub Actions CI (.github/workflows/ci.yml) — four jobs on "
    "every push to main + every PR: ruff lint, pytest under "
    "Python 3.11 + 3.12 matrix, seed-vault format-check, and hatch "
    "build with wheel template-count verification. Concurrency cancels "
    "superseded runs; pip cache keyed on pyproject.toml. Every future "
    "release now gets PR-time regression detection.\n"
    " • Pre-CI codebase hygiene — 121 ruff violations in src/ + tests/ "
    "addressed: 105 auto-fixed (unused imports, empty f-string "
    "placeholders), 15 manually (unused variables, ambiguous names, "
    "module-import ordering). Codebase now lints clean against the "
    "configured ruleset.\n"
    " • Hatch force-include verification — confirmed "
    "vault/resources/templates/ ships in the wheel at "
    "tessellum/data/templates/ (18 templates). Build job's wheel "
    "assertion catches future regressions.\n"
    "\n"
    "No new runtime features. 867 tests pass (unchanged from v0.0.55)."
)
