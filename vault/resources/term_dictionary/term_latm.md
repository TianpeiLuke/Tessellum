---
tags:
  - resource
  - terminology
  - llm
  - tool_use
  - program_synthesis
  - cost_efficiency
  - agentic_ai
keywords:
  - LATM
  - large language models as tool makers
  - tool making
  - tool use
  - functional caching
  - tool dispatch
  - amortized cost
  - role specialization
  - GPT-4
  - GPT-3.5
  - Cai et al.
topics:
  - Large Language Models
  - Tool Use
  - Program Synthesis
  - Cost Efficiency
  - LLM Systems
language: markdown
date of note: 2026-04-10
status: active
building_block: concept
---

# LATM — Large Language Models as Tool Makers

## Definition

**LATM** (Large Language Models as Tool Makers) is an LLM deployment framework that separates **tool creation** from **tool use** by assigning them to different models:

1. **Tool Maker** (powerful LLM, e.g. GPT-4): Receives a class of structurally similar problems, writes a reusable Python function that solves all instances in the class, verifies correctness via test execution, and stores the function in a tool cache.
2. **Tool User** (lightweight LLM, e.g. GPT-3.5): Receives a new problem instance, retrieves the appropriate cached tool via a dispatcher, extracts function arguments, invokes the function, and returns the result.

Introduced by Tianle Cai, Xuezhi Wang, Tengyu Ma, Xinyun Chen, and Denny Zhou (Google DeepMind) in arXiv:2305.17126, published at ICLR 2024 with 276 citations.

> **Simple Definition**: LATM is to LLM query handling what software engineering is to problem solving — a powerful expert writes a general solution once; everyone else applies it repeatedly.

## Key Properties

### 1. Two-Phase Role Separation

The fundamental design decision in LATM is role specialization based on task difficulty:

| Phase | Role | Model | Frequency | Cost | Task |
|-------|------|-------|-----------|------|------|
| **Offline** | Tool Maker | GPT-4 | Once per problem class | High | Create + verify Python function |
| **Online** | Tool User | GPT-3.5 | Every query | Low | Extract args + invoke function |

This separation is maintained strictly: the Tool User never writes new code; the Tool Maker never handles individual query instances directly.

### 2. Functional Caching

LATM stores **functions** (procedures) in its cache, not **responses** (outputs). This is a fundamental departure from standard caching:

- **Response cache entry**: "The answer to *this specific query* is X"
- **Function cache entry**: "The procedure for solving *any query in this class* is `f(args) -> output`"

A single function cache entry handles arbitrarily many future queries in the same class. The function is verified before caching (by running it on representative examples), providing a correctness guarantee absent from response caching.

### 3. Tool Dispatch

A lightweight dispatcher (LLM call) routes each incoming problem:

- **Match found**: Retrieve cached tool → Tool User path (cheap)
- **No match**: Invoke Tool Maker → create new tool → cache → Tool User path

The dispatcher's matching criterion is semantic: does the natural-language description of any existing tool cover the new problem's structure?

### 4. Amortized Cost Model

LATM's economic argument rests on amortization:

```
Cost without LATM = n × C(GPT-4)

Cost with LATM = k × C(GPT-4) + n × C(GPT-3.5)
              ≈ n × C(GPT-3.5)   when k << n

where:
  n = number of queries
  k = number of distinct problem classes (k << n in practice)
  C(GPT-4) ≈ 10-20 × C(GPT-3.5)
```

For production systems with many queries across few recurring problem types, amortized cost converges to GPT-3.5 pricing at GPT-4 accuracy.

### 5. Verification as a First-Class Step

Unlike response caching (where correctness cannot be checked without a ground-truth oracle) or direct LLM calls (where correctness is assumed), LATM verifies each tool before caching by executing the Python function on representative test cases. Only tools that pass verification enter the cache.

## Comparison with Related Frameworks

| Framework | What is Created/Cached | Who Creates | Who Uses | Verification |
|-----------|----------------------|-------------|----------|-------------|
| **Toolformer** | Nothing (uses pre-existing APIs) | N/A (tools are external) | LLM (fine-tuned) | N/A |
| **LATM** | Python functions (tools) | Powerful LLM (GPT-4) | Lightweight LLM (GPT-3.5) | Yes (test execution) |
| **DSPy** | Optimized prompts + demonstrations | Optimizer (BootstrapFewShot, MIPRO) | Any LLM | Metric-based |
| **Meta-Harness** | Full agentic harnesses (tools + prompts + flow) | Agentic proposer (GPT-4+) | Any agent | Execution traces |
| **Voyager** | JavaScript skill functions | GPT-4 | GPT-4 agent | Environment feedback |

### Toolformer vs. LATM

- **Toolformer** teaches an LLM to *use* a fixed, pre-existing set of tools (calculators, search engines). If a task requires a tool that doesn't exist, Toolformer cannot help.
- **LATM** teaches an LLM to *create* new tools on demand. The tool set is not fixed — it grows as new problem classes are encountered.
- LATM subsumes Toolformer's domain: wherever Toolformer uses an existing external API, LATM could create a Python wrapper for that API and cache it.

### DSPy vs. LATM

- **DSPy** compiles LLM pipelines into optimized prompt-and-demonstration combinations. The "what is cached" is a set of prompts and in-context examples.
- **LATM** compiles a problem class into a Python function. The "what is cached" is executable code.
- **Key difference**: DSPy optimization still requires an LLM call at inference time (to apply the optimized prompt); LATM's cached tools execute deterministically without LLM calls after the first use.
- **Relationship**: DSPy is to prompt optimization as LATM is to code synthesis. Both share the compilation metaphor — a powerful process runs once to produce an artifact that is applied cheaply many times.

### Meta-Harness vs. LATM

- **LATM** creates tools (Python functions) for individual problem classes.
- **Meta-Harness** creates harnesses (full agentic pipelines: tools + prompts + control flow + output schemas) for complex multi-step workflows.
- LATM is a special case of Meta-Harness optimization where the harness is a single, pure Python function with no sub-agent calls.
- Meta-Harness addresses LATM's W1 weakness (tools are simple functions) by operating at the level of full harness structure.

### Voyager vs. LATM

- **Voyager** (Wang et al., 2023) uses GPT-4 to generate JavaScript skill functions for a Minecraft agent. Skills are stored in a skill library, retrieved by description similarity, and applied to new tasks.
- **LATM** uses GPT-4 to generate Python tools for reasoning tasks. Tools are stored in a tool cache, retrieved by dispatcher, and applied by a lightweight LLM.
- The architectures are structurally identical; they differ in domain (embodied game agent vs. text reasoning), language (JavaScript vs. Python), and tool user (GPT-4 agent vs. GPT-3.5).
- Voyager can be understood as LATM applied to an open-world sequential decision problem with environment feedback as the verification signal.

## Applications

### Direct Applications

- **Structured reasoning**: Any reasoning task with stable algorithmic structure expressible in Python (date arithmetic, object counting, logical constraint solving, sorting)
- **Cost-sensitive production deployment**: High-volume LLM APIs where paying GPT-4 prices per query is unsustainable but GPT-3.5 quality is insufficient for complex sub-tasks
- **Knowledge distillation via code**: Encoding GPT-4's reasoning capability in verifiable Python functions that lightweight models can leverage

### Abuse SlipBox Applications

The LATM framework provides the theoretical grounding for the Abuse SlipBox's human-as-maker, agent-as-user architecture:

| LATM | Abuse SlipBox | Notes |
|------|--------------|-------|
| Tool Maker (GPT-4) | Human skill designer (model dev, PM, investigator) | Human expertise is the expensive, one-time input |
| Tool User (GPT-3.5) | SlipBox agent | Agent execution is cheap and repeated |
| Python function | Skill (`.claude/skills/<name>/SKILL.md`) | Skill encodes the general procedure for a task class |
| Tool Cache | `.claude/skills/` library | Skill library is the organizational artifact |
| Tool Dispatch | Skill invocation (`/skill-name`) | User explicitly routes requests to appropriate skills |
| Functional caching | Skill reuse | Each new agent invocation amortizes the skill design investment |
| Verification | Skill validation (testing, review) | Skills should be tested before production use |

**Key implication**: The LATM amortization argument justifies investing heavily in skill quality — each improvement to a skill's correctness or robustness pays dividends over all future invocations of that skill.

## Scope and Limitations

- Tools must be expressible as Python functions (does not cover open-ended generation, subjective judgment, or retrieval-dependent tasks)
- No native support for tool composition or chaining
- Dispatcher reliability determines overall system reliability
- Evaluation scope (BBH algorithmically-structured tasks) may not generalize to all production problem types

## Related Terms

- [Toolformer](term_toolformer.md) — LLMs that use pre-existing tools; LATM's predecessor that motivates the "why not create tools?" question
- [DSPy](term_dspy.md) — Compilation-based LLM pipeline optimization; shares the one-time-optimization-for-repeated-use philosophy
- [Meta-Harness](term_meta_harness.md) — Extends LATM's tool creation to full harness creation; LATM is a special case
- [Voyager](term_voyager.md) — Skill library in embodied agents; structurally identical to LATM's tool cache in a different domain
- [LLM](term_llm.md) — Both the Tool Maker and Tool User in LATM are LLMs
- [Function Calling](term_function_calling.md) — LATM's tool use phase is implemented via LLM function calling

## References

### Vault (Literature & Reviews)

- [lit_cai2023latm](../papers/lit_cai2023latm.md) — Primary literature note: Cai et al. (2023), arXiv:2305.17126, ICLR 2024, 276 citations
- [review_cai2023latm](../papers/review_cai2023latm.md) — Full OpenReview-style critical evaluation; Soundness 3/4, Overall 7/10
- [paper_cai2023latm_intro](../papers/paper_cai2023latm_intro.md) — Problem statement and motivation
- [paper_cai2023latm_contrib](../papers/paper_cai2023latm_contrib.md) — Three contributions: two-phase framework, functional caching, tool dispatch
- [paper_cai2023latm_algo](../papers/paper_cai2023latm_algo.md) — Architecture, tool making process, dispatch mechanism, caching comparison
- [paper_cai2023latm_exp_design](../papers/paper_cai2023latm_exp_design.md) — Benchmarks (BBH), models, baselines (GPT-4, GPT-3.5, CoT, PoT)
- [paper_cai2023latm_exp_result](../papers/paper_cai2023latm_exp_result.md) — Performance parity with GPT-4-only, cost analysis, Abuse SlipBox implications

### External

- **arXiv**: [arXiv:2305.17126](https://arxiv.org/abs/2305.17126) — "Large Language Models as Tool Makers"
- **ICLR 2024**: [OpenReview page](https://openreview.net/forum?id=qV83K9d5WB)
- **Authors**: Tianle Cai, Xuezhi Wang, Tengyu Ma, Xinyun Chen, Denny Zhou (Google DeepMind)
