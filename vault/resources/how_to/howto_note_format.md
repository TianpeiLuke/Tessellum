---
tags:
  - resource
  - how_to
  - note_format
  - yaml
  - frontmatter
keywords:
  - YAML frontmatter
  - note format spec
  - required fields
  - tessellum format check
  - building_block
  - bb_schema_version
topics:
  - Note Format
  - Vault Authoring
language: markdown
date of note: 2026-05-11
status: active
building_block: procedure
bb_schema_version: 1
---

# How To: Write a Note That Validates

This guide walks through Tessellum's YAML frontmatter spec — the contract every note must satisfy — and shows how to fix the common errors `tessellum format check` reports.

## Overview

Every Tessellum note is a `.md` file with two parts:

1. **YAML frontmatter** between two `---` lines at the top. Required.
2. **Markdown body** below. Free-form except for one required `# H1` line.

The frontmatter declares:
- *What kind of note this is* (`building_block:` — one of the 8 BB types).
- *Where it fits in the PARA scheme* (`tags[0]:` — `resource` / `area` / `project` / `archive` / `entry_point`).
- *How active it is* (`status:` — `active`, `draft`, `template`, etc.).
- *When it was written* (`date of note:` — ISO date).
- *What it's about* (`tags`, `keywords`, `topics`).
- *Which schema version was current when it was written* (`bb_schema_version:` — Tessellum auto-populates this on capture).
- *Where it sits in any FZ trail* (`folgezettel:` + `folgezettel_parent:` — empty when not part of a trail).

## Required fields

The validator enforces seven required fields:

```yaml
---
tags:                                # array, >= 2 entries, [0] must be a PARA bucket
  - resource                         # PARA: resource / area / project / archive / entry_point
  - analysis                         # second_category — free; classifies within PARA
  - dks                              # subject domain — free
keywords:                            # array, >= 3 recommended
  - DKS cycle
  - 7-component closed loop
  - typed atomic notes
topics:                              # array, >= 2 recommended
  - Dialectic Knowledge System
  - System P Runtime
language: markdown                   # always "markdown"
date of note: 2026-05-11             # ISO date (YYYY-MM-DD)
status: active                       # active / draft / archived / template / ...
building_block: argument             # one of the 8 BB types
---
```

Anything missing from this seven-field set produces a validator ERROR. The format check refuses to consider the note "valid" until all seven are present and shaped correctly.

## Optional fields (when relevant)

```yaml
bb_schema_version: 1                 # auto-populated by `tessellum capture`; D8 frozen-at-creation
folgezettel: "2c1"                   # quoted string — required if part of an FZ trail
folgezettel_parent: "2c"             # quoted string — the FZ this note descends from
argument_perspective: "conservative" # optional, on argument-typed notes (v0.0.55+)
pipeline_metadata: ./skill_<slug>.pipeline.yaml  # on skill canonicals — sidecar pointer
```

The optional fields are read by specific tools:
- `bb_schema_version:` is the D8 frozen-at-creation marker — TESS-005 validates the note's links against the schema as of *that* version (per v0.0.55).
- `folgezettel:` + `folgezettel_parent:` together register the note as a FZ trail node. They must agree (a child's parent FZ must be the prefix of its own FZ).
- `argument_perspective:` is the per-argument perspective string (e.g., `conservative` / `exploratory`) — feeds meta-DKS per-perspective stratification (v0.0.55).

## H1 + body sections

After the closing `---`, the body starts with **exactly one** `# H1` line — usually the title. Then a series of `## H2` sections.

Each BB type has *expected* H2 sections (per the templates):

- `concept` (term-dictionary): `## Definition`, `## Examples`, `## References`
- `argument`: `## Claim`, `## Reason`, `## Evidence`, `## Counter`
- `procedure` (how-to): `## Setup`, `## Steps`, `## Validation`, `## References`
- `model`: `## Architecture`, `## Components`, `## Relationships`, `## References`
- `empirical_observation`: `## Observation`, `## Method`, `## Result`, `## References`
- `hypothesis`: `## Hypothesis`, `## Reasoning`, `## Falsifiability`, `## References`
- `counter_argument`: `## Counter-claim`, `## Reason`, `## Strength`, `## References`
- `navigation`: `## Purpose`, `## Index`, `## Related Entry Points`

These are *recommendations* — the validator doesn't error on missing sections (yet), but the templates ship with them so notes start consistent.

## Run the format check

```bash
tessellum format check vault/resources/term_dictionary/term_warrant.md
```

Output format:

```
term_warrant.md:
  ERROR[tags] YAML-001: required field 'tags' missing
  WARNING[links] TESS-005: body link from 'concept' to 'argument' (...): BB-pair not in BB_SCHEMA@v1

validated 1 file(s); 1 with issues; 1 error(s), 1 warning(s), 0 info(s)
```

The CLI returns exit code 1 if any errors exist; warnings don't fail.

Check a whole directory:

```bash
tessellum format check vault/
# Recurses, validates every .md
```

## Common errors + fixes

| Error | What it means | Fix |
|---|---|---|
| `YAML-001` missing field | A required key is absent | Add the field. Check the template under `vault/resources/templates/` for the canonical shape. |
| `YAML-014` bad enum value | E.g. `status: dragons-here` | Use one of the allowed values in `tessellum.format.frontmatter_spec.VALID_STATUSES`. |
| `YAML-015` lowercase tag mismatch | `tags[0]: Resource` instead of `resource` | Tags are lowercase. |
| `TESS-001` folgezettel without parent | `folgezettel:` set but `folgezettel_parent:` missing | Add the parent FZ (or null for trail roots). |
| `TESS-004` counter_argument without arg link | A `counter_argument` note doesn't link to any `argument`-typed note | Add a markdown link to the attacked argument. |
| `LINK-003` link target does not exist | Markdown link points at a missing file | Fix the path or remove the link. |
| `TESS-005` BB-pair not in schema | Body link between BB types that don't have a declared edge | Acceptable as documentation (advisory only). Or propose a schema extension. |

## When format check is part of CI

CI runs `tessellum format check vault/` on every PR (v0.0.56+). Errors fail the build; warnings don't. If you're authoring a note that triggers a TESS-005 warning for a *legitimate* documentation cross-reference, leave it — the warning is informational, not blocking.

## Use the capture command instead of authoring by hand

The cleanest way to start a new note is:

```bash
tessellum capture argument my_new_argument --vault vault
# → writes vault/resources/analysis_thoughts/thought_my_new_argument.md
#   with the right frontmatter + status: draft + today's date + bb_schema_version
```

The capture command auto-populates the seven required fields from the template, leaves placeholders for the body, and (per v0.0.55) writes the current `bb_schema_version` so TESS-005 validates against the right schema.

Override the default destination + filename prefix when needed (per v0.0.57):

```bash
tessellum capture model my_algo --destination areas/tools --prefix tool_
# → vault/areas/tools/tool_my_algo.md
```

## Related Notes

- [`term_format_spec`](../term_dictionary/term_format_spec.md) — the formal spec this how-to demonstrates
- [`entry_building_block_index`](../../0_entry_points/entry_building_block_index.md) — pick the right `building_block:` value
- [`howto_first_vault`](howto_first_vault.md) — getting-started, prerequisite

## See Also

- [`skill_tessellum_format_check`](../skills/skill_tessellum_format_check.md) — the agent-invocable surface of the format validator
