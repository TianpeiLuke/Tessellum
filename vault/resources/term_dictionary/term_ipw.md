---
tags:
  - resource
  - terminology
  - causal_inference
  - statistics
  - machine_learning
keywords:
  - IPW
  - IPTW
  - Inverse Probability Weighting
  - Inverse Probability of Treatment Weighting
  - propensity score weighting
  - stabilized weights
  - weight trimming
  - doubly robust estimator
  - AIPW
  - Augmented IPW
  - pseudo-population
topics:
  - causal inference
  - observational studies
  - treatment effect estimation
  - reweighting
language: markdown
date of note: 2026-05-01
status: active
building_block: concept
related_wiki: null
---

# IPW - Inverse Probability Weighting

## Definition

Inverse Probability Weighting (IPW), also called Inverse Probability of Treatment Weighting (IPTW), is a statistical technique for estimating causal effects from observational data by constructing a **pseudo-population** in which treatment assignment is independent of measured confounders. Each observation is reweighted by the inverse of its **propensity score** $e(X)$ — the conditional probability of receiving the treatment actually received given observed covariates $X$:

- Treated unit $i$: weight $w_i = 1 / e(X_i)$
- Control unit $i$: weight $w_i = 1 / (1 - e(X_i))$

The ATE estimator is then the weighted mean outcome difference between the two groups:

$$\hat{\tau}^{IPW} = \frac{1}{n}\sum_{i} \frac{Z_i Y_i}{e(X_i)} - \frac{1}{n}\sum_{i} \frac{(1-Z_i) Y_i}{1 - e(X_i)}$$

Intuitively, IPW upweights observations in underrepresented portions of covariate space, balancing the treated and control groups as if they had been drawn from the same distribution — approximating a randomized experiment without requiring random assignment.

## Causal Assumptions

IPW requires three identifying assumptions:

| Assumption | Formal Statement | Violation Consequence |
|-----------|-----------------|----------------------|
| **Consistency** | $Y_i = Y_i(Z_i)$ — observed outcome equals potential outcome under the assigned treatment | Causal interpretation breaks down |
| **Exchangeability** (Ignorability) | $(Y(0), Y(1)) \perp Z \mid X$ — no unmeasured confounders | Biased ATE estimates |
| **Positivity** (Common Support) | $0 < e(X) < 1$ for all $X$ — every unit has non-zero probability of each treatment | Extreme or undefined weights |

A fourth practical assumption — **correct model specification** of the propensity score model — is required in finite samples; a misspecified propensity model causes residual confounding even when the three causal assumptions hold.

## Stabilization Strategies

Propensity scores near 0 or 1 produce extreme weights that inflate variance and destabilize estimates. Two standard fixes:

### Stabilized Weights
Replace the raw numerator 1 with the marginal treatment prevalence:
- Treated: $w_i = P(Z=1) / e(X_i)$
- Control: $w_i = P(Z=0) / (1 - e(X_i))$

Stabilized weights have mean 1 by construction, reducing variance while preserving the ATE target population. Preferred over unstabilized weights in practice (Austin & Stuart 2015).

### Weight Trimming (Truncation)
Cap weights at a specified percentile threshold (commonly the 1st/99th percentiles of the weight distribution). Trimming trades a small increase in bias for a large reduction in variance and changes the effective inference population away from ATE toward a trimmed-population estimand.

## Augmented IPW (AIPW) — Doubly Robust Extension

The AIPW estimator augments IPW with a regression outcome model $\hat{m}(X, Z) = E[Y \mid X, Z]$. AIPW is **doubly robust**: consistent if *either* the propensity model or the outcome model is correctly specified — providing protection against model misspecification that pure IPW lacks. AIPW is the recommended estimator when model uncertainty is high, and reduces to IPW when no outcome model is available.

## Applications

| Domain | Use Case |
|--------|---------|
| **Medicine** | Treatment effectiveness from observational health records; pharmacoepidemiology |
| **Economics** | Policy evaluation from administrative data (job training, welfare programs) |
| **Abuse Prevention** | Causal effect of enforcement actions (suppression, CPC warnings) on future abuse rates |
| **DSI Estimation** | Downstream impact measurement for abuse programs from observational enforcement logs |
| **Off-policy Evaluation** | IPW-style importance sampling in contextual bandits uses logging policy probabilities as propensity scores to evaluate a new policy from historical data |
| **Covariate Shift** | Importance weighting to correct for distribution shift between training and deployment data |

## Questions

### Validation
1. When weight trimming reduces variance at the cost of bias, how does one quantify the bias-variance trade-off to choose the trimming threshold — and does the resulting estimand still target the ATE or a different population?
   - **Tests**: Understanding of trimming's effect on estimand (Socratic)

### Application
2. How would IPW be applied to estimate the causal effect of concession grant policy changes on refund rates — what confounders must be in $X$, and where does the positivity assumption likely fail (e.g., high-value ASIN buyers almost always granted concessions)?
   - **Tests**: Domain applicability to buyer concessions and abuse (Adjacent Possible)

### Synthesis
3. When should AIPW be preferred over IPW, and under what conditions does the doubly-robust property of AIPW fail to protect against bias (e.g., both models misspecified in correlated ways due to the same omitted confounder)?
   - **Tests**: Integration with doubly-robust methods and limits of double robustness (Liquid Network)

## Related Terms

- **[Propensity Score Matching](term_propensity_score_matching.md)**: Sibling method — PSM matches on propensity scores while IPW reweights; both require the same causal assumptions but have different efficiency properties
- **[Causal Inference](term_causal_inference.md)**: The broader field in which IPW is a primary identification strategy for observational data
- **[Counterfactual Reasoning](term_counterfactual_reasoning.md)**: IPW constructs a pseudo-population approximating the counterfactual distribution under each treatment level
- **[Confounding Variable](term_confounding_variable.md)**: IPW is specifically designed to eliminate confounding by balancing covariates via reweighting
- **[Randomized Controlled Trial](term_randomized_controlled_trial.md)**: RCTs are the experimental gold standard; IPW approximates them from observational data by rebalancing covariate distributions
- **[Structural Causal Model](term_structural_causal_model.md)**: SCMs formalize the DAG structure that justifies the ignorability assumption underpinning IPW
- **[Collider Bias](term_collider_bias.md)**: Conditioning on a collider violates ignorability — the exact assumption IPW requires; must be avoided when selecting covariates $X$
- **[False Causality](term_false_causality.md)**: IPW is a defense against spurious correlation from confounding; fails when unmeasured confounders remain
- **[Ladder of Causation](term_ladder_of_causation.md)**: IPW operates at rung 2 (intervention) of Pearl's causal hierarchy — estimating $P(Y \mid do(Z))$ from observational data
- **[Double Machine Learning](term_double_machine_learning.md)**: DML extends AIPW with Neyman orthogonality and cross-fitting to achieve root-n consistency under flexible ML propensity models
- **[Contextual Bandit](term_contextual_bandit.md)**: Off-policy evaluation in bandits uses IPW-style importance sampling with logging policy probabilities as propensity scores
- **[Logistic Regression](term_logistic_regression.md)**: The standard model for estimating propensity scores $e(X)$ in binary treatment settings
- **[Weblab](term_weblab.md)**: Amazon's A/B testing platform — the randomized experimental counterpart that IPW approximates from observational data
- **[DSI](term_dsi.md)**: Downstream Impact metrics in buyer abuse — IPW enables causal DSI estimation from observational enforcement data
- **[Drift Detection](term_drift_detection.md)**: Covariate shift correction via importance weighting is structurally analogous to IPW — both reweight observations by likelihood ratios
- **[MAB](term_mab.md)**: Multi-armed bandit off-policy evaluation uses IPW estimators for counterfactual policy comparison

## References

- [Austin, P.C. & Stuart, E.A. (2015). "Moving towards best practice when using inverse probability of treatment weighting (IPTW) using the propensity score to estimate causal treatment effects in observational studies." *Statistics in Medicine*.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4626409/)
- [Westreich, D. et al. (2015). "Imputation approaches for potential confounders in observational studies." *American Journal of Epidemiology*.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4351790/)
- [Xu, S. et al. (2021). "Use of stabilized inverse propensity scores as weights to directly estimate relative risk." *Value in Health*.](https://pmc.ncbi.nlm.nih.gov/articles/PMC8757413/)
- [Tian, L. et al. (2021). "A practical guide to applying weighting and trimming estimators." *Epidemiology*.](https://pmc.ncbi.nlm.nih.gov/articles/PMC8327194/)
- [Wikipedia: Inverse probability weighting](https://en.wikipedia.org/wiki/Inverse_probability_weighting)
- [Duke STAT 640: Observational Studies with Weighting (lecture notes)](https://www2.stat.duke.edu/~fl35/teaching/640/Chap3.4_observational_weighting.pdf)
