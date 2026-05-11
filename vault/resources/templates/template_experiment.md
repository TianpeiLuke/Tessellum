---
tags:
  - archive
  - experiment
  - template
  - empirical_observation
keywords:
  - experiment template
  - pre-registered experiment
  - reproducible experiment
  - archived experiment
topics:
  - Note Format
  - Templates
language: markdown
date of note: 2026-05-10
status: template
building_block: empirical_observation
folgezettel: ""              # if part of an FZ trail; empty/absent otherwise
folgezettel_parent: ""       # if has a parent in the FZ trail; empty/absent otherwise
---

<!--
NOTE ON YAML:
- tags[0] = `archive` (NOT `resource`) — experiments live under `vault/archives/experiments/`,
  which is the PARA Archive bucket. Time-bounded investigations whose primary
  value is the result; not for ongoing maintenance.
- tags[1] = `experiment` — the second-category routing label.
- folgezettel + folgezettel_parent: fill in if this experiment is part of a
  Folgezettel trail (most experiments are children of an upstream argument
  or hypothesis). For trail-root experiments, set folgezettel_parent: null
  or omit the field. For non-trail one-off experiments, omit BOTH FZ fields.
-->


# Experiment: <Hypothesis Tested or Question Investigated>

<!--
HOW TO USE THIS TEMPLATE:
1. Copy to `vault/archives/experiments/experiment_<topic>.md`. Note: experiments
   live under `archives/` (not `resources/`) because they're time-bounded
   investigations whose primary value is the result, not ongoing maintenance.
2. Rename the file with the `experiment_` prefix.
3. Update YAML — tags[1] is `experiment`. Initial status: `active` while
   running, then `completed` (with the verdict in the body) when finished.
4. Fill all sections in order. The Pre-Registration sections (Hypothesis,
   Setup, Expected Results, Decision Rule) MUST be filled BEFORE the experiment
   runs — that's the load-bearing discipline.
5. After the experiment runs, fill Analysis, Verdict, and Limitations.
   Update status to `completed`.
6. Remove this commentary block.

EPISTEMIC FUNCTION (Testing): an experiment is a pre-registered empirical_observation —
it states the prediction + decision rule BEFORE measuring, then records the result
+ honest assessment AFTER. The pre-registration discipline is what distinguishes
science from rationalization.

This template is heavier than `template_empirical_observation.md`, which is for
inline observations embedded in research trails. Use this template when:
  - You're running a deliberate, time-bounded investigation
  - The result will inform a downstream decision
  - You want the experiment to be reproducible by someone else
  - The result is significant enough to deserve a dedicated archive note

Use `template_empirical_observation.md` instead when the observation is a
casual measurement embedded in a thought trail, or a corollary of a larger
investigation.
-->

## Overview

<One paragraph: what was tested, why this question matters, and what the
headline result was (or what it WILL be once run, in pre-registration form).
A reader should be able to tell within 10 seconds whether to read further.>

## Hypothesis Tested

<The specific, falsifiable hypothesis this experiment was designed to support
or refute. State it sharply enough that the experiment can give a clear
yes/no/indeterminate verdict.>

> **H**: <state precisely, in one sentence>.

**Target hypothesis note** (if separate): [<Hypothesis Title>](../../resources/analysis_thoughts/thought_hypothesis.md)

## Root Cause Connection

<Why does this hypothesis matter? What upstream argument or open question
motivated running this experiment? This section anchors the experiment in
the broader research trail; an experiment without a root-cause connection is
unmoored.>

This experiment serves: [<Argument or Question>](../../resources/analysis_thoughts/thought_upstream.md)

The argument needs this experiment because: <one-paragraph rationale>.

## Setup

<Pre-experiment configuration. Everything a replicator needs to set up before
running. State the inputs, instruments, sample size, and controls.>

**Inputs**:
- <dataset / corpus>
- <parameter settings>
- <starting state>

**Instruments**:
- <tool / script / model used to do the measurement>

**Sample size**: <n>, justified by: <why this is enough>

**Controls (held constant)**:
- <variable 1 = value>
- <variable 2 = value>

**Variables (manipulated or measured)**:
- <independent variable: how varied>
- <dependent variable: how measured>

## Expected Results (Pre-Registration)

<State BEFORE running what would constitute success vs failure. Pre-registration
prevents post-hoc rationalization. If the experiment surprises you, the
pre-registration is what tells you the surprise is real.>

**If hypothesis TRUE, we expect**:
- <observable outcome 1>
- <observable outcome 2>

**If hypothesis FALSE, we expect**:
- <observable outcome 1>

**Pre-registered decision rule**:

| Result | Verdict |
|---|---|
| <metric> ≥ <threshold T> | SUPPORTS hypothesis |
| <metric> < <threshold T> with effect size > <ε> in opposite direction | REFUTES hypothesis |
| <other condition> | INDETERMINATE / requires follow-up |

## How to Run

<The executable form of the experiment. A reader should be able to follow these
steps and replicate the result. Aim for copy-pasteable commands.>

```bash
# Step 1: <action>
<command>

# Step 2: <action>
<command>

# Step 3: <action>
<command>
```

**Estimated runtime**: <duration>
**Estimated cost**: <if LLM API calls or compute charges apply>
**Output location**: <where results land>

---

<!-- The sections BELOW are filled AFTER the experiment runs. -->

## Result

<The actual measurement. Tables are the right format here. Distinguish primary
metrics (load-bearing for the verdict) from secondary metrics (context).>

### Primary Metric

| Metric | Value | Pre-Registered Threshold | Pass? |
|---|---|---|---|
| <metric name> | <value> | <threshold> | ✅ / ❌ |

### Secondary Metrics

| Metric | Value | Notes |
|---|---|---|
| <metric> | <value> | <context> |

### Statistical Significance

- **Test**: <test name>
- **Sample size**: <n>
- **p-value**: <value>
- **Confidence interval**: <CI>
- **Effect size**: <metric and value>

## Analysis

<What does the result mean? Distinguish what the data show from what you infer.>

**The data show**: <strict description of what was measured, no interpretation>

**This implies**: <your interpretation, with appropriate hedging>

**Surprises**: <anything unexpected — these are the most valuable findings>

**Mechanism**: <if the result is surprising, what's the proposed explanation?
This often becomes a follow-up hypothesis.>

## Verdict

<Did the experiment confirm, refute, or partially answer the hypothesis?
Quote the pre-registered decision rule and apply it directly. Be honest —
"close to the threshold" is not a pass.>

| Hypothesis | Pre-Registered Threshold | Observed | Verdict |
|---|---|---|---|
| <hypothesis> | <threshold> | <value> | **<SUPPORTS / REFUTES / PARTIAL / INDETERMINATE>** |

**Decision implication**: <if the hypothesis was a precondition for a downstream
decision, what does the verdict mean for that decision?>

## Limitations

<Honest assessment of what this experiment cannot tell you. List confounds,
threats to validity, scope limitations. The strongest experiments openly
document what they don't establish — this is what makes them trustworthy.>

- **Confound 1**: <variable that wasn't fully controlled and could explain the result>
- **Scope limitation**: <what the result does NOT generalize to>
- **Sample limitation**: <if applicable, why the sample may not represent the population>
- **Measurement limitation**: <known measurement noise or bias>

## Follow-Up Questions

<What does this experiment open up? List 2-4 follow-up hypotheses the result
suggests testing next. Often the most valuable output of an experiment isn't
the verdict — it's the next experiment.>

- <Follow-up Q1>
- <Follow-up Q2>

## References

- [Hypothesis tested](../../resources/analysis_thoughts/thought_hypothesis.md)
- [Upstream argument](../../resources/analysis_thoughts/thought_upstream.md)
- [Method's source](../../resources/how_to/howto_method.md) — if the procedure was defined elsewhere
- [Related experiment](experiment_other.md) — for cross-reference
