---
tags:
  - resource
  - how_to
  - getting_started
  - onboarding
keywords:
  - first vault
  - getting started
  - tessellum tutorial
  - capture index search
  - composer pipeline
topics:
  - Getting Started
  - Vault Workflow
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
---

# How To: Your First Tessellum Vault

## Overview

This is the 8-step walkthrough every new user should run after `pip install tessellum`. It starts with an empty directory and ends with a vault that has its first typed atomic note authored, validated, indexed, searchable, and (optionally) running through Composer. Total time: 10–15 minutes.

The vocabulary in this walkthrough is defined in [`acronym_glossary_tessellum_foundations`](../../0_entry_points/acronym_glossary_tessellum_foundations.md); the format rules are in [`term_format_spec`](../term_dictionary/term_format_spec.md); the BB-type picker is in [`entry_building_block_index`](../../0_entry_points/entry_building_block_index.md). Don't read those first — run this how-to, then read them when a step refers to them.

## Prerequisites

- Python 3.11+
- A terminal
- ~50 MB free disk space for the install + indexed embeddings

## Setup

```bash
pip install tessellum
tessellum --version          # → tessellum 0.0.30 (or later)
```

If `tessellum --version` doesn't print, the install didn't finish — check for `ImportError` messages above and verify `pip show tessellum`.

## Steps

### 1. Scaffold a vault

```bash
tessellum init my-vault
cd my-vault
ls 0_entry_points/ resources/term_dictionary/ resources/templates/
```

**Expected:** Three directories appear with content. `0_entry_points/` has `entry_master_toc.md` + `entry_acronym_glossary.md` + `entry_building_block_index.md` + 6 glossary files. `resources/term_dictionary/` has 12 term notes (11 foundation terms + `term_format_spec`). `resources/templates/` has 15 templates.

This is your seed. Read `0_entry_points/entry_master_toc.md` for the navigation root — it points at the foundations glossary, the BB picker, this how-to, and the per-vault reading order.

### 2. Capture your first note

Pick the BB type using the picker matrix ([`entry_building_block_index`](../../0_entry_points/entry_building_block_index.md)). For "what is PageRank?" the question matches *What is it called?* → BB type is `concept`.

```bash
tessellum capture concept page_rank
```

**Expected:**
```
created: ./resources/term_dictionary/term_page_rank.md
  flavor:  concept
  next:    fill placeholders, then `tessellum format check ./resources/term_dictionary/term_page_rank.md`
```

The capture command copied `template_concept.md` to the right directory with the right filename prefix and stripped the HOW-TO-USE commentary block. The note is now a valid skeleton.

### 3. Fill the template

Open `resources/term_dictionary/term_page_rank.md` in your editor. Replace the placeholder content with real content. Required sections are listed in the picker matrix — for `concept`, you need `## Definition`, `## Examples`, `## References`.

Minimal example:

```markdown
## Definition

PageRank is the link-analysis algorithm Google's original search engine used.
It assigns each node a probability equal to the long-run fraction of time a
random walker spends at that node...

## Examples

- Web search: nodes are pages, edges are hyperlinks.
- Citation networks: nodes are papers, edges are citations.

## References

- Page, L. et al. (1999). *The PageRank Citation Ranking: Bringing Order to the Web.*
```

### 4. Validate

```bash
tessellum format check resources/term_dictionary/term_page_rank.md
```

**Expected:**
```
validated 1 file(s); 0 with issues; 0 error(s), 0 warning(s), 0 info(s)
```

If you see errors, look up the code (e.g., `YAML-015`) in [`term_format_spec`](../term_dictionary/term_format_spec.md) — it tells you exactly what to fix.

### 5. Index the vault

```bash
tessellum index build
```

**Expected:** A line about loading the embedding model, then "indexed N notes" where N matches `find . -name '*.md' | wc -l`. The first run is slow (~2 seconds for the embedding model load); subsequent runs are fast.

The index lands in `data/tessellum.db` — one SQLite file with the notes table, the link graph, FTS5 lexical index, and `vec0` dense embeddings.

### 6. Search

```bash
tessellum search "PageRank"
```

**Expected:** A ranked list with `term_page_rank.md` at or near the top. Default is hybrid (BM25 + dense + RRF); add `--bm25` / `--dense` / `--bfs` for explicit strategies, or `tessellum filter --tag concept` for direct metadata filtering.

### 7. Capture a skill (with paired pipeline sidecar)

Skills are agent-executable procedures. Capture one:

```bash
tessellum capture skill my_first_skill
```

**Expected:** Two files appear under `resources/skills/`:
- `skill_my_first_skill.md` (the canonical procedure)
- `skill_my_first_skill.pipeline.yaml` (the Composer typed-contract sidecar)

The two are linked by `<!-- :: section_id = X :: -->` anchors in the canonical and matching `section_id:` entries in the sidecar. Together they define a typed DAG that Composer can compile + execute.

### 8. Compose

```bash
tessellum composer validate resources/skills/skill_my_first_skill.md
tessellum composer compile  resources/skills/skill_my_first_skill.md
```

**Expected:** Both report `OK` (or report contract violations if you've drifted from the schema). `validate` is light (cross-file consistency); `compile` is heavier (full DAG check). If you want to execute the skill against canned inputs:

```bash
tessellum composer run resources/skills/skill_my_first_skill.md
```

That runs through MockBackend (no API key needed). For real Claude calls, install the optional dependency:

```bash
pip install tessellum[agent]
export ANTHROPIC_API_KEY=sk-ant-...
tessellum composer run resources/skills/skill_my_first_skill.md --backend anthropic
```

## Validation

You're done with the basics when all of the following work:

| Check | Command | Expected |
|---|---|---|
| Vault has notes | `find . -name '*.md' \| wc -l` | ≥ 36 (35 seed files + your authored note) |
| Format passes | `tessellum format check .` | "validated N file(s); 0 error(s)" |
| Index is built | `ls -la data/tessellum.db` | File exists, > 0 bytes |
| Search resolves | `tessellum search "PageRank"` | Your note appears in the ranked list |
| Skill validates | `tessellum composer validate resources/skills/` | All skills `OK` |

## Going further

You now have a working vault, the foundation vocabulary, and the format spec. Next:

- **Add more notes.** Each new note picks a BB type from the picker matrix and goes through capture → fill → format check.
- **Grow a trail.** Add `folgezettel:` + `folgezettel_parent:` fields to link notes into a Folgezettel descent ([`term_folgezettel`](../term_dictionary/term_folgezettel.md)).
- **Run a skill end-to-end.** Author a real skill canonical + sidecar pair, then `tessellum composer run` it against a leaves JSON file — the typed DAG drives the agent calls.
- **Customize the templates.** All 15 templates live in `resources/templates/` — edit them; future captures use your edits.

## Related Entry Points

- [`entry_master_toc`](../../0_entry_points/entry_master_toc.md) — vault navigation root
- [`entry_building_block_index`](../../0_entry_points/entry_building_block_index.md) — the BB picker matrix
- [`entry_acronym_glossary`](../../0_entry_points/entry_acronym_glossary.md) — all glossaries

## Related Terms

- [`term_format_spec`](../term_dictionary/term_format_spec.md) — the rules `tessellum format check` enforces
- [`term_building_block`](../term_dictionary/term_building_block.md) — depth on the 8-type ontology

---

**Last Updated**: 2026-05-10
**Status**: Active
