---
tags:
  - entry_point
  - index
  - navigation
  - quick_reference
  - glossary
  - tessellum
  - foundations
keywords:
  - Tessellum foundations glossary
  - typed atomic note vocabulary
  - building block ontology
  - zettelkasten methodology
  - PARA method
  - building a second brain
  - CODE method
  - folgezettel trails
  - dialectic knowledge system
  - CQRS architecture
topics:
  - Tessellum Foundations
  - Personal Knowledge Management
  - Typed Knowledge
  - Note Format
language: markdown
date of note: 2026-05-10
status: active
building_block: navigation
---

# Tessellum Foundations Glossary

**Purpose**: One-glance lookup for the 11 foundation terms every Tessellum vault rests on. The headlines here are written for a reader meeting the vocabulary for the first time. Each entry has a one-line "what it is" + a `→` link to the full term note for depth.

**Navigation**: [↑ Acronym Glossaries Index](entry_acronym_glossary.md)

---

## Methodology Lineage

The historical and contemporary practices Tessellum descends from. Read these first if "what is a Tessellum vault?" is the open question.

### Z — Zettelkasten
**Full Name**: Zettelkasten (German: "slip box")
**One-line**: Niklas Luhmann's method for atomic notes + bidirectional links that scaled to ~90,000 connected ideas.
**Key idea**: One note = one atomic idea; relationships are explicit links, not folders.
**Documentation**: [`term_zettelkasten`](../resources/term_dictionary/term_zettelkasten.md)
**Source**: Luhmann, N. (1992). *Communicating with Slip Boxes*; Ahrens, S. (2017). *How to Take Smart Notes*.

### Slipbox
**Full Name**: Slipbox (English for *Zettelkasten*)
**One-line**: The system class — a typed-atomic-note vault with an explicit graph layer.
**Key idea**: Tessellum is one Slipbox implementation; Obsidian, Roam, and Logseq are others. The class is defined by atomicity + linking, not by tooling.
**Documentation**: [`term_slipbox`](../resources/term_dictionary/term_slipbox.md)

### FZ — Folgezettel
**Full Name**: Folgezettel (German: "follow-up slip")
**One-line**: Alphanumeric ID system encoding *how thinking developed* (`1` → `1a` → `1a1` → `1a1a`).
**Key idea**: A `1a` slip sits "below" `1` in the trail; together they encode argument descent. Tells you what relates AND how thinking got there.
**Documentation**: [`term_folgezettel`](../resources/term_dictionary/term_folgezettel.md)

### PARA — Projects/Areas/Resources/Archives
**Full Name**: PARA (Projects, Areas, Resources, Archives)
**One-line**: Tiago Forte's organizational scheme — four top-level buckets that survive growth.
**Key idea**: Sort by *actionability*, not by topic. Projects (active deliverables) → Areas (ongoing responsibilities) → Resources (reference) → Archives (inactive).
**Documentation**: [`term_para_method`](../resources/term_dictionary/term_para_method.md)
**Source**: Forte, T. (2022). *Building a Second Brain*.

### BASB — Building a Second Brain
**Full Name**: Building a Second Brain (Tiago Forte's PKM methodology)
**One-line**: The personal-knowledge-management movement Tessellum descends from on the human-workflow side.
**Key idea**: Externalize knowledge into a system that thinks alongside you. PARA + CODE are its load-bearing primitives.
**Documentation**: [`term_basb`](../resources/term_dictionary/term_basb.md)
**Source**: Forte, T. (2022). *Building a Second Brain*.

### CODE — Capture / Organize / Distill / Express
**Full Name**: CODE (Capture, Organize, Distill, Express)
**One-line**: Forte's four-phase PKM lifecycle — the procedural complement to PARA's organizational scheme.
**Key idea**: Knowledge moves through phases: capture (collect raw input), organize (file with PARA), distill (extract the essence), express (use it). Each Tessellum skill maps to a CODE stage.
**Documentation**: [`term_code_method`](../resources/term_dictionary/term_code_method.md)
**Source**: Forte, T. (2022). *Building a Second Brain*.

### Knowledge Building Blocks
**Full Name**: Knowledge Building Blocks (Sascha Fast's historical taxonomy)
**One-line**: The predecessor to Tessellum's 8-type ontology — Sascha's six knowledge atom types (premises, logical form, conclusion, definitions, distinctions, heuristics).
**Key idea**: Atomicity isn't subjective ("one idea per note") — it's objective: a note is atomic when it represents one of the six taxonomy types. Tessellum's BB extends this to 8 types + 10 edges.
**Documentation**: [`term_knowledge_building_blocks`](../resources/term_dictionary/term_knowledge_building_blocks.md)
**Source**: Sascha Fast at zettelkasten.de.

---

## Tessellum-Specific Architecture

What Tessellum adds on top of the lineage above. Read these once you've absorbed the methodology terms.

### BB — Building Block
**Full Name**: Building Block (Tessellum's 8-type typed atomic ontology)
**One-line**: Every note declares one of 8 types via `building_block:` YAML field — each type carries a defining epistemic function.
**The 8 types**: `empirical_observation`, `concept`, `model`, `hypothesis`, `argument`, `counter_argument`, `procedure`, `navigation`.
**Key idea**: Type-the-atomicity. A note's type tells the system what it is and what it can do.
**Documentation**: [`term_building_block`](../resources/term_dictionary/term_building_block.md)
**Picker**: [`entry_building_block_index`](entry_building_block_index.md) (scannable matrix for "which BB for my note?")

### EF — Epistemic Function
**Full Name**: Epistemic Function
**One-line**: What each BB *does* — `naming` (concept), `structuring` (model), `predicting` (hypothesis), `claiming` (argument), `refuting` (counter_argument), `observing` (empirical_observation), `doing` (procedure), `indexing` (navigation).
**Key idea**: BB types aren't arbitrary labels; each names a specific epistemic role.
**Documentation**: [`term_epistemic_function`](../resources/term_dictionary/term_epistemic_function.md)

### DKS — Dialectic Knowledge System
**Full Name**: Dialectic Knowledge System
**One-line**: The closed-loop protocol where arguments attract counters, counters absorb into syntheses, and warrants update from observed disagreement.
**Key idea**: Knowledge isn't static; it updates. DKS makes the dialectic cycle (thesis → antithesis → synthesis) operational on the BB graph.
**Documentation**: [`term_dialectic_knowledge_system`](../resources/term_dictionary/term_dialectic_knowledge_system.md)
**Source**: Hegel's *Phenomenology of Spirit* (1807), generalized to typed knowledge.

### CQRS — Command Query Responsibility Segregation
**Full Name**: Command Query Responsibility Segregation
**One-line**: The architectural split underlying Tessellum — System P (Prescriptive, write side — typed authoring) ⊥ System D (Descriptive, read side — retrieval) sharing one substrate (the vault).
**Key idea**: Reads and writes optimize for different things. Separate them; share the substrate.
**Documentation**: [`term_cqrs`](../resources/term_dictionary/term_cqrs.md)
**Source**: Greg Young (~2010); Bertrand Meyer's earlier Command-Query Separation.

---

## How these fit together

A first-pass map of the relationships:

```
Methodology lineage (what Tessellum descends from)
  Zettelkasten  ──┬── atomic notes + explicit links
  Slipbox       ──┤   the system class
  Folgezettel   ──┤   trail mechanism encoding "how thinking developed"
                  │
  BASB          ──┼── personal KM movement
  PARA          ──┤   actionability-first organization
  CODE          ──┤   lifecycle (Capture → Organize → Distill → Express)
                  │
  Knowledge BB  ──┘   Sascha Fast's six atom types (predecessor to Tessellum's 8)

Tessellum-specific architecture (what's new)
  BB    ── 8 types × Epistemic Function (typed atomicity)
  DKS   ── closed-loop dialectic over the 10-edge BB graph
  CQRS  ── System P (write) ⊥ System D (read) across the vault substrate
```

The methodology lineage establishes *atomic notes + explicit links*. Tessellum then types the atomicity (BB), names what each type does (EF), closes the dialectic loop over the type graph (DKS), and splits read/write paths over the shared substrate (CQRS).

## Reading order

If this is your first time meeting the vocabulary:

1. **`howto_first_vault`** — what you'll actually do at the keyboard (5 min)
2. **This glossary** — the names and one-liners (10 min)
3. **`term_zettelkasten`** then **`term_slipbox`** — the foundational methodology (~30 min)
4. **`term_building_block`** + **`entry_building_block_index`** — Tessellum's typed atomicity (~30 min)
5. **`term_epistemic_function`**, **`term_folgezettel`**, **`term_dialectic_knowledge_system`**, **`term_cqrs`** — the architectural depth (~1 hour)
6. **`term_basb`**, **`term_code_method`**, **`term_para_method`** — the PKM heritage (~30 min)
7. **`term_knowledge_building_blocks`** — Sascha's historical taxonomy (~15 min)

## Related Entry Points

- [`entry_master_toc`](entry_master_toc.md) — the vault's navigation root
- [`entry_acronym_glossary`](entry_acronym_glossary.md) — master index of all acronym glossaries
- [`entry_building_block_index`](entry_building_block_index.md) — BB picker matrix
- Other glossaries: [statistics](acronym_glossary_statistics.md), [critical thinking](acronym_glossary_critical_thinking.md), [cognitive science](acronym_glossary_cognitive_science.md), [network science](acronym_glossary_network_science.md), [LLMs](acronym_glossary_llm.md)

---

**Last Updated**: 2026-05-10
**Status**: Active — covers the 11 foundation term notes shipped with every Tessellum install
