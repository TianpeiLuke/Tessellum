---
tags:
  - resource
  - literature_note
  - nlp
  - reasoning
  - prompting
keywords:
  - chain of thought
  - CoT
  - few-shot prompting
  - reasoning
  - emergent abilities
  - GSM8K
  - PaLM
  - LLM reasoning
topics:
  - Natural Language Processing
  - Reasoning
  - Prompt Engineering
domain: "Reasoning & Prompting"
language: markdown
date of note: 2026-03-07
paper_title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
authors:
  - Jason Wei
  - Xuezhi Wang
  - Dale Schuurmans
  - Maarten Bosma
  - Ed H. Chi
  - Fei Xia
  - Quoc Le
  - Denny Zhou
year: 2022
source: "arXiv:2201.11903"
venue: "NeurIPS 2022"
DOI: "10.52202/068431-1800"
arXiv: "2201.11903"
semantic_scholar_id: "1b6e810ce0afd0dd093f789d2b2742d047e316d5"
zotero_key: Q6VGHCJG
citations: 16066
paper_id: wei2022chain
paper_notes:
  - papers/paper_wei2022chain_intro.md
  - papers/paper_wei2022chain_contrib.md
  - papers/paper_wei2022chain_algo.md
  - papers/paper_wei2022chain_exp_design.md
  - papers/paper_wei2022chain_exp_result.md
status: active
building_block: hypothesis
---

# Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

## Metadata

| Field      | Value                                                                |
| ---------- | -------------------------------------------------------------------- |
| Authors    | Wei, Wang, Schuurmans, Bosma, Chi, Xia, Le, Zhou                    |
| Year       | 2022                                                                 |
| Venue      | NeurIPS 2022                                                         |
| arXiv      | [2201.11903](https://arxiv.org/abs/2201.11903)                       |
| DOI        | [10.52202/068431-1800](https://doi.org/10.52202/068431-1800)         |
| S2 ID      | 1b6e810ce0afd0dd093f789d2b2742d047e316d5                            |
| Zotero     | Q6VGHCJG                                                             |
| Citations  | 16,066                                                               |
| paper_id   | wei2022chain                                                         |

## Abstract

> We explore how generating a chain of thought — a series of intermediate reasoning steps — significantly improves the ability of large language models to perform complex reasoning. In particular, we show how such reasoning abilities emerge naturally in sufficiently large language models via a simple method called chain-of-thought prompting, where a few chain of thought demonstrations are provided as exemplars in prompting. Experiments on three large language models show that chain-of-thought prompting improves performance on a range of arithmetic, commonsense, and symbolic reasoning tasks. The empirical gains can be striking. For instance, prompting a PaLM 540B with just eight chain-of-thought exemplars achieves state-of-the-art accuracy on the GSM8K benchmark of math word problems, surpassing even finetuned GPT-3 with a verifier.

*(Source: Semantic Scholar abstract)*

## Table of Contents

| Section | Paper Note | Key Content |
|---------|-----------|-------------|
| **Introduction** | [paper_wei2022chain_intro](paper_wei2022chain_intro.md) | Research context, problem motivation, research gap, key prior work |
| **Contribution** | [paper_wei2022chain_contrib](paper_wei2022chain_contrib.md) | Claimed contributions, positioning among related work, novelty assessment |
| **Algorithm / Method** | [paper_wei2022chain_algo](paper_wei2022chain_algo.md) | Technical approach, CoT prompting format, key design choices, properties |
| **Experiment Design** | [paper_wei2022chain_exp_design](paper_wei2022chain_exp_design.md) | Datasets, models, baselines, evaluation metrics, ablation setup |
| **Experiment Results** | [paper_wei2022chain_exp_result](paper_wei2022chain_exp_result.md) | Key results, ablation studies, scaling analysis, robustness, limitations |
| **Review** | [review_wei2022chain](review_wei2022chain.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 7 questions (5 review lenses applied) |

## Summary

<!-- VERIFY: Review each summary sentence against the paper. These are AI-generated. -->

- Chain-of-thought (CoT) prompting augments standard few-shot exemplars with intermediate natural language reasoning steps, enabling LLMs to solve complex reasoning tasks without any fine-tuning or architectural changes.
- CoT is an [emergent](../term_dictionary/term_emergence.md) capability: it provides meaningful gains only for models with roughly 100B or more parameters; smaller models see flat or degraded performance.
- PaLM 540B with 8 CoT exemplars achieves 56.9% on GSM8K, surpassing fine-tuned GPT-3 with a verifier (55%), and improvements generalize across arithmetic, commonsense, and symbolic reasoning benchmarks.
- Ablations confirm that natural language reasoning steps — not merely extra compute tokens or equation-only output — are essential for the performance gains.

## Relevance to Our Work

CoT prompting is directly applicable to any LLM-based reasoning pipeline. Understanding its requirements (scale, exemplar quality) and failure modes (hallucinated reasoning, scale dependency) informs how we design and evaluate LLM components in our system.

## Questions

### Validation (Socratic)
1. The paper evaluates CoT across three reasoning categories (arithmetic, commonsense, symbolic) on 12 benchmarks — all well-established academic datasets with single correct answers. What information is *missing* about CoT's applicability to other reasoning types — causal reasoning, spatial reasoning, analogical reasoning, ethical dilemmas? These untested domains lack clean ground-truth answers, which means the "correct final answer" evaluation paradigm used throughout the paper cannot apply. Would CoT's benefits persist, diminish, or manifest differently when there is no single extractable answer to verify? *(WYSIATI lens)*
2. The ablation study shows "variable compute" (dots adding extra tokens) yields only 6.4% vs. 14.3% for full CoT on LaMDA 137B, presented as evidence that **natural language reasoning** — not additional computation — drives CoT's gains. But the "dots" condition gives the model more *serial* computation without *structured* content. This null result could mean that *unstructured* extra computation doesn't help, not that computation allocation is irrelevant. What ablation would distinguish between "CoT works because of *language*" vs. "CoT works because of *structured intermediate computation*"? For instance, what if the intermediate steps were in Python pseudocode or first-order logic rather than natural language — would the gains persist? *(Causal vs. Correlational lens)*

### Application (Taxonomic)
3. CoT prompting unlocked multi-step reasoning at inference time — a capability that was impossible with standard few-shot prompting. This created an [adjacent possible](../term_dictionary/term_chain_of_thought.md) explosion: Zero-shot CoT (Kojima, 2022), Self-Consistency (Wang, 2022), Tree of Thought (Yao, 2023), and Process Reward Models (Lightman, 2023) all build on CoT's demonstration that intermediate reasoning steps improve performance. Which of these extensions would NOT have been conceivable without CoT's specific contribution — and which were independently motivated ideas that CoT merely catalyzed? This distinguishes CoT's role as a *necessary precursor* vs. an *accelerant* for reasoning research. *(Adjacent Possible lens)*
4. The paper reports that CoT sometimes produces correct final answers through incorrect intermediate reasoning (hallucinated chains), and that sub-100B models show *degraded* performance with CoT. Rather than treating these as pure limitations, what would the *most informative failure* of CoT look like? If we systematically analyzed the error patterns in models where CoT *hurts* (350M, 1.3B, 6.7B on GSM8K), would the failure modes reveal (a) the model cannot decompose problems but tries to imitate the chain format, (b) the model introduces compounding errors across steps, or (c) the extra output length dilutes attention from the question? Each failure mode implies a different minimum capability threshold for CoT to work. *(Error as Signal lens)*

### Synthesis (Lateral)
5. This paper and [InstructGPT (Ouyang et al., 2022)](lit_ouyang2022training.md) both improve LLM behavior but through fundamentally different mechanisms — CoT through *prompt engineering* at inference time, InstructGPT through *RLHF training* that modifies the model itself. The Related Documentation links them as "complementary," but what is the precise interaction? If a model is first RLHF-trained and *then* CoT-prompted, does the combination produce super-additive gains (synergy), or does RLHF training internalize reasoning patterns that make explicit CoT less necessary (substitution)? The later success of o1/o3 models (RLHF + long-chain reasoning) suggests synergy — but does the Wei et al. evidence speak to this, or is it a post-hoc narrative? *(Liquid Network lens — bridging with lit_ouyang2022training)*
6. CoT was designed for *reasoning tasks* (math, logic, commonsense), but the technique has been [exapted](../term_dictionary/term_architectural_exaptation.md) far beyond its original scope — into code generation, creative writing, scientific analysis, visual reasoning (multimodal CoT), and even [abuse investigation reasoning](../term_dictionary/term_greentea.md) in production systems. What specific properties of CoT made it so broadly exaptable? Is it (a) the intermediate steps (decomposition), (b) the natural language format (accessibility), or (c) the few-shot demonstration pattern (learnability)? Which domain adaptation of CoT is *most surprising* and *least predicted* by the original paper's framing? -> Follow-up: [term_prompt_exaptation](../term_dictionary/term_prompt_exaptation.md) *(Exaptation lens)*

## Related Documentation

### Term Notes
- [LLM](../term_dictionary/term_llm.md) — CoT leverages LLM scale; the term note mentions CoT in prompt engineering
- [Scaling Law](../term_dictionary/term_scaling_law.md) — CoT demonstrates emergent abilities; the term note cites Wei et al. 2022
- [Transfer Learning](../term_dictionary/term_transfer_learning.md) — CoT is a form of zero/few-shot transfer
- [Chain of Thought](../term_dictionary/term_chain_of_thought.md) — Term stub created alongside this literature note
- [System 1 and System 2](../term_dictionary/term_system_1_and_system_2.md) — CoT forces System 2 (deliberate) reasoning vs System 1 (automatic)

### Related Literature
- [GPT-3 (Brown et al., 2020)](lit_brown2020language.md) — GPT-3 introduced few-shot in-context learning that CoT builds on
- [GPT-2 (Radford et al., 2019)](lit_radford2019language.md) — Established autoregressive generation and zero-shot task conditioning (e.g., "TL;DR:") that CoT prompting extends
- [Scaling Laws (Kaplan et al., 2020)](lit_kaplan2020scaling.md) — Scaling laws predict smooth loss improvement; CoT shows discrete capability emergence
- [InstructGPT (Ouyang et al., 2022)](lit_ouyang2022training.md) — RLHF instruction following is complementary to CoT prompting
- [TextGrad (Yuksekgonul et al., 2024)](lit_yuksekgonul2024textgrad.md) — TextGrad uses CoT-style reasoning chains as textual feedback; CoT is a baseline in TextGrad's question answering experiments (GPQA, MMLU)
