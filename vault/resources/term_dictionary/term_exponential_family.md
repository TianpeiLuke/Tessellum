---
tags:
  - resource
  - terminology
  - statistics
  - probability
keywords:
  - exponential family
  - sufficient statistics
  - natural parameter
  - log-partition function
  - canonical form
  - GLM
topics:
  - statistical theory
  - probability distributions
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Exponential Family

The **exponential family** is a parametric class of probability distributions whose density (or mass) function can be written in a unified canonical form. It encompasses most commonly used distributions in statistics and machine learning, and provides the theoretical foundation for sufficient statistics, conjugate priors, and generalized linear models.

## Definition

A distribution belongs to the exponential family if its PDF/PMF can be expressed as:

$$f(\mathbf{x} \mid \boldsymbol{\theta}) = h(\mathbf{x}) \exp\!\bigl[\boldsymbol{\eta}(\boldsymbol{\theta}) \cdot \mathbf{T}(\mathbf{x}) - A(\boldsymbol{\theta})\bigr]$$

where:

- $\mathbf{x}$ — observed data
- $\boldsymbol{\theta}$ — parameter vector
- $\boldsymbol{\eta}(\boldsymbol{\theta})$ — **natural (canonical) parameters**, the transformed parameter vector
- $\mathbf{T}(\mathbf{x})$ — **sufficient statistics**, functions of the data that capture all information about $\boldsymbol{\theta}$
- $A(\boldsymbol{\theta})$ — **log-partition function** (log-normalizer), ensures the distribution integrates to 1
- $h(\mathbf{x})$ — **base measure**, a non-negative function independent of $\boldsymbol{\theta}$

When $\boldsymbol{\eta}(\boldsymbol{\theta}) = \boldsymbol{\theta}$, the family is said to be in **canonical form**. The support of the distribution must be independent of $\boldsymbol{\theta}$ for membership in the exponential family.

Members include: Normal, Bernoulli, Binomial (fixed $n$), Poisson, Exponential, Gamma, Beta, Dirichlet, Multinomial (fixed $n$), Categorical, Chi-squared, Wishart, Inverse Gaussian, and von Mises–Fisher.

Notable non-members: Student's $t$, Cauchy, uniform (with varying bounds), mixture distributions, and F-distribution.

## Key Properties

- **Sufficient statistics**: $\mathbf{T}(\mathbf{x})$ captures all information about $\boldsymbol{\theta}$. For $n$ i.i.d. observations, the sufficient statistic is $\sum_{i=1}^{n} \mathbf{T}(x_i)$ — its dimension does not grow with sample size (Pitman–Koopman–Darmois theorem).
- **Natural parameters**: The vector $\boldsymbol{\eta}$ defines a convex natural parameter space. Reparameterizing in terms of $\boldsymbol{\eta}$ simplifies many derivations.
- **Log-partition function $A(\boldsymbol{\eta})$**: Acts as a cumulant generating function for $\mathbf{T}(\mathbf{x})$:
  - $\mathbb{E}[T_j] = \frac{\partial A}{\partial \eta_j}$ (first derivative gives the mean)
  - $\text{Cov}(T_i, T_j) = \frac{\partial^2 A}{\partial \eta_i \, \partial \eta_j}$ (second derivative gives the covariance)
- **Conjugate priors**: Every exponential family member admits a conjugate prior of the form $p(\boldsymbol{\eta} \mid \boldsymbol{\chi}, \nu) \propto g(\boldsymbol{\eta})^{\nu} \exp(\boldsymbol{\eta}^{\top} \boldsymbol{\chi})$, making Bayesian updating analytically tractable.
- **Maximum entropy**: Exponential family distributions are the maximum-entropy distributions subject to constraints on the expected values of $\mathbf{T}(\mathbf{x})$.
- **GLM foundation**: Generalized linear models use exponential family distributions as the response distribution, linking the mean to a linear predictor via a link function.

## Taxonomy

| Distribution | Natural Parameter $\boldsymbol{\eta}$ | Sufficient Statistic $\mathbf{T}(x)$ | Log-Partition $A(\boldsymbol{\eta})$ |
|---|---|---|---|
| **Bernoulli** | $\log \frac{p}{1-p}$ (logit) | $x$ | $\log(1 + e^{\eta})$ |
| **Binomial** ($n$ fixed) | $\log \frac{p}{1-p}$ | $x$ | $n \log(1 + e^{\eta})$ |
| **Poisson** | $\log \lambda$ | $x$ | $e^{\eta}$ |
| **Exponential** | $-\lambda$ | $x$ | $-\log(-\eta)$ |
| **Normal** ($\mu, \sigma^2$) | $\bigl[\frac{\mu}{\sigma^2},\; -\frac{1}{2\sigma^2}\bigr]$ | $[x,\; x^2]$ | $-\frac{\eta_1^2}{4\eta_2} - \frac{1}{2}\log(-2\eta_2)$ |
| **Gamma** ($\alpha, \beta$) | $[\alpha - 1,\; -\beta]$ | $[\log x,\; x]$ | $\log \Gamma(\eta_1+1) - (\eta_1+1)\log(-\eta_2)$ |
| **Beta** ($\alpha, \beta$) | $[\alpha,\; \beta]$ | $[\log x,\; \log(1-x)]$ | $\log \frac{\Gamma(\eta_1)\Gamma(\eta_2)}{\Gamma(\eta_1+\eta_2)}$ |
| **Dirichlet** ($\alpha_1 \ldots \alpha_k$) | $[\alpha_1, \ldots, \alpha_k]$ | $[\log x_1, \ldots, \log x_k]$ | $\sum_i \log\Gamma(\eta_i) - \log\Gamma(\sum_i \eta_i)$ |
| **Multinomial** ($n$ fixed) | $\bigl[\log \frac{p_1}{p_k}, \ldots, \log \frac{p_{k-1}}{p_k}, 0\bigr]$ | $[x_1, \ldots, x_k]$ | $n \log(1 + \sum_{i=1}^{k-1} e^{\eta_i})$ |

## Related Terms

- [Beta Distribution](term_beta_distribution.md) — exponential family member; conjugate prior for Bernoulli/Binomial
- [Binomial Distribution](term_binomial_distribution.md) — exponential family member (fixed $n$)
- [Dirichlet Distribution](term_dirichlet_distribution.md) — multivariate generalization of Beta; conjugate prior for Multinomial
- [Multinomial Distribution](term_multinomial_distribution.md) — exponential family member (fixed $n$); models categorical counts
- [Conjugate Prior](term_conjugate_prior.md) — always exists for exponential family members
- [Logistic Regression](term_logistic_regression.md) — GLM using Bernoulli (exponential family) with logit link
- **[LDA](term_lda.md)**: Uses Dirichlet-Multinomial (both exponential family) as generative model
- **[Linear Regression](term_linear_regression.md)**: Normal distribution (exponential family) underlies OLS
- **[Least Squares](term_least_squares.md)**: MLE under Gaussian (exponential family) = least squares
- **[Clopper-Pearson](term_clopper_pearson.md)**: Uses Beta quantiles (exponential family member)

- **[Normal Distribution](term_normal_distribution.md)**: Normal is the k=2 exponential family member for continuous data
- **[Gamma Distribution](term_gamma_distribution.md)**: Gamma is an exponential family member
- **[Poisson Distribution](term_poisson_distribution.md)**: Exponential family member for count data
- **[Exponential Distribution](term_exponential_distribution.md)**: Exponential family member for waiting times
- **[JL Lemma](term_johnson_lindenstrauss_lemma.md)**: Exponential family MGF structure enables JL-type concentration proofs

## References

- [Exponential family — Wikipedia](https://en.wikipedia.org/wiki/Exponential_family)
- Nielsen, F. & Garcia, V. (2009). *Statistical Exponential Families: A Digest with Flash Cards*. arXiv:0911.4863.
- Barndorff-Nielsen, O. (1978). *Information and Exponential Families in Statistical Theory*. Wiley.
