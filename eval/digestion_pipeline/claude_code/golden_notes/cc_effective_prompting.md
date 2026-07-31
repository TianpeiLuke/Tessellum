---
tags:
  - resource
  - documentation
  - claude_code
  - prompting
  - context
keywords:
  - effective prompting
  - provide specific context
  - scope the task
  - reference existing patterns
  - describe the symptom
  - rich content
  - reference files with @
  - paste images
  - pipe data into claude
  - mcp resource reference
topics:
  - Claude Code
  - Prompting
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/best-practices
access_control_group: ["general"]
---

# Claude Code — Effective Prompting and Rich Content

## Overview

The core claim of this note is that **the more precise your instructions, the fewer corrections you'll need**: Claude can infer intent, but it can't read your mind, so reference specific files, mention constraints, and point to example patterns. Effective prompting has two halves — saying the right thing (specific context) and supplying the right inputs (rich content). The first half is four strategies for turning a vague ask into a precise one; the second is the set of mechanisms (`@` references, pasted images, URLs, piped data) for loading the data Claude needs to act on. Vague prompts still have their place when you're exploring and can afford to course-correct.

## Provide specific context in your prompts

> **Tip (source):** The more precise your instructions, the fewer corrections you'll need.

Claude can infer intent, but it can't read your mind. Reference specific files, mention constraints, and point to example patterns. The docs give four before/after strategies:

- **Scope the task.** Specify which file, what scenario, and testing preferences. Before: *"add tests for foo.py"* → After: *"write a test for foo.py covering the edge case where the user is logged out. avoid mocks."*
- **Point to sources.** Direct Claude to the source that can answer a question. Before: *"why does ExecutionFactory have such a weird api?"* → After: *"look through ExecutionFactory's git history and summarize how its api came to be"*
- **Reference existing patterns.** Point Claude to patterns in your codebase. Before: *"add a calendar widget"* → After: *"look at how existing widgets are implemented on the home page to understand the patterns. HotDogWidget.php is a good example. follow the pattern to implement a new calendar widget that lets the user select a month and paginate forwards/backwards to pick a year. build from scratch without libraries other than the ones already used in the codebase."*
- **Describe the symptom.** Provide the symptom, the likely location, and what "fixed" looks like. Before: *"fix the login bug"* → After: *"users report that login fails after session timeout. check the auth flow in src/auth/, especially token refresh. write a failing test that reproduces the issue, then fix it"*

### The vague-prompt exception

Specificity is not always the goal. Per the source: vague prompts can be useful when you're exploring and can afford to course-correct. A prompt like `"what would you improve in this file?"` can surface things you wouldn't have thought to ask about.

## Provide rich content

> **Tip (source):** Use `@` to reference files, paste screenshots/images, or pipe data directly.

Precise wording is only half of the input; the other half is feeding Claude the actual data. The docs list several ways to provide rich content:

- **Reference files with `@`** instead of describing where code lives. Claude reads the file before responding.
- **Paste images directly.** Copy/paste or drag and drop images into the prompt.
- **Give URLs** for documentation and API references. Use `/permissions` to allowlist frequently-used domains.
- **Pipe in data** by running `cat error.log | claude` to send file contents directly.
- **Let Claude fetch what it needs.** Tell Claude to pull context itself using Bash commands, MCP tools, or by reading files.

### `@` reference semantics (files, directories, MCP resources)

The `@` syntax lets you include content without waiting for Claude to read it. There are three forms, each loading something different into the conversation:

```text
Explain the logic in @src/utils/auth.js
```

A single-file reference includes the **full content of the file** in the conversation.

```text
What's the structure of @src/components?
```

A directory reference provides a **directory listing with file information** (file listings, not contents).

```text
Show me the data from @github:repos/owner/repo/issues
```

An MCP-resource reference (`@server:resource` form) fetches data from connected MCP servers. Per source notes on `@`: file paths can be relative or absolute; `@` file references also add `CLAUDE.md` in the file's directory and parent directories to context; and you can reference multiple files in a single message (for example, `"@file1.js and @file2.js"`).

### Working with images

Images are a rich-content input where text descriptions would be unclear or cumbersome. There are three ways to add an image to the conversation: (1) drag and drop an image into the Claude Code window; (2) copy an image and paste it into the CLI with `ctrl+v` (do not use `cmd+v`); or (3) provide an image path, e.g. *"Analyze this image: /path/to/your/image.png"*. From there you can ask Claude to analyze the image (*"Describe the UI elements in this screenshot"*), use it for context (*"Here's a screenshot of the error. What's causing it?"*), or get code suggestions from visual content (*"Generate CSS to match this design mockup"*). Image analysis works with diagrams, screenshots, mockups, and more, and you can work with multiple images in a conversation. When Claude references an image (for example, `[Image #1]`), `Cmd+Click` (Mac) or `Ctrl+Click` (Windows/Linux) the link to open it in your default viewer.

**Source**: https://code.claude.com/docs/en/best-practices
**Last Updated**: 2026-06-13
**Status**: Active
