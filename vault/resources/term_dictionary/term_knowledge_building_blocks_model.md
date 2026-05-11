---
tags:
  - resource
  - terminology
  - knowledge_management
  - zettelkasten
  - systems_theory
keywords:
  - model
  - knowledge building blocks
  - relationships
  - entity relationships
  - whole-part dynamics
  - architecture
  - system description
  - Luhmann
  - Stachowiak
  - Giere
topics:
  - Knowledge Management
  - Zettelkasten Method
  - Systems Theory
language: markdown
date of note: 2026-03-29
status: active
building_block: concept
author: lukexie
---

# Term: Knowledge Building Blocks -- Model

## Definition

A **model** is a knowledge building block that shows relationships between entities and captures whole-part dynamics within a system. Where a concept defines *one thing* and an argument *transfers truth about things*, a model reveals *how things relate to each other* -- composition hierarchies, dependency structures, data flows, and causal pathways. Models are **structural** knowledge: they answer "How is X organized?" and "What are the parts of X and how do they connect?" rather than "What is X?" (concept) or "Why is X true?" (argument).

Formally, a model $\mathcal{M}$ can be represented as a graph $G = (V, E)$ where vertices $V = \{v_1, v_2, \ldots, v_n\}$ are entities (concepts, components, actors) and edges $E \subseteq V \times V$ encode relationships (dependencies, compositions, data flows, causal links). Each edge $e_{ij}$ carries a **relationship type** -- is-part-of, depends-on, causes, transforms, etc. The mapping from reality to model is necessarily a **reduction**: following Stachowiak's model theory, every model is a mapping ($\mathcal{M}: \Omega \to \mathcal{M}(\Omega)$), a reduction (some attributes are omitted), and pragmatic (built for a specific purpose). A model note succeeds when it makes the relational structure visible and inspectable.

## Historical Origin

The model building block draws from traditions that treat relational structure as a primary form of knowledge, distinct from propositional truth.

| Contributor | Work | Key Contribution |
|-------------|------|------------------|
| **Niklas Luhmann** (1927--1998) | *Social Systems* (1984) | Modeled society as a system of self-referential, autopoietic subsystems. His Zettelkasten itself was a relational model -- 90,000 notes connected by explicit links encoding relationships between ideas. |
| **Herbert Stachowiak** (1921--2004) | *Allgemeine Modelltheorie* (1973) | Proposed three properties of all models: **mapping** (models represent an original), **reduction** (models omit some attributes), and **pragmatism** (models serve a purpose). Provides the meta-theory for what model notes are. |
| **Ronald Giere** (1938--2020) | *Science Without Laws* (1999) | Argued that scientific knowledge is best understood as families of models rather than universal laws. Models are not true or false but more or less similar to the systems they represent. |

## Recognition Criteria

Your note is a model note if:

- It contains **architecture diagrams** or structural descriptions showing how components fit together
- It describes a **system** with identifiable components and their interactions
- It maps **entity relationships** -- which entities depend on, compose, or communicate with which others
- It describes **component hierarchies** -- whole-part decompositions or layer structures
- It contains **data schemas** or table definitions showing how data entities relate
- It presents a **workflow** or **pipeline** showing sequential or parallel processing stages
- It would be most naturally represented as a diagram, graph, or table of relationships rather than as prose

## Writing Guide

A good model note should:

- Name the **entities** (vertices) in the model and define each briefly or link to their concept notes
- Specify the **relationships** (edges) between entities: what type of connection exists and in which direction
- Explain the **whole-part dynamics**: what is the whole system, and what are its constituent parts?
- Include a structural representation -- a table, ASCII diagram, or Mermaid diagram that makes relationships visible
- State the **purpose** of the model: what question does this structural view answer? (Stachowiak's pragmatism property)
- Acknowledge what the model **omits**: what aspects of reality are reduced away? (Stachowiak's reduction property)
- Use formal notation where it adds precision, e.g., $\text{ETL pipeline}: \text{Source} \xrightarrow{extract} \text{Raw} \xrightarrow{transform} \text{Clean} \xrightarrow{load} \text{Target}$
- Link component entities to their respective concept notes for full definitions

## Vault Examples

| Note | Why It Is a Model |
|------|-------------------|
| `area_mfn.md` and area notes | Area notes describe organizational structures -- teams, programs, and their relationships. They map entities (teams, systems, programs) to each other via ownership, dependency, and data flow relationships. |
| ETL job notes (`entry_etlm_jobs`) | Each ETL note describes a pipeline: source tables $\to$ transformations $\to$ target tables, with dependency relationships between jobs. Pure relational structure. |
| Table schema notes | Schema notes define entities (columns), their types, and relationships (foreign keys, joins). They are models of data structure -- $G = (\text{tables}, \text{joins})$. |

## Common Mistakes

- **Describing a model without explaining the relationships**: A note that lists components but does not specify how they connect is an inventory (a collection of concepts), not a model. The relationships are the core content of a model note.
- **Conflating model with procedure**: A model shows *structure* (what connects to what); a procedure shows *sequence* (what to do in what order). "The ETL pipeline has three stages" is a model; "First run the extraction script, then validate, then load" is a procedure. If your note is primarily a how-to guide, it is a heuristic, not a model.
- **Omitting the reduction acknowledgment**: Every model leaves things out. A model note that presents itself as a complete description of reality is misleading. State what the model covers and what it deliberately excludes.

## Related Terms

- **[Knowledge Building Blocks](term_knowledge_building_blocks.md)** -- parent term; the model is one of the building block types in the atomicity framework
- **[Knowledge Building Blocks -- Concept](term_knowledge_building_blocks_concept.md)** -- sibling block; concepts define the individual entities that models arrange into relational structures
- **[Knowledge Building Blocks -- Argument](term_knowledge_building_blocks_argument.md)** -- sibling block; arguments transfer truth about the entities and relationships that models describe
- **[Knowledge Building Blocks -- Counter-Argument](term_knowledge_building_blocks_counter_argument.md)** -- sibling block; counter-arguments may challenge the relationships a model posits
- **[Zettelkasten](term_zettelkasten.md)** -- the knowledge management system; Luhmann's Zettelkasten is itself a model of interconnected knowledge
- **[Hub Notes](term_hub_notes.md)** -- hub notes often serve as model notes, mapping the relational structure of a topic area

## References

### External Sources

- Luhmann, N. (1984). *Soziale Systeme: Grundriss einer allgemeinen Theorie*. Suhrkamp. [English: *Social Systems*. Stanford University Press, 1995.]
- Stachowiak, H. (1973). *Allgemeine Modelltheorie*. Springer-Verlag.
- Giere, R.N. (1999). *Science Without Laws*. University of Chicago Press.
- Sascha (2025). "The Complete Guide to Atomic Note-Taking." zettelkasten.de.
