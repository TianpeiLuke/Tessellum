---
tags:
  - resource
  - documentation
  - hermes_agent
  - cli
  - sessions
keywords:
  - hermes cli session resume
  - continue resume session
  - state.db sqlite storage
  - inline context compression
  - background sessions daemon
  - non-blocking parallel tasks
topics:
  - Hermes Agent
  - CLI
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/cli
access_control_group: ["general"]
---

# Hermes Agent — CLI Session & Background Sessions

## Overview

This is the CLI-side session operations surface of the classic Hermes REPL: how to resume a prior conversation, where those conversations live on disk, the inline knobs that keep a long session inside its context window, and how to fork isolated work off into background daemon sessions. Resuming restores the full transcript from a SQLite `state.db` store; `/background` spawns a completely separate agent session that runs non-blocking while you keep using the foreground prompt. It complements the interactive REPL surface (keybindings, slash commands, status bar) covered in the sibling [CLI Interface](hermes_cli_interface.md) note, and the cross-platform session lifecycle covered in [Sessions — Lifecycle & Resume](hermes_sessions_lifecycle_resume.md).

## Session Management

### Resuming Sessions

When you exit a CLI session, a resume command is printed:

```
Resume this session with:
  hermes --resume 20260225_143052_a1b2c3

Session:        20260225_143052_a1b2c3
Duration:       12m 34s
Messages:       28 (5 user, 18 tool calls)
```

Resume options:

```bash
hermes --continue                          # Resume the most recent CLI session
hermes -c                                  # Short form
hermes -c "my project"                     # Resume a named session (latest in lineage)
hermes --resume 20260225_143052_a1b2c3     # Resume a specific session by ID
hermes --resume "refactoring auth"         # Resume by title
hermes -r 20260225_143052_a1b2c3           # Short form
```

Resuming restores the full conversation history from SQLite. The agent sees all previous messages, tool calls, and responses — just as if you never left.

Use `/title My Session Name` inside a chat to name the current session, or `hermes sessions rename <id> <title>` from the command line. Use `hermes sessions list` to browse past sessions. (The full `hermes sessions` command set and cross-platform `/handoff` live in [Sessions — Lifecycle & Resume](hermes_sessions_lifecycle_resume.md).)

### Session Storage

CLI sessions are stored in Hermes's SQLite state database under `~/.hermes/state.db`. The database keeps:

- session metadata (ID, title, timestamps, token counters)
- message history
- lineage across compressed/resumed sessions
- full-text search indexes used by `session_search`

Some messaging adapters also keep per-platform transcript files alongside the database, but the CLI itself resumes from the SQLite session store. (The `state.db` schema and the FTS5 `session_search` tool are documented in the model note [Session Search & Storage](hermes_session_search_storage.md).)

### Context Compression

Long conversations are automatically summarized when approaching context limits:

```yaml
# In ~/.hermes/config.yaml
compression:
  enabled: true
  threshold: 0.50    # Compress at 50% of context limit by default

# Summarization model configured under auxiliary:
auxiliary:
  compression:
    model: ""  # Leave empty to use the main chat model (default). Or pin a cheap fast model, e.g. "google/gemini-3-flash-preview".
```

When compression triggers, middle turns are summarized while the first 3 and last 20 turns are always preserved. (The full compression thresholds, summarizer-model requirement, and the pluggable context engine live in [Runtime & Context Settings](hermes_runtime_context_settings.md).)

## Background Sessions

Run a prompt in a separate background session while continuing to use the CLI for other work:

```
/background Analyze the logs in /var/log and summarize any errors from today
```

Hermes immediately confirms the task and gives you back the prompt:

```
🔄 Background task #1 started: "Analyze the logs in /var/log and summarize..."
   Task ID: bg_143022_a1b2c3
```

### How It Works

Each `/background` prompt spawns a **completely separate agent session** in a daemon thread:

- **Isolated conversation** — the background agent has no knowledge of your current session's history. It receives only the prompt you provide.
- **Same configuration** — the background agent inherits your model, provider, toolsets, reasoning settings, and fallback model from the current session.
- **Non-blocking** — your foreground session stays fully interactive. You can chat, run commands, or even start more background tasks.
- **Multiple tasks** — you can run several background tasks simultaneously. Each gets a numbered ID.

The `▶ N` element in the status bar tracks how many `/background` prompts are still in flight (see [CLI Interface — Status Bar](hermes_cli_interface.md)).

### Results

When a background task finishes, the result appears as a panel in your terminal:

```
╭─ ⚕ Hermes (background #1) ──────────────────────────────────╮
│ Found 3 errors in syslog from today:                         │
│ 1. OOM killer invoked at 03:22 — killed process nginx        │
│ 2. Disk I/O error on /dev/sda1 at 07:15                      │
│ 3. Failed SSH login attempts from 192.168.1.50 at 14:30      │
╰──────────────────────────────────────────────────────────────╯
```

If the task fails, you'll see an error notification instead. If `display.bell_on_complete` is enabled in your config, the terminal bell rings when the task finishes.

### Use Cases

- **Long-running research** — "/background research the latest developments in quantum error correction" while you work on code
- **File processing** — "/background analyze all Python files in this repo and list any security issues" while you continue a conversation
- **Parallel investigations** — start multiple background tasks to explore different angles simultaneously

Background sessions do not appear in your main conversation history. They are standalone sessions with their own task ID (e.g., `bg_143022_a1b2c3`).

**Source**: `inbox/hermes_agent_docs/user-guide/cli.md` · https://hermes-agent.nousresearch.com/docs/user-guide/cli
**Last Updated**: 2026-06-19
**Status**: Active
