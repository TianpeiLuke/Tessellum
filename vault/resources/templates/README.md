---
tags:
  - resource
  - template
  - navigation
keywords:
  - templates directory
  - note templates
  - copy and fill
  - executable spec
  - tessellum format
topics:
  - Note Format
  - Templates
language: markdown
date of note: 2026-05-10
status: active
building_block: navigation
---

# Templates — Executable Skeletons of the YAML Frontmatter Spec

This directory holds **one template per Building Block type** — eight skeletons that exemplify Tessellum's note format. The templates are *executable*: the format validator (`scripts/check_note_format.py`) runs against them, so the templates and the spec cannot drift apart.

> **The spec is documented in [`DEVELOPING.md § YAML Frontmatter Specification`](../../../DEVELOPING.md#yaml-frontmatter-specification). The templates are its executable form.**

## How to Use

1. Pick the template matching the Building Block type of your new note (see table below).
2. Copy it to the appropriate vault subdirectory (per the BB → second-category mapping).
3. Rename the file (e.g., `template_concept.md` → `term_<your_topic>.md`).
4. Update the YAML frontmatter — at minimum: `date of note`, `tags[1]` (second category), `keywords`, `topics`. Set `status: active`.
5. Fill the required H2 sections.
6. **Remove the `<!-- HOW TO USE -->` commentary block at the top.**
7. Run `python scripts/check_note_format.py --path <your-file.md>` to validate.

## The 12 Templates + 1 YAML Reference

8 BB-type templates + 1 skill-canonical + 1 experiment + 1 entry-point + 1 acronym-glossary + 1 YAML header reference.

**For YAML conventions in isolation** (no body, just the frontmatter spec): [`template_yaml_header.md`](template_yaml_header.md). Read this if you want to scan the 7 required fields, the closed enums, the open vocabularies, and the type-specific extensions in one place — without picking a BB-type skeleton first.

**For copy-and-fill skeletons** (full YAML + body sections per BB type): pick from the table below.

| Template | BB Type | tags[1] | Common Destination |
|---|---|---|---|
| [template_concept.md](template_concept.md) | `concept` | `terminology` | `vault/resources/term_dictionary/` |
| [template_procedure.md](template_procedure.md) | `procedure` | `how_to` | `vault/resources/how_to/` |
| [template_skill.md](template_skill.md) | `procedure` | `skill` | `vault/resources/skills/` (paired with `.claude/skills/` + `.kiro/skills/` thin headers) |
| [template_model.md](template_model.md) | `model` | `code_repo` / `architecture` / `schema` | `vault/areas/code_repos/` or `vault/resources/term_dictionary/` |
| [template_argument.md](template_argument.md) | `argument` | `analysis` | `vault/resources/analysis_thoughts/` |
| [template_counter_argument.md](template_counter_argument.md) | `counter_argument` | `analysis` | `vault/resources/analysis_thoughts/` |
| [template_hypothesis.md](template_hypothesis.md) | `hypothesis` | `analysis` | `vault/resources/analysis_thoughts/` |
| [template_empirical_observation.md](template_empirical_observation.md) | `empirical_observation` | `analysis` | `vault/resources/analysis_thoughts/` (inline observations in trails) |
| [template_experiment.md](template_experiment.md) | `empirical_observation` | `experiment` | `vault/archives/experiments/` (full pre-registered investigations) |
| [template_navigation.md](template_navigation.md) | `navigation` | `navigation` | `vault/0_entry_points/` (generic case) |
| [template_entry_point.md](template_entry_point.md) | `navigation` | `index` | `vault/0_entry_points/entry_*.md` (master TOCs + per-surface entries) |
| [template_acronym_glossary.md](template_acronym_glossary.md) | `navigation` | `index` (with `glossary` topic tag) | `vault/0_entry_points/acronym_glossary_*.md` |

**Three pairs share a `building_block:` value but have distinct shapes**:

- **`template_procedure` vs `template_skill`** — both are `procedure` BB. `procedure` is for human-readable how-tos. `skill` is for agent-executable skill canonicals — includes `<!-- :: section_id = X :: -->` markers that the composer pipeline relies on for typed-contract parsing, plus `related_skill_headers:` + `pipeline_metadata:` YAML fields.
- **`template_empirical_observation` vs `template_experiment`** — both are `empirical_observation` BB. `empirical_observation` is for inline observations embedded in thought trails (lighter, less pre-registration emphasis). `experiment` is for full pre-registered investigations archived under `vault/archives/experiments/` (heavier, with explicit Pre-Registration sections that must be filled before running).
- **`template_concept` vs `template_model`** — `concept` is for definitions of named things (term notes); `model` is for relational structures (architectures, schemas). A note about an ML technique might be either, depending on whether it primarily *names* the technique (concept) or *structures its components* (model).
- **`template_navigation` vs `template_entry_point` vs `template_acronym_glossary`** — all three are `navigation` BB. `template_navigation` is generic (any index/routing note, anywhere in the vault). `template_entry_point` is the specific case of navigation notes that live in `vault/0_entry_points/entry_*.md` and serve as named master TOCs / per-surface indexes (incl. the master `entry_acronym_glossary.md` that aggregates per-field sub-glossaries). `template_acronym_glossary` is the further-specialized case for acronym glossary notes — both the single `acronym_glossary.md` (pattern A, small vault) and per-field `acronym_glossary_<field>.md` sub-glossaries (pattern B, partitioned, recommended for vaults > 50 terms). Glossaries cover **all term notes** via per-acronym `### ACRONYM` entries with Full Name / Description / Documentation / Related sub-fields; in pattern B, the union of sub-glossaries covers every term note.

## Why Templates Live in the Vault

Tessellum dogfoods itself. Every other piece of project documentation (term notes, examples, master TOC) lives inside `vault/`. Templates fit the same pattern — they're *notes about how to write notes*, and they belong alongside the notes they exemplify.

This has three concrete benefits:

1. **The validator binds spec to template** — `scripts/check_note_format.py` runs on these templates as part of CI. If a template breaks the format, the build fails. Spec and exemplar cannot diverge.
2. **Self-applied retrieval** — `tessellum search "concept template"` finds the right starting point. Templates are searchable like any other note.
3. **No mechanism overhead** — `tessellum capture <bb>` (planned in v0.1) just does `cp templates/template_<bb>.md <destination>/`. No template engine, no Jinja, no string interpolation.

## Status Convention for Templates

Templates use `status: template` — a dedicated value distinct from `stub` (real note that's incomplete) and `placeholder` (future-real note that doesn't exist yet). The `template` status signals "intentional skeleton, not real content." Search filters templates out by default; explicit `--status template` queries them.

## Adding a New Template

If you find yourself writing the same shape of note repeatedly and there's no template for it (e.g., a literature note `lit_*.md`, a paper section `paper_*_*.md`, an FZ trail root), add a new template here. Naming: `template_<purpose>.md`. Update this README's table.

The 8 BB-type templates are the load-bearing minimum. Type-specific templates layer atop without polluting the BB taxonomy.

## See Also

- [DEVELOPING.md § YAML Frontmatter Specification](../../../DEVELOPING.md#yaml-frontmatter-specification) — full spec
- [CONTRIBUTING.md § Note Format Standards](../../../CONTRIBUTING.md#note-format-standards) — contributor-facing summary
- [term_building_block.md](../term_dictionary/term_building_block.md) — the BB ontology these templates implement
- [Master TOC](../../0_entry_points/entry_master_toc.md) — back to vault top
