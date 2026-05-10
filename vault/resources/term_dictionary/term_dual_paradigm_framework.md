---
tags:
  - resource
  - terminology
  - agentic_ai
  - taxonomy
keywords:
  - dual-paradigm framework
  - symbolic vs neural
  - agentic AI classification
  - paradigm taxonomy
topics:
  - AI Paradigm Classification
language: markdown
date of note: 2026-03-12
status: active
building_block: concept
---

# Dual-Paradigm Framework

## Definition

The **dual-paradigm framework** is a taxonomic model for classifying agentic AI systems along two independent dimensions:

1. **Architectural Paradigm**: Symbolic/Classical (algorithmic planning, persistent state) vs. Neural/Generative (stochastic generation, prompt-driven orchestration)
2. **Degree of Agency & Coordination**: Single-Agent vs. Multi-Agent

The framework was introduced by Abou Ali & Dornaika (2025) to prevent conceptual retrofitting — the misapplication of one paradigm's concepts to describe another.

## Key Properties

- Resolves the conflation of symbolic and neural agentic systems
- Provides paradigm-appropriate evaluation criteria
- Reveals paradigm-market fit across application domains
- Enables paradigm-specific governance frameworks

## Framework Structure

```
                    │ Single-Agent          │ Multi-Agent
────────────────────┼───────────────────────┼──────────────────────
Symbolic/Classical  │ MDP, POMDP, BDI/SOAR │ CNP, Blackboard,
                    │ (algorithmic planning) │ Market-Based
────────────────────┼───────────────────────┼──────────────────────
Neural/Generative   │ LLM-orchestrated      │ AutoGen, CrewAI,
                    │ (prompt-driven)        │ LangGraph
────────────────────┼───────────────────────┼──────────────────────
```

## Paradigm-Market Fit

| Domain | Preferred Paradigm | Rationale |
|--------|-------------------|-----------|
| Healthcare | Symbolic / Deterministic | Safety, privacy (HIPAA), explainability |
| Finance | Neural / Orchestration | Real-time throughput, complex pattern detection |
| Robotics | Hybrid | Physical safety (symbolic) + adaptability (neural) |
| Education | Neural / Conversational | Personalization, natural language interaction |
| Legal | Neural (RAG-Heavy) | Unstructured data + hallucination mitigation |

## Comparison with Alternative Taxonomies

| Taxonomy | Source | Approach | Limitation |
|----------|--------|----------|-----------|
| **Dual-Paradigm** | Abou Ali & Dornaika (2025) | Binary paradigm × binary agency | May oversimplify hybrid systems |
| **Venn Diagram** | Bandi et al. (2025) | GenAI ∩ MAS ∩ Autonomic Computing | Doesn't distinguish architectural mechanisms |
| **What/When/How/Where** | Gao et al. (2025) | 4-dimensional self-evolution taxonomy | Specific to self-evolving agents |
| **Agent-as-a-Judge** | You et al. (2026) | Evaluation-centric hierarchy | Focused on assessment, not architecture |

## Related Terms

- [Conceptual Retrofitting](term_conceptual_retrofitting.md) — the problem this framework is designed to solve
- [Neuro-Symbolic AI](term_neuro_symbolic.md) — the hybrid approach the framework identifies as the future
- [Multi-Agent Collaboration](term_multi_agent_collaboration.md) — one axis of the framework

## References

- [Agentic AI Survey (Abou Ali & Dornaika, 2025)](../papers/lit_abouali2025agentic.md) — source paper
- [Rise of Agentic AI (Bandi et al., 2025)](../papers/lit_bandi2025rise.md) — alternative taxonomy for comparison
- [Self-Evolving Agents Survey (Gao et al., 2025)](../papers/lit_gao2025survey.md) — complementary taxonomy
