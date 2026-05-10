"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.29"

__status__ = (
    "alpha — Seed vault now ships 11 foundation term notes (added "
    "term_knowledge_building_blocks, term_basb, term_code_method) plus 6 "
    "acronym-glossary entry points. Three previously-shipped notes "
    "(zettelkasten / slipbox / DKS) had residual internal references in "
    "their bodies; scrubbed to ship as general public knowledge. Every "
    "shipped seed note passes `tessellum format check` with 0 errors and 0 "
    "Amazon-internal hits."
)
