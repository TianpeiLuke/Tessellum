---
tags:
  - resource
  - template
  - yaml_header
keywords:
  - YAML header template
  - frontmatter template
  - YAML reference
  - common note header
  - note metadata
topics:
  - Note Format
  - Templates
language: markdown
date of note: 2026-05-10
status: template
building_block: navigation
---

# YAML Header Reference — Common Frontmatter Template for All Notes

<!--
HOW TO USE THIS TEMPLATE:
This file is a reference, not a copy-and-fill skeleton like the BB-type
templates. It documents the canonical YAML frontmatter shape — the 7 required
fields, common optional fields, type-specific extensions, and convention rules
— in one place a contributor can scan in 30 seconds.

For copy-and-fill BB-type skeletons (with body sections), use:
  template_concept / template_procedure / template_skill / template_model /
  template_argument / template_counter_argument / template_hypothesis /
  template_empirical_observation / template_experiment / template_navigation

For the prose specification, see [DEVELOPING.md § YAML Frontmatter Specification].
-->

## The 7 Required Fields

Every Tessellum note MUST have these 7 fields. The format validator (`scripts/check_note_format.py`) rejects notes missing any of them.

```yaml
---
tags:                          # ≥ 2 items, list format
  - <para-bucket>              # tags[0]: closed PARA enum
  - <second-category>          # tags[1]: open routing label
  - <topic-tag-1>              # tags[2..]: free-form, lowercase + underscore
  - <topic-tag-2>
keywords:                      # ≥ 3 recommended, list
  - <key-term-1>
  - <key-term-2>
  - <key-term-3>
topics:                        # ≥ 2 recommended, list
  - <topic-1>
  - <topic-2>
language: markdown             # almost always markdown; can be python/yaml/sql for code-bearing notes
date of note: YYYY-MM-DD       # KEY HAS SPACES — do NOT use date_of_note
status: active                 # closed enum (see status table below)
building_block: <bb>           # closed 8-element enum
---
```

## Closed Enums (must match exactly)

### `tags[0]` — PARA bucket (5 values)

| Value | When to use | Top-level dir |
|---|---|---|
| `resource` | Reference material — terms, how-tos, papers, snippets | `vault/resources/` |
| `area` | Ongoing responsibilities — code repos / teams / tools you maintain | `vault/areas/` |
| `project` | Active, time-bound effort with a defined endpoint | `vault/projects/` |
| `archive` | Past content — completed projects, retired material, archived experiments | `vault/archives/` |
| `entry_point` | Master TOC + per-surface entries (the navigation meta-bucket) | `vault/0_entry_points/` |

### `building_block` — Building Block (8 values)

| Value | Question | Function |
|---|---|---|
| `concept` | What is it called? | Naming |
| `procedure` | How do we act on this? | Doing |
| `model` | How is it structured? | Structuring |
| `hypothesis` | What will happen next? | Predicting |
| `argument` | Is the prediction true? | Claiming |
| `counter_argument` | What are the flaws? | Refuting |
| `empirical_observation` | What happened? | Testing |
| `navigation` | Where does this live? | Indexing |

### `status` — closed values

| Value | Semantic |
|---|---|
| `active` | Real, current content |
| `draft` | Work-in-progress real content |
| `archived` | Real content moved to `vault/archives/` |
| `deprecated` | Superseded but kept for reference |
| `superseded` | Replaced by a newer note (link to successor) |
| `stub` | Real note known to be incomplete |
| `placeholder` | Future-real note that doesn't exist yet (referenced from elsewhere) |
| `template` | Intentional skeleton — not real content |
| `wip`, `in_progress`, `proposal`, `development`, `planning` | Project-state markers |
| `legacy`, `disabled`, `cancelled` | Inactive / retired |
| `research`, `review`, `pending`, `completed` | Workflow markers |
| `production` | Live / shipped real content |

## Open Vocabularies

### `tags[1]` — second category (open routing label)

The routing label that determines the subdirectory. Open and extensible — add new values as your domain requires. Common values seen in this vault:

| Value | Lives in subdir | Used for |
|---|---|---|
| `terminology` | `term_dictionary/` | Concept definitions / glossary |
| `skill` | `skills/` | Skill canonical bodies |
| `how_to` | `how_to/` | User-facing how-to procedures |
| `analysis` | `analysis_thoughts/` | Argument / counter / hypothesis / observation trails |
| `digest` | `digest/` | Book / paper / external content digests |
| `code` | `code_snippets/` | Reusable code components |
| `papers` | `papers/` | Research paper notes |
| `code_repo` | `code_repos/` (under `areas/`) | Code repository documentation |
| `experiment` | `experiments/` (under `archives/`) | Pre-registered experiment archives |
| `navigation` | `0_entry_points/` | Entry-point indexes |
| `template` | `templates/` | These templates |
| `tool` | `tools/` | Tool / software documentation |
| `team` | `teams/` | Team / organizational entity |
| `faq` | `faqs/` | Q&A documentation |

Note that the directory name sometimes differs from the tag value (`terminology` → `term_dictionary/`, `code` → `code_snippets/`). The tag value is the canonical SoT; the directory follows it (with possible pluralization).

### `tags[2..]` — topic tags

Free-form. Lowercase, underscore-separated. Three common patterns:

- **Domain tags**: `knowledge_management`, `agentic_ai`, `retrieval`
- **Technique tags**: `embedding`, `pagerank`, `bm25`
- **Status / lifecycle tags**: `draft`, `pinned`, `core`

## Common Optional Fields

```yaml
last_updated: YYYY-MM-DD       # if note has been revised since `date of note`
author: <handle>               # for attribution (e.g., GitHub handle)
related_wiki: null             # external reference URL or null (kept for parent-vault compat; usually null)
```

## Type-Specific Field Extensions

### Folgezettel-trail notes

For notes that are part of an FZ trail (most commonly argument / counter / hypothesis / empirical_observation, but can apply to any BB type):

```yaml
folgezettel: "<id>"             # the FZ ID — string; can include letters/digits (e.g., "7", "10", "13a2", "14d1d1")
folgezettel_parent: "<id>"      # the parent FZ ID — or null for trail roots; or omit both fields for non-trail notes
```

#### When are FZ fields expected vs omitted

| Note type | FZ fields |
|---|---|
| Argument / counter_argument / hypothesis / empirical_observation in `vault/resources/analysis_thoughts/` | **Expected** — most participate in dialectic trails |
| Experiment in `vault/archives/experiments/` | **Expected** — almost always tied to upstream argument or hypothesis |
| Trail-root navigation note (rare; e.g., `entry_<trail>_trail.md` for a major argument trail) | Optional — usually omitted; presence indicates the entry point itself is the trail root |
| Term notes, how-tos, skill canonicals, code-repo docs, FAQs, papers, digests, models | **Omitted** — these are reference material, not trail nodes |

#### Trail-position rule

| Trail position | `folgezettel:` | `folgezettel_parent:` |
|---|---|---|
| Trail root (top of an argument chain) | `"<root-id>"` (e.g., `"14"`) | `null` |
| Trail child (mid-chain or leaf) | `"<child-id>"` (e.g., `"14d1"`) | `"<parent-id>"` (e.g., `"14d"`) |
| Non-trail note | omit | omit |

#### Both-or-neither rule (validator-enforced)

The two fields travel as a pair. Three valid configurations:

1. **Both filled** (trail child): `folgezettel: "14d1"`, `folgezettel_parent: "14d"`
2. **Filled-with-null** (trail root): `folgezettel: "14"`, `folgezettel_parent: null`
3. **Both omitted** (non-trail note): neither key present in YAML

**Invalid**: setting `folgezettel:` without `folgezettel_parent:` (or vice versa). The validator flags this as an error — it's the partial-fill bug, where an author forgot the second field.

The canonical key is `folgezettel_parent:` (long form). The shorter `fz_parent:` is accepted as an alias for backwards compatibility, but `folgezettel_parent:` is preferred and used in all Tessellum templates.

#### Why FZ fields are NOT required universally

FZ fields encode dialectic argument descent — a specific mechanism, not a universal note property. Forcing `folgezettel: null` on every term note adds noise without information; it would also dilute the signal (the *presence* of the field is meaningful precisely because it's selective). The 7 required fields are the ones every note benefits from; FZ fields benefit only the ~10–20% of notes participating in trails.

### Skill canonical bodies (`vault/resources/skills/skill_*.md`)

```yaml
related_skill_headers:
  - .claude/skills/<name>/SKILL.md
  - .kiro/skills/<name>/SKILL.md
pipeline_metadata: ./skill_<name>.pipeline.yaml   # or "none"
```

### Literature notes (`vault/resources/papers/lit_*.md`)

```yaml
paper_title: "Full Paper Title"
authors:
  - "Last, First"
  - "Last, First"
year: "2026"                   # quote the year — YAML treats unquoted 2026 as integer
paper_notes: <paper_id>
```

### Paper section notes (`vault/resources/papers/paper_*_*.md`)

```yaml
paper_id: <id>
section_type: <abstract|intro|method|...>
```

### Experiment notes (`vault/archives/experiments/experiment_*.md`)

```yaml
folgezettel: "<id>"             # if part of an FZ trail
folgezettel_parent: "<parent-id>"
```

(Note: experiments use `tags[0]: archive`, not `resource`. They live in the PARA Archive bucket.)

## Convention Rules (Hard Rules — Format Validator Enforces)

1. **`tags[0]` IS the PARA category.** Closed 5-element vocabulary. Mirrors the directory: `vault/resources/...` → `tags[0]: resource`, `vault/areas/...` → `tags[0]: area`, etc.

2. **`tags[1]` IS the second category** (the routing label). Open, extensible. Mirrors the subdirectory.

3. **`building_block` is a SEPARATE FIELD from tags.** The 8 BB types live in their own field; they are NOT part of `tags`.

4. **`date of note` uses spaces in the key.** YAML allows it; the indexer expects the spaced form. Do NOT change to `date_of_note`.

5. **Do NOT add a separate `note_second_category:` field.** `tags[1]` is the canonical SoT.

6. **All tags lowercase + underscores.** `knowledge_management`, NOT `Knowledge Management` or `knowledge-management`.

7. **Year-like strings must be quoted.** `year: "2026"`, NOT `year: 2026` (the latter is parsed as integer).

8. **Tags must form a list.** Use the YAML list syntax (one tag per line with `-` prefix). Avoid inline `[a, b, c]` syntax — the validator prefers the multiline form.

9. **FZ fields travel as a pair.** If `folgezettel:` is present, `folgezettel_parent:` must also be present (with a value or `null` for trail roots). If `folgezettel:` is absent, `folgezettel_parent:` must also be absent. Setting one without the other is a validation error — the partial-fill bug.

## Validation

```bash
python scripts/check_yaml_frontmatter.py --path <your-note>.md
python scripts/check_note_format.py --path <your-note>.md
```

The format checker enforces:
- All 7 required fields present
- `tags[0]` ∈ closed PARA enum
- `tags[1]` ∈ open list (warning if undocumented; not a hard fail)
- `building_block` ∈ closed 8-element enum
- `status` ∈ closed VALID_STATUSES
- `keywords` list with ≥ 3 items (warning if fewer)
- `topics` list with ≥ 2 items (warning if fewer)
- All tags lowercase + underscored
- Year strings quoted

## Three Worked Examples

### Example 1 — Term note (concept)

```yaml
---
tags:
  - resource
  - terminology
  - knowledge_management
  - retrieval
keywords:
  - PageRank
  - random walk
  - graph centrality
  - node importance
topics:
  - Information Retrieval
  - Graph Algorithms
language: markdown
date of note: 2026-05-09
status: active
building_block: concept
---
```

### Example 2 — FZ-trail argument note (mid-trail)

```yaml
---
tags:
  - resource
  - analysis
  - dialectic
  - cqrs
keywords:
  - CQRS
  - typed knowledge
  - System P
  - System D
  - synthesis
topics:
  - Knowledge System Architecture
  - Folgezettel Trails
language: markdown
date of note: 2026-04-28
status: active
building_block: argument
folgezettel: "7g1a1a1a1a1"
folgezettel_parent: "7g1a1a1a1a"
---
```

### Example 3 — Skill canonical body

```yaml
---
tags:
  - resource
  - skill
  - procedure
  - distill
  - retrieval
keywords:
  - search notes
  - tessellum-search
  - hybrid retrieval
topics:
  - Skill Procedures
  - Vault Tools
language: markdown
date of note: 2026-05-09
status: active
building_block: procedure
related_skill_headers:
  - .claude/skills/tessellum-search/SKILL.md
  - .kiro/skills/tessellum-search/SKILL.md
pipeline_metadata: none
---
```

## See Also

- [DEVELOPING.md § YAML Frontmatter Specification](../../../DEVELOPING.md#yaml-frontmatter-specification) — full prose spec
- [CONTRIBUTING.md § Note Format Standards](../../../CONTRIBUTING.md#note-format-standards) — contributor-facing summary
- [`templates/README.md`](README.md) — back to the templates directory
- [`term_building_block.md`](../term_dictionary/term_building_block.md) — the BB ontology referenced by `building_block:`
- [`term_para_method.md`](../term_dictionary/term_para_method.md) — the PARA scheme referenced by `tags[0]`
