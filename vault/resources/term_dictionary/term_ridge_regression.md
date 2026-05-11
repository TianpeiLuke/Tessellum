---
tags:
  - resource
  - terminology
  - statistics
  - machine_learning
  - regularization
keywords:
  - Ridge regression
  - L2 regularization
  - Tikhonov regularization
  - regularized least squares
  - RLS
  - weight decay
  - shrinkage
  - multicollinearity
topics:
  - statistical modeling
  - machine learning
  - regularization
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Ridge Regression (Regularized Least Squares / L2 Regularization)

## Definition

Ridge regression is a regularized extension of ordinary least squares (OLS) that adds an **L2 penalty** on the coefficient vector to prevent overfitting and handle multicollinearity. The objective function is:

$$\hat{\beta}_{\text{ridge}} = \arg\min_{\beta} \left\{ \|y - X\beta\|_2^2 + \lambda \|\beta\|_2^2 \right\}$$

where $\lambda \geq 0$ is the regularization hyperparameter controlling the strength of shrinkage.

The closed-form solution is:

$$\hat{\beta}_{\text{ridge}} = (X^T X + \lambda I)^{-1} X^T y$$

The method was introduced by **Hoerl & Kennard (1970)** and is also known as:

- **Tikhonov regularization** (in applied mathematics / inverse problems)
- **Weight decay** (in neural network optimization)
- **Regularized Least Squares (RLS)** (in signal processing)

The addition of $\lambda I$ to $X^T X$ ensures the matrix is always invertible, which directly resolves the rank-deficiency problem in multicollinear or underdetermined settings.

## Key Properties

- **Closed-form solution** — unlike LASSO, the ridge estimator has an explicit matrix formula, making it computationally efficient.
- **Shrinkage without sparsity** — all coefficients are shrunk toward zero but never set exactly to zero. Ridge does *not* perform feature selection.
- **Handles multicollinearity** — stabilizes coefficient estimates when predictors are highly correlated by adding $\lambda I$ to the Gram matrix.
- **Bayesian interpretation** — ridge regression is equivalent to **MAP estimation** under a Gaussian prior $\beta \sim \mathcal{N}(0, \sigma^2 / \lambda \cdot I)$ on the coefficients. The prior is a [conjugate prior](term_conjugate_prior.md) for the [normal](term_normal_distribution.md) likelihood.
- **Bias-variance tradeoff** — increasing $\lambda$ introduces bias but reduces variance, typically improving out-of-sample prediction when OLS overfits.

## Comparison with LASSO

| Property | Ridge (L2) | [LASSO](term_lasso.md) (L1) |
|---|---|---|
| Penalty | $\lambda \|\beta\|_2^2$ | $\lambda \|\beta\|_1$ |
| Effect on coefficients | Shrinkage toward zero | Shrinkage + exact zeros |
| Feature selection | No | Yes |
| Closed-form solution | Yes | No (requires iterative solver) |
| Bayesian prior | [Gaussian](term_normal_distribution.md) | Laplace |
| Multicollinearity | Handles well (groups shrunk together) | Tends to select one from correlated group |

**Elastic Net** combines both penalties: $\lambda_1 \|\beta\|_1 + \lambda_2 \|\beta\|_2^2$.

## Related Terms

- [LASSO](term_lasso.md) — L1-regularized regression with sparsity
- [Least Squares](term_least_squares.md) — unregularized baseline ($\lambda = 0$)
- [Linear Regression](term_linear_regression.md) — general family of linear models
- [Normal Distribution](term_normal_distribution.md) — Gaussian prior interpretation of ridge
- [Conjugate Prior](term_conjugate_prior.md) — Gaussian prior is conjugate for normal likelihood

- **[Elastic Net](term_elastic_net.md)**: Combines Ridge (L2) + LASSO (L1) penalties
- **[Tikhonov Regularization](term_tikhonov_regularization.md)**: General framework; Ridge is the $\Gamma=I$ special case

## References

- Hoerl, A. E., & Kennard, R. W. (1970). Ridge regression: Biased estimation for nonorthogonal problems. *Technometrics*, 12(1), 55–67.
- [Ridge regression — Wikipedia](https://en.wikipedia.org/wiki/Ridge_regression)
