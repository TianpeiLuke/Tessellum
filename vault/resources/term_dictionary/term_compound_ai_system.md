---
tags:
  - resource
  - terminology
  - llm_agents
  - systems
keywords:
  - compound AI system
  - multi-component AI
  - LLM pipeline
  - AI system composition
  - agentic systems
topics:
  - LLM Agents
  - Systems Design
language: markdown
date of note: 2026-03-09
status: active
building_block: concept
---

# Term: Compound AI System

## Definition

A **compound AI system** is an AI application that combines multiple interacting components — LLM calls, retrieval modules, code executors, domain-specific tools, and other processing steps — orchestrated together to solve complex tasks. The term was popularized by Zaharia et al. (2024) to describe the paradigm shift from training individual monolithic models to building multi-component systems where the overall system behavior emerges from the interaction of its parts.

Compound AI systems are distinguished from single-model approaches by having **multiple optimizable components** — each of which may have its own inputs, outputs, and failure modes. This creates the need for system-level optimization frameworks like TextGrad (Yuksekgonul et al., 2024), which models compound AI systems as computation graphs with textual backpropagation.

## Examples

| System Type | Components | Optimization Challenge |
|-------------|-----------|----------------------|
| RAG pipeline | Retriever + Reranker + Generator LLM | Joint optimization of retrieval and generation |
| Code assistant | Planner LLM + Code generator + Test runner + Debugger | Multi-step optimization with external tool feedback |
| Agent system | Reasoning LLM + Tool calls + Memory + Planning | Coordination across components with different capabilities |
| Scientific AI | LLM + Domain simulator + Constraint checker | Interfacing LLM decisions with domain-specific tools |

## Key Properties

| Property | Description |
|----------|-------------|
| **Multi-component** | Multiple LLM calls and/or tools orchestrated together |
| **Emergent behavior** | System behavior arises from component interactions, not any single model |
| **Optimizable at multiple levels** | Each component can be independently optimized (prompt, retrieval config, tool parameters) |
| **Computation graph structure** | Components form a DAG where outputs of one feed into inputs of another |

## Related Terms

- [RAG](term_rag.md) — A common type of compound AI system (retriever + generator)
- [Textual Gradient](term_textual_gradient.md) — Optimization signal for compound AI systems
- [Instance Optimization](term_instance_optimization.md) — Test-time optimization of individual compound system outputs
- [Prompt Optimization](term_prompt_optimization.md) — Optimizing the prompt component of compound systems
- [Self-Evolving Agent](term_self_evolving_agent.md) — Agents that improve their own compound system components
- [AgentZ](term_agentz.md) — Amazon's compound AI platform combining LLMs, tools, and HITL
- **[Neural Computer](term_neural_computer.md)**: NCs propose collapsing compound multi-component systems into a single neural runtime
- **[World Model](term_world_model.md)**: World models can serve as planning and simulation components within compound AI systems

## References

- Zaharia, M. et al. (2024). "The Shift from Models to Compound AI Systems." BAIR Blog.
- Yuksekgonul, M. et al. (2024). "TextGrad: Automatic 'Differentiation' via Text." arXiv:2406.07496 — [lit_yuksekgonul2024textgrad](../papers/lit_yuksekgonul2024textgrad.md)
