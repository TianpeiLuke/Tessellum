---
tags:
  - entry_point
  - template
  - navigation
keywords:
  - navigation template
  - entry point template
  - master TOC template
  - index template
topics:
  - Note Format
  - Templates
language: markdown
date of note: 2026-05-10
status: template
building_block: navigation
---

# Entry: <Domain or Surface Name>

<!--
HOW TO USE THIS TEMPLATE:
1. Copy to `vault/0_entry_points/entry_<surface_name>.md`.
2. NOTE: navigation notes have `tags[0]: entry_point`, NOT `resource`. The
   entry-point bucket is the meta-navigation layer that indexes all PARA buckets.
3. Update YAML — tags[1] is usually `navigation`.
4. Fill required sections: Purpose, Index, Related Entry Points.
5. Remove this commentary block.

EPISTEMIC FUNCTION (Indexing): a navigation note routes readers to other notes.
It answers "Where does this live?" Navigation notes have no original content —
their value is in the curation. The strongest entry points are short, well-organized,
and link directly to the most-used downstream notes.

The Master TOC (`vault/0_entry_points/entry_master_toc.md`) is the top-level
navigation note. Per-surface entry points (skills, FZ trails, code repos,
templates, etc.) live alongside it. Avoid creating navigation notes for
surfaces that don't need them — sub-categories with < 5 notes don't warrant
a dedicated entry point.
-->

## Purpose

<One paragraph: what surface or domain does this entry point index? Who is the
intended reader? What question does it answer? If a reader can't tell within
3 seconds whether they're in the right entry point, the Purpose section is too
abstract.>

This entry point indexes <surface> for readers who want to <use case>.

## Index

<The actual routing. Group related notes into sections. Each row should give a
title, a one-line description (so the reader can decide whether to follow the
link), and the link itself.>

### <Section A>

| Note | What it covers |
|---|---|
| [Title](path/to/note.md) | <one-line description> |
| [Title](path/to/note.md) | <one-line description> |

### <Section B>

| Note | What it covers |
|---|---|
| [Title](path/to/note.md) | <one-line description> |

## Recently Added

<Optional but valuable. The 3-5 most recent additions to this surface, so
readers know what's new since they last visited.>

| Date | Note |
|---|---|
| YYYY-MM-DD | [Title](path/to/note.md) |

## How to Use

<Optional but recommended for richer entry points. Tell the reader the typical
workflow: do they read top-to-bottom? Pick by use case? Follow links by some
ordering? This converts a flat index into a guided tour.>

- **If you want to <use case A>**: start with [Note X](path.md)
- **If you want to <use case B>**: read [Note Y](path.md) first, then [Note Z](path.md)
- **For an audit**: run `<command or skill>` to surface integrity issues

## Related Entry Points

<Sibling navigation notes. Helps readers who are in the wrong entry point find
the right one without going back to the Master TOC.>

- [Master TOC](entry_master_toc.md) — top-level vault navigation
- [Related Entry A](entry_related_a.md) — <how it relates>
- [Related Entry B](entry_related_b.md) — <how it relates>

---

**Last Updated**: YYYY-MM-DD
**Status**: Active — <indexed-surface count>; <brief currency note>
