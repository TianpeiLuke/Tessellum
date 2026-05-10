---
tags:
  - resource
  - terminology
  - knowledge_management
  - ontology
  - building_blocks
  - tessellum_core
keywords:
  - building block
  - knowledge building block
  - typed atomic note
  - epistemic function
  - Sascha Fast
  - Zettelkasten extension
  - directed ontology
topics:
  - Knowledge Management
  - Ontology
  - Note Format
language: markdown
date of note: 2026-05-09
status: active
building_block: concept
note_second_category: term
---

# Term: Building Block

## Definition

A **Building Block** (BB) is a typed atomic note in Tessellum. It carries one and only one **epistemic claim**, declared via the `building_block:` field in YAML frontmatter, and conforms to the format that type prescribes (required H2 sections, recommended length, allowed sub-kinds).

The Building Block is the **unit of work** in Tessellum — what you write, what you query, what you index. The 8 BB types together form the typed substrate; the 10 directed edges between them form the epistemic ontology that drives the [Dialectic Knowledge System](term_dialectic_knowledge_system.md).

## Why "Building Block"

The term comes from [Sascha Fast](https://zettelkasten.de)'s [Complete Guide to Atomic Note-Taking](https://zettelkasten.de/posts/atomic-note-types/) (2011–), which proposed a 6-type taxonomy of "Knowledge Building Blocks": concept, argument, counter-argument, model, hypothesis, empirical observation. Sascha's framework answered "what type of knowledge is this note?" but deliberately left the relationships between types unspecified.

Tessellum extends Sascha's framework in three ways:

1. **+2 types**: `procedure` (operational knowledge — workflows, SOPs, training loops) and `navigation` (entry points, master TOCs, trail indexes)
2. **10 directed edges** between the 8 types — naming the *transition* (the reasoning step that produces the target type from the source)
3. **4 epistemic layers** — Knowledge / Reasoning / Action / Meta — grouping types by the *kind* of failure they're prone to

The result transforms Sascha's classification into an **ontology** (types + relations), with both prescriptive and descriptive uses.

## The 8 Types

Each Building Block answers one question and serves one epistemic function:

| BB Type | Question | Function | Layer |
|---|---|---|---|
| `empirical_observation` | What happened? | Testing | Knowledge |
| `concept` | What is it called? | Naming | Knowledge |
| `model` | How is it structured? | Structuring | Knowledge |
| `hypothesis` | What will happen next? | Predicting | Reasoning |
| `argument` | Is the prediction true? | Claiming | Reasoning |
| `counter_argument` | What are the flaws? | Refuting | Reasoning |
| `procedure` | How do we act on this? | Doing | Action |
| `navigation` | Where does this live? | Indexing | Meta |

## The 10 Directed Edges

Each edge is a **transition** — a reasoning step from source to target:

| From | Transition | To |
|---|---|---|
| Empirical Observation | Naming & Defining | Concept |
| Concept | Structuring | Model |
| Model | Predicting | Hypothesis |
| Model | Codifying | Procedure |
| Hypothesis | Testing & Evidence | Argument |
| Argument | Challenging | Counter-Argument |
| Counter-Argument | Motivates new | Empirical Observation |
| Procedure | Execution Data | Empirical Observation |
| Navigation | Indexes | All 7 other types |

The edges close into a **cycle** — counter-arguments motivate new observations, which feed back into concepts; procedures generate execution data that feeds back into observations. This cycle is what the [Dialectic Knowledge System](term_dialectic_knowledge_system.md) runtime walks.

## Why Typed Atomicity Matters

Untyped note systems (Obsidian, Notion, Roam) treat all notes as opaque markdown. The system can't:

- Check whether a note is **complete** (a hypothesis without falsifiability is broken; a counter-argument without a target is decorative)
- **Route** to downstream notes that should follow
- **Diagnose** vault-level imbalances ("many observations, few concepts" → naming gap)
- **Retrieve** by epistemic function

Typed atomicity solves all four. It also enables the **CQRS architecture** ([term_cqrs.md](term_cqrs.md)) — System P (typed prescriptive substrate, what you author) is orthogonal to System D (computational descriptive retrieval, what queries return). Without typing, there's no System P.

## Sub-Kinds

The 8 top-level Building Blocks are **stable** — closed list, don't extend. **Sub-kinds** (declared via `note_second_category:` in YAML) are **open** — extend as your domain requires.

Examples:
- `building_block: concept` + `note_second_category: term` → glossary entry
- `building_block: concept` + `note_second_category: metric` → measurable quantity
- `building_block: procedure` + `note_second_category: sop` → standard operating procedure
- `building_block: procedure` + `note_second_category: how_to` → user-facing how-to
- `building_block: model` + `note_second_category: ml_model` → ML architecture spec
- `building_block: model` + `note_second_category: schema` → data schema

A real Tessellum vault tends to discover 80+ sub-kinds organically. The 8-type taxonomy is the load-bearing primitive; sub-kinds layer atop without polluting it.

## Examples

| Type | Example title |
|---|---|
| `empirical_observation` | "Hybrid backend +12 pp Hit@5 on n=80 stratified set" |
| `concept` | "PageRank: a node-importance score from random-walk stationary distribution" |
| `model` | "Hybrid retrieval architecture: Dense top-50 → graph re-rank" |
| `hypothesis` | "BB-induced summarization improves retrieval over flat chunking" |
| `argument` | "CQRS is the right primitive for typed knowledge systems" |
| `counter_argument` | "Counter: dense retrieval Pareto-dominates graph strategies on Hit@5" |
| `procedure` | "How to build the unified DB from a fresh vault" |
| `navigation` | "Entry: Folgezettel trails — master index of N active trails" |

See `vault/examples/` for one full example per BB type.

## Programmatic Access

```python
from tessellum.format import BuildingBlock, BB_SPECS, get_spec, downstream

spec = get_spec(BuildingBlock.ARGUMENT)
# spec.question = "Is the prediction true?"
# spec.function = "Claiming"
# spec.required_sections = ('Claim', 'Reason', 'Evidence', 'References')

for edge in downstream(BuildingBlock.HYPOTHESIS):
    print(f"  {edge.label} → {edge.target.value}")
# Testing & Evidence → argument
```

## Heritage

- **Niklas Luhmann** (1950s) — the Zettelkasten method; proved typed atomic notes scale to ~90k connected ideas
- **Sascha Fast** (zettelkasten.de, 2011–) — original 6-type Building Block taxonomy
- **Tessellum** (2024–2026) — extension to 8 types + 10 edges + 4 layers; formalized via Folgezettel trail FZ 7g in the parent research vault
- **The Dialectic Knowledge System** (FZ 8) — the runtime that walks the BB ontology cycle as a closed-loop protocol

## References

- [Term: Zettelkasten](term_zettelkasten.md)
- [Term: Slipbox](term_slipbox.md)
- [Term: Folgezettel](term_folgezettel.md)
- [Term: Dialectic Knowledge System](term_dialectic_knowledge_system.md)
- [Term: CQRS](term_cqrs.md)
- [Term: Epistemic Function](term_epistemic_function.md)
- [docs/bb-ontology.md](../../../docs/bb-ontology.md) — public-facing ontology page with diagrams
- [docs/note-format.md](../../../docs/note-format.md) — YAML frontmatter spec + required sections per BB type
- `src/tessellum/format/building_blocks.py` — typed Python registry
- Sascha Fast — [Knowledge Building Blocks: A Universal Method for Note-Taking](https://zettelkasten.de/posts/atomic-note-types/)
- Niklas Luhmann — [Communicating with Slip Boxes](https://luhmann.surge.sh/communicating-with-slip-boxes) (English translation)
