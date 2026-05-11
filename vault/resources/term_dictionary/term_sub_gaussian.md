---
tags:
  - resource
  - terminology
  - statistics
  - probability
  - concentration_inequality
keywords:
  - sub-Gaussian
  - sub-exponential
  - light tail
  - tail behavior
  - Orlicz norm
  - moment generating function
  - concentration
topics:
  - high-dimensional probability
  - concentration inequalities
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Sub-Gaussian Random Variables

## Definition

A centered random variable $X$ is **sub-Gaussian** with parameter $\sigma$ if its moment generating function satisfies:

$$E\left[e^{s(X - EX)}\right] \leq e^{s^2 \sigma^2 / 2} \quad \text{for all } s \in \mathbb{R}$$

Equivalently, the tails of $X$ decay at least as fast as those of a Gaussian with variance $\sigma^2$. The **sub-Gaussian norm** (Orlicz $\psi_2$-norm) provides an equivalent characterization:

$$\|X\|_{\psi_2} = \inf\left\{t > 0 : E\left[e^{X^2/t^2}\right] \leq 2\right\}$$

Examples of sub-Gaussian random variables include: bounded random variables (by Hoeffding's lemma), Gaussian, Rademacher, and Bernoulli.

## Key Properties

- **Tail bound**: $P(|X - EX| \geq t) \leq 2\exp\left(-\frac{t^2}{2\sigma^2}\right)$
- **Closure under summation**: if $X_1, \ldots, X_n$ are independent sub-Gaussian, then $\sum_i X_i$ is sub-Gaussian with $\sigma^2 = \sum_i \sigma_i^2$
- **Hoeffding's inequality** is a direct consequence for bounded sub-Gaussians
- **Sub-exponential** is the next broader class — heavier tails, $E[e^{s|X|}] < \infty$ only for $|s| < \lambda$
- Product of two sub-Gaussians is sub-exponential (Bernstein-type behavior)

## Related Terms

- [Concentration Inequality](term_concentration_inequality.md)
- [Hoeffding's Inequality](term_hoeffding_inequality.md)
- [Normal Distribution](term_normal_distribution.md) — Gaussian is sub-Gaussian
- [Bernstein Inequality](term_bernstein_inequality.md) — sub-exponential extension
- **[Chernoff Bound](term_chernoff_bound.md)**: Chernoff method proves sub-Gaussian tail bounds via MGF
- **[Bounded Differences](term_bounded_differences_inequality.md)**: Functions of sub-Gaussian RVs satisfy bounded differences
- **[Exponential Family](term_exponential_family.md)**: Many exponential family members are sub-Gaussian (bounded support)
- **[Binomial Distribution](term_binomial_distribution.md)**: Centered Binomial is sub-Gaussian (bounded)
- **[Beta Distribution](term_beta_distribution.md)**: Beta RVs are sub-Gaussian (bounded on [0,1])
- **[Confidence Interval](term_confidence_interval.md)**: Sub-Gaussian concentration gives tighter CIs than Chebyshev
- **[PAC Learning](term_pac_learning.md)**: PAC bounds for sub-Gaussian losses are tighter than general case
- **[LASSO](term_lasso.md)**: LASSO theory assumes sub-Gaussian design matrix for consistency
- **[UCB](term_ucb.md)**: UCB analysis assumes sub-Gaussian reward distributions for confidence bounds
- **[Contextual Bandit](term_contextual_bandit.md)**: LinUCB assumes sub-Gaussian noise on linear reward model
- **[Alignment Scaling Law](term_alignment_scaling_law.md)**: Scaling law residuals are often sub-Gaussian
- **[JL Lemma](term_johnson_lindenstrauss_lemma.md)**: JL extends to sub-Gaussian projections — not just Gaussian
