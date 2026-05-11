---
tags:
  - resource
  - terminology
  - llm_evaluation
  - agentic_ai
keywords:
  - rubric discovery
  - adaptive rubrics
  - evaluation criteria generation
  - self-evolving evaluation
  - dynamic rubric synthesis
topics:
  - AI Evaluation
  - LLM Agents
language: markdown
date of note: 2026-03-10
status: active
building_block: concept
---

# Term: Rubric Discovery

## Definition

**Rubric Discovery** is the capability of agent judges to autonomously formulate, refine, and evolve evaluation criteria (rubrics) during operation, rather than relying on predefined static rubrics. This is a hallmark of Self-Evolving Agent-as-a-Judge systems. Rubric discovery enables evaluation agents to adapt to novel tasks and domains without requiring human-authored scoring guidelines, by synthesizing criteria from task descriptions, exemplars, and accumulated evaluation experience.

**Key Function**: Shift evaluation criteria from static human-authored guidelines to dynamically generated and continuously refined rubrics, enabling agentic judges to handle novel evaluation domains autonomously.

## Full Name

**Rubric Discovery** (also: Adaptive Rubric Generation, Dynamic Rubric Synthesis)

## How Rubric Discovery Works

### Approaches

| Method | Approach | Stage | Key Innovation |
|--------|----------|-------|----------------|
| **EvalAgents** | Web-search for rubric components; synthesize from retrieved evaluation standards | Self-Evolving | External knowledge retrieval for rubric construction |
| **AGENT-X** | Adaptive router selects evaluation guidelines and subagents based on task characteristics | Reactive/Self-Evolving | Dynamic guideline selection from a growing library |
| **ARJudge** | Iterative questioning to progressively refine evaluation criteria during assessment | Self-Evolving | Rubric emerges from evaluation interaction |
| **OnlineRubrics** | RL-integrated rubric evolution; rubrics updated based on evaluation outcomes and human feedback | Self-Evolving | Continuous rubric improvement through reinforcement signals |
| **GradeOpt** | Iterative guideline refinement via feedback loops for educational assessment | Self-Evolving | Rubric co-evolution with grading outcomes |
| **FinDeepResearch** | Hierarchical rubric generation from financial report structure | Reactive | Domain-specific rubric decomposition |

### Rubric Discovery vs Static Rubrics

| Aspect | Static Rubrics | Rubric Discovery |
|--------|---------------|-----------------|
| **Source** | Human-authored | Agent-generated |
| **Adaptability** | Fixed at design time | Evolves during operation |
| **Domain coverage** | Limited to authored domains | Generalizes to novel domains |
| **Consistency** | High (same rubric always) | Variable (rubric evolves) |
| **Cost** | High upfront (expert authoring) | Low upfront, continuous compute |
| **Quality** | Depends on expert quality | Depends on agent capability |

### Connection to Self-Evolving Agents

Rubric discovery is the evaluation-specific manifestation of self-evolving agent capabilities. In the Agent-as-a-Judge taxonomy:
- **Procedural agents**: Use fixed, externally supplied rubrics
- **Reactive agents**: Select rubrics from a predefined set based on task characteristics
- **Self-Evolving agents**: Synthesize rubrics on-the-fly and refine them through experience

## Relevance to BRP

- **Abuse policy evolution**: As new abuse patterns emerge, rubric discovery can automatically generate evaluation criteria from policy documents and historical decisions
- **GreenTEA SOP compliance**: Instead of static SOP checklists, rubric discovery can synthesize compliance criteria that adapt to new investigation workflows
- **Model evaluation**: Rubric discovery can generate evaluation criteria for new model types without manual rubric authoring

## Related Terms

- **[Term: Agent-as-a-Judge](term_agent_as_a_judge.md)** — Rubric discovery is a key differentiator of advanced Agent-as-a-Judge systems
- **[Term: Self-Evolving Agent](term_self_evolving_agent.md)** — Self-Evolving agents are the developmental stage where rubric discovery emerges
- **[Term: Prompt Optimization](term_prompt_optimization.md)** — Rubric discovery can be viewed as prompt optimization applied to evaluation criteria
- **[Term: Agentic Evaluation](term_agentic_evaluation.md)** — Rubric discovery is an advanced capability within the agentic evaluation umbrella
- **[Term: LLM-as-a-Judge](term_llm_as_a_judge.md)** — LLM-as-a-Judge relies on static rubrics; rubric discovery overcomes this limitation

## References

- You et al. (2026), "Agent-as-a-Judge: Evaluate Agents with Agents" — [lit_you2026agent](../papers/lit_you2026agent.md) | [planning branch](../papers/paper_you2026agent_survey_planning.md) | [benchmark](../papers/paper_you2026agent_benchmark.md)
- EvalAgents, AGENT-X, ARJudge, OnlineRubrics — representative systems implementing rubric discovery
