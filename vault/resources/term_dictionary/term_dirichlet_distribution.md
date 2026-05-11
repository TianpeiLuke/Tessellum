---
tags:
  - resource
  - terminology
  - statistics
  - probability
  - bayesian
keywords:
  - Dirichlet distribution
  - Dir(alpha)
  - conjugate prior
  - multinomial
  - probability simplex
  - concentration parameter
  - LDA
topics:
  - probability theory
  - Bayesian statistics
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Dirichlet Distribution

## Definition

The **Dirichlet distribution**, denoted $\text{Dir}(\boldsymbol{\alpha})$, is a family of continuous multivariate probability distributions parameterized by a vector $\boldsymbol{\alpha} = (\alpha_1, \alpha_2, \ldots, \alpha_K)$ of positive reals. It is the **multivariate generalization of the Beta distribution**, hence its alternative name *multivariate beta distribution*.

A Dirichlet-distributed random vector $\mathbf{x} = (x_1, \ldots, x_K)$ lives on the **(K−1)-dimensional probability simplex**:

$$\Delta^{K-1} = \left\{ \mathbf{x} \in \mathbb{R}^K \;\middle|\; x_i \geq 0,\; \sum_{i=1}^{K} x_i = 1 \right\}$$

The probability density function is:

$$f(x_1, \ldots, x_K;\, \alpha_1, \ldots, \alpha_K) = \frac{1}{B(\boldsymbol{\alpha})} \prod_{i=1}^{K} x_i^{\alpha_i - 1}$$

where the normalizing constant $B(\boldsymbol{\alpha})$ is the **multivariate Beta function**:

$$B(\boldsymbol{\alpha}) = \frac{\prod_{i=1}^{K} \Gamma(\alpha_i)}{\Gamma\!\left(\sum_{i=1}^{K} \alpha_i\right)}$$

The Dirichlet distribution is the **conjugate prior** for the [Multinomial distribution](term_multinomial_distribution.md) (and the Categorical distribution). Given a Multinomial likelihood with observed counts $(n_1, \ldots, n_K)$ and a $\text{Dir}(\boldsymbol{\alpha})$ prior, the posterior is $\text{Dir}(\alpha_1 + n_1, \ldots, \alpha_K + n_K)$.

When $K = 2$, the Dirichlet reduces to the [Beta distribution](term_beta_distribution.md).

## Historical Context

The distribution is named after **Peter Gustav Lejeune Dirichlet** (1805–1859), a German mathematician born in Düren. Dirichlet made foundational contributions to number theory, analysis, and mechanics — most notably proving that any arithmetic progression with coprime first term and common difference contains infinitely many primes (Dirichlet's theorem on primes). He also formalized the modern definition of a function and advanced the theory of Fourier series.

The **Dirichlet process** (Ferguson, 1973) is the infinite-dimensional generalization of the Dirichlet distribution. While the Dirichlet distribution is a distribution over finite-dimensional probability vectors, the Dirichlet process is a distribution over probability *measures* on arbitrary spaces, enabling nonparametric Bayesian models with a potentially infinite number of mixture components.

## Key Properties

Let $\alpha_0 = \sum_{i=1}^{K} \alpha_i$ denote the **concentration parameter** (also called *precision*).

- **Mean**: $E[x_i] = \dfrac{\alpha_i}{\alpha_0}$
- **Variance**: $\text{Var}(x_i) = \dfrac{\alpha_i(\alpha_0 - \alpha_i)}{\alpha_0^2(\alpha_0 + 1)}$
- **Covariance** ($i \neq j$): $\text{Cov}(x_i, x_j) = \dfrac{-\alpha_i \alpha_j}{\alpha_0^2(\alpha_0 + 1)}$
- **Mode** (for $\alpha_i > 1$): $\text{mode}(x_i) = \dfrac{\alpha_i - 1}{\alpha_0 - K}$

**Concentration parameter interpretation**:

- $\alpha_0$ controls the **spread** of the distribution around the mean. Larger $\alpha_0$ concentrates mass near the mean; smaller $\alpha_0$ pushes mass toward the simplex corners (sparse vectors).
- When all $\alpha_i = 1$ (i.e., $\boldsymbol{\alpha} = \mathbf{1}$), the distribution is **uniform** over the simplex.
- When all $\alpha_i < 1$, the distribution is **sparse** — favoring vectors where most components are near zero.
- The **symmetric Dirichlet** ($\alpha_i = \alpha$ for all $i$) is commonly used when no component is preferred a priori.

## Notable Applications

| Application | Role of Dirichlet |
|---|---|
| **LDA topic modeling** | Prior over per-document topic proportions $\theta_d \sim \text{Dir}(\boldsymbol{\alpha})$ and per-topic word distributions $\phi_k \sim \text{Dir}(\boldsymbol{\beta})$ |
| **Bayesian NLP** | Prior for language model smoothing and categorical parameter estimation |
| **HMM emission priors** | Conjugate prior for discrete emission probabilities in Hidden Markov Models |
| **Bayesian mixture models** | Prior over mixture weights $\boldsymbol{\pi} \sim \text{Dir}(\boldsymbol{\alpha})$ |
| **Population genetics** | Modeling allele frequency distributions across populations (Balding–Nichols model) |
| **Information retrieval** | Smoothing document-term distributions in probabilistic retrieval models |

## Related Terms

- [Beta Distribution](term_beta_distribution.md) — the $K=2$ special case of the Dirichlet
- [Multinomial Distribution](term_multinomial_distribution.md) — the Dirichlet is its [conjugate prior](term_conjugate_prior.md)
- [Conjugate Prior](term_conjugate_prior.md) — the Dirichlet–Multinomial pair is a canonical example
- **[Bayesian Reasoning](term_bayesian_reasoning.md)**: The broader inference framework that Dirichlet priors serve
- **[CDF Transform](term_cdf_transform.md)**: Dirichlet marginals are Beta; CDF transform applies to each

- **[Bag of Words](term_bag_of_words.md)**: Dirichlet prior on BoW topic proportions in LDA
- **[LDA](term_lda.md)**: Latent Dirichlet Allocation — the most famous application of the Dirichlet distribution
- **[Probabilistic Graphical Model](term_probabilistic_graphical_model.md)**: Dirichlet is the prior in LDA (a directed PGM)

## References

- [Wikipedia — Dirichlet distribution](https://en.wikipedia.org/wiki/Dirichlet_distribution)
- [Wikipedia — Peter Gustav Lejeune Dirichlet](https://en.wikipedia.org/wiki/Peter_Gustav_Lejeune_Dirichlet)
- Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). Latent Dirichlet Allocation. *JMLR*, 3, 993–1022.
- Ferguson, T. S. (1973). A Bayesian Analysis of Some Nonparametric Problems. *Annals of Statistics*, 1(2), 209–230.
