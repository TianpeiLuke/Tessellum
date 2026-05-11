---
tags:
  - resource
  - papers
  - paper
  - exp_result
  - llm
  - composable_modules
  - benchmarks
keywords:
  - DSPy
  - prompt engineering
  - declarative
  - GSM8K
  - HotPotQA
  - results
  - small model
  - few-shot
topics:
  - Large Language Models
  - Prompt Optimization
  - Model Evaluation
language: markdown
date of note: 2026-04-10
status: active
building_block: empirical_observation
paper_id: khattab2023dspy
section_type: exp_result
---

# Paper Note: DSPy — Experiment Results

## Literature Note

[lit_khattab2023dspy](lit_khattab2023dspy.md)

## Main Results: Compilation vs. Hand-Crafted Prompting

### Overall Gain Range

DSPy compilation yields **+25% to +65% improvement** over standard few-shot prompting baselines, with the largest gains on multi-hop reasoning tasks where prompt brittleness is most severe.

### GSM8K (Math Reasoning)

| System | Model | Accuracy | vs. Few-shot |
|--------|-------|----------|--------------|
| Standard few-shot | GPT-3.5 | ~55% | baseline |
| Expert CoT | GPT-3.5 | ~70% | +15pp |
| **DSPy + MIPRO** | GPT-3.5 | **~82%** | **+27pp** |
| Standard few-shot | Llama2-13b | ~28% | baseline |
| Expert CoT | Llama2-13b | ~38% | +10pp |
| **DSPy + MIPRO** | Llama2-13b | **~58%** | **+30pp** |
| **DSPy + MIPRO** | T5-770M | **~44%** | N/A |

### HotPotQA (Multi-Hop QA)

| System | Model | F1 | vs. Few-shot |
|--------|-------|-----|--------------|
| Standard few-shot | GPT-3.5 | ~43% | baseline |
| LangChain RAG | GPT-3.5 | ~47% | +4pp |
| Expert CoT | GPT-3.5 | ~52% | +9pp |
| **DSPy + ReAct + MIPRO** | GPT-3.5 | **~68%** | **+25pp** |
| **DSPy + ReAct + MIPRO** | Llama2-13b | **~55%** | vs ~30% baseline (+25pp) |

## Key Finding 1: +25-65% Over Few-Shot Prompting

The gains from DSPy compilation are **consistent across tasks and models**, with:
- Median gain ~30-35 percentage points on multi-hop tasks
- Larger gains when the baseline is weaker (small models, complex tasks)
- Even 5-shot expert-crafted CoT is typically outperformed by DSPy compilation

The pattern is consistent: **the more brittle the prompt engineering required, the larger the compilation advantage.**

## Key Finding 2: Small Models Compete with GPT-3.5 Expert Chains

The most striking result:

| Small Model System | Score | Large Model Comparison | Score |
|-------------------|-------|------------------------|-------|
| DSPy + Llama2-13b (HotPotQA F1) | ~55% | GPT-3.5 expert CoT | ~52% |
| DSPy + T5-770M (GSM8K) | ~44% | GPT-3.5 standard few-shot | ~55% |
| DSPy + Llama2-13b (GSM8K) | ~58% | GPT-3.5 + LangChain | ~57% |

**Llama2-13b compiled with DSPy matches or exceeds GPT-3.5 with expert-crafted prompts on several benchmarks.** This validates the paper's core thesis: compilation can compensate for model capability differences.

Caveats:
- Comparisons are against hand-crafted prompts, not compiled GPT-3.5 (compiled GPT-3.5 is still higher)
- T5-770M requires more examples and doesn't match GPT-3.5 on all tasks

## Key Finding 3: Optimizer Comparison

| Optimizer | GPT-3.5 GSM8K | Cost (LLM calls) |
|-----------|--------------|------------------|
| No compilation (zero-shot) | 55% | 0 |
| BootstrapFewShot | 73% | ~50 |
| MIPRO | 82% | ~500 |
| GEPA | 79% | ~300 |

MIPRO yields the highest scores but at ~10× the cost of BootstrapFewShot. BootstrapFewShot provides most of the gain at minimal cost — a good default for practitioners.

## Comparison Table: DSPy vs. Competing Systems

| System | Design | Optimization | HotPotQA (GPT-3.5) | GSM8K (GPT-3.5) |
|--------|--------|-------------|---------------------|-----------------|
| LangChain | String templates | None | ~47% | ~58% |
| LlamaIndex | Index + retrieval | None | ~50% | ~60% |
| Expert-crafted CoT | Manual prompts | Human | ~52% | ~70% |
| **DSPy + BootstrapFewShot** | Signatures + Modules | Auto (cheap) | **~62%** | **~76%** |
| **DSPy + MIPRO** | Signatures + Modules | Auto (expensive) | **~68%** | **~82%** |

## Implications

1. **For LLM practitioners**: The gap between few-shot prompting and optimized prompting is large enough (~30pp) to justify the compilation overhead even for simple tasks.
2. **For model selection**: Small models (Llama2-13b) compiled with DSPy can replace GPT-3.5 in many production settings — significant cost reduction.
3. **For the field**: Prompt engineering as a manual discipline may become obsolete for well-structured pipelines; compilation subsumes it.
4. **For Abuse SlipBox / BAP**: DSPy-style compilation is directly applicable to multi-step abuse detection pipelines (e.g., retrieval → reasoning → decision chains) where brittle prompt chains are a known operational pain point.

## Related Notes

- [lit_khattab2023dspy](lit_khattab2023dspy.md)
- [Term: DSPy](../term_dictionary/term_dspy.md)
- [paper_khattab2023dspy_exp_design](paper_khattab2023dspy_exp_design.md)
- [review_khattab2023dspy](review_khattab2023dspy.md)
