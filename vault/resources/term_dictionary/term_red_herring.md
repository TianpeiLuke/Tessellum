---
tags:
  - resource
  - terminology
  - critical_thinking
  - argumentation
  - logical_fallacies
keywords:
  - red herring
  - ignoratio elenchi
  - irrelevant conclusion
  - changing the subject
  - misdirection
  - non sequitur
  - smoke screen
topics:
  - critical thinking
  - argumentation
  - analytical reasoning
language: markdown
date of note: 2026-03-12
status: active
building_block: concept
---

# Term: Red Herring

## Definition

A **red herring** is a logical fallacy that introduces an **irrelevant topic** to divert attention from the original issue, making the audience forget or abandon the original argument. The name derives from the practice of using smoked herring (which turns red and has a strong scent) to train hunting dogs -- or, apocryphally, to throw them off a trail. In argumentation, the red herring works by redirecting the discussion to a topic that may be interesting or emotionally engaging but is **logically irrelevant** to the claim under evaluation.

Red herrings are particularly effective in **group settings** where the conversation's direction is hard to track and revisit. In a meeting, once attention has shifted to a new topic, the social cost of saying "Let's go back to the original point" is high -- and the longer the digression continues, the harder it becomes to recover the thread. "The model accuracy is low, but look at how fast inference is" redirects from the accuracy concern to a different (possibly irrelevant) metric; the audience may leave the discussion believing the model is acceptable because inference speed is impressive, even though the original concern was never addressed.

The fallacy exploits **attention as a scarce resource** -- once redirected, the original point is often lost. This connects to Kahneman's concept of **WYSIATI** ("What You See Is All There Is"): the new topic displaces the original in working memory, and people evaluate whatever is currently in front of them rather than tracking what was previously under discussion. The red herring is the master fallacy of distraction; several other fallacies (tu quoque, appeal to emotion, whataboutism) are specific subtypes that achieve their effect through the red herring mechanism.

## Full Name

**Red Herring** (also known as: *ignoratio elenchi* [irrelevant conclusion], misdirection, smoke screen, changing the subject, *non sequitur* [in informal usage])

Related but distinct terms:
- **Ignoratio elenchi** -- Aristotle's original term for proving a conclusion irrelevant to the issue at hand
- **Non sequitur** -- literally "it does not follow"; sometimes used interchangeably, though *non sequitur* more precisely refers to a conclusion that does not follow from its premises
- **Whataboutism** -- a political variant: deflecting criticism by raising a different issue ("What about X?")

## Logical Structure

The invalid reasoning pattern:

> Premise: Claim X is under discussion
> Move: Topic Y is introduced (Y is irrelevant to X)
> Effect: Discussion shifts to Y
> Result: X is abandoned without resolution
> **Invalid because**: Y's truth, interest, or importance has no bearing on the truth of X

## Examples

| Context | Fallacious Argument | The Original Issue (Abandoned) |
|---------|-------------------|-------------------------------|
| **Meeting** | "Our latency numbers are concerning, but I want to highlight the team's great work on the UI redesign" | Latency was never addressed; the compliment redirected attention |
| **Data analysis** | "The model accuracy is low, but look at how fast inference is" | Accuracy was the issue; inference speed is a different metric |
| **Policy debate** | "We should discuss the abuse rate increase" -- "But our customer satisfaction scores are at an all-time high" | Abuse rate increase was never examined; CSAT is a different dimension |
| **Code review** | "This function has a race condition" -- "Well, the whole module needs refactoring anyway" | The race condition was never resolved; the broader refactor is a separate concern |

## Detection and Countermeasures

| Strategy | How It Works | Socratic Question |
|----------|-------------|-------------------|
| **Track the original claim** | Explicitly name and record the issue under discussion before evaluating new topics | "Let's return to the original question: [restate X]" |
| **Use written agendas** | In meetings, maintain a written agenda and parking lot for off-topic items | "This is interesting -- let's add it to the parking lot and come back to [X]" |
| **Name the diversion** | Politely identify that the topic has shifted | "How does this relate to the issue we were discussing?" |
| **Demand resolution before moving on** | Insist that the original claim be resolved (affirmed, refuted, or tabled) before new topics are introduced | "Before we discuss Y, can we first reach a conclusion on X?" |
| **Apply Socratic questioning (Type 1)** | Use clarification questions to reconnect the new topic to the original | "Can you help me understand how Y relates to X?" |

## Relationship to Cognitive Biases

Red herrings exploit several well-documented cognitive biases:

| Bias | Mechanism in This Fallacy |
|------|--------------------------|
| **Attention as scarce resource** | Redirected attention is hard to recover; working memory is limited |
| **WYSIATI** | The new topic displaces the original; people evaluate only what is currently salient |
| **Narrative fallacy** | The new topic often provides a more engaging or coherent story than the original issue |
| **Recency bias** | The most recently discussed topic feels more important than earlier ones |

## Related Terms

- [Logical Fallacies](term_logical_fallacies.md) -- parent term; red herring is classified as a fallacy of relevance
- [Appeal to Emotion](term_appeal_to_emotion.md) -- emotional diversion is a common red herring mechanism; triggering emotion redirects attention from the original claim
- [Appeal to Authority](term_appeal_to_authority.md) -- invoking authority can serve as a red herring that shifts discussion from evidence to status
- [Hasty Generalization](term_hasty_generalization.md) -- a vivid anecdote introduced as a red herring can lead to hasty generalization about the new topic
- [WYSIATI](term_wysiati.md) -- the new topic displaces the original in working memory; "What You See Is All There Is"
- [Cognitive Bias](term_cognitive_bias.md) -- attention, recency, and narrative biases that red herrings exploit
- [Socratic Questioning](term_socratic_questioning.md) -- clarification questions (Type 1) reconnect diverted discussions to the original issue
- [Five Whys](term_five_whys.md) -- iterative causal questioning keeps analysis anchored to the original problem

## References

- [Wikipedia: Red Herring](https://en.wikipedia.org/wiki/Red_herring) -- overview of the term's etymology, usage in argumentation, and literary tradition
- [Wikipedia: Ignoratio Elenchi](https://en.wikipedia.org/wiki/Ignoratio_elenchi) -- Aristotle's original formulation of the irrelevant conclusion fallacy
- Walton, D. (2004). Relevance in Argumentation. *Argumentation*, 18(2), 153-183. -- formal treatment of relevance and irrelevance in argument theory
- Aristotle. *Sophistical Refutations*, Ch. 5. -- the original taxonomy identifying irrelevant conclusions as a class of fallacy
- Source: [Digest: Critical Thinking Think Smarter](../digest/digest_critical_thinking_hartley.md) -- Hartley's treatment of relevance fallacies in argumentation
- Source: [Digest: Thinking, Fast and Slow](../digest/digest_thinking_fast_and_slow_kahneman.md) -- WYSIATI and attention as the cognitive mechanisms red herrings exploit

---

**Last Updated**: March 12, 2026
**Status**: Active -- critical thinking and logical fallacies terminology
