---
tags:
  - resource
  - terminology
  - behavioral_economics
  - decision_making
  - cognitive_science
keywords:
  - prospect theory
  - Kahneman
  - Tversky
  - reference point
  - value function
  - probability weighting
  - loss aversion
  - diminishing sensitivity
  - risk attitudes
  - fourfold pattern
  - cumulative prospect theory
topics:
  - behavioral economics
  - decision making
  - judgment under uncertainty
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Prospect Theory

## Definition

**Prospect theory** is a descriptive model of decision-making under risk developed by Daniel Kahneman and Amos Tversky, first published in their 1979 paper "Prospect Theory: An Analysis of Decision under Risk" in *Econometrica*. It replaced *expected utility theory (EUT)* as the dominant behavioral model of how people actually make risky choices, and was the primary work cited in the awarding of the 2002 Nobel Memorial Prize in Economic Sciences to Kahneman (Tversky had died in 1996 and was therefore ineligible).

Prospect theory arose from a systematic catalog of violations of expected utility theory -- situations in which real people consistently chose differently from what rational-actor models predicted. Where EUT assumes that people evaluate outcomes in terms of final states of wealth and weight outcomes by their objective probabilities, prospect theory introduces three key departures: (1) **reference dependence** -- outcomes are coded as gains or losses relative to a reference point (usually the status quo), not as absolute wealth levels; (2) **diminishing sensitivity** -- the marginal impact of both gains and losses decreases as their magnitude increases; and (3) **loss aversion** -- losses are weighted approximately 1.5 to 2.5 times more heavily than equivalent gains.

In 1992, Tversky and Kahneman published an updated version called **cumulative prospect theory** (CPT), which extended the original model to handle uncertain prospects with any number of outcomes and introduced rank-dependent probability weighting. CPT applies cumulative probability transformations rather than weighting individual probabilities, resolving technical issues with the original formulation (including potential violations of first-order stochastic dominance). Cumulative prospect theory is the version most commonly used in contemporary research.

## Full Name

- **Full**: Prospect Theory: An Analysis of Decision under Risk
- **Updated version**: Cumulative Prospect Theory (CPT, 1992)
- **Contrasted with**: Expected Utility Theory (EUT, von Neumann & Morgenstern, 1944); Subjective Expected Utility (SEU, Savage, 1954)

## Three Pillars of Prospect Theory

### Pillar 1: Reference Dependence

People evaluate outcomes as **gains or losses relative to a reference point**, not in terms of absolute wealth. The reference point is typically the status quo, but can be shifted by expectations, aspirations, or framing.

- A $100 bonus feels very different depending on whether you expected $0 (a gain) or $200 (a loss)
- The same objective outcome can be experienced as a gain or a loss depending on how it is framed
- This directly contradicts expected utility theory, which assumes that only final wealth states matter ("Bernoulli's error," as Kahneman calls it)

**Implication**: Two people with identical final wealth can have very different subjective evaluations of the same outcome if they started from different reference points.

### Pillar 2: Diminishing Sensitivity

The **value function** is concave for gains and convex for losses, meaning that the psychological impact of a marginal dollar decreases as you move further from the reference point in either direction.

- The subjective difference between $100 and $200 is much larger than between $1,100 and $1,200
- The subjective difference between losing $100 and losing $200 is much larger than between losing $1,100 and losing $1,200
- This produces risk aversion in the domain of gains (people prefer a sure $500 to a 50% chance at $1,000) and risk seeking in the domain of losses (people prefer a 50% chance of losing $1,000 to a sure loss of $500)

### Pillar 3: Loss Aversion

**Losses loom larger than gains.** The value function is steeper for losses than for gains, with empirical estimates placing the loss aversion coefficient (lambda) at approximately 2.25 (Tversky & Kahneman, 1992). This means losing $100 feels roughly 2 to 2.5 times worse than gaining $100 feels good.

## The Value Function

The prospect theory value function has a distinctive **S-shaped curve**:

```
Value
  ^
  |        ___---  (gains: concave - diminishing sensitivity)
  |      /
  |    /
  |  /
  |----- Reference Point (0,0) -------> Outcome
  |  \
  |    \
  |      \          (losses: convex - diminishing sensitivity)
  |        \____    (steeper slope than gains - loss aversion)
  v
```

Key properties:
- Passes through the origin (the reference point)
- Concave above the reference point (risk aversion for gains)
- Convex below the reference point (risk seeking for losses)
- Steeper for losses than for gains (loss aversion)

## The Probability Weighting Function

People do not weight outcomes by their objective probabilities. Instead, they apply a **probability weighting function** that:

- **Overweights small probabilities** -- rare events receive more decision weight than their objective probability warrants (explains both lottery ticket purchases and insurance buying)
- **Underweights moderate to high probabilities** -- likely outcomes receive less weight than they "should"
- **Certainty effect** -- the jump from 95% to 100% (certainty) has disproportionate psychological impact compared to the jump from 50% to 55%

## The Fourfold Pattern of Risk Attitudes

The interaction of the value function and the probability weighting function produces four distinct risk attitudes:

| | **High Probability** | **Low Probability** |
|---|---|---|
| **Gains** | **Risk-averse**: prefer a sure $900 over a 90% chance of $1,000 (certainty effect) | **Risk-seeking**: prefer a 5% chance of $10,000 over a sure $500 (lottery effect) |
| **Losses** | **Risk-seeking**: prefer a 90% chance of losing $1,000 over a sure loss of $900 (hope to avoid loss) | **Risk-averse**: prefer a sure loss of $5 over a 5% chance of losing $100 (insurance effect) |

This fourfold pattern explains otherwise puzzling behaviors: the same person can buy both lottery tickets (risk-seeking for low-probability gains) and insurance (risk-averse for low-probability losses).

## Key Research and Evidence

- **Kahneman & Tversky (1979)**: The original *Econometrica* paper; presented experimental evidence of systematic violations of EUT; introduced the value function and probability weighting; became one of the most cited papers in economics (over 80,000 citations as of 2025)
- **Tversky & Kahneman (1992)**: "Advances in Prospect Theory: Cumulative Representation of Uncertainty" in *Journal of Risk and Uncertainty*; introduced cumulative prospect theory with rank-dependent probability weighting and estimated lambda = 2.25
- **Thaler (1980)**: Applied prospect theory to consumer behavior, introducing "mental accounting" -- the tendency to categorize money into separate mental accounts with different reference points
- **Global replication (2019)**: A large-scale cross-cultural study found that Kahneman and Tversky's 1979 empirical foundations broadly replicated across all countries studied, with approximately 90% replication of the core theoretical contrasts
- **Barberis (2013)**: "Thirty Years of Prospect Theory in Economics" in the *Journal of Economic Perspectives* -- comprehensive review of applications in finance, insurance, labor supply, and industrial organization

## Practical Applications

### Finance and Investment
- **Disposition effect**: Investors sell winners too early (locking in gains) and hold losers too long (avoiding the realization of losses) -- directly predicted by the S-shaped value function
- **Equity premium puzzle**: The historically high premium demanded for holding stocks over bonds can be partially explained by loss-averse investors who evaluate their portfolio frequently (narrow framing + loss aversion = myopic loss aversion, per Benartzi & Thaler, 1995)

### Policy and Nudge Design
- **Default options**: Prospect theory explains why defaults are powerful -- changing from the status quo is coded as a potential loss; opt-out organ donation systems achieve near-universal participation
- **Framing of policy outcomes**: Describing a medical procedure as having a "90% survival rate" vs. a "10% mortality rate" produces different patient choices for the same objective information

### Abuse Prevention and Decision Science
- **Reference point manipulation**: Abusers may exploit reference dependence by framing a return or refund request as recovering from an unexpected loss, triggering loss-aversion-based empathy in agents
- **Risk attitudes in fraud**: The fourfold pattern predicts that potential abusers facing likely detection (high-probability loss) may become risk-seeking -- escalating fraud rather than stopping -- because they prefer a gamble over a sure penalty
- **Policy framing**: How abuse penalties are framed (loss of account privileges vs. failure to earn trust-based benefits) can change deterrent effectiveness based on prospect theory predictions

## Criticisms and Limitations

- **Reference point ambiguity**: The theory does not precisely specify how reference points are determined; different reference point assumptions can generate different predictions from the same model
- **Parameter instability**: The loss aversion coefficient and probability weighting parameters vary across studies, populations, and domains; there is no single "correct" parameterization
- **Gal & Rucker (2018)**: Challenged whether loss aversion is as universal as claimed, arguing that context moderates the effect and that some standard demonstrations (endowment effect, status quo bias) admit alternative explanations
- **Complexity**: Prospect theory is more descriptively accurate but less mathematically tractable than EUT, which remains the dominant normative model in formal economic theory
- **Individual differences**: The theory describes average tendencies; individual variation in risk attitudes and loss aversion is substantial

## Related Terms

- [Term: Loss Aversion](term_loss_aversion.md) -- the asymmetric weighting of losses vs. gains; a core pillar of prospect theory
- [Term: Cognitive Bias](term_cognitive_bias.md) -- prospect theory describes several specific biases in risky choice
- [Term: Framing Effect](term_framing_effect.md) -- identical options described differently produce different choices; directly follows from reference dependence
- [Term: System 1 and System 2](term_system_1_and_system_2.md) -- the dual-process framework; prospect theory effects emerge from System 1 evaluation
- [Term: Anchoring](term_anchoring.md) -- reference points in prospect theory function similarly to anchors in estimation tasks
- [Term: Availability Heuristic](term_availability_heuristic.md) -- vivid availability of rare outcomes amplifies probability overweighting
- [Term: WYSIATI](term_wysiati.md) -- "What You See Is All There Is"; interacts with framing to determine which reference point is salient
- [Term: Planning Fallacy](term_planning_fallacy.md) -- optimistic estimation driven by inside-view evaluation, connected to the certainty effect
- [Term: Peak-End Rule](term_peak_end_rule.md) -- how experiences are remembered, with implications for retrospective reference points
- [Term: Zettelkasten](term_zettelkasten.md) -- structured knowledge management counteracts narrow framing by making full evidence bases visible
- [Commitment Device](term_commitment_device.md) -- penalty-based commitment devices (losses) are more effective than reward-based ones (gains), as predicted by the value function's steeper loss curve

## References

- Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263-292.
- Tversky, A., & Kahneman, D. (1992). Advances in prospect theory: Cumulative representation of uncertainty. *Journal of Risk and Uncertainty*, 5(4), 297-323.
- Barberis, N. C. (2013). Thirty years of prospect theory in economics: A review and assessment. *Journal of Economic Perspectives*, 27(1), 173-196.
- [Wikipedia: Prospect Theory](https://en.wikipedia.org/wiki/Prospect_theory) -- comprehensive overview with mathematical formulation and applications
- [The Decision Lab: Prospect Theory](https://thedecisionlab.com/reference-guide/economics/prospect-theory) -- accessible explanation with examples and practical implications
- [Econometric Society: Original 1979 Paper](https://www.econometricsociety.org/publications/econometrica/1979/03/01/prospect-theory-analysis-decision-under-risk) -- original publication page
- Source: [Digest: Thinking, Fast and Slow](../digest/digest_thinking_fast_and_slow_kahneman.md)

---

**Last Updated**: March 7, 2026
**Status**: Active -- behavioral economics terminology
