---
tags:
  - resource
  - terminology
  - knowledge_management
  - productivity
  - analytical_frameworks
keywords:
  - CODE method
  - Capture Organize Distill Express
  - knowledge lifecycle
  - Tiago Forte
  - Building a Second Brain
  - BASB
  - personal knowledge management
  - PKM
  - information processing
  - creative output
topics:
  - knowledge management
  - personal productivity
  - information processing
language: markdown
date of note: 2026-03-11
status: active
building_block: concept
---

# Term: CODE Method

## Definition

The **CODE method** — **Capture, Organize, Distill, Express** — is a four-phase knowledge lifecycle framework introduced by Tiago Forte in *Building a Second Brain* (2022). It describes the complete cycle by which raw information is transformed into creative output: information enters the system (Capture), is sorted by actionability (Organize), is compressed to its essence (Distill), and is used to produce tangible deliverables (Express). Each phase has a dedicated technique: Capture uses the **Twelve Favorite Problems** as a filter, Organize uses the **PARA framework**, Distill uses **Progressive Summarization**, and Express uses **Intermediate Packets**.

The CODE method is significant because it treats knowledge management not as a *storage* problem (how to file things) but as a *flow* problem (how to move information from input to output). The goal is not to accumulate the most information but to produce the most valuable creative output. This output-orientation distinguishes BASB from earlier PKM systems that optimized primarily for retrieval.

## The Four Phases

| Phase | Core Question | Technique | Input | Output |
|-------|-------------|-----------|-------|--------|
| **Capture** | "Does this resonate?" | Twelve Favorite Problems; intuition-based filtering | Information stream (articles, books, conversations, ideas) | Raw notes in inbox |
| **Organize** | "How will this help me move a current project forward?" | PARA framework (Projects, Areas, Resources, Archives) | Raw notes | Notes sorted by actionability |
| **Distill** | "What is the most important point?" | Progressive Summarization (4 layers) | Organized notes | Distilled notes with highlighted essence |
| **Express** | "What can I create with this?" | Intermediate Packets; Archipelago of Ideas | Distilled notes | Creative output (articles, presentations, code, decisions) |

### Phase Relationships

The four phases form a **cycle**, not a pipeline. Express generates new insights that become inputs for Capture. Organizing notes may reveal gaps that trigger new Capture. Distilling a note may change how you Organize related notes. The cycle is recursive and self-reinforcing.

### Divergence ↔ Convergence Mapping

| Mode | Phases | Activity |
|------|--------|----------|
| **Divergence** | Capture + Organize | Generating ideas, exploring, gathering |
| **Convergence** | Distill + Express | Narrowing, selecting, constructing |

## Comparison with Other Lifecycle Models

| Framework | Phases | Domain | Emphasis |
|-----------|--------|--------|----------|
| **CODE** (Forte) | Capture → Organize → Distill → Express | Personal knowledge management | Output and actionability |
| **GTD** (Allen) | Capture → Clarify → Organize → Reflect → Engage | Task management | Stress-free execution |
| **Zettelkasten** (Luhmann) | Capture (fleeting) → Process (literature) → Connect (permanent) → Retrieve | Intellectual production | Connection and emergence |
| **DIKW Pyramid** | Data → Information → Knowledge → Wisdom | Information science | Abstraction levels |
| **Design Thinking** (d.school) | Empathize → Define → Ideate → Prototype → Test | Product design | User-centered iteration |

**Key differences**: GTD has five phases (adding Clarify and Reflect); the Zettelkasten has an implicit fourth phase (Retrieve/Publish) not always articulated; Design Thinking is iterative and non-linear. CODE's four phases are the most compressed lifecycle — each phase maps cleanly to one of Forte's core techniques.

## The Vault's C.O.D.E. Implementation

The vault's skill classification system uses C.O.D.E. stages directly derived from Forte's framework:

| CODE Phase | Vault Skills | Examples |
|------------|-------------|---------|
| **Capture** | Skills that bring new information into the vault | `slipbox-save-paper-zotero`, `slipbox-search-papers`, `slipbox-digest-paper`, `slipbox-digest-external` |
| **Organize** | Skills that structure, link, and maintain vault notes | `slipbox-run-full-database-rebuild`, `slipbox-fix-broken-links`, `slipbox-check-broken-links` |
| **Distill** | Skills that analyze, synthesize, and generate questions | `slipbox-review-paper`, `slipbox-generate-questions`, `slipbox-analyze-term-relevance` |
| **Express** | Skills that produce output from vault knowledge | `slipbox-search-notes`, `answer-query`, `slipbox-update-repo-docs` |

Each skill is tagged with a `code-stage` metadata field in both Claude and Kiro skill formats, enabling classification and reporting.

## Related Terms

- [Progressive Summarization](term_progressive_summarization.md) — the primary technique for the Distill phase; compresses notes through four layers
- [Intermediate Packets](term_intermediate_packets.md) — the primary output mechanism for the Express phase; modular, reusable knowledge units
- [Trusted System](term_trusted_system.md) — the CODE method requires a trusted system as its substrate; without reliable capture and retrieval, the cycle breaks
- [Open Loops](term_open_loops.md) — captured but unprocessed information creates open loops; the Organize and Distill phases close them
- Natural Planning Model — Allen's five-phase planning model complements CODE: NPM plans projects, CODE processes knowledge
- [Zettelkasten](term_zettelkasten.md) — the vault's primary methodology; CODE provides the lifecycle framework, Zettelkasten provides the note-linking architecture
- Design Thinking — parallel lifecycle structure (Empathize → Define → Ideate → Prototype → Test) with similar diverge-then-converge dynamics
- Habit Loop — each CODE phase can become a habitual practice; the cycle's regularity builds the knowledge management habit
- Divergence and Convergence — Capture + Organize are divergent; Distill + Express are convergent; mixing modes causes friction
- [Compound Effect](term_compound_effect.md) — each cycle through CODE adds value to the system; the compound effect of consistent practice builds an increasingly powerful knowledge base
- [SlipBox](term_slipbox.md) — the vault implements CODE as its operational framework; the `code-stage` metadata on skills derives from this
- [BASB](term_basb.md) — Building a Second Brain; the book that introduced the CODE method as its primary framework

## References

- Forte, T. (2022). *Building a Second Brain: A Proven Method to Organize Your Digital Life and Unlock Your Creative Potential*. Atria Books. Chapter 3: "How a Second Brain Works."
- Allen, D. (2015). *Getting Things Done: The Art of Stress-Free Productivity* (Revised Edition). Penguin Books. — The five-step workflow that CODE simplifies
- Source: [Digest: Building a Second Brain](../digest/digest_building_second_brain_forte.md)
- Source: [Digest: How to Take Smart Notes](../digest/digest_smart_notes_ahrens.md) — Ahrens' three-stage pipeline (fleeting → literature → permanent) parallels CODE's four stages
- Source: Digest: Getting Things Done — Allen's five-step workflow that CODE simplifies for knowledge management

---

**Last Updated**: March 11, 2026
**Status**: Active — knowledge management and productivity terminology
