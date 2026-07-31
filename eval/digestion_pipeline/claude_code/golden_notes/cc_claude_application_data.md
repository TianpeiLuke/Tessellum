---
tags:
  - resource
  - documentation
  - claude_code
  - application_data
  - data_lifecycle
keywords:
  - application data
  - cleanupperioddays
  - session transcript jsonl
  - file-history snapshots
  - plaintext storage
  - claude project purge
  - history.jsonl
  - clear local data
topics:
  - Claude Code
  - Application Data
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/claude-directory
access_control_group: ["general"]
---

# Claude Code — Application Data Lifecycle

## Overview

Beyond the configuration files you author under `.claude/`, `~/.claude` also holds **data Claude Code writes during sessions**: conversation transcripts, prompt history, file snapshots, caches, and logs. This note covers the lifecycle of that application data — which paths are swept automatically on startup, which persist until you delete them, the plaintext-at-rest exposure they create, and how to clear local state per project with `claude project purge` or by hand.

All of this state is **plaintext**. Anything that passes through a tool lands in a transcript on disk: file contents, command output, pasted text. Managing this data is a procedure with three concerns — cleanup, exposure, and deletion — each handled below.

## Troubleshoot configuration

If a setting, hook, or file isn't taking effect, see [Debug your configuration](https://code.claude.com/docs/en/debug-your-config) for the inspection commands and a symptom-first lookup table.

## Cleaned up automatically

Files in the paths below are deleted on startup once they're older than [`cleanupPeriodDays`](https://code.claude.com/docs/en/settings#available-settings). **The default is 30 days.** Each path lives under `~/.claude/`:

- `projects/<project>/<session>.jsonl` — full conversation transcript: every message, tool call, and tool result.
- `projects/<project>/<session>/subagents/` — [subagent](https://code.claude.com/docs/en/sub-agents) conversation transcripts, removed with the parent session transcript when it ages out.
- `projects/<project>/<session>/tool-results/` — large tool outputs spilled to separate files.
- `file-history/<session>/` — pre-edit snapshots of files Claude changed, used for [checkpoint restore](cc_checkpointing.md).
- `plans/` — plan files written during [plan mode](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode).
- `debug/` — per-session debug logs, written only when you start with `--debug` or run `/debug`.
- `paste-cache/`, `image-cache/` — contents of large pastes and attached images.
- `session-env/` — per-session environment metadata.
- `tasks/` — per-session task lists written by the task tools.
- `shell-snapshots/` — captured shell environment used by the Bash tool. Removed on clean exit; the sweep clears any left after a crash.
- `backups/` — timestamped copies of `~/.claude.json` taken before config migrations.
- `feedback-bundles/` — redacted transcript archives written by `/feedback` on third-party providers, for sending to your Anthropic account team.
- `todos/`, `statsig/`, `logs/` — legacy directories from older versions. No longer written. The sweep removes their contents and then the empty directory.

## Kept until you delete them

The following paths are **not** covered by automatic cleanup and persist indefinitely (under `~/.claude/`):

- `history.jsonl` — every prompt you've typed, with timestamp and project path. Used for up-arrow recall.
- `stats-cache.json` — aggregated token and cost counts shown by `/usage`.
- `remote-settings.json` — cached copy of [server-managed settings](https://code.claude.com/docs/en/server-managed-settings) for your organization. Only present when your organization has configured them. Refreshed on each launch.

Other small cache and lock files appear depending on which features you use and are safe to delete.

## Plaintext storage

Transcripts and history are **not encrypted at rest**. OS file permissions are the only protection. If a tool reads a `.env` file or a command prints a credential, that value is written to `projects/<project>/<session>.jsonl`. To reduce exposure:

- Lower `cleanupPeriodDays` to shorten how long transcripts are kept.
- Set the [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](https://code.claude.com/docs/en/env-vars) environment variable to skip writing transcripts and prompt history in any mode. In non-interactive mode, you can instead pass `--no-session-persistence` alongside `-p`, or set `persistSession: false` in the Agent SDK.
- Use [permission rules](https://code.claude.com/docs/en/permissions) to deny reads of credential files.

## Clear local data

Run `claude project purge` to delete the state Claude Code holds for one project. The command requires Claude Code v2.1.124 or later. It deletes:

- Transcripts and auto memory under `projects/`
- Per-session `tasks/`, `debug/`, and `file-history/` entries
- Matching prompt lines in `history.jsonl`
- The project's entry in `~/.claude.json`

The command prints the full deletion plan and asks for confirmation before removing anything.

Preview the plan without deleting anything:

```bash
claude project purge ~/work/my-repo --dry-run
```

Delete with a single confirmation prompt (omit the path to pick a project from an interactive list):

```bash
claude project purge ~/work/my-repo
```

Skip the confirmation prompt for use in scripts:

```bash
claude project purge ~/work/my-repo --yes
```

Pass `--all` instead of a path to purge state for every project at once, which deletes `history.jsonl` outright rather than filtering it. Pass `-i` to step through the deletion plan one item at a time. The command leaves `shell-snapshots/` and `backups/` alone because those are not project-scoped, and warns about them in the plan output. It exits with status 1 if no state matches the given path.

### Manual deletion — what you lose

You can also delete any of the application-data paths by hand. New sessions are unaffected. The table shows what you lose for past sessions:

| Delete | You lose |
| --- | --- |
| `~/.claude/projects/` | Resume, continue, and rewind for past sessions |
| `~/.claude/history.jsonl` | Up-arrow prompt recall |
| `~/.claude/file-history/` | Checkpoint restore for past sessions |
| `~/.claude/stats-cache.json` | Historical totals shown by `/usage` |
| `~/.claude/remote-settings.json` | Nothing. Re-fetched on next launch. |
| `~/.claude/debug/`, `plans/`, `paste-cache/`, `image-cache/`, `session-env/`, `tasks/`, `shell-snapshots/`, `backups/` | Nothing user-facing |
| `~/.claude/todos/`, `statsig/`, `logs/` | Nothing. Legacy directories not written by current versions. |

Do **not** delete `~/.claude.json`, `~/.claude/settings.json`, or `~/.claude/plugins/`: those hold your auth, preferences, and installed plugins.

**Source**: https://code.claude.com/docs/en/claude-directory
**Last Updated**: 2026-06-13
**Status**: Active
