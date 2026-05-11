---
tags:
  - resource
  - terminology
  - statistics
  - probability
keywords:
  - Poisson distribution
  - count data
  - rate parameter
  - rare events
  - lambda
  - Poisson process
topics:
  - probability theory
  - count data modeling
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Poisson Distribution

## Definition

The **Poisson distribution** models the number of events occurring in a fixed interval of time or space, given a constant average rate $\lambda > 0$. The probability mass function is:

$$P(X = k) = \frac{\lambda^k \, e^{-\lambda}}{k!}, \quad k = 0, 1, 2, \ldots$$

Written as $X \sim \text{Poisson}(\lambda)$.

The Poisson distribution is a member of the **exponential family** with natural parameter $\eta = \ln \lambda$. Its **conjugate prior** is the Gamma distribution:

$$\lambda \sim \text{Gamma}(\alpha, \beta) \implies \lambda \mid x_{1:n} \sim \text{Gamma}\!\left(\alpha + \sum x_i, \, \beta + n\right)$$

## Key Properties

- **Mean**: $\mathbb{E}[X] = \lambda$
- **Variance**: $\text{Var}(X) = \lambda$ (equidispersion: mean equals variance)
- **Binomial limit**: for $n \to \infty$, $p \to 0$, $np \to \lambda$: $\text{Binomial}(n, p) \to \text{Poisson}(\lambda)$
- **Normal approximation**: for large $\lambda$, $\text{Poisson}(\lambda) \approx \mathcal{N}(\lambda, \lambda)$
- **Additivity**: if $X_1 \sim \text{Poisson}(\lambda_1)$ and $X_2 \sim \text{Poisson}(\lambda_2)$ are independent, then $X_1 + X_2 \sim \text{Poisson}(\lambda_1 + \lambda_2)$
- **Poisson process**: inter-arrival times are exponentially distributed with rate $\lambda$ (memoryless property)
- **Moment generating function**: $M_X(t) = \exp\!\left(\lambda(e^t - 1)\right)$

## Applications

| Application | Description |
|---|---|
| **Event counting** | Number of arrivals, calls, or transactions in a time window |
| **Queue theory** | Arrival process in M/M/1 and M/M/c queuing models |
| **Insurance claims** | Modeling claim frequency per policy period |
| **Abuse detection** | Modeling abuse claim frequency per customer — unusually high counts signal potential abuse |

## BAP Relevance

In Buyer Abuse Prevention, the Poisson distribution is relevant for **claim frequency modeling** — the number of concession claims a buyer files within a time window. Overdispersion (variance > mean) in real data often motivates extensions such as Negative Binomial or zero-inflated models.

## Related Terms

- [Gamma Distribution](term_gamma_distribution.md)
- [Binomial Distribution](term_binomial_distribution.md)
- [Exponential Family](term_exponential_family.md)
- [Conjugate Prior](term_conjugate_prior.md)
- [Normal Distribution](term_normal_distribution.md) (Poisson → Normal for large $\lambda$)

- **[Vector Space Model](term_vector_space_model.md)**: TF-IDF term frequencies approximately Poisson
- **[Exponential Distribution](term_exponential_distribution.md)**: Inter-arrival times of Poisson process
- **[HMM](term_hmm.md)**: Poisson HMM models count-valued emissions (event frequencies)
- **[LDA](term_lda.md)**: Poisson factorization is an alternative to LDA for count data
- **[Concentration Inequality](term_concentration_inequality.md)**: Poisson tail bounds via Chernoff are tighter than generic bounds
- **[Confidence Interval](term_confidence_interval.md)**: Poisson CI uses chi-squared relationship
- **[Return Rate](term_return_rate.md)**: Poisson models claim frequency (count of returns per period)
- **[XGBoost](term_xgboost.md)**: XGBoost with Poisson loss for count regression

## References

- [Wikipedia — Poisson distribution](https://en.wikipedia.org/wiki/Poisson_distribution)
