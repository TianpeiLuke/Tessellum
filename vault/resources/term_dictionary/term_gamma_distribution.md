---
tags:
  - resource
  - terminology
  - statistics
  - probability
  - bayesian
keywords:
  - gamma distribution
  - Gamma(alpha beta)
  - shape rate
  - conjugate prior
  - Poisson
  - exponential
  - waiting time
  - chi-squared
topics:
  - probability theory
  - Bayesian statistics
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Gamma Distribution

The **Gamma distribution** is a two-parameter continuous probability distribution defined on $(0, \infty)$. It models waiting times, aggregate event counts, and serves as a conjugate prior for the Poisson rate parameter in Bayesian inference.

## Definition

A random variable $X \sim \text{Gamma}(\alpha, \beta)$ has probability density function:

$$f(x;\, \alpha, \beta) = \frac{\beta^\alpha}{\Gamma(\alpha)}\, x^{\alpha - 1}\, e^{-\beta x}, \quad x > 0$$

where:

- $\alpha > 0$ — **shape** parameter (controls skewness)
- $\beta > 0$ — **rate** parameter (inverse scale; some texts use scale $\theta = 1/\beta$)
- $\Gamma(\alpha) = \int_0^\infty t^{\alpha-1} e^{-t}\, dt$ — the Gamma function

**Moments:**

| Quantity | Value |
|----------|-------|
| Mean | $\mathbb{E}[X] = \alpha / \beta$ |
| Variance | $\text{Var}(X) = \alpha / \beta^2$ |
| Mode | $(\alpha - 1) / \beta$ for $\alpha \geq 1$ |
| MGF | $M_X(t) = \left(\frac{\beta}{\beta - t}\right)^\alpha$ for $t < \beta$ |

## Key Properties

- **Conjugate prior for Poisson rate**: If the prior on rate $\lambda$ is $\text{Gamma}(\alpha, \beta)$ and we observe $n$ Poisson counts summing to $s$, the posterior is $\text{Gamma}(\alpha + s,\; \beta + n)$. This makes the Gamma distribution central to Bayesian rate estimation in abuse-detection models.
- **Exponential family member**: The Gamma PDF can be written in canonical exponential-family form with sufficient statistics $(x, \log x)$.
- **Additivity**: If $X_i \sim \text{Gamma}(\alpha_i, \beta)$ are independent with common rate $\beta$, then $\sum_i X_i \sim \text{Gamma}\!\left(\sum_i \alpha_i,\; \beta\right)$.

**Special cases:**

| Distribution | Gamma parameters |
|---|---|
| Exponential($\beta$) | $\alpha = 1$ |
| Chi-squared($k$) | $\alpha = k/2,\; \beta = 1/2$ |
| Erlang($k, \beta$) | $\alpha = k \in \mathbb{Z}^+$ |

- **Sum of exponentials**: The sum of $k$ i.i.d. $\text{Exp}(\beta)$ random variables follows $\text{Gamma}(k, \beta)$, making it a natural model for the waiting time until the $k$-th event in a Poisson process.

## Related Terms

- [Beta Distribution](term_beta_distribution.md) — conjugate prior for binomial; related via the Beta function $B(\alpha,\beta) = \Gamma(\alpha)\Gamma(\beta)/\Gamma(\alpha+\beta)$
- [Exponential Family](term_exponential_family.md) — the Gamma distribution is a member
- [Conjugate Prior](term_conjugate_prior.md) — Gamma is conjugate prior for the Poisson rate parameter
- [Normal Distribution](term_normal_distribution.md) — by CLT, $\text{Gamma}(\alpha, \beta)$ approaches Normal as $\alpha \to \infty$
- [Pareto Distribution](term_pareto_distribution.md) — heavy-tailed alternative; Gamma mixtures of exponentials yield Pareto-like tails

- **[Chi-Squared Distribution](term_chi_squared_distribution.md)**: Special case: $\text{Gamma}(k/2, 1/2)$
- **[Poisson Distribution](term_poisson_distribution.md)**: Gamma is conjugate prior for Poisson rate
- **[Exponential Distribution](term_exponential_distribution.md)**: Special case: $\text{Gamma}(1, \lambda)$

## References

- [Gamma distribution — Wikipedia](https://en.wikipedia.org/wiki/Gamma_distribution)
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*, §2.3.6 (Conjugate priors for the Gaussian)
