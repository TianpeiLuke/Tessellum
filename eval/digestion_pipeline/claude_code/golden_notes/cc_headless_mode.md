---
tags:
  - resource
  - documentation
  - claude_code
  - headless
  - automation
keywords:
  - headless mode
  - non-interactive mode
  - claude -p
  - print flag
  - bare mode
  - agent sdk cli
  - background tasks at exit
  - bare mode auth
topics:
  - Claude Code
  - Automation & Scheduling
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/headless
access_control_group: ["general"]
---

# Claude Code — Headless Mode (`claude -p` and `--bare`)

## Overview

Headless (non-interactive) mode runs Claude Code programmatically from the CLI by passing the `-p` (or `--print`) flag with a prompt and any [CLI options](https://code.claude.com/docs/en/cli-reference). It exposes the same tools, agent loop, and context management that power interactive Claude Code through the [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview), available as a CLI for scripts and CI/CD or as Python and TypeScript packages for full programmatic control. This note covers the operating model — what `-p` loads, the faster `--bare` variant, and how background tasks are handled at exit; the reusable invocation recipes live in the sibling note [cc_headless_examples.md](cc_headless_examples.md).

The page also carries a billing note: starting June 15, 2026, Agent SDK and `claude -p` usage on subscription plans will draw from a new monthly Agent SDK credit, separate from interactive usage limits (see [Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)). This page documents the Agent SDK via the CLI (`claude -p`); the Python and TypeScript SDK packages (structured outputs, tool approval callbacks, native message objects) are covered in the [full Agent SDK documentation](https://code.claude.com/docs/en/agent-sdk/overview).

## Basic Usage

Add the `-p` (or `--print`) flag to any `claude` command to run it non-interactively. All [CLI options](https://code.claude.com/docs/en/cli-reference) work with `-p`, including `--continue` for continuing conversations, `--allowedTools` for auto-approving tools, and `--output-format` for structured output. This example asks Claude a question about your codebase and prints the response:

```bash
claude -p "What does the auth module do?"
```

Without `--bare`, `claude -p` loads the same [context](https://code.claude.com/docs/en/how-claude-code-works#the-context-window) an interactive session would, including anything configured in the working directory or `~/.claude`.

## Start Faster with Bare Mode

Add `--bare` to reduce startup time by skipping auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md. Bare mode is useful for CI and scripts where you need the same result on every machine: a hook in a teammate's `~/.claude` or an MCP server in the project's `.mcp.json` won't run, because bare mode never reads them — only flags you pass explicitly take effect. This example runs a one-off summarize task in bare mode and pre-approves the Read tool so the call completes without a permission prompt:

```bash
claude --bare -p "Summarize this file" --allowedTools "Read"
```

In bare mode Claude has access to the Bash, file read, and file edit tools. Pass any other context you need with a flag:

| To load                 | Use                                                     |
| ----------------------- | ------------------------------------------------------- |
| System prompt additions | `--append-system-prompt`, `--append-system-prompt-file` |
| Settings                | `--settings <file-or-json>`                             |
| MCP servers             | `--mcp-config <file-or-json>`                           |
| Custom agents           | `--agents <json>`                                       |
| A plugin                | `--plugin-dir <path>`, `--plugin-url <url>`             |

Bare mode skips OAuth and keychain reads, so Anthropic authentication must come from `ANTHROPIC_API_KEY` or an `apiKeyHelper` in the JSON passed to `--settings`. Bedrock, Vertex, and Foundry use their usual provider credentials. `--bare` is the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release.

## Background Tasks at Exit

If Claude starts a [background Bash task](https://code.claude.com/docs/en/tools-reference#bash-tool-behavior) during a `claude -p` run — for example a dev server or a watch build — that task is terminated about five seconds after Claude has returned its final result and stdin has closed. The grace period lets a task that finishes right after the result still deliver its output. Before v2.1.163, a never-exiting background process would hold the `claude -p` invocation open indefinitely.

**Source**: https://code.claude.com/docs/en/headless
**Last Updated**: 2026-06-13
**Status**: Active
