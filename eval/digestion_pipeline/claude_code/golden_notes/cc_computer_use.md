---
tags:
  - resource
  - documentation
  - claude_code
  - computer_use
  - surfaces
keywords:
  - computer use
  - claude code cli
  - macos screen control
  - computer-use mcp server
  - precision ladder
  - accessibility screen recording
  - gui task automation
  - research preview
topics:
  - Claude Code
  - Computer Use
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/computer-use
access_control_group: ["general"]
---

# Claude Code — Computer Use (CLI)

## Overview

**Computer use** lets Claude open apps, control your screen, and work on your machine the way you would, driven from the Claude Code CLI. In one conversation Claude can compile a Swift app, launch it, click through every button, and screenshot the result — the same session where it wrote the code. It is a **research preview on macOS** that requires a **Pro or Max plan** (not available on Team or Enterprise), Claude Code **v2.1.85 or later**, and an **interactive session** — it is not available in non-interactive mode with the `-p` flag.

This note covers what CLI computer use is, when Claude reaches for it, how to enable it, how it runs on your screen, and how the CLI differs from the Desktop surface. The per-app approval flow and the safety/trust-boundary argument are covered in the sibling note [Computer Use Safety](cc_computer_use_safety.md). For the Desktop app on macOS or Windows, see [computer use in Desktop](https://code.claude.com/docs/en/desktop).

## What you can do with computer use

Computer use handles tasks that require a GUI — anything you'd normally have to leave the terminal and do by hand:

- **Build and validate native apps** — ask Claude to build a macOS menu bar app; Claude writes the Swift, compiles it, launches it, and clicks through every control to verify it works before you ever open it.
- **End-to-end UI testing** — point Claude at a local Electron app and say "test the onboarding flow"; Claude opens the app, clicks through signup, and screenshots each step. No Playwright config, no test harness.
- **Debug visual and layout issues** — tell Claude "the modal is clipping on small windows"; Claude resizes the window, reproduces the bug, screenshots it, patches the CSS, and verifies the fix. Claude sees what you see.
- **Drive GUI-only tools** — interact with design tools, hardware control panels, the iOS Simulator, or proprietary apps that have no CLI or API.

## When computer use applies

Claude has several ways to interact with an app or service. Computer use is the **broadest and slowest**, so Claude tries the most precise tool first — a precision ladder:

1. If you have an [MCP server](https://code.claude.com/docs/en/mcp) for the service, Claude uses that.
2. If the task is a shell command, Claude uses Bash.
3. If the task is browser work and you have [Claude in Chrome](https://code.claude.com/docs/en/chrome) set up, Claude uses that.
4. If none of those apply, Claude uses computer use.

Screen control is reserved for things nothing else can reach: native apps, simulators, and tools without an API.

## Enable computer use

Computer use is available as a **built-in MCP server called `computer-use`**. It is off by default until you enable it.

1. **Open the MCP menu** — in an interactive Claude Code session, run `/mcp` and find `computer-use` in the server list. It shows as disabled.
2. **Enable the server** — select `computer-use` and choose **Enable**. The setting persists per project, so you only do this once for each project where you want computer use.
3. **Grant macOS permissions** — the first time Claude tries to use your computer, you'll see a prompt to grant two macOS permissions: **Accessibility** (lets Claude click, type, and scroll) and **Screen Recording** (lets Claude see what's on your screen). The prompt includes links to open the relevant System Settings pane. Grant both, then select **Try again** in the prompt. macOS may require you to restart Claude Code after granting Screen Recording.

After setup, ask Claude to do something that needs the GUI, e.g. "Build the app target, launch it, and click through each tab to make sure nothing crashes. Screenshot any error states you find."

> Enabling the `computer-use` server does not grant access to every app on your machine — Claude requests per-app approval per session. That approval flow is covered in [Computer Use Safety](cc_computer_use_safety.md).

## How Claude works on your screen

Understanding the flow helps you anticipate what Claude will do and how to intervene.

### One session at a time

Computer use holds a **machine-wide lock** while active. If another Claude Code session is already using your computer, new attempts fail with a message telling you which session holds the lock. Finish or exit that session first.

### Apps are hidden while Claude works

When Claude starts controlling your screen, other visible apps are **hidden** so Claude interacts with only the approved apps. Your **terminal window stays visible and is excluded from screenshots**, so you can watch the session and Claude never sees its own output. When Claude finishes the turn, hidden apps are restored automatically.

### Screenshots are downscaled automatically

Claude Code **downscales every screenshot** before sending it to the model, so you don't need to lower your display resolution or resize windows on Retina or other high-resolution displays. A 16-inch MacBook Pro at native Retina resolution captures at 3456×2234 and downscales to roughly 1372×887, preserving aspect ratio. There is no setting to change the target size. If on-screen text or controls are too small for Claude to read after downscaling, increase their size in the app rather than changing your display resolution.

### Stop at any time

When Claude acquires the lock, a macOS notification appears: "Claude is using your computer · press Esc to stop." Press `Esc` anywhere to abort the current action immediately, or press `Ctrl+C` in the terminal. Either way, Claude releases the lock, unhides your apps, and returns control to you. A second notification appears when Claude is done.

## Example workflows

These examples show common ways to combine computer use with coding tasks.

**Validate a native build** — after making changes to a macOS or iOS app, have Claude compile and verify in one pass:

```text theme={null}
Build the MenuBarStats target, launch it, open the preferences window,
and verify the interval slider updates the label. Screenshot the
preferences window when you're done.
```

Claude runs `xcodebuild`, launches the app, interacts with the UI, and reports what it finds.

**Reproduce a layout bug** — when a visual bug only appears at certain window sizes, let Claude find it:

```text theme={null}
The settings modal clips its footer on narrow windows. Resize the app
window down until you can reproduce it, screenshot the clipped state,
then check the CSS for the modal container.
```

Claude resizes the window, captures the broken state, and reads the relevant stylesheets.

**Test a simulator flow** — drive the iOS Simulator without writing XCTest:

```text theme={null}
Open the iOS Simulator, launch the app, tap through the onboarding
screens, and tell me if any screen takes more than a second to load.
```

Claude controls the simulator the same way you would with a mouse.

## Differences from the Desktop app

The CLI and Desktop surfaces share the same computer use engine, with a few differences:

| Feature | Desktop | CLI |
| :--- | :--- | :--- |
| Platforms | macOS and Windows | macOS only |
| Enable | Toggle in **Settings > General** (under **Desktop app**) | Enable `computer-use` in `/mcp` |
| Denied apps list | Configurable in Settings | Not yet available |
| Auto-unhide toggle | Optional | Always on |
| Dispatch integration | Dispatch-spawned sessions can use computer use | Not applicable |

See [computer use in Desktop](https://code.claude.com/docs/en/desktop) for the graphical settings page.

## Troubleshooting

- **"Computer use is in use by another Claude session"** — another Claude Code session holds the lock. Finish the task in that session or exit it. If the other session crashed, the lock is released automatically when Claude detects the process is no longer running.
- **macOS permissions prompt keeps reappearing** — macOS sometimes requires a restart of the requesting process after you grant Screen Recording. Quit Claude Code completely and start a new session. If the prompt persists, open **System Settings > Privacy & Security > Screen Recording** and confirm your terminal app is listed and enabled.
- **`computer-use` doesn't appear in `/mcp`** — the server only appears on eligible setups. Check that: you're on **macOS** (CLI computer use is not available on Linux or Windows — on Windows, use computer use in Desktop instead); you're running Claude Code **v2.1.85 or later** (`claude --version`); you're on a **Pro or Max plan** (`/status`); you're **authenticated through claude.ai** (it is not available with third-party providers like Amazon Bedrock, Google Cloud Vertex AI, or Microsoft Foundry — if you access Claude exclusively through a third-party provider, you need a separate claude.ai account); and you're in an **interactive session** (not the `-p` flag).

**Source**: https://code.claude.com/docs/en/computer-use
**Last Updated**: 2026-06-13
**Status**: Active
