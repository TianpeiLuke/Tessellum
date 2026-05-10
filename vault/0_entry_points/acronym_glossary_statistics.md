---
tags:
 - entry_point
 - index
 - navigation
 - quick_reference
 - glossary
 - causal_inference
 - statistics
 - experimentation
keywords:
 - causal inference
 - statistics
 - Judea Pearl
 - ladder of causation
 - counterfactual reasoning
 - structural causal model
 - DAG
 - do-calculus
 - confounding
 - Simpson's paradox
 - randomized controlled trial
 - A/B testing
 - mediation analysis
topics:
 - causal inference
 - statistics and probability
 - experimental design
 - measurement methodology
language: markdown
date of note: 2026-05-10
status: active
building_block: navigation
---

# Statistics, Causal Inference & Experimentation Glossary

**Purpose**: Quick reference for causal inference theory (Pearl's framework), statistical reasoning concepts, and experimentation tools used in research analytics and knowledge management. Covers both foundational theory and domain-specific applications.

**Navigation**: [← Back to Main Glossary](entry_acronym_glossary.md) | [Cognitive Science Glossary](acronym_glossary_cognitive_science.md) | [Machine Learning Glossary](acronym_glossary_ml.md)

---

## Causal Inference Theory (Pearl's Framework)

### Causal Inference
**Full Name**: Causal Inference (CI)
**Description**: A collection of statistical and machine learning methodologies that estimate the **causal effect** of an action, intervention, or treatment on an outcome — answering "what happens if we act?" rather than "what will happen?" Causal inference is applied across multiple domains: measuring policy impact, identifying false positives via uplift models, and optimizing treatment decisions through CATE estimation. The core challenge is the **fundamental problem of counterfactuals** — for each customer, only one treatment outcome is observed.
**Documentation**: [Causal Inference Term](../resources/term_dictionary/term_causal_inference.md)
**Source**: Pearl, J. (2000). *Causality*; Pearl, J. & Mackenzie, D. (2018). *The Book of Why*
**Related**: [Ladder of Causation](#ladder-of-causation), [Structural Causal Model](#structural-causal-model), [Counterfactual Reasoning](#counterfactual-reasoning)

### Ladder of Causation
**Full Name**: Ladder of Causation (Causal Hierarchy)
**Description**: Judea Pearl's three-rung hierarchy organizing causal reasoning: (1) **Association/Seeing** — observing correlations, P(Y|X); (2) **Intervention/Doing** — predicting effects of actions, P(Y|do(X)); (3) **Counterfactual/Imagining** — reasoning about alternatives, "What if X had not occurred?" Each rung requires qualitatively different reasoning that cannot be reduced to the rung below. Pearl argues current AI/ML operates entirely on rung 1.
**Documentation**: [Ladder of Causation Term](../resources/term_dictionary/term_ladder_of_causation.md)
**Source**: Pearl, J. & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*
**Related**: [Structural Causal Model](#structural-causal-model), [Counterfactual Reasoning](#counterfactual-reasoning), [Do-Calculus](#do-calculus)

### Structural Causal Model
**Full Name**: SCM — Structural Causal Model
**Description**: Pearl's mathematical framework consisting of (1) a set of variables, (2) structural equations defining each variable as a function of its direct causes plus an error term, and (3) a causal diagram (DAG). SCMs unify all three rungs of the ladder: they generate observational distributions (rung 1), predict interventional distributions via the do-operator (rung 2), and evaluate counterfactuals by modifying structural equations (rung 3).
**Documentation**: [Structural Causal Model Term](../resources/term_dictionary/term_structural_causal_model.md)
**Source**: Pearl, J. (2000). *Causality: Models, Reasoning, and Inference*
**Related**: [Directed Acyclic Graph](#directed-acyclic-graph), [Do-Calculus](#do-calculus), [Counterfactual Reasoning](#counterfactual-reasoning)

### Directed Acyclic Graph
→ **Moved to [Network Science Glossary](acronym_glossary_network_science.md#dag---directed-acyclic-graph)**. DAGs are a graph type; causal applications reference [Structural Causal Model](#structural-causal-model).

### Counterfactual Reasoning
**Full Name**: Counterfactual Reasoning
**Description**: The third rung of the ladder of causation — reasoning about what would have happened under alternative conditions ("What if I had acted differently?"). Evaluated via SCMs by modifying structural equations for a specific individual. Foundational for causal attribution, legal liability, medical decisions, and scientific explanation. Connects to Rubin's potential outcomes framework. Pearl argues that counterfactual reasoning is what separates human intelligence from current AI systems.
**Documentation**: [Counterfactual Reasoning Term](../resources/term_dictionary/term_counterfactual_reasoning.md)
**Source**: Pearl, J. & Mackenzie, D. (2018). *The Book of Why*, Chapter 8
**Related**: [Ladder of Causation](#ladder-of-causation), [Structural Causal Model](#structural-causal-model), [Causal Inference](#causal-inference)

### Do-Calculus
**Full Name**: Do-Calculus
**Description**: A set of three algebraic rules developed by Pearl (1995) that determine when a causal effect P(Y|do(X)) can be computed from observational data given a causal diagram. Includes two key special cases: the **back-door criterion** (control for confounders to block non-causal paths) and the **front-door criterion** (identify effects through mediators when confounders are unmeasured). Proven complete — can derive all identifiable causal effects.
**Documentation**: [Do-Calculus Term](../resources/term_dictionary/term_do_calculus.md)
**Source**: Pearl, J. (1995). "Causal Diagrams for Empirical Research." *Biometrika*, 82(4), 669–688
**Related**: [Structural Causal Model](#structural-causal-model), [Directed Acyclic Graph](#directed-acyclic-graph), [Confounding Variable](#confounding-variable), [Randomized Controlled Trial](#randomized-controlled-trial)

---

## Statistical Phenomena & Pitfalls

### Confounding Variable
**Full Name**: Confounding Variable (Confounder)
**Description**: A variable that causally influences both treatment and outcome, creating a spurious (non-causal) association between them. Cannot be identified from data alone — requires a causal model (DAG). Addressed by randomization (RCTs) or by Pearl's back-door criterion. Central to the smoking-cancer debate where Fisher argued that a genetic confounder could explain the correlation. Pearl's key insight: what counts as a confounder depends on the causal structure, not on statistical properties.
**Documentation**: [Confounding Variable Term](../resources/term_dictionary/term_confounding_variable.md)
**Source**: Pearl, J. & Mackenzie, D. (2018). *The Book of Why*, Chapter 4
**Related**: [Directed Acyclic Graph](#directed-acyclic-graph), [Randomized Controlled Trial](#randomized-controlled-trial), [Simpson's Paradox](#simpsons-paradox)

### Simpson's Paradox
**Full Name**: Simpson's Paradox (Simpson's Reversal)
**Description**: A statistical phenomenon where a trend that appears in several subgroups reverses when the subgroups are combined. Pearl argues this is a *causal*, not statistical, puzzle — resolution requires knowing whether the partitioning variable is a confounder (adjust for it) or a collider (do not adjust). Famously demonstrated in 1973 Berkeley admissions data where apparent gender discrimination reversed when analyzed by department.
**Documentation**: [Simpson's Paradox Term](../resources/term_dictionary/term_simpsons_paradox.md)
**Source**: Pearl, J. & Mackenzie, D. (2018). *The Book of Why*, Chapter 6
**Related**: [Confounding Variable](#confounding-variable), [Directed Acyclic Graph](#directed-acyclic-graph), [Collider Bias](#collider-bias)

### Collider Bias
**Full Name**: Collider Bias (Selection Bias, Berkson's Paradox)
**Description**: A form of selection bias that occurs when conditioning on (controlling for) a common *effect* of two independent causes, creating a spurious association between them. One of the three basic junction types in causal diagrams (A→B←C). Explains Berkson's paradox, the Monty Hall problem, and many forms of selection bias in observational studies. Counterintuitive: while controlling for confounders removes bias, controlling for colliders *introduces* bias.
**Documentation**: [Collider Bias Term](../resources/term_dictionary/term_collider_bias.md)
**Source**: Pearl, J. & Mackenzie, D. (2018). *The Book of Why*, Chapter 6
**Related**: [Directed Acyclic Graph](#directed-acyclic-graph), [Confounding Variable](#confounding-variable), [Simpson's Paradox](#simpsons-paradox)

### Mediation Analysis
**Full Name**: Mediation Analysis (Causal Mediation)
**Description**: The study of *how* a cause produces its effect, decomposing total effects into **direct effects** (not through the mediator) and **indirect effects** (through the mediator). Pearl's Natural Direct/Indirect Effects (NDE/NIE) use counterfactual definitions that work for nonlinear systems, unlike Baron & Kenny's traditional regression approach. Critical insight: NDE + NIE ≠ Total Effect in general, reflecting genuine causal complexity.
**Documentation**: [Mediation Analysis Term](../resources/term_dictionary/term_mediation_analysis.md)
**Source**: Pearl, J. & Mackenzie, D. (2018). *The Book of Why*, Chapter 9
**Related**: [Structural Causal Model](#structural-causal-model), [Counterfactual Reasoning](#counterfactual-reasoning), [Directed Acyclic Graph](#directed-acyclic-graph)

### Semiparametric Model
**Full Name**: Semiparametric Model (Semiparametric Estimation)
**Description**: A statistical model combining a finite-dimensional parametric component (parameters of interest) with an infinite-dimensional nonparametric component (nuisance functions left unspecified). **Occupies the middle ground between parametric (fully specified, potentially misspecified) and nonparametric (minimal assumptions, statistically harder) models**. The infinite-dimensional component is treated as a nuisance — estimated or eliminated but not itself the target. Key examples include the Cox Proportional Hazards model (survival analysis) and the partially linear model (causal inference). Modern semiparametric methods like DML achieve $\sqrt{n}$-consistency for the target parameter while using ML to estimate nuisance functions.
**Documentation**: [Semiparametric Model](../resources/term_dictionary/term_semiparametric_model.md)
**Related**: [DML](#dml---double-machine-learning), [Causal Inference](#causal-inference), [PSM](#psm---propensity-score-matching)

### DML - Double Machine Learning
**Full Name**: DML — Double/Debiased Machine Learning
**Description**: A semiparametric framework for estimating causal treatment effects that combines modern ML with econometric rigor. DML solves the problem that **naively plugging ML predictions into causal estimating equations produces biased estimates due to regularization bias and overfitting**. Two key ingredients: Neyman orthogonality (scores insensitive to first-order nuisance estimation errors) and cross-fitting (sample splitting to prevent overfitting). Achieves $\sqrt{n}$-consistency for the causal parameter while allowing any ML method (random forests, neural nets, boosting) to estimate nuisance functions.
**Documentation**: [Double Machine Learning](../resources/term_dictionary/term_double_machine_learning.md)
**Source**: Chernozhukov, V. et al. (2018). "Double/Debiased Machine Learning for Treatment and Structural Parameters." *The Econometrics Journal*, 21(1): C1-C68.
**Related**: [Causal Inference](#causal-inference), [PSM](#psm---propensity-score-matching), [DiD](#did---difference-in-differences)

### DiD - Difference-in-Differences
**Full Name**: DiD — Difference-in-Differences
**Description**: A quasi-experimental statistical technique that estimates causal treatment effects by comparing the change in outcomes over time between a treatment group and a control group. DiD **removes time-invariant confounders through double differencing** — the first difference removes group-level fixed effects, the second removes common time trends. The critical identifying assumption is parallel trends: absent treatment, both groups would have followed the same trajectory. Recent methodological advances (Callaway-Sant'Anna 2021, Goodman-Bacon 2021) revealed that standard two-way fixed effects (TWFE) estimators can be biased with staggered treatment adoption and heterogeneous effects.
**Documentation**: [Difference-in-Differences](../resources/term_dictionary/term_difference_in_differences.md)
**Source**: Card, D. & Krueger, A. (1994). "Minimum Wages and Employment." *AER*; Ashenfelter & Card (1984) coined the term.
**Related**: [Causal Inference](#causal-inference), [PSM](#psm---propensity-score-matching), [Randomized Controlled Trial](#randomized-controlled-trial)

### PSM - Propensity Score Matching
**Full Name**: PSM — Propensity Score Matching
**Description**: A statistical technique for estimating causal treatment effects from observational data by matching treated and control units with similar propensity scores — the conditional probability of receiving treatment given observed covariates. PSM **reduces confounding bias by collapsing high-dimensional covariate adjustment into a single scalar score**, mimicking randomization without random assignment. Four main approaches exist: matching, stratification, inverse probability weighting (IPTW), and covariate adjustment. Rosenbaum and Rubin (1983) proved that if treatment is strongly ignorable given covariates, it remains ignorable given the propensity score alone.
**Documentation**: [Propensity Score Matching](../resources/term_dictionary/term_propensity_score_matching.md)
**Source**: Rosenbaum, P.R. & Rubin, D.B. (1983). "The Central Role of the Propensity Score in Observational Studies for Causal Effects." *Biometrika*, 70(1): 41-55.
**Related**: [Causal Inference](#causal-inference), [Randomized Controlled Trial](#randomized-controlled-trial), [Counterfactual Reasoning](#counterfactual-reasoning), [IPW](#ipw---inverse-probability-weighting)

### IPW - Inverse Probability Weighting
**Full Name**: IPW (also IPTW — Inverse Probability of Treatment Weighting)
**Description**: A statistical technique for estimating causal treatment effects from observational data by reweighting observations by the inverse of their propensity score, constructing a pseudo-population where treatment assignment is independent of measured confounders. **Each treated unit gets weight 1/e(X) and each control gets weight 1/(1-e(X))** — upweighting underrepresented portions of covariate space to mimic randomization. The ATE is estimated as the weighted mean outcome difference between groups (Horvitz-Thompson estimator). IPW is sensitive to extreme propensities (weights blow up when e(X) is near 0 or 1) — common stabilizations include weight trimming and stabilized weights. Often combined with outcome regression in doubly robust estimators (AIPW) which remain consistent if either the propensity model OR the outcome model is correctly specified.
**Documentation**: [Inverse Probability Weighting](../resources/term_dictionary/term_ipw.md)
**Source**: Horvitz, D.G. & Thompson, D.J. (1952). "A Generalization of Sampling Without Replacement from a Finite Universe." *JASA*, 47(260): 663-685; Robins, J.M., Hernán, M.A. & Brumback, B. (2000). "Marginal Structural Models and Causal Inference in Epidemiology." *Epidemiology*, 11(5): 550-560.
**Related**: [PSM](#psm---propensity-score-matching), [Causal Inference](#causal-inference), [DML](#dml---double-machine-learning), [Counterfactual Reasoning](#counterfactual-reasoning)

---

## Probability & Bayesian Inference

### Bayesian Reasoning
**Full Name**: Bayesian Reasoning (Bayesian Inference / Probability Updating)
**Description**: Framework for updating beliefs in light of new evidence using **Bayes's rule**: `P(hypothesis | evidence) ∝ P(evidence | hypothesis) × P(hypothesis)`. The **prior** encodes pre-existing knowledge (base rates); the **likelihood** measures how well the hypothesis explains evidence; the **posterior** is the updated belief. Central insight: the prior matters enormously — with sparse evidence, base rates dominate; with abundant evidence, data overwhelms the prior. Christian & Griffiths show humans are good Bayesian reasoners when they have correct priors; most prediction errors stem from **wrong priors (base-rate neglect)**, not flawed reasoning. The distribution-prediction table maps phenomena to prediction rules: normal → predict the average; power law → predict continuation; memoryless → [Lindy effect](../resources/term_dictionary/term_lindy_effect.md).
**Documentation**: [Bayesian Reasoning Term](../resources/term_dictionary/term_bayesian_reasoning.md)
**Source**: Christian, B. & Griffiths, T. (2016). *Algorithms to Live By*, Chapter 6; Bayes, T. (1763)
**Related**: [Causal Inference](#causal-inference), [Confounding Variable](#confounding-variable), [Counterfactual Reasoning](#counterfactual-reasoning)

### Beta-Binomial Model
**Full Name**: Beta-Binomial Model (Bayesian Conjugate Model for Count Data)
**Description**: Bayesian model combining a Beta prior on success probability with Binomial likelihood, yielding a closed-form Beta posterior. **Key property: Bayesian shrinkage — when sample size is small, estimates are pulled toward the population mean, biasing in favor of uncertainty.** Captures overdispersion via intra-class correlation $\rho = 1/(\alpha+\beta+1)$. In one application context, models customer return rates where each customer has an unknown "true" rate estimated from sparse observations. Extended to zero-inflated (hurdle) variant for the ~80% of customers with zero returns. Also used in A/B testing, clinical trials, and sports analytics.
**Documentation**: [Beta-Binomial Model Term](../resources/term_dictionary/term_beta_binomial_model.md)
**Related**: [Bayesian Reasoning](#bayesian-reasoning)

### Conjugate Prior
**Full Name**: Conjugate Prior (Bayesian Conjugacy)
**Description**: A prior distribution is conjugate to a likelihood if the posterior has the same parametric form as the prior, enabling closed-form Bayesian inference without MCMC. **Key pairs: Beta-Binomial, Dirichlet-Multinomial, Normal-Normal, Gamma-Poisson.** Hyperparameters have pseudo-count interpretation — Beta(a,b) prior is equivalent to having observed a successes and b failures before seeing data. Foundation of the application return rate estimation.
**Documentation**: [Conjugate Prior Term](../resources/term_dictionary/term_conjugate_prior.md)
**Related**: [Beta Distribution](#beta-distribution), [Bayesian Reasoning](#bayesian-reasoning), [Dirichlet Distribution](#dirichlet-distribution)

### Multinomial Distribution
**Full Name**: Multinomial Distribution — Mult(n, p₁,...,pₖ)
**Description**: Generalization of the Binomial to k > 2 categories. Models counts of outcomes in n independent trials where each trial has k possible outcomes. **The Dirichlet distribution is its conjugate prior**, just as Beta is conjugate for Binomial. Used in text classification (word counts), topic modeling (LDA), and customer segmentation.
**Documentation**: [Multinomial Distribution Term](../resources/term_dictionary/term_multinomial_distribution.md)
**Related**: [Binomial Distribution](#binomial-distribution), [Dirichlet Distribution](#dirichlet-distribution), [Conjugate Prior](#conjugate-prior)

### Dirichlet Distribution
**Full Name**: Dirichlet Distribution — Dir(α₁,...,αₖ)
**Description**: Multivariate generalization of the Beta distribution — a distribution over probability vectors on the simplex. Named after Peter Gustav Lejeune Dirichlet (1805-1859). **Conjugate prior for the Multinomial likelihood.** Concentration parameter α₀ = Σαᵢ controls spread: uniform when all αᵢ = 1, sparse when αᵢ < 1. Foundation of LDA topic modeling (Blei et al., 2003). Reduces to Beta when k = 2.
**Documentation**: [Dirichlet Distribution Term](../resources/term_dictionary/term_dirichlet_distribution.md)
**Related**: [Beta Distribution](#beta-distribution), [Multinomial Distribution](#multinomial-distribution), [Conjugate Prior](#conjugate-prior)

### CDF Transform
**Full Name**: CDF Transform (Probability Integral Transform)
**Description**: Maps a random variable through its own CDF to produce a Uniform(0,1) variable; the inverse maps back. **In one application context, normalizes return rates across categories: $T_{\alpha,\beta}(x) = I_{1.5,4}^{-1}(I_{\alpha,\beta}(x))$ maps any Beta(α,β) to a common Beta(1.5,4) reference.** Also used in copula modeling, random variate generation, and goodness-of-fit testing (Kolmogorov-Smirnov).
**Documentation**: [CDF Transform Term](../resources/term_dictionary/term_cdf_transform.md)
**Related**: [Beta Distribution](#beta-distribution), [Beta-Binomial Model](#beta-binomial-model)

### Bayesian Inference
**Full Name**: Bayesian Inference
**Description**: Statistical framework updating probability estimates as new evidence is observed via Bayes' theorem. In, used for A/B testing, Thompson sampling (explore-exploit), model calibration, and uncertainty quantification. **Produces probability distributions rather than point estimates**, naturally handling sequential data.
**Documentation**: [Bayesian Term](../resources/term_dictionary/term_bayesian.md)
**Related**: [FPR](../resources/term_dictionary/term_fpr.md), [Precision](../resources/term_dictionary/term_precision.md)

### FPR - False Positive Rate
**Full Name**: False Positive Rate (Type I Error Rate)
**Documentation**: [FPR Term](../resources/term_dictionary/term_fpr.md)
**Related**: [Precision](../resources/term_dictionary/term_precision.md), [PFOC](../resources/term_dictionary/term_pfoc.md)

### Exponential Family
**Full Name**: Exponential Family of Distributions
**Description**: Family of distributions whose PDF/PMF has the form $f(x|\theta) = h(x)\exp[\eta(\theta) \cdot T(x) - A(\theta)]$. **Includes Normal, Binomial, Poisson, Beta, Gamma, Dirichlet, Multinomial — unifying all our stats terms.** Key property: conjugate priors always exist for exponential family members. Log-partition function $A(\theta)$ generates all moments. Foundation of GLMs (logistic regression = Binomial + logit link).
**Documentation**: [Exponential Family Term](../resources/term_dictionary/term_exponential_family.md)
**Related**: [Beta Distribution](#beta-distribution), [Binomial Distribution](#binomial-distribution), [Conjugate Prior](#conjugate-prior)

### Quantile
**Full Name**: Quantile (Percentile, Quartile)
**Description**: The q-th quantile is the value x where $P(X \leq x) = q$ — the inverse CDF. Special cases: median (q=0.5), quartiles, percentiles. **In one application context, percentiles of the prior distribution define "excessive" return rate thresholds (e.g., 95th percentile).** Also used in P50/P90/P99 SLAs and VaR risk metrics.
**Documentation**: [Quantile Term](../resources/term_dictionary/term_quantile.md)
**Related**: [CDF Transform](#cdf-transform), [Beta Distribution](#beta-distribution)

### Quantile Regression
**Full Name**: Quantile Regression (Koenker & Bassett, 1978)
**Description**: Estimates conditional quantiles of the response (not just the mean). Minimizes asymmetric check loss $\rho_\tau(u) = u(\tau - \mathbf{1}_{\{u<0\}})$. **Unlike OLS which estimates E[Y|X], QR estimates $Q_\tau(Y|X)$ for any quantile τ.** Robust to outliers, handles heteroscedasticity, reveals distributional effects. Relevant to modeling tails of return rate distributions.
**Documentation**: [Quantile Regression Term](../resources/term_dictionary/term_quantile_regression.md)
**Related**: [Quantile](#quantile), [Linear Regression](#linear-regression), [Least Squares](#least-squares-estimation)

### Linear Regression
**Full Name**: Linear Regression (OLS)
**Description**: Models $y = X\beta + \epsilon$, estimated via OLS (minimize squared residuals) or MLE (Gaussian errors). **Closed-form solution: $\hat{\beta} = (X'X)^{-1}X'y$.** Gauss-Markov theorem: OLS is BLUE (Best Linear Unbiased Estimator). Foundation for logistic regression (GLM with logit link) and all regression-based ML.
**Documentation**: [Linear Regression Term](../resources/term_dictionary/term_linear_regression.md)
**Related**: [Least Squares](#least-squares-estimation), [Logistic Regression](acronym_glossary_ml.md#logistic-regression), [Quantile Regression](#quantile-regression)

### Least Squares Estimation
**Full Name**: Least Squares (OLS, Gauss-Legendre Method)
**Description**: Minimizes $\sum(y_i - x_i'\beta)^2$. Independently discovered by Gauss (1795) and Legendre (1805). **Variants: OLS, weighted (WLS), generalized (GLS), regularized (Ridge = L2, Lasso = L1).** Equivalent to MLE under Gaussian errors. Sensitive to outliers — quantile regression is the robust alternative.
**Documentation**: [Least Squares Term](../resources/term_dictionary/term_least_squares.md)
**Related**: [Linear Regression](#linear-regression), [Quantile Regression](#quantile-regression), [Exponential Family](#exponential-family)

### Clopper-Pearson Method
**Full Name**: Clopper-Pearson Exact Binomial Confidence Interval (1934)
**Description**: Exact CI for a binomial proportion: $[B(\alpha/2; k, n-k+1), B(1-\alpha/2; k+1, n-k)]$ where B is the Beta quantile. **Guarantees at least $1-\alpha$ coverage (conservative).** In one application context, compared against Bayesian beta-binomial — Bayesian chosen because it uses population prior, shrinks uncertain estimates, and biases in customer's favor at low n.
**Documentation**: [Clopper-Pearson Term](../resources/term_dictionary/term_clopper_pearson.md)
**Related**: [Binomial Distribution](#binomial-distribution), [Beta Distribution](#beta-distribution), [Beta-Binomial Model](#beta-binomial-model)

### Normal Distribution
**Full Name**: Normal (Gaussian) Distribution — $N(\mu, \sigma^2)$
**Description**: Bell curve with PDF $f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/2\sigma^2}$. **Central Limit Theorem: sum of iid RVs → normal.** Exponential family member. Conjugate prior for normal likelihood. Maximum entropy for given mean+variance. Foundation of linear regression (Gaussian errors), Ridge regression (Gaussian prior), and most of classical statistics.
**Documentation**: [Normal Distribution Term](../resources/term_dictionary/term_normal_distribution.md)
**Related**: [Exponential Family](#exponential-family), [Linear Regression](#linear-regression), [Conjugate Prior](#conjugate-prior)

### Gamma Distribution
**Full Name**: Gamma Distribution — $\text{Gamma}(\alpha, \beta)$
**Description**: Continuous distribution on $(0, \infty)$. **Conjugate prior for Poisson rate parameter.** Exponential family member. Special cases: Exponential ($\alpha=1$), Chi-squared ($\alpha=k/2, \beta=1/2$). Mean $= \alpha/\beta$. Used for waiting times, rate estimation, and as prior in Bayesian models.
**Documentation**: [Gamma Distribution Term](../resources/term_dictionary/term_gamma_distribution.md)
**Related**: [Exponential Family](#exponential-family), [Conjugate Prior](#conjugate-prior), [Normal Distribution](#normal-distribution)

### Pareto Distribution
**Full Name**: Pareto Distribution (Power Law)
**Description**: Heavy-tailed distribution with $P(X > x) \sim x^{-\alpha}$. **NOT an exponential family member** (support depends on parameter $x_m$). Infinite variance when $\alpha \leq 2$, infinite mean when $\alpha \leq 1$. Models extreme values: wealth distribution, city sizes, insurance claims. In anomaly detection, extreme return rates follow power law tails.
**Documentation**: [Pareto Distribution Term](../resources/term_dictionary/term_pareto_distribution.md)
**Related**: [Fat Tails](../resources/term_dictionary/term_fat_tails.md), [Normal Distribution](#normal-distribution) (contrast: thin vs fat tails)

### Confidence Interval
**Full Name**: Confidence Interval (Frequentist CI)
**Description**: Range $[\hat{\theta} \pm z_{\alpha/2} \cdot SE]$ containing the true parameter with probability $1-\alpha$ over repeated sampling. **NOT the probability the parameter is in the interval** (that's Bayesian credible interval). In one application context, credible intervals chosen over CIs because they incorporate prior information. Clopper-Pearson provides exact binomial CIs.
**Documentation**: [Confidence Interval Term](../resources/term_dictionary/term_confidence_interval.md)
**Related**: [Clopper-Pearson](#clopper-pearson-method), [Normal Distribution](#normal-distribution), [Beta-Binomial Model](#beta-binomial-model)

### LASSO
**Full Name**: LASSO — Least Absolute Shrinkage and Selection Operator (Tibshirani, 1996)
**Description**: L1-regularized regression: $\min_\beta \|y - X\beta\|_2^2 + \lambda\|\beta\|_1$. **Key property: L1 penalty induces SPARSITY — drives coefficients exactly to zero, performing automatic feature selection.** Contrast with Ridge (L2) which shrinks but doesn't zero out. Elastic Net combines L1+L2. Foundation for GraphLasso (sparse precision matrix estimation).
**Documentation**: [LASSO Term](../resources/term_dictionary/term_lasso.md)
**Related**: [Ridge Regression](#ridge-regression), [Least Squares](#least-squares-estimation), [GraphLasso](#graphlasso)

### Ridge Regression
**Full Name**: Ridge Regression (L2 Regularization / Tikhonov / RLS / Weight Decay)
**Description**: L2-regularized regression: $\min_\beta \|y - X\beta\|_2^2 + \lambda\|\beta\|_2^2$. **Closed-form: $\hat{\beta} = (X^TX + \lambda I)^{-1}X^Ty$.** Shrinks ALL coefficients toward zero but never exactly zero. Bayesian interpretation: MAP estimation with Gaussian prior on coefficients. Handles multicollinearity.
**Documentation**: [Ridge Regression Term](../resources/term_dictionary/term_ridge_regression.md)
**Related**: [LASSO](#lasso), [Least Squares](#least-squares-estimation), [Normal Distribution](#normal-distribution) (Gaussian prior)

### GraphLasso
**Full Name**: Graphical LASSO (Sparse Precision Matrix Estimation)
**Description**: Estimates sparse inverse covariance matrix via L1-penalized Gaussian log-likelihood: $\max_\Theta \log\det\Theta - \text{tr}(S\Theta) - \lambda\|\Theta\|_1$. **Non-zero entries in $\Theta$ = conditional dependencies = graph edges.** Applications: gene networks, brain connectivity, financial networks, graph anomaly detection (customer interaction graphs).
**Documentation**: [GraphLasso Term](../resources/term_dictionary/term_graphlasso.md)
**Related**: [LASSO](#lasso), [Normal Distribution](#normal-distribution), [Concentration Inequality](#concentration-inequalities)

### Concentration Inequalities
**Full Name**: Concentration Inequalities (Tail Bounds)
**Description**: Bounds on $P(|X - E[X]| \geq t)$. **Key inequalities: Hoeffding (bounded RVs, exponential tail), Bernstein (uses variance, tighter), McDiarmid (bounded differences), Chernoff (MGF-based).** Foundation for: LASSO consistency, GraphLasso convergence, UCB bandit bounds, sample size calculations, conformal prediction coverage guarantees.
**Documentation**: [Concentration Inequality Term](../resources/term_dictionary/term_concentration_inequality.md)
**Related**: [LASSO](#lasso), [GraphLasso](#graphlasso), [Confidence Interval](#confidence-interval), [Normal Distribution](#normal-distribution)

### Elastic Net
**Full Name**: Elastic Net (L1 + L2 Regularization, Zou & Hastie 2005)
**Description**: Combines LASSO (L1) and Ridge (L2) penalties: $\min_\beta \|y-X\beta\|_2^2 + \lambda_1\|\beta\|_1 + \lambda_2\|\beta\|_2^2$. **Overcomes LASSO limitations: handles correlated features via grouped selection, selects >n variables when p>n.** Mixing parameter $\alpha$ controls L1/L2 balance.
**Documentation**: [Elastic Net Term](../resources/term_dictionary/term_elastic_net.md)
**Related**: [LASSO](#lasso), [Ridge Regression](#ridge-regression), [Least Squares](#least-squares-estimation)

### Chi-Squared Distribution
**Full Name**: Chi-Squared Distribution — $\chi^2_k$
**Description**: Sum of $k$ squared standard normals. **Special case of $\text{Gamma}(k/2, 1/2)$.** Mean $= k$, variance $= 2k$. Foundation of: Pearson's goodness-of-fit test, independence tests, variance estimation, likelihood ratio tests.
**Documentation**: [Chi-Squared Distribution Term](../resources/term_dictionary/term_chi_squared_distribution.md)
**Related**: [Normal Distribution](#normal-distribution), [Gamma Distribution](#gamma-distribution), [Confidence Interval](#confidence-interval)

### Poisson Distribution
**Full Name**: Poisson Distribution — $\text{Pois}(\lambda)$
**Description**: Discrete distribution for count data: $P(X=k) = \lambda^k e^{-\lambda}/k!$. **Mean = variance = $\lambda$ (equidispersion).** Exponential family member. Conjugate prior: Gamma. Limit of Binomial for large $n$, small $p$. Models event counts: queue theory, insurance claims, event frequency.
**Documentation**: [Poisson Distribution Term](../resources/term_dictionary/term_poisson_distribution.md)
**Related**: [Gamma Distribution](#gamma-distribution), [Binomial Distribution](#binomial-distribution), [Exponential Family](#exponential-family)

### Hoeffding's Inequality
**Full Name**: Hoeffding's Inequality (1963)
**Description**: For bounded iid RVs $X_i \in [a_i, b_i]$: $P(|\bar{X} - E[\bar{X}]| \geq t) \leq 2\exp(-2n^2t^2/\sum(b_i-a_i)^2)$. **Exponential tail decay without using variance info.** Bernstein is tighter when variance is small.
**Documentation**: [Hoeffding's Inequality Term](../resources/term_dictionary/term_hoeffding_inequality.md)
**Related**: [Concentration Inequalities](#concentration-inequalities), [Bernstein's Inequality](#bernsteins-inequality)

### Bernstein's Inequality
**Full Name**: Bernstein's Inequality (Variance-Sensitive Bound)
**Description**: For bounded RVs with variance $\sigma^2$: $P(|\bar{X}-E[\bar{X}]| \geq t) \leq 2\exp(-nt^2/(2\sigma^2 + 2Mt/3))$. **Tighter than Hoeffding when variance is small.** Interpolates between Gaussian tail (small $t$) and exponential tail (large $t$).
**Documentation**: [Bernstein's Inequality Term](../resources/term_dictionary/term_bernstein_inequality.md)
**Related**: [Concentration Inequalities](#concentration-inequalities), [Hoeffding's Inequality](#hoeffdings-inequality)

### Chernoff Bound
**Full Name**: Chernoff Bound (MGF Method)
**Description**: Generic MGF-based bound: $P(X \geq t) \leq \inf_{s>0} e^{-st}E[e^{sX}]$. **The tightest exponential bound from the MGF.** Hoeffding and Bernstein are special cases. Multiplicative form for Binomial is widely used in randomized algorithms.
**Documentation**: [Chernoff Bound Term](../resources/term_dictionary/term_chernoff_bound.md)
**Related**: [Concentration Inequalities](#concentration-inequalities), [Binomial Distribution](#binomial-distribution)

### Bounded Differences Inequality
**Full Name**: McDiarmid's Inequality (Bounded Differences, 1989)
**Description**: For $f(X_1,...,X_n)$ where changing any $X_i$ changes $f$ by at most $c_i$: $P(|f-E[f]| \geq t) \leq 2\exp(-2t^2/\sum c_i^2)$. **Generalizes Hoeffding to functions of independent RVs.** Key tool for ML generalization bounds.
**Documentation**: [Bounded Differences Term](../resources/term_dictionary/term_bounded_differences_inequality.md)
**Related**: [Concentration Inequalities](#concentration-inequalities), [Hoeffding's Inequality](#hoeffdings-inequality)

### Tikhonov Regularization
**Full Name**: Tikhonov Regularization (General L2 Penalty for Inverse Problems)
**Description**: $\min_x \|Ax-b\|_2^2 + \lambda\|\Gamma x\|_2^2$. **When $\Gamma = I$, this is Ridge regression.** Named after Andrey Tikhonov (1943). Stabilizes ill-conditioned problems. Bayesian interpretation: Gaussian prior. L-curve method for choosing $\lambda$.
**Documentation**: [Tikhonov Regularization Term](../resources/term_dictionary/term_tikhonov_regularization.md)
**Related**: [Ridge Regression](#ridge-regression), [LASSO](#lasso), [Least Squares](#least-squares-estimation)

### Precision Matrix
**Full Name**: Precision Matrix (Inverse Covariance / Concentration Matrix)
**Description**: $\Theta = \Sigma^{-1}$. **$\Theta_{ij} = 0$ iff $X_i \perp X_j | \text{rest}$ (conditional independence for Gaussian data).** Sparse precision = sparse graph. Estimated by GraphLasso. Partial correlation: $\rho_{ij|\text{rest}} = -\Theta_{ij}/\sqrt{\Theta_{ii}\Theta_{jj}}$.
**Documentation**: [Precision Matrix Term](../resources/term_dictionary/term_precision_matrix.md)
**Related**: [GraphLasso](#graphlasso), [Normal Distribution](#normal-distribution)

---

## Experimental Design & Measurement

### Randomized Controlled Trial
**Full Name**: RCT — Randomized Controlled Trial
**Description**: Experimental design that randomly assigns treatments to break confounding associations, considered the "gold standard" for causal inference. Pearl shows RCTs are one tool in the causal toolkit — not the only path to causal knowledge. Observational data combined with causal models can sometimes yield equally valid causal conclusions, especially when RCTs are impossible or unethical. RCTs work by physically intervening to set treatment assignment, making P(Y|do(X)) directly observable.
**Documentation**: [Randomized Controlled Trial Term](../resources/term_dictionary/term_randomized_controlled_trial.md)
**Source**: Pearl, J. & Mackenzie, D. (2018). *The Book of Why*, Chapters 4–5
**Related**: [Confounding Variable](#confounding-variable), [Do-Calculus](#do-calculus)

---

## Statistical Distributions & Power Laws

### Exponential Distribution
**Full Name**: Exponential Distribution — $\text{Exp}(\lambda)$
**Description**: Continuous distribution for waiting times: $f(x) = \lambda e^{-\lambda x}$. **The ONLY continuous memoryless distribution**: $P(X > s+t | X > s) = P(X > t)$. Special case of $\text{Gamma}(1, \lambda)$. Exponential family member. Inter-arrival times of Poisson process. Constant hazard rate. Mean $= 1/\lambda$.
**Documentation**: [Exponential Distribution Term](../resources/term_dictionary/term_exponential_distribution.md)
**Related**: [Gamma Distribution](#gamma-distribution), [Poisson Distribution](#poisson-distribution), [Exponential Family](#exponential-family)

### Sub-Gaussian Random Variables
**Full Name**: Sub-Gaussian (Light-Tailed Distributional Class)
**Description**: RV $X$ is sub-Gaussian with parameter $\sigma$ if $E[e^{s(X-EX)}] \leq e^{s^2\sigma^2/2}$. **Tails decay at least as fast as Gaussian.** Includes: bounded RVs, Gaussian, Bernoulli. Key class for concentration inequalities — Hoeffding's inequality applies to sub-Gaussians. Sub-exponential is the next heavier class.
**Documentation**: [Sub-Gaussian Term](../resources/term_dictionary/term_sub_gaussian.md)
**Related**: [Concentration Inequalities](#concentration-inequalities), [Hoeffding's Inequality](#hoeffdings-inequality), [Normal Distribution](#normal-distribution)

### Fat Tails
*Moved to [Network Science Glossary](acronym_glossary_network_science.md#fat-tails)* — fat-tailed distributions describe network degree distributions and are foundational to network science.
**Documentation**: [Fat Tails Term](../resources/term_dictionary/term_fat_tails.md)

### Power Law
*Moved to [Network Science Glossary](acronym_glossary_network_science.md#power-law)* — power law distributions are the signature of scale-free networks.
**Documentation**: [Power Law Term](../resources/term_dictionary/term_power_law.md)

### Zipf's Law
*Moved to [Network Science Glossary](acronym_glossary_network_science.md#zipfs-law)* — the discrete rank-frequency form of a power law, appearing in network degree distributions.
**Documentation**: [Zipf's Law Term](../resources/term_dictionary/term_zipfs_law.md)

### Mediocristan and Extremistan
**Full Name**: Mediocristan and Extremistan
**Description**: Two conceptual realms of randomness coined by Nassim Nicholas Taleb in *The Black Swan* (2007). **Mediocristan** is the domain of thin-tailed, non-scalable randomness where no single observation significantly changes the aggregate (e.g., height, weight); the Gaussian distribution applies and standard statistics work reliably. **Extremistan** is the domain of fat-tailed, scalable randomness where **a single observation can dominate the entire aggregate** (e.g., wealth, book sales, war casualties); power-law distributions govern and standard Gaussian tools fail catastrophically. Taleb extended this into the Fourth Quadrant framework, crossing distribution type with payoff complexity to identify the "danger zone" where statistics is most unreliable.
**Documentation**: [Mediocristan and Extremistan Term](../resources/term_dictionary/term_mediocristan_and_extremistan.md)
**Source**: Taleb, N. N. (2007). *The Black Swan*; Taleb, N. N. (2008). "The Fourth Quadrant" (Edge.org)
**Related**: [Black Swan](acronym_glossary_cognitive_science.md#black-swan), [Power Law](acronym_glossary_network_science.md#power-law), [Zipf's Law](acronym_glossary_network_science.md#zipfs-law), [Pareto Principle](acronym_glossary_cognitive_science.md#pareto-principle-8020-rule)

### Tail Risk
**Full Name**: Tail Risk
**Description**: The risk of rare, extreme outcomes residing in the tails of a probability distribution — specifically, the risk of an asset or portfolio moving more than three standard deviations from its current price. Real-world financial distributions exhibit **fat tails (excess kurtosis)**, meaning extreme events occur far more frequently than Gaussian models predict. Central to Nassim Taleb's critique of Value-at-Risk (VaR) and modern risk management, tail risk bridges Frank Knight's distinction between measurable risk and unmeasurable uncertainty. Tail risk hedging strategies (deep OTM puts, tail risk parity) aim to protect portfolios against catastrophic losses at a manageable cost.
**Documentation**: [Tail Risk Term](../resources/term_dictionary/term_tail_risk.md)
**Related**: [Black Swan](acronym_glossary_cognitive_science.md#black-swan), [Power Law](acronym_glossary_network_science.md#power-law), [Mediocristan and Extremistan](#mediocristan-and-extremistan)

---

## Cross-Reference: Theory to Practice

| Theoretical Concept | domain Application | How It's Used |
|---------------------|-----------------|---------------|
| [Collider Bias](#collider-bias) | Investigation selection effects | Conditioning on "investigated customers" creates spurious risk factor correlations |
| [Do-Calculus](#do-calculus) | Observational causal studies | Deriving policy decisions from historical data without new experiments |

---

## Related Entry Points

- [Cognitive Science & Decision Frameworks Glossary](acronym_glossary_cognitive_science.md) — cognitive biases, learning science, decision frameworks
- [Machine Learning Glossary](acronym_glossary_ml.md) — ML algorithms, deep learning, uplift models

---

## References

- Pearl, J. & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*. Basic Books.
- Pearl, J. (2000). *Causality: Models, Reasoning, and Inference* (2nd ed. 2009). Cambridge University Press.
- Pearl, J. (1995). "Causal Diagrams for Empirical Research." *Biometrika*, 82(4), 669–688.
- Künzel, S. et al. (2019). "Metalearners for estimating heterogeneous treatment effects using machine learning." *PNAS*, 116(10), 4156–4165.
- [Digest: The Book of Why](../resources/digest/digest_book_of_why_pearl.md) — vault digest of Pearl's framework

---

**Last Updated**: March 7, 2026
**Status**: Active — Statistics, causal inference, and experimentation glossary
**Maintenance**: Update when new causal inference or experimentation terms are added to the vault
