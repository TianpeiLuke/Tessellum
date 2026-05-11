---
tags:
  - resource
  - terminology
  - statistics
  - probability
  - concentration_inequality
keywords:
  - Chernoff bound
  - moment generating function
  - MGF method
  - exponential bound
  - multiplicative form
topics:
  - concentration inequalities
  - probability theory
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Chernoff Bound

## Definition

The **Chernoff bound** is a generic technique for deriving exponential tail bounds using the moment generating function (MGF). It produces the tightest possible exponential bound obtainable from the MGF.

For any random variable $X$ and threshold $t$:

$$P(X \geq t) \leq \inf_{s > 0}\; e^{-st}\, E[e^{sX}]$$

This follows from Markov's inequality applied to $e^{sX}$: $P(X \geq t) = P(e^{sX} \geq e^{st}) \leq e^{-st} E[e^{sX}]$, then optimizing over $s > 0$.

## Multiplicative Form (Binomial)

For $X = \sum_{i=1}^n X_i$ where $X_i \sim \text{Bernoulli}(p_i)$ independently, with $\mu = E[X]$:

$$P(X \geq (1+\delta)\mu) \leq \left(\frac{e^\delta}{(1+\delta)^{(1+\delta)}}\right)^\mu$$

Useful simplified forms for $\delta \in (0, 1]$:

$$P(X \geq (1+\delta)\mu) \leq \exp\left(-\frac{\mu \delta^2}{3}\right)$$

$$P(X \leq (1-\delta)\mu) \leq \exp\left(-\frac{\mu \delta^2}{2}\right)$$

## Relationship to Other Bounds

The Chernoff method is the **parent technique** — other concentration inequalities are derived by bounding the MGF under specific assumptions:

| Inequality | MGF Assumption |
|-----------|----------------|
| [Hoeffding](term_hoeffding_inequality.md) | Bounded support → Hoeffding's lemma for MGF |
| [Bernstein](term_bernstein_inequality.md) | Bounded + variance constraint on MGF |
| [Bounded Differences](term_bounded_differences_inequality.md) | Lipschitz function → per-coordinate MGF bound |

## Abuse Prevention Relevance

The multiplicative form is natural for count-based abuse metrics (e.g., number of fraudulent returns out of $n$ orders), where deviations are best expressed as a fraction of the expected count.

## Related Terms

- [Concentration Inequality](term_concentration_inequality.md) — parent overview
- [Hoeffding's Inequality](term_hoeffding_inequality.md) — special case for bounded RVs
- [Bernstein's Inequality](term_bernstein_inequality.md) — special case with variance info
- [Binomial Distribution](term_binomial_distribution.md) — multiplicative form applies here
- **[LASSO](term_lasso.md)**: LASSO restricted eigenvalue conditions proved via Chernoff-type bounds
- **[GraphLasso](term_graphlasso.md)**: Sample covariance concentration uses Chernoff bounds
- **[PAC Learning](term_pac_learning.md)**: Finite hypothesis PAC bounds use Chernoff + union bound
- **[Normal Distribution](term_normal_distribution.md)**: Gaussian Chernoff bound gives optimal sub-Gaussian tail
- **[Exponential Family](term_exponential_family.md)**: Chernoff bound uses MGF — defined for exponential family
- **[Confidence Interval](term_confidence_interval.md)**: Chernoff gives exponentially tight CIs for bounded RVs
- **[JL Lemma](term_johnson_lindenstrauss_lemma.md)**: $\chi^2$ Chernoff bound is the core of JL proof
