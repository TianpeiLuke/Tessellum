---
tags:
  - resource
  - documentation
  - claude_code
  - cost
  - token_reduction
keywords:
  - reduce token usage
  - context management
  - clear between tasks
  - custom compaction
  - choose the right model
  - reduce mcp overhead
  - offload to hooks and skills
  - adjust extended thinking
  - delegate to subagents
  - agent team costs
  - specific prompts
  - plan mode
topics:
  - Claude Code
  - Cost
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/costs
access_control_group: ["general"]
---

# Claude Code — Reduce Token Usage

## Overview

Claude Code's central cost argument is that **token costs scale with context size**: the more context Claude processes, the more tokens you use. Claude Code already optimizes automatically through [prompt caching](cc_prompt_caching_mechanism.md) (which reduces costs for repeated content like system prompts) and auto-compaction (which summarizes conversation history when approaching context limits), but the remaining strategies all share one goal — **keep context small and reduce per-message costs**.

This note collects the eleven strategies the `costs` page recommends, each framed as "do X to keep the window small." They range from in-session hygiene (`/clear`, custom compaction) to structural choices (right model, offload to hooks/skills, move CLAUDE.md content out) to workflow discipline (specific prompts, plan mode). Detailed configuration for the underlying features is owned by other pages and linked out; this note is the rationale-and-when of cost reduction.

## Manage context proactively

Use `/usage` to check your current token usage, or configure your status line to display it continuously.

- **Clear between tasks**: Use `/clear` to start fresh when switching to unrelated work. Stale context wastes tokens on every subsequent message. Use `/rename` before clearing so you can easily find the session later, then `/resume` to return to it.
- **Add custom compaction instructions**: `/compact Focus on code samples and API usage` tells Claude what to preserve during summarization. You can also customize compaction behavior in your CLAUDE.md:

```markdown
# Compact instructions

When you are using compact, please focus on test output and code changes
```

## Choose the right model

Sonnet handles most coding tasks well and costs less than Opus. Reserve Opus for complex architectural decisions or multi-step reasoning. Use `/model` to switch models mid-session, or set a default in `/config`. For simple subagent tasks, specify `model: haiku` in your subagent configuration. (Model selection detail is owned by [model-config](https://code.claude.com/docs/en/model-config).)

## Reduce MCP server overhead

MCP tool definitions are deferred by default, so only tool names enter context until Claude uses a specific tool. Run `/context` to see what's consuming space.

- **Prefer CLI tools when available**: Tools like `gh`, `aws`, `gcloud`, and `sentry-cli` are still more context-efficient than MCP servers because they don't add any per-tool listing. Claude can run CLI commands directly.
- **Disable unused servers**: Run `/mcp` to see configured servers and disable any you're not actively using.

(MCP tool search detail is owned by [mcp](https://code.claude.com/docs/en/mcp).)

## Install code intelligence plugins for typed languages

Code intelligence plugins give Claude precise symbol navigation instead of text-based search, reducing unnecessary file reads when exploring unfamiliar code. A single "go to definition" call replaces what might otherwise be a grep followed by reading multiple candidate files. Installed language servers also report type errors automatically after edits, so Claude catches mistakes without running a compiler. (See [discover-plugins](https://code.claude.com/docs/en/discover-plugins).)

## Offload processing to hooks and skills

Custom hooks can preprocess data before Claude sees it. Instead of Claude reading a 10,000-line log file to find errors, a hook can grep for `ERROR` and return only matching lines, reducing context from tens of thousands of tokens to hundreds.

A skill can give Claude domain knowledge so it doesn't have to explore. For example, a "codebase-overview" skill could describe your project's architecture, key directories, and naming conventions. When Claude invokes the skill, it gets this context immediately instead of spending tokens reading multiple files to understand the structure.

For example, this `PreToolUse` hook filters test output to show only failures. Add this to your `settings.json` to run the hook before every Bash command:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/filter-test-output.sh"
          }
        ]
      }
    ]
  }
}
```

The hook calls a script that checks if the command is a test runner and modifies it to show only failures (it reads the tool input from stdin via `jq`, and for `npm test`/`pytest`/`go test` rewrites the command to pipe through `grep` and `head` before returning an `updatedInput` decision). See [hooks](https://code.claude.com/docs/en/hooks) and [skills](https://code.claude.com/docs/en/skills) for the full reference.

## Move instructions from CLAUDE.md to skills

Your CLAUDE.md file is loaded into context at session start. If it contains detailed instructions for specific workflows (like PR reviews or database migrations), those tokens are present even when you're doing unrelated work. Skills load on-demand only when invoked, so moving specialized instructions into skills keeps your base context smaller. Aim to keep CLAUDE.md under 200 lines by including only essentials. (CLAUDE.md hierarchy is owned by [memory](https://code.claude.com/docs/en/memory).)

## Adjust extended thinking

Extended thinking is enabled by default because it significantly improves performance on complex planning and reasoning tasks. Thinking tokens are billed as output tokens, and the default budget can be tens of thousands of tokens per request depending on the model. For simpler tasks where deep reasoning isn't needed, you can reduce costs by:

- lowering the effort level with `/effort` or in `/model`,
- disabling thinking in `/config`, or
- on models with a fixed thinking budget, lowering the budget with `MAX_THINKING_TOKENS=8000`.

Adaptive-reasoning models ignore nonzero budgets, so use effort levels there instead. Disabling thinking is not available on Fable 5, which always uses extended thinking. (Effort-level detail is owned by [model-config](https://code.claude.com/docs/en/model-config).)

## Delegate verbose operations to subagents

Running tests, fetching documentation, or processing log files can consume significant context. Delegate these to subagents so the verbose output stays in the subagent's context while only a summary returns to your main conversation.

## Manage agent team costs

Agent teams use approximately 7x more tokens than standard sessions when teammates run in plan mode, because each teammate maintains its own context window and runs as a separate Claude instance. Keep team tasks small and self-contained to limit per-teammate token usage. (See [agent-teams](https://code.claude.com/docs/en/agent-teams) for details.)

## Write specific prompts

Vague requests like "improve this codebase" trigger broad scanning. Specific requests like "add input validation to the login function in auth.ts" let Claude work efficiently with minimal file reads.

## Work efficiently on complex tasks

For longer or more complex work, these habits help avoid wasted tokens from going down the wrong path:

- **Use plan mode for complex tasks**: Press Shift+Tab to enter plan mode before implementation. Claude explores the codebase and proposes an approach for your approval, preventing expensive re-work when the initial direction is wrong.
- **Course-correct early**: If Claude starts heading the wrong direction, press Escape to stop immediately. Use `/rewind` or double-tap Escape to restore conversation and code to a previous checkpoint.
- **Give verification targets**: Include test cases, paste screenshots, or define expected output in your prompt. When Claude can verify its own work, it catches issues before you need to request fixes.
- **Test incrementally**: Write one file, test it, then continue. This catches issues early when they're cheap to fix.

**Source**: https://code.claude.com/docs/en/costs
**Last Updated**: 2026-06-13
**Status**: Active
