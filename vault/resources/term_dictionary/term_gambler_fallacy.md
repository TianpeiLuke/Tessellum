---
tags:
  - resource
  - terminology
  - cognitive_science
  - behavioral_economics
keywords:
  - gambler's fallacy
  - Monte Carlo fallacy
  - hot hand fallacy
  - statistical independence
  - representativeness heuristic
  - law of small numbers
  - independent events
  - coin flip
  - roulette
  - clustering illusion
topics:
  - Cognitive Bias
  - Probability and Randomness
  - Decision Making
language: markdown
date of note: 2026-03-13
status: active
building_block: concept
---

# Gambler's Fallacy

## Definition

The **gambler's fallacy** is the mistaken belief that if a particular event has occurred more frequently than expected during some period, it is less likely to occur in the future (or vice versa), when the events are actually independent. If a fair coin lands heads five times in a row, the gambler's fallacy is believing that tails is "due" — but the probability of tails on the next flip remains exactly 50%. The coin has no memory. Each flip is independent, and no finite sequence of past outcomes alters the probability of future outcomes.

The fallacy arises from the **representativeness heuristic** (Tversky & Kahneman, 1971): people expect small samples to mirror the properties of the underlying population. A sequence of HHHHH doesn't "look random" — it lacks the apparent disorder that people associate with randomness. The expectation that the next flip should "correct" the imbalance reflects a false belief in the "law of small numbers" — the intuition that even short sequences should be representative of long-run frequencies. In reality, the law of large numbers guarantees convergence over thousands of trials, not over five.

The reverse phenomenon is the **"hot hand fallacy"** — the belief that a streak makes the next event more likely to continue. A basketball player who sinks five three-pointers in a row is said to have a "hot hand," and teammates feed them the ball. While recent research (Miller & Sanjurjo, 2018) has nuanced this finding — there may be a small hot hand effect in some sports — the magnitude is far less than people perceive, and in purely random processes like roulette, the hot hand is entirely illusory. The gambler's fallacy and the hot hand fallacy are mirror images of the same fundamental error: treating independent events as if they are dependent.

## Historical Context

The gambler's fallacy is sometimes called the **Monte Carlo fallacy** after the most famous instance in gambling history. On August 18, 1913, at the Monte Carlo Casino, the roulette ball landed on black 26 consecutive times. As the streak grew, gamblers rushed to bet on red, convinced that red was increasingly "due." They lost millions. The probability of black on each spin remained exactly 18/37 (European roulette), regardless of the preceding 25 blacks. The event itself — 26 blacks in a row — was improbable ex ante (roughly 1 in 67 million), but once it occurred, it had zero bearing on the next spin.

Tversky and Kahneman (1971) formalized the cognitive mechanism in their paper on the "belief in the law of small numbers," showing that even trained statisticians expected small samples to be more representative of population parameters than probability theory warrants. Their subsequent work on the representativeness heuristic (1974) provided the broader framework: the gambler's fallacy is a specific consequence of judging probability by similarity to a mental prototype of "randomness." Gilovich, Vallone, and Tversky (1985) extended the analysis to basketball, finding no statistical evidence for the hot hand in their original study — a result that generated decades of debate and refinement.

## Key Properties

- **Confuses independent and dependent events**: The core error is applying reasoning appropriate for dependent events (drawing without replacement, finite populations) to independent events (coin flips, roulette spins, dice rolls)
- **Driven by the representativeness heuristic**: People expect random sequences to "look random" — alternating, balanced, and lacking streaks — even though true random sequences frequently contain apparent patterns
- **The law of small numbers**: People intuitively expect small samples to mirror population statistics; five coin flips "should" contain roughly 2-3 heads, and deviations feel like they need correction
- **The Monte Carlo fallacy**: The 1913 Monte Carlo Casino incident — 26 consecutive blacks at roulette — caused massive losses as gamblers bet on red, believing it was "due"; the probability of black remained constant at each spin
- **Hot hand as mirror image**: The gambler's fallacy predicts reversal; the hot hand fallacy predicts continuation; both err by treating independent events as dependent, just in opposite directions
- **Applies beyond gambling**: The fallacy affects investment decisions (selling after a winning streak, expecting reversal), judicial sentencing (judges grant fewer paroles after a streak of approvals; Chen, Moskowitz, & Shue, 2016), and sports predictions
- **Not the same as regression to the mean**: Regression to the mean is a genuine statistical phenomenon concerning measurements with imperfect correlation; the gambler's fallacy is a false belief about independent events — they are often conflated but are distinct
- **The clustering illusion**: Related to the gambler's fallacy — people underestimate the frequency of streaks and clusters in random data, perceiving patterns where only chance exists
- **Countered by understanding independence**: Explicitly checking whether events are independent (does the coin "remember"? does the roulette wheel "track" previous outcomes?) directly targets the fallacy
- **Correct for dependent events**: When events are genuinely dependent (card games with finite decks, sampling without replacement), updating probabilities based on past outcomes is rational, not fallacious — the error is applying this logic to independent events

## Applications

| Domain | Gambler's Fallacy Manifestation | Consequence |
|--------|-------------------------------|-------------|
| **Casino Gambling** | Betting on red after a streak of blacks; changing slot machines after a dry spell | Systematic losses from probability-irrelevant bet adjustments; casinos display previous roulette outcomes to encourage the fallacy |
| **Financial Markets** | "The market has gone up five days in a row, it's due for a correction" | Premature selling or shorting based on streak length rather than fundamental analysis; Benartzi (2001) documents irrational portfolio rebalancing |
| **Judicial Sentencing** | Judges approve fewer asylum cases after a streak of approvals | Chen, Moskowitz, & Shue (2016) found a 3.3 percentage-point drop in approval rate for each additional approval in the streak — potentially affecting thousands of cases |
| **Sports Betting** | Betting against teams on winning streaks, expecting "regression" | Conflation of gambler's fallacy with regression to the mean; independent game outcomes treated as self-correcting sequences |
| **Fraud Detection** | Assuming abuse patterns will self-correct after a spike | Failure to investigate genuine regime changes (new fraud technique) because the spike is dismissed as random variation that will regress |
| **Lottery** | Avoiding recently drawn numbers, or choosing "overdue" numbers | No effect on probability; but generates suboptimal number selection patterns that increase the chance of sharing a jackpot |

## Related Terms

- [Cognitive Bias](term_cognitive_bias.md) — parent category of systematic judgment errors
- [Base Rate Neglect](term_base_rate_neglect.md) — ignoring base rates of independent events in favor of sequence-based reasoning
- [Neglect of Probability](term_neglect_of_probability.md) — broader tendency to mishandle probabilistic reasoning; gambler's fallacy is a specific instance
- [Conjunction Fallacy](term_conjunction_fallacy.md) — another consequence of the representativeness heuristic; judging conjunctions as more probable than components
- [Regression to the Mean](term_regression_to_mean.md) — genuine statistical phenomenon often confused with the gambler's fallacy; regression concerns correlated measurements, not independent events
- [Clustering Illusion](term_clustering_illusion.md) — seeing meaningful patterns in random clusters; the flip side of the gambler's fallacy
- [Illusion of Control](term_illusion_of_control.md) — belief in ability to influence random outcomes; often co-occurs with the gambler's fallacy
- [Confirmation Bias](term_confirmation_bias.md) — selectively remembering instances where the "due" outcome occurred, reinforcing the fallacy
- [Narrative Fallacy](term_narrative_fallacy.md) — constructing stories about why a streak "must" end, providing false justification for the fallacy

## References

### Vault Sources
- [Thinking Clearly (Dobelli)](../digest/digest_thinking_clearly_dobelli.md) — discusses the gambler's fallacy as a fundamental thinking error
- [Thinking, Fast and Slow (Kahneman)](../digest/digest_thinking_fast_and_slow_kahneman.md) — representativeness heuristic and the law of small numbers as root causes

### External Sources
- Tversky, A., & Kahneman, D. (1971). "Belief in the Law of Small Numbers." *Psychological Bulletin*, 76(2), 105-110 — foundational paper on why people expect small samples to be representative
- Tversky, A., & Kahneman, D. (1974). "Judgment under Uncertainty: Heuristics and Biases." *Science*, 185(4157), 1124-1131 — representativeness heuristic framework
- Gilovich, T., Vallone, R., & Tversky, A. (1985). "The Hot Hand in Basketball: On the Misperception of Random Sequences." *Cognitive Psychology*, 17(3), 295-314 — original hot hand study
- Miller, J. B., & Sanjurjo, A. (2018). "Surprised by the Hot Hand Fallacy? A Truth in the Law of Small Numbers." *Econometrica*, 86(6), 2019-2047 — statistical correction showing a small hot hand effect may exist
- Chen, D. L., Moskowitz, T. J., & Shue, K. (2016). "Decision-Making Under the Gambler's Fallacy: Evidence from Asylum Judges, Loan Officers, and Baseball Umpires." *Quarterly Journal of Economics*, 131(3), 1181-1242 — real-world consequences in judicial and financial decisions
- [Wikipedia: Gambler's fallacy](https://en.wikipedia.org/wiki/Gambler%27s_fallacy)
