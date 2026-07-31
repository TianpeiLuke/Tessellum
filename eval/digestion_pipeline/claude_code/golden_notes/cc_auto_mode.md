---
tags:
  - resource
  - documentation
  - claude_code
  - permissions
  - auto_mode
keywords:
  - auto mode
  - classifier model
  - eliminate permission prompts
  - blocked by default
  - allowed by default
  - conversational boundaries
  - auto mode fallback
  - subagent classifier checks
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

# Claude Code — Auto Mode

## Overview

**Auto mode** lets Claude Code execute without routine permission prompts. Instead of pausing on every action, a **separate classifier model** reviews each action before it runs and blocks anything that escalates beyond your request, targets unrecognized infrastructure, or appears driven by hostile content Claude read. It is the high-autonomy point on the permission-mode spectrum — fewer prompts in exchange for classifier-mediated trust — but explicit ask rules and deny rules still resolve first, so the classifier is a second gate layered on top of the [permission system](https://code.claude.com/docs/en/permissions), not a replacement for it.

Auto mode also nudges Claude to keep working without stopping for clarifying questions (though Claude still asks when your prompt or a skill explicitly relies on it). The docs flag it as a **research preview**: it reduces prompts but does not guarantee safety — use it for tasks where you trust the general direction, not as a replacement for review on sensitive operations. Its `autoMode` configuration reference (trusted-infrastructure entries and the rule lists) lives in [`cc_auto_mode_configuration`](cc_auto_mode_configuration.md).

## Requirements

Auto mode requires Claude Code **v2.1.83 or later** and is available only when your account meets all of these requirements:

- **Plan**: All plans.
- **Admin**: on Team and Enterprise, an admin must enable it in Claude Code admin settings before users can turn it on. Admins can also lock it off by setting `permissions.disableAutoMode` to `"disable"` in managed settings.
- **Model**: on the Anthropic API, Claude Opus 4.6 or later, or Sonnet 4.6. On Amazon Bedrock, Google Cloud Vertex AI, and Microsoft Foundry, only Claude Opus 4.7 and Opus 4.8. Older models (Sonnet 4.5, Opus 4.5, Haiku, claude-3) are not supported on any provider.
- **Provider**: available by default on the Anthropic API. On Bedrock, Vertex AI, and Foundry, auto mode is off until you set `CLAUDE_CODE_ENABLE_AUTO_MODE`.

If Claude Code reports auto mode as unavailable, one of these requirements is unmet — this is not a transient outage. A separate message naming a model and saying auto mode "cannot determine the safety" of an action is a transient classifier outage (see the [error reference](https://code.claude.com/docs/en/errors)). If `defaultMode: "auto"` is set but the session starts in `default` mode with no error, the setting is likely in `.claude/settings.json` or `.claude/settings.local.json`; Claude Code v2.1.142+ ignore `auto` from those files so a repository cannot grant itself auto mode — move it to `~/.claude/settings.json`.

## Enable auto mode on Bedrock, Vertex AI, or Foundry

On Amazon Bedrock, Google Cloud Vertex AI, and Microsoft Foundry, auto mode does not appear in the `Shift+Tab` cycle until `CLAUDE_CODE_ENABLE_AUTO_MODE` is set to `1` (works in v2.1.158+; only Opus 4.7 and Opus 4.8 are supported on these providers). To enable it for one developer, add the variable to the `env` block in `~/.claude/settings.json`:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_AUTO_MODE": "1"
  }
}
```

To enable it organization-wide, add the same `env` block to managed settings. Once set, auto mode appears in the `Shift+Tab` cycle for every session; to make it the default starting mode, also set `"permissions": {"defaultMode": "auto"}` in user or managed settings (on these providers, `defaultMode: "auto"` is ignored unless `CLAUDE_CODE_ENABLE_AUTO_MODE` is also set). To prevent developers from enabling it, set `disableAutoMode` to `"disable"` in managed settings, which overrides the enable variable. Through an LLM gateway configured with `ANTHROPIC_BASE_URL`, auto mode may already be reachable without the enable variable because the gateway routes through the Anthropic API; `disableAutoMode` still applies.

## What the classifier blocks and allows by default

The classifier trusts your working directory and your repo's configured remotes. Everything else is treated as external until you configure trusted infrastructure (see [`cc_auto_mode_configuration`](cc_auto_mode_configuration.md)).

**Blocked by default**: downloading and executing code, like `curl | bash`; sending sensitive data to external endpoints; production deploys and migrations; mass deletion on cloud storage; granting IAM or repo permissions; modifying shared infrastructure; irreversibly destroying files that existed before the session; force push, or pushing directly to `main`.

**Allowed by default**: local file operations in your working directory; installing dependencies declared in your lock files or manifests; reading `.env` and sending credentials to their matching API; read-only HTTP requests; pushing to the branch you started on or one Claude created.

Sandbox network access requests are routed through the classifier rather than allowed by default. Run `claude auto-mode defaults` to see the full rule lists. If routine actions get blocked, an administrator can add trusted repos, buckets, and services via the `autoMode.environment` setting.

## Boundaries you state in conversation

The classifier treats boundaries you state in the conversation as a block signal. If you tell Claude "don't push" or "wait until I review before deploying", the classifier blocks matching actions even when the default rules would allow them. A boundary stays in force until you lift it in a later message — Claude's own judgment that a condition was met does not lift it.

Boundaries are not stored as rules. The classifier re-reads them from the transcript on each check, so a boundary can be lost if context compaction removes the message that stated it. For a hard guarantee, add a deny rule instead.

## When auto mode falls back

Each denied action shows a notification and appears in `/permissions` under the Recently denied tab, where you can press `r` to retry it with a manual approval. If the classifier blocks an action **3 times in a row or 20 times total**, auto mode pauses and Claude Code resumes prompting; approving the prompted action resumes auto mode. These thresholds are not configurable. Any allowed action resets the consecutive counter, while the total counter persists for the session and resets only when its own limit triggers a fallback. In non-interactive mode with the `-p` flag, repeated blocks abort the session since there is no user to prompt. Repeated blocks usually mean the classifier is missing context about your infrastructure — use `/feedback` to report false positives, or have an administrator configure trusted infrastructure.

## How the classifier evaluates actions

Each action goes through a fixed decision order; the first matching step wins:

1. Actions matching your allow or deny rules resolve immediately, except writes to protected paths, which route to the classifier even when an allow rule matches.
2. Read-only actions and file edits in your working directory are auto-approved, except writes to protected paths.
3. Everything else goes to the classifier.
4. If the classifier blocks, Claude receives the reason and tries an alternative.

On entering auto mode, broad allow rules that grant arbitrary code execution are dropped: blanket `Bash(*)` or `PowerShell(*)`, wildcarded interpreters like `Bash(python*)`, package-manager run commands, and `Agent` allow rules. Narrow rules like `Bash(npm test)` carry over. Dropped rules are restored when you leave auto mode.

The classifier sees user messages, tool calls, and your CLAUDE.md content. Tool results are stripped, so hostile content in a file or web page cannot manipulate it directly. A separate server-side probe scans incoming tool results and flags suspicious content before Claude reads it.

## How auto mode handles subagents

The classifier checks subagent work at three points:

1. **Before a subagent starts**, the delegated task description is evaluated, so a dangerous-looking task is blocked at spawn time.
2. **While the subagent runs**, each of its actions goes through the classifier with the same rules as the parent session, and any `permissionMode` in the subagent's frontmatter is ignored.
3. **When the subagent finishes**, the classifier reviews its full action history; if that return check flags a concern, a security warning is prepended to the subagent's results.

## Cost and latency

The classifier runs on a server-configured model that is independent of your `/model` selection, so switching models does not change classifier availability. Classifier calls count toward your token usage. Each check sends a portion of the transcript plus the pending action, adding a round-trip before execution. Reads and working-directory edits outside protected paths skip the classifier, so the overhead comes mainly from shell commands and network operations.

**Source**: https://code.claude.com/docs/en/permission-modes
**Last Updated**: 2026-06-13
**Status**: Active
