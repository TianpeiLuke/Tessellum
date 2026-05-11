"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.50"

__status__ = (
    "alpha — vault cleanup release. LINK-006 status=template exemption "
    "lands in the format validator + skill canonical + tests (parallel "
    "to TESS-004's authoring-state exemption — templates are orphans "
    "by design). Dogfood vault gains 553 ported notes from the parent "
    "AB project to resolve every broken-link target from the original "
    "Tessellum seed (the SEED_VAULT_MANIFEST stays unchanged at ~50 "
    "entries; the ports are dogfood-only). 5 AB-vault format quirks "
    "fixed at port time (DKS→dks tags, folgezettel-pair completion, "
    "paper-review reclassification). v0.0.49's Phase 7 behaviour "
    "unchanged."
)
