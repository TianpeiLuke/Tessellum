---
tags:
  - resource
  - terminology
  - format
  - specification
  - regularization
keywords:
  - format specification
  - YAML frontmatter contract
  - validator issue codes
  - tag conventions
  - link rules
  - naming conventions
topics:
  - Note Format
  - Validation
  - Regularization
language: markdown
date of note: 2026-05-10
status: active
building_block: model
---

# Tessellum Format Specification

## Definition

The **Format Specification** is the contract every typed atomic note in a Tessellum vault must satisfy. It defines what makes a note *valid* — which YAML fields are required, which enums are closed, how tags compose, how links resolve, and how filenames map to vault directories. The specification is enforced by `tessellum format check`; this note is its human-readable counterpart.

When the validator reports an issue, it cites a stable code (`TESS-001`, `YAML-013`, `LINK-003`, etc.). Each code in this note maps to one fixable problem.

## Why a written spec

The validator is the source of truth in code; this note is the source of truth in vocabulary. Without a readable spec:

- An LLM agent authoring a note from a template can't tell what's optional vs required without running `tessellum format check` and parsing the error.
- A new contributor sees a `YAML-013` error and has nowhere to look up what `YAML-013` means.
- "What's a valid `building_block:` value?" is one Python-source read away, but should be one note-read away.

This is the **system regularization** in vault form. Programs enforce it; this note explains it.

## YAML Frontmatter Contract

Every note begins with a `---`-delimited YAML frontmatter block. The validator reads the frontmatter and checks each field against its rule.

### Required fields

| Field | Type | Rule | Code if missing |
|---|---|---|---|
| `tags` | list of strings | At least 1 item; lowercase letters/digits/underscores only | YAML-010 |
| `keywords` | list of strings | At least 3 items (recommended); short noun phrases | YAML-020 |
| `topics` | list of strings | At least 2 items (recommended); broader than keywords | YAML-030 |
| `language` | string | Lowercase identifier (e.g., `markdown`, `python`, `sql`) | YAML-040 |
| `date of note` | string | ISO-8601 date (`YYYY-MM-DD`); not a YAML date object | YAML-050 |
| `status` | string | One of: `active`, `archived`, `draft`, `superseded`, `template` | YAML-060 |
| `building_block` | string | One of the 8 BB types (see below) | YAML-100 |

### Closed enums

**`building_block:`** — exactly one of:

```
empirical_observation | concept | model | hypothesis |
argument | counter_argument | procedure | navigation
```

See [`entry_building_block_index.md`](../../0_entry_points/entry_building_block_index.md) for the picker table (what each BB type is for, where it lives, which others it connects to).

**`status:`** — exactly one of:

```
active      — note is in use
draft       — work in progress; not ready for citation
template    — only for templates (status: template; YAML-061 if used elsewhere)
archived    — superseded but kept for history
superseded  — replaced by a newer note (cite the replacement)
```

### Tag conventions (`tags[0]`, `tags[1]`, `tags[2..]`)

Tags are ordered. Position carries meaning:

| Position | Role | Examples |
|---|---|---|
| `tags[0]` | **PARA bucket** | `resource`, `project`, `area`, `archive` |
| `tags[1]` | **second category** (drives directory) | `terminology`, `how_to`, `skill`, `analysis`, `code_repo`, `code_snippets`, `index`, ... |
| `tags[2..]` | **domain tags** (free-form) | `pagerank`, `bayesian`, `causal_inference` |

Lowercase letters, digits, underscores only. No spaces. No camelCase. No leading/trailing underscores.

**Violations:**
- `YAML-015` — a tag contains uppercase or special characters
- `YAML-013` — `tags[0]` is not a valid PARA bucket

### Folgezettel fields (optional, both-or-neither)

If a note is part of a Folgezettel trail, both fields must be present:

| Field | Rule |
|---|---|
| `folgezettel` | The trail ID (e.g., `5e1c3a1a`) |
| `folgezettel_parent` | The parent trail ID (e.g., `5e1c3a1`) |

**Violations:**
- `TESS-001` — `folgezettel:` set but `folgezettel_parent:` missing
- `TESS-002` — `folgezettel_parent:` set but `folgezettel:` missing

### Forbidden fields

A small set of fields are intentionally banned:

| Field | Why forbidden | Code |
|---|---|---|
| `note_second_category` | `tags[1]` is the canonical source for second category; this field is redundant | TESS-003 |

When porting notes from another vault, strip these fields.

## Link Rules

Internal links between notes use markdown link syntax with **relative paths**:

```markdown
[link text](../resources/term_dictionary/term_other.md)
```

Rules:

| Rule | Code | Fix |
|---|---|---|
| Internal links must end in `.md` | LINK-001 | Add the extension |
| Relative paths only — no absolute paths | LINK-002 | Strip the leading `/` and use `../` or `./` |
| Link target file must exist | LINK-003 | Author the missing note, or fix the path |
| Note should have at least one outbound internal link | LINK-006 | Add a `## See Also` or `## Related Terms` section |

**No wikilinks (`[[...]]`)** anywhere in the body or frontmatter. Wikilinks are an Obsidian-specific shortcut that the validator and indexer don't parse.

**No markdown links inside YAML frontmatter.** Frontmatter is YAML, not markdown — links there are interpreted as strings.

## Filename + Directory Conventions

Tessellum maps capture flavor → filename prefix → directory. The capture registry is the source of truth (see `tessellum.capture.REGISTRY`); this table mirrors it.

| Flavor | Filename prefix | Directory |
|---|---|---|
| `concept` | `term_` | `resources/term_dictionary/` |
| `procedure` | `howto_` | `resources/how_to/` |
| `skill` | `skill_` | `resources/skills/` (+ paired `.pipeline.yaml`) |
| `model` | `term_` | `resources/term_dictionary/` |
| `argument` | `thought_` | `resources/analysis_thoughts/` |
| `counter_argument` | `thought_counter_` | `resources/analysis_thoughts/` |
| `hypothesis` | `thought_hypothesis_` | `resources/analysis_thoughts/` |
| `empirical_observation` | `thought_observation_` | `resources/analysis_thoughts/` |
| `experiment` | `experiment_` | `archives/experiments/` |
| `navigation` | *(none)* | `0_entry_points/` |
| `entry_point` | `entry_` | `0_entry_points/` |
| `acronym_glossary` | `acronym_glossary_` | `0_entry_points/` |
| `code_snippet` | `snippet_` | `resources/code_snippets/` |
| `code_repo` | `repo_` | `areas/code_repos/` |

Filename slugs are `[a-z0-9_]+` — same character class as tags.

## Validator Issue Codes — Quick Reference

When `tessellum format check` reports an issue, look it up here.

### Required-field codes (`YAML-NNN`)

| Code | Meaning |
|---|---|
| YAML-010 | `tags:` field missing or empty |
| YAML-013 | `tags[0]` is not a valid PARA bucket |
| YAML-014 | `tags[1]` is not a valid second category for this directory |
| YAML-015 | A tag is malformed (uppercase, special chars, etc.) |
| YAML-020 | `keywords:` field missing |
| YAML-021 | `keywords[]` has too few items |
| YAML-022 | A keyword is malformed |
| YAML-030 | `topics:` field missing |
| YAML-031 | `topics[]` has too few items |
| YAML-032 | A topic is malformed |
| YAML-040 | `language:` field missing |
| YAML-050 | `date of note:` field missing |
| YAML-051 | `date of note:` is not ISO-8601 (`YYYY-MM-DD`) |
| YAML-060 | `status:` field missing |
| YAML-061 | `status:` value is not in the closed enum |
| YAML-062 | `status: template` used outside `resources/templates/` |
| YAML-063 | A note in `resources/templates/` has `status: active` (should be `template`) |
| YAML-100 | `building_block:` field missing |
| YAML-101 | `building_block:` value is not in the closed enum |

### Tessellum-specific codes (`TESS-NNN`)

| Code | Meaning |
|---|---|
| TESS-001 | `folgezettel:` set but `folgezettel_parent:` missing |
| TESS-002 | `folgezettel_parent:` set but `folgezettel:` missing |
| TESS-003 | Forbidden field (`note_second_category`) used |

### Link codes (`LINK-NNN`)

| Code | Meaning |
|---|---|
| LINK-001 | Internal link missing `.md` extension |
| LINK-002 | Internal link uses absolute path (`/...`) instead of relative |
| LINK-003 | Link target file does not exist |
| LINK-006 | Note has no internal links (orphan) — warning, not error |

## How to fix an error

```bash
$ tessellum format check resources/term_dictionary/term_my_thing.md
  ERROR[tags] YAML-015: a tag contains characters outside [a-z0-9_]

validated 1 file(s); 1 with issues; 1 error(s), 0 warning(s), 0 info(s)
```

1. Look up `YAML-015` in the table above → "A tag is malformed."
2. Open the note, find the offending tag (usually one with uppercase or a hyphen).
3. Fix it (`my-tag` → `my_tag`, `MyTag` → `my_tag`).
4. Re-run `tessellum format check`. The error is gone.

The validator's job is to report exactly what's wrong, citing a stable code; this note's job is to explain each code in human terms.

## Related Terms

- [`term_building_block`](term_building_block.md) — the 8-type BB ontology (which `building_block:` value applies)
- [`entry_building_block_index`](../../0_entry_points/entry_building_block_index.md) — the BB picker matrix (one-line per type)
- [`term_para_method`](term_para_method.md) — the four PARA buckets used in `tags[0]`
- [`term_folgezettel`](term_folgezettel.md) — the trail mechanism `folgezettel:` fields encode
- [`template_yaml_header`](../templates/template_yaml_header.md) — the executable spec exemplar (templates are the format spec by example)

## See Also

- [`howto_first_vault`](../how_to/howto_first_vault.md) — practical walkthrough that uses these rules
- [`entry_master_toc`](../../0_entry_points/entry_master_toc.md) — the navigation root that points at this spec

---

**Last Updated**: 2026-05-10
**Status**: Active
