---
tags:
  - resource
  - terminology
  - statistics
  - graphical_models
keywords:
  - precision matrix
  - inverse covariance
  - conditional independence
  - partial correlation
  - Gaussian graphical model
  - concentration matrix
topics:
  - multivariate statistics
  - graphical models
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Precision Matrix (Inverse Covariance Matrix)

## Definition

The **precision matrix** (also called the **concentration matrix**) is the inverse of the covariance matrix:

$$\Theta = \Sigma^{-1}$$

where $\Sigma$ is the covariance matrix of a random vector $\mathbf{X} = (X_1, \ldots, X_p)$.

The key property that makes the precision matrix central to graphical models: for **Gaussian data**,

$$\Theta_{ij} = 0 \iff X_i \perp\!\!\!\perp X_j \mid \mathbf{X}_{\setminus\{i,j\}}$$

That is, a zero entry means $X_i$ and $X_j$ are **conditionally independent** given all other variables. This makes the sparsity pattern of $\Theta$ the **adjacency matrix** of the Gaussian graphical model.

**Partial correlations** are directly recovered from the precision matrix:

$$\rho_{ij|\text{rest}} = -\frac{\Theta_{ij}}{\sqrt{\Theta_{ii} \Theta_{jj}}}$$

## Key Properties

- **Zeros encode conditional independence**: the fundamental link between precision matrices and graphical model structure.
- **Sparse precision = sparse graph**: a precision matrix with many zeros corresponds to a graph with few edges, revealing the core dependency structure.
- **Estimated by GraphLasso**: the $L_1$-penalized maximum likelihood estimator encourages sparsity in $\Theta$, performing simultaneous estimation and model selection.
- **Partial correlations from off-diagonal entries**: unlike marginal correlations, partial correlations isolate direct relationships by controlling for all other variables.
- **Positive definiteness**: a valid precision matrix must be symmetric positive definite, which GraphLasso enforces by construction.

## Estimation Methods

| Method | Approach | Sparsity |
|--------|----------|----------|
| Sample inverse $S^{-1}$ | Direct inversion | None (requires $n > p$) |
| **GraphLasso** | $L_1$-penalized MLE | Yes |
| CLIME | Constrained $L_1$ minimization | Yes |
| Neighborhood selection | Node-wise Lasso regressions | Yes |

## Related Terms

- [GraphLasso](term_graphlasso.md) — $L_1$-penalized estimator for sparse precision matrices
- [Gaussian Graphical Model](term_gaussian_graphical_model.md) — the graphical model whose structure is encoded by $\Theta$
- [Normal Distribution](term_normal_distribution.md) — the distributional assumption underlying the conditional independence interpretation
- [Concentration Inequality](term_concentration_inequality.md) — provides estimation guarantees for sample precision matrices

- **[LASSO](term_lasso.md)**: GraphLasso applies LASSO penalty to precision matrix entries
- **[Exponential Family](term_exponential_family.md)**: Gaussian (exponential family) precision matrix encodes conditional structure
- **[Markov Random Field](term_markov_random_field.md)**: Precision matrix IS the MRF parameter matrix for Gaussians
- **[Belief Propagation](term_belief_propagation.md)**: Gaussian BP computes marginals using precision matrix
- **[Factor Graph](term_factor_graph.md)**: Precision matrix entries correspond to pairwise factors
- **[ERGM](term_ergm.md)**: Network precision matrix relates to ERGM sufficient statistics
- **[Variational Inference](term_variational_inference.md)**: Variational Gaussian approximation estimates precision matrix
- **[JL Lemma](term_johnson_lindenstrauss_lemma.md)**: Precision matrix estimation in projected space via JL + GraphLasso

## References

- Lauritzen, S. L. (1996). *Graphical Models*. Oxford University Press.
- Wikipedia: [Precision matrix](https://en.wikipedia.org/wiki/Precision_(statistics))
