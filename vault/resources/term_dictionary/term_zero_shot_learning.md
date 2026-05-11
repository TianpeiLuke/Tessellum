---
tags:
  - resource
  - terminology
  - deep_learning
  - transfer_learning
  - nlp
keywords:
  - zero-shot learning
  - zero-shot transfer
  - zero-shot evaluation
  - no fine-tuning
  - task transfer
  - in-context learning
  - few-shot learning
  - prompt conditioning
  - task specification
topics:
  - Deep Learning
  - Transfer Learning
  - Natural Language Processing
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Zero-Shot Learning

## Definition

**Zero-Shot Learning** (ZSL) is the ability of a model to perform a task without any task-specific training examples or parameter updates. The model receives only a natural language description of the task (or structured input formatting) and generates outputs directly. In the language model context, zero-shot was first demonstrated at scale by GPT-2 (Radford et al., 2019), which conditioned on task descriptions like "TL;DR:" for summarization and example format pairs for translation — achieving state-of-the-art on 7/8 language modeling benchmarks without ever being explicitly trained on those tasks.

## Full Name

**Zero-Shot Learning** (ZSL)

**Also Known As**: Zero-shot transfer, zero-shot evaluation, zero-shot inference

## The Transfer Learning Spectrum

Zero-shot learning exists on a continuum of task adaptation strategies, distinguished by how much task-specific information the model receives:

| Setting | Task-Specific Data | Parameter Updates | Task Specification | Example |
|---------|:------------------:|:-----------------:|-------------------|---------|
| **Zero-shot** | None | None | Natural language description only | "TL;DR:" for summarization |
| **One-shot** | 1 example | None | 1 demonstration in context | 1 translation pair + new source |
| **Few-shot** | K examples (K=2-64) | None | K demonstrations in context | 32 QA pairs + new question |
| **Fine-tuning** | Full dataset | Full model update | Supervised training objective | Train on 127K CoQA examples |
| **PEFT** | Full dataset | Partial update (LoRA, adapters) | Supervised on small parameter set | LoRA rank-16 on 127K examples |

**Key insight**: Moving down the spectrum increases task performance but requires more data and compute. The GPT-2/GPT-3 papers demonstrated that moving *up* the spectrum (toward zero-shot) becomes viable at sufficient model scale.

## How Zero-Shot Works in LLMs

### Task Specification via Natural Language

Zero-shot requires encoding the task entirely through the input prompt. GPT-2 demonstrated several natural language task specification patterns:

| Task | Zero-Shot Prompt Format | Example |
|------|------------------------|---------|
| **Summarization** | `{article} TL;DR:` | Article text followed by "TL;DR:" |
| **Translation** | `{english} = {french}` (example pair) + `{new english} =` | Pattern demonstration |
| **Reading Comprehension** | `{document} Q: {question} A:` | Document + question + answer marker |
| **Question Answering** | `Q: {question} A:` with example pairs | QA format conditioning |

No special tokens, no task-specific output heads, no gradient updates — the same autoregressive model handles all tasks through different conditioning.

### Why Zero-Shot Scales with Model Size

GPT-2 demonstrated that zero-shot performance improves log-linearly with model parameters:

| Model | Parameters | LAMBADA PPL↓ | LAMBADA ACC↑ | CBT-CN ACC↑ | Winograd ACC↑ |
|-------|:---------:|:------------:|:------------:|:-----------:|:-------------:|
| Small | 117M | 35.13 | 45.99% | 87.65% | — |
| Medium | 345M | 15.60 | 55.48% | 92.35% | — |
| Large | 762M | 10.87 | 60.12% | 93.45% | — |
| XL (GPT-2) | 1,542M | **8.63** | **63.24%** | **93.30%** | **70.70%** |

GPT-3 (Brown et al., 2020) confirmed this trend at 175B parameters and showed that few-shot performance scales even faster than zero-shot — the gap between few-shot and fine-tuned SOTA narrows with scale.

## Zero-Shot vs. Few-Shot: When to Use Which

| Criterion | Prefer Zero-Shot | Prefer Few-Shot |
|-----------|:---------------:|:---------------:|
| No labeled examples available | Yes | — |
| Prompt length budget is tight | Yes | — |
| Task is straightforward (classification, extraction) | Yes | — |
| Task requires complex formatting | — | Yes |
| Task benefits from format demonstration | — | Yes |
| Task involves reasoning chains | — | Yes (+ CoT) |

**Practical rule**: Zero-shot works best for tasks where the natural language task description is unambiguous. Few-shot helps when the output format or reasoning pattern needs to be demonstrated.

## Limitations

1. **Performance gap**: Zero-shot consistently underperforms few-shot and fine-tuning. GPT-2's zero-shot summarization barely beats random 3-sentence extraction (21.40 vs. 20.98 R-AVG)
2. **Task ambiguity**: Without examples, the model may misinterpret the desired output format, length, or style
3. **Scale dependency**: Zero-shot is only practical at very large model scales — GPT-2 Small (117M) zero-shot performance is often near random
4. **Domain sensitivity**: Performance drops sharply on tasks far from the pre-training distribution (e.g., GPT-2 achieves only 4.1% exact match on Natural Questions)

## Applications to Our Work

- **LLM-based abuse classification**: Zero-shot prompting enables abuse detection without task-specific training data — describe the abuse pattern in natural language and let the LLM classify
- **Rapid prototyping**: Zero-shot evaluation is the fastest way to test whether an LLM can handle a new abuse type before investing in labeled data collection
- **Rare abuse types**: For abuse patterns with <100 historical examples, zero-shot may be the only viable approach without synthetic data augmentation

## Related Terms

### Transfer Learning Spectrum
- [Transfer Learning](term_transfer_learning.md) — Zero-shot is the extreme end: no parameter updates, no examples
- [Fine-Tuning](term_fine_tuning.md) — The opposite extreme: full parameter updates on task-specific data
- [Chain of Thought](term_chain_of_thought.md) — Extends few-shot prompting with intermediate reasoning steps

### Models and Architectures
- [LLM](term_llm.md) — Zero-shot capability emerges at large model scales
- [Transformer](term_transformer.md) — Architecture enabling the autoregressive generation required for zero-shot task completion
- [BERT](term_bert.md) — Encoder-only model; requires fine-tuning, not amenable to zero-shot generation

### Evaluation
- [Perplexity](term_perplexity.md) — Primary metric for zero-shot language modeling evaluation
- [Scaling Law](term_scaling_law.md) — Formalizes the relationship between model size and zero-shot performance

## References

- Radford, A. et al. (2019). [Language Models are Unsupervised Multitask Learners](../papers/lit_radford2019language.md). OpenAI Technical Report.
- Brown, T. et al. (2020). [Language Models are Few-Shot Learners](../papers/lit_brown2020language.md). NeurIPS. arXiv:2005.14165.
- Wei, J. et al. (2022). [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](../papers/lit_wei2022chain.md). NeurIPS. arXiv:2201.11903.
- Xian, Y. et al. (2018). Zero-Shot Learning — A Comprehensive Evaluation of the Good, the Bad and the Ugly. IEEE TPAMI. arXiv:1707.00600.
