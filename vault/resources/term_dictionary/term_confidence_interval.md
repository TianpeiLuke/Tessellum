---
tags:
  - resource
  - terminology
  - statistics
  - inference
keywords:
  - confidence interval
  - CI
  - frequentist inference
  - coverage probability
  - margin of error
  - standard error
  - Neyman
topics:
  - statistical inference
  - hypothesis testing
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Confidence Interval

## Definition

A **confidence interval** (CI) is a range of values, computed from sample data, that contains the true population parameter $\theta$ with a specified probability $1 - \alpha$ over repeated sampling. For a $(1 - \alpha) \times 100\%$ CI with a point estimate $\hat{\theta}$ and standard error $SE$:

$$
CI = \left[\hat{\theta} - z_{\alpha/2} \cdot SE, \;\; \hat{\theta} + z_{\alpha/2} \cdot SE\right]
$$

where $z_{\alpha/2}$ is the critical value from the standard normal distribution (e.g., $z_{0.025} = 1.96$ for a 95% CI).

The frequentist interpretation: if we repeated the experiment many times and constructed a CI each time, $(1 - \alpha) \times 100\%$ of those intervals would contain the true parameter $\theta$. Crucially, a CI does **not** say "there is a 95% probability that $\theta$ lies in this interval." The parameter is fixed; the interval is random. The probabilistic statement that $\theta$ lies within a given interval with some posterior probability is the domain of the **Bayesian credible interval**.

## Comparison with Credible Interval

| Property | Confidence Interval | Credible Interval |
|---|---|---|
| **Framework** | Frequentist | Bayesian |
| **Guarantee** | Coverage probability over repeated samples | Posterior probability given observed data |
| **Parameter** | Fixed but unknown | Random variable with a distribution |
| **Prior information** | Not used | Incorporated via prior distribution |
| **Interpretation** | "95% of such intervals contain $\theta$" | "95% probability $\theta$ is in this interval" |
| **Common methods** | Wald, Clopper-Pearson, Wilson | HPD, equal-tailed from posterior |

In **CUBES**, Bayesian credible intervals were chosen over frequentist confidence intervals because they naturally incorporate prior information (e.g., historical abuse rates via a [Beta-Binomial model](term_beta_binomial_model.md)) and provide direct probability statements about the parameter of interest, which aligns better with decision-making under uncertainty in abuse prevention.

## Key Properties

- **Coverage probability**: A $(1-\alpha)$ CI achieves its nominal coverage rate asymptotically — in finite samples, actual coverage may differ depending on the method.
- **Width**: Proportional to $z_{\alpha/2} \cdot \sigma / \sqrt{n}$. Increasing sample size $n$ or decreasing confidence level $1-\alpha$ narrows the interval.
- **Normal approximation**: For large $n$, the CLT justifies using the Gaussian-based formula above. Breaks down for small $n$ or extreme proportions.
- **[Clopper-Pearson](term_clopper_pearson.md)**: The exact binomial CI that inverts two one-sided binomial tests. Guarantees $\geq 1-\alpha$ coverage for any $n$ and true proportion $p$, at the cost of being conservative (wider than necessary).
- **Wilson interval**: A score-based alternative for binomial proportions that has better coverage properties than Wald for small $n$ or $p$ near 0 or 1.
- **Bootstrap CI**: Nonparametric approach using resampling; useful when the sampling distribution of $\hat{\theta}$ is unknown or intractable.

## Related Terms

- [Clopper-Pearson](term_clopper_pearson.md) — exact binomial confidence interval
- [Beta-Binomial Model](term_beta_binomial_model.md) — Bayesian model producing credible intervals
- [Normal Distribution](term_normal_distribution.md) — basis for the large-sample CI formula
- [Binomial Distribution](term_binomial_distribution.md) — discrete distribution for which exact CIs exist
- [Conformal Prediction](term_conformal_prediction.md) — distribution-free prediction intervals with finite-sample coverage guarantees

- **[Concentration Inequality](term_concentration_inequality.md)**: CI width formulas are derived from concentration inequalities
- **[JL Lemma](term_johnson_lindenstrauss_lemma.md)**: JL projection preserves distances — gives $(1\pm\epsilon)$ CI on projected distances

## References

- Neyman, J. (1937). "Outline of a Theory of Statistical Estimation Based on the Classical Theory of Probability." *Philosophical Transactions of the Royal Society A*, 236(767), 333–380.
- [Wikipedia: Confidence interval](https://en.wikipedia.org/wiki/Confidence_interval)
- Clopper, C. J. & Pearson, E. S. (1934). "The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial." *Biometrika*, 26(4), 404–413.
