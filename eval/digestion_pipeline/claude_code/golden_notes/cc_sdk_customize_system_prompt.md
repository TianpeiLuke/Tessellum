---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - system_prompts
keywords:
  - customize system prompt
  - claude_code preset append
  - custom system prompt
  - claude.md setting sources
  - output styles
  - excludedynamicsections prompt caching
  - combine approaches
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts
access_control_group: ["general"]
---

# Customize the Agent SDK System Prompt

## Overview

This note is the how-to for applying each of the four Agent SDK system-prompt customization methods: load a **CLAUDE.md** file via setting sources, create and activate an **output style**, `append` instructions to the `claude_code` preset, or supply a fully **custom** prompt string. It also covers the `excludeDynamicSections` option for improving prompt-cache reuse across machines, the when-to-use guidance for each method, and how to **combine** a persistent output style or CLAUDE.md with session-specific `append` text.

For the conceptual decision (minimal default vs `claude_code` preset vs custom, and the four-method comparison matrix) see the sibling note [SDK System Prompts](cc_sdk_system_prompts.md). Output styles, hooks, and Skills also shape behavior outside the system prompt; this note only covers how output styles load into the SDK.

## CLAUDE.md files for project-level instructions

CLAUDE.md files give Claude persistent project context and instructions. The SDK takes a different path for CLAUDE.md than for the other methods: it reads the file and **injects its content into the conversation as project context, not into the system prompt**, so it works with any system prompt configuration.

The SDK reads CLAUDE.md when the matching setting source is enabled:

- `'project'` loads `CLAUDE.md` or `.claude/CLAUDE.md` from the working directory.
- `'user'` loads `~/.claude/CLAUDE.md`.

Default `query()` options enable both sources, so CLAUDE.md loads automatically. If you set `settingSources` (TypeScript) / `setting_sources` (Python) explicitly, include the sources you need — CLAUDE.md loading is controlled by setting sources, **not** by the `claude_code` preset. It is not loaded if you pass an empty `settingSources` array.

CLAUDE.md is persistent across all sessions in a project, shared with your team through git, and discovered automatically without code changes. (For what to put in CLAUDE.md and how to write effective instructions, see [How Claude remembers your project](https://code.claude.com/docs/en/memory).)

### Load CLAUDE.md with the SDK

Set `settingSources` to include the level your CLAUDE.md lives at. The example loads a project-level CLAUDE.md alongside the `claude_code` preset, so Claude has both the full coding-agent prompt and your project's conventions:

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

const messages = [];

for await (const message of query({
  prompt: "Add a new React component for user profiles",
  options: {
    systemPrompt: {
      type: "preset",
      preset: "claude_code" // Use Claude Code's system prompt
    },
    settingSources: ["project"] // Loads CLAUDE.md from project
  }
})) {
  messages.push(message);
}

// Now Claude has access to your project guidelines from CLAUDE.md
```

The Python equivalent passes `setting_sources=["project"]` to `ClaudeAgentOptions`.

## Output styles for persistent configurations

Output styles are saved configurations that modify Claude's system prompt. They're stored as markdown files and can be reused across sessions and projects.

### Create an output style

An output style is a markdown file with frontmatter for metadata, followed by the prompt content. Save it to `~/.claude/output-styles/` for a user-level style available in every project, or `.claude/output-styles/` in your repository for a project-level style you can commit and share with your team.

By default, a custom output style **replaces** the `claude_code` preset's software engineering instructions with your own. To keep them and layer your instructions on top, set `keep-coding-instructions: true` in the frontmatter. Keep them when your agent is still doing software engineering work; leave them out when you're replacing the role entirely. The example defines a code-review persona that keeps the coding instructions, saved as `~/.claude/output-styles/code-reviewer.md`:

```markdown ~/.claude/output-styles/code-reviewer.md theme={null}
---
name: Code Reviewer
description: Thorough code review assistant
keep-coding-instructions: true
---

You are an expert code reviewer.

For every code submission:
1. Check for bugs and security issues
2. Evaluate performance
3. Suggest improvements
4. Rate code quality (1-10)
```

### Activate an output style

Once created, activate output styles via:

- **CLI**: run `/config` and select an output style.
- **Settings**: set `outputStyle` in `.claude/settings.local.json`.
- **TypeScript SDK**: set `outputStyle` inside the inline `settings` object passed to `query()`, or point `settings` at a settings file that sets it. `outputStyle` is **not** a top-level `Options` field.

The **Python SDK does not** have an option to select an output style programmatically. For code-only deployments where you can't write to `.claude/settings.local.json`, use `append` or a custom prompt string instead.

Output styles are loaded when you include `settingSources: ['user']` or `settingSources: ['project']` (TypeScript) / `setting_sources=["user"]` or `setting_sources=["project"]` (Python) in your options.

## Append to the `claude_code` preset

Use the `claude_code` preset with an `append` property to add your custom instructions while preserving all built-in functionality (tool guidance, safety rules, coding conventions):

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

const messages = [];

for await (const message of query({
  prompt: "Help me write a Python function to calculate fibonacci numbers",
  options: {
    systemPrompt: {
      type: "preset",
      preset: "claude_code",
      append: "Always include detailed docstrings and type hints in Python code."
    }
  }
})) {
  messages.push(message);
  if (message.type === "assistant") {
    console.log(message.message.content);
  }
}
```

The Python form passes `system_prompt={"type": "preset", "preset": "claude_code", "append": "..."}` to `ClaudeAgentOptions`.

### Improve prompt caching across users and machines

By default, two sessions that use the same `claude_code` preset and `append` text still cannot share a prompt cache entry if they run from different working directories. The preset embeds per-session context in the system prompt ahead of your `append` text — the working directory, whether it's a git repository, the platform, the active shell, the OS version, and auto-memory paths. Any difference in that context produces a different system prompt and a cache miss. (CLAUDE.md content doesn't affect the system prompt cache because the SDK injects it into the conversation, not the system prompt.)

To make the system prompt identical across sessions, set `excludeDynamicSections: true` in TypeScript or `"exclude_dynamic_sections": True` in Python. The per-session context moves into the first user message, leaving only the static preset and your `append` text in the system prompt, so identical configurations share a cache entry across users and machines:

```python Python theme={null}
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Triage the open issues in this repo",
    options=ClaudeAgentOptions(
        system_prompt={
            "type": "preset",
            "preset": "claude_code",
            "append": "You operate Acme's internal triage workflow. Label issues by component and severity.",
            "exclude_dynamic_sections": True,
        },
    ),
):
    ...
```

`excludeDynamicSections` requires `@anthropic-ai/claude-agent-sdk` v0.2.98 or later, or `claude-agent-sdk` v0.1.58 or later for Python. It applies only to the **preset object form** and has no effect when `systemPrompt` is a string.

**Tradeoffs:** the working directory, the git-repo flag, the platform, the active shell, the OS version, and auto-memory paths still reach Claude, but as part of the first user message rather than the system prompt. Instructions in the user message carry marginally less weight than the same text in the system prompt, so Claude may rely on them less strongly when reasoning about the current directory or auto-memory paths. Enable this option when cross-session cache reuse matters more than maximally authoritative environment context. For the equivalent flag in non-interactive CLI mode, see [`--exclude-dynamic-system-prompt-sections`](https://code.claude.com/docs/en/cli-reference).

## Custom system prompts

Provide a custom string as `systemPrompt` to replace the default entirely with your own instructions:

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

const customPrompt = `You are a Python coding specialist.
Follow these guidelines:
- Write clean, well-documented code
- Use type hints for all functions
- Include comprehensive docstrings
- Prefer functional programming patterns when appropriate
- Always explain your code choices`;

const messages = [];

for await (const message of query({
  prompt: "Create a data processing pipeline",
  options: {
    systemPrompt: customPrompt
  }
})) {
  messages.push(message);
  if (message.type === "assistant") {
    console.log(message.message.content);
  }
}
```

The Python form passes `system_prompt=custom_prompt` to `ClaudeAgentOptions`. With a custom string the SDK sends only what you provide, so you take responsibility for any tool guidance and safety rules your agent needs.

## Use cases and best practices

- **When to use CLAUDE.md** — for instructions that should apply to every session in a project regardless of which system prompt the session uses: coding standards, common commands, architecture context, and team conventions. CLAUDE.md is committed to your repository, so it stays in sync with the code it describes. It loads when the `project` setting source is enabled (the default); if you set sources explicitly, include `'project'`.
- **When to use output styles** — for personas you want to reuse across the CLI and SDK without changing application code. Best for persistent behavior changes across sessions, team-shared configurations, specialized assistants (code reviewer, data scientist, DevOps), and complex prompt modifications that need versioning.
- **When to use `systemPrompt` with append** — when the `claude_code` preset already fits your product and you only need to layer in extra instructions, keeping the preset's tool guidance, safety rules, and coding conventions. Best for adding coding standards, customizing output formatting, adding domain-specific knowledge, modifying response verbosity, and enhancing default behavior without losing tool instructions.
- **When to use custom `systemPrompt`** — when your agent's surface, identity, or permission model differs from Claude Code's. You define the full instruction set, including tool guidance and safety rules. Best for complete control over behavior, specialized single-session tasks, testing new prompt strategies, situations where default tools aren't needed, and building specialized agents with unique behavior.

## Combine approaches

These methods compose. A persistent output style or CLAUDE.md sets the long-lived behavior, and `append` layers session-specific instructions on top without touching the saved configuration.

### Combine an output style with session-specific additions

The example assumes a Code Reviewer output style is already active. The `append` block layers session-specific focus areas on top of the persona, so a single review session can prioritize OAuth and token storage without changing the saved output style:

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

// Assuming "Code Reviewer" output style is active (via /config or settings)
// Add session-specific focus areas
const messages = [];

for await (const message of query({
  prompt: "Review this authentication module",
  options: {
    systemPrompt: {
      type: "preset",
      preset: "claude_code",
      append: `
        For this review, prioritize:
        - OAuth 2.0 compliance
        - Token storage security
        - Session management
      `
    }
  }
})) {
  messages.push(message);
}
```

The Python form passes the same preset-plus-`append` object to `ClaudeAgentOptions`.

**Source**: https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts
**Last Updated**: 2026-06-13
**Status**: Active
