---
tags:
  - resource
  - documentation
  - claude_code
  - vs_code
  - prompt_box
keywords:
  - vs code prompt box
  - permission mode indicator
  - command menu
  - context indicator
  - extended thinking toggle
  - at-mention files folders
  - resume cloud sessions
  - manage plugins ui
  - browser tasks chrome
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

# Claude Code in VS Code — Prompt Box, Sessions, Plugins, and Chrome

## Overview

This note covers the day-to-day operating surface of the Claude Code VS Code extension: the **prompt box** and its features (permission modes, command menu, context indicator, extended thinking, multi-line input), how to **reference files and folders** with @-mentions, how to **resume** past local conversations and cloud sessions from Claude.ai, the **account & usage** dialog, customizing the panel **layout**, running **multiple conversations**, switching to **terminal mode**, the **plugin management** UI, and connecting Claude to **Chrome** with `@browser`. Install/getting-started is covered in [`cc_vs_code_extension`](cc_vs_code_extension.md); settings, CLI relationship, and git are in [`cc_vs_code_settings_and_cli_relationship`](cc_vs_code_settings_and_cli_relationship.md).

## Use the prompt box

The prompt box supports several features:

- **Permission modes**: click the mode indicator at the bottom of the prompt box to switch modes. In normal mode, Claude asks permission before each action. In Plan mode, Claude describes what it will do and waits for approval before making changes; VS Code automatically opens the plan as a full markdown document where you can add inline comments to give feedback before Claude begins. In auto-accept mode, Claude makes edits without asking. Set the default in VS Code settings under `claudeCode.initialPermissionMode`. (Permission-mode concepts are documented at https://code.claude.com/docs/en/permission-modes.)
- **Command menu**: click `/` or type `/` to open the command menu. Options include attaching files, switching models, toggling extended thinking, viewing plan usage (`/usage`), and starting a Remote Control session (`/remote-control`). The Customize section provides access to MCP servers, hooks, memory, permissions, and plugins. Items with a terminal icon open in the integrated terminal.
- **Context indicator**: the prompt box shows how much of Claude's context window you're using. Claude automatically compacts when needed, or you can run `/compact` manually.
- **Extended thinking**: lets Claude spend more time reasoning through complex problems. Toggle it on via the command menu (`/`). Claude's reasoning appears in the conversation as collapsed blocks: click a block to read it, or press `Ctrl+O` to expand or collapse every thinking block in the session. (See extended thinking details at https://code.claude.com/docs/en/model-config#extended-thinking.)
- **Multi-line input**: press `Shift+Enter` to add a new line without sending. This also works in the "Other" free-text input of question dialogs.

### Reference files and folders

Use @-mentions to give Claude context about specific files or folders. When you type `@` followed by a file or folder name, Claude reads that content and can answer questions about it or make changes to it. Claude Code supports fuzzy matching, so you can type partial names to find what you need:

```text
> Explain the logic in @auth (fuzzy matches auth.js, AuthService.ts, etc.)
> What's in @src/components/ (include a trailing slash for folders)
```

For large PDFs, you can ask Claude to read specific pages instead of the whole file: a single page, a range like pages 1-10, or an open-ended range like page 3 onward.

When you select text in the editor, Claude can see your highlighted code automatically. The prompt box footer shows how many lines are selected. Press `Option+K` (Mac) / `Alt+K` (Windows/Linux) to insert an @-mention with the file path and line numbers (e.g., `@app.ts#5-10`). Click the selection indicator to toggle whether Claude can see your highlighted text — the eye-slash icon means the selection is hidden from Claude.

You can also hold `Shift` while dragging files into the prompt box to add them as attachments. Click the X on any attachment to remove it from context.

### Resume past conversations

Click the **Session history** button at the top of the Claude Code panel to access your conversation history. You can search by keyword or browse by time (Today, Yesterday, Last 7 days, etc.). Click any conversation to resume it with the full message history. New sessions receive AI-generated titles based on your first message. Hover over a session to reveal rename and remove actions: rename to give it a descriptive title, or remove to delete it from the list. (For more on resuming sessions, see https://code.claude.com/docs/en/sessions.)

### Resume cloud sessions from Claude.ai

If you use Claude Code on the web, you can resume those cloud sessions directly in VS Code. This requires signing in with **Claude.ai Subscription**, not Anthropic Console.

1. **Open session history** — click the **Session history** button at the top of the Claude Code panel.
2. **Select the Remote tab** — the dialog shows two tabs: Local and Remote. Click **Remote** to see sessions from claude.ai.
3. **Select a session to resume** — browse or search your cloud sessions. Click any session to download it and continue the conversation locally.

Only web sessions started with a GitHub repository appear in the Remote tab. Resuming loads the conversation history locally; changes are not synced back to claude.ai. (Cloud/web sessions are documented at https://code.claude.com/docs/en/claude-code-on-the-web.)

### Check account and usage

Run `/usage` from the command menu to open the Account & usage dialog. It shows your signed-in account, plan, and usage bars for the current session and week with how long until each limit resets.

The dialog also breaks down what is contributing to your plan limits. It flags behaviors that account for 10% or more of recent usage, such as cache misses, long context, and subagent-heavy or highly parallel sessions, each with a tip to reduce it. Attribution tables show how much usage came from each skill, subagent, plugin, and MCP server. Requires Claude Code v2.1.174 or later.

Use the Day and Week toggle to switch between the last 24 hours and the last 7 days. The figures are approximate and computed from local sessions on this machine, so usage from other devices or claude.ai is not included.

## Customize your workflow

Once you're up and running, you can reposition the Claude panel, run multiple sessions, or switch to terminal mode.

### Choose where Claude lives

You can drag the Claude panel to reposition it anywhere in VS Code. Grab the panel's tab or title bar and drag it to:

- **Secondary sidebar**: the right side of the window. Keeps Claude visible while you code.
- **Primary sidebar**: the left sidebar with icons for Explorer, Search, etc.
- **Editor area**: opens Claude as a tab alongside your files. Useful for side tasks.

Use the sidebar for your main Claude session and open additional tabs for side tasks. Claude remembers your preferred location. The Activity Bar sessions list icon is separate from the Claude panel: the sessions list is always visible in the Activity Bar, while the Claude panel icon only appears there when the panel is docked to the left sidebar.

### Run multiple conversations

Use **Open in New Tab** or **Open in New Window** from the Command Palette to start additional conversations. Each conversation maintains its own history and context, allowing you to work on different tasks in parallel.

When using tabs, a small colored dot on the spark icon indicates status: blue means a permission request is pending, orange means Claude finished while the tab was hidden.

### Switch to terminal mode

By default, the extension opens a graphical chat panel. If you prefer the CLI-style interface, open the Use Terminal setting (`vscode://settings/claudeCode.useTerminal`) and check the box.

You can also open VS Code settings (`Cmd+,` on Mac or `Ctrl+,` on Windows/Linux), go to Extensions → Claude Code, and check **Use Terminal**.

## Manage plugins

The VS Code extension includes a graphical interface for installing and managing plugins. Type `/plugins` in the prompt box to open the **Manage plugins** interface. (Plugin concepts are documented at https://code.claude.com/docs/en/plugins.)

### Install plugins

The plugin dialog shows two tabs: **Plugins** and **Marketplaces**.

In the Plugins tab:

- **Installed plugins** appear at the top with toggle switches to enable or disable them
- **Available plugins** from your configured marketplaces appear below
- Search to filter plugins by name or description
- Click **Install** on any available plugin

When you install a plugin, choose the installation scope:

- **Install for you**: available in all your projects (user scope)
- **Install for this project**: shared with project collaborators (project scope)
- **Install locally**: only for you, only in this repository (local scope)

### Manage marketplaces

Switch to the **Marketplaces** tab to add or remove plugin sources:

- Enter a GitHub repo, URL, or local path to add a new marketplace
- Click the refresh icon to update a marketplace's plugin list
- Click the trash icon to remove a marketplace

After making changes, a banner prompts you to restart Claude Code to apply the updates.

Plugin management in VS Code uses the same CLI commands under the hood. Plugins and marketplaces you configure in the extension are also available in the CLI, and vice versa.

## Automate browser tasks with Chrome

Connect Claude to your Chrome browser to test web apps, debug with console logs, and automate browser workflows without leaving VS Code. This requires the Claude in Chrome extension version 1.0.36 or higher.

Type `@browser` in the prompt box followed by what you want Claude to do:

```text
@browser go to localhost:3000 and check the console for errors
```

You can also open the attachment menu to select specific browser tools like opening a new tab or reading page content.

Claude opens new tabs for browser tasks and shares your browser's login state, so it can access any site you're already signed into. (For setup, the full list of capabilities, and troubleshooting, see https://code.claude.com/docs/en/chrome.)

**Source**: https://code.claude.com/docs/en/vs-code
**Last Updated**: 2026-06-13
**Status**: Active
