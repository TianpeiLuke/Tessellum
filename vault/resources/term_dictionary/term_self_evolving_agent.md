---
tags:
  - resource
  - terminology
  - agentic_ai
  - reinforcement_learning
  - continual_learning
  - self_improvement
keywords:
  - self evolving agent
  - self-evolving agent
  - autonomous adaptation
  - POMDP
  - experience acquisition
  - self-refinement
  - environment learning
  - social learning
  - model evolution
  - context evolution
  - tool evolution
  - architecture evolution
topics:
  - self-evolving agents
  - agentic AI
  - continual learning
  - reinforcement learning
  - multi-agent systems
language: markdown
date of note: 2026-03-04
status: active
building_block: concept
---

# Self-Evolving Agent

## Definition

A **self-evolving agent** is an AI system that autonomously modifies its internal parameters, contextual state, toolset, or architectural topology based on its own trajectories or feedback signals, with the explicit objective of improving future performance. Unlike static LLM-based agents that rely solely on pre-trained knowledge and fixed prompting strategies, self-evolving agents continuously learn from data, interactions, and experiences -- representing a paradigm shift from scaling static models to developing systems that adapt over time. The concept is formally grounded in the Partially Observable Markov Decision Process (POMDP) framework, where the agent system comprises an architecture, models, context, and tools that are transformed through a self-evolving strategy function.

Three inclusion criteria distinguish self-evolving agents from simpler adaptive systems: (i) **experience-dependent updates** -- the agent's behavior must change based on accumulated experience rather than fixed rules; (ii) **persistent policy-changing effects** -- modifications must carry forward across tasks, not merely within a single inference pass; and (iii) **autonomous exploration or self-initiated learning** -- the agent must actively seek out learning opportunities rather than passively receiving training signals. These criteria separate self-evolving agents from related paradigms such as curriculum learning (no runtime adaptation), lifelong learning (no active exploration or structural change), and model editing (no flexible, environment-responsive strategies).

The self-evolving agent paradigm has gained significant attention as LLMs are deployed in open-ended environments where static knowledge quickly becomes insufficient. Systems like Voyager (open-ended skill acquisition in Minecraft), Reflexion (verbal reinforcement learning via self-reflection), and the Darwin Godel Machine (open-ended self-improving agents) exemplify the frontier of this research. The KARL system (Chang et al., 2026) demonstrates how iterative bootstrapping from increasingly capable models -- a core self-evolving pattern -- can train knowledge agents that achieve state-of-the-art performance on diverse agentic search tasks.

## Core Concepts

### POMDP Formulation

Self-evolving agents are formalized using a POMDP framework with the following components:

| Component | Formal | Description |
|-----------|--------|-------------|
| **Environment** | E = (G, S, A, T, R, Omega, O, gamma) | Goals, states, actions, transitions, rewards, observations |
| **Agent System** | Pi = (Gamma, {psi_i}, {C_i}, {W_i}) | Architecture, models, context, tools |
| **Self-Evolving Strategy** | f(Pi, tau, r) = Pi' | Transformation mapping current system + trajectory + feedback to new system state |
| **Objective** | max_f Sum U(Pi_j, T_j) | Maximize cumulative utility across sequential tasks |

The key insight is that the self-evolving strategy f operates on the entire agent system -- not just model parameters -- enabling adaptation across all four evolutionary loci (models, context, tools, architecture).

### Experience Acquisition

Self-evolving agents acquire experience through two temporal phases:

- **Intra-test-time** (during task execution): The agent adapts while solving a problem, using in-context learning (e.g., Reflexion's verbal self-reflection), supervised fine-tuning on self-generated data, or reinforcement learning from step-level feedback.
- **Inter-test-time** (between tasks): The agent consolidates experience after task completion, updating its policy, memory, or tools for future tasks. This includes workflow memory accumulation, self-training (STaR-style bootstrapping), and RL from outcome rewards.

### Self-Refinement

Self-refinement is the mechanism by which agents improve without external supervision. Three primary modes exist:

1. **Reward-based**: Agents receive feedback signals (textual critique, scalar rewards, environment outcomes, or implicit signals from next-token prediction) and update accordingly. This includes Reflexion-style verbal RL, self-rewarding LMs, and external environment rewards.
2. **Imitation-based**: Agents learn from self-generated demonstrations (STaR bootstrapping), cross-agent knowledge sharing (SiriuS experience libraries), or hybrid approaches combining self-reflection with demonstration filtering.
3. **Population-based**: Multiple agent variants compete or cooperate, with evolutionary selection pressure driving improvement. This includes self-play (Absolute Zero, SPIN) and multi-agent architecture evolution (EvoMAC).

### Environment and Social Learning

Self-evolving agents learn from two interaction modalities:

- **Environment learning**: Direct interaction with task environments provides grounding signals. The agent takes actions, observes outcomes, and updates its strategy. This is the classical RL loop, extended to multi-step agentic rollouts with tool use. KARL exemplifies this with agents learning to iteratively query and reason over document collections.
- **Social learning**: In multi-agent settings, agents learn from peers through knowledge sharing, competitive dynamics, or collaborative problem-solving. Systems like MDTeamGPT maintain shared knowledge bases (CorrectKB + ChainKB), while self-play frameworks like Absolute Zero use challenger-solver dynamics for zero-data bootstrapping.

## Key Frameworks (Gao et al. Survey)

The Gao et al. (2025) survey organizes self-evolving agents along four dimensions:

### What to Evolve -- Evolutionary Loci

| Locus | Components | Examples |
|-------|-----------|----------|
| **Models** | Policy (self-generated SFT/RL data), Experience (environment interaction, self-challenge) | STaR, RAGEN, WebRL |
| **Context** | Memory evolution (long-term, episodic, workflow), Prompt optimization (APE, DSPy, TextGrad, SPO) | Reflexion, Expel, AdaPlanner |
| **Tools** | Autonomous discovery and creation, Mastery through iterative refinement, Scalable management and selection | Voyager, CRAFT, ToolGen |
| **Architecture** | Single-agent (node optimization, autonomous-agent optimization), Multi-agent (workflow optimization, multi-autonomous-agent) | ADAS, AFlow, EvoMAC |

### When to Evolve -- Temporal Phases

Two phases crossed with three learning paradigms (ICL, SFT, RL) yield six cells:

- **Intra-test-time x ICL**: Reflexion, AdaPlanner (adapt during task via in-context reflection)
- **Intra-test-time x SFT**: Self-adaptive LM, TT-SI (fine-tune during task execution)
- **Intra-test-time x RL**: LADDER, TTRL (RL-based adaptation within a single task)
- **Inter-test-time x ICL**: Workflow memory, ICRL (accumulate context between tasks)
- **Inter-test-time x SFT**: SELF, STaR, SiriuS (self-train on completed task data)
- **Inter-test-time x RL**: RAGEN, WebRL, DigiRL (RL from task outcome rewards)

### How to Evolve -- Algorithmic Mechanisms

Three paradigms address the self-evolving strategy implementation:

1. **Reward-based**: Textual feedback (Reflexion), internal rewards (self-confidence, self-rewarding), external rewards (environment, majority voting), implicit rewards (endogenous reward, PIT)
2. **Imitation and demonstration**: Self-generated (STaR, V-STaR), cross-agent (SiriuS), hybrid (RISE, confidence-guided)
3. **Population-based and evolutionary**: Single-agent evolution (DGM, GENOME), self-play (Absolute Zero, SPIN), multi-agent architecture evolution (EvoMAC), knowledge-based evolution (MDTeamGPT)

### Where to Evolve -- Application Domains

- **General domain**: Memory mechanisms, model-agent co-evolution, curriculum design
- **Specialized domains**: Coding (SWE-Dev, SICA), GUI agents (DigiRL), financial, medical (MedAgentSim), education

## Applications to Our Work

The self-evolving agent paradigm has several concrete applications for BRP:

1. **Memory Evolution for Abuse Patterns**: BRP models could maintain evolving memory of abuse MOs (like Expel's experiential learning) to prevent catastrophic forgetting during model refresh. This directly connects to the continual learning project's work on GEM/EWC.

2. **Tool Creation for Signal Generation**: AutoSignality-style automated feature discovery maps directly to the "Autonomous Discovery and Creation" evolutionary locus. Self-evolving agents that create and refine their own fraud signals could reduce manual signal engineering.

3. **Prompt Optimization for Investigation**: GreenTEA's SOP-driven prompting could be formalized as SPO-style self-supervised prompt optimization, enabling the investigation agent to improve its prompting strategy based on investigation outcomes.

4. **RL for Knowledge Agents**: KARL demonstrates that off-policy RL (OAPL) can train agents to iteratively query, retrieve, and reason over large data collections -- directly applicable to BRP's agentic investigation tools that search across case databases and policy documents.

5. **Safety Guardrails**: The survey's compliance checklist (sandboxing, audit trails, approval gates) provides a framework for deploying BRP's agentic automation safely, addressing the "misevolution" risk where safety alignment degrades during evolution.

## Distinguishing from Related Paradigms

| Paradigm | Runtime Context | Evolving Toolset | Dynamic Tasks | Test-time Adaptation | Active Exploration | Structural Change | Self-Reflect |
|----------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Curriculum Learning | - | - | - | - | - | - | - |
| Lifelong Learning | - | - | Yes | - | - | - | - |
| Model Editing | - | - | Yes | Yes | - | - | - |
| **Self-Evolving Agents** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** |

## Related Terms

- [Reinforcement Learning](term_rl.md) -- Core "how to evolve" mechanism; reward-based evolution is the dominant paradigm across all temporal phases
- [RLHF](term_rlhf.md) -- KL-regularized RL foundations from RLHF extend to self-evolving agent training (e.g., KARL's OAPL objective)
- [LLM](term_llm.md) -- Foundation models that self-evolving agents build upon and adapt
- [Continual Learning](term_continual_learning.md) -- Closest related paradigm; self-evolving agents extend lifelong learning with runtime context, active exploration, and structural change
- [Reward Model](term_reward_model.md) -- Provides reward signals for reward-based self-evolution; trained value models enable test-time compute scaling (e.g., KARL's Value-Guided Search)
- [OAPL](term_oapl.md) -- Off-policy RL algorithm used in KARL for training self-evolving knowledge agents
- [AgentZ](term_agentz.md) -- Amazon's agent platform with self-improving onboarding (sandbox → shadow → production)
- [Knowledge Agent](term_knowledge_agent.md) -- A class of self-evolving agent that iteratively queries and reasons over document collections
- [KARLBench](term_karlbench.md) -- Multi-capability evaluation suite for knowledge agents
- [Prompt Optimization](term_prompt_optimization.md) -- Context evolution mechanism; automated refinement of LLM inputs without weight updates (APE, DSPy, ACE)
- [Agentic Memory](term_agentic_memory.md) -- Memory evolution mechanism; A-MEM implements Zettelkasten-inspired self-organizing memory with link generation and memory evolution
- [Textual Gradient](term_textual_gradient.md) -- TextGrad enables self-improving systems through iterative LLM-generated textual feedback on computation graphs
- [Compound AI System](term_compound_ai_system.md) -- Self-evolving agents often operate as compound AI systems with multiple optimizable components
- [Instance Optimization](term_instance_optimization.md) -- Test-time self-improvement by refining individual solutions via textual gradients
- [Deliberate Practice](term_deliberate_practice.md) -- agents that review performance logs and update playbooks perform automated deliberate practice; structured self-improvement through feedback
- [Compound Effect](term_compound_effect.md) -- iterative agent improvement compounds; each iteration builds on prior iterations producing accelerating capability growth (AgentRxiv: +11.4% over 40 iterations)

## References

- Source: [Gao et al. (2025). "A Survey of Self-Evolving Agents"](../papers/lit_gao2025survey.md) -- First systematic survey organizing the field around What/When/How/Where to evolve
- Source: [Chang et al. (2026). "KARL: Knowledge Agents via Reinforcement Learning"](../papers/lit_chang2026karl.md) -- Demonstrates self-evolving agent training via iterative off-policy RL bootstrapping for knowledge agents
- Source: [Zhang et al. (2025). "ACE: Agentic Context Engineering"](../papers/lit_zhang2025agentic.md) -- Context evolution via structured evolving playbooks with Generator-Reflector-Curator pipeline
- Source: [Xu et al. (2025). "A-MEM: Agentic Memory for LLM Agents"](../papers/lit_xu2025amem.md) -- Memory evolution locus: Zettelkasten-inspired agentic memory with note construction, link generation, and memory evolution
- Source: [Yuksekgonul et al. (2024). "TextGrad: Automatic 'Differentiation' via Text"](../papers/lit_yuksekgonul2024textgrad.md) -- Context optimization via textual gradients; enables self-improving systems through iterative LLM feedback on computation graphs

---

**Last Updated**: March 9, 2026
**Status**: Active -- Core concept for next-generation adaptive AI systems
**Domain**: Agentic AI, Reinforcement Learning, Continual Learning, Self-Improvement
