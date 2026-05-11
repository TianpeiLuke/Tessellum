---
tags:
  - resource
  - terminology
  - causal_inference
  - statistics
  - econometrics
  - quasi_experiment
keywords:
  - difference in differences
  - DID
  - DiD
  - DD
  - diff-in-diff
  - quasi-experiment
  - parallel trends
  - treatment effect
  - natural experiment
  - panel data
  - two-way fixed effects
  - TWFE
  - staggered adoption
  - Callaway-Sant'Anna
  - Card-Krueger
topics:
  - Causal Inference
  - Econometrics
  - Quasi-Experimental Design
  - Treatment Effect Estimation
language: markdown
date of note: 2026-03-29
status: active
building_block: concept
---

# Difference-in-Differences (DiD)

## Definition

**Difference-in-Differences (DiD)** is a quasi-experimental statistical technique for estimating causal treatment effects by comparing the change in outcomes over time between a treatment group and a control group. It exploits the structure of longitudinal (panel) data to remove time-invariant confounders, isolating the treatment effect as the *difference* between the treatment group's change and the control group's change.

The basic DiD estimator is:

$$\hat{\delta} = (\bar{Y}_{T,\text{post}} - \bar{Y}_{T,\text{pre}}) - (\bar{Y}_{C,\text{post}} - \bar{Y}_{C,\text{pre}})$$

where $T$ denotes the treatment group, $C$ the control group, and $\text{pre}$/$\text{post}$ denote the periods before and after treatment. The first difference removes time-invariant group characteristics; the second difference removes common time trends — hence "difference-in-differences."

In regression form:

$$Y_{it} = \alpha + \beta \cdot \text{Group}_i + \gamma \cdot \text{Post}_t + \delta \cdot (\text{Group}_i \times \text{Post}_t) + \varepsilon_{it}$$

where $\delta$ is the DiD estimator — the causal effect of interest.

The key identifying assumption is **parallel trends**: absent treatment, the treatment and control groups would have followed the same trajectory over time. This assumption is fundamentally untestable but can be assessed by examining pre-treatment trends.

## Historical Context

| Year | Contributor | Contribution |
|------|------------|--------------|
| 1854 | John Snow | Used proto-DiD logic to identify cholera transmission by comparing water companies in London — considered the earliest application of the underlying reasoning |
| 1847 | Ignaz Semmelweis | Compared maternal mortality rates before/after handwashing intervention across clinics — another proto-DiD application |
| **1984** | **Ashenfelter & Card** | **Coined the term "difference-in-differences"** in an NBER working paper studying job training programs |
| **1994** | **Card & Krueger** | Famous minimum wage study comparing NJ vs. PA fast-food employment — became the canonical DiD example. Card received the 2021 Nobel Prize in part for this work. |
| 2000s | Bertrand, Duflo, Mullainathan | Identified serial correlation problem in DiD standard errors; proposed clustering |
| 2021 | Callaway & Sant'Anna | New framework for DiD with multiple time periods and staggered treatment — addressing TWFE bias |
| 2021 | Sun & Abraham | Interaction-weighted estimator for staggered DiD |
| 2020-2023 | de Chaisemartin & D'Haultfoeuille, Goodman-Bacon, Borusyak et al. | "DiD revolution" — showed that two-way fixed effects (TWFE) estimators can be biased with heterogeneous treatment effects and staggered adoption |

## Taxonomy

### DiD Variants

| Variant | Description | When to Use |
|---------|-------------|-------------|
| **Classic 2x2 DiD** | Two groups, two time periods | Single treatment at a single point in time |
| **Two-Way Fixed Effects (TWFE)** | Unit and time fixed effects in regression | Multiple periods, but homogeneous treatment effects |
| **Staggered DiD** | Treatment adopted at different times by different units | Policy rollouts, phased launches |
| **Triple Differences (DDD)** | Add a third differencing dimension | When parallel trends holds only conditionally |
| **Synthetic DiD** | Combine synthetic control with DiD | Few treated units; improve parallel trends |
| **Callaway-Sant'Anna** | Group-time ATT with aggregation | Staggered adoption with heterogeneous effects |
| **Sun-Abraham** | Interaction-weighted estimator | Staggered adoption; event study specification |
| **de Chaisemartin-D'Haultfoeuille** | Robust estimator for heterogeneous effects | TWFE is biased; need treatment effect heterogeneity |

### Estimands

| Estimand | Definition | Context |
|----------|-----------|---------|
| **ATT** | Average Treatment Effect on the Treated | Most common DiD target — effect on those who received treatment |
| **Group-time ATT** | $ATT(g,t)$ — effect for group $g$ at time $t$ | Callaway-Sant'Anna framework; allows heterogeneity |
| **Dynamic treatment effects** | Effect at event-time $e$ relative to treatment | Event study designs; captures effect evolution |

## Key Properties

- **Controls for time-invariant confounders**: Unit fixed effects absorb all stable characteristics (risk profile, geography, demographics) without measuring them
- **Controls for common time trends**: Time fixed effects absorb shocks affecting all units equally (seasonality, policy changes)
- **Requires only two periods minimum**: The simplest quasi-experimental design — just pre and post for two groups
- **Transparent**: The 2x2 table of means is immediately interpretable; no black-box estimation
- **Complementary to matching**: DiD can be combined with [Propensity Score Matching](term_propensity_score_matching.md) to strengthen the parallel trends assumption
- **Vulnerable to differential trends**: If treatment and control groups have different underlying trends, the estimate is biased
- **Serial correlation**: Standard errors must be clustered at the unit level to account for within-unit correlation over time (Bertrand, Duflo, Mullainathan 2004)

### Key Assumptions

| Assumption | Formal Statement | Violation Consequence |
|-----------|-----------------|----------------------|
| **Parallel trends** | $E[Y(0)_{T,\text{post}} - Y(0)_{T,\text{pre}}] = E[Y(0)_{C,\text{post}} - Y(0)_{C,\text{pre}}]$ | Biased treatment effect (most critical) |
| **No anticipation** | Treatment group does not change behavior before treatment | Pre-treatment divergence biases estimate |
| **SUTVA** | Treatment of one unit does not affect others | Spillover effects bias estimate |
| **Stable composition** | Group membership does not change over time | Selection bias from differential attrition |
| **No concurrent shocks** | No other event affects treatment group differently | Confounded estimate |

## Applications

| Domain | Application | Example |
|--------|-------------|---------|
| **Labor economics** | Minimum wage effects | Card & Krueger (1994): NJ vs. PA fast-food employment |
| **Public health** | Policy impact evaluation | Effect of smoking bans on heart attack rates |
| **Education** | Program evaluation | Impact of school funding reforms on student outcomes |
| **Economic history** | Historical event analysis | Sherman's March long-term economic effects |
| **Tech/A-B testing** | Quasi-experimental analysis | Effect of a feature rollout when A/B test is infeasible |
| **Abuse prevention** | Enforcement impact | Comparing abuse rates in treatment vs. control marketplaces before/after policy launch; measuring [DSI](term_dsi.md) when [RCT](term_randomized_controlled_trial.md) is not available |

## Challenges and Limitations

### The "DiD Revolution" (2020-2023)

Recent econometric research revealed that the standard **Two-Way Fixed Effects (TWFE)** estimator — the workhorse of applied DiD — can produce severely biased estimates under two common conditions:

1. **Heterogeneous treatment effects**: When the treatment effect varies across units or over time, TWFE can assign negative weights to some group-time ATTs, producing estimates with the wrong sign
2. **Staggered adoption**: When units adopt treatment at different times, already-treated units serve as implicit controls for newly-treated units — contaminating the estimate

This led to a wave of new estimators (Callaway-Sant'Anna, Sun-Abraham, de Chaisemartin-D'Haultfoeuille, Goodman-Bacon decomposition) that provide valid estimates under these conditions.

### Practical Challenges

- **Parallel trends is untestable**: The assumption is about counterfactual outcomes that are never observed; pre-treatment trend tests provide suggestive but not definitive evidence
- **Finding good controls**: Requires a control group that would have evolved similarly to the treatment group absent treatment
- **Functional form**: DiD assumes the parallel trends hold in levels; if they hold in logs or other transformations, the level-based estimate is biased
- **Short pre-treatment periods**: Few pre-treatment observations make it difficult to assess parallel trends
- **Inference with few clusters**: Standard clustered errors require many clusters; few treated states/regions require wild cluster bootstrap or randomization inference

## Notable Implementations

| Software | Package | Features |
|----------|---------|----------|
| **R** | `did` (Callaway-Sant'Anna) | Group-time ATTs, aggregation, pre-testing |
| **R** | `fixest` | Fast TWFE, Sun-Abraham, cluster-robust SEs |
| **R** | `DIDmultiplegt` | de Chaisemartin-D'Haultfoeuille estimator |
| **R** | `bacondecomp` | Goodman-Bacon decomposition of TWFE |
| **Python** | `differences` | DiD estimation with multiple estimators |
| **Python** | `linearmodels` | Panel data models including TWFE |
| **Stata** | `did_multiplegt`, `csdid`, `eventstudyinteract` | Modern DiD estimators |

## Questions

### Validation (Socratic — "Why?")
1. The parallel trends assumption is untestable — pre-treatment trend tests are necessary but not sufficient. What additional evidence (placebo tests, falsification tests, bounding exercises) can strengthen the credibility of a DiD estimate?
   - **Tests**: Whether DiD results are robust beyond visual pre-trend inspection (WYSIATI)

2. The "DiD revolution" showed TWFE can be severely biased with staggered adoption — how many published DiD studies are potentially invalidated, and should we re-estimate all prior TWFE results with modern estimators?
   - **Tests**: Whether the TWFE bias is quantitatively important in practice (Devil's Advocate)

### Application (Taxonomic — "What If? / How?")
3. How would DiD be applied to evaluate the causal effect of a new abuse enforcement policy launched in one marketplace but not others — what would serve as the control group, and where would the parallel trends assumption be most vulnerable?
   - **Tests**: Domain applicability to abuse prevention (Adjacent Possible)

### Synthesis (Lateral — "Who Else?")
4. DiD and [PSM](term_propensity_score_matching.md) are often combined (match on propensity scores, then apply DiD to the matched sample). When does this combination outperform either method alone, and when does it introduce additional bias?
   - **Tests**: Complementarity between two causal inference methods (Liquid Network)

## Related Terms

- **[Causal Inference](term_causal_inference.md)**: The broader field DiD belongs to — estimating causal effects from data
- **[Propensity Score Matching](term_propensity_score_matching.md)**: Often combined with DiD to improve parallel trends; both are quasi-experimental methods
- **[Randomized Controlled Trial](term_randomized_controlled_trial.md)**: The gold standard that DiD approximates when randomization is infeasible
- **[Counterfactual Reasoning](term_counterfactual_reasoning.md)**: DiD constructs counterfactuals via the parallel trends assumption
- **[Structural Causal Model](term_structural_causal_model.md)**: Pearl's framework formalizes the causal assumptions underlying DiD
- **[Directed Acyclic Graph](term_directed_acyclic_graph.md)**: DAGs can represent the causal structure and identify when DiD assumptions hold
- **[DSI](term_dsi.md)**: Downstream Impact measurement — DiD is one method for estimating DSI when RCTs are unavailable
- **[Ladder of Causation](term_ladder_of_causation.md)**: DiD operates at rung 2 (intervention) — estimating $P(Y \mid do(X))$ from observational data
- **[Double Machine Learning](term_double_machine_learning.md)**: DML can be combined with DiD; handles high-dimensional confounders via Neyman orthogonality

## References

### Vault Sources

### External Sources
- [Card, D. & Krueger, A. (1994). "Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania." *American Economic Review*, 84(4): 772-793.](https://en.wikipedia.org/wiki/Difference_in_differences) — The canonical DiD study
- [Callaway, B. & Sant'Anna, P. (2021). "Difference-in-Differences with Multiple Time Periods." *Journal of Econometrics*, 225(2): 200-230.](https://bcallaway11.github.io/did/) — Modern staggered DiD framework
- [Goodman-Bacon, A. (2021). "Difference-in-Differences with Variation in Treatment Timing." *Journal of Econometrics*, 225(2): 254-277.](https://en.wikipedia.org/wiki/Difference_in_differences) — TWFE decomposition showing bias sources
- [Cunningham, S. (2021). *Causal Inference: The Mixtape*. Yale University Press. Chapter 9.](https://mixtape.scunning.com/09-difference_in_differences) — Comprehensive DiD tutorial
- [Wikipedia: Difference in Differences](https://en.wikipedia.org/wiki/Difference_in_differences)
- [Columbia Public Health: Difference-in-Difference Estimation](https://www.publichealth.columbia.edu/research/population-health-methods/difference-difference-estimation)
