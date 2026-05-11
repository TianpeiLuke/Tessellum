---
tags:
  - resource
  - terminology
  - knowledge_management
  - zettelkasten
  - empiricism
keywords:
  - empirical observation
  - observation note
  - sensory data
  - evidence
  - measurement
  - experiment results
  - raw data
  - theory-ladenness
  - knowledge building block
topics:
  - Knowledge Management
  - Zettelkasten Method
  - Empiricism
  - Epistemology
language: markdown
date of note: 2026-03-29
status: active
building_block: concept
author: lukexie
---

# Term: Knowledge Building Blocks -- Empirical Observation

## Definition

An **Empirical Observation** is a knowledge building block that records the results of sensory engagement with reality. Observation notes capture what was seen, measured, counted, or otherwise experienced -- the raw evidential input to reasoning. In a Zettelkasten knowledge system, empirical observations serve as the ground-truth layer: they are the data points, metrics, experiment outcomes, and recorded events that premises draw upon and hypotheses are tested against. Without observations, arguments float unanchored; without arguments, observations remain uninterpreted.

The evidential role of observations places them at the foundation of the epistemic hierarchy. An observation note does not argue, conclude, or recommend -- it reports. The critical discipline is keeping the observation separate from the interpretation. When a metric drops by 15%, the observation note records the drop; a separate argument note explains why it dropped and what should be done. This separation is what makes observations reusable across multiple arguments. The same data point can serve as a premise in one argument and a counter-example in another, but only if the observation itself is recorded without argumentative coloring. In Sascha's expanded taxonomy, empirical observations are listed alongside hypotheses and arguments as a distinct building block type, reflecting the recognition that knowledge systems need raw evidence as a first-class citizen, not merely as footnotes within arguments.

## Historical Origin

The philosophical foundations of empirical observation as a distinct epistemic category span three centuries of debate about the relationship between experience and knowledge:

| Contributor | Work | Key Contribution |
|-------------|------|-------------------|
| **John Locke** | *An Essay Concerning Human Understanding* (1689) | Established **empiricism**: all knowledge derives from experience. The mind begins as a *tabula rasa*; sensory observation is the sole source of ideas. Legitimized observation as the foundation of knowledge. |
| **David Hume** | *A Treatise of Human Nature* (1739) | Identified the **problem of induction**: no finite set of observations can logically guarantee a universal conclusion. Observing $n$ white swans does not prove all swans are white. This limits what observations alone can establish. |
| **W.V.O. Quine** | "Two Dogmas of Empiricism" (1951) | Argued for **theory-ladenness**: observations are never purely neutral; what we notice and how we categorize it depends on our theoretical commitments. Pure observation is an ideal, not an achievable reality. |
| **Sascha Fast** | *The Complete Guide to Atomic Note-Taking* (2025) | Listed empirical observations as a building block type in the expanded taxonomy, giving observational knowledge first-class status in the Zettelkasten framework alongside arguments and hypotheses. |

The tension between Locke's foundationalism (observations ground everything) and Quine's holism (observations are theory-laden) remains unresolved. In practice, Zettelkasten note-takers navigate this tension by recording observations as cleanly as possible while acknowledging the interpretive frame through linked term and argument notes.

## Recognition Criteria

Your note is an empirical observation building block if it:

- Contains **recorded data** -- numbers, measurements, counts, percentages, or other quantitative values drawn from a specific source or event
- Reports **experiment results** -- outcomes of A/B tests, model evaluations, system benchmarks, or controlled comparisons
- Documents **observed events** -- things that happened at a specific time and place (launches, incidents, changes, announcements)
- Captures **metrics** -- KPIs, performance indicators, system health measures, or tracked values over time
- Records **sensory or system output** without interpretation -- what the dashboard showed, what the log said, what the user reported
- Can be summarized as "I/we observed X" rather than "I/we argue X" or "X should be done"

A useful test: if you remove all interpretation and recommendation from the note, does substantive content remain? If yes, the remaining content is the empirical observation.

## Writing Guide

A good empirical observation note should:

- **Lead with the observation** -- state what was measured, seen, or recorded before providing any context or interpretation
- **Include provenance** -- specify the source, date, methodology, and conditions under which the observation was made. An observation without provenance is an anecdote
- **Quantify where possible** -- prefer "precision dropped from 0.87 to 0.72 on the holdout set" over "precision got worse"
- **Separate observation from interpretation** -- if the note contains both data and an explanation of the data, split it. Link the observation note to an argument note that interprets it
- **Record negative results** -- observations that disconfirm a hypothesis are as valuable as confirmatory ones. Do not selectively record only what supports your current view
- **Use consistent units and formats** -- ensure metrics are comparable across observation notes by using standard units, time ranges, and measurement definitions
- **Tag the observation type** -- distinguish between experimental observations (controlled), operational observations (system metrics), and anecdotal observations (individual cases)

## Vault Examples

| Example Note | Why It Is an Empirical Observation |
|--------------|-------------------------------------|
| MTR (Monthly Ticket Review) notes in [entry_mtr_monthly_reviews.md](../../0_entry_points/entry_mtr_monthly_reviews.md) | Monthly reviews that record metrics like defect rates, false positive rates, and operational counts -- direct measurements of system performance. |
| Launch announcement notes in [entry_launch_announcements.md](../../0_entry_points/entry_launch_announcements.md) | Document observable events: what was launched, when, with what measured impact. The announcement records the fact; analysis notes interpret it. |
| SlipBot Q&A captures and oncall summaries in [entry_oncall_summaries.md](../../0_entry_points/entry_oncall_summaries.md) | Record what questions were asked, what issues occurred, and what was found during investigation -- raw operational observations. |

## Common Mistakes

- **Interpreting observations as arguments**: Writing "the false positive rate increased to 12%, which means the model is degrading" in a single note. The increase to 12% is the observation; the claim about model degradation is an argument that uses the observation as a premise. Separate them into two notes and link.
- **Mixing observation with conclusion**: Ending an observation note with "therefore we should retrain the model" conflates the evidential layer (what was observed) with the prescriptive layer (what should be done). The observation note should stop at the data; the recommendation belongs in an argument or procedure note.
- **Omitting provenance**: Recording "precision is 0.85" without specifying which model, which dataset, which time period, or which evaluation methodology. Without provenance, the observation cannot be compared, reproduced, or meaningfully cited.

## Related Terms

- **[Knowledge Building Blocks](term_knowledge_building_blocks.md)**: Parent term -- empirical observations are one of the building block types in Sascha's expanded taxonomy
- **[Argumentation](term_argumentation.md)**: Sibling block -- arguments consume observations as premises; observations without arguments are uninterpreted data
- **[Knowledge Building Blocks -- Hypothesis](term_knowledge_building_blocks_hypothesis.md)**: Sibling block -- hypotheses generate predictions that observations test
- **[Prescriptive Knowledge](term_prescriptive_knowledge.md)**: Contrasts with empirical observation: prescriptive knowledge says what to do; empirical observation says what is
- **[Propositional Knowledge](term_propositional_knowledge.md)**: Empirical observations are a subtype of propositional knowledge -- knowing-that claims grounded in experience
- **[Fleeting Notes](term_fleeting_notes.md)**: Raw observations often enter the vault as fleeting notes before being formalized into permanent observation notes

## References

### Vault Sources

- [Digest: Intellectual Roots of Knowledge Building Blocks](../digest/digest_intellectual_roots_knowledge_building_blocks.md) -- philosophical lineage including empiricist foundations

### External Sources

- Locke, J. (1689). *An Essay Concerning Human Understanding*. Thomas Bassett.
- Hume, D. (1739). *A Treatise of Human Nature*. John Noon.
- Quine, W.V.O. (1951). "Two Dogmas of Empiricism." *The Philosophical Review*, 60(1), 20-43.
- Sascha (2025). "The Complete Guide to Atomic Note-Taking." zettelkasten.de -- lists empirical observations as a building block type.
