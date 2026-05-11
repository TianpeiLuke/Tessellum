"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.42"

__status__ = (
    "alpha — DKS Phase 2 ships. tessellum-dks-cycle lands as a Composer "
    "skill: canonical body + .pipeline.yaml sidecar mapping the 7-component "
    "closed loop onto 7 pipeline steps. Steps 1, 2, 3, 5, 6, 7 each "
    "materialise a typed atomic note via body_markdown_frontmatter_to_file; "
    "step 4 is a no_op (the contradicts edge lives as a markdown link in "
    "the attacker's body). One closed cycle deposits a 6-node Folgezettel "
    "subtree designed in FZ 2a1. Both canonical + sidecar seed via "
    "SEED_VAULT_MANIFEST so `tessellum init` copies them into every new "
    "vault. Phase 3 (multi-cycle CLI) is next."
)
