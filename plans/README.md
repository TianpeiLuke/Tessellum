# Tessellum Plans

Top-level home for **project-management planning documents** — milestones, layout changes, refactor scopes, release ship-lists.

## What lives here

Plans capture **decisions about how Tessellum is built**. Each plan is a single markdown file with the standard Tessellum YAML frontmatter.

Plans are NOT typed atomic notes:

- They're project-state, not knowledge content.
- They have a lifecycle (`active` → `completed` / `archived` / `superseded`), tracked via the `status:` YAML field.
- They live OUTSIDE both System P (capture) and System D (retrieval) — see [`plan_cqrs_repo_layout.md`](plan_cqrs_repo_layout.md) for the framing.

## Filename convention

`plan_<topic_or_initiative>.md` — short, descriptive, lowercase with underscores. Examples:

- `plan_v01_src_tessellum_layout.md`
- `plan_cqrs_repo_layout.md`

## YAML frontmatter

```yaml
---
tags:
  - project              # or `area` for ongoing initiatives
  - plan
  - <other topic tags>
keywords: [...]          # ≥ 3 entries
topics: [...]            # ≥ 2 entries
language: markdown
date of note: YYYY-MM-DD
status: active           # active | completed | archived | superseded
building_block: procedure
---
```

## Recommended H2 sections

`## Problem` → `## Why This Matters` (when load-bearing) → `## Design Principles` → `## Proposed <Approach>` → `## Migration Steps` / `## Order of Operations` → `## Open Questions` → `## See Also`

## Validation

Plans validate alongside vault notes:

```bash
tessellum format check plans/
```

The CLI's non-note skip list excludes this `README.md`.

## Status as a YAML field, not a folder

We do **not** use `plans/active/`, `plans/completed/` subdirectories. Status changes via a YAML edit, not a file move — keeps history clean and avoids move-churn.
