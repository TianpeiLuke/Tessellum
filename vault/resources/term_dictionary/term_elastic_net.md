---
tags:
  - resource
  - terminology
  - statistics
  - machine_learning
  - regularization
keywords:
  - elastic net
  - L1 L2 regularization
  - Zou Hastie 2005
  - LASSO Ridge combination
  - grouped selection
topics:
  - regularization
  - machine learning
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Elastic Net

## Definition

**Elastic Net** is a regularized regression method that linearly combines the L1 (LASSO) and L2 (Ridge) penalties. The optimization objective is:

$$\min_{\beta} \frac{1}{2n} \|y - X\beta\|_2^2 + \lambda_1 \|\beta\|_1 + \lambda_2 \|\beta\|_2^2$$

Equivalently, using a mixing parameter $\alpha \in [0, 1]$:

$$\min_{\beta} \frac{1}{2n} \|y - X\beta\|_2^2 + \lambda \left( \alpha \|\beta\|_1 + \frac{1 - \alpha}{2} \|\beta\|_2^2 \right)$$

- When $\alpha = 1$: reduces to LASSO
- When $\alpha = 0$: reduces to Ridge regression

Introduced by **Zou & Hastie (2005)** to overcome key limitations of LASSO:

1. When $p > n$ (more features than samples), LASSO selects at most $n$ variables. Elastic Net removes this ceiling.
2. When features are highly correlated, LASSO tends to arbitrarily pick one and discard the rest. Elastic Net exhibits **grouped selection** — correlated features are selected or dropped together.

## Key Properties

- **Sparsity** (from L1): drives irrelevant coefficients exactly to zero, performing automatic feature selection
- **Stability** (from L2): shrinks correlated coefficients toward each other, reducing variance
- **Grouped selection**: correlated predictors receive similar coefficients rather than one being zeroed out
- **Mixing parameter** $\alpha$: controls the balance between L1 and L2 penalties; tuned via cross-validation alongside $\lambda$
- **Convexity**: the objective is strictly convex when $\alpha < 1$, guaranteeing a unique solution
- **Solution path**: can be computed efficiently via coordinate descent or LARS-EN algorithm

## BAP Relevance

Elastic Net is used in **Buyer Abuse Prevention (BAP) feature selection** pipelines where:

- Feature spaces are high-dimensional ($p \gg n$)
- Many features are correlated (e.g., multiple concession-related signals)
- Interpretable sparse models are needed for downstream rule-based systems

## Related Terms

- [LASSO](term_lasso.md)
- [Ridge Regression](term_ridge_regression.md)
- [Least Squares](term_least_squares.md)
- [Linear Regression](term_linear_regression.md)

- **[GraphLasso](term_graphlasso.md)**: Elastic net penalty can be applied to precision matrix estimation
- **[Concentration Inequality](term_concentration_inequality.md)**: Elastic net consistency requires restricted eigenvalue conditions
- **[XGBoost](term_xgboost.md)**: XGBoost with L1+L2 regularization is an elastic net analog for trees
- **[Normal Distribution](term_normal_distribution.md)**: Elastic net = MAP with Gaussian (L2) + Laplace (L1) prior
- **[Exponential Family](term_exponential_family.md)**: Elastic net extends to GLMs with exponential family likelihoods
- **[Coordinate Descent](term_coordinate_descent.md)**: glmnet uses coordinate descent to solve elastic net path
- **[ADMM](term_admm.md)**: ADMM solves distributed elastic net
- **[PAC Learning](term_pac_learning.md)**: Elastic net generalization bounds via Rademacher complexity

## References

- Zou, H., & Hastie, T. (2005). *Regularization and variable selection via the elastic net*. Journal of the Royal Statistical Society: Series B, 67(2), 301–320.
- [Wikipedia — Elastic net regularization](https://en.wikipedia.org/wiki/Elastic_net_regularization)
