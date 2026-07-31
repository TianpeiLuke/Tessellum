---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - recipes
keywords:
  - reload environment hook
  - cwdchanged hook
  - filechanged hook
  - claude_env_file
  - direnv reload
  - auto-approve permission prompt
  - permissionrequest hook
  - exitplanmode auto-approve
  - setmode acceptedits
  - narrow matcher caution
topics:
  - Claude Code
  - Hooks
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/hooks-guide
access_control_group: ["general"]
---

# Claude Code Hooks — Environment & Permission Recipes

## Overview

Two ready-to-use hook recipes that adapt Claude Code to your working context. The first keeps Claude's Bash tool in sync with per-directory environment variables (the kind tools like [direnv](https://direnv.net/) manage in a shell) by pairing `SessionStart`, `CwdChanged`, and `FileChanged` hooks that all write to `CLAUDE_ENV_FILE`. The second skips the approval dialog for tool calls you always allow by writing a JSON decision from a `PermissionRequest` hook — and shows how to optionally switch the session's permission mode.

Both recipes are configuration blocks you add to a [settings file](https://code.claude.com/docs/en/hooks-guide#configure-hook-location); for the lifecycle-event model, exit codes, and structured JSON output these rely on, see the sibling note [`cc_hooks_io_and_decision_control`](cc_hooks_io_and_decision_control.md). Full event schemas (`CwdChanged`, `FileChanged`, `PermissionRequest`) live in the [Hooks reference](https://code.claude.com/docs/en/hooks).

## Reload environment when directory or files change

Some projects set different environment variables depending on which directory you are in. Tools like direnv do this automatically in your shell, but Claude's Bash tool does not pick up those changes on its own.

Pairing a `SessionStart` hook with a `CwdChanged` hook fixes this. `SessionStart` loads the variables for the directory you launch in, and `CwdChanged` reloads them each time Claude changes directory. Both write to `CLAUDE_ENV_FILE`, which Claude Code runs as a script preamble before each Bash command. Add this to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "direnv export bash > \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ],
    "CwdChanged": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "direnv export bash > \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

Run `direnv allow` once in each directory that has an `.envrc` so direnv is permitted to load it. If you use devbox or nix instead of direnv, the same pattern works with `devbox shellenv` or `devbox global shellenv` in place of `direnv export bash`.

### React to specific files with `FileChanged`

To react to specific files instead of every directory change, use `FileChanged` with a `matcher` listing the filenames to watch, separated by `|`. To build the watch list, this value is split into literal filenames rather than evaluated as a regex. (The same value also filters which hook groups run when a file changes — see the [FileChanged reference](https://code.claude.com/docs/en/hooks).) This example watches `.envrc` and `.env` in the working directory:

```json
{
  "hooks": {
    "FileChanged": [
      {
        "matcher": ".envrc|.env",
        "hooks": [
          {
            "type": "command",
            "command": "direnv export bash > \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

See the `CwdChanged` and `FileChanged` reference entries for input schemas, `watchPaths` output, and `CLAUDE_ENV_FILE` details. For injecting context on every session start (rather than environment variables), consider [CLAUDE.md](https://code.claude.com/docs/en/memory) instead.

## Auto-approve specific permission prompts

Skip the approval dialog for tool calls you always allow. This example auto-approves `ExitPlanMode`, the tool Claude calls when it finishes presenting a plan and asks to proceed, so you aren't prompted every time a plan is ready.

Unlike the exit-code examples elsewhere, auto-approval requires your hook to write a JSON decision to stdout. A `PermissionRequest` hook fires when Claude Code is about to show a permission dialog, and returning `"behavior": "allow"` answers it on your behalf. The matcher scopes the hook to `ExitPlanMode` only, so no other prompts are affected. Add this to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"PermissionRequest\", \"decision\": {\"behavior\": \"allow\"}}}'"
          }
        ]
      }
    ]
  }
}
```

When the hook approves, Claude Code exits plan mode and restores whatever permission mode was active before you entered plan mode. The transcript shows "Allowed by PermissionRequest hook" where the dialog would have appeared. The hook path always keeps the current conversation: it cannot clear context and start a fresh implementation session the way the dialog can.

### Switch the session's permission mode with `setMode`

To set a specific permission mode instead, your hook's output can include an `updatedPermissions` array with a `setMode` entry. The `mode` value is any permission mode like `default`, `acceptEdits`, or `bypassPermissions`, and `destination: "session"` applies it for the current session only. To switch the session to `acceptEdits`, your hook writes this JSON to stdout:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedPermissions": [
        { "type": "setMode", "mode": "acceptEdits", "destination": "session" }
      ]
    }
  }
}
```

`bypassPermissions` only applies if the session was launched with bypass mode already available (`--dangerously-skip-permissions`, `--permission-mode bypassPermissions`, `--allow-dangerously-skip-permissions`, or `permissions.defaultMode: "bypassPermissions"` in settings, and not disabled by `permissions.disableBypassPermissionsMode`). It is never persisted as `defaultMode`. Permission rules and modes themselves are owned by the [permissions docs](https://code.claude.com/docs/en/permissions).

> **Keep the matcher as narrow as possible.** Matching on `.*` or leaving the matcher empty would auto-approve every permission prompt, including file writes and shell commands. See the [PermissionRequest reference](https://code.claude.com/docs/en/hooks) for the full set of decision fields.

**Source**: https://code.claude.com/docs/en/hooks-guide
**Last Updated**: 2026-06-13
**Status**: Active
