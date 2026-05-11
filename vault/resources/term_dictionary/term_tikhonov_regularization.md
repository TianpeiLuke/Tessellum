---
tags:
  - resource
  - terminology
  - statistics
  - machine_learning
  - regularization
  - inverse_problems
keywords:
  - Tikhonov regularization
  - L2 penalty
  - ill-posed problems
  - regularization parameter
  - ridge regression
  - inverse problems
  - Andrey Tikhonov
topics:
  - regularization theory
  - inverse problems
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Tikhonov Regularization

## Definition

**Tikhonov regularization** is the general framework for solving ill-posed inverse problems by adding a penalty term to the least-squares objective. The optimization problem is:

$$\min_{x} \|Ax - b\|_2^2 + \lambda \|\Gamma x\|_2^2$$

where:
- $A$ is the forward operator (design matrix),
- $b$ is the observed data,
- $\lambda > 0$ is the **regularization parameter** controlling the tradeoff between fitting the data and keeping the solution smooth/small,
- $\Gamma$ is the **Tikhonov matrix** that encodes prior structure (smoothness, norm constraints).

When $\Gamma = I$ (the identity matrix), this reduces to **Ridge regression** ($L_2$-penalized least squares). The closed-form solution is:

$$\hat{x} = (A^T A + \lambda \Gamma^T \Gamma)^{-1} A^T b$$

Named after **Andrey Tikhonov** (1943), who introduced the method to stabilize solutions of integral equations.

## Key Properties

- **Stabilizes ill-conditioned problems**: adds $\lambda \Gamma^T \Gamma$ to $A^T A$, ensuring invertibility even when $A$ is rank-deficient.
- **Equivalent to Ridge regression** when $\Gamma = I$: the most common special case in machine learning.
- **Bayesian interpretation**: corresponds to a **Gaussian prior** $x \sim \mathcal{N}(0, (\lambda \Gamma^T \Gamma)^{-1})$ on the parameters, making the solution the MAP estimate.
- **L-curve method**: a standard technique for choosing $\lambda$ by plotting $\|Ax - b\|$ vs. $\|\Gamma x\|$ and selecting the corner of the L-shaped curve.
- **Generalized cross-validation (GCV)**: another data-driven method for selecting $\lambda$.
- **Bias-variance tradeoff**: increasing $\lambda$ reduces variance (smaller coefficients) but increases bias (worse data fit).

## Related Terms

- [Ridge Regression](term_ridge_regression.md) — special case when $\Gamma = I$
- [Lasso](term_lasso.md) — $L_1$ alternative that induces sparsity
- [Least Squares](term_least_squares.md) — unregularized case ($\lambda = 0$)
- [Normal Distribution](term_normal_distribution.md) — Gaussian prior interpretation

- **[Elastic Net](term_elastic_net.md)**: Elastic net adds L1 to Tikhonov's L2 penalty
- **[Concentration Inequality](term_concentration_inequality.md)**: Tikhonov estimation error bounds use matrix concentration
- **[Exponential Family](term_exponential_family.md)**: Tikhonov with Gaussian likelihood = Ridge = MAP with Gaussian prior
- **[Linear Regression](term_linear_regression.md)**: Ridge regression is Tikhonov with Gamma=I applied to linear regression
- **[GraphLasso](term_graphlasso.md)**: GraphLasso replaces Tikhonov's L2 with L1 for sparse estimation
- **[ADMM](term_admm.md)**: ADMM solves general Tikhonov problems in distributed settings
- **[Coordinate Descent](term_coordinate_descent.md)**: CD solves Tikhonov variants with non-smooth penalties

## References

- Tikhonov, A. N. (1943). "On the stability of inverse problems."
- Hansen, P. C. (1998). *Rank-Deficient and Discrete Ill-Posed Problems*.
- Wikipedia: [Tikhonov regularization](https://en.wikipedia.org/wiki/Tikhonov_regularization)
