---
tags:
  - resource
  - literature_note
  - agentic_ai
  - survey
  - dual_paradigm
  - symbolic_ai
  - neural_ai
  - multi_agent_systems
  - ai_governance
keywords:
  - agentic AI
  - dual-paradigm framework
  - symbolic AI
  - neural AI
  - conceptual retrofitting
  - BDI
  - POMDP
  - MDP
  - LLM orchestration
  - multi-agent systems
  - neuro-symbolic
  - PRISMA
  - AI governance
  - hybrid architectures
  - prompt chaining
  - LangChain
  - AutoGen
  - CrewAI
topics:
  - Agentic AI Architectures
  - AI Paradigm Classification
  - Multi-Agent Coordination
  - AI Ethics and Governance
domain: "Agentic AI"
language: markdown
date of note: 2026-03-12
paper_title: "Agentic AI: A Comprehensive Survey of Architectures, Applications, and Future Directions"
authors:
  - Mohamad Abou Ali
  - Fadi Dornaika
year: 2025
source: "arXiv:2510.25445"
venue: "Artificial Intelligence Review"
DOI: "10.1007/s10462-025-11422-4"
arXiv: "2510.25445"
semantic_scholar_id: ""
zotero_key: "3IEDPUUA"
paper_id: abouali2025agentic
paper_notes:
  - paper_abouali2025agentic_intro.md
  - paper_abouali2025agentic_taxonomy.md
  - paper_abouali2025agentic_survey_symbolic.md
  - paper_abouali2025agentic_survey_neural.md
  - paper_abouali2025agentic_survey_applications.md
  - paper_abouali2025agentic_survey_governance.md
  - paper_abouali2025agentic_survey_hybrid.md
  - paper_abouali2025agentic_benchmark.md
review_note: ""
status: active
building_block: hypothesis
---

# Agentic AI: A Comprehensive Survey of Architectures, Applications, and Future Directions

| Field | Value |
|-------|-------|
| **Paper** | Agentic AI: A Comprehensive Survey of Architectures, Applications, and Future Directions |
| **Authors** | Mohamad Abou Ali, Fadi Dornaika |
| **Year** | 2025 |
| **Venue** | Artificial Intelligence Review (Springer) |
| **DOI** | [10.1007/s10462-025-11422-4](https://doi.org/10.1007/s10462-025-11422-4) |
| **arXiv** | [2510.25445](https://arxiv.org/abs/2510.25445) |
| **Citations** | 18 |
| **Type** | Survey (90 studies, PRISMA-based) |

## Abstract

Agentic AI represents a transformative shift in artificial intelligence, but its rapid advancement has led to a fragmented understanding, often conflating modern neural systems with outdated symbolic models—a practice known as conceptual retrofitting. This survey cuts through this confusion by introducing a novel dual-paradigm framework that categorizes agentic systems into two distinct lineages: the Symbolic/Classical (relying on algorithmic planning and persistent state) and the Neural/Generative (leveraging stochastic generation and prompt-driven orchestration). Through a systematic PRISMA-based review of 90 studies (2018–2025), we provide a comprehensive analysis structured around this framework across three dimensions: (1) the theoretical foundations and architectural principles defining each paradigm; (2) domain-specific implementations in healthcare, finance, and robotics, demonstrating how application constraints dictate paradigm selection; and (3) paradigm-specific ethical and governance challenges, revealing divergent risks and mitigation strategies.

## Table of Contents

| # | Section Note | Key Content |
|---|-------------|-------------|
| 1 | [Introduction](paper_abouali2025agentic_intro.md) | AI Agent vs Agentic AI distinction, 5 AI eras, conceptual retrofitting problem, 4 contributions |
| 2 | [Taxonomy](paper_abouali2025agentic_taxonomy.md) | Dual-paradigm framework: Symbolic/Classical vs Neural/Generative along 2 dimensions (paradigm + agency degree) |
| 3 | [Symbolic Paradigm](paper_abouali2025agentic_survey_symbolic.md) | MDPs, POMDPs, BDI/SOAR cognitive architectures, algorithmic decision-making |
| 4 | [Neural Paradigm](paper_abouali2025agentic_survey_neural.md) | DRL, LLM substrate, orchestration frameworks (LangChain, AutoGen, CrewAI), MAS coordination |
| 5 | [Domain Applications](paper_abouali2025agentic_survey_applications.md) | Healthcare (symbolic), Finance (neural), Robotics (hybrid), Education, Legal |
| 6 | [Ethics & Governance](paper_abouali2025agentic_survey_governance.md) | Paradigm-specific ethical challenges, 3 agency levels, policy framework |
| 7 | [Hybrid & Future](paper_abouali2025agentic_survey_hybrid.md) | Neuro-symbolic integration, research gaps, strategic roadmap |
| 8 | [Benchmark](paper_abouali2025agentic_benchmark.md) | Cross-paradigm comparison, evaluation frameworks, 90-study analysis |
| **Review** | [review_abouali2025agentic](review_abouali2025agentic.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 8 questions (6 review lenses applied) |

## Summary

- **Introduction**: Distinguishes AI Agent (single autonomous system) from Agentic AI (broader field, often MAS). Identifies conceptual retrofitting — misapplying BDI/PPAR frameworks to LLM-based agents — as a critical field problem. Charts 5 AI eras: Symbolic (1950s-80s) → ML (1980s-2010s) → Deep Learning (2010s+) → Generative AI (2014+) → Agentic AI (2022+). <!-- VERIFY -->
- **Taxonomy**: Dual-paradigm framework classifying agentic systems along 2 axes: Architectural Paradigm (Symbolic vs Neural) × Degree of Agency (Single-Agent vs Multi-Agent). Symbolic lineage: algorithmic planning, persistent state. Neural lineage: stochastic generation, prompt-driven orchestration. <!-- VERIFY -->
- **Symbolic Paradigm**: MDPs for full-state environments, POMDPs for partial observability with belief states, BDI/SOAR cognitive architectures as pinnacle of symbolic agency. Strengths: verifiability, determinism. Limitations: brittleness, scalability. <!-- VERIFY -->
- **Neural Paradigm**: DRL as bridge (neural networks learning policies), LLM substrate as paradigm shift. Modern orchestration frameworks replace symbolic planning: LangChain (prompt chaining), AutoGen (multi-agent conversation), CrewAI (role-based workflow), Semantic Kernel (plugin composition), LlamaIndex (RAG). <!-- VERIFY -->
- **Applications**: Paradigm choice is domain-driven: symbolic for safety-critical (healthcare), neural for data-rich adaptive (finance), hybrid for embodied (robotics), neural-conversational for education, neural-RAG for legal. <!-- VERIFY -->
- **Ethics**: Paradigm-specific challenges across 6 dimensions (accountability, transparency, bias, safety, autonomy, security). Three agency levels proposed: Assistive, Shared, Delegated — each with different governance needs. <!-- VERIFY -->
- **Future**: Neuro-symbolic integration as keystone. 8 research gap areas identified. Future lies in strategic synthesis of both paradigms, not dominance of one. <!-- VERIFY -->

## Relevance to Our Work

This survey provides a unifying framework for classifying the Abuse Slipbox's agentic AI capabilities:
- The **dual-paradigm framework** maps to the slipbox's own architecture: symbolic (SQLite database, graph queries, PageRank) + neural (LLM-based skill orchestration)
- **Conceptual retrofitting** is a useful lens for evaluating whether our agent architecture genuinely implements agentic patterns or merely mimics them
- The **evaluation framework** for agency (beyond accuracy) informs how to assess slipbox agent quality
- **Multi-agent coordination patterns** (conversation-based, role-based workflow) map to the slipbox's skill-based orchestration model

### Vault Connections

- [Multi-Agent Collaboration](../term_dictionary/term_multi_agent_collaboration.md) — directly analyzed as MAS in both paradigms
- [Self-Evolving Agent](../term_dictionary/term_self_evolving_agent.md) — lifelong learning frameworks discussed as emerging trend
- [Transformer](../term_dictionary/term_transformer.md) — identified as pivotal enabling technology for the neural paradigm
- [MCP](../term_dictionary/term_mcp.md) — related to tool use and orchestration patterns discussed
- [Rise of Agentic AI (Bandi 2025)](lit_bandi2025rise.md) — companion survey on same topic with different framework

## Questions

*(To be generated via `/slipbox-generate-questions`)*

## Related Documentation

- [Rise of Agentic AI (Bandi et al., 2025)](lit_bandi2025rise.md) — complementary survey reviewing 143 studies with focus on definitions, frameworks, and evaluation metrics
- [Agent Survey (You et al., 2026)](lit_you2026agent.md) — another agentic AI survey for comparison
