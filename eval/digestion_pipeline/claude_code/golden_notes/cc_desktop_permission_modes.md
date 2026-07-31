---
tags:
  - resource
  - documentation
  - claude_code
  - desktop
  - permission_modes
keywords:
  - desktop permission modes
  - ask permissions
  - auto accept edits
  - plan mode
  - auto mode
  - bypass permissions
  - mode selector
  - auto mode availability
  - cloud session permission mapping
topics:
  - Claude Code
  - Desktop application
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/desktop
access_control_group: ["general"]
---

# Claude Desktop — Permission Modes

## Overview

In the Claude Desktop **Code** tab, **permission modes** control how much autonomy Claude has during a session — whether it asks before editing files, running commands, or both. Unlike the CLI (which uses `Shift+Tab` to cycle modes), Desktop exposes the modes through a graphical **mode selector** next to the send button, and you can switch modes at any time during a session. The recommended progression is to start with **Ask permissions** to see exactly what Claude does, then move to **Auto accept edits** or **Plan mode** as you grow comfortable.

This note documents the five graphical modes and their settings keys, the availability requirements for the newer **Auto** mode, how cloud sessions map the selector differently, and the one mode (`dontAsk`) that remains CLI-only. The permission *concept* itself (how rules and modes work across all surfaces) is owned by the [permission modes reference](https://code.claude.com/docs/en/permission-modes).

## The Five Permission Modes

Each mode maps to a `settings` key and a distinct behavior. You switch between them with the mode selector next to the send button (or press `Cmd+Shift+M` to open the permission mode menu).

| Mode | Settings key | Behavior |
| ---- | ------------ | -------- |
| **Ask permissions** | `default` | Claude asks before editing files or running commands. You see a diff and can accept or reject each change. Recommended for new users. |
| **Auto accept edits** | `acceptEdits` | Claude auto-accepts file edits and common filesystem commands like `mkdir`, `touch`, and `mv`, but still asks before running other terminal commands. Use this when you trust file changes and want faster iteration. |
| **Plan mode** | `plan` | Claude reads files and runs commands to explore, then proposes a plan without editing your source code. Good for complex tasks where you want to review the approach first. |
| **Auto** | `auto` | Claude executes all actions with background safety checks that verify alignment with your request. Reduces permission prompts while maintaining oversight. Enable in your Settings → Claude Code. See availability requirements below. |
| **Bypass permissions** | `bypassPermissions` | Claude runs without permission prompts, except those forced by explicit [ask rules](https://code.claude.com/docs/en/permissions); equivalent to `--dangerously-skip-permissions` in the CLI. Enable in your Settings → Claude Code under "Allow bypass permissions mode". Only use this in sandboxed containers or VMs. Enterprise admins can disable this option. |

The recommended workflow is to start a complex task in **Plan mode** so Claude maps out an approach before making changes; once you approve the plan, switch to **Auto accept edits** or **Ask permissions** to execute it (see [explore first, then plan, then code](https://code.claude.com/docs/en/best-practices)).

## Auto Mode Availability

**Auto** mode is a research preview available to all users on the Anthropic API, and it requires **Claude Opus 4.6 or later, or Sonnet 4.6**.

In **Enterprise deployments** that route Desktop to Google Cloud Vertex AI, Auto mode is **off until you set `CLAUDE_CODE_ENABLE_AUTO_MODE`** (see [enable auto mode on Bedrock, Vertex AI, or Foundry](https://code.claude.com/docs/en/permission-modes)), and only **Claude Opus 4.7 and Opus 4.8** are supported there.

## Cloud Session Mode Mapping

Cloud (Remote) sessions expose a different subset of modes, because the cloud environment is already sandboxed:

- Cloud sessions support **Accept edits, Plan mode, and Auto mode**.
- **Accept edits corresponds to `default` mode**: cloud sessions pre-approve file edits, so the selector shows **Accept edits** instead of Ask permissions.
- **Bypass permissions is not available** in cloud sessions, because the cloud environment is already sandboxed.

## Enterprise Restrictions

Enterprise admins can restrict which permission modes are available to users in their organization (for example, disabling Bypass permissions mode). The mechanism and the relevant managed-settings keys are covered in [enterprise configuration](https://code.claude.com/docs/en/desktop#enterprise-configuration) (digested in [`cc_desktop_environments_extend_and_enterprise`](cc_desktop_environments_extend_and_enterprise.md)).

## What's Not in Desktop

The `dontAsk` permission mode — which allows only pre-approved tools — is available **only in the CLI**, not in the Desktop mode selector. See [allow only pre-approved tools with dontAsk mode](https://code.claude.com/docs/en/permission-modes) for the CLI behavior.

**Source**: https://code.claude.com/docs/en/desktop
**Last Updated**: 2026-06-13
**Status**: Active
