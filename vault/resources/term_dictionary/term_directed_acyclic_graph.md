---
tags:
  - resource
  - terminology
  - causal_inference
  - statistics
  - graph_theory
keywords:
  - directed acyclic graph
  - DAG
  - causal diagram
  - causal graph
  - path analysis
  - d-separation
  - chain
  - fork
  - collider
  - junction
  - Sewall Wright
  - Judea Pearl
topics:
  - causal inference
  - graph theory
  - statistics
  - epidemiology
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Directed Acyclic Graph

## Definition

A **Directed Acyclic Graph (DAG)** is a graph consisting of nodes (vertices) connected by directed edges (arrows) with the constraint that no sequence of directed edges forms a closed loop (cycle). In causal inference, DAGs are used to represent **causal assumptions**: each node represents a variable, and each arrow represents a direct causal relationship from the parent node to the child node. DAGs provide the graphical language underlying Judea Pearl's Structural Causal Model (SCM) framework and are the primary tool for reasoning about confounding, selection bias, mediation, and the identifiability of causal effects from observational data.

The use of directed graphs to represent causal relationships was pioneered by the geneticist **Sewall Wright** in the 1920s through his method of **path analysis**, which he developed to study the inheritance patterns of guinea pig coat colors. Wright's path diagrams showed how multiple causal factors could combine to produce an observed outcome, and he derived rules (path coefficients) for computing correlations from the causal structure. This work was largely ignored by mainstream statistics for decades. In the 1980s and 1990s, Judea Pearl -- originally working on Bayesian networks in artificial intelligence -- rediscovered the power of directed graphs for causal reasoning and formalized them within the SCM framework. Pearl's key innovation was the concept of **d-separation** (directional separation), a graphical criterion that determines which variables are conditionally independent given a set of observed variables. D-separation provides the bridge between the causal structure encoded in a DAG and the statistical properties of the data, enabling researchers to read off testable implications from their causal assumptions.

DAGs in causal inference operate under several key assumptions: (1) the **Causal Markov Condition** -- each variable is independent of its non-descendants conditional on its parents; (2) **faithfulness** -- all observed independencies are a consequence of the DAG structure (no "accidental" cancellations); and (3) **acyclicity** -- causal relationships do not form feedback loops (though extensions to cyclic graphs exist for dynamic systems). These assumptions, combined with the three basic junction types (chain, fork, collider), make DAGs a remarkably powerful tool for determining what to control for -- and what not to control for -- in observational studies.

## Full Name

Also known as:
- **DAG** (abbreviation, pronounced "dag")
- **Causal diagram** / **causal graph** (when used for causal inference)
- **Path diagram** (Sewall Wright's original term)
- **Influence diagram** (in decision analysis, with some differences)

Contrasted with:
- **Undirected graph** -- edges have no direction; used for association networks but cannot represent causal asymmetry
- **Cyclic graph** -- allows feedback loops; DAGs exclude these by definition
- **Bayesian network** -- uses DAGs to encode conditional independence but originally lacked causal semantics; Pearl added these

## Core Concepts

### The Three Basic Junction Types

The behavior of information flow in a DAG is determined entirely by three elementary junction structures:

| Junction Type | Structure | Information Flow (Unconditional) | Information Flow (Conditional on Middle Node) |
|--------------|-----------|--------------------------------|---------------------------------------------|
| **Chain (Mediator)** | A --> B --> C | Open (A and C are associated) | Blocked (conditioning on B blocks the path) |
| **Fork (Confounder)** | A <-- B --> C | Open (A and C are associated via B) | Blocked (conditioning on B removes the spurious association) |
| **Collider** | A --> B <-- C | Blocked (A and C are independent) | Open (conditioning on B creates a spurious association) |

### D-Separation

Two variables X and Y are **d-separated** by a set Z in a DAG if every path between X and Y is blocked by Z. A path is blocked if:
1. It contains a **chain** (A --> B --> C) or **fork** (A <-- B --> C) where the middle node B is in Z (conditioned on), OR
2. It contains a **collider** (A --> B <-- C) where the middle node B is NOT in Z and no descendant of B is in Z.

If X and Y are d-separated by Z, then X and Y are conditionally independent given Z in any probability distribution compatible with the DAG.

### Building a Causal DAG

| Step | Action | Guidance |
|------|--------|----------|
| 1 | **List variables** | Include treatment, outcome, and all relevant covariates |
| 2 | **Draw arrows** | An arrow from A to B means "A is a direct cause of B" (relative to the variables in the model) |
| 3 | **No arrows for associations** | If two variables are associated but neither causes the other, there must be a common cause or a pathway -- draw those |
| 4 | **Check acyclicity** | No variable can be its own ancestor; if feedback exists, model it with time-indexed variables |
| 5 | **Identify adjustment sets** | Use the back-door criterion to find valid sets of covariates to control for |

### DAGs in Practice: Common Structures

| Structure Name | DAG | Implication |
|---------------|-----|-------------|
| **Simple confounding** | X <-- Z --> Y, X --> Y | Must control for Z to estimate X --> Y |
| **Mediation** | X --> M --> Y, X --> Y | Controlling for M gives direct effect; not controlling gives total effect |
| **Collider bias** | X --> Z <-- Y | Do NOT control for Z; doing so creates a spurious X-Y association |
| **M-bias** | U1 --> Z <-- U2, U1 --> X, U2 --> Y | Controlling for Z (which looks like a confounder) actually introduces bias |
| **Instrumental variable** | I --> X --> Y, U --> X, U --> Y | I affects X but not Y directly; can identify causal effect even with unmeasured U |

## Key Research and Evidence

- **Wright, S. (1921)**: "Correlation and causation" -- introduced path analysis and path diagrams; the intellectual origin of causal DAGs
- **Wright, S. (1934)**: "The method of path coefficients" -- expanded path analysis to more complex systems
- **Pearl, J. (1988)**: *Probabilistic Reasoning in Intelligent Systems* -- introduced Bayesian networks using DAGs; the precursor to causal DAGs
- **Verma, T. & Pearl, J. (1988)**: "Causal networks: Semantics and expressiveness" -- introduced d-separation
- **Pearl, J. (1995)**: "Causal diagrams for empirical research" -- the foundational paper connecting DAGs to causal inference via the back-door criterion and do-calculus
- **Greenland, S., Pearl, J., & Robins, J. M. (1999)**: "Causal diagrams for epidemiologic research" -- brought DAGs into mainstream epidemiology
- **Textor, J. et al. (2016)**: "Robust causal inference using directed acyclic graphs: the R package 'dagitty'" -- a widely used tool for DAG-based causal analysis

## Practical Applications

### Epidemiology
- DAGs are now standard practice in observational epidemiology for deciding which covariates to adjust for. Major journals (e.g., *American Journal of Epidemiology*, *International Journal of Epidemiology*) encourage or require DAGs as part of study design.

### Abuse Prevention and Fraud Detection
- **Enforcement pathway modeling**: A DAG can represent the causal pathway from abuse behavior through detection, enforcement action, customer response, and downstream outcomes. This clarifies which variables are confounders (customer risk tier), mediators (customer response to enforcement), and colliders (appeal outcome), guiding the correct statistical analysis.
- **False positive root cause analysis**: DAGs can map the causal structure behind false positives, distinguishing between model error, data quality issues, and policy design problems.
- **Feature selection for causal models**: DAGs guide which features to include (and exclude) when building causal models for treatment effect estimation, avoiding the common mistake of adjusting for colliders or mediators.

### Software Tools
- **DAGitty** (dagitty.net): Web-based tool for drawing DAGs and finding valid adjustment sets
- **ggdag** (R package): DAG visualization and analysis in R
- **DoWhy** (Python): Microsoft's library for causal inference that uses DAGs as input

## Criticisms and Limitations

- **Subjective construction**: DAGs encode assumptions, not facts. Different researchers may draw different DAGs for the same problem, leading to different conclusions. There is no purely data-driven method to determine the "correct" DAG.
- **Acyclicity assumption**: Many real systems involve feedback loops (e.g., poverty --> poor health --> reduced income --> more poverty). Standard DAGs cannot represent these; extensions (e.g., time-indexed DAGs, cyclic causal models) are needed.
- **Causal sufficiency**: DAGs assume that all common causes of any two variables in the graph are included. If important common causes are omitted, the DAG may yield incorrect adjustment sets.
- **Static representation**: DAGs represent a snapshot of causal relationships and do not naturally capture how relationships change over time.
- **Complexity scaling**: For systems with many variables, DAGs become unwieldy and the number of possible DAGs grows super-exponentially with the number of nodes.

## Related Terms

- [Term: Causal Inference](term_causal_inference.md) -- the field that DAGs serve as a foundational tool for
- [Term: Structural Causal Model](term_structural_causal_model.md) -- DAGs are the graphical component of SCMs
- [Term: Confounding Variable](term_confounding_variable.md) -- identified via the fork junction and back-door paths in a DAG
- [Term: Collider Bias](term_collider_bias.md) -- a specific junction type in DAGs; conditioning on a collider opens a biasing path
- [Term: Do-Calculus](term_do_calculus.md) -- operates on DAGs to derive interventional distributions
- [Term: Simpson's Paradox](term_simpsons_paradox.md) -- resolved by drawing the correct DAG and applying the back-door criterion
- [Term: Mediation Analysis](term_mediation_analysis.md) -- the chain junction (X --> M --> Y) in a DAG defines mediation
- [Term: Counterfactual Reasoning](term_counterfactual_reasoning.md) -- DAGs + structural equations enable counterfactual evaluation
- [Term: Ladder of Causation](term_ladder_of_causation.md) -- DAGs are the graphical language used across all three rungs
- [Term: Randomized Controlled Trial](term_randomized_controlled_trial.md) -- randomization can be represented in a DAG by removing arrows into the treatment variable
- [Term: Systems Thinking](term_systems_thinking.md) -- DAGs formalize the causal structure that systems thinking reasons about informally
- **[GraphQL](term_graphql.md)**: GraphQL query execution follows a DAG structure -- resolvers are invoked in dependency order with no cycles, paralleling DAG-based computation
- [Term: Zettelkasten](term_zettelkasten.md) -- the link structure of a Zettelkasten can be viewed as a directed graph of knowledge relationships

## References

- Pearl, J. (1995). Causal diagrams for empirical research. *Biometrika*, 82(4), 669-688.
- Pearl, J. (2000). *Causality: Models, Reasoning, and Inference*. Cambridge University Press.
- Pearl, J., & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*. Basic Books. (Chapter 3: "From Evidence to Causes: Reverend Bayes Meets Mr. Holmes")
- Greenland, S., Pearl, J., & Robins, J. M. (1999). Causal diagrams for epidemiologic research. *Epidemiology*, 10(1), 37-48.
- [Wikipedia: Directed Acyclic Graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph)
- [Tutorial on Directed Acyclic Graphs (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8821727/)
- [DAGitty -- drawing and analyzing causal diagrams](https://dagitty.net/)
- [Digest: The Book of Why](../digest/digest_book_of_why_pearl.md)

---

**Last Updated**: March 7, 2026
**Status**: Active
