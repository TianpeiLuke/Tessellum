---
tags:
  - resource
  - terminology
  - agentic_ai
  - cognitive_science
  - memory_systems
  - reinforcement_learning
keywords:
  - episodic memory
  - EM
  - event memory
  - experience replay
  - context-sensitive memory
  - single-shot learning
  - complementary learning systems
  - long-term memory
  - memory consolidation
topics:
  - memory systems
  - agentic AI
  - cognitive science
  - reinforcement learning
language: markdown
date of note: 2026-03-30
status: active
building_block: concept
---

# Episodic Memory

## Definition

Episodic memory is a memory system that stores specific experiences and events — what happened, when, where, and in what context — enabling an agent to recall past interactions and learn from prior task executions. Originally defined by Endel Tulving (1972) in cognitive science, episodic memory refers to the ability to recall particular past events that one participated in personally, as distinct from semantic memory (general facts) and procedural memory (skills and habits). In the context of AI agents, episodic memory enables the formation and retrieval of memories of events that happen post-deployment at runtime, supporting adaptive and context-sensitive behavior over extended timescales.

Episodic memory is distinguished from other memory types by a unique combination of five key properties: (1) long-term storage, (2) explicit reasoning over stored content, (3) single-shot learning from individual exposures, (4) instance-specific memories tied to particular events, and (5) contextual relations binding when, where, and why an event occurred.

## Historical Context

| Year | Milestone |
|------|-----------|
| 1972 | Endel Tulving introduces the distinction between episodic and semantic memory |
| 1995 | McClelland, McNaughton & O'Reilly propose Complementary Learning Systems (CLS) theory |
| 2002 | O'Reilly & Norman formalize hippocampal fast learning vs. neocortical slow learning |
| 2016 | Kumaran et al. update CLS theory for deep learning era |
| 2018 | Episodic memory integrated into RL agents (NEC, EMAC) |
| 2024 | Fountas et al. propose human-like episodic memory for infinite-context LLMs |
| 2025 | Pink et al. present episodic memory as unifying framework for long-term LLM agents |

## Taxonomy

| Memory Type | Long-term | Explicit | Single-shot | Instance-specific | Contextual |
|-------------|-----------|----------|-------------|-------------------|------------|
| **Episodic** | ✓ | ✓ | ✓ | ✓ | ✓ |
| Procedural | ✓ | ✗ | ✗ | ✗ | ✗ |
| Semantic | ✓ | ✓ | ✗ | ✗ | ✗ |
| Working | ✗ | ✓ | ✓ | ✓ | ✓ |

## Key Properties

- **Long-term storage**: Retains memories across arbitrary timescales, unlike working memory which is transient
- **Explicit reasoning**: Stored content can be directly queried and used in reasoning processes
- **Single-shot learning**: Captures information from a single exposure without requiring repeated training
- **Instance-specific**: Stores details unique to particular occurrences, including past reasoning traces and decisions
- **Contextual relations**: Binds temporal, spatial, and causal context to memory content, enabling retrieval based on contextual cues
- **Complementary to semantic memory**: Episodic memories can be consolidated into generalized semantic knowledge over time
- **Encoding-retrieval-consolidation cycle**: Three core operations — encoding new experiences, retrieving relevant past episodes, and consolidating into parametric knowledge

## Notable Systems / Implementations

| System | Mechanism | Application |
|--------|-----------|-------------|
| Neural Episodic Control (NEC) | Differentiable neural dictionary for fast value estimation | RL game playing |
| Larimar | Distributed external memory with episodic control for LLMs | Fact editing, long-context QA |
| EM-LLM (Fountas et al.) | Bayesian surprise-based event segmentation with episodic retrieval | Infinite-context LLM reasoning |
| SENTRIX/PROPHET | Episodic memory of past reasoning trajectories for phishing detection | Phishing URL detection at Amazon |
| HippoRAG | Neurobiologically-inspired long-term memory using hippocampal indexing | Knowledge-intensive QA |
| MemoryBank | Timestamps and personality profiles as contextual episodic storage | Long-range open-domain conversation |
| Self-Evolving Agents | Runtime RL on episodic memory for continuous agent improvement | Autonomous agent adaptation |

## Applications

| Domain | Application |
|--------|-------------|
| **Fraud Detection** | Storing past reasoning trajectories to guide decisions on recurring threats (e.g., SENTRIX at Amazon) |
| **Reinforcement Learning** | Experience replay buffers enabling sample-efficient learning from past episodes |
| **Conversational AI** | Recalling prior interactions for consistent, personalized assistance |
| **Autonomous Research** | Tracking literature reviews, data analyses, and hypothesis generation over time |
| **Software Development** | Maintaining context across long-running projects with evolving requirements |

## Challenges and Limitations

- **Capacity management**: External episodic stores grow unboundedly; forgetting and consolidation mechanisms are needed
- **Retrieval efficiency**: Finding relevant episodes from large stores without prohibitive computational cost
- **Consolidation**: Transferring episodic knowledge into parametric memory without catastrophic forgetting remains unsolved
- **Event segmentation**: Determining when to segment continuous experience into discrete episodes is non-trivial
- **Contextual fidelity**: Preserving rich contextual relations during compression and storage
- **Evaluation**: Lack of standardized benchmarks for assessing episodic memory in LLM agents

## Related Terms
- **[Reinforcement Learning](term_rl.md)**: RL agents use experience replay as a form of episodic memory
- **[Continual Learning](term_continual_learning.md)**: Episodic memory helps prevent catastrophic forgetting in continual learning
- **[RAG](term_rag.md)**: External memory retrieval approach that partially implements episodic memory properties
- **[GraphRAG](term_graphrag.md)**: Structured graph-based retrieval that adds contextual relations to RAG
- **[Knowledge Graph](term_knowledge_graph.md)**: Structured knowledge representation complementary to episodic storage
- **[Self-Evolving Agent](term_self_evolving_agent.md)**: Agents that use episodic memory for runtime self-improvement
- **[LLM](term_llm.md)**: Large language models that episodic memory systems augment for long-term operation
- **[Multi-Modal](term_multi_modal.md)**: Episodic memories can span multiple modalities (text, images, actions)

## References

### Vault Sources
- [BRP ML Research 2026 - #11 SENTRIX](../../0_entry_points/entry_brp_ml_research_2026.md) — SENTRIX uses episodic memory of past reasoning trajectories for phishing detection

### External Sources
- [Tulving, E. (1972). "Episodic and semantic memory." Organization of Memory, Academic Press](https://en.wikipedia.org/wiki/Episodic_memory)
- [Pink et al. (2025). "Episodic Memory is the Missing Piece for Long-Term LLM Agents." arXiv:2502.06975](https://arxiv.org/html/2502.06975v1)
- [Fountas et al. (2024). "Human-like Episodic Memory for Infinite Context LLMs." arXiv:2407.09450](https://arxiv.org/abs/2407.09450)
- [Botvinick et al. (2019). "Reinforcement Learning and Episodic Memory in Humans and Animals." Annual Review of Psychology](https://www.annualreviews.org/content/journals/10.1146/annurev-psych-122414-033625)
- [GeeksforGeeks: Episodic Memory in AI Agents](https://www.geeksforgeeks.org/artificial-intelligence/episodic-memory-in-ai-agents/)
