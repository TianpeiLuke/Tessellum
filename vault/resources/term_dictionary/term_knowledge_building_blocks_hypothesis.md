---
tags:
  - resource
  - terminology
  - knowledge_management
  - zettelkasten
  - philosophy_of_science
keywords:
  - hypothesis
  - falsifiability
  - testable prediction
  - theory
  - research claim
  - paradigm
  - research programme
  - knowledge building block
  - scientific method
topics:
  - Knowledge Management
  - Zettelkasten Method
  - Philosophy of Science
  - Epistemology
language: markdown
date of note: 2026-03-29
status: active
building_block: concept
author: lukexie
---

# Term: Knowledge Building Blocks -- Hypothesis

## Definition

A **Hypothesis** is a knowledge building block that formulates a testable statement about reality. In the context of a Zettelkasten knowledge system, a hypothesis note articulates a claim that can, in principle, be confirmed or refuted by evidence. Unlike a bare conclusion (which states what is argued), a hypothesis note explicitly frames the claim as provisional and specifies the conditions under which it would be falsified or supported. Hypotheses function as the generative engine of a knowledge system -- they are what produce new lines of inquiry, connect disparate premises, and drive the system forward from passive storage to active thinking.

Theories, in this framing, are hypotheses that have survived scrutiny and have been extended with methodological commitments. A theory note includes not just the testable claim but also the methods by which it was or should be tested, the scope conditions that bound it, and the auxiliary assumptions it relies on. In Sascha Fast's expanded taxonomy (published in the Complete Guide to Atomic Note-Taking), hypotheses and theories occupy the scientific layer of knowledge building blocks -- the layer concerned with how we generate, test, and revise claims about the world. A good hypothesis note makes the reasoning chain visible: here is the claim, here is what would count as evidence for or against it, and here is what I expect to find.

## Historical Origin

The concept of hypothesis as a formal epistemic unit has deep roots in the philosophy of science. Three key thinkers shaped how we understand what makes a hypothesis scientifically legitimate:

| Contributor | Work | Key Contribution |
|-------------|------|-------------------|
| **Karl Popper** | *The Logic of Scientific Discovery* (1934/1959) | Introduced **falsifiability** as the demarcation criterion: a hypothesis is scientific if and only if it specifies conditions that would refute it. Shifted emphasis from verification to refutation. |
| **Thomas Kuhn** | *The Structure of Scientific Revolutions* (1962) | Argued that hypotheses operate within **paradigms** -- shared frameworks of assumptions. Normal science tests hypotheses within a paradigm; revolutionary science replaces the paradigm itself. |
| **Imre Lakatos** | *The Methodology of Scientific Research Programmes* (1978) | Proposed **research programmes** with a hard core of unfalsifiable axioms surrounded by a protective belt of auxiliary hypotheses. A programme is progressive if it predicts novel facts; degenerating if it only accommodates known ones. |

These three perspectives -- falsifiability, paradigm-dependence, and progressive research programmes -- provide complementary lenses for evaluating hypothesis notes in a knowledge system.

## Recognition Criteria

Your note is a hypothesis building block if it:

- Contains a **testable prediction** -- a claim that specifies what should be observed if the hypothesis is correct
- Proposes an **explanation** for an observed phenomenon, mechanism, or pattern
- Articulates a **research claim** or thesis that a paper, project, or investigation is organized around
- Includes **scope conditions** -- boundary statements about when and where the claim applies
- States or implies **falsification criteria** -- what evidence would cause you to abandon or revise the claim
- Frames a question in the form "If $X$, then we should observe $Y$" or equivalent conditional structure

Formally, a hypothesis $H$ is testable if there exists an observable outcome $O$ such that:

$$P(O \mid H) \neq P(O \mid \neg H)$$

That is, the hypothesis must make a difference to what we expect to observe.

## Writing Guide

A good hypothesis note should:

- **State the claim first** -- lead with the hypothesis in one or two sentences before providing background or motivation
- **Specify the observable implications** -- what would we see in data, experiments, or practice if this hypothesis is true?
- **Name the falsification conditions** -- what evidence would refute this claim? A hypothesis without falsification criteria is not yet a hypothesis; it is a speculation
- **Declare the scope** -- state the domain, population, or conditions under which the claim is expected to hold
- **Link to supporting premises** -- connect to the evidence notes, observation notes, and term notes that ground the claim
- **Distinguish hypothesis from conclusion** -- a conclusion is argued for within a note; a hypothesis is proposed for future testing. If the evidence already settles it, promote to a conclusion
- **Keep one hypothesis per note** -- if the note contains two testable claims, split it into two hypothesis notes

## Vault Examples

| Example Note | Why It Is a Hypothesis |
|--------------|------------------------|
| [lit_yang2026plugmem.md](../papers/lit_yang2026plugmem.md) | Literature note capturing a paper's central thesis: that external memory modules can improve LLM performance on long-context tasks. The paper's claim is a testable hypothesis with specified benchmarks. |
| Research presentation notes in [entry_brp_ml_research_by_category.md](../../0_entry_points/entry_brp_ml_research_by_category.md) | ML research presentations often propose hypotheses about model performance, feature importance, or detection effectiveness -- claims tested against metrics. |
| Analysis notes proposing model improvements | Notes that argue "if we add feature X, precision should improve by Y%" contain testable predictions about system behavior. |

## Common Mistakes

- **HARKing (Hypothesizing After Results are Known)**: Writing a hypothesis note after you already know the outcome, then presenting it as if the prediction preceded the evidence. This is intellectually dishonest and undermines the epistemic value of the note. If you discovered the pattern post hoc, label it as an observation or a post-hoc explanation, not a prediction.
- **Unfalsifiable claims**: Writing "this model could potentially improve outcomes" without specifying what improvement means, by how much, or under what conditions. If no possible observation could refute the claim, it is not a hypothesis -- rewrite with concrete, measurable criteria.
- **Conflating hypothesis with opinion**: A hypothesis is grounded in existing evidence and proposes a specific mechanism or prediction. "I think X is better than Y" without evidence, mechanism, or testable implication is an opinion, not a hypothesis.

## Related Terms

- **[Knowledge Building Blocks](term_knowledge_building_blocks.md)**: Parent term -- hypotheses are one of the building block types in Sascha's expanded taxonomy
- **[Research Argument](term_research_argument.md)**: Sibling block -- arguments provide the logical structure (premises + logical form + conclusion) that a hypothesis is tested through
- **[Argumentation](term_argumentation.md)**: The formal structure of reasoning that connects hypotheses to evidence
- **[Critical Thinking](term_critical_thinking.md)**: The discipline of evaluating claims, which includes assessing whether hypotheses meet falsifiability criteria
- **[Literature Notes](term_literature_notes.md)**: The note type that most frequently captures others' hypotheses from papers and books
- **[Propositional Knowledge](term_propositional_knowledge.md)**: Hypotheses are a subtype of propositional knowledge -- knowing-that claims awaiting verification

## References

### Vault Sources

- [Digest: Intellectual Roots of Knowledge Building Blocks](../digest/digest_intellectual_roots_knowledge_building_blocks.md) -- traces the philosophical lineage from Popper through Kuhn to modern Zettelkasten practice

### External Sources

- Popper, K. (1959). *The Logic of Scientific Discovery*. Routledge. (Original: *Logik der Forschung*, 1934.)
- Kuhn, T. (1962). *The Structure of Scientific Revolutions*. University of Chicago Press.
- Lakatos, I. (1978). *The Methodology of Scientific Research Programmes*. Cambridge University Press.
- Sascha (2025). "The Complete Guide to Atomic Note-Taking." zettelkasten.de -- expanded taxonomy listing hypotheses/theories as a building block type.
