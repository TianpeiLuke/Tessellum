---
tags:
  - resource
  - terminology
  - statistics
  - probability
  - concentration_inequality
keywords:
  - Bernstein inequality
  - variance-dependent bound
  - sub-exponential
  - tighter than Hoeffding
topics:
  - concentration inequalities
  - statistical learning theory
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Bernstein's Inequality

## Definition

**Bernstein's inequality** provides a variance-sensitive tail bound for sums of bounded random variables, yielding tighter results than [Hoeffding's inequality](term_hoeffding_inequality.md) when the variance is small.

Let $X_1, \ldots, X_n$ be independent random variables with $E[X_i] = 0$, $\text{Var}(X_i) \leq \sigma^2$, and $|X_i| \leq M$. Then:

$$P\left(\left|\frac{1}{n}\sum_{i=1}^n X_i\right| \geq t\right) \leq 2\exp\left(-\frac{nt^2 / 2}{\sigma^2 + Mt/3}\right)$$

## Two Regimes

The bound interpolates between two tail behaviors depending on the deviation size $t$:

| Regime | Condition | Tail Behavior | Character |
|--------|-----------|---------------|-----------|
| **Small $t$** | $t \ll \sigma^2 / M$ | $\exp\left(-\frac{nt^2}{2\sigma^2}\right)$ | Gaussian (sub-Gaussian) |
| **Large $t$** | $t \gg \sigma^2 / M$ | $\exp\left(-\frac{3nt}{2M}\right)$ | Exponential (sub-exponential) |

## Why Tighter Than Hoeffding

Hoeffding uses only the range $[a, b]$ and effectively assumes worst-case variance $\sigma^2 = (b-a)^2/4$. Bernstein exploits the actual variance $\sigma^2$, so when $\sigma^2 \ll (b-a)^2/4$ (e.g., rare-event indicators), Bernstein gives a much tighter bound.

**Example**: for a Bernoulli($p$) with $p = 0.01$, Hoeffding treats the range as $[0,1]$ while Bernstein uses $\sigma^2 = p(1-p) \approx 0.01$ — a 25× improvement in the exponent.

## Abuse Prevention Relevance

Abuse events are typically rare ($p \ll 1$), making Bernstein bounds substantially tighter than Hoeffding for estimating abuse rates and designing sample sizes for policy experiments.

## Related Terms

- [Concentration Inequality](term_concentration_inequality.md) — parent overview
- [Hoeffding's Inequality](term_hoeffding_inequality.md) — simpler but looser alternative
- [Chernoff Bound](term_chernoff_bound.md) — underlying MGF framework
- **[LASSO](term_lasso.md)**: LASSO consistency proofs use Bernstein-type bounds for restricted eigenvalue conditions
- **[GraphLasso](term_graphlasso.md)**: GraphLasso convergence rates use Bernstein bounds on sample covariance
- **[PAC Learning](term_pac_learning.md)**: Variance-dependent PAC bounds via Bernstein are tighter than Hoeffding-based
- **[Confidence Interval](term_confidence_interval.md)**: Bernstein gives tighter CIs when variance is known to be small
- **[Binomial Distribution](term_binomial_distribution.md)**: Bernstein bound for Binomial is tighter than Hoeffding when p is small
- **[Normal Distribution](term_normal_distribution.md)**: Bernstein interpolates between Gaussian tail (small t) and exponential tail (large t)
- **[Exponential Family](term_exponential_family.md)**: Bernstein applies to bounded exponential family members
- **[Sub-Gaussian](term_sub_gaussian.md)**: Sub-exponential class (Bernstein's domain) is strictly larger than sub-Gaussian
- **[JL Lemma](term_johnson_lindenstrauss_lemma.md)**: Bernstein bounds give tighter JL guarantees when projection variance is small
