---
tags:
  - resource
  - terminology
  - knowledge_management
  - zettelkasten
  - note_organization
keywords:
  - index notes
  - keyword register
  - Schlagwortregister
  - Schlagwortverzeichnis
  - entry points
  - navigation
  - keyword index
  - sparse indexing
  - Niklas Luhmann
  - Sönke Ahrens
  - Johannes Schmidt
topics:
  - knowledge_management
  - writing methodology
language: markdown
date of note: 2026-03-11
status: active
building_block: concept
author: lukexie
---

# Term: Index Notes (Keyword Register)

## Definition

**Index notes** are the keyword-based entry points into a [Zettelkasten](term_zettelkasten.md), mapping topic keywords to a small number of note IDs where relevant trains of thought begin. In Luhmann's physical system, the index took the form of a **Schlagwortregister** (keyword register) — a separate lookup artifact listing keywords with corresponding Zettel numbers. The critical design choice is **deliberate sparsity**: each keyword points to only **one to four notes**, not an exhaustive list. The register gets you *into the neighborhood*; internal linking (Folgezettel and cross-references) does the rest.

Ahrens emphasizes that keywords should be chosen "with an eye towards the topics you are working on or interested in, **never by looking at the note in isolation**." The writer asks: *"In which circumstances will I want to stumble upon this note, even if I forget about it?"*

## Full Name

**Index Notes** / **Keyword Register** (German: *Schlagwortregister* or *Schlagwortverzeichnis*)

Also known as:
- Keyword index
- Register
- Topic index
- Entry-point index
- Overview notes (Ahrens' related concept)

## How the Register Functions

Luhmann's navigation operated in a specific sequence:

```
[Keyword Register] → [Entry-Point Note] → [Folgezettel Sequence] → [Cross-References]
     (enter)              (land)              (follow train)          (branch)
```

1. **Enter** via the keyword register (find an entry point for a topic)
2. **Land** on one of 1-4 referenced notes
3. **Follow** [Folgezettel](term_folgezettel.md) sequences (notes numbered 9, 9a, 9a1, 9b, etc.)
4. **Branch** via cross-references to other parts of the Zettelkasten
5. **Discover** unexpected connections through the network structure

The register was a *gateway*, not a comprehensive index. Once inside the Zettelkasten, navigation relied entirely on the internal linking structure.

## Deliberate Sparsity

The most counterintuitive design principle of the keyword register is its intentional incompleteness.

| Statistic | Detail |
|-----------|--------|
| **Zettelkasten II size** | ~67,000 notes |
| **Keywords in register** | ~3,200 |
| **References per keyword** | 1-4 (rarely more) |
| **Coverage** | Intentionally incomplete — most notes NOT directly indexed |

Johannes Schmidt (archivist of Luhmann's Nachlass) explains:

> "The file's keyword index makes no claim to providing a complete list of all cards in the collection that refer to a specific term. Rather, Luhmann typically listed only **one to four places** where the term could be found in the file, the idea being that all other relevant entries in the collection could be quickly identified via the internal system of references."

### Why Sparsity Works

| Reason | Explanation |
|--------|-------------|
| **Self-indexing** | The Zettelkasten is self-indexing through Folgezettel and cross-references; find one note and you can reach all related notes |
| **Forces discovery** | Sparse indexing means you navigate through connections, encountering unexpected material along the way |
| **Prevents archive thinking** | Exhaustive indexing treats the system as storage ("put in, take out"); sparse indexing treats it as a thinking partner |
| **Fabricates serendipity** | The combination of sparse entry and dense internal linking produces surprise encounters that fuel creative thinking |

Ahrens captures the philosophy:

> "Focusing exclusively on the index would basically mean that we always know upfront what we are looking for — we would have to have a fully developed plan in our heads. But **liberating our brains from the task of organizing the notes is the main reason we use the slip-box**."

## The Archivist vs. Writer Mindset

Ahrens draws a fundamental distinction in how to choose keywords:

| Mindset | Question Asked | Result |
|---------|---------------|--------|
| **Archivist** | "Which keyword is the most fitting?" | Files by category; retrieves only what was explicitly stored |
| **Writer** | "In which circumstances will I want to stumble upon this note?" | Files by future context; enables unexpected retrieval |

A psychologist's note about decision-making biases filed under the generic keyword "misjudgements" will only surface when thinking about misjudgements. The same note filed under "capital allocation problems" becomes discoverable in a completely different, potentially more productive context.

Keywords should be assigned **by retrieval context, not by topic of origin**.

## Index Notes vs. Hub Notes

Index notes and [hub notes](term_hub_notes.md) are complementary but distinct navigation tools:

| Dimension | Index Notes / Register | Hub Notes |
|-----------|----------------------|-----------|
| **Format** | Keyword → 1-4 note IDs (lookup table) | Annotated link lists within a note |
| **Location** | Separate artifact (outside the Zettelkasten) | Inside the Zettelkasten (a Zettel itself) |
| **Creation** | Deliberately maintained as keywords arise | Emerge organically from above-average link density |
| **Granularity** | Keyword-level (broad topic) | Train-of-thought level (specific sequences) |
| **Density** | Very sparse (1-4 references per keyword) | Can be extensive (many trains of thought listed) |
| **Workflow** | Register → hub note or entry-point note | Hub note → specific Folgezettel sequence |

In practice, the keyword register often pointed to hub notes (which had high link density), and hub notes pointed to individual trains of thought. The register was the first layer of navigation; hub notes were the second.

## The Register Is Not a Tagging System

A critical distinction: Luhmann did **not tag individual notes**. The keyword register was a separate lookup artifact mapping terms to entry-point note IDs. This is fundamentally different from modern tagging:

| Tagging System | Keyword Register |
|---------------|-----------------|
| Multiple tags per note | 1-2 keywords per note (if any) |
| Tags are on the note itself | Keywords are in a separate register |
| Every tagged note appears in tag results | Only 1-4 entry-point notes per keyword |
| Produces flat lists | Produces entry points into networks |
| Scales linearly | Scales through internal linking |

As zettelkasten.de states: "Luhmann's register could be mistaken for a tag system. However, the individual notes were not tagged, nor did he put a tagging system in place to organise his Zettelkasten."

## Ahrens' Overview Notes

Ahrens also describes **overview notes** — notes that structure related thoughts, link to relevant [permanent notes](term_permanent_notes.md), and serve as intermediate organizational layers. Overview notes can hold up to 25+ links and expand organically over time. They function as an enriched version of the index entry — while the index provides a bare keyword-to-ID mapping, overview notes provide structured navigation with context.

Making sure notes "can be found from the index" means either adding an entry directly or linking from a note that is already connected to the index — ensuring the entire Zettelkasten remains reachable.

## Comparison Across Systems

| System | Equivalent | Key Difference |
|--------|-----------|----------------|
| **Luhmann's Zettelkasten** | Schlagwortregister (keyword register) | Separate physical artifact; 3,200 keywords for 67,000 notes |
| **Ahrens (HTSN)** | Index + overview notes | Recommends the same sparse approach for digital systems |
| **Doto's Zettelkasten** | Keyword notes (one of 6 note types) | Topic-based entry points; narrower framing than Ahrens' overview notes |
| **Nick Milo (LYT)** | Home note + Maps of Content (MOCs) | MOCs are richer than index entries; serve active sensemaking |
| **Sascha Fast (zettelkasten.de)** | Top-layer structure notes | Structure notes emerge as search becomes unwieldy (~500-700 notes) |
| **BASB (Forte)** | PARA folder hierarchy | Folder-based; no concept of sparse keyword entry points |
| **Digital full-text search** | Search bar | Functionally replaces keyword lookup, but sparse curation remains valuable |
| **Vault** | Entry points (`0_entry_points/`) + database keyword search | Entry points serve as curated index; SQL keyword search serves as digital register |

## Vault Implementation

In the vault, index notes map to:
- **Entry points** (`0_entry_points/`) — the curated navigation layer that maps broad topics to relevant vault notes, functioning as the digital equivalent of Luhmann's keyword register combined with Doto's hub notes
- **Database keyword search** — `sqlite3 $DB_PATH "SELECT ... WHERE keywords LIKE '%term%'"` serves as a digital Schlagwortregister, finding entry points into the knowledge graph
- **Graph traversal** — once an entry point is found, BFS/DFS traversal follows the internal linking structure, exactly as Luhmann navigated from register → Folgezettel → cross-references
- **Term dictionary** (`resources/term_dictionary/`) — each term note functions as both a permanent note and an implicit index entry, grounding a keyword to a specific concept definition

The vault's sparse entry-point design (96 curated entry points for 4,200+ notes) echoes Luhmann's sparse register philosophy: a small number of curated entry points, with graph structure providing comprehensive navigation.

## Related Terms

- [Hub Notes](term_hub_notes.md) — complementary navigation tool; hub notes contain annotated link lists within the Zettelkasten itself
- [Permanent Notes](term_permanent_notes.md) — the notes that index entries point to; the core units of the slip-box
- [Folgezettel](term_folgezettel.md) — the sequencing system that makes sparse indexing work; once you find one note, you can follow the sequence
- [Zettelkasten](term_zettelkasten.md) — the methodology in which index notes serve as the entry-point navigation layer
- [Fleeting Notes](term_fleeting_notes.md) — raw captures that eventually become permanent notes reachable through the index
- [Literature Notes](term_literature_notes.md) — source summaries that feed permanent notes; stored separately from the index
- [Commonplace Book](term_commonplace_book.md) — historical predecessor; John Locke's 1706 "New Method of a Common-Place-Book" introduced alphabetical indexing, a precursor to the keyword register
- [Trusted System](term_trusted_system.md) — the index contributes to system trust by ensuring findability; without reliable entry points, the system loses its value
- [Serendipity](term_serendipity.md) — sparse indexing forces navigation through connections, manufacturing serendipitous encounters with forgotten notes
- [Systems Thinking](term_systems_thinking.md) — the index is the input interface of the Zettelkasten system; its deliberate sparsity creates the feedback loop that produces emergent knowledge

## References

- Ahrens, S. (2022). *How to Take Smart Notes* (2nd ed.). Index description, overview notes, keyword selection philosophy.
- Schmidt, J.F.K. (2018). "Niklas Luhmann's Card Index: The Fabrication of Serendipity." *Sociologica*, 12(1), 53-60.
- Doto, B. (2024). *A System for Writing*. Keyword notes as topic-based entry points.
- [Zettelkasten.de — Introduction to the Zettelkasten Method](https://zettelkasten.de/introduction/) — register as entry map, not comprehensive index
- [Zettelkasten.de — The Money Is in the Hubs](https://zettelkasten.de/posts/zettelkasten-hubs/) — Schmidt's research on hub Zettels vs. keyword register
- [Niklas Luhmann Archive — Tutorial](https://niklas-luhmann-archiv.de/bestand/zettelkasten/tutorial) — original Zettelkasten with register
- [Digest: How to Take Smart Notes](../digest/digest_smart_notes_ahrens.md) — Ahrens' index and keyword selection philosophy
- [Digest: A System for Writing](../digest/digest_system_for_writing_doto.md) — Doto's keyword notes as entry points
- [Digest: Search Alone Is Not Enough](../digest/digest_search_not_enough_christian.md) — index notes occupy the middle tier (tags/keywords) of the connection hierarchy; they enable browsing within a domain
