---
tags:
  - resource
  - terminology
  - knowledge_management
  - zettelkasten
  - epistemology
keywords:
  - concept
  - definition
  - taxonomy
  - classification
  - knowledge building blocks
  - boundary drawing
  - Aristotle
  - Kant
  - Rosch
  - Wittgenstein
  - prototype theory
  - family resemblance
topics:
  - Knowledge Management
  - Zettelkasten Method
  - Epistemology
language: markdown
date of note: 2026-03-29
status: active
building_block: concept
author: lukexie
---

# Term: Knowledge Building Blocks -- Concept

## Definition

A **concept** is a knowledge building block that defines a part of reality by drawing boundaries around it -- separating what belongs to the concept from what does not. Concepts answer the question "What is X?" by specifying properties, characteristics, and membership criteria. In a knowledge system, concepts are the foundational building blocks upon which all other types depend: arguments require well-defined terms to reason about, counter-arguments target the boundaries concepts draw, and models arrange concepts into relational structures. Without precise concepts, knowledge degrades into ambiguity.

Formally, a concept note captures a **definition** $D(x)$ that partitions a domain $\Omega$ into members $\{x \in \Omega \mid D(x) = \text{true}\}$ and non-members $\{x \in \Omega \mid D(x) = \text{false}\}$. This boundary-drawing function is what distinguishes a concept from an observation (which records data) or an argument (which transfers truth). Concept notes may include taxonomies (hierarchical partitions), classifications (categorical assignments), and distinctions (boundary clarifications between neighboring concepts). The concept block is **static** -- it describes what something *is*, not how to do something or why something is true.

## Historical Origin

The concept building block draws from a rich philosophical tradition of how humans carve reality into categories.

| Contributor | Work | Key Contribution |
|-------------|------|------------------|
| **Aristotle** (384--322 BC) | *Categories* | Introduced genus-differentia definitions: define a concept by its genus (broader class) and differentia (distinguishing property). The template "X is a Y that Z" remains the backbone of concept notes. |
| **Immanuel Kant** (1724--1804) | *Critique of Pure Reason* (1781) | Distinguished analytic concepts (true by definition) from synthetic concepts (requiring empirical input). Showed that concepts without intuitions are empty -- a concept note must connect to concrete instances. |
| **Eleanor Rosch** (b. 1938) | Prototype Theory (1975) | Demonstrated that natural concepts have graded membership -- robins are "more bird" than penguins. Implies concept notes should specify prototypical cases alongside boundary cases. |
| **Ludwig Wittgenstein** (1889--1951) | *Philosophical Investigations* (1953) | Argued that many concepts lack necessary-and-sufficient conditions, instead held together by "family resemblance" -- overlapping similarities with no single shared feature. Warns against over-rigid definitions. |

## Recognition Criteria

Your note is a concept note if:

- It answers "What is X?" with a definition, not "Why is X true?" or "How do you do X?"
- It contains **definitions** that specify membership criteria for a category
- It contains **taxonomies** that organize sub-concepts into hierarchical classes
- It contains **classifications** that assign entities to categories
- It contains **properties** or **characteristics** that describe what makes X what it is
- It contains **distinctions** that clarify the boundary between X and a related concept Y
- It would still be valid even if no one ever acted on it -- concepts are declarative, not procedural

## Writing Guide

A good concept note should:

- Start with a one-sentence genus-differentia definition: "X is a [broader category] that [distinguishing property]"
- Specify boundary cases: what is and is not included in the concept
- Provide prototypical examples that anchor the abstract definition in concrete instances
- Draw explicit distinctions from neighboring concepts to prevent conflation
- Remain **purely descriptive** -- no procedures ("How to detect X"), no metrics ("X costs $Y"), no arguments ("X causes Y")
- Use MathJax notation when a formal definition adds precision, e.g., $P(A \mid B) = \frac{P(B \mid A) P(A)}{P(B)}$ for Bayes' theorem as a concept
- Include a taxonomy table if the concept has recognized sub-types or variants

## Vault Examples

| Note | Why It Is a Concept |
|------|---------------------|
| [term_dnr.md](term_dnr.md) | Defines the DNR (Did Not Receive) abuse vector -- its membership criteria, sub-types, and boundary with INR (Item Not Received). Pure boundary-drawing. |
| [term_causal_inference.md](term_causal_inference.md) | Defines causal inference as a field, distinguishes it from correlation-based analysis, and taxonomizes methods (RCT, IV, DiD, RDD). No procedures embedded. |
| [term_propensity_score_matching.md](term_propensity_score_matching.md) | Defines PSM as a technique, specifies the propensity score $e(x) = P(T=1 \mid X=x)$, and distinguishes matching from weighting. Concept with formal notation. |

## Common Mistakes

- **Embedding procedures**: A concept note that drifts into "## How to Detect DNR Abuse" has crossed from *concept* into *heuristic* or *procedure*. Extract the procedural content into a separate note and link to it.
- **Embedding metrics**: Adding "## Business Impact: $2.3M annual loss" turns a concept note into an argument note (the metric is evidence for a claim). Keep concepts domain-independent where possible.
- **Conflating concept with model**: A concept defines *one* entity; a model describes *relationships between* entities. If your note has an architecture diagram showing how A connects to B, it is a model note, not a concept note.

## Related Terms

- **[Knowledge Building Blocks](term_knowledge_building_blocks.md)** -- parent term; the concept block is one of six building block types in the atomicity framework
- **[Knowledge Building Blocks -- Argument](term_knowledge_building_blocks_argument.md)** -- sibling block; arguments transfer truth *between* concepts
- **[Knowledge Building Blocks -- Counter-Argument](term_knowledge_building_blocks_counter_argument.md)** -- sibling block; counter-arguments challenge the boundaries concepts draw
- **[Knowledge Building Blocks -- Model](term_knowledge_building_blocks_model.md)** -- sibling block; models arrange concepts into relational structures
- **[Zettelkasten](term_zettelkasten.md)** -- the knowledge management system in which concept notes serve as foundational vocabulary
- **[Critical Thinking](term_critical_thinking.md)** -- precise concepts are prerequisites for rigorous critical thinking

## References

### External Sources

- Aristotle. *Categories*. Translated by E.M. Edghill.
- Kant, I. (1781). *Critique of Pure Reason*. Translated by Norman Kemp Smith.
- Rosch, E. (1975). "Cognitive Representations of Semantic Categories." *Journal of Experimental Psychology: General*, 104(3), 192--233.
- Wittgenstein, L. (1953). *Philosophical Investigations*. Translated by G.E.M. Anscombe.
