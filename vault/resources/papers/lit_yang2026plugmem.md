---
tags:
  - resource
  - literature_note
  - agentic_ai
  - memory_systems
  - knowledge_graphs
  - cognitive_science
keywords:
  - PlugMem
  - task-agnostic memory
  - knowledge-centric memory graph
  - propositional knowledge
  - prescriptive knowledge
  - episodic memory
  - semantic memory
  - procedural memory
  - memory-to-knowledge abstraction
  - memory information density
  - PMI
  - LLM agents
topics:
  - Agentic AI
  - Memory Systems
  - Knowledge Representation
domain: "Agentic AI"
language: markdown
date of note: 2026-03-27
paper_title: "PlugMem: A Task-Agnostic Plugin Memory Module for LLM Agents"
authors:
  - Ke Yang
  - Zixiang Chen
  - Xuan He
  - Jize Jiang
  - Michel Galley
  - Chenglong Wang
  - Jianfeng Gao
  - Jiawei Han
  - C. Zhai
year: 2026
source: "arXiv:2603.03296"
venue: "arXiv (preprint)"
arXiv: "2603.03296"
semantic_scholar_id: "6ae3fb18300289acc53af5535508500992aa185c"
zotero_key: "K4I37IXH"
paper_id: yang2026plugmem
paper_notes:
  - paper_yang2026plugmem_intro.md
  - paper_yang2026plugmem_contrib.md
  - paper_yang2026plugmem_algo.md
  - paper_yang2026plugmem_exp_design.md
  - paper_yang2026plugmem_exp_result.md
review_note: review_yang2026plugmem.md
status: active
building_block: hypothesis
---

# PlugMem: A Task-Agnostic Plugin Memory Module for LLM Agents

## Metadata

| Field | Value |
|-------|-------|
| **Paper** | PlugMem: A Task-Agnostic Plugin Memory Module for LLM Agents |
| **Authors** | Ke Yang, Zixiang Chen, Xuan He, Jize Jiang, Michel Galley, Chenglong Wang, Jianfeng Gao, Jiawei Han, C. Zhai |
| **Year** | 2026 |
| **Venue** | arXiv (preprint) |
| **Affiliations** | UIUC, Tsinghua University, Microsoft Research |
| **arXiv** | [2603.03296](https://arxiv.org/abs/2603.03296) |
| **Semantic Scholar** | [6ae3fb18...](https://www.semanticscholar.org/paper/6ae3fb18300289acc53af5535508500992aa185c) |
| **Zotero** | K4I37IXH |
| **Citations** | 1 (new preprint) |
| **Code** | [TIMAN-group/PlugMem](https://github.com/TIMAN-group/PlugMem) |

## Abstract

Long-term memory is essential for large language model (LLM) agents operating in complex environments, yet existing memory designs are either task-specific and non-transferable, or task-agnostic but less effective due to low task-relevance and context explosion from raw memory retrieval. We propose PlugMem, a task-agnostic plugin memory module that can be attached to arbitrary LLM agents without task-specific redesign. Motivated by the fact that decision-relevant information is concentrated as abstract knowledge rather than raw experience, we draw on cognitive science to structure episodic memories into a compact, extensible knowledge-centric memory graph that explicitly represents propositional and prescriptive knowledge. This representation enables efficient memory retrieval and reasoning over task-relevant knowledge, rather than verbose raw trajectories, and departs from other graph-based methods like GraphRAG by treating knowledge as the unit of memory access and organization instead of entities or text chunks. We evaluate PlugMem unchanged across three heterogeneous benchmarks (long-horizon conversational question answering, multi-hop knowledge retrieval, and web agent tasks). The results show that PlugMem consistently outperforms task-agnostic baselines and exceeds task-specific memory designs, while also achieving the highest information density under a unified information-theoretic analysis.

## Table of Contents

| Section | Note | Key Content |
|---------|------|-------------|
| **Introduction** | [paper_yang2026plugmem_intro](paper_yang2026plugmem_intro.md) | Task-specific memory modules fail to generalize; raw episodic retrieval suffers from knowledge sparsity and context explosion; cognitive science motivates knowledge-level abstraction |
| **Contribution** | [paper_yang2026plugmem_contrib](paper_yang2026plugmem_contrib.md) | Four contributions: cognitively motivated design principles, information-theoretic evaluation framework (PMI/Memory Information Density), general plugin memory module, reproducibility |
| **Method** | [paper_yang2026plugmem_algo](paper_yang2026plugmem_algo.md) | Three-module architecture: Structuring (episodic → semantic + procedural knowledge graphs), Retrieval (abstraction-aware multi-hop), Reasoning (task-adaptive compression); knowledge-centric memory graph with propositions, prescriptions, concepts, intents |
| **Experiment Design** | [paper_yang2026plugmem_exp_design](paper_yang2026plugmem_exp_design.md) | Three benchmarks: LongMemEval (conversational QA), HotpotQA (multi-hop retrieval), WebArena (web agent tasks); baselines grouped as vanilla, task-agnostic, task-specific |
| **Experiment Results** | [paper_yang2026plugmem_exp_result](paper_yang2026plugmem_exp_result.md) | PlugMem achieves 75.1% on LongMemEval, 61.4 EM on HotpotQA, 52.6/58.4 SR on WebArena; highest information density (1.6e-2, 1.4e-1, 1.4e-3); ablations show retrieval is the bottleneck, structuring determines what can be retrieved, reasoning controls efficiency |
| **Review** | [review_yang2026plugmem](review_yang2026plugmem.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 7 questions (6 review lenses applied) |

## Summary

- **Background**: LLM agents need long-term memory for complex environments, but existing designs are either task-specific (non-transferable) or task-agnostic (ineffective due to knowledge sparsity in raw retrieval). Cognitive science distinguishes episodic, semantic, and procedural memory — effective agent memory should transform raw experience into structured knowledge. <!-- VERIFY -->
- **Contribution**: (1) Cognitively motivated design principles for task-agnostic memory. (2) Information-theoretic evaluation framework: PMI (decision information gain per token) and Memory Information Density. (3) PlugMem: a plugin memory module applicable across heterogeneous benchmarks unchanged. (4) Released code and data.
- **Method**: Three-module pipeline: *Structuring* standardizes episodic memory into (o,s,a,r,g) tuples, then extracts propositional knowledge (fact blocks) into a semantic graph and prescriptive knowledge (workflow blocks) into a procedural graph. *Retrieval* uses abstraction-aware multi-hop traversal: concepts/intents serve as routing signals to activate relevant propositions/prescriptions. *Reasoning* compresses retrieved knowledge into task-adaptive guidance. <!-- VERIFY -->
- **Results**: PlugMem outperforms all task-agnostic baselines and exceeds task-specific designs on all three benchmarks while using 1-2 orders of magnitude fewer memory tokens. Achieves highest memory information density across all benchmarks. Ablations: removing retrieval causes worst degradation; structuring improves what retrieval can access; reasoning improves token efficiency. <!-- VERIFY -->

## Relevance to Our Work

- **[Agentic Memory](../term_dictionary/term_agentic_memory.md)**: PlugMem provides a principled framework for structuring agent memory — directly relevant to how abuse detection agents could maintain and retrieve investigation knowledge across cases
- **[HippoRAG](../term_dictionary/term_hipporag.md)**: Key baseline; HippoRAG uses hippocampal-inspired indexing but operates at entity level while PlugMem operates at knowledge level
- **[GraphRAG](../term_dictionary/term_graphrag.md)**: PlugMem can be viewed as a knowledge-centric form of GraphRAG where graph nodes are knowledge units (propositions/prescriptions) rather than entities or text chunks
- **[Experience Replay](../term_dictionary/term_experience_replay.md)**: PlugMem's episodic-to-knowledge transformation parallels experience replay's role in RL — raw experience is restructured for more efficient learning
- **[RAG](../term_dictionary/term_rag.md)**: PlugMem addresses fundamental limitations of vanilla RAG for agent memory: knowledge sparsity and context explosion from raw episodic retrieval
- **[Knowledge Graph](../term_dictionary/term_knowledge_graph.md)**: The memory graph uses knowledge (not entities) as the unit of organization — a novel departure from traditional KG approaches
- **[Context Engineering](../term_dictionary/term_context_engineering.md)**: The reasoning module performs task-adaptive context compression, reducing memory tokens by 1-2 orders of magnitude
- **[Knowledge Building Blocks](../term_dictionary/term_knowledge_building_blocks.md)**: Propositions and prescriptions as atomic knowledge units align with the building blocks concept for modular knowledge representation

## Questions

### Validation (Socratic — "Why?")
1. PlugMem claims that knowledge-level organization outperforms entity-level organization (GraphRAG, HippoRAG) — but is this distinction fundamental, or would any hierarchical summarization approach achieve similar gains regardless of whether nodes represent "knowledge" or "entities"?
   - **Tests**: Whether the cognitive science framing adds genuine architectural value beyond hierarchical abstraction (Devil's Advocate)
   - **If genuine**: Knowledge-centric design is a new paradigm for agent memory
   - **If not**: The contribution reduces to a well-engineered hierarchical summarization system

2. The paper assumes cognitive science memory taxonomy (episodic → semantic + procedural) transfers to LLM agents — what evidence would validate or break this analogy? Do LLMs process propositional vs. prescriptive knowledge differently at the representation level?
   - **Tests**: Whether the cognitive science warrant is load-bearing or decorative (WYSIATI)
   - **If validated**: Cognitive science provides principled design guidance for agent memory
   - **If broken**: The system works for engineering reasons unrelated to its theoretical motivation

3. Memory Information Density ($\rho = \text{PMI} / |m|$) assumes that $P_{\text{base}}(a^* \mid s)$ and $P_{\text{mem}}(a^* \mid s, m)$ can be reliably estimated — under what conditions does this metric become unreliable (e.g., binary outcomes, small sample sizes, model miscalibration)?
   - **Tests**: Robustness of the novel evaluation framework (Causal vs. Correlational)
   - **If robust**: The metric generalizes as a standard for memory evaluation
   - **If fragile**: Reported density advantages may be measurement artifacts

### Application (Taxonomic — "What If? / How?")
4. How would PlugMem's structuring module perform on abuse investigation memory — could raw abuse case interactions be standardized into $(o_t, s_t, a_t, r_t, g_t)$ tuples where $s_t$ = investigation state, $g_t$ = abuse detection subgoal, and $r_t$ = outcome quality?
   - **Tests**: Transferability to the buyer abuse domain (Adjacent Possible)

5. What if the structuring module used a weaker LLM (e.g., 7B parameters instead of 32B/72B) — would the knowledge extraction quality degrade gracefully or catastrophically? Where is the quality cliff?
   - **Tests**: Practical deployability under cost constraints (Scale Shift)

6. How would you operationally test whether PlugMem's procedural graph (prescriptions with return scores) produces better investigation workflows than a manually curated SOP library?
   - **Tests**: Whether automated knowledge extraction competes with expert-curated procedures (Operationalization)

### Synthesis (Lateral — "Who Else?")
7. How does PlugMem's proposition-prescription duality relate to [Knowledge Building Blocks](../term_dictionary/term_knowledge_building_blocks.md)'s modular knowledge types — are Fact Blocks and Workflow Blocks instances of the same abstraction?
   - **Tests**: Whether PlugMem's knowledge units fit into an existing vault framework

8. PlugMem's abstraction-aware retrieval uses concepts/intents as routing signals — how does this compare to [HippoRAG](../term_dictionary/term_hipporag.md)'s Personalized PageRank routing? Could the two approaches be combined (hippocampal indexing for entity discovery + knowledge-centric graphs for abstraction)?
   - **Tests**: Complementarity between two graph-based memory approaches (Liquid Network)

9. What partial ideas in the vault about [Experience Replay](../term_dictionary/term_experience_replay.md) could PlugMem's episodic-to-knowledge transformation help complete — specifically, could PlugMem's structuring module serve as a "knowledge replay buffer" that replays abstractions instead of raw transitions?
   - **Tests**: Cross-domain connection between RL memory and agent memory (Slow Hunch)

## Related Documentation

### Paper Notes
- [Introduction](paper_yang2026plugmem_intro.md)
- [Contribution](paper_yang2026plugmem_contrib.md)
- [Method](paper_yang2026plugmem_algo.md)
- [Experiment Design](paper_yang2026plugmem_exp_design.md)
- [Experiment Results](paper_yang2026plugmem_exp_result.md)

### Related Vault Notes
- [Agentic Memory](../term_dictionary/term_agentic_memory.md) — Principled framework for structuring agent memory
- [HippoRAG](../term_dictionary/term_hipporag.md) — Key baseline; hippocampal-inspired indexing at entity level
- [GraphRAG](../term_dictionary/term_graphrag.md) — Knowledge-centric alternative to entity-based GraphRAG
- [Experience Replay](../term_dictionary/term_experience_replay.md) — Episodic-to-knowledge transformation parallels experience replay
- [RAG](../term_dictionary/term_rag.md) — Addresses RAG limitations for agent memory
- [Knowledge Graph](../term_dictionary/term_knowledge_graph.md) — Novel knowledge-unit-centric graph organization
- [Context Engineering](../term_dictionary/term_context_engineering.md) — Task-adaptive context compression
- [Knowledge Building Blocks](../term_dictionary/term_knowledge_building_blocks.md) — Propositions/prescriptions as atomic knowledge units

### Related Literature
- Edge et al. (2025). "From Local to Global: A Graph RAG Approach" — [GraphRAG](../term_dictionary/term_graphrag.md)
- Gutiérrez et al. (2025). "From RAG to Memory" — non-parametric continual learning
- Wang et al. (2024b). "Agent Workflow Memory" — task-specific procedural memory baseline
- Ouyang et al. (2025). "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory"
