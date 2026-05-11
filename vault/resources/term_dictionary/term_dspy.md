---
tags:
  - resource
  - terminology
  - llm
  - composable_modules
  - prompt_optimization
  - program_synthesis
  - agentic_ai
keywords:
  - DSPy
  - declarative LM programming
  - signatures
  - modules
  - teleprompters
  - compilation
  - composability
  - prompt optimization
  - LLM pipelines
  - BootstrapFewShot
  - MIPRO
  - GEPA
topics:
  - Large Language Models
  - Prompt Optimization
  - LLM Systems
  - Program Synthesis
language: markdown
date of note: 2026-04-10
status: active
building_block: concept
---

# DSPy — Declarative Self-improving Language Programs

## Definition

**DSPy** (Declarative Self-improving Python) is an open-source programming framework for building LLM pipelines as **compiled declarative programs** rather than hand-crafted prompt strings. Introduced by Khattab et al. (2023/2024, arXiv:2310.03714, ICLR 2024), DSPy treats prompt engineering as a **compilation problem**: the developer specifies *what* each LM module should do (via Signatures), *how* modules compose (via a Python program), and DSPy's Optimizers automatically discover *how* to prompt each module to maximize a metric.

> **Simple Definition**: DSPy is to LLM pipelines what a compiler is to programs — you write the intent, DSPy figures out the best implementation (prompts + demonstrations) for your target model.

## Key Properties

### 1. Signatures — Typed Interface Declarations

A **Signature** is a declarative specification of a module's inputs and outputs:

```python
"question -> answer"
"context, question -> answer"
"document -> summary, keywords"
```

Signatures decouple **interface** (what the module does) from **implementation** (how the prompt works). The same signature compiles to different prompts for GPT-3.5 vs. Llama2 vs. T5.

### 2. Modules — Composable Building Blocks

| Module | Strategy | Use Case |
|--------|----------|----------|
| `Predict` | Direct generation | Classification, extraction |
| `ChainOfThought` | Step-by-step reasoning before answer | Math, multi-step logic |
| `ReAct` | Interleaved Thought / Action / Observation | Agentic tasks, retrieval loops |
| `ProgramOfThought` | Generates + executes code | Math, data analysis |
| `Retrieve` | Retrieves top-k passages | RAG pipelines |

Modules are composable Python objects — they can be nested, chained, and combined into programs of arbitrary complexity.

### 3. Optimizers (Teleprompters) — The Compilation Engine

Given a program, a metric, and a small training set (20-200 examples), an Optimizer automatically finds the best prompts and demonstrations for each module:

| Optimizer | Strategy | Cost | Best For |
|-----------|----------|------|----------|
| `BootstrapFewShot` | Self-supervised demo generation from training traces | Low (~50 calls) | Quick baseline |
| `MIPRO` | Multi-stage instruction proposal + Bayesian search | Medium (~500 calls) | Production pipelines |
| `GEPA` | LM-as-critic gradient-like feedback | High | Complex metrics |

### 4. Compilation — The Central Metaphor

```
Source code:      Signatures + Module composition (Python)
Compiler:         Optimizer (BootstrapFewShot / MIPRO / GEPA)
Target hardware:  LLM (GPT-3.5, Llama-2, T5, ...)
Compiled output:  Optimized prompts + demonstrations (serializable JSON)
```

Compilation is **metric-driven**: the optimizer searches for prompts that maximize a developer-specified metric function (accuracy, F1, custom reward). The metric is the analogue of an optimization objective.

### 5. Composability

DSPy programs are standard Python — modules can be combined using any Python control flow:

```python
class MultiHopQA(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=3)
        self.reason = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        passages = self.retrieve(question).passages
        return self.reason(context="\n".join(passages), question=question)
```

The entire program compiles together — the optimizer sees all modules and can assign demonstrations coherently across the pipeline.

## Comparison with LangChain and LlamaIndex

| Dimension | DSPy | LangChain | LlamaIndex |
|-----------|------|-----------|------------|
| **Abstraction** | Typed Signatures + Modules | String templates + chains | Index + query pipeline |
| **Optimization** | Automatic (BootstrapFewShot, MIPRO, GEPA) | None | None |
| **Model-agnostic** | Yes — recompile for each model | Partially (different prompt templates per model) | Partially |
| **Prompt brittleness** | Low — prompts generated, not hardcoded | High — prompts are hardcoded strings | High |
| **Composability** | Full Python (loops, conditionals, nesting) | Chain-of-responsibility pattern | Pipeline graph |
| **Retrieval support** | Yes (Retrieve module + ColBERT/BM25) | Yes (many retrievers) | Yes (core focus) |
| **Cold start** | Requires 20-200 examples + metric | Immediate | Immediate |
| **Primary use case** | Optimized multi-step pipelines | Rapid prototyping | Document Q&A |

**When to choose DSPy**: When you have a defined metric and small training set, and want to automatically optimize a multi-step pipeline for a specific model. DSPy pays off most when prompts are complex, models change frequently, or small models need to be competitive with large ones.

**When to choose LangChain/LlamaIndex**: When you need rapid prototyping, have no training data, or the pipeline is simple enough that manual prompting is adequate.

## Empirical Performance

From the DSPy paper (Khattab et al., 2024):
- **+25-65% improvement** over standard few-shot prompting on GSM8K and HotPotQA
- **Llama2-13b compiled with DSPy** matches GPT-3.5 with expert-crafted CoT on several benchmarks
- **BootstrapFewShot** captures most of the gain at ~10% of MIPRO's cost

## Applications

### Direct Applications

- **Multi-hop QA**: RAG pipelines with 2-5 retrieval + reasoning hops (HotPotQA, 2WikiMultiHopQA)
- **Math reasoning**: Chain-of-thought programs with code execution fallback (GSM8K, MATH)
- **Fact verification**: Multi-evidence aggregation pipelines (FEVER)
- **Agentic tool use**: ReAct-style pipelines with tool calls

### the project / Tessellum Applications

DSPy is directly relevant to the domain multi-step scoring pipelines:
- **Abuse detection chains**: Retrieve account history → reason over signals → classify risk — each step is a DSPy module with a Signature
- **Small model deployment**: Compiled Llama2-13b or similar models can replace GPT-3.5 API calls in production ETL scoring, reducing latency and cost
- **Metric-driven optimization**: the project metrics (precision @ policy threshold, F1 over investigation outcomes) can drive compilation without manually tuning prompts for each model update

## Related Terms

- Prompt Optimization — DSPy is one of the primary prompt optimization frameworks; see also APE, OPRO, TextGrad, SPO
- Prompt Engineering — The manual practice that DSPy's compilation aims to replace
- [Meta-Harness](term_meta_harness.md) — The next level of abstraction above DSPy: optimizes harness structure (which modules exist, how they compose) rather than prompt content
- LLM — The compilation target in DSPy
- RAG — Retrieval-Augmented Generation; DSPy's Retrieve module and ReAct loop implement RAG patterns
- Chain-of-Thought — Reasoning strategy implemented by DSPy's ChainOfThought module

## References

### Vault (Literature & Reviews)

- lit_khattab2023dspy — Primary literature note: Khattab et al. (2023/2024), arXiv:2310.03714, ICLR 2024, 634 citations
- review_khattab2023dspy — Full OpenReview-style critical evaluation; Soundness 3/4, Overall 8/10
- lit_lee2026metaharness — Meta-Harness paper by Lee et al. (2026); Khattab is co-author; extends DSPy compilation metaphor to harness structure optimization
- paper_khattab2023dspy_intro — Problem statement and motivation
- paper_khattab2023dspy_contrib — Three contributions: Signatures, Modules, Optimizers
- paper_khattab2023dspy_algo — Architecture, Signature format, Module types, Optimizer algorithms
- paper_khattab2023dspy_exp_design — Benchmarks (GSM8K, HotPotQA), models, baselines
- paper_khattab2023dspy_exp_result — +25-65% gains, small model competitiveness, comparison table

### External

- **arXiv**: [arXiv:2310.03714](https://arxiv.org/abs/2310.03714) — "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines"
- **Website**: [dspy.ai](https://dspy.ai) — Official documentation and tutorials
- **GitHub**: [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) — Open-source repository (Stanford NLP)
- **ICLR 2024**: [OpenReview page](https://openreview.net/forum?id=sY5N0zY5Od)
