---
tags:
  - resource
  - documentation
  - hermes_agent
  - sessions
  - cli
keywords:
  - session resume
  - hermes sessions commands
  - cross-platform handoff
  - session naming lineage
  - continue resume by title
  - conversation recap panel
topics:
  - Hermes Agent
  - Sessions
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/sessions
access_control_group: ["general"]
---

# Hermes Agent — Sessions: Lifecycle, Resume & Management

## Overview

This is the user-facing **session lifecycle procedure** for Hermes Agent: what a session is and what enters context on each turn, how to resume past conversations from the CLI (by id, title, or compression lineage), how to hand a live conversation off to a messaging platform, how sessions get titled, and the full `hermes sessions` command set. Hermes automatically saves every conversation — from the CLI or any of 20+ messaging platforms — as a session with full message history, enabling resume, search, and history management. This note covers the *procedural workflow*; the underlying data model (the `session_search` FTS5 tool, the gateway session-key scheme, the `state.db` schema, and expiry/cleanup) is documented in its sibling [hermes_session_search_storage](hermes_session_search_storage.md).

## How Sessions Work

Every conversation — whether from the CLI, Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Teams, or any other messaging platform — is stored as a session with full message history, tracked in a SQLite database (`~/.hermes/state.db`) with FTS5 full-text search. The database stores: session ID, source platform, user ID; the unique human-readable session title; model name and configuration; a system-prompt snapshot; full message history (role, content, tool calls, tool results); token counts (input/output); timestamps (started_at, ended_at); and the parent session ID used for compression-triggered session splitting. (The on-disk storage layout and DB schema are detailed in [hermes_session_search_storage](hermes_session_search_storage.md).)

### What Counts Toward Context

Hermes stores session history so it can resume conversations, but it does not re-send every byte it has ever handled. On each turn the model sees the selected system prompt, the current conversation window, and any content Hermes explicitly injects for that turn. Media attachments are handled as turn-scoped inputs:

- Images may be attached natively to the next model call, or pre-analyzed into a text description when the active model does not support native vision.
- Audio is transcribed into text when speech-to-text is configured.
- Text documents can have their extracted text included; other document types are usually represented by a saved local path and a short note.
- Attachment paths and extracted/derived text can appear in the transcript, but the raw image, audio, or binary file bytes are not repeatedly copied into future prompts.

For example, if a user sends an image and asks Hermes to make a meme from it, Hermes may inspect that image once with vision and run an image-processing script; future turns carry only what was written into the conversation (the request, a short image description, a local cache path, or the final response), not the original JPEG. The most common cause of context growth is not the media file but verbose text — pasted transcripts, full logs, large tool outputs, long diffs, repeated status reports, and proof dumps. The source recommends `/compress` when a session gets long, `/new` for a fresh thread (pass a name like `/new payments-refactor` to set the title up front), and `hermes sessions prune` only to delete old ended sessions. Compression reduces active context; it is not a privacy delete.

### Session Sources

Each session is tagged with its source platform. The source enumerates: `cli` (interactive CLI, `hermes` or `hermes chat`), `telegram`, `discord`, `slack`, `whatsapp`, `signal`, `matrix`, `mattermost`, `email` (IMAP/SMTP), `sms` (via Twilio), `dingtalk`, `feishu`, `wecom`, `weixin`, `bluebubbles` (Apple iMessage via BlueBubbles macOS server), `qqbot` (QQ Bot via Official API v2), `homeassistant`, `webhook`, `api-server`, `acp` (ACP editor integration), `cron` (scheduled cron jobs), and `batch` (batch processing runs).

## CLI Session Resume

Resume previous conversations from the CLI using `--continue` or `--resume`.

### Continue Last Session

```bash
# Resume the most recent CLI session
hermes --continue
hermes -c

# Or with the chat subcommand
hermes chat --continue
hermes chat -c
```

This looks up the most recent `cli` session from the SQLite database and loads its full conversation history.

### Resume by Name and by Specific Session

If a session has a title, you can resume it by name; if there are lineage variants, `-c "name"` automatically resumes the most recent one (`my project` → resumes `my project #3`). You can also resume a specific session by ID or by title:

```bash
# Resume a specific session by ID
hermes --resume 20250305_091523_a1b2c3d4
hermes -r 20250305_091523_a1b2c3d4

# Resume by title
hermes --resume "refactoring auth"
```

Session IDs are shown when you exit a CLI session, and can be found with `hermes sessions list`. Per the source, session IDs follow the format `YYYYMMDD_HHMMSS_<hex>` — CLI/TUI sessions use a 6-char hex suffix (e.g. `20250305_091523_a1b2c3`), gateway sessions use an 8-char suffix (e.g. `20250305_091523_a1b2c3d4`). You can resume by ID (full or unique prefix) or by title — both work with `-c` and `-r`.

### Conversation Recap on Resume

When you resume a session, Hermes displays a compact recap of the previous conversation in a styled panel before the input prompt. The recap: shows user messages (gold `●`) and assistant responses (green `◆`); truncates long messages (300 chars for user, 200 chars / 3 lines for assistant); collapses tool calls to a count with tool names (e.g. `[3 tool calls: terminal, web_search]`); hides system messages, tool results, and internal reasoning; caps at the last 10 exchanges with a "... N earlier messages ..." indicator; and uses dim styling to distinguish from the active conversation. To disable the recap and keep the minimal one-liner behavior, set in `~/.hermes/config.yaml`:

```yaml
display:
  resume_display: minimal   # default: full
```

## Cross-Platform Handoff

Use `/handoff <platform>` from a CLI session to transfer the live conversation to a messaging platform's home channel. The agent picks up exactly where the CLI left off — same session id, full role-aware transcript, tool calls and all.

```bash
# Inside a CLI session
/handoff telegram
```

What happens:

1. The CLI validates that `<platform>` is enabled and has a home channel set (run `/sethome` from the destination chat once to configure it).
2. The CLI marks the session pending and **block-polls the gateway**. It refuses if the agent is mid-turn — wait for the current response to finish first.
3. The gateway watcher claims the handoff and asks the destination adapter for a fresh thread:
   - **Telegram** — opens a new forum topic (DM topics if Bot API 9.4+ Topics mode is enabled in the chat, or a forum supergroup topic).
   - **Discord** — creates a 1440-min auto-archive thread under the home text channel.
   - **Slack** — posts a seed message and uses its `ts` as the thread anchor.
   - **WhatsApp / Signal / Matrix / SMS** — no native threads, falls back to the home channel directly.
4. The gateway re-binds the destination key to your existing CLI session id, then forges a synthetic user turn asking the agent to confirm and summarize. The reply lands in the new thread.
5. When the gateway acknowledges success, the CLI prints a `/resume` hint and exits cleanly (`↻ Handoff complete. The session is now active on telegram. Resume it on this CLI later with: /resume my-session-title`).
6. From that point the conversation lives on the platform; anyone authorized in that channel shares the same session, and any later real user message in the thread joins seamlessly because thread sessions key without `user_id`.

**Resume back to CLI:** run `/resume <title>` (or `hermes -r "<title>"` from the shell) to pick up where the platform left off.

**Failure modes:** no home channel → CLI refuses with a `/sethome` hint; platform not enabled / gateway not running → CLI times out at 60s with a clear message and the CLI session stays intact; thread creation fails (permissions, topics-mode off) → falls back to the home channel directly and still completes; `adapter.send` fails (rate limit, transient API error) → handoff marked failed with the reason and the row clears so you can retry. **Limitation:** for non-thread-capable platforms with multi-user group home channels, the synthetic turn keys as a DM-style session — fine for self-DM home channels (the typical setup), less ideal for genuinely shared group chats. Threading covers Telegram / Discord / Slack, the common case.

## Session Naming

Give sessions human-readable titles so you can find and resume them easily.

- **Auto-Generated Titles** — Hermes automatically generates a short descriptive title (3–7 words) for each session after the first exchange. This runs in a background thread using a fast auxiliary model, so it adds no latency; titles surface in `hermes sessions list`/`browse`. Auto-titling fires once per session and is skipped if you've set a title manually.
- **Setting a Title Manually** — use the `/title` slash command inside any chat session (CLI or gateway), e.g. `/title my research project`. Applied immediately; if the session isn't in the DB yet (you ran `/title` before your first message), it's queued and applied once the session starts. You can also rename from the command line: `hermes sessions rename 20250305_091523_a1b2c3d4 "refactoring auth module"`.
- **Title Rules** — Unique (no two sessions share a title); Max 100 characters; Sanitized (control chars, zero-width chars, RTL overrides stripped); Normal Unicode is fine (emoji, CJK, accented characters work).
- **Auto-Lineage on Compression** — when a session's context is compressed (via `/compress` or automatically), Hermes creates a new continuation session; if the original had a title, the new one gets a numbered title (`"my project" → "my project #2" → "my project #3"`). Resuming by name (`hermes -c "my project"`) automatically picks the most recent session in the lineage.
- **/title in Messaging Platforms** — works in all gateway platforms (Telegram, Discord, Slack, WhatsApp): `/title My Research` sets the title; bare `/title` shows the current title.

## Session Management Commands

Hermes provides a full set of session management commands via `hermes sessions`:

```bash
# List recent sessions (default: last 20), filter by platform, raise the limit
hermes sessions list
hermes sessions list --source telegram
hermes sessions list --limit 50

# Export all / per-platform / a single session to JSONL (one JSON object per line)
hermes sessions export backup.jsonl
hermes sessions export telegram-history.jsonl --source telegram
hermes sessions export session.jsonl --session-id 20250305_091523_a1b2c3d4

# Delete a specific session (confirmation, or --yes to skip)
hermes sessions delete 20250305_091523_a1b2c3d4
hermes sessions delete 20250305_091523_a1b2c3d4 --yes

# Set or change a session's title (multi-word titles don't need quotes in the CLI)
hermes sessions rename 20250305_091523_a1b2c3d4 "debugging auth flow"

# Prune ended sessions older than 90 days (default); custom age / per-platform / --yes
hermes sessions prune
hermes sessions prune --older-than 30
hermes sessions prune --source telegram --older-than 60

# Aggregate statistics
hermes sessions stats
```

When sessions have titles, `list` output shows titles, previews, and relative timestamps; when none have titles, a simpler preview/source/ID format is used. `rename` errors if the title is already in use by another session. **Pruning only deletes ended sessions** (explicitly ended or auto-reset) — active sessions are never pruned (the auto-prune `sessions.*` config and `VACUUM` reclamation are covered in [hermes_session_search_storage](hermes_session_search_storage.md)). `hermes sessions stats` reports total sessions, total messages, per-source session counts, and database size; for deeper analytics — token usage, cost estimates, tool breakdown, and activity patterns — use `hermes insights`.

**Source**: `inbox/hermes_agent_docs/user-guide/sessions.md`
**Last Updated**: 2026-06-19
**Status**: Active
