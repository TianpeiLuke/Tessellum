"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.40"

__status__ = (
    "alpha — DKS Phase 1 ships. tessellum.composer.dks lands the core "
    "Python API: 7 typed dataclasses (DKSObservation, DKSWarrant, "
    "DKSArgument, DKSContradicts, DKSCounterArgument, DKSPattern, "
    "DKSRuleRevision), DKSCycleResult, the allocate_cycle_fz allocator "
    "with three modes (fresh/extend/branch), and DKSCycle that drives "
    "the 7-component closed loop through any LLMBackend. Each cycle "
    "deposits a 6-node Folgezettel subtree as designed in FZ 2a1. "
    "Phase 2 (DKS as a composer skill) is next."
)
