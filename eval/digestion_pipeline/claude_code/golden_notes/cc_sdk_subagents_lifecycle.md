---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - subagents
keywords:
  - subagent lifecycle
  - automatic invocation
  - explicit invocation
  - dynamic agent configuration
  - detecting subagent invocation
  - parent_tool_use_id
  - resuming subagents
  - agentId
  - workflow tool
  - dynamic workflows
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/subagents
access_control_group: ["general"]
---

# SDK Subagents — Runtime Lifecycle

## Overview

Once subagents are defined (the declarative model — `AgentDefinition`, benefits, inheritance, tool restrictions — is covered in [SDK Subagents — Definition](cc_sdk_subagents_definition.md)), this note covers their **runtime lifecycle** in a Claude Agent SDK `query()` session: how a subagent gets invoked (automatically, explicitly, or via a runtime-built dynamic definition), how to detect an invocation from the streamed message stream, how to resume a subagent to continue where it left off, how to scale beyond a handful of delegated tasks using the `Workflow` tool, and how to troubleshoot common failures.

Subagents are invoked through the `Agent` tool, so `Agent` must be in `allowedTools` to auto-approve invocations without a permission prompt. Each subagent runs in its own fresh conversation and only its final message returns to the parent.

## Invoking subagents

### Automatic invocation

Claude automatically decides when to invoke subagents based on the task and each subagent's `description`. For example, if you define a `performance-optimizer` subagent with the description "Performance optimization specialist for query tuning", Claude will invoke it when your prompt mentions optimizing queries. Write clear, specific descriptions so Claude can match tasks to the right subagent.

### Explicit invocation

To guarantee Claude uses a specific subagent, mention it by name in your prompt. This bypasses automatic matching and directly invokes the named subagent:

```text theme={null}
"Use the code-reviewer agent to check the authentication module"
```

### Dynamic agent configuration

You can create agent definitions dynamically based on runtime conditions. A factory function returns an `AgentDefinition` built from runtime input — for example a security reviewer with different strictness levels that uses a more capable model (`opus`) for strict reviews and `sonnet` otherwise. Because the agent is created at query time, each request can use different settings:

```python Python theme={null}
# Factory function that returns an AgentDefinition
# This pattern lets you customize agents based on runtime conditions
def create_security_agent(security_level: str) -> AgentDefinition:
    is_strict = security_level == "strict"
    return AgentDefinition(
        description="Security code reviewer",
        # Customize the prompt based on strictness level
        prompt=f"You are a {'strict' if is_strict else 'balanced'} security reviewer...",
        tools=["Read", "Grep", "Glob"],
        # Key insight: use a more capable model for high-stakes reviews
        model="opus" if is_strict else "sonnet",
    )
```

The factory result is passed into the `agents` parameter of `query()` (`agents={"security-reviewer": create_security_agent("strict")}`), with `allowed_tools` including `Agent`. The TypeScript SDK uses the same pattern with a function returning an `AgentDefinition` object.

## Detecting subagent invocation

Subagents are invoked via the Agent tool. To detect when a subagent is invoked, check for `tool_use` blocks where `name` is `"Agent"`. Messages from within a subagent's context include a `parent_tool_use_id` field.

> The tool name was renamed from `"Task"` to `"Agent"` in Claude Code v2.1.63. Current SDK releases emit `"Agent"` in `tool_use` blocks but still use `"Task"` in the `system:init` tools list and in `result.permission_denials[].tool_name`. Checking both values in `block.name` ensures compatibility across SDK versions.

The message structure differs between SDKs. In Python, content blocks are accessed directly via `message.content`. In TypeScript, `SDKAssistantMessage` wraps the Claude API message, so content is accessed via `message.message.content`. This example iterates streamed messages, logging when a subagent is invoked and when subsequent messages originate from within that subagent's execution context:

```python Python theme={null}
# Check for subagent invocation. Match both names: older SDK
# versions emitted "Task", current versions emit "Agent".
if hasattr(message, "content") and message.content:
    for block in message.content:
        if isinstance(block, ToolUseBlock) and block.name in (
            "Task",
            "Agent",
        ):
            print(f"Subagent invoked: {block.input.get('subagent_type')}")

# Check if this message is from within a subagent's context
if hasattr(message, "parent_tool_use_id") and message.parent_tool_use_id:
    print("  (running inside subagent)")
```

## Resuming subagents

Subagents can be resumed to continue where they left off. Resumed subagents retain their full conversation history, including all previous tool calls, results, and reasoning — the subagent picks up exactly where it stopped rather than starting fresh.

When a subagent completes, the Agent tool result includes a text block containing `agentId: <id>`. The built-in `Explore` and `Plan` agents are one-shot and do not return an `agentId`, so use a custom agent or `general-purpose` when you need to resume. To resume a subagent programmatically:

1. **Capture the session ID**: Extract `session_id` from messages during the first query.
2. **Extract the agent ID**: Parse `agentId` from the Agent tool result text.
3. **Resume the session**: Pass `resume: sessionId` in the second query's options, and include the agent ID in your prompt.

> You must resume the **same session** to access the subagent's transcript. Each `query()` call starts a new session by default, so pass `resume: sessionId` to continue in the same session. When using a custom agent, pass the same agent definition in the `agents` parameter for both queries.

The two-query pattern below runs a custom `endpoint-finder` agent, captures `session_id` (from the `ResultMessage`) and `agentId` (parsed from the Agent `ToolResultBlock`) in the first query, then resumes in a second query with `resume=session_id` to ask a follow-up requiring context from the first analysis:

```python Python theme={null}
def extract_agent_id(block: ToolResultBlock) -> str | None:
    """Extract agentId from an Agent tool result's text content."""
    parts = block.content if isinstance(block.content, list) else [{"text": block.content}]
    for part in parts:
        if match := re.search(r"agentId:\s*([\w-]+)", part.get("text") or ""):
            return match.group(1)
    return None
```

The second invocation passes `resume=session_id` in `ClaudeAgentOptions` and a prompt such as `f"Resume agent {agent_id} and list the top 3 most complex endpoints"`. (Session resume-by-id is covered further in the SDK [sessions guide](https://code.claude.com/docs/en/agent-sdk/sessions).)

Subagent transcripts persist independently of the main conversation:

* **Main conversation compaction**: When the main conversation compacts, subagent transcripts are unaffected. They're stored in separate files.
* **Session persistence**: Subagent transcripts persist within their session. You can resume a subagent after restarting Claude Code by resuming the same session.
* **Automatic cleanup**: Transcripts are cleaned up based on the `cleanupPeriodDays` setting (default: 30 days).

## Scale up with dynamic workflows

Subagents work well for a few delegated tasks per turn. For runs that coordinate dozens to hundreds of agents, use the `Workflow` tool, which moves the orchestration into a script the runtime executes outside the conversation context. See [dynamic workflows](https://code.claude.com/docs/en/workflows) for how workflows differ from turn-by-turn subagent delegation.

The `Workflow` tool is available in the TypeScript Agent SDK v0.3.149 and later. Include `Workflow` in `allowedTools` to auto-approve workflow runs. The tool input and output schemas are listed in the TypeScript reference.

## Troubleshooting

### Claude not delegating to subagents

If Claude completes tasks directly instead of delegating to your subagent:

1. **Check Agent invocations are approved**: include `Agent` in `allowedTools` to auto-approve subagent calls. Without it, Agent invocations fall through to your `canUseTool` callback or, in `dontAsk` mode, are denied.
2. **Use explicit prompting**: mention the subagent by name in your prompt (for example, "Use the code-reviewer agent to...").
3. **Write a clear description**: explain exactly when the subagent should be used so Claude can match tasks appropriately.

### Filesystem-based agents not loading

Agents defined in `.claude/agents/` are loaded at startup only. If you create a new agent file while Claude Code is running, restart the session to load it.

### Windows: long prompt failures

On Windows, subagents with very long prompts may fail due to command line length limits (8191 chars). Keep prompts concise or use filesystem-based agents for complex instructions.

**Source**: https://code.claude.com/docs/en/agent-sdk/subagents
**Last Updated**: 2026-06-13
**Status**: Active
