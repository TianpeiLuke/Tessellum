"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.44"

__status__ = (
    "alpha — DKS Phase 4 ships. The integration phase: tessellum.dks "
    "wires through every other Tessellum subsystem along typed contracts. "
    "RetrievalClient (P-side R-Cross client) lets DKS read through the "
    "unified index via hybrid_search — read-only by construction, no "
    "mutating surface. TESS-004 validator rule enforces that "
    "counter_argument notes (status: active) link to a building_block: "
    "argument note in their body; templates/drafts are exempt. The "
    "LLMJudge rubric grows from 5 to 6 dimensions with the addition of "
    "epistemic_congruence — does the output honour the BB-type "
    "expectations the question implies? FZ 2b thought note "
    "(thought_dks_runtime_integration) closes Trail 2 with a synthesis "
    "of how runtime + composer + retrieval + format + capture wire "
    "together. R-P and R-Cross both halves now actively enforced. "
    "Phase 5 (confidence gating + warrant persistence) is next."
)
