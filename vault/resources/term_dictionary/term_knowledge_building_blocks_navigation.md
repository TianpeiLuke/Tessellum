---
tags:
  - resource
  - terminology
  - knowledge_management
  - zettelkasten
  - information_architecture
keywords:
  - navigation note
  - index note
  - entry point
  - routing structure
  - graph traversal
  - table of contents
  - glossary
  - meta-structure
  - knowledge building block
  - vault extension
topics:
  - Knowledge Management
  - Zettelkasten Method
  - Information Architecture
  - Knowledge Organization
language: markdown
date of note: 2026-03-29
status: active
building_block: concept
author: lukexie
---

# Term: Knowledge Building Blocks -- Navigation

## Definition

A **Navigation** note is a knowledge building block that provides index and routing structures for graph traversal within a knowledge system. Navigation notes do not contain substantive knowledge themselves -- they organize access to knowledge atoms stored elsewhere. They are the maps, tables of contents, and signposts that enable a user (human or agent) to find, browse, and traverse the vault's knowledge graph efficiently. In a system with thousands of notes, the ability to locate the right note at the right time is as critical as the quality of the notes themselves.

**Vault Extension**: Navigation is not part of Sascha Fast's original six knowledge building blocks or his expanded taxonomy. It was added to this vault's taxonomy because knowledge systems operating at scale need explicit meta-structures that organize access to knowledge atoms. Luhmann himself recognized this need -- his physical Zettelkasten included a dedicated register (index) that served as an entry point into the slip-box. The navigation building block formalizes what Luhmann practiced implicitly: that a knowledge system needs a layer of notes whose sole purpose is routing, not reasoning. Navigation notes relate to content notes the way a library catalog relates to books -- the catalog contains no knowledge about chemistry, but without it, finding the chemistry books becomes intractable. In graph-theoretic terms, if content notes are the vertices and links are the edges, navigation notes are the designated entry points and traversal guides for the graph $G = (V, E)$.

## Historical Origin

The idea that knowledge systems need dedicated navigation structures predates digital tools by decades. Three foundational thinkers articulated why and how routing mechanisms are essential:

| Contributor | Work | Key Contribution |
|-------------|------|-------------------|
| **Vannevar Bush** | "As We May Think" (1945) | Envisioned the **memex** -- a desk-sized device storing all of a person's documents with associative trails linking related items. Bush's insight was that the problem is not storage but *retrieval*: we need trails (navigation paths) to find what we have stored. |
| **Ted Nelson** | *Literary Machines* (1981) | Coined **hypertext** -- non-sequential writing with links that the reader follows. Nelson formalized the idea that documents need navigational structures (link lists, transclusions, backlinks) to be usable in a networked knowledge system. |
| **Niklas Luhmann** | Zettelkasten practice (1952-1997) | Maintained a **register/index system** -- a set of entry-point slips that listed key terms and their locations within the box. The register was not content; it was a navigation layer that made 90,000 slips traversable. This is the direct historical precedent for vault entry point notes. |

These three contributions -- Bush's associative trails, Nelson's hypertext links, and Luhmann's register system -- converge in the navigation building block: a note type dedicated to helping users find and traverse knowledge rather than store it.

## Recognition Criteria

Your note is a navigation building block if it:

- Contains a **table of contents** -- an organized listing of notes, sections, or topics with links to each
- Provides a **link list** -- a curated set of links to related notes, organized by category, chronology, or priority
- Functions as a **glossary** -- an alphabetical or categorical index of terms with links to their definitions
- Serves as an **entry point index** -- a starting place for exploring a topic area, project, or domain
- Acts as a **routing guide** -- directs the reader to different notes based on their question, role, or context
- Contains primarily **links and organizational structure** rather than substantive arguments, observations, or procedures
- Can be summarized as "to find notes about X, start here" rather than "X is true" or "do X"

A useful test: if you removed all links from the note, would any substantive knowledge remain? If the answer is no, it is a navigation note. If substantive content remains, the note is a hybrid and should be decomposed.

## Writing Guide

A good navigation note should:

- **State its scope immediately** -- the first line should tell the reader what domain, project, or topic this navigation note covers and who it is for
- **Organize links by a clear principle** -- chronological, categorical, alphabetical, or by workflow stage. Do not dump links in an unstructured list
- **Use tables for structured navigation** -- tables with columns for note name, type, date, and brief description are more scannable than plain link lists
- **Link, do not contain** -- a navigation note should point to content, not duplicate it. If you find yourself writing substantive paragraphs, extract them into a separate content note and link to it
- **Include brief annotations** -- a bare link list is hard to scan. Add one-line descriptions of what each linked note contains so readers can choose without clicking
- **Maintain currency** -- navigation notes rot faster than content notes. When new notes are added to the vault, update the relevant navigation notes. Stale indexes are worse than no indexes
- **Define the traversal order** -- if the links should be read in a particular sequence (e.g., a curriculum), number them. If they are unordered alternatives, use bullets

## Vault Examples

| Example Note | Why It Is a Navigation Note |
|--------------|------------------------------|
| Entry point notes (e.g., [entry_buyer_abuse_ml_programs.md](../../0_entry_points/entry_buyer_abuse_ml_programs.md)) | Entry point notes are pure navigation: they list and link to all notes related to a program area, organized by category. They contain no substantive analysis -- only routing structure. |
| [entry_acronym_glossary.md](../../0_entry_points/entry_acronym_glossary.md) | An alphabetical index of acronyms with links to their term notes. Classic glossary-style navigation: organizational structure over substantive content. |
| [README.md](../../../README.md) | The vault's top-level routing guide: points new users to entry points, explains the folder structure, and provides statistics. Navigation meta-structure for the entire system. |

## Common Mistakes

- **Putting substantive content in navigation notes**: Writing analysis, arguments, or detailed explanations inside what should be a routing note. If a navigation note grows paragraphs of conceptual discussion, extract the discussion into a content note and replace it with a link. Navigation notes should be lean.
- **Creating navigation for too-small collections**: Building an entry point index for three notes is overhead without benefit. Navigation notes earn their keep when the collection they index is large enough (roughly 10+ notes) that a reader cannot hold the full set in working memory. For small collections, a section within a parent navigation note suffices.
- **Letting navigation notes go stale**: A navigation note that links to notes that no longer exist, or that omits recently added notes, is actively harmful -- it routes users to dead ends or hides new content. Navigation notes require periodic maintenance, ideally as part of the note-creation workflow (add a new note, update the relevant entry point).

## Related Terms

- **[Knowledge Building Blocks](term_knowledge_building_blocks.md)**: Parent term -- navigation is a vault extension to Sascha's taxonomy, adding a meta-structural layer to the content-level building blocks
- **[Knowledge Building Blocks -- Hypothesis](term_knowledge_building_blocks_hypothesis.md)**: Sibling block -- navigation notes organize access to hypothesis notes but do not contain hypotheses themselves
- **[Knowledge Building Blocks -- Empirical Observation](term_knowledge_building_blocks_empirical_observation.md)**: Sibling block -- navigation notes route to observation notes (e.g., MTR review entry points)
- **[Knowledge Building Blocks -- Procedure](term_knowledge_building_blocks_procedure.md)**: Sibling block -- navigation notes index procedures (e.g., SOP entry points) without containing procedural steps
- **[Hub Notes](term_hub_notes.md)**: A closely related concept in traditional Zettelkasten practice -- hub notes serve as local navigation centers within a topic cluster
- **[Index Notes](term_index_notes.md)**: The Zettelkasten term for top-level navigation notes that serve as entry points into the slip-box
- **[Information Architecture](term_information_architecture.md)**: The discipline of organizing and structuring information for findability -- navigation notes are an information architecture artifact
- **[Folgezettel](term_folgezettel.md)**: Luhmann's sequential numbering system, which provided implicit navigation through physical adjacency -- navigation notes provide explicit navigation through links

## References

### Vault Sources

- [entry_faq.md](../../0_entry_points/entry_faq.md) -- a navigation note that routes common questions to relevant vault notes
- [entry_buyer_abuse_ml_model_landscape.md](../../0_entry_points/entry_buyer_abuse_ml_model_landscape.md) -- navigation note organizing the ML model portfolio

### External Sources

- Bush, V. (1945). "As We May Think." *The Atlantic Monthly*, 176(1), 101-108. -- the memex vision and associative trails.
- Nelson, T. (1981). *Literary Machines*. Mindful Press. -- hypertext theory and navigational link structures.
- Luhmann, N. (1992). "Kommunikation mit Zettelkasten." In *Universitat als Milieu*, ed. A. Kieserling, 53-61. -- describes the register/index system for navigating 90,000 slips.
- Sascha (2025). "The Complete Guide to Atomic Note-Taking." zettelkasten.de -- the expanded taxonomy that this vault extension supplements.
