---
tags:
  - resource
  - terminology
  - statistics
  - probability
  - power_law
keywords:
  - Pareto distribution
  - power law
  - heavy tail
  - fat tail
  - Pareto principle
  - 80/20
  - scale-free
  - Vilfredo Pareto
  - wealth distribution
  - Type I
topics:
  - probability theory
  - extreme value theory
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Pareto Distribution

## Definition

The **Pareto distribution** is a heavy-tailed, continuous probability distribution named after Italian economist Vilfredo Pareto (1848–1923), who used it to model the distribution of wealth across populations.

The Type I Pareto distribution has probability density function (PDF):

$$f(x) = \frac{\alpha \, x_m^\alpha}{x^{\alpha+1}}, \quad x \geq x_m$$

and survival function (complementary CDF):

$$P(X > x) = \left(\frac{x_m}{x}\right)^\alpha, \quad x \geq x_m$$

**Parameters:**
- $\alpha > 0$ — **shape** (tail index): controls how heavy the tail is; smaller $\alpha$ = heavier tail
- $x_m > 0$ — **scale** (minimum value): the lower bound of the support

The Pareto distribution is **not** a member of the exponential family — its support $[x_m, \infty)$ depends on the parameter $x_m$, violating a key requirement for exponential family membership.

## Key Properties

| Property | Value |
|----------|-------|
| Mean | $\frac{\alpha \, x_m}{\alpha - 1}$ for $\alpha > 1$; $\infty$ for $\alpha \leq 1$ |
| Variance | $\frac{x_m^2 \, \alpha}{(\alpha-1)^2(\alpha-2)}$ for $\alpha > 2$; $\infty$ for $\alpha \leq 2$ |
| Median | $x_m \, 2^{1/\alpha}$ |
| Mode | $x_m$ |

- **Heavy tail**: $P(X > x) \sim x^{-\alpha}$ — polynomial decay, much slower than exponential
- **Infinite variance** when $\alpha \leq 2$: sample variance does not converge
- **Infinite mean** when $\alpha \leq 1$: sample mean does not converge
- **Connection to the Pareto principle**: when $\alpha = \log_4 5 \approx 1.16$, the distribution produces the classic 80/20 rule — 20% of the population holds 80% of the total
- **Scale-free property**: if $X$ is Pareto, then $P(X > cx \mid X > c) = P(X > x)$ — the tail looks the same at every scale
- **Not exponential family**: contrast with [Gamma](term_gamma_distribution.md) or [Normal](term_normal_distribution.md), which are exponential family members

## Applications

| Domain | Example |
|--------|---------|
| Economics | Wealth and income distribution across populations |
| Linguistics | City sizes, word frequencies (Zipf's law) |
| Computer science | File sizes, network traffic, degree distributions |
| Insurance | Large claim sizes, catastrophic loss modeling |
| **Abuse detection** | Extreme return rates follow power-law tails — a small fraction of buyers account for a disproportionate share of total abuse losses |

In buyer abuse prevention, the Pareto distribution motivates focusing enforcement on the heavy tail of abusive behavior, where a small number of accounts generate outsized losses.

## Related Terms

- [Fat Tails](term_fat_tails.md) — the distributional property that Pareto exemplifies
- [Exponential Family](term_exponential_family.md) — contrast: Pareto is **not** an exponential family member
- [Pareto Principle](term_pareto_principle.md) — the 80/20 rule derived from Pareto-distributed phenomena
- [Gamma Distribution](term_gamma_distribution.md) — an exponential family alternative for modeling skewed data
- [Normal Distribution](term_normal_distribution.md) — contrast: thin-tailed (sub-exponential decay) vs. Pareto's fat tail

- **[Concentration Inequality](term_concentration_inequality.md)**: Pareto tails violate sub-Gaussian assumptions — need heavy-tail concentration
- **[LASSO](term_lasso.md)**: LASSO with heavy-tailed (Pareto) errors requires robust variants
- **[Confidence Interval](term_confidence_interval.md)**: Pareto CIs are much wider than Gaussian CIs due to heavy tails
- **[Return Rate](term_return_rate.md)**: Extreme return rates follow Pareto-like power law tails
- **[XGBoost](term_xgboost.md)**: Tree models handle Pareto-distributed features better than linear models
- **[Alignment Scaling Law](term_alignment_scaling_law.md)**: Neural scaling laws  \propto N^{-\alpha}$ ARE power laws — Pareto is the canonical power law distribution

## References

- [Pareto distribution — Wikipedia](https://en.wikipedia.org/wiki/Pareto_distribution)
- Pareto, V. (1896). *Cours d'économie politique*.
