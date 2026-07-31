---
tags:
  - resource
  - documentation
  - claude_code
  - vs_code
  - mcp
keywords:
  - ide mcp server
  - built-in ide mcp server
  - mcp__ide__getdiagnostics
  - mcp__ide__executecode
  - selection and open-file context
  - jupyter execute quick pick
  - read deny rule
  - 127.0.0.1 random port auth token
topics:
  - Claude Code
  - VS Code
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/vs-code
access_control_group: ["general"]
---

# Claude Code — The Built-in IDE MCP Server

## Overview

When the Claude Code VS Code extension is active, it runs a **local MCP server** that the CLI connects to automatically. This server — named `ide` — is how the CLI opens diffs in VS Code's native diff viewer, reads your current selection for `@`-mentions, and (when you're working in a Jupyter notebook) asks VS Code to execute cells. It is hidden from `/mcp` because there is nothing to configure, but it exists, so if your organization uses a `PreToolUse` hook to allowlist MCP tools you need to know about it.

## Selection and Open-File Context

While connected, the CLI includes your **current editor selection** and the **path of the active file** as context on each prompt you send. The transcript shows a `⧉ Selected N lines from <file>` line when this happens. To exclude a sensitive file such as `.env`, add a `Read` deny rule for its path — a matching deny rule prevents both the selected text and the open-file notice for that file from reaching Claude.

## Transport and Authentication

The server binds to `127.0.0.1` on a random high port and is not reachable from other machines. Each extension activation generates a fresh random auth token that the CLI must present to connect. The token is written to a lock file under `~/.claude/ide/` with `0600` permissions in a `0700` directory, so only the user running VS Code can read it.

## Tools Exposed to the Model

The server hosts a dozen tools, but only two are visible to the model. The rest are internal RPC the CLI uses for its own UI — opening diffs, reading selections, saving files — and are filtered out before the tool list reaches Claude.

| Tool name (as seen by hooks) | What it does | Writes? |
| --- | --- | --- |
| `mcp__ide__getDiagnostics` | Returns language-server diagnostics — the errors and warnings in VS Code's Problems panel. Optionally scoped to one file. | No |
| `mcp__ide__executeCode` | Runs Python code in the active Jupyter notebook's kernel. See confirmation flow below. | Yes |

## Jupyter Execution Always Asks First

`mcp__ide__executeCode` can't run anything silently. On each call, the code is inserted as a new cell at the end of the active notebook, VS Code scrolls it into view, and a native Quick Pick asks you to **Execute** or **Cancel**. Cancelling — or dismissing the picker with `Esc` — returns an error to Claude and nothing runs. The tool also refuses outright when there's no active notebook, when the Jupyter extension (`ms-toolsai.jupyter`) isn't installed, or when the kernel isn't Python.

The Quick Pick confirmation is **separate from `PreToolUse` hooks**. An allowlist entry for `mcp__ide__executeCode` lets Claude *propose* running a cell; the Quick Pick inside VS Code is what lets it *actually* run.

**Source**: https://code.claude.com/docs/en/vs-code
**Last Updated**: 2026-06-13
**Status**: Active
