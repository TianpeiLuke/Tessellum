---
tags:
  - resource
  - terminology
  - statistics
  - regression
keywords:
  - quantile regression
  - conditional quantile
  - Koenker Bassett
  - median regression
  - heteroscedasticity
  - robust regression
  - distributional regression
topics:
  - statistical modeling
  - regression analysis
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Quantile Regression

## Definition

Quantile regression estimates **conditional quantiles** of a response variable given covariates, rather than the conditional mean. Introduced by Koenker & Bassett (1978), it solves:

$$\hat{\beta}(\tau) = \arg\min_{\beta} \sum_{i=1}^{n} \rho_\tau(y_i - \mathbf{x}_i'\beta)$$

where $\rho_\tau(u) = u(\tau - \mathbf{1}_{\{u < 0\}})$ is the **check function** (also called pinball loss or tick loss). This applies an asymmetric penalty: underestimates are weighted by $\tau$ and overestimates by $(1 - \tau)$. At $\tau = 0.5$, this reduces to **median regression** (minimizing the sum of absolute deviations).

## Comparison with OLS

| Aspect | OLS | Quantile Regression |
|---|---|---|
| **Estimand** | $E[Y \mid X]$ (conditional mean) | $Q_\tau(Y \mid X)$ (conditional quantile) |
| **Loss function** | Squared error $\sum(y_i - x_i'\beta)^2$ | Check function $\sum \rho_\tau(y_i - x_i'\beta)$ |
| **Outlier sensitivity** | Sensitive (squared penalty) | Robust (linear penalty) |
| **Heteroscedasticity** | Assumes homoscedastic errors | Naturally accommodates heteroscedasticity |
| **Distributional insight** | Single summary (mean) | Full distributional picture across quantiles |

## Applications

| Domain | Use Case |
|---|---|
| **Economics** | Wage inequality — effects of education differ at 10th vs 90th percentile of income |
| **Finance** | Value-at-Risk (VaR) estimation via lower quantiles of portfolio returns |
| **Ecology** | Species response to environmental gradients at distributional extremes |
| **Abuse prevention** | Modeling tails of return rate distributions to identify policy stretchers who exploit return policies at extreme quantiles |

## Related Terms

- [Quantile](term_quantile.md) — the statistical concept underlying quantile regression
- [Linear Regression](term_linear_regression.md) — the mean-based counterpart
- [Least Squares](term_least_squares.md) — the standard OLS estimation method

- **[Return Rate](term_return_rate.md)**: QR could model tails of return rate distributions for policy stretcher identification
- **[Exponential Family](term_exponential_family.md)**: QR doesn't assume exponential family — that's its advantage over GLMs
- **[Normal Distribution](term_normal_distribution.md)**: QR doesn't assume Gaussian errors — that's its advantage over OLS
- **[Confidence Interval](term_confidence_interval.md)**: QR produces conditional quantile CIs, not just mean CIs
- **[Concentration Inequality](term_concentration_inequality.md)**: QR consistency proofs use empirical process concentration
- **[LASSO](term_lasso.md)**: L1-penalized quantile regression for sparse quantile models
- **[Ridge Regression](term_ridge_regression.md)**: L2-penalized quantile regression for regularized quantile estimation
- **[XGBoost](term_xgboost.md)**: Quantile regression forests and XGBoost quantile loss for distributional prediction
- **[Pareto Distribution](term_pareto_distribution.md)**: QR is especially useful for heavy-tailed (Pareto-like) response distributions

## References

- Koenker, R. & Bassett, G. (1978). Regression Quantiles. *Econometrica*, 46(1), 33–50.
- [Wikipedia — Quantile regression](https://en.wikipedia.org/wiki/Quantile_regression)
