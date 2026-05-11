---
tags:
  - resource
  - terminology
  - agentic_ai
  - agent_platform
  - mcp
  - buyer_abuse_prevention
  - ai_infrastructure
keywords:
  - AgentSpace
  - Agentic AI
  - Agent Platform
  - Model Context Protocol
  - MCP
  - AI Agent Environment
  - Multi-Agent Systems
  - Agent Orchestration
topics:
  - agentic AI
  - agent platforms
  - buyer abuse prevention
  - AI infrastructure
  - multi-agent systems
  - agent orchestration
language: markdown
date of note: 2026-03-14
status: active
building_block: concept
related_wiki: https://docs.hub.amazon.dev/gen-ai-dev/mcp-guidance/
---

# AgentSpace - Agentic AI Environment and Platform Framework

## Definition

**AgentSpace** is the conceptual and technical framework encompassing the **integrated environment where AI agents operate, collaborate, and access resources** within Amazon's buyer abuse prevention ecosystem. At Amazon/BRP, AgentSpace represents the **convergence of agentic AI systems, MCP (Model Context Protocol) tool integration, and multi-agent orchestration platforms** that enable autonomous fraud detection, investigation automation, and adaptive threat response. The framework combines **specialized AI agents** (PROPHET 2.0, Nirvana, Cursus) with **MCP-enabled resource access** (Andes, BumbleBee, Datanet) to create a **unified intelligent environment** where agents can dynamically access data, tools, and services while maintaining contextual awareness and collaborative workflows.

**Key Function**: Provide an integrated operational environment where AI agents can autonomously access resources, collaborate with other agents, and execute complex buyer abuse prevention tasks through standardized protocols and shared context management.

## Full Name

**Agentic AI Environment and Platform Framework for Buyer Abuse Prevention**

**Synonyms & Related Terms**:
- **Agent Platform**: Infrastructure supporting multiple AI agents
- **Agentic Environment**: Operational space for AI agent interactions
- **Multi-Agent System**: Coordinated network of AI agents
- **Agent Orchestration Platform**: System managing agent workflows and interactions

## Key Highlights

**Architecture**: Three-layer architecture — Agent Layer (PROPHET 2.0, Nirvana, BRP Agent Platform V2), MCP Integration Layer (Andes, BumbleBee, Datanet), and Resource Layer (data sources, tools, knowledge bases). Supports three collaboration patterns: sequential agent chaining, parallel execution with coordination, and hierarchical supervisor-specialist organization. Five core principles: autonomous operation, resource integration, contextual awareness, collaborative intelligence, and adaptive learning.

**BRP Agent Ecosystem**: Four major agentic systems — PROPHET 2.0 (ReAct framework with episodic memory for phishing detection), Nirvana (Claude 3 Sonnet for SOP automation with mini-SOP StateMachines), BRP Agent Platform V2 (containerized multi-agent platform hosting ChatBRP, RISE, Analytics Assistant with Harmony UI), and Cursus (Slipbox-based context engine achieving 90% development time reduction and 65,000+ lines of code). MCP integration via Andes (datasets), BumbleBee (metadata), Datanet (ETL), Cradle (processing), Builder (42+ tools), COE (incidents), Cornell (catalog), Pippin (SDLC).

**Benefits and Evolution**: Key benefits include automated threat detection, 90% development acceleration, multi-agent validation, and elastic deployment. Evolution: individual agents (2024) → agentic workflow integration (2025) → unified AgentSpace framework with comprehensive MCP integration (2026) → self-managing agent ecosystems (future). Research directions include advanced memory systems, meta-learning agents, and collaborative reasoning.

## See Also

- **[AgentSpace Architecture and Integration at Amazon/BRP](../policy_sops/sop_agentspace_architecture_and_integration.md)** — Three-layer architecture diagrams, workflow orchestration patterns (sequential/parallel/hierarchical), core principles, key architectural components, BRP agent ecosystem details (PROPHET 2.0/Nirvana/BRP Agent Platform V2/Cursus with implementation patterns and key innovations), MCP integration framework, integration patterns (MCP-enabled access, cross-agent communication, human-agent collaboration), architecture component layers (runtime/MCP/orchestration/storage), implementation technologies (agent frameworks, MCP servers, platform infrastructure)
- **[AgentSpace Benefits and Evolution at Amazon/BRP](../analysis_thoughts/thought_agentspace_evolution.md)** — Operational efficiency, scalability and adaptability, quality and reliability, innovation enablement benefits for BRP, historical development timeline (2024-2026), current state assessment, future vision (self-organizing agents, continuous learning), near-term and long-term evolution directions, research directions (advanced memory, meta-learning, collaborative reasoning, ethical AI)

## Related Terms

### Agent Technologies
- **[AgentSpaces](term_agentspaces.md)**: Zero-setup AI agent platform at agentspaces.amazon.dev (product implementation)
- **[Agentic AI](term_agentic_ai.md)**: AI systems capable of autonomous action and decision-making
- **[Multi-Agent Systems](term_multi_agent_systems.md)**: Networks of interacting AI agents
- **[Agent Orchestration](term_agent_orchestration.md)**: Coordination and management of agent workflows
- **[Episodic Memory](term_episodic_memory.md)**: Long-term memory system for agent learning

### MCP and Integration
- **[MCP](term_mcp.md)**: Model Context Protocol for tool and resource integration
- **[BumbleBee MCP](term_bumblebee_mcp.md)**: Database metadata access through MCP
- **[Andes MCP](term_andes_mcp.md)**: Data marketplace integration via MCP
- **[Builder MCP](term_builder_mcp.md)**: Amazon internal tooling through MCP

### BRP Agent Systems
- **[PROPHET](term_prophet.md)**: Multi-modal agentic AI for phishing detection
- **[Nirvana](term_nirvana.md)**: Agentic workflow for SOP automation
- **[BRP Agent Platform](term_brp_agent_platform.md)**: Multi-agent hosting platform
- **[Cursus](term_cursus.md)**: Automated development with agentic workflows

### Development and Operations
- **[ReAct Framework](term_react_framework.md)**: Reasoning and Acting pattern for agents
- **[LangGraph](term_langgraph.md)**: Graph-based agent workflow definition
- **[Bedrock Agents](term_bedrock_agents.md)**: Amazon Bedrock agent framework
- **[Slipbox](term_slipbox.md)**: Knowledge management system for [context engineering](term_context_engineering.md)

## References

### Amazon Internal
- **BuilderHub MCP Guidance**: https://docs.hub.amazon.dev/gen-ai-dev/mcp-guidance/
- **BRP Agent Platform Wiki**: https://w.amazon.com/bin/view/BuyerAbuse/Engineering/Internal/ (Agent Platform section)
- **MCP Registry**: https://console.harmony.a2z.com/mcp-registry - Complete catalog of MCP servers
- **PROPHET 2.0 Documentation**: Internal agentic AI architecture documentation
- **Nirvana SOP Automation**: Agentic workflow documentation and implementation guides

### Training Resources
- **Agentic AI Foundations**: Internal training on autonomous AI system design
- **MCP Integration Guide**: Hands-on training for Model Context Protocol implementation
- **Multi-Agent Systems**: Best practices for agent coordination and collaboration
- **Agent Platform Development**: Building and deploying agents in Amazon infrastructure

### External Standards
- **Model Context Protocol Specification**: Official MCP protocol documentation
- **ReAct Framework Paper**: Academic foundation for Reasoning and Acting agents
- **Multi-Agent Systems Research**: Academic literature on agent coordination
- **Autonomous AI Guidelines**: Industry best practices for autonomous AI systems

