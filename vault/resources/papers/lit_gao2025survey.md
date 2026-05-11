---
tags:
  - resource
  - literature_note
  - survey
  - self_evolving_agents
  - agentic_ai
  - continual_learning
  - reinforcement_learning
keywords:
  - self-evolving agents
  - LLM agents
  - continual learning
  - self-improvement
  - multi-agent systems
  - test-time adaptation
  - reward-based evolution
  - tool creation
  - memory evolution
  - prompt optimization
topics:
  - agentic AI
  - self-evolving systems
  - continual learning
  - reinforcement learning
  - multi-agent collaboration
domain: "Agentic AI"
paper_title: "A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve on the Path to Artificial Super Intelligence"
authors: Huan-ang Gao, Jiayi Geng, Wenyue Hua, Mengkang Hu, Xinzhe Juan, Hongzhang Liu, Shilong Liu, Jiahao Qiu, Xuan Qi, Qihan Ren, Yiran Wu, Hongru Wang, Han Xiao, Yuhang Zhou, Shaokun Zhang, Jiayi Zhang, et al. (27 authors)
year: 2025
source: arXiv
venue: preprint
DOI: null
arXiv: "2507.21046"
semantic_scholar_id: "74deef6100e5d9baf2eaa86e20618fa34d02c678"
zotero_key: WE5CWX69
paper_id: gao2025survey
paper_notes:
  - paper_gao2025survey_intro.md
  - paper_gao2025survey_taxonomy.md
  - paper_gao2025survey_survey_what.md
  - paper_gao2025survey_survey_when.md
  - paper_gao2025survey_survey_how.md
  - paper_gao2025survey_survey_where.md
  - paper_gao2025survey_benchmark.md
review_note: review_gao2025survey.md
status: active
language: markdown
building_block: hypothesis
date of note: 2026-03-10
---

# A Survey of Self-Evolving Agents

| Field | Value |
|-------|-------|
| **Paper** | A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve |
| **Authors** | Gao, Geng, Hua, Hu, Juan, Liu, Liu, Qiu, Qi, Ren, Wu, Wang, Xiao, Zhou, Zhang, Zhang et al. (27 total) |
| **Year** | 2025 |
| **Venue** | arXiv preprint |
| **arXiv** | [2507.21046](https://arxiv.org/abs/2507.21046) |
| **Citations** | 62 (4 influential) |
| **GitHub** | [CharlesQ9/Self-Evolving-Agents](https://github.com/CharlesQ9/Self-Evolving-Agents) |

## Abstract

Large Language Models (LLMs) have demonstrated remarkable capabilities across diverse tasks but remain fundamentally static, unable to adapt their internal parameters to novel tasks, evolving knowledge domains, or dynamic interaction contexts. This survey provides the first systematic and comprehensive review of self-evolving agents, organizing the field around three foundational dimensions: what to evolve (models, memory, tools, architecture), when to evolve (intra-test-time vs inter-test-time), and how to evolve (reward-based, imitation-based, population-based). Additionally covers evaluation metrics/benchmarks, applications in coding/education/healthcare, and challenges in safety, scalability, and co-evolutionary dynamics.

## Table of Contents

| Paper Section | Note | Key Content |
|---------------|------|-------------|
| §1 Introduction, §2 Definitions | [paper_gao2025survey_intro](paper_gao2025survey_intro.md) | Problem motivation, formal POMDP definition, positioning vs curriculum/lifelong/model editing |
| §3-§5 Taxonomy (What/When/How) | [paper_gao2025survey_taxonomy](paper_gao2025survey_taxonomy.md) | Three-dimensional classification framework with taxonomy tree |
| §3 What to Evolve | [paper_gao2025survey_survey_what](paper_gao2025survey_survey_what.md) | Models (policy + experience), Context (memory + prompts), Tools (create/master/manage), Architecture (single + multi-agent) |
| §4 When to Evolve | [paper_gao2025survey_survey_when](paper_gao2025survey_survey_when.md) | Intra-test-time vs Inter-test-time × ICL/SFT/RL |
| §5 How to Evolve | [paper_gao2025survey_survey_how](paper_gao2025survey_survey_how.md) | Reward-based (4 types), Imitation (self/cross/hybrid), Population-based (evolution + self-play) |
| §6 Where to Evolve | [paper_gao2025survey_survey_where](paper_gao2025survey_survey_where.md) | General domain (memory, co-evolution, curriculum) vs Specialized (coding, GUI, finance, medical, education) |
| §7 Evaluation | [paper_gao2025survey_benchmark](paper_gao2025survey_benchmark.md) | 5 goals (adaptivity, retention, generalization, efficiency, safety), 30+ benchmarks, standardized protocols |
| §8 Future Directions | [paper_gao2025survey_benchmark](paper_gao2025survey_benchmark.md) | Personalization, generalization, safety/compliance checklist, multi-agent ecosystems |
| **Review** | [review_gao2025survey](review_gao2025survey.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 7 questions (3 review lenses applied) |

## Summary

<!-- VERIFY -->
- **Introduction**: LLMs are fundamentally static; self-evolving agents represent a paradigm shift from scaling static models to developing systems that continuously learn from data, interactions, and experiences. Formally defined via POMDP with self-evolving strategy as a transformation function.
- **Taxonomy**: Three orthogonal dimensions — What (4 pillars: model, context, tools, architecture), When (intra vs inter test-time × 3 learning paradigms), How (reward-based, imitation, population-based) — plus Where (general vs specialized domains) and Evaluation (5 goals).
- **Key Insight**: Self-evolving agents differ from lifelong learning by having runtime context adaptation, active exploration, and structural self-modification capabilities — not just parameter updates.

## Relevance to Our Work

- Related: [Continual Learning](../term_dictionary/term_continual_learning.md) — BRP's continual learning research directly addresses the "when to evolve" dimension; self-evolving agents extend this beyond parameter updates
- Related: [Catastrophic Forgetting](../term_dictionary/term_catastrophic_forgetting.md) — Identified as a key challenge in §8.2; BRP faces this in abuse model retraining
- Related: [GreenTEA](../term_dictionary/term_greentea.md) — BRP's agentic AI for investigation automation is a proto-self-evolving agent (prompt optimization + tool use)
- Related: [AutoSignality](../term_dictionary/term_autosignality.md) — Automated fraud signal generation maps to the "tool creation" evolutionary locus
- Related: [RL](../term_dictionary/term_rl.md) — Reinforcement learning is a core "how to evolve" mechanism across all temporal phases
- Related: [UCM](../term_dictionary/term_ucm.md) — Unified Concessions Model's cross-market learning relates to knowledge transfer in self-evolving agents

## Questions

- How would BRP's abuse detection models benefit from intra-test-time self-evolution (adapting during investigation)?
- Could GreenTEA's SOP-driven prompting be formalized as a prompt optimization evolutionary locus?
- What safety guardrails from §8.3 (sandboxing, audit trails, approval gates) apply to BRP's agentic automation?
- Is the "misevolution" risk (safety alignment degradation during evolution) relevant to BRP's model refresh cycles?

## Related Documentation

### Paper Notes
- [paper_gao2025survey_intro](paper_gao2025survey_intro.md)
- [paper_gao2025survey_taxonomy](paper_gao2025survey_taxonomy.md)
- [paper_gao2025survey_survey_what](paper_gao2025survey_survey_what.md)
- [paper_gao2025survey_survey_when](paper_gao2025survey_survey_when.md)
- [paper_gao2025survey_survey_how](paper_gao2025survey_survey_how.md)
- [paper_gao2025survey_survey_where](paper_gao2025survey_survey_where.md)
- [paper_gao2025survey_benchmark](paper_gao2025survey_benchmark.md)

### Related Vault Notes
- [Continual Learning](../term_dictionary/term_continual_learning.md)
- [Catastrophic Forgetting](../term_dictionary/term_catastrophic_forgetting.md)
- [GreenTEA](../term_dictionary/term_greentea.md)
- [AutoSignality](../term_dictionary/term_autosignality.md)
- [RL](../term_dictionary/term_rl.md)
- [UCM](../term_dictionary/term_ucm.md)
- [Continual Learning ATO](../../projects/project_continual_learning_ato.md)
- [Meta Learning Fraud](../../projects/project_meta_learning_fraud.md)
- [TextGrad](lit_yuksekgonul2024textgrad.md) — Implements "experience-driven self-refinement" via textual gradients; fits the survey's taxonomy of self-evolving agents that improve through feedback without weight updates
- [Textual Gradient](../term_dictionary/term_textual_gradient.md) — Key mechanism in the survey's landscape of self-improvement approaches
