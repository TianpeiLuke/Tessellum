---
tags:
  - resource
  - terminology
  - statistics
  - bayesian
keywords:
  - conjugate prior
  - Bayesian conjugacy
  - closed-form posterior
  - analytical tractability
  - prior-likelihood pair
topics:
  - Bayesian inference
  - statistical modeling
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Conjugate Prior

## Definition

A **conjugate prior** is a prior distribution that, when combined with a given likelihood function, yields a posterior distribution belonging to the same parametric family as the prior. The concept was introduced by Howard Raiffa and Robert Schlaifer in their work on Bayesian decision theory.

Formally, if the prior $p(\theta)$ and the posterior $p(\theta|x)$ both belong to the same distribution family $\mathcal{F}$, then $\mathcal{F}$ is called the **conjugate family** for the likelihood $p(x|\theta)$. This property provides a closed-form expression for the posterior, eliminating the need for numerical integration or MCMC sampling.

Conjugate priors exist for all likelihood functions in the exponential family. The Beta-Binomial conjugacy is the foundation of CUBES return rate estimation in buyer abuse prevention.

## Taxonomy

Common conjugate prior-likelihood pairs:

| Likelihood | Conjugate Prior | Parameter | Posterior Predictive |
|---|---|---|---|
| Binomial / Bernoulli | $\text{Beta}(\alpha, \beta)$ | $p$ (probability) | Beta-Binomial |
| Multinomial / Categorical | $\text{Dirichlet}(\boldsymbol{\alpha})$ | $\mathbf{p}$ (probability vector) | Dirichlet-Multinomial |
| Normal (known $\sigma^2$) | $\text{Normal}(\mu_0, \sigma_0^2)$ | $\mu$ (mean) | Normal |
| Poisson | $\text{Gamma}(\alpha, \beta)$ | $\lambda$ (rate) | Negative Binomial |
| Normal (known $\mu$) | $\text{Inverse-Gamma}(\alpha, \beta)$ | $\sigma^2$ (variance) | Student-t |
| Normal (unknown $\mu, \sigma^2$) | Normal-Inverse-Gamma | $\mu, \sigma^2$ | Student-t |
| Exponential | $\text{Gamma}(\alpha, \beta)$ | $\lambda$ (rate) | Lomax |

## Key Properties

- **Analytical tractability**: The posterior has a known closed-form distribution, avoiding expensive numerical integration or sampling methods.
- **Interpretable hyperparameters (pseudo-counts)**: Prior hyperparameters can be interpreted as pseudo-observations. For example, $\text{Beta}(\alpha, \beta)$ encodes $\alpha$ pseudo-successes and $\beta$ pseudo-failures.
- **Sequential updating**: The posterior from one batch of data becomes the prior for the next batch. For Beta-Binomial: observing $s$ successes and $f$ failures updates $\text{Beta}(\alpha, \beta) \to \text{Beta}(\alpha + s, \beta + f)$.
- **Exponential family guarantee**: Every exponential family distribution has a conjugate prior, also typically in the exponential family.
- **Dimensionality pattern**: The conjugate prior typically has one more hyperparameter than the number of parameters in the likelihood.

## Related Terms

- [Beta Distribution](term_beta_distribution.md) — The conjugate prior for Binomial/Bernoulli likelihoods
- [Beta-Binomial Model](term_beta_binomial_model.md) — The most common conjugate pair, used in CUBES
- [Dirichlet Distribution](term_dirichlet_distribution.md) — Multivariate generalization of Beta; conjugate to Multinomial
- [Multinomial Distribution](term_multinomial_distribution.md) — Likelihood for categorical count data
- [Bayesian Reasoning](term_bayesian_reasoning.md) — The broader inference framework that conjugate priors simplify

- **[Gamma Distribution](term_gamma_distribution.md)**: Gamma is conjugate prior for Poisson rate; exponential family member
- **[Poisson Distribution](term_poisson_distribution.md)**: Exponential family member; Gamma is its conjugate prior

## References

- [Wikipedia: Conjugate prior](https://en.wikipedia.org/wiki/Conjugate_prior)
- Raiffa, H. & Schlaifer, R. (1961). *Applied Statistical Decision Theory*. Harvard University Press.
- Fink, D. (1997). *A Compendium of Conjugate Priors*. Technical Report.
- Murphy, K.P. (2007). *Conjugate Bayesian Analysis of the Gaussian Distribution*.
