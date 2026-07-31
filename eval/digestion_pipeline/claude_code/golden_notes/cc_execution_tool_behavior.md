---
tags:
  - resource
  - documentation
  - claude_code
  - tools
  - execution_tools
keywords:
  - agent tool behavior
  - bash tool persistence
  - monitor tool background watch
  - powershell tool enablement
  - webfetch lossy extraction
  - websearch backend
  - lsp code intelligence
  - background subagent permissions
topics:
  - Claude Code
  - Tools
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/tools-reference
access_control_group: ["general"]
---

# Claude Code — Execution, Web & Agent Tool Behavior

## Overview

This note documents the per-tool semantics for Claude Code's execution, web, and agent built-in tools: **Agent**, **Bash**, **Monitor**, **PowerShell**, **WebFetch**, **WebSearch**, and **LSP**. These are the tools that run commands, spawn subagents, watch background processes, and reach the network — as opposed to the file/search tools (Read, Edit, Write, NotebookEdit, Glob, Grep) covered in the sibling note `cc_file_tool_behavior`.

Each tool has behavior worth knowing before relying on it: Bash carries over working directory but not environment variables; the Agent tool runs a subagent in an isolated context window with inheritance rules for which tools it gets; WebFetch is lossy by design because it runs an extraction prompt instead of returning the raw page. For the full catalog with permission-required flags and the shared `ToolName(specifier)` rule format, see the sibling note `cc_tools_catalog`.

## Agent tool behavior

The Agent tool spawns a [subagent](https://code.claude.com/docs/en/sub-agents) in a **separate context window**. The subagent works through its task autonomously, then returns a single text result to the parent conversation. The parent does not see the subagent's intermediate tool calls or outputs, only that final result. To cap how many turns a subagent runs, set `maxTurns` in the subagent definition.

The same Agent tool also launches **forked subagents** when fork mode is enabled. A fork inherits the full parent conversation instead of starting fresh, always runs in the background, and still surfaces permission prompts in your terminal. The rest of this behavior describes named subagents.

Which tools a named subagent can use depends on the `tools` and `disallowedTools` fields in the [subagent definition](https://code.claude.com/docs/en/sub-agents):

- **Neither field set**: the subagent inherits every tool available to the parent.
- **`tools` only**: the subagent gets only the listed tools.
- **`disallowedTools` only**: the subagent gets every parent tool except the listed ones.
- **Both set**: `disallowedTools` takes precedence — a tool listed in both is removed.

Launching the subagent does not itself prompt for permission. The subagent's own tool calls are checked against your permission rules as it runs:

- **Foreground subagents** show the same permission prompts you would see in the main conversation, at the moment each tool call happens.
- **Background subagents** do not show prompts. They run with the permissions already granted in the session and **auto-deny** any tool call that would otherwise prompt. After a denial, the subagent keeps going without that tool.

To limit what a subagent can reach in the first place, narrow its `tools` field, leave Bash off the list, or set deny rules in your settings. The subagent frontmatter fields are owned by the subagents reference (sub-plan B10A).

## Bash tool behavior

The Bash tool runs each command in a **separate process** with this persistence behavior:

- When Claude runs `cd` in the main session, the new working directory **carries over** to later Bash commands as long as it stays inside the project directory or an additional working directory added with `--add-dir`, `/add-dir`, or `additionalDirectories` in settings. Subagent sessions never carry over working directory changes.
  - If `cd` lands outside those directories, Claude Code resets to the project directory and appends `Shell cwd was reset to <dir>` to the tool result.
  - To disable this carry-over so every Bash command starts in the project directory, set `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1`.
- **Environment variables do not persist.** An `export` in one command will not be available in the next.
- **Aliases and shell functions** defined in your shell startup file are available. At session start, Claude Code sources `~/.zshrc`, `~/.bashrc`, or `~/.profile` depending on your shell, captures the resulting aliases, functions, and shell options, and applies them to every Bash command.

To make environment variables persist across Bash commands, set `CLAUDE_ENV_FILE` to a shell script before launching Claude Code, or use a SessionStart hook to populate it dynamically. Activate your virtualenv or conda environment before launching Claude Code.

Two limits bound each command:

- **Timeout**: two minutes by default. Claude can request up to 10 minutes per command with the `timeout` parameter. Override the default and ceiling with `BASH_DEFAULT_TIMEOUT_MS` and `BASH_MAX_TIMEOUT_MS`.
- **Output length**: 30,000 characters by default. When a command produces more, Claude Code saves the full output to a file in the session directory and gives Claude the file path plus a short preview from the start; Claude reads or searches that file when it needs the rest. Raise the limit with `BASH_MAX_OUTPUT_LENGTH`, up to a hard ceiling of 150,000 characters.

For long-running processes such as dev servers or watch builds, Claude can set `run_in_background: true` to start the command as a background task and continue working while it runs. List and stop background tasks with `/tasks`.

## Monitor tool

The Monitor tool (requires Claude Code v2.1.98 or later) lets Claude watch something in the background and react when it changes, without pausing the conversation. Ask Claude to:

- Tail a log file and flag errors as they appear
- Poll a PR or CI job and report when its status changes
- Watch a directory for file changes
- Track output from any long-running script you point it at

Claude writes a small script for the watch, runs it in the background, and receives each output line as it arrives. You keep working in the same session and Claude interjects when an event lands. Stop a monitor by asking Claude to cancel it or by ending the session.

Monitor uses the **same permission rules as Bash**, so `allow` and `deny` patterns set for Bash apply here too. It is **not available** on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry. It is also not available when `DISABLE_TELEMETRY` or `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` is set.

Plugins can declare monitors that start automatically when the plugin is active, instead of asking Claude to start them.

## PowerShell tool

The PowerShell tool lets Claude run PowerShell commands natively. On Windows, this means commands run in PowerShell instead of routing through Git Bash. On Windows without Git Bash, the tool is enabled automatically. On Windows with Git Bash installed, the tool is rolling out progressively. On Linux, macOS, and WSL, the tool is opt-in.

### Enable the PowerShell tool

Set `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` in your environment or in `settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_USE_POWERSHELL_TOOL": "1"
  }
}
```

On Windows, set the variable to `0` to opt out of the rollout. On Linux, macOS, and WSL, the tool requires PowerShell 7 or later: install `pwsh` and ensure it is on your `PATH`. On Windows, Claude Code auto-detects `pwsh.exe` for PowerShell 7+ with a fallback to `powershell.exe` for PowerShell 5.1. When the tool is enabled, Claude treats PowerShell as the primary shell; the Bash tool remains available for POSIX scripts when Git Bash is installed.

Claude Code spawns PowerShell with `-ExecutionPolicy Bypass` at **process scope only**, so `.ps1` scripts and module imports work on default Windows installs without changing the machine's policy. Process-scope bypass does not override Group Policy `MachinePolicy` or `UserPolicy`, so enterprise lockdowns still apply. To respect the machine's effective execution policy instead, set `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1`.

### Shell selection in settings, hooks, and skills

Three additional settings control where PowerShell is used:

- `"defaultShell": "powershell"` in `settings.json`: routes interactive `!` commands through PowerShell. Requires the PowerShell tool to be enabled.
- `"shell": "powershell"` on individual command hooks: runs that hook in PowerShell. Hooks spawn PowerShell directly, so this works regardless of `CLAUDE_CODE_USE_POWERSHELL_TOOL`.
- `shell: powershell` in skill frontmatter: runs `` !`command` `` blocks in PowerShell. Requires the PowerShell tool to be enabled.

The same main-session working-directory reset behavior described under Bash applies to PowerShell commands, including the `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` environment variable.

### Preview limitations

During the preview, the PowerShell tool has these known limitations:

- PowerShell profiles are not loaded.
- On Windows, sandboxing is not supported.

## WebFetch tool behavior

WebFetch takes a URL and a prompt describing what to extract. It fetches the page, converts the response to Markdown when the server returns HTML, and runs the prompt against the content using a **small, fast model**. For most fetches, Claude receives that model's answer, not the raw page. The conversion step is not configurable.

This makes WebFetch **lossy by design**. The extraction prompt determines what reaches Claude, so a result saying a page does not mention something may only mean the prompt did not ask about it. Ask Claude to fetch again with a more specific prompt, or use `curl` via Bash for the unprocessed page.

A few behaviors shape the response Claude receives:

- HTTP URLs are automatically upgraded to HTTPS.
- Large pages are truncated to a fixed character limit before processing.
- Responses are cached for 15 minutes, so repeated fetches of the same URL return quickly.
- When a URL redirects to a different host, WebFetch returns a text result naming the original URL and the redirect target instead of following it; Claude then fetches the new URL with a second WebFetch call.

In the default and `acceptEdits` permission modes, WebFetch **prompts the first time it reaches a new domain**, except for a built-in set of preapproved documentation domains that fetch without a prompt. To allow another domain in advance, add a permission rule like `WebFetch(domain:example.com)`. The `auto` and `bypassPermissions` permission modes skip the prompt entirely. An explicit `WebFetch(domain:...)` rule in `deny`, `ask`, or `allow` takes precedence over the preapproved set, so you can block a preapproved domain or require a prompt for it.

WebFetch sets a `User-Agent` header beginning with `Claude-User`, and an `Accept` header that prefers Markdown over HTML so servers that support content negotiation can return Markdown directly. Sandbox network rules are configured separately, so a domain you want a sandboxed process to reach still needs an explicit sandbox permission rule.

## WebSearch tool behavior

WebSearch runs a query against Anthropic's web search backend and returns result **titles and URLs**. It does not fetch the result pages; to read a page Claude finds, it follows up with WebFetch.

The tool may issue up to **eight backend searches per call**, refining the search internally before returning results. Claude can scope results with `allowed_domains` to include only certain hosts, or `blocked_domains` to exclude them — the two lists cannot be combined in a single call. The search backend is not configurable; to search with a different provider, add an MCP server that exposes a search tool.

WebSearch permission rules take **no specifier**: a bare `WebSearch` entry in `allow` or `deny` is the only form. WebSearch is available on the Claude API and Microsoft Foundry. On Google Cloud Vertex AI it works with Claude 4 models (including Opus, Sonnet, and Haiku). Amazon Bedrock does not expose the server-side web search tool.

## LSP tool behavior

The LSP tool gives Claude **code intelligence** from a running language server. After each file edit, it automatically reports type errors and warnings so Claude can fix issues without a separate build step. Claude can also call it directly to navigate code:

- Jump to a symbol's definition
- Find all references to a symbol
- Get type information at a position
- List symbols in a file
- Search for a symbol by name across the workspace
- Find implementations of an interface
- Trace call hierarchies

The tool is **inactive until you install a code intelligence plugin** for your language. The plugin bundles the language server configuration, and you install the server binary separately.

**Source**: https://code.claude.com/docs/en/tools-reference
**Last Updated**: 2026-06-13
**Status**: Active
