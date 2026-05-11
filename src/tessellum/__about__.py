"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.51"

__status__ = (
    "alpha — Phase 8 of plan_dks_expansion lands: dispatcher refactor "
    "(the FZ 2a2-deferred work). D1 resolution implemented end-to-end: "
    "subclass-per-BBType frozen dataclasses with kw_only=True. "
    "EmpiricalObservationNode/ConceptNode/ModelNode/HypothesisNode/"
    "ArgumentNode/CounterArgumentNode/ProcedureNode/NavigationNode "
    "each fix bb_type via field(default=..., init=False). DKS cycle "
    "dataclasses (DKSObservation/DKSArgument/DKSCounterArgument/"
    "DKSPattern) inherit from the corresponding *Node — every cycle-"
    "step output is a typed BBNode subclass. New tessellum.dks.fsm "
    "module ships DKSStateMachine with .walk() returning BBPath, plus "
    "a TransitionHandler registry surface for future meta-DKS handler "
    "swaps. v0.0.51 walk() delegates to DKSCycle internally; the "
    "registry is wired but not yet dispatched-through (Phase 9 "
    "meta-DKS pays into it). DKSCycle's public API unchanged."
)
