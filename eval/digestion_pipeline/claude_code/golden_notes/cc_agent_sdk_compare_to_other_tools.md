---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - tool_comparison
keywords:
  - agent sdk vs client sdk
  - agent sdk vs claude code cli
  - agent sdk vs managed agents
  - built-in tool loop
  - hosted rest api
  - when to choose
  - in-process library
  - managed sandbox
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/agent-sdk/overview
access_control_group: ["general"]
---

# Compare the Agent SDK to Other Claude Tools

## Overview

The Claude Platform offers multiple ways to build with Claude, and the Agent SDK is one option among several. This note argues *when to choose* the Agent SDK by contrasting it with the three alternatives the overview page compares it against: the **Anthropic Client SDK** (direct API access where you implement the tool loop), the **Claude Code CLI** (the same engine with an interactive interface), and **Managed Agents** (a hosted REST service where Anthropic runs the agent and sandbox). The throughline is *who runs the agent loop and where the work happens* — the Agent SDK occupies the middle ground of an in-process library that ships Claude Code's built-in tool execution, sitting between hand-rolling the loop yourself (Client SDK) and offloading the whole runtime to Anthropic (Managed Agents).

## Agent SDK vs Client SDK

The [Anthropic Client SDK](https://platform.claude.com/docs/en/api/client-sdks) gives you direct API access: you send prompts and implement tool execution yourself. The **Agent SDK** gives you Claude with built-in tool execution.

The deciding difference is the tool loop. With the Client SDK you write the loop — repeatedly calling the API while `stop_reason == "tool_use"`, executing each requested tool, and feeding the result back. With the Agent SDK, Claude handles that loop for you:

```python
# Client SDK: You implement the tool loop
response = client.messages.create(...)
while response.stop_reason == "tool_use":
    result = your_tool_executor(response.tool_use)
    response = client.messages.create(tool_result=result, **params)

# Agent SDK: Claude handles tools autonomously
async for message in query(prompt="Fix the bug in auth.py"):
    print(message)
```

**When to choose:** Reach for the Client SDK when you need raw, low-level API access and want to own tool execution. Reach for the Agent SDK when you want the built-in agentic tool loop (and Claude Code's built-in tools) without hand-rolling it.

## Agent SDK vs Claude Code CLI

The Agent SDK and the Claude Code CLI offer the **same capabilities, different interface**. The source page recommends each by use case:

| Use case                | Best choice |
| ----------------------- | ----------- |
| Interactive development | CLI         |
| CI/CD pipelines         | SDK         |
| Custom applications     | SDK         |
| One-off tasks           | CLI         |
| Production automation   | SDK         |

The CLI is the right interface for interactive, human-in-the-loop work and one-off tasks; the SDK is the right interface for programmatic, automated, and production scenarios (CI/CD, custom apps). Because they share the same engine, **many teams use both** — the CLI for daily development and the SDK for production — and workflows translate directly between them.

## Agent SDK vs Managed Agents

[Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) is a hosted REST API: Anthropic runs the agent and the sandbox, and your application sends events and streams back results. The **Agent SDK** is a library that runs the agent loop inside your own process.

|                    | Agent SDK                                                                    | Managed Agents                                                                                                |
| ------------------ | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Runs in**        | Your process, your infrastructure                                            | Anthropic-managed infrastructure                                                                              |
| **Interface**      | Python or TypeScript library                                                 | REST API                                                                                                      |
| **Agent works on** | Files on your infrastructure                                                 | A managed sandbox per session                                                                                 |
| **Session state**  | JSONL on your filesystem                                                     | Anthropic-hosted event log                                                                                    |
| **Custom tools**   | In-process Python or TypeScript functions                                    | Claude triggers the tool; you execute and return results                                                      |
| **Best for**       | Local prototyping, agents that work directly on your filesystem and services | Production agents without operating sandbox or session infrastructure, long-running and asynchronous sessions |

The axis here is *where the runtime and sandbox live*. The Agent SDK keeps the loop, the files, and session state (JSONL) on your own infrastructure; Managed Agents moves all of that to Anthropic-managed infrastructure with a per-session managed sandbox and a hosted event log. A **common path** is to prototype with the Agent SDK locally, then move to Managed Agents for production — particularly when you want production agents without operating sandbox or session infrastructure, or need long-running and asynchronous sessions.

**Source**: https://code.claude.com/docs/en/agent-sdk/overview
**Last Updated**: 2026-06-13
**Status**: Active
