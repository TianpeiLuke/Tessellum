---
tags:
  - resource
  - documentation
  - claude_code
  - computer_use
  - safety
keywords:
  - computer use safety
  - trust boundary
  - per-app approval
  - sentinel warnings
  - guardrails
  - terminal excluded from screenshots
  - global escape
  - lock file
topics:
  - Claude Code
  - Computer Use
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/computer-use
access_control_group: ["general"]
---

# Computer Use — Safety and the Trust Boundary

## Overview

Computer use puts a different argument on the table than the rest of Claude Code's tools: unlike the **sandboxed Bash tool**, computer use runs on your *actual desktop* with access to the apps you approve, so the trust boundary is genuinely different. The claim this page makes is that this expanded boundary is acceptable because a set of built-in guardrails reduce risk without requiring any configuration — chief among them a per-app, per-session approval gate that asks you to consent before Claude touches any specific application.

This note covers the safety case: how per-app approval works (including the sentinel warnings for high-reach apps and the view-only / click-only / full-control tiers), and the guardrails that back the trust-boundary argument. How computer use works mechanically (enabling it, the machine-wide lock, app hiding, screenshot downscaling) is the concept note — see [Computer Use](cc_computer_use.md).

## Approve apps per session

Enabling the `computer-use` server doesn't grant Claude access to every app on your machine. The first time Claude needs a specific app in a session, a prompt appears in your terminal showing:

- Which apps Claude wants to control
- Any extra permissions requested, such as clipboard access
- How many other apps will be hidden while Claude works

You choose **Allow for this session** or **Deny**. Approvals last for the current session. You can approve multiple apps at once when Claude requests them together.

### Sentinel warnings for high-reach apps

Apps with broad reach show an extra warning in the prompt so you know what approving them grants:

| Warning                    | Applies to                                                   |
| :------------------------- | :----------------------------------------------------------- |
| Equivalent to shell access | Terminal, iTerm, VS Code, Warp, and other terminals and IDEs |
| Can read or write any file | Finder                                                       |
| Can change system settings | System Settings                                              |

These apps aren't blocked. The warning lets you decide whether the task warrants that level of access.

### Control tiers vary by app category

Claude's level of control also varies by app category: browsers and trading platforms are view-only, terminals and IDEs are click-only, and everything else gets full control. For the complete tier breakdown, see [app permissions in Desktop](https://code.claude.com/docs/en/desktop) (`/en/desktop#app-permissions`).

## Safety and the trust boundary

Unlike the [sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing), computer use runs on your actual desktop with access to the apps you approve. Claude checks each action and flags potential **prompt injection** from on-screen content, but the trust boundary is different. See the [computer use safety guide](https://support.claude.com/en/articles/14128542) for best practices.

The built-in guardrails reduce risk without requiring configuration:

- **Per-app approval**: Claude can only control apps you've approved in the current session.
- **Sentinel warnings**: apps that grant shell, filesystem, or system settings access are flagged before you approve.
- **Terminal excluded from screenshots**: Claude never sees your terminal window, so on-screen prompts in your session can't feed back into the model.
- **Global escape**: the `Esc` key aborts computer use from anywhere, and the key press is consumed so prompt injection can't use it to dismiss dialogs.
- **Lock file**: only one session can control your machine at a time.

**Source**: https://code.claude.com/docs/en/computer-use
**Last Updated**: 2026-06-13
**Status**: Active
