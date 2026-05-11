---
tags:
  - resource
  - terminology
  - statistics
  - probability
  - statistical_learning_theory
keywords:
  - concentration inequality
  - Hoeffding
  - Bernstein
  - McDiarmid
  - sub-Gaussian
  - sub-exponential
  - tail bound
  - high-dimensional statistics
  - PAC learning
  - generalization bound
topics:
  - statistical learning theory
  - high-dimensional statistics
  - probability theory
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Concentration Inequalities

## Definition

Concentration inequalities are bounds on how much a random variable deviates from its expected value. They are the fundamental tool for proving that sample statistics converge to population parameters at quantifiable rates.

The general form is:

$$P(|X - \mathbb{E}[X]| \geq t) \leq f(t, n)$$

where $f$ is a decreasing function of the deviation threshold $t$ and the sample size $n$. The sharper $f$ decays, the more useful the bound. Polynomial decay (Chebyshev) is weak; exponential decay (Hoeffding, Bernstein) is the workhorse of modern statistics and learning theory.

## Taxonomy

| Inequality | Bound | Assumptions | Tail Decay |
|---|---|---|---|
| **Markov** | $P(X \geq t) \leq \frac{\mathbb{E}[X]}{t}$ | $X \geq 0$ | $O(1/t)$ |
| **Chebyshev** | $P(\|X - \mu\| \geq t) \leq \frac{\sigma^2}{t^2}$ | Finite variance | $O(1/t^2)$ |
| **Hoeffding** | $P(\|\bar{X}_n - \mu\| \geq t) \leq 2\exp\!\left(-\frac{2nt^2}{(b-a)^2}\right)$ | $X_i \in [a,b]$, independent | Exponential |
| **Bernstein** | $P(\|\bar{X}_n - \mu\| \geq t) \leq 2\exp\!\left(-\frac{nt^2/2}{\sigma^2 + Mt/3}\right)$ | $\|X_i - \mu\| \leq M$, uses variance $\sigma^2$ | Exponential (tighter) |
| **McDiarmid** | $P(\|f(X) - \mathbb{E}[f(X)]\| \geq t) \leq 2\exp\!\left(-\frac{2t^2}{\sum c_i^2}\right)$ | Bounded differences $c_i$ | Exponential |
| **Chernoff** | $P(X \geq t) \leq \inf_{s>0} e^{-st}\,\mathbb{E}[e^{sX}]$ | MGF exists | Exponential (generic) |
| **Sub-Gaussian** | $P(\|X\| \geq t) \leq 2\exp(-t^2 / 2\sigma^2)$ | Sub-Gaussian parameter $\sigma$ | Gaussian-type |
| **Sub-Exponential** | $P(\|X\| \geq t) \leq 2\exp(-t^2/2\sigma^2)$ for small $t$; $\leq 2\exp(-t/2b)$ for large $t$ | Parameters $(\sigma, b)$ | Mixed regime |

## Key Properties

- **Exponential tails dominate**: Hoeffding and Bernstein bounds decay as $\exp(-Cnt^2)$, making them exponentially sharper than Chebyshev's $O(1/t^2)$. This is why they underpin virtually all finite-sample guarantees in ML.
- **Bernstein improves on Hoeffding** when variance is small relative to the range. The bound interpolates between a Gaussian regime ($t$ small, variance dominates) and a Poisson regime ($t$ large, range dominates).
- **Sub-Gaussian class** captures "light-tailed" behavior: a random variable $X$ is sub-Gaussian with parameter $\sigma$ if $\mathbb{E}[\exp(sX)] \leq \exp(s^2\sigma^2/2)$ for all $s$. Bounded, Gaussian, and Rademacher variables are all sub-Gaussian.
- **Dimension-free bounds**: McDiarmid and tensorization arguments yield bounds that depend on the number of variables but not on ambient dimension, enabling high-dimensional statistics where $p \gg n$.

## Applications

| Domain | How Concentration Inequalities Are Used |
|---|---|
| **PAC Learning** | Generalization bounds via uniform convergence: $P(\sup_{h \in \mathcal{H}} \|R(h) - \hat{R}(h)\| \geq \epsilon) \leq \delta$ requires Hoeffding + union bound over hypothesis class |
| **LASSO Theory** | Proving restricted eigenvalue conditions and $\ell_1$ consistency requires sub-Gaussian tail bounds on $\frac{1}{n}X^\top X$ entries |
| **Bandit Algorithms** | UCB constructs confidence bounds $\hat{\mu}_a + \sqrt{\frac{2\ln t}{n_a}}$ directly from Hoeffding's inequality |
| **A/B Testing** | Sample size formulas $n = O(\sigma^2 / \epsilon^2 \cdot \ln(1/\delta))$ derive from inverting Hoeffding/Bernstein bounds |
| **GraphLasso** | Convergence guarantees for sparse covariance estimation rely on concentration of sample covariance entries around population values |
| **Conformal Prediction** | Coverage guarantees $P(Y \in C(X)) \geq 1 - \alpha$ use exchangeability + concentration to bound miscoverage |

## Related Terms

- [Normal Distribution](term_normal_distribution.md) — sub-Gaussian with parameter $\sigma$; the prototypical light-tailed distribution
- [LASSO](term_lasso.md) — $\ell_1$ consistency proofs rely on sub-Gaussian concentration of design matrix entries
- [GraphLasso](term_graphlasso.md) — sparse precision matrix estimation with concentration-based convergence rates
- [Confidence Interval](term_confidence_interval.md) — CI width is the applied face of concentration inequalities
- [Multi-Armed Bandit](term_mab.md) — UCB confidence bounds are direct applications of Hoeffding's inequality
- [Conformal Prediction](term_conformal_prediction.md) — finite-sample coverage guarantees via exchangeability and concentration

- **[Hoeffding's Inequality](term_hoeffding_inequality.md)**: Exponential bound for bounded RVs
- **[Bernstein's Inequality](term_bernstein_inequality.md)**: Variance-sensitive bound, tighter than Hoeffding
- **[Chernoff Bound](term_chernoff_bound.md)**: Generic MGF-based parent technique
- **[Bounded Differences (McDiarmid)](term_bounded_differences_inequality.md)**: Generalizes Hoeffding to functions of independent RVs
- **[JL Lemma](term_johnson_lindenstrauss_lemma.md)**: JL proof uses $\chi^2$ Chernoff + union bound — canonical concentration application

## References

- Boucheron, S., Lugosi, G., & Massart, P. (2013). *Concentration Inequalities: A Nonasymptotic Theory of Independence*. Oxford University Press.
- Vershynin, R. (2018). *High-Dimensional Probability: An Introduction with Applications in Data Science*. Cambridge University Press.
- [Wikipedia: Concentration inequality](https://en.wikipedia.org/wiki/Concentration_inequality)
