---
tags:
  - resource
  - terminology
  - agentic_ai
  - multi_agent_systems
  - protocol
  - interoperability
keywords:
  - A2A
  - Agent2Agent
  - Agent-to-Agent
  - agent interoperability
  - Google
  - Linux Foundation
  - Agent Card
  - JSON-RPC
  - multi-agent communication
topics:
  - Multi-Agent Systems
  - Agent Interoperability
  - Open Standards
language: markdown
date of note: 2026-04-09
status: active
building_block: concept
---

# A2A (Agent2Agent Protocol)

## Definition

**Agent2Agent (A2A)** is an open protocol that defines how AI agents communicate with each other across different systems, platforms, and vendors. Announced by Google at Cloud Next in April 2025, transferred to the Linux Foundation in June 2025, and backed by 150+ organizations including AWS, Microsoft, Cisco, Salesforce, and SAP. A2A enables agents to discover one another, exchange structured messages, and coordinate tasks without requiring shared internal state or proprietary integrations.

**A2A is to agent-agent communication what MCP is to agent-tool communication.** MCP connects agents to tools and data sources (vertical); A2A connects agents to each other (horizontal). Both protocols are complementary and active in the same system at different layers.

## Historical Context

| Date | Event |
|------|-------|
| April 9, 2025 | Google announces A2A at Cloud Next 2025 with 50+ partners |
| May 2025 | Microsoft announces A2A support in its AI platforms |
| June 2025 | Google transfers A2A to Linux Foundation for vendor-neutral governance |
| Mid-2025 | Partner count grows past 150 (AWS, Cisco join as validators) |

## Key Properties

- **Agent Cards**: JSON metadata documents describing an agent's capabilities and access endpoints — the discovery mechanism
- **Built on web standards**: HTTP, JSON-RPC 2.0, Server-Sent Events (SSE) — no proprietary protocols
- **Opaque agents**: Agents collaborate without sharing memory, tools, or execution plans — only exchanging messages
- **Security**: TLS, JSON Web Tokens (JWTs), OpenID Connect for authentication and authorization
- **Multi-modal**: Supports text, images, video, and structured data exchange
- **Multi-turn**: Supports long-running conversations and task coordination
- **Open source**: Apache 2.0 license, governed by Linux Foundation

## A2A vs MCP

| Dimension | A2A | MCP |
|-----------|-----|-----|
| **Focus** | Agent-to-agent communication | Agent-to-tool/data connection |
| **Analogy** | Network cable between agents | USB-C port for tools |
| **Direction** | Horizontal (peer-to-peer) | Vertical (agent-to-resource) |
| **Originator** | Google (2025) | Anthropic (2024) |
| **Governance** | Linux Foundation | Anthropic |
| **Transport** | HTTP + JSON-RPC + SSE | JSON-RPC over stdio/SSE |
| **Discovery** | Agent Cards | Tool manifests |
| **State sharing** | No shared state (opaque) | Shared context window |

## Design Principles

1. **Embrace agentic capabilities**: Agents collaborate without sharing memory, tools, or execution plans
2. **Built on open standards**: HTTP, JSON-RPC, SSE for easy interoperability
3. **Security first**: TLS, JWT, OpenID Connect for authentication
4. **Support long-running tasks**: Multi-turn conversations with streaming
5. **Modality agnostic**: Text, images, video, structured data

## Related Terms
- **[MCP](term_mcp.md)**: Model Context Protocol — complementary protocol for agent-to-tool connections
- **[Multi-Agent Collaboration](term_multi_agent_collaboration.md)**: Broader paradigm that A2A enables
- **[Agent Orchestration](term_agent_orchestration.md)**: Coordination patterns that can use A2A for inter-agent communication
- **[Agent-as-a-Tool](term_agent_as_a_tool.md)**: Pattern where agents wrap other agents — A2A formalizes the communication layer
- **[Strands Agents](../tools/tool_strands_agents.md)**: AWS agent SDK that can use A2A for multi-agent patterns
- **[GenAI](term_genai.md)**: Generative AI

## References

### External Sources
- [Google Blog: Announcing A2A](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) — Original announcement
- [Wikipedia: Agent2Agent](https://en.wikipedia.org/wiki/Agent2Agent) — Overview and history
- [A2A Protocol Website](https://a2a-protocol.org/) — Official specification
- [GitHub: google/A2A](https://github.com/google/A2A) — Source code and SDK
- [Linux Foundation: A2A Project](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents) — Governance announcement
- [Microsoft: A2A Support](https://www.microsoft.com/en-us/microsoft-cloud/blog/2025/05/07/empowering-multi-agent-apps-with-the-open-agent2agent-a2a-protocol/) — Microsoft adoption
- [AWS Blog: Open Protocols for Agent Interoperability](https://aws.amazon.com/blogs/opensource/open-protocols-for-agent-interoperability-part-1-inter-agent-communication-on-mcp/) — AWS perspective on A2A + MCP
- [arXiv: MCP vs A2A vs ACP vs ANP Comparison](https://arxiv.org/html/2505.02279v1) — Academic comparison of agent protocols
