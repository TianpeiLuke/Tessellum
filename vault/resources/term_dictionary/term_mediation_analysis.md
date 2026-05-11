---
tags:
  - resource
  - terminology
  - causal_inference
  - statistics
keywords:
  - mediation analysis
  - mediator
  - mediating variable
  - direct effect
  - indirect effect
  - natural direct effect
  - NDE
  - natural indirect effect
  - NIE
  - controlled direct effect
  - CDE
  - total effect
  - Baron and Kenny
  - causal mediation
  - Judea Pearl
topics:
  - causal inference
  - statistics
  - social science methodology
  - epidemiology
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Mediation Analysis

## Definition

**Mediation analysis** is the study of *how* a cause produces its effect -- the decomposition of the total causal effect of a treatment X on an outcome Y into the portion that operates through an intermediate variable M (the **mediator**, representing the indirect effect) and the portion that operates through all other pathways (the **direct effect**). The central question is not merely "Does X cause Y?" but "Through which pathways does X cause Y?" For example, does a new enforcement policy reduce abuse directly by deterring abusers, or indirectly by changing the customer experience (a mediating variable)?

The traditional approach to mediation analysis was established by **Baron and Kenny (1986)** in their enormously influential paper (over 100,000 citations), which proposed a four-step regression procedure: (1) show that X predicts Y; (2) show that X predicts M; (3) show that M predicts Y controlling for X; and (4) show that the effect of X on Y is reduced when M is controlled for. The indirect effect was estimated as the product of the X-M and M-Y coefficients (the "product method") or the difference between the total and direct effects (the "difference method"). While intuitively appealing and enormously popular, this approach has significant limitations: it assumes linear, additive relationships, no interaction between treatment and mediator, and correctly specified models with no unmeasured confounding.

Judea Pearl's causal mediation framework, developed in *Causality* (2000) and the paper "Direct and Indirect Effects" (2001), addresses these limitations by defining mediation effects **counterfactually** within the Structural Causal Model (SCM) framework. Pearl introduced the **Natural Direct Effect (NDE)** and **Natural Indirect Effect (NIE)**, which are defined in terms of nested counterfactuals: the NDE asks "What is the effect of changing X from x to x' while holding M at the value it would naturally take under x?" and the NIE asks "What is the effect of changing M from the value it would take under x to the value it would take under x', while holding X at x?" These definitions work for nonlinear systems, allow for treatment-mediator interaction, and decompose the total effect exactly: TE = NDE + NIE (on the risk difference scale, or TE = NDE * NIE on the risk ratio scale). However, they require stronger assumptions than the Baron-Kenny approach, particularly the "cross-world independence" assumption that the mediator under one treatment level is independent of the outcome under another treatment level, conditional on confounders.

## Full Name

Also known as:
- **Causal mediation analysis** (when using Pearl's or Robins' counterfactual definitions)
- **Mechanism analysis** / **Pathway analysis**
- **Process analysis** (in psychology)

Key quantities:
- **NDE**: Natural Direct Effect
- **NIE**: Natural Indirect Effect
- **CDE**: Controlled Direct Effect (the effect of X on Y when M is held fixed at a specific value)
- **ACME**: Average Causal Mediation Effect (Imai, Keele & Tingley, 2010)

Contrasted with:
- **Total effect estimation** -- asks "Does X cause Y?" without decomposing the pathway
- **Moderation analysis** -- asks "For whom or under what conditions does X cause Y?" (interaction effects), not "Through what pathway?"

## Core Concepts

### Traditional vs. Causal Mediation

| Feature | Baron & Kenny (1986) | Pearl's Causal Framework (2001) |
|---------|---------------------|---------------------------------|
| **Effect definitions** | Regression coefficients (a*b product, c-c' difference) | Counterfactual contrasts (NDE, NIE) |
| **Linearity assumption** | Required | Not required |
| **Treatment-mediator interaction** | Not handled | Fully accommodated |
| **Confounding** | Assumed away | Explicitly modeled via DAG |
| **Decomposition** | Approximate (fails with interaction) | Exact: TE = NDE + NIE |
| **Identification assumptions** | Implicit | Explicit (sequential ignorability) |

### Natural Direct and Indirect Effects

| Effect | Definition (Counterfactual) | Intuition |
|--------|----------------------------|-----------|
| **NDE** | E[Y(x', M(x)) - Y(x, M(x))] | Effect of changing treatment from x to x' while keeping the mediator at its natural value under x |
| **NIE** | E[Y(x, M(x')) - Y(x, M(x))] | Effect of changing the mediator from its natural value under x to its natural value under x', while keeping treatment at x |
| **CDE(m)** | E[Y(x', m) - Y(x, m)] | Effect of changing treatment from x to x' while holding the mediator fixed at level m |
| **Total Effect** | E[Y(x') - Y(x)] = NDE + NIE | The overall causal effect of X on Y |

### Identification Assumptions

For NDE and NIE to be identified from observational data, the following "sequential ignorability" conditions must hold:

| Assumption | Meaning |
|-----------|---------|
| No unmeasured confounding of X-Y | All common causes of treatment and outcome are measured |
| No unmeasured confounding of M-Y | All common causes of mediator and outcome are measured |
| No unmeasured confounding of X-M | All common causes of treatment and mediator are measured |
| No effect of X on confounders of M-Y | Treatment does not cause any confounder of the mediator-outcome relationship |

The fourth assumption is particularly stringent and often violated in practice.

### Example: Does Enforcement Reduce Abuse Through Deterrence or Through Friction?

```
Enforcement (X) --> Customer Friction (M) --> Abuse Reduction (Y)
       |                                          ^
       +------------------------------------------+
              (direct deterrence effect)
```

- **Total effect**: Overall impact of enforcement on abuse
- **NIE (indirect via friction)**: How much of the effect operates by making abuse harder (increased verification steps, delivery requirements)
- **NDE (direct deterrence)**: How much of the effect operates through the knowledge of being watched, independent of friction

## Key Research and Evidence

- **Wright, S. (1934)**: "The method of path coefficients" -- path analysis as the precursor to mediation analysis
- **Baron, R. M. & Kenny, D. A. (1986)**: "The moderator-mediator variable distinction in social psychological research" -- *Journal of Personality and Social Psychology* -- the most cited paper on mediation; introduced the four-step regression approach
- **Robins, J. M. & Greenland, S. (1992)**: "Identifiability and exchangeability for direct and indirect effects" -- first counterfactual definitions of direct and indirect effects
- **Pearl, J. (2001)**: "Direct and indirect effects" -- *Proceedings of the 17th Conference on Uncertainty in AI* -- introduced NDE and NIE within the SCM framework
- **Imai, K., Keele, L., & Tingley, D. (2010)**: "A general approach to causal mediation analysis" -- *Psychological Methods* -- influential applied framework; introduced the `mediation` R package
- **VanderWeele, T. J. (2015)**: *Explanation in Causal Inference: Methods for Mediation and Interaction* -- comprehensive modern textbook
- **Pearl, J. & Mackenzie, D. (2018)**: *The Book of Why*, Chapter 9 ("Mediation: The Search for a Mechanism")

## Practical Applications

### Social Science and Public Health
- Mediation analysis is used extensively to understand *why* interventions work (or fail), guiding the design of more targeted and efficient programs. For example, understanding whether a job training program reduces poverty through increased skills (mediator 1) or increased confidence (mediator 2) helps allocate resources.

### Abuse Prevention and Fraud Detection
- **Enforcement mechanism analysis**: Decomposing the total effect of enforcement into direct (deterrence) and indirect (friction, customer service changes) effects helps optimize enforcement design -- if the effect is mostly through friction, simpler friction-based interventions may be cheaper and less damaging to customer experience than heavy enforcement.
- **Policy pathway evaluation**: When a new abuse prevention policy has multiple effects (changes to UI, changes to refund process, changes to detection algorithms), mediation analysis can isolate which pathway drives the observed outcome change.
- **Customer experience impact**: Understanding whether enforcement reduces customer lifetime value directly (through alienation) or indirectly (through increased friction that degrades shopping experience) informs how to design enforcement that minimizes collateral damage.

### Knowledge Management
- Mediation analysis maps directly to the Zettelkasten principle of tracing chains of ideas: if concept A leads to outcome C, mediation asks "through which intermediate concepts (B) does this connection operate?" This is the intellectual analog of causal pathway decomposition.

## Criticisms and Limitations

- **Strong identification assumptions**: The sequential ignorability assumptions required for NDE/NIE identification are often untestable and may be implausible in many settings. Violation leads to biased estimates.
- **Cross-world counterfactuals**: The NDE involves counterfactuals that combine the mediator value from one "world" (treatment = x) with the treatment value from another "world" (treatment = x'). Some philosophers and statisticians find these cross-world quantities conceptually problematic.
- **Multiple mediators**: Extending mediation analysis to multiple, potentially interacting mediators is technically challenging and requires additional assumptions.
- **Measurement error**: Mediation analysis is highly sensitive to measurement error in the mediator, which biases estimates of both direct and indirect effects.
- **Overinterpretation of Baron-Kenny**: Despite its limitations, the Baron-Kenny approach remains dominant in practice; many published mediation analyses use it without checking the assumptions required for causal interpretation.

## Related Terms

- [Term: Causal Inference](term_causal_inference.md) -- the broader field; mediation analysis is a core subfield
- [Term: Structural Causal Model](term_structural_causal_model.md) -- the framework within which NDE/NIE are formally defined
- [Term: Counterfactual Reasoning](term_counterfactual_reasoning.md) -- NDE and NIE are defined counterfactually
- [Term: Directed Acyclic Graph](term_directed_acyclic_graph.md) -- the chain junction (X --> M --> Y) defines the basic mediation structure
- [Term: Confounding Variable](term_confounding_variable.md) -- mediator-outcome confounding is the central challenge of mediation analysis
- [Term: Do-Calculus](term_do_calculus.md) -- the front-door criterion is a mediation-based identification strategy
- [Term: Ladder of Causation](term_ladder_of_causation.md) -- mediation involves both Rung 2 (CDE) and Rung 3 (NDE/NIE) reasoning
- [Term: Randomized Controlled Trial](term_randomized_controlled_trial.md) -- RCTs can estimate total effects but not NDE/NIE without additional assumptions
- [Term: Collider Bias](term_collider_bias.md) -- conditioning on a post-treatment variable in mediation analysis can introduce collider bias
- [Term: Simpson's Paradox](term_simpsons_paradox.md) -- the subgroup vs. aggregate question in mediation relates to Simpson's Paradox structure
- [Term: Systems Thinking](term_systems_thinking.md) -- mediation analysis formalizes the systems thinking question "through which pathways does this effect operate?"

## References

- Baron, R. M., & Kenny, D. A. (1986). The moderator-mediator variable distinction in social psychological research. *Journal of Personality and Social Psychology*, 51(6), 1173-1182.
- Pearl, J. (2001). Direct and indirect effects. *Proceedings of the 17th Conference on Uncertainty in Artificial Intelligence*, 411-420.
- Pearl, J., & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*. Basic Books. (Chapter 9)
- VanderWeele, T. J. (2015). *Explanation in Causal Inference: Methods for Mediation and Interaction*. Oxford University Press.
- [Columbia University: Causal Mediation](https://www.publichealth.columbia.edu/research/population-health-methods/causal-mediation)
- [Pearl (2001) -- Interpretation and Identification of Causal Mediation](https://ftp.cs.ucla.edu/pub/stat_ser/r389.pdf)
- [Digest: The Book of Why](../digest/digest_book_of_why_pearl.md)

---

**Last Updated**: March 7, 2026
**Status**: Active
