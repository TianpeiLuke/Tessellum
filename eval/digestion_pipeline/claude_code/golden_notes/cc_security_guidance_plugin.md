---
tags:
  - resource
  - documentation
  - claude_code
  - security
  - plugin
keywords:
  - security-guidance plugin
  - install plugin
  - reload-plugins
  - enabledPlugins
  - cloud sessions
  - shared repositories
  - disable plugin
  - uninstall plugin
  - in-session security review
topics:
  - Claude Code
  - Security
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/security-guidance
access_control_group: ["general"]
---

# Claude Code — Install and Manage the Security Guidance Plugin

## Overview

The **security guidance plugin** makes Claude review its own code changes for common vulnerabilities while it works and fix what it finds in the same session, catching issues such as injection, unsafe deserialization, and unsafe DOM APIs **before the code reaches a pull request** and reducing how much security review falls to human reviewers downstream. It is the in-session companion to [Code Review](https://code.claude.com/docs/en/code-review), which runs on pull requests: the plugin reduces what reaches the PR, and Code Review catches what does. Once installed, the plugin runs automatically — there is nothing to invoke and no separate command to remember.

This note is the **install / enable / disable procedure**. For what the plugin actually checks (its three review layers), how to add your own rules, usage cost, hook integration, and troubleshooting, see [Security Guidance — Review Layers and Rules](cc_security_guidance_layers_and_rules.md).

## Prerequisites

Before installing, confirm:

- **Claude Code CLI version 2.1.144 or later.**
- **Python 3.8 or later on your `PATH`.** The plugin tries `python3`, `python`, and `py -3` in that order.
- **A git repository for the directory you work in.** The end-of-turn and commit reviews diff against git state and skip silently outside a repository. The per-edit pattern check works anywhere.

On first run the plugin creates a virtual environment under `~/.claude/security/` and installs the Claude Agent SDK into it, which requires `pip` and network access. If that install fails, the commit review falls back to a single-shot review instead of the agentic one. On Windows the virtual environment step is skipped, so the agentic commit review runs only if `claude-agent-sdk` is already importable and otherwise falls back the same way.

## Install the plugin

In a Claude Code session, install from the [official Anthropic marketplace](https://code.claude.com/docs/en/discover-plugins#official-anthropic-marketplace):

```text
/plugin install security-guidance@claude-plugins-official
```

The install prompts for a scope. **Choose user scope** to write the plugin to your user settings, so it loads in every new local session you start on this machine. If Claude Code reports that the marketplace is not found, run `/plugin marketplace add anthropics/claude-plugins-official` first, then retry the install.

Then activate it in the current session with `/reload-plugins`, which applies pending plugin changes without a restart:

```text
/reload-plugins
```

### Enable in cloud sessions and shared repositories

User-scoped plugins do not carry into [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web), because those sessions run on Anthropic infrastructure rather than your machine. To enable the plugin there, or to turn it on for everyone who clones a repository, declare it in the project's checked-in settings:

```json
{
  "enabledPlugins": {
    "security-guidance@claude-plugins-official": true
  }
}
```

Administrators can enable the plugin organization-wide by setting [`enabledPlugins`](https://code.claude.com/docs/en/settings#plugin-settings) in [managed settings](https://code.claude.com/docs/en/admin-setup).

## Disable or uninstall

To turn off **individual layers** while keeping the rest, set the matching environment variable:

| Variable | Effect |
| :--- | :--- |
| `ENABLE_PATTERN_RULES=0` | Disable the per-edit pattern check |
| `ENABLE_STOP_REVIEW=0` | Disable the end-of-turn diff review |
| `ENABLE_COMMIT_REVIEW=0` | Disable the commit and push review |
| `ENABLE_CODE_SECURITY_REVIEW=0` | Disable all model-backed reviews at once |
| `SECURITY_GUIDANCE_DISABLE=1` | Disable the plugin entirely without uninstalling |

To pause the plugin in your user scope:

```text
/plugin disable security-guidance@claude-plugins-official
```

To remove it from your user scope:

```text
/plugin uninstall security-guidance@claude-plugins-official
```

If the plugin was enabled through a project's `.claude/settings.json`, disabling it from `/plugin` writes an override to your `.claude/settings.local.json` rather than editing the checked-in file, so the plugin stays off for you while teammates are unaffected. If it was enabled through [managed settings](https://code.claude.com/docs/en/admin-setup), only an administrator can disable it.

**Source**: https://code.claude.com/docs/en/security-guidance
**Last Updated**: 2026-06-13
**Status**: Active
