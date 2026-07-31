---
tags:
  - resource
  - documentation
  - claude_code
  - statusline
  - data_contract
keywords:
  - status line json fields
  - json on stdin
  - context_window object
  - used_percentage formula
  - absent vs null fields
  - rate_limits effort thinking
  - current_usage cache tokens
  - claude code session data
topics:
  - Claude Code
  - Status Line
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/statusline
access_control_group: ["general"]
---

# Claude Code — Status Line JSON Fields

## Overview

The status line is driven by a **JSON-on-stdin data contract**: before each update, Claude Code serializes the current session state into a single JSON object and pipes it to your status-line script's stdin. Your script reads that object, extracts whatever fields it wants, and prints to stdout (see [Status Line Setup](cc_statusline_setup.md) for the wiring). This note catalogs the full field set, the `context_window` object semantics (including the input-only `used_percentage` formula), and the rules for when fields are **absent** versus **`null`** — the two distinct missing-data states your script must handle.

The fields are read-only session telemetry: model identity, working directory and workspace, cost, context-window usage, reasoning effort, rate limits, PR state, and worktree info. None of these consume API tokens to read; the status line runs locally.

## Field Catalog

Claude Code sends the following JSON fields to your script via stdin:

| Field | Description |
| --- | --- |
| `model.id`, `model.display_name` | Current model identifier and display name |
| `cwd`, `workspace.current_dir` | Current working directory. Both contain the same value; `workspace.current_dir` is preferred for consistency with `workspace.project_dir`. |
| `workspace.project_dir` | Directory where Claude Code was launched; may differ from `cwd` if the working directory changes during a session |
| `workspace.added_dirs` | Additional directories added via `/add-dir` or `--add-dir`. Empty array if none added |
| `workspace.git_worktree` | Git worktree name when the current directory is inside a linked worktree created with `git worktree add`. Absent in the main working tree. Populated for any git worktree, unlike `worktree.*` which applies only to `--worktree` sessions |
| `workspace.repo.host`, `.owner`, `.name` | Repository identity parsed from the `origin` remote (e.g. `"github.com"`, `"anthropics"`, `"claude-code"`). Absent outside a git repo or when no `origin` remote is configured |
| `cost.total_cost_usd` | Estimated session cost in USD, computed client-side. May differ from your actual bill |
| `cost.total_duration_ms` | Total wall-clock time since the session started, in milliseconds |
| `cost.total_api_duration_ms` | Total time spent waiting for API responses, in milliseconds |
| `cost.total_lines_added`, `.total_lines_removed` | Lines of code changed |
| `context_window.total_input_tokens`, `.total_output_tokens` | Token counts currently in the context window, from the most recent API response. Input includes cache reads and writes. Before v2.1.132 these were cumulative session totals |
| `context_window.context_window_size` | Maximum context window size in tokens. 200000 by default, or 1000000 for models with extended context |
| `context_window.used_percentage` | Pre-calculated percentage of context window used |
| `context_window.remaining_percentage` | Pre-calculated percentage of context window remaining |
| `context_window.current_usage` | Token counts from the last API call (see Context Window Fields below) |
| `exceeds_200k_tokens` | Whether the combined input, cache, and output token count from the most recent response exceeds 200k. A fixed threshold regardless of actual window size |
| `effort.level` | Current reasoning effort (`low`, `medium`, `high`, `xhigh`, or `max`). Reflects live session value incl. mid-session `/effort` changes. Ultracode is not a distinct level and reports as `xhigh`. Absent when the model does not support the effort parameter |
| `thinking.enabled` | Whether extended thinking is enabled for the session |
| `rate_limits.five_hour.used_percentage`, `.seven_day.used_percentage` | Percentage of the 5-hour or 7-day rate limit consumed, from 0 to 100 |
| `rate_limits.five_hour.resets_at`, `.seven_day.resets_at` | Unix epoch seconds when the 5-hour or 7-day rate limit window resets |
| `session_id` | Unique session identifier |
| `session_name` | Custom session name set with `--name` or `/rename`. Absent if no custom name set |
| `transcript_path` | Path to conversation transcript file |
| `version` | Claude Code version |
| `output_style.name` | Name of the current output style |
| `vim.mode` | Current vim mode (`NORMAL`, `INSERT`, `VISUAL`, or `VISUAL LINE`) when vim mode is enabled |
| `agent.name` | Agent name when running with the `--agent` flag or agent settings configured |
| `pr.number`, `pr.url` | Open PR for the current branch. Mirrors the PR badge in the status bar. Absent until a PR is found, when not in a git repo, or once the PR merges or closes |
| `pr.review_state` | Review status: `approved`, `pending`, `changes_requested`, or `draft`. May be independently absent even when `pr` is present |
| `worktree.name` | Name of the active worktree. Present only during `--worktree` sessions |
| `worktree.path` | Absolute path to the worktree directory |
| `worktree.branch` | Git branch name for the worktree (e.g. `"worktree-my-feature"`). Absent for hook-based worktrees |
| `worktree.original_cwd` | Directory Claude was in before entering the worktree |
| `worktree.original_branch` | Branch checked out before entering the worktree. Absent for hook-based worktrees |

The full JSON structure delivered on stdin:

```json
{
  "cwd": "/current/working/directory",
  "session_id": "abc123...",
  "session_name": "my-session",
  "transcript_path": "/path/to/transcript.jsonl",
  "model": {
    "id": "claude-opus-4-8",
    "display_name": "Opus"
  },
  "workspace": {
    "current_dir": "/current/working/directory",
    "project_dir": "/original/project/directory",
    "added_dirs": [],
    "git_worktree": "feature-xyz",
    "repo": {
      "host": "github.com",
      "owner": "anthropics",
      "name": "claude-code"
    }
  },
  "version": "2.1.90",
  "output_style": {
    "name": "default"
  },
  "cost": {
    "total_cost_usd": 0.01234,
    "total_duration_ms": 45000,
    "total_api_duration_ms": 2300,
    "total_lines_added": 156,
    "total_lines_removed": 23
  },
  "context_window": {
    "total_input_tokens": 15500,
    "total_output_tokens": 1200,
    "context_window_size": 200000,
    "used_percentage": 8,
    "remaining_percentage": 92,
    "current_usage": {
      "input_tokens": 8500,
      "output_tokens": 1200,
      "cache_creation_input_tokens": 5000,
      "cache_read_input_tokens": 2000
    }
  },
  "exceeds_200k_tokens": false,
  "effort": {
    "level": "high"
  },
  "thinking": {
    "enabled": true
  },
  "rate_limits": {
    "five_hour": {
      "used_percentage": 23.5,
      "resets_at": 1738425600
    },
    "seven_day": {
      "used_percentage": 41.2,
      "resets_at": 1738857600
    }
  },
  "vim": {
    "mode": "NORMAL"
  },
  "agent": {
    "name": "security-reviewer"
  },
  "pr": {
    "number": 1234,
    "url": "https://github.com/anthropics/claude-code/pull/1234",
    "review_state": "pending"
  },
  "worktree": {
    "name": "my-feature",
    "path": "/path/to/.claude/worktrees/my-feature",
    "branch": "worktree-my-feature",
    "original_cwd": "/path/to/project",
    "original_branch": "main"
  }
}
```

## Absent vs. Null Fields

The contract distinguishes two missing-data states. **Absent** means the key is not present in the JSON at all (handle with conditional access); **`null`** means the key exists but has no value yet (handle with fallback defaults like `// 0` in jq).

**Fields that may be absent**:

- `session_name` — appears only when a custom name has been set with `--name` or `/rename`
- `workspace.git_worktree` — appears only inside a linked git worktree
- `workspace.repo` — appears only inside a git repo with an `origin` remote configured
- `effort` — appears only when the current model supports the reasoning effort parameter
- `vim` — appears only when vim mode is enabled
- `agent` — appears only with the `--agent` flag or agent settings configured
- `pr` — appears only while an open PR is found for the current branch; removed once the PR merges or closes. `pr.review_state` may be independently absent
- `worktree` — appears only during `--worktree` sessions; when present, `branch` and `original_branch` may also be absent for hook-based worktrees
- `rate_limits` — appears only for Claude.ai subscribers (Pro/Max) after the first API response in the session. Each window (`five_hour`, `seven_day`) may be independently absent. Use `jq -r '.rate_limits.five_hour.used_percentage // empty'` to handle absence gracefully

**Fields that may be `null`**:

- `context_window.current_usage` — `null` before the first API call in a session, and again after `/compact` until the next API call repopulates it
- `context_window.used_percentage`, `.remaining_percentage` — may be `null` early in the session

A defensive jq read combines both: provide a fallback so a `null` becomes a usable value, and let absence yield nothing.

```bash
# // 0 turns a null used_percentage into 0; // empty drops an absent field entirely
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0')
FIVE_H=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
```

## Context Window Fields

The `context_window` object describes the live context window from the most recent API response. As of v2.1.132, `total_input_tokens` and `total_output_tokens` reflect current context usage, not cumulative session totals.

- **Combined totals** (`total_input_tokens`, `total_output_tokens`): tokens currently in the context window. `total_input_tokens` is the sum of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`; `total_output_tokens` is the output tokens from the most recent response. Both are `0` before the first API response.
- **Per-component usage** (`current_usage`): the same token counts broken out by category — use this when you need cache hits separate from fresh input. The object contains `input_tokens` (input tokens in current context), `output_tokens` (output tokens generated), `cache_creation_input_tokens` (tokens written to cache), and `cache_read_input_tokens` (tokens read from cache). For what the cache fields mean and how they are billed, see [check cache performance](https://code.claude.com/docs/en/prompt-caching#check-cache-performance).

The `used_percentage` field is calculated from **input tokens only**:

```
used_percentage  ←  input_tokens + cache_creation_input_tokens + cache_read_input_tokens
```

It does **not** include `output_tokens`. If you calculate context percentage manually from `current_usage`, use this same input-only formula to match `used_percentage`. The `current_usage` object is `null` before the first API call in a session, and again immediately after `/compact` until the next API call repopulates it.

**Source**: https://code.claude.com/docs/en/statusline
**Last Updated**: 2026-06-13
**Status**: Active
