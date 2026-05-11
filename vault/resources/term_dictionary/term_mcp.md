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
  - builder-mcp
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
related_wiki: https://docs.hub.amazon.dev/docs/gen-ai-dev/mcp-guidance/
---

# MCP - Model Context Protocol

## Definition

**MCP** stands for **Model Context Protocol**. It is an open standardized protocol that defines how applications provide context to Large Language Models (LLMs), enabling AI assistants to connect with external data sources, tools, and services through a unified interface. At Amazon, MCP powers the integration between AI coding assistants (Kiro, Cline, Q Developer, Wasabi) and internal tools like SIM, Wiki, Code Browser, Paragon, and other Amazon-specific services, allowing AI tools to provide contextual and relevant assistance by understanding Amazon workflows.

**Key Function**: Standardized interface connecting AI models to external tools, data sources, and services - enabling more capable agents and complex agentic workflows.

## Full Name

**Model Context Protocol**

**Key Benefits**:
- Build more capable and versatile AI agents
- Enable complex multi-step workflows
- Flexibility to switch between LLM providers
- Secure data integration within infrastructure
- Standardized tool discovery and invocation

## Key Highlights

**Architecture & Protocol Design** -- MCP follows a three-tier architecture (Client-Server-Data Sources) using JSON-RPC over stdio or HTTP. Clients such as Kiro, Cline, Q Developer, and Wasabi discover and invoke tools exposed by MCP servers (builder-mcp, aws-api-mcp, custom servers), which in turn connect to external data sources and tools. The protocol supports three loading patterns -- eager, progressive disclosure, and on-invoke -- for context-efficient tool management. MCP also complements the emerging Agent-to-Agent (A2A) protocol for multi-agent collaboration. See [Thought: MCP Architecture and Protocol Components](../analysis_thoughts/thought_mcp_architecture_and_components.md).

**Amazon Ecosystem & Operations** -- At Amazon, the MCP Registry provides a curated catalog of ASBX-reviewed servers (builder-mcp, andes-mcp, aws-api-mcp, aws-knowledge-mcp-server, loaf_mcp). The builder-mcp server is the primary entry point, connecting to 15+ internal tools (SIM, Wiki, Code Browser, Paragon, Quip, PhoneTool, MCM, OnCall, etc.). AIM (AI Integration Manager) handles automated MCP server installation and dependency management. Security review follows a four-tier assessment (Recommended, Supported, Under Assessment, Not Reviewed). See [Thought: MCP Amazon Ecosystem](../analysis_thoughts/thought_mcp_amazon_ecosystem.md), [SOP: MCP Security Review](../policy_sops/sop_mcp_security_review.md), and [SOP: Creating Custom MCP Servers](../policy_sops/sop_mcp_custom_server_development.md).

**Use Cases & Comparative Advantage** -- MCP enables AI-assisted software development (code search, ticket lookup, wiki reading, on-call checks), investigation support (Paragon queries, SOP retrieval, related-ticket lookup), and agentic context-engineering workflows. Compared to direct API calls or custom plugins, MCP provides universal standardization, automatic tool discovery, LLM-provider portability, centralized security review, and simplified maintenance. See [Thought: MCP Use Cases and Protocol Comparison](../analysis_thoughts/thought_mcp_use_cases_and_comparison.md).

## See Also

### Procedures & SOPs
- **[SOP: MCP Security Review and Best Practices](../policy_sops/sop_mcp_security_review.md)** -- ASBX review process, assessment status categories, and security best practices for MCP server usage
- **[SOP: Creating Custom MCP Servers](../policy_sops/sop_mcp_custom_server_development.md)** -- When to create custom servers, six-step development process, and registration workflow

### Analysis & Thoughts
- **[Thought: MCP Architecture and Protocol Components](../analysis_thoughts/thought_mcp_architecture_and_components.md)** -- Three-tier architecture, protocol components, client configuration, loading patterns, communication protocols (agent-to-tool, A2A)
- **[Thought: MCP Amazon Ecosystem and AIM Integration](../analysis_thoughts/thought_mcp_amazon_ecosystem.md)** -- Amazon MCP Registry, builder-mcp capabilities and installation, AIM agent specification and dependency management
- **[Thought: MCP Use Cases and Protocol Comparison](../analysis_thoughts/thought_mcp_use_cases_and_comparison.md)** -- Software development tasks, investigation support, agentic workflows, MCP vs direct API calls vs custom plugins

## FAQ

- **[FAQ: Which MCP Servers Are Approved for Use at Amazon?](../faqs/faq_mcp_server_approved_usage.md)** — Assessment categories, recommended servers, installation, security guidance
- **[FAQ: Is There an MCP Solution to Access share.amazon.com (SharePoint)?](../faqs/faq_mcp_access_sharepoint.md)** -- Options for accessing SharePoint via MCP (m365-mcp, AmazonSharePointMCP, OneDrive workaround)
- **[FAQ: How Do I Create an Internal Wiki Page on w.amazon.com?](../faqs/faq_create_internal_wiki_page.md)** -- 4 methods (UI, CLI, REST API, MCP tools) for creating wiki pages with authentication and rate limits
- **[FAQ: How Do I Register My MCP Server in the Amazon MCP Registry?](../faqs/faq_register_mcp_server_registry.md)** — Self-service registration via aim mcp create/publish
- **[FAQ: How Do I Create My Own MCP Server at Amazon?](../faqs/faq_create_custom_mcp_server.md)** — Local vs remote, prerequisites, development and registration workflow
- **[FAQ: What Are the Benefits of MCP Over Custom Integrations?](../faqs/faq_mcp_benefits_vs_custom_integrations.md)** — MCP vs direct API calls vs custom plugins comparison
- **[FAQ: How Do I Configure MCP Servers for Different AI Clients?](../faqs/faq_configure_mcp_servers_ai_clients.md)** -- Per-client config file locations, JSON format, setup for Kiro, Amazon Q, Cline, Wasabi
- **[FAQ: What Are My Responsibilities as an MCP Server Owner?](../faqs/faq_mcp_server_owner_responsibilities.md)** — Metadata maintenance, semi-annual verification, vending best practices

---

## How-To Guides

- **[How To: Install and Verify session-mcp](../how_to/howto_install_session_mcp.md)** — Set up the v0.5.5 virtual MCP that gives session-tied skills (e.g., `write_coe`) machine-checkable access to the active Claude Code transcript.

---

## Related Terms

### AI Development Tools
- **[AIM](term_aim.md)**: AI Integration Manager (manages MCP configuration)
- **[Skills](term_skills.md)**: Packaged expertise for AI agents
- **[Kiro](term_kiro.md)**: AI-powered IDE
- **[Cline](term_cline.md)**: AI coding assistant in VS Code

### Protocols & Standards
- **[A2A](term_a2a.md)**: Agent-to-Agent Protocol (complements MCP)
- **JSON-RPC**: Communication protocol used by MCP

### Context Engineering
- **[RAG](term_rag.md)**: Retrieval Augmented Generation
- **[LLM](term_llm.md)**: Large Language Models (consumers of MCP context)

## References

### Primary Documentation
- **MCP Guidance**: https://docs.hub.amazon.dev/docs/gen-ai-dev/mcp-guidance/
- **Creating MCP Servers**: https://docs.hub.amazon.dev/docs/gen-ai-dev/creating-mcp-servers/
- **AI Development Terms**: https://docs.hub.amazon.dev/docs/gen-ai-dev/ai-development-terms/

### Training
- **Introduction to MCP at Amazon**: https://atoz.amazon.work/m/learn/transcriptdetail?trainingId=TCRLERN2025062518425977d694e3&trainingLms=LEARN
- **Context Engineering with AI Coding Agents**: https://atoz.amazon.work/m/learn/transcriptdetail?trainingId=TCRLERN20250825042058971fb690&trainingLms=LEARN

### Specification
- **MCP Official Docs**: https://modelcontextprotocol.io/docs/getting-started/intro
- **Amazon MCP Registry**: Internal registry of available MCP servers

### Support
- **Slack**: #kiro-cli-interest, #asbx-aim-interest
- **Kiro Feature Requests**: https://w.amazon.com/bin/view/ASBX/Kiro-AmazonInternal

## Summary

**MCP Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Full Name** | Model Context Protocol |
| **Purpose** | Standardized AI-to-tool communication |
| **Key Server** | builder-mcp (Amazon internal tools) |
| **Clients** | Kiro, Cline, Q Developer, Wasabi |
| **Installation** | `mcp-registry install builder-mcp` |
| **Config Location** | `~/.kiro/settings/mcp.json` |
| **Registry** | Amazon MCP Registry (security-reviewed) |
| **Status Categories** | Recommended, Supported, Under Assessment |
| **Complementary Protocol** | A2A (Agent-to-Agent) |
| **Owner** | ASBX (Amazon Software Builder Experience) |

**Key Insight**: MCP is the **foundational protocol enabling agentic AI** at Amazon. By providing a standardized interface between AI assistants and internal tools/data, MCP enables developers to leverage AI capabilities without building custom integrations for each tool. The **builder-mcp** server is the primary entry point, providing access to 15+ internal websites (SIM, Wiki, Code Browser, Paragon, Quip, PhoneTool, etc.) through a single unified interface. For BAP applications, MCP enables AI-assisted investigations where agents can query Paragon, fetch SOPs from Wiki, look up related tickets, and assemble context from multiple sources - all through natural language interactions. As agentic workflows mature, MCP serves as the **tool integration backbone** connecting AI reasoning to Amazon's operational systems.

### Related Code Repos
- [Code Repo: WorkplaceChatMCP](../../areas/code_repos/repo_workplace_chat_mcp.md) — Slack MCP server (18 tools, Midway SAML auth)


### Related Code Repos
- [Code Repo: CoreServicesMCPServers](../../areas/code_repos/repo_core_services_mcp.md) — Core Services MCP server source code

---

**Last Updated**: March 15, 2026
**Status**: Active - core protocol for agentic AI development at Amazon
