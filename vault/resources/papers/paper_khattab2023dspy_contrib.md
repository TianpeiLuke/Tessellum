---
tags:
  - resource
  - papers
  - paper
  - contrib
  - llm
  - composable_modules
keywords:
  - DSPy
  - prompt engineering
  - brittle
  - declarative
  - signatures
  - modules
  - teleprompters
topics:
  - Large Language Models
  - Prompt Optimization
  - LLM Systems
language: markdown
date of note: 2026-04-10
status: active
building_block: argument
paper_id: khattab2023dspy
section_type: contrib
---

# Paper Note: DSPy — Contributions

## Literature Note

[lit_khattab2023dspy](lit_khattab2023dspy.md)

## Key Contributions

### Contribution 1: Signatures as Atomic Interfaces

DSPy introduces **Signatures** as the fundamental abstraction for describing what an LM module does, decoupled from how it does it.

A Signature is a typed declaration of input and output fields:

```
"question -> answer"
"context, question -> answer"
"document -> summary, keywords"
```

Signatures are:
- **Declarative**: They specify the interface, not the implementation
- **Composable**: They can be chained into multi-step pipelines
- **Model-agnostic**: The same signature can be compiled for GPT-3.5, Llama-2, or T5

This is analogous to a function signature in typed programming languages: `def qa(question: str) -> str`. The signature contracts what the function does; the implementation (the compiled prompt) is separate.

### Contribution 2: Composable Modules

DSPy provides a library of **Modules** that implement signatures using different LM strategies:

| Module | Strategy | Use Case |
|--------|----------|----------|
| `Predict` | Direct generation | Simple classification, extraction |
| `ChainOfThought` | Step-by-step reasoning before answer | Multi-step reasoning, math |
| `ReAct` | Interleaved reasoning and actions (tool calls) | Agentic tasks, retrieval loops |
| `ProgramOfThought` | Generates executable code, runs it, returns result | Math, data analysis |
| `MultiChainComparison` | Generates multiple chains, selects best | High-stakes decisions |

Modules are **composable** in the full Python sense: they can be nested, called in loops, and combined into arbitrarily complex programs. A `dspy.Module` subclass (a "Program") can contain multiple inner modules, each with its own signature, all compiled together.

### Contribution 3: Teleprompter Optimizers (Compilation)

**Teleprompters** (later renamed "Optimizers") are the compilation engine of DSPy. Given:
1. A program (composed of modules with signatures)
2. A metric function (how to evaluate outputs)
3. A training set (small, typically 20–200 examples)

...an optimizer automatically finds the best prompts (few-shot examples, instructions, chain-of-thought demonstrations) for each module in the program.

Key optimizers:

| Optimizer | Strategy | Cost |
|-----------|----------|------|
| `BootstrapFewShot` | Generates demonstrations via self-supervision on training data | Low |
| `MIPRO` | Multi-stage instruction proposal + Bayesian search over prompt space | Medium |
| `GEPA` | Gradient-estimated prompt adaptation — uses LM feedback as gradient signal | High |

## Novelty: The Compilation Metaphor

The central insight of DSPy is the **compilation metaphor**:

```
High-level specification (Signatures + Program structure)
            ↓
       Compiler (Optimizer / Teleprompter)
            ↓
Optimized implementation (Prompts + Few-shot examples + Instructions)
```

This is analogous to how a C++ compiler takes a high-level program and produces optimized machine code — the programmer writes the intent, the compiler handles the implementation details for the target hardware.

For DSPy:
- The **source language** is Python with Signatures and Modules
- The **compiler** is the Teleprompter/Optimizer
- The **target hardware** is the LLM (GPT-3.5, Llama-2, T5, etc.)
- The **optimized output** is a set of prompts with demonstrations

### Why This Matters

Before DSPy, optimizing a prompt required:
1. Manual inspection of model outputs
2. Iterative prompt rewriting by an expert
3. Re-doing everything when the model changed

With DSPy compilation:
1. Define the task as a Signature
2. Specify the metric
3. Run the optimizer — it finds the best prompts automatically
4. Changing models requires only re-running the optimizer

## Related Notes

- [lit_khattab2023dspy](lit_khattab2023dspy.md)
- [Term: DSPy](../term_dictionary/term_dspy.md)
- [Term: Prompt Optimization](../term_dictionary/term_prompt_optimization.md)
- [paper_khattab2023dspy_intro](paper_khattab2023dspy_intro.md)
- [paper_khattab2023dspy_algo](paper_khattab2023dspy_algo.md)
