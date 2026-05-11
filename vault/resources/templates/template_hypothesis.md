---
tags:
  - resource
  - template
  - hypothesis
keywords:
  - hypothesis template
  - prediction template
  - falsifiable claim
  - pre-experiment hypothesis
topics:
  - Note Format
  - Templates
language: markdown
date of note: 2026-05-10
status: template
building_block: hypothesis
folgezettel: ""              # if part of an FZ trail
folgezettel_parent: ""       # if has a parent (e.g., the model that generated this hypothesis)
---

<!--
NOTE ON FOLGEZETTEL FIELDS:
A hypothesis is most often a child of either a `model` (the model predicts
this hypothesis — Predicting edge in the BB ontology) or an `argument` (the
argument leads to this testable prediction). Set `folgezettel_parent:` to
that upstream parent's FZ ID. The hypothesis itself usually becomes the
parent of an `empirical_observation` or `experiment` that tests it.

Trail-root hypotheses are valid (e.g., FZ 13 "PGHAM hypothesis") — in that
case set `folgezettel: "<root-id>"` and `folgezettel_parent: null`.
-->


# Hypothesis: <Falsifiable Prediction, Stated Sharply>

<!--
HOW TO USE THIS TEMPLATE:
1. Copy to `vault/resources/analysis_thoughts/thought_<topic>.md`.
2. If part of a Folgezettel trail, add `folgezettel:` and `fz_parent:`.
3. Update YAML — tags[1] is usually `analysis`.
4. Fill required sections: Hypothesis, Reasoning, Falsifiability, References.
5. Remove this commentary block.

EPISTEMIC FUNCTION (Predicting): a hypothesis note makes a falsifiable
prediction. It answers "What will happen next?" A hypothesis without
falsifiability criteria is broken — it must specify what observation would
prove it wrong.

A hypothesis becomes an argument when tested with evidence. The transition is
the testing-and-evidence edge in the BB ontology.
-->

## Hypothesis

<One sentence. The hypothesis is a specific, testable prediction. It should
take the form "If X, then Y" or "X causes Y" or "X > Y by Δ" — something
sharp enough that a future observation can confirm or refute it.>

> Hypothesis: <state it precisely, in one sentence>.

## Reasoning

<Why do you predict this? What model or theory generates the prediction?
Hypothesis without reasoning is a wild guess; reasoning makes it a *principled*
prediction worth testing.>

The hypothesis follows from:

1. **Premise / Model**: <what assumption or model generates the prediction>
2. **Mechanism**: <the causal path from premise to predicted outcome>
3. **Therefore**: <the prediction>

## Falsifiability

<What observation would prove this hypothesis WRONG? Be specific. "It depends"
is not a falsifiability criterion. State the failing condition precisely.>

**This hypothesis is FALSIFIED if**:

- <Observation criterion 1: e.g., "metric X measured below threshold T">
- <Observation criterion 2: e.g., "intervention has no measurable effect at p < 0.05">

**This hypothesis is CONFIRMED if**:

- <Observation criterion: what would count as evidence in favor>

**This hypothesis is INDETERMINATE if**:

- <Conditions where the test wouldn't tell you anything>

## Test Design (Optional)

<If you have a specific experiment in mind, sketch it. The transition to an
empirical_observation note is downstream of this hypothesis — link forward when
the experiment runs.>

| Variable | Manipulation | Measurement |
|---|---|---|
| <independent var> | <how varied> | <baseline> |
| <dependent var> | — | <how measured> |

## Prior Evidence (Optional)

<If existing observations partially inform the hypothesis, cite them. This
distinguishes a *principled* prediction (reasoning + prior evidence) from a
hunch (reasoning only).>

- Related Observation — <how it informs>

## References

- Related Model — <the model this
  hypothesis derives from>
- Related Argument — <prior argument that motivated this
  hypothesis>
