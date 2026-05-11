"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.47"

__status__ = (
    "alpha — FSM refactor lands: new tessellum.bb module is the source "
    "of truth for the BB ontology. BBType (StrEnum, 8 values) replaces "
    "VALID_BUILDING_BLOCKS as the canonical BB enum; EpistemicEdgeType "
    "+ BB_SCHEMA (8 epistemic + 7 navigation + 1 DKS extension for "
    "CTR→MOD = 16 typed edges) is the schema graph FZ 1b proposed. "
    "BBGraph holds either the synthetic schema (BBGraph.schema()) or "
    "the live corpus (BBGraph.from_db(db_path)) — read-only, with "
    "untyped-edge detection + per-label edge counting for telemetry. "
    "DKS dataclasses (DKSObservation/DKSArgument/DKSCounterArgument/"
    "DKSPattern) carry bb_type ClassVars pointing at BBType. No DKS "
    "dispatcher refactor (per FZ 2a2's deferral reasons); per-component "
    "dataclasses are typed views over BBNode. Public API stable."
)
