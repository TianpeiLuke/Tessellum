---
tags:
  - resource
  - terminology
  - critical_thinking
  - argumentation
  - logical_fallacies
keywords:
  - false dilemma
  - false dichotomy
  - black-or-white thinking
  - either-or fallacy
  - bifurcation fallacy
  - excluded middle
  - binary thinking
topics:
  - critical thinking
  - argumentation
  - analytical reasoning
language: markdown
date of note: 2026-03-12
status: active
building_block: concept
---

# Term: False Dilemma

## Definition

A **false dilemma** (also called a false dichotomy or either/or fallacy) presents only two options when more exist, forcing a choice between extremes while ignoring the middle ground, hybrid solutions, or alternative approaches entirely. The fallacy exploits the **framing effect** -- constraining the choice set constrains the conclusion. By presenting a decision as binary ("Either we do X or terrible outcome Y happens"), the arguer eliminates from consideration options C, D, and E that might be superior to both A and B.

False dilemmas are pervasive in **organizational decision-making** ("Either we ship now or we lose the market"), **political rhetoric** ("You're either with us or against us"), and **technical debates** ("Either we rewrite the entire system or we accept technical debt forever"). The fallacy is compelling because binary choices are cognitively simple -- System 1 prefers clear, decisive frames over the ambiguity of multiple options. Real decisions, however, almost always involve a spectrum of possibilities, partial solutions, and trade-offs that a binary frame obscures.

**MECE decomposition** (Mutually Exclusive, Collectively Exhaustive) is the structural antidote to false dilemma. The "Collectively Exhaustive" requirement forces enumeration of ALL options, not just the two most salient or rhetorically convenient ones. Similarly, the divergent phase of **design thinking** -- where the goal is to generate as many alternatives as possible before converging -- directly counteracts the false dilemma's premature narrowing.

## Full Name

- **False Dilemma** (primary term)
- Also called: **false dichotomy**, **black-or-white thinking**, **either/or fallacy**, **bifurcation fallacy**, **excluded middle** (informal), **binary thinking**
- Contrast with: **true dilemma** -- a genuine situation where only two mutually exclusive options exist (rare in practice)

## Logical Structure

The invalid reasoning pattern:

1. Either A or B (presented as exhaustive)
2. Not A
3. Therefore B

**Why it is invalid**: The disjunction in step 1 is not exhaustive -- options C, D, E, and more may also exist. The argument is valid only if A and B truly exhaust all possibilities, which is rarely the case in complex decisions.

## Examples

| Context | False Dilemma Example | Hidden Alternatives |
|---------|----------------------|-------------------|
| **Meeting** | "Either we hire 10 more engineers or we miss the deadline" | Reduce scope, negotiate deadline, redistribute existing team, outsource specific components |
| **Data analysis** | "The model is either accurate enough to deploy or we need to start over" | Recalibrate specific features, deploy with guardrails, use ensemble approach, deploy for low-risk segments only |
| **Policy debate** | "Either we block all returns over $100 or fraud will destroy our margins" | Tiered review thresholds, ML-based risk scoring, identity verification for high-value returns, loyalty-based policies |
| **Code review** | "We can either use microservices or stay with the monolith forever" | Modular monolith, strangler fig pattern, extract only high-churn services, event-driven hybrid architecture |

## Detection and Countermeasures

| Strategy | Application |
|----------|-------------|
| **Ask "What are we NOT considering?"** | Explicitly prompt the group to generate alternatives beyond the two presented |
| **Apply MECE decomposition** | Map the full option space -- the CE (Collectively Exhaustive) requirement exposes missing alternatives |
| **Use Berger's "What if?" questions** | Divergent questioning generates alternatives: "What if we could do both?" "What if neither?" "What else?" |
| **Look for middle ground** | Most binary frames hide a spectrum -- ask "Is there a partial or hybrid option?" |
| **Challenge the framing** | Ask "Who framed these as the only two options, and what was their reasoning?" |
| **Time-box divergent thinking** | Spend 10 minutes brainstorming alternatives before evaluating any option |

## Relationship to Cognitive Biases

The false dilemma exploits several cognitive biases:

- **Framing effect** -- the binary frame shapes the conclusion by constraining what options are even considered
- **WYSIATI** (What You See Is All There Is) -- only the two visible options are evaluated; System 1 does not spontaneously search for invisible alternatives
- **Anchoring** -- the first two options presented anchor the debate, making subsequent alternatives feel like afterthoughts
- **Cognitive ease** -- binary choices are easy to process; multi-option decisions require more cognitive effort, which System 1 resists
- **Status quo bias** -- false dilemmas often pair a dramatic change with the status quo, hiding incremental options in between

## Related Terms

- [Logical Fallacies](term_logical_fallacies.md) -- parent taxonomy; false dilemma is classified as a fallacy of presumption
- [Framing Effect](term_framing_effect.md) -- the cognitive bias that enables false dilemma; the binary frame shapes the conclusion
- [MECE](term_mece.md) -- the structural antidote; the Collectively Exhaustive requirement forces consideration of all options
- [WYSIATI](term_wysiati.md) -- "What You See Is All There Is"; only visible options are evaluated
- [Straw Man](term_straw_man.md) -- also constrains the argument space, but by distorting the opponent's position rather than the option set
- [Slippery Slope](term_slippery_slope.md) -- a related fallacy that also constrains perceived options by projecting catastrophic outcomes
- [Design Thinking](term_design_thinking.md) -- the divergent phase generates alternatives, counteracting premature binary framing
- [Ad Hominem](term_ad_hominem.md) -- another fallacy of misdirection, attacking the person rather than constraining the options

## References

- Source: [Digest: Critical Thinking Think Smarter](../digest/digest_critical_thinking_hartley.md) -- practical detection advice for informal fallacies
- [Wikipedia: False Dilemma](https://en.wikipedia.org/wiki/False_dilemma) -- comprehensive overview of forms, history, and logical structure
- Damer, T.E. (2009). *Attacking Faulty Reasoning* (6th ed.). Wadsworth -- standard reference on false dilemma and its variants
- Sinnott-Armstrong, W. & Fogelin, R. (2015). *Understanding Arguments* (9th ed.). Cengage -- formal treatment of exhaustive disjunctions and the bifurcation fallacy

---

**Last Updated**: March 12, 2026
**Status**: Active -- critical thinking and argumentation terminology
