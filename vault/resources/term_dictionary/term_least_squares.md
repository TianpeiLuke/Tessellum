---
tags:
  - resource
  - terminology
  - statistics
  - optimization
keywords:
  - least squares
  - OLS
  - ordinary least squares
  - sum of squared residuals
  - normal equations
  - Gauss
  - Legendre
  - regression
  - curve fitting
topics:
  - statistical estimation
  - optimization
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Least Squares Estimation

## Definition

**Least squares** is a statistical estimation method that finds parameter values by minimizing the sum of squared residuals between observed and predicted values.

Given a linear model $y = X\beta + \varepsilon$, the least squares objective is:

$$\hat{\beta} = \arg\min_{\beta} \sum_{i=1}^{n} (y_i - \mathbf{x}_i^\top \beta)^2 = \arg\min_{\beta} \| y - X\beta \|^2$$

Setting the gradient to zero yields the **normal equations**:

$$X^\top X \hat{\beta} = X^\top y \quad \Longrightarrow \quad \hat{\beta} = (X^\top X)^{-1} X^\top y$$

The method was independently discovered by **Carl Friedrich Gauss** (1795, published 1809 in *Theoria Motus*) and **Adrien-Marie Legendre** (first published 1805 in *Nouvelles méthodes pour la détermination des orbites des comètes*). Both applied it to astronomical orbit determination.

## Key Properties

- **Closed-form solution** — the normal equations give an explicit formula requiring no iterative optimization.
- **BLUE (Best Linear Unbiased Estimator)** — under the Gauss–Markov assumptions ($E[\varepsilon]=0$, $\text{Var}(\varepsilon)=\sigma^2 I$, uncorrelated errors), OLS has the smallest variance among all linear unbiased estimators.
- **MLE equivalence** — when errors are i.i.d. Gaussian, the OLS estimator coincides with the maximum likelihood estimator.
- **Geometric interpretation** — $\hat{y} = X\hat{\beta}$ is the orthogonal projection of $y$ onto the column space of $X$.
- **Sensitivity to outliers** — squaring residuals amplifies the influence of extreme observations, motivating robust alternatives.

## Variants

| Variant | Modification | Use Case |
|---|---|---|
| **OLS** | Standard $\min \|y - X\beta\|^2$ | Homoscedastic, uncorrelated errors |
| **Weighted LS (WLS)** | $\min \sum w_i (y_i - \mathbf{x}_i^\top\beta)^2$ | Known heteroscedastic variances |
| **Generalized LS (GLS)** | $\min (y-X\beta)^\top \Omega^{-1}(y-X\beta)$ | Correlated and/or heteroscedastic errors |
| **Nonlinear LS** | $\min \sum (y_i - f(\mathbf{x}_i,\beta))^2$ | Nonlinear model $f$ |
| **Ridge (L2)** | $\min \|y-X\beta\|^2 + \lambda\|\beta\|^2$ | Multicollinearity, regularization |
| **Lasso (L1)** | $\min \|y-X\beta\|^2 + \lambda\|\beta\|_1$ | Sparsity, feature selection |

## Related Terms

- [Linear Regression](term_linear_regression.md) — the primary model estimated via least squares
- [Logistic Regression](term_logistic_regression.md) — uses maximum likelihood instead of least squares for classification
- [Quantile Regression](term_quantile_regression.md) — robust alternative minimizing asymmetric absolute loss
- [Exponential Family](term_exponential_family.md) — generalization connecting least squares to broader GLM framework

- **[Return Rate](term_return_rate.md)**: OLS could estimate return rate trends; but Bayesian approach preferred for sparse data
- **[Normal Distribution](term_normal_distribution.md)**: MLE under Gaussian = least squares
- **[LASSO](term_lasso.md)**: L1 regularized variant of least squares
- **[Ridge Regression](term_ridge_regression.md)**: L2 regularized variant of least squares

## References

- Gauss, C. F. (1809). *Theoria Motus Corporum Coelestium*. Hamburg: Perthes et Besser.
- Legendre, A.-M. (1805). *Nouvelles méthodes pour la détermination des orbites des comètes*. Paris: Firmin Didot.
- [Least squares — Wikipedia](https://en.wikipedia.org/wiki/Least_squares)
- [Gauss–Markov theorem — Wikipedia](https://en.wikipedia.org/wiki/Gauss%E2%80%93Markov_theorem)
