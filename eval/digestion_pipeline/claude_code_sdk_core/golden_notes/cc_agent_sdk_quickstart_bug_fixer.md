---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - quickstart
keywords:
  - agent sdk quickstart
  - build a bug-fixing agent
  - query entry point
  - claudeagentoptions
  - allowed_tools
  - permission_mode acceptedits
  - find and fix bugs
  - first agent
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/quickstart
access_control_group: ["general"]
---

# Agent SDK Quickstart — Build a Bug-Fixing Agent

## Overview

This quickstart builds an AI agent on the Agent SDK that **reads your code, finds bugs, and fixes them, all without manual intervention**. You set up a project, create a file with intentional bugs, then run an agent that finds and fixes the bugs automatically. The three things you do: (1) set up a project with the Agent SDK, (2) create a file with some buggy code, (3) run an agent that finds and fixes the bugs.

The agent is driven by a single `query()` call configured with `ClaudeAgentOptions`. The SDK handles the orchestration (tool execution, context management, retries) so you just consume the streamed messages. This is what makes the Agent SDK different: Claude executes tools directly instead of asking you to implement them.

## Prerequisites

- **Node.js 18+** or **Python 3.10+**
- An **Anthropic account** (sign up at platform.claude.com)

## Setup

**1. Create a project folder.** Create a new directory and move into it. For your own projects you can run the SDK from any folder; it will have access to files in that directory and its subdirectories by default.

```bash
mkdir my-agent
cd my-agent
```

**2. Install the SDK** for your language. The TypeScript SDK bundles a native Claude Code binary for your platform as an optional dependency, so you don't need to install Claude Code separately.

```bash
# TypeScript
npm install @anthropic-ai/claude-agent-sdk
# Python (uv): uv init && uv add claude-agent-sdk
# Python (pip): python3 -m venv .venv && source .venv/bin/activate && pip install claude-agent-sdk
```

**3. Set your API key.** Get an API key from the Claude Console, then create a `.env` file in your project directory containing `ANTHROPIC_API_KEY=your-api-key`. The SDK also supports authentication via third-party API providers — Amazon Bedrock (`CLAUDE_CODE_USE_BEDROCK=1`), Claude Platform on AWS (`CLAUDE_CODE_USE_ANTHROPIC_AWS=1`), Google Vertex AI (`CLAUDE_CODE_USE_VERTEX=1`), and Microsoft Azure (`CLAUDE_CODE_USE_FOUNDRY=1`); each also needs the provider's cloud credentials configured (see [`cc_agent_sdk_install_and_auth`](cc_agent_sdk_install_and_auth.md) and the provider setup guides). Unless previously approved, Anthropic does not allow third-party developers to offer claude.ai login or rate limits for products built on the SDK — use API key authentication.

## Create a buggy file

Create `utils.py` in the `my-agent` directory with two intentional bugs for the agent to fix:

```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)


def get_user_name(user):
    return user["name"].upper()
```

The two bugs: `calculate_average([])` crashes with division by zero, and `get_user_name(None)` crashes with a TypeError.

## Build an agent that finds and fixes bugs

Create `agent.py` (Python SDK) or `agent.ts` (TypeScript). The Python version:

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage


async def main():
    # Agentic loop: streams messages as Claude works
    async for message in query(
        prompt="Review utils.py for bugs that would cause crashes. Fix any issues you find.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],  # Auto-approve these tools
            permission_mode="acceptEdits",  # Auto-approve file edits
        ),
    ):
        # Print human-readable output
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)  # Claude's reasoning
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")  # Tool being called
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")  # Final result


asyncio.run(main())
```

The code has three main parts:

1. **`query`** — the main entry point that creates the agentic loop. It returns an async iterator, so you use `async for` to stream messages as Claude works.
2. **`prompt`** — what you want Claude to do. Claude figures out which tools to use based on the task.
3. **`options`** — configuration for the agent. This example uses `allowed_tools` to pre-approve `Read`, `Edit`, and `Glob`, and `permission_mode="acceptEdits"` to auto-approve file changes. Other options include `system_prompt`, `mcpServers`, and more.

The `async for` loop keeps running as Claude thinks, calls tools, observes results, and decides what to do next. Each iteration yields a message: Claude's reasoning, a tool call, a tool result, or the final outcome. The loop ends when Claude finishes the task or hits an error. The message handling inside the loop filters for human-readable output — without filtering you'd see raw message objects including system initialization and internal state (useful for debugging but noisy otherwise). This example streams to show progress in real time; for background jobs or CI pipelines you can collect all messages at once (see [Streaming vs. single-turn mode](https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode)). The TypeScript equivalent uses `message.type === "assistant"` / `"result"` checks against `message.message?.content` instead of Python's `isinstance`.

### Run your agent

Run it: `npx tsx agent.ts` (TypeScript), `uv run agent.py` (Python uv), or `python agent.py` (Python pip, venv activated). After running, check `utils.py` — you'll see defensive code handling empty lists and null users. The agent autonomously **Read** `utils.py` to understand the code, **Analyzed** the logic and identified edge cases that would crash, and **Edited** the file to add proper error handling. If you see "API key not found", confirm `ANTHROPIC_API_KEY` is set in your `.env` or shell.

### Try other prompts

With the agent set up, try different prompts: `"Add docstrings to all functions in utils.py"`, `"Add type hints to all functions in utils.py"`, or `"Create a README.md documenting the functions in utils.py"`.

### Customize your agent

Change the `options` to modify behavior:

- **Add web search**: include `"WebSearch"` in `allowed_tools` / `allowedTools`.
- **Custom system prompt**: set `system_prompt` (Python) / `systemPrompt` (TypeScript), e.g. `"You are a senior Python developer. Always follow PEP 8 style guidelines."`.
- **Run terminal commands**: include `"Bash"` in the tool list. With `Bash` enabled, try: `"Write unit tests for utils.py, run them, and fix any failures"`.

The `acceptEdits` mode auto-approves file operations so the agent runs without interactive prompts. To prompt users for approval, use `default` mode and provide a `canUseTool` callback that collects user input. The tool ladder (read-only vs. modify vs. full automation) and the full permission-mode table are covered in [`cc_agent_sdk_tool_execution`](cc_agent_sdk_tool_execution.md) and [`cc_agent_sdk_loop_controls`](cc_agent_sdk_loop_controls.md); the streamed message loop is dissected in [`cc_agent_sdk_agent_loop`](cc_agent_sdk_agent_loop.md).

## Troubleshooting

**API error `thinking.type.enabled` is not supported for this model.** Claude Opus 4.7 replaces `thinking.type.enabled` with `thinking.type.adaptive`. Older Agent SDK versions fail with a 400 `invalid_request_error` when you select `claude-opus-4-7`. Upgrade to Agent SDK v0.2.111 or later to use Opus 4.7. See the [full troubleshooting guide](https://code.claude.com/docs/en/troubleshooting).

## Next steps

Extend the agent with [Permissions](https://code.claude.com/docs/en/agent-sdk/permissions) (control what the agent can do and when it needs approval), [Hooks](https://code.claude.com/docs/en/agent-sdk/hooks) (run custom code before or after tool calls), [Sessions](https://code.claude.com/docs/en/agent-sdk/sessions) (multi-turn agents that maintain context), [MCP servers](https://code.claude.com/docs/en/agent-sdk/mcp) (connect databases, browsers, APIs), and [Hosting](https://code.claude.com/docs/en/agent-sdk/hosting) (deploy to Docker, cloud, CI/CD). Complete examples (email assistant, research agent) are in the claude-agent-sdk-demos repo.

## Related Notes

### Related Notes (Claude Code Series)

- [Agent SDK Overview](cc_agent_sdk_overview.md) — relevance: this quickstart is the hands-on first build of the SDK that the overview defines ("Claude Code as a library"); the overview frames the same `query()` + `ClaudeAgentOptions` + `allowed_tools` entry point this tutorial walks step by step.
- [Agent SDK — The Agent Loop](cc_agent_sdk_agent_loop.md) — relevance: the tutorial's `async for message in query(...)` loop that streams Claude's reasoning, tool calls, and results is exactly the agent loop this sibling dissects (turns, messages, `max_turns`/`max_budget_usd` caps).
- [Agent SDK — Tool Execution](cc_agent_sdk_tool_execution.md) — relevance: the quickstart pre-approves `Read`/`Edit`/`Glob` via `allowed_tools` and the body explicitly defers the full tool ladder (read-only vs. modify vs. full automation) to this note.
- [Agent SDK — Loop Controls](cc_agent_sdk_loop_controls.md) — relevance: the body points here for the full permission-mode table behind `permission_mode="acceptEdits"`, and this sibling covers the loop-budget controls that bound a bug-fixing run.
- [SDK Permission Modes](cc_sdk_permission_modes.md) — relevance: the tutorial's `acceptEdits` (auto-approve edits) vs. `default` mode with a `canUseTool` callback is precisely the permission-mode behavior this note documents in detail.

### Related Notes (Out-of-Series)

- [Claude Code](../../term_dictionary/term_claude_code.md) — relevance: the quickstart builds an agent on the Agent SDK (Claude Code as a library); the product term anchors the engine the tutorial drives.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — relevance: the whole tutorial is "build an AI agent that reads your code, finds bugs, and fixes them, all without manual intervention" — the autonomous-coding-agent behavior this term names.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — relevance: the `query()` call the tutorial centers on starts the agent harness loop (the SDK handles tool execution, context, retries); the harness term explains what `query()` is driving.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — relevance: the agent autonomously calls `Read`/`Edit`/`Glob` to fix the buggy file — the function-calling/tool-use loop the tutorial demonstrates end to end.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — relevance: the tutorial uses `permission_mode="acceptEdits"` to auto-approve file edits while gating other actions — the graduated, scope-by-trust permission model this term defines.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — relevance: the "Try other prompts" / custom system-prompt steps show how prompt wording steers the agent's behavior, a direct application of prompt engineering to the SDK.
- [Tool: Strands Agents](../../tools/tool_strands_agents.md) — relevance: AWS's open-source Python agent SDK is the closest peer to the Claude Agent SDK this quickstart uses — same model-driven "let the FM pick the tools" pattern, a useful comparison point for builders choosing an SDK.
- [Tool: Cline](../../tools/tool_cline.md) — relevance: the quickstart's read-code/find-bugs/edit-file behavior is the same autonomous-coding-agent loop Cline runs in VS Code, a concrete consumer-facing instance of what the SDK lets you build programmatically.
- [Tutorial Part 4: Configuration & Permissions](../tutorials/tutorial_claude_code_04_configuration.md) — relevance: the SDK quickstart's `allowed_tools` pre-approval and `permission_mode` map onto the same tool-permission/`settings.json` configuration this Claude Code tutorial teaches hands-on.
- [Agent Composer Backend](../../../areas/code_repos/repo_agent_composer_backend.md) — relevance: a real project's agent that drives an `anthropic-api` Python SDK backend (alongside a `claude-code-cli` backend) to materialize files end-to-end — a production instance of the programmatic agent this quickstart bootstraps.

**Source**: https://code.claude.com/docs/en/agent-sdk/quickstart
**Last Updated**: 2026-06-13
**Status**: Active
