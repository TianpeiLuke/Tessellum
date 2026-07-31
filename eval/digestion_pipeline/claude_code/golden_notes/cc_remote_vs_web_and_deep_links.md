---
tags:
  - resource
  - documentation
  - claude_code
  - remote_surfaces
  - deep_links
keywords:
  - remote control vs web
  - choose the right approach
  - away-from-terminal matrix
  - deep links
  - claude-cli url scheme
  - inert until enter
  - cwd vs repo
  - url handler registration
topics:
  - Claude Code
  - Web & Remote Surfaces
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/remote-control
access_control_group: ["general"]
---

# Remote Control vs Web, and Deep Links

## Overview

This note gathers two cross-surface decision aids for working with Claude Code away from your terminal. The first is **where the session runs**: Remote Control executes on *your machine* (your filesystem, MCP servers, and project config stay available; the web/mobile UI is just a window into that local session) while [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) executes in Anthropic-managed cloud infrastructure. A broader "choose the right approach" matrix extends this across all the away-from-terminal modes (Dispatch, Remote Control, Channels, Slack, Scheduled tasks).

The second is **deep links** — `claude-cli://` URLs that open a local Claude Code terminal session in a chosen directory with a prompt pre-filled. A deep link is inert until you press Enter, so it is a safe one-click starting point you can embed in runbooks, alerts, dashboards, or READMEs.

## Remote Control vs Claude Code on the web

Remote Control and Claude Code on the web both use the claude.ai/code interface. The key difference is **where the session runs**:

- **Remote Control** executes on your machine, so your local MCP servers, tools, and project configuration stay available. The web and mobile interfaces are just a window into that local session.
- **Claude Code on the web** executes in Anthropic-managed cloud infrastructure.

When to pick which:

- Use **Remote Control** when you're in the middle of local work and want to keep going from another device.
- Use **Claude Code on the web** when you want to kick off a task without any local setup, work on a repo you don't have cloned, or run multiple tasks in parallel.

## Choose the right approach

Claude Code offers several ways to work when you're not at your terminal. They differ in what triggers the work, where Claude runs, and how much you need to set up:

| Approach | Trigger | Claude runs on | Best for |
| :--- | :--- | :--- | :--- |
| Dispatch | Message a task from the Claude mobile app | Your machine (Desktop) | Delegating work while you're away, minimal setup |
| Remote Control | Drive a running session from claude.ai/code or the Claude mobile app | Your machine (CLI or VS Code) | Steering in-progress work from another device |
| Channels | Push events from a chat app like Telegram or Discord, or your own server | Your machine (CLI) | Reacting to external events like CI failures or chat messages |
| Slack | Mention `@Claude` in a team channel | Anthropic cloud | PRs and reviews from team chat |
| Scheduled tasks | Set a schedule | CLI, Desktop, or cloud | Recurring automation like daily reviews |

Setup ranges from "pair the mobile app with Desktop" (Dispatch) and "run `claude remote-control`" (Remote Control) to installing a channel/Slack plugin or picking a frequency (Scheduled tasks). See [`cc_remote_control`](cc_remote_control.md) for the Remote Control setup procedure, and the home pages for [Dispatch](https://code.claude.com/docs/en/desktop#sessions-from-dispatch), [Channels](https://code.claude.com/docs/en/channels), [Slack](https://code.claude.com/docs/en/slack), and [Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks).

## Deep links: launch sessions from a URL

A deep link is a `claude-cli://` URL that opens Claude Code in a new terminal window, carrying a working directory and a prompt to pre-fill. It shares a one-click starting point for a task: anyone with Claude Code installed who clicks the link sees a session open with the prompt already typed. The prompt is populated but **not sent until you press Enter**. (Deep links require Claude Code v2.1.91 or later.)

Because a deep link is a URL, you can put one anywhere a link can go — an incident runbook step, a monitoring alert or dashboard, a README or wiki page, or a CI failure notification.

### How it works (and the inert-until-Enter safety model)

`claude-cli://` is a custom URL scheme that Claude Code registers with your OS, similar to how `mailto:` opens your email client. When you click one: the browser hands the URL to your OS, the OS recognizes the prefix and starts Claude Code on your machine, a new terminal window opens in the link's directory with the prompt already in the input box, and you read/edit the prompt and press Enter to send it. The link can be hosted anywhere, but the session always opens locally on the computer where you clicked.

A deep link **never executes anything on its own** — it only chooses a directory and fills the prompt box. Even from a page you don't trust, the prompt stays inert: nothing reaches the model until you read what was filled in and press Enter. When the session opens, a warning line below the input box reads `Prompt from an external link` and stays visible until you send or clear the prompt; for prompts over 1,000 characters it includes the character count and tells you to scroll and review the full text first. Permission rules, `CLAUDE.md`, and trust prompts for the selected directory apply the same way as for any other session.

### Build a link: `q`, `cwd`, and `repo`

Every deep link starts with `claude-cli://open`, the only path the handler accepts, followed by optional query parameters. The minimal form opens Claude Code in your home directory with an empty prompt:

```text
claude-cli://open
```

| Parameter | Description |
| :--- | :--- |
| `q` | Text to pre-fill in the prompt box. URL-encode the value. Use `%0A` for line breaks in multi-line prompts. Maximum 5,000 characters. |
| `cwd` | Absolute path to use as the working directory. Network and UNC paths are rejected. |
| `repo` | A GitHub `owner/name` slug. Claude Code resolves it to a local clone it has seen before and starts there. If you have no matching clone, the session opens in your home directory instead. |

`cwd` and `repo` are two ways to set the working directory. If you pass both, `cwd` takes precedence and `repo` is ignored, even if the `cwd` path does not exist.

**Choosing between `cwd` and `repo`:** use `cwd` when everyone who clicks the link has the project at the same absolute path (a standardized devcontainer or VM image); use `repo` when the link is shared and each person clones to a different location. For `repo`, each time you run `claude` in a Git repository, that directory's path is recorded against the repo's `owner/name` slug; a deep link opens whichever matching path you used most recently (multiple clones and worktrees are tracked separately). The lookup only finds paths where you have already run Claude Code at least once, and the link does not change which branch is checked out. The welcome header shows which path it picked.

### Examples: runbooks and the shell

A deep link in a runbook gives whoever is triaging a one-click way to start investigating in the right repository with a prepared prompt. The example below embeds an investigation entry point in an incident runbook, pointing at a `web-gateway` repo with a URL-encoded diagnostic prompt:

```markdown
## High 5xx rate on web-gateway

1. Acknowledge the page in PagerDuty.
2. [Open Claude Code in the gateway repo](claude-cli://open?repo=acme/web-gateway&q=5xx%20rate%20is%20elevated%20on%20web-gateway.%20Check%20recent%20deploys%2C%20error%20logs%20from%20the%20last%2030%20minutes%2C%20and%20open%20incidents%20in%20Linear.)
3. Post initial findings in #incident.
```

You can also open a deep link from a script or alias by calling your OS's URL-opening command with the link as the argument: macOS uses the built-in `open`, Linux uses `xdg-open`, and Windows uses `Start-Process` in PowerShell (or `start "" "<url>"` in `cmd.exe`, since `start` treats its first quoted argument as a window title).

### Registration and supported platforms

Claude Code registers the `claude-cli://` handler the first time you start an interactive session on macOS, Linux, and Windows — there is no separate install command, and registration writes to user-level locations only (`~/Applications/Claude Code URL Handler.app` on macOS; a `claude-code-url-handler.desktop` file under `$XDG_DATA_HOME/applications` on Linux; the `HKEY_CURRENT_USER\Software\Classes\claude-cli` registry key on Windows). The handler launches Claude Code in a detected terminal emulator: macOS reuses the terminal from your most recent interactive session (iTerm2, Ghostty, kitty, Alacritty, WezTerm, Terminal.app); Linux honors `$TERMINAL`, then `x-terminal-emulator`, then common emulators; Windows prefers Windows Terminal, then PowerShell, then `cmd.exe`. To prevent registration entirely, set [`disableDeepLinkRegistration`](https://code.claude.com/docs/en/settings) to `"disable"` in `settings.json`, or in [managed settings](https://code.claude.com/docs/en/server-managed-settings) to enforce it across an organization.

### VS Code tab instead of a terminal

The VS Code extension registers its own handler at `vscode://anthropic.claude-code/open`, which opens a Claude Code editor tab rather than a terminal window. See the [VS Code docs](https://code.claude.com/docs/en/vs-code#launch-a-vs-code-tab-from-other-tools) for that URL's parameters.

### Troubleshooting

- **Clicking the link does nothing**: the handler likely isn't registered yet — start an interactive `claude` session once on that machine, exit, and try again. On Linux without a desktop environment, `xdg-open` may have nothing to dispatch to.
- **The link renders as plain text**: some Markdown renderers only allow `http`/`https` and strip other schemes. GitHub does this in READMEs, issues, pull requests, and wikis — a `claude-cli://` link written as a normal Markdown link (a bracketed label followed by the URL in parentheses) renders as just the label text, with no link and the URL removed. Put the deep link in a code block so readers can copy the URL into their address bar.
- **Session opens in the home directory instead of the repo**: `repo` only resolves to clones Claude Code has already seen; run `claude` inside the clone once, or switch to `cwd` with an absolute path.
- **The link opens the wrong terminal**: on macOS start `claude` in your preferred terminal once; on Linux set `$TERMINAL`; on Windows the order is fixed (install Windows Terminal if you want links to open there).

**Source**: https://code.claude.com/docs/en/remote-control
**Last Updated**: 2026-06-13
**Status**: Active
