---
tags:
  - resource
  - terminology
  - statistics
  - probability
keywords:
  - CDF transform
  - cumulative distribution function
  - probability integral transform
  - quantile function
  - inverse CDF
  - normalization
topics:
  - statistical modeling
  - probability theory
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# CDF Transform (Probability Integral Transform)

## Definition

The **CDF transform** (also called the **probability integral transform**) states that if $X$ is a continuous random variable with CDF $F_X$, then the transformed variable

$$Y = F_X(X) \sim \text{Uniform}(0, 1)$$

follows a standard uniform distribution. The **inverse CDF** (quantile function) reverses this: if $U \sim \text{Uniform}(0, 1)$, then $F_X^{-1}(U) \sim F_X$.

Composing a forward CDF with a different inverse CDF maps between arbitrary distributions:

$$T_{a,b \to c,d}(x) = F_{c,d}^{-1}\bigl(F_{a,b}(x)\bigr)$$

In **CUBES**, this is used to normalize return rates across product categories. Each category's return rate follows a $\text{Beta}(a_i, b_i)$ distribution with category-specific shape parameters. The CDF transform maps every category to a common reference distribution:

$$T_{a,b}(x) = I_{1.5,\,4}^{-1}\!\bigl(I_{a,b}(x)\bigr)$$

where $I_{a,b}$ is the regularized incomplete beta function (i.e., the Beta CDF). This makes cross-category return rate comparisons distribution-free.

## Key Properties

- **Universality** — applies to any continuous distribution; $F_X(X)$ is always $\text{Uniform}(0,1)$ regardless of the form of $F_X$.
- **Invertibility** — the transform is bijective for strictly increasing CDFs, so no information is lost.
- **Distribution-free** — the resulting uniform variable carries no distributional assumptions, enabling nonparametric comparisons.

## Applications

| Application | Description |
|---|---|
| **CUBES normalization** | Maps category-specific $\text{Beta}(a_i, b_i)$ return rates to a common $\text{Beta}(1.5, 4)$ reference for cross-category defect scoring |
| **Copula modeling** | Separates marginal distributions from dependence structure by transforming margins to uniform |
| **Random variate generation** | Inverse transform sampling: draw $U \sim \text{Uniform}(0,1)$, compute $X = F^{-1}(U)$ to sample from $F$ |
| **Goodness-of-fit testing** | If a model is correct, CDF-transformed residuals should be uniform; departures indicate misfit |

## Related Terms

- [Beta Distribution](term_beta_distribution.md)
- [Beta-Binomial Model](term_beta_binomial_model.md)
- [Defect Index](term_defect_index.md)
- **[Binomial Distribution](term_binomial_distribution.md)**: The likelihood whose Beta conjugate prior is transformed by the CDF
- **[Conjugate Prior](term_conjugate_prior.md)**: CDF transform leverages the Beta-Binomial conjugate relationship
- **[Dirichlet Distribution](term_dirichlet_distribution.md)**: Multivariate generalization; CDF transform extends to Dirichlet via marginals

## References

- **Vault**: CUBES project notes; CUBES experiment documentation
- **External**: [Probability integral transform — Wikipedia](https://en.wikipedia.org/wiki/Probability_integral_transform)
- **External**: [Inverse transform sampling — Wikipedia](https://en.wikipedia.org/wiki/Inverse_transform_sampling)
