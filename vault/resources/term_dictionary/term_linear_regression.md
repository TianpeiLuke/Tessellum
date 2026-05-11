---
tags:
  - resource
  - terminology
  - statistics
  - machine_learning
  - regression
keywords:
  - linear regression
  - OLS
  - ordinary least squares
  - regression coefficients
  - R-squared
  - residuals
  - normal equations
  - gradient descent
topics:
  - statistical modeling
  - machine learning
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Linear Regression

## Definition

Linear regression models the relationship between a dependent variable $y$ and one or more independent variables $X$ as:

$$y = X\beta + \epsilon$$

where $\beta$ is the vector of regression coefficients and $\epsilon$ is the error term. Parameters are estimated via **Ordinary Least Squares (OLS)**, which minimizes the sum of squared residuals $\sum(y_i - \hat{y}_i)^2$, or equivalently via **Maximum Likelihood Estimation (MLE)** assuming Gaussian errors. The OLS solution has a closed-form via the **normal equations**:

$$\hat{\beta} = (X^T X)^{-1} X^T y$$

For large-scale problems, **gradient descent** is used instead of the direct solve.

## Key Properties

- **Gauss-Markov Theorem**: Under the classical assumptions, OLS is the **Best Linear Unbiased Estimator (BLUE)** — it has the lowest variance among all linear unbiased estimators.
- **R-squared ($R^2$)**: Proportion of variance in $y$ explained by the model; ranges from 0 to 1. Adjusted $R^2$ penalizes for additional predictors.
- **Classical Assumptions**:
  1. **Linearity** — the true relationship is linear in parameters
  2. **Independence** — observations are independent
  3. **Homoscedasticity** — constant error variance across observations
  4. **Normality** — errors are normally distributed (required for inference, not for BLUE)
  5. **No perfect multicollinearity** — predictors are not perfectly correlated

## Applications

| Application | Description |
|---|---|
| Baseline ML model | Simple, interpretable benchmark before deploying complex models |
| Feature importance | Coefficient magnitudes and p-values indicate predictor relevance |
| Causal inference | With proper controls, estimates causal effects (e.g., diff-in-diff, IV) |
| Trend modeling | Could model return rate trends in CUBES or similar abuse metrics |

## Related Terms

- [Least Squares](term_least_squares.md) — the optimization criterion underlying OLS
- [Logistic Regression](term_logistic_regression.md) — extends linear regression to binary classification via the logit link
- [Quantile Regression](term_quantile_regression.md) — models conditional quantiles instead of the conditional mean
- [Binomial Distribution](term_binomial_distribution.md) — GLM link: logistic regression uses binomial likelihood
- [Exponential Family](term_exponential_family.md) — generalized linear models unify linear and logistic regression under this family
- **[Return Rate](term_return_rate.md)**: Linear regression could model return rate trends over time
- **[Clopper-Pearson](term_clopper_pearson.md)**: Both are frequentist estimation methods

- **[Normal Distribution](term_normal_distribution.md)**: Gaussian errors underlie OLS estimation
- **[LASSO](term_lasso.md)**: L1 regularized extension of linear regression for feature selection
- **[Ridge Regression](term_ridge_regression.md)**: L2 regularized extension; Bayesian interpretation as Gaussian prior

## References

- [Linear regression — Wikipedia](https://en.wikipedia.org/wiki/Linear_regression)
- [Gauss–Markov theorem — Wikipedia](https://en.wikipedia.org/wiki/Gauss%E2%80%93Markov_theorem)
