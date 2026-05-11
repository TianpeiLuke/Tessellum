---
tags:
  - resource
  - terminology
  - causal_inference
  - statistics
  - cognitive_science
keywords:
  - Simpson's paradox
  - Simpson paradox
  - Yule-Simpson effect
  - reversal paradox
  - amalgamation paradox
  - ecological fallacy
  - Berkeley admissions
  - Edward Simpson
  - Judea Pearl
topics:
  - causal inference
  - statistics
  - cognitive science
  - paradoxes
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Simpson's Paradox

## Definition

**Simpson's Paradox** (also known as the **Yule-Simpson effect** or the **reversal paradox**) is a statistical phenomenon in which a trend or association that appears in several separate groups of data reverses direction or disappears when the groups are combined. The paradox has been known since at least 1899, when Karl Pearson and colleagues observed it in correlational data, and was named after Edward Simpson, who described it in a 1951 technical paper, though Udny Yule had also noted the phenomenon in 1903. The paradox is not merely a curiosity of aggregation; it arises frequently in real data and has led to serious errors in medical treatment decisions, legal rulings, and policy evaluations.

Judea Pearl argues in *The Book of Why* (2018, Chapter 6: "Paradoxes Galore!") that Simpson's Paradox is fundamentally a **causal**, not a statistical, puzzle. The purely statistical question -- "Should we use the aggregated data or the disaggregated data?" -- has no answer within statistics alone. The resolution requires knowing the **causal structure** underlying the data, specifically whether the variable used to partition the data (the "lurking variable") is a **confounder** (a common cause of treatment and outcome) or a **collider** (a common effect). If it is a confounder, the disaggregated (stratified) data reflect the true causal effect and we should control for it. If it is a collider, the aggregated data are correct and conditioning on it would *introduce* bias. Pearl's back-door criterion provides a formal, algorithmic test for determining which case applies.

The most famous real-world example is the **UC Berkeley graduate admissions case** (1973). Aggregate data showed that 44% of male applicants were admitted versus only 35% of female applicants, suggesting gender discrimination. However, when the data were broken down by department, women were actually admitted at slightly higher rates than men in most departments. The reversal occurred because women tended to apply to more competitive departments with lower overall admission rates. In this case, the causal analysis reveals that "department" is partly a collider (gender influences department choice, and department influences admission), making the correct analysis more nuanced than simply stratifying -- a point Pearl uses to illustrate why causal reasoning, not just statistical reasoning, is necessary.

## Full Name

Also known as:
- **Yule-Simpson effect** (acknowledging Udny Yule's earlier observation)
- **Reversal paradox**
- **Amalgamation paradox**
- **Simpson's reversal**

Related phenomena:
- **Ecological fallacy** -- drawing individual-level conclusions from aggregate data (related but distinct)
- **Lord's paradox** -- a continuous-variable analog of Simpson's paradox in analysis of covariance
- **Suppression effect** -- a related statistical phenomenon where adding a variable increases the apparent effect

## Core Concepts

### The Paradox Illustrated

Consider a hypothetical treatment study:

| Group | Treatment Success | Control Success | Conclusion |
|-------|------------------|-----------------|------------|
| **Men** | 80/100 (80%) | 60/100 (60%) | Treatment helps |
| **Women** | 40/100 (40%) | 20/100 (20%) | Treatment helps |
| **Combined** | 120/200 (60%) | 80/200 (40%) | Treatment helps |

Now change the group sizes:

| Group | Treatment Success | Control Success | Conclusion |
|-------|------------------|-----------------|------------|
| **Men** | 80/100 (80%) | 600/1000 (60%) | Treatment helps |
| **Women** | 4/10 (40%) | 200/1000 (20%) | Treatment helps |
| **Combined** | 84/110 (76%) | 800/2000 (40%) | Treatment helps |

But with different allocation:

| Group | Treatment Success | Control Success | Conclusion |
|-------|------------------|-----------------|------------|
| **Men** | 8/10 (80%) | 600/1000 (60%) | Treatment helps |
| **Women** | 400/1000 (40%) | 20/100 (20%) | Treatment helps |
| **Combined** | 408/1010 (40.4%) | 620/1100 (56.4%) | Treatment **hurts**! |

In both subgroups the treatment helps, but in the combined data it appears to hurt -- because the lurking variable (gender) is associated with both treatment assignment and baseline recovery rates.

### Pearl's Causal Resolution

| Causal Structure | Lurking Variable Role | Correct Action | Example |
|-----------------|----------------------|----------------|---------|
| Z causes both X and Y | **Confounder** (fork: X <-- Z --> Y) | Stratify by Z (use subgroup data) | Age confounds exercise-health association |
| X and Y both cause Z | **Collider** (X --> Z <-- Y) | Do NOT stratify by Z (use aggregate data) | Talent and attractiveness both cause fame |
| Z is on the causal path X --> Z --> Y | **Mediator** | Depends on question (total vs. direct effect) | Tar deposits mediate smoking-cancer |

### The Berkeley Admissions Case

| Level | Male Admit Rate | Female Admit Rate | Apparent Conclusion |
|-------|----------------|-------------------|---------------------|
| **Aggregate** | 44% | 35% | Bias against women |
| **By department** | Women admitted at equal or higher rates in most departments | -- | No systematic bias against women |
| **Explanation** | Women applied disproportionately to more competitive departments with lower admission rates for everyone | -- | Department choice, not discrimination, explains the aggregate gap |

Pearl notes that the causal structure here is subtle: gender may influence department choice (making department a mediator on the path Gender --> Department --> Admission), or there may be department-level discrimination that affects both which students apply and how they are evaluated. The correct analysis depends on the causal question being asked.

## Key Research and Evidence

- **Yule, G. U. (1903)**: "Notes on the theory of association of attributes in statistics" -- first noted the possibility of reversal in aggregated associations
- **Simpson, E. H. (1951)**: "The interpretation of interaction in contingency tables" -- the paper that gave the paradox its name
- **Bickel, P. J., Hammel, E. A., & O'Connell, J. W. (1975)**: "Sex bias in graduate admissions: Data from Berkeley" -- *Science* -- the landmark empirical demonstration
- **Pearl, J. (2000)**: *Causality*, Section 6.1 -- formal treatment using back-door criterion
- **Pearl, J. (2014)**: "Comment: Understanding Simpson's Paradox" -- *The American Statistician* -- Pearl's definitive statement that the paradox is causal, not statistical
- **Pearl, J. & Mackenzie, D. (2018)**: *The Book of Why*, Chapter 6 -- accessible treatment with multiple examples

## Practical Applications

### Medical Decision-Making
- Simpson's paradox has appeared in real clinical data, where a treatment appears effective overall but harmful in every subgroup (or vice versa). Without causal analysis, clinicians may make the wrong treatment decision. Pearl argues that the only reliable resolution is to draw the causal diagram and apply the back-door criterion.

### Abuse Prevention and Fraud Detection
- **Aggregate vs. segmented metrics**: Abuse rates that appear to be decreasing overall may be increasing within every customer segment if the composition of the customer base is shifting. Causal analysis is needed to determine whether a policy is truly working.
- **Enforcement effectiveness**: An enforcement action might appear ineffective in aggregate but effective within each risk tier, or vice versa, depending on how enforcement is allocated across tiers. Simpson's paradox warns against naive before-after comparisons without stratification by relevant confounders.
- **Model fairness evaluation**: A fraud model might appear unbiased overall while being biased within specific demographic subgroups, or appear biased in aggregate while being fair within each subgroup -- a direct analog of the Berkeley admissions case.

### Knowledge Management
- Simpson's paradox is a powerful reminder that the "right" level of aggregation for analyzing data depends on the causal question, not on statistical convenience. In a SlipBox, this principle can be applied to any note that presents aggregate statistics: always ask "Could this pattern reverse at a finer level of analysis?"

## Criticisms and Limitations

- **Not always a "paradox"**: Some statisticians object to calling it a paradox, since the mathematics are straightforward -- the apparent paradox arises only from the expectation that subgroup trends should persist in aggregates, which is not a mathematical law.
- **Multiple valid causal models**: The "correct" resolution depends on the causal model, and reasonable people may disagree about the correct model, leaving the paradox unresolved in practice.
- **Overuse as a cautionary tale**: The paradox is sometimes invoked to dismiss any aggregate finding, when in fact many aggregate findings are perfectly valid and subgroup analysis can introduce its own biases (e.g., multiple comparisons, small subgroups).
- **Continuous variables**: The standard presentation uses discrete groups, but the paradox can also arise with continuous variables (Lord's paradox), where the resolution is even less intuitive.

## Related Terms

- [Term: Causal Inference](term_causal_inference.md) -- the field that provides the tools to resolve Simpson's Paradox
- [Term: Confounding Variable](term_confounding_variable.md) -- the most common causal explanation for Simpson's Paradox
- [Term: Collider Bias](term_collider_bias.md) -- the alternative explanation; conditioning on a collider can create reversal
- [Term: Directed Acyclic Graph](term_directed_acyclic_graph.md) -- the graphical tool needed to determine the correct resolution
- [Term: Do-Calculus](term_do_calculus.md) -- provides a complete resolution when back-door adjustment is insufficient
- [Term: Structural Causal Model](term_structural_causal_model.md) -- the formal framework for encoding the causal assumptions needed to resolve the paradox
- [Term: Ladder of Causation](term_ladder_of_causation.md) -- Simpson's Paradox illustrates why Rung 1 (association) is insufficient for Rung 2 (intervention) questions
- [Term: Cognitive Bias](term_cognitive_bias.md) -- the paradox exploits our intuitive expectation that subgroup trends must persist in aggregates
- [Term: Framing Effect](term_framing_effect.md) -- how the data are "framed" (aggregated vs. disaggregated) dramatically changes conclusions
- [Term: WYSIATI](term_wysiati.md) -- analysts who see only the aggregate data fall prey to "What You See Is All There Is"
- [Term: Randomized Controlled Trial](term_randomized_controlled_trial.md) -- randomization prevents Simpson's Paradox by balancing confounders
- [Logical Fallacies](term_logical_fallacies.md) — Simpson's Paradox is a statistical phenomenon that can be seen as a data-level analogue of hasty generalization

- **[Binomial Distribution](term_binomial_distribution.md)**: Simpson's paradox often arises with binomial proportions across subgroups
- **[Confidence Interval](term_confidence_interval.md)**: Subgroup CIs can reverse the aggregate CI — Simpson's paradox

## References

- Pearl, J., & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*. Basic Books. (Chapter 6)
- Simpson, E. H. (1951). The interpretation of interaction in contingency tables. *Journal of the Royal Statistical Society, Series B*, 13(2), 238-241.
- Bickel, P. J., Hammel, E. A., & O'Connell, J. W. (1975). Sex bias in graduate admissions: Data from Berkeley. *Science*, 187(4175), 398-404.
- Pearl, J. (2014). Comment: Understanding Simpson's Paradox. *The American Statistician*, 68(1), 8-13.
- [Wikipedia: Simpson's Paradox](https://en.wikipedia.org/wiki/Simpson%27s_paradox)
- [Stanford Encyclopedia of Philosophy: Simpson's Paradox](https://plato.stanford.edu/entries/paradox-simpson/)
- [Digest: The Book of Why](../digest/digest_book_of_why_pearl.md)

---

**Last Updated**: March 7, 2026
**Status**: Active
