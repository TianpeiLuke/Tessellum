---
tags:
  - resource
  - terminology
  - agentic_ai
  - memory_systems
  - knowledge_graphs
  - cognitive_science
keywords:
  - PlugMem
  - task-agnostic memory
  - knowledge-centric memory graph
  - plugin memory module
  - LLM agents
  - memory-to-knowledge abstraction
  - structuring module
  - retrieval module
  - reasoning module
  - propositional knowledge
  - prescriptive knowledge
  - fact block
  - workflow block
  - memory information density
  - PMI
  - episodic memory
  - semantic memory
  - procedural memory
topics:
  - Agentic AI
  - Memory Systems
  - Knowledge Representation
language: markdown
date of note: 2026-03-27
status: active
building_block: concept
---

# PlugMem

## Definition

**PlugMem** is a task-agnostic plugin memory module for LLM agents that transforms raw episodic experience into a **knowledge-centric memory graph** organized around [propositional knowledge](term_propositional_knowledge.md) (Fact Blocks — "knowing that") and [prescriptive knowledge](term_prescriptive_knowledge.md) (Workflow Blocks — "knowing how"). It can be attached to arbitrary LLM agents without task-specific redesign, performing **memory-to-knowledge abstraction** that converts verbose interaction histories into compact, reusable knowledge units.

The critical design departure from prior graph-based methods like [GraphRAG](term_graphrag.md) and [HippoRAG](term_hipporag.md) is that PlugMem treats **knowledge — not entities or text chunks — as the fundamental unit of memory access and organization**. Concepts and intents serve as abstract routing signals for retrieval, while propositions and prescriptions are the actual content nodes. This bipartite structure enables efficient multi-hop retrieval across distant parts of the knowledge graph.

Introduced by Yang et al. (2026) at UIUC, Tsinghua University, and Microsoft Research.

## Historical Context

| Year | System | Approach | Limitation Addressed by PlugMem |
|------|--------|----------|--------------------------------|
| 2021 | Vanilla RAG (Lewis et al.) | Flat retrieval over unstructured episodic memory | Knowledge sparsity — raw memories are verbose, decision-relevant info is sparse |
| 2024 | GraphRAG (Edge et al.) | Entity-centric graph with community summaries | Entity-level, not knowledge-level organization |
| 2024 | AWM (Wang et al.) | Task-specific procedural workflow memory | Non-transferable — optimized for web navigation only |
| 2025 | A-Mem (Xu et al.) | Zettelkasten-inspired agentic memory | Task-agnostic but less effective due to emergent (unconstrained) structure |
| 2025 | HippoRAG2 (Gutiérrez et al.) | Hippocampal-inspired entity + passage retrieval | Entity-level indexing; retrieves dialogue chunks, not knowledge |
| 2025 | Zep (Rasmussen et al.) | Temporal knowledge graph for agent memory | Task-specific temporal structure |
| 2025 | ReasoningBank (Ouyang et al.) | Scaling agents with reasoning memory | Task-specific knowledge representation |
| **2026** | **PlugMem (Yang et al.)** | **Knowledge-centric memory graph with cognitive science foundations** | **First task-agnostic system to outperform task-specific designs across heterogeneous benchmarks** |

PlugMem grounds its design in cognitive science: Tulving (1972) distinguished episodic from semantic memory; Squire (2004) added procedural memory to the taxonomy. PlugMem operationalizes this tripartite model for LLM agents.

## Taxonomy

### Three-Module Architecture

| Module | Function | Input → Output |
|--------|----------|---------------|
| **Structuring** | Transforms raw episodic memory into knowledge-dense representations | Raw interactions → Standardized episodes → Semantic graph $G^S$ + Procedural graph $G^P$ |
| **Retrieval** | Selects task-relevant knowledge via abstraction-aware multi-hop traversal | Query → Abstract routing through concepts/intents → Relevant propositions/prescriptions |
| **Reasoning** | Compresses retrieved knowledge into actionable guidance | Retrieved memory (many tokens) → Task-adaptive summary (few tokens) |

### Memory Type Mapping

| Memory Type | Nature | Knowledge-Dense Unit | Graph Structure |
|-------------|--------|---------------------|----------------|
| **Semantic** | Declarative, context-independent facts | Proposition (Fact Block) | Concept-centric: concepts as lightweight indices → propositions |
| **Procedural** | Executive, goal-oriented "how-to" | Prescription (Workflow Block) | Intent-centric: intents as keys → prescriptions (with return scores) |
| **Episodic** | Autobiographical, raw interaction record | Source Trace (Event Window) | Anchor: episodic acts as "ground truth"; Knowledge ←proves→ Source |

### Graph Operations

| Operation | Description |
|-----------|-------------|
| **Create** | Insert new experience → standardize → extract knowledge |
| **Retrieve** | Select task-relevant subgraphs via multi-hop traversal |
| **Update** | Atomic merge & split when new evidence arrives |
| **Delete** | Decay & compress low-utility nodes |

## Key Properties

- **Task-agnostic**: Evaluated *unchanged* across conversational QA (LongMemEval), multi-hop retrieval (HotpotQA), and web agent tasks (WebArena)
- **Knowledge-centric**: Graph nodes are knowledge units (propositions/prescriptions), not entities or text chunks
- **Bipartite graph structure**: High-level nodes (concepts/intents) route retrieval; low-level nodes (propositions/prescriptions) store content
- **Provenance-preserving**: All knowledge traces back to source episodic memory via provenance edges, enabling verification
- **Quality-aware reuse**: Prescriptions carry return scores measuring how well the intent was achieved
- **Token-efficient**: Achieves 1-2 orders of magnitude reduction in memory tokens compared to baselines
- **Cognitively motivated**: Architecture grounded in Tulving's episodic-semantic distinction and Ryle's knowing-that/knowing-how distinction

## Notable Systems / Implementations

| System | Relationship to PlugMem | Key Difference |
|--------|------------------------|----------------|
| **PlugMem** | The system itself | Knowledge-centric, task-agnostic |
| [GraphRAG](term_graphrag.md) | Entity-centric alternative | Nodes are entities/text chunks, not knowledge units |
| [HippoRAG](term_hipporag.md) | Hippocampal-inspired alternative | Entity-level indexing with PPR routing |
| [A-Mem](term_agentic_memory.md) | Zettelkasten-inspired alternative | Emergent structure via agent agency; no cognitive science constraints |
| [AWM](../papers/lit_yang2026plugmem.md) | Task-specific procedural memory | Only procedural memory; web navigation only |
| [ReasoningBank](../papers/lit_yang2026plugmem.md) | Task-specific reasoning memory | Tightly coupled to specific benchmarks |
| **Abuse SlipBox** | Structural analog | Term notes ≈ Fact Blocks; SOP notes ≈ Workflow Blocks; entry points ≈ concept routing nodes |

## Applications

| Domain | Application | How PlugMem Applies |
|--------|-------------|-------------------|
| **Long-horizon Conversational QA** | LongMemEval benchmark | Extract user preferences as propositions; retrieve via concept routing across long histories |
| **Multi-hop Knowledge Retrieval** | HotpotQA benchmark | Bridge-entity discovery via abstraction-to-specificity interleaving across Wikipedia articles |
| **Web Agent Tasks** | WebArena benchmark | Extract reusable navigation prescriptions; transfer procedural knowledge across websites |
| **Abuse Investigation** (potential) | Case memory for investigation agents | Extract abuse pattern propositions and investigation workflow prescriptions from case histories |
| **Knowledge Management** (potential) | Zettelkasten-style knowledge bases | Formalize atomic notes as knowledge units with typed graph relationships |

## Empirical Results

### Performance Across Benchmarks

| Benchmark | PlugMem | Best Baseline | Improvement | Token Reduction |
|-----------|---------|---------------|-------------|-----------------|
| **LongMemEval** (Acc.) | **75.1%** | 73.0% (LiCoMemory) | +2.1 | 10x fewer tokens (363 vs. 3743+) |
| **HotpotQA** (EM) | **61.4** | 60.0 (HippoRAG2) | +1.4 | 7x fewer tokens (82 vs. 595) |
| **WebArena** (SR on/off) | **52.6/58.4** | 44.7/44.3 (A-Mem) | +7.9/+14.1 | 67x fewer tokens (301 vs. 20,516) |

### Memory Information Density

| Benchmark | PlugMem Density | Best Baseline Density | Density Ratio |
|-----------|----------------|----------------------|---------------|
| LongMemEval | **1.6e-2** | 9.3e-4 (LiCoMemory) | 17x higher |
| HotpotQA | **1.4e-1** | 1.9e-2 (HippoRAG2) | 7x higher |
| WebArena | **1.4e-3** | 3.4e-7 (A-Mem) | 4,100x higher |

### Ablation Summary

| Component Removed | Effect | Interpretation |
|-------------------|--------|---------------|
| **No Retrieval** | Most severe degradation | Memory is only useful when accessible at decision time |
| **No Structuring** | Moderate degradation | Structuring determines *what* retrieval can access |
| **No Reasoning** | Modest accuracy loss, large token increase | Reasoning controls *how efficiently* memory is consumed |

## Challenges and Limitations

### Computational
- **Structuring cost**: Multiple LLM calls (Qwen2.5-32B/72B) per episodic unit for standardization and knowledge extraction — total system cost not quantified
- **LLM dependency**: Quality of extracted knowledge depends on instruction-following quality of the structuring LLM

### Evaluation
- **Narrow LLM evaluation**: Only tested with Qwen2.5 + GPT-4o; unclear how it performs with weaker or different model families
- **Limited graph operation evaluation**: Update and delete operations evaluated only in appendix
- **Three benchmarks**: While diverse, may not represent all agentic task types (e.g., no adversarial, multi-user, or privacy-constrained scenarios)

### Theoretical
- **Cognitive science analogy**: The mapping from cognitive memory types to graph structures is motivated by analogy, not formally grounded — no evidence LLMs process propositional vs. prescriptive knowledge differently
- **Missing comparison**: MemGPT/Letta (Packer et al., 2024) is a prominent task-agnostic memory system not included in comparisons

## Questions

### Validation (Socratic — "Why?")
1. Is the knowledge-centric organization genuinely novel, or is it an exaptation of hierarchical summarization (like RAPTOR) applied to agent memory? What specifically about treating knowledge as the memory unit produces gains that hierarchical entity organization cannot achieve?
   - **Tests**: Genuine conceptual innovation vs. engineering refinement (Innovation Assessment)

2. PlugMem's structuring module requires Qwen2.5-32B/72B for knowledge extraction — what is the total computational cost (structuring + retrieval + reasoning) compared to simpler baselines, and does token efficiency at inference offset structuring cost at indexing time?
   - **Tests**: Whether the system is practically deployable (WYSIATI — missing cost data)

### Application (Taxonomic — "What If? / How?")
3. How would PlugMem handle memory that accumulates over thousands of episodes — does the knowledge graph remain effective at scale, or do update/delete operations become bottlenecks?
   - **Tests**: Long-running agent scalability (Scale Shift)

4. Could PlugMem's architecture be applied to build a shared investigation memory across multiple abuse analysts — where propositions capture known abuse patterns and prescriptions encode proven investigation workflows?
   - **Tests**: Multi-user collaborative memory application (Adjacent Possible)

### Synthesis (Lateral — "Who Else?")
5. How does PlugMem's concept-centric semantic memory compare to [HippoRAG](term_hipporag.md)'s PPR-based entity routing — could the two be combined (hippocampal indexing for entity discovery + knowledge graphs for abstraction)?
   - **Tests**: Complementarity of two graph-based memory approaches (Liquid Network)

6. The Abuse SlipBox already implements PlugMem's architecture informally (term notes ≈ Fact Blocks, SOPs ≈ Workflow Blocks, entry points ≈ concept routing) — what specific vault improvements would formalize this mapping? See [analysis_plugmem_lens_on_abuse_slipbox](../analysis_thoughts/analysis_plugmem_lens_on_abuse_slipbox.md).
   - **Tests**: Practical vault improvement roadmap (Operationalization)

## Related Terms

- **[Propositional Knowledge](term_propositional_knowledge.md)**: "Knowing that" — semantic memory operationalized as Fact Blocks in PlugMem's semantic graph
- **[Prescriptive Knowledge](term_prescriptive_knowledge.md)**: "Knowing how" — procedural memory operationalized as Workflow Blocks in PlugMem's procedural graph
- **[Memory Information Density](term_memory_information_density.md)**: Information-theoretic metric introduced by PlugMem for evaluating memory efficiency ($\rho = \text{PMI} / |m|$)
- **[Agentic Memory](term_agentic_memory.md)**: Broader paradigm where agents control memory organization; PlugMem adds cognitive science constraints
- **[GraphRAG](term_graphrag.md)**: Entity-centric graph approach that PlugMem departs from by using knowledge units as nodes
- **[HippoRAG](term_hipporag.md)**: Hippocampal-inspired entity-level retrieval; key baseline that PlugMem outperforms
- **[RAG](term_rag.md)**: Vanilla retrieval baseline; PlugMem addresses RAG's knowledge sparsity problem
- **[Knowledge Graph](term_knowledge_graph.md)**: Traditional KGs use entities as nodes; PlugMem uses knowledge units
- **[Experience Replay](term_experience_replay.md)**: RL technique where raw transitions are stored and replayed; PlugMem's episodic-to-knowledge transformation is an abstracted form of replay
- **[Context Engineering](term_context_engineering.md)**: PlugMem's reasoning module performs task-adaptive context compression
- **[Knowledge Building Blocks](term_knowledge_building_blocks.md)**: Propositions and prescriptions as atomic, self-contained knowledge units
- **[Self-Evolving Agent](term_self_evolving_agent.md)**: PlugMem's knowledge transfer results show agents improving through accumulated memory

## References

### Vault Sources
- [PlugMem Paper](../papers/lit_yang2026plugmem.md) — Full literature note with abstract, summary, and vault connections
- [PlugMem Method](../papers/paper_yang2026plugmem_algo.md) — Detailed three-module architecture, graph structures, and retrieval algorithm
- [PlugMem Contributions](../papers/paper_yang2026plugmem_contrib.md) — Four contributions and positioning among related work
- [PlugMem Experiment Design](../papers/paper_yang2026plugmem_exp_design.md) — Three benchmarks, baselines, and PMI framework
- [PlugMem Experiment Results](../papers/paper_yang2026plugmem_exp_result.md) — Results tables, ablations, and knowledge transfer analysis
- [PlugMem Review](../papers/review_yang2026plugmem.md) — OpenReview-style evaluation: Soundness 3/4, Overall 7/10
- [PlugMem Lens on Abuse SlipBox](../analysis_thoughts/analysis_plugmem_lens_on_abuse_slipbox.md) — How PlugMem's framework explains and improves the vault

### External Sources
- [Yang et al. (2026). "PlugMem: A Task-Agnostic Plugin Memory Module for LLM Agents." arXiv:2603.03296.](https://arxiv.org/abs/2603.03296)
- [TIMAN-group/PlugMem — GitHub Repository](https://github.com/TIMAN-group/PlugMem)
- [Tulving, E. (1972). "Episodic and Semantic Memory." *Organization of Memory*.](https://psycnet.apa.org/record/1973-08477-007) — Foundational episodic-semantic distinction
- [Squire, L.R. (2004). "Memory systems of the brain." *Neurobiology of Learning and Memory*.](https://pubmed.ncbi.nlm.nih.gov/15504407/) — Extended memory taxonomy
- [Ryle, G. (1949). *The Concept of Mind*.](https://en.wikipedia.org/wiki/The_Concept_of_Mind) — "Knowing-that" vs. "knowing-how"
- [Microsoft Research Blog: From Raw Interaction to Reusable Knowledge](https://www.microsoft.com/en-us/research/blog/from-raw-interaction-to-reusable-knowledge-rethinking-memory-for-ai-agents/) — PlugMem overview
