---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - transcripts
keywords:
  - openclaw transcripts
  - transcripts list show path
  - openclaw state directory transcripts
  - transcript.jsonl summary.md
  - transcripts list --json fields
  - date-qualified session selector
  - missing summaries summarize
  - transcripts.enabled autostart config
topics:
  - OpenClaw
  - CLI Transcripts
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/transcripts
access_control_group: ["general"]
---

# OpenClaw — The `openclaw transcripts` CLI Inspector

## Overview

This note documents the read-only `openclaw transcripts` command — the terminal inspector for transcripts written by OpenClaw's core `transcripts` tool. It mirrors the `cli/transcripts` source page: the on-disk state-directory artifact layout, the `list` / `show` / `path` commands (and their `--json` variants), the tab-separated and JSON output fields, per-day session grouping ("many meetings per day"), why summaries can be missing, and the opt-in `transcripts.enabled` / `transcripts.autoStart` configuration. The CLI is read-only: capture, import, and summarization are owned by the agent tool and configured auto-start sources, not by this command.

## State Directory Artifact Layout

Artifacts live under the OpenClaw state directory, grouped by the session start date and then by a session directory derived from the session id:

```text
$OPENCLAW_STATE_DIR/transcripts/YYYY-MM-DD/<session>/
  metadata.json
  transcript.jsonl
  summary.json
  summary.md
```

The default state directory is `~/.openclaw`; set `OPENCLAW_STATE_DIR` to use a different one. The date directory comes from the session start time, and the session directory is a safe filesystem segment derived from the session id. Each session directory holds four artifacts: `metadata.json` (session metadata), the append-only `transcript.jsonl` (the raw utterance log), `summary.json`, and `summary.md` (the human-readable Markdown summary).

## When to Use It

Use the CLI when you want to find yesterday's notes, open the Markdown file in an editor, feed a transcript to another tool, or debug where a session landed on disk. It does not start or stop capture — that is owned by the core `transcripts` agent tool and the configured auto-start sources.

## Commands

The command surface is three verbs — `list`, `show`, and `path` — each accepting a session selector and an optional `--json` flag; `path` additionally accepts artifact-selector flags:

```bash
openclaw transcripts list
openclaw transcripts show <session>
openclaw transcripts show YYYY-MM-DD/<session>
openclaw transcripts path <session>
openclaw transcripts path YYYY-MM-DD/<session>
openclaw transcripts path <session> --dir
openclaw transcripts path <session> --metadata
openclaw transcripts path <session> --transcript
openclaw transcripts list --json
openclaw transcripts show <session> --json
openclaw transcripts path <session> --json
```

The verbs and selectors do the following:

- `list` — list stored sessions, with the date-qualified selector, start time, title, and `summary.md` path.
- `show <session>` — print the stored `summary.md`.
- `path <session>` — print the `summary.md` path.
- `path <session> --dir` — print the session directory.
- `path <session> --metadata` — print `metadata.json`.
- `path <session> --transcript` — print `transcript.jsonl`.
- `--json` — print machine-readable output.

When a human session id repeats across days, use the date-qualified selector from `list`, for example `openclaw transcripts show 2026-05-22/standup`. Default session ids include a timestamp and random suffix; configure fixed session ids only when they are unique within the day.

## Output

`list` prints one session per line, tab-separated:

```text
2026-05-22/standup  2026-05-22T09:00:00.000Z  Weekly standup  /Users/alex/.openclaw/transcripts/2026-05-22/standup/summary.md
```

The columns are selector, start time, title, and summary path. The selector is the safest value to pass back to `show` or `path`.

`list --json` prints objects with the fields `sessionId`, `selector`, `date`, `title`, `startedAt`, `stoppedAt`, `source`, `path`, `summaryPath`, and `hasSummary`. `show --json` returns the stored session metadata, selector, session directory, summary path, and summary Markdown text. `path --json` returns the selected path and whether that file exists.

## Many Meetings Per Day

Transcripts groups sessions by date, then by session id, so ten meetings on one day become ten sibling folders:

```text
~/.openclaw/transcripts/2026-05-22/
  transcript-2026-05-22T09-00-00-000Z-a1b2c3d4/
  transcript-2026-05-22T10-30-00-000Z-b2c3d4e5/
  standup/
```

Use default generated ids for most automation. Use a fixed id such as `standup` only when the same id will not be used twice on the same date.

## Missing Summaries

Live sessions write `summary.md` when the session stops; imported transcripts write `summary.md` immediately after import. A session can still appear in `list` without a summary when capture is active, a provider failed during stop, or metadata was written before any utterances arrived. To recover, use `path <session> --transcript` to inspect the append-only transcript, and use the `transcripts` tool action `summarize` to regenerate the Markdown summary.

## Configuration

Transcript capture is opt-in because live sources can join and record meeting audio. Enable the tool with the top-level `transcripts.enabled` setting:

```json
{
  "transcripts": {
    "enabled": true,
    "maxUtterances": 2000
  }
}
```

Configure auto-start sources with `transcripts.autoStart` in `openclaw.json`. Each entry is enabled by being present; omit an entry to disable that source:

```json
{
  "transcripts": {
    "enabled": true,
    "autoStart": [
      {
        "providerId": "discord-voice",
        "guildId": "1234567890",
        "channelId": "2345678901"
      },
      {
        "providerId": "slack-huddle",
        "accountId": "workspace",
        "channelId": "C123"
      }
    ]
  }
}
```

**Source**: OpenClaw documentation — `cli/transcripts` (mirror `inbox/openclaw_docs/cli/transcripts.md`)
**Last Updated**: 2026-06-22
**Status**: Active
