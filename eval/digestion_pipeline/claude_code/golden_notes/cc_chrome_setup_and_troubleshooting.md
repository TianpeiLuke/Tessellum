---
tags:
  - resource
  - documentation
  - claude_code
  - chrome
  - troubleshooting
keywords:
  - chrome setup
  - claude --chrome
  - enable chrome by default
  - site permissions
  - native messaging host
  - extension not detected
  - service worker idle
  - eaddrinuse
topics:
  - Claude Code
  - Chrome Integration
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/chrome
access_control_group: ["general"]
---

# Claude Code — Chrome Setup and Troubleshooting

## Overview

This is the install, enable, and troubleshooting procedure for Claude Code's Chrome integration — the browser-automation surface whose capabilities and example workflows are documented on the [Chrome integration page](https://code.claude.com/docs/en/chrome). Setup requires the right browser, a recent extension, a recent Claude Code, and a direct Anthropic plan; you then launch with `claude --chrome` (or `/chrome` in-session), optionally enable Chrome by default (a context trade-off), and control which sites Claude may touch through extension-level permissions.

Most failures trace to the connection between Claude Code and the extension — the **native messaging host** configuration file or the extension's **service worker**. The troubleshooting section walks the detection failures, an unresponsive browser, idle-connection drops during long sessions, Windows-specific named-pipe and host errors, and the common error messages with their fixes.

## Prerequisites

Before using Claude Code with Chrome, you need:

- [Google Chrome](https://www.google.com/chrome/) or [Microsoft Edge](https://www.microsoft.com/edge) browser
- [Claude in Chrome extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) version **1.0.36 or higher**, available in the Chrome Web Store for both browsers
- [Claude Code](https://code.claude.com/docs/en/quickstart) version **2.0.73 or higher**
- A direct Anthropic plan (Pro, Max, Team, or Enterprise)

Chrome integration is **not** available through third-party providers like Amazon Bedrock, Google Cloud Vertex AI, or Microsoft Foundry. If you access Claude exclusively through a third-party provider, you need a separate claude.ai account to use this feature. (The integration is in beta and currently works only with Google Chrome and Microsoft Edge — not Brave, Arc, or other Chromium-based browsers; WSL is also unsupported.)

## Get started in the CLI

Start Claude Code with the `--chrome` flag:

```bash
claude --chrome
```

You can also enable Chrome from within an existing session by running `/chrome`. Run `/chrome` at any time to check the connection status, manage permissions, reconnect the extension, or choose which connected browser to use. If more than one browser is connected when a browser action starts, Claude prompts you to pick one.

For VS Code, browser automation is available through the [VS Code extension](https://code.claude.com/docs/en/vs-code) instead.

### Enable Chrome by default

To avoid passing `--chrome` each session, run `/chrome` and select **"Enabled by default"**. In the VS Code extension, Chrome is available whenever the Chrome extension is installed — no additional flag is needed.

Enabling Chrome by default in the CLI **increases context usage** since browser tools are always loaded. If you notice increased context consumption, disable this setting and use `--chrome` only when needed.

### Manage site permissions

Site-level permissions are inherited from the Chrome extension. Manage permissions in the **Chrome extension settings** to control which sites Claude can browse, click, and type on.

## Troubleshooting

### Extension not detected

If Claude Code's setup-issues line lists `chrome`:

1. Verify the Chrome extension is installed and enabled in `chrome://extensions`
2. Verify Claude Code is up to date by running `claude --version`
3. Check that Chrome is running
4. Run `/chrome` and select **"Reconnect extension"** to re-establish the connection
5. If the issue persists, restart both Claude Code and Chrome

The first time you enable Chrome integration, Claude Code installs a **native messaging host configuration file**. Chrome reads this file on startup, so if the extension isn't detected on your first attempt, restart Chrome to pick up the new configuration.

If the connection still fails, verify the host configuration file (`com.anthropic.claude_code_browser_extension.json`) exists at the platform-specific path:

- **Chrome — macOS**: `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/`
- **Chrome — Linux**: `~/.config/google-chrome/NativeMessagingHosts/`
- **Chrome — Windows**: check `HKCU\Software\Google\Chrome\NativeMessagingHosts\` in the Windows Registry
- **Edge — macOS**: `~/Library/Application Support/Microsoft Edge/NativeMessagingHosts/`
- **Edge — Linux**: `~/.config/microsoft-edge/NativeMessagingHosts/`
- **Edge — Windows**: check `HKCU\Software\Microsoft\Edge\NativeMessagingHosts\` in the Windows Registry

### Browser not responding

If Claude's browser commands stop working:

1. Check if a **modal dialog** (alert, confirm, prompt) is blocking the page. JavaScript dialogs block browser events and prevent Claude from receiving commands. Dismiss the dialog manually, then tell Claude to continue.
2. Ask Claude to create a new tab and try again.
3. Restart the Chrome extension by disabling and re-enabling it in `chrome://extensions`.

### Connection drops during long sessions

The Chrome extension's **service worker** can go idle during extended sessions, which breaks the connection. If browser tools stop working after a period of inactivity, run `/chrome` and select **"Reconnect extension"**.

### Windows-specific issues

On Windows, you may encounter:

- **Named pipe conflicts (EADDRINUSE)**: if another process is using the same named pipe, restart Claude Code. Close any other Claude Code sessions that might be using Chrome.
- **Native messaging host errors**: if the native messaging host crashes on startup, try reinstalling Claude Code to regenerate the host configuration.

### Common error messages

These are the most frequently encountered errors and how to resolve them:

| Error | Cause | Fix |
| --- | --- | --- |
| "Browser extension is not connected" | Native messaging host cannot reach the extension | Restart Chrome and Claude Code, then run `/chrome` to reconnect |
| "Extension not detected" | Chrome extension is not installed or is disabled | Install or enable the extension in `chrome://extensions` |
| "No tab available" | Claude tried to act before a tab was ready | Ask Claude to create a new tab and retry |
| "Receiving end does not exist" | Extension service worker went idle | Run `/chrome` and select "Reconnect extension" |

**Source**: https://code.claude.com/docs/en/chrome
**Last Updated**: 2026-06-13
**Status**: Active
