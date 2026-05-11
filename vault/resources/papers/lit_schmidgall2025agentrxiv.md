---
tags:
  - resource
  - literature_note
  - autonomous_research
  - multi_agent_collaboration
  - llm_agents
  - scientific_discovery
keywords:
  - AgentRxiv
  - collaborative autonomous research
  - preprint server
  - LLM agent laboratories
  - Simultaneous Divergence Averaging
  - SDA
  - multi-agent research
  - iterative discovery
  - MATH-500
  - reward hacking
  - agent hallucination
topics:
  - Multi-Agent Systems
  - Autonomous Research
  - Scientific Discovery
domain: "Agentic AI"
language: markdown
date of note: 2026-03-11
paper_title: "AgentRxiv: Towards Collaborative Autonomous Research"
authors:
  - Samuel Schmidgall
  - Michael Moor
year: 2025
source: "arXiv:2503.18102"
venue: "arXiv.org"
arXiv: "2503.18102"
doi: "10.48550/arXiv.2503.18102"
semantic_scholar_id: "594773309239331e6afcd2892136c5233383d3a5"
zotero_key: "QBU7E3HG"
paper_id: schmidgall2025agentrxiv
paper_notes:
  - paper_schmidgall2025agentrxiv_intro.md
  - paper_schmidgall2025agentrxiv_contrib.md
  - paper_schmidgall2025agentrxiv_algo.md
  - paper_schmidgall2025agentrxiv_exp_design.md
  - paper_schmidgall2025agentrxiv_exp_result.md
review_note: ""
status: active
building_block: hypothesis
---

# AgentRxiv: Towards Collaborative Autonomous Research

## Metadata

| Field | Value |
|-------|-------|
| **Paper** | AgentRxiv: Towards Collaborative Autonomous Research |
| **Authors** | Samuel Schmidgall, Michael Moor |
| **Year** | 2025 |
| **Venue** | arXiv.org |
| **arXiv** | [2503.18102](https://arxiv.org/abs/2503.18102) |
| **Semantic Scholar** | [594773309239...](https://www.semanticscholar.org/paper/594773309239331e6afcd2892136c5233383d3a5) |
| **Zotero** | QBU7E3HG |
| **Citations** | ~32 |

## Abstract

Progress in scientific discovery is rarely the result of a single "Eureka" moment, but is rather the product of hundreds of scientists incrementally working together toward a common goal. While existing agent workflows are capable of producing research autonomously, they do so in isolation, without the ability to continuously improve upon prior research results. To address these challenges, we introduce AgentRxiv — a framework that lets LLM agent laboratories upload and retrieve reports from a shared preprint server in order to collaborate, share insights, and iteratively build on each other's research. We task agent laboratories to develop new reasoning and prompting techniques and find that agents with access to their prior research achieve higher performance improvements compared to agents operating in isolation (11.4% relative improvement over baseline on MATH-500). We find that the best performing strategy generalizes to benchmarks in other domains (improving on average by 3.3%). Multiple agent laboratories sharing research through AgentRxiv are able to work together towards a common goal, progressing more rapidly than isolated laboratories, achieving higher overall accuracy (13.7% relative improvement over baseline on MATH-500).

## Table of Contents

| Section | Note | Key Content |
|---------|------|-------------|
| **Introduction** | [paper_schmidgall2025agentrxiv_intro](paper_schmidgall2025agentrxiv_intro.md) | Scientific progress as incremental collaboration; isolated agent research as the gap; motivation for shared knowledge infrastructure |
| **Contribution** | [paper_schmidgall2025agentrxiv_contrib](paper_schmidgall2025agentrxiv_contrib.md) | AgentRxiv framework for collaborative autonomous research; shared preprint server enabling iterative knowledge building across agent labs |
| **Method** | [paper_schmidgall2025agentrxiv_algo](paper_schmidgall2025agentrxiv_algo.md) | Agent Laboratory architecture (PhD, Postdoc, ML Engineer agents); mle-solver for code generation; paper-solver for report writing; SentenceTransformer retrieval from preprint server |
| **Experiment Design** | [paper_schmidgall2025agentrxiv_exp_design](paper_schmidgall2025agentrxiv_exp_design.md) | MATH-500 primary benchmark; sequential single-lab (40 papers), parallel multi-lab (3x40), ablation on prior work access; generalization across 4 benchmarks and 5 models |
| **Experiment Results** | [paper_schmidgall2025agentrxiv_exp_result](paper_schmidgall2025agentrxiv_exp_result.md) | +11.4% sequential, +13.7% parallel on MATH-500; SDA technique discovery; generalization to GPQA/MMLU-Pro/MedQA; failure modes including hallucination and reward hacking |
| **Review** | [review_schmidgall2025agentrxiv](review_schmidgall2025agentrxiv.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 7 questions (3 review lenses applied) |

## Summary

- **Background**: Scientific discovery is an incremental, collaborative process — yet existing autonomous research agents (e.g., Agent Laboratory) operate in isolation, unable to build upon prior findings or share insights with other agent systems. This mirrors a fundamental limitation: current AI research workflows lack the shared knowledge infrastructure that human scientific communities rely on (preprint servers, conferences, peer review). <!-- VERIFY: problem statement -->
- **Contribution**: AgentRxiv introduces a shared preprint server framework where multiple LLM agent laboratories can upload, retrieve, and build upon each other's research reports. The key insight is that enabling agents to access prior work — both their own and from other labs — creates a positive feedback loop of iterative improvement, analogous to how human scientists build on published literature. <!-- VERIFY: contributions -->
- **Method**: Built on the Agent Laboratory framework, AgentRxiv uses a multi-agent pipeline: PhD agents plan research, Postdoc agents evaluate plans, and ML Engineer agents implement experiments via the mle-solver module. A centralized preprint server stores generated papers, which are retrieved via SentenceTransformer embeddings for similarity-based lookup. The paper-solver module produces LaTeX reports, creating a complete research cycle from literature review through experimentation to publication. <!-- VERIFY: method details -->
- **Results**: Sequential single-lab experiments (40 papers) achieved 78.2% accuracy on MATH-500, a +11.4% relative improvement over the 70.2% baseline (gpt-4o mini zero-shot). Parallel execution with 3 concurrent labs achieved 79.8% (+13.7%). The discovered technique — Simultaneous Divergence Averaging (SDA) — generalized across benchmarks (GPQA +6.8%, MMLU-Pro +12.2%, MedQA +8.9%) and across models (avg +3.3%). However, significant failure modes were documented including agent hallucination, reward hacking, and fabricated experimental results. <!-- VERIFY: exact numbers -->

## Relevance to Our Work

- **[Self-Evolving Agent](../term_dictionary/term_self_evolving_agent.md)**: AgentRxiv demonstrates agents that iteratively improve through access to their own prior research — a form of self-evolution through accumulated knowledge rather than weight updates
- **[AgentSpace](../term_dictionary/term_agentspace.md)**: Related multi-agent coordination paradigm; AgentRxiv addresses the collaboration aspect through a shared preprint server rather than direct agent communication
- **[Chain-of-Thought](../term_dictionary/term_chain_of_thought.md)**: SDA technique builds on chain-of-thought by employing multiple reasoning paths and aggregating confidence signals — extending self-consistency prompting
- **[Hallucination](../term_dictionary/term_hallucination.md)**: Paper documents significant hallucination failure modes in autonomous research — agents fabricate experimental results and print false runtime outputs
- **[Agentic Memory](../term_dictionary/term_agentic_memory.md)**: The preprint server functions as a form of persistent agentic memory — shared across labs, enabling cumulative knowledge building over time

## Related Documentation

### Paper Notes
- [Introduction](paper_schmidgall2025agentrxiv_intro.md)
- [Contribution](paper_schmidgall2025agentrxiv_contrib.md)
- [Method](paper_schmidgall2025agentrxiv_algo.md)
- [Experiment Design](paper_schmidgall2025agentrxiv_exp_design.md)
- [Experiment Results](paper_schmidgall2025agentrxiv_exp_result.md)

### Related Vault Notes
- [Self-Evolving Agent](../term_dictionary/term_self_evolving_agent.md) — AgentRxiv enables self-improving agents through iterative research accumulation
- [AgentSpace](../term_dictionary/term_agentspace.md) — Related multi-agent coordination paradigm
- [Chain-of-Thought](../term_dictionary/term_chain_of_thought.md) — SDA extends chain-of-thought with divergent path aggregation
- [Hallucination](../term_dictionary/term_hallucination.md) — Key failure mode documented in autonomous research agents
- [Agentic Memory](../term_dictionary/term_agentic_memory.md) — Preprint server as shared persistent memory
- [Prompt Optimization](../term_dictionary/term_prompt_optimization.md) — AgentRxiv discovers new prompting strategies through automated experimentation

### Related Literature
- Zhang et al. (2025). "Agentic Context Engineering" — [lit_zhang2025agentic](lit_zhang2025agentic.md) — Related self-improving agent paradigm; ACE evolves playbooks while AgentRxiv evolves shared research papers
- You et al. (2026). "Agent Survey" — [lit_you2026agent](lit_you2026agent.md) — Comprehensive survey of LLM agent architectures including multi-agent collaboration
