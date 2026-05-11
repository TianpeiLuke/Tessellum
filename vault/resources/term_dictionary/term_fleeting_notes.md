---
tags:
  - resource
  - terminology
  - knowledge_management
  - zettelkasten
  - note_taking
keywords:
  - fleeting notes
  - Zettelkasten
  - temporary captures
  - quick notes
  - note pipeline
  - Sönke Ahrens
  - Niklas Luhmann
topics:
  - knowledge_management
  - writing methodology
language: markdown
date of note: 2026-03-11
status: active
building_block: concept
author: lukexie
---

# Term: Fleeting Notes

## Definition

**Fleeting notes** are temporary, informal captures of ideas, thoughts, or reactions — "mere reminders of what is in your head" (Ahrens). They are the first stage of the Zettelkasten note pipeline, designed to be processed into [literature notes](term_literature_notes.md) or [permanent notes](term_permanent_notes.md) within 1-2 days, then discarded. Fleeting notes have no required structure, no formatting standards, and no permanent home — they exist only to prevent ideas from being lost before they can be properly elaborated.

## Full Name

**Fleeting Notes** (German: *flüchtige Notizen*)

Also known as:
- Scratch notes
- Quick captures
- Jottings
- Inbox items (in GTD/BASB terminology)

## Purpose

Fleeting notes solve the capture problem: ideas arrive at inconvenient times, and working memory is severely limited (~4 items). Without a capture mechanism, valuable ideas are lost. Fleeting notes provide a zero-friction capture point that separates the *moment of inspiration* from the *work of elaboration*.

**Key constraint**: Fleeting notes must be processed within 1-2 days or explicitly discarded. "Just collecting unprocessed fleeting notes inevitably leads to chaos" (Ahrens). The danger is confusing capture with understanding — the [collector's fallacy](https://zettelkasten.de/posts/collectors-fallacy/).

## Characteristics

| Attribute | Detail |
|-----------|--------|
| **Format** | Unstructured; any medium (notebook, phone, napkin, voice memo) |
| **Lifespan** | Temporary; process within 1-2 days or discard |
| **Storage** | Temporary location (inbox, notebook, capture app) — NOT the slip-box |
| **Effort** | Minimal; speed of capture matters more than quality |
| **Purpose** | Prevent idea loss; bridge the gap between inspiration and elaboration |
| **Content** | Fragments, reactions, questions, connections, hunches |

## In the Note Pipeline

```
[Fleeting Notes] → [Literature Notes] → [Permanent Notes]
   (capture)         (source summary)     (atomic idea)
   temporary         reference manager    the slip-box
   1-2 day shelf     permanent            permanent
   life
```

Fleeting notes are the raw material. They become useful only when processed into literature notes (if sourced from reading) or permanent notes (if sourced from thinking). Unprocessed fleeting notes are cognitive debt.

## Comparison Across Systems

| System | Equivalent | Key Difference |
|--------|-----------|----------------|
| **Zettelkasten** (Ahrens) | Fleeting notes | Must be processed or discarded within 1-2 days |
| **Zettelkasten** (Doto) | Fleeting notes | Same concept; emphasizes "note-making" as the transformation step |
| **GTD** (Allen) | Inbox items | GTD processes into next actions; Zettelkasten processes into permanent notes |
| **BASB** (Forte) | Capture phase | BASB captures more broadly (bookmarks, highlights); Zettelkasten captures own thoughts |
| **Commonplace book** | Marginalia / jottings | Historical equivalent; no processing pipeline |

## Vault Implementation

In the vault, fleeting notes map to:
- **Paper reading captures**: Raw highlights and reactions during PDF reading, before they are processed into `paper_*` section notes
- **Inbox items**: Ideas captured during daily work that haven't been processed into term notes, area notes, or SOPs
- **`<!-- VERIFY -->` markers**: Temporary annotations in lit notes that flag content needing scientist review — a form of fleeting note embedded in permanent structure

## Related Terms

- [Permanent Notes](term_permanent_notes.md) — the destination: self-contained atomic ideas in the slip-box
- [Literature Notes](term_literature_notes.md) — the intermediate step: source summaries in your own words
- [Folgezettel](term_folgezettel.md) — the sequencing system for filing permanent notes; not applicable to fleeting notes
- [Zettelkasten](term_zettelkasten.md) — the methodology that defines the three note types
- [Open Loops](term_open_loops.md) — uncaptured fleeting notes create open loops that consume working memory (Zeigarnik effect)
- [Trusted System](term_trusted_system.md) — fleeting notes work only when the processing pipeline is trusted to handle them
- [Desirable Difficulties](term_desirable_difficulties.md) — the effort of transforming fleeting notes into permanent notes creates productive difficulty that deepens understanding
- [BASB](term_basb.md) — Forte's Capture phase is a broader version of fleeting note capture
- [Hub Notes](term_hub_notes.md) — hub notes are at the opposite end of the pipeline from fleeting notes; fleeting notes are captured, hub notes help retrieve
- [Index Notes](term_index_notes.md) — index entries help locate the permanent notes that originated as fleeting captures
- Zeigarnik Effect — capturing a fleeting note discharges the Zeigarnik tension for an intellectual open loop

## References

- Ahrens, S. (2022). *How to Take Smart Notes* (2nd ed.). Chapter 2: "Everything You Need to Do."
- Doto, B. (2024). *A System for Writing*. Part I: "Making Notes."
- [Digest: How to Take Smart Notes](../digest/digest_smart_notes_ahrens.md) — the definitive guide to the note pipeline
- [Digest: A System for Writing](../digest/digest_system_for_writing_doto.md) — practical examples of fleeting → main note transformation
- [Digest: The Zettelkasten Iceberg](../digest/digest_zettelkasten_iceberg_sascha.md) — the Evernote Effect (passive capture without processing) is a Level 1 failure mode where fleeting notes never become permanent notes
