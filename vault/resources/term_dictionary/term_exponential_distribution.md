---
tags:
  - resource
  - terminology
  - statistics
  - probability
keywords:
  - exponential distribution
  - memoryless
  - rate parameter
  - waiting time
  - Poisson process
  - hazard rate
  - survival analysis
topics:
  - probability theory
  - survival analysis
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Exponential Distribution

## Definition

The **Exponential distribution** is a continuous probability distribution modeling the time between events in a Poisson process. Its PDF is:

$$f(x; \lambda) = \lambda e^{-\lambda x}, \quad x \geq 0$$

where $\lambda > 0$ is the **rate parameter**. Key moments:

- Mean: $\mathbb{E}[X] = 1/\lambda$
- Variance: $\text{Var}(X) = 1/\lambda^2$
- CDF: $F(x) = 1 - e^{-\lambda x}$

The Exponential distribution is a **special case of the Gamma distribution**: $\text{Exponential}(\lambda) = \text{Gamma}(1, \lambda)$.

It is the **only continuous memoryless distribution**.

## Key Properties

- **Memoryless property**: $P(X > s + t \mid X > s) = P(X > t)$ — the remaining waiting time is independent of how long you have already waited
- **Exponential family member**: can be written in canonical exponential family form
- **Poisson process link**: if events arrive as a Poisson process with rate $\lambda$, inter-arrival times are $\text{Exponential}(\lambda)$
- **Constant hazard rate**: $h(x) = \lambda$ for all $x$ — the instantaneous failure rate does not change over time
- **Minimum property**: the minimum of independent exponentials $X_i \sim \text{Exp}(\lambda_i)$ is $\text{Exp}(\sum_i \lambda_i)$

## Applications

| Domain | Use Case | Details |
|---|---|---|
| Poisson processes | Inter-arrival times | Time between events with constant rate |
| Survival analysis | Time-to-event modeling | Baseline model with constant hazard |
| Queuing theory | Service/arrival times | M/M/1 and related queue models |
| Reliability engineering | Component lifetimes | Constant failure rate assumption |
| **Abuse prevention** | **Time between abuse events** | **Model inter-event gaps to detect acceleration in abusive behavior** |

## Related Terms

- [Gamma Distribution](term_gamma_distribution.md) — Exponential is Gamma($1, \lambda$); generalizes to shape $\alpha > 0$
- [Poisson Distribution](term_poisson_distribution.md) — counts events whose inter-arrival times are Exponential
- [Exponential Family](term_exponential_family.md) — Exponential distribution is a member
- [Normal Distribution](term_normal_distribution.md) — contrast: Normal is not memoryless

- **[HMM](term_hmm.md)**: Continuous-time HMM uses exponential sojourn times between state transitions
- **[Chi-Squared Distribution](term_chi_squared_distribution.md)**: Both are special cases of Gamma distribution
- **[Confidence Interval](term_confidence_interval.md)**: Exponential CI uses chi-squared relationship
- **[Sub-Gaussian](term_sub_gaussian.md)**: Exponential distribution is sub-exponential (heavier than sub-Gaussian)
- **[Binomial Distribution](term_binomial_distribution.md)**: Poisson (limit of Binomial) has Exponential inter-arrivals
- **[Conjugate Prior](term_conjugate_prior.md)**: Gamma is conjugate prior for Exponential rate parameter
- **[Concentration Inequality](term_concentration_inequality.md)**: Exponential RVs satisfy Bernstein-type concentration bounds
- **[SIR Model](term_sir_model.md)**: SIR infection/recovery times are exponentially distributed
- **[SIS Model](term_sis_model.md)**: SIS inter-event times follow exponential distribution
- **[Percolation Theory](term_percolation_theory_networks.md)**: Bond percolation with exponential weights models network reliability
- **[Alignment Scaling Law](term_alignment_scaling_law.md)**: Contrast — scaling laws follow power law decay, NOT exponential decay; but exponential concentration bounds analyze scaling law confidence

## References

- [Wikipedia — Exponential Distribution](https://en.wikipedia.org/wiki/Exponential_distribution)
