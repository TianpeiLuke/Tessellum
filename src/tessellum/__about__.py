"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.49"

__status__ = (
    "alpha — Phase 7 of plan_dks_expansion lands: learned confidence + "
    "retrieval-grounded warrants. CalibratedConfidence reads "
    "WarrantHistory for a recency-weighted attack-rate signal "
    "(replaces ConstantConfidence placeholder). `tessellum dks "
    "--calibrate` mode replays past per-cycle traces, reports the "
    "achieved false-gate rate at the current threshold, and suggests a "
    "threshold that hits --target-false-gate-rate (default 10% per "
    "D2). DKSCycle gains retrieval_client + semantic_disagreement "
    "kwargs: argument prompts get a 'Related material from the "
    "substrate' block when a RetrievalClient is wired; step 4 can use "
    "one LLM call for semantic disagreement detection (off by default; "
    "falls back to string-compare on parse failure). CLI flags: "
    "--confidence-model {constant,calibrated}, --calibrate, "
    "--target-false-gate-rate, --retrieval-db, --semantic-disagreement. "
    "Operationalises FZ 2a2's Level 2 learning."
)
