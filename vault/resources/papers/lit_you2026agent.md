---
tags:
  - resource
  - literature_note
  - survey
  - llm_evaluation
  - agentic_ai
  - agent_as_a_judge
keywords:
  - Agent-as-a-Judge
  - LLM-as-a-Judge
  - agentic evaluation
  - multi-agent collaboration
  - tool-augmented verification
  - reward modeling
  - self-evolving agents
topics:
  - AI Evaluation
  - LLM Agents
  - Agentic AI
domain: "Agentic AI"
language: markdown
date of note: 2026-03-10
paper_title: "Agent-as-a-Judge"
authors: "Runyang You, Hongru Cai, Caiqi Zhang, Qiancheng Xu, Meng Liu, Tiezheng Yu, Yongqing Li, Wenjie Li"
year: 2026
source: "arXiv"
venue: "arXiv preprint"
DOI: "10.48550/arXiv.2601.05111"
arXiv: "2601.05111"
semantic_scholar_id: "b56501d945e165ae9e364473708b2f897f4cb570"
zotero_key: "S9EWKVB7"
paper_id: you2026agent
paper_notes:
  - paper_you2026agent_intro.md
  - paper_you2026agent_taxonomy.md
  - paper_you2026agent_survey_collaboration.md
  - paper_you2026agent_survey_planning.md
  - paper_you2026agent_survey_tools.md
  - paper_you2026agent_survey_memory.md
  - paper_you2026agent_survey_optimization.md
  - paper_you2026agent_benchmark.md
review_note: null
status: active
building_block: hypothesis
---

# Agent-as-a-Judge

## Metadata

| Field | Value |
|-------|-------|
| **Paper** | Agent-as-a-Judge |
| **Authors** | Runyang You, Hongru Cai, Caiqi Zhang, Qiancheng Xu, Meng Liu, Tiezheng Yu, Yongqing Li, Wenjie Li |
| **Year** | 2026 |
| **Venue** | arXiv preprint |
| **arXiv** | [2601.05111](https://arxiv.org/abs/2601.05111) |
| **Semantic Scholar** | [b56501d945...](https://www.semanticscholar.org/paper/b56501d945e165ae9e364473708b2f897f4cb570) |
| **Zotero** | S9EWKVB7 |
| **Citations** | 5 |

## Abstract

LLM-as-a-Judge has revolutionized AI evaluation by leveraging large language models for scalable assessments. However, as evaluands become increasingly complex, specialized, and multi-step, the reliability of LLM-as-a-Judge has become constrained by inherent biases, shallow single-pass reasoning, and the inability to verify assessments against real-world observations. This has catalyzed the transition to Agent-as-a-Judge, where agentic judges employ planning, tool-augmented verification, multi-agent collaboration, and persistent memory to enable more robust, verifiable, and nuanced evaluations. Despite the rapid proliferation of agentic evaluation systems, the field lacks a unified framework to navigate this shifting landscape. To bridge this gap, we present the first comprehensive survey tracing this evolution. Specifically, we identify key dimensions that characterize this paradigm shift and establish a developmental taxonomy. We organize core methodologies and survey applications across general and professional domains. Furthermore, we analyze frontier challenges and identify promising research directions, ultimately providing a clear roadmap for the next generation of agentic evaluation.

## Table of Contents

| Paper Section | Note | Key Content |
|---------------|------|-------------|
| §1 Introduction | [paper_you2026agent_intro](paper_you2026agent_intro.md) | LLM-as-a-Judge limitations (biases, passive observation, cognitive overload); motivation for agentic evaluation |
| §2-§3 Taxonomy & Developmental Stages | [paper_you2026agent_taxonomy](paper_you2026agent_taxonomy.md) | 3 stages (Procedural, Reactive, Self-Evolving); 3 dimensions (Robustness, Verification, Granularity) |
| §4.1 Multi-Agent Collaboration | [paper_you2026agent_survey_collaboration](paper_you2026agent_survey_collaboration.md) | Monolithic to decentralized judging; debate, jury, court-of-law paradigms |
| §4.2 Planning | [paper_you2026agent_survey_planning](paper_you2026agent_survey_planning.md) | Structured evaluation workflows; decomposition and sequential reasoning |
| §4.3 Tool Integration | [paper_you2026agent_survey_tools](paper_you2026agent_survey_tools.md) | Tool-augmented verification; code execution, web search, formal methods |
| §4.4 Memory & Personalization | [paper_you2026agent_survey_memory](paper_you2026agent_survey_memory.md) | Persistent memory for consistent evaluation; personalized judging criteria |
| §4.5 Optimization Paradigms | [paper_you2026agent_survey_optimization](paper_you2026agent_survey_optimization.md) | Reward modeling; self-evolving evaluation agents; optimization loops |
| §5 Applications, §6 Challenges, §7 Future | [paper_you2026agent_benchmark](paper_you2026agent_benchmark.md) | General domains (Math/Code, Fact-Checking, Conversation, Multimodal); Professional domains (Medicine, Law, Finance, Education); challenges and future directions |
| **Review** | [review_you2026agent](review_you2026agent.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 7 questions (5 review lenses applied) |

## Summary

<!-- VERIFY -->
- **Introduction**: LLM-as-a-Judge enabled scalable evaluation but faces three fundamental limitations as evaluands grow more complex: parametric biases (position, verbosity, self-enhancement), passive single-pass observation without environmental interaction, and cognitive overload from processing long multi-step outputs. These limitations motivate the transition to Agent-as-a-Judge.
- **Taxonomy**: The survey identifies three developmental stages -- Procedural (fixed evaluation workflows), Reactive (environment-responsive judging), and Self-Evolving (agents that improve their evaluation capabilities over time) -- along three key dimensions: Robustness (monolithic to decentralized), Verification (intuition-based to execution-based), and Granularity (global scoring to fine-grained feedback).
- **Methodologies**: Five core methodology categories organize the field: (1) Multi-Agent Collaboration for robustness through diverse perspectives, (2) Planning for structured evaluation decomposition, (3) Tool Integration for grounded verification via code execution and search, (4) Memory & Personalization for consistent and context-aware judging, and (5) Optimization Paradigms for reward-driven and self-evolving evaluation improvement.
- **Applications & Challenges**: Applications span general domains (mathematical reasoning, code generation, fact-checking, conversational quality, multimodal/vision) and professional domains (medicine, law, finance, education). Key challenges include computational cost, latency, safety alignment, and privacy in agentic evaluation pipelines.

## Relevance to Our Work

- **[GreenTEA](../term_dictionary/term_greentea.md)**: GreenTEA's agentic investigation automation directly benefits from Agent-as-a-Judge principles -- the survey's tool-augmented verification and multi-agent collaboration patterns can inform how GreenTEA evaluates investigation quality and decision correctness
- **[BAP](../term_dictionary/term_bap.md)**: BAP automation quality assessment maps to the survey's granularity dimension; moving from global pass/fail scoring to fine-grained evaluation of individual automation steps aligns with the Procedural-to-Self-Evolving trajectory
- **[Prompt Optimization](../term_dictionary/term_prompt_optimization.md)**: The optimization paradigms methodology category (reward modeling, self-evolving agents) directly informs prompt optimization strategies for evaluation prompts used in BRP's agentic systems
- **[LLM-as-a-Judge](../term_dictionary/term_llm_as_a_judge.md)**: This survey provides the roadmap for evolving BRP's current LLM-as-a-Judge evaluation patterns (e.g., AtoZ-Eval) into full Agent-as-a-Judge systems with tool verification and multi-agent robustness
- **[Red Teaming](../term_dictionary/term_red_teaming.md)**: The survey's multi-agent collaboration patterns (debate, court-of-law) relate to adversarial evaluation and red teaming of abuse detection models

## Questions

- How would the Procedural-to-Reactive transition apply to GreenTEA's evaluation of investigation outcomes -- can the judge agent interact with the investigation environment?
- Could BRP's abuse decision auditing benefit from the court-of-law multi-agent collaboration pattern (prosecution/defense/judge)?
- What is the computational cost overhead of Agent-as-a-Judge vs LLM-as-a-Judge for high-volume abuse evaluation (millions of cases)?
- Can the self-evolving evaluation paradigm be applied to continuously improve BRP's model evaluation criteria as abuse patterns shift?
- How do the privacy challenges identified in §6 affect deployment of agentic judges that interact with sensitive customer data?

## Related Documentation

### Paper Notes
- [paper_you2026agent_intro](paper_you2026agent_intro.md)
- [paper_you2026agent_taxonomy](paper_you2026agent_taxonomy.md)
- [paper_you2026agent_survey_collaboration](paper_you2026agent_survey_collaboration.md)
- [paper_you2026agent_survey_planning](paper_you2026agent_survey_planning.md)
- [paper_you2026agent_survey_tools](paper_you2026agent_survey_tools.md)
- [paper_you2026agent_survey_memory](paper_you2026agent_survey_memory.md)
- [paper_you2026agent_survey_optimization](paper_you2026agent_survey_optimization.md)
- [paper_you2026agent_benchmark](paper_you2026agent_benchmark.md)

### Related Vault Notes
- [LLM-as-a-Judge](../term_dictionary/term_llm_as_a_judge.md) — Foundational paradigm that Agent-as-a-Judge extends; this survey traces the full evolution
- [Self-Evolving Agent](../term_dictionary/term_self_evolving_agent.md) — The third developmental stage (Self-Evolving) represents agents that improve their evaluation capabilities autonomously
- [Reward Model](../term_dictionary/term_reward_model.md) — Optimization paradigms methodology category includes reward-based self-improvement of evaluation agents
- [RLHF](../term_dictionary/term_rlhf.md) — Human feedback alignment; Agent-as-a-Judge can serve as a scalable proxy for human evaluation in RLHF pipelines
- [RLAIF](../term_dictionary/term_rlaif.md) — AI feedback alignment; agentic judges provide richer, more verifiable feedback signals than monolithic LLM judges
- [Hallucination](../term_dictionary/term_hallucination.md) — Tool-augmented verification directly addresses hallucination in evaluation outputs through grounded checking
- [Red Teaming](../term_dictionary/term_red_teaming.md) — Multi-agent adversarial patterns (debate, court-of-law) connect to red teaming methodologies for robust evaluation
- [Prompt Optimization](../term_dictionary/term_prompt_optimization.md) — Self-evolving evaluation agents optimize their own evaluation prompts and criteria over time
- [Agentic Memory](../term_dictionary/term_agentic_memory.md) — Memory & Personalization methodology enables persistent, consistent evaluation across sessions
- [MT-Bench](../term_dictionary/term_mt_bench.md) — Benchmark from LLM-as-a-Judge era that Agent-as-a-Judge aims to surpass in evaluation depth
- [Chatbot Arena](../term_dictionary/term_chatbot_arena.md) — Crowdsourced evaluation platform; Agent-as-a-Judge offers an alternative scalable approach
- [Position Bias](../term_dictionary/term_position_bias.md) — Key parametric bias in LLM-as-a-Judge that multi-agent collaboration patterns mitigate
- [GreenTEA](../term_dictionary/term_greentea.md) — BRP's agentic AI for investigation automation; Agent-as-a-Judge patterns inform quality evaluation of GreenTEA outputs

### Related Literature
- Zheng et al. (2023). "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" — [lit_zheng2023judging](lit_zheng2023judging.md) — Foundational LLM-as-a-Judge paper; establishes the paradigm that this survey traces forward
- Gao et al. (2025). "A Survey of Self-Evolving Agents" — [lit_gao2025survey](lit_gao2025survey.md) — Complementary survey on self-evolving agents; the self-evolving developmental stage connects directly
- Zhang et al. (2025). "Agentic Context Engineering (ACE)" — [lit_zhang2025agentic](lit_zhang2025agentic.md) — Context evolution framework relevant to the Memory & Personalization methodology
- Xu et al. (2025). "A-MEM: Agentic Memory for LLM Agents" — [lit_xu2025amem](lit_xu2025amem.md) — Agentic memory architecture applicable to persistent evaluation context
- Yuksekgonul et al. (2024). "TextGrad: Automatic Differentiation via Text" — [lit_yuksekgonul2024textgrad](lit_yuksekgonul2024textgrad.md) — Textual gradient optimization applicable to the Optimization Paradigms methodology
