---
tags:
  - resource
  - documentation
  - claude_code
  - permissions
  - permission_modes
keywords:
  - acceptedits mode
  - plan mode
  - dontask mode
  - bypasspermissions mode
  - protected paths
  - auto-approve file edits
  - plan approval flow
  - per-mode behavior
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

# Claude Code — Permission Modes (Per-Mode Detail)

## Overview

Beyond `default` (reads-only review of each action), Claude Code offers four looser permission modes plus a cross-cutting protected-paths guard. **`acceptEdits`** auto-approves file edits and common filesystem commands inside the working directory; **`plan`** mode researches and proposes changes without making them, gated by an explicit plan-approval step; **`dontAsk`** auto-denies anything that would prompt, leaving only pre-approved tools; and **`bypassPermissions`** skips all checks for use only in isolated environments. Each mode is a distinct trust level, and across every mode except `bypassPermissions`, writes to a fixed set of **protected paths** are never auto-approved.

The overview, the full mode table, and how to switch between modes are covered separately in [`cc_permission_modes_overview`](cc_permission_modes_overview.md); the substantial auto-mode section lives in [`cc_auto_mode`](cc_auto_mode.md). This note details the behavior of `acceptEdits`, `plan`, `dontAsk`, `bypassPermissions`, and protected paths.

## Auto-approve file edits with acceptEdits mode

`acceptEdits` mode lets Claude create and edit files in your working directory without prompting. The status bar shows `⏵⏵ accept edits on` while this mode is active.

In addition to file edits, `acceptEdits` mode auto-approves common filesystem Bash commands: `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, and `sed`. These commands are also auto-approved when prefixed with safe environment variables such as `LANG=C` or `NO_COLOR=1`, or process wrappers such as `timeout`, `nice`, or `nohup`. Like file edits, auto-approval applies only to paths inside your working directory or `additionalDirectories`. Paths outside that scope, writes to protected paths, and all other Bash commands still prompt.

When the [PowerShell tool](https://code.claude.com/docs/en/tools-reference) is enabled, `acceptEdits` mode also auto-approves `Set-Content`, `Add-Content`, `Clear-Content`, and `Remove-Item` on in-scope paths, along with their common aliases. The same scope and protected-path rules apply.

Use `acceptEdits` when you want to review changes in your editor or via `git diff` after the fact rather than approving each edit inline. Press `Shift+Tab` once from default mode to enter it, or start with it directly:

```bash theme={null}
claude --permission-mode acceptEdits
```

## Analyze before you edit with plan mode

Plan mode tells Claude to research and propose changes without making them. Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source. Permission prompts still apply the same as default mode.

Enter plan mode by pressing `Shift+Tab` or prefixing a single prompt with `/plan`. You can also start in plan mode from the CLI:

```bash theme={null}
claude --permission-mode plan
```

Press `Shift+Tab` again to leave plan mode without approving a plan.

### Review and approve a plan

When the plan is ready, Claude presents it and asks how to proceed. From that prompt you can:

* Approve and start in auto mode
* Approve and accept edits
* Approve and review each edit manually
* Keep planning with feedback
* Refine with [Ultraplan](https://code.claude.com/docs/en/ultraplan) for browser-based review

Approving a plan exits plan mode and switches the session to the permission mode each approve option describes, so Claude starts editing. To plan again, cycle back to plan mode with `Shift+Tab`, or prefix your next prompt with `/plan`.

Press `Ctrl+G` to open the proposed plan in your default text editor and edit it directly before Claude proceeds. When `showClearContextOnPlanAccept` is enabled, each approve option also offers to clear the planning context first. Accepting a plan also names the session from the plan content automatically, unless you've already set a name with `--name` or `/rename`.

### Set plan mode as the default

To make plan mode the default for a project, set `defaultMode` in `.claude/settings.json`:

```json theme={null}
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

## Allow only pre-approved tools with dontAsk mode

`dontAsk` mode auto-denies every tool call that would otherwise prompt. Only actions matching your `permissions.allow` rules and [read-only Bash commands](https://code.claude.com/docs/en/permissions#read-only-commands) can execute; explicit `ask` rules are denied rather than prompting. This makes the mode fully non-interactive for CI pipelines or restricted environments where you pre-define exactly what Claude may do. Cloud sessions on [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) ignore `defaultMode: "dontAsk"`; see bypassPermissions below for details. Set it at startup with the flag `claude --permission-mode dontAsk`.

## Skip all checks with bypassPermissions mode

`bypassPermissions` mode disables permission prompts and safety checks so tool calls execute immediately. As of v2.1.126 this includes writes to protected paths, which earlier versions still prompted for. Explicit `ask` rules still force a prompt in this mode, and removals targeting the filesystem root or home directory, such as `rm -rf /` and `rm -rf ~`, still prompt as a circuit breaker against model error. Only use this mode in isolated environments like containers, VMs, or dev containers without internet access, where Claude Code cannot damage your host system.

You cannot enter `bypassPermissions` from a session that was started without one of the enabling flags; restart with one to enable it (`claude --permission-mode bypassPermissions`). The `--dangerously-skip-permissions` flag is equivalent.

On Linux and macOS, Claude Code refuses to start in this mode when running as root or under `sudo`:

```text theme={null}
--dangerously-skip-permissions cannot be used with root/sudo privileges for security reasons
```

The check is skipped automatically inside a recognized sandbox. To run autonomously in a container, use the [dev container](https://code.claude.com/docs/en/devcontainer) configuration, which runs Claude Code as a non-root user.

[Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) does not honor `defaultMode: "bypassPermissions"` or `"dontAsk"` from your settings files, so a repository's checked-in settings cannot start a cloud session in bypass-permissions mode. The setting is ignored silently and the session starts in the mode shown in the mode dropdown instead.

`bypassPermissions` offers no protection against prompt injection or unintended actions. For background safety checks with far fewer prompts, use [auto mode](cc_auto_mode.md) instead. Administrators can block this mode by setting `permissions.disableBypassPermissionsMode` to `"disable"` in [managed settings](cc_managed_permission_settings_and_precedence.md).

## Protected paths

Writes to a small set of paths are never auto-approved, in every mode except `bypassPermissions`. This prevents accidental corruption of repository state and Claude's own configuration.

| Mode                             | Protected-path writes    |
| :------------------------------- | :----------------------- |
| `default`, `acceptEdits`, `plan` | Prompted                 |
| `auto`                           | Routed to the classifier |
| `dontAsk`                        | Denied                   |
| `bypassPermissions`              | Allowed                  |

`permissions.allow` rules in settings files do not pre-approve protected-path writes. The safety check runs before Claude Code evaluates allow rules from settings, so an entry such as `Edit(.claude/**)` does not change the per-mode outcome in the table above. In modes that prompt, the prompt for a `.claude/` write offers **Yes, and allow Claude to edit its own settings for this session**, which approves later `.claude/` writes in that session without prompting again.

**Protected directories**: `.git`, `.config/git`, `.vscode`, `.idea`, `.husky`, `.cargo`, `.devcontainer`, `.yarn`, `.mvn`, and `.claude` (except `.claude/worktrees`, where Claude stores its own git worktrees).

**Protected files** include git config (`.gitconfig`, `.gitmodules`), shell profiles (`.bashrc`, `.bash_profile`, `.zshrc`, `.profile`, `.envrc`, and related dotfiles), package-manager configs (`.npmrc`, `.yarnrc`, `.pnp.cjs`, `bunfig.toml`, etc.), Bazel configs (`.bazelrc`, `.bazelversion`, `.bazeliskrc`), pre-commit/hook configs (`.pre-commit-config.yaml`, `lefthook.yml` and variants), build-wrapper properties (`gradle-wrapper.properties`, `maven-wrapper.properties`), `.devcontainer.json`, tooling configs (`.ripgreprc`, `pyrightconfig.json`), and `.mcp.json` / `.claude.json`.

**Source**: https://code.claude.com/docs/en/permission-modes
**Last Updated**: 2026-06-13
**Status**: Active
