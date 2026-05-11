---
tags:
  - resource
  - terminology
  - knowledge_management
  - zettelkasten
  - note_taking
  - reading
keywords:
  - literature notes
  - reference notes
  - Zettelkasten
  - active reading
  - source summary
  - note pipeline
  - Sönke Ahrens
  - Bob Doto
  - Niklas Luhmann
topics:
  - knowledge_management
  - writing methodology
  - reading
language: markdown
date of note: 2026-03-11
status: active
building_block: concept
author: lukexie
---

# Term: Literature Notes

## Definition

**Literature notes** are concise summaries of source material written in your own words, with full bibliographic reference. They represent the second stage of the Zettelkasten note pipeline — the bridge between raw capture ([fleeting notes](term_fleeting_notes.md)) and refined understanding ([permanent notes](term_permanent_notes.md)). The critical requirement is **rephrasing**: literature notes must never be verbatim copies. The act of translating source material into your own language is where genuine understanding begins.

Doto calls these **reference notes** — functionally identical but emphasizing their role as citeable source references rather than personal summaries.

## Full Name

**Literature Notes** (German: *Literaturnotizen*)

Also known as:
- Reference notes (Doto's terminology)
- Source notes
- Reading notes
- Bibliographic notes

## Purpose

Literature notes solve the comprehension problem: reading feels like understanding, but passive consumption creates an illusion of knowledge. Writing a literature note forces active engagement — you must select what matters, rephrase it in your own words, and record the source. This leverages the **generation effect**: self-generated content is remembered far better than passively received content.

**Key principles**:
1. **Selective** — not everything from a source, only what is relevant to your thinking
2. **In your own words** — never copy verbatim; rephrasing forces understanding
3. **With bibliographic reference** — always traceable back to the source
4. **Brief** — capture the essence, not the entirety

## Characteristics

| Attribute | Detail |
|-----------|--------|
| **Format** | Structured; includes source citation + key ideas in own words |
| **Lifespan** | Permanent; stored in reference management system |
| **Storage** | Reference manager (e.g., Zotero) or dedicated folder — NOT the slip-box |
| **Effort** | Moderate; requires active reading and rephrasing |
| **Purpose** | Bridge between source material and personal understanding |
| **Content** | Selective summaries, key arguments, relevant data, own-word restatements |

## In the Note Pipeline

```
[Fleeting Notes] → [Literature Notes] → [Permanent Notes]
   (capture)         (source summary)     (atomic idea)
   temporary         reference manager    the slip-box
                     ← YOU ARE HERE →
```

Literature notes serve as the processing step where external knowledge is internalized. They are not yet atomic ideas (that's the permanent note's job) — they are source-anchored summaries that can feed multiple permanent notes.

## Ahrens vs. Doto

| Aspect | Ahrens (Literature Notes) | Doto (Reference Notes) |
|--------|--------------------------|----------------------|
| **Name** | Literature notes | Reference notes |
| **Storage** | Reference management system (Zotero) | Dedicated folder |
| **Key emphasis** | Own words; never verbatim | Citation accuracy; extracted passages with source info |
| **Relationship to main notes** | Feed permanent notes during daily processing | Feed main notes during note-making sessions |
| **Scope** | Selective (only what matters to your thinking) | Selective (only what matters to your writing) |

## Comparison Across Systems

| System | Equivalent | Key Difference |
|--------|-----------|----------------|
| **Zettelkasten** (Ahrens) | Literature notes | Written in own words; stored in reference manager |
| **Zettelkasten** (Doto) | Reference notes | Includes extracted passages with citations; dedicated folder |
| **BASB** (Forte) | Progressive Summarization Layer 1-3 | BASB uses highlighting (bold/highlight); Zettelkasten requires rephrasing |
| **GTD** (Allen) | Reference material | GTD stores but doesn't process references for insight |
| **Academic practice** | Annotated bibliography | Similar format; Zettelkasten adds connection to permanent notes |

## Vault Implementation

In the vault, literature notes map to:
- **`lit_*` notes** — the index cards for digested papers. Each `lit_*` note captures paper metadata, abstract, and synthesized summaries with source citations — exactly the function of a literature note
- **`paper_*` section notes** — deeper literature notes that capture specific sections (intro, algorithm, experiments) in the reader's own words, with `<!-- VERIFY -->` and `<!-- REWRITE -->` markers for the elaboration step
- **Digest notes** — `digest_*` files are literature notes for books and articles: source-anchored summaries with key frameworks extracted

## Related Terms

- [Fleeting Notes](term_fleeting_notes.md) — the predecessor: raw captures that feed literature note creation
- [Permanent Notes](term_permanent_notes.md) — the successor: atomic ideas synthesized from literature notes
- [Folgezettel](term_folgezettel.md) — the sequencing system for permanent notes; literature notes are pre-folgezettel
- [Zettelkasten](term_zettelkasten.md) — the methodology that defines the note pipeline
- [Progressive Summarization](term_progressive_summarization.md) — Forte's alternative processing method using highlighting layers rather than rephrasing
- [Elaborative Interrogation](term_elaborative_interrogation.md) — asking "why?" and "how?" during literature note creation deepens understanding
- [Retrieval Practice](term_retrieval_practice.md) — writing literature notes from memory (after closing the book) exercises retrieval
- [Desirable Difficulties](term_desirable_difficulties.md) — rephrasing in own words is harder than highlighting but produces deeper learning
- [BASB](term_basb.md) — Forte's system uses Progressive Summarization for the same processing step where Zettelkasten uses literature notes
- [Hub Notes](term_hub_notes.md) — hub notes navigate the slip-box to find trains of thought fed by literature notes
- [Index Notes](term_index_notes.md) — keywords chosen for the register come from the literature note processing step
- Analytical Reading — literature notes are the Zettelkasten output of Adler's interpretive stage (Stage 2: come to terms, grasp propositions, know arguments)

## References

- Ahrens, S. (2022). *How to Take Smart Notes* (2nd ed.). Chapter 2, 10.
- Doto, B. (2024). *A System for Writing*. Part I: "Making Notes."
- [Digest: How to Take Smart Notes](../digest/digest_smart_notes_ahrens.md) — theory of literature note creation
- [Digest: A System for Writing](../digest/digest_system_for_writing_doto.md) — practical examples of reference note creation
- Digest: Make It Stick — generation effect and elaboration as learning mechanisms
