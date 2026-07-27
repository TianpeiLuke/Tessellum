---
tags:
  - resource
  - documentation
  - claude_code
  - mcp
keywords:
  - model context protocol
  - mcp servers
  - connect external tools
  - issue trackers databases monitoring
  - anthropic directory
  - prompt injection trust
  - mcp-server-dev plugin
topics:
  - Claude Code
  - MCP
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/mcp
access_control_group: ["general"]
---

# Claude Code — MCP Overview

## Overview

Claude Code can connect to hundreds of external tools and data sources through the **Model Context Protocol (MCP)**, an open-source standard for AI-tool integrations. MCP servers give Claude Code access to your tools, databases, and APIs — so Claude can read and act on those systems directly instead of working from data you paste into chat.

The signal that you should connect a server is when you find yourself copying data into chat from another tool, such as an issue tracker or a monitoring dashboard. Once a server is connected, Claude can operate on that system directly. This note is the conceptual entry point; for the step-by-step first connection see [cc_mcp_quickstart](cc_mcp_quickstart.md), and the full reference page is the source for the rest of the MCP cluster.

## What you can do with MCP

With MCP servers connected, you can ask Claude Code to handle tasks that span the external systems it now reaches. The docs give six representative task categories:

- **Implement features from issue trackers**: e.g. "Add the feature described in JIRA issue ENG-4521 and create a PR on GitHub."
- **Analyze monitoring data**: e.g. "Check Sentry and Statsig to check the usage of the feature described in ENG-4521."
- **Query databases**: e.g. "Find emails of 10 random users who used feature ENG-4521, based on our PostgreSQL database."
- **Integrate designs**: e.g. "Update our standard email template based on the new Figma designs that were posted in Slack."
- **Automate workflows**: e.g. "Create Gmail drafts inviting these 10 users to a feedback session about the new feature."
- **React to external events**: an MCP server can also act as a *channel* that pushes messages into your session, so Claude reacts to Telegram messages, Discord chats, or webhook events while you're away. (Channels are covered separately at https://code.claude.com/docs/en/channels.)

## Find and build MCP servers

You can browse reviewed connectors in the **Anthropic Directory** (`claude.ai/directory`). Directory connectors use the same MCP infrastructure as Claude Code, so you can add any remote server listed there with `claude mcp add`.

A trust warning applies to every server you connect:

> Verify you trust each server before connecting it. Servers that fetch external content can expose you to [prompt injection risk](https://code.claude.com/docs/en/security#protect-against-prompt-injection).

To build your own server, the docs point to the MCP server guide (`modelcontextprotocol.io`) for protocol fundamentals and the Claude connector building docs for authentication, testing, and Directory submission.

Claude Code can also scaffold a server for you using the official `mcp-server-dev` plugin. After installing the plugin in a Claude Code session, you run the build skill, and Claude asks about your use case and scaffolds a remote HTTP or local stdio server:

```
/mcp-server-dev:build-mcp-server
```

(Installing and reloading the plugin is part of the plugin system; see https://code.claude.com/docs/en/plugins for plugin install/marketplace details.)

## Related Notes

### Related Notes (Claude Code Series)

- [Claude Code — MCP Quickstart](cc_mcp_quickstart.md) — relevance: this overview points the reader to the quickstart for the step-by-step first connection (`claude mcp add` → verify → use); it is the procedural counterpart to this conceptual entry point.
- [Claude Code — MCP Transports](cc_mcp_transports.md) — relevance: the overview says servers are added with `claude mcp add`; this sibling details the four transports (HTTP/SSE/stdio/WebSocket) that connection actually uses.
- [Claude Code — Managed MCP Configuration](cc_managed_mcp_configuration.md) — relevance: the overview's "verify you trust each server" warning is enforced organizationally by the allowlist/denylist controls this sibling documents.
- [Claude Code — MCP Tool Search](cc_mcp_tool_search.md) — relevance: connecting many servers (the overview's premise) inflates context; this sibling covers the deferred-tool-loading that keeps that affordable.
- [Claude Code — Extending Claude Code](cc_extending_claude_code.md) — relevance: the overview frames MCP as one extension layer; this note situates it among skills/hooks/subagents/plugins as complementary extensions.

### Related Notes (Out-of-Series)

- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — open standardized protocol letting LLMs connect to external data sources and tools; relevance: this note IS the Claude Code overview of MCP, so the term note is its canonical definitional anchor (linked, not recreated).
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — LLM capability to invoke external functions/APIs via structured tool calls; relevance: MCP servers expose their capabilities as tools Claude calls, so MCP is a tool-use delivery mechanism this overview frames.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic CLI coding tool; relevance: the note documents Claude Code's own MCP connectivity, so the product term grounds what is being extended.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — software infrastructure wrapping an LLM with tools/context/execution; relevance: MCP servers plug into the harness's tool layer, expanding what the harness can do beyond built-in tools.
- [OWASP Top 10 for LLM Applications](../../term_dictionary/term_owasp_llm.md) — security framework for the most critical LLM-deployment vulnerabilities; relevance: the note's trust warning that servers fetching external content can expose you to prompt-injection risk is exactly an OWASP-LLM threat class.
- [Skills](../../term_dictionary/term_skills.md) — packaged expertise extending agent capabilities; relevance: the note contrasts MCP (external tool connection) with skills (packaged knowledge) and cites the `mcp-server-dev` scaffolding plugin.
- [Tool: Example MCP Server](../../tools/tool_example_mcp.md) — relevance: a concrete MCP server you would connect via the `claude mcp add` flow this overview introduces — the real-world server behind the abstraction.
- [Tool: Popular Open-Source MCP Servers](../../tools/tool_popular_mcp_servers.md) — relevance: a catalog of the kind of community MCP servers the overview's "Anthropic Directory" surfaces for connection.
- [Org MCP Guidance](../org_docs/org_mcp_guidance.md) — relevance: organizational policy/assessment guidance for adopting MCP servers, the org-context complement to the overview's generic trust warning.
- [Vetted MCP Servers Reference](../references/ref_vetted_mcp_servers.md) — relevance: a reference list of vetted MCP servers, concrete instances of the connectable servers this overview describes.
- [AgentCore Gateway — MCP Server Target Concepts](../aws_bedrock_agentcore/bedrock_agentcore_gateway_target_mcp_concepts.md) — relevance: shows how the same MCP protocol is exposed server-side on AWS Bedrock AgentCore, the production hosting analog of the servers Claude Code connects to.

*(No project note is closely relevant to the MCP overview specifically; project-level MCP usage is captured in the tool/doc links above.)*
- **[Workspace MCP Tools Reference — The 80+ Workspace Tool Surface](../workspace_tools/workspace_mcp_tools_reference.md)** — a workspace platform exposing **80+ MCP tools** that agents use to interact with the workspace, auto-injected into every ACP session (no manual approval)…

**Source**: https://code.claude.com/docs/en/mcp
**Last Updated**: 2026-06-13
**Status**: Active
