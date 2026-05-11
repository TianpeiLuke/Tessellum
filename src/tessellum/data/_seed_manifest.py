"""Single source of truth for the seed-vault file list.

This module is the *only* place to declare which files ship as seed
content in every Tessellum install. Both ends of the seed-vault
pipeline read from here:

- ``src/tessellum/init.py`` — at runtime, ``tessellum init`` copies
  each listed file from the installed ``data/seed_vault/`` (or the
  source-tree fallback) into the newly scaffolded vault.
- ``hatch_build.py`` — at wheel build time, the custom Hatch build
  hook reads this module and registers ``force_include`` mappings
  so each listed file is grafted from the dogfooded ``vault/`` into
  the wheel's ``tessellum/data/seed_vault/`` package-data directory.

Adding a seed file means **appending one line** to
:data:`SEED_VAULT_MANIFEST`. No other file changes are required —
the build hook picks it up automatically at the next ``python -m build``
and ``tessellum init`` will start copying it on the next install.

Paths in the manifest are **vault-relative**: each entry ``X`` maps to:

- source (dogfood): ``vault/X``
- wheel destination: ``tessellum/data/seed_vault/X``
- runtime copy target: ``<scaffolded_vault>/X``

Two special grafts ship via static ``force-include`` in
``pyproject.toml`` because their shape is different — a directory
copy rather than a per-file mapping:

- ``vault/resources/templates/`` → ``tessellum/data/templates/``
  (15 templates, shipped wholesale as a directory)

Those grafts are NOT in this manifest because ``tessellum init`` copies
them through ``templates_dir()`` rather than through the per-file
loop that consumes :data:`SEED_VAULT_MANIFEST`.
"""

from __future__ import annotations

__all__ = ["SEED_VAULT_MANIFEST"]


SEED_VAULT_MANIFEST: tuple[str, ...] = (
    # ── 11 foundation term notes (the conceptual primer) ─────────────────
    "resources/term_dictionary/term_knowledge_building_blocks.md",     # Sascha Fast — historical
    "resources/term_dictionary/term_building_block.md",                # Tessellum's 8-type BB ontology
    "resources/term_dictionary/term_epistemic_function.md",            # what each BB does
    "resources/term_dictionary/term_dialectic_knowledge_system.md",    # DKS
    "resources/term_dictionary/term_cqrs.md",                          # System P ⊥ System D
    "resources/term_dictionary/term_zettelkasten.md",                  # Luhmann's method
    "resources/term_dictionary/term_para_method.md",                   # Forte's PARA
    "resources/term_dictionary/term_basb.md",                          # Building a Second Brain
    "resources/term_dictionary/term_code_method.md",                   # CODE lifecycle
    "resources/term_dictionary/term_slipbox.md",                       # the system class
    "resources/term_dictionary/term_folgezettel.md",                   # trail mechanism

    # ── System regularization (the format contract) ──────────────────────
    "resources/term_dictionary/term_format_spec.md",

    # ── Canonical BB exemplar — model (areas/code_repos/ per convention) ──
    "areas/code_repos/repo_tessellum.md",                              # ★ canonical model exemplar

    # ── COE (Correction of Errors) review-and-reflect surface ────────────
    "resources/term_dictionary/term_coe.md",                           # method + 9-section shape
    "resources/skills/skill_tessellum_write_coe.md",                   # 6-step Composer skill canonical
    "resources/skills/skill_tessellum_write_coe.pipeline.yaml",        # sidecar (Composer-compatible)

    # ── FZ trail tooling (skills used with `tessellum fz` CLI) ───────────
    "resources/skills/skill_tessellum_traverse_folgezettel.md",        # ancestors / descendants / siblings
    "resources/skills/skill_tessellum_manage_folgezettel.md",          # list / next-FZ / integrity audit
    "resources/skills/skill_tessellum_append_to_trail.md",             # full append-new-node procedure

    # ── DKS Phase 2 (composer skill) — the agent-invocable surface ──────
    "resources/skills/skill_tessellum_dks_cycle.md",                   # 7-component closed-loop canonical
    "resources/skills/skill_tessellum_dks_cycle.pipeline.yaml",        # sidecar (Composer-compatible)
    "resources/skills/skill_tessellum_meta_dks_cycle.md",              # 4-step meta-cycle canonical (v0.0.53)
    "resources/skills/skill_tessellum_meta_dks_cycle.pipeline.yaml",   # meta-cycle sidecar

    # ── Capture-side helpers (v0.0.58) — classification + routing ────────
    "resources/skills/skill_tessellum_classify_content.md",            # 5-step BB classification (ported from AB, adapted)
    "resources/skills/skill_tessellum_classify_content.pipeline.yaml", # classify sidecar
    "resources/skills/skill_tessellum_route_content.md",               # 6-step routing + 3-criterion novelty (ported from AB, trimmed)
    "resources/skills/skill_tessellum_route_content.pipeline.yaml",    # route sidecar

    # ── Getting-started walkthrough ──────────────────────────────────────
    "resources/how_to/howto_first_vault.md",
    "resources/how_to/howto_note_format.md",                           # v0.0.59 — YAML frontmatter spec walkthrough
    "resources/how_to/howto_agent_integration.md",                     # v0.0.59 — invoke skills from MCP / Composer / Python
    "resources/how_to/howto_growing_a_trail.md",                       # v0.0.59 — FZ trail authoring + DKS-driven growth

    # ── FZ trail nodes (Trail 1: Architecture / CQRS — 8 thoughts) ───────
    "resources/analysis_thoughts/thought_building_block_ontology_relationships.md",        # FZ 1
    "resources/analysis_thoughts/thought_cqrs_design_evolution.md",                        # FZ 1a
    "resources/analysis_thoughts/thought_synthesis_two_systems_cqrs_value_proposition.md", # FZ 1a1
    "resources/analysis_thoughts/thought_cqrs_essence_for_tessellum.md",                   # FZ 1a1a
    "resources/analysis_thoughts/thought_cqrs_r_cross_rules.md",                           # FZ 1a1b
    "resources/analysis_thoughts/thought_cqrs_r_cross_gap_audit.md",                       # FZ 1a1b1
    "resources/analysis_thoughts/thought_bb_ontology_as_typed_graph.md",                   # FZ 1b — BB-graph formalisation (co-companion of FZ 2a2)
    "resources/analysis_thoughts/thought_bb_internal_transitions_evidence.md",             # FZ 1c — BB-internal-transitions counter (co-companion of FZ 2c)

    # ── FZ trail nodes (Trail 2: Dialectic / DKS — 6 thoughts) ───────────
    "resources/analysis_thoughts/thought_dks_evolution.md",                  # FZ 2
    "resources/analysis_thoughts/thought_dks_design_synthesis.md",           # FZ 2a
    "resources/analysis_thoughts/thought_dks_fz_integration.md",             # FZ 2a1 — spatial sharpening (FZ duality)
    "resources/analysis_thoughts/thought_dks_as_fsm_on_bb_graph.md",         # FZ 2a2 — formal sharpening (FSM on BB graph)
    "resources/analysis_thoughts/thought_dks_runtime_integration.md",        # FZ 2b  — runtime integration (Phase 4)
    "resources/analysis_thoughts/thought_dks_transition_model_adaptation.md",# FZ 2c  — transition-model adaptation (companion to FZ 1c)
    "resources/analysis_thoughts/thought_meta_dks_design.md",                # FZ 2c1 — meta-DKS design synthesis (v0.0.52 runtime)
    "resources/analysis_thoughts/thought_meta_dks_validation_v053.md",       # FZ 2c1a — Phase V validation evidence (v0.0.53)

    # ── FZ trail nodes (Trail 3: Retrieval / System D — 2 thoughts) ──────
    "resources/analysis_thoughts/thought_retrieval_evolution.md",      # FZ 3
    "resources/analysis_thoughts/thought_retrieval_synthesis.md",      # FZ 3a

    # ── Entry points (master TOCs / pickers / FZ trail map / glossary index) ─
    "0_entry_points/entry_acronym_glossary.md",
    "0_entry_points/entry_building_block_index.md",         # BB picker matrix
    "0_entry_points/entry_folgezettel_trails.md",           # FZ master trail index
    "0_entry_points/entry_architecture_trail.md",           # per-trail entry: Trail 1
    "0_entry_points/entry_dialectic_trail.md",              # per-trail entry: Trail 2
    "0_entry_points/entry_retrieval_trail.md",              # per-trail entry: Trail 3
    "0_entry_points/entry_coes.md",                         # COE index (skill writes here)

    # ── Acronym glossaries (1 Tessellum-foundations + 5 universal) ───────
    "0_entry_points/acronym_glossary_tessellum_foundations.md",
    "0_entry_points/acronym_glossary_statistics.md",
    "0_entry_points/acronym_glossary_critical_thinking.md",
    "0_entry_points/acronym_glossary_cognitive_science.md",
    "0_entry_points/acronym_glossary_network_science.md",
    "0_entry_points/acronym_glossary_llm.md",
)
