"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.48"

__status__ = (
    "alpha — Phase 6 of plan_dks_expansion lands: validator + telemetry "
    "generalisation. TESS-005 (WARNING-only) flags body-links between "
    "BB-typed notes whose pair isn't in BB_SCHEMA (in either direction); "
    "same-BB cross-references and active-status-only constraints keep "
    "noise low. New top-level CLI `tessellum bb audit` surfaces "
    "vault-wide BBGraph telemetry: node counts by BBType, edge counts "
    "by epistemic-edge label, untyped edges, orphan nodes, unrealised "
    "schema edges. `tessellum dks --report --include-bb-graph` joins "
    "per-run aggregate stats with corpus telemetry. 7 of 8 plan open "
    "questions resolved against best-practice principles before Phase 6 "
    "shipped; the resolutions land in plans/plan_dks_expansion.md."
)
