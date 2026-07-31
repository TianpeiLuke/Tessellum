---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - subagents
keywords:
  - agentdefinition
  - agents parameter
  - subagent definition
  - context isolation
  - tool restrictions
  - programmatic subagents
  - what subagents inherit
  - general-purpose subagent
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/subagents
access_control_group: ["general"]
---

# SDK Subagents — Declarative Model

## Overview

A **subagent** is a separate agent instance the main agent spawns to handle a focused subtask — isolating context, running analyses in parallel, and applying specialized instructions without bloating the main agent's prompt. In the Claude Agent SDK you declare subagents through the `agents` parameter on your `query()` options. This note covers the *declarative* surface: how a subagent is defined (the three creation paths and the `AgentDefinition` field set), why you would use one (the four benefits), and what a defined subagent does and does not inherit from its parent. The runtime side — invoking, detecting, resuming, scaling, and troubleshooting — lives in [SDK Subagents — Lifecycle](cc_sdk_subagents_lifecycle.md).

Claude decides whether to invoke a defined subagent based on its `description` field, so descriptions should clearly explain when the subagent should be used; you can also request one explicitly by name in your prompt.

## Three ways to create subagents

You can create subagents in three ways:

- **Programmatically** — use the `agents` parameter in your `query()` options. This is the recommended approach for SDK applications and is the focus of the page.
- **Filesystem-based** — define agents as markdown files in `.claude/agents/` directories (see the [Claude Code subagents documentation](https://code.claude.com/docs/en/sub-agents) for this approach). **Programmatically defined agents take precedence over filesystem-based agents with the same name.**
- **Built-in `general-purpose`** — Claude can invoke the built-in `general-purpose` subagent at any time via the Agent tool without you defining anything, which is useful for delegating research or exploration without creating a specialized agent.

For any of these, include `Agent` in `allowedTools` so subagent invocations auto-approve without a permission prompt.

## Benefits of using subagents

- **Context isolation** — each subagent runs in its own fresh conversation. Intermediate tool calls and results stay inside the subagent; only its final message returns to the parent. A `research-assistant` subagent can explore dozens of files without any of that content accumulating in the main conversation — the parent receives a concise summary, not every file read.
- **Parallelization** — multiple subagents can run concurrently, so independent subtasks finish in the time of the slowest one rather than the sum of all of them (e.g. running `style-checker`, `security-scanner`, and `test-coverage` simultaneously during a code review).
- **Specialized instructions and knowledge** — each subagent can have a tailored system prompt with specific expertise, best practices, and constraints (e.g. a `database-migration` subagent loaded with SQL best practices and rollback strategies that would be noise in the main agent's instructions).
- **Tool restrictions** — subagents can be limited to specific tools, reducing the risk of unintended actions (e.g. a `doc-reviewer` with only Read and Grep so it can analyze but never accidentally modify files).

## Programmatic definition

Define subagents directly in code via the `agents` parameter, mapping each subagent name to an `AgentDefinition`. Claude invokes subagents through the `Agent` tool, so include `Agent` in `allowedTools` to auto-approve invocations. This example defines a read-only `code-reviewer` plus a `test-runner` with `Bash` access (TypeScript form is equivalent, using `allowedTools` / `agents`):

```python Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition


async def main():
    async for message in query(
        prompt="Review the authentication module for security issues",
        options=ClaudeAgentOptions(
            # Auto-approve these tools, including Agent for subagent invocation
            allowed_tools=["Read", "Grep", "Glob", "Agent"],
            agents={
                "code-reviewer": AgentDefinition(
                    # description tells Claude when to use this subagent
                    description="Expert code review specialist. Use for quality, security, and maintainability reviews.",
                    # prompt defines the subagent's behavior and expertise
                    prompt="""You are a code review specialist with expertise in security, performance, and best practices.

When reviewing code:
- Identify security vulnerabilities
- Check for performance issues
- Verify adherence to coding standards
- Suggest specific improvements

Be thorough but concise in your feedback.""",
                    # tools restricts what the subagent can do (read-only here)
                    tools=["Read", "Grep", "Glob"],
                    # model overrides the default model for this subagent
                    model="sonnet",
                ),
                "test-runner": AgentDefinition(
                    description="Runs and analyzes test suites. Use for test execution and coverage analysis.",
                    prompt="""You are a test execution specialist. Run tests and provide clear analysis of results.

Focus on:
- Running test commands
- Analyzing test output
- Identifying failing tests
- Suggesting fixes for failures""",
                    # Bash access lets this subagent run test commands
                    tools=["Bash", "Read", "Grep"],
                ),
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)


asyncio.run(main())
```

## AgentDefinition configuration

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `description` | `string` | Yes | Natural language description of when to use this agent |
| `prompt` | `string` | Yes | The agent's system prompt defining its role and behavior |
| `tools` | `string[]` | No | Array of allowed tool names. If omitted, inherits all tools |
| `disallowedTools` | `string[]` | No | Array of tool names to remove from the agent's tool set |
| `model` | `string` | No | Model override for this agent. Accepts an alias such as `'fable'`, `'opus'`, `'sonnet'`, `'haiku'`, `'inherit'`, or a full model ID. Defaults to main model if omitted |
| `skills` | `string[]` | No | List of skill names to preload into the agent's context at startup. Unlisted skills remain invocable through the Skill tool |
| `memory` | `'user' \| 'project' \| 'local'` | No | Memory source for this agent |
| `mcpServers` | `(string \| object)[]` | No | MCP servers available to this agent, by name or inline config |
| `initialPrompt` | `string` | No | Auto-submitted as the first user turn when this agent runs as the main thread agent. Ignored when the agent is invoked as a subagent |
| `maxTurns` | `number` | No | Maximum number of agentic turns before the agent stops |
| `background` | `boolean` | No | Run this agent as a non-blocking background task when invoked |
| `effort` | `'low' \| 'medium' \| 'high' \| 'xhigh' \| 'max' \| number` | No | Reasoning effort level for this agent |
| `permissionMode` | `PermissionMode` | No | Permission mode for tool execution within this agent |

In the Python SDK, these field names use camelCase to match the wire format; see the [`AgentDefinition` reference](https://code.claude.com/docs/en/agent-sdk/python#agentdefinition) for details.

As of Claude Code v2.1.172, subagents can spawn their own subagents: a background subagent five levels below the main agent cannot spawn further subagents, while foreground subagents can spawn at any depth. To prevent a subagent from spawning others, omit `Agent` from its `tools` array or add it to `disallowedTools`.

## What subagents inherit

A subagent's context window starts fresh (no parent conversation) but is not empty. **The only channel from parent to subagent is the Agent tool's prompt string**, so include any file paths, error messages, or decisions the subagent needs directly in that prompt.

| The subagent receives | The subagent does not receive |
| :--- | :--- |
| Its own system prompt (`AgentDefinition.prompt`) and the Agent tool's prompt | The parent's conversation history or tool results |
| Project CLAUDE.md (loaded via `settingSources`) | Preloaded skill content, unless listed in `AgentDefinition.skills` |
| Tool definitions (inherited from parent, or the subset in `tools`) | The parent's system prompt |

The parent receives the subagent's final message verbatim as the Agent tool result, but may summarize it in its own response. To preserve subagent output verbatim in the user-facing response, include an instruction to do so in the prompt or `systemPrompt` option passed to the **main** `query()` call.

## Tool restrictions

Subagents can have restricted tool access via the `tools` field:

- **Omit the field** — the agent inherits all available tools (default).
- **Specify tools** — the agent can only use the listed tools.

A read-only analysis agent, for example, is defined with `tools=["Read", "Grep", "Glob"]` so it can examine code but cannot modify files or run commands (no `Edit`, `Write`, or `Bash`).

### Common tool combinations

| Use case | Tools | Description |
| :--- | :--- | :--- |
| Read-only analysis | `Read`, `Grep`, `Glob` | Can examine code but not modify or execute |
| Test execution | `Bash`, `Read`, `Grep` | Can run commands and analyze output |
| Code modification | `Read`, `Edit`, `Write`, `Grep`, `Glob` | Full read/write access without command execution |
| Full access | All tools | Inherits all tools from parent (omit `tools` field) |

Once defined, subagents are invoked, detected, and resumed at runtime — see [SDK Subagents — Lifecycle](cc_sdk_subagents_lifecycle.md). For scaling beyond a few delegated tasks per turn, the `Workflow` tool moves orchestration into a script (see [dynamic workflows](https://code.claude.com/docs/en/workflows)).

**Source**: https://code.claude.com/docs/en/agent-sdk/subagents
**Last Updated**: 2026-06-13
**Status**: Active
