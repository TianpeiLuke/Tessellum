---
tags:
  - resource
  - template
  - empirical_observation
keywords:
  - empirical observation template
  - measurement template
  - evidence template
  - inline observation
topics:
  - Note Format
  - Templates
language: markdown
date of note: 2026-05-10
status: template
building_block: empirical_observation
folgezettel: ""              # if part of an FZ trail
folgezettel_parent: ""       # usually the FZ ID of the hypothesis or argument this observation tests
---

<!--
NOTE ON FOLGEZETTEL FIELDS:
An observation is most often a child of a `hypothesis` (the hypothesis it
tests — Testing-and-Evidence edge in the BB ontology) or an `argument`
(observation provides evidence for the argument's claim). Set
`folgezettel_parent:` to that upstream parent's FZ ID.

Inline thought-trail observations (this template) live in
`vault/resources/analysis_thoughts/`. For full pre-registered investigations
that warrant their own archive note, use `template_experiment.md` instead
(those live in `vault/archives/experiments/` with `tags[0]: archive`).

Non-trail observations (rare) omit both FZ fields.
-->


# Observation: <What Was Measured, Headline Result>

<!--
HOW TO USE THIS TEMPLATE:
1. Copy to:
   - `vault/resources/analysis_thoughts/thought_<topic>.md` (in-flight observations)
   - `vault/archives/experiments/experiment_<topic>.md` (completed experiments)
2. If part of a Folgezettel trail, add `folgezettel:` and `fz_parent:`.
3. Update YAML — tags[1] is usually `analysis` or `experiment`.
4. Fill required sections: Observation, Method, Result, References.
5. Remove this commentary block.

EPISTEMIC FUNCTION (Testing): an empirical observation records what happened
when something was measured. It answers "What happened?" An observation tests
a hypothesis by providing evidence. Without observations, hypotheses can't
become arguments and counters can't ground their refutations.

Observations should be reproducible. Capture method + result so a future
reader could either replicate the test or assess its validity.
-->

## Overview

<One paragraph: what was tested, why, and what the headline result was. This
is the section a reader uses to decide whether to read further.>

## Hypothesis Tested

<The specific hypothesis this experiment was designed to support or refute.
Link to the hypothesis note if it exists as a separate note.>

> **H**: <state the hypothesis precisely, in one sentence>.

This was authored as: <Hypothesis Title> (if separate)

## Observation

<One sentence + headline number. State what was measured and the result, in a
form a reader can extract in 5 seconds.>

> **Result**: <metric> = <value> (<unit>) on <dataset/condition> at <date>.
> **Verdict**: <SUPPORTS / REFUTES / PARTIAL / INDETERMINATE> the hypothesis above.

## Setup

<Pre-experiment configuration. State the inputs, instruments, and conditions
that hold throughout the experiment. This is what a replicator needs to set up
before running.>

**Inputs**:
- <dataset / condition>
- <parameter settings>

**Instruments**: <what tools / scripts / models did the measurement>

**Sample size**: <n>

**Controls**: <what was held constant>

## Expected Results (Pre-Registration)

<Optional but strongly recommended for principled experiments. State BEFORE
the experiment runs what would constitute success vs failure. Pre-registration
prevents post-hoc rationalization of unexpected outcomes.>

**If hypothesis is true, we expect**:
- <observable outcome 1>
- <observable outcome 2>

**If hypothesis is false, we expect**:
- <observable outcome 1>

**Pre-registered decision rule**: <if metric > T, conclude X; if metric < T, conclude Y; otherwise INDETERMINATE>

## How to Run

<The executable form of the experiment. A reader should be able to follow these
steps and either replicate the result or run a related experiment.>

```bash
# Step-by-step commands
```

**Estimated runtime**: <duration>
**Estimated cost**: <if LLM API calls or compute charges apply>

## Result

<The measurement(s). Tables work well here. Distinguish primary metrics
(load-bearing for the verdict) from secondary metrics (context).>

### Primary Metric

| Metric | Value | Baseline / Comparator | Δ |
|---|---|---|---|
| <metric name> | <value> | <baseline value> | <difference> |

### Secondary Metrics

| Metric | Value | Notes |
|---|---|---|
| <metric> | <value> | <context> |

### Statistical Significance

<If applicable. State p-value, confidence interval, effect size. State the test
used. State the null hypothesis that was rejected.>

- **Test**: <test name>
- **p-value**: <value>
- **CI**: <interval>
- **Effect size**: <metric and value>

## Interpretation

<What does this mean? Distinguish what the data show from what you infer.>

**The data show**: <a strict description of what was measured>

**This implies**: <your interpretation, with appropriate hedging>

**Limitations**:
- <what the observation cannot tell us>
- <known confounders>

## Verdict

<Did this observation support, refute, or partially confirm a hypothesis?
Be explicit. Link to the hypothesis note.>

| Hypothesis tested | Verdict |
|---|---|
| <hypothesis title> | <SUPPORTS / REFUTES / PARTIAL / INDETERMINATE> |

## References

- Hypothesis tested
- Method's source — if the procedure was defined elsewhere
- Related observation — for cross-reference
