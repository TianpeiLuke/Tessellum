"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.54"

__status__ = (
    "alpha — Phase 10 of plan_dks_expansion: multi-perspective DKS "
    "+ Dung grounded labelling. DKSCycle accepts a perspectives "
    "kwarg (default ('conservative', 'exploratory') preserves "
    "v0.0.40-era A/B behaviour). N>2 perspectives activates "
    "pairwise contradicts: every (i, j) pair with i<j and "
    "different claims emits one DKSContradicts edge with the "
    "later perspective as attacker. New tessellum.dks.dung module "
    "ships DungAF + grounded_labelling implementing Dung 1995's "
    "grounded semantics via fixpoint iteration (in/out/undec). "
    "DKSCycleResult gains three additive fields: arguments "
    "(tuple), contradicts_edges (tuple), grounded_labelling "
    "(dict). New surviving_argument_fzs property surfaces the "
    "set of IN-labelled arguments — the multi-survivor surface "
    "for DKSRunner warrant threading. CLI gains "
    "--perspectives <comma-separated> flag passing through to "
    "DKSRunner. Back-compat preserved end-to-end: existing N=2 "
    "callers see identical output, with the new fields populated "
    "additively (grounded_labelling shows {A: out, B: in} when "
    "contradicts fires, both in when they agree)."
)
