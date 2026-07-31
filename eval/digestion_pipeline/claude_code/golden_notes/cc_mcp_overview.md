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

**Source**: https://code.claude.com/docs/en/mcp
**Last Updated**: 2026-06-13
**Status**: Active
