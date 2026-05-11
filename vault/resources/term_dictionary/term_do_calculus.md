---
tags:
  - resource
  - terminology
  - causal_inference
  - statistics
keywords:
  - do-calculus
  - do calculus
  - do operator
  - do(x)
  - interventional distribution
  - back-door criterion
  - backdoor criterion
  - front-door criterion
  - frontdoor criterion
  - causal effect identification
  - three rules
  - Judea Pearl
topics:
  - causal inference
  - statistics
  - mathematical logic
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Do-Calculus

## Definition

**Do-calculus** is a set of three algebraic inference rules developed by Judea Pearl (1995) that provides a complete and systematic method for determining when and how a causal effect -- expressed as an interventional probability P(Y | do(X=x)) -- can be computed from observational (non-experimental) data, given a causal diagram (DAG). The **do-operator**, denoted do(X=x), represents a physical intervention that sets the variable X to the value x, as distinct from passively observing X=x. The critical difference is that do(X=x) breaks the natural causal mechanisms that determine X (graphically, it "mutilates" the DAG by removing all arrows into X), while conditioning on X=x merely filters the existing data. This distinction is the mathematical expression of the difference between Rung 1 (association/seeing) and Rung 2 (intervention/doing) on the Ladder of Causation.

Pearl's three rules of do-calculus specify conditions under which terms in a causal expression can be simplified: **Rule 1** (Insertion/deletion of observations) allows adding or removing observed variables from a conditional probability when they are irrelevant given the causal structure. **Rule 2** (Action/observation exchange) specifies when an intervention do(X) can be replaced by an observation X=x (or vice versa) -- this is a generalization of the back-door criterion. **Rule 3** (Insertion/deletion of actions) allows adding or removing interventions when they have no causal effect on the outcome given the causal structure. Together, these three rules form a complete calculus: any causal effect that can in principle be identified from observational data can be derived by repeated application of these rules, and if the rules cannot reduce a do-expression to an observational expression, then the causal effect is provably non-identifiable from the available data.

The **completeness** of do-calculus was proven by Shpitser and Pearl (2006) and independently by Huang and Valtorta (2006). This is a profound result: it means that do-calculus is not merely a useful heuristic but a provably sufficient toolset for all identifiable causal queries. The well-known **back-door criterion** and **front-door criterion** are special cases that can be derived from the three rules. The back-door criterion applies when a sufficient set of non-descendant covariates blocks all confounding paths, while the front-door criterion applies when there exists a mediator that is (a) fully caused by the treatment, (b) the sole pathway from treatment to outcome, and (c) whose effect on the outcome is not confounded except through the treatment.

## Full Name

Also known as:
- **Calculus of interventions**
- **Pearl's do-calculus**
- **Causal calculus**

Key components:
- **Do-operator**: do(X=x) -- the mathematical representation of an intervention
- **Back-door criterion** -- the most commonly used special case
- **Front-door criterion** -- an alternative when back-door adjustment is impossible
- **Adjustment formula** -- the computational formula derived from applying the criteria

Contrasted with:
- **Conditional probability** P(Y | X) -- passive observation, not intervention
- **Instrumental variable methods** -- an alternative approach to unmeasured confounding, not derived from do-calculus but compatible with it
- **Randomization** -- physically implements do(X) by randomly assigning X values

## Core Concepts

### The Do-Operator and Graph Mutilation

The intervention do(X=x) is modeled by **graph mutilation**: removing all arrows pointing into X in the DAG and setting X to the value x. This reflects the idea that an intervention overrides the natural causal mechanisms that determine X.

| Expression | Meaning | Graph Operation |
|-----------|---------|-----------------|
| P(Y \| X=x) | Probability of Y given that we **observe** X=x | No change to DAG; filter data |
| P(Y \| do(X=x)) | Probability of Y if we **set** X to x | Remove all arrows into X; set X=x |

### The Three Rules

| Rule | Name | Condition (in mutilated graph G) | Transformation |
|------|------|--------------------------------|----------------|
| **Rule 1** | Insertion/deletion of observations | Y is d-separated from Z given X, W in the appropriate subgraph | P(Y \| do(X), Z, W) = P(Y \| do(X), W) |
| **Rule 2** | Action/observation exchange | Y is d-separated from X given Z, W in the graph where arrows into X are removed | P(Y \| do(X), do(Z), W) = P(Y \| do(X), Z, W) |
| **Rule 3** | Insertion/deletion of actions | Y is d-separated from X in the graph where arrows into X are removed and certain nodes are also removed | P(Y \| do(X), do(Z), W) = P(Y \| do(X), W) |

### Back-Door Criterion (Special Case of Rule 2)

A set of variables Z satisfies the back-door criterion relative to (X, Y) if:
1. No variable in Z is a descendant of X
2. Z blocks every back-door path from X to Y (every path with an arrow into X)

**Adjustment formula**: P(Y | do(X=x)) = sum_z P(Y | X=x, Z=z) P(Z=z)

### Front-Door Criterion (Derived from Rules 2 and 3)

A set of variables M satisfies the front-door criterion relative to (X, Y) if:
1. X blocks all paths from M to any confounder of X and Y
2. There is no unblocked back-door path from X to M
3. All back-door paths from M to Y are blocked by X

**Front-door formula**: P(Y | do(X=x)) = sum_m P(M=m | X=x) sum_{x'} P(Y | X=x', M=m) P(X=x')

### Example: The Smoking-Tar-Cancer Problem

```
       U (unobserved gene)
      / \
     v   v
Smoking --> Tar --> Cancer
```

- Back-door criterion fails: U is unmeasured, so we cannot block the back-door path Smoking <-- U --> Cancer
- Front-door criterion succeeds: Tar is a mediator that satisfies the front-door conditions
- Result: The causal effect of Smoking on Cancer is identifiable from observational data on Smoking, Tar, and Cancer alone

## Key Research and Evidence

- **Pearl, J. (1993)**: "Comment: Graphical models, causality and intervention" -- introduced the back-door criterion
- **Pearl, J. (1995)**: "Causal diagrams for empirical research" -- the foundational paper introducing the three rules of do-calculus
- **Pearl, J. (2000)**: *Causality: Models, Reasoning, and Inference* -- comprehensive treatment; Chapter 3 covers do-calculus in detail
- **Shpitser, I. & Pearl, J. (2006)**: "Identification of joint interventional distributions in recursive semi-Markovian causal models" -- proved completeness of do-calculus
- **Huang, Y. & Valtorta, M. (2006)**: "Identifiability in causal Bayesian networks: A sound and complete algorithm" -- independent completeness proof
- **Pearl, J. & Mackenzie, D. (2018)**: *The Book of Why*, Chapter 7 ("Beyond Adjustment: The Conquest of Mount Intervention") -- accessible treatment of do-calculus

## Practical Applications

### Observational Causal Inference
Do-calculus provides the theoretical foundation for determining whether a causal question can be answered from observational data and, if so, how. This is invaluable when experiments are unethical, impractical, or too expensive.

### Abuse Prevention and Fraud Detection
- **Policy impact from observational data**: When A/B testing a new enforcement policy is impractical (e.g., for ethical reasons or because the policy is already deployed), do-calculus can determine whether the causal effect of the policy can be identified from historical data, given assumptions encoded in a DAG.
- **Identifying treatment effects without RCTs**: The front-door criterion may apply when enforcement (X) affects outcomes (Y) through a measurable mediator (M, e.g., customer friction events) and direct measurement of all confounders is impossible.
- **Automated causal reasoning**: Do-calculus can be implemented algorithmically (e.g., in the DoWhy Python library), enabling automated identification of causal effects in complex systems.

### Knowledge Management
- Do-calculus formalizes the distinction between "correlation" claims and "causation" claims in a knowledge base. When reviewing a note that asserts a causal relationship, one can ask: "What causal model would make this identifiable? Does the back-door or front-door criterion apply?"

## Criticisms and Limitations

- **Requires correct DAG**: Do-calculus is a powerful tool, but its output is only as valid as the input DAG. If the DAG misspecifies the causal structure, the identified formula may be wrong.
- **Complexity**: Applying the three rules manually to complex problems can be extremely tedious; algorithmic implementations are needed for practical use. Even with algorithms, the computational complexity of checking identifiability grows with the size of the DAG.
- **Non-identifiability is common**: Many causal queries are provably non-identifiable from observational data, meaning do-calculus correctly tells you "this cannot be determined" -- which, while informative, does not solve the original problem.
- **Functional form not specified**: Do-calculus tells you *which* observational distributions to compute but not *how* to estimate them from finite data -- practical estimation requires additional statistical methods.
- **Limited to Rung 2**: Do-calculus addresses interventional queries (Rung 2) but cannot, by itself, answer counterfactual queries (Rung 3), which require the full SCM framework.

## Related Terms

- [Term: Causal Inference](term_causal_inference.md) -- the field; do-calculus is one of its most important tools
- [Term: Structural Causal Model](term_structural_causal_model.md) -- do-calculus operates within the SCM framework
- [Term: Directed Acyclic Graph](term_directed_acyclic_graph.md) -- do-calculus applies its rules to DAGs
- [Term: Confounding Variable](term_confounding_variable.md) -- the back-door criterion identifies and adjusts for confounders
- [Term: Ladder of Causation](term_ladder_of_causation.md) -- do-calculus bridges Rung 1 and Rung 2
- [Term: Counterfactual Reasoning](term_counterfactual_reasoning.md) -- goes beyond do-calculus to Rung 3
- [Term: Randomized Controlled Trial](term_randomized_controlled_trial.md) -- RCTs physically implement do(X); do-calculus shows when the same effect can be computed without randomization
- [Term: Simpson's Paradox](term_simpsons_paradox.md) -- do-calculus provides a complete resolution by determining the correct adjustment
- [Term: Collider Bias](term_collider_bias.md) -- do-calculus rules respect collider structure to avoid introducing bias
- [Term: Mediation Analysis](term_mediation_analysis.md) -- the front-door criterion exploits mediating pathways
- [Term: Cognitive Bias](term_cognitive_bias.md) -- do-calculus provides a formal antidote to the human tendency to conflate correlation with causation

## References

- Pearl, J. (1995). Causal diagrams for empirical research. *Biometrika*, 82(4), 669-688.
- Pearl, J. (2000). *Causality: Models, Reasoning, and Inference*. Cambridge University Press. (Chapter 3)
- Pearl, J., & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*. Basic Books. (Chapter 7)
- Shpitser, I., & Pearl, J. (2006). Identification of joint interventional distributions in recursive semi-Markovian causal models. *Proceedings of the 21st National Conference on Artificial Intelligence (AAAI-06)*.
- [Do-calculus adventures (Andrew Heiss)](https://www.andrewheiss.com/blog/2021/09/07/do-calculus-backdoors/)
- [The Do-Calculus Revisited (Pearl, 2012)](https://ftp.cs.ucla.edu/pub/stat_ser/r402.pdf)
- [Digest: The Book of Why](../digest/digest_book_of_why_pearl.md)

---

**Last Updated**: March 7, 2026
**Status**: Active
