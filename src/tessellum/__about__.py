"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.35"

__status__ = (
    "alpha — Seed vault gains the Correction of Errors (COE) "
    "review-and-reflect surface. Ported from the parent project and "
    "generalised as public knowledge: term_coe.md (the method + 9-section "
    "shape + 5 Whys), skill_tessellum_write_coe.md + sidecar (6-step "
    "Composer pipeline: gather → 5-Whys → write → check duplicates → "
    "verify → update index), and entry_coes.md (the index the skill "
    "appends to). Skill validates + compiles cleanly; works with "
    "MockBackend (offline) and AnthropicBackend (`[agent]` extras)."
)
