"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.37"

__status__ = (
    "alpha — Architecture trail branches into the R-Cross sub-branch. "
    "Two new thought notes append to Trail 1: thought_cqrs_r_cross_rules "
    "(FZ 1a1b) formalises R-P (Schema ⊥ Runtime co-evolve), R-D (Descriptive "
    "purity), and R-Cross (System boundary) as the three architect-facing "
    "rules; thought_cqrs_r_cross_gap_audit (FZ 1a1b1) applies the three "
    "rules to Tessellum's current codebase and surfaces the productive-half "
    "gaps (DKS runtime, P→D retrieval client, Stage 3 BB-aware re-rank) "
    "that constitute the v0.2+ delta."
)
