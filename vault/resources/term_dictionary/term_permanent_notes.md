---
tags:
  - resource
  - terminology
  - knowledge_management
  - zettelkasten
  - note_taking
  - writing
keywords:
  - permanent notes
  - main notes
  - Zettelkasten
  - atomic notes
  - one idea per note
  - self-contained
  - slip-box
  - note pipeline
  - Sönke Ahrens
  - Bob Doto
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

# Term: Permanent Notes

## Definition

**Permanent notes** are self-contained, context-independent ideas stored in the Zettelkasten (slip-box). Each note contains **one idea** written "as if for publication" — understandable without knowing the original context, linked to other permanent notes, and filed by retrieval context rather than topic. Permanent notes are the core building blocks of the Zettelkasten: they accumulate over time, form clusters through linking, and serve as the raw material for writing projects.

Doto uses the broader term **main notes** — "the fundamental building blocks of your future writing" — emphasizing their role as writing components rather than archival units.

## Full Name

**Permanent Notes** (German: *dauerhafte Notizen*)

Also known as:
- Main notes (Doto's terminology)
- Evergreen notes (Andy Matuschak's variant)
- Zettels (individual cards in Luhmann's system)
- Atomic notes (emphasizing the one-idea-per-note constraint)

## Purpose

Permanent notes are the product of intellectual work — the refined output of reading, thinking, and connecting. They solve the retrieval and recombination problem: by being atomic (one idea), self-contained (context-independent), and linked (connected to the network), they can be freely recombined into new arguments, papers, and projects that the writer never originally planned.

**Ahrens' key insight**: "The restriction to one idea per note is also the precondition to recombine them freely later."

## Characteristics

| Attribute | Detail |
|-----------|--------|
| **Format** | Structured; one idea, fully elaborated, with links |
| **Lifespan** | Permanent; the core of the slip-box |
| **Storage** | The Zettelkasten / slip-box |
| **Effort** | High; requires elaboration, connection-finding, and careful writing |
| **Standard** | "Written as if for publication" — understandable by a reader who has no context |
| **Atomicity** | One idea per note; the fundamental constraint |
| **Links** | Explicitly linked to related permanent notes; 1-2 keywords for retrieval |
| **Filing** | By context of future retrieval, not by topic of origin |

## The Atomicity Principle

The one-idea-per-note constraint is the most important design decision in the Zettelkasten:

| Why Atomicity Matters | Explanation |
|-----------------------|-------------|
| **Enables recombination** | Small, independent units can be freely rearranged into new structures |
| **Forces clarity** | Writing one idea fully requires understanding it completely |
| **Maximizes linkability** | A focused note can connect to many different contexts |
| **Prevents information hoarding** | Large notes become archives; atomic notes become tools |
| **Mirrors thinking** | Ideas are atomic; documents are not. The note should match the unit of thought |

## In the Note Pipeline

```
[Fleeting Notes] → [Literature Notes] → [Permanent Notes]
   (capture)         (source summary)     (atomic idea)
   temporary         reference manager    the slip-box
                                          ← YOU ARE HERE →
```

Permanent notes are created by synthesizing fleeting and literature notes. The processing step requires asking: *How does this connect to what I already know? What is the one idea here? Can I write it so someone else would understand without context?*

## Ahrens vs. Doto

| Aspect | Ahrens (Permanent Notes) | Doto (Main Notes) |
|--------|--------------------------|-------------------|
| **Name** | Permanent notes | Main notes (broader category) |
| **Key emphasis** | Self-contained; "written as if for print" | "Fundamental building blocks of future writing" |
| **Filing** | By context of retrieval; 1-2 keywords | Via folgezettel (alphanumeric IDs); eufriction forces connections |
| **Scope** | Strictly one idea | One idea, but emphasizes the idea's potential for writing output |
| **Development** | Clusters form bottom-up through linking | Trains of thought develop through sequential connections |

## Comparison Across Systems

| System | Equivalent | Key Difference |
|--------|-----------|----------------|
| **Zettelkasten** (Ahrens) | Permanent notes | Self-contained, linked, filed by context |
| **Zettelkasten** (Doto) | Main notes | Same function, broader framing for writing |
| **BASB** (Forte) | Intermediate Packets | IPs are project-oriented; permanent notes are idea-oriented |
| **Andy Matuschak** | Evergreen notes | Similar concept; Matuschak adds "evergreen" (continuously refined) |
| **Academic** | Research cards / index cards | Zettelkasten adds explicit linking and network effects |
| **Vault** | Term notes, area notes | Atomic, self-contained, linked — direct implementation |

## Vault Implementation

In the vault, permanent notes map to:
- **Term notes** (`term_*.md`) — the clearest permanent notes: one concept per note, self-contained definition, explicitly linked to related terms
- **Area notes** (`area_*.md`) — permanent notes at the program/domain level
- **Paper section notes** (`paper_*_algo.md`, etc.) — permanent notes synthesized from literature notes (`lit_*`)
- **Entry points** — hub notes that aggregate permanent notes by domain (Doto's hub note concept)

The vault's atomic note design — one concept per file, bidirectional links, graph-traversable — is a direct implementation of the permanent note principle.

## Related Terms

- [Fleeting Notes](term_fleeting_notes.md) — the raw captures that feed permanent note creation
- [Literature Notes](term_literature_notes.md) — the source summaries that inform permanent notes
- [Folgezettel](term_folgezettel.md) — the sequencing system for placing permanent notes in the slip-box
- [Hub Notes](term_hub_notes.md) — navigational notes that organize permanent notes into findable trains of thought
- [Index Notes](term_index_notes.md) — keyword-based entry points that lead to permanent notes in the slip-box
- [Knowledge Building Blocks](term_knowledge_building_blocks.md) — Sascha's six knowledge atoms that define what constitutes an atomic permanent note; the argument (premises + logical form + conclusion) is the fundamental atom
- [Zettelkasten](term_zettelkasten.md) — the methodology built around permanent notes as the core unit
- [Intermediate Packets](term_intermediate_packets.md) — Forte's project-oriented equivalent; permanent notes are idea-oriented
- [Elaborative Interrogation](term_elaborative_interrogation.md) — asking "why?" and "how?" when creating permanent notes produces richer connections
- [Compound Effect](term_compound_effect.md) — each permanent note adds marginal value to the network; knowledge compounds through connection
- [Adjacent Possible](term_adjacent_possible.md) — each new permanent note expands the adjacent possible of the knowledge graph
- [Liquid Network](term_liquid_network.md) — the slip-box as a liquid network where permanent notes collide to generate insight
- [Slow Hunch](term_slow_hunch.md) — permanent notes incubate over time, connecting with future notes to complete slow hunches
- [Trusted System](term_trusted_system.md) — permanent notes work only in a trusted system with reliable retrieval
- [BASB](term_basb.md) — Forte's complementary approach; BASB uses Progressive Summarization where Zettelkasten uses permanent notes

## References

- Ahrens, S. (2022). *How to Take Smart Notes* (2nd ed.). Chapter 11: "Take Smart Notes."
- Doto, B. (2024). *A System for Writing*. Part I: "Making Notes."
- [Digest: How to Take Smart Notes](../digest/digest_smart_notes_ahrens.md) — the definitive guide to permanent note creation
- [Digest: A System for Writing](../digest/digest_system_for_writing_doto.md) — practical examples with actual notes shown
- [Digest: Building a Second Brain](../digest/digest_building_second_brain_forte.md) — Forte's Intermediate Packets as a complementary concept
- [Digest: The Zettelkasten Iceberg](../digest/digest_zettelkasten_iceberg_sascha.md) — permanent notes are Level 3 output: notes written to benefit the system itself, not just the current project
