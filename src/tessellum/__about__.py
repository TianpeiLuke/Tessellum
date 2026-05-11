"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.52"

__status__ = (
    "alpha — Phase 9 of plan_dks_expansion lands: meta-DKS (the "
    "schema-mutation runtime). Three load-bearing design commitments "
    "ship: D3 event-sourced schema (BB_SCHEMA_USER_EXTENSIONS is now "
    "the fold over an append-only SchemaEditEvent log; the schema is "
    "retractable state with immutable history); D4 META_SCHEMA in "
    "code, PR-gated (the recursion stop — one level of meta, anchored "
    "by human-authored meta-meta-schema with 5 states + 4 "
    "transitions); D8 frozen-at-creation bb_schema_version (corpus "
    "migration becomes a query, not a rewrite). New tessellum.dks.meta "
    "package ships MetaObservation (telemetry-derived anchor), "
    "SchemaEditProposal (the meta-cycle's argument), MetaCycle (4-stage "
    "dispatcher: build proposals → filter → survive → emit events). "
    "v0.0.52 ships heuristic-based proposers (Toulmin-failure "
    "dominance + unrealised-edge retraction); Phase 11+ will swap in "
    "LLM-driven dialectic. New `tessellum dks --meta` CLI mode with "
    "--apply / --min-cycles / --target-failure flags + JSON output. "
    "Cold-start guard at 20 cycles prevents premature schema edits. "
    "Events land in runs/dks/meta/schema_events.jsonl with an "
    "auto-generated migration note per --apply. FZ 2c1 design note "
    "(thought_meta_dks_design.md) documents the synthesis. R-P's "
    "productive half lands at full strength here — the first phase "
    "where the schema *changes* in response to runtime evidence."
)
