---
tags:
  - resource
  - terminology
  - critical_thinking
  - argumentation
  - logical_fallacies
keywords:
  - straw man
  - straw man fallacy
  - misrepresentation
  - argument distortion
  - weak man
  - hollow man
  - iron man
topics:
  - critical thinking
  - argumentation
  - analytical reasoning
language: markdown
date of note: 2026-03-12
status: active
building_block: concept
---

# Term: Straw Man

## Definition

The **straw man fallacy** occurs when someone misrepresents an opponent's argument as a weaker or more extreme version, then refutes the distorted version instead of the actual claim. The name comes from the military practice of training against straw dummies rather than real opponents -- it is far easier to defeat an argument that no one actually made. The fallacy works because audiences evaluate only the version presented to them, exploiting **WYSIATI** ("What You See Is All There Is") -- if the audience never hears the original argument stated accurately, they accept the distorted version as genuine.

Three common forms of straw man exist: (1) **exaggeration** -- making the position more extreme than it actually is ("They want better testing" becomes "They think our code is garbage"), (2) **oversimplification** -- reducing a nuanced, multi-part position to a one-dimensional caricature, and (3) **fabrication** -- attributing a position the opponent never held at all. The straw man is especially dangerous in **written communication** (emails, documents, meeting notes) where the original arguer cannot immediately correct the misrepresentation, and where the distorted version may become the "official" record of their position.

The structural antidote to the straw man is the **steelman principle**: always represent opposing views in their strongest possible form before attempting to refute them. This discipline, rooted in the philosophical tradition of **charity of interpretation**, forces engagement with the actual argument rather than a convenient phantom.

## Full Name

- **Straw Man Fallacy** (primary term)
- Also called: **straw man argument**, **aunt sally** (British English)
- Variants: **weak man** (attacking the weakest proponent of a position rather than the strongest), **hollow man** (attacking a position no one holds)
- Contrast with: **steelman** (the opposite practice -- representing the strongest version of an opposing argument)

## Logical Structure

The invalid reasoning pattern:

1. Person A claims X
2. Person B distorts X into X' (a weaker, more extreme, or fabricated version)
3. Person B refutes X'
4. Person B concludes that X is refuted

**Why it is invalid**: X' is not X. Refuting a distorted version of an argument says nothing about the validity of the original argument.

## Examples

| Context | Straw Man Example | Actual Argument |
|---------|-------------------|-----------------|
| **Meeting** | "So you're saying we should stop all new development and only fix bugs?" | "I think we should allocate 20% of sprint capacity to reducing tech debt" |
| **Data analysis** | "They claim the model is useless and should be scrapped entirely" | "The model's precision drops significantly for edge cases and needs recalibration" |
| **Policy debate** | "Apparently they want zero enforcement -- just let every fraudster through" | "I'm proposing we raise the threshold from $10 to $25 to reduce false positives" |
| **Code review** | "This PR basically rewrites the entire service from scratch" | The PR refactors one module to improve testability while keeping the same interface |

## Detection and Countermeasures

| Strategy | Application |
|----------|-------------|
| **Quote the original** | Ask: "Is that what they actually said, or is that our interpretation?" -- go back to the source |
| **Apply the steelman principle** | Before refuting, restate the opposing view in its strongest form and confirm with the arguer |
| **Watch for intensifiers** | Words like "always," "never," "completely," "total" often signal exaggeration of the original position |
| **Demand accurate summary** | In meetings, ask the person to restate the original argument before critiquing it |
| **Document positions precisely** | In written contexts, use direct quotes and explicit attribution to prevent drift |

## Relationship to Cognitive Biases

The straw man exploits several cognitive mechanisms:

- **WYSIATI** (What You See Is All There Is) -- audiences evaluate only the version of the argument presented to them, without seeking the original
- **Confirmation bias** -- a distorted version that confirms the audience's existing skepticism is accepted uncritically
- **Cognitive ease** -- a simplified, extreme version is easier to process and evaluate than the nuanced original
- **Attribution substitution** -- System 1 substitutes "Is this distorted version wrong?" (easy question) for "Is the original argument valid?" (harder question)

## Related Terms

- [Logical Fallacies](term_logical_fallacies.md) -- parent taxonomy; straw man is classified as a fallacy of relevance
- [WYSIATI](term_wysiati.md) -- "What You See Is All There Is"; the bias straw man exploits most directly
- [Ad Hominem](term_ad_hominem.md) -- another fallacy that redirects from the actual argument, but attacks the person rather than distorting the claim
- [False Dilemma](term_false_dilemma.md) -- also constrains the argument space, presenting only two options instead of the full range
- [Slippery Slope](term_slippery_slope.md) -- can function as a straw man when it exaggerates the consequences of a proposal
- [Socratic Questioning](term_socratic_questioning.md) -- probing questions ("Is that what was actually claimed?") expose the distortion
- [Red Herring](term_red_herring.md) -- also diverts attention from the original argument, but by introducing an irrelevant topic rather than distorting the original
- [Argumentation](term_argumentation.md) -- the broader discipline; straw man violates the pragma-dialectical rule requiring faithful representation of the opponent's position

## References

- Source: [Digest: Critical Thinking Think Smarter](../digest/digest_critical_thinking_hartley.md) -- practical detection advice for informal fallacies
- [Wikipedia: Straw Man](https://en.wikipedia.org/wiki/Straw_man) -- comprehensive overview of forms, history, and examples
- Damer, T.E. (2009). *Attacking Faulty Reasoning* (6th ed.). Wadsworth -- standard reference on straw man and argument reconstruction
- Walton, D. (1996). "The Straw Man Fallacy." In *Logic and Argumentation*. Royal Netherlands Academy of Arts and Sciences -- formal analysis of misrepresentation in argumentation

---

**Last Updated**: March 12, 2026
**Status**: Active -- critical thinking and argumentation terminology
