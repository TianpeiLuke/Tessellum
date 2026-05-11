---
tags:
  - resource
  - terminology
  - causal_inference
  - statistics
keywords:
  - structural causal model
  - SCM
  - structural equation model
  - causal diagram
  - structural equations
  - exogenous variables
  - endogenous variables
  - error term
  - Judea Pearl
topics:
  - causal inference
  - statistical modeling
  - philosophy of science
  - artificial intelligence
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Structural Causal Model

## Definition

A **Structural Causal Model (SCM)** is a mathematical framework developed by Judea Pearl that provides a formal language for defining, analyzing, and answering causal questions at all three levels of the Ladder of Causation. An SCM consists of three components: (1) a set of **exogenous variables** (U) representing external factors not explained by the model, (2) a set of **endogenous variables** (V) whose values are determined within the model, and (3) a set of **structural equations** (F) that define each endogenous variable as a function of its direct causes (other variables in the model) plus an error term drawn from the exogenous variables. Every SCM implies a **causal diagram** -- a directed acyclic graph (DAG) -- where arrows represent the direct causal relationships encoded in the structural equations.

Pearl developed the SCM framework throughout the 1990s and 2000s, culminating in his foundational text *Causality: Models, Reasoning, and Inference* (2000, 2nd edition 2009). The framework extends and formalizes earlier work on structural equation modeling (SEM) from economics (Haavelmo, 1943) and path analysis from genetics (Sewall Wright, 1921), but with a crucial innovation: Pearl gave the equations an explicit **causal** interpretation rather than merely a statistical one. In a traditional SEM, the equation Y = bX + e is symmetric -- it could be read as "Y depends on X" or rearranged to "X depends on Y." In an SCM, the equation Y := f(X, U_Y) is **asymmetric**: it asserts that X is a direct cause of Y, not vice versa. This asymmetry is what gives SCMs their causal power.

The SCM framework is uniquely powerful because it unifies all three rungs of the Ladder of Causation within a single formal system. Rung 1 (association) is handled by the probability distribution implied by the structural equations and the distribution over exogenous variables. Rung 2 (intervention) is handled by the **do-operator**, which modifies the structural equations by replacing the equation for the intervened variable with a constant. Rung 3 (counterfactual) is handled by using the observed evidence to infer the values of exogenous variables (abduction), modifying the relevant structural equations (action), and computing the outcome under the modified model (prediction). This three-step process -- **abduction, action, prediction** -- is the SCM's algorithm for evaluating counterfactuals.

## Full Name

Also known as:
- **SCM** (abbreviation)
- **Structural equation model (SEM)** -- the broader statistical tradition; SCM adds explicit causal semantics
- **Functional causal model**
- **Causal model** (informal)
- **Nonparametric structural equation model (NPSEM)**

Contrasted with:
- **Rubin Causal Model (RCM) / Potential Outcomes Framework** -- focuses on potential outcomes Y(1), Y(0) rather than structural equations; Pearl's SCM subsumes it
- **Bayesian networks** -- share the DAG structure but lack the interventional and counterfactual semantics of SCMs
- **Statistical regression models** -- symmetric; do not encode causal direction

## Core Concepts

### The Three Components of an SCM

| Component | Symbol | Description | Example |
|-----------|--------|-------------|---------|
| **Exogenous variables** | U | External, unmodeled factors | Genetic predisposition, unmeasured environment |
| **Endogenous variables** | V | Variables explained by the model | Smoking (X), Tar deposits (M), Lung cancer (Y) |
| **Structural equations** | F | Functions mapping causes to effects | Y := f_Y(M, U_Y); M := f_M(X, U_M) |

### How SCMs Handle Each Rung

| Rung | Operation | SCM Mechanism |
|------|-----------|---------------|
| **1. Association** | Observe P(Y \| X) | Standard probability from the joint distribution implied by F and P(U) |
| **2. Intervention** | Compute P(Y \| do(X=x)) | Replace the equation for X with X := x; compute Y under the modified model |
| **3. Counterfactual** | Compute P(Y_x \| X=x', Y=y') | (1) Abduction: use evidence to update P(U); (2) Action: set X := x; (3) Prediction: compute Y |

### The Abduction-Action-Prediction Algorithm for Counterfactuals

1. **Abduction**: Given the observed evidence (e.g., patient took drug X=1 and died Y=1), use Bayesian inference to update the probability distribution over exogenous variables U.
2. **Action**: Modify the structural equation for the treatment variable to reflect the counterfactual scenario (e.g., set X := 0, meaning the patient did not take the drug).
3. **Prediction**: Use the modified model with the updated U to compute the counterfactual outcome (e.g., would the patient have survived?).

### SCM vs. Bayesian Network

| Feature | Bayesian Network | SCM |
|---------|-----------------|-----|
| Graph structure | DAG | DAG (same) |
| Encodes | Conditional independencies | Causal mechanisms |
| Handles interventions | Not natively | Yes, via do-operator |
| Handles counterfactuals | No | Yes, via abduction-action-prediction |
| Equations | None (only conditional probabilities) | Structural equations for each variable |

## Key Research and Evidence

- **Wright, S. (1921)**: "Correlation and causation" -- path analysis; the intellectual ancestor of DAG-based causal modeling
- **Haavelmo, T. (1943)**: "The statistical implications of a system of simultaneous equations" -- structural equations in economics; Nobel Prize 1989
- **Pearl, J. (1995)**: "Causal diagrams for empirical research" -- introduced the do-calculus and connected DAGs to interventional reasoning
- **Pearl, J. (2000)**: *Causality: Models, Reasoning, and Inference* -- the definitive text formalizing SCMs; 2nd edition 2009
- **Pearl, J. (2001)**: "Direct and indirect effects" -- showed how SCMs define natural direct and indirect effects for mediation analysis
- **Pearl, J. & Mackenzie, D. (2018)**: *The Book of Why* -- made SCMs accessible to a general audience

## Practical Applications

### Causal Inference in Observational Studies
SCMs provide the theoretical foundation for extracting causal conclusions from non-experimental data. By specifying a causal diagram and using the do-calculus, researchers can determine which variables to control for (and which not to) without running an experiment.

### Abuse Prevention and Fraud Detection
- **Enforcement impact modeling**: An SCM can formalize the causal pathway from enforcement action (warning, closure) through customer behavior changes to downstream outcomes (OPS, CP). This enables principled estimation of enforcement effects even from observational data.
- **False positive analysis**: Counterfactual reasoning via SCMs answers "Would this customer have been flagged as abusive even under a different policy?" -- essential for understanding whether enforcement decisions were correct.
- **Policy design**: SCMs allow simulation of hypothetical policy changes (interventions) before implementation, reducing the need for costly A/B tests.

### Knowledge Management
- SCMs provide a rigorous way to encode causal relationships between concepts in a knowledge graph or Zettelkasten, distinguishing "X is associated with Y" from "X causes Y" from "X would have prevented Y."

## Criticisms and Limitations

- **Model specification**: SCMs require the researcher to specify the correct causal diagram *a priori*, which is a strong assumption. If the diagram is wrong, all downstream inferences may be invalid.
- **Untestable assumptions**: Many of the assumptions encoded in an SCM (e.g., no unobserved confounders along a specific path) cannot be verified from data alone.
- **Functional form assumptions**: While Pearl's framework is "nonparametric" in principle (structural equations can take any functional form), practical estimation often requires parametric assumptions.
- **Scalability**: For complex systems with many variables, specifying and validating a complete SCM can be impractical.
- **Debate with statisticians**: Some prominent statisticians (e.g., Andrew Gelman, Donald Rubin) argue that the potential outcomes framework is more transparent and closer to experimental practice, though Pearl maintains that SCMs are strictly more general.

## Related Terms

- [Term: Causal Inference](term_causal_inference.md) -- the broader field for which SCMs provide the foundational framework
- [Term: Ladder of Causation](term_ladder_of_causation.md) -- the three-rung hierarchy that SCMs unify
- [Term: Directed Acyclic Graph](term_directed_acyclic_graph.md) -- the graphical component of an SCM
- [Term: Do-Calculus](term_do_calculus.md) -- the algebraic rules for deriving interventional distributions from an SCM
- [Term: Counterfactual Reasoning](term_counterfactual_reasoning.md) -- the third rung of the ladder, evaluated via SCMs
- [Term: Confounding Variable](term_confounding_variable.md) -- identified and addressed via the DAG component of an SCM
- [Term: Mediation Analysis](term_mediation_analysis.md) -- Pearl's NDE/NIE are defined within the SCM framework
- [Term: Simpson's Paradox](term_simpsons_paradox.md) -- resolved by SCMs through the back-door criterion
- [Term: Collider Bias](term_collider_bias.md) -- a structural feature identified from the DAG of an SCM
- [Term: Randomized Controlled Trial](term_randomized_controlled_trial.md) -- one method for estimating interventional distributions; SCMs generalize this
- [Term: Cognitive Bias](term_cognitive_bias.md) -- SCMs can formalize how biased reasoning confuses association with causation
- [Term: Systems Thinking](term_systems_thinking.md) -- SCMs provide a formal version of systems-level causal reasoning

## References

- Pearl, J. (2000). *Causality: Models, Reasoning, and Inference*. Cambridge University Press. (2nd edition 2009)
- Pearl, J., & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*. Basic Books.
- Pearl, J. (2009). Causal inference in statistics: An overview. *Statistics Surveys*, 3, 96-146.
- [Wikipedia: Causal Model](https://en.wikipedia.org/wiki/Causal_model)
- [CAUSALITY, 2nd Edition (Pearl's website)](https://bayes.cs.ucla.edu/BOOK-2K/)
- [Causal Inference in Statistics: A Primer (Pearl, Glymour, Jewell)](https://www.cambridge.org/core/books/causal-inference-in-statistics/16205BA70B1E2CA0D7D86C8B991A93D7)
- [Digest: The Book of Why](../digest/digest_book_of_why_pearl.md)

---

**Last Updated**: March 7, 2026
**Status**: Active
