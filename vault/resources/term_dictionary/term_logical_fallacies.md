---
tags:
  - resource
  - terminology
  - critical_thinking
  - analytical_frameworks
  - argumentation
keywords:
  - logical fallacies
  - informal fallacies
  - formal fallacies
  - reasoning errors
  - ad hominem
  - straw man
  - false dilemma
  - slippery slope
  - appeal to emotion
  - appeal to authority
  - red herring
  - circular reasoning
  - hasty generalization
  - bandwagon fallacy
  - tu quoque
  - argumentum
topics:
  - critical thinking
  - argumentation
  - analytical reasoning
language: markdown
date of note: 2026-03-11
status: active
building_block: concept
---

# Term: Logical Fallacies

## Definition

**Logical fallacies** are errors in reasoning that undermine the logical validity of an argument. They are patterns of argument that appear persuasive on the surface but fail to support their conclusion through sound logic. Unlike factual errors (where the premises are wrong), fallacies are structural errors — the premises may be true, but the reasoning connecting them to the conclusion is flawed.

Fallacies are broadly divided into two categories: **formal fallacies**, which can be detected by examining the logical structure alone (e.g., affirming the consequent, denying the antecedent), and **informal fallacies**, which depend on the content and context of the argument (e.g., ad hominem, straw man). Informal fallacies are far more common in everyday reasoning, professional communication, and analytical work because they exploit cognitive biases and social dynamics that formal logic alone cannot capture.

The study of fallacies traces back to **Aristotle's *Sophistical Refutations*** (c. 350 BCE), which catalogued thirteen fallacies used by Sophists. The modern taxonomy has expanded to over 100 named fallacies, though most practical guides focus on the 10-15 most frequently encountered.

## Classification

### Formal vs. Informal

| Type | Detection Method | Example |
|------|-----------------|---------|
| **Formal** | Examine logical structure (form) alone; the conclusion does not follow from the premises regardless of content | Affirming the consequent: "If P then Q; Q; therefore P" |
| **Informal** | Examine the content, context, and relevance of the argument; structurally valid but relies on irrelevant or misleading content | Ad hominem: attacking the arguer instead of the argument |

### Informal Fallacy Categories

| Category | Mechanism | Common Fallacies |
|----------|-----------|-----------------|
| **Fallacies of relevance** | Premises are logically irrelevant to the conclusion | Ad hominem, appeal to emotion, appeal to authority, red herring, tu quoque |
| **Fallacies of presumption** | Premises presuppose what they claim to prove, or assume false constraints | Circular reasoning, false dilemma, loaded question, begging the question |
| **Fallacies of ambiguity** | Exploit vague or shifting meanings of terms | Equivocation, amphiboly, accent |
| **Fallacies of induction** | Draw conclusions from insufficient or unrepresentative evidence | Hasty generalization, slippery slope, false cause (post hoc), bandwagon |

## Major Informal Fallacies

| Fallacy | Description | Example | Why It Works |
|---------|-------------|---------|-------------|
| **[Ad Hominem](term_ad_hominem.md)** | Attacking the person making the argument rather than the argument itself | "Their analysis is wrong because they failed last quarter" | Exploits the halo effect and social judgment (System 1) |
| **[Straw Man](term_straw_man.md)** | Misrepresenting an opponent's position as a weaker version, then refuting the distortion | "They want more testing" → "They think our code is garbage" | Exploits WYSIATI — the audience evaluates only the presented (distorted) version |
| **[False Dilemma](term_false_dilemma.md)** | Presenting only two options when more exist (also: black-or-white thinking) | "Either we ship now or we lose the market entirely" | Exploits framing effect — constraining the choice set constrains the conclusion |
| **[Slippery Slope](term_slippery_slope.md)** | Asserting that one step will inevitably lead to extreme consequences without evidence for each link in the causal chain | "If we allow one policy exception, everyone will demand exceptions and the system collapses" | Exploits availability heuristic — vivid worst-case scenarios feel more probable |
| **[Appeal to Emotion](term_appeal_to_emotion.md)** | Substituting emotional persuasion for evidence | "Think of the customers who will suffer if we don't act immediately" | Bypasses System 2 entirely; emotional arousal reduces analytical scrutiny |
| **[Appeal to Authority](term_appeal_to_authority.md)** | Citing an authority figure as evidence, without evaluating whether the authority is relevant or the claim is supported | "The VP said this approach is best, so we should follow it" | Exploits authority bias and social proof |
| **[Red Herring](term_red_herring.md)** | Introducing an irrelevant topic to divert attention from the original issue | "The model accuracy is low, but look at how fast inference is" | Redirects attention; the audience forgets the original claim |
| **[Hasty Generalization](term_hasty_generalization.md)** | Drawing a broad conclusion from a small or unrepresentative sample | "Two customers complained, so the product must be failing" | Exploits availability heuristic and anchoring to small samples |
| **[Circular Reasoning](term_circular_reasoning.md)** | Using the conclusion as a premise (begging the question) | "This is the right approach because it's the best way to do it" | The circularity is often obscured by verbose restatement |
| **[Bandwagon](term_bandwagon.md)** | Arguing that something is true or good because many people believe or do it | "Everyone uses this framework, so it must be the best" | Exploits social proof and conformity bias |
| **[Tu Quoque](term_tu_quoque.md)** | Deflecting criticism by pointing out the critic's own hypocrisy | "You can't criticize our testing practices — your team ships bugs too" | Shifts focus from the argument to the arguer's behavior |
| **[Post Hoc](term_post_hoc.md)** | Assuming that because B followed A, A caused B | "We deployed the model and fraud dropped — the model must be working" | Exploits the brain's compulsive pattern-matching (narrative fallacy) |

## Fallacy Detection in Practice

### The SEEC Framework for Argument Evaluation

1. **State** the claim being made
2. **Evidence**: What evidence is provided? Is it relevant? Sufficient?
3. **Evaluate**: Does the evidence logically support the claim? What fallacies might be present?
4. **Conclusion**: Is the conclusion warranted, or does it overreach the evidence?

### Common Contexts Where Fallacies Appear

| Context | Most Common Fallacies | Why |
|---------|----------------------|-----|
| **Meetings and presentations** | Appeal to authority, bandwagon, ad hominem | Social pressure and hierarchy |
| **Data analysis** | Post hoc, hasty generalization, false dilemma | Causal inference is hard; binary framing is easy |
| **Policy debates** | Slippery slope, straw man, appeal to emotion | Complex trade-offs invite simplification |
| **Code reviews** | Ad hominem, tu quoque, appeal to authority | Ego involvement in technical work |
| **Paper reviews** | Straw man, hasty generalization, red herring | Misrepresenting authors' claims; judging by one weak section |

## Relationship to Cognitive Biases

Logical fallacies and cognitive biases are distinct but deeply intertwined:

- **Cognitive biases** are involuntary mental shortcuts (System 1 heuristics) that distort perception and judgment
- **Logical fallacies** are argumentation patterns that exploit or manifest these biases

| Bias | Fallacy It Enables |
|------|-------------------|
| **WYSIATI** | Straw man (evaluating only the presented version), false dilemma (considering only visible options) |
| **Anchoring** | Hasty generalization (anchoring to small samples) |
| **Availability** | Slippery slope (vivid scenarios feel probable), hasty generalization |
| **Narrative fallacy** | Post hoc (constructing causal stories from sequential events) |
| **Authority bias** | Appeal to authority |
| **Conformity bias** | Bandwagon, groupthink |
| **Framing effect** | False dilemma, appeal to emotion |

Understanding this mapping enables a **two-level defense**: bias awareness reduces susceptibility to fallacies in one's own thinking; fallacy recognition catches them in others' arguments.

## Related Terms

- [Cognitive Bias](term_cognitive_bias.md) — involuntary mental shortcuts that logical fallacies exploit; biases are the mechanism, fallacies are the manifestation in argument
- [WYSIATI](term_wysiati.md) — "What You See Is All There Is" enables straw man and false dilemma by constraining the information evaluated
- [Socratic Questioning](term_socratic_questioning.md) — disciplined questioning is the primary tool for exposing fallacies; Socrates' method was designed to reveal unjustified assumptions
- [Systems Thinking](term_systems_thinking.md) — systems thinking counteracts slippery slope and false dilemma by revealing the full causal structure
- [Framing Effect](term_framing_effect.md) — framing creates the conditions for false dilemmas and appeals to emotion
- [MECE](term_mece.md) — MECE decomposition is a structural defense against false dilemma (ensuring all options are considered)
- [Design Thinking](term_design_thinking.md) — divergent thinking in design counteracts false dilemma by generating multiple alternatives
- [Question Storming](term_question_storming.md) — generating diverse questions surfaces hidden assumptions that fallacies exploit
- [Groupthink](term_groupthink.md) — groupthink creates the social conditions where bandwagon, appeal to authority, and conformity fallacies thrive
- [Five Whys](term_five_whys.md) — iterative causal questioning counteracts post hoc fallacy by demanding evidence for each causal link
- [Simpson's Paradox](term_simpsons_paradox.md) — a statistical phenomenon where aggregate trends reverse within subgroups; a data-level analogue of hasty generalization
- [Argumentation](term_argumentation.md) — the broader discipline of constructing and evaluating arguments; each fallacy type maps to a failure in a specific argumentation component (claim, warrant, evidence)
- [Critical Thinking](term_critical_thinking.md) — the parent discipline; recognizing and avoiding logical fallacies is a core skill of critical thinking training

## References

- Aristotle. *Sophistical Refutations* (c. 350 BCE). — The original taxonomy of fallacies
- Hamblin, C.L. (1970). *Fallacies*. Methuen. — The definitive academic treatment of fallacy theory
- Damer, T.E. (2009). *Attacking Faulty Reasoning: A Practical Guide to Fallacy-Free Arguments* (6th ed.). Wadsworth. — Comprehensive reference with over 60 fallacies
- [Purdue OWL: Logical Fallacies](https://owl.purdue.edu/owl/general_writing/academic_writing/logic_in_argumentative_writing/fallacies.html) — educational reference
- [Wikipedia: List of Fallacies](https://en.wikipedia.org/wiki/List_of_fallacies) — comprehensive categorized list
- Source: [Digest: Critical Thinking Think Smarter](../digest/digest_critical_thinking_hartley.md) — Hartley's taxonomy of five key informal fallacies with practical detection advice
- Source: [Digest: Strategic Problem Solving](../digest/digest_strategic_problem_solving_hartley.md) — hypothesis-driven analysis as a structural defense against reasoning errors
- Source: [Digest: Thinking, Fast and Slow](../digest/digest_thinking_fast_and_slow_kahneman.md) — the cognitive bias mechanisms that fallacies exploit

---

**Last Updated**: March 11, 2026
**Status**: Active — critical thinking and analytical frameworks terminology
