---
tags:
  - resource
  - documentation
  - claude_code
  - output_styles
  - customization
keywords:
  - output style
  - system prompt modification
  - role tone format
  - built-in output styles
  - keep-coding-instructions
  - explanatory learning proactive
  - claude code customization
topics:
  - Claude Code
  - Output Styles
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/output-styles
access_control_group: ["general"]
---

# Claude Code — Output Styles

## Overview

An **output style** changes *how* Claude Code responds, not *what* it knows: it modifies the system prompt to set Claude's **role, tone, and output format**. Reach for one when you keep re-prompting for the same voice or format every turn, or when you want Claude to act as something other than a software engineer. A custom output style adds your instructions to the system prompt and lets you choose whether to keep Claude Code's built-in software engineering instructions — keep them when you are changing how Claude communicates but still coding (e.g. always answering with a diagram), and leave them out when Claude is not doing software engineering at all (e.g. a writing assistant or data analyst).

For instructions about your project, conventions, or codebase, use [CLAUDE.md](https://code.claude.com/docs/en/memory) instead — that is a different layer than an output style.

## Built-in output styles

Claude Code's **Default** output style is the existing system prompt, designed to help you complete software engineering tasks efficiently. There are three additional built-in styles:

- **Proactive** — Claude executes immediately, makes reasonable assumptions instead of pausing for routine decisions, and prefers action over planning. This is stronger autonomous-execution guidance than [auto mode](https://code.claude.com/docs/en/permission-modes) applies, and it works without changing your permission mode, so you still see permission prompts before tools run.
- **Explanatory** — provides educational "Insights" in between helping you complete software engineering tasks, helping you understand implementation choices and codebase patterns.
- **Learning** — a collaborative, learn-by-doing mode where Claude not only shares "Insights" while coding but also asks you to contribute small, strategic pieces of code yourself; Claude Code adds `TODO(human)` markers in your code for you to implement.

## Change your output style

Run `/config` and select **Output style** to pick a style from a menu. Your selection is saved to `.claude/settings.local.json` at the [local project level](https://code.claude.com/docs/en/settings).

> The standalone `/output-style` command was deprecated in v2.1.73 and removed in v2.1.91. Use `/config` or edit the `outputStyle` setting directly.

To set a style without the menu, edit the `outputStyle` field directly in a settings file:

```json theme={null}
{
  "outputStyle": "Explanatory"
}
```

Output style is part of the system prompt, which Claude Code reads once at session start. Changes take effect after `/clear` or a new session. See [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching) for what an output style change does to the cache.

## Create a custom output style

A custom output style is a Markdown file: frontmatter for metadata, then the instructions to add to the system prompt.

1. **Create a Markdown file** at one of three levels (the file name becomes the style name unless you set `name` in the frontmatter):
   - User: `~/.claude/output-styles`
   - Project: `.claude/output-styles`
   - Managed policy: `.claude/output-styles` inside the [managed settings directory](https://code.claude.com/docs/en/settings)
2. **Add frontmatter and instructions.** Decide whether to keep Claude Code's software engineering instructions: set `keep-coding-instructions: true` if you are changing how Claude communicates but still want it coding the same way; leave it out if Claude will not be doing software engineering. This example leads every explanation with a diagram while keeping Claude's coding behavior:

   ```markdown theme={null}
   ---
   name: Diagrams first
   description: Lead every explanation with a diagram
   keep-coding-instructions: true
   ---

   When explaining code, architecture, or data flow, start with a Mermaid diagram showing the structure, then explain in prose.

   ## Diagram conventions

   Use `flowchart TD` for control flow and `sequenceDiagram` for request paths. Keep diagrams under 15 nodes.
   ```
3. **Switch to your style.** Run `/config` and select your style under **Output style**. It takes effect after `/clear` or the next time you start a session.

[Plugins](https://code.claude.com/docs/en/plugins-reference) can also ship output styles in an `output-styles/` directory.

### Frontmatter

Output style files support these frontmatter fields:

| Frontmatter | Purpose | Default |
| :--- | :--- | :--- |
| `name` | Name of the output style, if not the file name | Inherits from file name |
| `description` | Description of the output style, shown in the `/config` picker | None |
| `keep-coding-instructions` | Keep Claude Code's built-in software engineering instructions | `false` |
| `force-for-plugin` | Plugin output styles only: apply this style automatically whenever the plugin is enabled, without requiring users to select it. Overrides the user's `outputStyle` setting. If multiple enabled plugins set this, Claude Code uses the first one loaded. | `false` |

## How output styles work

Output styles directly modify Claude Code's system prompt:

- All output styles have their own custom instructions added to the **end** of the system prompt.
- All output styles trigger reminders for Claude to adhere to the output style instructions during the conversation.
- Custom output styles **leave out** Claude Code's built-in software engineering instructions (such as how to scope changes, write comments, and verify work) unless `keep-coding-instructions` is set to `true`.

Token usage depends on the style. Adding instructions to the system prompt increases input tokens, though prompt caching reduces this cost after the first request in a session. The built-in Explanatory and Learning styles produce longer responses than Default by design, which increases output tokens. For custom styles, output token usage depends on what your instructions tell Claude to produce.

## Comparisons to related features

Several features customize how Claude Code behaves. Output styles modify the system prompt directly and apply to every response; the others add instructions without changing the default system prompt, or scope them to a specific task.

| Feature | How it works | Use it when |
| :--- | :--- | :--- |
| Output styles | Modifies the system prompt | You want a different role, tone, or default response format every turn |
| [CLAUDE.md](https://code.claude.com/docs/en/memory) | Adds a user message after the system prompt | Claude should always know your project conventions and codebase context |
| `--append-system-prompt` | Appends to the system prompt without removing anything | You want a one-off addition for a single invocation |
| [Agents](https://code.claude.com/docs/en/sub-agents) | Runs a subagent with its own system prompt, model, and tools | You want a separately scoped helper for a focused task |
| [Skills](https://code.claude.com/docs/en/skills) | Loads task-specific instructions when invoked or relevant | You have a reusable workflow |

**Source**: https://code.claude.com/docs/en/output-styles
**Last Updated**: 2026-06-13
**Status**: Active
