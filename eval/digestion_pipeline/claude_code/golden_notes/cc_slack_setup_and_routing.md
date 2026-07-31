---
tags:
  - resource
  - documentation
  - claude_code
  - slack
  - setup
keywords:
  - claude code in slack setup
  - routing mode code only code plus chat
  - slack app marketplace install
  - connect claude account
  - invite claude to channel
  - channel based access control
  - github repository authentication
  - slack troubleshooting
topics:
  - Claude Code
  - Slack
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/slack
access_control_group: ["general"]
---

# Claude Code in Slack — Setup, Routing & Access

## Overview

This is the operational procedure for standing up **Claude Code in Slack** and governing who can use it. Setup is a five-step sequence — a workspace admin installs the Claude app, each user connects their Claude account, configures Claude Code on the web with a GitHub repository, chooses a **routing mode** (Code only vs. Code + Chat), and invites Claude to the specific channels where it should respond. Access is governed at three layers — per-user plan limits and repository scoping, workspace-admin install/removal, and channel-membership gating — and the page closes with a troubleshooting checklist for the common setup failures.

For what Claude Code in Slack *is* and how a request flows to a web session, see the sibling note [Claude Code in Slack (concept)](cc_claude_code_in_slack.md).

## Prerequisites

Before using Claude Code in Slack, ensure you have the following:

| Requirement | Details |
| :--- | :--- |
| Claude Plan | Pro, Max, Team, or Enterprise with Claude Code access (premium seats or Chat + Claude Code seats) |
| Claude Code on the web | Access to [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) must be enabled |
| GitHub Account | Connected to Claude Code on the web with at least one repository authenticated |
| Slack Authentication | Your Slack account linked to your Claude account via the Claude app |

## Setting up Claude Code in Slack

The setup is a five-step sequence:

1. **Install the Claude App in Slack** — A workspace administrator must install the Claude app from the [Slack App Marketplace](https://slack.com/marketplace/A08SF47R6P4) and click "Add to Slack" to begin the installation process.
2. **Connect your Claude account** — After the app is installed, authenticate your individual Claude account: open the Claude app in Slack by clicking on "Claude" in your Apps section, navigate to the **App Home** tab, click **Connect** to link your Slack account with your Claude account, then complete the authentication flow in your browser.
3. **Configure Claude Code on the web** — Ensure your Claude Code on the web is properly configured: visit [claude.ai/code](https://claude.ai/code) and sign in with the same account you connected to Slack, connect your GitHub account if not already connected, and authenticate at least one repository that you want Claude to work with.
4. **Choose your routing mode** — After connecting your accounts, configure how Claude handles your messages in Slack. Navigate to the Claude App Home in Slack to find the **Routing Mode** setting (see the routing-mode table below).
5. **Add Claude to channels** — Claude is not automatically added to any channels after installation. To use Claude in a channel, invite it by typing `/invite @Claude` in that channel. Claude can only respond to @mentions in channels where it has been added.

### Choose your routing mode

The Routing Mode setting (Step 4) determines how each @mention is dispatched:

| Mode | Behavior |
| :--- | :--- |
| **Code only** | Claude routes all @mentions to Claude Code sessions. Best for teams using Claude in Slack exclusively for development tasks. |
| **Code + Chat** | Claude analyzes each message and intelligently routes between Claude Code (for coding tasks) and Claude Chat (for writing, analysis, and general questions). Best for teams who want a single @Claude entry point for all types of work. |

In **Code + Chat** mode, if Claude routes a message to Chat but you wanted a coding session, you can click **Retry as Code** to create a Claude Code session instead. Similarly, if it's routed to Code but you wanted a Chat session, you can choose that option in that thread.

## Access and permissions

### User-level access

| Access Type | Requirement |
| :--- | :--- |
| Claude Code Sessions | Each user runs sessions under their own Claude account |
| Usage & Rate Limits | Sessions count against the individual user's plan limits |
| Repository Access | Users can only access repositories they've personally connected |
| Session History | Sessions appear in your Claude Code history on claude.ai/code |

### Workspace-level access

Slack workspace administrators control whether the Claude app is available in their workspace:

| Control | Description |
| :--- | :--- |
| App installation | Workspace admins decide whether to install the Claude app from the Slack App Marketplace |
| Enterprise Grid distribution | For Enterprise Grid organizations, organization admins can control which workspaces have access to the Claude app |
| App removal | Removing the app from a workspace immediately revokes access for all users in that workspace |

### Channel-based access control

Claude is not automatically added to any channels after installation. Users must explicitly invite Claude to channels where they want to use it:

- **Invite required**: Type `/invite @Claude` in any channel to add Claude to that channel.
- **Channel membership controls access**: Claude can only respond to @mentions in channels where it has been added.
- **Access gating through channels**: Admins can control who uses Claude Code by managing which channels Claude is invited to and who has access to those channels.
- **Private channel support**: Claude works in both public and private channels, giving teams flexibility in controlling visibility.

This channel-based model lets teams restrict Claude Code usage to specific channels, providing an additional layer of access control beyond workspace-level permissions.

## Troubleshooting

### Sessions not starting

1. Verify your Claude account is connected in the Claude App Home.
2. Check that you have Claude Code on the web access enabled.
3. Ensure you have at least one GitHub repository connected to Claude Code.

### Repository not showing

1. Connect the repository in Claude Code on the web at [claude.ai/code](https://claude.ai/code).
2. Verify your GitHub permissions for that repository.
3. Try disconnecting and reconnecting your GitHub account.

### Wrong repository selected

1. Click the **Change Repo** button to select a different repository.
2. Include the repository name in your request for more accurate selection.

### Authentication errors

1. Disconnect and reconnect your Claude account in the App Home.
2. Ensure you're signed into the correct Claude account in your browser.
3. Check that your Claude plan includes Claude Code access.

### Session expiration

1. Sessions remain accessible in your Claude Code history on the web.
2. You can continue or reference past sessions from [claude.ai/code](https://claude.ai/code).

**Source**: https://code.claude.com/docs/en/slack
**Last Updated**: 2026-06-13
**Status**: Active
