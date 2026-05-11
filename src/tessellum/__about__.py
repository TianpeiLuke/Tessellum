"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.45"

__status__ = (
    "alpha — DKS Phase 5 ships. The production-polish phase + the v0.1 "
    "milestone for the closed-loop runtime. Confidence gating: optional "
    "DKSConfidenceModel + ConstantConfidence + DEFAULT_CONFIDENCE_THRESHOLD "
    "(0.85). Above-threshold observations short-circuit to observation + "
    "argument A (2-node FZ subtree, escalation_decision='gated'). "
    "Warrant persistence: WarrantRegistry holds the current warrant set; "
    "WarrantHistory appends every revision to runs/dks/warrant_history.jsonl; "
    "load_warrants_from_vault() picks up DKS-tagged procedure/concept "
    "notes. Inter-cycle telemetry: `tessellum dks --report` aggregates "
    "every aggregate trace under --runs-dir into closed-rate, "
    "gated-rate, top-K attacked warrants, per-run breakdown. R-Cross "
    "gap audit (FZ 1a1b1) re-validated: productive halves of R-P and "
    "R-Cross are now closed by DKS Phases 1-5. The runtime is feature-"
    "complete per the 5-phase plan; v0.1 polish next."
)
