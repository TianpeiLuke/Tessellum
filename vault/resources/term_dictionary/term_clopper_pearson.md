---
tags:
  - resource
  - terminology
  - statistics
  - confidence_interval
keywords:
  - Clopper-Pearson
  - exact binomial confidence interval
  - frequentist CI
  - binomial proportion
  - conservative interval
  - coverage probability
topics:
  - statistical inference
  - confidence intervals
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Clopper-Pearson Method

The **Clopper-Pearson method** (1934) is the standard exact confidence interval for a binomial proportion. It is the most commonly cited exact method and guarantees at least nominal coverage without relying on normal approximations.

## Definition

Given $k$ successes in $n$ independent Bernoulli trials, the two-sided $1 - \alpha$ Clopper-Pearson confidence interval for the true proportion $p$ is:

$$\left[ B\left(\frac{\alpha}{2};\, k,\, n - k + 1\right),\quad B\left(1 - \frac{\alpha}{2};\, k + 1,\, n - k\right) \right]$$

where $B(q;\, a,\, b)$ is the $q$-th quantile of the $\text{Beta}(a, b)$ distribution.

The interval is called **exact** because it inverts equal-tailed binomial tests, ensuring the actual coverage probability is *at least* $1 - \alpha$ for every value of $p$. This contrasts with approximate methods (Wald, Wilson) that only achieve nominal coverage asymptotically.

Special cases: when $k = 0$, the lower bound is $0$; when $k = n$, the upper bound is $1$.

## Comparison with Bayesian Approach

In the [CUBES](../areas/area_cubes_normalization.md) defect-index normalization work, Clopper-Pearson was evaluated as the frequentist alternative to Bayesian [beta-binomial](term_beta_binomial_model.md) estimation. The Bayesian approach was ultimately chosen because it:

1. **Incorporates population priors** — uses the empirical distribution of defect rates across customers as a $\text{Beta}(\alpha, \beta)$ prior, pulling extreme estimates toward the population mean.
2. **Shrinks uncertain estimates** — at low sample sizes, the posterior is dominated by the prior, producing stable estimates instead of the extremely wide Clopper-Pearson intervals.
3. **Biases in the customer's favor** — shrinkage toward the population mean reduces false positives for customers with few orders, a desirable property for abuse-prevention scoring.

Clopper-Pearson's strict frequentist guarantee (no prior information used) becomes a liability when per-customer order counts are small, which is the common case.

## Key Properties

- **Exact coverage guarantee**: $P(p \in \text{CI}) \geq 1 - \alpha$ for all $p \in [0, 1]$.
- **Conservative**: actual coverage often exceeds $1 - \alpha$, meaning intervals are wider than strictly necessary.
- **No prior information**: purely data-driven; does not borrow strength from population-level patterns.
- **Poor at low $n$**: intervals become very wide (e.g., $n = 3, k = 1$ gives a 95% CI of roughly $[0.01, 0.91]$), limiting practical utility for sparse data.
- **Computationally simple**: reduces to Beta quantile lookups, available in all statistical software.

## Related Terms

- [Binomial Distribution](term_binomial_distribution.md) — the sampling model underlying Clopper-Pearson
- [Beta Distribution](term_beta_distribution.md) — used to express the interval endpoints
- [Beta-Binomial Model](term_beta_binomial_model.md) — the Bayesian alternative chosen in CUBES
- [Defect Index](term_defect_index.md) — abuse metric where CI estimation is applied
- [F1 Score](term_f1_score.md) — CIs for precision/recall use analogous binomial proportion methods
- **[Quantile](term_quantile.md)**: Clopper-Pearson uses Beta quantiles
- **[Return Rate](term_return_rate.md)**: CI for return rate estimation
- **[CDF Transform](term_cdf_transform.md)**: Both use the Beta CDF/inverse CDF
- **[Exponential Family](term_exponential_family.md)**: Binomial (underlying model) is exponential family

- **[Confidence Interval](term_confidence_interval.md)**: Clopper-Pearson produces exact binomial CIs

## References

- Clopper, C. J. & Pearson, E. S. (1934). "The use of confidence or fiducial limits illustrated in the case of the binomial." *Biometrika*, 26(4), 404–413.
- [Binomial proportion confidence interval — Wikipedia](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval)
- CUBES normalization experiment (vault: [area_cubes_normalization.md](../areas/area_cubes_normalization.md))
