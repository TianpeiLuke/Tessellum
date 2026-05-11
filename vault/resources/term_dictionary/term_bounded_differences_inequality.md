---
tags:
  - resource
  - terminology
  - statistics
  - probability
  - concentration_inequality
keywords:
  - bounded differences
  - McDiarmid inequality
  - function of independent RVs
  - Lipschitz
  - stability
topics:
  - concentration inequalities
  - statistical learning theory
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Bounded Differences Inequality (McDiarmid's Inequality)

## Definition

The **bounded differences inequality** (McDiarmid's inequality) extends [Hoeffding's inequality](term_hoeffding_inequality.md) from sums to arbitrary functions of independent random variables that satisfy a Lipschitz-like stability condition.

Let $X_1, \ldots, X_n$ be independent random variables and $f: \mathcal{X}^n \to \mathbb{R}$ satisfy the **bounded differences condition**: for each $i$,

$$\sup_{x_1,\ldots,x_n,\, x_i'} |f(x_1,\ldots,x_i,\ldots,x_n) - f(x_1,\ldots,x_i',\ldots,x_n)| \leq c_i$$

Then:

$$P\left(|f(X_1,\ldots,X_n) - E[f]| \geq t\right) \leq 2\exp\left(-\frac{2t^2}{\sum_{i=1}^n c_i^2}\right)$$

## Key Properties

- **Generalizes Hoeffding**: setting $f = \frac{1}{n}\sum X_i$ with $X_i \in [a_i, b_i]$ gives $c_i = (b_i - a_i)/n$, recovering Hoeffding's inequality
- **Function-level concentration**: applies to any measurable function, not just sums
- **Stability interpretation**: $c_i$ measures how sensitive $f$ is to changing a single input — functions with small $c_i$ concentrate tightly

## Proof Sketch

1. Decompose $f - E[f]$ via a **martingale difference sequence** using conditional expectations
2. Apply [Hoeffding's lemma](term_hoeffding_inequality.md) to each martingale increment (bounded by $c_i$)
3. Combine via the [Chernoff bound](term_chernoff_bound.md) (MGF method)

## Applications in ML

McDiarmid's inequality is the standard tool for proving **generalization bounds** in statistical learning theory:

- **Empirical risk**: changing one training example changes the empirical risk by at most $c_i = M/n$ (for loss bounded by $M$), so empirical risk concentrates around expected risk
- **Rademacher complexity**: the symmetrized empirical process concentrates via bounded differences
- **Cross-validation**: leave-one-out stability arguments use the bounded differences condition

## Related Terms

- [Concentration Inequality](term_concentration_inequality.md) — parent overview
- [Hoeffding's Inequality](term_hoeffding_inequality.md) — special case for sums
- [Lasso](term_lasso.md) — stability analysis uses bounded differences
- **[PAC Learning](term_pac_learning.md)**: Generalization bounds use bounded differences inequality
- **[GraphLasso](term_graphlasso.md)**: GraphLasso estimation stability analyzed via bounded differences
- **[Normal Distribution](term_normal_distribution.md)**: McDiarmid gives sub-Gaussian concentration for functions of independent RVs
- **[Random Forest](term_random_forest.md)**: Random forest generalization bounds use McDiarmid's inequality
- **[XGBoost](term_xgboost.md)**: Ensemble stability bounds via bounded differences
- **[Neural Networks](term_neural_networks.md)**: Neural network generalization via algorithmic stability + McDiarmid
- **[JL Lemma](term_johnson_lindenstrauss_lemma.md)**: McDiarmid proves JL for functions of independent random projections
