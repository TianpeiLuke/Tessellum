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

## Related Notes

### Related Notes (Claude Code Series)

- [Agent SDK Overview](cc_agent_sdk_overview.md) — relevance: the parent overview defines what the Agent SDK *is* ("Claude Code as a library" with the same tools, agent loop, and context management); this note picks up where it ends, arguing *when to choose* it over the alternatives.
- [Agent SDK — Install and Authenticate](cc_agent_sdk_install_and_auth.md) — relevance: once this comparison points you to the Agent SDK, this sibling is the next step — installing the library and wiring credentials (including the Bedrock/Vertex/Azure provider paths).
- [Agent SDK — The Agent Loop](cc_agent_sdk_agent_loop.md) — relevance: the decisive Client-SDK contrast in this note is "you write the loop" vs "Claude handles the loop"; this sibling documents exactly that built-in autonomous loop (turns, `max_turns`, `max_budget_usd`) the Agent SDK ships.
- [Agent SDK — Tool Execution](cc_agent_sdk_tool_execution.md) — relevance: the "built-in tool execution" the SDK gives you over the Client SDK is detailed here — the built-in tool set and how the SDK runs requested tools, the action half of the loop this comparison hinges on.
- [Agent SDK — Provisioning and Scaling the Host](cc_sdk_hosting_provisioning_and_scaling.md) — relevance: the SDK-vs-Managed-Agents axis is "where the runtime/sandbox live"; this sibling spells out the self-hosting burden (RAM/disk, agents-per-host, tenant isolation) you take on by keeping the loop in your own process.

### Related Notes (Out-of-Series)

- [Claude Code](../../term_dictionary/term_claude_code.md) — relevance: the comparison's anchor — SDK vs Claude Code CLI is "same capabilities, different interface," so the Claude Code term defines the shared engine all the options build on.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — relevance: the decisive difference vs the Client SDK is that the Agent SDK ships the harness (built-in tool loop) while the Client SDK makes you hand-roll it; the harness term is the axis of this comparison.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — relevance: the note's central code contrast is the Client SDK's manual `while stop_reason == "tool_use"` loop vs the Agent SDK's automatic tool handling — the function-calling loop is exactly what's automated.
- [Bedrock Agents](../../term_dictionary/term_bedrock_agents.md) — relevance: the SDK-vs-Managed-Agents comparison (in-process library vs hosted, managed-sandbox REST service) parallels the managed-agent-service pattern Bedrock Agents represents, contextualizing the hosted-vs-self-hosted trade-off.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — relevance: choosing among Client SDK / Agent SDK / CLI / Managed Agents is an orchestration-architecture decision (who runs the loop, who executes tools, where state lives) — the trade-offs this term frames.
- [Sandbox](../../term_dictionary/term_sandbox.md) — relevance: the Managed-Agents column's key difference is "a managed sandbox per session" run by Anthropic vs files on your own infrastructure; sandboxing is the isolation dimension distinguishing the options.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — relevance: every option compared is a way to run autonomous coding/agentic work; the term defines the category the page is comparing delivery mechanisms for.
- [Tool: Strands Agents — Open-Source AI Agents SDK](../../tools/tool_strands_agents.md) — relevance: Strands is a direct peer to the Agent SDK — an in-process, library-style agent SDK (AWS's open-source one) you would weigh against the Agent SDK when picking "who runs the loop in your process."
- [Tool: Cline](../../tools/tool_cline.md) — relevance: Cline is an alternative autonomous coding agent (the CLI-side category this note compares the SDK against), making it a concrete instance of the "interactive development" vs "production automation" interface trade-off.
- [Hosted Agent Platform Project Overview](../../../projects/project_hosted_agent_platform.md) — relevance: a zero-setup, fully *hosted* agent platform — a real-world instance of the Managed-Agents end of this note's spectrum (Anthropic-/platform-run runtime vs the SDK's run-it-yourself library).
- [AgentCore Managed Harness [Preview]](../aws_bedrock_agentcore/bedrock_agentcore_harness.md) — relevance: the AWS analog of the Managed-Agents column — you declare what the agent does and AgentCore runs the environment, compute, tooling, and sandbox, the exact "offload the runtime" trade-off this note contrasts with the in-process SDK.

**Source**: https://code.claude.com/docs/en/agent-sdk/overview
**Last Updated**: 2026-06-13
**Status**: Active
