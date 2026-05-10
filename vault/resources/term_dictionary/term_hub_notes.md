---
tags:
  - resource
  - terminology
  - knowledge_management
  - zettelkasten
  - note_organization
keywords:
  - hub notes
  - hub zettels
  - Knotenpunkte
  - retrieval notes
  - navigation notes
  - entry points
  - trains of thought
  - Bob Doto
  - Johannes Schmidt
  - Niklas Luhmann
  - note finding
topics:
  - knowledge_management
  - writing methodology
language: markdown
date of note: 2026-03-11
status: active
building_block: concept
author: lukexie
---

# Term: Hub Notes

## Definition

**Hub notes** are navigational notes in the [Zettelkasten](term_zettelkasten.md) whose primary function is **retrieval** — helping the note maker find where specific trains of thought live in the slip-box. Each hub note contains a list of annotated links pointing to the **first note in a sequence** (a Folgezettel chain), organized around a broad topic area. Hub notes answer the question *"Where can I find my thinking about X?"* — they are maps, not arguments.

Doto defines hub notes as **"lists of links annotated by title (or some indication of the content)"** that make it easy to find areas of the Zettelkasten you'd like to explore. Their format is deliberately simple: a flat or near-flat list of entry points into developing trains of thought.

## Full Name

**Hub Notes** (German: *Knotenpunkte* — "node points")

Also known as:
- Hub Zettels (Schmidt's terminology)
- Navigation notes
- Topic entry points
- Retrieval notes

## How Hub Notes Work

A hub note takes this form:

```
Hub: [Topic Name]

- [[1a]] - Train of thought about X (brief annotation)
- [[3b2]] - Development of Y in relation to Z
- [[7c]] - Exploration of W from perspective of V
- [[12a1]] - Critique of Q connecting to R
```

Key characteristics:
- **Title/header** identifying the broad topic area
- **Annotated links** to first notes in various [Folgezettel](term_folgezettel.md) sequences
- **Brief descriptions** indicating what each train of thought covers
- **Minimal editorial structure** — a flat list, not an organized argument

The workflow: pull out a hub note, scan the trains of thought listed, pick one that interests you, then navigate to that region of the slip-box and explore.

## Hub Notes vs. Structure Notes (Doto's Key Distinction)

Doto's most important contribution is the sharp separation between **finding** notes and **developing** notes:

| Dimension | Hub Note | Structure Note |
|-----------|----------|----------------|
| **Primary function** | Retrieval / Finding | Development / Organizing |
| **What it contains** | Annotated link lists pointing to sequence starts | Organized arrangements of ideas into arguments |
| **What it does** | Points you to where trains of thought live | Arranges ideas into coherent arguments |
| **When to use** | When you want to locate and explore trains of thought | When you want to organize ideas for writing |
| **Analogy** | Table of contents / index / map | Outline / draft scaffold / workbench |
| **Relationship to writing** | Pre-writing navigation | Active writing preparation |

> "If you simply want to locate, read through, and explore different trains of thought developing in your zettelkasten, **use hub notes** to find the source of what you're looking for. If you want to better understand your ideas by organizing them into coherent arguments that can be used for writing and thinking, **use structure notes**."

The two work in tandem: you use hub notes to find relevant trains of thought, then create structure notes to develop those ideas for a specific writing project. Skipping either step leaves a gap.

## Hub Notes vs. Maps of Content (MOCs)

Hub notes are sometimes confused with Nick Milo's Maps of Content (MOCs) from the Linking Your Thinking (LYT) system. Doto argues they serve fundamentally different purposes:

| Dimension | Hub Note (Zettelkasten) | MOC (LYT) |
|-----------|------------------------|------------|
| **Primary function** | Navigation/retrieval: find where trains of thought live | Active thinking/sensemaking: where connections are made anew |
| **Relationship to connections** | Records/maps already-apparent connections | Creates and tests new connections |
| **System scope** | One note type in a writing-oriented system | Central organizational unit in a life operating system |

> "Instead of being a representation of previously made connections, MOCs are where connections are made anew."

Doto argues that MOCs in Milo's system serve a broader sensemaking function — "places to challenge notes, to see whether notes need to change" — while hub notes in the Zettelkasten serve a narrower navigational function.

## Luhmann's Practice

Johannes Schmidt (archivist of Luhmann's Nachlass at Bielefeld University) identified hub notes in Luhmann's physical Zettelkasten as:

> "Cards that function as nodes that feature an **above-average number of links** to other cards."

These hub Zettels functioned as **"highways between topics"**, providing access points to extensive parts of the collection. In Luhmann's system, hub notes emerged organically — Zettels that naturally accumulated many cross-references became navigational hubs — rather than being intentionally created as organizational scaffolding.

| Aspect | Detail |
|--------|--------|
| **Emergence** | Organic — arose from accumulated cross-references, not pre-planned |
| **Link density** | Above-average number of links compared to regular Zettels |
| **Function** | Connect distant parts of the collection; "highways between topics" |
| **Relationship to register** | Complementary — the keyword register pointed to hubs, hubs pointed to trains of thought |

## Common Misconceptions

### Hub notes and structure notes are the same thing
They are not interchangeable. Hub notes are for *finding*; structure notes are for *developing*. They serve categorically different functions even when they look superficially similar (both contain lists of links).

### Hub notes organize the Zettelkasten hierarchically
Hub notes do not impose hierarchy. They provide entry points into an otherwise non-hierarchical web. As Doto emphasizes: "The ideas found in your zettelkasten are not organized hierarchically, as if in an outline."

### More hub notes = better system
Luhmann's hub notes were emergent phenomena — Zettels that naturally accumulated above-average link density. Creating empty hub notes as pre-planned categories before having content defeats their purpose.

### Hub notes are the same as MOCs
While superficially similar, MOCs serve active sensemaking in a broad life operating system; hub notes serve retrieval in a narrow writing-oriented system.

## Comparison Across Systems

| System | Equivalent | Key Difference |
|--------|-----------|----------------|
| **Luhmann's Zettelkasten** | Hub Zettels (Knotenpunkte) | Emerged organically from above-average link density |
| **Doto's Zettelkasten** | Hub Notes | Explicitly defined as retrieval tools; deliberately created |
| **Ahrens (HTSN)** | Overview notes / [Index Notes](term_index_notes.md) | Less sharp distinction from structure notes |
| **Nick Milo (LYT)** | Maps of Content (MOCs) | MOCs are active thinking tools, not just retrieval aids |
| **Sascha Fast (zettelkasten.de)** | Middle-layer structure notes | Conflates what Doto separates; serves both finding and developing |
| **BASB (Forte)** | No direct equivalent | PARA is folder-based; no concept of navigational notes within note collections |
| **Vault** | Entry points (`0_entry_points/`) | Entry points are curated hub notes with tables-of-contents for each domain |

## Vault Implementation

In the vault, hub notes map to:
- **Entry points** (`0_entry_points/`) — the most direct implementation: curated lists of links organized by domain, each pointing to relevant vault notes. Entry points serve the exact retrieval function Doto describes: "Where can I find notes about X?"
- **Glossary entry points** (e.g., `acronym_glossary_cognitive_science.md`) — specialized hub notes organized as quick-reference lookups for term definitions
- **Reading log** (`entry_research_paper_reading_log.md`) — hub note for paper literature, linking to `lit_*` notes

The vault's entry point design — curated link lists with brief annotations, organized by domain — is a direct digital implementation of Doto's hub note concept.

## Related Terms

- [Index Notes](term_index_notes.md) — Luhmann's keyword register / Ahrens' index; complementary navigation tool that maps keywords to entry-point note IDs
- [Permanent Notes](term_permanent_notes.md) — the notes that hub notes point to; the core units organized into trains of thought
- [Folgezettel](term_folgezettel.md) — the sequencing system that creates the trains of thought hub notes navigate
- [Zettelkasten](term_zettelkasten.md) — the methodology in which hub notes serve as one of six note types
- [Fleeting Notes](term_fleeting_notes.md) — raw captures at the opposite end of the pipeline from hub notes
- [Literature Notes](term_literature_notes.md) — source summaries that feed the permanent notes hub notes organize
- [Trusted System](term_trusted_system.md) — hub notes contribute to system trust by making retrieval reliable
- [Slow Hunch](term_slow_hunch.md) — hub notes help surface slow hunches by making forgotten trains of thought findable
- [Liquid Network](term_liquid_network.md) — hub notes create navigational structure within the liquid network of ideas
- [Systems Thinking](term_systems_thinking.md) — hub notes create a reinforcing feedback loop: better navigation → more retrieval → more connections → richer trains of thought
- [Syntopical Reading](term_syntopical_reading.md) — hub notes implement syntopical structure, organizing notes across sources by topic like Adler's Syntopicon

## References

- Doto, B. (2024). *A System for Writing*. Chapter 6: hub notes as retrieval tools; pp. 114-115.
- Schmidt, J.F.K. (2018). "Niklas Luhmann's Card Index: The Fabrication of Serendipity." *Sociologica*, 12(1), 53-60. Hub Zettels as "highways between topics."
- [Bob Doto — The Difference Between Hub Notes and Structure Notes Explained](https://writing.bobdoto.computer/the-difference-between-hub-notes-and-structure-notes-explained/)
- [Bob Doto — Zettelkasten, Linking Your Thinking, and Nick Milo's Search for Ground](https://writing.bobdoto.computer/zettelkasten-linking-your-thinking-and-nick-milos-search-for-ground/)
- [Zettelkasten.de — The Money Is in the Hubs: Johannes Schmidt on Luhmann's Zettelkasten](https://zettelkasten.de/posts/zettelkasten-hubs/)
- [Digest: The Zettelkasten Iceberg](../digest/digest_zettelkasten_iceberg_sascha.md) — hub notes are a Level 2/3 construct; their quality depends on Level 4 thinking about what connections matter
- [Digest: Search Alone Is Not Enough](../digest/digest_search_not_enough_christian.md) — hub notes are the structural embodiment of curated links over search; they pre-answer "what matters here?"
- [Digest: A System for Writing](../digest/digest_system_for_writing_doto.md) — Doto's hub note concept and 6-type note taxonomy
- [Digest: How to Take Smart Notes](../digest/digest_smart_notes_ahrens.md) — Ahrens' overview/index notes as navigation tools
