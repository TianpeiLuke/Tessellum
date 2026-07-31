---
tags:
  - resource
  - documentation
  - claude_code
  - setup
  - updates
keywords:
  - claude code update
  - auto-updates
  - release channel
  - autoupdateschannel latest stable
  - minimumversion pin
  - disable autoupdater
  - claude update
  - managed version range
topics:
  - Claude Code
  - Setup
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/setup
access_control_group: ["general"]
---

# Claude Code — Update and Release Channels

## Overview

Native installations of Claude Code **automatically update in the background**, while Homebrew, WinGet, and Linux package manager installations require manual updates by default. This note covers how the auto-updater works, how to choose a **release channel** (`latest` vs `stable`), how to pin a minimum version floor, how to disable auto-updates, and how to apply an update manually with `claude update`.

The release channel and version controls let you trade immediacy for stability: `latest` ships new versions as soon as they're released, while `stable` runs a build that is typically about a week old and skips releases with major regressions. For enterprise deployments, organizations can enforce both a channel and a version range across all users through managed settings.

## Auto-updates

Claude Code checks for updates on startup and periodically while running. Updates download and install in the background, then take effect the next time you start Claude Code.

Run `claude doctor` to see the result of the most recent update attempt.

If an npm global install can't auto-update because the npm global directory isn't writable, Claude Code shows a one-time notice at startup, and `claude doctor` lists the available fixes. See [permission errors during installation](https://code.claude.com/docs/en/troubleshoot-install#permission-errors-during-installation) for details.

Homebrew, WinGet, apt, dnf, and apk installations do not auto-update by default. To upgrade Homebrew manually, run `brew upgrade claude-code` or `brew upgrade claude-code@latest`, depending on which cask you installed; for WinGet, run `winget upgrade Anthropic.ClaudeCode`. To have Claude Code run the upgrade command for you on Homebrew or WinGet, set [`CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE`](https://code.claude.com/docs/en/env-vars) to `1` — Claude Code then runs the upgrade in the background when a new version is available and shows a restart prompt on success, targeting only the Claude Code package. On WinGet the upgrade may fail while Claude Code is running because Windows locks the executable, in which case the manual command is shown instead; apt, dnf, and apk continue to require a manual upgrade because those commands need elevated privileges.

> **Known issue:** Claude Code may notify you of updates before the new version is available in these package managers. If an upgrade fails, wait and try again later. Homebrew also keeps old versions on disk after upgrades — run `brew cleanup` periodically to reclaim disk space.

## Configure release channel

Control which release channel Claude Code follows for auto-updates and `claude update` with the `autoUpdatesChannel` setting:

- `"latest"`, the default: receive new features as soon as they're released
- `"stable"`: use a version that is typically about one week old, skipping releases with major regressions

Configure this via `/config` → **Auto-update channel**, or add it to your [settings.json file](https://code.claude.com/docs/en/settings):

```json
{
  "autoUpdatesChannel": "stable"
}
```

For enterprise deployments, you can enforce a consistent release channel across your organization using [managed settings](https://code.claude.com/docs/en/permissions#managed-settings).

Homebrew installations choose a channel by cask name instead of this setting: `claude-code` tracks stable and `claude-code@latest` tracks latest.

## Pin a minimum version

The `minimumVersion` setting establishes a floor. Background auto-updates and `claude update` refuse to install any version below this value, so moving to the `"stable"` channel does not downgrade you if you are already on a newer `"latest"` build.

Switching from `"latest"` to `"stable"` via `/config` prompts you to either stay on the current version or allow the downgrade. Choosing to stay sets `minimumVersion` to that version. Switching back to `"latest"` clears it.

Add it to your [settings.json file](https://code.claude.com/docs/en/settings) to pin a floor explicitly:

```json
{
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.100"
}
```

In [managed settings](https://code.claude.com/docs/en/permissions#managed-settings), this enforces an organization-wide minimum that user and project settings cannot override.

The `minimumVersion` pin only constrains updates. To make Claude Code refuse to start outside a version range, use the managed settings `requiredMinimumVersion` and `requiredMaximumVersion` instead. Updates also respect the `requiredMaximumVersion` ceiling. See [available settings](https://code.claude.com/docs/en/settings#available-settings).

## Disable auto-updates

Set `DISABLE_AUTOUPDATER` to `"1"` in the `env` key of your [`settings.json`](https://code.claude.com/docs/en/settings#available-settings) file:

```json
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

`DISABLE_AUTOUPDATER` only stops the background check; `claude update` and `claude install` still work. To block all update paths, including manual updates, set [`DISABLE_UPDATES`](https://code.claude.com/docs/en/env-vars) instead. Use this when you distribute Claude Code through your own channels and need users to stay on the version you provide.

## Update manually

To apply an update immediately without waiting for the next background check, run:

```bash
claude update
```

**Source**: https://code.claude.com/docs/en/setup
**Last Updated**: 2026-06-13
**Status**: Active
