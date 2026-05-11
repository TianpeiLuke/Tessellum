---
tags:
  - resource
  - papers
  - paper
  - intro
  - llm
  - composable_modules
keywords:
  - DSPy
  - prompt engineering
  - brittle
  - declarative
topics:
  - Large Language Models
  - Prompt Optimization
  - LLM Systems
language: markdown
date of note: 2026-04-10
status: active
building_block: argument
paper_id: khattab2023dspy
section_type: intro
---

# Paper Note: DSPy — Introduction

## Literature Note

[lit_khattab2023dspy](lit_khattab2023dspy.md)

## Problem Statement

Prompt engineering for LLM pipelines is **brittle**. When a developer hand-crafts prompts for a multi-step pipeline — e.g., a retrieval-augmented reasoning chain — those prompts are coupled to a specific model, a specific model version, and a specific task decomposition. Any change in:

1. **Model** (e.g., switching from GPT-3.5 to Llama-2)
2. **Model version** (e.g., a provider silently updates weights)
3. **Task structure** (e.g., adding a new retrieval hop)
4. **Metric** (e.g., changing from exact match to F1)

...requires manual re-engineering of the entire prompt chain. This is not just labor-intensive — it makes LLM pipelines fragile in production, where models evolve and requirements change.

### The Core Pain Point

Every component in a pipeline depends on the exact phrasing, formatting, and few-shot examples embedded in its prompt. There is no abstraction layer between the pipeline's *intent* and its *implementation*. Prompts are both the interface specification and the implementation detail — conflated into a single brittle artifact.

### Magnitude of the Problem

For a pipeline with N components:
- Each component has a hand-crafted prompt
- Changing one component's output format may require updating N downstream prompts
- Adding few-shot examples requires manual curation per-model
- Optimization is impossible without running the whole pipeline

## Background: The Status Quo (LangChain / LlamaIndex)

Prior LLM orchestration frameworks — including LangChain and LlamaIndex — provide **string-based composition**:

- Prompts are Python strings with template variables
- Few-shot examples are hardcoded strings inserted into prompts
- There is no formalized notion of what a module's inputs and outputs are
- There is **no optimization layer** — the developer is responsible for tuning all prompts manually

This is analogous to writing machine code by hand rather than using a compiler: it works, but it does not scale, does not generalize, and breaks whenever the underlying hardware (model) changes.

### Analogy: Pre-Compilation Era

Before compilers, programmers wrote assembly code directly for each CPU architecture. Switching from one CPU to another required rewriting programs from scratch. Compilers abstracted away the hardware and allowed programs to be written once, compiled to many targets.

DSPy proposes the same paradigm shift for LLM pipelines: write a declarative specification once, *compile* it into optimized prompts for any model.

## Research Question

> Can we build a system that takes **declarative specifications** of LM tasks — expressed as typed input/output signatures — and automatically **compiles** those specifications into optimized prompts (with few-shot examples, chain-of-thought demonstrations, or other prompt strategies) for any target LLM?

More specifically:
- Can compilation replace hand-crafted prompting without sacrificing performance?
- Can small models (T5-770M, Llama2-13B) be made competitive with GPT-3.5 expert chains through compilation?
- Does the declarative approach generalize across multi-hop reasoning, math, and question-answering tasks?

## Related Notes

- [lit_khattab2023dspy](lit_khattab2023dspy.md)
- [Term: DSPy](../term_dictionary/term_dspy.md)
- [Term: Prompt Engineering](../term_dictionary/term_prompt_engineering.md)
- [Term: Prompt Optimization](../term_dictionary/term_prompt_optimization.md)
- [paper_khattab2023dspy_contrib](paper_khattab2023dspy_contrib.md)
