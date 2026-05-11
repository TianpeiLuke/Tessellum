---
tags:
  - resource
  - terminology
  - agentic_ai
  - multi_agent_systems
  - collaboration
keywords:
  - multi-agent collaboration
  - multi-agent systems
  - agent communication
  - shared knowledge
  - preprint server
  - agent debate
  - division of labor
  - collective intelligence
topics:
  - Multi-Agent Systems
  - Agentic AI
  - Collaboration
language: markdown
date of note: 2026-03-11
status: active
building_block: concept
---

# Multi-Agent Collaboration

## Definition

**Multi-agent collaboration** refers to architectures where multiple AI agents work together toward shared goals, coordinating through communication protocols, shared resources, or structured interaction patterns. Unlike single-agent systems that handle all aspects of a task, multi-agent collaboration distributes responsibilities across specialized agents, enabling division of labor, diverse perspectives, and collective problem-solving.

The paradigm encompasses several interaction modalities:
- **Debate and discussion**: Agents argue different positions to reach better conclusions (e.g., Du et al., 2023)
- **Division of labor**: Agents specialize in subtasks (e.g., Agent Laboratory's PhD/Postdoc/ML Engineer roles)
- **Publication-based sharing**: Agents communicate through shared artifacts rather than direct messages (e.g., AgentRxiv's preprint server)
- **Hierarchical coordination**: Manager agents delegate to worker agents with different capabilities

AgentRxiv (Schmidgall & Moor, 2025) demonstrated that publication-based collaboration — where agents share findings through a preprint server rather than direct communication — enables faster convergence (+13.7% improvement) and accelerated discovery compared to isolated operation. This mirrors how human scientific communities collaborate through publications rather than direct coordination.

## Core Concepts

### Communication Paradigms

| Paradigm | Mechanism | Latency | Interpretability | Example |
|----------|-----------|---------|-------------------|---------|
| **Direct message** | Agents exchange messages in conversation | Low | High | AutoGen, CAMEL |
| **Shared memory** | Agents read/write to common memory store | Low | Medium | SiriuS, MDTeamGPT |
| **Publication-based** | Agents produce documents others can retrieve | High | Very High | AgentRxiv |
| **Competitive** | Agents compete, with selection pressure driving improvement | Variable | Low | Self-play, SPIN |

### Scaling Properties

Multi-agent collaboration introduces trade-offs:
- **Positive**: More diverse exploration, faster convergence to solutions, fault tolerance
- **Negative**: Coordination overhead, redundant work (AgentRxiv: 3x cost for parallel labs), potential for error propagation
- **Key finding from AgentRxiv**: Parallel labs reached 76.2% accuracy in 7 papers vs. 23 papers sequentially, but at 203.9% higher total cost

## Related Terms
- **A2A (Agent2Agent)**: Open protocol enabling cross-vendor agent collaboration

- AgentSpace -- Multi-agent coordination framework
- Self-Evolving Agent -- Agents that improve through multi-agent interaction (social learning)
- Agentic Memory -- Shared memory as a collaboration mechanism
- Compound AI System -- Multi-agent systems as compound AI architectures
- Agent as a Judge -- Evaluation paradigm where agents assess each other's outputs

## References

- Source: lit_schmidgall2025agentrxiv -- Publication-based multi-agent collaboration through shared preprint server
- Source: lit_you2026agent -- Survey covering multi-agent collaboration architectures
- Wu et al. (2023). "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" -- General-purpose multi-agent conversation framework

---

**Last Updated**: March 11, 2026
**Status**: Active
**Domain**: Agentic AI, Multi-Agent Systems

## Related Terms

- [`term_dialectic_knowledge_system`](term_dialectic_knowledge_system.md) — DKS is the persistent-substrate counterpart to MAD; multi-agent collaboration *without* substrate persistence is the contrast case
- [`term_building_block`](term_building_block.md) — Tessellum's 8-type substrate gives multi-agent collaboration a shared typed corpus to coordinate over
- [`term_basb`](term_basb.md) — Forte's "second brain" is the single-agent precursor; multi-agent collaboration extends the idea across multiple reasoners
