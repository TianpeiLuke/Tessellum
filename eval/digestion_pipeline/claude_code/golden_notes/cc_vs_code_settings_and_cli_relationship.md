---
tags:
  - resource
  - documentation
  - claude_code
  - vs_code
  - settings
keywords:
  - vs code extension settings
  - claude code settings json
  - vs code extension vs cli
  - checkpoints rewind
  - vscode uri handler
  - run cli in vs code
  - claude mcp add
  - git worktree parallel
  - third-party providers vs code
topics:
  - Claude Code
  - VS Code
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/vs-code
access_control_group: ["general"]
---

# VS Code Extension — Settings and the CLI Relationship

## Overview

The Claude Code VS Code extension has two distinct configuration layers: **Extension settings** (VS-Code-scoped, controlling how the extension behaves inside the editor) and **Claude Code settings** in `~/.claude/settings.json` (shared with the CLI for allowed commands, environment variables, hooks, and MCP servers). The extension and CLI are two front-ends over the same product: they share conversation history and `~/.claude/settings.json`, but some features are CLI-only. This note covers the settings split, the VS Code command/shortcut surface and its `vscode://` URI handler, the extension-vs-CLI feature matrix (including checkpoints, running the CLI in the integrated terminal, sharing history, `@terminal`, and MCP), git commit/PR workflows with the `--worktree` flag, and third-party-provider setup.

## Configure settings

The extension has two types of settings:

- **Extension settings** in VS Code: control the extension's behavior within VS Code. Open with `Cmd+,` (Mac) or `Ctrl+,` (Windows/Linux), then go to Extensions → Claude Code. You can also type `/` and select **General Config** to open settings.
- **Claude Code settings** in `~/.claude/settings.json`: shared between the extension and CLI. Use for allowed commands, environment variables, hooks, and MCP servers. See [Settings](https://code.claude.com/docs/en/settings) for details.

Adding `"$schema": "https://json.schemastore.org/claude-code-settings.json"` to your `settings.json` gives autocomplete and inline validation for all available settings directly in VS Code.

### Extension settings

| Setting | Default | Description |
| --- | --- | --- |
| `useTerminal` | `false` | Launch Claude in terminal mode instead of graphical panel |
| `initialPermissionMode` | `default` | Controls approval prompts for new conversations: `default`, `plan`, `acceptEdits`, or `bypassPermissions`. See permission modes. |
| `preferredLocation` | `panel` | Where Claude opens: `sidebar` (right) or `panel` (new tab) |
| `autosave` | `true` | Auto-save files before Claude reads or writes them |
| `useCtrlEnterToSend` | `false` | Use Ctrl/Cmd+Enter instead of Enter to send prompts |
| `enableNewConversationShortcut` | `false` | Enable Cmd/Ctrl+N to start a new conversation |
| `enableReopenClosedSessionShortcut` | `true` | Use Cmd/Ctrl+Shift+T to reopen the most recently closed Claude session tab. When the last closed tab wasn't a Claude session, the shortcut runs VS Code's normal reopen-closed-editor command instead. |
| `hideOnboarding` | `false` | Hide the onboarding checklist (graduation cap icon) |
| `respectGitIgnore` | `true` | Exclude .gitignore patterns from file searches |
| `usePythonEnvironment` | `true` | Activate the workspace's Python environment when running Claude. Requires the Python extension. |
| `environmentVariables` | `[]` | Set environment variables for the Claude process. Use Claude Code settings instead for shared config. |
| `disableLoginPrompt` | `false` | Skip authentication prompts (for third-party provider setups) |
| `allowDangerouslySkipPermissions` | `false` | Adds Bypass permissions to the mode selector. Use it only in sandboxes with no internet access. |
| `claudeProcessWrapper` | - | Executable used to launch the Claude process. The bundled binary path is passed as an argument when present. Set this to a separately installed `claude` binary if the extension build doesn't include one for your platform. |

## VS Code commands and shortcuts

Open the Command Palette (`Cmd+Shift+P` on Mac or `Ctrl+Shift+P` on Windows/Linux) and type "Claude Code" to see all available VS Code commands for the extension. Some shortcuts depend on which panel is "focused" (receiving keyboard input): when the cursor is in a code file the editor is focused; when it is in Claude's prompt box Claude is focused. Use `Cmd+Esc` / `Ctrl+Esc` to toggle between them. These are VS Code commands for controlling the extension — not all built-in Claude Code commands are available in the extension.

| Command | Shortcut | Description |
| --- | --- | --- |
| Focus Input | `Cmd+Esc` (Mac) / `Ctrl+Esc` (Win/Linux) | Toggle focus between editor and Claude |
| Open in Side Bar | - | Open Claude in the left sidebar |
| Open in Terminal | - | Open Claude in terminal mode |
| Open in New Tab | `Cmd+Shift+Esc` / `Ctrl+Shift+Esc` | Open a new conversation as an editor tab |
| Open in New Window | - | Open a new conversation in a separate window |
| New Conversation | `Cmd+N` / `Ctrl+N` | Start a new conversation. Requires Claude focused and `enableNewConversationShortcut` set to `true` |
| Reopen Closed Session | `Cmd+Shift+T` / `Ctrl+Shift+T` | Reopen the most recently closed Claude session tab. Falls through to VS Code's normal reopen-closed-editor when the last closed tab wasn't a Claude session. Disable with `enableReopenClosedSessionShortcut` |
| Insert @-Mention Reference | `Option+K` (Mac) / `Alt+K` (Win/Linux) | Insert a reference to the current file and selection (requires editor focused) |
| Show Logs | - | View extension debug logs |
| Logout | - | Sign out of your Anthropic account |

### Launch a VS Code tab from other tools

The extension registers a URI handler at `vscode://anthropic.claude-code/open`. Use it to open a new Claude Code tab from your own tooling — a shell alias, browser bookmarklet, or any script that can open a URL. If VS Code isn't already running, opening the URL launches it first; if it is running, the URL opens in whichever window is currently focused. Invoke the handler with your OS's URL opener (`open` on macOS, `xdg-open` on Linux, `Start-Process` in PowerShell):

```bash theme={null}
open "vscode://anthropic.claude-code/open"
```

The handler accepts two optional query parameters: `prompt` (URL-encoded text to pre-fill in the prompt box; pre-filled but not submitted automatically) and `session` (a session ID to resume instead of starting a new conversation — the session must belong to the workspace open in VS Code; if not found, a fresh conversation starts; if already open in a tab, that tab is focused). For example, to open a tab pre-filled with "review my changes":

```text theme={null}
vscode://anthropic.claude-code/open?prompt=review%20my%20changes
```

To launch a terminal session instead of a VS Code tab, use the CLI's `claude-cli://` handler (see [Launch sessions from links](https://code.claude.com/docs/en/deep-links)).

## VS Code extension vs. Claude Code CLI

Claude Code is available as both a VS Code extension (graphical panel) and a CLI (command-line interface in the terminal). Some features are only available in the CLI. If you need a CLI-only feature, run `claude` in VS Code's integrated terminal — this requires the standalone CLI install, because the extension does not add `claude` to your PATH.

| Feature | CLI | VS Code Extension |
| --- | --- | --- |
| Commands and skills | All | Subset (type `/` to see available) |
| MCP server config | Yes | Partial (add servers via CLI; manage existing servers with `/mcp` in the chat panel) |
| Checkpoints | Yes | Yes |
| `!` bash shortcut | Yes | No |
| Tab completion | Yes | No |

### Rewind with checkpoints

The extension supports checkpoints, which track Claude's file edits and let you rewind to a previous state. Hover over any message to reveal the rewind button, then choose from three options:

- **Fork conversation from here**: start a new conversation branch from this message while keeping all code changes intact.
- **Rewind code to here**: revert file changes back to this point in the conversation while keeping the full conversation history.
- **Fork conversation and rewind code**: start a new conversation branch and revert file changes to this point.

For full details on how checkpoints work and their limitations, see [Checkpointing](https://code.claude.com/docs/en/checkpointing).

### Run CLI in VS Code

To use the CLI while staying in VS Code, open the integrated terminal (`` Ctrl+` `` on Windows/Linux or `` Cmd+` `` on Mac) and run `claude`. The CLI automatically integrates with your IDE for features like diff viewing and diagnostic sharing. Installing the extension does **not** put `claude` on your shell PATH: the extension bundles a private copy of the CLI for its chat panel, but typing `claude` in a terminal requires the standalone CLI install. Run the install once and commands like `claude mcp add` and `claude --resume` work in any terminal. If using an external terminal, run `/ide` inside Claude Code to connect it to VS Code.

### Switch between extension and CLI

The extension and CLI share the same conversation history. To continue an extension conversation in the CLI, run `claude --resume` in the terminal. This opens an interactive picker where you can search for and select your conversation.

### Include terminal output in prompts

Reference terminal output in your prompts using `@terminal:name` where `name` is the terminal's title. This lets Claude see command output, error messages, or logs without copy-pasting.

### Monitor background processes

When Claude runs long-running commands, the extension shows progress in the status bar. However, visibility for background tasks is limited compared to the CLI. For better visibility, have Claude output the command so you can run it in VS Code's integrated terminal.

### Connect to external tools with MCP

MCP servers give Claude access to external tools, databases, and APIs. To add an MCP server, open the integrated terminal and run `claude mcp add`. The example below adds GitHub's remote MCP server, which authenticates with a personal access token passed as a header:

```bash theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

Once configured, ask Claude to use the tools (e.g., "Review PR #456"). To manage MCP servers without leaving VS Code, type `/mcp` in the chat panel — the MCP management dialog lets you enable or disable servers, reconnect to a server, and manage OAuth authentication. See the [MCP documentation](https://code.claude.com/docs/en/mcp).

## Work with git

Claude Code integrates with git to help with version control workflows directly in VS Code. Ask Claude to commit changes, create pull requests, or work across branches.

### Create commits and pull requests

Claude can stage changes, write commit messages, and create pull requests based on your work:

```text theme={null}
> commit my changes with a descriptive message
> create a pr for this feature
> summarize the changes I've made to the auth module
```

When creating pull requests, Claude generates descriptions based on the actual code changes and can add context about testing or implementation decisions.

### Use git worktrees for parallel tasks

Use the `--worktree` (`-w`) flag to start Claude in an isolated worktree with its own files and branch. Each worktree maintains independent file state while sharing git history, which prevents Claude instances from interfering with each other when working on different tasks (see [Run parallel sessions with Git worktrees](https://code.claude.com/docs/en/worktrees)):

```bash theme={null}
claude --worktree feature-auth
```

## Use third-party providers

By default, Claude Code connects directly to Anthropic's API. If your organization uses Amazon Bedrock, Google Vertex AI, or Microsoft Foundry to access Claude, configure the extension to use your provider instead:

1. **Disable login prompt** — open the Disable Login Prompt setting (`vscode://settings/claudeCode.disableLoginPrompt`) and check the box, or open VS Code settings, search for "Claude Code login", and check **Disable Login Prompt**.
2. **Configure your provider** — follow the setup guide for your provider: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock), [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai), or [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry). These guides cover configuring your provider in `~/.claude/settings.json`, which ensures your settings are shared between the VS Code extension and the CLI.

**Source**: https://code.claude.com/docs/en/vs-code
**Last Updated**: 2026-06-13
**Status**: Active
