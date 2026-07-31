---
tags:
  - resource
  - documentation
  - claude_code
  - tools
keywords:
  - built-in tools
  - tool categories
  - file operations
  - search execution web
  - code intelligence
  - tools make claude code agentic
  - claude chooses tools
topics:
  - Claude Code
  - Built-in Tools
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/how-claude-code-works
access_control_group: ["general"]
---

# Claude Code — Built-in Tools

## Overview

Tools are what make Claude Code agentic. Without tools, Claude can only respond with text; with tools, Claude can act — read code, edit files, run commands, search the web, and interact with external services. Each tool use returns information that feeds back into the loop, informing Claude's next decision. The built-in tools generally fall into **five categories**, each representing a different kind of agency. They are the foundation that can be extended with additional capabilities.

## The Five Tool Categories

The built-in tools generally fall into five categories, each representing a different kind of agency:

- **File operations** — Read files, edit code, create new files, rename and reorganize.
- **Search** — Find files by pattern, search content with regex, explore codebases.
- **Execution** — Run shell commands, start servers, run tests, use git.
- **Web** — Search the web, fetch documentation, look up error messages.
- **Code intelligence** — See type errors and warnings after edits, jump to definitions, find references (requires code intelligence plugins).

These are the primary capabilities. Claude also has tools for spawning subagents, asking you questions, and other orchestration tasks. For the complete list, see the [tools reference](https://code.claude.com/docs/en/tools-reference) (digested separately under sub-plan B03B).

## How Claude Uses Tools

Claude chooses which tools to use based on your prompt and what it learns along the way. Each tool use gives Claude new information that informs the next step — this is the agentic loop in action. For example, when you say "fix the failing tests," Claude might run the test suite to see what's failing, read the error output, search for the relevant source files, read those files to understand the code, edit the files to fix the issue, and run the tests again to verify.

## Extending the Base Capabilities

The built-in tools are the foundation. You can extend what Claude knows with skills, connect to external services with MCP, automate workflows with hooks, and offload tasks to subagents. These extensions form a layer on top of the core agentic loop (see [Extending Claude Code](cc_extending_claude_code.md)).

**Source**: https://code.claude.com/docs/en/how-claude-code-works
**Last Updated**: 2026-06-13
**Status**: Active
