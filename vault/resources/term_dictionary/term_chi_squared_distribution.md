---
tags:
  - resource
  - terminology
  - statistics
  - probability
keywords:
  - chi-squared
  - chi2
  - degrees of freedom
  - goodness of fit
  - hypothesis testing
  - Pearson
topics:
  - probability theory
  - hypothesis testing
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Chi-Squared Distribution

## Definition

The **Chi-Squared distribution** with $k$ degrees of freedom is the distribution of the sum of $k$ independent squared standard normal random variables:

$$X = \sum_{i=1}^{k} Z_i^2, \quad Z_i \sim \mathcal{N}(0, 1)$$

Written as $X \sim \chi^2(k)$ or $X \sim \chi^2_k$.

The probability density function for $x > 0$ is:

$$f(x; k) = \frac{1}{2^{k/2} \, \Gamma(k/2)} \, x^{k/2 - 1} \, e^{-x/2}$$

The Chi-Squared distribution is a **special case of the Gamma distribution**:

$$\chi^2(k) = \text{Gamma}\!\left(\frac{k}{2}, \frac{1}{2}\right)$$

where Gamma uses the rate parameterization $\text{Gamma}(\alpha, \beta)$ with shape $\alpha = k/2$ and rate $\beta = 1/2$.

## Key Properties

- **Mean**: $\mathbb{E}[X] = k$
- **Variance**: $\text{Var}(X) = 2k$
- **Additivity**: if $X_1 \sim \chi^2(k_1)$ and $X_2 \sim \chi^2(k_2)$ are independent, then $X_1 + X_2 \sim \chi^2(k_1 + k_2)$
- **Normal approximation**: for large $k$, $\chi^2(k) \approx \mathcal{N}(k, 2k)$ by the Central Limit Theorem
- **Moment generating function**: $M_X(t) = (1 - 2t)^{-k/2}$ for $t < 1/2$
- **Mode**: $\max(k - 2, 0)$

## Applications

| Application | Description |
|---|---|
| **Goodness-of-fit test** | Pearson's $\chi^2$ test compares observed vs. expected frequencies: $\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$ |
| **Independence test** | Tests whether two categorical variables are independent in a contingency table |
| **Variance estimation** | Sample variance of normal data: $(n-1)s^2 / \sigma^2 \sim \chi^2(n-1)$ |
| **Likelihood ratio test** | Test statistic $-2 \ln(\Lambda)$ is asymptotically $\chi^2$ under $H_0$ |

## Related Terms

- [Normal Distribution](term_normal_distribution.md)
- [Gamma Distribution](term_gamma_distribution.md)
- [Exponential Family](term_exponential_family.md)
- [Confidence Interval](term_confidence_interval.md)

- **[Binomial Distribution](term_binomial_distribution.md)**: Chi-squared test for goodness-of-fit to binomial model
- **[Poisson Distribution](term_poisson_distribution.md)**: Chi-squared test for Poisson fit; Poisson deviance is chi-squared
- **[Conjugate Prior](term_conjugate_prior.md)**: Inverse-chi-squared is conjugate prior for normal variance
- **[Linear Regression](term_linear_regression.md)**: F-test and t-test in regression use chi-squared distribution
- **[LASSO](term_lasso.md)**: LASSO degrees of freedom estimated via chi-squared approximation
- **[Concentration Inequality](term_concentration_inequality.md)**: Chi-squared tail bounds are sub-exponential concentration inequalities
- **[F1 Score](term_f1_score.md)**: Chi-squared test for comparing classifier performance
- **[JL Lemma](term_johnson_lindenstrauss_lemma.md)**: Projected squared norm follows $\chi^2_k$ — key to JL proof

## References

- [Wikipedia — Chi-squared distribution](https://en.wikipedia.org/wiki/Chi-squared_distribution)
