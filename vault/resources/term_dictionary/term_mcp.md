---
tags:
  - resource
  - terminology
  - agentic_ai
  - developer_tools
  - protocol
  - infrastructure
keywords:
  - MCP
  - Model Context Protocol
  - agentic AI
  - tool integration
  - AI assistant
  - LLM
topics:
  - agentic AI
  - developer tools
  - AI infrastructure
  - context engineering
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# MCP - Model Context Protocol

## Definition

**MCP** stands for **Model Context Protocol**. It is an open, standardized protocol that defines how applications provide context to Large Language Models (LLMs), enabling AI assistants to connect with external data sources, tools, and services through a unified interface. MCP lets AI tools discover and invoke capabilities exposed by servers without requiring a bespoke integration for each tool, so agents can assemble contextual, task-relevant information from many sources.

**Key Function**: Standardized interface connecting AI models to external tools, data sources, and services - enabling more capable agents and complex agentic workflows.

## Full Name

**Model Context Protocol**

**Key Benefits**:
- Build more capable and versatile AI agents
- Enable complex multi-step workflows
- Flexibility to switch between LLM providers
- Secure, standardized data integration
- Standardized tool discovery and invocation

## Key Highlights

**Architecture & Protocol Design** -- MCP follows a three-tier architecture (Client-Server-Data Sources) using JSON-RPC over stdio or HTTP. Clients (AI assistants and IDEs) discover and invoke tools exposed by MCP servers, which in turn connect to external data sources and tools. The protocol supports multiple context-loading patterns -- eager, progressive disclosure, and on-invoke -- for context-efficient tool management. MCP also complements the emerging Agent-to-Agent (A2A) protocol for multi-agent collaboration.

**Ecosystem & Operations** -- MCP servers can be curated in registries that catalog reviewed servers, and clients configure which servers to load. Server owners are responsible for maintaining metadata, versioning, and security posture. Security reviews commonly follow tiered assessment models before a server is broadly recommended for use.

**Use Cases & Comparative Advantage** -- MCP enables AI-assisted software development (code search, ticket lookup, documentation reading), investigation and analysis support (data queries, procedure retrieval, related-record lookup), and agentic context-engineering workflows. Compared to direct API calls or custom plugins, MCP provides universal standardization, automatic tool discovery, LLM-provider portability, centralized security review, and simplified maintenance.

## Related Terms

### AI Development Tools
- **[Skills](term_skills.md)**: Packaged expertise for AI agents

### Protocols & Standards
- **[A2A](term_a2a.md)**: Agent-to-Agent Protocol (complements MCP)
- **JSON-RPC**: Communication protocol used by MCP

### Context Engineering
- **[RAG](term_rag.md)**: Retrieval Augmented Generation
- **[LLM](term_llm.md)**: Large Language Models (consumers of MCP context)

## References

### Specification
- **MCP Official Docs**: https://modelcontextprotocol.io/docs/getting-started/intro
- **MCP Specification**: https://modelcontextprotocol.io/specification

### External Resources
- **MCP GitHub Organization**: https://github.com/modelcontextprotocol
- **Introducing the Model Context Protocol (Anthropic)**: https://www.anthropic.com/news/model-context-protocol

## Summary

**MCP Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Full Name** | Model Context Protocol |
| **Purpose** | Standardized AI-to-tool communication |
| **Transport** | JSON-RPC over stdio or HTTP |
| **Architecture** | Client - Server - Data Sources |
| **Complementary Protocol** | A2A (Agent-to-Agent) |
| **Status** | Open standard |

**Key Insight**: MCP is a **foundational protocol enabling agentic AI**. By providing a standardized interface between AI assistants and external tools/data, MCP lets developers leverage AI capabilities without building custom integrations for each tool. As agentic workflows mature, MCP serves as the **tool integration backbone** connecting AI reasoning to operational systems - agents can query data sources, fetch documentation, look up related records, and assemble context from multiple sources through natural language interactions.

---

**Last Updated**: March 15, 2026
**Status**: Active - core protocol for agentic AI development
</content>
