---
tags:
  - resource
  - terminology
  - cognitive_science
keywords:
  - WYSIATI
  - What You See Is All There Is
  - cognitive completeness
  - coherence
  - System 1
  - Kahneman
  - jumping to conclusions
  - information neglect
  - overconfidence
  - narrative construction
topics:
  - cognitive psychology
  - decision making
  - judgment under uncertainty
  - behavioral economics
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: WYSIATI (What You See Is All There Is)

## Definition

**WYSIATI** is an acronym coined by Daniel Kahneman in *Thinking, Fast and Slow* (2011) standing for **"What You See Is All There Is."** It describes the fundamental tendency of System 1 -- the fast, automatic, intuitive mode of thinking -- to construct the most coherent narrative possible from whatever information happens to be available, without stopping to consider what information might be *missing*. When System 1 builds a story, it uses only the evidence currently at hand and treats that evidence as if it were the complete picture. The result is a subjective sense of confidence and coherence that bears little relationship to the actual quality or quantity of the underlying evidence.

WYSIATI is arguably the most foundational of the cognitive biases catalogued by Kahneman, because it underlies and enables many other biases. Overconfidence arises because people do not notice what they do not know. The anchoring effect works because the anchor is the available information and nothing else is considered. The availability heuristic operates because what comes to mind easily is treated as all there is. Confirmation bias persists because people build coherent stories from the evidence they have already found, without seeking disconfirming evidence. In Kahneman's framework, WYSIATI is not just one bias among many -- it is the meta-bias that makes most other biases possible.

The concept is introduced in Chapter 7 of *Thinking, Fast and Slow* ("A Machine for Jumping to Conclusions") and recurs throughout the book as a unifying explanatory principle. Kahneman describes WYSIATI as the reason that "the confidence that individuals have in their beliefs depends mostly on the quality of the story they can tell about what they see, even if they see little." System 2 (the slow, deliberate mode) can in principle question the completeness of the evidence, but it is cognitively lazy and typically endorses whatever coherent story System 1 has constructed.

## Full Name

- **WYSIATI**: What You See Is All There Is
- Kahneman's original coinage; the acronym appears throughout *Thinking, Fast and Slow*
- Related concept: **coherence-based reasoning** -- the tendency to seek narrative consistency
- Contrast with: **actively open-minded thinking** (Jonathan Baron) -- deliberately seeking information that could disconfirm the current narrative

## Core Mechanisms

### How WYSIATI Operates

WYSIATI works through a three-step process that is largely automatic and unconscious:

1. **Information acquisition**: System 1 rapidly gathers whatever information is immediately available -- from the current stimulus, from recent memory, from primed associations. It does not conduct a systematic search for relevant information.

2. **Story construction**: System 1 builds the most coherent narrative it can from the available fragments. Coherence, not completeness, is the criterion. A good story is one where the pieces fit together, not one where all relevant pieces have been considered.

3. **Confidence assignment**: The confidence attached to the resulting judgment is determined by the *coherence* of the constructed story, not by the *amount* of evidence supporting it. This is why people can be highly confident based on very little information -- a small amount of consistent evidence produces a very coherent (and therefore confident) judgment.

### The Coherence Illusion

| Feature of WYSIATI | Description | Consequence |
|---------------------|-------------|-------------|
| **Incomplete evidence** | System 1 works with whatever is available | Critical information may be overlooked entirely |
| **Coherence over completeness** | Internal consistency of the story matters more than evidence breadth | A single compelling anecdote can outweigh a dataset |
| **No "missing data" warning** | System 1 does not flag the absence of evidence | People do not spontaneously ask "What am I NOT seeing?" |
| **Confidence from coherence** | Confidence scales with narrative quality, not evidence quality | Small samples that tell a clear story produce overconfidence |
| **Lazy System 2** | System 2 could question completeness but usually does not | The coherent story is accepted by default |

### WYSIATI as a Meta-Bias

WYSIATI enables or amplifies virtually every other cognitive bias in Kahneman's catalog:

- **Overconfidence**: Because people do not notice what they do not know, they are systematically more confident than their evidence warrants
- **Anchoring**: The anchor is the available information; WYSIATI prevents spontaneous adjustment beyond the anchor
- **Availability heuristic**: What comes to mind easily is treated as all there is; no correction for what did not come to mind
- **Confirmation bias**: The story built from existing evidence feels complete; there is no felt need to seek disconfirming data
- **Framing effects**: The frame presented is the available information; alternative frames are not spontaneously generated
- **Narrative fallacy**: WYSIATI drives the construction of coherent post-hoc narratives from random events
- **Halo effect**: A single positive trait (available information) colors judgment of all other traits (missing information is filled in consistently)
- **Planning fallacy**: The inside view focuses on the specific case at hand (what is visible) while ignoring base rates (what is not visible)

## Key Research and Evidence

### Kahneman's "Jumping to Conclusions" Experiments

In *Thinking, Fast and Slow* (Chapter 7), Kahneman describes the "jumping to conclusions" (JTC) phenomenon with several demonstrations:
- When given a one-sided description of a person (e.g., "Alan: intelligent, industrious, impulsive, critical, stubborn, envious"), people form a strong impression without asking whether the description is complete or biased. The order of traits matters enormously (primacy effect), and people do not consider what traits might be missing.
- In the "Is Sam friendly?" experiment, people who are asked whether Sam is friendly search their memory for evidence of friendliness and, finding some, conclude that Sam is indeed friendly. People asked "Is Sam unfriendly?" search for unfriendliness and reach the opposite conclusion. Neither group considers the question they were not asked.

### The One-Sided Evidence Effect

Kahneman describes experiments in which subjects were given only one side of a legal case and asked to judge the verdict. Subjects who heard only the plaintiff's case were confident the plaintiff should win; subjects who heard only the defendant's case were confident the defendant should win. Neither group adjusted their confidence to account for the fact that they had heard only one side.

### The CIA and Intelligence Analysis

Richards Heuer, in *Psychology of Intelligence Analysis* (1999, CIA Center for the Study of Intelligence), identified WYSIATI-like phenomena as a central challenge in intelligence work. Analysts tend to construct coherent narratives from the intelligence available to them without adequately considering what intelligence might be missing or deliberately withheld. Heuer's "Analysis of Competing Hypotheses" (ACH) methodology is explicitly designed as a counter-WYSIATI tool.

## Practical Applications

### Abuse Prevention and Fraud Detection

WYSIATI has direct implications for abuse prevention:
- **Investigator bias**: When reviewing a buyer's history, investigators may construct a coherent abuse narrative from the available signals (high return rate, pattern of claims) without considering what might be missing -- legitimate reasons for returns, changes in life circumstances, or data gaps in the system
- **Model design**: Machine learning models trained on available features are inherently WYSIATI-prone -- they can only use what is in the feature set. Deliberately engineering features that capture "what is missing" (e.g., absence of expected behavior, gaps in activity) can counteract this
- **Policy decisions**: When designing abuse prevention policies, decision-makers may anchor on the most recent or most visible abuse type without considering the full landscape of abuse modalities

### Knowledge Management and the Vault

WYSIATI directly motivates several design features in the Zettelkasten/SlipBox approach:
- **Ghost notes** (placeholder notes for concepts not yet documented) make the absence of knowledge *visible*, counteracting WYSIATI
- **Broken link detection** (`slipbox-check-broken-links`) systematically surfaces what is missing from the knowledge graph
- **Multi-tier relevance analysis** (`slipbox-analyze-term-relevance`) deliberately explores beyond the immediately available Tier 1 connections through Tiers 2-5, forcing consideration of more distant (and therefore less "available") knowledge

### Decision Hygiene Practices

Kahneman and colleagues (in *Noise: A Flaw in Human Judgment*, 2021) recommend several counter-WYSIATI practices:
- **Structured decision-making**: Use checklists and protocols that require consideration of specific categories of evidence, preventing omission of non-salient factors
- **Devil's advocate**: Assign someone to argue the opposing case, making alternative evidence visible
- **Premortem**: Before committing to a decision, imagine it has failed and ask "Why?" -- this surfaces risks that WYSIATI would otherwise hide
- **Actively ask**: "What am I NOT seeing? What evidence would change my mind?"

## Criticisms and Limitations

- **Descriptive rather than predictive**: WYSIATI is a powerful explanatory concept but is difficult to operationalize as a precise, testable hypothesis. It describes a tendency rather than specifying exact conditions under which it occurs
- **Adaptive value**: In many everyday situations, acting quickly on available information is adaptive. The cognitive cost of exhaustively searching for missing information would be prohibitive for routine decisions. WYSIATI is only problematic for high-stakes decisions where completeness matters
- **Overlap with other constructs**: WYSIATI overlaps substantially with confirmation bias, the anchoring effect, and the narrative fallacy. Some critics argue it is more of a meta-narrative than a distinct cognitive mechanism
- **Debiasing difficulty**: Even knowing about WYSIATI does not reliably prevent it. Kahneman himself acknowledged that awareness of biases does not eliminate them -- "you cannot eliminate biases, but you can design around them"

## Related Terms

- [Term: System 1 and System 2](term_system_1_and_system_2.md) -- WYSIATI is a core property of System 1's automatic processing
- [Term: Cognitive Bias](term_cognitive_bias.md) -- WYSIATI is the meta-bias that enables most other biases
- [Term: Availability Heuristic](term_availability_heuristic.md) -- what comes to mind easily is treated as all there is
- [Term: Anchoring](term_anchoring.md) -- the anchor is the available information; WYSIATI prevents adjustment
- [Term: Framing Effect](term_framing_effect.md) -- the presented frame is the available information
- [Term: Prospect Theory](term_prospect_theory.md) -- reference dependence reflects WYSIATI applied to the status quo
- [Term: Loss Aversion](term_loss_aversion.md) -- losses are more salient, making them disproportionately "available"
- [Term: Planning Fallacy](term_planning_fallacy.md) -- the inside view is a WYSIATI-driven focus on visible specifics
- [Term: Peak-End Rule](term_peak_end_rule.md) -- the remembering self uses only peak and end (available moments), ignoring duration
- [Term: Socratic Questioning](term_socratic_questioning.md) -- disciplined questioning that surfaces hidden assumptions and missing evidence
- [Term: Elaborative Interrogation](term_elaborative_interrogation.md) -- asking "why?" and "how?" forces consideration of evidence beyond what is immediately available
- [Term: MECE](term_mece.md) -- Mutually Exclusive, Collectively Exhaustive frameworks counteract WYSIATI by ensuring completeness
- [Term: Design Thinking](term_design_thinking.md) -- empathy and user research deliberately surface evidence the designer would not otherwise see
- [Term: Systems Thinking](term_systems_thinking.md) -- holistic analysis counteracts WYSIATI's tendency to focus on visible parts
- [Open Loops](term_open_loops.md) -- partial capture is WYSIATI applied to task management: the mind treats whatever commitments it can recall as "all there is"
- [Trusted System](term_trusted_system.md) -- a trusted system counteracts WYSIATI by making all commitments visible, not just the ones currently in awareness
- [Progressive Summarization](term_progressive_summarization.md) — counteracts WYSIATI by making the most important information the most visible
- [Logical Fallacies](term_logical_fallacies.md) — WYSIATI enables straw man (evaluating only the presented version) and false dilemma (considering only visible options)
- [Groupthink](term_groupthink.md) — groupthink's information filtering ensures the group evaluates only the visible, confirming evidence — a social amplifier of WYSIATI
- [Critical Thinking](term_critical_thinking.md) — critical thinking directly counteracts WYSIATI by asking "What information is missing?" — the most fundamental critical thinking question

## References

- [Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.](https://www.amazon.com/Thinking-Fast-Slow-Daniel-Kahneman/dp/0374275637) -- Chapter 7 introduces WYSIATI; the concept recurs throughout the book
- [Wikipedia: Thinking, Fast and Slow](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow) -- overview of the book including WYSIATI's role
- [Shortform: What You See Is All There Is (WYSIATI)](https://www.shortform.com/blog/what-you-see-is-all-there-is/) -- accessible explanation with practical examples
- [The Decision Lab: System 1 and System 2 Thinking](https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking) -- framework context for WYSIATI
- [LitCharts: WYSIATI Analysis in Thinking, Fast and Slow](https://www.litcharts.com/lit/thinking-fast-and-slow/terms/what-you-see-is-all-there-is-wysiati) -- literary analysis of the concept's role in the book
- Source: [Digest: Thinking, Fast and Slow](../digest/digest_thinking_fast_and_slow_kahneman.md)

---

**Last Updated**: March 7, 2026
**Status**: Active -- cognitive science terminology
