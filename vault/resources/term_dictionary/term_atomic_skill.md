---
tags:
  - resource
  - terminology
  - llm
  - coding_agents
  - reinforcement_learning
  - skill_composition
  - agentic_ai
keywords:
  - atomic skill
  - basis vectors
  - skill decomposition
  - code localization
  - code editing
  - unit-test generation
  - issue reproduction
  - code review
  - GRPO
  - joint RL
  - composability
  - Ma et al.
topics:
  - LLM Coding Agents
  - Skill Decomposition
  - Reinforcement Learning
  - Agentic AI
language: markdown
date of note: 2026-04-10
status: active
building_block: concept
---

# Atomic Skill

## Definition

An **atomic skill** is a minimal, self-contained capability that:
1. Can be **independently trained** with its own execution-grounded reward signal
2. Can be **independently evaluated** on a standalone benchmark
3. **Composes** with other atomic skills to produce complex behaviors
4. Is **not decomposable further** without losing its semantic coherence as a meaningful task primitive

The term is formalized in Ma et al. (2026), *Scaling Coding Agents via Atomic Skills* (arXiv:2604.05013), where 5 atomic skills are identified for software engineering tasks. The paper frames these skills as **basis vectors**: just as any vector in R^n can be expressed as a linear combination of n basis vectors, any SE task can be expressed as a sequence of atomic skill invocations.

> **Simple Definition**: An atomic skill is the smallest unit of capability that can be trained, evaluated, and composed — the "atom" in the chemistry of agent task decomposition.

## Key Properties

### 1. Minimality

An atomic skill cannot be decomposed into simpler sub-skills without losing its meaningful identity as a task primitive. Code localization is atomic because "find the relevant code" cannot be reduced to simpler skills that are independently meaningful in the SE context — it is a primitive act. By contrast, "fix a bug" is not atomic because it decomposes into localization + reproduction + editing + review.

The minimality criterion is relative to a domain: what counts as atomic in software engineering (code editing) may decompose further in other domains (natural language editing, AST manipulation, diff formatting). Atomic skills are domain-specific basis vectors, not universal primitives.

### 2. Self-Containedness

Each atomic skill takes a well-defined input and produces a well-defined output, without requiring the outputs of other skills as prerequisites at training time. This is captured by the formal task instance τ = (k, x, c):
- k = skill type
- x = task input (independent of other skills' outputs)
- c = context (repository, environment — static background, not dynamic skill outputs)

At inference time, atomic skills may be chained (one skill's output becomes another's input), but during training, each skill instance is self-contained.

### 3. Independent Evaluability

Atomic skills can be evaluated on standalone benchmarks with objective metrics:
- Code localization → F1 score on file/line predictions
- Code editing → test pass rate
- Unit-test generation → coverage + mutation kill rate
- Issue reproduction → binary execution success
- Code review → agreement with expert verdicts

This independent evaluability is what makes execution-grounded reward design tractable. If a skill required the outputs of 3 other skills to evaluate, its reward would be confounded and hard to assign credit for.

### 4. Composability

The defining value of atomic skills is that they **recombine** to produce complex behaviors not seen during training. This is the basis vector property: linear independence + span. A model trained on 5 atomic skills generalizes to composite tasks (SWE-bench, SEC-Bench, Terminal-Bench) because those tasks are compositions of the trained skills.

Composability at inference time can be realized through:
- **Sequential chaining**: Localize → Reproduce → Edit → Review (one skill feeds the next)
- **DAG composition**: Skills with shared context but independent outputs, joined by a merge step
- **LangGraph-style orchestration**: Explicit state graph where nodes are skill invocations

### 5. Reusability

Atomic skills, once mastered, apply across task distributions. Code localization trained on Python repositories transfers to Java, TypeScript, and Go repositories. Issue reproduction trained on bug reports transfers to security vulnerabilities and refactoring requests. This cross-distribution reusability is validated by the SWE-bench Multilingual result (+8.9 pp from Python-trained skills to multi-language tasks).

## The 5 Coding Atomic Skills

Ma et al. (2026) identify the following 5 atomic skills as a sufficient basis for software engineering tasks:

| # | Skill | Input x | Output | Reward |
|---|-------|---------|--------|--------|
| 1 | **Code Localization** | Issue description + repo | File paths + line ranges | F1 vs. ground-truth patch locations |
| 2 | **Code Editing** | Code snippet + edit spec | Modified code | Test pass rate |
| 3 | **Unit-Test Generation** | Function/class | Test suite | Coverage × mutation kill rate |
| 4 | **Issue Reproduction** | Issue description + repo | Reproduction script | Binary: reproduces the issue |
| 5 | **Code Review** | Code diff + context | Review comments + verdict | Expert agreement |

### Why These 5?

The 5 skills were derived by analyzing SWE-bench instances and identifying the minimal set of sub-tasks present in every instance. 97.3% of SWE-bench instances decompose cleanly into these 5 skill types with no remainder, suggesting they form a near-complete basis for the SWE-bench distribution.

## Parallel to Tessellum Building Blocks

The Tessellum defines 8 **building blocks** as the atomic types of knowledge notes. The parallel to Ma et al.'s atomic skills is direct:

| Atomic Skills (Ma et al.) | Tessellum Building Blocks |
|--------------------------|------------------------------|
| Code Localization | Concept (locating/defining a term) |
| Code Editing | Procedure (step-by-step instructions for modification) |
| Unit-Test Generation | Hypothesis (testable prediction + verification plan) |
| Issue Reproduction | Empirical Observation (documenting a observed phenomenon) |
| Code Review | Counter-Argument (critical analysis of a claim) |
| — | Argument (positive claim with reasoning) |
| — | Model (structural/causal representation) |
| — | Navigation (index/hub linking atomic notes) |

The mapping is not exact — 5 coding skills ≠ 8 knowledge block types — but the structural analogy is strong:
- Both systems identify a small set of **minimal, self-contained units** that span their respective domains
- Both systems use these units as **training/ingestion targets** (atomic skill RL vs. C.O.D.E. pipeline)
- Both systems demonstrate that **joint processing of all unit types** outperforms single-type optimization (joint RL vs. uniform C.O.D.E.)
- Both systems show that **atomic unit mastery enables composite task generalization** (SWE-bench transfer vs. novel query answering)

## Comparison Table: Atomic Skill vs. Building Block vs. DSPy Module vs. LATM Tool

| Property | Atomic Skill (Ma et al.) | Building Block (SlipBox) | DSPy Module | LATM Tool |
|----------|--------------------------|--------------------------|-------------|-----------|
| **Domain** | Software engineering tasks | Knowledge management | LLM pipeline steps | Structured reasoning |
| **Learning signal** | Execution-grounded RL (GRPO) | Human authorship + C.O.D.E. ingestion | Compiled via LLM optimizer | LLM-generated + test verification |
| **Composability** | Sequential/DAG chaining | Vault links + navigation blocks | Pipeline chaining | Tool dispatch |
| **Evaluation** | Standalone benchmarks (per skill) | Building block quality checks | Signature-level metrics | Test case execution |
| **Discovery** | Manual (task analysis) | Defined a priori (ontology) | Signature-defined by programmer | Problem-class driven |
| **Reusability** | Cross-language, cross-task | Cross-domain note reuse | Cross-prompt-template reuse | Cross-query-class reuse |
| **Atomicity guarantee** | Empirical (97.3% decomposition rate) | Definitional (enforced by C.O.D.E.) | None (modules can be arbitrary size) | None (tools can be complex) |

## Related Terms

- [Term: Building Blocks](term_knowledge_building_blocks.md) — The Tessellum's equivalent of atomic skills; 8 types spanning the knowledge management domain
- [Term: DSPy](term_dspy.md) — Composable LLM modules with typed signatures; DSPy's modules are the closest prior analog to atomic skills in the LLM pipeline context
- Term: LATM — Tool creation and functional caching; tools are reusable skills in a code execution context
- [Term: Meta-Harness](term_meta_harness.md) — Harness-level optimization that builds on atomic skill foundations
- Term: Voyager — Skill library for embodied agents; GPT-4-generated executable skills in Minecraft; the SE analog is coding atomic skills

## References

- Ma et al. (2026). "Scaling Coding Agents via Atomic Skills." arXiv:2604.05013. → Literature Note
- Cai et al. (2023). "Large Language Models as Tool Makers." ICLR 2024. → Literature Note
- Khattab et al. (2023). "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines." → Literature Note
