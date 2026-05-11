---
tags:
  - resource
  - terminology
  - statistics
  - decision_making
  - probability
keywords:
  - Bayesian reasoning
  - Bayes rule
  - prior
  - posterior
  - base rate
  - Bayesian inference
  - probability updating
topics:
  - statistics
  - decision making
  - probability theory
language: markdown
date of note: 2026-03-12
status: active
building_block: concept
---

# Term: Bayesian Reasoning

## Definition

**Bayesian reasoning** is a framework for updating beliefs in light of new evidence, formalized by **Bayes's rule**: `P(hypothesis | evidence) ∝ P(evidence | hypothesis) × P(hypothesis)`. The **prior** P(hypothesis) encodes what you believed before seeing data; the **likelihood** P(evidence | hypothesis) measures how well the hypothesis explains the evidence; the **posterior** P(hypothesis | evidence) is your updated belief. The framework's central insight is that **the prior matters enormously** — with limited evidence, pre-existing knowledge (base rates) should dominate predictions; with abundant evidence, data overwhelms the prior. Christian & Griffiths demonstrate that humans are surprisingly good Bayesian reasoners when they have correct priors; most systematic prediction errors stem from **wrong priors (base-rate neglect)**, not flawed reasoning.

## Full Name

**Bayesian Reasoning** = Bayesian Inference / Bayesian Probability Updating

Also known as: **Bayesian Inference**, **Bayesian Updating**, **Probabilistic Reasoning**

## How Bayesian Reasoning Works

### Bayes's Rule

```
                    P(evidence | hypothesis) × P(hypothesis)
P(hypothesis | evidence) = ──────────────────────────────────────────
                                    P(evidence)

Prior:      What you believed before seeing evidence
Likelihood: How probable the evidence is under each hypothesis
Posterior:  Your updated belief after seeing evidence
```

### The Distribution-Prediction Table

Different real-world phenomena follow different distributions, and the correct prior determines the correct prediction rule:

| Type of Phenomenon | Distribution | Prediction Rule | Example |
|-------------------|-------------|----------------|---------|
| Human lifespan, movie runtime | Normal (Gaussian) | Predict the average | "A movie will be about 2 hours" |
| City population, wealth | Power law | Predict current value will increase | "A big city will keep growing" |
| Political term length | Erlang | Predict the average term | "A president will serve one term" |
| Pharaoh's reign, parking meter | Memoryless (exponential) | Will last as long as it already has ([Lindy effect](term_lindy_effect.md)) | "If it's lasted 10 years, expect 10 more" |

### Prior Strength vs. Evidence Strength

| Regime | Prior | Evidence | Strategy |
|--------|-------|----------|----------|
| **Strong prior, weak evidence** | High confidence | Little data | Trust the prior; evidence barely moves you |
| **Weak prior, strong evidence** | Low confidence | Abundant data | Let the data drive; prior is washed out |
| **Strong prior, strong evidence** | High confidence | Abundant data | Posterior is precise; small uncertainty |
| **Weak prior, weak evidence** | Low confidence | Little data | High uncertainty; be cautious about any prediction |

## Key Concepts

### Base Rate Neglect
The most common Bayesian failure: ignoring the prior probability (base rate) when evaluating evidence. A positive medical test result for a rare disease is usually a false positive — because P(disease) is very low, even a highly accurate test produces more false positives than true positives in absolute numbers.

### Uninformative vs. Informative Priors
- **Uninformative prior**: Maximum ignorance (uniform distribution) — let the data speak
- **Informative prior**: Encodes domain knowledge — useful when data is scarce
- **Empirical Bayes**: Estimate the prior from the data itself

### Bayesian Updating as Learning
Each new observation updates the posterior, which becomes the prior for the next observation. Over time, posteriors converge regardless of starting priors (given enough evidence) — a property called **Bayesian convergence**.

## Practical Applications

1. **Protect your priors**: Exposure to unrepresentative samples (media, social circles) corrupts priors, leading to biased predictions
2. **Use base rates first**: Before evaluating specific evidence, start with the population base rate
3. **Match predictions to distributions**: Identify whether a phenomenon is normal, power-law, or memoryless to choose the right prediction rule
4. **With sparse data, trust experience**: When evidence is limited, prior knowledge (heuristics, gut instinct) is the dominant signal

## Related Terms

### Statistical Foundations
- **[Term: Causal Inference](term_causal_inference.md)** — Pearl's causal framework extends Bayesian reasoning to causal claims
- **[Term: Confounding Variable](term_confounding_variable.md)** — Bayesian reasoning alone cannot resolve confounding without causal assumptions
- **[Term: Overfitting](term_overfitting.md)** — Bayesian regularization (informative priors) prevents overfitting to noise

### Cognitive Science
- **[Term: Cognitive Bias](term_cognitive_bias.md)** — Many biases (anchoring, availability, base-rate neglect) are Bayesian failures
- **[Term: System 1 and System 2](term_system_1_and_system_2.md)** — System 1 uses fast heuristics that approximate (but sometimes violate) Bayesian norms
- **[Term: MAB (Multi-Armed Bandit)](term_mab.md)** — Thompson Sampling is a Bayesian approach to the explore/exploit trade-off

### Source
- **[Digest: Algorithms to Live By](../digest/digest_algorithms_to_live_by_christian.md)** — Chapter 6: Bayes's Rule
- **[Digest: The Book of Why](../digest/digest_book_of_why_pearl.md)** — Pearl's Bayesian networks formalize causal-probabilistic reasoning

- **[Probabilistic Graphical Model](term_probabilistic_graphical_model.md)**: Bayesian reasoning is the foundation of directed PGMs
- **[Variational Inference](term_variational_inference.md)**: Approximate Bayesian inference by optimization (alternative to MCMC)

### Cross-Domain: Argumentation-Theoretic Aggregation
- **[DF-QuAD](term_df_quad.md)**: Discontinuity-Free QuAD gradual semantics — deterministic aggregation function for argumentation strength; a non-probabilistic counterpart to Bayesian belief updating that operates on attack/support edges instead of conditional independence

## References

- Christian, B. & Griffiths, T. (2016). *Algorithms to Live By*, Chapter 6: Bayes's Rule. Henry Holt and Company.
- Bayes, T. (1763). "An Essay towards Solving a Problem in the Doctrine of Chances." *Philosophical Transactions of the Royal Society*, 53, 370–418.
- Kahneman, D. & Tversky, A. (1973). "On the Psychology of Prediction." *Psychological Review*, 80(4), 237–251.

---

**Last Updated**: March 12, 2026
**Status**: Active — Statistics, probability, and decision science
