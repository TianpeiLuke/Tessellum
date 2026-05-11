---
tags:
  - resource
  - terminology
  - statistics
  - machine_learning
  - regularization
keywords:
  - LASSO
  - L1 regularization
  - least absolute shrinkage
  - feature selection
  - sparsity
  - Tibshirani
  - compressed sensing
  - elastic net
topics:
  - statistical modeling
  - machine learning
  - regularization
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# LASSO (Least Absolute Shrinkage and Selection Operator)

## Definition

LASSO is a regularized regression method that adds an **L1 penalty** to the ordinary least squares objective, solving:

$$\min_{\beta} \frac{1}{2n} \|y - X\beta\|_2^2 + \lambda \|\beta\|_1$$

where $\lambda \geq 0$ controls regularization strength and $\|\beta\|_1 = \sum_{j=1}^{p} |\beta_j|$ is the L1 norm.

Introduced by **Robert Tibshirani (1996)**, LASSO's key property is that the L1 penalty induces **sparsity** — it drives coefficients exactly to zero, performing automatic feature selection. This contrasts with Ridge regression (L2), which shrinks coefficients toward zero but never sets them exactly to zero.

The name stands for **Least Absolute Shrinkage and Selection Operator**, reflecting its dual role: shrinking coefficient magnitudes and selecting a subset of features.

## Historical Context

| Year | Contribution | Authors |
|------|-------------|---------|
| 1970 | **Ridge Regression** — L2 penalty for multicollinearity | Hoerl & Kennard |
| 1996 | **LASSO** — L1 penalty for sparsity and feature selection | Tibshirani |
| 2005 | **Elastic Net** — convex combination of L1 and L2 penalties | Zou & Hastie |

## Key Properties

- **Sparsity**: The L1 penalty produces exact zeros in $\hat{\beta}$, yielding interpretable sparse models. For sufficiently large $\lambda$, most coefficients vanish.
- **Convex but non-differentiable**: The L1 norm is not differentiable at zero, so standard gradient descent fails. Optimization uses **coordinate descent**, **subgradient methods**, or **ADMM** (Alternating Direction Method of Multipliers).
- **Geometric interpretation**: The L1 constraint set $\|\beta\|_1 \leq t$ forms a diamond (cross-polytope) whose **corners lie on axes**. The least squares contours are more likely to intersect these corners, setting some $\beta_j = 0$.
- **Elastic Net extension**: Combines L1 and L2 penalties:

$$\min_{\beta} \frac{1}{2n} \|y - X\beta\|_2^2 + \lambda_1 \|\beta\|_1 + \lambda_2 \|\beta\|_2^2$$

This addresses LASSO's limitations with correlated features, where it tends to select one and ignore the rest.

## Comparison with Ridge

| Property | LASSO (L1) | Ridge (L2) |
|----------|-----------|------------|
| Penalty | $\lambda \|\beta\|_1$ | $\lambda \|\beta\|_2^2$ |
| Sparsity | Yes — exact zeros | No — shrinks toward zero |
| Feature selection | Automatic | No |
| Differentiability | Non-differentiable at 0 | Differentiable everywhere |
| Closed-form solution | No | Yes: $\hat{\beta} = (X^TX + \lambda I)^{-1} X^T y$ |
| Correlated features | Selects one arbitrarily | Shares weight across group |
| Constraint geometry | Diamond (corners on axes) | Sphere (no corners) |

## Applications

| Domain | Use Case |
|--------|----------|
| Genomics | Gene selection from high-dimensional expression data ($p \gg n$) |
| NLP | Sparse feature selection in text classification |
| Abuse detection | Sparse feature models for buyer abuse signals in BAP; L1 regularization identifies the most predictive features from large variable sets |
| Compressed sensing | Recovering sparse signals from few measurements via L1 minimization |
| Finance | Portfolio selection with sparse asset weights |

## Related Terms

- [Ridge Regression](term_ridge_regression.md) — L2 regularization counterpart
- [Least Squares](term_least_squares.md) — unregularized baseline
- [Linear Regression](term_linear_regression.md) — foundational regression framework
- [Graphical LASSO](term_graphlasso.md) — L1-penalized precision matrix estimation
- [Exponential Family](term_exponential_family.md) — generalized linear model distributions
- [Concentration Inequality](term_concentration_inequality.md) — theoretical guarantees for LASSO consistency

- **[Elastic Net](term_elastic_net.md)**: Combines L1 (LASSO) + L2 (Ridge) penalties
- **[Coordinate Descent](term_coordinate_descent.md)**: Standard solver for LASSO (soft-thresholding per coordinate)
- **[ADMM](term_admm.md)**: Distributed optimization alternative for LASSO/GraphLasso
- **[JL Lemma](term_johnson_lindenstrauss_lemma.md)**: Compressed sensing (LASSO) uses JL-type restricted isometry property (RIP)

## References

- Tibshirani, R. (1996). "Regression Shrinkage and Selection via the Lasso." *Journal of the Royal Statistical Society, Series B*, 58(1), 267–288.
- Zou, H. & Hastie, T. (2005). "Regularization and Variable Selection via the Elastic Net." *Journal of the Royal Statistical Society, Series B*, 67(2), 301–320.
- [LASSO — Wikipedia](https://en.wikipedia.org/wiki/Lasso_(statistics))
