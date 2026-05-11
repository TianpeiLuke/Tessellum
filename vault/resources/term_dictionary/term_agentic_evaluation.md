---
tags:
  - resource
  - terminology
  - llm_evaluation
  - agentic_ai
keywords:
  - agentic evaluation
  - automated evaluation
  - agent judge
  - multi-step evaluation
  - tool-augmented assessment
topics:
  - AI Evaluation
  - LLM Agents
language: markdown
date of note: 2026-03-10
status: active
building_block: concept
---

# Term: Agentic Evaluation

## Definition

**Agentic Evaluation** is an automated evaluation approach using LLM agents with agentic capabilities — planning, tool use, memory, and multi-agent collaboration — rather than single-pass LLM inference. Agentic evaluation systems orchestrate multiple reasoning steps, invoke external verification tools (code execution, retrieval, formal provers), and optionally coordinate across specialized sub-agents to produce evaluation judgments that are grounded in evidence rather than solely in the model's parametric knowledge.

**Key Function**: Replace passive, single-pass evaluation with active, multi-step assessment workflows that can interact with the environment to verify claims and ground judgments.

## Full Name

**Agentic Evaluation**

**Synonyms & Related Terms**:
- **Agent-Based Evaluation**: Equivalent term
- **Multi-Step Evaluation**: Emphasizes the iterative nature
- **Grounded Evaluation**: Emphasizes tool-augmented evidence gathering

## How Agentic Evaluation Works

### Contrast with Traditional Approaches

| Approach | Steps | Tool Use | Memory | Grounding |
|----------|-------|----------|--------|-----------|
| **Metric-Based** (BLEU, ROUGE) | 1 | None | None | Lexical overlap |
| **LLM-as-a-Judge** | 1 | None | None | Parametric knowledge |
| **Agentic Evaluation** | N (multi-step) | Code exec, search, provers | Optional persistent | External evidence |

### Core Capabilities

1. **Planning**: Decompose complex evaluation into structured sub-tasks (e.g., check correctness, assess style, verify factual claims separately)
2. **Tool Use**: Invoke external tools — run code to verify solutions, search databases for fact-checking, use formal provers for mathematical correctness
3. **Memory**: Maintain evaluation state across steps (intermediate results, evidence collected) and optionally across evaluation sessions (learned rubrics, calibration data)
4. **Collaboration**: Coordinate multiple specialized agents — debate for robustness, task decomposition for thoroughness, meta-evaluation for quality control

### When Agentic Evaluation is Warranted

| Scenario | Traditional Sufficient? | Agentic Needed? |
|----------|------------------------|-----------------|
| Short factual QA | Yes (LLM-as-a-Judge) | No |
| Code correctness | Partially (test suites) | Yes (execution + reasoning) |
| Multi-step agent trajectories | No | Yes (trajectory replay, tool verification) |
| Domain-specific assessment | Depends on domain | Yes (domain tools, expert agents) |
| High-volume simple eval | Yes (LLM-as-a-Judge) | No (cost prohibitive) |

## Related Terms

- **[Term: Agent-as-a-Judge](term_agent_as_a_judge.md)** — Specific paradigm within agentic evaluation with a developmental taxonomy
- **[Term: LLM-as-a-Judge](term_llm_as_a_judge.md)** — Single-pass predecessor that agentic evaluation extends
- **[Term: Reward Model](term_reward_model.md)** — Agentic evaluation can incorporate reward model signals as one component
- **[Term: Self-Evolving Agent](term_self_evolving_agent.md)** — Self-evolving agentic evaluation agents improve their own assessment capabilities
- **[Term: Rubric Discovery](term_rubric_discovery.md)** — Advanced agentic evaluation capability: autonomous generation of evaluation criteria
- **[Term: Prompt Optimization](term_prompt_optimization.md)** — Adaptive inference-time methods are runtime prompt optimization for evaluation
- **[Delegated Work](term_delegated_work.md)** — Long-horizon delegated workflows (DELEGATE-52) are a stress test for agentic evaluation methodology

## References

- You et al. (2026), "Agent-as-a-Judge: Evaluate Agents with Agents" — [lit_you2026agent](../papers/lit_you2026agent.md) — First comprehensive survey of agentic evaluation
- Zheng et al. (2023), "Judging LLM-as-a-Judge" — [lit_zheng2023judging](../papers/lit_zheng2023judging.md) — Establishes the non-agentic baseline
