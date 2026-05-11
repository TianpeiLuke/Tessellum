---
tags:
  - resource
  - terminology
  - statistics
  - probability
  - concentration_inequality
keywords:
  - Hoeffding inequality
  - bounded random variables
  - exponential tail bound
  - sub-Gaussian
  - sample complexity
topics:
  - concentration inequalities
  - statistical learning theory
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Hoeffding's Inequality

## Definition

**Hoeffding's inequality** provides an exponential tail bound for sums of bounded independent random variables, without requiring knowledge of their variances.

Let $X_1, \ldots, X_n$ be independent random variables with $X_i \in [a_i, b_i]$. Then for the sample mean $\bar{X} = \frac{1}{n}\sum_{i=1}^n X_i$:

$$P\left(|\bar{X} - E[\bar{X}]| \geq t\right) \leq 2\exp\left(-\frac{2n^2 t^2}{\sum_{i=1}^n (b_i - a_i)^2}\right)$$

For the **identical range** case where all $X_i \in [a, b]$, this simplifies to:

$$P\left(|\bar{X} - E[\bar{X}]| \geq t\right) \leq 2\exp\left(-\frac{2nt^2}{(b - a)^2}\right)$$

## Key Properties

- **Distribution-free**: only requires bounded support, no variance or shape assumptions
- **Sub-Gaussian behavior**: the tail decays as $\exp(-Ct^2)$, matching Gaussian tail rates
- **Does not use variance information**: this makes it looser than [Bernstein's inequality](term_bernstein_inequality.md) when the variance $\sigma^2$ is small relative to the range $(b - a)^2$
- **Sample complexity**: inverting the bound gives the classic $n = O(1/\epsilon^2)$ scaling for $\epsilon$-accurate estimation

## Proof Sketch

1. Apply the [Chernoff bound](term_chernoff_bound.md) (MGF method) to each $X_i$
2. Use **Hoeffding's lemma**: if $X \in [a, b]$ and $E[X] = 0$, then $E[e^{sX}] \leq \exp\left(\frac{s^2(b-a)^2}{8}\right)$
3. Optimize over the free parameter $s > 0$

## Abuse Prevention Relevance

Used to derive [confidence intervals](term_confidence_interval.md) for abuse rate estimates and to bound the sample complexity needed for reliable A/B tests on policy changes.

## Related Terms

- [Concentration Inequality](term_concentration_inequality.md) — parent overview
- [Bernstein's Inequality](term_bernstein_inequality.md) — tighter variance-aware alternative
- [Chernoff Bound](term_chernoff_bound.md) — underlying MGF technique
- [Confidence Interval](term_confidence_interval.md) — practical application
- [Normal Distribution](term_normal_distribution.md) — sub-Gaussian connection
- **[Sub-Gaussian](term_sub_gaussian.md)**: Distributional class for which Hoeffding-type bounds hold
- **[PAC Learning](term_pac_learning.md)**: Uses Hoeffding + union bound for finite hypothesis class sample complexity
- **[JL Lemma](term_johnson_lindenstrauss_lemma.md)**: Sparse JL uses Hoeffding for $\{-1,0,+1\}$ projection entries
