---
tags:
  - resource
  - terminology
  - agentic_ai
  - epistemology
keywords:
  - conceptual retrofitting
  - paradigm conflation
  - BDI
  - PPAR
  - LLM agents
topics:
  - AI Paradigm Classification
language: markdown
date of note: 2026-03-12
status: active
building_block: concept
---

# Conceptual Retrofitting

## Definition

**Conceptual retrofitting** is the misapplication of classical symbolic AI frameworks (e.g., Belief-Desire-Intention (BDI), Perceive-Plan-Act-Reflect (PPAR) loops) to describe modern LLM-based agentic systems that operate on fundamentally different principles of stochastic generation and prompt-driven orchestration.

This practice:
- Obscures the true operational mechanics of LLM-based agents
- Creates a false sense of continuity between incompatible architectural paradigms
- Impedes accurate system classification and evaluation

## Examples

| Retrofitted Concept | Symbolic Origin | Actual Neural Mechanism |
|---------------------|----------------|------------------------|
| "The agent *plans*" | Symbolic planning (A* search, STRIPS, hierarchical task networks) | LLM generates next steps via stochastic token prediction; no explicit search |
| "The agent has *beliefs*" | BDI belief module (symbolic knowledge base) | Information exists in the context window; no persistent belief representation |
| "The agent *reasons*" | Logical inference, theorem proving | Pattern matching on training data distributions; emergent, not deductive |
| "PPAR loop" | Perceive-Plan-Act-Reflect as explicit algorithmic stages | Prompt chaining where each "stage" is a different prompt template, not a cognitive module |

## Why It Matters

1. **Impedes accurate evaluation**: If we describe an LLM agent as "planning," we may evaluate it on plan optimality — a metric that doesn't capture its actual stochastic generation behavior
2. **Creates false security**: Describing neural agents in symbolic terms suggests they have the determinism and verifiability of symbolic systems, when they do not
3. **Blocks innovation**: Forces researchers to frame novel neural mechanisms in legacy terms rather than developing appropriate new vocabulary
4. **Governance mismatch**: Leads to regulation designed for symbolic properties (verifiability, explainability) being applied to fundamentally opaque neural systems

## Origin

Term introduced by Abou Ali & Dornaika (2025) in their dual-paradigm framework for agentic AI classification. The concept builds on broader philosophy-of-science critiques of anachronistic conceptual application, but is specifically operationalized for the symbolic-to-neural AI paradigm shift.

## Related Terms

- [Dual-Paradigm Framework](term_dual_paradigm_framework.md) — the taxonomy designed to prevent conceptual retrofitting
- [Neuro-Symbolic AI](term_neuro_symbolic.md) — hybrid approach that intentionally bridges paradigms (not retrofitting)
- [Multi-Agent Collaboration](term_multi_agent_collaboration.md) — coordination mechanisms differ fundamentally by paradigm
- [Self-Evolving Agent](term_self_evolving_agent.md) — neural paradigm concept that resists symbolic framing
- [Transformer](term_transformer.md) — the architecture that created the paradigm shift

## References

- [Agentic AI Survey (Abou Ali & Dornaika, 2025)](../papers/lit_abouali2025agentic.md) — source of the term
- [Rise of Agentic AI (Bandi et al., 2025)](../papers/lit_bandi2025rise.md) — exhibits some conceptual retrofitting by applying BDI/ReAct uniformly
