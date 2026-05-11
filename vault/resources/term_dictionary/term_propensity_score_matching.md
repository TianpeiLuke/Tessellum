---
tags:
  - resource
  - terminology
  - causal_inference
  - statistics
  - observational_studies
  - treatment_effects
keywords:
  - propensity score matching
  - PSM
  - propensity score
  - causal inference
  - observational study
  - treatment effect
  - confounding
  - selection bias
  - inverse probability weighting
  - IPTW
  - average treatment effect
  - ATE
  - ATT
  - Rosenbaum
  - Rubin
topics:
  - Causal Inference
  - Statistics
  - Observational Studies
  - Treatment Effect Estimation
language: markdown
date of note: 2026-03-29
status: active
building_block: concept
---

# Propensity Score Matching (PSM)

## Definition

**Propensity Score Matching (PSM)** is a statistical technique for estimating causal treatment effects from observational data by matching treated and control units with similar **propensity scores** — the conditional probability of receiving treatment given observed covariates. Introduced by Rosenbaum and Rubin (1983), PSM reduces confounding bias by balancing observed covariates across treatment groups, mimicking the conditions of a [Randomized Controlled Trial](term_randomized_controlled_trial.md) without requiring random assignment.

Formally, the **propensity score** for a unit $i$ with covariates $X_i$ is:

$$e(X_i) = P(Z_i = 1 \mid X_i)$$

where $Z_i \in \{0, 1\}$ is the binary treatment indicator. Rosenbaum and Rubin proved that if treatment assignment is strongly ignorable given $X$, then it is also strongly ignorable given $e(X)$ alone — reducing a potentially high-dimensional covariate matching problem to a single-dimensional score.

The key insight is **dimensionality reduction**: instead of matching on all covariates simultaneously (which becomes infeasible in high dimensions — the "curse of dimensionality"), PSM collapses all covariates into a single scalar summary that is sufficient for removing confounding bias under the identifying assumptions.

## Historical Context

| Year | Contributor | Contribution |
|------|------------|--------------|
| 1973-1979 | Donald Rubin | Foundational work on matching methods and the potential outcomes framework |
| **1983** | **Rosenbaum & Rubin** | **"The Central Role of the Propensity Score in Observational Studies for Causal Effects"** — *Biometrika*, 70(1): 41-55. Defined propensity scores and proved their balancing properties. |
| 1984 | Rosenbaum & Rubin | Extended PSM to sensitivity analysis for hidden bias |
| 2000 | Judea Pearl | *Causality* — provided structural causal model framework; later critiqued PSM's vulnerability to dormant confounders |
| 2006 | Austin | Systematic comparison of PSM implementations in observational studies |
| 2011 | Austin | Tutorial on propensity score methods — established four main approaches |
| 2019 | King & Nielsen | "Why Propensity Scores Should Not Be Used for Matching" — *Political Analysis*. Argued PSM can increase imbalance, inefficiency, and bias compared to alternatives |

## Taxonomy

### Four Propensity Score Methods

| Method | Mechanism | Strengths | Weaknesses |
|--------|-----------|-----------|------------|
| **Matching** | Pair treated units with control units having similar propensity scores | Intuitive; explicit counterfactual construction | Discards unmatched units; order-dependent |
| **Stratification** (Subclassification) | Partition sample into strata by propensity score quintiles; estimate treatment effect within each stratum | Retains all observations; simple | Coarse adjustment; residual confounding within strata |
| **Inverse Probability Weighting (IPTW)** | Weight each observation by the inverse of its propensity score to create a pseudopopulation | Retains full sample; less bias for hazard ratios | Extreme weights from near-zero probabilities; high variance |
| **Covariate Adjustment** | Include propensity score as a covariate in outcome regression | Simple to implement | May not fully balance covariates; model-dependent |

### Matching Algorithm Variants

| Variant | Description | Trade-off |
|---------|-------------|-----------|
| **Nearest neighbor** | Match to closest propensity score | Simple but can produce poor matches if caliper is wide |
| **Caliper matching** | Match within a maximum distance threshold | Prevents bad matches; may discard units outside caliper |
| **Kernel matching** | Use weighted average of all controls, weighted by kernel function of distance | Uses all data; bandwidth choice matters |
| **Optimal full matching** | Minimize total distance across all matched sets | Optimal; computationally expensive |
| **Mahalanobis distance + PSM** | Match on Mahalanobis distance within propensity score calipers | Better balance; more complex |
| **Many-to-one matching** | Match multiple controls to each treated unit | Increases efficiency; requires sufficient controls |

### Estimands

| Estimand | Definition | When to Use |
|----------|-----------|-------------|
| **ATE** (Average Treatment Effect) | $E[Y(1) - Y(0)]$ — average effect across entire population | Policy evaluation affecting everyone |
| **ATT** (Average Treatment Effect on Treated) | $E[Y(1) - Y(0) \mid Z=1]$ — effect for those who received treatment | Evaluating effect on those who were actually treated |
| **ATC** (Average Treatment Effect on Controls) | $E[Y(1) - Y(0) \mid Z=0]$ — effect for untreated group | Estimating what would happen if controls received treatment |

## Key Properties

- **Balancing property**: Within strata of the propensity score, the distribution of observed covariates is the same for treated and control units
- **Sufficiency**: The propensity score is the coarsest balancing score — it provides the minimum dimensionality reduction sufficient for confounding adjustment
- **Dimensionality reduction**: Collapses multi-dimensional covariate space into a single scalar, making matching feasible in high dimensions
- **Design separation**: PSM separates the design phase (constructing matched groups) from the analysis phase (estimating treatment effects), reducing researcher degrees of freedom
- **Transparency**: Matched samples can be inspected for balance before outcome analysis — unlike regression adjustment which conflates design and analysis

### Key Assumptions

| Assumption | Formal Statement | Violation Consequence |
|-----------|-----------------|----------------------|
| **Unconfoundedness** (Ignorability) | $(Y(0), Y(1)) \perp Z \mid X$ — no unobserved confounders | Biased treatment effect estimates |
| **Overlap** (Common Support) | $0 < P(Z=1 \mid X) < 1$ for all $X$ | Extrapolation beyond data; extreme weights in IPTW |
| **SUTVA** | Treatment of one unit does not affect others' outcomes | Interference bias (e.g., network effects) |
| **Correct model specification** | Propensity score model includes all confounders in correct functional form | Residual confounding |

## Applications

| Domain | Application | Example |
|--------|-------------|---------|
| **Medicine** | Treatment effectiveness from observational health records | Comparing drug A vs. drug B when RCT is unethical |
| **Economics** | Policy evaluation from administrative data | Effect of job training programs on employment |
| **Education** | Program impact evaluation | Effect of school vouchers on student achievement |
| **Epidemiology** | Exposure-outcome studies | Smoking and lung cancer from cohort data |
| **Abuse Prevention** | Evaluating intervention effectiveness | Effect of enforcement actions (suppression, warnings) on future abuse behavior; measuring [DSI](term_dsi.md) of abuse prevention programs |
| **Tech/A-B Testing** | Quasi-experimental analysis when randomization fails | Analyzing treatment effects when A/B test has selection bias or compliance issues |

## Challenges and Limitations

### Fundamental Limitations

- **Unobserved confounders**: PSM only balances *observed* covariates — hidden confounders can still bias results. Judea Pearl argued matching may "unleash bias due to dormant unobserved confounders" that were d-separated before conditioning
- **Model dependence**: King & Nielsen (2019) showed PSM can increase imbalance, inefficiency, model dependence, and bias compared to alternatives like coarsened exact matching (CEM) or Mahalanobis distance matching
- **No causation guarantee**: Even with perfect balance on observed covariates, causal interpretation requires the unconfoundedness assumption — which is fundamentally untestable

### Practical Challenges

- **Propensity score model specification**: Incorrect functional form (e.g., missing interactions, nonlinearities) leads to residual confounding
- **Common support**: Lack of overlap between treatment and control propensity score distributions limits valid inference
- **Sample loss**: Matching (especially with calipers) can discard a large fraction of the sample, reducing generalizability
- **Multiple testing**: Researchers may iterate on propensity score models until balance is achieved, inflating Type I error
- **Sensitivity to matching algorithm**: Results can vary across nearest-neighbor, caliper, kernel, and full matching methods

### Alternatives When PSM Fails

| Alternative | When Preferred | Reference |
|-------------|---------------|-----------|
| **Coarsened Exact Matching (CEM)** | Fewer covariates; want exact balance | Iacus, King, Porro (2012) |
| **Doubly Robust Estimation** | Want protection against model misspecification | Robins, Rotnitzky, Zhao (1994) |
| **Instrumental Variables (IV)** | Unobserved confounders present; valid instrument available | Angrist, Imbens, Rubin (1996) |
| **Regression Discontinuity (RD)** | Treatment assigned by a threshold | Thistlethwaite, Campbell (1960) |
| **Difference-in-Differences (DiD)** | Panel data; parallel trends assumption holds | Card, Krueger (1994) |
| **Synthetic Control** | Few treated units; aggregate outcomes | Abadie, Diamond, Hainmueller (2010) |

## Notable Implementations

| Software | Package | Features |
|----------|---------|----------|
| **R** | `MatchIt` | Nearest neighbor, optimal, full, CEM, exact matching |
| **R** | `optmatch` | Optimal full matching |
| **R** | `WeightIt` | IPTW, entropy balancing, CBPS |
| **Python** | `PsmPy` | PSM with visualization |
| **Python** | `DoWhy` | End-to-end causal inference with PSM |
| **Python** | `CausalML` | Uplift modeling with propensity-based methods |
| **Stata** | `psmatch2`, `teffects` | PSM, IPTW, regression adjustment |
| **SAS** | `PSMatch` | Propensity score matching procedure |

## Questions

### Validation (Socratic — "Why?")
1. The unconfoundedness assumption is fundamentally untestable — how do we assess the credibility of PSM results when we cannot verify the core identifying assumption? What sensitivity analysis approaches (e.g., Rosenbaum bounds) provide useful diagnostics?
   - **Tests**: Whether PSM results are robust to potential hidden bias (WYSIATI)

2. King & Nielsen (2019) argue PSM should not be used for matching at all — is this critique definitive, or does it apply only to specific PSM implementations (e.g., nearest-neighbor without calipers)?
   - **Tests**: Whether PSM is still a valid method post-King-Nielsen critique (Devil's Advocate)

### Application (Taxonomic — "What If? / How?")
3. How would PSM be applied to evaluate the causal effect of abuse enforcement actions (e.g., account suppression) on future abuse behavior — what covariates would need to be balanced, and where would the overlap assumption likely fail?
   - **Tests**: Domain applicability to buyer abuse prevention (Adjacent Possible)

### Synthesis (Lateral — "Who Else?")
4. How does PSM relate to [Do-Calculus](term_do_calculus.md) and the [Structural Causal Model](term_structural_causal_model.md) framework — does Pearl's critique of PSM imply that SCM-based adjustment (backdoor criterion) is strictly superior, or do the two approaches have complementary strengths?
   - **Tests**: Relationship between Rubin's potential outcomes framework and Pearl's structural approach (Liquid Network)

## Related Terms

- **[Causal Inference](term_causal_inference.md)**: The broader field PSM belongs to — estimating causal effects from data
- **[Randomized Controlled Trial](term_randomized_controlled_trial.md)**: The gold standard that PSM approximates for observational data
- **[Counterfactual Reasoning](term_counterfactual_reasoning.md)**: The conceptual foundation — PSM constructs counterfactuals by matching
- **[Structural Causal Model](term_structural_causal_model.md)**: Pearl's alternative framework for causal reasoning; provides d-separation and backdoor criterion
- **[Do-Calculus](term_do_calculus.md)**: Pearl's formal system for identifying causal effects; relates to but differs from propensity score approaches
- **[Ladder of Causation](term_ladder_of_causation.md)**: PSM operates at rung 2 (intervention) of Pearl's causal hierarchy
- **[Directed Acyclic Graph](term_directed_acyclic_graph.md)**: DAGs formalize the causal structure that PSM's assumptions require
- **[DSI](term_dsi.md)**: Downstream Impact measurement in abuse prevention — PSM can estimate DSI when randomization is infeasible
- **[Mediation Analysis](term_mediation_analysis.md)**: Related causal method for decomposing direct and indirect effects
- **[Difference-in-Differences](term_difference_in_differences.md)**: Complementary quasi-experimental method; often combined with PSM to strengthen parallel trends
- **[Double Machine Learning](term_double_machine_learning.md)**: DML improves on PSM by being robust to propensity model misspecification through Neyman orthogonality
- **[Inverse Probability Weighting](term_ipw.md)**: IPW (also IPTW) is a sibling propensity-score method that reweights observations by 1/e(X) instead of matching; both share Rosenbaum-Rubin foundations

## References

### Vault Sources

### External Sources
- [Rosenbaum, P.R. & Rubin, D.B. (1983). "The Central Role of the Propensity Score in Observational Studies for Causal Effects." *Biometrika*, 70(1): 41-55.](https://www.stat.cmu.edu/~ryantibs/journalclub/rosenbaum_1983.pdf) — The foundational PSM paper
- [Austin, P.C. (2011). "An Introduction to Propensity Score Methods for Reducing the Effects of Confounding in Observational Studies." *Multivariate Behavioral Research*, 46(3): 399-424.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3144483/) — Comprehensive tutorial on four propensity score methods
- [King, G. & Nielsen, R. (2019). "Why Propensity Scores Should Not Be Used for Matching." *Political Analysis*, 27(4): 435-454.](https://gking.harvard.edu/publications/why-propensity-scores-should-not-be-used-formatching) — Influential critique of PSM
- [Wikipedia: Propensity Score Matching](https://en.wikipedia.org/wiki/Propensity_score_matching)
- [Columbia Public Health: Propensity Score Analysis](https://www.publichealth.columbia.edu/research/population-health-methods/propensity-score-analysis) — Methods overview
- [Built In: Propensity Score Matching Guide](https://builtin.com/data-science/propensity-score-matching) — Practical tutorial
