---
tags:
  - entry_point
  - template
  - index
  - navigation
keywords:
  - entry point template
  - master TOC template
  - per-surface index
  - vault navigation
  - entry point pattern
topics:
  - Note Format
  - Templates
  - Vault Navigation
language: markdown
date of note: 2026-05-10
status: template
building_block: navigation
---

# Entry: <Domain or Surface Name>

<!--
HOW TO USE THIS TEMPLATE:
1. Copy to `vault/0_entry_points/entry_<surface>.md`. Entry-point notes ALWAYS
   live in this directory — that's the convention the database indexer relies on.
2. Filename convention: `entry_<surface>.md` for surface-specific entries
   (`entry_skill_catalog.md`, `entry_code_repos.md`, `entry_folgezettel_trails.md`),
   `entry_master_toc.md` for the top-level master TOC.
3. Update YAML — tags[0]=entry_point, tags[1]=index (most common; can also be
   `navigation`), additional tags describe the domain.
4. Fill the H2 sections. Common structure:
   - Purpose (always)
   - Quick Reference / Quick Stats (often — at-a-glance info)
   - One or more topical/categorical content sections
   - Related Entry Points (always — link to siblings)
   - References (optional)
5. Remove this commentary block.

EPISTEMIC FUNCTION (Indexing): an entry-point note routes readers to other
notes. It answers "Where does this live?" Entry points have no original
content — their value is in CURATION. The strongest entry points are short,
well-organized, and link directly to the most-used downstream notes.

Distinction from `template_navigation.md`: entry-point notes are the SPECIFIC
case of navigation notes that live in `vault/0_entry_points/`. Both share the
`navigation` BB type. Use this template (template_entry_point) when authoring
under `0_entry_points/`; use template_navigation for ad-hoc index notes that
live elsewhere in the vault.

Use `template_acronym_glossary.md` instead if you're authoring an
`acronym_glossary_<domain>.md` file (a more specialized entry-point shape with
per-acronym definitions).
-->

## Purpose

<One paragraph. What surface or domain does this entry point index? Who is the
intended reader? What question does it answer? A reader should be able to tell
within 5 seconds whether they're in the right entry point.>

This entry point indexes <surface> for readers who want to <use case>.

## Quick Reference

<Optional but valuable for entry points with > 20 indexed notes. A short table
of the most-common access patterns so a reader doesn't have to scroll. Format
as "I want to X → see Y".>

| If you want to... | Read |
|---|---|
| <use case 1> | Note Title |
| <use case 2> | Note Title |
| <use case 3> | Note Title |

## <Section A — Primary Categorization>

<Group indexed notes into a category. Each row should give a title, a one-line
description (so the reader can decide whether to follow the link), and the
link itself.

Common categorization schemes:
- By BB type (concept / procedure / model / argument / ...)
- By second-category (terms / how-tos / skills / papers / ...)
- By domain area (retrieval / capture / dialectic / ...)
- By lifecycle stage (active / archived / planned / ...)
- By workflow phase (capture → organize → distill → express)

Pick the scheme that fits the surface — there's no universal answer.>

| Note | What it covers |
|---|---|
| Title | <one-line description> |
| Title | <one-line description> |

## <Section B — Secondary Categorization>

<Optional. Use when the surface has > 30 indexed notes and benefits from
multiple categorization axes (e.g., the master TOC categorizes by both PARA
bucket and access pattern).>

| Note | What it covers |
|---|---|
| Title | <one-line description> |

## Statistics

<Optional but valuable for surfaces > 50 indexed notes. Headline counts that
help a reader gauge the scale.>

| Metric | Value |
|---|---|
| Total notes indexed | <count> |
| Active | <count> |
| Archived | <count> |
| Last updated | YYYY-MM-DD |

## Recently Added

<Optional. The 3-5 most recent additions to this surface, so readers know
what's new since they last visited.>

| Date | Note |
|---|---|
| YYYY-MM-DD | Title |

## How to Use

<Optional but recommended for richer entry points. Tell the reader the typical
workflow: do they read top-to-bottom? Pick by use case? Follow links by some
ordering? This converts a flat index into a guided tour.>

- **If you want to <use case A>**: start with Note X
- **If you want to <use case B>**: read Note Y first, then Note Z
- **For an audit**: run `<command or skill>` to surface integrity issues

## Related Entry Points

<Sibling navigation notes. Helps readers who are in the wrong entry point find
the right one without going back to the Master TOC.>

- Master TOC — top-level vault navigation
- Related Entry A — <how it relates>
- Related Entry B — <how it relates>

## References

<Optional. Include if the entry point itself cites authoritative sources
(e.g., a methodology that the indexed notes implement).>

- <Author, Year, Title, URL>

---

**Last Updated**: YYYY-MM-DD
**Status**: Active — <indexed-surface count>; <brief currency note>
