---
tags:
  - resource
  - literature_note
  - llm_evaluation
  - agentic_ai
  - benchmark
  - delegated_work
  - long_horizon_evaluation
keywords:
  - DELEGATE-52
  - delegated work
  - round-trip relay
  - backtranslation evaluation
  - document corruption
  - long-horizon LLM evaluation
  - agentic tool use
  - critical failure
  - jagged frontier
  - reconstruction score
topics:
  - LLM Benchmarking
  - Agentic AI Evaluation
  - Document Editing
paper_title: "LLMs Corrupt Your Documents When You Delegate"
authors: "Philippe Laban, Tobias Schnabel, Jennifer Neville"
year: "2026"
source: "arXiv preprint"
venue: "arXiv"
DOI: ""
arXiv: "2604.15597"
semantic_scholar_id: "4f146c317371920f0211555973482b9c040a54c4"
zotero_key: "I3VK6R9Z"
paper_notes:
  - paper_laban2026llms_intro.md
  - paper_laban2026llms_contrib.md
  - paper_laban2026llms_algo.md
  - paper_laban2026llms_exp_design.md
  - paper_laban2026llms_exp_result.md
review_note:
language: markdown
date of note: 2026-04-28
status: active
building_block: hypothesis
---

# LLMs Corrupt Your Documents When You Delegate — Laban et al., 2026

## Metadata

| Field | Value |
|-------|-------|
| **Paper** | LLMs Corrupt Your Documents When You Delegate |
| **Authors** | Philippe Laban, Tobias Schnabel, Jennifer Neville |
| **Affiliation** | Microsoft Research |
| **Year** | 2026 |
| **Venue** | arXiv preprint (under review) |
| **arXiv** | [2604.15597](https://arxiv.org/abs/2604.15597) |
| **Citations** | 0 (new preprint) |
| **Code/Data** | github.com/microsoft/DELEGATE52, datasets/microsoft/DELEGATE52 |

## Abstract

Large Language Models (LLMs) are poised to disrupt knowledge work, with the emergence of *delegated work* as a new interaction paradigm (e.g., vibe coding). Delegation requires trust — the expectation that the LLM will faithfully execute the task without introducing errors into documents. We introduce DELEGATE-52 to study the readiness of AI systems in delegated workflows. DELEGATE-52 simulates long delegated workflows that require in-depth document editing across 52 professional domains, such as coding, crystallography, and music notation. Our large-scale experiment with 19 LLMs reveals that current models degrade documents during delegation: even frontier models (Gemini 3.1 Pro, Claude 4.6 Opus, GPT 5.4) corrupt an average of 25% of document content by the end of long workflows, with other models failing more severely. Additional experiments reveal that agentic tool use does not improve performance on DELEGATE-52, and that degradation severity is exacerbated by document size, length of interaction, or presence of distractor files. Our analysis shows that current LLMs are unreliable delegates: they introduce sparse but severe errors that silently corrupt documents, compounding over long interaction.

## Table of Contents

| Section | Note | Key Content |
|---------|------|-------------|
| **Introduction** | [paper_laban2026llms_intro](paper_laban2026llms_intro.md) | Delegated work paradigm, motivation for long-horizon eval, three contributions |
| **Contribution** | [paper_laban2026llms_contrib](paper_laban2026llms_contrib.md) | DELEGATE-52 benchmark, round-trip relay simulation, large-scale 19-LLM study |
| **Method** | [paper_laban2026llms_algo](paper_laban2026llms_algo.md) | Round-trip relay primitive, RS@k metric, 52-domain parsing, distractor context |
| **Experiment Design** | [paper_laban2026llms_exp_design](paper_laban2026llms_exp_design.md) | 19 LLMs, 310 environments, RS@k after each round-trip, agentic harness comparison |
| **Experiment Result** | [paper_laban2026llms_exp_result](paper_laban2026llms_exp_result.md) | 25% frontier-model degradation, agentic tools hurt, critical failures explain ~80% |
| **Review** | [review_laban2026llms](review_laban2026llms.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 8 questions (4 review lenses applied) |

## Summary

<!-- VERIFY -->
**Introduction**: The paper frames delegated work as an emerging LLM interaction paradigm that hinges on faithful task execution without introducing document errors. Existing benchmarks evaluate single-domain tasks (e.g., code editing) or short interactions, leaving long-horizon delegation across diverse knowledge work professions understudied.

**Contribution**: Three contributions — (1) DELEGATE-52, a 52-domain benchmark with 310 work environments and ~15k-token documents; (2) round-trip relay simulation that uses chained backtranslation to evaluate without reference solutions; (3) a large-scale evaluation of 19 LLMs revealing systematic document corruption.

**Method**: A round-trip primitive applies a forward edit instruction (σ) and its inverse (σ⁻¹) to a seed document, measuring reconstruction quality via domain-specific parsing-based similarity in [0,1]. Multiple round-trips are chained (n-relay) to simulate long workflows; the main experiment uses 10 round-trips per environment (20 interactions) with round-robin task scheduling.

**Experiments**: Frontier models (Gemini 3.1 Pro, Claude 4.6 Opus, GPT 5.4) lose ~25% of content by interaction 20, average across all 19 models is ~50%. Python is the only domain where most models reach the "ready" threshold (RS@20 ≥ 98%). Agentic tool use degrades performance by an additional 6% on average. Document size, interaction length, and distractor context all worsen degradation, with effects compounding over time.

## Relevance to Our Work

- **[Hallucination](../term_dictionary/term_hallucination.md)**: DELEGATE-52 reframes hallucination — delegation degradation is not classical hallucination but silent content corruption that compounds across iterations
- **[Agentic AI](../term_dictionary/term_agentic_ai.md)**: Direct evidence that current agentic tool use does not improve, and may worsen, performance on long-horizon document editing tasks
- **[Agentic Evaluation](../term_dictionary/term_agentic_evaluation.md)**: Validates that short-interaction (≤2 step) evaluation is not predictive of long-horizon performance — buyer-abuse agentic systems need long-horizon benchmarks
- **[Greentea LLM Pipeline](../../areas/models/model_greentea_llm_pipeline.md)**: BRP's LLM-based investigation pipeline operates over multi-document evidence; DELEGATE-52 findings on distractor and long-horizon degradation are directly relevant
- **[SOPA LLM Pipeline](../../areas/models/model_sopa_llm_pipeline.md)**: SOPA's LLM-driven seller-page assessment touches similar trust-in-delegation concerns when summarizing long evidence

## Questions

- Do the document corruption patterns observed here generalize to read-and-decide LLM tasks (e.g., abuse classification on long evidence) or are they specific to edit tasks?
- How would BRP's typical LLM use cases (summarization over investigator evidence, policy citation) score on a DELEGATE-52-style round-trip eval?
- The paper finds Python as the only "ready" domain. What domains relevant to abuse prevention (legal text, policy citation, structured ledger data) would benchmark similarly?
- Could the round-trip relay methodology be adapted to evaluate agentic abuse-investigator harnesses for silent-corruption failure modes?

## Related Documentation

- arXiv: https://arxiv.org/abs/2604.15597
- Code: github.com/microsoft/DELEGATE52
- Dataset: huggingface.co/datasets/microsoft/DELEGATE52
