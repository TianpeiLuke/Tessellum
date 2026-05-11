---
tags:
  - resource
  - terminology
  - critical_thinking
  - argumentation
  - logical_fallacies
keywords:
  - post hoc
  - post hoc ergo propter hoc
  - false cause
  - correlation causation
  - cum hoc ergo propter hoc
  - questionable cause
  - non causa pro causa
  - after therefore because
topics:
  - critical thinking
  - argumentation
  - analytical reasoning
language: markdown
date of note: 2026-03-12
status: active
building_block: concept
---

# Term: Post Hoc

## Definition

The **post hoc** fallacy (post hoc ergo propter hoc — "after this, therefore because of this") is the assumption that because event B followed event A, A caused B. "We deployed the model and fraud dropped — the model must be working" conflates temporal sequence with causation. The fallacy exploits the brain's compulsive pattern-matching — the **narrative fallacy** (Kahneman) that constructs causal stories from sequential events.

Post hoc reasoning is the most common analytical error in data-driven organizations because observational data always contains temporal sequences that LOOK causal but may reflect **confounding variables**, **regression to the mean**, or **coincidence**. A fraud rate dropping after a model deployment may also reflect seasonal effects, a concurrent policy change, or simply a return to baseline after an anomalous spike.

Judea Pearl's **Ladder of Causation** provides the framework for understanding why post hoc fails: observational data (rung 1: seeing) can establish correlation but not causation; causal claims require intervention (rung 2: doing) or counterfactual reasoning (rung 3: imagining). The **Five Whys** technique counteracts post hoc by demanding explicit evidence for each causal link, forcing the analyst past the first plausible-sounding explanation.

## Full Name

**Post Hoc Ergo Propter Hoc** (also known as: Post Hoc Fallacy, False Cause, After Therefore Because, Questionable Cause, Non Causa Pro Causa)

**Variant**: **Cum Hoc Ergo Propter Hoc** ("with this, therefore because of this") — correlation treated as causation even without temporal ordering.

## Logical Structure

| Step | Content |
|------|---------|
| Observation | A occurred before B |
| Conclusion | Therefore A caused B |
| **Why invalid** | Temporal precedence is necessary but not sufficient for causation; confounders, coincidence, regression to the mean, and reverse causation are alternative explanations |

## Examples

| Context | Fallacious Argument | Why It Is Fallacious |
|---------|--------------------|--------------------|
| **Meeting** | "We changed the process last quarter and customer satisfaction improved — the new process is working" | Other factors (seasonal trends, staffing changes, concurrent initiatives) may explain the improvement |
| **Data analysis** | "Countries that adopted policy X have lower crime rates — policy X reduces crime" | Self-selection bias: countries that adopt the policy may differ systematically from those that do not |
| **Policy debate** | "We tightened enforcement and abuse rates dropped, proving our enforcement works" | Regression to the mean: abuse rates may have been at a temporary peak and would have dropped regardless |
| **Code review** | "After the refactor, page load times improved — the refactor was worth it" | A concurrent infrastructure upgrade, caching change, or reduced traffic may be the actual cause |

## Detection and Countermeasures

| Strategy | How It Works |
|----------|-------------|
| **Demand a causal mechanism** | Ask: "How specifically would A cause B?" — forces the arguer to articulate a plausible pathway rather than relying on temporal coincidence |
| **Look for confounders** | Systematically identify other factors that changed during the same period; any uncontrolled variable is an alternative explanation |
| **Apply Pearl's Ladder** | Can you establish causation via intervention (A/B test) or counterfactual ("what would have happened without A")? If not, the claim is merely correlational |
| **Five Whys** | Test each causal link: "Why did B happen?" → "Because of A" → "Why would A cause B?" — each level demands independent evidence |
| **Check for regression to the mean** | Was A introduced after an unusually high or low measurement? If so, the subsequent movement toward the mean is expected regardless of intervention |

## Relationship to Cognitive Biases

| Bias | How It Enables Post Hoc Reasoning |
|------|----------------------------------|
| **Narrative fallacy** | System 1 compulsively constructs causal stories from sequential events; temporal order becomes causal order automatically |
| **Pattern recognition (System 1)** | The brain evolved to detect causes quickly; false positives (seeing causation where there is none) were less costly than false negatives in ancestral environments |
| **Confirmation bias** | We notice temporal sequences that confirm our expectations and ignore those that disconfirm; confirming sequences are remembered, disconfirming ones are forgotten |
| **Anchoring** | The first plausible-sounding cause anchors the analysis; subsequent investigation adjusts insufficiently from this anchor |

## Related Terms

- [Logical Fallacies](term_logical_fallacies.md) — parent term; post hoc is a fallacy of induction (false cause)
- [Five Whys](term_five_whys.md) — demands evidence for each causal link, counteracting the single-step causal leap of post hoc
- [Circular Reasoning](term_circular_reasoning.md) — both involve unjustified claims; circularity restates the conclusion, post hoc asserts unwarranted causation
- [Bandwagon](term_bandwagon.md) — "we adopted X and things improved" can conflate bandwagon (everyone does it) with post hoc (it happened after adoption)
- [Tu Quoque](term_tu_quoque.md) — both are common in organizational retrospectives where attribution of cause and blame is contested
- [Hasty Generalization](term_hasty_generalization.md) — both draw conclusions from insufficient evidence; hasty generalization from small samples, post hoc from temporal coincidence
- [Slippery Slope](term_slippery_slope.md) — both involve unwarranted causal chains; slippery slope projects forward, post hoc reasons backward
- [Simpson's Paradox](term_simpsons_paradox.md) — aggregate correlations can reverse in subgroups, making post hoc inferences from aggregate data especially dangerous
- [Cognitive Bias](term_cognitive_bias.md) — narrative fallacy and confirmation bias are the psychological engines of post hoc reasoning
- [Socratic Questioning](term_socratic_questioning.md) — Type 3 (probing reasons and evidence) and Type 5 (probing implications) expose unjustified causal claims

## References

- Source: [Digest: Critical Thinking Think Smarter](../digest/digest_critical_thinking_hartley.md) — Hartley's analysis of false cause reasoning and its prevalence in analytical work
- [Wikipedia: Post Hoc Ergo Propter Hoc](https://en.wikipedia.org/wiki/Post_hoc_ergo_propter_hoc) — overview with historical origins and modern examples
- Pearl, J. & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*. Basic Books. — the Ladder of Causation framework for distinguishing correlation from causation
- Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux. — narrative fallacy and System 1's compulsive causal attribution
- Damer, T.E. (2009). *Attacking Faulty Reasoning* (6th ed.). Wadsworth. — practical guide to detecting false cause fallacies

---

**Last Updated**: March 12, 2026
**Status**: Active — critical thinking and argumentation terminology
