---
tags:
  - resource
  - documentation
  - claude_code
  - vs_code
  - setup
keywords:
  - vs code extension
  - install claude code
  - spark icon
  - vscode forks cursor
  - open vsx registry
  - get started steps
  - review changes diff
  - uninstall extension
  - fix common issues
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

# Claude Code — Install the VS Code Extension

## Overview

The Claude Code VS Code extension provides a native graphical interface for Claude Code integrated directly into the IDE, and is the recommended way to use Claude Code in VS Code. With it you can review and edit Claude's plans before accepting them, auto-accept edits as they're made, @-mention files with specific line ranges from your selection, access conversation history, and open multiple conversations in separate tabs or windows.

This note covers the setup lifecycle: the prerequisites, installing into VS Code (and forks like Cursor / Kiro via the Open VSX registry), the four-step getting-started flow (open the Spark icon panel, sign in, prompt, review diffs), the four common-issue fixes, and how to uninstall. Day-to-day prompt-box and session features live in [Prompt Box and Sessions](cc_vs_code_prompt_box_and_sessions.md), and settings / the CLI relationship in [Settings and CLI Relationship](cc_vs_code_settings_and_cli_relationship.md).

## Prerequisites

Before installing, make sure you have:

- **VS Code 1.98.0 or higher**
- **An Anthropic account**: any paid Claude subscription (Pro, Max, Team, or Enterprise) or a Claude Console account works, and no API key is required. You sign in with this account when you first open the extension. If you access Claude through a third-party provider like Amazon Bedrock or Google Vertex AI, see the third-party provider setup in [Settings and CLI Relationship](cc_vs_code_settings_and_cli_relationship.md).

The extension bundles its own copy of the CLI (command-line interface) for the chat panel. To run `claude` in VS Code's integrated terminal, you also need the standalone CLI install — see [Settings and CLI Relationship](cc_vs_code_settings_and_cli_relationship.md) for the extension-vs-CLI boundary.

## Install the extension

Click the link for your IDE to install directly:

- **Install for VS Code**: `vscode:extension/anthropic.claude-code`
- **Install for Cursor**: `cursor:extension/anthropic.claude-code`

Or in VS Code, press `Cmd+Shift+X` (Mac) or `Ctrl+Shift+X` (Windows/Linux) to open the Extensions view, search for "Claude Code", and click **Install**.

The extension also installs in other VS Code forks like Devin Desktop or Kiro. Search for "Claude Code" in the editor's Extensions view, or install from the [Open VSX registry](https://open-vsx.org/extension/Anthropic/claude-code). If your editor can't install the extension, install the CLI and run `claude` in its integrated terminal instead; the CLI works in any terminal.

If the extension doesn't appear after installation, restart VS Code or run "Developer: Reload Window" from the Command Palette.

## Get started

Once installed, you can start using Claude Code through the VS Code interface in four steps.

### Step 1 — Open the Claude Code panel

Throughout VS Code, the **Spark icon** indicates Claude Code. The quickest way to open Claude is to click the Spark icon in the **Editor Toolbar** (top-right corner of the editor); the icon only appears when you have a file open. Other ways to open Claude Code:

- **Activity Bar**: click the Spark icon in the left sidebar to open the sessions list. Click any session to open it as a full editor tab, or start a new one. This icon is always visible in the Activity Bar.
- **Command Palette**: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux), type "Claude Code", and select an option like "Open in New Tab".
- **Status Bar**: click **✱ Claude Code** in the bottom-right corner of the window. This works even when no file is open.

You can drag the Claude panel to reposition it anywhere in VS Code (see panel placement in [Prompt Box and Sessions](cc_vs_code_prompt_box_and_sessions.md)).

### Step 2 — Sign in

The first time you open the panel, a sign-in screen appears. Click **Sign in** and complete authorization in your browser. If you see **Not logged in · Please run /login** later, the extension reopens the sign-in screen automatically; if it doesn't appear, reload the window from the Command Palette with **Developer: Reload Window**.

If you have `ANTHROPIC_API_KEY` set in your shell but still see the sign-in prompt, VS Code may not have inherited your shell environment. Launch VS Code from a terminal with `code .` so it inherits your environment variables, or sign in with your Claude account instead.

After you sign in, a **Learn Claude Code** checklist appears. Work through each item by clicking **Show me**, or dismiss it with the X. To reopen it later, uncheck **Hide Onboarding** in VS Code settings under Extensions → Claude Code.

### Step 3 — Send a prompt

Ask Claude to help with your code or files, whether that's explaining how something works, debugging an issue, or making changes. Claude automatically sees your selected text. Press `Option+K` (Mac) / `Alt+K` (Windows/Linux) to also insert an @-mention reference (like `@file.ts#5-10`) into your prompt.

### Step 4 — Review changes

When Claude wants to edit a file, it shows a side-by-side comparison of the original and proposed changes, then asks for permission. You can **accept, reject, or tell Claude what to do instead**. If you edit the proposed content directly in the diff view before accepting, Claude is told that you modified it so it does not assume the file matches its original proposal. The permission modes that govern this accept/reject gate are detailed in [permission modes](https://code.claude.com/docs/en/permission-modes).

For a guided tour of the basics, run "Claude Code: Open Walkthrough" from the Command Palette.

## Fix common issues

### Extension won't install

- Ensure you have a compatible version of VS Code (1.98.0 or later).
- Check that VS Code has permission to install extensions.
- Try installing directly from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code).

### Spark icon not visible

The Spark icon appears in the **Editor Toolbar** (top-right of editor) when you have a file open. If you don't see it:

1. **Open a file**: the icon requires a file to be open; having just a folder open isn't enough.
2. **Check VS Code version**: requires 1.98.0 or higher (Help → About).
3. **Restart VS Code**: run "Developer: Reload Window" from the Command Palette.
4. **Disable conflicting extensions**: temporarily disable other AI extensions (Cline, Continue, etc.).
5. **Check workspace trust**: the extension doesn't work in Restricted Mode.

Alternatively, click "✱ Claude Code" in the **Status Bar** (bottom-right corner), which works even without a file open, or use the **Command Palette** and type "Claude Code".

### Cmd+Esc does nothing on macOS

On macOS Tahoe and later, the system Game Overlay shortcut is bound to `Cmd+Esc` by default and intercepts the keypress before it reaches VS Code. To free the shortcut: open System Settings → Keyboard → Keyboard Shortcuts → Game Controllers and clear the **Game Overlay** checkbox. Alternatively, rebind the extension to a different key via the VS Code Keyboard Shortcuts editor (`Cmd+K Cmd+S`), search for `Claude Code: Focus input`, and assign a new binding.

### Claude Code never responds

If Claude Code isn't responding to your prompts:

1. **Check your internet connection**: ensure you have a stable internet connection.
2. **Start a new conversation**: try starting a fresh conversation to see if the issue persists.
3. **Try the CLI**: run `claude` from the terminal to see if you get more detailed error messages.

If problems persist, file an issue on GitHub with details about the error.

## Uninstall the extension

To uninstall the Claude Code extension:

1. Open the Extensions view (`Cmd+Shift+X` on Mac or `Ctrl+Shift+X` on Windows/Linux).
2. Search for "Claude Code".
3. Click **Uninstall**.

To also remove extension data and reset all settings, delete the extension's storage directory for your platform. On macOS:

```bash
rm -rf ~/Library/"Application Support"/Code/User/globalStorage/anthropic.claude-code
```

On Linux:

```bash
rm -rf ~/.config/Code/User/globalStorage/anthropic.claude-code
```

On Windows, in PowerShell, the equivalent is `Remove-Item -Recurse -Force "$env:APPDATA\Code\User\globalStorage\anthropic.claude-code"`.

**Source**: https://code.claude.com/docs/en/vs-code
**Last Updated**: 2026-06-13
**Status**: Active
