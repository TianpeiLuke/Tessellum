---
tags:
  - resource
  - analysis
  - knowledge_management
  - building_blocks
  - question_analysis
  - methodology
  - measurement_validity
  - information_retrieval
keywords:
  - epistemic congruence
  - answer quality
  - building block mismatch
  - information need
  - slipbox-review-slipbot-answer
  - answerability
  - question demand
  - knowledge type alignment
  - construct validity
  - rating rubric
  - measurement instrument
topics:
  - Knowledge Management
  - Information Retrieval
  - Measurement Methodology
  - Question Analysis
language: markdown
date of note: 2026-04-20
status: active
building_block: argument
folgezettel: "5g3a"
folgezettel_parent: "5g3"
---

# Thought: Epistemic Congruence — The Missing Dimension in SlipBot Answer Review (FZ 5g3a)

## Thesis

> **The current `slipbox-review-slipbot-answer` skill measures whether an answer is *factually correct* but not whether it *satisfies the information need* behind the question. A factually correct answer in the wrong epistemological register is a failure that the current rubric cannot detect. We propose "epistemic congruence" as a complementary dimension that measures the alignment between the knowledge type delivered and the knowledge type demanded.**

## 1. The Problem: Correctness Without Satisfaction

### 1.1 What the Current Skill Measures

The `slipbox-review-slipbot-answer` skill (Step 4-5) evaluates answers on a single axis: **factual alignment with vault knowledge**. Each claim is checked as Correct/Incorrect/Unverifiable/Hallucinated. The 1-5 rating maps directly to claim accuracy:

| Rating | What It Captures |
|--------|-----------------|
| 5 | All claims verified correct |
| 4 | Core claims correct, minor omissions |
| 3 | Partially correct, gaps acknowledged |
| 2 | Key claims wrong |
| 1 | Actively incorrect |

This is a single-dimensional measurement: **answerability** (can we answer?) + **factual fidelity** (did we answer correctly?).

### 1.2 What It Misses

Consider these failure modes invisible to the current rubric:

| Question | Demand (BB) | Answer Delivered (BB) | Current Rating | Actual User Satisfaction |
|----------|-------------|----------------------|----------------|------------------------|
| "How do I investigate a DNR case?" | **procedure** (steps) | Concept definition of DNR | 4/5 (factually correct about DNR) | Low — user needed steps, got a definition |
| "What is the relationship between PFOC and AFN?" | **model** (system structure) | Procedure for configuring PFOC | 3/5 (partially correct, mentions PFOC) | Low — user needed architecture, got a how-to |
| "What are the metrics for RFS suppression in FE?" | **empirical_observation** (data) | Model description of RFS system | 3/5 (correct on system, gap on metrics) | Low — user needed numbers, got a diagram |
| "List all datastreams for concession abuse" | **navigation** (index/enumeration) | Concept note about concession abuse types | 4/5 (factually correct about abuse types) | Low — user needed a list, got an explanation |

In each case: the answer is factually correct *about something related* but fails to deliver *the type of knowledge the user actually needs*. The current rubric rewards correctness-about-anything; users need correctness-about-the-right-thing.

### 1.3 The Root Cause: Conflating Two Independent Quality Dimensions

Answer quality has (at minimum) two orthogonal dimensions:

```
                    Factual Correctness
                    Low ←──────────→ High
                     │                  │
                     │   Quadrant III   │   Quadrant IV
  Epistemic         │   Wrong type,    │   Right type,
  Congruence        │   wrong facts    │   wrong facts
  Low               │   (worst)        │   (misleading)
                     │                  │
                     ├──────────────────┤
                     │                  │
                     │   Quadrant II    │   Quadrant I
  Epistemic         │   Right type,    │   Right type,
  Congruence        │   wrong facts    │   right facts
  High              │   (promising)    │   (ideal)
                     │                  │
                    Low ←──────────→ High
```

The current skill only measures the horizontal axis. A Quadrant IV answer (right type of knowledge, but factually wrong) scores low despite understanding what the user needed. A Quadrant III answer (wrong type AND wrong facts) gets the same low score, obscuring *why* it failed. Crucially, a Quadrant II answer (right register, wrong details) scores the same as Quadrant III, despite being a fundamentally different — and more recoverable — failure.

---

## 2. Defining Epistemic Congruence

### 2.1 The Term

**Epistemic congruence**: the degree to which the *type of knowledge* provided in an answer matches the *type of knowledge* demanded by the question.

Etymologically: *epistemic* (relating to knowledge or knowing) + *congruence* (agreement in form or character). The answer's epistemological form agrees with the question's epistemological demand.

### 2.2 Operationalization

Epistemic congruence is determined by comparing two classifications:

1. **Question demand** (already established in FZ 5g1a, κ=0.711): What building block does the question seek? Annotate using the 5-type classification: `concept`, `procedure`, `model`, `empirical_observation`, `navigation`.

2. **Answer supply**: What building block does the answer actually deliver? Classify the answer's content by the same taxonomy.

**Congruence score**:

| Alignment | Score | Definition |
|-----------|-------|-----------|
| **Full congruence** | 1.0 | Answer delivers exactly the demanded building block type |
| **Partial congruence** | 0.5 | Answer delivers a related type that partially satisfies the need (e.g., `model` answer for `procedure` question — the architecture helps but doesn't give steps) |
| **Incongruence** | 0.0 | Answer delivers an unrelated type (e.g., `concept` definition for `navigation`/enumeration question) |

### 2.3 The Congruence Matrix

Not all mismatches are equally harmful. Some cross-type answers provide partial value:

| Question Demand → | concept | procedure | model | empirical_obs | navigation |
|-------------------|---------|-----------|-------|---------------|------------|
| **Answer: concept** | **1.0** | 0.0 | 0.5 | 0.0 | 0.0 |
| **Answer: procedure** | 0.0 | **1.0** | 0.5 | 0.0 | 0.0 |
| **Answer: model** | 0.5 | 0.5 | **1.0** | 0.0 | 0.5 |
| **Answer: empirical_obs** | 0.0 | 0.0 | 0.0 | **1.0** | 0.5 |
| **Answer: navigation** | 0.0 | 0.0 | 0.0 | 0.5 | **1.0** |

**Rationale for partial scores**:
- Model → concept (0.5): A system architecture description partially defines its components
- Model → procedure (0.5): Understanding how something works helps infer how to use it
- Model → navigation (0.5): Architecture notes often enumerate sub-components
- Empirical_observation → navigation (0.5): Metric summaries partially serve as enumeration
- Concept → model (0.5): A rich definition partially describes structure

All other off-diagonal pairings score 0.0: a definition cannot substitute for data, steps cannot substitute for enumerations, etc.

---

## 3. Proposed Combined Metric

### 3.1 The Two-Factor Rating

Replace the single 1-5 scalar with a two-dimensional assessment:

| Dimension | Question | Scale | Source |
|-----------|----------|-------|--------|
| **Factual fidelity** (F) | Are the claims in the answer correct? | 1-5 | Existing rubric (Steps 4-5 of current skill) |
| **Epistemic congruence** (E) | Does the answer provide the type of knowledge demanded? | 0.0, 0.5, or 1.0 | New: compare question BB demand vs answer BB supply |

### 3.2 Combined Score

```
Quality = F × (0.5 + 0.5 × E)
```

Where:
- F = factual fidelity (1-5, existing rating)
- E = epistemic congruence (0.0, 0.5, 1.0)
- Combined range: 0.5 to 5.0

**Interpretation**:
- Full congruence (E=1.0): Quality = F × 1.0 = F (factual score passes through unchanged)
- Partial congruence (E=0.5): Quality = F × 0.75 (25% penalty for type mismatch)
- Incongruence (E=0.0): Quality = F × 0.5 (50% penalty — even a perfect factual score is halved)

**Why multiplicative, not additive**: A factually correct answer in the wrong register (F=5, E=0) is fundamentally less useful than a factually correct answer in the right register (F=5, E=1). The multiplicative formulation ensures that even high factual scores are penalized for incongruence — matching the real-world user experience where "correct but unhelpful" is a genuine failure.

### 3.3 Worked Examples

| Q | Demand | Answer BB | F | E | Combined | Current Rating | Delta |
|---|--------|-----------|---|---|----------|---------------|-------|
| "How to investigate DNR?" | procedure | concept | 4 | 0.0 | 2.0 | 4 | **-2.0** |
| "What is UDV?" | concept | concept | 5 | 1.0 | 5.0 | 5 | 0 |
| "PFOC → AFN relationship?" | model | procedure | 3 | 0.5 | 2.25 | 3 | **-0.75** |
| "Metrics for RFS in FE?" | empirical_obs | model | 3 | 0.0 | 1.5 | 3 | **-1.5** |
| "How does AOC work?" | model | model | 5 | 1.0 | 5.0 | 5 | 0 |
| "List all DNR datastreams" | navigation | concept | 4 | 0.0 | 2.0 | 4 | **-2.0** |

The combined metric correctly identifies the "factually correct but wrong type" failures that the current rating misses. Questions where F and E align show no change; questions with type mismatch are appropriately penalized.

---

## 4. Implications for the FZ 5g Framework

### 4.1 Re-testing P1-P3 with the Combined Metric

The null results in experiments 5g1b (block count) and 5g1c (vault coverage) used single-axis F ratings as the dependent variable. If those ratings systematically over-scored incongruent answers (Quadrant III in Section 1.3), then:

- **P1 re-test**: Multi-block questions may genuinely be harder *when measured by combined quality* — their complexity creates more opportunities for type mismatch
- **P2/P3 re-test**: Vault coverage may predict combined quality even when it doesn't predict factual fidelity alone — a vault gap in `procedure` notes means procedure-demanding questions get concept answers (high F, low E)

### 4.2 The Retrieval Pipeline Interaction

The 89.5% retrieval failure rate (FZ 5e1b, LIMIT 10) creates a confound: when retrieval fails, both F and E are low (the answer is wrong about wrong things). Epistemic congruence becomes most diagnostic **when retrieval partially succeeds** — i.e., the system finds *some* relevant notes, but of the wrong building block type.

**Hypothesis**: Among the 10.5% of questions where retrieval succeeds (gold note in top-10), epistemic congruence will explain the residual variance in user satisfaction that factual fidelity alone cannot.

### 4.3 Practical Skill Improvement

A building-block-aware reviewer could:
1. **Detect the mismatch** before rating: "This question demands a `procedure` but the retrieved note provides a `concept`"
2. **Route remediation differently**: Type mismatch failures need different fixes than factual failures — not "correct the facts" but "find a different type of note"
3. **Inform retrieval strategy selection**: If the system knows the question demands a `procedure`, it can prefer `sop_*` and `how_to_*` notes over `term_*` notes during retrieval

---

## 5. Proposed Validation: Sub-Sample Re-Review

### 5.1 Study Design

Re-review a stratified sub-sample of 30 SlipBot questions from the existing archive using the two-factor rubric:

| Stratum | Selection | n | Rationale |
|---------|-----------|---|-----------|
| **High F, suspected low E** | Current rating 3-4, question type ≠ retrieved note type | 10 | Most likely to reveal hidden incongruence |
| **Low F (controls)** | Current rating 1-2 | 10 | Verify that low F correlates with low E (failures are dual-axis) |
| **High F, high E (controls)** | Current rating 5, type-matched | 10 | Verify congruent answers stay high under new metric |

### 5.2 Annotation Protocol

For each question-answer pair:
1. Classify question demand (primary building block) — use the established protocol from 5g1a
2. Classify answer supply (what building block does the answer actually deliver) — new annotation
3. Look up E from the congruence matrix (Section 2.3)
4. Compute combined quality score
5. Compare to original rating

### 5.3 Success Criteria

The combined metric provides new information if:
- At least 5/10 "High F, suspected low E" questions drop by ≥1.0 point under the combined metric
- The combined metric's variance is significantly lower than F alone (tighter distribution → better measurement)
- Inter-rater reliability for the E annotation is κ > 0.60 (epistemic type of answers is consistently classifiable)

### 5.4 What This Proves

If the sub-sample shows systematic incongruence in answers currently rated 3-4:
- The counter-argument (5g3) is validated: the rating instrument IS blind to building block effects
- The FZ 5g predictions (P1-P3) deserve re-testing with the combined metric
- The `slipbox-review-slipbot-answer` skill should be upgraded

If the sub-sample shows E ≈ 1.0 across all strata (no incongruence):
- The current single-axis rating is sufficient
- Building block mismatch is not a real failure mode in practice (retrieval failures dominate entirely)

---

## 6. Limitations of the Proposed Metric

1. **Annotation burden**: Classifying answer supply adds a step to every review. Feasible for human review; unclear how to automate reliably for LLM-generated answers about domain-specific content.

2. **Congruence matrix subjectivity**: The partial-congruence scores (0.5) are stipulated, not empirically derived. A user study correlating the matrix values with actual satisfaction would be needed to validate them.

3. **Single-block assumption**: Both Q demand and A supply are classified as a single primary block. Multi-block answers addressing multi-block questions need a more sophisticated alignment measure (e.g., set overlap rather than point comparison).

4. **Retrieval dominance**: If 89.5% of failures are retrieval-caused (gold note never enters candidate set), then E is only relevant for the 10.5% where retrieval succeeds but the answer still fails. The metric's discriminative power is limited to this subset.

5. **Redundancy with question type**: Experiment 5g1d showed that building block demand ≈ question type (diagonal dominance). Using question type as a proxy for demand would be cheaper (no human annotation needed) and nearly equivalent.

---

## 7. Connection to the Broader Framework

This note extends the counter-argument (FZ 5g3) from "the instrument is broken" to "here is how to fix it." It operationalizes the missing measurement dimension that 5g3 identified but did not formalize.

The proposed combined metric also connects to the retrieval strategy work (FZ 5e): if we know the question's epistemological demand, we can route retrieval toward notes of the matching building block type — making the retrieval system *building-block-aware* at the strategy level, not just at the evaluation level.

---

## Related Notes

### Cross-Trail Convergence (Architecture Trail)
- **[FZ 7g1a1a1a1a1: ★ Synthesis — The Vault Is a CQRS Knowledge System](thought_synthesis_two_systems_cqrs_value_proposition.md)** — names epistemic congruence as the **right place for System P typing inside System D**: BB-aware evaluation is a System D *evaluation* signal that uses System P typing — not a routing or candidate-generation use. Exemplifies the R-D rule (typed signals enter at stage 3-4).

### Within Phase 3 (Unification) Trail
- **[FZ 5g3: Counter — Rating Instrument Lacks BB Lens](counter_rating_instrument_lacks_bb_lens.md)** — parent counter-argument; this note proposes the concrete fix
- **[FZ 5g: Building Blocks as Question Complexity Lens](thought_building_block_as_question_complexity_lens.md)** — grandparent hypothesis
- **[FZ 5g1a: Inter-Annotator Agreement](../../archives/experiments/experiment_bb_demand_interannotator_agreement.md)** — annotation protocol for question demand (κ=0.711)
- **[FZ 5g1d: BB vs Question Type](../../archives/experiments/experiment_bb_demand_vs_question_type.md)** — shows BB ≈ QT, so question type could proxy for demand cheaply
- **[FZ 5e1b: Retrieval Failure Analysis](../../archives/experiments/experiment_retrieval_failure_analysis.md)** — the retrieval bottleneck that may dominate over measurement effects
- **[Question Type Classification](../term_dictionary/term_question_type_classification.md)** — the 10-type taxonomy (surface form proxy for BB demand)
- **[Knowledge Building Blocks](../term_dictionary/term_knowledge_building_blocks.md)** — the 8-type taxonomy defining building block types
- **[Retrieval Experiment Trail](../../0_entry_points/entry_retrieval_experiment_trail.md)** — experiment index
