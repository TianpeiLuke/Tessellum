---
tags:
  - resource
  - terminology
  - statistics
  - data_metrics
keywords:
  - quantile
  - percentile
  - quartile
  - median
  - quantile function
  - inverse CDF
  - order statistics
topics:
  - descriptive statistics
  - data analysis
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Quantile

## Definition

In statistics and probability, the **$q$-th quantile** of a probability distribution is the value $x$ such that:

$$P(X \leq x) = q, \quad q \in [0, 1]$$

Equivalently, the quantile function $Q$ is the **inverse of the cumulative distribution function (CDF)**:

$$Q(q) = F^{-1}(q) = \inf \{ x \in \mathbb{R} : F(x) \geq q \}$$

The infimum formulation handles discrete distributions where $F$ may have jumps.

**Special cases:**

| Name | $q$ value(s) | Description |
|------|-------------|-------------|
| Median | $q = 0.5$ | Splits distribution into equal halves |
| Quartiles | $q \in \{0.25, 0.50, 0.75\}$ | Divides into four equal parts (Q1, Q2, Q3) |
| Percentiles | $q \in \{0.01, 0.02, \ldots, 0.99\}$ | Divides into 100 equal parts (P1–P99) |
| Deciles | $q \in \{0.1, 0.2, \ldots, 0.9\}$ | Divides into 10 equal parts |

## Key Properties

- **Inverse relationship to CDF**: $Q(q) = F^{-1}(q)$; the CDF maps values to probabilities, the quantile function maps probabilities back to values.
- **Order statistics**: For a sample of size $n$, the $k$-th order statistic $X_{(k)}$ estimates the $(k/(n+1))$-th quantile. Sample quantiles are weighted averages of consecutive order statistics.
- **Interpolation methods**: For discrete/finite samples, different interpolation schemes exist (e.g., NumPy's 9 methods, R's 9 `type` options). Common approaches include linear interpolation between adjacent order statistics and nearest-rank methods.
- **Monotonicity**: $Q$ is non-decreasing; if $q_1 < q_2$ then $Q(q_1) \leq Q(q_2)$.

## Applications

| Domain | Usage | Example |
|--------|-------|---------|
| **CUBES** | Percentile thresholds from prior distribution define "excessive" return rates for policy stretching | 95th percentile of return-rate prior flags abnormal behavior |
| **Risk metrics** | Value at Risk (VaR) is the $q$-th quantile of a loss distribution | VaR$_{0.99}$ = 99th percentile loss |
| **Performance SLAs** | P50/P90/P99 latency targets | P99 latency < 200ms |
| **Salary benchmarks** | Compensation bands defined by market percentiles | Target 75th percentile for total comp |
| **Defect scoring** | Quantile-based normalization of defect indices across populations | Defect index mapped to percentile rank |

## Related Terms

- [CDF Transform](term_cdf_transform.md) — forward CDF; quantile is its inverse
- [Quantile Regression](term_quantile_regression.md) — models conditional quantiles instead of conditional mean
- [Beta Distribution](term_beta_distribution.md) — Beta quantile function yields Clopper-Pearson exact confidence intervals
- [Defect Index](term_defect_index.md) — quantile thresholds used in defect scoring
- **[Return Rate](term_return_rate.md)**: Quantile thresholds define excessive return rates in CUBES
- **[Clopper-Pearson](term_clopper_pearson.md)**: Uses Beta quantiles for exact binomial CI
- **[Exponential Family](term_exponential_family.md)**: Quantile function is the inverse CDF of exponential family members

- **[Normal Distribution](term_normal_distribution.md)**: Normal quantiles (z-scores) are the basis of standard CIs
- **[Pareto Distribution](term_pareto_distribution.md)**: Pareto quantiles grow much faster than Gaussian — heavy tail effect
- **[Poisson Distribution](term_poisson_distribution.md)**: Poisson quantiles for count data thresholds
- **[XGBoost](term_xgboost.md)**: Quantile regression with XGBoost for distributional prediction
- **[Linear Regression](term_linear_regression.md)**: OLS estimates conditional mean; quantiles give full distribution
- **[Latency](term_latency.md)**: Quantiles underpin percentile latency reporting — p50, p95, p99 measure the distribution of per-request response times

## References

- [Quantile — Wikipedia](https://en.wikipedia.org/wiki/Quantile)
- [Quantile Function — Wikipedia](https://en.wikipedia.org/wiki/Quantile_function)
