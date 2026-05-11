---
tags:
  - resource
  - terminology
  - statistics
  - probability
keywords:
  - normal distribution
  - Gaussian distribution
  - bell curve
  - central limit theorem
  - standard normal
  - z-score
  - N(mu sigma2)
topics:
  - probability theory
  - statistical modeling
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Normal Distribution (Gaussian Distribution)

The **normal distribution** (also called the **Gaussian distribution**) is the most important continuous probability distribution in statistics and machine learning. Denoted $X \sim \mathcal{N}(\mu, \sigma^2)$, it arises naturally whenever many small, independent effects combine additively.

## Definition

A continuous random variable $X$ follows a normal distribution with mean $\mu \in \mathbb{R}$ and variance $\sigma^2 > 0$ if its probability density function (PDF) is:

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\!\left(-\frac{(x - \mu)^2}{2\sigma^2}\right), \quad x \in \mathbb{R}$$

- **Mean**: $\mathbb{E}[X] = \mu$
- **Variance**: $\text{Var}(X) = \sigma^2$
- **Moment generating function**: $M_X(t) = \exp\!\left(\mu t + \frac{\sigma^2 t^2}{2}\right)$

The **standard normal distribution** is the special case $Z \sim \mathcal{N}(0, 1)$. Any normal variable can be standardized via the **z-score**: $Z = \frac{X - \mu}{\sigma}$.

## Historical Context

| Year | Contributor | Contribution |
|------|------------|--------------|
| 1733 | Abraham de Moivre | First derived the normal curve as an approximation to the binomial distribution |
| 1809 | Carl Friedrich Gauss | Used the distribution to analyze astronomical measurement errors; derived it from the principle of least squares |
| 1812 | Pierre-Simon Laplace | Proved the **Central Limit Theorem** (CLT), giving the normal distribution its foundational role |
| 1889 | Francis Galton | Observed normal distributions in biological data; introduced **regression to the mean** |

## Key Properties

- **Central Limit Theorem (CLT)**: If $X_1, X_2, \ldots, X_n$ are i.i.d. with mean $\mu$ and variance $\sigma^2$, then $\frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}} \xrightarrow{d} \mathcal{N}(0, 1)$ as $n \to \infty$. This is why the normal distribution appears so frequently in practice.
- **68-95-99.7 Rule**: Approximately 68% of values fall within $\pm 1\sigma$, 95% within $\pm 2\sigma$, and 99.7% within $\pm 3\sigma$ of the mean.
- **Conjugate prior**: Under a normal likelihood with known variance, the normal distribution is its own [conjugate prior](term_conjugate_prior.md) — the posterior is also normal (**normal-normal conjugacy**).
- **Maximum entropy**: Among all distributions with a specified mean and variance, the normal distribution has the **maximum entropy**, making it the least informative (most conservative) choice.
- **Exponential family member**: The normal PDF can be written in canonical [exponential family](term_exponential_family.md) form with sufficient statistics $(x, x^2)$ and natural parameters $(\mu/\sigma^2,\; -1/(2\sigma^2))$.
- **Stability**: The sum of independent normal random variables is itself normal: if $X \sim \mathcal{N}(\mu_1, \sigma_1^2)$ and $Y \sim \mathcal{N}(\mu_2, \sigma_2^2)$, then $X + Y \sim \mathcal{N}(\mu_1 + \mu_2,\; \sigma_1^2 + \sigma_2^2)$.
- **Closure under linear transforms**: $aX + b \sim \mathcal{N}(a\mu + b,\; a^2\sigma^2)$.

## Notable Applications

| Domain | Application | Notes |
|--------|------------|-------|
| Measurement science | Modeling measurement error | Gauss's original use case; errors as sum of many small perturbations |
| Finance | Modeling asset returns | Foundational assumption in Black-Scholes; however, real returns exhibit [fat tails](term_fat_tails.md) and skewness |
| Machine learning | Gaussian noise in [linear regression](term_linear_regression.md) | [Least squares](term_least_squares.md) estimation is MLE under the assumption $y = \mathbf{w}^\top \mathbf{x} + \epsilon$, $\epsilon \sim \mathcal{N}(0, \sigma^2)$ |
| Bayesian inference | Normal-normal [conjugate prior](term_conjugate_prior.md) | Prior $\mu \sim \mathcal{N}(\mu_0, \sigma_0^2)$ with normal likelihood yields a normal posterior with closed-form updates |
| Signal processing | Additive white Gaussian noise (AWGN) | Standard channel model in communications theory |

## Related Terms

- [Beta Distribution](term_beta_distribution.md) — another common distribution; conjugate prior for Bernoulli/binomial, not for normal
- [Exponential Family](term_exponential_family.md) — the normal distribution is a canonical member
- [Linear Regression](term_linear_regression.md) — assumes normally distributed errors (Gauss-Markov framework)
- [Least Squares](term_least_squares.md) — equivalent to MLE under Gaussian error assumptions
- [Conjugate Prior](term_conjugate_prior.md) — the normal is self-conjugate for the mean parameter
- [Fat Tails](term_fat_tails.md) — real-world data often deviates from normality; heavy-tailed distributions (Student-$t$, Cauchy, power laws) better capture extreme events

- **[Word Embedding](term_word_embedding.md)**: Embedding distributions often modeled as Gaussian
- **[Ridge Regression](term_ridge_regression.md)**: Ridge = MAP estimation with Gaussian (normal) prior on coefficients
- **[GraphLasso](term_graphlasso.md)**: Estimates sparse Gaussian graphical models
- **[Chi-Squared Distribution](term_chi_squared_distribution.md)**: Sum of squared standard normals
- **[Sub-Gaussian](term_sub_gaussian.md)**: Normal distribution is the canonical sub-Gaussian
- **[JL Lemma](term_johnson_lindenstrauss_lemma.md)**: Gaussian random projection matrix; projected norm is $\chi^2$

## References

- [Normal distribution — Wikipedia](https://en.wikipedia.org/wiki/Normal_distribution)
- Casella, G. & Berger, R. L. (2002). *Statistical Inference* (2nd ed.). Chapters 3–5.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. Section 2.6.
