---
tags:
  - resource
  - literature_note
  - agentic_ai
  - survey
  - multi_agent_systems
  - llm_agents
  - autonomous_systems
keywords:
  - agentic AI
  - AI agents
  - multi-agent systems
  - LLM-based agents
  - autonomous AI
  - planning
  - memory
  - reflection
  - ReAct
  - BDI
  - evaluation metrics
  - LangChain
  - AutoGPT
topics:
  - agentic AI systems
  - AI agent architectures
  - multi-agent coordination
  - LLM agent frameworks
domain: Agentic AI
paper_title: "The Rise of Agentic AI: A Review of Definitions, Frameworks, Architectures, Applications, Evaluation Metrics, and Challenges"
authors: "Ajay Bandi, Bhavani Kongari, Roshini Naguru, Sahitya Pasnoor, Sri Vidya Vilipala"
year: 2025
source: MDPI
venue: "Future Internet"
DOI: "10.3390/fi17090404"
arXiv: ""
semantic_scholar_id: "d9f0d979178e8e42c88e831ba4a1e4eca17f3e83"
zotero_key: "T8WIBAZF"
paper_notes:
  - paper_bandi2025rise_intro.md
  - paper_bandi2025rise_taxonomy.md
  - paper_bandi2025rise_survey_frameworks.md
  - paper_bandi2025rise_survey_architectures.md
  - paper_bandi2025rise_survey_applications.md
  - paper_bandi2025rise_survey_io_mechanisms.md
  - paper_bandi2025rise_survey_evaluation.md
  - paper_bandi2025rise_benchmark.md
review_note: ""
status: active
language: markdown
building_block: hypothesis
date of note: 2026-03-12
---

# The Rise of Agentic AI: A Review of Definitions, Frameworks, Architectures, Applications, Evaluation Metrics, and Challenges

| Field | Value |
|-------|-------|
| **Paper** | The Rise of Agentic AI |
| **Authors** | Ajay Bandi, Bhavani Kongari, Roshini Naguru, Sahitya Pasnoor, Sri Vidya Vilipala |
| **Year** | 2025 |
| **Venue** | Future Internet (MDPI) |
| **DOI** | [10.3390/fi17090404](https://doi.org/10.3390/fi17090404) |
| **Citations** | 45 |
| **Type** | Survey (143 primary studies reviewed) |

## Abstract

Agentic AI systems are a recently emerged and important approach that goes beyond traditional AI, generative AI, and autonomous systems by focusing on autonomy, adaptability, and goal-driven reasoning. This study provides a clear review of agentic AI systems by bringing together their definitions, frameworks, and architectures, and by comparing them with related areas like generative AI, autonomic computing, and multi-agent systems. To do this, we reviewed 143 primary studies on current LLM-based and non-LLM-driven agentic systems and examined how they support planning, memory, reflection, and goal pursuit. Furthermore, we classified architectural models, input–output mechanisms, and applications based on their task domains where agentic AI is applied, supported using tabular summaries that highlight real-world case studies. Evaluation metrics were classified as qualitative and quantitative measures, along with available testing methods of agentic AI systems to check the system's performance and reliability. This study also highlights the main challenges and limitations of agentic AI, covering technical, architectural, coordination, ethical, and security issues.

## Table of Contents

| # | Section Note | Key Content |
|---|-------------|-------------|
| 1 | [Introduction](paper_bandi2025rise_intro.md) | Research purpose, 7 research questions, methodology (143 studies), contributions |
| 2 | [Taxonomy](paper_bandi2025rise_taxonomy.md) | Agentic AI definition, distinction from GenAI/MAS/autonomic computing, Venn diagram taxonomy |
| 3 | [Frameworks & Tools](paper_bandi2025rise_survey_frameworks.md) | LLM-based (LangChain, AutoGPT, BabyAGI, AutoGen, etc.) + non-LLM systems |
| 4 | [Architectures & Components](paper_bandi2025rise_survey_architectures.md) | ReAct, Supervisor/Hierarchical, Hybrid, BDI, Neuro-Symbolic; core components |
| 5 | [Applications](paper_bandi2025rise_survey_applications.md) | 10+ domains: healthcare, software, finance, manufacturing, education, scientific discovery |
| 6 | [Input-Output Mechanisms](paper_bandi2025rise_survey_io_mechanisms.md) | Text→Actions, Audio→Text, Real-time→Actions, Datasets→Text, multimodal |
| 7 | [Evaluation & Testing](paper_bandi2025rise_survey_evaluation.md) | Testing methods (12+), qualitative metrics (6), quantitative metrics (10+) |
| 8 | [Benchmark](paper_bandi2025rise_benchmark.md) | Cross-survey comparison, challenges taxonomy, future directions |
| **Review** | [review_bandi2025rise](review_bandi2025rise.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 7 questions (3 review lenses applied) |

## Summary

- **Introduction**: Comprehensive survey of 143 primary studies addressing 7 research questions about agentic AI — definitions, frameworks, architectures, applications, I/O mechanisms, evaluation, and challenges. <!-- VERIFY -->
- **Taxonomy**: Agentic AI is distinguished from generative AI (content generation), autonomic computing (self-management), and multi-agent systems (coordination) through a Venn diagram showing overlaps. Core characteristics: autonomy, adaptability, goal-driven reasoning, planning, memory, reflection. <!-- VERIFY -->
- **Frameworks**: LLM-based frameworks (LangChain, AutoGPT, BabyAGI, AutoGen, OpenAgents, CAMEL, CrewAI, SuperAGI) compared across planning, memory, reflection, goal pursuit, and tool use capabilities. Non-LLM systems include rule-based MAS, RL agents, and hybrid approaches. <!-- VERIFY -->
- **Architectures**: Five architectural models identified — ReAct single-agent loop, Supervisor/Hierarchical, Hybrid reactive-deliberative, BDI, and Layered Neuro-Symbolic — each with distinct trade-offs in scalability, transparency, and robustness. <!-- VERIFY -->
- **Applications**: Agentic AI applied across 10+ domains including healthcare, transportation, software engineering, finance, manufacturing, education, and scientific discovery. <!-- VERIFY -->
- **Evaluation**: Testing methods include automated test generation, formal verification, runtime monitoring, benchmark testing, stress testing, A/B testing, and simulations. Metrics split into qualitative (explainability, transparency, fairness) and quantitative (accuracy, precision, recall, F1, GED). <!-- VERIFY -->

## Relevance to Our Work

This survey provides a comprehensive taxonomy of agentic AI that directly informs the Abuse Slipbox's agentic architecture:
- The **ReAct loop** and **Supervisor/Hierarchical** patterns map to the slipbox agent's search-then-synthesize workflow
- **Memory systems** (STM/LTM/episodic) parallel the vault's SQLite database + PageRank graph
- **Planning and reflection** components inform the Slipbox Thinking Protocol research direction
- **Evaluation metrics** (explainability, accuracy, GED) provide frameworks for assessing agent quality

### Vault Connections
- **[Term: AI Agent](../term_dictionary/term_agentic_ai.md)** — Core concept defined in this survey
- **[Term: RAG](../term_dictionary/term_rag.md)** — Retrieval-augmented generation used in many surveyed frameworks
- **[Term: Multi-Agent Collaboration](../term_dictionary/term_multi_agent_collaboration.md)** — Key coordination pattern
- **[Term: Knowledge Graph](../term_dictionary/term_knowledge_graph.md)** — Used in agentic memory systems
- **[Term: MCP](../term_dictionary/term_mcp.md)** — Model Context Protocol for agent-tool integration
- **[Paper: A-MEM](lit_xu2025amem.md)** — Zettelkasten-inspired agentic memory (surveyed)
- **[Paper: ACE](lit_zhang2025agentic.md)** — Agentic Context Engineering (related)
- **[Paper: Self-Evolving Agents Survey](lit_gao2025survey.md)** — Complementary survey on self-improving agents
- **[Paper: Agent-as-a-Judge](lit_you2026agent.md)** — Agentic evaluation framework
- **[Project: Abuse Slipbox](../../projects/project_abuse_slipbox.md)** — This vault's agentic architecture

## Questions

1. How do the 5 architectural models (ReAct, Supervisor, Hybrid, BDI, Neuro-Symbolic) map to the slipbox agent's current and planned capabilities?
2. Which evaluation metrics from this survey are most applicable to measuring the slipbox agent's answer quality?
3. How does the survey's memory taxonomy (STM/LTM/episodic) compare to the vault's database + PageRank approach?

## Related Documentation

- **[Paper: KARL](lit_chang2026karl.md)** — Knowledge agent with grounded reasoning
- **[Paper: AgentRxiv](lit_schmidgall2025agentrxiv.md)** — Collaborative autonomous research
- **[Term: RL](../term_dictionary/term_rl.md)** — Reinforcement learning in agent training
- **[Term: RLHF](../term_dictionary/term_rlhf.md)** — RL from human feedback

---

**Last Updated**: March 12, 2026
**Status**: Active
