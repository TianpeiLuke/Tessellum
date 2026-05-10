---
tags:
  - resource
  - terminology
  - knowledge_management
  - productivity
  - creative_process
keywords:
  - intermediate packets
  - modular knowledge
  - reusable work units
  - composability
  - atomic notes
  - Tiago Forte
  - Building a Second Brain
  - BASB
  - creative output
  - remixing
topics:
  - knowledge management
  - personal productivity
  - creative process
language: markdown
date of note: 2026-03-11
status: active
building_block: concept
---

# Term: Intermediate Packets

## Definition

**Intermediate Packets** (IPs) are discrete, reusable units of knowledge work that can be assembled into larger creative outputs. The concept was introduced by Tiago Forte in *Building a Second Brain* (2022) to describe the modular building blocks of creative production. Rather than starting every project from scratch — the "blank page" problem — a knowledge worker with a well-maintained Second Brain can assemble pre-made Intermediate Packets into new deliverables, dramatically reducing the activation energy for creative work.

The core insight is that **most creative work is recombination, not invention**. A presentation draws on research notes, prior slide decks, and insights from past projects. A report incorporates data analyses, frameworks, and templates. By treating these components as discrete, labeled, retrievable packets, they become available for future recombination — what Forte calls "remixing" and what Steven Johnson would recognize as **exaptation** (repurposing components evolved in one context for use in another).

## Five Types of Intermediate Packets

| Type | Description | Example |
|------|-------------|---------|
| **Distilled notes** | Notes processed through Progressive Summarization | A book digest with bolded highlights and executive summary |
| **Outtakes** | Material that didn't fit one project but may fit another | Research paragraphs cut from a paper; unused data analyses |
| **Work-in-process** | Partially completed deliverables | Draft outlines, rough diagrams, half-written sections |
| **Final deliverables** | Completed outputs that can be repurposed | Published articles, finished presentations, shipped code modules |
| **Documents from others** | External contributions worth preserving | A colleague's analysis, a shared template, meeting notes |

## Properties of Good Intermediate Packets

| Property | Description | Parallel |
|----------|-------------|----------|
| **Atomic** | Each packet contains one idea, one analysis, or one deliverable | Zettelkasten's "one concept per note" principle |
| **Self-contained** | The packet makes sense without external context | Microservice independence; API contract clarity |
| **Labeled** | Metadata (tags, titles, project links) enables retrieval | Database indexing; keyword search |
| **Reusable** | The packet can serve multiple projects across time | Software library reuse; DRY principle |
| **Composable** | Packets combine with other packets to form larger outputs | Unix philosophy; function composition |

## The Composability Advantage

Traditional knowledge work treats each project as a *monolith* — all research, drafting, and polishing happens within a single, project-specific effort. The Intermediate Packets approach treats projects as *assemblies* — each project is composed from pre-existing modules plus a small amount of new material.

| Approach | Startup Cost | Reuse | Quality Over Time |
|----------|-------------|-------|--------------------|
| **Monolithic** (start from scratch) | High — every project begins empty | None — work is trapped in project silos | Flat — no compounding |
| **Modular** (Intermediate Packets) | Low — assemble from existing components | High — packets serve multiple projects | Improving — packets get refined with each use |

This parallels software engineering's shift from monolithic codebases to microservice architectures: smaller, well-defined modules that compose into larger systems, with each module independently testable and reusable.

## Applications

### Vault as Intermediate Packet System

The vault's note architecture is an Intermediate Packets system:
- **Term notes** are IPs for definitions and domain vocabulary
- **Paper section notes** (intro, algo, results) are IPs for research synthesis
- **Digest notes** are IPs for book/article summaries
- **Entry points** are IPs for navigation and overview
- **Skills** are IPs for agent workflows — markdown-based, composable, independently executable

Each note is atomic, self-contained, labeled (YAML frontmatter), and reusable across projects through graph traversal and search.

### Creative and Research Workflows

When writing a paper review, the reviewer doesn't start from scratch — they assemble from existing paper section notes (IPs), term definitions (IPs), and prior reviews (IPs). When answering a vault query, the system retrieves and assembles relevant IPs through multi-strategy search. This is Forte's vision operationalized: creative work as component assembly rather than blank-page invention.

## Related Terms

- [Progressive Summarization](term_progressive_summarization.md) — the primary technique for creating the "distilled notes" type of Intermediate Packet
- [CODE Method](term_code_method.md) — Intermediate Packets are the primary output of the "Express" phase
- [Zettelkasten](term_zettelkasten.md) — atomic notes are the Zettelkasten's equivalent of Intermediate Packets; both emphasize modularity and reuse
- [Adjacent Possible](term_adjacent_possible.md) — each new Intermediate Packet expands the adjacent possible of what can be created
- [Compound Effect](term_compound_effect.md) — Intermediate Packets compound: the more you create, the more raw material is available for future projects
- [Trusted System](term_trusted_system.md) — Intermediate Packets must be stored in a trusted system to be reliably retrievable
- [Open Loops](term_open_loops.md) — work-in-process IPs are open loops until completed or archived; the Hemingway Bridge technique closes this loop
- [Divergence and Convergence](term_divergence_and_convergence.md) — during convergence, Intermediate Packets are assembled into final deliverables via the Archipelago of Ideas technique
- [Natural Planning Model](term_natural_planning_model.md) — NPM Phase 4 (Organize) and Phase 5 (Next Actions) map to assembling IPs into project plans
- [Slow Hunch](term_slow_hunch.md) — outtakes and work-in-process IPs may incubate as slow hunches, connecting with future ideas
- [Permanent Notes](term_permanent_notes.md) — atomic notes are the Zettelkasten's equivalent of Intermediate Packets; both emphasize modularity and reusability
- [Liquid Network](term_liquid_network.md) — the vault's link graph creates a liquid network where diverse IPs can collide and recombine
- [BASB](term_basb.md) — Building a Second Brain; Intermediate Packets are the primary output of the Express phase

## References

- Forte, T. (2022). *Building a Second Brain: A Proven Method to Organize Your Digital Life and Unlock Your Creative Potential*. Atria Books. Chapter 7: "Express — Show Your Work."
- Johnson, S. (2010). *Where Good Ideas Come From*. Riverhead Books. — Exaptation as the mechanism underlying IP reuse
- Source: [Digest: Building a Second Brain](../digest/digest_building_second_brain_forte.md)
- Source: [Digest: How to Take Smart Notes](../digest/digest_smart_notes_ahrens.md) — Ahrens' permanent notes are the Zettelkasten equivalent of Intermediate Packets
- Source: [Digest: Where Good Ideas Come From](../digest/digest_good_ideas_johnson.md) — exaptation as the mechanism underlying IP reuse and recombination

---

**Last Updated**: March 11, 2026
**Status**: Active — knowledge management and productivity terminology
