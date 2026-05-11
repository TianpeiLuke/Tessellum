---
tags:
  - resource
  - papers
  - paper
  - exp_design
  - llm
  - composable_modules
  - benchmarks
keywords:
  - DSPy
  - prompt engineering
  - declarative
  - GSM8K
  - HotPotQA
  - benchmarks
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
section_type: exp_design
---

# Paper Note: DSPy — Experiment Design

## Literature Note

[lit_khattab2023dspy](lit_khattab2023dspy.md)

## Evaluation Benchmarks

The paper evaluates DSPy across tasks requiring multi-step reasoning and retrieval, chosen to stress-test the compilation approach on pipelines of varying complexity:

| Benchmark | Task Type | Measures | Why Chosen |
|-----------|-----------|----------|------------|
| **GSM8K** | Grade school math word problems | Exact match accuracy | Multi-step arithmetic reasoning; well-established LLM benchmark |
| **HotPotQA** | Multi-hop open-domain QA | Exact match / F1 | Requires chaining retrieval across multiple documents |
| **MultiHop QA (2WikiMultiHopQA)** | Multi-hop QA over Wikipedia | Exact match | More complex retrieval chains than HotPotQA |
| **FEVER** | Fact verification | Label accuracy | Claims requiring multi-step evidence aggregation |
| **MNLI** | Natural language inference | Accuracy | Classification with implicit reasoning |

### Why Multi-Hop Tasks

The paper specifically targets **multi-hop reasoning** because these tasks expose the brittleness of hand-crafted prompts most clearly:
- Each hop requires a separate LM call
- The prompt for hop N depends on the output of hop N-1
- Manual prompt optimization across 3-5 hops is impractical
- Compilation offers the largest leverage in this regime

## Models Evaluated

| Model | Scale | Category | Access |
|-------|-------|----------|--------|
| **GPT-3.5-turbo** | ~175B | Frontier commercial | API |
| **Llama2-13b** | 13B | Open-weight mid-size | Local |
| **T5-770M** | 770M | Small encoder-decoder | Local |
| **CodeT5+** | Varies | Code-specialized | Local |

The deliberate inclusion of **small models (T5-770M, Llama2-13b)** is critical to the paper's thesis: DSPy compilation should close the gap between small and large models by extracting better reasoning behavior through optimized prompting.

## Baselines

### Prompt Engineering Baselines

| Baseline | Description |
|----------|-------------|
| **Standard few-shot** | k manually chosen demonstrations per module, fixed across evaluation |
| **Zero-shot** | No demonstrations; instruction only |
| **Expert-crafted CoT** | Human expert writes chain-of-thought prompts with demonstrations; represents the "best case" manual approach |

### System Baselines

| Baseline | Description |
|----------|-------------|
| **LangChain** | String-template based pipelines, no optimization |
| **LlamaIndex** | Index-augmented retrieval pipelines, no optimization |
| **Vanilla RAG** | Retrieve top-k, concatenate to context, single LM call |

### DSPy Variants (Ablation)

| Variant | What It Tests |
|---------|---------------|
| DSPy + Predict | Baseline DSPy without CoT or retrieval |
| DSPy + ChainOfThought | Adds reasoning traces |
| DSPy + ReAct | Adds retrieval loop |
| DSPy + BootstrapFewShot | Compiled with cheapest optimizer |
| DSPy + MIPRO | Compiled with instruction search |

## Evaluation Methodology

- **Metric**: Exact match accuracy for QA tasks; F1 for partial credit; accuracy for classification
- **Train set size**: 20-200 examples (intentionally small to demonstrate low-resource optimization)
- **Validation set**: Used during compilation for optimizer search
- **Test set**: Held out; evaluated once after compilation
- **Retrieval**: ColBERT or BM25 over Wikipedia corpus for retrieval-augmented tasks

### Design Philosophy

The evaluation is designed to test two orthogonal claims:
1. **Compilation replaces hand-crafting**: DSPy + BootstrapFewShot should match or exceed expert-crafted few-shot
2. **Small models compete with large**: DSPy + T5-770M / Llama2-13b should approach GPT-3.5 expert chains

## Related Notes

- [lit_khattab2023dspy](lit_khattab2023dspy.md)
- [Term: DSPy](../term_dictionary/term_dspy.md)
- [paper_khattab2023dspy_algo](paper_khattab2023dspy_algo.md)
- [paper_khattab2023dspy_exp_result](paper_khattab2023dspy_exp_result.md)
