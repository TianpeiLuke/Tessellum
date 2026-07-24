---
tags:
  - resource
  - terminology
  - machine_learning
  - causal_inference
  - analytics
  - experimentation
keywords:
  - Causal Inference
  - CI
  - uplift modeling
  - CATE
  - treatment effect
  - counterfactual
  - RDD
  - A/B testing
  - observational data
topics:
  - measurement methodology
  - experimentation
  - ML causal methods
language: markdown
date of note: 2026-03-02
status: active
building_block: concept
---

# Term: Causal Inference

## Definition

**Causal Inference** is a collection of statistical and machine learning methodologies that estimate the **causal effect** of an action, intervention, or treatment on an outcome — answering the "with-and-without" question rather than the "before-and-after" question that standard prediction models address. It is applied across three broad domains: (1) **measuring intervention impact**, quantifying how an action affects an outcome over time; (2) **identifying heterogeneous responders** via uplift models that find which units benefit most (or are harmed) by a treatment; and (3) **optimizing treatment decisions** through CATE (Conditional Average Treatment Effect) estimation. The core challenge across all these applications is the **fundamental problem of counterfactuals** — for each unit, only one treatment outcome (treated or control) is observed, never both.

## Core Concepts

### The Causal vs. Predictive Distinction

| Approach | Question | Method |
|----------|----------|--------|
| **Predictive ML** | "Given features, what outcome will occur?" | XGBoost, Neural Networks |
| **Causal Inference** | "If we take this action, how does it change the outcome?" | Uplift models, matching, RDD |

**Key Insight**: A predictive model that says "this unit has 90% event probability" cannot tell you what happens if you intervene one way vs. another. Only causal methods answer the counterfactual question.

### Fundamental Problem of Causal Inference

For any individual, we observe only one potential outcome:
- **Observed**: What actually happened after treatment (or control) was applied
- **Counterfactual**: What *would* have happened under the alternative action

```
Y_observed(unit_i) = Y_treatment(i) if treated, OR Y_control(i) if control
Y_counterfactual(unit_i) = NEVER directly observable
```

**CATE (Conditional Average Treatment Effect)**:  
`τ(x) = E[Y_treatment(x) - Y_control(x)]`  
→ The expected difference in outcome between treated and control, conditional on features x

## Causal Inference Methods

### 1. Treatment-Control Matching

Used for measuring intervention impact from observational data:
- **Treatment group**: Units that received the intervention
- **Control group**: Statistically matched units that did NOT receive the intervention
- **Matching**: [Propensity score matching](term_propensity_score_matching.md) or covariate matching to ensure comparable groups
- **Measurement**: Track outcomes over multiple time horizons
- **Validation**: Placebo test — apply methodology to a period where no effect should exist; if the causal estimate is near zero, the methodology is valid

### 2. Uplift Modeling

Used for identifying which units respond to treatment:

**Problem**: A treatment may help some units, harm others, and leave the rest unaffected. Aggregate metrics obscure this heterogeneity.

**Solution**: Uplift models predict the incremental effect of treatment per unit, enabling targeting of the units most positively affected.

**Algorithms**:
- **Uplift Random Forest**: Split criterion based on KL divergence or Euclidean distance between treatment/control distributions
- **Meta-Learners** (T-Learner, S-Learner, X-Learner): Train separate models for treatment and control groups, compute CATE as difference
- **Orthogonal Random Forest**: Doubly robust estimation; computationally intensive
- **Evaluation**: Qini curve and Qini coefficient (since no counterfactual ground truth exists)

### 3. Causal ML for Treatment Optimization

For choosing the best action per unit:

**Methods Compared**:
| Method | Approach | Strength |
|--------|----------|---------|
| T-Learner (XGB) | Train separate models per action | Strong Qini curve performance |
| X-Learner | Impute counterfactual outcomes | Reduces bias for imbalanced groups |
| S-Learner (TabNet) | Single model with action indicator | Simple but biases toward 0 |
| DragonNet | Shared embedding + action heads | Better cell-wise prediction |
| Q-Learning (RL) | Optimize cumulative reward | Best for sequential decisions |

**Key distinction — Estimation vs. Optimization**:
- **Uplift/Causal ML**: Estimates CATE — identifies who benefits from treatment
- **RL/Contextual Bandits**: Optimizes cumulative return — directly maximizes policy objective

### 4. Multi-Outcome Uplift Modeling

Extension for complex scenarios where outcomes are not binary:

**Generalized ATE (GATE)**:  
`GATE(i,j) = P[Y_treatment = i] - P[Y_control = j]`

Used when outcomes are multi-valued, requiring generalized gain curves and T-learners extended to multi-class classification.

### 5. A/B Testing (Randomized Controlled Experiments)

Randomized controlled experiments for measuring causal effects when randomization is possible:
- **Pre-registered treatment/control** groups with known randomization → enables unbiased CATE estimation
- Used for validating observational measurements and testing new policies before full rollout

### 6. Regression Discontinuity Design (RDD)

A quasi-experimental causal method leveraging thresholds in assignment rules:
- **Intuition**: Units just above/below a score threshold are comparable — differences in outcomes near the cutoff are causally attributable to the treatment
- Uses the discontinuity at the threshold to identify local average treatment effect (LATE)

## Key Causal Inference Packages

| Package | Use Case | Notes |
|---------|----------|-------|
| **CausalML** | Meta-learners, uplift RF | Uber's open-source library |
| **EconML** | Orthogonal RF, CATE estimation | Microsoft, doubly robust methods |
| **scikit-uplift** | Uplift evaluation (Qini, lift curves) | Dedicated uplift evaluation tools |
| **Ray RLlib** | RL-based treatment optimization | Used for Q-learning experiments |

## Causal Inference vs. Standard ML

| Dimension | Standard ML (XGBoost, LightGBM) | Causal Inference |
|-----------|----------------------------------|------------------|
| **Question** | What outcome will occur? | What changes if we act? |
| **Data requirement** | Large labeled dataset | Treatment/control split or experimental data |
| **Evaluation** | AUC, F1, Precision/Recall | Qini curve, AUUC, ATE |
| **Output** | Risk score (probability) | Treatment effect (CATE τ(x)) |
| **Use case** | Real-time prediction | Policy design, responder detection, impact measurement |

## Related Terms

### Causal Methods & Applications
- **[Term: Causal Model](term_causal_model.md)** - Structured causal models (DAGs) for encoding causal assumptions

### ML Methods Related to Causal Inference
- **[Term: XGBoost](term_xgboost.md)** - Used as base learner in T-Learner and X-Learner meta-learning approaches
- **[Term: RL](term_rl.md)** - Reinforcement learning; optimization-focused alternative to causal estimation
- **[Term: CMAB](term_contextual_bandit.md)** - Contextual Bandits; bridges causal estimation and policy optimization
- **[Term: Active Learning](term_active_learning.md)** - Selects informative samples; complements causal methods for label efficiency

### Measurement & Metrics
- **[Term: FPR](term_false_positive.md)** - False Positive Rate; causal methods help estimate true FPR beyond observed rates
- **[Term: AUC](term_auc.md)** - Predictive model evaluation; complemented by Qini curve for uplift model evaluation

## References

### External Resources
- **CausalML Library**: https://causalml.readthedocs.io/en/latest/about.html
- **EconML Library**: https://econml.azurewebsites.net/index.html
- **Awesome Causality Algorithms**: https://github.com/rguo12/awesome-causality-algorithms
- **"Metalearners for estimating heterogeneous treatment effects using machine learning"** (Künzel et al., PNAS 2019): https://www.pnas.org/doi/full/10.1073/pnas.1804597116
- **"Causal Inference and Uplift Modeling: A review of the literature"** (JMLR 2016): https://proceedings.mlr.press/v67/gutierrez17a/gutierrez17a.pdf

## Summary

**Causal Inference Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Core Question** | "What would happen if we had acted differently?" (counterfactual) |
| **vs Predictive ML** | Predicts effect of action, not just probability of outcome |
| **Key Concept** | CATE: τ(x) = E[Y_treatment - Y_control \| features x] |
| **Key Methods** | Uplift RF, T/X/S-Learner, Treatment-Control Matching, RDD, A/B Testing |
| **Evaluation** | Qini curve, AUUC (uplift); matched-outcome comparison with placebo test |
| **Key Challenge** | Fundamental problem: only one outcome observed per individual per treatment |
| **Packages** | CausalML, EconML, scikit-uplift |

**Key Insight**: Causal inference **bridges the gap between what models detect and what interventions should be taken**. Standard ML answers "is this event likely?" while causal inference answers "what happens if we intervene?" Because observed data reflect only the actions actually taken, naive metrics can severely misestimate the effect of alternative policies — a systematic bias that only causal methods can detect and correct.

---

**Last Updated**: March 2, 2026  
**Status**: Active - foundational methodology for intervention impact measurement and responder detection
