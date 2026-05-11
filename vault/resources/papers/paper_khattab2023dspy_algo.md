---
tags:
  - resource
  - papers
  - paper
  - algo
  - llm
  - composable_modules
keywords:
  - DSPy
  - prompt engineering
  - declarative
  - signatures
  - modules
  - teleprompters
  - compilation
topics:
  - Large Language Models
  - Prompt Optimization
  - LLM Systems
  - Model Architecture
language: markdown
date of note: 2026-04-10
status: active
building_block: model
paper_id: khattab2023dspy
section_type: algo
---

# Paper Note: DSPy — Architecture & Algorithm

## Literature Note

[lit_khattab2023dspy](lit_khattab2023dspy.md)

## System Architecture

### End-to-End Compilation Diagram

```
Developer writes:
  ┌─────────────────────────────────────┐
  │  Signatures (typed I/O declarations) │
  │  + Module composition (Python)       │
  │  + Metric function                   │
  │  + Small training set (20-200 ex.)   │
  └─────────────────────────────────────┘
                    │
                    ▼
  ┌─────────────────────────────────────┐
  │         Optimizer / Teleprompter     │
  │  (BootstrapFewShot / MIPRO / GEPA)  │
  │  - Generates candidate demonstrations│
  │  - Evaluates on metric               │
  │  - Searches prompt space             │
  └─────────────────────────────────────┘
                    │
                    ▼
  ┌─────────────────────────────────────┐
  │        Optimized Program             │
  │  - Each module has compiled prompt   │
  │  - Few-shot examples selected        │
  │  - Instructions tuned per module     │
  └─────────────────────────────────────┘
                    │
                    ▼
  ┌─────────────────────────────────────┐
  │       Inference / Deployment         │
  │  Any LLM backend (GPT, Llama, T5)   │
  └─────────────────────────────────────┘
```

## Signature Format

Signatures use a concise string DSL that is parsed into typed fields:

| Signature String | Inputs | Outputs | Example Use |
|-----------------|--------|---------|-------------|
| `"question -> answer"` | question | answer | Open-domain QA |
| `"context, question -> answer"` | context, question | answer | Reading comprehension |
| `"document -> summary"` | document | summary | Summarization |
| `"question -> reasoning, answer"` | question | reasoning, answer | Chain-of-thought |
| `"passage, query -> relevant: bool"` | passage, query | relevant (bool) | Retrieval scoring |

Fields can also be annotated with docstrings for richer descriptions:

```python
class GenerateAnswer(dspy.Signature):
    """Answer questions with short factual answers."""
    context = dspy.InputField(desc="relevant facts from search")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often 1-5 words")
```

## Module Types

| Module | Class | Behavior | Internal Prompt Strategy |
|--------|-------|----------|--------------------------|
| **Predict** | `dspy.Predict` | Direct input → output generation | Single LM call; format = signature fields |
| **ChainOfThought** | `dspy.ChainOfThought` | Generates `reasoning` field before answer | Adds "Let's think step by step" structure |
| **ReAct** | `dspy.ReAct` | Interleaves Thought / Action / Observation loops | Tool-calling loop; actions invoke retrieval/APIs |
| **ProgramOfThought** | `dspy.ProgramOfThought` | Generates Python code, executes it, returns output | Code interpreter in the loop |
| **MultiChainComparison** | `dspy.MultiChainComparison` | Generates N candidate chains, selects best | Self-consistency + comparison |
| **Retrieve** | `dspy.Retrieve` | Retrieves top-k passages from a retriever | Not an LM call; wraps retrieval backend |

Modules share a common interface: they take keyword arguments matching input fields and return a `Prediction` object with output fields.

## Optimizer Types

### BootstrapFewShot

The simplest and lowest-cost optimizer:

```
1. Run the uncompiled program on training examples
2. Collect (input, output) pairs where metric passes
3. Use passing examples as few-shot demonstrations
4. Assign demonstrations to each module's compiled prompt
```

- Cost: O(|train_set| × program_calls)
- No LLM calls for optimization itself — uses program's own traces
- Works well with 20-50 training examples

### MIPRO (Multi-Stage Instruction PRoposal and Optimization)

A more sophisticated optimizer using Bayesian search:

```
Stage 1: Instruction Proposal
  - LLM proposes K candidate instruction variants per module
  - Candidates are diverse paraphrases / specifications

Stage 2: Bayesian Optimization
  - Treat (instruction_i, demos_j) as a discrete hyperparameter
  - Use TPE (Tree-structured Parzen Estimator) to search combinations
  - Evaluate each candidate combination on validation set
  - Select highest-scoring combination
```

- Cost: O(K × iterations × val_set_size) LLM calls
- Better than BootstrapFewShot on complex programs (5-10 modules)

### GEPA (Gradient-Estimated Prompt Adaptation)

Uses LM-as-critic feedback as a gradient signal:

```
1. Run program, collect failures (low-metric outputs)
2. Ask a critic LLM: "What should the prompt have said to get a better answer?"
3. Use critic feedback to propose prompt edits (analogous to a gradient step)
4. Apply edits, evaluate, repeat
```

- Cost: Highest — requires additional LLM calls for the critic
- Best for tasks with differentiable-like metric signals
- Conceptually bridges to TextGrad (gradient feedback on text)

## Compilation Process: Step by Step

```
Given: program P, metric M, train_set T, optimizer O

1. BOOTSTRAP TRACES
   For each example (x, y*) in T:
     Run P(x) → ŷ
     If M(ŷ, y*) passes threshold:
       Store execution trace (input, intermediate outputs, final output)

2. GENERATE CANDIDATES
   For each module m in P:
     Collect traces where m was on the "successful path"
     (BootstrapFewShot: use as demonstrations)
     (MIPRO: additionally propose K instruction variants via LLM)

3. SEARCH / SELECT
   Evaluate candidate combinations on validation set
   Select combination maximizing M

4. COMPILE
   Assign selected demonstrations + instructions to each module
   Return compiled program P* (a Python object with frozen prompts)

5. DEPLOY
   P* behaves identically to P but with optimized internals
   Can be serialized to JSON for reproducible deployment
```

## Related Notes

- [lit_khattab2023dspy](lit_khattab2023dspy.md)
- [Term: DSPy](../term_dictionary/term_dspy.md)
- [Term: Prompt Optimization](../term_dictionary/term_prompt_optimization.md)
- [Term: Prompt Engineering](../term_dictionary/term_prompt_engineering.md)
- [paper_khattab2023dspy_contrib](paper_khattab2023dspy_contrib.md)
- [paper_khattab2023dspy_exp_design](paper_khattab2023dspy_exp_design.md)
