---
tags:
  - resource
  - documentation
  - claude_code
  - permissions
  - permission_modes
keywords:
  - permission modes
  - default acceptedits plan auto dontask bypasspermissions
  - shift+tab cycle
  - permission-mode flag
  - defaultmode setting
  - modes set the baseline
  - protected paths
  - per-interface mode switching
topics:
  - Claude Code
  - Permissions
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/permission-modes
access_control_group: ["general"]
---

# Claude Code — Permission Modes Overview

## Overview

When Claude wants to edit a file, run a shell command, or make a network request, it pauses and asks you to approve the action. **Permission modes** control how often that pause happens. The mode you pick shapes the flow of a session: `default` mode has you review each action as it comes, while looser modes let Claude work in longer uninterrupted stretches and report back when done. Pick more oversight for sensitive work, or fewer interruptions when you trust the direction.

There are six modes — `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, and `bypassPermissions` — forming a spectrum from full oversight to full autonomy. **Modes set the baseline**; [permission rules](https://code.claude.com/docs/en/permissions) layer on top to pre-approve or block specific tools. This note covers the mode set and how to switch modes per interface; per-mode behavior detail lives in [cc_permission_modes_detail](cc_permission_modes_detail.md) and the auto-mode classifier in [cc_auto_mode](cc_auto_mode.md).

## Available modes

Each mode makes a different tradeoff between convenience and oversight. The table below shows what Claude can do without a permission prompt in each mode.

| Mode | What runs without asking | Best for |
| :--- | :--- | :--- |
| `default` | Reads only | Getting started, sensitive work |
| `acceptEdits` | Reads, file edits, and common filesystem commands (`mkdir`, `touch`, `mv`, `cp`, etc.) | Iterating on code you're reviewing |
| `plan` | Reads only | Exploring a codebase before changing it |
| `auto` | Everything, with background safety checks | Long tasks, reducing prompt fatigue |
| `dontAsk` | Only pre-approved tools | Locked-down CI and scripts |
| `bypassPermissions` | Everything | Isolated containers and VMs only |

In every mode except `bypassPermissions`, writes to [protected paths](cc_permission_modes_detail.md) are never auto-approved, guarding repository state and Claude's own configuration against accidental corruption.

Modes set the baseline. Layer [permission rules](https://code.claude.com/docs/en/permissions) on top to pre-approve or block specific tools. **Deny rules and explicit ask rules apply in every mode, including `bypassPermissions`.** Allow rules have no effect in that mode because everything else is already approved.

## Switch permission modes

You can switch modes mid-session, at startup, or as a persistent default. The mode is set through these controls, **not by asking Claude in chat**. The control surface differs per interface.

### CLI

**During a session**: press `Shift+Tab` to cycle `default` → `acceptEdits` → `plan`. The current mode appears in the status bar. Not every mode is in the default cycle:

- `auto`: appears when your account meets the [auto mode requirements](cc_auto_mode.md); cycling to auto shows an opt-in prompt until you accept it, or select **No, don't ask again** to remove auto from the cycle.
- `bypassPermissions`: appears after you start with `--permission-mode bypassPermissions`, `--dangerously-skip-permissions`, or `--allow-dangerously-skip-permissions`; the `--allow-` variant adds the mode to the cycle without activating it.
- `dontAsk`: never appears in the cycle; set it with `--permission-mode dontAsk`.

Enabled optional modes slot in after `plan`, with `bypassPermissions` first and `auto` last. If you have both enabled, you will cycle through `bypassPermissions` on the way to `auto`.

**At startup**: pass the mode as a flag.

```bash
claude --permission-mode plan
```

**As a default**: set `defaultMode` in [settings](https://code.claude.com/docs/en/settings).

```json
{
  "permissions": {
    "defaultMode": "acceptEdits"
  }
}
```

The same `--permission-mode` flag works with `-p` for [non-interactive runs](https://code.claude.com/docs/en/headless).

### VS Code

**During a session**: click the mode indicator at the bottom of the prompt box. **As a default**: set `claudeCode.initialPermissionMode` in VS Code settings, or use the Claude Code extension settings panel. The mode indicator labels map to modes as follows: **Ask before edits** → `default`, **Edit automatically** → `acceptEdits`, **Plan mode** → `plan`, **Auto mode** → `auto`, **Bypass permissions** → `bypassPermissions`.

Auto mode appears in the mode indicator when your account meets every [auto mode requirement](cc_auto_mode.md). The `claudeCode.initialPermissionMode` setting does not accept `auto`; to start in auto mode by default, set `defaultMode` in your user settings instead — Claude Code ignores `defaultMode: "auto"` in project and local settings. Bypass permissions requires the **Allow dangerously skip permissions** toggle in the extension settings before it appears in the mode indicator.

### JetBrains

The JetBrains plugin runs Claude Code in the IDE terminal, so switching modes works the same as in the CLI: press `Shift+Tab` to cycle, or pass `--permission-mode` when launching.

### Desktop

Use the mode selector next to the send button. Auto and Bypass permissions appear only after you enable them in Desktop settings.

### Web and mobile

Use the mode dropdown next to the prompt box on [claude.ai/code](https://claude.ai/code) or in the mobile app. Permission prompts appear in claude.ai for approval. Which modes appear depends on where the session runs:

- **Cloud sessions** on Claude Code on the web: Accept edits, Plan mode, and Auto mode. Accept edits corresponds to `default` mode (the cloud environment pre-approves file edits regardless of mode), so the dropdown shows Accept edits instead of Ask permissions. `defaultMode: "acceptEdits"` from settings is still honored. Auto mode appears only when your organization allows it and the selected model supports it. Bypass permissions is not available.
- **Remote Control sessions** on your local machine: Ask permissions, Auto accept edits, and Plan mode. Auto and Bypass permissions are not available.

For Remote Control, you can also set the starting mode when launching the host:

```bash
claude remote-control --permission-mode acceptEdits
```

**Source**: https://code.claude.com/docs/en/permission-modes
**Last Updated**: 2026-06-13
**Status**: Active
