---
tags:
  - resource
  - terminology
  - argumentation
  - computational_argumentation
  - explainable_ai
  - knowledge_representation
  - critical_thinking
keywords:
  - QBAF
  - Quantitative Bipolar Argumentation Framework
  - bipolar argumentation framework
  - BAF
  - abstract argumentation framework
  - gradual semantics
  - intrinsic strength
  - base score
  - Baroni
  - Toni
  - Dung 1995
  - argument graph
topics:
  - Computational Argumentation
  - Explainable AI
  - Knowledge Representation
language: markdown
date of note: 2026-04-25
status: active
building_block: concept
related_wiki: null
---

# QBAF - Quantitative Bipolar Argumentation Framework

## Definition

A **Quantitative Bipolar Argumentation Framework (QBAF)** is a formal structure from computational argumentation theory used to represent and reason about networks of arguments that may attack or support each other, where each argument additionally carries a numerical *intrinsic strength* (or *base score*). Formally, a QBAF is a quadruple $\langle A, R^-, R^+, \tau \rangle$ where $A$ is a finite set of arguments, $R^- \subseteq A \times A$ is a binary attack relation, $R^+ \subseteq A \times A$ is a binary support relation (with $R^- \cap R^+ = \emptyset$), and $\tau: A \to [0, 1]$ is a total function assigning each argument an intrinsic *base score*. A QBAF generalises Dung's (1995) abstract Argumentation Framework (AF) by adding (i) a second **bipolar** relation type — support — alongside attack (Cayrol & Lagasquie-Schiex 2005), and (ii) a **quantitative** strength annotation that captures graded confidence rather than treating arguments as equally strong propositional atoms (Baroni, Rago & Toni 2019).

Given a QBAF, a *gradual semantics* $\sigma: A \to [0, 1]$ aggregates each argument's base score $\tau(\alpha)$ with the *dialectical* contributions of its attackers $R^-(\alpha)$ and supporters $R^+(\alpha)$ to yield a final *strength* $\sigma(\alpha)$ (also called the *acceptability* or *dialectical strength*). The semantics decides — deterministically and recursively over the argument graph — how much an argument's standing is amplified by its supporters, suppressed by its attackers, and anchored by its intrinsic base score. QBAFs are the structured, interpretable substrate underlying recent neuro-symbolic systems such as ArgLLMs (Freedman et al. 2025), where an LLM populates the arguments and base scores while a fixed semantics (typically [DF-QuAD](term_df_quad.md)) computes the verdict.

## Context

QBAFs are the central data structure of **quantitative computational argumentation**, an area developed by the Imperial CLArg group (Toni, Rago, Baroni and colleagues) and used in: (i) *explainable AI* — as a faithful, contestable representation of a system's reasoning (Cyras et al. 2021); (ii) *recommender systems* — for explaining and contesting recommendations (Rago et al. 2023); (iii) *fact / claim verification* and *fake news detection* — Freedman et al.'s ArgLLMs build a QBAF per claim from LLM-generated pro/con arguments and apply DF-QuAD; (iv) *medical and legal decision support* — where conflicts among graded evidence must be resolved transparently; and (v) *argumentation-machine-learning hybrids* — surveyed by Rago, Cyras, Mumford & Cocarascu (2024), where QBAFs sit between a learning component and a downstream decision so that gradients, attributions, or predictions can be argued over rather than blindly trusted. 

## Key Characteristics

- **Quadruple structure**: $\langle A, R^-, R^+, \tau \rangle$ — arguments, attack edges, support edges, and a base-score function $\tau: A \to [0, 1]$ (Baroni, Rago, Toni 2019).
- **Bipolar**: distinguishes attack (negative / dialectical conflict) from support (positive / dialectical reinforcement); attack and support sets are disjoint (Cayrol & Lagasquie-Schiex 2005).
- **Quantitative**: each argument has an intrinsic strength in $[0, 1]$ representing prior confidence, evidence quality, or LLM-emitted likelihood — not a binary "in / out" status as in Dung's AFs.
- **Generalises Dung's AF**: with `R+ = ∅` and `tau` collapsed to `{0, 1}`, a QBAF reduces to a standard abstract argumentation framework.
- **Composable with gradual semantics**: many semantics operate on QBAFs — DF-QuAD (Rago et al. 2016), QuAD (Baroni et al. 2015), Quadratic Energy (Potyka 2018), Euler-based (Amgoud & Ben-Naim 2017), among others — each producing a deterministic strength assignment.
- **Restricted (tree-shaped) variants**: a QBAF is *restricted* (a tree) when there is a unique root argument `α*` and every other argument has a unique path to it; ArgLLMs and many gradual-semantics analyses assume this form for tractability.
- **Faithful and interpretable explanation**: because the verdict is a deterministic function of the QBAF, the QBAF itself constitutes a *faithful* explanation in the sense of Rudin (2019) — what you see is provably what the model computed.
- **Contestable substrate**: QBAFs natively support [contestability](term_contestability.md) — a user can edit `tau(α)`, add or remove arguments, or flip an edge between attack and support, then re-run the semantics and observe a measurable change in the verdict.
- **Distinguished from probabilistic graphical models**: edges encode dialectical relations, not conditional probabilities; the strength function is rule-based and does not normalise over a sample space.
- **Pro / con argument typology**: for a target argument $\alpha^*$, a *pro* argument is one whose path to $\alpha^*$ uses an even number of attacks (so it ultimately reinforces the target), and a *con* argument is one whose path uses an odd number of attacks (so it ultimately undermines the target).

## Related Terms

- **[Argumentation](term_argumentation.md)**: the broader interdisciplinary field of which QBAFs are a quantitative, computational instantiation
- **[Dialectic Knowledge System](term_dialectic_knowledge_system.md)**: a vault knowledge architecture whose claim-adjudication step is naturally implemented over a QBAF with intrinsic strengths from corroborating evidence
- **[Dialectical Adequacy](term_dialectical_adequacy.md)**: the epistemic standard that QBAF-based reasoning approaches by exposing every counter-argument as an explicit, weighted attacker
- **[DF-QuAD](term_df_quad.md)**: the discontinuity-free gradual semantics most commonly applied to QBAFs and used in ArgLLMs
- **[Contestability](term_contestability.md)**: the formal property — provable for DF-QuAD over QBAFs — that a user's edit of base scores or relations measurably moves the verdict
- **Knowledge Building Blocks Argument**: vault building-block representation of an argument; QBAF arguments are its formal-graph counterpart
- **Knowledge Building Blocks Counter-Argument**: vault building-block representation of an attacker in a QBAF
- **Multi-Agent Debate**: an LLM-debate paradigm whose unstructured exchanges QBAFs replace with a formal, deterministically aggregated argument graph
- **Chain of Thought**: contrasted approach that produces post-hoc reasoning traces; QBAFs are positioned as a faithful, deterministic alternative
- **Neuro-Symbolic**: ArgLLMs are a neuro-symbolic system in which the LLM is the neural perception layer and the QBAF + gradual semantics is the symbolic reasoner
- **Hallucination**: QBAFs do not eliminate LLM hallucinations but expose them as visible, contestable arguments inside the framework
- **LLM as a Judge**: in QBAF-based pipelines the LLM is also the judge — assigning intrinsic strengths $\tau(\alpha)$ to LLM-generated arguments
- **Research Argument**: Booth's claim/reasons/evidence/warrant model is the natural-language analogue of a QBAF's argument / supporter / base-score machinery
- **Logical Fallacies**: a fallacious argument inside a QBAF appears as a regular node, which is precisely what makes the framework contestable — a human can lower its $\tau$
- **[Critical Thinking](term_critical_thinking.md)**: QBAFs operationalise the critical-thinking principle that beliefs should be supported by weighed reasons and survive counter-arguments

## References

- [Baroni, Rago & Toni (2019). "From Fine-Grained Properties to Broad Principles for Gradual Argumentation: A Principled Spectrum." International Journal of Approximate Reasoning](https://www.sciencedirect.com/science/article/pii/S0888613X18302888) — the modern reference defining QBAFs and the principle-based analysis of gradual semantics
- [Cayrol & Lagasquie-Schiex (2005). "On the Acceptability of Arguments in Bipolar Argumentation Frameworks." ECSQARU](https://link.springer.com/chapter/10.1007/11518655_33) — original bipolar argumentation framework with separate attack and support relations
- [Dung (1995). "On the Acceptability of Arguments and Its Fundamental Role in Nonmonotonic Reasoning, Logic Programming and n-Person Games." Artificial Intelligence](https://www.sciencedirect.com/science/article/pii/000437029400041X) — the foundational abstract argumentation framework that QBAFs extend
- [Freedman, Dejl, Gorur, Yin, Rago & Toni (2025). "Argumentative Large Language Models for Explainable and Contestable Claim Verification." AAAI 2025 (oral)](https://arxiv.org/abs/2405.02079) — ArgLLMs use QBAFs as the structured output of LLM argument generation
- [Rago, Cyras, Mumford & Cocarascu (2024). "Argumentation and Machine Learning." Handbook of Formal Argumentation Vol. 4](https://arxiv.org/abs/2410.21130) — survey situating QBAFs within the broader argumentation-and-ML landscape
- [Cyras, Rago, Albini, Baroni & Toni (2021). "Argumentative XAI: A Survey." IJCAI](https://www.ijcai.org/proceedings/2021/0600.pdf) — survey of argumentation-based explainable AI, with QBAFs as a central representation
- [Wikipedia. "Argumentation framework."](https://en.wikipedia.org/wiki/Argumentation_framework) — encyclopedic overview of Dung's AF and bipolar / quantitative extensions
