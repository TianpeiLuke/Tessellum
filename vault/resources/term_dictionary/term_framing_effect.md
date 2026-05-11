---
tags:
  - resource
  - terminology
  - behavioral_economics
keywords:
  - framing effect
  - framing bias
  - choice architecture
  - Asian disease problem
  - Tversky and Kahneman
  - prospect theory
  - risk preferences
  - gain frame
  - loss frame
  - nudge
  - default options
topics:
  - behavioral economics
  - decision making
  - cognitive psychology
  - public policy
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Framing Effect

## Definition

The **framing effect** is a cognitive bias in which people's decisions and preferences are systematically influenced by the way information is presented (or "framed"), even when the underlying options are objectively identical. The same outcome described as a gain produces different choices than when described as a loss. For example, people respond differently to "90% survival rate" versus "10% mortality rate," despite both statements conveying the same information. The framing effect demonstrates that human preferences are not stable, pre-existing entities that are merely "revealed" by choices -- instead, preferences are actively *constructed* at the moment of decision, shaped by context, wording, and presentation.

The framing effect was formally identified by Amos Tversky and Daniel Kahneman in their seminal 1981 paper "The Framing of Decisions and the Psychology of Choice," published in *Science*. The concept is deeply connected to **prospect theory** (Kahneman & Tversky, 1979), which explains *why* framing works: people evaluate outcomes relative to a reference point (usually the status quo), are risk-averse in the domain of gains, and risk-seeking in the domain of losses. The frame determines which domain the decision-maker operates in, and thus which risk attitude governs the choice.

Framing effects violate a fundamental axiom of rational choice theory -- the **invariance principle** -- which holds that logically equivalent descriptions of the same problem should yield the same preference. The fact that they do not is one of the strongest pieces of evidence against the classical economic model of rational agents and in favor of the behavioral economics paradigm. As Kahneman writes in *Thinking, Fast and Slow*, "the framing of problems is controlled by the manner of presentation as well as by norms, habits, and expectations of the decision-maker."

## Full Name

- **Framing Effect** (primary term)
- Also called: **framing bias**, **description invariance violation**
- Closely related: **choice architecture** (Thaler & Sunstein) -- the deliberate design of how choices are presented
- Closely related: **nudge** -- using framing and defaults to guide behavior without restricting options
- Contrast with: **invariance principle** -- the rational-choice assumption that equivalent descriptions produce identical preferences

## Core Concepts

### Types of Framing Effects

Framing effects manifest in several distinct forms, each with different mechanisms:

#### 1. Risky Choice Framing (Gain vs. Loss Frames)

The most studied form, demonstrated by the Asian disease problem. Identical options are described in terms of gains (lives saved) or losses (lives lost), producing systematic shifts in risk preference:
- **Gain frame**: People become risk-averse, preferring the certain option
- **Loss frame**: People become risk-seeking, preferring the gamble
- **Mechanism**: Prospect theory's S-shaped value function -- concave for gains (diminishing marginal value), convex for losses (diminishing marginal loss)

#### 2. Attribute Framing

A single attribute of an object or event is described in positive or negative terms:
- "95% lean" beef vs. "5% fat" beef -- the positive frame is rated as higher quality
- "90% success rate" surgery vs. "10% failure rate" surgery -- the positive frame increases willingness to undergo the procedure
- **Mechanism**: Valence-consistent encoding -- the frame activates positive or negative associations in memory

#### 3. Goal Framing

A message emphasizes either the benefits of performing an action or the costs of not performing it:
- "Using sunscreen reduces your chance of skin cancer" (gain frame) vs. "Not using sunscreen increases your chance of skin cancer" (loss frame)
- **Mechanism**: Loss aversion -- loss-framed messages are generally more persuasive for prevention behaviors because they highlight what could be lost

#### 4. Default Framing

The status quo or default option constitutes a powerful frame:
- **Organ donation**: Countries with opt-out defaults (presumed consent) have donation rates of ~85-90%, while opt-in countries have rates of ~15-20% (Johnson & Goldstein, 2003)
- **Retirement savings**: Automatic enrollment in 401(k) plans dramatically increases participation (Thaler & Benartzi, 2004)
- **Mechanism**: Status quo bias + loss aversion -- switching from the default is perceived as a loss

### The Prospect Theory Foundation

The framing effect is best understood through prospect theory's three principles:

| Principle | Description | Role in Framing |
|-----------|-------------|-----------------|
| **Reference dependence** | Outcomes are evaluated relative to a reference point | The frame sets the reference point -- gains vs. losses are defined relative to it |
| **Diminishing sensitivity** | Marginal impact decreases with distance from reference point | Explains the S-shape of the value function that drives risk attitude shifts |
| **Loss aversion** | Losses loom ~1.5-2.5x larger than equivalent gains | Loss frames trigger stronger emotional responses and different risk preferences |

## Key Research and Evidence

### The Asian Disease Problem (Tversky & Kahneman, 1981)

The most famous demonstration of the framing effect. Participants were told that the US was preparing for an outbreak of an unusual Asian disease expected to kill 600 people:

**Gain frame** (Program A vs. B):
- Program A: 200 people will be saved (certain)
- Program B: 1/3 probability that 600 will be saved; 2/3 probability that no one will be saved
- **Result**: 72% chose Program A (risk-averse)

**Loss frame** (Program C vs. D):
- Program C: 400 people will die (certain)
- Program D: 1/3 probability that nobody will die; 2/3 probability that 600 will die
- **Result**: 78% chose Program D (risk-seeking)

Programs A and C are identical, as are B and D. Yet the majority preference reverses depending on the frame. This result has been replicated in numerous studies across cultures, though the effect size is sometimes smaller than the original.

### Medical Decision Framing (McNeil et al., 1982)

When physicians and patients were presented with treatment options for lung cancer described in terms of survival rates vs. mortality rates, the framing significantly affected treatment preferences -- even among experienced doctors. A surgery with a "90% one-month survival rate" was preferred over the same surgery described as having a "10% one-month mortality rate."

### Organ Donation Defaults (Johnson & Goldstein, 2003)

A landmark study showed that European countries with opt-out organ donation systems (where the default is to be a donor) had dramatically higher effective consent rates than countries with opt-in systems. The difference was not explained by cultural attitudes toward donation but by the default frame. This became one of the foundational studies for the "nudge" movement.

### Thaler and Sunstein's Nudge Framework (2008)

Richard Thaler and Cass Sunstein built on framing research to develop the concept of **libertarian paternalism** -- the idea that choices can be structured ("choice architecture") to guide people toward beneficial outcomes without restricting their freedom. Their book *Nudge* (2008) popularized the application of framing effects to public policy, including retirement savings, organ donation, and environmental behavior.

## Practical Applications

### Abuse Prevention and Customer Experience

Framing effects are directly relevant to buyer abuse prevention:
- **Policy communication**: How return and refund policies are communicated (gain vs. loss framing) affects both legitimate customer satisfaction and potential abuse. "You may return within 30 days" (gain frame) vs. "Returns after 30 days are not accepted" (loss frame) activate different psychological responses
- **Abuse deterrence messaging**: Loss-framed messages ("Abusing our return policy may result in account restrictions") tend to be more effective than gain-framed messages ("Following our return policy ensures uninterrupted service") because loss aversion makes the negative consequence more psychologically impactful
- **Decision presentation for investigators**: How abuse signals are presented to human reviewers can frame their judgment. Presenting the same data as "this customer has had 15 returns in 6 months" vs. "this customer has kept 85% of orders" activates different investigative mindsets

### Public Health and Communication

- **Vaccination messaging**: Gain-framed messages ("Vaccination protects your family") tend to be more effective for promotion behaviors, while loss-framed messages ("Not vaccinating puts your family at risk") are more effective for detection/prevention behaviors
- **Nutritional labeling**: "95% fat-free" vs. "5% fat" labeling systematically affects consumer perception of healthiness

### Negotiation and Persuasion

- Experienced negotiators frame concessions as gains ("I'm offering you X") rather than emphasizing what the other party must give up
- Presenting a discount as "save $50" vs. "price reduced from $250 to $200" activates different reference points

### Countermeasures

- **Rephrase the problem in multiple frames**: Before deciding, restate the options in both gain and loss terms and check whether your preference changes
- **Use joint evaluation**: Present options side by side rather than one at a time to reduce framing vulnerability
- **Require quantitative representation**: Translate qualitative descriptions into numbers (percentages, absolute values) to strip away valence framing
- **Awareness training**: Simply knowing about framing effects provides partial (though incomplete) protection

## Criticisms and Limitations

- **Replication variability**: While the framing effect is one of the most robust findings in behavioral science, the magnitude varies considerably across studies. Some replications of the Asian disease problem have found smaller effects than the original, though the direction is consistent
- **Individual differences**: Not everyone is equally susceptible to framing. People with higher numeracy, higher need for cognition, and greater deliberative thinking style show reduced framing effects
- **Ecological validity**: Some critics argue that the lab-based scenarios (e.g., the Asian disease problem) are artificial and that people may be less susceptible to framing in high-stakes, familiar, real-world decisions
- **Normative ambiguity**: While framing violates the invariance axiom, some philosophers argue that gain and loss frames carry genuinely different normative information (about responsibility, agency, and moral context) and that responding differently to them may sometimes be rational

## Related Terms

- [Term: Cognitive Bias](term_cognitive_bias.md) -- framing is one of the most well-documented cognitive biases
- [Term: Prospect Theory](term_prospect_theory.md) -- the theoretical foundation explaining why framing effects occur
- [Term: Loss Aversion](term_loss_aversion.md) -- the asymmetric weighting of losses vs. gains that drives framing's power
- [Term: System 1 and System 2](term_system_1_and_system_2.md) -- framing exploits System 1's automatic emotional responses
- [Term: Anchoring](term_anchoring.md) -- the frame functions as an anchor that shapes subsequent evaluation
- [Term: WYSIATI](term_wysiati.md) -- people respond to the frame presented without spontaneously generating alternative frames
- [Term: Availability Heuristic](term_availability_heuristic.md) -- gain frames and loss frames activate different memories and associations
- [Term: Planning Fallacy](term_planning_fallacy.md) -- the inside view is an optimistically framed perspective on a project
- [Term: Peak-End Rule](term_peak_end_rule.md) -- memory of experiences is "framed" by peak and end moments
- [Term: Socratic Questioning](term_socratic_questioning.md) -- systematic questioning can reveal hidden framing assumptions
- [Term: Question Storming](term_question_storming.md) -- reframing problems through questions counters default framing
- [Term: Design Thinking](term_design_thinking.md) -- empathy-driven reframing is a core technique in design thinking
- [Term: MECE](term_mece.md) -- structured decomposition resists the influence of arbitrary frames
- [Choice Architecture](term_choice_architecture.md) -- framing is a core mechanism of choice architecture; how options are presented determines which frame people adopt
- [Logical Fallacies](term_logical_fallacies.md) — framing creates the conditions for false dilemmas and appeals to emotion

## References

- [Tversky, A. & Kahneman, D. (1981). The Framing of Decisions and the Psychology of Choice. *Science*, 211(4481), 453-458](https://en.wikipedia.org/wiki/Framing_effect_(psychology)) -- the foundational paper introducing the Asian disease problem
- [Wikipedia: Framing Effect (Psychology)](https://en.wikipedia.org/wiki/Framing_effect_(psychology)) -- comprehensive overview of types, research, and applications
- [The Decision Lab: Framing Effect](https://thedecisionlab.com/biases/framing-effect) -- practical explanation with examples
- [Johnson, E.J. & Goldstein, D. (2003). Do Defaults Save Lives? *Science*, 302(5649), 1338-1339](https://www.science.org/doi/10.1126/science.1091721) -- landmark study on organ donation defaults
- [Thaler, R.H. & Sunstein, C.R. (2008). *Nudge: Improving Decisions About Health, Wealth, and Happiness*. Yale University Press](https://en.wikipedia.org/wiki/Choice_architecture) -- popularized the application of framing to choice architecture
- Source: [Digest: Thinking, Fast and Slow](../digest/digest_thinking_fast_and_slow_kahneman.md)

---

**Last Updated**: March 7, 2026
**Status**: Active -- behavioral economics terminology
