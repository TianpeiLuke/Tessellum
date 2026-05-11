"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.43"

__status__ = (
    "alpha — DKS Phase 3 ships. Multi-cycle orchestration arrives: "
    "DKSRunner threads warrants across N sequential cycles, WarrantChange "
    "tags each rule revision as added/revised/superseded, and the new "
    "`tessellum composer dks <observations.jsonl>` CLI loads observations, "
    "runs the DKSRunner over MockBackend or AnthropicBackend, and writes "
    "per-cycle + aggregate trace JSON to runs/dks/. JSONL entries support "
    "explicit mode/parent_fz for fresh/extend/branch trail allocation. "
    "Phase 4 (P-side retrieval client + TESS-004 validator + 6th LLMJudge "
    "dim) is next."
)
